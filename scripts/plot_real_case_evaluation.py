from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sklearn.metrics import (
    auc,
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)


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


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def prediction_value(row: dict[str, Any]) -> bool:
    if "swept_pred_docs_update_required" in row:
        return bool_value(row["swept_pred_docs_update_required"])
    return bool_value(row.get("pred_docs_update_required"))


def split_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_split: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_split[str(row.get("dataset_split") or "unknown")].append(row)
    return dict(by_split)


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    gold = [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]
    pred = [1 if prediction_value(row) else 0 for row in rows]

    if not rows:
        return {
            "total_cases": 0,
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "specificity": 0.0,
            "false_positive_rate": 0.0,
            "true_positives": 0,
            "false_positives": 0,
            "true_negatives": 0,
            "false_negatives": 0,
        }

    tn, fp, fn, tp = confusion_matrix(gold, pred, labels=[0, 1]).ravel()
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)

    return {
        "total_cases": len(rows),
        "accuracy": safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "gold_distribution": dict(Counter(str(bool_value(row.get("gold_docs_update_required"))) for row in rows)),
        "pred_distribution": dict(Counter(str(prediction_value(row)) for row in rows)),
    }


def metric_at_threshold(rows: list[dict[str, Any]], threshold: float) -> dict[str, Any]:
    converted: list[dict[str, Any]] = []
    for row in rows:
        copied = dict(row)
        copied["swept_pred_docs_update_required"] = float(row.get("pred_probability")) >= threshold
        converted.append(copied)
    metrics = compute_metrics(converted)
    metrics["threshold"] = threshold
    return metrics


def save_confusion_matrix(path: Path, rows: list[dict[str, Any]], *, normalized: bool) -> None:
    gold = [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]
    pred = [1 if prediction_value(row) else 0 for row in rows]

    matrix = confusion_matrix(gold, pred, labels=[0, 1])
    title = "Confusion Matrix"
    if normalized:
        row_sums = matrix.sum(axis=1, keepdims=True)
        matrix_to_show = matrix / row_sums.clip(min=1)
        title = "Normalized Confusion Matrix"
    else:
        matrix_to_show = matrix

    plt.figure(figsize=(6, 5))
    plt.imshow(matrix_to_show)
    plt.title(title)
    plt.colorbar()
    labels = ["no update", "docs update"]
    plt.xticks([0, 1], labels)
    plt.yticks([0, 1], labels)
    plt.xlabel("Predicted")
    plt.ylabel("Gold")

    for i in range(2):
        for j in range(2):
            if normalized:
                text = f"{matrix_to_show[i, j]:.1%}\n({matrix[i, j]})"
            else:
                text = str(matrix[i, j])
            plt.text(j, i, text, ha="center", va="center")

    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def save_roc_curve(path: Path, rows: list[dict[str, Any]]) -> dict[str, float]:
    gold = [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]
    scores = [float(row.get("pred_probability")) for row in rows]

    if len(set(gold)) < 2:
        return {"roc_auc": 0.0}

    fpr, tpr, _thresholds = roc_curve(gold, scores)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, marker=".")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title(f"ROC Curve, AUC={roc_auc:.3f}")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate / Recall")
    plt.xlim(0, 1)
    plt.ylim(0, 1.02)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()

    return {"roc_auc": float(roc_auc)}


def save_pr_curve(path: Path, rows: list[dict[str, Any]]) -> dict[str, float]:
    gold = [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]
    scores = [float(row.get("pred_probability")) for row in rows]

    if len(set(gold)) < 2:
        return {"average_precision": 0.0}

    precision, recall, _thresholds = precision_recall_curve(gold, scores)
    avg_precision = average_precision_score(gold, scores)

    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, marker=".")
    plt.title(f"Precision-Recall Curve, AP={avg_precision:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1.02)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()

    return {"average_precision": float(avg_precision)}


def save_threshold_curves(path: Path, validation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    thresholds = [round(value / 100, 2) for value in range(5, 96, 5)]
    metrics = [metric_at_threshold(validation_rows, threshold) for threshold in thresholds]

    plt.figure(figsize=(9, 6))
    for key in ["precision", "recall", "f1", "specificity", "accuracy"]:
        plt.plot(thresholds, [item[key] for item in metrics], marker="o", label=key)

    plt.title("Validation Threshold Curves")
    plt.xlabel("Threshold")
    plt.ylabel("Score")
    plt.xlim(0, 1)
    plt.ylim(0, 1.02)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()

    return metrics


def save_probability_distribution(path: Path, rows: list[dict[str, Any]]) -> None:
    positives = [float(row.get("pred_probability")) for row in rows if bool_value(row.get("gold_docs_update_required"))]
    negatives = [float(row.get("pred_probability")) for row in rows if not bool_value(row.get("gold_docs_update_required"))]

    plt.figure(figsize=(8, 5))
    plt.hist(negatives, bins=20, alpha=0.65, label="gold no update")
    plt.hist(positives, bins=20, alpha=0.65, label="gold docs update")
    plt.title("Predicted Probability Distribution")
    plt.xlabel("Predicted probability")
    plt.ylabel("Count")
    plt.xlim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def save_metrics_bar(path: Path, metrics_by_name: dict[str, dict[str, Any]], title: str) -> None:
    names = list(metrics_by_name)
    metric_keys = ["accuracy", "precision", "recall", "f1", "specificity"]

    x = list(range(len(names)))
    width = 0.15

    plt.figure(figsize=(max(10, len(names) * 1.2), 6))
    for offset, key in enumerate(metric_keys):
        positions = [value + (offset - 2) * width for value in x]
        plt.bar(positions, [metrics_by_name[name][key] for name in names], width, label=key)

    plt.title(title)
    plt.xticks(x, names, rotation=45, ha="right")
    plt.ylabel("Score")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def grouped_metrics(rows: list[dict[str, Any]], group_key: str) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(group_key) or "unknown")].append(row)

    result = {
        name: compute_metrics(group_rows)
        for name, group_rows in groups.items()
        if len(group_rows) >= 5
    }
    return dict(sorted(result.items(), key=lambda item: item[0]))


def write_report(path: Path, summary: dict[str, Any], figure_paths: list[Path]) -> None:
    lines = [
        "# Real Case Study Evaluation Figures",
        "",
        "This report visualizes real GitHub PR classifier predictions.",
        "",
        "## Summary",
        "",
        f"- Prediction file: `{summary['prediction_file']}`",
        f"- Primary split: `{summary['primary_split']}`",
        f"- Primary cases: `{summary['primary_metrics']['total_cases']}`",
        f"- Accuracy: `{summary['primary_metrics']['accuracy']:.4f}`",
        f"- Precision: `{summary['primary_metrics']['precision']:.4f}`",
        f"- Recall: `{summary['primary_metrics']['recall']:.4f}`",
        f"- F1: `{summary['primary_metrics']['f1']:.4f}`",
        f"- Specificity: `{summary['primary_metrics']['specificity']:.4f}`",
        f"- ROC AUC: `{summary.get('roc_auc', 0.0):.4f}`",
        f"- Average precision: `{summary.get('average_precision', 0.0):.4f}`",
        "",
        "## Figures",
        "",
    ]

    for figure in figure_paths:
        lines.extend([f"### {figure.stem}", "", f"![{figure.stem}]({figure.name})", ""])

    path.write_text("\n".join(lines), encoding="utf-8")


def run(*, predictions_path: Path, output_dir: Path, primary_split: str) -> dict[str, Any]:
    rows = load_jsonl(predictions_path)
    by_split = split_rows(rows)

    if primary_split not in by_split:
        raise ValueError(f"Split {primary_split!r} not found. Available: {sorted(by_split)}")

    output_dir.mkdir(parents=True, exist_ok=True)

    primary_rows = by_split[primary_split]
    validation_rows = by_split.get("validation", [])

    figure_paths: list[Path] = []

    confusion_path = output_dir / f"confusion_matrix_{primary_split}.png"
    save_confusion_matrix(confusion_path, primary_rows, normalized=False)
    figure_paths.append(confusion_path)

    normalized_path = output_dir / f"confusion_matrix_{primary_split}_normalized.png"
    save_confusion_matrix(normalized_path, primary_rows, normalized=True)
    figure_paths.append(normalized_path)

    roc_path = output_dir / f"roc_curve_{primary_split}.png"
    roc_summary = save_roc_curve(roc_path, primary_rows)
    figure_paths.append(roc_path)

    pr_path = output_dir / f"precision_recall_curve_{primary_split}.png"
    pr_summary = save_pr_curve(pr_path, primary_rows)
    figure_paths.append(pr_path)

    prob_path = output_dir / f"probability_distribution_{primary_split}.png"
    save_probability_distribution(prob_path, primary_rows)
    figure_paths.append(prob_path)

    threshold_summary = []
    if validation_rows:
        threshold_path = output_dir / "threshold_metrics_curve_validation.png"
        threshold_summary = save_threshold_curves(threshold_path, validation_rows)
        figure_paths.append(threshold_path)

    split_metrics = {
        split: compute_metrics(split_rows)
        for split, split_rows in sorted(by_split.items())
    }
    split_path = output_dir / "metrics_by_split.png"
    save_metrics_bar(split_path, split_metrics, "Metrics by Split")
    figure_paths.append(split_path)

    language_metrics = grouped_metrics(primary_rows, "language")
    if language_metrics:
        language_path = output_dir / f"metrics_by_language_{primary_split}.png"
        save_metrics_bar(language_path, language_metrics, f"Metrics by Language, {primary_split}")
        figure_paths.append(language_path)

    candidate_metrics = grouped_metrics(primary_rows, "candidate_type")
    if candidate_metrics:
        candidate_path = output_dir / f"metrics_by_candidate_type_{primary_split}.png"
        save_metrics_bar(candidate_path, candidate_metrics, f"Metrics by Candidate Type, {primary_split}")
        figure_paths.append(candidate_path)

    summary = {
        "status": "ok",
        "prediction_file": str(predictions_path),
        "output_dir": str(output_dir),
        "primary_split": primary_split,
        "primary_metrics": compute_metrics(primary_rows),
        "metrics_by_split": split_metrics,
        "metrics_by_language": language_metrics,
        "metrics_by_candidate_type": candidate_metrics,
        "validation_threshold_curve": threshold_summary,
        "figures": [str(path) for path in figure_paths],
        **roc_summary,
        **pr_summary,
    }

    write_json(output_dir / "real_case_visual_summary.json", summary)
    write_report(output_dir / "real_case_visual_report.md", summary, figure_paths)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate real GitHub PR classifier evaluation figures.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--primary-split", default="locked_test")
    args = parser.parse_args()

    result = run(
        predictions_path=Path(args.predictions),
        output_dir=Path(args.output_dir),
        primary_split=args.primary_split,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())