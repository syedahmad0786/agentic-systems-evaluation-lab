import json
from pathlib import Path
import tomllib


ROOT = Path(__file__).parents[1]
CREW_ROOT = ROOT / "crewai" / "agentic-systems-editorial-crew"


def test_live_page_labels_the_teaching_replay_and_human_gate():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "public" / "app.js").read_text(encoding="utf-8")

    assert 'id="crewai-demo"' in html
    assert "Visual replay" in html
    assert html.count("data-crew-step=") == 4
    assert "Ahmad owns the publish decision" in html
    assert "never claims that animation is an AI run" in html
    assert "Crew stopped at the human gate" in javascript


def test_json_first_crew_has_four_agents_context_handoffs_and_one_human_gate():
    crew = json.loads((CREW_ROOT / "crew.jsonc").read_text(encoding="utf-8"))
    agent_files = sorted(path.stem for path in (CREW_ROOT / "agents").glob("*.jsonc"))

    assert crew["name"] == "Agentic Systems Editorial Crew"
    assert crew["process"] == "sequential"
    assert crew["tracing"] is True
    assert crew["agents"] == [
        "evidence_scout",
        "systems_mapper",
        "field_note_editor",
        "claims_gate",
    ]
    assert sorted(crew["agents"]) == agent_files
    assert [task["name"] for task in crew["tasks"]] == [
        "build_evidence_ledger",
        "map_the_system",
        "draft_content_pack",
        "review_release_packet",
    ]
    assert crew["tasks"][1]["context"] == ["build_evidence_ledger"]
    assert crew["tasks"][2]["context"] == ["build_evidence_ledger", "map_the_system"]
    assert crew["tasks"][3]["human_input"] is True
    assert sum(bool(task.get("human_input")) for task in crew["tasks"]) == 1


def test_agents_have_no_tools_and_cannot_delegate():
    for path in (CREW_ROOT / "agents").glob("*.jsonc"):
        agent = json.loads(path.read_text(encoding="utf-8"))
        assert agent["tools"] == []
        assert agent["settings"]["allow_delegation"] is False
        assert agent["llm"] == "openai/gpt-4o-mini"


def test_repository_root_has_classic_amp_compatibility_scaffold():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    classic_root = ROOT / "src" / "agentic_systems_evaluation_lab"

    assert project["tool"]["crewai"]["type"] == "crew"
    assert project["project"]["scripts"]["run_crew"] == "agentic_systems_evaluation_lab.main:run"
    assert (classic_root / "crew.py").is_file()
    assert (classic_root / "main.py").is_file()
    assert (classic_root / "config" / "agents.yaml").is_file()
    assert (classic_root / "config" / "tasks.yaml").is_file()
