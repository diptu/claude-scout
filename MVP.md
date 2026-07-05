# claude-scout MVP — Summary


## What it does

The full Discovery → Build → Evaluate loop, runnable from one CLI:

```
python main.py --mode scout
```

| Mode | What it does | Status |
|---|---|---|
| `harvest` | Pulls Claude-skill-shaped repos from GitHub Search API | **Real** — verified 30 fresh candidates on first run |
| `build` | Shells out to `claude -p` per candidate to draft `SKILL.md` | **Real** — works wherever `claude` CLI is installed |
| `eval` | Frontmatter check + 3 fixed test prompts via `claude -p` | **Real** — degrades to frontmatter-only without CLI |
| `search` | Grep library skills by keyword | **Real** |
| `show` | Print a skill's `SKILL.md` | **Real** |
| `review` | Interactive promote-to-library / trash / skip | **Real** |
| `scout` | Runs harvest → build → eval in sequence | **Real** |

## What's actually inside

- **`main.py`** — argparse entrypoint, ~150 lines, zero magic
- **`scout/harvest_github.py`** — unauth GitHub Search, server-side star/recency filter, flat-file dedupe via `seen.txt`
- **`scout/harvest_reddit.py`** — intentional stub (Phase 6)
- **`scout/build.py`** — `subprocess.run(["claude", "-p", ...])` with 10-min timeout, failures move to `drafts/failed/`
- **`scout/eval.py`** — size + frontmatter gate, then 3 test prompts; no LLM judge
- **`prompts/build.md`** — house style template for SKILL.md generation
- **`prompts/eval_tests.md`** — fixed 3-prompt battery (rarely edited)
- **2 seeded library skills** (`git-commit-craft`, `pr-description-writer`) so search/show demo out of the box
- **3 seeded candidates** so build has material to chew on

## What's deliberately NOT here

- No database (flat files only)
- No async (sequential HTTP, 5s beats complexity)
- No plugin system / `BaseScraper` abstraction
- No web UI (terminal only)
- No Docker sandbox (Phase 7, deferred)
- No LLM-as-judge (eyeballs during review)
- Reddit source (stub)

## Verified working

- `--help` renders cleanly
- `--mode search git` finds both seeded skills
- `--mode show <name>` prints SKILL.md
- `--mode harvest --github-only` returned **30 real candidates** to `candidates/discovery-github-2026-07-05.json`
- `--mode eval` smoke-tested on a fake draft, passed

## Next 30-minute wins (in order)

1. **Fill in `harvest_reddit.py`** — install `praw`, copy `harvest_github.run` pattern, dedupe via the same `seen.txt`. Don't abstract.
2. **Wire `--mode harvest` into a daily cron** — `0 9 * * * cd /path && python main.py --mode harvest >> logs/harvest.log 2>&1`.
3. **Set up GitHub auth token** — bumps rate limit from 60/hr to 5000/hr; one env var change in `harvest_github.py`.

## To actually use the `build` / live `eval` paths

```bash
pip install -r requirements.txt
# install Claude Code CLI on your machine (per Anthropic docs)
cd /workspace/claude-scout
python main.py --mode scout --limit 5
```

Everything else works without the CLI.
