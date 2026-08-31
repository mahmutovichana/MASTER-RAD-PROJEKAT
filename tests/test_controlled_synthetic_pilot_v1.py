import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/final_v2/controlled_synthetic_positive_v1"


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_controlled_pilot_distribution_and_provenance():
    candidates = load_jsonl(OUT / "cases/synthetic_candidates.jsonl")
    assert len(candidates) == 200
    categories = {category: sum(row.get("synthetic_category_by_design") == category for row in candidates) for category in {"api_reference", "configuration", "developer_setup", "model_contract"}}
    assert categories == {"api_reference": 50, "configuration": 50, "developer_setup": 50, "model_contract": 50}
    assert all(row.get("synthetic_case") is True for row in candidates)
    assert all(row.get("case_origin") == "controlled_synthetic_positive_v1" for row in candidates)
    assert all(row.get("synthetic_base_sha") and row.get("synthetic_head_sha") for row in candidates)


def test_quality_audit_and_review_batches_are_ready_for_human_review():
    audit = json.loads((OUT / "audits/synthetic_case_quality_audit.json").read_text(encoding="utf-8"))
    manifest = json.loads((OUT / "human_review/review_batch_manifest.json").read_text(encoding="utf-8"))
    assert audit["all_candidates_pre_review_valid"] is True
    assert audit["human_review_required"] is True
    assert audit["repository_overlap_with_consolidated_corpus"] == []
    assert manifest["total_rows"] == 200
    assert manifest["batch_count"] == 4
    assert manifest["review_status_initial"] == "pending"
