import json

from scout.commands import committee


def _make_draft(drafts_dir, name, content="---\nname: x\ndescription: d\n---\nbody"):
    d = drafts_dir / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(content)
    (d / ".eval_status").write_text("passed\n")
    (d / "candidate.json").write_text('{"url": "https://x/repo"}')
    return d


def _patch_dirs(monkeypatch, tmp_path, drafts_dir):
    monkeypatch.setattr(committee, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(committee, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(committee, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(committee, "LOGS_DIR", tmp_path / "logs")
    prompt_file = tmp_path / "committee.md"
    prompt_file.write_text(
        "{voter_name} {voter_focus} {library_names}\n{skill_md_content}"
    )
    monkeypatch.setattr(committee, "COMMITTEE_PROMPT_FILE", prompt_file)
    monkeypatch.setattr(
        committee, "_committee_config",
        lambda: (3.5, 3, [{"name": "V1", "focus": "f"}, {"name": "V2", "focus": "f"},
                           {"name": "V3", "focus": "f"}]),
    )


def _vote_json(usefulness=5, uniqueness=5, quality=5, safety=5, reason="great"):
    return json.dumps({
        "usefulness": usefulness, "uniqueness": uniqueness,
        "quality": quality, "safety": safety, "reason": reason,
    })


def _canned_claude(stdouts):
    it = iter(stdouts)

    def fake_run(*_args, **_kwargs):
        from unittest.mock import MagicMock
        return MagicMock(returncode=0, stdout=next(it), stderr="")
    return fake_run


def _fake_council(decision="add", reason="worth it"):
    def fake_evaluate(_skill_md, _library_names):
        return {"decision": decision, "reason": reason, "advisors": [], "log_lines": ["x"]}
    return fake_evaluate


def _unreachable_council(monkeypatch):
    def fail_evaluate(*_a, **_k):
        raise AssertionError("council.evaluate should not be called")
    monkeypatch.setattr(committee.council, "evaluate", fail_evaluate)


def test_nothing_to_do(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path, tmp_path / "drafts")
    result = committee.run()
    assert result == {"pending_review": 0, "rejected": 0, "duplicate": 0, "no_quorum": 0,
                       "collisions": 0, "already_decided": 0, "report": []}


def test_hired_and_council_approves_leaves_for_review(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "good-skill")
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(committee.subprocess, "run",
                         _canned_claude([_vote_json(5, 5, 5, 5)] * 3))
    monkeypatch.setattr(committee.council, "evaluate", _fake_council("add", "genuinely new"))

    result = committee.run()

    assert result["pending_review"] == 1
    assert result["rejected"] == 0
    assert result["duplicate"] == 0
    assert result["report"][0]["decision"] == "pending-review"
    # never auto-promoted: draft stays in drafts/ for `make review`
    draft_dir = drafts_dir / "good-skill"
    assert draft_dir.joinpath("SKILL.md").exists()
    assert not (tmp_path / "library" / "good-skill").exists()
    committee_verdict = json.loads(draft_dir.joinpath("committee_verdict.json").read_text())
    assert committee_verdict["decision"] == "hired"
    assert committee_verdict["overall_score"] == 5.0
    council_verdict = json.loads(draft_dir.joinpath("council_verdict.json").read_text())
    assert council_verdict["decision"] == "add"
    assert council_verdict["reason"] == "genuinely new"


def test_hired_but_council_flags_duplicate_trashes(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "dupey-skill")
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(committee.subprocess, "run",
                         _canned_claude([_vote_json(5, 5, 5, 5)] * 3))
    monkeypatch.setattr(committee.council, "evaluate", _fake_council("skip", "redundant"))

    result = committee.run()

    assert result["pending_review"] == 0
    assert result["duplicate"] == 1
    assert result["report"][0]["decision"] == "duplicate"
    assert not (drafts_dir / "dupey-skill").exists()
    assert not (tmp_path / "library" / "dupey-skill").exists()
    trash_dir = tmp_path / "trash" / "dupey-skill"
    assert trash_dir.joinpath("SKILL.md").exists()
    committee_verdict = json.loads(trash_dir.joinpath("committee_verdict.json").read_text())
    assert committee_verdict["decision"] == "hired"
    council_verdict = json.loads(trash_dir.joinpath("council_verdict.json").read_text())
    assert council_verdict["decision"] == "skip"
    assert council_verdict["reason"] == "redundant"


def test_low_scores_reject_to_trash_without_calling_council(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "bad-skill")
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(committee.subprocess, "run",
                         _canned_claude([_vote_json(1, 1, 1, 1)] * 3))
    _unreachable_council(monkeypatch)

    result = committee.run()

    assert result["pending_review"] == 0
    assert result["rejected"] == 1
    assert result["duplicate"] == 0
    assert result["report"][0]["decision"] == "rejected"
    assert (tmp_path / "trash" / "bad-skill" / "SKILL.md").exists()
    assert not (tmp_path / "library" / "bad-skill").exists()


def test_name_collision_with_existing_library_entry_is_never_overwritten(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "dup-skill")
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    existing_lib = tmp_path / "library" / "dup-skill"
    existing_lib.mkdir(parents=True)
    (existing_lib / "SKILL.md").write_text("curated content")
    (existing_lib / "meta.json").write_text('{"name": "dup-skill", "tags": ["hand-curated"]}')
    _unreachable_council(monkeypatch)

    calls = []
    monkeypatch.setattr(committee.subprocess, "run", lambda *a, **k: calls.append(1))

    result = committee.run()

    assert calls == []  # no claude calls spent on a candidate that can't be auto-decided
    assert result["pending_review"] == 0
    assert result["rejected"] == 0
    assert result["collisions"] == 1
    assert result["report"][0]["decision"] == "name-collision"
    # existing curated entry is untouched
    assert existing_lib.joinpath("SKILL.md").read_text() == "curated content"
    assert json.loads(existing_lib.joinpath("meta.json").read_text())["tags"] == ["hand-curated"]
    # draft is left in place, not moved to trash either
    assert (drafts_dir / "dup-skill" / "SKILL.md").exists()


def test_below_quorum_leaves_draft_in_place(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "unsure-skill")
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    _unreachable_council(monkeypatch)
    # only 1 of 3 voters returns a parseable vote
    monkeypatch.setattr(committee.subprocess, "run",
                         _canned_claude([_vote_json(), "not json at all", "still not json"]))

    result = committee.run()

    assert result["pending_review"] == 0
    assert result["rejected"] == 0
    assert result["no_quorum"] == 1
    assert result["report"][0]["decision"] == "no-quorum"
    assert (drafts_dir / "unsure-skill" / "SKILL.md").exists()
    assert not (tmp_path / "library" / "unsure-skill").exists()
    assert not (tmp_path / "trash" / "unsure-skill").exists()


def test_already_decided_draft_is_skipped(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    draft_dir = _make_draft(drafts_dir, "pending-skill")
    (draft_dir / "committee_verdict.json").write_text(
        json.dumps({"overall_score": 5.0, "decision": "hired"})
    )
    (draft_dir / "council_verdict.json").write_text(
        json.dumps({"decision": "add", "reason": "ok"})
    )
    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    _unreachable_council(monkeypatch)

    calls = []
    monkeypatch.setattr(committee.subprocess, "run", lambda *a, **k: calls.append(1))

    result = committee.run()

    assert calls == []  # no re-voting on an already-decided draft
    assert result["already_decided"] == 1
    assert result["report"][0]["decision"] == "already-decided"
    assert draft_dir.joinpath("SKILL.md").exists()
