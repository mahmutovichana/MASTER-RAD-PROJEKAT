from __future__ import annotations

import json
from pathlib import Path

from docguard_demo.project_evolution_scenarios import BASE_DIR, generate_project_evolution_cases
from docguard_demo.run_project_evolution_flow import prediction_input, run


REQUIRED_FIELDS = {
    "case_id",
    "project_id",
    "pr_title",
    "sequence_number",
    "code_changed_files",
    "code_diff",
    "docs_before",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "expected_facts",
    "expected_patch_summary",
    "scenario_type",
    "change_summary",
    "difficulty",
    "realism_notes",
}
MAIN_CATEGORIES = {
    "api_reference",
    "model_contract",
    "configuration",
    "testing_instructions",
    "workflow_documentation",
    "architecture_flow",
    "developer_setup",
    "changelog",
    "no_update",
}


def test_project_evolution_generation_shape() -> None:
    records = generate_project_evolution_cases()
    assert len(records) >= 24
    assert len({record["project_id"] for record in records}) >= 3
    assert MAIN_CATEGORIES <= {record["gold_doc_category"] for record in records}
    assert sum(1 for record in records if not record["gold_docs_update_required"]) >= 5
    for record in records:
        assert REQUIRED_FIELDS <= set(record)
        if record["gold_docs_update_required"]:
            assert record["gold_target_doc_file"]


def test_project_evolution_prediction_input_is_sanitized() -> None:
    record = generate_project_evolution_cases()[0]
    payload = prediction_input(record)
    forbidden = {"scenario_type", "gold_doc_category", "gold_target_doc_file", "expected_facts", "expected_patch_summary"}
    assert not (forbidden & set(payload))


def test_project_evolution_runner_outputs(tmp_path: Path) -> None:
    result = run(tmp_path)
    predictions_path = tmp_path / "docguard_project_evolution_predictions.jsonl"
    report_path = tmp_path / "docguard_project_evolution_evaluation_2026_08.md"
    walkthrough_path = tmp_path / "docguard_project_evolution_walkthrough_2026_08.md"
    assert result["status"] == "ok"
    assert predictions_path.exists()
    assert report_path.exists()
    assert walkthrough_path.exists()
    predictions = [json.loads(line) for line in predictions_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert predictions


def test_generated_project_folders_have_docs_and_source() -> None:
    generate_project_evolution_cases()
    projects = [path for path in BASE_DIR.iterdir() if path.is_dir()]
    assert len(projects) >= 3
    for project in projects:
        assert (project / "evolution_log.md").exists()
        assert (project / "docs").exists()
        assert (project / "src").exists()
