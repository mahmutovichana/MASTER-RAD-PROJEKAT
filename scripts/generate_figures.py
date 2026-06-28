from __future__ import annotations

import json
import sys
import zlib
import textwrap
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
from docguard_llm.evaluator import MOCK_WARNING, evaluate_predictions as evaluate_llm_predictions


def save_bar(path: Path, labels: list[str], values: list[float], title: str, ylabel: str = "Count") -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_bar(path, values)
        return
    plt.figure(figsize=(max(8, len(labels) * 0.35), 5))
    bars = plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    max_value = max(values) if values else 0
    if max_value <= 0:
        plt.ylim(0, 1)
        plt.text(0.5, 0.55, "All values are zero", transform=plt.gca().transAxes, ha="center", va="center", fontsize=11)
    elif max_value <= 1.0 and ylabel.lower() in {"accuracy", "score", "f1", "macro f1", "agreement"}:
        plt.ylim(0, 1.05)
    for bar, value in zip(bars, values):
        if len(labels) <= 20:
            label = f"{value:.2f}" if isinstance(value, float) and value <= 1 else f"{value:.0f}"
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label, ha="center", va="bottom", fontsize=7)
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


def save_float_confusion_matrix(path: Path, matrix: list[list[float]], labels: list[str], title: str) -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_matrix(path, [[int(value * 100) for value in row] for row in matrix])
        return
    wrapped = ["\n".join(textwrap.wrap(label, width=18)) for label in labels]
    size = max(7, min(16, len(labels) * 0.65))
    plt.figure(figsize=(size, size))
    plt.imshow(matrix, cmap="Blues", vmin=0, vmax=1)
    plt.title(title)
    plt.colorbar(label="Row-normalized share")
    plt.xticks(range(len(labels)), wrapped, rotation=0, ha="center", fontsize=7)
    plt.yticks(range(len(labels)), wrapped, fontsize=7)
    if len(labels) <= 14:
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value >= 0.05:
                    plt.text(j, i, f"{value:.0%}", ha="center", va="center", fontsize=6)
    plt.xlabel("Predicted")
    plt.ylabel("Gold")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def save_horizontal_bar(path: Path, labels: list[str], values: list[float], title: str, xlabel: str = "Count") -> None:
    if not HAS_MATPLOTLIB:
        save_fallback_bar(path, values)
        return
    height = max(4, min(14, len(labels) * 0.45 + 1.5))
    wrapped = ["\n".join(textwrap.wrap(label, width=42)) for label in labels]
    plt.figure(figsize=(12, height))
    bars = plt.barh(wrapped, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.gca().invert_yaxis()
    for bar, value in zip(bars, values):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f" {value:.2f}" if isinstance(value, float) and value <= 1 else f" {value:.0f}", va="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(path, dpi=170)
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
    if all(float(value) == 0.0 for value in values):
        rect(pixels, 360, 245, 540, 275, (210, 210, 210))
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
    for stale_name in ["real_llm_parse_error_counts_v0_3.png", "real_llm_latency_comparison_v0_3.png"]:
        stale_path = FIGURES_DIR / stale_name
        if stale_path.exists():
            stale_path.unlink()
    records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    test_records = read_jsonl(DATA_DIR / "test.jsonl")
    metrics, predictions = evaluate_split("test")

    save_bar(FIGURES_DIR / "dataset_version_record_counts.png", ["v0.1", "v0.2", "v0.3"], [1000, 1500, len(records)], "Dataset Version Record Counts")
    save_bar(FIGURES_DIR / "dataset_version_record_counts_v0_3_v0_4.png", ["v0.3", "v0.4"], [2500, len(records)], "Dataset Version Record Counts: v0.3 vs v0.4")

    scenario_counts = Counter(r["scenario_type"] for r in records)
    save_bar(FIGURES_DIR / "scenario_distribution_v0_3.png", list(scenario_counts), list(scenario_counts.values()), "Scenario Distribution v0.3")
    save_bar(FIGURES_DIR / "scenario_distribution_v0_4.png", list(scenario_counts), list(scenario_counts.values()), "Scenario Distribution v0.4")

    category_counts = Counter(r["doc_category"] for r in records)
    save_bar(FIGURES_DIR / "doc_category_distribution_v0_3.png", list(category_counts), list(category_counts.values()), "Documentation Category Distribution v0.3")
    save_bar(FIGURES_DIR / "doc_category_distribution_v0_4.png", list(category_counts), list(category_counts.values()), "Documentation Category Distribution v0.4")

    label_counts = Counter("positive" if r["docs_update_required"] else "negative" for r in records)
    save_bar(FIGURES_DIR / "positive_negative_distribution_v0_3.png", list(label_counts), list(label_counts.values()), "Positive vs Negative Records v0.3")
    save_bar(FIGURES_DIR / "positive_negative_distribution_v0_4.png", list(label_counts), list(label_counts.values()), "Positive vs Negative Records v0.4")

    split_counts = {split: len(read_jsonl(DATA_DIR / f"{split}.jsonl")) for split in ["train", "validation", "test"]}
    save_bar(FIGURES_DIR / "split_distribution_v0_3.png", list(split_counts), list(split_counts.values()), "Split Distribution v0.3")
    write_v0_4_figures(metrics)

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

    top_scenarios = [name for name, _count in Counter(r["scenario_type"] for r in test_records).most_common(15)]
    scenario_labels = sorted(set(top_scenarios + ["other", "unknown_change"]))
    def group_scenario(name: str) -> str:
        return name if name in top_scenarios or name == "unknown_change" else "other"
    idx = {label: i for i, label in enumerate(scenario_labels)}
    matrix = [[0 for _ in scenario_labels] for _ in scenario_labels]
    for record, prediction in zip(test_records, predictions):
        matrix[idx[group_scenario(record["scenario_type"])]][idx[group_scenario(prediction["scenario_type"])]] += 1
    save_confusion_matrix(FIGURES_DIR / "scenario_confusion_matrix_v0_3.png", matrix, scenario_labels, "Scenario Type Confusion Matrix v0.3")

    pr, roc = pr_roc_points(test_records, predictions)
    save_line(FIGURES_DIR / "precision_recall_curve_v0_3.png", pr, "Baseline Precision-Recall Curve v0.3", "Recall", "Precision")
    save_line(FIGURES_DIR / "roc_curve_v0_3.png", roc, "Baseline ROC Curve v0.3", "False Positive Rate", "True Positive Rate")

    mock_llm_metrics = load_llm_metrics("mock")
    if mock_llm_metrics:
        write_llm_figures(metrics, mock_llm_metrics, "mock", "mock backend")

    real_llm_metrics = load_llm_metrics("real")
    if real_llm_metrics:
        write_llm_figures(metrics, real_llm_metrics, "real", "real Hugging Face")

    report_lines = [
        "# Visual Evaluation Report",
        "",
        f"> {MOCK_WARNING}",
        "",
        "These figures summarize dataset v0.3 history, v0.4 CPU-first dataset diagnostics, and the rule-based, ML, and deterministic hybrid evaluation paths. ROC and precision-recall curves use simple baseline scores: 1.0 for confident positive, 0.0 for confident negative, and 0.5 for unknown or unsupported changes.",
        "",
        "The all-scenario HF confusion chart with an `other` bucket is diagnostic only and should not be used as the main thesis figure because `other` aggregates unrelated scenario labels. Use the positive scenario, negative scenario, grouped negative reason, and top-confusion figures instead.",
        "",
        "Figure generation tries to use matplotlib first. In this local environment matplotlib was unavailable, so the script can fall back to a small built-in PNG renderer while preserving the same output filenames.",
        "",
    ]
    add_figure_section(report_lines, "Rule-based baseline figures", [p for p in sorted(FIGURES_DIR.glob("*.png")) if not is_llm_figure(p.name)])
    add_figure_section(report_lines, "Mock LLM pipeline figures", [p for p in sorted(FIGURES_DIR.glob("*_mock.png"))])
    real_figures = [p for p in sorted(FIGURES_DIR.glob("*.png")) if is_real_llm_figure(p.name)]
    if real_figures:
        add_figure_section(report_lines, "Real Hugging Face LLM figures", real_figures)
    else:
        report_lines.extend(["## Real Hugging Face LLM figures", "", "No real Hugging Face LLM prediction files were found yet.", ""])
    (REPORTS_DIR / "visual_evaluation_report.md").write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Generated {len(list(FIGURES_DIR.glob('*.png')))} figures in {FIGURES_DIR.relative_to(ROOT)}")
    return 0


def add_figure_section(report_lines: list[str], title: str, images: list[Path]) -> None:
    report_lines.extend([f"## {title}", ""])
    for image in images:
        report_lines.extend([f"### {image.stem}", "", f"![{image.stem}](figures/{image.name})", ""])


def is_llm_figure(name: str) -> bool:
    return "llm" in name


def is_real_llm_figure(name: str) -> bool:
    return name.startswith("baseline_vs_real_llm_") or name.startswith("real_llm_")


def load_llm_predictions_for_model(model_key: str, result_kind: str) -> tuple[str, list[dict]] | None:
    if result_kind == "mock":
        candidates = sorted(DATA_DIR.glob(f"llm_predictions_v0_3_*_mock_{model_key}.jsonl"))
    else:
        candidates = [p for p in sorted(DATA_DIR.glob(f"llm_predictions_v0_3_*_*_{model_key}.jsonl")) if "_mock_" not in p.name]
    if not candidates:
        return None
    path = candidates[-1]
    stem = path.name.removeprefix("llm_predictions_v0_3_").removesuffix(f"_{model_key}.jsonl")
    split = stem.split("_mock_")[0] if "_mock_" in stem else stem.split("_", 1)[0]
    return split, read_jsonl(path)


def load_llm_metrics(result_kind: str) -> dict[str, dict]:
    metrics = {}
    for path in sorted(DATA_DIR.glob("llm_predictions_v0_3_*.jsonl")):
        is_mock = "_mock_" in path.name
        if result_kind == "mock" and not is_mock:
            continue
        if result_kind == "real" and is_mock:
            continue
        stem = path.stem.removeprefix("llm_predictions_v0_3_")
        for split in ["validation", "test", "train"]:
            mock_prefix = f"{split}_mock_"
            real_prefixes = [f"{split}_transformers_local_", f"{split}_text_generation_inference_"]
            if result_kind == "mock" and stem.startswith(mock_prefix):
                model_key = stem.removeprefix(mock_prefix)
            elif result_kind == "real" and any(stem.startswith(prefix) for prefix in real_prefixes):
                prefix = next(prefix for prefix in real_prefixes if stem.startswith(prefix))
                model_key = stem.removeprefix(prefix)
            else:
                continue
            predictions = read_jsonl(path)
            records = read_jsonl(DATA_DIR / f"{split}.jsonl")[: len(predictions)]
            metrics[model_key] = evaluate_llm_predictions(records, predictions)
            break
    return metrics


def write_llm_figures(baseline_metrics: dict, llm_metrics: dict[str, dict], result_kind: str, title_suffix: str) -> None:
    model_labels = list(llm_metrics)
    best_model = max(model_labels, key=lambda key: llm_metrics[key]["docs_update_required_f1"])
    best_metrics = llm_metrics[best_model]
    if result_kind == "mock":
        names = {
            "baseline": "baseline_vs_llm_metrics_v0_3_mock.png",
            "comparison": "llm_model_comparison_metrics_v0_3_mock.png",
            "category": "baseline_vs_llm_doc_category_accuracy_v0_3_mock.png",
            "facts": "baseline_vs_llm_fact_coverage_v0_3_mock.png",
            "parse": "llm_parse_error_counts_v0_3_mock.png",
            "latency": "llm_latency_comparison_v0_3_mock.png",
            "confusion": "llm_confusion_matrix_best_model_v0_3_mock.png",
            "per_category": "llm_per_doc_category_best_model_v0_3_mock.png",
        }
    else:
        names = {
            "baseline": "baseline_vs_real_llm_metrics_v0_3.png",
            "comparison": "real_llm_model_comparison_metrics_v0_3.png",
            "category": "baseline_vs_real_llm_doc_category_accuracy_v0_3.png",
            "facts": "baseline_vs_real_llm_fact_coverage_v0_3.png",
            "parse": "real_llm_parse_errors_v0_3.png",
            "latency": "real_llm_latency_v0_3.png",
            "confusion": "real_llm_confusion_matrix_best_model_v0_3.png",
            "per_category": "real_llm_per_doc_category_best_model_v0_3.png",
        }
    save_bar(
        FIGURES_DIR / names["baseline"],
        ["baseline F1", *[f"{m} F1" for m in model_labels]],
        [baseline_metrics["docs_update_required_f1"], *[llm_metrics[m]["docs_update_required_f1"] for m in model_labels]],
        f"Baseline vs LLM F1 v0.3 ({title_suffix})",
        "F1",
    )
    save_grouped_llm_metrics(FIGURES_DIR / names["comparison"], llm_metrics, title_suffix)
    save_bar(
        FIGURES_DIR / names["category"],
        ["baseline", *model_labels],
        [baseline_metrics["doc_category_accuracy"], *[llm_metrics[m]["doc_category_accuracy"] for m in model_labels]],
        f"Baseline vs LLM Doc Category Accuracy v0.3 ({title_suffix})",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / names["facts"],
        ["baseline", *model_labels],
        [baseline_metrics["patch_fact_coverage"], *[llm_metrics[m]["patch_fact_coverage"] for m in model_labels]],
        f"Baseline vs LLM Fact Coverage v0.3 ({title_suffix})",
        "Coverage",
    )
    save_bar(FIGURES_DIR / names["parse"], model_labels, [llm_metrics[m]["parse_error_count"] for m in model_labels], f"LLM Parse Error Counts v0.3 ({title_suffix})")
    if any(llm_metrics[m].get("average_latency_seconds") is not None for m in model_labels):
        save_bar(FIGURES_DIR / names["latency"], model_labels, [llm_metrics[m].get("average_latency_seconds") or 0 for m in model_labels], f"LLM Latency Comparison v0.3 ({title_suffix})", "Seconds")
    if result_kind == "real":
        labels = []
        values = []
        for model_key, model_metrics in llm_metrics.items():
            labels.extend([
                f"{model_key} raw scenario",
                f"{model_key} norm scenario",
                f"{model_key} raw category",
                f"{model_key} norm category",
                f"{model_key} raw target",
                f"{model_key} norm target",
            ])
            values.extend([
                model_metrics.get("raw_scenario_type_accuracy", 0.0),
                model_metrics.get("scenario_type_accuracy", 0.0),
                model_metrics.get("raw_doc_category_accuracy", 0.0),
                model_metrics.get("doc_category_accuracy", 0.0),
                model_metrics.get("raw_target_doc_file_accuracy", 0.0),
                model_metrics.get("target_doc_file_accuracy", 0.0),
            ])
        save_bar(FIGURES_DIR / "real_llm_normalized_vs_raw_accuracy_v0_3.png", labels, values, "Real LLM Normalized vs Raw Accuracy v0.3", "Accuracy")
    best_predictions = load_llm_predictions_for_model(best_model, result_kind)
    if best_predictions:
        best_split, best_rows = best_predictions
        best_records = read_jsonl(DATA_DIR / f"{best_split}.jsonl")[: len(best_rows)]
        labels = ["negative", "positive"]
        llm_matrix = [[0, 0], [0, 0]]
        for record, prediction in zip(best_records, best_rows):
            i = 1 if record["docs_update_required"] else 0
            j = 1 if prediction["docs_update_required"] else 0
            llm_matrix[i][j] += 1
        save_confusion_matrix(FIGURES_DIR / names["confusion"], llm_matrix, labels, f"LLM Confusion Matrix: {best_model} ({title_suffix})")
        save_bar(
            FIGURES_DIR / names["per_category"],
            list(best_metrics["per_doc_category"]),
            [m["accuracy"] for m in best_metrics["per_doc_category"].values()],
            f"LLM Per-Doc-Category Accuracy: {best_model} ({title_suffix})",
            "Accuracy",
        )


def save_grouped_llm_metrics(path: Path, llm_metrics: dict[str, dict], title_suffix: str = "") -> None:
    values = []
    labels = []
    for model_key, metrics in llm_metrics.items():
        labels.extend([f"{model_key} precision", f"{model_key} recall", f"{model_key} F1"])
        values.extend([
            metrics["docs_update_required_precision"],
            metrics["docs_update_required_recall"],
            metrics["docs_update_required_f1"],
        ])
    suffix = f" ({title_suffix})" if title_suffix else ""
    save_bar(path, labels, values, f"LLM Model Comparison Metrics v0.3{suffix}", "Score")


def write_v0_4_figures(baseline_metrics: dict) -> None:
    try:
        from docguard_ml.evaluate import evaluate as evaluate_ml
        from docguard_hybrid.evaluator import evaluate_records as evaluate_hybrid
    except Exception:
        return
    try:
        ml_metrics = evaluate_ml("validation")
        hybrid_records = read_jsonl(DATA_DIR / "validation.jsonl")
        hybrid_metrics, _hybrid_predictions = evaluate_hybrid(hybrid_records)
    except Exception:
        return
    hf_metrics = read_metrics_report(REPORTS_DIR / "hf_embedding_evaluation_v0_4_raw_diff_plus_docs_validation.md")
    full_hf_metrics = read_metrics_report(REPORTS_DIR / "hf_embedding_evaluation_v0_4_full_current_validation.md") or read_metrics_report(REPORTS_DIR / "hf_embedding_evaluation_v0_4_validation.md")
    hybrid_hf_metrics = read_metrics_report(REPORTS_DIR / "hybrid_hf_embedding_evaluation_v0_4_raw_diff_plus_docs_validation.md") or read_metrics_report(REPORTS_DIR / "hybrid_hf_embedding_evaluation_v0_4_validation.md")
    save_bar(
        FIGURES_DIR / "baseline_vs_ml_vs_hybrid_metrics_v0_4.png",
        ["baseline F1", "ML F1", "hybrid F1"],
        [
            baseline_metrics.get("docs_update_required_f1", 0.0),
            ml_metrics.get("docs_update_required_f1", 0.0),
            hybrid_metrics.get("docs_update_required_f1", 0.0),
        ],
        "Baseline vs ML vs Hybrid Binary F1 v0.4",
        "F1",
    )
    names = ["baseline", "ML", "HF emb.", "hybrid", "hybrid+HF"]
    values = [
        baseline_metrics.get("docs_update_required_f1", 0.0),
        ml_metrics.get("docs_update_required_f1", 0.0),
        hf_metrics.get("docs_update_required_f1", 0.0),
        hybrid_metrics.get("docs_update_required_f1", 0.0),
        hybrid_hf_metrics.get("docs_update_required_f1", 0.0),
    ]
    save_bar(
        FIGURES_DIR / "baseline_vs_ml_vs_hf_vs_hybrid_metrics_v0_4.png",
        names,
        values,
        "Baseline vs ML vs HF vs Hybrid Binary F1 v0.4",
        "F1",
    )
    save_bar(
        FIGURES_DIR / "positive_only_target_file_accuracy_v0_4.png",
        ["ML", "hybrid"],
        [ml_metrics.get("positive_target_doc_file_accuracy", 0.0), hybrid_metrics.get("positive_target_doc_file_accuracy", 0.0)],
        "Positive-Only Target File Accuracy v0.4",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / "negative_classification_accuracy_v0_4.png",
        ["ML", "hybrid"],
        [ml_metrics.get("negative_classification_accuracy", 0.0), hybrid_metrics.get("negative_classification_accuracy", 0.0)],
        "Negative Classification Accuracy v0.4",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / "macro_f1_scenario_doc_category_v0_4.png",
        ["ML scenario", "hybrid scenario", "ML category", "hybrid category"],
        [
            ml_metrics.get("macro_scenario_f1", 0.0),
            hybrid_metrics.get("macro_scenario_f1", 0.0),
            ml_metrics.get("macro_doc_category_f1", 0.0),
            hybrid_metrics.get("macro_doc_category_f1", 0.0),
        ],
        "Macro F1 by Scenario and Doc Category v0.4",
        "Macro F1",
    )
    save_bar(
        FIGURES_DIR / "router_ml_llm_agreement_v0_4.png",
        ["router/ML", "router/LLM"],
        [hybrid_metrics.get("router_ml_agreement_rate", 0.0), hybrid_metrics.get("router_llm_agreement_rate", 0.0)],
        "Router, ML, and LLM Agreement v0.4",
        "Agreement",
    )
    save_bar(
        FIGURES_DIR / "hf_embedding_vs_ml_scenario_accuracy_v0_4.png",
        ["ML", "HF embedding"],
        [ml_metrics.get("positive_scenario_type_accuracy", 0.0), hf_metrics.get("positive_scenario_type_accuracy", 0.0)],
        "HF Embedding vs ML Scenario Accuracy v0.4",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / "hf_embedding_doc_category_accuracy_v0_4.png",
        ["HF positive category", "HF macro category"],
        [hf_metrics.get("positive_doc_category_accuracy", 0.0), hf_metrics.get("macro_doc_category_f1", 0.0)],
        "HF Embedding Doc Category Accuracy v0.4",
        "Accuracy",
    )
    save_bar(
        FIGURES_DIR / "router_vs_hf_agreement_v0_4.png",
        ["hybrid router/HF"],
        [hybrid_hf_metrics.get("router_hf_agreement_rate", 0.0)],
        "Router vs HF Agreement v0.4",
        "Agreement",
    )
    save_bar(
        FIGURES_DIR / "hf_latency_comparison_v0_4.png",
        ["HF embedding", "hybrid+HF"],
        [hf_metrics.get("average_embedding_inference_latency_seconds", 0.0), hybrid_hf_metrics.get("average_latency_seconds", 0.0)],
        "HF Latency Comparison v0.4",
        "Seconds",
    )
    save_bar(
        FIGURES_DIR / "hf_full_vs_no_leak_comparison_v0_4.png",
        ["raw_diff_plus_docs F1", "full_current F1", "raw_diff_plus_docs scenario", "full_current scenario"],
        [
            hf_metrics.get("docs_update_required_f1", 0.0),
            full_hf_metrics.get("docs_update_required_f1", 0.0),
            hf_metrics.get("positive_scenario_type_accuracy", 0.0),
            full_hf_metrics.get("positive_scenario_type_accuracy", 0.0),
        ],
        "HF Full Current vs No-Leak Comparison v0.4",
        "Score",
    )
    write_hf_input_ablation_figures()
    write_hf_stress_figure()
    write_negative_subtype_figures()
    write_staged_vs_flat_figure()
    write_hf_confusion_figure()
    save_bar(
        FIGURES_DIR / "invalid_source_target_file_count_v0_4.png",
        ["invalid source targets", "corrected targets"],
        [hybrid_metrics.get("invalid_source_file_target_count", 0), hybrid_metrics.get("corrected_target_doc_file_count", 0)],
        "Invalid Source Target File Count v0.4",
        "Count",
    )
    save_bar(
        FIGURES_DIR / "cpu_latency_comparison_v0_4.png",
        ["hybrid avg", "hybrid p50", "hybrid p95"],
        [
            hybrid_metrics.get("average_latency_seconds", 0.0),
            hybrid_metrics.get("p50_latency_seconds", 0.0),
            hybrid_metrics.get("p95_latency_seconds", 0.0),
        ],
        "CPU Latency Comparison v0.4",
        "Seconds",
    )
    all_records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    positive_records = [record for record in all_records if record["docs_update_required"]]
    negative_records = [record for record in all_records if not record["docs_update_required"]]
    positive_categories = Counter(record["doc_category"] for record in positive_records)
    positive_scenarios = Counter(record["scenario_type"] for record in positive_records)
    negative_scenarios = Counter(record["scenario_type"] for record in negative_records)
    save_bar(
        FIGURES_DIR / "positive_doc_category_distribution_v0_4.png",
        list(positive_categories),
        list(positive_categories.values()),
        "Positive Documentation Category Distribution v0.4",
    )
    save_bar(
        FIGURES_DIR / "positive_scenario_distribution_v0_4.png",
        list(positive_scenarios),
        list(positive_scenarios.values()),
        "Positive Scenario Distribution v0.4",
    )
    save_bar(
        FIGURES_DIR / "negative_scenario_distribution_v0_4.png",
        list(negative_scenarios),
        list(negative_scenarios.values()),
        "Negative Scenario Distribution v0.4",
    )


def read_metrics_report(path: Path) -> dict:
    metrics = {}
    if not path.exists():
        return metrics
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| `"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 2:
                key = parts[0].strip("`")
                try:
                    metrics[key] = float(parts[1])
                except ValueError:
                    metrics[key] = parts[1]
    return metrics


def write_hf_confusion_figure() -> None:
    pred_path = DATA_DIR / "hf_embedding_predictions_v0_4_raw_diff_plus_docs_validation.jsonl"
    if not pred_path.exists():
        save_confusion_matrix(FIGURES_DIR / "hf_embedding_confusion_scenarios_v0_4.png", [[0]], ["not run"], "HF Embedding Scenario Confusion v0.4")
        save_confusion_matrix(FIGURES_DIR / "hf_positive_scenario_confusion_v0_4.png", [[0]], ["not run"], "HF Positive Scenario Confusion v0.4")
        save_confusion_matrix(FIGURES_DIR / "hf_negative_scenario_confusion_v0_4.png", [[0]], ["not run"], "HF Negative Scenario Confusion v0.4")
        save_confusion_matrix(FIGURES_DIR / "hf_negative_reason_group_confusion_v0_4.png", [[0]], ["not run"], "HF Negative Reason Group Confusion v0.4")
        save_horizontal_bar(FIGURES_DIR / "hf_top_scenario_confusions_v0_4.png", ["not run"], [0], "HF Top Scenario Confusions v0.4")
        return
    records = {row["id"]: row for row in read_jsonl(DATA_DIR / "hf_v0_4" / "raw_diff_plus_docs" / "validation.jsonl")}
    predictions = read_jsonl(pred_path)
    write_split_scenario_confusions(records, predictions)
    write_negative_group_confusion(records, predictions)
    write_top_scenario_confusions(records, predictions)
    errors = [pred for pred in predictions if records.get(pred["record_id"], {}).get("scenario_type_label") != pred["scenario_type"]]
    if not errors:
        save_bar(FIGURES_DIR / "hf_embedding_confusion_scenarios_v0_4.png", ["scenario errors"], [0], "HF Embedding Scenario Confusion v0.4", "Errors")
        return
    top = [name for name, _count in Counter(row["scenario_type_label"] for row in records.values()).most_common(12)]
    labels = sorted(set(top + ["other"]))
    index = {label: i for i, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for pred in predictions:
        row = records.get(pred["record_id"])
        if not row:
            continue
        gold = row["scenario_type_label"] if row["scenario_type_label"] in top else "other"
        got = pred["scenario_type"] if pred["scenario_type"] in top else "other"
        matrix[index[gold]][index[got]] += 1
    save_confusion_matrix(FIGURES_DIR / "hf_embedding_confusion_scenarios_v0_4.png", matrix, labels, "HF Embedding Scenario Confusion v0.4")
    (FIGURES_DIR / "hf_embedding_scenario_confusion_all_with_other_v0_4.png").write_bytes((FIGURES_DIR / "hf_embedding_confusion_scenarios_v0_4.png").read_bytes())


NEGATIVE_REASON_GROUPS = {
    "no_behavior_change_refactor": {
        "internal_variable_rename_no_behavior_change",
        "private_helper_refactor_no_flow_change",
        "helper_extraction_no_behavior_change",
        "internal_performance_refactor_no_documented_behavior_change",
        "type_alias_rename_no_contract_change",
    },
    "no_contract_change_textual": {
        "formatting_only_in_docs_or_code",
        "comments_reworded_no_contract_change",
        "log_message_change_no_user_visible_behavior",
    },
    "test_only_no_product_behavior": {"test_assertion_refactor_no_behavior_change"},
    "dependency_or_config_no_doc_impact": {"dev_dependency_patch_no_command_change", "config_refactor_no_new_env_var"},
    "docs_already_consistent": {"docs_already_updated"},
    "route_internal_no_contract_change": {"route_implementation_refactor_no_contract_change"},
}
NEGATIVE_SCENARIO_TO_GROUP = {scenario: group for group, scenarios in NEGATIVE_REASON_GROUPS.items() for scenario in scenarios}


def negative_reason_group(label: str) -> str:
    return NEGATIVE_SCENARIO_TO_GROUP.get(label, "other_negative")


def normalized_matrix(labels: list[str], pairs: list[tuple[str, str]]) -> list[list[float]]:
    counts = [[0 for _ in labels] for _ in labels]
    idx = {label: i for i, label in enumerate(labels)}
    for gold, pred in pairs:
        if gold in idx and pred in idx:
            counts[idx[gold]][idx[pred]] += 1
    matrix = []
    for row in counts:
        total = sum(row)
        matrix.append([value / total if total else 0.0 for value in row])
    return matrix


def write_split_scenario_confusions(records: dict[str, dict], predictions: list[dict]) -> None:
    positive_pairs = []
    negative_pairs = []
    for pred in predictions:
        row = records.get(pred["record_id"])
        if not row:
            continue
        pair = (row["scenario_type_label"], pred["scenario_type"])
        if row["docs_update_required_label"] == "true":
            positive_pairs.append(pair)
        else:
            negative_pairs.append(pair)
    pos_labels = sorted({gold for gold, _pred in positive_pairs} | {pred for _gold, pred in positive_pairs})
    neg_labels = sorted({gold for gold, _pred in negative_pairs} | {pred for _gold, pred in negative_pairs})
    save_float_confusion_matrix(FIGURES_DIR / "hf_positive_scenario_confusion_v0_4.png", normalized_matrix(pos_labels, positive_pairs), pos_labels, "HF Positive Scenario Confusion v0.4")
    save_float_confusion_matrix(FIGURES_DIR / "hf_negative_scenario_confusion_v0_4.png", normalized_matrix(neg_labels, negative_pairs), neg_labels, "HF Negative Scenario Confusion v0.4")


def write_negative_group_confusion(records: dict[str, dict], predictions: list[dict]) -> None:
    pairs = []
    for pred in predictions:
        row = records.get(pred["record_id"])
        if row and row["docs_update_required_label"] == "false":
            pairs.append((negative_reason_group(row["scenario_type_label"]), negative_reason_group(pred["scenario_type"])))
    labels = sorted({gold for gold, _pred in pairs} | {pred for _gold, pred in pairs})
    save_float_confusion_matrix(FIGURES_DIR / "hf_negative_reason_group_confusion_v0_4.png", normalized_matrix(labels, pairs), labels, "HF Negative Reason Group Confusion v0.4")


def write_top_scenario_confusions(records: dict[str, dict], predictions: list[dict]) -> None:
    confusions = Counter()
    support = Counter()
    for pred in predictions:
        row = records.get(pred["record_id"])
        if not row:
            continue
        gold = row["scenario_type_label"]
        got = pred["scenario_type"]
        support[gold] += 1
        if gold != got:
            confusions[(gold, got)] += 1
    if not confusions:
        save_horizontal_bar(FIGURES_DIR / "hf_top_scenario_confusions_v0_4.png", ["no off-diagonal errors"], [0], "HF Top Scenario Confusions v0.4")
        return
    labels = []
    values = []
    for (gold, got), count in confusions.most_common(20):
        labels.append(f"{gold} -> {got} ({count}, {count / max(1, support[gold]):.1%})")
        values.append(count)
    save_horizontal_bar(FIGURES_DIR / "hf_top_scenario_confusions_v0_4.png", labels, values, "HF Top Scenario Confusions v0.4", "Count")


def ablation_metrics_by_mode() -> dict[str, dict]:
    path = REPORTS_DIR / "hf_input_ablation_v0_4.md"
    if not path.exists():
        return {}
    results: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `") or "validation" not in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 15:
            continue
        mode = parts[0].strip("`")
        results[mode] = {
            "f1": float(parts[4]),
            "doc_category": float(parts[7]),
            "scenario": float(parts[9]),
            "latency": float(parts[13]),
        }
    return results


def write_hf_input_ablation_figures() -> None:
    results = ablation_metrics_by_mode()
    if not results:
        save_bar(FIGURES_DIR / "hf_input_ablation_binary_f1_v0_4.png", ["not run"], [0], "HF Input Ablation Binary F1 v0.4", "F1")
        save_bar(FIGURES_DIR / "hf_input_ablation_scenario_accuracy_v0_4.png", ["not run"], [0], "HF Input Ablation Scenario Accuracy v0.4", "Accuracy")
        save_bar(FIGURES_DIR / "hf_input_ablation_doc_category_accuracy_v0_4.png", ["not run"], [0], "HF Input Ablation Doc Category Accuracy v0.4", "Accuracy")
        return
    modes = list(results)
    save_bar(FIGURES_DIR / "hf_input_ablation_binary_f1_v0_4.png", modes, [results[m]["f1"] for m in modes], "HF Input Ablation Binary F1 v0.4", "F1")
    save_bar(FIGURES_DIR / "hf_input_ablation_scenario_accuracy_v0_4.png", modes, [results[m]["scenario"] for m in modes], "HF Input Ablation Scenario Accuracy v0.4", "Accuracy")
    save_bar(FIGURES_DIR / "hf_input_ablation_doc_category_accuracy_v0_4.png", modes, [results[m]["doc_category"] for m in modes], "HF Input Ablation Doc Category Accuracy v0.4", "Accuracy")


def write_hf_stress_figure() -> None:
    metrics = read_metrics_report(REPORTS_DIR / "hf_stress_test_v0_4.md")
    save_bar(
        FIGURES_DIR / "hf_stress_test_metrics_v0_4.png",
        ["F1", "doc category", "target file", "scenario", "negative acc."],
        [
            metrics.get("docs_update_required_f1", 0.0),
            metrics.get("positive_doc_category_accuracy", 0.0),
            metrics.get("positive_target_doc_file_accuracy", 0.0),
            metrics.get("positive_scenario_type_accuracy", 0.0),
            metrics.get("negative_classification_accuracy", 0.0),
        ],
        "HF Stress Test Metrics v0.4",
        "Score",
    )


def read_accuracy_table(path: Path, section_title: str) -> dict[str, float]:
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    values = {}
    for line in lines:
        if line.startswith("## "):
            in_section = line.strip("# ").strip() == section_title
            continue
        if in_section and line.startswith("| `"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 4:
                try:
                    values[parts[0].strip("`")] = float(parts[3])
                except ValueError:
                    pass
    return values


def write_negative_subtype_figures() -> None:
    path = REPORTS_DIR / "hf_negative_subtype_error_analysis_v0_4.md"
    subtype = read_accuracy_table(path, "Negative Scenario Subtype Accuracy")
    groups = read_accuracy_table(path, "Negative Reason Group Accuracy")
    if subtype:
        save_horizontal_bar(FIGURES_DIR / "hf_negative_subtype_accuracy_v0_4.png", list(subtype), list(subtype.values()), "HF Negative Subtype Accuracy v0.4", "Accuracy")
    else:
        save_horizontal_bar(FIGURES_DIR / "hf_negative_subtype_accuracy_v0_4.png", ["not run"], [0], "HF Negative Subtype Accuracy v0.4", "Accuracy")
    if groups:
        save_horizontal_bar(FIGURES_DIR / "hf_negative_reason_group_accuracy_v0_4.png", list(groups), list(groups.values()), "HF Negative Reason Group Accuracy v0.4", "Accuracy")
    else:
        save_horizontal_bar(FIGURES_DIR / "hf_negative_reason_group_accuracy_v0_4.png", ["not run"], [0], "HF Negative Reason Group Accuracy v0.4", "Accuracy")


def write_staged_vs_flat_figure() -> None:
    path = REPORTS_DIR / "hf_staged_vs_flat_comparison_v0_4.md"
    if not path.exists():
        save_bar(FIGURES_DIR / "hf_staged_vs_flat_metrics_v0_4.png", ["flat", "staged"], [0, 0], "HF Staged vs Flat Metrics v0.4", "Score")
        return
    labels = []
    values = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 6 or parts[1] == "not run":
            continue
        name = parts[0].strip("`")
        labels.extend([f"{name} F1", f"{name} neg scenario", f"{name} neg group"])
        values.extend([float(parts[1]), float(parts[3]), float(parts[4])])
    if not values:
        labels, values = ["flat", "staged"], [0, 0]
    save_bar(FIGURES_DIR / "hf_staged_vs_flat_metrics_v0_4.png", labels, values, "HF Staged vs Flat Metrics v0.4", "Score")


if __name__ == "__main__":
    raise SystemExit(main())
