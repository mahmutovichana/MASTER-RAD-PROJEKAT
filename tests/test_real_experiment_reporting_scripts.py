from __future__ import annotations

import json
from pathlib import Path

from scripts.build_llm_judge_retry_set import build_retry_set
from scripts.merge_llm_judge_predictions import merge_predictions
from scripts.summarize_llm_judge_coverage import summarize
from scripts.sweep_real_gold_classifier_thresholds import compute_metrics, select_threshold


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_llm_coverage_summary_completed_only() -> None:
    rows = [
        {
            "case_id": "A",
            "decision_status": "ok",
            "gold_docs_update_required": True,
            "pred_docs_update_required": True,
            "documentation_area": "api",
        },
        {
            "case_id": "B",
            "decision_status": "error",
            "decision_error": "HTTP 402 depleted credits",
            "gold_docs_update_required": True,
            "pred_docs_update_required": False,
            "documentation_area": "error",
        },
    ]

    result = summarize(rows, input_path=Path("predictions.jsonl"))

    assert result["coverage"] == 0.5
    assert result["failure_reason_counts"] == {"quota_or_credits_depleted": 1}
    assert result["completed_only_metrics"]["true_positives"] == 1


def test_build_retry_set(tmp_path: Path) -> None:
    original = tmp_path / "original.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    retry = tmp_path / "retry.jsonl"

    write_jsonl(
        original,
        [
            {"case_id": "A", "payload": 1},
            {"case_id": "B", "payload": 2},
        ],
    )
    write_jsonl(
        predictions,
        [
            {"case_id": "A", "decision_status": "ok"},
            {"case_id": "B", "decision_status": "error"},
        ],
    )

    result = build_retry_set(
        original_input=original,
        predictions=predictions,
        output=retry,
        retry_statuses={"error"},
    )

    assert result["retry_rows"] == 1
    assert json.loads(retry.read_text(encoding="utf-8").strip())["case_id"] == "B"


def test_merge_predictions_replaces_successful_retry(tmp_path: Path) -> None:
    base = tmp_path / "base.jsonl"
    retry = tmp_path / "retry.jsonl"
    output = tmp_path / "merged.jsonl"
    summary = tmp_path / "summary.json"

    write_jsonl(
        base,
        [
            {
                "case_id": "A",
                "decision_status": "ok",
                "gold_docs_update_required": True,
                "pred_docs_update_required": True,
            },
            {
                "case_id": "B",
                "decision_status": "error",
                "gold_docs_update_required": True,
                "pred_docs_update_required": False,
            },
        ],
    )
    write_jsonl(
        retry,
        [
            {
                "case_id": "B",
                "decision_status": "ok",
                "gold_docs_update_required": True,
                "pred_docs_update_required": True,
            }
        ],
    )

    result = merge_predictions(
        base_predictions=base,
        retry_predictions=retry,
        output_predictions=output,
        output_summary=summary,
    )

    assert result["replaced_with_successful_retry"] == 1
    assert result["completed_cases"] == 2
    assert result["all_cases_conservative_metrics"]["true_positives"] == 2


def test_threshold_metrics_and_selection() -> None:
    rows = [
        {"gold_docs_update_required": True, "pred_probability": 0.90},
        {"gold_docs_update_required": True, "pred_probability": 0.60},
        {"gold_docs_update_required": False, "pred_probability": 0.55},
        {"gold_docs_update_required": False, "pred_probability": 0.10},
    ]

    metrics = compute_metrics(rows, 0.5)
    assert metrics["true_positives"] == 2
    assert metrics["false_positives"] == 1

    selected = select_threshold(rows, "balanced_accuracy")
    assert "selected_threshold" in selected