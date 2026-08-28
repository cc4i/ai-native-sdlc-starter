#!/usr/bin/env python3
"""
Autonomous Agent Lifecycle Guard Hook (PreToolUse & Stop).
Intercepts tool executions and completion attempts to enforce non-negotiable SDLC safety rules.
"""

import json
import re
import sys
from typing import Any, Dict

# Regex patterns matching dangerous git commands
GIT_ADD_ALL = re.compile(r"\bgit\s+add\s+([^|;&\n]*\s+)?(-A|-u|--all|--update|\.)(\s|[;&|]|$)")
GIT_COMMIT_ALL = re.compile(
    r"\bgit\s+commit\s+([^|;&\n]*\s+)?(--all|-[a-zA-Z]*a[a-zA-Z]*)(\s|[=;&|]|$)"
)


def evaluate_pre_tool_use(payload: Dict[str, Any]) -> Dict[str, Any]:
    tool_call = payload.get("toolCall", {})
    name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    if name == "run_command":
        cmd = args.get("CommandLine", "").strip()

        # Rule 1: No staging the whole working tree with git add -A / .
        if GIT_ADD_ALL.search(cmd):
            return {
                "decision": "deny",
                "reason": (
                    "SDLC Policy Violation: 'git add -A' / '.' / '--all' is forbidden. "
                    "Stage only the specific files you authored or modified explicitly."
                ),
            }

        # Rule 2: No committing all unstaged changes with git commit -a / -am
        if GIT_COMMIT_ALL.search(cmd):
            return {
                "decision": "deny",
                "reason": (
                    "SDLC Policy Violation: 'git commit -a' / '-am' is forbidden. "
                    "Inspect staged changes with 'git diff --cached' and stage explicitly."
                ),
            }

    return {"decision": "allow"}


def evaluate_stop(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Stop hook allows clean exit by default unless conditions fail
    return {"decision": "allow"}


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw)
        if "toolCall" in payload:
            res = evaluate_pre_tool_use(payload)
        elif "terminationReason" in payload:
            res = evaluate_stop(payload)
        else:
            res = {"decision": "allow"}

        print(json.dumps(res))
    except Exception as e:
        # Fall open with warning to avoid deadlocking agent loops
        print(json.dumps({"decision": "allow", "reason": f"Hook error fallback: {e}"}))


if __name__ == "__main__":
    main()
