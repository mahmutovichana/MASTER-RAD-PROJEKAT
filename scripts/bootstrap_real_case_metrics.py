from __future__ import annotations

import argparse
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def pred_value(row: dict[str, Any]) -> bool:
    if "swept_pred_docs_update_required" in row:
        return bool_value(row["swept_pred_docs_update_required"])
    return bool_value(row.get("pred_docs_update_required"))


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for row in rows:
        gold = bool_value(row.get("gold_docs_update_required"))
        pred = pred_value(row)

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
    }


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * q
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = index - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def bootstrap(rows: list[dict[str, Any]], *, iterations: int, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    metric_keys = ["accuracy", "precision", "recall", "f1", "specificity", "false_positive_rate"]
    samples: dict[str, list[float]] = {key: [] for key in metric_keys}

    for _ in range(iterations):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        metrics = compute_metrics(sample)
        for key in metric_keys:
            samples[key].append(float(metrics[key]))

    return {
        key: {
            "mean": sum(values) / len(values) if values else 0.0,
            "p025": percentile(values, 0.025),
            "p500": percentile(values, 0.500),
            "p975": percentile(values, 0.975),
        }
        for key, values in samples.items()
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Real Case Metrics Bootstrap Confidence Intervals",
        "",
        f"- Prediction file: `{report['prediction_file']}`",
        f"- Split: `{report['split']}`",
        f"- Cases: `{report['metrics']['total_cases']}`",
        f"- Bootstrap iterations: `{report['bootstrap_iterations']}`",
        "",
        "## Point Metrics",
        "",
        "```json",
        json.dumps(report["metrics"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## 95% Bootstrap Intervals",
        "",
        "| Metric | Mean | 2.5% | Median | 97.5% |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for key, values in report["bootstrap_ci"].items():
        lines.append(
            f"| {key} | {values['mean']:.4f} | {values['p025']:.4f} | {values['p500']:.4f} | {values['p975']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Wide intervals indicate that the evaluation split is too small for a stable final claim.",
            "- This script should be run again on the large-scale labeled/reviewed locked-test split.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap real-case classifier metrics.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--split", default="locked_test")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    rows = [
        row for row in load_jsonl(Path(args.predictions))
        if str(row.get("dataset_split")) == args.split
    ]

    if not rows:
        raise ValueError(f"No rows found for split: {args.split}")

    report = {
        "status": "ok",
        "prediction_file": args.predictions,
        "split": args.split,
        "metrics": compute_metrics(rows),
        "gold_distribution": dict(Counter(str(bool_value(row.get("gold_docs_update_required"))) for row in rows)),
        "pred_distribution": dict(Counter(str(pred_value(row)) for row in rows)),
        "bootstrap_iterations": args.iterations,
        "bootstrap_seed": args.seed,
        "bootstrap_ci": bootstrap(rows, iterations=args.iterations, seed=args.seed),
        "warning": "Confidence intervals on very small splits are diagnostic only.",
    }

    write_json(Path(args.output_json), report)
    write_markdown(Path(args.output_md), report)

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())