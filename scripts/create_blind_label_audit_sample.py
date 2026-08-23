from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc

            if not isinstance(row, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")

            rows.append(row)

    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def pred_value(row: dict[str, Any]) -> bool:
    if "swept_pred_docs_update_required" in row:
        return bool_value(row.get("swept_pred_docs_update_required"))

    return bool_value(row.get("pred_docs_update_required"))


def error_type(row: dict[str, Any]) -> str:
    gold = bool_value(row.get("gold_docs_update_required"))
    pred = pred_value(row)

    if gold and pred:
        return "TP"

    if not gold and pred:
        return "FP"

    if not gold and not pred:
        return "TN"

    return "FN"


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]

    if value is None:
        return []

    return [str(value)]


def compact(value: Any, limit: int) -> str:
    text = " ".join(str(value or "").split())

    if len(text) <= limit:
        return text

    return text[: limit - 3] + "..."


def load_cases(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("case_id")): row
        for row in load_jsonl(path)
        if row.get("case_id")
    }


def merge_prediction_with_case(
    prediction: dict[str, Any],
    cases_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    case_id = str(prediction.get("case_id"))
    merged = dict(cases_by_id.get(case_id, {}))
    merged.update(prediction)
    merged["error_type"] = error_type(merged)
    return merged


def stratified_sample(
    rows: list[dict[str, Any]],
    *,
    per_error_type: int,
    seed: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []

    for group in ["TP", "TN", "FP", "FN"]:
        group_rows = [row for row in rows if row.get("error_type") == group]
        rng.shuffle(group_rows)
        selected.extend(group_rows[:per_error_type])

    rng.shuffle(selected)

    return selected


def write_review_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "audit_id",
        "case_id",
        "repository",
        "language",
        "source_url",
        "code_changed_files",
        "code_diff_excerpt",
        "docs_before_excerpt",
        "review_docs_update_required",
        "review_doc_category",
        "review_confidence",
        "review_notes",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for index, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "audit_id": f"AUDIT-{index:04d}",
                    "case_id": row.get("case_id"),
                    "repository": row.get("repository"),
                    "language": row.get("language"),
                    "source_url": row.get("source_url"),
                    "code_changed_files": "\n".join(safe_list(row.get("code_changed_files"))),
                    "code_diff_excerpt": compact(row.get("code_diff_excerpt"), 5000),
                    "docs_before_excerpt": compact(row.get("docs_before_excerpt"), 5000),
                    "review_docs_update_required": "",
                    "review_doc_category": "",
                    "review_confidence": "",
                    "review_notes": "",
                }
            )


def build_key_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    key_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        key_rows.append(
            {
                "audit_id": f"AUDIT-{index:04d}",
                "case_id": row.get("case_id"),
                "dataset_split": row.get("dataset_split"),
                "repository": row.get("repository"),
                "language": row.get("language"),
                "candidate_type": row.get("candidate_type"),
                "gold_docs_update_required": bool_value(row.get("gold_docs_update_required")),
                "gold_doc_category": row.get("gold_doc_category"),
                "label_confidence": row.get("label_confidence"),
                "label_source": row.get("label_source"),
                "pred_docs_update_required": pred_value(row),
                "pred_probability": row.get("pred_probability"),
                "swept_threshold": row.get("swept_threshold"),
                "error_type": row.get("error_type"),
            }
        )

    return key_rows


def run(
    *,
    predictions_path: Path,
    cases_path: Path,
    output_review_csv: Path,
    output_key_jsonl: Path,
    output_summary_json: Path,
    per_error_type: int,
    seed: int,
    split: str,
) -> dict[str, Any]:
    predictions = load_jsonl(predictions_path)
    cases_by_id = load_cases(cases_path)

    merged_rows = [
        merge_prediction_with_case(prediction, cases_by_id)
        for prediction in predictions
    ]

    if split != "all":
        merged_rows = [
            row
            for row in merged_rows
            if str(row.get("dataset_split")) == split
        ]

    selected = stratified_sample(
        merged_rows,
        per_error_type=per_error_type,
        seed=seed,
    )

    key_rows = build_key_rows(selected)

    write_review_csv(output_review_csv, selected)
    write_jsonl(output_key_jsonl, key_rows)

    summary = {
        "status": "ok",
        "predictions": str(predictions_path),
        "cases": str(cases_path),
        "split": split,
        "seed": seed,
        "per_error_type": per_error_type,
        "total_available_rows": len(merged_rows),
        "selected_rows": len(selected),
        "selected_error_type_counts": dict(Counter(row["error_type"] for row in selected)),
        "selected_language_counts": dict(Counter(str(row.get("language") or "unknown") for row in selected)),
        "selected_candidate_type_counts": dict(Counter(str(row.get("candidate_type") or "unknown") for row in selected)),
        "outputs": {
            "review_csv": str(output_review_csv),
            "key_jsonl": str(output_key_jsonl),
            "summary_json": str(output_summary_json),
        },
        "blind_review_policy": {
            "review_csv_excludes": [
                "gold_docs_update_required",
                "pred_docs_update_required",
                "pred_probability",
                "error_type",
                "candidate_type",
                "label_confidence",
                "label_source",
                "manual_label_notes",
            ],
            "key_file_must_not_be_used_during_review": True,
        },
    }

    write_json(output_summary_json, summary)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a blind manual label audit sample.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output-review-csv", required=True)
    parser.add_argument("--output-key-jsonl", required=True)
    parser.add_argument("--output-summary-json", required=True)
    parser.add_argument("--per-error-type", type=int, default=60)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--split", default="all", choices=["all", "train", "validation", "locked_test"])

    args = parser.parse_args()

    summary = run(
        predictions_path=Path(args.predictions),
        cases_path=Path(args.cases),
        output_review_csv=Path(args.output_review_csv),
        output_key_jsonl=Path(args.output_key_jsonl),
        output_summary_json=Path(args.output_summary_json),
        per_error_type=args.per_error_type,
        seed=args.seed,
        split=args.split,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())