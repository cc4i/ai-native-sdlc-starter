---
name: intent-capture
description: Elicit, interview, and formalize raw user requirements and ideas into a structured intent.md proto-spec. Trigger whenever starting a new feature, discussing user requirements, or running the planning loop.
---

# Intent Capture Skill

Use this skill when a user or team member brings an idea, problem, or feature request to the repository.

## 🎯 Process
1. **Interactive Grilling**: Ask targeted questions like an experienced product analyst:
   - What specific problem does this solve?
   - Who is affected today, and what is the current workaround?
   - What does a successful outcome look like?
   - What are the hard security, latency, or compliance constraints?
   - What is explicitly OUT of scope for this iteration?
2. **Synthesize**: Format findings into a draft adhering strictly to `templates/intent.template.md`.
3. **Save**: Save to `intent/NNN-[feature-slug].md`.
4. **Handoff**: Prompt the user to review and correct any assumptions before marking approved.
