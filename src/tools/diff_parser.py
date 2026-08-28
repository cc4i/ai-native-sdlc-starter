"""
Diff parser and line anchor calculator for GitHub Pull Request inline reviews.
"""

import re
from typing import Dict, Set, List, Tuple
from src.models.review import Finding

class DiffParser:
    """Parses unified git diffs and maps valid diff hunk lines for inline PR commenting."""

    def __init__(self, diff_text: str = ""):
        self.diff_text = diff_text
        self.file_hunks: Dict[str, Set[int]] = {}
        if diff_text:
            self.parse(diff_text)

    def parse(self, diff_text: str) -> Dict[str, Set[int]]:
        """
        Parses unified diff output into a mapping of {file_path: set(valid_new_line_numbers)}.
        Only lines present in diff hunks (the 'RIGHT' side of a PR) can accept inline comments.
        """
        self.diff_text = diff_text
        self.file_hunks = {}
        
        current_file = None
        current_new_line = 0

        # Regex for diff header: +++ b/path/to/file.py
        file_header_re = re.compile(r"^\+\+\+\s+b/(.*)$")
        # Regex for hunk header: @@ -old_start,old_len +new_start,new_len @@
        hunk_header_re = re.compile(r"^@@\s+-\d+(?:,\d+)?\s+\+(\d+)(?:,(\d+))?\s+@@")

        for line in diff_text.splitlines():
            file_match = file_header_re.match(line)
            if file_match:
                current_file = file_match.group(1).strip()
                if current_file not in self.file_hunks:
                    self.file_hunks[current_file] = set()
                continue

            if not current_file:
                continue

            hunk_match = hunk_header_re.match(line)
            if hunk_match:
                current_new_line = int(hunk_match.group(1))
                continue

            if line.startswith("+") and not line.startswith("+++"):
                # Added line on the RIGHT side
                self.file_hunks[current_file].add(current_new_line)
                current_new_line += 1
            elif line.startswith(" "):
                # Unchanged context line within diff hunk
                self.file_hunks[current_file].add(current_new_line)
                current_new_line += 1
            elif line.startswith("-") and not line.startswith("---"):
                # Deleted line (only exists on LEFT side, does not increment new_line)
                pass

        return self.file_hunks

    def is_line_in_diff(self, file_path: str, line_number: int) -> bool:
        """Returns True if the line number is part of an active diff hunk for the file."""
        normalized_path = file_path.lstrip("./")
        for path, lines in self.file_hunks.items():
            if path == normalized_path or path.endswith(normalized_path) or normalized_path.endswith(path):
                return line_number in lines
        return False

    def partition_findings(self, findings: List[Finding]) -> Tuple[List[Finding], List[Finding]]:
        """
        Partitions findings into:
        1. inline_findings: findings that safely anchor to lines inside the diff hunk.
        2. summary_findings: file-level findings or findings outside the active diff hunks.
        """
        inline: List[Finding] = []
        summary: List[Finding] = []

        for finding in findings:
            if finding.line_number > 0 and self.is_line_in_diff(finding.file_path, finding.line_number):
                inline.append(finding)
            else:
                summary.append(finding)

        return inline, summary
