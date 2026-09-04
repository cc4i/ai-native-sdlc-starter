"""
Autonomous Multi-Provider Semantic Code Reviewer.
Supports Anthropic Claude, OpenAI Codex/GPT, and Google Gemini via zero-dependency HTTP requests.
"""

import json
import os
import re
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.agent.gemini_reviewer import GeminiReviewer
from src.models.review import Finding, ReviewReport, Severity, Verdict

DEFAULT_CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_GEMINI_MODEL = "gemini-3.7-flash"

SEMANTIC_REVIEW_SYSTEM_PROMPT = """You are an expert autonomous software reviewer performing an adversarial code review of a pull request diff against REVIEW.md.
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


def _extract_json_block(text: str) -> Dict[str, Any]:
    """Extracts JSON object from model output text, handling possible markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Match outermost curly braces
        match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise


def _parse_findings_report(
    result: Dict[str, Any], default_rule_id: str, model_name: str
) -> ReviewReport:
    """Parses standard review JSON into a ReviewReport with 5-nit cap and severity mapping."""
    summary = result.get("summary", f"{model_name} Semantic Review completed.")
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
        if sev_str in ("IMPORTANT", "BLOCKER"):
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
                rule_id=f.get("rule_id", default_rule_id),
                suggestion=f.get("suggestion"),
            )
        )

    return ReviewReport(
        target_name=f"PR Diff ({model_name})",
        verdict=verdict,
        findings=findings,
        summary=summary,
    )


class BaseSemanticReviewer(ABC):
    """Abstract base class for all semantic reviewer backends."""

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if provider credentials are configured."""
        ...

    @abstractmethod
    def review_diff(
        self,
        diff_text: str,
        review_policy: str = "",
        spec_content: str = "",
    ) -> Optional[ReviewReport]:
        """Runs cloud semantic review and returns ReviewReport, or None on failure."""
        ...


class ClaudeReviewer(BaseSemanticReviewer):
    """Invokes Anthropic Messages API (Claude 3.7 / 3.5) via standard urllib."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model or os.getenv("ANTHROPIC_MODEL", DEFAULT_CLAUDE_MODEL)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def review_diff(
        self,
        diff_text: str,
        review_policy: str = "",
        spec_content: str = "",
    ) -> Optional[ReviewReport]:
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

Perform the 3-pass review and return JSON matching the schema.
"""
        endpoint = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": SEMANTIC_REVIEW_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key or "",
                    "anthropic-version": "2023-06-01",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            content_blocks = data.get("content", [])
            if not content_blocks:
                return None

            raw_text = content_blocks[0].get("text", "")
            result = _extract_json_block(raw_text)
            return _parse_findings_report(
                result, default_rule_id="CLAUDE-3.7", model_name=self.model
            )

        except Exception as e:
            print(f"⚠️  [Claude Reviewer] Notice: Semantic review skipped due to: {e}")
            return None


class OpenAIReviewer(BaseSemanticReviewer):
    """Invokes OpenAI Chat Completions API (GPT-4o / Codex) via standard urllib."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model or os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def review_diff(
        self,
        diff_text: str,
        review_policy: str = "",
        spec_content: str = "",
    ) -> Optional[ReviewReport]:
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

Perform the 3-pass review and return JSON matching the schema.
"""
        endpoint = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SEMANTIC_REVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }

        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            choices = data.get("choices", [])
            if not choices:
                return None

            raw_text = choices[0]["message"].get("content", "")
            result = _extract_json_block(raw_text)
            return _parse_findings_report(
                result, default_rule_id="OPENAI-GPT4O", model_name=self.model
            )

        except Exception as e:
            print(f"⚠️  [OpenAI Reviewer] Notice: Semantic review skipped due to: {e}")
            return None


def get_semantic_reviewer(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Optional[BaseSemanticReviewer]:
    """
    Factory function returning the configured semantic reviewer.
    Priority:
    1. Explicit provider argument (claude | openai | gemini)
    2. LLM_PROVIDER environment variable
    3. Auto-detection based on present API keys:
       - ANTHROPIC_API_KEY -> ClaudeReviewer
       - OPENAI_API_KEY    -> OpenAIReviewer
       - GEMINI_API_KEY    -> GeminiReviewer
    """
    prov = (provider or os.getenv("LLM_PROVIDER", "auto")).lower().strip()

    if prov in ("claude", "anthropic"):
        return ClaudeReviewer(model=model, api_key=api_key)
    elif prov in ("openai", "codex"):
        return OpenAIReviewer(model=model, api_key=api_key)
    elif prov == "gemini":
        return GeminiReviewer(model=model, api_key=api_key)
    elif prov in ("auto", ""):
        if api_key:
            return GeminiReviewer(model=model, api_key=api_key)
        if os.getenv("ANTHROPIC_API_KEY"):
            return ClaudeReviewer(model=model)
        elif os.getenv("OPENAI_API_KEY"):
            return OpenAIReviewer(model=model)
        elif os.getenv("GEMINI_API_KEY"):
            return GeminiReviewer(model=model)
        return None

    return None
