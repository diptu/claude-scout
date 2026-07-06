# claude-scout — User Manual

claude-scout discovers, drafts, and evaluates Claude Code skills through one
loop: **Harvest → Build → Eval → Review**. This manual covers day-to-day use
of the CLI. For the internal architecture, see `CLAUDE.md`.

## 1. Setup

```
make install-dev
```

Installs runtime deps (`requests`, `praw`, `pyyaml`) plus dev tools (`pytest`,
`ruff`, `mypy`, `pylint`, `bandit`).

Requirements:
- Python 3.13+
- The `claude` CLI on your `PATH` — used by `build` and `eval`. Without it,
  `build` fails per-candidate and `eval` degrades to a frontmatter-only check
  (see §4).
- Optional: `GITHUB_TOKEN` env var — raises your GitHub API rate limit for
  `harvest`. Works without it, just slower.
- Optional: `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` env vars — required
  for the Reddit half of `harvest`. Without them (or without `praw`
  installed), Reddit harvesting silently no-ops — it returns `0 new` rather
  than erroring, so don't read "0 new from Reddit" as "nothing matched."

Always run through `make`, not `python3 -m scout` directly — the Makefile is
the single source of truth for how each stage is invoked.

## 2. The loop, end to end

```
make harvest LIMIT=20       # pull candidates from GitHub + Reddit
make build LIMIT=20         # draft a SKILL.md per candidate via `claude`
make eval                   # smoke-test each draft
make review                 # you promote survivors to library/, or trash them
```

Or run harvest+build+eval in one shot with `make scout LIMIT=20` (review is
always manual — it's the human quality gate).

## 3. Harvest

```
make harvest                          # all sources, no limit
make harvest LIMIT=20                 # cap total new candidates at 20
make harvest GITHUB_ONLY=1            # skip Reddit even if configured
make harvest LIMIT=20 GITHUB_ONLY=1   # combine
```

- Pulls repos from GitHub search and posts from configured subreddits,
  filtered by `defaults/config.yml` (stars/score thresholds, age window,
  keywords — edit that file to tighten or loosen what counts as a
  candidate).
- New candidates land in `candidates/discovery-YYYY-MM-DD.json`.
- Every discovered URL is recorded in `candidates/seen.txt` so re-running
  harvest never re-adds the same repo/post twice.
- URLs already promoted into `library/` are also skipped automatically,
  independent of `seen.txt` — so a `reset-harvest` (below) won't cause
  already-curated skills to come back as candidates.
- `Makefile` flags are `make`-variables, not CLI flags — use `LIMIT=20`, not
  `--limit=20`.

### Resetting harvest state

```
make reset-harvest
```

Deletes all `candidates/discovery-*.json` files and `candidates/seen.txt` so
the next harvest starts clean under your current `config.yml`. Useful after
tightening criteria, since harvest never retroactively re-validates or prunes
candidates already on disk. It's interactive — it lists what it's about to
delete and asks `Proceed? [y/N]` before touching anything. Candidates not yet
built are lost permanently; anything already in `drafts/`, `library/`, or
`trash/` is untouched.

## 4. Build

```
make build LIMIT=20
```

For each undrafted candidate, shells out to `claude -p <prompt>` (see
`prompts/build.md`) to write a `SKILL.md` into `drafts/<name>/`. Candidates
already drafted or already in `drafts/failed/` are skipped automatically —
safe to re-run.

Failures (timeout, nonzero exit, empty output) move the candidate's data into
`drafts/failed/<name>/candidate.json` rather than retrying forever.

## 5. Eval

```
make eval
```

Only checks "does it run," never "is it good" (quality judgment is manual,
via `review`). For each undrafted-but-unevaluated draft:

1. If `SKILL.md`'s frontmatter is missing `name:`/`description:`, it fails
   immediately — no `claude` call needed.
2. Otherwise, if the `claude` CLI is unavailable, it passes on the
   frontmatter check alone (`battery: frontmatter-only`) — a degraded pass,
   not a full evaluation.
3. Otherwise, it first asks `claude` whether the fixed test battery
   (`prompts/eval_tests.md`) makes sense for this particular skill. If yes,
   it runs that battery (`battery: standard`); if no, `claude` designs one
   short tailored test instead (`battery: custom`) and that's what runs.
4. Pass/fail is exit codes and timeouts only — the LLM designs tests, it
   never grades answers.

Output is a table:

```
| skill      | battery  | tests | result | reason                          |
|------------|----------|-------|--------|---------------------------------|
| skill-a    | standard |     3 | passed |                                 |
| skill-b    | custom   |     1 | failed | prompt 1/1 exited 1: crashed... |
```

The `reason` column is populated only on failure — a short, truncated
explanation (missing frontmatter, which prompt failed and how). Passing
drafts get a `.eval_status` sentinel and stay in `drafts/`; failing drafts
move to `drafts/failed-reason-eval/`. Full transcripts land in
`logs/eval-<timestamp>-<name>.log`.

## 6. Review

```
make review
```

Interactive. For each eval-passed draft, prints the first 400 chars of its
`SKILL.md` and asks:

- `p` — promote to `library/<name>/` (you'll be asked for optional
  comma-separated tags). You're then asked `also add to .claude/skills/?
  [y/N]` — say `y` to copy the same `SKILL.md` into `.claude/skills/<name>/`
  so it's usable as a local skill immediately, in addition to being tracked
  in `library/`.
- `t` — discard to `trash/<name>/`.
- `s` (or anything else) — skip, leave it for next time.
- `q` — quit the review session early.

## 7. Search and show

```
make search KEYWORD=git              # substring match across library/ + .claude/skills/
make show NAME=ai-engineer            # print a skill's full SKILL.md
```

`search`/`show` look in both `library/` (promoted skills) and
`.claude/skills/` (skills already available in this environment, including
generic ones like `ai-engineer` that didn't come through this pipeline) — so
a draft still sitting in `drafts/` won't show up until it's promoted via
`review`. To read an unreviewed draft directly:

```
cat drafts/<name>/SKILL.md
```

## 8. Finding a better alternative to an existing skill

There's no automated "replace this skill" feature — quality judgment is
always manual here. To evaluate whether something better exists for a given
niche (e.g. `ai-engineer`):

1. `make show NAME=ai-engineer` — read the current skill as your baseline.
2. Narrow `defaults/config.yml`'s `github.keywords` (and `reddit.keywords`)
   to terms specific to that niche instead of the generic defaults.
3. `make harvest LIMIT=10 GITHUB_ONLY=1` — scoped discovery.
4. `make build LIMIT=10` then `make eval` — draft and smoke-test candidates.
5. Manually read each surviving draft against your baseline — eval only
   proves "doesn't explode," not "is better."
6. `make review` to promote a genuine improvement (optionally also into
   `.claude/skills/`).
7. If replacing the old skill outright, remove `.claude/skills/<old-name>/`
   yourself — nothing here does that automatically.

## 9. Command reference

| Command | What it does |
|---|---|
| `make install` / `make install-dev` | Install runtime / runtime+dev dependencies |
| `make harvest [LIMIT=N] [GITHUB_ONLY=1]` | Discover new candidates |
| `make reset-harvest` | Wipe discovery files + seen.txt (interactive confirm) |
| `make build [LIMIT=N]` | Draft `SKILL.md` for undrafted candidates |
| `make eval` | Smoke-test undrafted-but-unevaluated drafts |
| `make scout [LIMIT=N]` | harvest + build + eval, one shot |
| `make search KEYWORD=...` | Substring search across `library/` + `.claude/skills/` |
| `make show NAME=...` | Print a skill's full `SKILL.md` |
| `make review` | Interactively promote/trash eval-passed drafts |
| `make lint` / `make mypy` / `make pylint` / `make bandit` / `make test` | Individual checks |
| `make check` | Everything CI runs (lint + mypy + pylint + bandit + test) |
| `make clean` | Remove `__pycache__`/`.pytest_cache`/`.ruff_cache` |

## 10. Folder layout

All at repo root, not under `src/`:

- `candidates/` — raw harvest output (`discovery-*.json`) + `seen.txt` dedup log
- `drafts/` — in-progress skills (`failed/` and `failed-reason-eval/` subfolders for build/eval failures)
- `library/` — promoted, curated skills (`meta.json` + `SKILL.md` per skill)
- `trash/` — discarded drafts
- `logs/` — per-run transcripts and stage summaries
- `prompts/` — prompt templates fed to `claude` for build/eval
- `.claude/skills/` — skills actually usable in this environment (generic ones plus anything you opted to also add during review)

## 11. Single test

```
python3 -m pytest tests/commands/test_build.py::test_skip_already_drafted -v
```

`tests/conftest.py` puts `src/` on `sys.path` for imports to resolve.
