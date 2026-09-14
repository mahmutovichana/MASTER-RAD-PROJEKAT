from __future__ import annotations

import hashlib
import inspect
import json
from functools import lru_cache
from pathlib import Path

import numpy as np

from experiments.posthoc_stage3_s1.scripts import retrieval
from experiments.posthoc_stage3_s1.scripts.kaggle_development_runner import run_canary
from experiments.posthoc_stage3_s1.scripts.repository_corpus import DocumentChunk
from experiments.posthoc_stage3_s1.scripts.repository_corpus import discover_candidates, resolve_pre_change_source
from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import (
    ACTIVE_RETRIEVAL_METHOD,
    CONTROLLED_TARGET_COUNT,
    FROZEN_LEXICAL_METRICS,
    RANK2_REGRESSION_CASES,
    THRESHOLDS,
    count_durable_jsonl_rows_without_scores,
    main,
    paired_prompt_run_keys,
    prompt_selection_case_ids,
    selected_prompt_missing_run_keys,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import GENERATOR_MODEL_ID, GENERATOR_REVISION, build_retrieval_query


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


def test_phase0_whole_document_representation_and_exact_truncation():
    document = retrieval.phase0_document_chunk(
        "docs/a.md", "x" * 100_001, priority_tier="B", path_distance=4, identifier_overlap=2,
    )
    assert (document.heading, document.heading_path, document.chunk_index) == ("", (), 0)
    assert len(document.text) == 100_000
    assert (document.priority_tier, document.path_distance, document.identifier_overlap) == ("B", 4, 2)


def test_phase0_metadata_order_is_score_tier_distance_overlap_path(monkeypatch):
    documents = [
        retrieval.phase0_document_chunk("z.md", "z", priority_tier="A", path_distance=1, identifier_overlap=0),
        retrieval.phase0_document_chunk("b.md", "b", priority_tier="A", path_distance=1, identifier_overlap=2),
        retrieval.phase0_document_chunk("a.md", "a", priority_tier="A", path_distance=1, identifier_overlap=2),
        retrieval.phase0_document_chunk("tier.md", "t", priority_tier="B", path_distance=0, identifier_overlap=9),
        retrieval.phase0_document_chunk("distance.md", "d", priority_tier="A", path_distance=2, identifier_overlap=9),
        retrieval.phase0_document_chunk("score.md", "s", priority_tier="D", path_distance=9, identifier_overlap=0),
    ]
    monkeypatch.setattr(retrieval, "lexical_scores", lambda query, values: np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.6]))
    ranked = retrieval.phase0_rank_documents("query", documents)
    assert [item.chunk.path for item in ranked] == ["score.md", "a.md", "b.md", "z.md", "distance.md", "tier.md"]


def test_representative_section_localization_is_deterministic_and_cannot_change_document_rank(monkeypatch):
    documents = [
        retrieval.phase0_document_chunk(path, path, priority_tier="A", path_distance=0, identifier_overlap=0)
        for path in ("a.md", "b.md", "c.md", "d.md")
    ]
    semantic = [
        DocumentChunk(path, str(index), (str(index),), f"{path}-{index}", index)
        for path in ("a.md", "b.md", "c.md", "d.md") for index in (1, 0)
    ]
    calls = iter((np.array([0.9, 0.8, 0.7, 0.6]), np.array([0.5, 0.5]), np.array([0.1, 0.9]), np.array([0.4, 0.4])))
    monkeypatch.setattr(retrieval, "lexical_scores", lambda query, values: next(calls))
    ranked = retrieval.phase0_rank_documents("query", documents)
    localized = retrieval.localize_representative_sections("query", ranked, semantic)
    assert [item.chunk.path for item in localized] == ["a.md", "b.md", "c.md"]
    assert [item.chunk.chunk_index for item in localized] == [0, 0, 0]
    assert [item.lexical_score for item in localized] == [0.9, 0.8, 0.7]
    assert all(item.dense_score is None and item.reranker_score is None for item in localized)


def _read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


@lru_cache(maxsize=1)
def _controlled_rank_reproduction():
    sampled = _read_jsonl(ROOT / "reports/final_v2/gate4/primary_sample.jsonl") + _read_jsonl(ROOT / "reports/final_v2/gate4/secondary_stress_sample.jsonl")
    gold = {}
    for split in ("train", "validation"):
        for row in _read_jsonl(ROOT / f"experiments/consolidated_enriched_training_v2/gold/{split}.jsonl"):
            gold[row["case_id"]] = row
    reproduced = []
    for sampled_row in sampled:
        base = gold.get(sampled_row["case_id"], {})
        if not base.get("synthetic_target_doc_path"):
            continue
        row = dict(base)
        row.update(sampled_row)
        source = resolve_pre_change_source(row, root=ROOT)
        assert source.kind == "frozen_controlled_baseline"
        local_root = Path(source.local_root)
        paths = [item.relative_to(local_root).as_posix() for item in local_root.rglob("*") if item.is_file()]
        candidates = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or ""))
        documents = [
            retrieval.phase0_document_chunk(
                path,
                (local_root / Path(path)).read_text(encoding="utf-8", errors="replace"),
                priority_tier=tier,
                path_distance=distance,
                identifier_overlap=overlap,
            )
            for path, tier, distance, overlap in candidates
        ]
        ranked = retrieval.phase0_rank_documents(build_retrieval_query(row), documents)
        ranked_paths = [item.chunk.path for item in ranked]
        target = base["synthetic_target_doc_path"]
        reproduced.append({"case_id": row["case_id"], "target_document": target, "lexical_rank": ranked_paths.index(target) + 1 if target in ranked_paths else None})
    return reproduced


def test_controlled_phase0_metrics_are_frozen_and_natural_rows_are_excluded():
    audit = json.loads((BASE / "development/local_lexical_target_diagnostics.json").read_text(encoding="utf-8"))
    reproduced_cases = _controlled_rank_reproduction()
    assert reproduced_cases == [
        {key: value for key, value in item.items() if key in {"case_id", "target_document", "lexical_rank"}}
        for item in audit["cases"]
    ]
    ranks = [item["lexical_rank"] for item in reproduced_cases]
    reproduced = {
        "n": len(ranks),
        "hit_at_1": sum(rank == 1 for rank in ranks) / len(ranks),
        "hit_at_3": sum(rank is not None and rank <= 3 for rank in ranks) / len(ranks),
        "hit_at_5": sum(rank is not None and rank <= 5 for rank in ranks) / len(ranks),
        "hit_at_10": sum(rank is not None and rank <= 10 for rank in ranks) / len(ranks),
        "mrr": sum(0 if rank is None else 1 / rank for rank in ranks) / len(ranks),
    }
    assert ACTIVE_RETRIEVAL_METHOD == "PHASE0_EXACT_DOCUMENT_LEXICAL_TOP3"
    assert CONTROLLED_TARGET_COUNT == 79
    assert reproduced == FROZEN_LEXICAL_METRICS
    rank_map = {item["case_id"]: item["lexical_rank"] for item in reproduced_cases}
    assert all(rank_map[case_id] == 2 for case_id in RANK2_REGRESSION_CASES)
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


def test_amendment07_records_pre_generation_correction_and_unchanged_boundaries():
    amendment = json.loads((BASE / "S1_RUNTIME_AMENDMENT_07_PHASE0_RETRIEVAL_REPRODUCTION.json").read_text(encoding="utf-8"))
    assert amendment["scientific_status"] == "PRE-GENERATION IMPLEMENTATION CORRECTION TO AMENDMENT 06"
    assert amendment["amendment06_observed_metrics_not_adopted"]["used_for_method_selection"] is False
    assert amendment["generation_rows_before_amendment"] == 0
    assert amendment["prompt_selection_occurred"] is False
    assert amendment["development_metrics_produced"] is False
    assert amendment["embedding_model_loaded"] is False
    assert amendment["reranker_model_loaded"] is False
    assert amendment["partial_reranker_scores_read"] is False
    assert amendment["confirmation_accessed"] is False
    assert amendment["gate6_row_level_human_data_accessed"] is False
    assert amendment["mandatory_pre_generation_validation"]["required_metrics"] == {
        "hit_at_1": 0.9746835443037974,
        "hit_at_3": 1.0,
        "hit_at_5": 1.0,
        "hit_at_10": 1.0,
        "mrr": 0.9873417721518988,
    }
