#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

def main():
    config_file = root_dir / "evals" / "eval-config.json"
    if not config_file.exists():
        print("❌ Error: evals/eval-config.json not found.")
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    evals = config.get("evals", [])
    print("==================================================")
    print("🤖 [AI Evals] Running Continuous Evaluation Suite...")
    print("==================================================")

    passed = 0
    failed = 0
    templates_dir = root_dir / "docs" / "templates"
    if not templates_dir.exists():
        templates_dir = root_dir / "templates"

    for idx, case in enumerate(evals, 1):
        name = case.get("name", case.get("id"))
        eval_id = case.get("id", "")
        if "intent" in eval_id:
            target = templates_dir / "intent.template.md"
        elif "spec" in eval_id:
            target = templates_dir / "spec.template.md"
        elif "plan" in eval_id:
            target = templates_dir / "plan.template.md"
        else:
            target = root_dir / "GEMINI.md"

        if not target.exists():
            print(f"  [{idx}/{len(evals)}] FAIL: {name} (Missing {target.name})")
            failed += 1
            continue

        content = target.read_text(encoding="utf-8").lower()
        missing = [sec for sec in case.get("required_sections", []) if sec.lower() not in content]

        if not missing:
            print(f"  [{idx}/{len(evals)}] PASS: {name}")
            passed += 1
        else:
            print(f"  [{idx}/{len(evals)}] FAIL: {name} (Missing sections: {missing})")
            failed += 1

    print("==================================================")
    print(f"📊 Summary: {passed} Passed, {failed} Failed.")
    print("==================================================")
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
