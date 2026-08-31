from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.finalize_natural_diversity_review_v1 import (
    decision,
    immutable_projection,
    run as finalize_review,
    validate_decision,
)
from scripts.run_natural_diversity_refresh_category_v1 import (
    audit_membership,
    primary_expansion,
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def review_row(
    case_id: str,
    *,
    partition: str = "development_train",
    docs_required: bool | None = None,
    category: str | None = None,
    status: str = "pending",
) -> dict:
    return {
        "case_id": case_id,
        "repository": f"org/{case_id}",
        "pr_number": 1,
        "partition": partition,
        "language": "python",
        "code_changed_files": ["app.py"],
        "code_diff_excerpt": "+ change",
        "docs_before_excerpt": "Existing documented behavior",
        "suggested_docs_update_required": None,
        "suggested_doc_category": None,
        "suggested_notes": None,
        "human_docs_update_required": docs_required,
        "human_doc_category": category,
        "human_label_notes": "reviewed",
        "review_status": status,
        "label_source": None,
    }


def training_row(case_id: str, repo: str, pr: int, category: str) -> dict:
    return {
        "case_id": case_id,
        "repository": repo,
        "pr_number": pr,
        "gold_doc_category": category,
        "gold_docs_update_required": True,
    }


def test_review_decision_validation_and_immutable_projection() -> None:
    base = review_row("case-1")
    reviewed = dict(base)
    reviewed.update({
        "human_docs_update_required": True,
        "human_doc_category": "api_reference",
        "review_status": "approved",
    })

    assert decision(reviewed) == (True, "api_reference", "reviewed", "approved")
    assert validate_decision(reviewed) == []
    assert immutable_projection(base) == immutable_projection(reviewed)

    invalid = dict(reviewed)
    invalid["human_doc_category"] = "no_update"
    assert any("invalid category" in error for error in validate_decision(invalid))


def test_finalize_review_rejects_non_human_field_mutation(tmp_path: Path) -> None:
    prefilled = review_row("case-1")
    reviewed = dict(prefilled)
    reviewed.update({
        "code_diff_excerpt": "+ mutated evidence",
        "human_docs_update_required": False,
        "human_doc_category": "no_update",
        "review_status": "approved",
    })
    prefilled_path = tmp_path / "prefilled_review.jsonl"
    batches_dir = tmp_path / "batches"
    write_jsonl(prefilled_path, [prefilled])
    write_jsonl(batches_dir / "batch_001.jsonl", [reviewed])
    write_csv(batches_dir / "batch_001.csv", [reviewed])

    with pytest.raises(ValueError, match="immutable evidence"):
        finalize_review(
            prefilled_path=prefilled_path,
            batches_dir=batches_dir,
            output_dir=tmp_path / "finalized",
        )


def test_finalize_review_outputs_gold_splits_after_cross_checks(tmp_path: Path) -> None:
    train = review_row("case-1")
    refresh = review_row("case-2", partition="refresh_validation")
    train_reviewed = dict(train)
    train_reviewed.update({
        "human_docs_update_required": True,
        "human_doc_category": "developer_setup",
        "review_status": "approved",
    })
    refresh_reviewed = dict(refresh)
    refresh_reviewed.update({
        "human_docs_update_required": False,
        "human_doc_category": "no_update",
        "review_status": "approved",
    })
    prefilled_path = tmp_path / "prefilled_review.jsonl"
    batches_dir = tmp_path / "batches"
    output_dir = tmp_path / "finalized"
    write_jsonl(prefilled_path, [train, refresh])
    write_jsonl(batches_dir / "batch_001.jsonl", [train_reviewed, refresh_reviewed])
    write_csv(batches_dir / "batch_001.csv", [train_reviewed, refresh_reviewed])

    summary = finalize_review(
        prefilled_path=prefilled_path,
        batches_dir=batches_dir,
        output_dir=output_dir,
    )

    assert summary["approved_rows"] == 2
    assert summary["positive_category_counts"] == {"developer_setup": 1}
    train_gold = [
        json.loads(line)
        for line in (output_dir / "natural_expansion_train_gold.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    refresh_gold = [
        json.loads(line)
        for line in (output_dir / "natural_refresh_validation_gold.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert train_gold[0]["owner_accepted_for_training"] is True
    assert refresh_gold[0]["owner_accepted_for_training"] is False


def test_primary_expansion_uses_only_approved_primary_four_rows() -> None:
    rows = [
        {
            **training_row("api", "org/api", 1, "api_reference"),
            "partition": "development_train",
            "review_status": "approved",
            "independent_human_reviewed": True,
        },
        {
            **training_row("other", "org/other", 2, "other_documentation"),
            "partition": "development_train",
            "review_status": "approved",
            "independent_human_reviewed": True,
        },
        {
            **training_row("pending", "org/pending", 3, "configuration"),
            "partition": "development_train",
            "review_status": "pending",
            "independent_human_reviewed": False,
        },
    ]

    assert [row["case_id"] for row in primary_expansion(rows, "development_train")] == ["api"]

    rows[0]["partition"] = "refresh_validation"
    with pytest.raises(ValueError, match="expected partition"):
        primary_expansion(rows, "development_train")


def test_membership_audit_catches_repository_overlap_and_duplicate_pr() -> None:
    old_train = [training_row("old", "org/shared", 1, "api_reference")]
    old_validation = [training_row("val", "org/val", 1, "configuration")]
    expansion_train = [training_row("new", "org/shared", 2, "developer_setup")]
    refresh = [training_row("dupe", "org/val", 1, "model_contract")]

    audit = audit_membership(old_train, old_validation, expansion_train, refresh)

    assert audit["status"] == "failed"
    assert audit["duplicate_repository_pr_count"] == 1
    assert audit["repository_overlaps"]["expansion_train_vs_old_train"] == ["org/shared"]
    assert audit["repository_overlaps"]["refresh_vs_old_validation"] == ["org/val"]
