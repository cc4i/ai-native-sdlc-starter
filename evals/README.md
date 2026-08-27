# Continuous AI Evaluation Suite (`evals/`)

This directory contains regression evaluations that test Antigravity's capability, prompt alignment, and adherence to project skills/rules.

## 🎯 Why Continuous Evals?
In the AI-Native SDLC, **evals are the equivalent of CI regression tests for AI agent instructions**. Whenever you update:
- `GEMINI.md`
- `.gemini/skills/`
- `.gemini/agents/`
- `REVIEW.md`

The eval runner executes the suite non-interactively to ensure that agent outputs still meet required quality, security, and architectural standards.

## 🏃 Running Evals
```bash
make eval
# Or directly:
python3 evals/run_evals.py
```

## ➕ Adding New Eval Cases
Edit `evals/eval-config.json` and add a new test scenario with expected assertion keywords, required file modifications, and scoring criteria.
Whenever a production bug occurs (Stage 6), create an eval case to prevent recurrence!
