# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
