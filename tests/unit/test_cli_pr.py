"""
Unit tests for CLI review-pr command.
"""

import unittest

from src.agent.review_agent import ReviewAgent
from src.models.review import Verdict


class TestCliPrUnit(unittest.TestCase):
    def setUp(self):
        self.agent = ReviewAgent()

    def test_review_files_clean(self):
        report = self.agent.review_files(["src/cli.py", "src/models/review.py"])
        self.assertEqual(report.verdict, Verdict.PASS)
        self.assertEqual(len(report.findings), 0)

    def test_review_files_with_findings(self):
        # tests/unit/test_agent.py contains intentional eval snippet for testing
        report = self.agent.review_files(["tests/unit/test_agent.py"])
        self.assertEqual(report.verdict, Verdict.BLOCKED)


if __name__ == "__main__":
    unittest.main()
