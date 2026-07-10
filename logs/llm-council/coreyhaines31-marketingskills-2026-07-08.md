# LLM Council — is `drafts/coreyhaines31-marketingskills` worth adding to library/?

Question framed with context: draft "marketing-growth-toolkit" (CRO/copywriting/SEO/growth
analytics, source github.com/coreyhaines31/marketingskills, 36,812 stars, eval-passed) — flagged
before convening that `library/coreyhaines31-marketingskills/` already exists with the same
source URL, added 2026-07-07.

## Advisor responses

**The Contrarian:** Not a "worth adding" question — a duplicate-detection failure. Suspected the
guard/dedup keys on name, not source URL. Recommend: fix root cause, then trash the draft.

**The First Principles Thinker:** The premise is wrong — this isn't a fresh candidacy decision,
it's an identification problem (same skill under two names, or a genuine fork?). That's a 5-minute
diff, not a committee vote. committee.py's collision guard already encodes the right epistemic
stance by declining to auto-decide here.

**The Expansionist:** Don't auto-trash — diff first. If the draft covers something the promoted
entry doesn't, merge the delta. Also flagged: the promoted entry covers 4 sub-domains (CRO, copy,
SEO, analytics) — a real splitting candidate independent of this draft.

**The Outsider:** No, don't add it. This is bookkeeping wearing a quality question's clothes. The
system's collision guard already worked as designed by declining to auto-decide. Route to manual
review with one question: same skill (delete) or has unique content (cherry-pick then delete)?

**The Executor:** No — and flagged a real, verified mechanism gap: the collision guard only checks
by **draft's own directory name**, not source URL. Since this draft is named `marketing-growth-toolkit`
(not `coreyhaines31-marketingskills`), **the guard will not fire** if run through `make committee` —
it would burn 5 real `claude -p` calls re-adjudicating an already-decided source.

## Chairman synthesis

**Verdict: do not promote as a second library entry.** All 5 advisors independently converged on
this despite starting from very different angles — the strongest possible agreement signal.

**Verified findings, not just opinion:**
- `candidates/seen.txt` **does** contain the source URL already — so this isn't a fundamentally
  broken URL-dedup (the Contrarian's theory), more likely the draft was built before the promotion
  happened and never got cleaned up afterward.
- The Executor's mechanism claim checks out against `committee.py`'s actual code: the collision
  guard matches on `draft_dir.name` vs `library/<name>/`, not source URL. This draft's internal
  name (`marketing-growth-toolkit`) doesn't match the promoted entry's name
  (`coreyhaines31-marketingskills`) — **the guard would not catch this if run through `make committee`.**
  Real, verified, actionable: running the normal pipeline on this draft would waste 5 real API
  calls on a question already settled.
- Diff against `library/coreyhaines31-marketingskills/SKILL.md`: real content differences exist
  (different rewrite, different section ordering), but the library version is longer and more
  thorough, not missing coverage — the Expansionist's "merge the delta" concern doesn't apply here;
  there's no delta worth merging.

**Blind spot the group didn't fully resolve:** whether harvest-time naming instability (same repo,
different candidate name across runs) is worth a fix now or later. Expansionist and Executor both
flagged it as a real but low-priority backlog item — correct call, not urgent.

**One concrete next step:** delete `drafts/coreyhaines31-marketingskills/` (it is git-tracked, not
gitignored — flagging before deletion rather than doing it silently). Do not run `make committee`
or `make review` on it; both would waste effort re-deciding something already decided.
