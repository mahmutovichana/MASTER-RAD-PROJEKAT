from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.verify_final_v2_gold_freeze import canonical_json_sha256, duplicate_groups, verify, verify_json_artifact_identity


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


def test_partition_json_identity_accepts_lf_and_crlf_equivalents(tmp_path: Path) -> None:
    value = {"confirmation_sealed": True, "repository_assignments": {"org/a": "development_train"}, "counts": {"development_train": 1}}
    lf = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    crlf = lf.replace(b"\n", b"\r\n")
    expected_raw = __import__("hashlib").sha256(crlf).hexdigest()
    expected_canonical = canonical_json_sha256(value)
    path = tmp_path / "partition.json"
    for payload in (lf, crlf):
        path.write_bytes(payload)
        parsed, errors = verify_json_artifact_identity(path, expected_raw_sha256=expected_raw, expected_canonical_sha256=expected_canonical)
        assert parsed == value
        assert errors == []


@pytest.mark.parametrize(
    "mutation",
    [
        {"confirmation_sealed": True, "repository_assignments": {"org/a": "confirmation"}, "counts": {"development_train": 1}},
        {"confirmation_sealed": True, "repository_assignments": {"org/a": "development_train"}, "counts": {"development_train": 2}},
    ],
)
def test_partition_json_identity_rejects_semantic_change(tmp_path: Path, mutation: dict) -> None:
    original = {"confirmation_sealed": True, "repository_assignments": {"org/a": "development_train"}, "counts": {"development_train": 1}}
    path = tmp_path / "partition.json"
    path.write_text(json.dumps(mutation), encoding="utf-8")
    _, errors = verify_json_artifact_identity(path, expected_raw_sha256="0" * 64, expected_canonical_sha256=canonical_json_sha256(original))
    assert errors == ["raw and canonical JSON SHA-256 mismatch"]


def test_partition_json_identity_rejects_malformed_json(tmp_path: Path) -> None:
    path = tmp_path / "partition.json"
    path.write_text("{not-json", encoding="utf-8")
    parsed, errors = verify_json_artifact_identity(path, expected_raw_sha256="0" * 64, expected_canonical_sha256="1" * 64)
    assert parsed is None
    assert errors and errors[0].startswith("malformed JSON:")
