"""
Autonomous Semantic Code Reviewer powered by Gemini 3.7 Flash.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from src.models.review import Finding, ReviewReport, Severity, Verdict

DEFAULT_GEMINI_MODEL = "gemini-3.7-flash"

GEMINI_REVIEW_SYSTEM_PROMPT = """You are an expert autonomous software reviewer performing an adversarial code review of a pull request diff against REVIEW.md.
Follow REVIEW.md strictly:
1. Pass 1: Correctness (logic errors, off-by-one, unhandled None, resource/lock leaks, async bugs: un-awaited coroutines, gather exceptions).
2. Pass 2: Security (router authorization, credentials/secrets in logs, input sanitization, impersonation boundaries).
3. Pass 3: Plan Compliance (verifying corresponding docs/plans/ artifacts and frontmatter).

Severity Ladder:
- Important: Breaks behavior, leaks data, or violates a stated policy.
- Consider: Real but arguable. Missing guard, fragile assumption.
- Nit: Style, naming, minor phrasing (MAX 5 Nits total, then stop).

Do NOT review formatting, import ordering, line length, or type annotations already handled by linters.
If a direct fix is clear, provide the exact code replacement in the `suggestion` field.

Output valid JSON matching this schema:
{
  "summary": "Concise executive summary of review",
  "verdict": "PASS" | "CHANGES_REQUESTED" | "BLOCKED",
  "findings": [
    {
      "severity": "Important" | "Consider" | "Nit",
      "title": "Short title",
      "message": "Detailed explanation citing why it is a defect",
      "file_path": "path/to/file.py",
      "line_number": 123,
      "rule_id": "SEMANTIC-001",
      "suggestion": "optional exact code replacement"
    }
  ]
}
"""


class GeminiReviewer:
    """Invokes Gemini 3.7 Flash to perform deep semantic code reviews."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def is_available(self) -> bool:
        """Returns True if a Gemini API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def review_diff(
        self,
        diff_text: str,
        review_policy: str = "",
        spec_content: str = "",
    ) -> Optional[ReviewReport]:
        """
        Runs semantic review using Gemini 3.7 Flash.
        Returns ReviewReport if successful, or None if unconfigured / unavailable.
        """
        if not self.is_available() or not diff_text.strip():
            return None

        prompt = f"""### REVIEW POLICY (from REVIEW.md):
{review_policy or "Standard AI-Native SDLC Review Standard: Pass 1 Correctness, Pass 2 Security, Pass 3 Plan Compliance."}

### SPECIFICATION CONTEXT:
{spec_content or "No external spec provided."}

### PULL REQUEST DIFF TO REVIEW:
```diff
{diff_text}
```

Perform the 3-pass review and return JSON.
"""

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload = {
            "system_instruction": {"parts": [{"text": GEMINI_REVIEW_SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        }

        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            candidates = data.get("candidates", [])
            if not candidates:
                return None

            raw_text = candidates[0]["content"]["parts"][0]["text"]
            result = json.loads(raw_text)
            return self._parse_json_result(result)

        except Exception as e:
            # Gracefully log without crashing CI pipeline
            print(f"⚠️  [Gemini Reviewer] Notice: Cloud review skipped due to: {e}")
            return None

    def _parse_json_result(self, result: Dict[str, Any]) -> ReviewReport:
        """Parses structured JSON response into a ReviewReport."""
        summary = result.get("summary", "Gemini 3.7 Flash Semantic Review completed.")
        verdict_str = result.get("verdict", "PASS").upper()
        if verdict_str == "BLOCKED":
            verdict = Verdict.BLOCKED
        elif verdict_str == "CHANGES_REQUESTED":
            verdict = Verdict.CHANGES_REQUESTED
        else:
            verdict = Verdict.PASS

        findings: List[Finding] = []
        raw_findings = result.get("findings", [])

        nit_count = 0
        for f in raw_findings:
            sev_str = str(f.get("severity", "Consider")).upper()
            if sev_str == "IMPORTANT" or sev_str == "BLOCKER":
                severity = Severity.BLOCKER
            elif sev_str == "CONSIDER":
                severity = Severity.IMPORTANT
            else:
                severity = Severity.NIT
                nit_count += 1
                if nit_count > 5:
                    # Enforce strict 5-nit cap
                    continue

            findings.append(
                Finding(
                    severity=severity,
                    title=f.get("title", "Review Finding"),
                    message=f.get("message", ""),
                    file_path=f.get("file_path", ""),
                    line_number=f.get("line_number"),
                    rule_id=f.get("rule_id", "GEMINI-3.7"),
                    suggestion=f.get("suggestion"),
                )
            )

        return ReviewReport(
            target_name=f"PR Diff ({self.model})",
            verdict=verdict,
            findings=findings,
            summary=summary,
        )
