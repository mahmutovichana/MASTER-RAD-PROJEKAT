from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from docguard_ml_v2.gate2_study import (
    append_registry,
    assert_inner_repo_disjoint,
    assert_registered_family,
    development_view_hash,
    load_development_rows,
    load_fold_map,
    make_outer_folds,
    safe_code_view,
    safe_docs_view,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/final_v2/gate2_model_study.json"


def test_canonical_loader_verifies_hash_and_refuses_confirmation() -> None:
    rows, metadata = load_development_rows(config_path=CONFIG)
    assert len(rows) == 22166
    assert metadata["confirmation_rows_excluded"] == 3747
    assert not any(row["partition"] == "confirmation" for row in rows)


def test_sha_mismatch_blocks_gate2(tmp_path: Path) -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["gate1"]["gold_sha256"] = "0" * 64
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Gate 1 SHA mismatch"):
        load_development_rows(config_path=bad)


def test_safe_views_use_only_preregistered_fields() -> None:
    row = {
        "language": "Python",
        "code_changed_files": ["a.py"],
        "code_diff_excerpt": "+ x = 1",
        "docs_before_excerpt": "Old docs",
        "pr_title": "MUST NOT APPEAR",
        "human_label_notes": "MUST NOT APPEAR",
    }
    combined = safe_code_view(row) + safe_docs_view(row)
    assert "Python".lower() in combined.lower()
    assert "+ x = 1" in combined and "Old docs" in combined
    assert "MUST NOT APPEAR" not in combined


def test_fold_generation_is_deterministic_and_repo_disjoint() -> None:
    rows, _ = load_development_rows(config_path=CONFIG)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    first, splits = make_outer_folds(rows, task="binary", config=config)
    second, second_splits = make_outer_folds(rows, task="binary", config=config)
    assert splits == second_splits == 5
    assert first == second
    assert len(first) == len({row["repository"] for row in first}) == 232


def test_frozen_fold_files_have_one_assignment_per_repository() -> None:
    for task, expected in [("binary", 232), ("category", 98)]:
        mapping = load_fold_map(ROOT / f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv", task=task)
        assert len(mapping) == expected
        assert set(mapping.values()) == {0, 1, 2, 3, 4}


def test_inner_fold_overlap_is_rejected() -> None:
    rows = [{"repository": "a"}, {"repository": "b"}, {"repository": "a"}]
    assert_inner_repo_disjoint(rows, [0], [1])
    with pytest.raises(RuntimeError, match="Inner repository leakage"):
        assert_inner_repo_disjoint(rows, [0], [2])


def test_unregistered_family_is_rejected() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    for family in ["M0", "M1", "M2", "M3"]:
        assert_registered_family(config, family)
    with pytest.raises(ValueError, match="Unregistered"):
        assert_registered_family(config, "CodeBERT")


def test_embedding_identity_is_stable_and_order_independent() -> None:
    rows = [
        {"case_id": "b", "repository": "x/b", "partition": "development_train", "language": "go", "code_changed_files": [], "code_diff_excerpt": "b", "docs_before_excerpt": "d", "gold_docs_update_required": False, "gold_doc_category": "no_update"},
        {"case_id": "a", "repository": "x/a", "partition": "development_validation", "language": "python", "code_changed_files": ["a.py"], "code_diff_excerpt": "a", "docs_before_excerpt": "", "gold_docs_update_required": True, "gold_doc_category": "api_reference"},
    ]
    assert development_view_hash(rows) == development_view_hash(list(reversed(rows)))


def test_registry_is_append_only_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "registry.jsonl"
    base = {"run_id": "r1", "task": "binary", "family": "M1", "outer_fold": 0, "config": {}, "random_seed": 42, "source_commit": "abc", "gold_sha": "def"}
    append_registry(path, {**base, "status": "STARTED"})
    append_registry(path, {**base, "status": "COMPLETED", "result_artifact_identity": "123"})
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [row["status"] for row in records] == ["STARTED", "COMPLETED"]


def test_preregistered_config_and_fold_hashes_match_manifest() -> None:
    manifest = json.loads((ROOT / "reports/final_v2/gate2/development_view_manifest.json").read_text(encoding="utf-8"))
    assert manifest["config_sha256"] == hashlib.sha256(CONFIG.read_bytes()).hexdigest()
    for task in ("binary", "category"):
        path = ROOT / manifest["fold_artifacts"][task]["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest["fold_artifacts"][task]["sha256"]
