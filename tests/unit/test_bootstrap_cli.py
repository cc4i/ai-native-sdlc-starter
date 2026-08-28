import subprocess
import unittest
from pathlib import Path


class TestBootstrapAndMakefileCli(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.bootstrap_script = self.root_dir / "bootstrap.sh"
        self.makefile = self.root_dir / "Makefile"

    def test_bootstrap_without_args_shows_help(self):
        """Running bootstrap.sh without arguments must display usage and exit 0."""
        res = subprocess.run(
            ["bash", str(self.bootstrap_script)],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Usage: bootstrap.sh <target-directory>", res.stdout)
        self.assertIn("Arguments:", res.stdout)

    def test_bootstrap_with_help_flag_shows_help(self):
        """Running bootstrap.sh with -h or --help must display usage."""
        for flag in ["-h", "--help"]:
            res = subprocess.run(
                ["bash", str(self.bootstrap_script), flag],
                cwd=str(self.root_dir),
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertIn("Usage: bootstrap.sh <target-directory>", res.stdout)

    def test_bootstrap_safety_guard_prevents_starter_repo_overwrite(self):
        """Running bootstrap.sh targeting the starter repo must be blocked by the safety guard."""
        res = subprocess.run(
            ["bash", str(self.bootstrap_script), "."],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 1)
        self.assertIn("Safety Guard", res.stdout + res.stderr)
        self.assertIn("starter repository itself", res.stdout + res.stderr)

    def test_makefile_without_args_shows_help(self):
        """Running 'make' without arguments must display the help command reference."""
        res = subprocess.run(
            ["make"],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("AI-Native SDLC Lifecycle Commands:", res.stdout)
        self.assertIn("make help", res.stdout)
        self.assertIn("make verify", res.stdout)


if __name__ == "__main__":
    unittest.main()
