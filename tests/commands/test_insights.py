import json

from scout.commands import insights


def _write_verdict(base_dir, name, committee_verdict, council_verdict=None):
    d = base_dir / name
    d.mkdir(parents=True)
    (d / "committee_verdict.json").write_text(json.dumps(committee_verdict))
    if council_verdict is not None:
        (d / "council_verdict.json").write_text(json.dumps(council_verdict))
    return d


def _committee_verdict(decision, votes):
    return {"overall_score": 4.0, "passing_score": 3.5, "decision": decision, "votes": votes}


def _vote(voter, usefulness=4, uniqueness=4, quality=4, safety=4):
    return {"voter": voter,
            "scores": {"usefulness": usefulness, "uniqueness": uniqueness,
                       "quality": quality, "safety": safety},
            "reason": "ok"}


def test_no_verdicts_anywhere(tmp_path, monkeypatch):
    monkeypatch.setattr(insights, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(insights, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(insights, "LIBRARY_DIR", tmp_path / "library")

    result = insights.run()

    assert result == {"counts": {}, "voters": [], "dimensions": [],
                       "council_overlap": {"add_n": 0, "add_avg_uniqueness": None,
                                            "skip_n": 0, "skip_avg_uniqueness": None}}


def test_buckets_rejected_duplicate_and_pending_review(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    trash_dir = tmp_path / "trash"
    monkeypatch.setattr(insights, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(insights, "TRASH_DIR", trash_dir)
    monkeypatch.setattr(insights, "LIBRARY_DIR", tmp_path / "library")

    _write_verdict(trash_dir, "rejected-skill",
                    _committee_verdict("rejected", [_vote("CEO", uniqueness=1)]))
    _write_verdict(trash_dir, "dupey-skill",
                    _committee_verdict("hired", [_vote("CEO", uniqueness=5)]),
                    {"decision": "skip", "reason": "redundant"})
    _write_verdict(drafts_dir, "pending-skill",
                    _committee_verdict("hired", [_vote("CEO", uniqueness=2)]),
                    {"decision": "add", "reason": "genuinely new"})

    result = insights.run()

    assert result["counts"] == {"rejected": 1, "duplicate": 1, "pending-review": 1}
    assert result["council_overlap"] == {
        "add_n": 1, "add_avg_uniqueness": 2.0,
        "skip_n": 1, "skip_avg_uniqueness": 5.0,
    }


def test_hired_without_council_verdict_is_its_own_bucket(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    monkeypatch.setattr(insights, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(insights, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(insights, "LIBRARY_DIR", tmp_path / "library")

    _write_verdict(drafts_dir, "legacy-skill", _committee_verdict("hired", [_vote("CEO")]))

    result = insights.run()

    assert result["counts"] == {"hired-no-council": 1}


def test_voter_and_dimension_averages(tmp_path, monkeypatch):
    trash_dir = tmp_path / "trash"
    monkeypatch.setattr(insights, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(insights, "TRASH_DIR", trash_dir)
    monkeypatch.setattr(insights, "LIBRARY_DIR", tmp_path / "library")

    _write_verdict(trash_dir, "skill-a", _committee_verdict("rejected", [
        _vote("CEO", usefulness=2, uniqueness=2, quality=2, safety=2),
        _vote("CTO", usefulness=4, uniqueness=4, quality=4, safety=4),
    ]))

    result = insights.run()

    voters = {v["voter"]: v for v in result["voters"]}
    assert voters["CEO"] == {"voter": "CEO", "avg_score": 2.0, "votes_cast": 1}
    assert voters["CTO"] == {"voter": "CTO", "avg_score": 4.0, "votes_cast": 1}
    assert result["dimensions"] == [
        {"decision": "rejected", "usefulness": 3.0, "uniqueness": 3.0,
         "quality": 3.0, "safety": 3.0},
    ]


def test_backfilled_library_entries_bucket_separately(tmp_path, monkeypatch):
    library_dir = tmp_path / "library"
    monkeypatch.setattr(insights, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(insights, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(insights, "LIBRARY_DIR", library_dir)

    _write_verdict(library_dir, "old-skill",
                    _committee_verdict("backfilled", [_vote("CEO")]))

    result = insights.run()

    assert result["counts"] == {"backfilled": 1}
