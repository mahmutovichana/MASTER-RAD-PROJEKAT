from __future__ import annotations

import json
from pathlib import Path

from scripts.apply_locked_test_review import apply_review


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_apply_locked_test_review_changes_and_excludes(tmp_path: Path) -> None:
    locked = tmp_path / "locked.jsonl"
    preds = tmp_path / "preds.jsonl"
    review = tmp_path / "review.csv"
    output = tmp_path / "reviewed.jsonl"
    excluded = tmp_path / "excluded.jsonl"
    summary = tmp_path / "summary.json"

    write_jsonl(
        locked,
        [
            {"case_id": "A", "gold_docs_update_required": True},
            {"case_id": "B", "gold_docs_update_required": True},
            {"case_id": "C", "gold_docs_update_required": False},
        ],
    )

    write_jsonl(
        preds,
        [
            {
                "case_id": "A",
                "dataset_split": "locked_test",
                "swept_pred_docs_update_required": False,
                "pred_probability": 0.4,
                "swept_threshold": 0.55,
            },
            {
                "case_id": "B",
                "dataset_split": "locked_test",
                "swept_pred_docs_update_required": True,
                "pred_probability": 0.9,
                "swept_threshold": 0.55,
            },
            {
                "case_id": "C",
                "dataset_split": "locked_test",
                "swept_pred_docs_update_required": True,
                "pred_probability": 0.8,
                "swept_threshold": 0.55,
            },
        ],
    )

    review.write_text(
        "\n".join(
            [
                "case_id,review_gold_docs_update_required,review_label_confidence,review_notes",
                "A,false,reviewed_high,Changed after review",
                "B,,reviewed_ambiguous,Unclear case",
                "C,false,reviewed_high,Confirmed original",
            ]
        ),
        encoding="utf-8",
    )

    result = apply_review(
        locked_test_path=locked,
        classifier_predictions_path=preds,
        review_csv_path=review,
        output_jsonl=output,
        excluded_jsonl=excluded,
        summary_json=summary,
    )

    assert result["included_reviewed_records"] == 2
    assert result["excluded_records"] == 1
    assert result["review_action_counts"]["review_changed_label"] == 1
    assert result["review_action_counts"]["excluded_reviewed_ambiguous"] == 1

    reviewed_rows = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert reviewed_rows[0]["case_id"] == "A"
    assert reviewed_rows[0]["gold_docs_update_required"] is False