# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Hiring-committee gate (`scout/commands/committee.py`, `make committee`): a
  fixed panel of exec personas (CEO, CTO, Solution Architect, Security Lead,
  QA Lead — configurable in `defaults/config.yml`'s `committee.voters`) votes
  on each eval-passed draft, scoring usefulness/uniqueness/quality/safety
  1-5 via `prompts/committee.md`. The average decides automatically:
  promotes to `library/` or rejects to `trash/`, with a
  `committee_verdict.json` audit record either way. Below quorum, or when a
  draft's name collides with an already-curated `library/` entry, the draft
  is left for manual `make review` instead of being auto-decided. Folded
  into `make scout`.

### Changed
- Restructured the package into `commands/` (build, eval, library), `core/`
  (config, logger, exceptions, util), and `services/` (GitHub/Reddit
  harvesters) under `src/scout/`; tests mirror the same layout.
- The CLI is now runnable as `python -m scout` or, once installed, `claude-scout`.

### Added
- `defaults/config.yml` — user-editable candidacy criteria (GitHub minimum
  stars/age/keywords, Reddit minimum score/comments/age/subreddits), with
  built-in fallbacks when the file or a key is absent.

## [0.1.0] - 2026-07-06

### Added
- Discovery → Build → Eval loop: GitHub/Reddit harvest into `candidates/`,
  drafting via the `claude` CLI into `drafts/`, smoke-test eval gate, and
  interactive review promoting drafts into `library/`.
- `search`/`show` over the promoted library.
- CI (ruff + pytest) via GitHub Actions.
