"""
Integration tests for AI-Native SDLC Git enforcement hooks.
"""

import os
import stat
import subprocess
import unittest
from pathlib import Path


class TestGitHooksIntegration(unittest.TestCase):
    """Verifies that Git pre-commit and pre-push enforcement hooks are properly configured."""

    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.pre_commit_hook = self.root_dir / ".githooks" / "pre-commit"
        self.pre_push_hook = self.root_dir / ".githooks" / "pre-push"
        self.installer_script = self.root_dir / "scripts" / "install-hooks.sh"

    def test_pre_commit_hook_exists_and_executable(self):
        self.assertTrue(self.pre_commit_hook.exists(), ".githooks/pre-commit must exist")
        mode = os.stat(self.pre_commit_hook).st_mode
        self.assertTrue(bool(mode & stat.S_IXUSR), ".githooks/pre-commit must be executable")

    def test_pre_push_hook_exists_and_executable(self):
        self.assertTrue(self.pre_push_hook.exists(), ".githooks/pre-push must exist")
        mode = os.stat(self.pre_push_hook).st_mode
        self.assertTrue(bool(mode & stat.S_IXUSR), ".githooks/pre-push must be executable")

    def test_install_hooks_script_runs_cleanly(self):
        result = subprocess.run(
            ["bash", str(self.installer_script)],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Installer failed: {result.stderr}")
        self.assertIn("Git hooks", result.stdout)


if __name__ == "__main__":
    unittest.main()
