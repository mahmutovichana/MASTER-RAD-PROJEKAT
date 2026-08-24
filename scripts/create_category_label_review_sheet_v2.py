from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


THESIS4_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

TARGET_CATEGORY_ALIASES = {
    "api": "api_reference",
    "api_endpoint": "api_reference",
    "api_endpoint_change": "api_reference",
    "api_reference": "api_reference",
    "endpoint": "api_reference",
    "request_response": "api_reference",
    "request_response_change": "api_reference",

    "configuration": "configuration",
    "configuration_change": "configuration",
    "config": "configuration",
    "settings": "configuration",
    "environment": "configuration",
    "env": "configuration",

    "developer_setup": "developer_setup",
    "setup": "developer_setup",
    "installation": "developer_setup",
    "install": "developer_setup",
    "cli": "developer_setup",
    "command": "developer_setup",
    "commands": "developer_setup",
    "testing": "developer_setup",
    "testing_instructions": "developer_setup",
    "testing_command_change": "developer_setup",
    "workflow": "developer_setup",
    "workflow_change": "developer_setup",
    "workflow_documentation": "developer_setup",
    "project_documentation": "developer_setup",

    "model_contract": "model_contract",
    "model": "model_contract",
    "data_model": "model_contract",
    "request_response_schema_change": "model_contract",
    "schema": "model_contract",
    "schemas": "model_contract",
    "type": "model_contract",
    "types": "model_contract",
    "interface": "model_contract",
    "interfaces": "model_contract",
    "contract": "model_contract",
    "security": "model_contract",
}


FIELDNAMES = [
    "case_id",
    "dataset_split",
    "review_priority",
    "review_reason",
    "repository",
    "source_url",
    "language",
    "current_gold_doc_category",
    "v4_pred_doc_category",
    "v4_pred_confidence",
    "v4_top1",
    "v4_top2",
    "v4_top3",
    "review_decision",
    "review_doc_category",
    "review_notes",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc

            if not isinstance(value, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")

            rows.append(value)

    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]

    if value is None:
        return []

    return [str(value)]


def normalize_category(value: Any) -> str | None:
    raw = str(value or "").strip().lower()

    if not raw or raw in {"no_update", "not_available", "none", "null"}:
        return None

    normalized = TARGET_CATEGORY_ALIASES.get(raw, raw)

    if normalized in THESIS4_CATEGORIES:
        return normalized

    return None


def ranked_categories(prediction: dict[str, Any] | None) -> list[str]:
    if not prediction:
        return []

    ranked = prediction.get("pred_ranked_categories")
    if isinstance(ranked, list):
        output: list[str] = []
        for item in ranked:
            if isinstance(item, dict) and item.get("category"):
                output.append(str(item["category"]))
        return output

    probabilities = prediction.get("pred_probabilities")
    if isinstance(probabilities, dict):
        return [
            str(category)
            for category, _ in sorted(
                probabilities.items(),
                key=lambda item: float(item[1]),
                reverse=True,
            )
        ]

    pred = prediction.get("pred_doc_category")
    return [str(pred)] if pred else []


def compact_text(value: Any, limit: int) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def load_predictions(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}

    predictions: dict[str, dict[str, Any]] = {}

    for row in load_jsonl(path):
        case_id = str(row.get("case_id") or "").strip()
        split = str(row.get("dataset_split") or "").strip()

        if not case_id:
            continue

        if split not in {"train", "validation"}:
            continue

        predictions[case_id] = row

    return predictions


def review_priority(row: dict[str, Any], prediction: dict[str, Any] | None) -> tuple[int, str]:
    gold = normalize_category(row.get("gold_doc_category"))

    if prediction is None:
        return 50, "no_prediction_available"

    pred = normalize_category(prediction.get("pred_doc_category"))
    ranked = ranked_categories(prediction)
    confidence = float(prediction.get("pred_confidence") or 0.0)

    if gold is None:
        return 90, "gold_category_not_supported"

    if pred != gold and gold not in ranked[:2]:
        return 0, "wrong_and_gold_not_in_top2"

    if pred != gold and confidence >= 0.75:
        return 1, "high_confidence_error"

    if pred != gold:
        return 2, "prediction_error"

    if confidence < 0.40:
        return 3, "low_confidence_correct"

    return 10, "correct_quality_control"


def make_review_row(
    *,
    row: dict[str, Any],
    split_name: str,
    prediction: dict[str, Any] | None,
) -> dict[str, Any]:
    gold = normalize_category(row.get("gold_doc_category"))
    ranked = ranked_categories(prediction)
    priority, reason = review_priority(row, prediction)

    pred_category = ""
    pred_confidence = ""

    if prediction is not None:
        pred_category = str(prediction.get("pred_doc_category") or "")
        pred_confidence = str(prediction.get("pred_confidence") or "")

    return {
        "case_id": row.get("case_id"),
        "dataset_split": split_name,
        "review_priority": priority,
        "review_reason": reason,
        "repository": row.get("repository"),
        "source_url": row.get("source_url"),
        "language": row.get("language"),
        "current_gold_doc_category": gold or "",
        "v4_pred_doc_category": pred_category,
        "v4_pred_confidence": pred_confidence,
        "v4_top1": ranked[0] if len(ranked) > 0 else "",
        "v4_top2": ranked[1] if len(ranked) > 1 else "",
        "v4_top3": ranked[2] if len(ranked) > 2 else "",
        "review_decision": "",
        "review_doc_category": gold or "",
        "review_notes": "",
        "code_changed_files": "\n".join(safe_list(row.get("code_changed_files"))),
        "code_diff_excerpt": compact_text(row.get("code_diff_excerpt"), 6000),
        "docs_before_excerpt": compact_text(row.get("docs_before_excerpt"), 3000),
    }


def eligible_category_rows(rows: list[dict[str, Any]], split_name: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for row in rows:
        if not bool_value(row.get("gold_docs_update_required")):
            continue

        if normalize_category(row.get("gold_doc_category")) is None:
            continue

        copied = dict(row)
        copied["dataset_split"] = split_name
        output.append(copied)

    return output


def run(
    *,
    train_path: Path,
    validation_path: Path,
    predictions_path: Path | None,
    output_csv: Path,
    max_rows: int,
    correct_sample_per_class: int,
) -> dict[str, Any]:
    train_rows = eligible_category_rows(load_jsonl(train_path), "train")
    validation_rows = eligible_category_rows(load_jsonl(validation_path), "validation")
    predictions = load_predictions(predictions_path)

    review_rows: list[dict[str, Any]] = []

    for split_name, rows in [("train", train_rows), ("validation", validation_rows)]:
        for row in rows:
            case_id = str(row.get("case_id") or "")
            prediction = predictions.get(case_id)
            review_rows.append(
                make_review_row(
                    row=row,
                    split_name=split_name,
                    prediction=prediction,
                )
            )

    high_priority = [
        row
        for row in review_rows
        if int(row["review_priority"]) < 10
    ]

    correct_rows = [
        row
        for row in review_rows
        if int(row["review_priority"]) == 10
    ]

    correct_selected: list[dict[str, Any]] = []
    by_class_counter: Counter[str] = Counter()

    for row in sorted(correct_rows, key=lambda item: (item["current_gold_doc_category"], item["case_id"])):
        category = str(row["current_gold_doc_category"])
        if by_class_counter[category] >= correct_sample_per_class:
            continue
        correct_selected.append(row)
        by_class_counter[category] += 1

    selected = high_priority + correct_selected
    selected = sorted(
        selected,
        key=lambda item: (
            int(item["review_priority"]),
            str(item["dataset_split"]),
            str(item["current_gold_doc_category"]),
            str(item["case_id"]),
        ),
    )[:max_rows]

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in selected:
            writer.writerow(row)

    summary = {
        "status": "ok",
        "output_csv": str(output_csv),
        "train_rows_positive_supported": len(train_rows),
        "validation_rows_positive_supported": len(validation_rows),
        "predictions_loaded": len(predictions),
        "review_rows_written": len(selected),
        "review_reason_counts": dict(Counter(str(row["review_reason"]) for row in selected)),
        "review_split_counts": dict(Counter(str(row["dataset_split"]) for row in selected)),
        "review_gold_category_counts": dict(Counter(str(row["current_gold_doc_category"]) for row in selected)),
        "methodology": {
            "locked_test_included": False,
            "purpose": "Create a train/validation-only category label review sheet.",
            "review_columns_to_edit": [
                "review_decision",
                "review_doc_category",
                "review_notes",
            ],
            "allowed_review_decisions": [
                "",
                "keep",
                "update",
                "exclude",
                "no_update",
            ],
            "allowed_review_doc_categories": sorted(THESIS4_CATEGORIES),
        },
    }

    write_json(output_csv.with_suffix(".summary.json"), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a train/validation-only category label review sheet."
    )
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--predictions", default=None)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--max-rows", type=int, default=700)
    parser.add_argument("--correct-sample-per-class", type=int, default=35)

    args = parser.parse_args()

    run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        predictions_path=Path(args.predictions) if args.predictions else None,
        output_csv=Path(args.output_csv),
        max_rows=args.max_rows,
        correct_sample_per_class=args.correct_sample_per_class,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())