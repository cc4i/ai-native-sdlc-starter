"""
Integration tests for CLI entrypoint.
"""

import os
import subprocess
import tempfile
import unittest


class TestCliIntegration(unittest.TestCase):
    def test_cli_review_clean_file(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write('def hello():\n    return "world"\n')
            temp_name = f.name

        try:
            result = subprocess.run(
                ["python3", "-m", "src.cli", "review", temp_name],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("PASS", result.stdout)
        finally:
            os.remove(temp_name)

    def test_cli_review_blocked_file(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("KEY = " + '"sk-proj-1234567890abcdef1234567890abcdef1234"\n')
            temp_name = f.name

        try:
            result = subprocess.run(
                ["python3", "-m", "src.cli", "review", temp_name],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("BLOCKED", result.stdout)
            self.assertIn("Secret Detected", result.stdout)
        finally:
            os.remove(temp_name)


if __name__ == "__main__":
    unittest.main()
