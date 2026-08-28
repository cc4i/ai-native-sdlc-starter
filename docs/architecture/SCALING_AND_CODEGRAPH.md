# Codebase Intelligence & Scalability: Integrating CodeGraph

> How to scale autonomous AI engineering beyond single files to large, multi-module repositories using [`colbymchenry/codegraph`](https://github.com/colbymchenry/codegraph).

---

## 1. The Context Scaling Challenge in AI Coding

In early-stage projects (under 20 files), AI coding agents easily discover code by searching filenames or running basic `grep`.

However, as repositories grow past **25+ files or 2,500+ lines of code**, agents face three critical failure modes:

1. **Context Blindness & Broken Callers**: An agent modifies a function signature in `src/models/` without knowing that five callers across `src/cli.py`, `src/agent/`, and external consumers depend on the old signature.
2. **Token Bloat & Discovery Drag**: The agent spends 60–80% of its token budget running repetitive `grep` and `find` calls, re-reading entire files to reconstruct dependency paths from scratch.
3. **Slow Regression Testing**: Running full test suites on every micro-step degrades developer velocity.

---

## 2. The Solution: Pre-Indexed Knowledge Graphs

Instead of having the AI re-discover code structure from scratch on every turn, we integrate **[CodeGraph (colbymchenry/codegraph)](https://github.com/colbymchenry/codegraph)** — a battle-tested, 100% local code knowledge graph with 68,000+ stars on GitHub.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AI Agent (Antigravity / ReviewAgent)                            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ MCP Tool Query (codegraph_explore)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               colbymchenry/codegraph (100% Local, Auto-Syncing Daemon)                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  • Blast Radius Analysis       • Cross-File Call Paths      • Symbol Relationships     │
│  • Framework Routes (URLs)     • 20+ Languages Indexed      • Sub-Second File Watcher  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Measured Real-World Efficiency
Benchmarked across major open-source repositories:
- **88% fewer tool calls**: Agents answer directly from graph symbols rather than crawling directory trees.
- **62% fewer tokens consumed**: Surgical symbol context replaces dumping full files into context windows.
- **44% lower execution cost**: Shorter trajectories and faster time-to-green.
- **Sub-second auto-sync**: Rust-native file watcher updates the graph within 300ms of any file edit.

---

## 3. Quickstart: 3-Step Setup

### Step 1: Install the CodeGraph CLI
```bash
# macOS / Linux (no Node.js required, bundles self-contained binary)
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# Or via npm
npm i -g @colbymchenry/codegraph
```

### Step 2: Wire Up Your AI Agents (Antigravity, Gemini, Claude Code, Cursor)
In a fresh terminal, auto-configure the MCP server into your local agent environments:
```bash
codegraph install
```
This automatically registers the CodeGraph MCP server into **Antigravity IDE**, **Gemini CLI**, **Claude Code**, and **Cursor**.

### Step 3: Initialize Your Project Index
In your project root:
```bash
codegraph init
```
This creates `.codegraph/` and generates the cross-file symbol index. The native file watcher auto-syncs subsequent edits in the background.

---

## 4. How AI Agents Leverage CodeGraph Across the SDLC

### Stage 2 (Design) & Stage 3 (Build): Blast Radius Sizing
When writing `docs/plans/NNN-title.md`, the `architect` and `engineer` agents query `codegraph_explore`:
> *"What calls `ReviewAgent.review_files` and what are all dependent types?"*

CodeGraph returns the exact symbol hierarchy, callers, and test files. This prevents unexpected regressions before a single line of code is written.

### Stage 4 (Test): Test Impact Analysis (TIA)
Instead of executing long integration test runs on minor edits, the agent queries which test suites cover the modified symbols, keeping the inner feedback loop under 1 second.

### Stage 5 (Deploy): Context-Aware PR Reviews
The autonomous `ReviewAgent` cross-checks diffs against caller signatures in `.codegraph/`, instantly catching breaking interface changes across un-staged files.

---

## 5. Repository Scalability Growth Triggers

Our verification harness ([`scripts/verify.sh`](../../scripts/verify.sh)) automatically counts tracked source files and lines of code.

When your codebase exceeds **25 source files or 2,500 LOC** and `.codegraph/` is not present, `make verify` surfaces an advisory notice:
```
💡 [SDLC Scalability Tip]: Codebase has grown to 32 files (3,400 LOC).
   AI agents may burn excess tokens or encounter context blindness grepping flat files.
   Recommended: Run 'codegraph init' to enable instant symbol indexing & blast radius detection.
   Powered by: https://github.com/colbymchenry/codegraph (colbymchenry/codegraph)
```

Initializing CodeGraph immediately suppresses the advisory.
