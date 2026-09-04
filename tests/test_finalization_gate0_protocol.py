from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports/final_v2"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_gate0_protocol_and_artifact_map_exist() -> None:
    protocol = REPORTS / "FINALIZATION_PROTOCOL.md"
    artifact_map = REPORTS / "CANONICAL_ARTIFACT_MAP.md"

    assert protocol.exists()
    assert artifact_map.exists()

    protocol_text = protocol.read_text(encoding="utf-8")
    for gate in range(8):
        assert f"Gate {gate}" in protocol_text
    assert "Do not execute Gate 5 inside Gate 0." in protocol_text

    map_text = artifact_map.read_text(encoding="utf-8")
    assert "CANONICAL FINAL V2" in map_text
    assert "HISTORICAL / DEPRECATED" in map_text
    assert "IMMUTABLE AFTER FREEZE" in map_text


def test_gate0_state_is_machine_checkable_and_confirmation_safe() -> None:
    state = read_json(REPORTS / "finalization_state.json")

    assert state["gate_0_status"] == "PASS"
    assert state["confirmation_sealed"] is True
    assert state["confirmation_results_accessed_by_gate_0"] is False
    assert state["pre_experiment_audit"] == {"status": "PASS", "checks": 15}
    assert state["tests"]["status"] == "PASS"
    assert state["tests"]["passed"] >= 122
    assert state["tests"]["failed"] == 0
    assert state["safe_model_fields"] == [
        "language",
        "code_changed_files",
        "code_diff_excerpt",
        "docs_before_excerpt",
    ]

    for key, rel_path in state["canonical_paths"].items():
        assert rel_path
        assert (ROOT / rel_path).exists(), key

    assert state["final_model_freeze_state"] == {
        "binary_freeze_manifest_present": True,
        "category_freeze_manifest_present": True,
        "stage3_freeze_manifest_present": False,
    }


def test_gate0_state_matches_current_canonical_manifests() -> None:
    state = read_json(REPORTS / "finalization_state.json")
    consolidated = read_json(ROOT / state["canonical_paths"]["consolidated_review_manifest"])
    gold = read_json(ROOT / state["canonical_paths"]["final_human_gold_manifest"])
    partitions = read_json(ROOT / state["canonical_paths"]["canonical_partition_manifest"])

    assert consolidated["validation"] == state["dataset_state"]["validation"]
    assert consolidated["row_count"] == state["dataset_state"]["row_count"]
    assert consolidated["positive_count"] == state["dataset_state"]["positive_rows"]
    assert consolidated["negative_count"] == state["dataset_state"]["negative_rows"]
    assert consolidated["category_counts"] == state["dataset_state"]["category_counts"]

    assert gold["repository_overlap_count"] == state["gold_split_state"]["repository_overlap_count"]
    assert gold["partition_row_counts"] == state["gold_split_state"]["partition_row_counts"]
    assert gold["partition_repository_counts"] == state["gold_split_state"]["partition_repository_counts"]
    for filename, digest in gold["sha256"].items():
        assert state["gold_split_state"]["sha256"][filename] == digest
    assert gold["sealed_confirmation_case_ids_preserved"] is True

    assert partitions["confirmation_sealed"] is True
