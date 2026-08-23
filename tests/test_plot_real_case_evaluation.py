from __future__ import annotations

import json
from pathlib import Path

from scripts.plot_real_case_evaluation import run


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_plot_real_case_evaluation_outputs_summary_and_figures(tmp_path: Path) -> None:
    predictions = tmp_path / "predictions.jsonl"
    output_dir = tmp_path / "figures"

    rows = [
        {
            "case_id": "train-1",
            "dataset_split": "train",
            "gold_docs_update_required": True,
            "swept_pred_docs_update_required": True,
            "pred_probability": 0.9,
            "language": "python",
            "candidate_type": "code_only",
        },
        {
            "case_id": "validation-1",
            "dataset_split": "validation",
            "gold_docs_update_required": True,
            "swept_pred_docs_update_required": True,
            "pred_probability": 0.8,
            "language": "python",
            "candidate_type": "code_only",
        },
        {
            "case_id": "validation-2",
            "dataset_split": "validation",
            "gold_docs_update_required": False,
            "swept_pred_docs_update_required": False,
            "pred_probability": 0.2,
            "language": "python",
            "candidate_type": "code_only",
        },
        {
            "case_id": "test-1",
            "dataset_split": "locked_test",
            "gold_docs_update_required": True,
            "swept_pred_docs_update_required": True,
            "pred_probability": 0.85,
            "language": "typescript",
            "candidate_type": "code_and_docs",
        },
        {
            "case_id": "test-2",
            "dataset_split": "locked_test",
            "gold_docs_update_required": False,
            "swept_pred_docs_update_required": False,
            "pred_probability": 0.15,
            "language": "typescript",
            "candidate_type": "code_and_docs",
        },
    ]

    write_jsonl(predictions, rows)

    summary = run(
        predictions_path=predictions,
        output_dir=output_dir,
        primary_split="locked_test",
    )

    assert summary["status"] == "ok"
    assert summary["primary_metrics"]["total_cases"] == 2
    assert (output_dir / "real_case_visual_summary.json").exists()
    assert (output_dir / "real_case_visual_report.md").exists()
    assert (output_dir / "confusion_matrix_locked_test.png").exists()
    assert (output_dir / "roc_curve_locked_test.png").exists()