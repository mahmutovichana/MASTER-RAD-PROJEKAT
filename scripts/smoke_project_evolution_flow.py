from __future__ import annotations

import tempfile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_demo.project_evolution_scenarios import BASE_DIR, generate_project_evolution_cases
from docguard_demo.run_project_evolution_flow import prediction_input, run


def main() -> int:
    records = generate_project_evolution_cases()
    categories = {record["gold_doc_category"] for record in records}
    required_categories = {
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
    assert len(records) >= 24
    assert len({record["project_id"] for record in records}) >= 3
    assert required_categories <= categories
    assert sum(1 for record in records if not record["gold_docs_update_required"]) >= 5
    forbidden = {"scenario_type", "gold_doc_category", "gold_target_doc_file", "expected_facts", "expected_patch_summary"}
    for record in records:
        assert forbidden.isdisjoint(prediction_input(record))
    assert all((path / "docs").exists() and (path / "src").exists() for path in BASE_DIR.iterdir() if path.is_dir())
    with tempfile.TemporaryDirectory() as tmp:
        result = run(Path(tmp))
        assert result["status"] == "ok"
        assert (Path(tmp) / "docguard_project_evolution_predictions.jsonl").exists()
        assert (Path(tmp) / "docguard_project_evolution_evaluation_2026_08.md").exists()
        assert (Path(tmp) / "docguard_project_evolution_walkthrough_2026_08.md").exists()
    print("project evolution smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
