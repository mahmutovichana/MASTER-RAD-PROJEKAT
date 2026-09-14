from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from experiments.posthoc_stage3_s1.scripts.kaggle_development_runner import controlled_reranker_memory_checks
from experiments.posthoc_stage3_s1.scripts.retrieval import (
    QwenReranker,
    RERANKER_MAX_LENGTH,
    RERANKER_MODEL_ID,
    RERANKER_PROMPT_TEMPLATE,
    RERANKER_REVISION,
)
from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import (
    atomic_jsonl,
    load_valid_reranker_checkpoints,
    valid_score_checkpoint,
)


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


def reranker_with_failure(fails):
    reranker = object.__new__(QwenReranker)
    reranker.torch = FakeTorch()
    reranker.last_score_diagnostics = {}
    reranker.successful_queries = []
    reranker.successful_documents = []

    def score_batch(query, documents):
        if fails(len(documents)):
            raise InjectedOOM(f"injected OOM at {len(documents)}")
        reranker.successful_queries.append(query)
        reranker.successful_documents.extend(documents)
        return [int(document) / 10.0 for document in documents]

    reranker._score_batch = score_batch
    return reranker


def test_full_reranker_batch_is_attempted_first_and_succeeds():
    reranker = reranker_with_failure(lambda size: False)
    documents = [str(index) for index in range(5)]
    scores = reranker.score("query-exact", documents)
    assert scores == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert reranker.last_score_diagnostics["candidate_count"] == 5
    assert reranker.last_score_diagnostics["attempted_batch_sizes"] == [5]
    assert reranker.last_score_diagnostics["effective_batch_sizes_used"] == [5]
    assert reranker.last_score_diagnostics["oom_split_count"] == 0
    assert reranker.last_score_diagnostics["minimum_effective_batch_size"] == 5
    assert reranker.last_score_diagnostics["single_item_oom"] is False
    assert reranker.last_score_diagnostics["output_count"] == 5


def test_injected_oom_bisects_odd_batch_deterministically_and_preserves_inputs():
    reranker = reranker_with_failure(lambda size: size > 2)
    documents = [str(index) for index in range(5)]
    scores = reranker.score("query-exact", documents)
    assert scores == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert reranker.successful_documents == documents
    assert reranker.successful_queries == ["query-exact"] * 3
    assert reranker.last_score_diagnostics["attempted_batch_sizes"] == [5, 2, 3, 1, 2]
    assert reranker.last_score_diagnostics["effective_batch_sizes_used"] == [2, 1, 2]
    assert reranker.last_score_diagnostics["oom_split_count"] == 2
    assert reranker.last_score_diagnostics["minimum_effective_batch_size"] == 1


def test_recursive_split_can_reach_batch_size_one_without_dropping_candidates():
    reranker = reranker_with_failure(lambda size: size > 1)
    documents = [str(index) for index in range(5)]
    assert reranker.score("query-exact", documents) == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert reranker.successful_documents == documents
    assert reranker.last_score_diagnostics["effective_batch_sizes_used"] == [1] * 5
    assert reranker.last_score_diagnostics["output_count"] == len(documents)


def test_single_item_oom_fails_closed():
    reranker = reranker_with_failure(lambda size: True)
    with pytest.raises(InjectedOOM):
        reranker.score("query", ["0"])
    assert reranker.last_score_diagnostics["single_item_oom"] is True
    assert reranker.last_score_diagnostics["output_count"] == 0


def test_unrelated_runtime_error_propagates_without_split():
    reranker = reranker_with_failure(lambda size: False)
    reranker._score_batch = lambda query, documents: (_ for _ in ()).throw(RuntimeError("unrelated failure"))
    with pytest.raises(RuntimeError, match="unrelated failure"):
        reranker.score("query", ["0", "1"])
    assert reranker.last_score_diagnostics["attempted_batch_sizes"] == [2]
    assert reranker.last_score_diagnostics["oom_split_count"] == 0


def test_canary_controlled_fault_injection_covers_fallback_guards():
    result = controlled_reranker_memory_checks(FakeTorch())
    assert result["recursive_split_exercised"] is True
    assert result["original_order_preserved"] is True
    assert result["no_candidate_dropped"] is True
    assert result["single_item_oom_fails_closed"] is True
    assert result["unrelated_runtime_error_propagates"] is True


@pytest.mark.parametrize("bad_scores", [[0.1], [float("nan"), 0.2], [-0.1, 0.2], [0.1, 1.1]])
def test_score_count_finiteness_and_probability_bounds_are_enforced(bad_scores):
    reranker = reranker_with_failure(lambda size: False)
    reranker._score_batch = lambda query, documents: bad_scores
    with pytest.raises(RuntimeError, match="score count|non-finite|out-of-range"):
        reranker.score("query", ["0", "1"])


def test_frozen_reranker_model_prompt_scoring_and_no_cpu_fallback():
    assert RERANKER_MAX_LENGTH == 8192
    assert (RERANKER_MODEL_ID, RERANKER_REVISION) == (
        "Qwen/Qwen3-Reranker-0.6B", "e61197ed45024b0ed8a2d74b80b4d909f1255473",
    )
    assert RERANKER_PROMPT_TEMPLATE == (
        "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query. Answer only yes or no.<|im_end|>\n"
        "<|im_start|>user\n<Query>: {query}\n<Document>: {document}<|im_end|>\n<|im_start|>assistant\n"
    )
    source = (BASE / "scripts/retrieval.py").read_text(encoding="utf-8")
    for phrase in (
        "padding=True", "truncation=True", "max_length=RERANKER_MAX_LENGTH", "[self.no_id, self.yes_id]",
        "torch.softmax(logits, dim=1)[:, 1]",
    ):
        assert phrase in source
    assert "device or \"cpu\"" not in source


def reranker_record(case_id="case-1", indices=None, scores=None):
    indices = [2, 10] if indices is None else indices
    scores = [0.25, 0.75] if scores is None else scores
    return {
        "case_id": case_id,
        "candidate_indices": indices,
        "scores": {str(index): score for index, score in zip(indices, scores)},
        "reranker_runtime_diagnostics": {"candidate_count": len(indices), "output_count": len(scores)},
    }


def test_valid_persisted_reranker_row_is_reused(tmp_path):
    path = tmp_path / "reranker_scores.jsonl"
    record = reranker_record()
    atomic_jsonl(path, [record])
    assert load_valid_reranker_checkpoints(path, {"case-1": [2, 10]}) == {"case-1": record}
    assert not path.with_suffix(".jsonl.tmp").exists()


@pytest.mark.parametrize(
    "record",
    [
        {"case_id": "case-1", "candidate_indices": [2, 10], "scores": {"2": 0.25}},
        reranker_record(indices=[10, 2]),
        reranker_record(scores=[float("nan"), 0.75]),
    ],
)
def test_invalid_reranker_row_is_ignored_for_safe_recomputation(tmp_path, record):
    path = tmp_path / "reranker_scores.jsonl"
    path.write_text(json.dumps(record) + "\n{partial", encoding="utf-8")
    assert load_valid_reranker_checkpoints(path, {"case-1": [2, 10]}) == {}


def test_duplicate_reranker_case_id_is_rejected(tmp_path):
    path = tmp_path / "reranker_scores.jsonl"
    record = reranker_record()
    path.write_text(json.dumps(record) + "\n" + json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Duplicate reranker checkpoint case_id"):
        load_valid_reranker_checkpoints(path, {"case-1": [2, 10]})


def test_completed_embedding_checkpoint_validation_is_read_only(tmp_path):
    path = tmp_path / "case.npz"
    np.savez_compressed(
        path,
        case_id="case-1",
        query_embedding=np.zeros(1024),
        document_embeddings=np.zeros((2, 1024)),
        lexical_scores=np.zeros(2),
        dense_scores=np.zeros(2),
    )
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert valid_score_checkpoint(path, "case-1", 2) is True
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
