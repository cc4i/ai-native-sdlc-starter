---
name: adversarial-review
description: Conduct multi-perspective adversarial review on specs, plans, and diffs. Categorize findings into Blocker, Important, and Nit per REVIEW.md.
---

# Adversarial Review Skill

Use this skill when auditing specs, plans, or code diffs before human commit sign-off.

## 🎯 Review Posture: Default to Skepticism
Assume the proposed document or code change has hidden defects, missing edge cases, or false assumptions.

## 🔍 Three Review Passes:
1. **Spec / Intent Fidelity Pass**: Does the implementation satisfy all Gherkin acceptance criteria without omitting requirements?
2. **Security & Boundary Pass**: Are there auth bypasses, unvalidated inputs, data leaks, or unhandled errors?
3. **Anti-Shortcut Pass**: Are there hidden `TODO` comments, fake mock implementations in production paths, or disabled tests?

## 📊 Output Format
Generate an audit report adhering strictly to `templates/review.template.md` with explicit severity classifications (`Blocker`, `Important`, `Nit`).
