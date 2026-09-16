# 🦕 Dinosaur Runner Game (AI-Native SDLC Edition)

[![SDLC: AI-Native](https://img.shields.io/badge/SDLC-AI--Native-brightgreen.svg)](docs/plans/00-ROADMAP.md)
[![Agent: DeepSeek Harness](https://img.shields.io/badge/agent-DeepSeek%20Harness-blue.svg)](DSH.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An offline, zero-dependency HTML5 Canvas endless runner browser game inspired by the classic Chromium T-Rex runner, built and maintained entirely through the **AI-Native Software Development Life Cycle (SDLC)**.

---

## 🎮 Quickstart: How to Run and Play

### Option 1: Using Make (Recommended)
```bash
make run
```
This launches the built-in zero-dependency Python server on `http://127.0.0.1:8080`.

### Option 2: Direct Python Command
```bash
python3 -m src.server --port 8080
```

### Option 3: Direct Browser File Access
Open `public/index.html` directly in any modern web browser (Google Chrome, Safari, Firefox, Edge).

---

## 🕹️ Controls & Gameplay

| Action | Desktop Keyboard | Mobile / Touch Screen |
| :--- | :--- | :--- |
| **Start / Jump** | <kbd>Space</kbd> or <kbd>▲</kbd> (Up Arrow) | Tap Canvas or press **JUMP** button |
| **Duck** | <kbd>▼</kbd> (Down Arrow) | Hold **DUCK** button |
| **Pause / Resume** | <kbd>P</kbd> | Tap **PAUSE** button |
| **Mute / Unmute** | <kbd>M</kbd> | Tap **MUTE** button |
| **Restart Game** | <kbd>Space</kbd> or Click **PLAY AGAIN** | Tap **PLAY AGAIN** button |

### Gameplay Mechanics:
- **Procedural Obstacles**: Jump over small, double, and large cacti. Duck beneath high-flying pterodactyls.
- **Speed Progression**: Game scroll speed smoothly increases as your score climbs.
- **Day / Night Cycle**: The visual theme dynamically toggles between Day and Night every 700 points.
- **Audio Synthesis**: Built-in 8-bit retro sound effects generated via Web Audio API (jump sound, 100-point double chime, crash effect) without any external audio files.
- **High Scores**: Automatically saved to your browser's `localStorage`.

---

## 🛠️ Verification & Development Commands

This repository enforces strict, single-command automated verification:

```bash
# Full local verification loop (lint + unit tests + artifact traceability + anti-shortcut scan)
make verify

# Run automated test suite
make test

# Run continuous AI regression evaluation suite
make eval

# Scaffold a new feature intent artifact
make new-intent TITLE="Feature Name"
```

---

## 📁 Repository Structure & SDLC Traceability

All design decisions and implementation steps are tracked in version-controlled Markdown artifacts under `docs/`:

```
dinosaur-game/
├── DSH.md                   # DeepSeek Harness agent instructions & multi-agent mappings
├── AGENTS.md                # Universal AI agent engineering standards
├── CLAUDE.md                # Anthropic Claude Code agent directives
├── GEMINI.md                # Google Antigravity agent directives
├── CODEX.md                 # OpenAI Codex agent directives
├── Makefile                 # Lifecycle commands (run, verify, test, eval)
├── REVIEW.md                # Code review policy & severity tiers (Blocker / Important / Nit)
├── docs/
│   ├── intent/              # Stage 1: Problem statements & user intent
│   ├── specs/               # Stage 2: Technical specifications with Gherkin scenarios
│   ├── plans/               # Stage 3: TDD implementation plans & 00-ROADMAP.md
│   ├── reviews/             # Stage 5: PR review audit reports
│   └── templates/           # Markdown templates for all stages
├── evals/                   # Stage 4/6: Continuous AI evals
├── public/                  # Static web game assets
│   ├── index.html           # HTML5 Canvas layout & HUD
│   ├── game.js              # Canvas rendering engine, physics, Web Audio synthesizer
│   └── style.css            # Responsive layout & retro pixel styling
├── src/
│   ├── engine/physics.py    # Core physics equations, collision detection, and score scaling
│   └── server.py            # Zero-dependency Python HTTP server
└── tests/                   # Automated unit & integration tests
```

---

## 📈 Roadmap & Milestones

See [`docs/plans/00-ROADMAP.md`](docs/plans/00-ROADMAP.md) for complete milestone statuses.
