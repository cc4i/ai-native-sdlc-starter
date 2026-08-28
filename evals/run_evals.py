#!/usr/bin/env python3
"""
Continuous AI Evaluation Runner for AI-Native SDLC Starter.
Validates skills, rules, templates, and agent directives against regression tests.
"""

import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.agent.review_agent import ReviewAgent
from src.models.review import Verdict

def load_eval_config(config_path: Path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_eval_case(eval_case: dict, root_dir: Path) -> tuple[bool, list[str]]:
    errors = []
    eval_id = eval_case.get("id")
    eval_type = eval_case.get("type", "static")

    if eval_type == "functional":
        # Run live agent review eval
        agent = ReviewAgent()
        snippet = eval_case.get("input_snippet", "")
        expected_verdict = eval_case.get("expected_verdict", "PASS")
        report = agent.review_code(snippet, file_path="eval_snippet.py")
        if report.verdict.value != expected_verdict:
            errors.append(f"Expected verdict '{expected_verdict}', but got '{report.verdict.value}'")
        return len(errors) == 0, errors

    # Static structural evals
    templates_dir = root_dir / "docs" / "templates"
    if not templates_dir.exists():
        templates_dir = root_dir / "templates"

    if "intent" in eval_id:
        target_file = templates_dir / "intent.template.md"
    elif "spec" in eval_id:
        target_file = templates_dir / "spec.template.md"
    elif "plan" in eval_id:
        target_file = templates_dir / "plan.template.md"
    else:
        target_file = root_dir / "GEMINI.md"

    if not target_file.exists():
        errors.append(f"Target file {target_file} not found")
        return False, errors

    content = target_file.read_text(encoding="utf-8")

    # Verify required sections
    for section in eval_case.get("required_sections", []):
        if section.lower() not in content.lower():
            errors.append(f"Missing required section: '{section}' in {target_file.name}")

    return len(errors) == 0, errors

def main():
    config_file = root_dir / "evals" / "eval-config.json"

    if not config_file.exists():
        print(f"❌ Error: {config_file} not found.")
        sys.exit(1)

    config = load_eval_config(config_file)
    evals = config.get("evals", [])

    print("==================================================")
    print("🤖 [AI Evals] Running Continuous Evaluation Suite...")
    print("==================================================")

    passed_count = 0
    failed_count = 0

    for idx, case in enumerate(evals, 1):
        name = case.get("name", case.get("id"))
        success, errors = run_eval_case(case, root_dir)
        if success:
            print(f"  [{idx}/{len(evals)}] PASS: {name}")
            passed_count += 1
        else:
            print(f"  [{idx}/{len(evals)}] FAIL: {name}")
            for err in errors:
                print(f"       - {err}")
            failed_count += 1

    print("==================================================")
    print(f"📊 Summary: {passed_count} Passed, {failed_count} Failed.")
    print("==================================================")

    if failed_count > 0:
        sys.exit(1)
    else:
        print("✅ All AI regression evaluations passed successfully.")

if __name__ == "__main__":
    main()
