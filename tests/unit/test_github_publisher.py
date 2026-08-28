import unittest
from src.tools.github_publisher import GitHubReviewPublisher
from src.tools.diff_parser import DiffParser
from src.models.review import Finding, ReviewReport, Severity, Verdict

SAMPLE_DIFF = """diff --git a/src/api.py b/src/api.py
index 1111111..2222222 100644
--- a/src/api.py
+++ b/src/api.py
@@ -10,3 +10,4 @@ def handler():
     a = 1
-    b = 2
+    b = 3
+    c = 4
     return a + b
"""

class TestGitHubReviewPublisher(unittest.TestCase):
    def setUp(self):
        self.publisher = GitHubReviewPublisher(nit_cap=5)
        self.diff_parser = DiffParser(SAMPLE_DIFF)

    def test_calculate_tally_and_format(self):
        findings = [
            Finding(severity=Severity.BLOCKER, title="B1", message="m1"),
            Finding(severity=Severity.IMPORTANT, title="I1", message="m2"),
            Finding(severity=Severity.IMPORTANT, title="I2", message="m3"),
        ]
        # Add 6 nits
        for i in range(6):
            findings.append(Finding(severity=Severity.NIT, title=f"N{i}", message="nit"))

        tally = self.publisher.calculate_tally(findings)
        self.assertEqual(tally["important"], 1)
        self.assertEqual(tally["consider"], 2)
        self.assertEqual(tally["nit"], 5)  # capped at 5

        tally_line = self.publisher.format_tally_line(findings)
        self.assertEqual(tally_line, "Important: 1, Consider: 2, Nit: 5")

    def test_build_inline_comment_body_with_suggestion(self):
        finding = Finding(
            severity=Severity.BLOCKER,
            title="Dangerous eval",
            message="Use ast.literal_eval instead",
            suggestion="ast.literal_eval(user_input)",
            rule_id="SEC-001"
        )
        body = self.publisher.build_inline_comment_body(finding)
        self.assertIn("🚨 Important: Dangerous eval", body)
        self.assertIn("```suggestion", body)
        self.assertIn("ast.literal_eval(user_input)", body)
        self.assertIn("*Rule: `SEC-001`*", body)

    def test_build_review_payload_partitioning(self):
        f_inline = Finding(
            severity=Severity.BLOCKER,
            title="Syntax Error",
            message="Bad line",
            file_path="src/api.py",
            line_number=11,  # in diff
            suggestion="b = 3"
        )
        f_summary = Finding(
            severity=Severity.IMPORTANT,
            title="Module Config",
            message="Missing config at file top",
            file_path="src/api.py",
            line_number=2,  # outside diff hunk
        )

        report = ReviewReport(
            target_name="PR #1",
            verdict=Verdict.BLOCKED,
            findings=[f_inline, f_summary],
            summary="Review failed due to blocker."
        )

        payload = self.publisher.build_review_payload(
            report=report,
            diff_parser=self.diff_parser,
            commit_id="abc1234"
        )

        self.assertEqual(payload["event"], "COMMENT")
        self.assertEqual(payload["commit_id"], "abc1234")
        self.assertEqual(len(payload["comments"]), 1)
        self.assertEqual(payload["comments"][0]["path"], "src/api.py")
        self.assertEqual(payload["comments"][0]["line"], 11)
        self.assertIn("```suggestion", payload["comments"][0]["body"])

        # Summary finding is in the review body
        self.assertIn("Additional Findings (File / Global Scope)", payload["body"])
        self.assertIn("Missing config at file top", payload["body"])
        self.assertIn("Important: 1, Consider: 1, Nit: 0", payload["body"])

if __name__ == "__main__":
    unittest.main()
