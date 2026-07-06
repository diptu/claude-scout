# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Implemented and verified end-to-end (real GitHub API + real `claude` CLI calls). Source lives under `src/scout/`, split into `commands/` (build, eval, committee, library), `core/` (config, logger, exceptions, util), and `services/` (GitHub/Reddit harvesters), with `main.py` (argparse dispatch) and `__main__.py` (`python -m scout`) at the package root; `tests/` mirrors the same subdirectories. User-editable candidacy criteria (and the hiring-committee rubric) live in `defaults/config.yml` (read by `scout.core.config.load_config`, with built-in fallbacks). Data directories (`candidates/`, `drafts/`, `library/`, `trash/`, `logs/`, `prompts/`) stay at the repo root, not under `src/`.

## Commands

Use the `Makefile` rather than invoking `python` directly — it's the single source of truth for how to run anything here:

```
make install-dev        # runtime deps + dev tools (pytest, ruff, mypy, pylint, bandit)
make check               # lint + mypy + pylint + bandit + test — what CI runs
make harvest             # --mode harvest (LIMIT=N, GITHUB_ONLY=1 to scope)
make build               # --mode build (LIMIT=N)
make eval                # --mode eval
make committee           # --mode committee (hiring-committee vote: auto promote/reject)
make scout               # --mode scout (harvest + build + eval + committee, in-process)
make search KEYWORD=git  # --mode search (covers library/ and .claude/skills/)
make show NAME=<name>    # --mode show (e.g. NAME=ai-engineer)
make review              # --mode review (interactive fallback for no-quorum drafts)
```

A single test: `python3 -m pytest tests/commands/test_build.py::test_skip_already_drafted -v` (module import resolves via `tests/conftest.py`, which puts `src/` on `sys.path`).

## What this project is

claude-scout is a CLI tool that automates discovering, drafting, and evaluating Claude Code skills:

**Discovery → Build → Eval → Committee** loop:
- **Harvest**: pull candidate skills from GitHub (`scout/services/harvest_github.py`) and Reddit (`scout/services/harvest_reddit.py`, degrades to a no-op without `praw`/credentials configured) into `candidates/discovery-YYYY-MM-DD.json`, deduped via a flat `candidates/seen.txt`; thresholds come from `defaults/config.yml`.
- **Build**: shell out to the `claude` CLI (`subprocess.run(["claude", "-p", ...])`) per candidate to draft a `SKILL.md` into `drafts/<name>/`, treating candidate content as untrusted data (see `prompts/build.md`'s `<candidate_data>` delimiters).
- **Eval**: per draft, first ask the `claude` CLI whether the fixed battery (`prompts/eval_tests.md`) applies to that skill — if not, it designs one short tailored test instead — then run the tests via the CLI, writing a `drafts/<name>/.eval_status` sentinel (`passed`/`failed`) and printing a tabular report. Pass/fail only checks "does it explode" (exit codes/timeouts), never answer quality — the LLM designs tests, it never grades.
- **Committee**: `scout/commands/committee.py` — the one deliberate exception to "eval never judges quality." A fixed panel of exec personas from `defaults/config.yml`'s `committee.voters` (CEO, CTO, Solution Architect, Security Lead, QA Lead by default) each cast one `claude -p` vote per eval-passed draft, scoring it 1-5 on usefulness/uniqueness/quality/safety (`prompts/committee.md`). The average across all successful voters/dimensions decides the outcome automatically: `>= committee.passing_score` promotes straight to `library/`, otherwise it moves to `trash/` — both with a `committee_verdict.json` audit record. Below `committee.min_voters` successful votes, the draft is left alone for manual `review` rather than decided on partial data. If a draft's name already exists in `library/`, it's skipped entirely (no `claude` calls, no auto-decision) rather than silently overwriting an already-curated entry's hand-set tags/content.
- **Review**: a human promotes surviving drafts from `drafts/` into `library/`, or discards to `trash/`, via `scout/commands/library.py`'s interactive `review()` — now only needed for drafts the committee couldn't reach quorum on (or that predate the committee gate).

Folder layout (all at repo root, not under `src/`): `candidates/`, `drafts/` (with `drafts/failed/` and `drafts/failed-reason-eval/`), `library/`, `trash/`, `prompts/`, `logs/`, `docs/`.

## Two competing visions — README.md's aspirational framing loses

`README.md` describes an ambitious multi-agent system (skill battle arena, executive/engineering/QA/research/product voting, skill replacement engine). The `TODO.md`/`MVP.md` files that used to be this repo's tiebreaker (a much leaner, phased build) were deleted in the `V1` commit — the guiding principles they set out are preserved directly below instead. **When `README.md`'s framing conflicts with the principles below, follow the principles, not `README.md`** — most of README's elaborate architecture (plugin system, vector DB, full multi-agent orchestration) is still out of scope. The hiring-committee gate below is a deliberate, narrow exception carved out of principle 6, not a reversion to README's vision — it's still flat files, still one fixed panel of `claude -p` calls, no new orchestrator or framework.

## Guiding principles for implementation

These are load-bearing constraints on how to build this project, not generic advice — follow them over instinct to add structure:

1. The value of this project is 90% in the loop, 10% in the code. Run any new step manually before automating it.
2. Two files of duplicated code is cheaper than one premature abstraction — de-duplicate at three occurrences, not two. (E.g. don't extract a `BaseScraper` class when adding the Reddit source; duplicate `harvest_github.py`'s pattern instead.)
3. Flat files (JSON, `.txt`) over SQLite until there are 1000+ items. No database.
4. `print()` over a logging framework until there's a real debugging problem.
5. Claude Code itself is the orchestrator — don't build a second one (no separate agent framework). The committee panel is still just sequential `claude -p` calls from `committee.py`, not a second orchestrator.
6. Eval only measures "does it run without erroring," never "is it good" — quality judgment was manual-review-only until the hiring-committee gate (`committee.py`) was intentionally added ahead of the original 50+ skill/real-quality-problem trigger, at the user's explicit direction. Treat this as the one sanctioned LLM-as-judge path; don't generalize it into judging elsewhere (e.g. eval.py itself) without the same explicit sign-off.
7. No Docker/sandboxing until one of the Phase 7 trigger conditions fires (running skills you didn't write, a skill executing arbitrary code unreviewed, or sharing the registry with others).
8. If a phase's necessity can't be explained in one sentence, skip it.

## Note on `.claude/skills/`

This repo's `.claude/skills/` directory contains a large number of generic role-based skills (backend, frontend, cloud, ML, etc.). These are general-purpose Claude Code skills available in this environment, not code specific to claude-scout's own domain (skill harvesting/eval) — don't confuse them with the project's actual subject matter.
