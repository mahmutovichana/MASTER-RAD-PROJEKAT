from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

import numpy as np

from experiments.posthoc_stage3_s1.scripts import retrieval
from experiments.posthoc_stage3_s1.scripts.kaggle_development_runner import run_canary
from experiments.posthoc_stage3_s1.scripts.repository_corpus import DocumentChunk
from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import (
    ACTIVE_RETRIEVAL_METHOD,
    CONTROLLED_TARGET_COUNT,
    FROZEN_LEXICAL_METRICS,
    THRESHOLDS,
    count_durable_jsonl_rows_without_scores,
    main,
    paired_prompt_run_keys,
    prompt_selection_case_ids,
    selected_prompt_missing_run_keys,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import GENERATOR_MODEL_ID, GENERATOR_REVISION


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


def rows():
    return [{"case_id": f"case-{index:03d}"} for index in range(200)]


def test_active_path_skips_neural_models_and_does_not_require_reranker_completion():
    main_source = inspect.getsource(main)
    canary_source = inspect.getsource(run_canary)
    assert "QwenDenseEncoder(" not in main_source
    assert "QwenReranker(" not in main_source
    assert "QwenDenseEncoder(" not in canary_source
    assert "QwenReranker(" not in canary_source
    assert '"reranker_checkpoints_required": False' in main_source
    assert '"embedding_model_loaded": False' in main_source
    assert '"reranker_model_loaded": False' in main_source
    assert "reranking_complete.json" not in main_source


def test_partial_reranker_row_counter_never_parses_score_values(tmp_path):
    path = tmp_path / "reranker_scores.jsonl"
    path.write_bytes(b'{"case_id":"one","scores":THIS_IS_NOT_PARSED}\n{"case_id":"two","scores":{"0":0.5}}\npartial')
    assert count_durable_jsonl_rows_without_scores(path) == 2
    source = inspect.getsource(count_durable_jsonl_rows_without_scores)
    assert "json.loads" not in source and "json.dumps" not in source


def test_lexical_ranking_deduplicates_paths_and_returns_three_deterministically(monkeypatch):
    chunks = [
        DocumentChunk("b.md", "", (), "b0", 0),
        DocumentChunk("a.md", "", (), "a1", 1),
        DocumentChunk("a.md", "", (), "a0", 0),
        DocumentChunk("c.md", "", (), "c0", 0),
        DocumentChunk("d.md", "", (), "d0", 0),
    ]
    monkeypatch.setattr(retrieval, "lexical_scores", lambda query, values: np.array([0.9, 0.9, 0.9, 0.8, 0.7]))
    first = retrieval.path_aware_lexical_top_documents("unchanged query", chunks)
    second = retrieval.path_aware_lexical_top_documents("unchanged query", chunks)
    assert [(item.chunk.path, item.chunk.chunk_index) for item in first] == [("a.md", 0), ("b.md", 0), ("c.md", 0)]
    assert [(item.chunk.path, item.chunk.chunk_index) for item in second] == [("a.md", 0), ("b.md", 0), ("c.md", 0)]
    assert len({item.chunk.path for item in first}) == 3
    assert all(item.dense_score is None and item.reranker_score is None for item in first)


def test_controlled_phase0_metrics_are_frozen_and_natural_rows_are_excluded():
    audit = json.loads((BASE / "development/local_lexical_target_diagnostics.json").read_text(encoding="utf-8"))
    reproduced = {
        "n": audit["n"],
        "hit_at_1": audit["target_hit_at_1"],
        "hit_at_3": audit["target_hit_at_3"],
        "mrr": audit["mrr"],
    }
    assert ACTIVE_RETRIEVAL_METHOD == "PATH_AWARE_LEXICAL_TOP3"
    assert CONTROLLED_TARGET_COUNT == 79
    assert reproduced == FROZEN_LEXICAL_METRICS
    main_source = inspect.getsource(main)
    assert '"natural_target_ground_truth": False' in main_source
    assert '"natural_rows_excluded_from_target_accuracy": 121' in main_source
    assert "if active_metrics != FROZEN_LEXICAL_METRICS" in main_source


def test_time_budget_phase_a_and_phase_b_contract_is_unchanged():
    frozen_rows = rows()
    paired_cases = prompt_selection_case_ids(frozen_rows, 50)
    paired_keys = paired_prompt_run_keys(frozen_rows, 50)
    assert len(paired_cases) == 50 and len(paired_keys) == 100
    assert len(set(paired_cases) & {row["case_id"] for row in frozen_rows[:100]}) == 25
    assert len(set(paired_cases) & {row["case_id"] for row in frozen_rows[100:]}) == 25
    completed = set(paired_keys)
    phase_b = selected_prompt_missing_run_keys([row["case_id"] for row in frozen_rows], "P1", completed)
    assert len(phase_b) == 150
    assert all(key.startswith("P1:") for key in phase_b)
    main_source = inspect.getsource(main)
    assert "PROMPT_SELECTION_BLIND_REVIEW_REQUIRED" in main_source
    assert "select_prompt_from_completed_blind_review" in main_source


def test_generator_prompts_thresholds_retries_and_access_boundaries_are_unchanged():
    assert (GENERATOR_MODEL_ID, GENERATOR_REVISION) == (
        "Qwen/Qwen2.5-Coder-14B-Instruct", "aedcc2d42b622764e023cf882b6652e646b95671",
    )
    expected_hashes = {
        "P1_generation.txt": "c8d1ff147c7873c77ae20f631d979618e9d5296300350a9ff621b782cc963d1c",
        "P2_generation.txt": "7de26510a0b9380ad43da9e6dcb39557bc8ca4dbb131b3c0b798870b64a5d7d3",
    }
    assert {name: hashlib.sha256((BASE / "prompts" / name).read_bytes()).hexdigest() for name in expected_hashes} == expected_hashes
    config = json.loads((BASE / "configs/s1_frozen_candidate.json").read_text(encoding="utf-8"))
    assert THRESHOLDS == (0.35, 0.50, 0.65)
    assert config["structured_output_contract"]["schema_correction_retries"] == 1
    assert config["structured_output_contract"]["semantic_documentation_repairs"] == 1
    assert config["confirmation_accessed"] is False
    assert config["gate6_row_level_human_data_accessed"] is False


def test_amendment06_records_scientific_boundary_without_neural_metric_use():
    amendment = json.loads((BASE / "S1_RUNTIME_AMENDMENT_06_LEXICAL_FALLBACK.json").read_text(encoding="utf-8"))
    assert amendment["scientific_label"] == "POST-HOC S1 COMPUTE-CONSTRAINED LEXICAL RETRIEVAL CHALLENGER"
    assert amendment["failure_point"] == "scaled_dot_product_attention"
    assert amendment["generation_rows_before_amendment"] == 0
    assert amendment["neural_reranker_metrics_produced"] is False
    assert amendment["partial_reranker_scores_used_for_fallback_selection"] is False
    assert amendment["confirmation_accessed"] is False
    assert amendment["gate6_row_level_human_data_accessed"] is False
