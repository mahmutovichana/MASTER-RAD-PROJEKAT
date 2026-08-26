from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.audit_human_review_complete_v2 import audit
from scripts.build_human_review_batches_v2 import run as build_batches
from scripts.build_second_reviewer_subset_v2 import run as second_subset
from scripts.finalize_human_gold_v2 import LABEL_SOURCE, finalize_row
from scripts.human_review_workflow_v2 import (
    make_review_row,
    read_csv,
    review_row_hash,
    validate_integrity,
    validate_taxonomy,
    write_csv,
    write_jsonl,
)
from scripts.merge_human_review_batches_v2 import run as merge_batches


ROOT = Path(__file__).resolve().parents[1]


def candidate(case_id: str, repo: str = "org/repo", category: str = "api_reference") -> dict:
    return {
        "case_id": case_id,
        "repository": repo,
        "pr_number": int(case_id.strip("c") or 1),
        "language": "python",
        "code_changed_files": ["src/api.py"],
        "code_diff_excerpt": "+def reviews():\n+    return 'review, \"quoted\" unicode č'",
        "docs_before_excerpt": "# API\nOld docs",
        "suggested_docs_update_required": True,
        "suggested_doc_category": category,
        "suggested_reason": "helper only",
        "partition": "confirmation",
    }


def approve(row: dict, docs_required: bool = True, category: str = "api_reference") -> dict:
    reviewed = dict(row)
    reviewed["human_docs_update_required"] = docs_required
    reviewed["human_doc_category"] = category
    reviewed["human_label_notes"] = "manual decision"
    reviewed["review_status"] = "approved"
    return reviewed


def test_batch_size_deterministic_and_every_case_once(tmp_path: Path):
    input_path = tmp_path / "prefilled.jsonl"
    rows = [candidate(f"c{i}", repo=f"org/r{i}") for i in range(1, 6)]
    write_jsonl(input_path, rows)
    manifest = build_batches(input_path, tmp_path / "batches", batch_size=2, seed=7, partition_manifest=tmp_path / "partition.json")
    assert [batch["row_count"] for batch in manifest["batches"]] == [2, 2, 1]
    output_rows = []
    for path in sorted((tmp_path / "batches").glob("batch_*.jsonl")):
        output_rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    assert sorted(row["case_id"] for row in output_rows) == [f"c{i}" for i in range(1, 6)]
    assert "partition" not in output_rows[0]
    assert output_rows[0]["human_docs_update_required"] == ""
    assert output_rows[0]["human_doc_category"] == ""
    assert output_rows[0]["review_status"] == "pending"


def test_suggested_fields_do_not_become_human_fields():
    row = make_review_row(candidate("c1", category="configuration"))
    assert row["suggested_doc_category"] == "configuration"
    assert row["human_doc_category"] == ""
    assert row["human_docs_update_required"] == ""


def test_review_row_hash_deterministic_and_excludes_human_and_suggested_fields():
    row = make_review_row(candidate("c1"))
    changed = approve(dict(row), category="configuration")
    changed["suggested_doc_category"] = "model_contract"
    assert review_row_hash(row) == review_row_hash(changed)
    changed["code_diff_excerpt"] += "\n+tampered"
    ok, reason = validate_integrity(changed)
    assert ok is False
    assert reason == "immutable_evidence_modified"


def test_csv_round_trip_preserves_multiline_diff(tmp_path: Path):
    row = make_review_row(candidate("c1"))
    csv_path = tmp_path / "batch.csv"
    write_csv(csv_path, [row])
    loaded = read_csv(csv_path)
    assert loaded[0]["code_diff_excerpt"] == row["code_diff_excerpt"]
    assert 'review, "quoted" unicode č' in loaded[0]["code_diff_excerpt"]


def test_invalid_taxonomy_rejected_and_no_aliases():
    row = approve(make_review_row(candidate("c1")), True, "security")
    ok, reason = validate_taxonomy(row)
    assert ok is False
    assert reason == "invalid_category"
    neg = approve(make_review_row(candidate("c2")), False, "api_reference")
    assert validate_taxonomy(neg)[1] == "negative_must_be_no_update"


def test_pending_row_not_finalizable():
    row = make_review_row(candidate("c1"))
    with pytest.raises(ValueError, match="approved"):
        finalize_row(row, 1)


def test_duplicate_and_conflicting_reviews_not_silently_resolved(tmp_path: Path):
    base = make_review_row(candidate("c1"))
    left = approve(base, True, "api_reference")
    right = approve(dict(base), False, "no_update")
    left_path = tmp_path / "left.jsonl"
    right_path = tmp_path / "right.jsonl"
    write_jsonl(left_path, [left])
    write_jsonl(right_path, [right])
    result = merge_batches([left_path, right_path], tmp_path / "merge")
    assert result["merged_rows"] == 1
    assert result["conflicts"] == 1


def test_modified_immutable_evidence_detected_on_merge(tmp_path: Path):
    row = approve(make_review_row(candidate("c1")))
    row["docs_before_excerpt"] = "changed after hash"
    path = tmp_path / "review.jsonl"
    write_jsonl(path, [row])
    result = merge_batches([path], tmp_path / "merge")
    assert result["conflicts"] == 1


def test_second_reviewer_sampling_ignores_labels_and_hides_primary_decision(tmp_path: Path):
    input_path = tmp_path / "prefilled.jsonl"
    rows = [approve(make_review_row(candidate(f"c{i}", repo=f"org/r{i}")), i % 2 == 0, "api_reference" if i % 2 == 0 else "no_update") for i in range(1, 8)]
    write_jsonl(input_path, rows)
    manifest = second_subset(input_path, tmp_path / "second", target=3, seed=11)
    selected = [json.loads(line) for line in (tmp_path / "second" / "second_reviewer_subset.jsonl").read_text(encoding="utf-8").splitlines()]
    assert manifest["sampling_ignores_labels_and_predictions"] is True
    assert len(selected) == 3
    assert all(row["human_docs_update_required"] == "" for row in selected)
    assert all(row["human_doc_category"] == "" for row in selected)


def test_reviewer_comparison_and_adjudication_are_human_only(tmp_path: Path):
    base = make_review_row(candidate("c1"))
    a = approve(base, True, "api_reference")
    b = approve(dict(base), False, "no_update")
    a_path = tmp_path / "a.jsonl"
    b_path = tmp_path / "b.jsonl"
    write_jsonl(a_path, [a])
    write_jsonl(b_path, [b])
    out = tmp_path / "agreement"
    result = subprocess.run([sys.executable, "scripts/compare_human_gold_reviewers_v2.py", "--reviewer-a", str(a_path), "--reviewer-b", str(b_path), "--output-dir", str(out)], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0
    conflicts = out / "reviewer_conflicts.jsonl"
    assert conflicts.read_text(encoding="utf-8").strip()
    adj = tmp_path / "adjudication"
    result = subprocess.run([sys.executable, "scripts/build_human_review_adjudication_v2.py", "--conflicts", str(conflicts), "--output-dir", str(adj)], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0
    row = json.loads((adj / "adjudication_sheet.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert row["adjudicated_docs_update_required"] == ""
    assert row["adjudication_status"] == "pending"


def test_completion_audit_fails_pending_and_passes_reviewed_fixture():
    pending = make_review_row(candidate("c1"))
    errors, report = audit([pending])
    assert errors
    assert report["label_source_can_become_human_reviewed_final_v2"] is False
    approved = approve(make_review_row(candidate("c2")), True, "api_reference")
    errors, report = audit([approved])
    assert not errors
    assert report["label_source_can_become_human_reviewed_final_v2"] is True


def test_finalizer_assigns_label_source_only_after_valid_approval():
    reviewed = approve(make_review_row(candidate("c1")), True, "api_reference")
    final = finalize_row(reviewed, 1)
    assert final["label_source"] == LABEL_SOURCE
    assert final["human_review_complete"] is True
    assert final["gold_docs_update_required"] is True
    assert final["gold_doc_category"] == "api_reference"
