from __future__ import annotations

import argparse
import csv
import json
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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load_review_csv(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            case_id = str(row.get("case_id") or "").strip()
            if not case_id:
                continue
            if case_id in rows:
                raise ValueError(f"Duplicate case_id in review CSV at line {line_number}: {case_id}")
            rows[case_id] = {key: str(value or "").strip() for key, value in row.items()}

    return rows


def parse_review_bool(value: str) -> bool | None:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    if lowered in {"", "none", "null"}:
        return None
    raise ValueError(f"Invalid review boolean: {value}")


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]], *, pred_key: str, gold_key: str) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool(row[gold_key])
        pred = bool(row[pred_key])

        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)

    return {
        "total_cases": len(rows),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "gold_distribution": dict(Counter(str(bool(row[gold_key])) for row in rows)),
        "pred_distribution": dict(Counter(str(bool(row[pred_key])) for row in rows)),
    }


def apply_review(
    *,
    locked_test_path: Path,
    classifier_predictions_path: Path,
    review_csv_path: Path,
    output_jsonl: Path,
    excluded_jsonl: Path,
    summary_json: Path,
) -> dict[str, Any]:
    locked_rows = load_jsonl(locked_test_path)
    classifier_rows = [
        row
        for row in load_jsonl(classifier_predictions_path)
        if str(row.get("dataset_split")) == "locked_test"
    ]

    classifier_by_case = {str(row.get("case_id")): row for row in classifier_rows}
    review_by_case = load_review_csv(review_csv_path)

    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    review_action_counts: Counter[str] = Counter()

    for locked in locked_rows:
        case_id = str(locked.get("case_id"))
        classifier = classifier_by_case.get(case_id)
        review = review_by_case.get(case_id, {})

        if classifier is None:
            raise ValueError(f"Missing classifier prediction for locked-test case: {case_id}")

        original_gold = bool(locked.get("gold_docs_update_required"))
        review_value = parse_review_bool(review.get("review_gold_docs_update_required", ""))
        review_confidence = review.get("review_label_confidence", "")
        review_notes = review.get("review_notes", "")

        if review_confidence == "reviewed_ambiguous":
            copied = dict(locked)
            copied["review_status"] = "excluded_reviewed_ambiguous"
            copied["review_notes"] = review_notes
            excluded.append(copied)
            review_action_counts["excluded_reviewed_ambiguous"] += 1
            continue

        final_gold = original_gold if review_value is None else review_value

        if review_value is None:
            review_status = "unchanged_no_review_override"
        elif review_value == original_gold:
            review_status = "review_confirmed_original"
        else:
            review_status = "review_changed_label"

        review_action_counts[review_status] += 1

        copied = dict(locked)
        copied["original_gold_docs_update_required"] = original_gold
        copied["reviewed_gold_docs_update_required"] = final_gold
        copied["gold_docs_update_required"] = final_gold
        copied["review_label_confidence"] = review_confidence
        copied["review_notes"] = review_notes
        copied["review_status"] = review_status
        copied["classifier_pred_docs_update_required"] = bool(
            classifier.get("swept_pred_docs_update_required", classifier.get("pred_docs_update_required"))
        )
        copied["classifier_probability"] = classifier.get("pred_probability")
        copied["classifier_threshold"] = classifier.get("swept_threshold")

        included.append(copied)

    metrics = compute_metrics(
        included,
        pred_key="classifier_pred_docs_update_required",
        gold_key="reviewed_gold_docs_update_required",
    )

    summary = {
        "status": "ok",
        "locked_test_input": str(locked_test_path),
        "classifier_predictions": str(classifier_predictions_path),
        "review_csv": str(review_csv_path),
        "output_jsonl": str(output_jsonl),
        "excluded_jsonl": str(excluded_jsonl),
        "input_locked_test_records": len(locked_rows),
        "included_reviewed_records": len(included),
        "excluded_records": len(excluded),
        "review_action_counts": dict(review_action_counts),
        "metrics": metrics,
        "interpretation": {
            "label_source": "second-pass AI-assisted locked-test review",
            "warning": "This is stronger than first-pass silver labels, but should still be described as AI-assisted unless independently human-reviewed.",
            "rule": "Reviewed ambiguous records are excluded from final reviewed locked-test metrics.",
        },
    }

    write_jsonl(output_jsonl, included)
    write_jsonl(excluded_jsonl, excluded)
    write_json(summary_json, summary)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply second-pass locked-test review decisions and compute reviewed metrics.")
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--classifier-predictions", required=True)
    parser.add_argument("--review-csv", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--excluded-jsonl", required=True)
    parser.add_argument("--summary-json", required=True)
    args = parser.parse_args()

    result = apply_review(
        locked_test_path=Path(args.locked_test),
        classifier_predictions_path=Path(args.classifier_predictions),
        review_csv_path=Path(args.review_csv),
        output_jsonl=Path(args.output_jsonl),
        excluded_jsonl=Path(args.excluded_jsonl),
        summary_json=Path(args.summary_json),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())