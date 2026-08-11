from __future__ import annotations

import json
from pathlib import Path

from docguard_demo.live_flow_scenarios import generate_live_flow_cases
from docguard_demo.run_live_flow import run


REQUIRED_FIELDS = {
    "id",
    "project_id",
    "changed_files",
    "code_diff",
    "docs_before",
    "docs_update_required",
    "scenario_type",
    "doc_category",
    "target_doc_file",
    "target_section",
    "expected_facts",
    "change_summary",
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


def test_live_scenario_generation_covers_main_categories() -> None:
    records = generate_live_flow_cases()
    categories = {record["doc_category"] for record in records}
    assert MAIN_CATEGORIES <= categories
    assert len(records) >= 15


def test_live_scenario_records_have_required_fields() -> None:
    records = generate_live_flow_cases()
    for record in records:
        assert REQUIRED_FIELDS <= set(record)
        if record["docs_update_required"]:
            assert record["target_doc_file"]
        else:
            assert not record["target_doc_file"]
            assert not record["expected_facts"]


def test_live_flow_runner_outputs_reports(tmp_path: Path) -> None:
    result = run(tmp_path)
    prediction_path = tmp_path / "docguard_live_flow_predictions.jsonl"
    report_path = tmp_path / "docguard_live_flow_evaluation_2026_08.md"
    assert result["status"] == "ok"
    assert prediction_path.exists()
    assert report_path.exists()
    predictions = [json.loads(line) for line in prediction_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert predictions
    assert "DocGuard Live Flow Evaluation" in report_path.read_text(encoding="utf-8")
