from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    auc,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/consolidated_enriched_training_v1"
OUT = RUN / "figures"
BLUE = "#2364AA"
ORANGE = "#F28E2B"
GREEN = "#2A9D8F"
RED = "#D1495B"
NAVY = "#17365D"
GRID = "#D9E2F3"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def style_axis(ax, title: str, xlabel: str = "", ylabel: str = ""):
    ax.set_title(title, fontsize=14, fontweight="bold", color=NAVY, pad=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.28, color=GRID)
    ax.spines[["top", "right"]].set_visible(False)


def save(fig, name: str):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_cm(matrix, labels, title, name, cmap="Blues"):
    fig, ax = plt.subplots(figsize=(7.2, 6.1))
    image = ax.imshow(matrix, cmap=cmap)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xticks(range(len(labels)), labels, rotation=25, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_title(title, fontsize=14, fontweight="bold", color=NAVY, pad=14)
    threshold = matrix.max() / 2 if matrix.size else 0
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            value = int(matrix[row, col])
            ax.text(col, row, f"{value:,}", ha="center", va="center",
                    color="white" if value > threshold else "#102A43", fontweight="bold")
    save(fig, name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    binary_summary = load_json(RUN / "binary_v4/training_summary.json")
    category_summary = load_json(RUN / "category_v8/training_summary.json")
    binary_rows = [
        row for row in load_jsonl(RUN / "binary_v4/development_predictions.jsonl")
        if row["split"] == "development_validation"
    ]
    category_rows = [
        row for row in load_jsonl(RUN / "category_v8/development_predictions.jsonl")
        if row["split"] == "development_validation"
    ]

    y_true = np.array([int(row["gold"]) for row in binary_rows])
    y_pred = np.array([int(row["prediction"]) for row in binary_rows])
    scores = np.array([float(row["probability"]) for row in binary_rows])
    binary_cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    plot_cm(binary_cm, ["No update", "Docs update"],
            "Binary V4 — Validation Confusion Matrix",
            "binary_confusion_matrix.png")

    fpr, tpr, _ = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    ax.plot(fpr, tpr, color=BLUE, linewidth=2.6, label=f"ROC-AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#7A8793", label="Random classifier")
    ax.fill_between(fpr, tpr, alpha=0.10, color=BLUE)
    style_axis(ax, "Binary V4 — ROC Curve", "False positive rate", "True positive rate")
    ax.legend(loc="lower right", frameon=False)
    save(fig, "binary_roc_curve.png")

    precision, recall, _ = precision_recall_curve(y_true, scores)
    pr_auc = auc(recall, precision)
    prevalence = float(y_true.mean())
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    ax.plot(recall, precision, color=ORANGE, linewidth=2.6, label=f"PR-AUC = {pr_auc:.3f}")
    ax.axhline(prevalence, linestyle="--", color="#7A8793", label=f"Prevalence = {prevalence:.3f}")
    ax.fill_between(recall, precision, alpha=0.10, color=ORANGE)
    style_axis(ax, "Binary V4 — Precision–Recall Curve", "Recall", "Precision")
    ax.legend(loc="lower left", frameon=False)
    save(fig, "binary_precision_recall_curve.png")

    selected = next(
        item for item in binary_summary["model_results"]
        if item["model_name"] == binary_summary["selected_model"]
    )
    sweep = selected["validation_threshold_sweep"]
    thresholds = [row["threshold"] for row in sweep]
    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    for metric, color in [("precision", BLUE), ("recall", ORANGE), ("f1", GREEN), ("mcc", RED), ("balanced_accuracy", NAVY)]:
        ax.plot(thresholds, [row[metric] for row in sweep], marker="o", markersize=3,
                linewidth=2, label=metric.replace("_", " ").title(), color=color)
    chosen = float(binary_summary["selected_threshold"])
    ax.axvline(chosen, color="#111111", linestyle="--", linewidth=1.5, label=f"Selected = {chosen:.2f}")
    style_axis(ax, "Binary V4 — Validation Threshold Sweep", "Decision threshold", "Metric")
    ax.set_ylim(-0.03, 1.03)
    ax.legend(ncol=3, frameon=False, loc="lower center")
    save(fig, "binary_threshold_sweep.png")

    categories = ["api_reference", "configuration", "developer_setup", "model_contract"]
    cat_true = [str(row["gold"]) for row in category_rows]
    cat_pred = [str(row["prediction"]) for row in category_rows]
    cat_cm = confusion_matrix(cat_true, cat_pred, labels=categories)
    plot_cm(cat_cm, ["API reference", "Configuration", "Developer setup", "Model contract"],
            "Category V8 — Validation Confusion Matrix",
            "category_confusion_matrix.png", cmap="YlGnBu")

    per_class = category_summary["best_metrics"]["development_validation"]["per_class"]
    display = ["API reference", "Configuration", "Developer setup", "Model contract"]
    x = np.arange(len(categories))
    width = 0.24
    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    for offset, metric, color in [(-width, "precision", BLUE), (0, "recall", ORANGE), (width, "f1", GREEN)]:
        values = [float(per_class[name][metric]) for name in categories]
        bars = ax.bar(x + offset, values, width, label=metric.title(), color=color)
        ax.bar_label(bars, labels=[f"{value:.2f}" for value in values], padding=3, fontsize=8)
    ax.set_xticks(x, display)
    style_axis(ax, "Category V8 — Per-Class Validation Metrics", "", "Score")
    ax.set_ylim(0, 1.08)
    ax.legend(frameon=False, ncol=3)
    save(fig, "category_per_class_metrics.png")

    b = binary_summary["best_metrics"]["development_validation"]
    c = category_summary["best_metrics"]["development_validation"]
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8))
    binary_names = ["Accuracy", "Precision", "Recall", "F1", "Balanced acc.", "MCC"]
    binary_values = [b["accuracy"], b["precision"], b["recall"], b["f1"], b["balanced_accuracy"], b["mcc"]]
    bars = axes[0].barh(binary_names, binary_values, color=[BLUE, GREEN, ORANGE, RED, NAVY, "#7C3AED"])
    axes[0].bar_label(bars, labels=[f"{value:.3f}" for value in binary_values], padding=4)
    axes[0].set_xlim(0, 1.08)
    style_axis(axes[0], "Binary V4 validation", "Score", "")
    category_names = ["Accuracy", "Macro-F1", "Weighted-F1", "Balanced acc."]
    category_values = [c["accuracy"], c["macro_f1"], c["weighted_f1"], c["balanced_accuracy"]]
    bars = axes[1].barh(category_names, category_values, color=[BLUE, RED, GREEN, NAVY])
    axes[1].bar_label(bars, labels=[f"{value:.3f}" for value in category_values], padding=4)
    axes[1].set_xlim(0, 1.08)
    style_axis(axes[1], "Category V8 validation", "Score", "")
    fig.suptitle("Consolidated Enriched Training v1 — Classifier Overview",
                 fontsize=16, fontweight="bold", color=NAVY, y=1.02)
    save(fig, "classifier_metrics_overview.png")

    manifest = {
        "output_dir": str(OUT),
        "figures": sorted(path.name for path in OUT.glob("*.png")),
        "binary_validation_rows": len(binary_rows),
        "category_validation_rows": len(category_rows),
        "binary_roc_auc": roc_auc,
        "binary_pr_auc": pr_auc,
    }
    (OUT / "figures_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
