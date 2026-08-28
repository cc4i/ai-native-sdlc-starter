"""
GitHub Pull Request Review Publisher & Formatter.
Constructs batch inline comments and summary payloads for GitHub's Pull Request Review API.
"""

from typing import Any, Dict, List, Optional

from src.models.review import Finding, ReviewReport, Severity
from src.tools.diff_parser import DiffParser


class GitHubReviewPublisher:
    """Formats review findings into GitHub PR Review payloads with inline comments."""

    def __init__(self, nit_cap: int = 5):
        self.nit_cap = nit_cap

    def calculate_tally(self, findings: List[Finding]) -> Dict[str, int]:
        """
        Calculates the standardized machine-readable severity tally:
        - Important (Blocker / Critical)
        - Consider (Important / Architectural)
        - Nit (Style / Minor, capped at nit_cap)
        """
        important_count = 0
        consider_count = 0
        nit_count = 0

        for f in findings:
            if f.severity == Severity.BLOCKER:
                important_count += 1
            elif f.severity == Severity.IMPORTANT:
                consider_count += 1
            elif f.severity == Severity.NIT:
                nit_count += 1

        capped_nits = min(nit_count, self.nit_cap)
        return {
            "important": important_count,
            "consider": consider_count,
            "nit": capped_nits,
        }

    def format_tally_line(self, findings: List[Finding]) -> str:
        """Returns the machine-readable tally line: Important: n, Consider: n, Nit: n"""
        t = self.calculate_tally(findings)
        return f"Important: {t['important']}, Consider: {t['consider']}, Nit: {t['nit']}"

    def build_inline_comment_body(self, finding: Finding) -> str:
        """Formats an inline diff review comment with optional 1-click suggestion block."""
        badge = (
            "🚨 Important"
            if finding.severity == Severity.BLOCKER
            else ("⚠️ Consider" if finding.severity == Severity.IMPORTANT else "💡 Nit")
        )
        body = f"### {badge}: {finding.title}\n\n{finding.message}"
        if finding.rule_id:
            body += f"\n\n*Rule: `{finding.rule_id}`*"

        if finding.suggestion and finding.suggestion.strip():
            body += f"\n\n```suggestion\n{finding.suggestion.strip()}\n```"

        return body

    def build_review_payload(
        self,
        report: ReviewReport,
        diff_parser: DiffParser,
        commit_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Constructs a payload suitable for:
        POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
        """
        inline_findings, summary_findings = diff_parser.partition_findings(report.findings)

        comments: List[Dict[str, Any]] = []
        for f in inline_findings:
            comments.append(
                {
                    "path": f.file_path.lstrip("./"),
                    "line": f.line_number,
                    "side": "RIGHT",
                    "body": self.build_inline_comment_body(f),
                }
            )

        # Build main review body
        tally_line = self.format_tally_line(report.findings)
        body_lines = [
            "# PR Review Audit Report",
            "",
            f"**Target**: `{report.target_name}`",
            f"**Verdict**: `{report.verdict.value}`",
            f"**Tally**: `{tally_line}`",
            "",
            f"{report.summary or 'Automated AI Code Review completed.'}",
            "",
        ]

        if summary_findings:
            body_lines.append("## Additional Findings (File / Global Scope)")
            for sf in summary_findings:
                sev_icon = (
                    "🚨"
                    if sf.severity == Severity.BLOCKER
                    else ("⚠️" if sf.severity == Severity.IMPORTANT else "💡")
                )
                loc = (
                    f" (`{sf.file_path}:{sf.line_number}`)"
                    if sf.line_number
                    else f" (`{sf.file_path}`)"
                )
                body_lines.append(f"- {sev_icon} **{sf.title}**{loc}: {sf.message}")
            body_lines.append("")

        body_lines.append("---")
        body_lines.append(f"*{tally_line}*")

        payload: Dict[str, Any] = {
            "body": "\n".join(body_lines),
            "event": "COMMENT",  # Strictly advisory, human decides merge
            "comments": comments,
        }

        if commit_id:
            payload["commit_id"] = commit_id

        return payload
