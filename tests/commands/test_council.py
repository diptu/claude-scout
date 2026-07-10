import json
import subprocess
from unittest.mock import MagicMock

from scout.commands import council


def _patch_prompts(monkeypatch, tmp_path):
    advisor_file = tmp_path / "council_advisor.md"
    advisor_file.write_text("{advisor_name} {advisor_lens} {library_names}\n{skill_md_content}")
    chairman_file = tmp_path / "council_chairman.md"
    chairman_file.write_text("{advisor_opinions}\n{skill_md_content}")
    monkeypatch.setattr(council, "ADVISOR_PROMPT_FILE", advisor_file)
    monkeypatch.setattr(council, "CHAIRMAN_PROMPT_FILE", chairman_file)
    monkeypatch.setattr(
        council, "_council_config",
        lambda: [{"name": "A1", "lens": "l"}, {"name": "A2", "lens": "l"},
                  {"name": "A3", "lens": "l"}],
    )


def _advisor_json(verdict="add", reason="fine"):
    return json.dumps({"verdict": verdict, "reason": reason})


def _chairman_json(decision="add", reason="synthesized"):
    return json.dumps({"decision": decision, "reason": reason})


def _canned_claude(stdouts):
    it = iter(stdouts)

    def fake_run(*_args, **_kwargs):
        item = next(it)
        if item == "TIMEOUT":
            raise subprocess.TimeoutExpired(cmd="claude", timeout=120)
        return MagicMock(returncode=0, stdout=item, stderr="")
    return fake_run


def test_all_advisors_and_chairman_agree_add(tmp_path, monkeypatch):
    _patch_prompts(monkeypatch, tmp_path)
    monkeypatch.setattr(
        council.subprocess, "run",
        _canned_claude([_advisor_json("add")] * 3 + [_chairman_json("add", "genuinely new")]),
    )

    result = council.evaluate("skill md content", "existing-a, existing-b")

    assert result["decision"] == "add"
    assert result["reason"] == "genuinely new"
    assert len(result["advisors"]) == 3


def test_chairman_can_decide_skip(tmp_path, monkeypatch):
    _patch_prompts(monkeypatch, tmp_path)
    monkeypatch.setattr(
        council.subprocess, "run",
        _canned_claude([_advisor_json("skip")] * 3 + [_chairman_json("skip", "redundant")]),
    )

    result = council.evaluate("skill md content", "existing-a, existing-b")

    assert result["decision"] == "skip"
    assert result["reason"] == "redundant"


def test_no_advisor_opinions_fails_open_to_add(tmp_path, monkeypatch):
    _patch_prompts(monkeypatch, tmp_path)
    # every advisor call times out or returns garbage -> no opinions -> chairman
    # is never even called -> evaluate() must not silently trash the draft
    monkeypatch.setattr(
        council.subprocess, "run",
        _canned_claude(["TIMEOUT", "not json", "also not json"]),
    )

    result = council.evaluate("skill md content", "existing-a")

    assert result["decision"] == "add"
    assert "deferring to human review" in result["reason"]
    assert result["advisors"] == []


def test_some_advisor_timeouts_still_reach_chairman(tmp_path, monkeypatch):
    _patch_prompts(monkeypatch, tmp_path)
    monkeypatch.setattr(
        council.subprocess, "run",
        _canned_claude(["TIMEOUT", _advisor_json("add"), _advisor_json("skip"),
                        _chairman_json("add", "majority holds")]),
    )

    result = council.evaluate("skill md content", "existing-a")

    assert result["decision"] == "add"
    assert len(result["advisors"]) == 2
