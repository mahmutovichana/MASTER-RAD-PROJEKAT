from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

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
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


class DeterministicTokenizer:
    def __init__(self):
        self.calls = []

    def __call__(self, prompts, **kwargs):
        self.calls.append((list(prompts), dict(kwargs)))
        rows = []
        for prompt in prompts:
            marker = sum(prompt.encode("utf-8")) % 17
            rows.append([1, 2, marker, 4, 5])
        return {
            "input_ids": torch.tensor(rows, dtype=torch.long),
            "attention_mask": torch.ones((len(rows), 5), dtype=torch.long),
        }


class DeterministicCausalLM(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(1), requires_grad=False)
        self.calls = []

    def forward(self, input_ids, attention_mask, *, logits_to_keep, use_cache):
        self.calls.append({
            "input_ids": input_ids.detach().clone(),
            "attention_mask": attention_mask.detach().clone(),
            "logits_to_keep": logits_to_keep,
            "use_cache": use_cache,
        })
        positions = input_ids.float().cumsum(dim=1).unsqueeze(-1)
        vocabulary = torch.arange(8, dtype=torch.float32).reshape(1, 1, 8)
        logits = positions * (vocabulary + 1.0) / 19.0 + vocabulary / 13.0
        if logits_to_keep:
            logits = logits[:, -logits_to_keep:, :]
        return SimpleNamespace(logits=logits)


def deterministic_reranker():
    reranker = object.__new__(QwenReranker)
    reranker.torch = torch
    reranker.tokenizer = DeterministicTokenizer()
    reranker.model = DeterministicCausalLM()
    reranker.no_id = 2
    reranker.yes_id = 3
    reranker.last_score_diagnostics = {}
    return reranker


def test_old_full_logits_and_last_token_only_probabilities_are_equivalent():
    reranker = deterministic_reranker()
    query = "deterministic query"
    documents = ["first document", "second document", "third document"]
    result = reranker.verify_last_token_equivalence(query, documents)
    assert result["equivalent"] is True
    assert result["use_cache_false_probability_equivalent"] is True
    assert result["maximum_absolute_difference"] == 0.0
    assert result["old_scores"] == result["new_scores"]
    assert result["pair_count"] == len(documents)
    assert result["tokenizer_output_identical"] is True
    assert result["yes_token_id"] == 3 and result["no_token_id"] == 2


def test_optimized_forward_passes_required_qwen_arguments_and_preserves_inputs():
    reranker = deterministic_reranker()
    query = "query unchanged"
    documents = ["document zero", "document one", "document two"]
    scores = reranker.score(query, documents)
    assert len(scores) == len(documents)
    assert np.isfinite(scores).all()
    assert all(0.0 <= score <= 1.0 for score in scores)
    assert len(reranker.model.calls) == 1
    assert reranker.model.calls[0]["logits_to_keep"] == 1
    assert reranker.model.calls[0]["use_cache"] is False
    prompts, tokenizer_kwargs = reranker.tokenizer.calls[0]
    assert prompts == [RERANKER_PROMPT_TEMPLATE.format(query=query, document=document) for document in documents]
    assert tokenizer_kwargs == {
        "padding": True,
        "truncation": True,
        "max_length": 8192,
        "return_tensors": "pt",
    }
    assert reranker.last_score_diagnostics["forward_mode"] == "LAST_TOKEN_ONLY"
    assert reranker.last_score_diagnostics["logits_to_keep"] == 1
    assert reranker.last_score_diagnostics["use_cache"] is False
    assert reranker.last_score_diagnostics["output_count"] == len(documents)


def test_equivalence_path_explicitly_checks_cache_setting_without_dtype_change():
    reranker = deterministic_reranker()
    result = reranker.verify_last_token_equivalence("q", ["d0", "d1"])
    assert [(call["logits_to_keep"], call["use_cache"]) for call in reranker.model.calls] == [
        (0, False), (1, False), (1, True),
    ]
    assert result["use_cache_false_probability_equivalent"] is True
    assert all(call["input_ids"].dtype == torch.long for call in reranker.model.calls)


def test_frozen_reranker_contract_and_prior_execution_amendments_are_retained():
    assert RERANKER_MAX_LENGTH == 8192
    assert (RERANKER_MODEL_ID, RERANKER_REVISION) == (
        "Qwen/Qwen3-Reranker-0.6B", "e61197ed45024b0ed8a2d74b80b4d909f1255473",
    )
    retrieval_source = (BASE / "scripts/retrieval.py").read_text(encoding="utf-8")
    amendment04 = json.loads((BASE / "S1_PREDEVELOPMENT_AMENDMENT_04_TIME_BUDGET.json").read_text(encoding="utf-8"))
    assert "outputs = self.model(**batch, logits_to_keep=1, use_cache=False)" in retrieval_source
    assert "except self.torch.cuda.OutOfMemoryError" in retrieval_source
    assert "midpoint = size // 2" in retrieval_source
    assert amendment04["two_gpu_reranker_execution"]["implementation"] == "two spawned process workers; no Python threads"
    assert amendment04["two_gpu_reranker_execution"]["worker_devices"] == {"0": "cuda:0", "1": "cuda:1"}


def test_existing_global_and_worker_rows_are_valid_and_reusable_without_mutation(tmp_path):
    expected = {"global": [1], "worker0": [2], "worker1": [3]}
    records = {
        case_id: {"case_id": case_id, "candidate_indices": indices, "scores": {str(indices[0]): 0.5}}
        for case_id, indices in expected.items()
    }
    for case_id in expected:
        path = tmp_path / f"{case_id}.jsonl"
        atomic_jsonl(path, [records[case_id]])
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        assert load_valid_reranker_checkpoints(path, {case_id: expected[case_id]}) == {case_id: records[case_id]}
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before


def test_amendment_boundary_preserves_rows_and_leaves_generation_untouched():
    amendment = json.loads((BASE / "S1_RUNTIME_AMENDMENT_05_LAST_TOKEN_RERANKER.json").read_text(encoding="utf-8"))
    assert amendment["global_reranker_completed_rows"] == 18
    assert amendment["worker0_durable_reranker_rows"] == 8
    assert amendment["worker1_durable_reranker_rows"] == 5
    assert amendment["generation_rows"] == 0
    assert amendment["retrieval_metrics_produced"] is False
    assert amendment["development_metrics_produced"] is False
    assert amendment["prompt_selection_occurred"] is False
    assert amendment["reranker_scores_used_to_choose_amendment"] is False


def test_prompts_thresholds_and_access_boundaries_are_unchanged():
    expected_hashes = {
        "P1_generation.txt": "c8d1ff147c7873c77ae20f631d979618e9d5296300350a9ff621b782cc963d1c",
        "P2_generation.txt": "7de26510a0b9380ad43da9e6dcb39557bc8ca4dbb131b3c0b798870b64a5d7d3",
    }
    assert {
        name: hashlib.sha256((BASE / "prompts" / name).read_bytes()).hexdigest() for name in expected_hashes
    } == expected_hashes
    prereg = json.loads((BASE / "S1_PREREGISTRATION.json").read_text(encoding="utf-8"))
    assert prereg["bounded_selection"]["target_confidence_threshold"] == [0.35, 0.5, 0.65]
    assert prereg["confirmation_accessed"] is False
    assert prereg["gate6_row_level_human_data_accessed"] is False
