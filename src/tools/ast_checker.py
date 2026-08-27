"""
Python AST Security and Code Quality Inspector.
"""

import ast
from typing import List
from src.models.review import Finding, Severity

DANGEROUS_CALLS = {
    "eval": (Severity.BLOCKER, "AST-001", "Dangerous execution: 'eval()' evaluates untrusted input as arbitrary Python code."),
    "exec": (Severity.BLOCKER, "AST-002", "Dangerous execution: 'exec()' executes arbitrary statements."),
}

class AstVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.findings: List[Finding] = []

    def visit_Call(self, node: ast.Call):
        # Detect eval / exec
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in DANGEROUS_CALLS:
                sev, rule_id, msg = DANGEROUS_CALLS[func_name]
                self.findings.append(
                    Finding(
                        severity=sev,
                        title=f"Dangerous Function Call: {func_name}()",
                        message=msg,
                        file_path=self.file_path,
                        line_number=node.lineno,
                        rule_id=rule_id,
                    )
                )
        
        # Detect subprocess.Popen / run with shell=True
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ("Popen", "run", "call", "check_output", "check_call"):
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        self.findings.append(
                            Finding(
                                severity=Severity.BLOCKER,
                                title="Command Injection Risk",
                                message=f"subprocess.{node.func.attr} called with shell=True",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                rule_id="AST-003",
                            )
                        )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        # Detect except Exception: pass or bare except: pass
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.findings.append(
                Finding(
                    severity=Severity.IMPORTANT,
                    title="Silent Exception Swallow",
                    message="Silent exception handling (except: pass) hides bugs and fails silently.",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    rule_id="AST-004",
                )
            )
        self.generic_visit(node)


class AstSecurityCheckerTool:
    """Inspects Python source code AST for security vulnerabilities and anti-patterns."""

    def scan(self, content: str, file_path: str = "") -> List[Finding]:
        if not file_path.endswith(".py") and not content.startswith("def ") and not "import " in content:
            # Non-python content, skip AST inspection
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return [
                Finding(
                    severity=Severity.BLOCKER,
                    title="Python Syntax Error",
                    message=f"Failed to parse AST: {e.msg}",
                    file_path=file_path,
                    line_number=e.lineno,
                    rule_id="AST-000",
                )
            ]

        visitor = AstVisitor(file_path=file_path)
        visitor.visit(tree)
        return visitor.findings
