from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def ranked_labels(row: dict[str, Any]) -> list[str]:
    ranked = row.get("pred_ranked_categories")
    if isinstance(ranked, list):
        labels: list[str] = []
        for item in ranked:
            if isinstance(item, dict) and item.get("category"):
                labels.append(str(item["category"]))
        return labels

    probabilities = row.get("pred_probabilities")
    if isinstance(probabilities, dict):
        return [
            category
            for category, _ in sorted(
                probabilities.items(),
                key=lambda item: float(item[1]),
                reverse=True,
            )
        ]

    pred = row.get("pred_doc_category")
    return [str(pred)] if pred else []


def summarize_split(rows: list[dict[str, Any]], split_name: str) -> dict[str, Any]:
    split_rows = [
        row
        for row in rows
        if str(row.get("dataset_split") or "") == split_name
    ]

    total = len(split_rows)
    correct = [
        row
        for row in split_rows
        if str(row.get("gold_doc_category")) == str(row.get("pred_doc_category"))
    ]
    errors = [
        row
        for row in split_rows
        if str(row.get("gold_doc_category")) != str(row.get("pred_doc_category"))
    ]

    gold_counts = Counter(str(row.get("gold_doc_category")) for row in split_rows)
    pred_counts = Counter(str(row.get("pred_doc_category")) for row in split_rows)

    pair_counts = Counter(
        f"{row.get('gold_doc_category')} -> {row.get('pred_doc_category')}"
        for row in errors
    )

    top2_correct = 0
    for row in split_rows:
        gold = str(row.get("gold_doc_category"))
        if gold in ranked_labels(row)[:2]:
            top2_correct += 1

    by_gold: dict[str, dict[str, Any]] = {}
    all_labels = sorted(set(gold_counts) | set(pred_counts))

    for label in all_labels:
        tp = sum(
            1
            for row in split_rows
            if str(row.get("gold_doc_category")) == label
            and str(row.get("pred_doc_category")) == label
        )
        fp = sum(
            1
            for row in split_rows
            if str(row.get("gold_doc_category")) != label
            and str(row.get("pred_doc_category")) == label
        )
        fn = sum(
            1
            for row in split_rows
            if str(row.get("gold_doc_category")) == label
            and str(row.get("pred_doc_category")) != label
        )

        precision = safe_div(tp, tp + fp)
        recall = safe_div(tp, tp + fn)
        f1 = safe_div(2 * precision * recall, precision + recall)

        by_gold[label] = {
            "support": gold_counts.get(label, 0),
            "predicted": pred_counts.get(label, 0),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    confidence_buckets = {
        "0.00-0.40": 0,
        "0.40-0.50": 0,
        "0.50-0.60": 0,
        "0.60-0.70": 0,
        "0.70-0.80": 0,
        "0.80-1.00": 0,
        "missing": 0,
    }

    error_confidence_buckets = dict(confidence_buckets)

    for row in split_rows:
        confidence = row.get("pred_confidence")
        bucket = confidence_bucket(confidence)
        confidence_buckets[bucket] += 1

    for row in errors:
        confidence = row.get("pred_confidence")
        bucket = confidence_bucket(confidence)
        error_confidence_buckets[bucket] += 1

    top_errors = sorted(
        errors,
        key=lambda row: float(row.get("pred_confidence") or 0.0),
        reverse=True,
    )[:25]

    low_confidence_correct = sorted(
        correct,
        key=lambda row: float(row.get("pred_confidence") or 0.0),
    )[:25]

    return {
        "split": split_name,
        "total": total,
        "correct": len(correct),
        "errors": len(errors),
        "accuracy": safe_div(len(correct), total),
        "top2_accuracy": safe_div(top2_correct, total),
        "gold_distribution": dict(gold_counts),
        "pred_distribution": dict(pred_counts),
        "per_class": by_gold,
        "confusion_pairs": dict(pair_counts.most_common()),
        "confidence_buckets": confidence_buckets,
        "error_confidence_buckets": error_confidence_buckets,
        "high_confidence_errors": [
            compact_case(row)
            for row in top_errors
        ],
        "low_confidence_correct": [
            compact_case(row)
            for row in low_confidence_correct
        ],
    }


def confidence_bucket(value: Any) -> str:
    if value is None:
        return "missing"

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return "missing"

    if confidence < 0.40:
        return "0.00-0.40"
    if confidence < 0.50:
        return "0.40-0.50"
    if confidence < 0.60:
        return "0.50-0.60"
    if confidence < 0.70:
        return "0.60-0.70"
    if confidence < 0.80:
        return "0.70-0.80"

    return "0.80-1.00"


def compact_case(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": row.get("case_id"),
        "repository": row.get("repository"),
        "language": row.get("language"),
        "source_url": row.get("source_url"),
        "gold_doc_category": row.get("gold_doc_category"),
        "pred_doc_category": row.get("pred_doc_category"),
        "pred_confidence": row.get("pred_confidence"),
        "top2": ranked_labels(row)[:2],
        "code_changed_files": row.get("code_changed_files"),
    }


def write_markdown(path: Path, summary: dict[str, Any]) -> None:
    lines: list[str] = [
        "# Category Classifier Error Analysis",
        "",
        "This report analyzes classifier errors only. It does not change predictions, labels, or model selection.",
        "",
    ]

    for split_name, split in summary["splits"].items():
        lines.extend(
            [
                f"## {split_name}",
                "",
                f"- total: `{split['total']}`",
                f"- accuracy: `{split['accuracy']:.4f}`",
                f"- top-2 accuracy: `{split['top2_accuracy']:.4f}`",
                f"- errors: `{split['errors']}`",
                "",
                "### Gold distribution",
                "",
                "```json",
                json.dumps(split["gold_distribution"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
                "### Predicted distribution",
                "",
                "```json",
                json.dumps(split["pred_distribution"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
                "### Per-class metrics",
                "",
                "```json",
                json.dumps(split["per_class"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
                "### Most common confusion pairs",
                "",
                "```json",
                json.dumps(split["confusion_pairs"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
                "### Error confidence buckets",
                "",
                "```json",
                json.dumps(split["error_confidence_buckets"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
                "### High-confidence errors",
                "",
                "```json",
                json.dumps(split["high_confidence_errors"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(*, predictions: Path, output_dir: Path) -> dict[str, Any]:
    rows = load_jsonl(predictions)
    split_names = sorted(set(str(row.get("dataset_split") or "unknown") for row in rows))

    summary = {
        "status": "ok",
        "input_predictions": str(predictions),
        "splits": {
            split_name: summarize_split(rows, split_name)
            for split_name in split_names
        },
        "note": "This is diagnostic analysis only. It does not alter labels, predictions, or model selection.",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "category_error_analysis.json", summary)
    write_markdown(output_dir / "category_error_analysis.md", summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze documentation category classifier errors.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output-dir", required=True)

    args = parser.parse_args()

    run(
        predictions=Path(args.predictions),
        output_dir=Path(args.output_dir),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())