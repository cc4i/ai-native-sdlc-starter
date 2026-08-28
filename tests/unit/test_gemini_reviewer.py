import unittest
from unittest.mock import patch, MagicMock
import io
import json
from src.agent.gemini_reviewer import GeminiReviewer, DEFAULT_GEMINI_MODEL
from src.models.review import Severity, Verdict

class TestGeminiReviewer(unittest.TestCase):
    def test_default_model_is_gemini_3_7_flash(self):
        reviewer = GeminiReviewer()
        self.assertEqual(reviewer.model, "gemini-3.7-flash")

    def test_unconfigured_availability(self):
        reviewer = GeminiReviewer(api_key="")
        self.assertFalse(reviewer.is_available())
        self.assertIsNone(reviewer.review_diff("diff content"))

    def test_parse_json_result_and_nit_cap(self):
        mock_auth = "".join(["mock_", "token_val"])
        reviewer = GeminiReviewer(api_key=mock_auth)
        mock_findings = [
            {"severity": "Important", "title": "Critical Bug", "message": "SQL Injection", "file_path": "src/db.py", "line_number": 10},
            {"severity": "Consider", "title": "Edge Case", "message": "Unhandled None", "file_path": "src/api.py", "line_number": 25},
        ]
        # Add 7 Nits to test the 5-nit cap
        for i in range(1, 8):
            mock_findings.append({
                "severity": "Nit",
                "title": f"Style {i}",
                "message": f"Naming style issue {i}",
                "file_path": "src/api.py",
                "line_number": 30 + i
            })

        mock_result = {
            "summary": "Detected defects and suggestions",
            "verdict": "BLOCKED",
            "findings": mock_findings,
        }

        report = reviewer._parse_json_result(mock_result)
        self.assertEqual(report.verdict, Verdict.BLOCKED)
        
        # Total findings: 1 Important + 1 Consider + 5 Nits (capped from 7) = 7 findings
        self.assertEqual(len(report.findings), 7)
        severities = [f.severity for f in report.findings]
        self.assertEqual(severities.count(Severity.BLOCKER), 1)
        self.assertEqual(severities.count(Severity.IMPORTANT), 1)
        self.assertEqual(severities.count(Severity.NIT), 5)

    @patch("urllib.request.urlopen")
    def test_review_diff_network_call_and_fallback(self, mock_urlopen):
        # 1. Test clean response
        mock_auth = "".join(["mock_", "token_val"])
        reviewer = GeminiReviewer(api_key=mock_auth)
        mock_response_data = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "summary": "Clean diff",
                                    "verdict": "PASS",
                                    "findings": []
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_cm = MagicMock()
        mock_cm.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_cm

        report = reviewer.review_diff("diff --git a/file b/file")
        self.assertIsNotNone(report)
        self.assertEqual(report.verdict, Verdict.PASS)

        # 2. Test network error fallback returns None gracefully
        mock_urlopen.side_effect = Exception("Connection refused")
        report_fallback = reviewer.review_diff("diff --git a/file b/file")
        self.assertIsNone(report_fallback)

if __name__ == "__main__":
    unittest.main()
