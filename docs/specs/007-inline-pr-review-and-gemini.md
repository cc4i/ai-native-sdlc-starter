# Specification: Autonomous PR Inline Review Engine with Gemini 3.7 Flash

**Linked Intent**: [`docs/intent/007-inline-pr-review-and-gemini.md`](file:///Users/chuancc/mywork/ai/project-start/docs/intent/007-inline-pr-review-and-gemini.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Ready for Planning  

---

## 1. Overview & Architecture

This specification details the design for:
1. **`DiffParser`**: Calculates valid line positions from git diff output so review comments accurately attach to PR hunks.
2. **`GeminiReviewer`**: Integrates Gemini 3.7 Flash (`gemini-3.7-flash`) via structured JSON schema prompting to evaluate diffs against `REVIEW.md`.
3. **`GitHubReviewPublisher`**: Formats and formats batch GitHub PR reviews (`comments: [{path, line, body}]`) with machine-readable tally (`Important: n, Consider: n, Nit: n`).
4. **Enhanced ReviewAgent CLI & GitHub Actions Workflow**: Runs locally with deterministic tools, and in CI with Gemini 3.7 Flash when configured.

---

## 2. Gherkin Acceptance Scenarios

### Feature: Diff Line Position Calculator
```gherkin
Scenario: Map finding line number to valid diff hunk
  Given a git diff with modified lines in "src/tools/scanner.py" at lines 15-20
  When DiffParser checks whether line 17 is part of the added/modified diff
  Then DiffParser marks line 17 as valid for inline commenting
  And returns the exact line position.

Scenario: Reject lines outside diff hunks
  Given a file with 100 lines but only lines 50-55 changed in the diff
  When a finding is reported on line 10 (unchanged)
  Then DiffParser flags it as outside the diff hunk
  And routes the finding to the PR summary rather than an invalid inline comment.
```

### Feature: Gemini 3.7 Flash Semantic Review
```gherkin
Scenario: Semantic review with Gemini 3.7 Flash
  Given a PR diff with an un-awaited coroutine or unhandled None
  When GeminiReviewer is invoked with model "gemini-3.7-flash"
  Then it produces structured findings conforming to the ReviewFindings schema
  And assigns severity ("Important", "Consider", or "Nit")
  And includes a 1-click suggestion block if a direct fix is available.

Scenario: Graceful degradation when Gemini is not configured
  Given no GEMINI_API_KEY or Google Cloud credentials in the environment
  When ReviewAgent executes in CI or locally
  Then it logs a graceful notice
  And relies on the Tier 1 deterministic AST and secret scanner
  And exits without crashing.
```

### Feature: Machine-Readable Severity Tally & Nit Cap
```gherkin
Scenario: Tally and Nit cap enforcement
  Given 8 Nit findings, 2 Important findings, and 1 Consider finding
  When ReviewAgent renders the review report
  Then Nits are capped at 5
  And the report concludes with "Important: 2, Consider: 1, Nit: 5".
```

---

## 3. Data Contracts

### Inline Comment Schema
```python
class InlineComment:
    path: str
    line: int
    body: str
    side: str = "RIGHT"  # Comments on new code in diff
    suggestion: Optional[str] = None
```

### Gemini Review Request & Structured Output Schema
```json
{
  "summary": "High-level review assessment",
  "verdict": "PASS" | "CHANGES_REQUESTED" | "BLOCKED",
  "findings": [
    {
      "rule_id": "string",
      "severity": "Important" | "Consider" | "Nit",
      "file_path": "string",
      "line_number": 123,
      "message": "Explanation of issue",
      "suggestion": "optional code replacement"
    }
  ]
}
```
