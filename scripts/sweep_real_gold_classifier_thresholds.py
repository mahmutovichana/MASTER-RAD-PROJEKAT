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


def probability_value(row: dict[str, Any]) -> float:
    value = row.get("pred_probability")

    if value is None:
        raise ValueError(f"Prediction row is missing pred_probability for case_id={row.get('case_id')}")

    return float(value)


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
        gold = bool_value(row.get("gold_docs_update_required"))
        probability = probability_value(row)
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
        "gold_distribution": dict(
            Counter(str(bool_value(row.get("gold_docs_update_required"))) for row in rows)
        ),
        "pred_distribution": dict(
            Counter(str(probability_value(row) >= threshold) for row in rows)
        ),
    }


def compute_metrics_from_predictions(
    rows: list[dict[str, Any]],
    *,
    pred_key: str,
) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool_value(row.get("gold_docs_update_required"))
        pred = bool_value(row.get(pred_key))

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
        "threshold_mode": "grouped",
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
        "gold_distribution": dict(
            Counter(str(bool_value(row.get("gold_docs_update_required"))) for row in rows)
        ),
        "pred_distribution": dict(Counter(str(bool_value(row.get(pred_key))) for row in rows)),
    }


def objective_key(metrics: dict[str, Any], objective: str) -> tuple[float, ...]:
    if objective == "f1":
        return (
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["balanced_accuracy"],
            metrics["mcc"],
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
    if not validation_rows:
        raise ValueError("Cannot select threshold because validation split is empty.")

    candidates = [round(value / 100, 2) for value in range(5, 96, 5)]
    scored = [compute_metrics(validation_rows, threshold) for threshold in candidates]

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
        probability = probability_value(row)
        pred = probability >= threshold
        gold = bool_value(row.get("gold_docs_update_required"))

        copied = dict(row)
        copied["swept_threshold"] = threshold
        copied["swept_pred_docs_update_required"] = pred
        copied["swept_binary_correct"] = pred == gold
        output.append(copied)

    return output


def candidate_type_value(row: dict[str, Any]) -> str:
    if row.get("candidate_type"):
        return str(row["candidate_type"])

    evidence = row.get("candidate_evidence")
    if isinstance(evidence, dict) and evidence.get("candidate_type"):
        return str(evidence["candidate_type"])

    audit = row.get("audit_labeling_context")
    if isinstance(audit, dict):
        audit_evidence = audit.get("candidate_evidence")
        if isinstance(audit_evidence, dict) and audit_evidence.get("candidate_type"):
            return str(audit_evidence["candidate_type"])

    return "unknown"


def group_value(row: dict[str, Any], group_by: str) -> str:
    if group_by == "none":
        return "__global__"

    if group_by == "candidate_type":
        return candidate_type_value(row)

    value = row.get(group_by)

    if value is None or str(value).strip() == "":
        return "unknown"

    return str(value)


def has_both_classes(rows: list[dict[str, Any]]) -> bool:
    values = {bool_value(row.get("gold_docs_update_required")) for row in rows}
    return len(values) == 2


def select_group_thresholds(
    *,
    validation_rows: list[dict[str, Any]],
    objective: str,
    group_by: str,
    min_validation_cases: int,
) -> dict[str, Any]:
    global_selection = select_threshold(validation_rows, objective)
    global_threshold = float(global_selection["selected_threshold"])

    groups = sorted({group_value(row, group_by) for row in validation_rows})

    group_thresholds: dict[str, float] = {}
    group_reports: dict[str, Any] = {}

    for group in groups:
        group_rows = [
            row
            for row in validation_rows
            if group_value(row, group_by) == group
        ]

        if len(group_rows) < min_validation_cases:
            group_thresholds[group] = global_threshold
            group_reports[group] = {
                "status": "fallback_global",
                "reason": "too_few_validation_cases",
                "validation_cases": len(group_rows),
                "threshold": global_threshold,
            }
            continue

        if not has_both_classes(group_rows):
            group_thresholds[group] = global_threshold
            group_reports[group] = {
                "status": "fallback_global",
                "reason": "single_class_validation_group",
                "validation_cases": len(group_rows),
                "threshold": global_threshold,
            }
            continue

        selection = select_threshold(group_rows, objective)
        threshold = float(selection["selected_threshold"])

        group_thresholds[group] = threshold
        group_reports[group] = {
            "status": "selected_on_validation",
            "validation_cases": len(group_rows),
            "threshold": threshold,
            "selected_validation_metrics": selection["selected_validation_metrics"],
            "validation_sweep": selection["validation_sweep"],
        }

    return {
        "mode": "grouped",
        "group_by": group_by,
        "objective": objective,
        "min_validation_cases": min_validation_cases,
        "global_threshold": global_threshold,
        "global_selection": global_selection,
        "group_thresholds": group_thresholds,
        "group_reports": group_reports,
    }


def apply_group_thresholds(
    rows: list[dict[str, Any]],
    *,
    group_by: str,
    group_thresholds: dict[str, float],
    global_threshold: float,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for row in rows:
        group = group_value(row, group_by)
        threshold = float(group_thresholds.get(group, global_threshold))
        probability = probability_value(row)
        pred = probability >= threshold
        gold = bool_value(row.get("gold_docs_update_required"))

        copied = dict(row)
        copied["swept_group_by"] = group_by
        copied["swept_group_value"] = group
        copied["swept_threshold"] = threshold
        copied["swept_pred_docs_update_required"] = pred
        copied["swept_binary_correct"] = pred == gold
        output.append(copied)

    return output


def split_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_split: dict[str, list[dict[str, Any]]] = {
        "train": [],
        "validation": [],
        "locked_test": [],
    }

    for row in rows:
        split = str(row.get("dataset_split"))

        if split in by_split:
            by_split[split].append(row)

    return by_split


def run_global_threshold(
    *,
    by_split: dict[str, list[dict[str, Any]]],
    objective: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    selection = select_threshold(by_split["validation"], objective)
    threshold = float(selection["selected_threshold"])

    metrics_by_split = {
        split: compute_metrics(split_rows_value, threshold)
        for split, split_rows_value in by_split.items()
    }

    swept_predictions = [
        item
        for split in ["train", "validation", "locked_test"]
        for item in apply_threshold(by_split[split], threshold)
    ]

    thresholding = {
        "mode": "global",
        "objective": objective,
        "selected_threshold": threshold,
        "selected_validation_metrics": selection["selected_validation_metrics"],
        "validation_sweep": selection["validation_sweep"],
    }

    return thresholding, swept_predictions, metrics_by_split


def run_group_threshold(
    *,
    by_split: dict[str, list[dict[str, Any]]],
    objective: str,
    group_by: str,
    min_validation_cases: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    thresholding = select_group_thresholds(
        validation_rows=by_split["validation"],
        objective=objective,
        group_by=group_by,
        min_validation_cases=min_validation_cases,
    )

    swept_predictions = [
        item
        for split in ["train", "validation", "locked_test"]
        for item in apply_group_thresholds(
            by_split[split],
            group_by=group_by,
            group_thresholds=thresholding["group_thresholds"],
            global_threshold=float(thresholding["global_threshold"]),
        )
    ]

    swept_by_split = split_rows(swept_predictions)

    metrics_by_split = {
        split: compute_metrics_from_predictions(
            split_rows_value,
            pred_key="swept_pred_docs_update_required",
        )
        for split, split_rows_value in swept_by_split.items()
    }

    return thresholding, swept_predictions, metrics_by_split


def run(
    *,
    predictions_path: Path,
    objective: str,
    group_by: str,
    min_validation_cases: int,
    output_json: Path,
    output_predictions: Path,
) -> dict[str, Any]:
    rows = load_jsonl(predictions_path)
    by_split = split_rows(rows)

    if not by_split["validation"]:
        raise ValueError("Validation split is empty. Threshold selection requires validation rows.")

    if group_by == "none":
        thresholding, swept_predictions, metrics_by_split = run_global_threshold(
            by_split=by_split,
            objective=objective,
        )
    else:
        thresholding, swept_predictions, metrics_by_split = run_group_threshold(
            by_split=by_split,
            objective=objective,
            group_by=group_by,
            min_validation_cases=min_validation_cases,
        )

    selected_threshold = float(
        thresholding.get("selected_threshold", thresholding.get("global_threshold"))
    )

    selected_validation_metrics = thresholding.get(
        "selected_validation_metrics",
        thresholding.get("global_selection", {}).get("selected_validation_metrics"),
    )

    validation_sweep = thresholding.get(
        "validation_sweep",
        thresholding.get("global_selection", {}).get("validation_sweep"),
    )

    report = {
        "status": "ok",
        "predictions": str(predictions_path),
        "objective": objective,
        "group_by": group_by,
        "min_validation_cases": min_validation_cases,
        "selected_threshold": selected_threshold,
        "selected_validation_metrics": selected_validation_metrics,
        "metrics_by_split": metrics_by_split,
        "split_sizes": {
            split: len(split_rows_value)
            for split, split_rows_value in by_split.items()
        },
        "validation_sweep": validation_sweep,
        "thresholding": thresholding,
        "interpretation": {
            "rule": "Thresholds are selected on validation only, then applied unchanged to locked_test.",
            "warning": "This does not change the trained classifier, only its validation-selected operating point.",
            "grouping_note": (
                "When group_by is not none, each group receives a validation-selected threshold only if it has enough validation cases and both classes. Otherwise it falls back to the global validation threshold."
            ),
        },
    }

    write_json(output_json, report)
    write_jsonl(output_predictions, swept_predictions)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep classifier thresholds using validation only and report locked-test results."
    )
    parser.add_argument("--predictions", required=True)
    parser.add_argument(
        "--objective",
        choices=["f1", "balanced_accuracy", "mcc", "precision"],
        default="balanced_accuracy",
    )
    parser.add_argument(
        "--group-by",
        choices=["none", "language", "candidate_type"],
        default="none",
    )
    parser.add_argument("--min-validation-cases", type=int, default=30)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-predictions", required=True)

    args = parser.parse_args()

    result = run(
        predictions_path=Path(args.predictions),
        objective=args.objective,
        group_by=args.group_by,
        min_validation_cases=args.min_validation_cases,
        output_json=Path(args.output_json),
        output_predictions=Path(args.output_predictions),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())