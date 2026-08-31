from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/final_v2/controlled_real_project_positive_v1"
OUT_V2 = ROOT / "data/final_v2/controlled_real_project_positive_v2_imbalanced"
CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
    "other_documentation",
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_controlled_positive_dataset_distribution_and_labels() -> None:
    rows = load_jsonl(OUT / "human_review/reviewed_2000.jsonl")

    assert len(rows) == 2_000
    assert Counter(row["human_doc_category"] for row in rows) == Counter(
        {category: 400 for category in CATEGORIES}
    )
    assert Counter(row["source_project_key"] for row in rows) == Counter(
        {
            "jobfair_platform": 500,
            "rbi_related_parties_portal": 500,
            "rbi_test_forge": 500,
            "rbi_property_valuation": 500,
        }
    )
    assert all(row["human_docs_update_required"] is True for row in rows)
    assert all(row["review_status"] == "approved" for row in rows)
    assert all(row["training_eligible"] is False for row in rows)
    assert all(row["merge_status"] == "pending_owner_acceptance" for row in rows)
    assert all(row["code_diff_excerpt"].startswith("--- a/") for row in rows)
    assert all("controlled-baseline:" in row["docs_before_excerpt"] for row in rows)


def test_controlled_positive_dataset_artifacts_and_quality_gate() -> None:
    audit = json.loads((OUT / "audits/quality_audit.json").read_text(encoding="utf-8"))

    assert audit["all_quality_gates_pass"] is True
    assert audit["validation_errors"] == []
    assert audit["review_hashes_valid"] is True
    assert audit["unique_case_ids"] == 2_000
    assert audit["unique_patch_hashes"] == 2_000
    assert audit["unique_repository_pr_keys"] == 2_000
    assert audit["documentation_files_changed_by_cases"] == 0
    assert audit["source_copies_have_no_git_directory"] is True
    assert audit["source_files_preserved_outside_generated_lab"] is True
    assert len(list((OUT / "cases/patches").rglob("*.patch"))) == 2_000
    assert len(list((OUT / "human_review/review_batches").glob("batch_*.jsonl"))) == 20
    assert len(list((OUT / "human_review/review_batches").glob("batch_*.csv"))) == 20
    assert not any((OUT / "source_copies").rglob(".git"))


def test_imbalanced_v2_distribution_and_quality_gate() -> None:
    rows = load_jsonl(OUT_V2 / "human_review/reviewed_2000.jsonl")
    audit = json.loads((OUT_V2 / "audits/quality_audit.json").read_text(encoding="utf-8"))

    assert len(rows) == 2_000
    assert Counter(row["human_doc_category"] for row in rows) == Counter(
        {
            "api_reference": 580,
            "configuration": 520,
            "developer_setup": 460,
            "model_contract": 300,
            "other_documentation": 140,
        }
    )
    assert Counter(row["source_project_key"] for row in rows) == Counter(
        {
            "jobfair_platform": 560,
            "rbi_related_parties_portal": 520,
            "rbi_test_forge": 430,
            "rbi_property_valuation": 490,
        }
    )
    assert all(row["human_docs_update_required"] is True for row in rows)
    assert all(row["review_status"] == "approved" for row in rows)
    assert audit["all_quality_gates_pass"] is True
    assert audit["original_17880_modified"] is False
    assert audit["case_id_overlap_with_original_corpus"] == 0
    assert audit["repository_pr_overlap_with_original_corpus"] == 0
