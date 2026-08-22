from __future__ import annotations

import argparse
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


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool(row.get("gold_docs_update_required"))
        pred = bool(row.get("pred_docs_update_required"))

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
        "gold_distribution": dict(Counter(str(bool(row.get("gold_docs_update_required"))) for row in rows)),
        "pred_distribution": dict(Counter(str(bool(row.get("pred_docs_update_required"))) for row in rows)),
    }


def merge_predictions(
    *,
    base_predictions: Path,
    retry_predictions: Path,
    output_predictions: Path,
    output_summary: Path,
) -> dict[str, Any]:
    base_rows = load_jsonl(base_predictions)
    retry_rows = load_jsonl(retry_predictions)

    retry_by_case = {
        str(row.get("case_id")): row
        for row in retry_rows
    }

    merged: list[dict[str, Any]] = []
    replaced = 0

    for base_row in base_rows:
        case_id = str(base_row.get("case_id"))
        retry_row = retry_by_case.get(case_id)

        if retry_row is not None and retry_row.get("decision_status") == "ok":
            merged.append(retry_row)
            replaced += 1
        else:
            merged.append(base_row)

    write_jsonl(output_predictions, merged)

    completed = [row for row in merged if row.get("decision_status") == "ok"]
    failed = [row for row in merged if row.get("decision_status") != "ok"]

    summary = {
        "status": "ok",
        "base_predictions": str(base_predictions),
        "retry_predictions": str(retry_predictions),
        "output_predictions": str(output_predictions),
        "replaced_with_successful_retry": replaced,
        "total_cases": len(merged),
        "completed_cases": len(completed),
        "failed_cases": len(failed),
        "coverage": safe_div(len(completed), len(merged)),
        "decision_status_counts": dict(Counter(str(row.get("decision_status")) for row in merged)),
        "all_cases_conservative_metrics": compute_metrics(merged),
        "completed_only_metrics": compute_metrics(completed),
    }

    output_summary.parent.mkdir(parents=True, exist_ok=True)
    output_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge base LLM judge predictions with retry predictions.")
    parser.add_argument("--base-predictions", required=True)
    parser.add_argument("--retry-predictions", required=True)
    parser.add_argument("--output-predictions", required=True)
    parser.add_argument("--output-summary", required=True)
    args = parser.parse_args()

    result = merge_predictions(
        base_predictions=Path(args.base_predictions),
        retry_predictions=Path(args.retry_predictions),
        output_predictions=Path(args.output_predictions),
        output_summary=Path(args.output_summary),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())