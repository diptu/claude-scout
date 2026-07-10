# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Implemented and verified end-to-end (real GitHub API + real `claude` CLI calls). Source lives under `src/scout/`, split into `commands/` (build, eval, committee, council, library), `core/` (config, logger, exceptions, util), and `services/` (GitHub/Reddit/X/YouTube/TikTok harvesters, plus shared `harvest_common.py` plumbing), with `main.py` (argparse dispatch) and `__main__.py` (`python -m scout`) at the package root; `tests/` mirrors the same subdirectories. User-editable candidacy criteria (and the hiring-committee and council rubrics) live in `defaults/config.yml` (read by `scout.core.config.load_config`, with built-in fallbacks). Data directories (`candidates/`, `drafts/`, `library/`, `trash/`, `logs/`, `prompts/`) stay at the repo root, not under `src/`.

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
- **Harvest**: pull candidate skills from GitHub (`scout/services/harvest_github.py`, works with no credentials), Reddit (`scout/services/harvest_reddit.py`), X/Twitter (`harvest_twitter.py`), YouTube (`harvest_youtube.py`), and TikTok (`harvest_tiktok.py`) into `candidates/discovery-YYYY-MM-DD.json`, deduped via a flat `candidates/seen.txt`; thresholds and keywords come from `defaults/config.yml`. The four non-GitHub sources each degrade to a no-op without their API credentials configured (Reddit needs `praw`+client id/secret; X/Twitter needs a bearer token; YouTube needs an API key; TikTok needs Research API client credentials, which require application approval). All five duplicate the same fetch-then-decide shape on purpose (CLAUDE.md principle 2), but share the identical seen.txt/library-url/write-candidates bookkeeping via `scout/services/harvest_common.py` — that plumbing was extracted once a fifth near-identical copy would otherwise exist.
- **Build**: shell out to the `claude` CLI (`subprocess.run(["claude", "-p", ...])`) per candidate to draft a `SKILL.md` into `drafts/<name>/`, treating candidate content as untrusted data (see `prompts/build.md`'s `<candidate_data>` delimiters).
- **Eval**: per draft, first ask the `claude` CLI whether the fixed battery (`prompts/eval_tests.md`) applies to that skill — if not, it designs one short tailored test instead — then run the tests via the CLI, writing a `drafts/<name>/.eval_status` sentinel (`passed`/`failed`) and printing a tabular report. Pass/fail only checks "does it explode" (exit codes/timeouts), never answer quality — the LLM designs tests, it never grades.
- **Committee**: `scout/commands/committee.py` — the first of two deliberate exceptions to "eval never judges quality." A fixed panel of exec personas from `defaults/config.yml`'s `committee.voters` (CEO, CTO, Solution Architect, Security Lead, QA Lead by default) each cast one `claude -p` vote per eval-passed draft, scoring it 1-5 on usefulness/uniqueness/quality/safety (`prompts/committee.md`). The average across all successful voters/dimensions decides the quality bar: below `committee.passing_score` moves straight to `trash/` with a `committee_verdict.json` audit record, no human involved. `>= committee.passing_score` ("hired") no longer auto-promotes to `library/` — it's handed to the council gate below. Below `committee.min_voters` successful votes, the draft is left alone for manual `review` rather than decided on partial data. If a draft's name already exists in `library/`, it's skipped entirely (no `claude` calls, no auto-decision) rather than silently overwriting an already-curated entry's hand-set tags/content. A draft that already carries a `committee_verdict.json` (already hired + council-checked on a prior run) is likewise skipped rather than re-voted on.
- **Council**: `scout/commands/council.py` — the second deliberate exception, run automatically for every committee-hired draft before anything is promoted. Mirrors `.claude/skills/llm-council`'s five-advisor-plus-chairman methodology (`prompts/council_advisor.md`, `prompts/council_chairman.md`), scoped to one question: given what's already in `library/`, is this candidate actually worth adding, or is it redundant? Five fixed advisor personas (`defaults/config.yml`'s `council.advisors`) each vote add/skip, then a chairman synthesizes one final decision. "skip" (redundant) trashes the draft automatically, same as a committee reject, with both `committee_verdict.json` and `council_verdict.json` as an audit record. "add" leaves the draft untouched in `drafts/` — committee and council together narrow what reaches a human, they don't replace the human. If the chairman can't reach a usable synthesis (too many advisor calls failed), council fails open to "add" rather than silently trashing a draft on partial data.
- **Review**: a human promotes surviving drafts from `drafts/` into `library/`, or discards to `trash/`, via `scout/commands/library.py`'s interactive `review()` — needed for drafts the committee couldn't reach quorum on, drafts council approved as worth adding, or drafts that predate the committee/council gates.

Folder layout (all at repo root, not under `src/`): `candidates/`, `drafts/` (with `drafts/failed/` and `drafts/failed-reason-eval/`), `library/`, `trash/`, `prompts/`, `logs/`, `docs/`.

## Two competing visions — README.md's aspirational framing loses

`README.md` describes an ambitious multi-agent system (skill battle arena, executive/engineering/QA/research/product voting, skill replacement engine). The `TODO.md`/`MVP.md` files that used to be this repo's tiebreaker (a much leaner, phased build) were deleted in the `V1` commit — the guiding principles they set out are preserved directly below instead. **When `README.md`'s framing conflicts with the principles below, follow the principles, not `README.md`** — most of README's elaborate architecture (plugin system, vector DB, full multi-agent orchestration) is still out of scope. The hiring-committee gate and the council gate below are deliberate, narrow exceptions carved out of principle 6, not a reversion to README's vision — each is still flat files, still a fixed panel of sequential `claude -p` calls, no new orchestrator or framework.

## Guiding principles for implementation

These are load-bearing constraints on how to build this project, not generic advice — follow them over instinct to add structure:

1. The value of this project is 90% in the loop, 10% in the code. Run any new step manually before automating it.
2. Two files of duplicated code is cheaper than one premature abstraction — de-duplicate at three occurrences, not two. (E.g. don't extract a `BaseScraper` class when adding the Reddit source; duplicate `harvest_github.py`'s pattern instead.)
3. Flat files (JSON, `.txt`) over SQLite until there are 1000+ items. No database.
4. `print()` over a logging framework until there's a real debugging problem.
5. Claude Code itself is the orchestrator — don't build a second one (no separate agent framework). The committee panel is still just sequential `claude -p` calls from `committee.py`, not a second orchestrator.
6. Eval only measures "does it run without erroring," never "is it good" — quality judgment was manual-review-only until the hiring-committee gate (`committee.py`) was intentionally added ahead of the original 50+ skill/real-quality-problem trigger, at the user's explicit direction. A second LLM-as-judge gate, the council redundancy check (`council.py`), was added the same way, at the same explicit direction, to sit between a committee "hire" and the human review step. Treat these two as the sanctioned LLM-as-judge paths; don't generalize the pattern into judging elsewhere (e.g. eval.py itself) without the same explicit sign-off.
7. No Docker/sandboxing until one of the Phase 7 trigger conditions fires (running skills you didn't write, a skill executing arbitrary code unreviewed, or sharing the registry with others).
8. If a phase's necessity can't be explained in one sentence, skip it.

## Note on `.claude/skills/`

This repo's `.claude/skills/` directory contains a large number of generic role-based skills (backend, frontend, cloud, ML, etc.). These are general-purpose Claude Code skills available in this environment, not code specific to claude-scout's own domain (skill harvesting/eval) — don't confuse them with the project's actual subject matter.
