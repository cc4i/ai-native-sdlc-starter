# Spec: Modern Packaging (uv, Python 3.14+), CodeGraph Scalability Guidance, Release Lifecycle & Repo Polish

**Linked Intent**: [`docs/intent/008-modern-tooling-codegraph-and-release.md`](../intent/008-modern-tooling-codegraph-and-release.md)  
**Author**: @antigravity  
**Date**: 2026-08-28  
**Status**: Validated  

---

## 1. Overview & Scope

- **Summary**: Modernize repository packaging with Python 3.14+ and `uv`, implement an automated codebase growth detector that proactively guides developers and agents to initialize CodeGraph (`colbymchenry/codegraph`), streamline `README.md` by removing the verbose ASCII directory tree while adding professional badges and repo promotion, automate regular releases via `scripts/release.sh` and GitHub Actions, and provide dedicated architecture scaling documentation.
- **In Scope**:
  - Root `pyproject.toml` conforming to PEP 621 with `requires-python = ">=3.14"`, `ruff` configuration (py314 target), `pytest`, and `ai-sdlc` CLI console script entry point.
  - Enhanced `Makefile` and `scripts/verify.sh` with `uv` detection and standard Python fallback.
  - Automated codebase growth analyzer in `scripts/verify.sh` and `scripts/check-artifacts.sh` (>25 files or >2,500 LOC triggers non-blocking advisory to initialize CodeGraph).
  - Antigravity/Jetski subagent directives in `GEMINI.md` for querying `codegraph_explore` MCP tool.
  - Streamlined `README.md`: removal of the ASCII repository structure tree, addition of open-source badges (CI, Python 3.14+, uv, CodeGraph, AI-Native SDLC, License), and repo "About" metadata recommendations.
  - Release automation script `scripts/release.sh`, `make release VERSION=v1.X.X`, `.github/workflows/release.yml`, and `docs/RELEASES.md`.
  - Architecture scaling documentation: `docs/architecture/SCALING_AND_CODEGRAPH.md`.
  - Update `ONBOARDING.md` and `bootstrap.sh`.
- **Out of Scope**:
  - Writing a custom graph indexing parser (we explicitly leverage `colbymchenry/codegraph`).
  - Deploying binary PyPI packages in this release.

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Python 3.14+ Baseline & Modern Packaging with `uv`
**As a** developer or CI runner  
**I want to** use Python 3.14+ and `uv` for sub-second dependency management, linting, and testing  
**So that** project setup is lightning fast and standardized  

#### Scenario 1.1: Verification with `uv` and Python 3.14+ Installed
```gherkin
Given a system with Python 3.14+ and "uv" installed on the PATH
And a valid "pyproject.toml" in the repository root specifying "requires-python = '>=3.14'"
When the developer runs "make verify"
Then "uv" is detected and used to run fast linting ("uv run ruff check .") and tests ("uv run pytest")
And all checks pass with exit code 0
```

#### Scenario 1.2: Verification Fallback Without `uv`
```gherkin
Given a system where "uv" is NOT installed on the PATH
When the developer runs "./scripts/verify.sh"
Then the script falls back cleanly to standard Python py_compile and unittest
And outputs zero fatal errors due to missing "uv"
And exits with code 0 if all tests pass
```

---

### Story 2: Codebase Growth Analysis & CodeGraph Scalability Guidance
**As an** AI agent or maintainer working on a growing repository  
**I want to** receive proactive guidance when the codebase crosses complexity thresholds  
**So that** agents avoid burning context tokens and avoid breaking un-staged callers  

#### Scenario 2.1: Codebase Growth Triggers CodeGraph Advisory
```gherkin
Given a repository containing more than 25 tracked source files or 2,500 lines of code
And the directory ".codegraph/" does NOT exist
When the verification loop ("make verify") or artifact check runs
Then an informative advisory notice is displayed recommending "codegraph init"
And references the mature "colbymchenry/codegraph" tool
And the verification loop does NOT fail because of the advisory (exit code remains 0)
```

#### Scenario 2.2: Initialized CodeGraph Suppresses Advisory
```gherkin
Given a repository where ".codegraph/" exists
When the verification loop ("make verify") runs
Then the CodeGraph setup reminder is suppressed
And verification reports clean codebase intelligence status
```

---

### Story 3: Streamlined Front Page & High-Bar Repository Polish
**As a** developer visiting the repository on GitHub  
**I want to** see a clean, punchy README focused on value proposition, badges, and the 6-stage lifecycle  
**So that** I understand the project in 30 seconds without scrolling through a 45-line ASCII file tree  

#### Scenario 3.1: Clean README Without Directory Tree
```gherkin
Given the file "README.md"
When inspected for layout and readability
Then it contains official status badges (CI, Python 3.14+, uv, CodeGraph, AI-Native SDLC, License)
And it does NOT contain an ASCII file directory tree block
And it directs developers to "ONBOARDING.md" for full file anatomy
```

---

### Story 4: Regular Release Automation
**As an** engineering maintainer  
**I want to** execute a single release command  
**So that** versions, changelog notes, artifact checks, and git release tags are consistently published  

#### Scenario 4.1: Automated Clean Release
```gherkin
Given a clean git working tree on a release branch
And all tests and artifact verification checks passing
When the maintainer runs "make release VERSION=v1.1.0"
Then the release script verifies the artifact chain and tests
And updates the version in "pyproject.toml"
And creates an annotated git tag "v1.1.0" with changelog summary
And prints instructions for pushing the release tag to trigger CI publishing
```

#### Scenario 4.2: Abort Release on Dirty Tree or Failing Tests
```gherkin
Given uncommitted git changes or failing unit tests
When the maintainer runs "make release VERSION=v1.1.0"
Then the release script aborts immediately with a descriptive error message
And no git tag is created
And exits with non-zero status
```

---

## 3. Architecture & Interface Contracts

### 3.1 `pyproject.toml` Specification
- PEP 621 metadata: `name = "ai-native-sdlc"`, `version = "1.1.0"`, `requires-python = ">=3.14"`.
- Console scripts: `ai-sdlc = "src.cli:main"`.
- Tool configuration:
  - `[tool.ruff]`: target-version = "py314", line-length = 100.
  - `[tool.pytest.ini_options]`: testpaths = ["tests"].

### 3.2 Codebase Growth Metric Contract
- Scope: Tracked source code matching `src/**/*`, `scripts/**/*`, `tests/**/*`.
- Threshold: $> 25$ source files OR $> 2,500$ LOC.
- Advisory output:
  ```
  💡 [SDLC Scalability Tip]: Codebase has grown to X files (Y LOC).
     Agents may burn extra tokens grepping for cross-file dependencies.
     Recommended: Run 'codegraph init' to enable instant symbol graphs & blast radius detection.
     See: https://github.com/colbymchenry/codegraph
  ```

### 3.3 Release Script Contract (`scripts/release.sh`)
- Usage: `bash scripts/release.sh <VERSION>` (e.g. `v1.1.0`).
- Validations:
  1. Semantic version regex: `^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$`.
  2. Git tree clean: `git diff --quiet && git diff --cached --quiet`.
  3. Verification: `bash scripts/verify.sh` exits 0.
  4. Artifact integrity: `bash scripts/check-artifacts.sh` exits 0.

---

## 4. Policy, Security & Quality Constraints

- **Python Version**: Strict requirement `>=3.14`.
- **Zero Bloat**: No heavy external dependencies; `uv` and `codegraph` are CLI tools.
- **Traceability**: Milestone tracked in `docs/plans/00-ROADMAP.md`.
- **Performance**: Single-command verification runs in < 1 second.
