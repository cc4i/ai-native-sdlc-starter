"""
Secret and credential detection tool.
"""

import re
from typing import List

from src.models.review import Finding, Severity

SECRET_PATTERNS = [
    (
        "OpenAI API Key",
        r"sk-[a-zA-Z0-9_\-]{20,}",
        Severity.BLOCKER,
        "SEC-001",
        "Found hardcoded OpenAI API key.",
    ),
    (
        "AWS Access Key ID",
        r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        Severity.BLOCKER,
        "SEC-002",
        "Found hardcoded AWS Access Key.",
    ),
    (
        "Private Key Header",
        r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
        Severity.BLOCKER,
        "SEC-003",
        "Found embedded cryptographic private key.",
    ),
    (
        "Generic Secret Assignment",
        r"(?:password|secret|api_key|access_token|bearer)\s*=\s*['\"][a-zA-Z0-9_\-\.]{8,}['\"]",
        Severity.BLOCKER,
        "SEC-004",
        "Found potential plaintext password or secret token assignment.",
    ),
]


class SecretScannerTool:
    """Scans code content for hardcoded secrets, passwords, and private keys."""

    def __init__(self):
        self.patterns = [
            (name, re.compile(pat, re.IGNORECASE), sev, rule_id, desc)
            for name, pat, sev, rule_id, desc in SECRET_PATTERNS
        ]

    def scan(self, content: str, file_path: str = "") -> List[Finding]:
        findings: List[Finding] = []
        lines = content.splitlines()

        for line_idx, line in enumerate(lines, 1):
            # Support inline secret suppression pragmas (e.g. for mock test fixtures)
            if "pragma: allowlist secret" in line.lower() or "nosec" in line.lower():
                continue

            for name, pattern, severity, rule_id, desc in self.patterns:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            severity=severity,
                            title=f"Secret Detected: {name}",
                            message=f"{desc} Line: {line.strip()[:60]}...",
                            file_path=file_path,
                            line_number=line_idx,
                            rule_id=rule_id,
                        )
                    )
        return findings
