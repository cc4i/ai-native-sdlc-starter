"""
Command-line interface for the Autonomous AI Code Review Agent.
"""

import argparse
import sys
from pathlib import Path
from src.agent.review_agent import ReviewAgent
from src.models.review import Verdict

def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Code Review & Security Auditor Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Review command
    review_parser = subparsers.add_parser("review", help="Review a file or diff")
    review_parser.add_argument("target", help="Path to file or diff to review")
    review_parser.add_argument("--spec", help="Path to spec.md file for compliance check", default=None)
    review_parser.add_argument("--output", help="Path to output markdown report", default=None)

    args = parser.parse_args()

    if args.command == "review":
        target_path = Path(args.target)
        if not target_path.exists():
            print(f"❌ Error: File '{args.target}' does not exist.")
            sys.exit(2)

        code_content = target_path.read_text(encoding="utf-8")
        spec_content = ""
        if args.spec:
            spec_path = Path(args.spec)
            if spec_path.exists():
                spec_content = spec_path.read_text(encoding="utf-8")

        agent = ReviewAgent()
        report = agent.review_code(
            code_content=code_content,
            file_path=str(target_path),
            spec_content=spec_content,
        )

        md_output = agent.render_markdown(report)

        if args.output:
            out_path = Path(args.output)
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
