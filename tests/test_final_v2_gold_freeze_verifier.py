from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.verify_final_v2_gold_freeze import duplicate_groups, verify


def test_gold_freeze_verifier_fails_without_manifest(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    result = verify(missing, project_root=tmp_path)

    assert result["status"] == "FAIL"
    assert "freeze manifest does not exist" in result["errors"][0]


def test_duplicate_safe_input_conflict_detection() -> None:
    base = {
        "case_id": "case-1",
        "repository": "org/repo",
        "pr_number": 1,
        "language": "python",
        "code_changed_files": ["pyproject.toml"],
        "code_diff_excerpt": "+python = '<3.14'",
        "docs_before_excerpt": "Requires Python 3.13.",
        "gold_docs_update_required": False,
        "gold_doc_category": "no_update",
    }
    other = {
        **base,
        "case_id": "case-2",
        "pr_number": 2,
        "gold_docs_update_required": True,
        "gold_doc_category": "developer_setup",
    }

    groups = duplicate_groups([base, other], "safe_input")

    assert len(groups) == 1
    assert groups[0]["conflicting_labels"] is True


def test_verifier_accepts_minimal_valid_frozen_manifest(tmp_path: Path) -> None:
    gold = tmp_path / "gold.jsonl"
    partition = tmp_path / "partition.json"
    completion = tmp_path / "completion.json"
    row = {
        "case_id": "case-1",
        "repository": "org/repo",
        "pr_number": 1,
        "review_status": "approved",
        "human_review_complete": True,
        "label_source": "human_reviewed_final_v2",
        "gold_docs_update_required": False,
        "gold_doc_category": "no_update",
        "partition": "development_train",
        "language": "python",
        "code_changed_files": ["src/app.py"],
        "code_diff_excerpt": "+x",
        "docs_before_excerpt": "Existing docs.",
    }
    gold.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    partition.write_text(json.dumps({"confirmation_sealed": True}, sort_keys=True), encoding="utf-8")
    completion.write_text(json.dumps({"status": "passed"}, sort_keys=True), encoding="utf-8")

    import hashlib

    def sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "gate": 1,
                "canonical_dataset_path": "gold.jsonl",
                "canonical_dataset_sha256": sha(gold),
                "row_count": 1,
                "safe_model_fields": ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"],
                "partition_manifest_path": "partition.json",
                "partition_manifest_sha256": sha(partition),
                "completion_audit_path": "completion.json",
                "completion_audit_sha256": sha(completion),
                "confirmation_sealed": True,
                "confirmation_accessed_by_gate_1": False,
                "split_counts": {
                    "development_train": {"rows": 1, "positive": 0, "negative": 1},
                },
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    result = verify(manifest, project_root=tmp_path)

    assert result["status"] == "PASS", result
