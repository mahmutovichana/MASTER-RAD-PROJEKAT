from __future__ import annotations

import json
from pathlib import Path

import pytest

from docguard_eval_v2.reference_evaluation import (
    BLIND_FORBIDDEN_FIELDS,
    build_blind_row,
    evaluation_reference_view,
    evaluate_reference_row,
    generation_view,
    reviewer_agreement,
    sample_primary,
    sample_stress,
    summarize_human_reviews,
    summarize_reference,
    validate_review,
    weighted_kappa,
    write_json,
    write_jsonl,
)
from scripts.aggregate_stage3_final_evaluation_v2 import run as aggregate_run
from scripts.build_stage3_confirmation_samples_v2 import run as sample_run
from scripts.finalize_stage3_human_review_v2 import run as finalize_reviews
from scripts.freeze_stage3_v2 import run as freeze_stage3


ROOT = Path(__file__).resolve().parents[1]


def stage3_row(case_id: str, category: str, language: str = "python", positive: bool = True) -> dict:
    return {
        "case_id": case_id,
        "repository": f"org/{case_id}",
        "language": language,
        "code_changed_files": ["src/config.ts"],
        "code_diff_excerpt": "+export const REVIEW_WINDOW = process.env.REVIEW_WINDOW || '7d';",
        "docs_before_excerpt": "# Configuration\n\n## Environment Variables",
        "documentation_context_candidates": [{"path": "docs/configuration.md", "excerpt": "# Configuration"}],
        "pred_docs_update_required": positive,
        "pred_doc_category": category,
        "target_document_path": "docs/configuration.md",
        "generated_patch": {"patch_markdown": "- `REVIEW_WINDOW` controls the review window and defaults to `7d`."},
        "docs_after_excerpt": "# Configuration\n- `REVIEW_WINDOW` controls the review window and defaults to `7d`.",
        "docs_diff_excerpt": "+- `REVIEW_WINDOW` controls the review window and defaults to `7d`.",
        "gold_patch_summary": "Document REVIEW_WINDOW default.",
        "gold_doc_category": category,
        "gold_docs_update_required": True,
        "human_label_notes": "reference only",
        "writer_confidence": 0.9,
        "verifier_result": {"safety_status": "pass"},
        "final_source": "llm",
        "repair_attempted": False,
        "grounded_output": "historical",
        "historical_qwen_output": "historical",
        "reference_metrics": {"score": 1.0},
    }


def review_row(case_id: str, *, approved: bool = True, score: int = 4, accept: str = "yes") -> dict:
    return {
        "case_id": case_id,
        "review_status": "approved" if approved else "pending",
        "human_factual_correctness": score,
        "human_semantic_completeness": score,
        "human_developer_usefulness": score,
        "human_readability": score,
        "human_style_fit": score,
        "human_accept_as_is": accept,
    }


def test_freeze_stage3_does_not_read_confirmation(tmp_path: Path):
    dev_summary = tmp_path / "development_summary.json"
    dev_summary.write_text("{}", encoding="utf-8")
    manifest = freeze_stage3(ROOT / "configs/stage3_semantic_generation_v2.json", ROOT / "docguard_llm_v2", dev_summary, tmp_path / "freeze.json")
    assert manifest["confirmation_accessed"] is False
    assert "pipeline.py" in manifest["source_file_sha256"]


def test_generation_and_reference_views_are_separated():
    row = stage3_row("c1", "configuration")
    gen = generation_view(row)
    ref = evaluation_reference_view(row)
    assert "docs_after_excerpt" not in gen
    assert "docs_diff_excerpt" not in gen
    assert "gold_patch_summary" not in gen
    assert ref["docs_after_excerpt"]


def test_primary_sample_is_natural_distribution_and_deterministic():
    rows = [
        stage3_row("a1", "api_reference"),
        stage3_row("a2", "api_reference"),
        stage3_row("c1", "configuration"),
        stage3_row("n1", "configuration", positive=False),
    ]
    first = sample_primary(rows, seed=5, target_size=3)
    second = sample_primary(rows, seed=5, target_size=3)
    assert [row["case_id"] for row in first] == [row["case_id"] for row in second]
    assert len(first) == 3
    assert [row["pred_doc_category"] for row in first].count("api_reference") == 2


def test_stress_sample_is_supplementary_in_manifest(tmp_path: Path):
    source = tmp_path / "predictions.jsonl"
    rows = [stage3_row(f"{category}{idx}", category) for category in ["api_reference", "configuration", "developer_setup", "model_contract"] for idx in range(2)]
    write_jsonl(source, rows)
    manifest = sample_run(source, tmp_path / "samples", seed=9, target_size=4, stress_per_category=1)
    assert manifest["secondary"]["sampling_method"] == "supplementary_category_stratified_stress_sample"
    assert manifest["secondary_is_supplementary"] is True


def test_blind_sheet_excludes_prohibited_fields():
    blind = build_blind_row(stage3_row("c1", "configuration"))
    assert not (BLIND_FORBIDDEN_FIELDS & set(blind))
    assert "generated_documentation_patch" in blind
    assert "writer_confidence" not in blind
    assert "verifier_result" not in blind


def test_scores_must_be_1_to_5_and_incomplete_reviews_excluded(tmp_path: Path):
    assert validate_review(review_row("ok", score=5))[0] is True
    assert validate_review(review_row("bad", score=6))[0] is False
    input_path = tmp_path / "reviews.jsonl"
    write_jsonl(input_path, [review_row("ok", score=5), review_row("pending", approved=False), review_row("bad", score=0)])
    summary = finalize_reviews(input_path, tmp_path / "finalized")
    assert summary["total_approved"] == 1
    assert summary["excluded_or_incomplete_reviews"] == 2
    assert summary["accept_as_is_rate"] == 1.0


def test_human_summary_metrics_are_correct():
    summary = summarize_human_reviews([review_row("a", score=3, accept="yes"), review_row("b", score=5, accept="no")])
    assert summary["dimensions"]["human_factual_correctness"]["mean"] == 4
    assert summary["dimensions"]["human_factual_correctness"]["median"] == 4.0
    assert summary["accept_as_is_rate"] == 0.5


def test_kappa_and_reviewer_agreement_are_deterministic():
    assert weighted_kappa([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    left = [review_row("a", score=4), review_row("b", score=5, accept="no")]
    right = [review_row("a", score=4), review_row("b", score=3, accept="no")]
    first = reviewer_agreement(left, right)
    second = reviewer_agreement(left, right)
    assert first == second
    assert first["overlap_size"] == 2


def test_reference_metrics_are_deterministic_and_missing_references_supported():
    row = stage3_row("c1", "configuration")
    assert evaluate_reference_row(row) == evaluate_reference_row(row)
    missing = dict(row)
    missing.pop("docs_after_excerpt")
    missing.pop("docs_diff_excerpt")
    missing.pop("gold_patch_summary")
    result = summarize_reference([missing])
    assert result["reference_availability_rate"] == 0.0
    assert result["case_metrics"][0]["reference_available"] is False


def test_safety_and_quality_metrics_remain_separate_and_one_shot_guard_works(tmp_path: Path):
    safety = tmp_path / "safety.json"
    reference = tmp_path / "reference.json"
    reviews = tmp_path / "approved_reviews.jsonl"
    freeze = tmp_path / "freeze.json"
    confirmation = tmp_path / "confirmation.jsonl"
    sample_manifest = tmp_path / "sample_manifest.json"
    write_json(safety, {"safety_pass_rate": 1.0})
    write_json(reference, {"mean_tfidf_cosine": 0.5})
    write_jsonl(reviews, [review_row("a", score=5)])
    write_json(tmp_path / "human_review_summary.json", summarize_human_reviews([review_row("a", score=5)]))
    write_json(freeze, {"config_sha256": "abc", "source_file_sha256": {"pipeline.py": "def"}})
    write_jsonl(confirmation, [stage3_row("a", "configuration")])
    write_json(sample_manifest, {"primary": {}})
    result = aggregate_run(safety=safety, reference=reference, human_reviews=reviews, freeze_manifest=freeze, confirmation_dataset=confirmation, sample_manifest=sample_manifest, output_dir=tmp_path / "agg", enforce_one_shot=True)
    assert "safety_provenance" in result
    assert "reference_metrics_supporting_only" in result
    assert "human_quality_primary" in result
    assert "opaque combined" in result["separation_policy"].lower()
    with pytest.raises(ValueError):
        aggregate_run(safety=safety, reference=reference, human_reviews=reviews, freeze_manifest=freeze, confirmation_dataset=confirmation, sample_manifest=sample_manifest, output_dir=tmp_path / "agg", enforce_one_shot=True)


def test_final_v2_does_not_use_v1_patch_quality_as_truth():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docguard_eval_v2").glob("*.py"))
    assert "patch_quality" not in source
    assert "usefulness_score" not in source.lower()


def test_historical_v1_artifacts_are_not_modified_by_eval_infrastructure():
    historical = ROOT / "reports/live_flow/patch_backend_comparison/docguard_patch_backend_comparison_2026_08.md"
    if historical.exists():
        before = historical.read_bytes()
        after = historical.read_bytes()
        assert before == after
