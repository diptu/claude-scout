# claude-scout — Implementation TODO

> Lazy senior mode: smallest loop first, grow only what hurts. Don't build the architecture for the system you wish you had.

---

## Phase 0 — Kill Scope Before Coding

- [ ] Write a one-page spec answering:
  - [ ] What does a "skill" actually look like as files? (Folder + `SKILL.md` + optional scripts)
  - [ ] What's "high-signal" content? (2–3 hard rules: stars/recency/keyword match)
  - [ ] What's "validated"? (Pass = runs end-to-end on a 3-line test prompt without erroring)
- [ ] Decide the final folder layout (`candidates/`, `drafts/`, `library/`, `trash/`)
- [ ] Write down what you are explicitly **NOT** building yet:
  - [ ] No Docker
  - [ ] No web UI
  - [ ] No plugin system
  - [ ] No multi-agent orchestration
  - [ ] No vector DB / embeddings

**Exit:** one-page spec exists in `docs/spec.md`.

---

## Phase 1 — The Manual Loop

- [ ] Create repo skeleton:
  - [ ] `candidates/` (empty, `.gitkeep`)
  - [ ] `drafts/` (empty, `.gitkeep`)
  - [ ] `library/` (empty, `.gitkeep`)
  - [ ] `trash/` (empty, `.gitkeep`)
  - [ ] `prompts/` (empty for now)
  - [ ] `logs/` (empty, `.gitkeep`)
- [ ] Hand-pick 5–10 seed GitHub repos you already trust
- [ ] Manually paste their READMEs into `candidates/<name>.md`
- [ ] Manually invoke Claude Code on each to generate `drafts/<name>/SKILL.md`
- [ ] Review each draft; move winners to `library/`, losers to `trash/`
- [ ] Actually use 2 of the approved skills twice in real work

**Exit:** 3 skills in `library/` that you've genuinely reused.

---

## Phase 2 — One Automated Source (GitHub only)

- [ ] Add `requirements.txt` with minimum deps (just `requests` to start)
- [ ] Write `harvest_github.py`:
  - [ ] Use GitHub Search API with hardcoded keyword list (`claude skill`, `claude code agent`, `mcp server`)
  - [ ] Filter by stars + recency **server-side** via query params
  - [ ] Dump raw results to `candidates/discovery-YYYY-MM-DD.json`
  - [ ] Maintain `candidates/seen.txt` for dedupe (flat URL list, no DB)
  - [ ] Sleep when `X-RateLimit-Remaining` drops below threshold
- [ ] Wire up `python main.py --mode harvest` as a thin wrapper
- [ ] Add a cron entry / scheduled task to run `harvest` daily
- [ ] Set up a 5-min/day review ritual for new candidates

**Exit:** daily `harvest` yields 2–5 candidates worth eyeballing; review takes <10 min.

---

## Phase 3 — The Build Step (Claude Code as orchestrator)

- [ ] Write `prompts/build.md` — house style for `SKILL.md`, under 200 tokens
- [ ] Write `build.py`:
  - [ ] For each candidate, run `claude -p "<prompt referencing candidate path>"` via `subprocess.run`
  - [ ] Write output to `drafts/<name>/SKILL.md`
  - [ ] Capture stdout/stderr to `logs/build-<timestamp>.log`
  - [ ] Hard timeout: 10 minutes per skill
  - [ ] On failure → move to `drafts/failed/` (no auto-retry)
- [ ] Wire up `python main.py --mode build`
- [ ] Manual review of one week's output to confirm drafts are usable

**Exit:** every candidate produces either a draft or a `failed/` entry; weekly review <15 min.

---

## Phase 4 — The Eval Gate

- [ ] Write `eval.py`:
  - [ ] Hardcoded battery of 3 test prompts in `prompts/eval_tests.md`
  - [ ] For each `drafts/<name>/SKILL.md`, run the battery
  - [ ] Pass = script runs + Claude Code returns non-error
  - [ ] Fail → move to `drafts/failed-reason-eval/`
- [ ] Wire up `python main.py --mode eval`
- [ ] Run on a sample batch; eyeball the false-positive rate

**Exit:** eval processes a batch in <30 min; false-positive rate <20%.

---

## Phase 5 — Library UX

- [ ] Add `meta.json` per skill:
  - [ ] `name`
  - [ ] `tags` (list)
  - [ ] `source_url`
  - [ ] `date_added`
  - [ ] `eval_status`
- [ ] Write `python main.py --mode search <keyword>`:
  - [ ] grep over `meta.json` + filenames
  - [ ] no full-text search, no embeddings
- [ ] Write `python main.py --mode show <name>`:
  - [ ] print the `SKILL.md` for a given skill
- [ ] Smoke-test finding an old skill in <10 seconds

**Exit:** library is findable from the terminal without opening a file manager.

---

## Phase 6 — Add Reddit (second source)

- [ ] Add `praw` to `requirements.txt`
- [ ] Hardcode subreddit list: `r/ClaudeAI`, `r/LocalLLaMA`, `r/Anthropic`
- [ ] Write `harvest_reddit.py`:
  - [ ] Filter: score > 50, comments > 10, last 7 days, keyword match
  - [ ] Same `candidates/discovery-YYYY-MM-DD.json` output format as GitHub
  - [ ] Same `candidates/seen.txt` dedupe
- [ ] **Do NOT** extract a `BaseScraper` class. Duplicate code is cheaper than premature abstraction.
- [ ] Update `harvest` mode to run both

**Exit:** Reddit contributes >20% of candidates that pass eval.

---

## Phase 7 — Sandbox (only when needed)

**Trigger conditions — do NOT start this phase unless one is true:**
- [ ] Running skills you didn't write yourself
- [ ] A skill in `library/` executes arbitrary code without you reading it first
- [ ] Sharing the registry with other people

When triggered:
- [ ] Wrap each eval/build run in a Docker container
- [ ] Limit network access per skill
- [ ] Add `--sandbox docker` flag to `main.py`

**Exit:** untrusted skills can run without risk to your laptop.

---

## Phase 8 — Stop

- [ ] Ship what you have at end of Phase 6
- [ ] Use it for 3 months before adding anything
- [ ] Only build a feature if you find yourself wanting it in real use:
  - [ ] Web UI → only if terminal search is genuinely slow
  - [ ] LLM-as-judge eval → only if 50+ skills and real quality problems
  - [ ] Queue system → only if serial build becomes a bottleneck
  - [ ] Docker → only if Phase 7 triggers fire

---

## Recurring / Ongoing

- [ ] Daily: review new `candidates/` drops (5–10 min)
- [ ] Weekly: review `drafts/`, promote/dump (15 min)
- [ ] Monthly: prune `library/`, refresh `seen.txt`, revisit keyword lists

---

## Guiding Principles (read first when stuck)

1. **The value of this project is 90% in the loop and 10% in the code.** Run the loop manually before automating it.
2. **Two files of duplicated code is cheaper than one premature abstraction.** De-duplicate at three, not two.
3. **Flat files > SQLite until you have 1000+ items.**
4. **`print()` > logging framework until you have a real debugging problem.**
5. **Claude Code is your orchestrator.** Don't build a second one.
6. **Eval measures "does it explode," not "is it good."** Quality is your eyeballs.
7. **If you can't explain why a phase is needed in one sentence, skip it.**
