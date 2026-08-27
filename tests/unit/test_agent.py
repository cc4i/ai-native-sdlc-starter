"""
Unit tests for ReviewAgent orchestrator.
"""

import unittest
from src.models.review import Severity, Verdict
from src.agent.review_agent import ReviewAgent

class TestReviewAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ReviewAgent()

    def test_verdict_blocked_on_secret(self):
        code = 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"'
        report = self.agent.review_code(code, "config.py")
        self.assertEqual(report.verdict, Verdict.BLOCKED)
        self.assertTrue(any(f.severity == Severity.BLOCKER for f in report.findings))

    def test_verdict_blocked_on_eval(self):
        code = 'def run(s):\n    return eval(s)'
        report = self.agent.review_code(code, "executor.py")
        self.assertEqual(report.verdict, Verdict.BLOCKED)

    def test_verdict_changes_requested_on_silent_exception(self):
        code = 'try:\n    pass\nexcept Exception:\n    pass'
        report = self.agent.review_code(code, "task.py")
        self.assertEqual(report.verdict, Verdict.CHANGES_REQUESTED)
        self.assertTrue(any(f.severity == Severity.IMPORTANT for f in report.findings))

    def test_verdict_pass_on_clean_code(self):
        code = '''
def calculate_tax(amount: float, rate: float) -> float:
    if amount < 0 or rate < 0:
        raise ValueError("Amount and rate must be non-negative")
    return amount * rate
'''
        report = self.agent.review_code(code, "tax.py")
        self.assertEqual(report.verdict, Verdict.PASS)
        self.assertEqual(len(report.findings), 0)

    def test_markdown_report_formatting(self):
        code = 'eval("1+1")'
        report = self.agent.review_code(code, "test.py")
        md = self.agent.render_markdown(report)
        self.assertIn("# PR Review Audit Report", md)
        self.assertIn("BLOCKED", md)
        self.assertIn("Tier 1: Blocker", md)


if __name__ == "__main__":
    unittest.main()
