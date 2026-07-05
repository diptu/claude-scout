<div align="center">

# 🕵️‍♂️ claude-scout
**The Autonomous Intelligence Gathering & Prototyping Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude-Code](https://img.shields.io/badge/Powered%20by-Claude%20Code-orange)](https://github.com/anthropics/claude-code)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

*Automating the discovery, validation, and curation of emerging Claude skills.*

</div>

---

## 🚀 Overview
`claude-scout` is an autonomous intelligence gathering and rapid prototyping engine designed to discover, validate, and curate emerging Claude-based skills. In a rapidly evolving ecosystem, it’s hard to keep track of the most effective patterns and skills appearing in public forums and repositories. `claude-scout` solves this by automating the **Discovery → Build → Evaluate** loop.

## 🛠 Tech Stack
<div align="left">

| Category | Technology |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Agentic Core** | ![Claude](https://img.shields.io/badge/Claude-000000?style=for-the-badge&logo=anthropic&logoColor=white) |
| **Sandbox** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| **Data Ingestion**| ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) ![Reddit](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white) |

## Project Structure
```
claude-scout/
├── pyproject.toml              # packaging, deps, [project.scripts] entry point
├── README.md
├── Dockerfile
├── docker-compose.yml          # CLI runtime + optional api profile
├── .env.example                # documented env vars
├── .github/
│   └── workflows/
│       └── ci.yml              # pytest on PR
├── src/
│   └── claude_scout/           # src/ layout prevents accidental root imports
│       ├── __init__.py
│       ├── __main__.py         # `python -m claude_scout` works
│       ├── cli/                # Click commands (the only required surface)
│       │   ├── __init__.py
│       │   ├── main.py         # Click group; registers all subcommands
│       │   ├── errors.py       # friendly error formatting for the terminal
│       │   └── commands/
│       │       ├── harvest.py  # `claude-scout harvest`
│       │       ├── build.py    # `claude-scout build`
│       │       ├── eval.py     # `claude-scout eval`
│       │       ├── search.py   # `claude-scout search <kw>`
│       │       ├── show.py     # `claude-scout show <name>`
│       │       ├── review.py   # `claude-scout review`
│       │       └── scout.py    # `claude-scout scout` (full loop)
│       ├── config.py           # pydantic-settings (env + .env file)
│       ├── logging.py          # structlog setup (JSON in prod, pretty in dev)
│       ├── domain/             # pure data types; no I/O
│       │   ├── candidate.py
│       │   ├── skill.py
│       │   └── job.py
│       ├── services/           # business logic; framework-agnostic
│       │   ├── scout_service.py    # orchestrates harvest→build→eval
│       │   ├── harvest_github.py
│       │   ├── harvest_reddit.py   # stub until Phase 6
│       │   ├── builder.py          # wraps `claude -p` subprocess
│       │   └── evaluator.py        # frontmatter + size + test battery
│       ├── sources/            # data-source adapters (the "ports")
│       │   ├── base.py             # tiny Protocol — only when you have 3+
│       │   └── github.py           # GitHub-specific HTTP logic
│       ├── storage/            # persistence adapters
│       │   ├── files.py            # current flat-file impl (default)
│       │   └── db.py               # SQLAlchemy impl (opt-in via config)
│       ├── http/               # OPTIONAL FastAPI layer
│       │   ├── README.md           # "build only when triggered"
│       │   ├── app.py              # FastAPI app factory
│       │   ├── deps.py             # DI wiring
│       │   ├── routers/
│       │   │   ├── skills.py
│       │   │   ├── candidates.py
│       │   │   └── jobs.py
│       │   └── schemas.py          # Pydantic request/response models
│       └── prompts/            # bundled prompt templates
│           ├── build.md
│           └── eval_tests.md
├── tests/
│   ├── conftest.py             # fixtures: CliRunner, mock HTTP, tmp data dirs
│   ├── unit/
│   │   ├── test_harvest_github.py  # mocked requests
│   │   ├── test_builder.py         # mocked subprocess
│   │   ├── test_evaluator.py       # frontmatter parsing edge cases
│   │   ├── test_config.py          # env var loading
│   │   └── test_storage_files.py   # dedupe, read/write
│   └── integration/
│       ├── test_cli.py             # Click CliRunner end-to-end
│       └── test_full_loop.py       # harvest→build→eval on fixtures
├── data/                       # runtime data (gitignored)
│   ├── candidates/
│   │   ├── seen.txt
│   │   ├── seed/
│   │   └── discovery-*.json
│   ├── drafts/
│   ├── library/
│   ├── trash/
│   └── logs/
├── docs/
│   ├── architecture.md         # the why behind this layout
│   ├── adding-a-source.md      # how to add Reddit / HN / etc.
│   ├── hardening-roadmap.md    # what to add when (and what NOT to add)
│   └── why-not-fastapi.md      # short, links the reasoning
└── scripts/
    ├── run-harvest.sh          # cron entry: harvest + rotate logs
    └── dev-setup.sh            # one-shot dev env bootstrap
```

</div>

## 🏗 Project Architecture
*   **Intelligence Layer:** Python-based scrapers (GitHub API, PRAW) scheduled to identify high-signal content.
*   **Orchestration Layer:** Agentic workflows (utilizing Claude Code) that interpret system prompts and execute code generation.
*   **Library Layer:** A structured repository of validated skills, searchable and tagged for your ML and Software Engineering workflows.

## ⚡ Quick Start

### Prerequisites
- [Claude Code](https://github.com/anthropics/claude-code) installed and authenticated.
- Python 3.10+
- Docker (for isolated sandbox environments).

### Installation
```bash
git clone [https://github.com/yourusername/claude-scout.git](https://github.com/yourusername/claude-scout.git)
cd claude-scout
pip install -r requirements.txt

### Usage
To start the scout, run:
```bash
python main.py --mode scout
```
This will scan for new skills, queue them for incubation, and prepare the demo builds for your review.

## Goal
The ultimate objective of `claude-scout` is to maintain a high-quality, verified registry of Claude skills that can be leveraged for advanced machine learning and software engineering workflows.

---
*Built as part of an ongoing commitment to mastering modern AI development and agentic system design.*
