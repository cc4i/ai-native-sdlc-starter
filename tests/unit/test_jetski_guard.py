"""
Unit tests for Jetski lifecycle hook guard (scripts/jetski_guard.py).
"""

import json
import unittest
from scripts.jetski_guard import evaluate_pre_tool_use, evaluate_stop

class TestJetskiGuard(unittest.TestCase):
    def test_allow_safe_command(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "make verify"}
            }
        }
        res = evaluate_pre_tool_use(payload)
        self.assertEqual(res["decision"], "allow")

    def test_deny_git_add_all(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "git add -A"}
            }
        }
        res = evaluate_pre_tool_use(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("git add -A", res["reason"])

    def test_deny_git_add_dot(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "git add ."}
            }
        }
        res = evaluate_pre_tool_use(payload)
        self.assertEqual(res["decision"], "deny")

    def test_deny_git_commit_all(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "git commit -am 'quick fix'"}
            }
        }
        res = evaluate_pre_tool_use(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("git commit -a", res["reason"])

    def test_allow_explicit_staging(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "git add src/cli.py tests/unit/test_cli.py"}
            }
        }
        res = evaluate_pre_tool_use(payload)
        self.assertEqual(res["decision"], "allow")

    def test_stop_hook_clean_exit(self):
        payload = {
            "executionNum": 1,
            "terminationReason": "model_stop",
            "fullyIdle": True
        }
        res = evaluate_stop(payload)
        self.assertEqual(res["decision"], "allow")

if __name__ == "__main__":
    unittest.main()
