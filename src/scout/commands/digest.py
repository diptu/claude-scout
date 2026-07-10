"""Digest: rank library/ entries by committee score for a quick "what's
worth your time" glance. Falls back to date_added (newest first) for any
entry with no score yet — that's a permanent fallback, not a one-time
bootstrap gap, since library.review() stays a live promotion path that
never writes a committee_score."""
# pylint: disable=protected-access
from scout.commands.library import _iter_library_entries, _skill_description

TOP_N = 10


def _sort_key(meta: dict):
    score = meta.get("committee_score")
    unscored = score is None
    date_added = meta.get("date_added") or ""
    try:
        year, month, day = (int(part) for part in date_added.split("-"))
        date_key = (-year, -month, -day)
    except ValueError:
        date_key = (0, 0, 0)
    return (unscored, -(score or 0.0), date_key)


def run(top_n: int = TOP_N) -> dict:
    entries = list(_iter_library_entries())
    if not entries:
        return {"total": 0, "rows": []}

    ranked = sorted(entries, key=lambda pair: _sort_key(pair[1]))
    rows = []
    for path, meta in ranked[:top_n]:
        skill_md = path / "SKILL.md"
        description = _skill_description(skill_md) if skill_md.exists() else ""
        rows.append({
            "name": meta.get("name", path.name),
            "score": meta.get("committee_score"),
            "description": description,
            "source_url": meta.get("source_url", ""),
        })
    return {"total": len(entries), "rows": rows}
