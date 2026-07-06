# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Implemented and verified end-to-end (real GitHub API + real `claude` CLI calls). Source lives under `src/` (`src/main.py`, `src/scout/`); data directories (`candidates/`, `drafts/`, `library/`, `trash/`, `logs/`, `prompts/`) stay at the repo root, not under `src/`.

## Commands

Use the `Makefile` rather than invoking `python` directly — it's the single source of truth for how to run anything here:

```
make install-dev        # runtime deps (requests, praw) + pytest, ruff
make check               # lint (ruff) + test (pytest) — what CI runs
make harvest             # --mode harvest (LIMIT=N, GITHUB_ONLY=1 to scope)
make build               # --mode build (LIMIT=N)
make eval                # --mode eval
make scout               # --mode scout (harvest + build + eval, in-process)
make search KEYWORD=git  # --mode search
make show NAME=<name>    # --mode show
make review              # --mode review (interactive)
```

A single test: `python3 -m pytest tests/test_build.py::test_skip_already_drafted -v` (module import resolves via `tests/conftest.py`, which puts `src/` on `sys.path`).

## What this project is

claude-scout is a CLI tool that automates discovering, drafting, and evaluating Claude Code skills:

**Discovery → Build → Eval** loop:
- **Harvest**: pull candidate skills from GitHub (`scout/harvest_github.py`) and Reddit (`scout/harvest_reddit.py`, degrades to a no-op without `praw`/credentials configured) into `candidates/discovery-YYYY-MM-DD.json`, deduped via a flat `candidates/seen.txt`.
- **Build**: shell out to the `claude` CLI (`subprocess.run(["claude", "-p", ...])`) per candidate to draft a `SKILL.md` into `drafts/<name>/`, treating candidate content as untrusted data (see `prompts/build.md`'s `<candidate_data>` delimiters).
- **Eval**: run a fixed battery of test prompts (`prompts/eval_tests.md`) against each draft via the `claude` CLI, writing a `drafts/<name>/.eval_status` sentinel (`passed`/`failed`); pass/fail only checks "does it explode," not skill quality.
- **Review**: a human promotes surviving drafts from `drafts/` into `library/`, or discards to `trash/`, via `scout/library.py`'s interactive `review()`.

Folder layout (all at repo root, not under `src/`): `candidates/`, `drafts/` (with `drafts/failed/` and `drafts/failed-reason-eval/`), `library/`, `trash/`, `prompts/`, `logs/`, `docs/`.

## Two competing visions — TODO.md/MVP.md win

`README.md` describes an ambitious multi-agent system (skill battle arena, executive/engineering/QA/research/product voting, skill replacement engine). `TODO.md` and `MVP.md` describe a much leaner, phased build. **When there's a conflict, follow `TODO.md`/`MVP.md`, not `README.md`'s aspirational framing** — the guiding principles in `TODO.md` explicitly reject the elaborate architecture (no plugin system, no multi-agent orchestration, no vector DB) in favor of shipping the smallest loop first and growing only what hurts.

## Guiding principles for implementation (from TODO.md)

These are load-bearing constraints on how to build this project, not generic advice — follow them over instinct to add structure:

1. The value of this project is 90% in the loop, 10% in the code. Run any new step manually before automating it.
2. Two files of duplicated code is cheaper than one premature abstraction — de-duplicate at three occurrences, not two. (E.g. don't extract a `BaseScraper` class when adding the Reddit source; duplicate `harvest_github.py`'s pattern instead.)
3. Flat files (JSON, `.txt`) over SQLite until there are 1000+ items. No database.
4. `print()` over a logging framework until there's a real debugging problem.
5. Claude Code itself is the orchestrator — don't build a second one (no separate agent framework).
6. Eval only measures "does it run without erroring," never "is it good" — quality judgment is manual review (LLM-as-judge is explicitly deferred, only reconsidered at 50+ skills with real quality problems).
7. No Docker/sandboxing until one of the Phase 7 trigger conditions fires (running skills you didn't write, a skill executing arbitrary code unreviewed, or sharing the registry with others).
8. If a phase's necessity can't be explained in one sentence, skip it.

Build in the phase order laid out in `TODO.md` (Phase 0 spec → Phase 1 manual loop → Phase 2 GitHub harvest → Phase 3 build step → Phase 4 eval gate → Phase 5 library search/show → Phase 6 Reddit source → Phase 7 sandbox only if triggered → Phase 8 stop and use it for 3 months). Don't jump ahead to later-phase features (web UI, vector search, queueing) unless the corresponding exit criteria/trigger in `TODO.md` is met.

## Note on `.claude/skills/`

This repo's `.claude/skills/` directory contains a large number of generic role-based skills (backend, frontend, cloud, ML, etc.). These are general-purpose Claude Code skills available in this environment, not code specific to claude-scout's own domain (skill harvesting/eval) — don't confuse them with the project's actual subject matter.
