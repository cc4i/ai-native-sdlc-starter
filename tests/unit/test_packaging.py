import tomllib
import unittest
from pathlib import Path


class TestProjectPackaging(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.pyproject_path = self.root_dir / "pyproject.toml"

    def test_pyproject_toml_exists(self):
        """pyproject.toml must exist at repository root."""
        self.assertTrue(self.pyproject_path.exists(), "pyproject.toml not found at repo root")

    def test_pyproject_conforms_to_pep621_and_python314(self):
        """pyproject.toml must contain valid PEP 621 metadata requiring Python >=3.14."""
        content = self.pyproject_path.read_text(encoding="utf-8")
        data = tomllib.loads(content)

        # Check project table
        self.assertIn("project", data)
        proj = data["project"]
        self.assertEqual(proj.get("name"), "ai-native-sdlc")
        self.assertIn("version", proj)
        self.assertIn("description", proj)

        # Must require Python >=3.14
        requires_python = proj.get("requires-python", "")
        self.assertTrue(
            ">=3.14" in requires_python or ">= 3.14" in requires_python,
            f"Expected requires-python >=3.14, got: {requires_python}",
        )

        # Check CLI console script
        scripts = proj.get("scripts", {})
        self.assertIn("ai-sdlc", scripts)
        self.assertEqual(scripts["ai-sdlc"], "src.cli:main")

        # Check ruff configuration
        self.assertIn("tool", data)
        self.assertIn("ruff", data["tool"])
        ruff_conf = data["tool"]["ruff"]
        self.assertEqual(ruff_conf.get("target-version"), "py314")


if __name__ == "__main__":
    unittest.main()
