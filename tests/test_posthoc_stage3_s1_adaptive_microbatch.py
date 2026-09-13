from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pytest

from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_LOGICAL_BATCH_SIZE,
    EMBEDDING_MAX_LENGTH,
    EMBEDDING_MODEL_ID,
    EMBEDDING_REVISION,
    QwenDenseEncoder,
)
from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import valid_score_checkpoint


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


class InjectedOOM(Exception):
    pass


class FakeCuda:
    OutOfMemoryError = InjectedOOM

    def __init__(self):
        self.empty_cache_calls = 0

    def empty_cache(self):
        self.empty_cache_calls += 1


class FakeTorch:
    def __init__(self):
        self.cuda = FakeCuda()


def encoder_with_failure(fails):
    encoder = object.__new__(QwenDenseEncoder)
    encoder.batch_size = EMBEDDING_LOGICAL_BATCH_SIZE
    encoder.torch = FakeTorch()
    encoder.last_encode_diagnostics = {}

    def encode_batch(texts):
        if fails(len(texts)):
            raise InjectedOOM(f"injected OOM at {len(texts)}")
        return np.stack([np.full(1024, float(text), dtype=np.float32) for text in texts])

    encoder._encode_batch = encode_batch
    return encoder


def test_batch_8_success_path_preserves_shape_finiteness_and_order():
    encoder = encoder_with_failure(lambda size: False)
    output = encoder.encode([str(index) for index in range(8)])
    assert output.shape == (8, 1024)
    assert np.isfinite(output).all()
    assert output[:, 0].tolist() == list(map(float, range(8)))
    assert encoder.last_encode_diagnostics["effective_batch_sizes_used"] == [8]
    assert encoder.last_encode_diagnostics["oom_split_count"] == 0


def test_injected_oom_at_8_splits_to_4_in_original_order():
    encoder = encoder_with_failure(lambda size: size == 8)
    output = encoder.encode([str(index) for index in range(8)])
    assert output[:, 0].tolist() == list(map(float, range(8)))
    assert encoder.last_encode_diagnostics["attempted_batch_sizes"] == [8, 4, 4]
    assert encoder.last_encode_diagnostics["effective_batch_sizes_used"] == [4, 4]
    assert encoder.last_encode_diagnostics["minimum_effective_batch_size"] == 4


def test_injected_oom_at_8_and_4_splits_to_2():
    encoder = encoder_with_failure(lambda size: size >= 4)
    output = encoder.encode([str(index) for index in range(8)])
    assert output.shape == (8, 1024)
    assert output[:, 0].tolist() == list(map(float, range(8)))
    assert encoder.last_encode_diagnostics["effective_batch_sizes_used"] == [2, 2, 2, 2]
    assert encoder.last_encode_diagnostics["oom_split_count"] == 3


def test_injected_oom_until_batch_1_succeeds():
    encoder = encoder_with_failure(lambda size: size > 1)
    output = encoder.encode([str(index) for index in range(8)])
    assert output[:, 0].tolist() == list(map(float, range(8)))
    assert encoder.last_encode_diagnostics["effective_batch_sizes_used"] == [1] * 8
    assert encoder.last_encode_diagnostics["minimum_effective_batch_size"] == 1
    assert encoder.last_encode_diagnostics["single_item_oom"] is False


def test_oom_at_batch_1_fails_closed():
    encoder = encoder_with_failure(lambda size: True)
    with pytest.raises(InjectedOOM):
        encoder.encode(["0"])
    assert encoder.last_encode_diagnostics["single_item_oom"] is True
    assert encoder.last_encode_diagnostics["effective_batch_sizes_used"] == []


def test_non_oom_exception_propagates_without_split():
    encoder = encoder_with_failure(lambda size: False)
    encoder._encode_batch = lambda texts: (_ for _ in ()).throw(RuntimeError("unrelated failure"))
    with pytest.raises(RuntimeError, match="unrelated failure"):
        encoder.encode(["0"] * 8)
    assert encoder.last_encode_diagnostics["attempted_batch_sizes"] == [8]
    assert encoder.last_encode_diagnostics["oom_split_count"] == 0


def test_frozen_embedding_contract_and_no_cpu_fallback():
    assert EMBEDDING_LOGICAL_BATCH_SIZE == 8
    assert EMBEDDING_MAX_LENGTH == 8192
    assert (EMBEDDING_MODEL_ID, EMBEDDING_REVISION) == (
        "Qwen/Qwen3-Embedding-0.6B", "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3",
    )
    source = (BASE / "scripts/retrieval.py").read_text(encoding="utf-8")
    assert "max_length=EMBEDDING_MAX_LENGTH" in source
    assert "cpu fallback" not in source.casefold()


def write_valid_score(path: Path, case_id: str, documents: int):
    np.savez_compressed(
        path,
        case_id=case_id,
        query_embedding=np.zeros(1024),
        document_embeddings=np.zeros((documents, 1024)),
        lexical_scores=np.zeros(documents),
        dense_scores=np.zeros(documents),
    )


def test_valid_completed_score_checkpoint_is_reused(tmp_path):
    path = tmp_path / "case.npz"
    write_valid_score(path, "case-1", 3)
    assert valid_score_checkpoint(path, "case-1", 3) is True


def test_temporary_or_incomplete_score_checkpoint_is_not_complete(tmp_path):
    temporary = tmp_path / "case.npz.tmp"
    temporary.write_bytes(b"partial")
    incomplete = tmp_path / "case.npz"
    np.savez_compressed(incomplete, case_id="case-1", query_embedding=np.zeros(1024))
    assert valid_score_checkpoint(temporary, "case-1", 3) is False
    assert valid_score_checkpoint(incomplete, "case-1", 3) is False


def test_p1_p2_hashes_remain_unchanged():
    expected = {
        "P1_generation.txt": "c8d1ff147c7873c77ae20f631d979618e9d5296300350a9ff621b782cc963d1c",
        "P2_generation.txt": "7de26510a0b9380ad43da9e6dcb39557bc8ca4dbb131b3c0b798870b64a5d7d3",
    }
    for name, digest in expected.items():
        assert hashlib.sha256((BASE / "prompts" / name).read_bytes()).hexdigest() == digest
