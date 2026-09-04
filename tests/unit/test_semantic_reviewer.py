import json
import os
import unittest
from unittest.mock import MagicMock, patch

from src.agent.semantic_reviewer import (
    ClaudeReviewer,
    GeminiReviewer,
    OpenAIReviewer,
    get_semantic_reviewer,
)
from src.models.review import Verdict


class TestSemanticReviewer(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_claude_reviewer_defaults(self):
        reviewer = ClaudeReviewer()
        self.assertEqual(reviewer.model, "claude-3-7-sonnet-20250219")
        self.assertFalse(reviewer.is_available())
        self.assertIsNone(reviewer.review_diff("dummy diff"))

    @patch.dict(os.environ, {}, clear=True)
    def test_openai_reviewer_defaults(self):
        reviewer = OpenAIReviewer()
        self.assertEqual(reviewer.model, "gpt-4o")
        self.assertFalse(reviewer.is_available())
        self.assertIsNone(reviewer.review_diff("dummy diff"))

    @patch("urllib.request.urlopen")
    def test_claude_reviewer_network_call_and_nit_cap(self, mock_urlopen):
        reviewer = ClaudeReviewer(api_key="mock_claude_key")
        self.assertTrue(reviewer.is_available())

        findings = [
            {
                "severity": "Important",
                "title": "XSS Bug",
                "message": "Raw HTML rendered",
                "file_path": "web.py",
                "line_number": 12,
            },
            {
                "severity": "Consider",
                "title": "Timeout",
                "message": "Missing timeout",
                "file_path": "req.py",
                "line_number": 40,
            },
        ]
        for i in range(1, 8):
            findings.append(
                {
                    "severity": "Nit",
                    "title": f"Style {i}",
                    "message": f"Naming {i}",
                    "file_path": "a.py",
                    "line_number": i,
                }
            )

        response_payload = {
            "content": [
                {
                    "text": json.dumps(
                        {
                            "summary": "Claude Code Review completed",
                            "verdict": "CHANGES_REQUESTED",
                            "findings": findings,
                        }
                    )
                }
            ]
        }
        mock_cm = MagicMock()
        mock_cm.read.return_value = json.dumps(response_payload).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_cm

        report = reviewer.review_diff("diff --git a/file b/file")
        self.assertIsNotNone(report)
        self.assertEqual(report.verdict, Verdict.CHANGES_REQUESTED)
        # 1 Blocker + 1 Important + 5 Nits (capped from 7) = 7 findings
        self.assertEqual(len(report.findings), 7)
        self.assertEqual(report.findings[0].rule_id, "CLAUDE-3.7")

        # Fallback on network error
        mock_urlopen.side_effect = Exception("API Timeout")
        self.assertIsNone(reviewer.review_diff("diff content"))

    @patch("urllib.request.urlopen")
    def test_openai_reviewer_network_call(self, mock_urlopen):
        reviewer = OpenAIReviewer(api_key="mock_openai_key")
        self.assertTrue(reviewer.is_available())

        response_payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "summary": "OpenAI Review completed",
                                "verdict": "PASS",
                                "findings": [],
                            }
                        )
                    }
                }
            ]
        }
        mock_cm = MagicMock()
        mock_cm.read.return_value = json.dumps(response_payload).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_cm

        report = reviewer.review_diff("diff --git a/file b/file")
        self.assertIsNotNone(report)
        self.assertEqual(report.verdict, Verdict.PASS)

        # Fallback on network error
        mock_urlopen.side_effect = Exception("OpenAI Service Unavailable")
        self.assertIsNone(reviewer.review_diff("diff content"))

    def test_factory_explicit_provider_selection(self):
        r_claude = get_semantic_reviewer(provider="claude", api_key="test_key")
        self.assertIsInstance(r_claude, ClaudeReviewer)

        r_openai = get_semantic_reviewer(provider="openai", api_key="test_key")
        self.assertIsInstance(r_openai, OpenAIReviewer)

        r_gemini = get_semantic_reviewer(provider="gemini", api_key="test_key")
        self.assertIsInstance(r_gemini, GeminiReviewer)

    @patch.dict(os.environ, {}, clear=True)
    def test_factory_auto_detection_priority(self):
        # 1. When ANTHROPIC_API_KEY is present
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
            r = get_semantic_reviewer(provider="auto")
            self.assertIsInstance(r, ClaudeReviewer)

        # 2. When OPENAI_API_KEY is present
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-openai-test"}):
            r = get_semantic_reviewer(provider="auto")
            self.assertIsInstance(r, OpenAIReviewer)

        # 3. When GEMINI_API_KEY is present
        with patch.dict(os.environ, {"GEMINI_API_KEY": "gemini-test"}):
            r = get_semantic_reviewer(provider="auto")
            self.assertIsInstance(r, GeminiReviewer)

        # 4. When no keys are present
        with patch.dict(os.environ, {}):
            r = get_semantic_reviewer(provider="auto")
            self.assertIsNone(r)


if __name__ == "__main__":
    unittest.main()
