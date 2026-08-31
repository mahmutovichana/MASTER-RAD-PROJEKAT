from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "experiments/consolidated_enriched_training_v1"
V2 = ROOT / "experiments/consolidated_enriched_training_v2"
DATASET = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    dataset = read(DATASET / "manifest.json")
    split = read(V2 / "gold/human_gold_manifest.json")
    b1 = read(V1 / "binary_v4/training_summary.json")["best_metrics"]["development_validation"]
    b2_summary = read(V2 / "binary_v4/training_summary.json")
    b2 = b2_summary["best_metrics"]["development_validation"]
    c1 = read(V1 / "category_v8/training_summary.json")["best_metrics"]["development_validation"]
    c2_summary = read(V2 / "category_v8/training_summary.json")
    c2 = c2_summary["best_metrics"]["development_validation"]

    comparison = {
        "dataset": dataset,
        "split": split,
        "binary": {
            "v1": b1,
            "v2": b2,
            "delta": {name: b2[name] - b1[name] for name in ["accuracy", "precision", "recall", "f1", "balanced_accuracy", "mcc", "roc_auc"]},
        },
        "category": {
            "v1": c1,
            "v2": c2,
            "delta": {name: c2[name] - c1[name] for name in ["accuracy", "macro_f1", "weighted_f1", "balanced_accuracy"]},
        },
    }
    (V2 / "comparison_metrics.json").write_text(
        json.dumps(comparison, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    cm = b2["confusion_matrix"]
    lines = [
        "# Consolidated enriched training v2 — results",
        "",
        "## Dataset",
        "",
        f"- Total rows: **{dataset['row_count']:,}**",
        f"- Positive: **{dataset['positive_count']:,} ({dataset['positive_rate']:.2%})**",
        f"- Negative: **{dataset['negative_count']:,}**",
        f"- Controlled train-only augmentation: **{dataset['controlled_augmentation_rows']:,}**",
        "- Additional reviewed natural positives: **54**",
        f"- Validation: **{dataset['validation']}**",
        "",
        "## Leakage-safe split",
        "",
        f"- Development train: **{split['partition_row_counts']['development_train']:,}**",
        f"- Development validation: **{split['partition_row_counts']['development_validation']:,}**",
        f"- Sealed confirmation: **{split['partition_row_counts']['confirmation']:,}**",
        "- Controlled/new augmentation is development-train-only.",
        "- Validation and confirmation case membership is unchanged from v1.",
        "- Repository overlap across splits: **0**",
        "",
        "## Binary V4 — unchanged natural validation",
        "",
        f"- Selected model: `{b2_summary['selected_model']}`; threshold: **{b2_summary['selected_threshold']:.2f}**",
        f"- Accuracy: **{b2['accuracy']:.4f}**",
        f"- Precision: **{b2['precision']:.4f}**",
        f"- Recall: **{b2['recall']:.4f}**",
        f"- F1: **{b2['f1']:.4f}** (v1 {b1['f1']:.4f}, delta {b2['f1'] - b1['f1']:+.4f})",
        f"- Balanced accuracy: **{b2['balanced_accuracy']:.4f}**",
        f"- MCC: **{b2['mcc']:.4f}** (v1 {b1['mcc']:.4f}, delta {b2['mcc'] - b1['mcc']:+.4f})",
        f"- ROC-AUC: **{b2['roc_auc']:.4f}** (v1 {b1['roc_auc']:.4f}, delta {b2['roc_auc'] - b1['roc_auc']:+.4f})",
        f"- Confusion matrix: TN **{cm['tn']:,}**, FP **{cm['fp']:,}**, FN **{cm['fn']:,}**, TP **{cm['tp']:,}**",
        "",
        "## Category V8 — unchanged natural validation",
        "",
        f"- Selected model: `{c2_summary['selected_model']}`",
        f"- Accuracy: **{c2['accuracy']:.4f}**",
        f"- Macro-F1: **{c2['macro_f1']:.4f}** (v1 {c1['macro_f1']:.4f}, delta {c2['macro_f1'] - c1['macro_f1']:+.4f})",
        f"- Weighted-F1: **{c2['weighted_f1']:.4f}**",
        f"- Balanced accuracy: **{c2['balanced_accuracy']:.4f}**",
        "",
    ]
    for category in ["api_reference", "configuration", "developer_setup", "model_contract"]:
        current = c2["per_class"][category]
        previous = c1["per_class"][category]
        lines.append(f"- `{category}` F1: **{current['f1']:.4f}** (v1 {previous['f1']:.4f}, delta {current['f1'] - previous['f1']:+.4f})")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The augmentation substantially improves training fit but does not materially improve natural repository-disjoint validation. Binary generalization is slightly worse; category macro-F1 is only marginally better, and developer_setup remains undetected. Controlled template volume should therefore not be treated as a substitute for diverse natural positive repositories.",
    ])
    (V2 / "RESULTS_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "ok", "summary": str(V2 / "RESULTS_SUMMARY.md")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
