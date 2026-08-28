import unittest
from pathlib import Path


class TestReadmeCleanliness(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.readme_path = self.root_dir / "README.md"
        self.readme_content = self.readme_path.read_text(encoding="utf-8")

    def test_readme_does_not_contain_ascii_directory_tree(self):
        """README.md should not contain a verbose ASCII directory tree."""
        self.assertNotIn(
            "## 📁 Repository Structure",
            self.readme_content,
            "README.md should not contain a redundant ASCII file directory tree block.",
        )
        self.assertNotIn(
            "├── GEMINI.md",
            self.readme_content,
            "ASCII directory tree should be removed from README.md.",
        )

    def test_readme_contains_badges(self):
        """README.md must contain badges for Python 3.14+, uv, and CodeGraph."""
        self.assertIn(
            "img.shields.io", self.readme_content, "README.md must include shields.io badges"
        )
        self.assertIn("3.14", self.readme_content, "README.md must display Python 3.14+ badge")
        self.assertIn(
            "uv", self.readme_content.lower(), "README.md must reference uv badge/tooling"
        )
        self.assertIn(
            "codegraph", self.readme_content.lower(), "README.md must reference CodeGraph"
        )

    def test_readme_references_onboarding_for_anatomy(self):
        """README.md must link to ONBOARDING.md for deep repository anatomy."""
        self.assertIn("ONBOARDING.md", self.readme_content)


if __name__ == "__main__":
    unittest.main()
