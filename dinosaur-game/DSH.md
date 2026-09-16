# DeepSeek Harness Directives (DSH.md)

This file provides system instructions, conventions, and operational workflows for **DeepSeek Harness (DSH)** autonomous coding agents and Web GUI sessions operating in this repository.

---

## 🎯 Primary Directives & Workflow Loop

We follow the strict **AI-Native SDLC** lifecycle:
1. **Never write non-trivial code without an approved plan.md** in plans/.
2. **Ground all plans in specs/ and intent/**.
3. **Strict Test-Driven Development (TDD)**: Failing test in tests/ -> minimal code -> refactor -> verify.
4. **Single-Command Verification**: Run make verify (or ./scripts/verify.sh) before declaring complete.
5. **Project-Local Environment Isolation**: Caches and environments remain strictly inside workspace (UV_CACHE_DIR=.uv_cache).
6. **Branch-First Development**: Always create a feature branch (feat/NNN-title).

---

## ⚡ DSH Native Tools & Skills
- Skills available in `.agents/skills/`: `intent-capture`, `spec-architect`, `secure-api-design`, `adversarial-review`, `verifier-loop`.
- Multi-agent delegation: `subagent` and `subagent_fork` for fresh-context delegation.
- Orchestration: `workflow` for JS-based parallel reviews; `ralph` for fresh-agent iteration.
