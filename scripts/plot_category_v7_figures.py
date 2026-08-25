from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_figure(output_dir: Path, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_dir / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.savefig(output_dir / f"{name}.pdf", bbox_inches="tight")
    plt.close()


def get_split_metrics(summary: dict[str, Any], split: str) -> dict[str, Any]:
    return summary["best_metrics_by_split"][split]


def plot_confusion_matrix(summary: dict[str, Any], output_dir: Path, split: str) -> None:
    metrics = get_split_metrics(summary, split)
    labels = metrics["labels"]
    matrix = metrics["confusion_matrix"]

    plt.figure(figsize=(7.5, 6.5))
    plt.imshow(matrix)
    plt.title(f"Category classifier confusion matrix — {split}")
    plt.xlabel("Predicted category")
    plt.ylabel("Gold category")
    plt.xticks(range(len(labels)), labels, rotation=35, ha="right")
    plt.yticks(range(len(labels)), labels)
    plt.colorbar(label="Number of cases")

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            plt.text(j, i, str(value), ha="center", va="center")

    save_figure(output_dir, f"category_v7_confusion_matrix_{split}")


def plot_per_class_f1(summary: dict[str, Any], output_dir: Path, split: str) -> None:
    metrics = get_split_metrics(summary, split)
    report = metrics["classification_report"]
    labels = metrics["labels"]
    f1_scores = [report[label]["f1-score"] for label in labels]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, f1_scores)
    plt.title(f"Per-class F1 score — {split}")
    plt.xlabel("Category")
    plt.ylabel("F1 score")
    plt.ylim(0, 1)
    plt.xticks(rotation=35, ha="right")

    for index, value in enumerate(f1_scores):
        plt.text(index, value + 0.02, f"{value:.3f}", ha="center")

    save_figure(output_dir, f"category_v7_per_class_f1_{split}")


def plot_metrics_by_split(summary: dict[str, Any], output_dir: Path) -> None:
    splits = ["train", "validation", "locked_test"]
    macro_f1 = [get_split_metrics(summary, split)["macro_f1"] for split in splits]
    weighted_f1 = [get_split_metrics(summary, split)["weighted_f1"] for split in splits]
    accuracy = [get_split_metrics(summary, split)["accuracy"] for split in splits]

    x = range(len(splits))
    width = 0.25

    plt.figure(figsize=(8.5, 5))
    plt.bar([value - width for value in x], macro_f1, width, label="Macro-F1")
    plt.bar(list(x), weighted_f1, width, label="Weighted-F1")
    plt.bar([value + width for value in x], accuracy, width, label="Accuracy")

    plt.title("Category classifier metrics by split")
    plt.xlabel("Split")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.xticks(list(x), splits)
    plt.legend()

    save_figure(output_dir, "category_v7_metrics_by_split")


def plot_distribution_by_split(summary: dict[str, Any], output_dir: Path) -> None:
    splits = ["train", "validation", "locked_test"]
    labels = summary["categories"]

    x = range(len(labels))
    width = 0.25

    plt.figure(figsize=(9, 5))

    for offset, split in zip([-width, 0, width], splits):
        counts = [
            summary["class_distribution"][split].get(label, 0)
            for label in labels
        ]
        plt.bar([value + offset for value in x], counts, width, label=split)

    plt.title("Category distribution by split")
    plt.xlabel("Category")
    plt.ylabel("Number of cases")
    plt.xticks(list(x), labels, rotation=35, ha="right")
    plt.legend()

    save_figure(output_dir, "category_v7_distribution_by_split")


def plot_prediction_distribution_locked(summary: dict[str, Any], output_dir: Path) -> None:
    metrics = get_split_metrics(summary, "locked_test")
    labels = metrics["labels"]

    gold = [metrics["gold_distribution"].get(label, 0) for label in labels]
    pred = [metrics["pred_distribution"].get(label, 0) for label in labels]

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(8.5, 5))
    plt.bar([value - width / 2 for value in x], gold, width, label="Gold")
    plt.bar([value + width / 2 for value in x], pred, width, label="Predicted")

    plt.title("Gold vs predicted category distribution — locked test")
    plt.xlabel("Category")
    plt.ylabel("Number of cases")
    plt.xticks(list(x), labels, rotation=35, ha="right")
    plt.legend()

    save_figure(output_dir, "category_v7_gold_vs_pred_locked_test")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate figures for V7 category classifier.")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--output-dir", required=True)

    args = parser.parse_args()

    summary = load_json(Path(args.summary))
    output_dir = Path(args.output_dir)

    plot_confusion_matrix(summary, output_dir, "validation")
    plot_confusion_matrix(summary, output_dir, "locked_test")
    plot_per_class_f1(summary, output_dir, "validation")
    plot_per_class_f1(summary, output_dir, "locked_test")
    plot_metrics_by_split(summary, output_dir)
    plot_distribution_by_split(summary, output_dir)
    plot_prediction_distribution_locked(summary, output_dir)

    print(
        json.dumps(
            {
                "status": "ok",
                "output_dir": str(output_dir),
                "figures": [
                    "category_v7_confusion_matrix_validation.png/pdf",
                    "category_v7_confusion_matrix_locked_test.png/pdf",
                    "category_v7_per_class_f1_validation.png/pdf",
                    "category_v7_per_class_f1_locked_test.png/pdf",
                    "category_v7_metrics_by_split.png/pdf",
                    "category_v7_distribution_by_split.png/pdf",
                    "category_v7_gold_vs_pred_locked_test.png/pdf",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())