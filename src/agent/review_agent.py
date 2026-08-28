"""
ReviewAgent - Autonomous multi-pass code review orchestrator.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from src.agent.gemini_reviewer import GeminiReviewer
from src.models.review import Finding, ReviewReport, Severity, Verdict
from src.tools.ast_checker import AstSecurityCheckerTool
from src.tools.secret_scanner import SecretScannerTool
from src.tools.spec_matcher import SpecComplianceTool


class ReviewAgent:
    """Orchestrates security, AST, spec compliance, and Gemini 3.7 Flash semantic tools to produce code review audits."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        self.secret_scanner = SecretScannerTool()
        self.ast_checker = AstSecurityCheckerTool()
        self.spec_matcher = SpecComplianceTool()
        self.gemini_reviewer = GeminiReviewer(model=model, api_key=api_key)

    def review_code(
        self,
        code_content: str,
        file_path: str = "diff.patch",
        spec_content: str = "",
    ) -> ReviewReport:
        findings: List[Finding] = []

        # Pass 1: Secret & Credential Scanning
        findings.extend(self.secret_scanner.scan(code_content, file_path=file_path))

        # Pass 2: AST Security & Anti-Pattern Analysis
        findings.extend(self.ast_checker.scan(code_content, file_path=file_path))

        # Pass 3: Spec Acceptance Compliance
        if spec_content:
            findings.extend(
                self.spec_matcher.scan(code_content, spec_content=spec_content, file_path=file_path)
            )

        # Compute Overall Verdict
        if any(f.severity == Severity.BLOCKER for f in findings):
            verdict = Verdict.BLOCKED
            summary = f"Review BLOCKED: Found {sum(1 for f in findings if f.severity == Severity.BLOCKER)} blocker issue(s)."
        elif any(f.severity == Severity.IMPORTANT for f in findings):
            verdict = Verdict.CHANGES_REQUESTED
            summary = f"Changes Requested: Found {sum(1 for f in findings if f.severity == Severity.IMPORTANT)} important issue(s)."
        else:
            verdict = Verdict.PASS
            summary = "Review PASSED: Zero blockers or security issues detected."

        return ReviewReport(
            target_name=file_path,
            verdict=verdict,
            findings=findings,
            summary=summary,
        )

    def review_files(
        self,
        file_paths: List[str],
        base_dir: str = ".",
        spec_content: str = "",
    ) -> ReviewReport:
        """Reviews multiple files and aggregates findings into a single PR review report."""
        all_findings: List[Finding] = []
        valid_files_count = 0

        for f in file_paths:
            path = Path(base_dir) / f if not Path(f).is_absolute() else Path(f)
            if path.exists() and path.is_file():
                valid_files_count += 1
                try:
                    content = path.read_text(encoding="utf-8")
                    sub_report = self.review_code(
                        code_content=content,
                        file_path=f,
                        spec_content=spec_content,
                    )
                    all_findings.extend(sub_report.findings)
                except OSError, UnicodeDecodeError:
                    continue

        # Compute Overall Verdict
        if any(f.severity == Severity.BLOCKER for f in all_findings):
            verdict = Verdict.BLOCKED
            summary = f"Review BLOCKED: Found {sum(1 for f in all_findings if f.severity == Severity.BLOCKER)} blocker issue(s) across {valid_files_count} file(s)."
        elif any(f.severity == Severity.IMPORTANT for f in all_findings):
            verdict = Verdict.CHANGES_REQUESTED
            summary = f"Changes Requested: Found {sum(1 for f in all_findings if f.severity == Severity.IMPORTANT)} important issue(s) across {valid_files_count} file(s)."
        else:
            verdict = Verdict.PASS
            summary = f"Review PASSED: Zero blockers or security issues detected across {valid_files_count} file(s)."

        target_desc = (
            f"PR Changes ({valid_files_count} files)"
            if valid_files_count > 1
            else (file_paths[0] if file_paths else "PR Diff")
        )
        return ReviewReport(
            target_name=target_desc,
            verdict=verdict,
            findings=all_findings,
            summary=summary,
        )

    def render_markdown(self, report: ReviewReport) -> str:
        blockers = [f for f in report.findings if f.severity == Severity.BLOCKER]
        importants = [f for f in report.findings if f.severity == Severity.IMPORTANT]
        nits = [f for f in report.findings if f.severity == Severity.NIT]

        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            "# PR Review Audit Report",
            "",
            f"**Target**: `{report.target_name}`  ",
            "**Reviewer**: Autonomous Antigravity ReviewAgent  ",
            f"**Date**: {date_str}  ",
            f"**Verdict**: `{report.verdict.value}`  ",
            "",
            "---",
            "",
            "## 1. Executive Summary",
            report.summary,
            "",
            "## 2. Findings by Severity Tier",
            "",
            f"### 🚨 Tier 1: Blocker ({len(blockers)} found)",
        ]

        if blockers:
            for b in blockers:
                loc = f" (`{b.file_path}:{b.line_number}`)" if b.line_number else ""
                lines.append(f"- **[{b.rule_id}] {b.title}**{loc}: {b.message}")
                if b.suggestion and b.suggestion.strip():
                    lines.append(f"  ```suggestion\n  {b.suggestion.strip()}\n  ```")
        else:
            lines.append("*None.*")

        lines.extend(
            [
                "",
                f"### ⚠️ Tier 2: Important ({len(importants)} found)",
            ]
        )

        if importants:
            for imp in importants:
                loc = f" (`{imp.file_path}:{imp.line_number}`)" if imp.line_number else ""
                lines.append(f"- **[{imp.rule_id}] {imp.title}**{loc}: {imp.message}")
                if imp.suggestion and imp.suggestion.strip():
                    lines.append(f"  ```suggestion\n  {imp.suggestion.strip()}\n  ```")
        else:
            lines.append("*None.*")

        capped_nits = nits[:5]
        lines.extend(
            [
                "",
                f"### 💡 Tier 3: Nit / Suggestions ({len(capped_nits)} shown, cap 5)",
            ]
        )

        if capped_nits:
            for nit in capped_nits:
                loc = f" (`{nit.file_path}:{nit.line_number}`)" if nit.line_number else ""
                lines.append(f"- {nit.title}{loc}: {nit.message}")
                if nit.suggestion and nit.suggestion.strip():
                    lines.append(f"  ```suggestion\n  {nit.suggestion.strip()}\n  ```")
        else:
            lines.append("*None.*")

        tally_line = (
            f"Important: {len(blockers)}, Consider: {len(importants)}, Nit: {len(capped_nits)}"
        )

        lines.extend(
            [
                "",
                "---",
                "## 3. Governance Sign-Off",
                f"- **Automated Verification**: {report.verdict.value}",
                "- **Human Code Owner Sign-Off**: [ ] Required for Blocker / Production Releases",
                f"- **Severity Tally**: `{tally_line}`",
                "",
                f"*{tally_line}*",
                "",
            ]
        )

        return "\n".join(lines)
