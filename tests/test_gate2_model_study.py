from __future__ import annotations

import csv
import hashlib
import json
import tarfile
from pathlib import Path

import pytest
import numpy as np

from docguard_ml_v2.gate2_study import (
    append_registry,
    assert_inner_repo_disjoint,
    assert_registered_family,
    development_view_hash,
    load_development_rows,
    load_fold_map,
    load_fold_checkpoint,
    make_outer_folds,
    safe_code_view,
    safe_docs_view,
    write_fold_checkpoint,
)
from scripts.extract_gate2_unixcoder_embeddings import open_embedding_checkpoint, persist_embedding_chunk, run as run_embedding_extraction
from scripts.manage_gate2_checkpoint import export_checkpoint, restore_checkpoint, scientific_identity
from scripts.run_gate2_external_compute import Stage, execute_fail_closed, require_embedding_compute


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


def _persist_fake_embedding(checkpoint: Path, chunks: list[tuple[int, int]]) -> tuple[bytes, bytes, dict]:
    identity = {"gold_sha256": "gold", "development_view_sha256": "view", "row_order_sha256": "rows", "encoder_revision": "encoder", "tokenizer_revision": "tokenizer", "pooling": "mean", "max_length": 512, "dtype": "float32"}
    metadata = arrays = metadata_path = None
    for chunk_index, (start, stop) in enumerate(chunks):
        metadata, arrays, metadata_path = open_embedding_checkpoint(checkpoint, identity=identity, total_rows=6, hidden_size=3, resume=chunk_index > 0)
        values = np.arange(start * 3, stop * 3, dtype=np.float32).reshape(stop - start, 3)
        persist_embedding_chunk(metadata=metadata, metadata_path=metadata_path, arrays=arrays, start=start, code=values, docs=values + 100, code_lengths=np.arange(start, stop, dtype=np.int32), docs_lengths=np.arange(start, stop, dtype=np.int32) + 10, code_truncated=np.zeros(stop - start, dtype=np.uint8), docs_truncated=np.ones(stop - start, dtype=np.uint8))
        del arrays
    assert metadata is not None
    return (checkpoint / "code.mmap").read_bytes(), (checkpoint / "docs.mmap").read_bytes(), metadata


def test_embedding_uninterrupted_equals_interrupted_then_resumed(tmp_path: Path) -> None:
    whole = _persist_fake_embedding(tmp_path / "whole", [(0, 6)])
    resumed = _persist_fake_embedding(tmp_path / "resumed", [(0, 2), (2, 6)])
    assert whole == resumed


def test_embedding_resume_rejects_identity_mismatch(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint"
    _persist_fake_embedding(checkpoint, [(0, 2)])
    bad = {"gold_sha256": "changed", "development_view_sha256": "view", "row_order_sha256": "rows", "encoder_revision": "encoder", "tokenizer_revision": "tokenizer", "pooling": "mean", "max_length": 512, "dtype": "float32"}
    with pytest.raises(RuntimeError, match="identity mismatch: gold_sha256"):
        open_embedding_checkpoint(checkpoint, identity=bad, total_rows=6, hidden_size=3, resume=True)


def test_embedding_resume_rejects_corrupt_checkpoint(tmp_path: Path) -> None:
    checkpoint = tmp_path / "checkpoint"
    _persist_fake_embedding(checkpoint, [(0, 2)])
    (checkpoint / "code.mmap").write_bytes(b"broken")
    identity = {"gold_sha256": "gold", "development_view_sha256": "view", "row_order_sha256": "rows", "encoder_revision": "encoder", "tokenizer_revision": "tokenizer", "pooling": "mean", "max_length": 512, "dtype": "float32"}
    with pytest.raises(RuntimeError, match="corrupt or incomplete"):
        open_embedding_checkpoint(checkpoint, identity=identity, total_rows=6, hidden_size=3, resume=True)


def _fold_payload(fold: int, case_ids: list[str], predictions: list[int]) -> dict:
    return {
        "status": "COMPLETE",
        "task": "binary",
        "family": "M1",
        "outer_fold": fold,
        "gold_sha256": "gold",
        "development_view_sha256": "view",
        "scientific_config_sha256": "config",
        "fold_assignment_sha256": "folds",
        "selected_config": {"C": 1.0, "class_weight": None, "semantic_scale": 1.0},
        "selected_threshold": 0.5,
        "validation_case_ids": case_ids,
        "validation_predictions": predictions,
        "validation_probabilities": [0.1 if value == 0 else 0.9 for value in predictions],
        "result": {"outer_fold": fold, "outer_metrics": {"mcc": 1.0}},
    }


def test_fold_uninterrupted_equals_interrupted_then_resumed(tmp_path: Path) -> None:
    expected = {"a": 0, "b": 1, "c": 1, "d": 0}
    identity_base = {"task": "binary", "family": "M1", "gold_sha256": "gold", "development_view_sha256": "view", "scientific_config_sha256": "config", "fold_assignment_sha256": "folds"}
    uninterrupted: dict[str, int] = {}
    resumed: dict[str, int] = {}
    for fold, ids, predictions in [(0, ["a", "b"], [0, 1]), (1, ["c", "d"], [1, 0])]:
        path = tmp_path / f"fold{fold}.json"
        write_fold_checkpoint(path, _fold_payload(fold, ids, predictions))
        checkpoint = load_fold_checkpoint(path, expected_identity={**identity_base, "outer_fold": fold})
        uninterrupted.update(zip(checkpoint["validation_case_ids"], checkpoint["validation_predictions"]))
    first = load_fold_checkpoint(tmp_path / "fold0.json", expected_identity={**identity_base, "outer_fold": 0})
    resumed.update(zip(first["validation_case_ids"], first["validation_predictions"]))
    second = load_fold_checkpoint(tmp_path / "fold1.json", expected_identity={**identity_base, "outer_fold": 1})
    resumed.update(zip(second["validation_case_ids"], second["validation_predictions"]))
    assert uninterrupted == resumed == expected


@pytest.mark.parametrize("field", ["scientific_config_sha256", "gold_sha256", "fold_assignment_sha256"])
def test_fold_resume_rejects_identity_mismatch(tmp_path: Path, field: str) -> None:
    path = tmp_path / "fold.json"
    payload = _fold_payload(0, ["a"], [1])
    write_fold_checkpoint(path, payload)
    identity = {key: payload[key] for key in ["task", "family", "outer_fold", "gold_sha256", "development_view_sha256", "scientific_config_sha256", "fold_assignment_sha256"]}
    identity[field] = "changed"
    with pytest.raises(RuntimeError, match=f"identity mismatch: {field}"):
        load_fold_checkpoint(path, expected_identity=identity)


def test_fold_resume_rejects_corrupt_checkpoint(tmp_path: Path) -> None:
    path = tmp_path / "fold.json"
    payload = _fold_payload(0, ["a"], [1])
    write_fold_checkpoint(path, payload)
    content = json.loads(path.read_text(encoding="utf-8"))
    content["validation_predictions"] = [0]
    path.write_text(json.dumps(content), encoding="utf-8")
    identity = {key: payload[key] for key in ["task", "family", "outer_fold", "gold_sha256", "development_view_sha256", "scientific_config_sha256", "fold_assignment_sha256"]}
    with pytest.raises(RuntimeError, match="payload hash"):
        load_fold_checkpoint(path, expected_identity=identity)


def test_external_wrapper_stops_after_failed_gate1_stage(tmp_path: Path) -> None:
    called: list[str] = []

    def fail_gate1() -> None:
        called.append("gate1")
        raise RuntimeError("Gate 1 failed")

    def forbidden_later_stage() -> None:
        called.append("embedding")

    with pytest.raises(RuntimeError, match="Gate 1 failed"):
        execute_fail_closed(
            [Stage("gate1_freeze_verifier", fail_gate1), Stage("embedding", forbidden_later_stage)],
            status_path=tmp_path / "status.json",
            event_path=tmp_path / "events.jsonl",
        )
    assert called == ["gate1"]
    status = json.loads((tmp_path / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "FAILED"
    assert status["failed_stage"] == "gate1_freeze_verifier"
    assert status["confirmation_accessed"] is False


def _portable_checkpoint(tmp_path: Path) -> tuple[Path, Path]:
    persistent = tmp_path / "persistent"
    checkpoint = persistent / "embedding_checkpoint"
    identity = scientific_identity(CONFIG)
    embedding_identity = {key: identity[key] for key in ["gold_sha256", "development_view_sha256", "row_order_sha256", "encoder_revision", "tokenizer_revision", "pooling", "max_length", "dtype"]}
    metadata, arrays, metadata_path = open_embedding_checkpoint(
        checkpoint,
        identity=embedding_identity,
        total_rows=identity["development_rows"],
        hidden_size=1,
        resume=False,
    )
    del arrays
    archive = tmp_path / "gate2_checkpoint.tar.gz"
    export_checkpoint(CONFIG, persistent, archive)
    return persistent, archive


def test_portable_checkpoint_export_restore(tmp_path: Path) -> None:
    persistent, archive = _portable_checkpoint(tmp_path)
    second_archive = tmp_path / "second-name.tar.gz"
    export_checkpoint(CONFIG, persistent, second_archive)
    assert archive.read_bytes() == second_archive.read_bytes()
    restored = tmp_path / "restored"
    result = restore_checkpoint(CONFIG, restored, archive)
    assert result["status"] == "RESTORED"
    assert (restored / "embedding_checkpoint/embedding_checkpoint.json").is_file()
    with tarfile.open(archive, "r:gz") as handle:
        names = {member.name for member in handle.getmembers()}
    assert not any("confirmation" in name.lower() or "token" in name.lower() or "cache" in name.lower() for name in names)


def test_portable_checkpoint_rejects_corruption(tmp_path: Path) -> None:
    _, archive = _portable_checkpoint(tmp_path)
    unpacked = tmp_path / "unpacked"
    with tarfile.open(archive, "r:gz") as handle:
        handle.extractall(unpacked, filter="data")
    (unpacked / "embedding_checkpoint/code.mmap").write_bytes(b"corrupt")
    corrupt = tmp_path / "corrupt.tar.gz"
    with tarfile.open(corrupt, "w:gz") as handle:
        for path in sorted(unpacked.rglob("*")):
            if path.is_file():
                handle.add(path, arcname=path.relative_to(unpacked).as_posix())
    with pytest.raises(RuntimeError, match="member hash mismatch"):
        restore_checkpoint(CONFIG, tmp_path / "corrupt-restore", corrupt)


def test_portable_checkpoint_rejects_scientific_identity_mismatch(tmp_path: Path) -> None:
    _, archive = _portable_checkpoint(tmp_path)
    changed = json.loads(CONFIG.read_text(encoding="utf-8"))
    changed["seed"] = 999
    changed_config = tmp_path / "changed.json"
    changed_config.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(RuntimeError, match="scientific identity mismatch"):
        restore_checkpoint(changed_config, tmp_path / "wrong-study", archive)


def test_complete_embeddings_allow_cpu_continuation() -> None:
    assert require_embedding_compute(complete_artifact=True, complete_checkpoint=False, cuda_available=False)
    assert require_embedding_compute(complete_artifact=False, complete_checkpoint=True, cuda_available=False)


def test_incomplete_embeddings_require_gpu() -> None:
    with pytest.raises(RuntimeError, match="CUDA GPU is required"):
        require_embedding_compute(complete_artifact=False, complete_checkpoint=False, cuda_available=False)
    assert require_embedding_compute(complete_artifact=False, complete_checkpoint=False, cuda_available=True) is False


def test_complete_embedding_memmaps_finalize_on_cpu(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    identity = scientific_identity(CONFIG)
    embedding_identity = {key: identity[key] for key in ["gold_sha256", "development_view_sha256", "row_order_sha256", "encoder_revision", "tokenizer_revision", "pooling", "max_length", "dtype"]}
    checkpoint = tmp_path / "checkpoint"
    metadata, arrays, metadata_path = open_embedding_checkpoint(
        checkpoint,
        identity=embedding_identity,
        total_rows=identity["development_rows"],
        hidden_size=1,
        resume=False,
    )
    for array in arrays.values():
        array.flush()
    del arrays
    metadata["completed_count"] = identity["development_rows"]
    metadata["status"] = "COMPLETE"
    metadata["extraction"] = {"encoder_repository": "microsoft/unixcoder-base", "device": "test GPU"}
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

    real_import = __import__

    def forbid_cuda_stack(name: str, *args, **kwargs):
        if name == "torch" or name.startswith("transformers"):
            raise AssertionError("COMPLETE checkpoint must not import the CUDA/model stack")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", forbid_cuda_stack)
    manifest = run_embedding_extraction(CONFIG, tmp_path / "embeddings", 16, checkpoint_dir=checkpoint, resume=True)
    assert manifest["status"] == "COMPLETE"
    assert manifest["confirmation_accessed"] is False
    assert (tmp_path / "embeddings/gate2_unixcoder_embeddings.npz").is_file()
