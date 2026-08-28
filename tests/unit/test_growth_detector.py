import unittest
from pathlib import Path


class TestGrowthDetector(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    def test_verify_script_contains_codegraph_growth_logic(self):
        """verify.sh must contain logic checking for codebase growth and recommending CodeGraph."""
        verify_script = (self.root_dir / "scripts" / "verify.sh").read_text(encoding="utf-8")
        self.assertIn("codegraph", verify_script.lower(), "verify.sh must reference codegraph")
        self.assertIn(
            "colbymchenry/codegraph",
            verify_script,
            "verify.sh must cite github.com/colbymchenry/codegraph",
        )

    def test_check_artifacts_contains_codegraph_growth_logic(self):
        """check-artifacts.sh must reference CodeGraph scalability guidance."""
        check_script = (self.root_dir / "scripts" / "check-artifacts.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "codegraph", check_script.lower(), "check-artifacts.sh must reference codegraph"
        )

    def test_gemini_directives_contain_codegraph_rules(self):
        """GEMINI.md must contain explicit directives on querying CodeGraph when available."""
        gemini_md = (self.root_dir / "GEMINI.md").read_text(encoding="utf-8")
        self.assertIn("CodeGraph", gemini_md, "GEMINI.md must contain CodeGraph guidance")
        self.assertIn(
            "codegraph_explore", gemini_md, "GEMINI.md must cite codegraph_explore MCP tool"
        )


if __name__ == "__main__":
    unittest.main()
