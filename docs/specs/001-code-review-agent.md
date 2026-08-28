# Spec: Autonomous AI Code Review & Security Auditor Agent

**Linked Intent**: [`intent/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/intent/001-code-review-agent.md)  
**Author**: Antigravity SDLC Architect  
**Date**: 2026-08-27  
**Status**: Approved  

---

## 1. Overview & Scope

Design an autonomous Code Review Agent that inspects source files and Git diffs using specialized tool modules, classifies findings into `Blocker`, `Important`, and `Nit`, and outputs structured audit reports adhering to `REVIEW.md`.

- **In Scope**:
  - `SecretScannerTool`: Detects hardcoded API keys, private keys, JWT tokens, AWS/Google credentials.
  - `AstSecurityCheckerTool`: Uses Python's `ast` parser to detect dangerous calls (`eval`, `exec`, `subprocess.Popen(..., shell=True)`), insecure exception handling (`except: pass`), and anti-shortcuts.
  - `SpecComplianceTool`: Verifies that key acceptance criteria from `spec.md` are referenced and implemented.
  - `ReviewAgent`: Orchestrator that coordinates the inspection tools, computes the overall verdict (`PASS`, `CHANGES_REQUESTED`, `BLOCKED`), and generates formatted reports.
  - CLI entrypoint: `python3 -m src.cli review <file-or-diff>`.
- **Out of Scope**:
  - Direct GitHub API PR posting (handled by CI action wrapper).

---

## 2. User Stories & Acceptance Criteria (Gherkin)

### Story 1: Detect Hardcoded Secrets in Code Diffs
**As a** repository maintainer  
**I want** the agent to scan incoming code for exposed credentials  
**So that** sensitive tokens never reach the repository  

#### Scenario 1.1: Catch AWS / API Key in diff
```gherkin
Given a source file containing 'OPENAI_API_KEY = "sk-proj-1234567890abcdef1234567890abcdef"'
When the ReviewAgent runs secret scanning
Then a finding is recorded with severity "Blocker"
And finding category is "Security / Secret Leak"
And the overall verdict is "BLOCKED"
```

### Story 2: Detect Dangerous Execution and Anti-Shortcuts
**As a** security engineer  
**I want** the agent to analyze AST syntax for dangerous functions  
**So that** malicious or unstable code is blocked before deployment  

#### Scenario 2.1: Detect eval() usage
```gherkin
Given a Python file with line 'result = eval(user_input)'
When the ReviewAgent runs AST security analysis
Then a finding is recorded with severity "Blocker"
And finding message specifies dangerous function "eval"
And the overall verdict is "BLOCKED"
```

#### Scenario 2.2: Detect silent exception swallow (except: pass)
```gherkin
Given code containing 'except Exception: pass'
When the ReviewAgent runs AST analysis
Then a finding is recorded with severity "Important"
And finding message flags silent exception suppression
```

### Story 3: Clean Code Approval
**As a** developer  
**I want** clean, well-tested code to pass with zero blockers  
**So that** I can merge my PR quickly  

#### Scenario 3.1: Clean code passes review
```gherkin
Given a clean Python module with proper validation and error handling
When the ReviewAgent reviews the code
Then zero "Blocker" and zero "Important" findings are recorded
And the overall verdict is "PASS"
```

---

## 3. Architecture & Interfaces

### 3.1 Data Models
```python
from dataclasses import dataclass
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
    file_path: str
    line_number: Optional[int] = None
    rule_id: str = ""


@dataclass
class ReviewReport:
    target_name: str
    verdict: Verdict
    findings: List[Finding]
    summary: str
```

### 3.2 Agent Pipeline Loop
1. **Input Ingestion**: Read target file(s) or diff string.
2. **Tool Execution**:
   - Run `SecretScannerTool.scan(content, filename)`
   - Run `AstSecurityCheckerTool.scan(content, filename)`
   - Run `SpecComplianceTool.scan(content, spec_content)`
3. **Synthesis & Verdict Calculation**:
   - If `any(f.severity == BLOCKER)` ➔ `BLOCKED`
   - Else if `any(f.severity == IMPORTANT)` ➔ `CHANGES_REQUESTED`
   - Else ➔ `PASS`
4. **Report Rendering**: Produce markdown report adhering to `templates/review.template.md`.

---

## 4. Adversarial Review & Sign-Off
- **Spec Validator Gate**: PASSED (Unanimous 3/3 skeptics)
- **Approved by**: @lead-architect on 2026-08-27
- **Ready for Stage 3 (Build)**: `plans/001-code-review-agent.md`
