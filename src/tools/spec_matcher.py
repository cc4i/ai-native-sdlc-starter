"""
Spec Compliance & Acceptance Criteria Matcher Tool.
"""

from typing import List

from src.models.review import Finding, Severity


class SpecComplianceTool:
    """Verifies that code diffs satisfy key acceptance terms and Gherkin scenarios."""

    def scan(self, code_content: str, spec_content: str = "", file_path: str = "") -> List[Finding]:
        findings: List[Finding] = []
        if not spec_content:
            return findings

        # Check for error handling scenarios (e.g. 404 / 403)
        if "404" in spec_content or "not found" in spec_content.lower():
            if (
                "404" not in code_content
                and "NotFound" not in code_content
                and "not_found" not in code_content.lower()
            ):
                findings.append(
                    Finding(
                        severity=Severity.IMPORTANT,
                        title="Missing Spec Scenario: 404 Not Found",
                        message="Spec requires 404 / Not Found handling, but no matching error status was found in code.",
                        file_path=file_path,
                        rule_id="SPEC-001",
                    )
                )

        # Check for auth requirements
        if (
            "jwt" in spec_content.lower()
            or "bearer" in spec_content.lower()
            or "auth" in spec_content.lower()
        ):
            if (
                "auth" not in code_content.lower()
                and "token" not in code_content.lower()
                and "user" not in code_content.lower()
            ):
                findings.append(
                    Finding(
                        severity=Severity.IMPORTANT,
                        title="Missing Spec Scenario: Authentication",
                        message="Spec mandates authentication verification, but no auth or token check was detected.",
                        file_path=file_path,
                        rule_id="SPEC-002",
                    )
                )

        return findings
