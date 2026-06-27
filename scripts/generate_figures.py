from __future__ import annotations

import json
import sys
import zlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
sys.path.insert(0, str(ROOT))
BUNDLED_PYTHON_PACKAGES = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python"
if BUNDLED_PYTHON_PACKAGES.exists():
    sys.path.insert(0, str(BUNDLED_PYTHON_PACKAGES))

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ModuleNotFoundError:
    plt = None
    HAS_MATPLOTLIB = False

from docguard.evaluator import evaluate_split, read_jsonl


def save_bar(path: Path, labels: list[str], values: list[float], title: str, ylabel: str = "Count") -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_bar(path, values)
        return
    plt.figure(figsize=(max(8, len(labels) * 0.35), 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_grouped_metrics(path: Path, metrics_v03: dict) -> None:
    labels = ["precision", "recall", "F1", "scenario acc.", "fact coverage"]
    v01 = [1.0, 1.0, 1.0, 1.0, 0.8]
    v02 = [0.9310, 1.0, 0.9643, 0.23, 0.2759]
    v03 = [
        metrics_v03["docs_update_required_precision"],
        metrics_v03["docs_update_required_recall"],
        metrics_v03["docs_update_required_f1"],
        metrics_v03["scenario_type_accuracy"],
        metrics_v03["patch_fact_coverage"],
    ]
    if not HAS_MATPLOTLIB:
        save_fallback_bar(path, v01 + v02 + v03)
        return
    x = list(range(len(labels)))
    width = 0.25
    plt.figure(figsize=(10, 5))
    plt.bar([i - width for i in x], v01, width, label="v0.1")
    plt.bar(x, v02, width, label="v0.2")
    plt.bar([i + width for i in x], v03, width, label="v0.3")
    plt.xticks(x, labels)
    plt.ylim(0, 1.05)
    plt.ylabel("Score")
    plt.title("Baseline Metrics Across Dataset Versions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_confusion_matrix(path: Path, matrix: list[list[int]], labels: list[str], title: str) -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_matrix(path, matrix)
        return
    plt.figure(figsize=(max(6, len(labels) * 0.35), max(5, len(labels) * 0.35)))
    plt.imshow(matrix, cmap="Blues")
    plt.title(title)
    plt.colorbar()
    plt.xticks(range(len(labels)), labels, rotation=75, ha="right", fontsize=7)
    plt.yticks(range(len(labels)), labels, fontsize=7)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value:
                plt.text(j, i, str(value), ha="center", va="center", fontsize=6)
    plt.xlabel("Predicted")
    plt.ylabel("Gold")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def pr_roc_points(records: list[dict], predictions: list[dict]) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    thresholds = [1.0, 0.5, 0.0]
    pr = []
    roc = []
    positives = sum(1 for r in records if r["docs_update_required"])
    negatives = len(records) - positives
    for threshold in thresholds:
        tp = fp = fn = tn = 0
        for record, prediction in zip(records, predictions):
            pred = prediction["docs_update_score"] >= threshold
            gold = record["docs_update_required"]
            if pred and gold:
                tp += 1
            elif pred and not gold:
                fp += 1
            elif not pred and gold:
                fn += 1
            else:
                tn += 1
        precision = tp / (tp + fp) if tp + fp else 1.0
        recall = tp / positives if positives else 0.0
        fpr = fp / negatives if negatives else 0.0
        tpr = recall
        pr.append((recall, precision))
        roc.append((fpr, tpr))
    return pr, roc


def save_line(path: Path, points: list[tuple[float, float]], title: str, xlabel: str, ylabel: str) -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_line(path, points)
        return
    xs, ys = zip(*points)
    plt.figure(figsize=(6, 5))
    plt.plot(xs, ys, marker="o")
    plt.xlim(0, 1.02)
    plt.ylim(0, 1.02)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def write_png(path: Path, width: int, height: int, pixels: list[list[tuple[int, int, int]]]) -> None:
    raw = b"".join(b"\x00" + b"".join(bytes(pixel) for pixel in row) for row in pixels)
    def chunk(kind: bytes, data: bytes) -> bytes:
        import struct
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return length + kind + data + crc
    import struct
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def blank(width: int = 900, height: int = 520) -> list[list[tuple[int, int, int]]]:
    return [[(250, 250, 250) for _ in range(width)] for _ in range(height)]


def rect(pixels: list[list[tuple[int, int, int]]], x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    height = len(pixels)
    width = len(pixels[0])
    for y in range(max(0, y0), min(height, y1)):
        for x in range(max(0, x0), min(width, x1)):
            pixels[y][x] = color


def save_fallback_bar(path: Path, values: list[float]) -> None:
    width, height = 900, 520
    pixels = blank(width, height)
    rect(pixels, 60, 40, 65, 470, (70, 70, 70))
    rect(pixels, 60, 470, 850, 475, (70, 70, 70))
    if not values:
        write_png(path, width, height, pixels)
        return
    max_value = max(values) or 1
    bar_w = max(4, 760 // len(values))
    for i, value in enumerate(values):
        x0 = 75 + i * bar_w
        x1 = x0 + max(3, bar_w - 4)
        bar_h = int((float(value) / max_value) * 380)
        rect(pixels, x0, 470 - bar_h, x1, 470, (46, 113, 184))
    write_png(path, width, height, pixels)


def save_fallback_matrix(path: Path, matrix: list[list[int]]) -> None:
    size = 700
    pixels = blank(size, size)
    n = max(1, len(matrix))
    cell = max(1, 600 // n)
    max_value = max([max(row) for row in matrix if row] or [1]) or 1
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            intensity = int(255 - 200 * (value / max_value))
            rect(pixels, 50 + j * cell, 50 + i * cell, 50 + (j + 1) * cell - 1, 50 + (i + 1) * cell - 1, (intensity, intensity, 255))
    write_png(path, size, size, pixels)


def save_fallback_line(path: Path, points: list[tuple[float, float]]) -> None:
    width, height = 700, 520
    pixels = blank(width, height)
    rect(pixels, 60, 40, 65, 460, (70, 70, 70))
    rect(pixels, 60, 460, 650, 465, (70, 70, 70))
    mapped = [(60 + int(x * 580), 460 - int(y * 400)) for x, y in points]
    for x, y in mapped:
        rect(pixels, x - 4, y - 4, x + 5, y + 5, (200, 70, 50))
    write_png(path, width, height, pixels)


def main() -> int:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    test_records = read_jsonl(DATA_DIR / "test.jsonl")
    metrics, predictions = evaluate_split("test")

    save_bar(FIGURES_DIR / "dataset_version_record_counts.png", ["v0.1", "v0.2", "v0.3"], [1000, 1500, len(records)], "Dataset Version Record Counts")

    scenario_counts = Counter(r["scenario_type"] for r in records)
    save_bar(FIGURES_DIR / "scenario_distribution_v0_3.png", list(scenario_counts), list(scenario_counts.values()), "Scenario Distribution v0.3")

    category_counts = Counter(r["doc_category"] for r in records)
    save_bar(FIGURES_DIR / "doc_category_distribution_v0_3.png", list(category_counts), list(category_counts.values()), "Documentation Category Distribution v0.3")

    label_counts = Counter("positive" if r["docs_update_required"] else "negative" for r in records)
    save_bar(FIGURES_DIR / "positive_negative_distribution_v0_3.png", list(label_counts), list(label_counts.values()), "Positive vs Negative Records v0.3")

    split_counts = {split: len(read_jsonl(DATA_DIR / f"{split}.jsonl")) for split in ["train", "validation", "test"]}
    save_bar(FIGURES_DIR / "split_distribution_v0_3.png", list(split_counts), list(split_counts.values()), "Split Distribution v0.3")

    save_grouped_metrics(FIGURES_DIR / "baseline_metrics_v0_1_v0_2_v0_3.png", metrics)

    save_bar(
        FIGURES_DIR / "per_scenario_accuracy_v0_3.png",
        list(metrics["per_scenario"]),
        [m["accuracy"] for m in metrics["per_scenario"].values()],
        "Per-Scenario Baseline Accuracy v0.3",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / "per_doc_category_accuracy_v0_3.png",
        list(metrics["per_doc_category"]),
        [m["accuracy"] for m in metrics["per_doc_category"].values()],
        "Per-Doc-Category Baseline Accuracy v0.3",
        "Accuracy",
    )

    binary_labels = ["negative", "positive"]
    binary_matrix = [[0, 0], [0, 0]]
    for record, prediction in zip(test_records, predictions):
        i = 1 if record["docs_update_required"] else 0
        j = 1 if prediction["docs_update_required"] else 0
        binary_matrix[i][j] += 1
    save_confusion_matrix(FIGURES_DIR / "binary_confusion_matrix_v0_3.png", binary_matrix, binary_labels, "docs_update_required Confusion Matrix v0.3")

    scenario_labels = sorted(set(r["scenario_type"] for r in test_records) | set(p["scenario_type"] for p in predictions))
    idx = {label: i for i, label in enumerate(scenario_labels)}
    matrix = [[0 for _ in scenario_labels] for _ in scenario_labels]
    for record, prediction in zip(test_records, predictions):
        matrix[idx[record["scenario_type"]]][idx[prediction["scenario_type"]]] += 1
    save_confusion_matrix(FIGURES_DIR / "scenario_confusion_matrix_v0_3.png", matrix, scenario_labels, "Scenario Type Confusion Matrix v0.3")

    pr, roc = pr_roc_points(test_records, predictions)
    save_line(FIGURES_DIR / "precision_recall_curve_v0_3.png", pr, "Baseline Precision-Recall Curve v0.3", "Recall", "Precision")
    save_line(FIGURES_DIR / "roc_curve_v0_3.png", roc, "Baseline ROC Curve v0.3", "False Positive Rate", "True Positive Rate")

    report_lines = [
        "# Visual Evaluation Report",
        "",
        "These figures summarize dataset v0.3 and the rule-based baseline. ROC and precision-recall curves use simple baseline scores: 1.0 for confident positive, 0.0 for confident negative, and 0.5 for unknown or unsupported changes. They are included for completeness; these curves will be more meaningful for the later NLP-assisted model.",
        "",
        "Figure generation tries to use matplotlib first. In this local environment matplotlib was unavailable, so the script can fall back to a small built-in PNG renderer while preserving the same output filenames.",
        "",
    ]
    for image in sorted(FIGURES_DIR.glob("*.png")):
        report_lines.extend([f"## {image.stem}", "", f"![{image.stem}](figures/{image.name})", ""])
    (REPORTS_DIR / "visual_evaluation_report.md").write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Generated {len(list(FIGURES_DIR.glob('*.png')))} figures in {FIGURES_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
