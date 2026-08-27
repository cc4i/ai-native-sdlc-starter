"""
Data models for Code Review findings and audit reports.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class Severity(str, Enum):
    BLOCKER = "BLOCKER"
    IMPORTANT = "IMPORTANT"
    NIT = "NIT"

class Verdict(str, Enum):
    PASS = "PASS"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    BLOCKED = "BLOCKED"

@dataclass
class Finding:
    severity: Severity
    title: str
    message: str
    file_path: str = ""
    line_number: Optional[int] = None
    rule_id: str = ""

@dataclass
class ReviewReport:
    target_name: str
    verdict: Verdict
    findings: List[Finding] = field(default_factory=list)
    summary: str = ""
