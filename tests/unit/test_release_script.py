import os
import subprocess
import unittest
from pathlib import Path


class TestReleaseScript(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.release_script = self.root_dir / "scripts" / "release.sh"

    def test_release_script_exists_and_executable(self):
        """scripts/release.sh must exist and be executable."""
        self.assertTrue(self.release_script.exists(), "scripts/release.sh does not exist")
        self.assertTrue(
            os.access(self.release_script, os.X_OK), "scripts/release.sh is not executable"
        )

    def test_release_script_rejects_invalid_version(self):
        """scripts/release.sh must reject versions that do not follow semantic versioning (vX.Y.Z)."""
        res = subprocess.run(
            ["bash", str(self.release_script), "invalid-version", "--dry-run"],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Invalid version", res.stdout + res.stderr)

    def test_release_script_validates_version_regex(self):
        """scripts/release.sh --dry-run must succeed with valid semantic version (v1.1.0)."""
        res = subprocess.run(
            ["bash", str(self.release_script), "v1.1.0", "--dry-run"],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertIn("Dry run", res.stdout + res.stderr)
        self.assertEqual(res.returncode, 0)

    def test_release_script_contains_no_git_commit(self):
        """scripts/release.sh must never run git commit to prevent branch protection violations on main."""
        content = self.release_script.read_text(encoding="utf-8")
        # Ensure no active git commit command exists in release.sh
        lines = [line.strip() for line in content.splitlines() if not line.strip().startswith("#")]
        self.assertFalse(
            any("git commit" in line for line in lines),
            "scripts/release.sh must not execute 'git commit' on protected branches",
        )

    def test_release_script_supports_push_flag_in_help(self):
        """scripts/release.sh usage string must include --push."""
        res = subprocess.run(
            ["bash", str(self.release_script)],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertIn("--push", res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
