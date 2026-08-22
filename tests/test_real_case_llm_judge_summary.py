from __future__ import annotations

from scripts.summarize_real_case_llm_judge_results import (
    build_summary,
    classify_failure_reason,
    compute_binary_metrics,
)


def test_summary_separates_completed_and_quota_failures() -> None:
    rows = [
        {
            "case_id": "A",
            "decision_status": "ok",
            "abstained": False,
            "gold_docs_update_required": True,
            "pred_docs_update_required": True,
            "documentation_area": "api",
        },
        {
            "case_id": "B",
            "decision_status": "ok",
            "abstained": False,
            "gold_docs_update_required": True,
            "pred_docs_update_required": False,
            "documentation_area": "no_update",
        },
        {
            "case_id": "C",
            "decision_status": "error",
            "abstained": True,
            "gold_docs_update_required": True,
            "pred_docs_update_required": False,
            "documentation_area": "error",
            "decision_error": "HTTP 402 from provider: depleted your monthly included credits",
        },
    ]

    summary = build_summary(rows)

    assert summary["total_cases"] == 3
    assert summary["completed_cases"] == 2
    assert summary["failed_or_abstained_cases"] == 1
    assert summary["failure_reason_counts"] == {"quota_or_credits_depleted": 1}
    assert summary["completed_cases_metrics"]["true_positives"] == 1
    assert summary["completed_cases_metrics"]["false_negatives"] == 1


def test_quota_failure_reason_is_detected() -> None:
    row = {
        "decision_status": "error",
        "decision_error": "HTTP 402 from https://router.huggingface.co/v1/chat/completions: depleted your monthly included credits",
    }

    assert classify_failure_reason(row) == "quota_or_credits_depleted"


def test_binary_metrics_are_computed_correctly() -> None:
    rows = [
        {"gold_docs_update_required": True, "pred_docs_update_required": True},
        {"gold_docs_update_required": False, "pred_docs_update_required": False},
        {"gold_docs_update_required": False, "pred_docs_update_required": True},
        {"gold_docs_update_required": True, "pred_docs_update_required": False},
    ]

    metrics = compute_binary_metrics(rows)

    assert metrics["true_positives"] == 1
    assert metrics["true_negatives"] == 1
    assert metrics["false_positives"] == 1
    assert metrics["false_negatives"] == 1
    assert metrics["accuracy"] == 0.5