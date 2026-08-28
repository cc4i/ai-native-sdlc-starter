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
        out_file = self.root_dir / "reviews" / "test_temp_audit.md"
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

if __name__ == "__main__":
    unittest.main()
