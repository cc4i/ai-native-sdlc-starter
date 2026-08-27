# Stage 1: Intent Artifacts (`intent/`)

This directory houses all Stage 1 proto-specifications representing raw user problems, business requests, and incident remediation intents.

## 🎯 Rules
1. **Originator's Voice**: Captured in plain language using the template in `templates/intent.template.md`.
2. **Interactive Grilling**: Use slash command `/grill-me` or ask Antigravity to interview you before drafting.
3. **Commit & Sign-off**: Every intent must be committed and approved by the Product Owner before advancing to Stage 2 (`specs/`).

## 📄 File Naming Convention
- `NNN-feature-name.md` (e.g., `001-claims-status-self-service.md`)
- `incident-INC-NNN.md` for automated maintenance incidents (e.g., `incident-001-db-pool-starvation.md`)
