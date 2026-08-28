"""
Command-line interface for the Autonomous AI Code Review Agent.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from src.agent.review_agent import ReviewAgent
from src.models.review import Severity, Verdict

def get_git_diff_files(base_ref: str = "origin/main") -> list[str]:
    """Gets list of modified files compared to base ref."""
    try:
        cmd = ["git", "diff", "--name-only", f"{base_ref}...HEAD"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            # Fallback to local main or direct diff
            cmd = ["git", "diff", "--name-only", "main...HEAD"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
        return files
    except Exception:
        return []

import json
from src.tools.diff_parser import DiffParser
from src.tools.github_publisher import GitHubReviewPublisher

def get_git_diff_text(base_ref: str = "origin/main") -> str:
    """Gets unified git diff text compared to base ref."""
    try:
        cmd = ["git", "diff", f"{base_ref}...HEAD"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0 or not res.stdout.strip():
            cmd = ["git", "diff", "main...HEAD"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return res.stdout
    except Exception:
        return ""

def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Code Review & Security Auditor Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Review single file command
    review_parser = subparsers.add_parser("review", help="Review a file or diff snippet")
    review_parser.add_argument("target", help="Path to file or diff to review")
    review_parser.add_argument("--spec", help="Path to spec.md file for compliance check", default=None)
    review_parser.add_argument("--output", help="Path to output markdown report", default=None)

    # 2. Review PR diff command
    review_pr_parser = subparsers.add_parser("review-pr", help="Review entire PR diff against base branch")
    review_pr_parser.add_argument("--base", help="Base branch (default: origin/main)", default="origin/main")
    review_pr_parser.add_argument("--files", nargs="*", help="Explicit list of files to review", default=None)
    review_pr_parser.add_argument("--spec", help="Path to spec.md file", default=None)
    review_pr_parser.add_argument("--output", help="Path to output markdown report", default=None)
    review_pr_parser.add_argument("--inline-json", help="Path to output GitHub PR review JSON payload", default=None)
    review_pr_parser.add_argument("--use-gemini", action="store_true", help="Enable semantic review with Gemini 3.7 Flash")
    review_pr_parser.add_argument("--model", help="Gemini model name (default: gemini-3.7-flash)", default="gemini-3.7-flash")

    args = parser.parse_args()

    model_name = getattr(args, "model", "gemini-3.7-flash")
    agent = ReviewAgent(model=model_name)
    spec_content = ""
    if args.spec:
        spec_path = Path(args.spec)
        if spec_path.exists():
            spec_content = spec_path.read_text(encoding="utf-8")

    if args.command == "review":
        target_path = Path(args.target)
        if not target_path.exists():
            print(f"❌ Error: File '{args.target}' does not exist.")
            sys.exit(2)

        code_content = target_path.read_text(encoding="utf-8")
        report = agent.review_code(
            code_content=code_content,
            file_path=str(target_path),
            spec_content=spec_content,
        )

    elif args.command == "review-pr":
        diff_text = get_git_diff_text(base_ref=args.base)
        if args.files:
            target_files = args.files
        else:
            target_files = get_git_diff_files(base_ref=args.base)

        # Filter for source code files
        code_files = [f for f in target_files if f.startswith("src/") or f.endswith(".py") or f.endswith(".ts") or f.endswith(".js") or f.endswith(".go")]

        if not code_files and not diff_text.strip():
            from src.models.review import ReviewReport
            report = ReviewReport(
                target_name="PR Diff (Non-code files)",
                verdict=Verdict.PASS,
                findings=[],
                summary="Review PASSED: No source code modifications detected in this PR.",
            )
        else:
            # Pass 1: Deterministic file analysis
            report = agent.review_files(
                file_paths=code_files,
                spec_content=spec_content,
            )

            # Pass 2: Optional Gemini 3.7 Flash semantic analysis
            if args.use_gemini and agent.gemini_reviewer.is_available() and diff_text.strip():
                review_policy = ""
                policy_file = Path("REVIEW.md")
                if policy_file.exists():
                    review_policy = policy_file.read_text(encoding="utf-8")

                gemini_report = agent.gemini_reviewer.review_diff(
                    diff_text=diff_text,
                    review_policy=review_policy,
                    spec_content=spec_content,
                )
                if gemini_report and gemini_report.findings:
                    report.findings.extend(gemini_report.findings)
                    # Recompute verdict if gemini found blockers
                    if any(f.severity == Severity.BLOCKER for f in gemini_report.findings):
                        report.verdict = Verdict.BLOCKED
                    elif any(f.severity == Severity.IMPORTANT for f in gemini_report.findings) and report.verdict == Verdict.PASS:
                        report.verdict = Verdict.CHANGES_REQUESTED

        # If --inline-json requested, format and write GitHub PR Review payload
        if args.inline_json:
            diff_parser = DiffParser(diff_text)
            publisher = GitHubReviewPublisher()
            payload = publisher.build_review_payload(report=report, diff_parser=diff_parser)
            out_json = Path(args.inline_json)
            out_json.parent.mkdir(parents=True, exist_ok=True)
            out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"📦 Inline review payload written to: {out_json}")

    md_output = agent.render_markdown(report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_output, encoding="utf-8")
        print(f"📄 Audit report written to: {out_path}")
    else:
        print(md_output)

    # Exit code: 0 if PASS, 1 if CHANGES_REQUESTED or BLOCKED
    if report.verdict == Verdict.PASS:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
