"""
Integration tests for CLI review-pr command execution.
"""

import subprocess
import unittest
from pathlib import Path

class TestPrReviewCliIntegration(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    def test_cli_review_pr_files_clean(self):
        cmd = [
            "python3",
            "-m",
            "src.cli",
            "review-pr",
            "--files",
            "src/cli.py",
            "src/models/review.py",
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Expected clean pass, got: {result.stderr}")
        self.assertIn("Verdict**: `PASS`", result.stdout)

    def test_cli_review_pr_output_file(self):
        reviews_dir = self.root_dir / "docs" / "reviews"
        if not reviews_dir.exists():
            reviews_dir = self.root_dir / "reviews"
        out_file = reviews_dir / "test_temp_audit.md"
        cmd = [
            "python3",
            "-m",
            "src.cli",
            "review-pr",
            "--files",
            "src/cli.py",
            "--output",
            str(out_file),
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(out_file.exists())
        content = out_file.read_text(encoding="utf-8")
        self.assertIn("PR Review Audit Report", content)
        out_file.unlink()

    def test_cli_review_pr_inline_json_generation(self):
        reviews_dir = self.root_dir / "docs" / "reviews"
        if not reviews_dir.exists():
            reviews_dir = self.root_dir / "reviews"
        out_json = reviews_dir / "test_temp_inline.json"
        cmd = [
            "python3",
            "-m",
            "src.cli",
            "review-pr",
            "--files",
            "src/cli.py",
            "--inline-json",
            str(out_json),
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(out_json.exists())
        import json
        data = json.loads(out_json.read_text(encoding="utf-8"))
        self.assertIn("body", data)
        self.assertIn("event", data)
        self.assertEqual(data["event"], "COMMENT")
        self.assertIn("comments", data)
        out_json.unlink()

if __name__ == "__main__":
    unittest.main()
