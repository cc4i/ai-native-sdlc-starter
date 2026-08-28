import unittest

from src.models.review import Finding, Severity
from src.tools.diff_parser import DiffParser

SAMPLE_DIFF = """diff --git a/src/example.py b/src/example.py
index abc1234..def5678 100644
--- a/src/example.py
+++ b/src/example.py
@@ -10,3 +10,4 @@ def calculate():
     x = 1
-    y = 2
+    y = 3
+    z = 4
     return x + y
@@ -30,2 +31,3 @@ def other():
     a = 10
+    b = 20
     return a
"""


class TestDiffParser(unittest.TestCase):
    def setUp(self):
        self.parser = DiffParser(SAMPLE_DIFF)

    def test_parse_diff_hunks(self):
        self.assertIn("src/example.py", self.parser.file_hunks)
        valid_lines = self.parser.file_hunks["src/example.py"]
        # Hunk 1 starts at 10:
        # line 10: "    x = 1" (context ' ')
        # line 11: "    y = 3" (added '+')
        # line 12: "    z = 4" (added '+')
        # line 13: "    return x + y" (context ' ')
        self.assertIn(10, valid_lines)
        self.assertIn(11, valid_lines)
        self.assertIn(12, valid_lines)
        self.assertIn(13, valid_lines)

        # Lines outside hunk should not be in valid_lines
        self.assertNotIn(5, valid_lines)
        self.assertNotIn(20, valid_lines)

    def test_is_line_in_diff(self):
        self.assertTrue(self.parser.is_line_in_diff("src/example.py", 11))
        self.assertTrue(self.parser.is_line_in_diff("src/example.py", 32))
        self.assertFalse(self.parser.is_line_in_diff("src/example.py", 99))
        self.assertFalse(self.parser.is_line_in_diff("src/nonexistent.py", 11))

    def test_partition_findings(self):
        f1 = Finding(
            severity=Severity.BLOCKER,
            title="Syntax Error",
            message="Error on line 11",
            file_path="src/example.py",
            line_number=11,
            rule_id="RULE-1",
        )
        f2 = Finding(
            severity=Severity.IMPORTANT,
            title="Warning",
            message="Error on line 5 (outside hunk)",
            file_path="src/example.py",
            line_number=5,
            rule_id="RULE-2",
        )
        f3 = Finding(
            severity=Severity.NIT,
            title="Nitpick",
            message="General file issue",
            file_path="src/example.py",
            line_number=0,
            rule_id="RULE-3",
        )

        inline, summary = self.parser.partition_findings([f1, f2, f3])
        self.assertEqual(len(inline), 1)
        self.assertEqual(inline[0].rule_id, "RULE-1")

        self.assertEqual(len(summary), 2)
        self.assertEqual({f.rule_id for f in summary}, {"RULE-2", "RULE-3"})


if __name__ == "__main__":
    unittest.main()
