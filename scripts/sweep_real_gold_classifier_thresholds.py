from __future__ import annotations

import argparse
import json
import math
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def matthews_corrcoef_binary(tp: int, fp: int, tn: int, fn: int) -> float:
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return 0.0
    return ((tp * tn) - (fp * fn)) / denom


def compute_metrics(rows: list[dict[str, Any]], threshold: float) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool(row.get("gold_docs_update_required"))
        probability = float(row.get("pred_probability"))
        pred = probability >= threshold

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
    balanced_accuracy = (recall + specificity) / 2

    return {
        "threshold": threshold,
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
        "balanced_accuracy": balanced_accuracy,
        "mcc": matthews_corrcoef_binary(tp=tp, fp=fp, tn=tn, fn=fn),
        "gold_distribution": dict(Counter(str(bool(row.get("gold_docs_update_required"))) for row in rows)),
        "pred_distribution": dict(Counter(str(float(row.get("pred_probability")) >= threshold) for row in rows)),
    }


def objective_key(metrics: dict[str, Any], objective: str) -> tuple[float, ...]:
    if objective == "f1":
        return (
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["balanced_accuracy"],
        )

    if objective == "balanced_accuracy":
        return (
            metrics["balanced_accuracy"],
            metrics["mcc"],
            metrics["f1"],
            metrics["precision"],
        )

    if objective == "mcc":
        return (
            metrics["mcc"],
            metrics["balanced_accuracy"],
            metrics["f1"],
            metrics["precision"],
        )

    if objective == "precision":
        return (
            metrics["precision"],
            metrics["f1"],
            metrics["balanced_accuracy"],
            metrics["recall"],
        )

    raise ValueError(f"Unsupported objective: {objective}")


def select_threshold(validation_rows: list[dict[str, Any]], objective: str) -> dict[str, Any]:
    candidates = [round(value / 100, 2) for value in range(5, 96, 5)]
    scored = [
        compute_metrics(validation_rows, threshold)
        for threshold in candidates
    ]

    best = max(scored, key=lambda item: objective_key(item, objective))
    return {
        "objective": objective,
        "selected_threshold": best["threshold"],
        "selected_validation_metrics": best,
        "validation_sweep": scored,
    }


def apply_threshold(rows: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for row in rows:
        probability = float(row.get("pred_probability"))
        pred = probability >= threshold
        gold = bool(row.get("gold_docs_update_required"))

        copied = dict(row)
        copied["swept_threshold"] = threshold
        copied["swept_pred_docs_update_required"] = pred
        copied["swept_binary_correct"] = pred == gold
        output.append(copied)

    return output


def run(
    *,
    predictions_path: Path,
    objective: str,
    output_json: Path,
    output_predictions: Path,
) -> dict[str, Any]:
    rows = load_jsonl(predictions_path)

    by_split: dict[str, list[dict[str, Any]]] = {
        "train": [],
        "validation": [],
        "locked_test": [],
    }

    for row in rows:
        split = str(row.get("dataset_split"))
        if split in by_split:
            by_split[split].append(row)

    selection = select_threshold(by_split["validation"], objective)
    threshold = float(selection["selected_threshold"])

    metrics_by_split = {
        split: compute_metrics(split_rows, threshold)
        for split, split_rows in by_split.items()
    }

    swept_predictions = [
        item
        for split in ["train", "validation", "locked_test"]
        for item in apply_threshold(by_split[split], threshold)
    ]

    report = {
        "status": "ok",
        "predictions": str(predictions_path),
        "objective": objective,
        "selected_threshold": threshold,
        "selected_validation_metrics": selection["selected_validation_metrics"],
        "metrics_by_split": metrics_by_split,
        "split_sizes": {split: len(split_rows) for split, split_rows in by_split.items()},
        "validation_sweep": selection["validation_sweep"],
        "interpretation": {
            "rule": "Threshold is selected on validation only, then applied unchanged to locked_test.",
            "warning": "This does not change the trained classifier, only its validation-selected operating point.",
        },
    }

    write_json(output_json, report)
    write_jsonl(output_predictions, swept_predictions)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep classifier thresholds using validation only and report locked-test results.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--objective", choices=["f1", "balanced_accuracy", "mcc", "precision"], default="balanced_accuracy")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-predictions", required=True)
    args = parser.parse_args()

    result = run(
        predictions_path=Path(args.predictions),
        objective=args.objective,
        output_json=Path(args.output_json),
        output_predictions=Path(args.output_predictions),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())