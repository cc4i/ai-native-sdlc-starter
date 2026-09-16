"""
Unit tests verifying multi-tool AI SDLC compliance across all supported coding tools:
Anthropic Claude Code, Google Antigravity, OpenAI Codex, Cursor, and GitHub Copilot.
"""

import unittest
from pathlib import Path


class TestMultiToolDirectives(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    def test_all_tool_directive_files_exist(self):
        """Verifies that directive files exist for all major coding tools."""
        expected_files = [
            "DSH.md",  # DeepSeek Harness
            "CLAUDE.md",  # Claude Code
            "GEMINI.md",  # Google Antigravity
            "AGENTS.md",  # Universal open agent standard
            "CODEX.md",  # OpenAI Codex
            ".cursorrules",  # Cursor root rules
            ".cursor/rules/sdlc.mdc",  # Cursor modern MDC rule
            ".github/copilot-instructions.md",  # GitHub Copilot
        ]
        for rel_path in expected_files:
            file_path = self.root_dir / rel_path
            self.assertTrue(
                file_path.exists(), f"Missing required agent directive file: {rel_path}"
            )
            content = file_path.read_text(encoding="utf-8").strip()
            self.assertGreater(
                len(content), 50, f"Directive file {rel_path} is empty or too brief."
            )

    def test_core_sdlc_rules_mirrored_across_directives(self):
        """
        Verifies that non-negotiable SDLC rules are mirrored in all primary directive files:
        1. Artifact chain (intent, spec, plan)
        2. TDD
        3. Verification (make verify)
        4. Branch-first development (feat/ or branch)
        5. Zero anti-shortcuts (TODO stubs)
        """
        primary_directives = ["DSH.md", "CLAUDE.md", "GEMINI.md", "AGENTS.md", "CODEX.md"]
        for rel_path in primary_directives:
            content = (self.root_dir / rel_path).read_text(encoding="utf-8").lower()
            self.assertIn("plan", content, f"{rel_path} missing plan requirement")
            self.assertIn("spec", content, f"{rel_path} missing spec requirement")
            self.assertIn("verify", content, f"{rel_path} missing verify command requirement")
            self.assertTrue(
                "tdd" in content or "test" in content, f"{rel_path} missing TDD requirement"
            )
            self.assertTrue(
                "branch" in content or "feat/" in content,
                f"{rel_path} missing branch-first development requirement",
            )
            self.assertTrue(
                "todo" in content or "shortcut" in content or "placeholder" in content,
                f"{rel_path} missing anti-shortcut prohibition",
            )

    def test_claude_code_slash_commands_present(self):
        """Verifies that all native Claude Code slash commands exist and contain required descriptions."""
        commands_dir = self.root_dir / ".claude" / "commands"
        self.assertTrue(commands_dir.exists(), ".claude/commands directory must exist")

        expected_commands = [
            "grill-me.md",
            "spec-architect.md",
            "verify.md",
            "review-pr.md",
            "new-intent.md",
        ]
        for cmd_name in expected_commands:
            cmd_file = commands_dir / cmd_name
            self.assertTrue(cmd_file.exists(), f"Missing Claude Code command: {cmd_name}")
            content = cmd_file.read_text(encoding="utf-8")
            self.assertTrue(
                content.startswith("---"), f"Command {cmd_name} must have YAML frontmatter"
            )
            self.assertIn("description:", content, f"Command {cmd_name} must have a description")

    def test_cursor_mdc_rule_format(self):
        """Verifies that .cursor/rules/sdlc.mdc has proper MDC frontmatter and globs."""
        mdc_file = self.root_dir / ".cursor" / "rules" / "sdlc.mdc"
        self.assertTrue(mdc_file.exists(), ".cursor/rules/sdlc.mdc must exist")
        content = mdc_file.read_text(encoding="utf-8")
        self.assertIn("globs:", content)
        self.assertIn("alwaysApply: true", content)
        self.assertIn("make verify", content)

    def test_dsh_directives_and_skills_exist(self):
        """Verifies that DSH.md exists and .agents/skills contains all 5 open agent skills."""
        dsh_file = self.root_dir / "DSH.md"
        self.assertTrue(dsh_file.exists(), "DSH.md directives file must exist")
        content = dsh_file.read_text(encoding="utf-8")
        self.assertIn("DeepSeek Harness", content)
        self.assertIn("subagent", content)
        self.assertIn("workflow", content)

        skills_dir = self.root_dir / ".agents" / "skills"
        self.assertTrue(skills_dir.exists(), ".agents/skills directory must exist")
        expected_skills = [
            "intent-capture",
            "spec-architect",
            "secure-api-design",
            "adversarial-review",
            "verifier-loop",
        ]
        for skill_name in expected_skills:
            skill_file = skills_dir / skill_name / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"Missing skill file: {skill_file}")
            text = skill_file.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---"), f"Skill {skill_name} must have YAML frontmatter")
            self.assertIn("name:", text)
            self.assertIn("description:", text)

    def test_uv_cache_isolation_in_scripts_and_makefile(self):
        """Verifies that UV_CACHE_DIR is scoped project-locally and ignored in .gitignore."""
        verify_script = (self.root_dir / "scripts" / "verify.sh").read_text(encoding="utf-8")
        self.assertIn("UV_CACHE_DIR=", verify_script, "scripts/verify.sh must set UV_CACHE_DIR")
        self.assertIn(".uv_cache", verify_script, "scripts/verify.sh must use .uv_cache")

        makefile = (self.root_dir / "Makefile").read_text(encoding="utf-8")
        self.assertIn("UV_CACHE_DIR", makefile, "Makefile must configure UV_CACHE_DIR")

        gitignore = (self.root_dir / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".uv_cache", gitignore, ".gitignore must ignore .uv_cache")


if __name__ == "__main__":
    unittest.main()
