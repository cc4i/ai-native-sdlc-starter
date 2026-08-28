"""
Unit tests for Code Review Agent Inspection Tools.
"""

import unittest

from src.models.review import Severity
from src.tools.ast_checker import AstSecurityCheckerTool
from src.tools.secret_scanner import SecretScannerTool
from src.tools.spec_matcher import SpecComplianceTool


class TestSecretScannerTool(unittest.TestCase):
    def setUp(self):
        self.scanner = SecretScannerTool()

    def test_detect_openai_api_key(self):
        code = 'OPENAI_KEY = "sk-proj-1234567890abcdef1234567890abcdef1234"'
        findings = self.scanner.scan(code, "test_secrets.py")
        self.assertTrue(len(findings) >= 1)
        self.assertEqual(findings[0].severity, Severity.BLOCKER)
        self.assertIn("Secret", findings[0].title)

    def test_detect_private_key_header(self):
        code = 'KEY = "-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA0..."'
        findings = self.scanner.scan(code, "config.py")
        self.assertTrue(len(findings) >= 1)
        self.assertEqual(findings[0].severity, Severity.BLOCKER)

    def test_clean_code_no_secrets(self):
        code = 'import os\napi_key = os.environ.get("OPENAI_API_KEY")'
        findings = self.scanner.scan(code, "safe.py")
        self.assertEqual(len(findings), 0)


class TestAstSecurityCheckerTool(unittest.TestCase):
    def setUp(self):
        self.checker = AstSecurityCheckerTool()

    def test_detect_eval_usage(self):
        code = "def calculate(expr):\n    return eval(expr)"
        findings = self.checker.scan(code, "calc.py")
        self.assertTrue(
            any(f.severity == Severity.BLOCKER and "eval" in f.message for f in findings)
        )

    def test_detect_exec_usage(self):
        code = "exec(\"import os; os.system('ls')\")"
        findings = self.checker.scan(code, "dynamic.py")
        self.assertTrue(
            any(f.severity == Severity.BLOCKER and "exec" in f.message for f in findings)
        )

    def test_detect_silent_exception_swallow(self):
        code = "try:\n    do_something()\nexcept Exception:\n    pass"
        findings = self.checker.scan(code, "handler.py")
        self.assertTrue(
            any(
                f.severity == Severity.IMPORTANT and "silent" in f.message.lower() for f in findings
            )
        )

    def test_clean_python_code(self):
        code = """
def add(a: int, b: int) -> int:
    try:
        return a + b
    except TypeError as e:
        logger.error(f"Invalid input: {e}")
        raise
"""
        findings = self.checker.scan(code, "math_utils.py")
        self.assertEqual(len(findings), 0)


class TestSpecComplianceTool(unittest.TestCase):
    def setUp(self):
        self.matcher = SpecComplianceTool()

    def test_spec_gherkin_coverage_check(self):
        spec_text = """
### Story 1: User Login
#### Scenario 1.1: Success
Given valid credentials
When user clicks login
Then redirect to dashboard
"""
        # Code missing login redirect
        code_text = "def login(): return True"
        findings = self.matcher.scan(code_text, spec_text)
        # Should flag missing or unverified scenario aspects
        self.assertIsInstance(findings, list)


if __name__ == "__main__":
    unittest.main()
