from __future__ import annotations

import json
import random
import re
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from docguard_hf_classifier.dataset_export import DATA_DIR, HF_DATA_DIR, export, mode_dir, read_jsonl
from docguard_hf_classifier.embedding_classifier import (
    compute_metrics,
    evaluate as evaluate_embeddings,
    load_model,
    negative_reason_group,
    predict_rows,
    prediction_path,
    train as train_embeddings,
    write_report,
)
from docguard_hf_classifier.text_builder import DEFAULT_INPUT_MODE, INPUT_MODES
from docguard_hybrid.doc_router import route

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


def write_error_analysis(split: str = "validation", input_mode: str = DEFAULT_INPUT_MODE) -> None:
    metrics, predictions = evaluate_embeddings(split, input_mode)
    rows = read_jsonl(mode_dir(input_mode) / f"{split}.jsonl")
    pred_by_id = {prediction["record_id"]: prediction for prediction in predictions}
    scenario_confusions = Counter()
    category_confusions = Counter()
    hf_router_disagree = []
    hf_correct_router_wrong = []
    router_correct_hf_wrong = []
    for row in rows:
        pred = pred_by_id[row["id"]]
        routed = route(row)
        router_category = routed["candidate_doc_categories"][0]
        router_scenario = routed["candidate_scenario_types"][0]
        if pred["scenario_type"] != row["scenario_type_label"]:
            scenario_confusions[(row["scenario_type_label"], pred["scenario_type"])] += 1
        if pred["doc_category"] != row["doc_category_label"]:
            category_confusions[(row["doc_category_label"], pred["doc_category"])] += 1
        hf_correct = pred["doc_category"] == row["doc_category_label"] and pred["scenario_type"] == row["scenario_type_label"]
        router_correct = router_category == row["doc_category_label"] and router_scenario == row["scenario_type_label"]
        if pred["doc_category"] != router_category or pred["scenario_type"] != router_scenario:
            hf_router_disagree.append(row["id"])
        if hf_correct and not router_correct:
            hf_correct_router_wrong.append(row["id"])
        if router_correct and not hf_correct:
            router_correct_hf_wrong.append(row["id"])
    lines = [
        "# HF Embedding Error Analysis v0.4",
        "",
        f"Split: `{split}`",
        f"Input mode: `{input_mode}`",
        f"F1: `{metrics['docs_update_required_f1']:.4f}`",
        "",
        "## Most Confused Scenario Pairs",
        "",
    ]
    for (gold, got), count in scenario_confusions.most_common(20):
        lines.append(f"- `{gold}` -> `{got}`: {count}")
    lines.extend(["", "## Most Confused Doc Categories", ""])
    for (gold, got), count in category_confusions.most_common(20):
        lines.append(f"- `{gold}` -> `{got}`: {count}")
    lines.extend([
        "",
        "## HF Disagrees With Router",
        "",
        ", ".join(hf_router_disagree[:20]) or "None",
        "",
        "## HF Correct, Router Wrong",
        "",
        ", ".join(hf_correct_router_wrong[:20]) or "None",
        "",
        "## Router Correct, HF Wrong",
        "",
        ", ".join(router_correct_hf_wrong[:20]) or "None",
    ])
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / f"hf_embedding_error_analysis_v0_4_{input_mode}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if input_mode == "full_current":
        (REPORTS_DIR / "hf_embedding_error_analysis_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


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


def format_metric(value: object) -> str:
    return f"{value:.4f}" if isinstance(value, float) else str(value)


def metric_row(mode: str, split: str, metrics: dict) -> str:
    keys = [
        "docs_update_required_precision",
        "docs_update_required_recall",
        "docs_update_required_f1",
        "false_positive_count",
        "false_negative_count",
        "positive_doc_category_accuracy",
        "positive_target_doc_file_accuracy",
        "positive_scenario_type_accuracy",
        "negative_classification_accuracy",
        "macro_scenario_f1",
        "macro_doc_category_f1",
        "average_embedding_inference_latency_seconds",
    ]
    values = " | ".join(format_metric(metrics.get(key, 0.0)) for key in keys)
    return f"| `{mode}` | `{split}` | {values} | {metrics.get('model_name', '')} | {metrics.get('classifier_type', '')} |"


def ablate_inputs(version: str = "v0_4", model: str = "sentence-transformers/all-MiniLM-L6-v2") -> dict:
    results: dict[str, dict] = {}
    for mode in INPUT_MODES:
        export(version, mode)
        train_embeddings(version=version, model_name=model, input_mode=mode)
        results[mode] = {}
        for split in ["validation", "test"]:
            metrics, _predictions = evaluate_embeddings(split, mode)
            results[mode][split] = metrics
    lines = [
        "# HF Input Ablation v0.4",
        "",
        "| Input mode | Split | Precision | Recall | F1 | FP | FN | Pos. doc category | Pos. target file | Pos. scenario | Negative acc. | Macro scenario F1 | Macro doc category F1 | Avg latency | Model | Classifier |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for mode in INPUT_MODES:
        for split in ["validation", "test"]:
            lines.append(metric_row(mode, split, results[mode][split]))
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "hf_input_ablation_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return results


def write_leakage_risk_report() -> None:
    lines = [
        "# HF Leakage Risk Analysis v0.4",
        "",
        "`full_current` is useful as an assisted upper-bound setting, but it can inflate performance because it combines raw diffs with derived summaries and rule-derived signal names.",
        "",
        "Change summaries and change-intent summaries can leak label semantics because generated phrases often name the scenario or documentation category directly. Extracted signals are useful engineering features, but they are partially produced by deterministic rules, so they should not be treated as a purely learned no-leak representation.",
        "",
        "Recommended thesis reporting:",
        "",
        "- Primary fair HF result: `raw_diff_plus_docs`",
        "- Assisted HF result: `raw_diff_plus_signals`",
        "- Upper-bound assisted result: `full_current`",
        "",
        "`raw_diff_only` is the strictest setting. `raw_diff_plus_docs` is the recommended default because the model sees the code change and the existing documentation context without gold-like summaries or handcrafted scenario signals.",
    ]
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "hf_leakage_risk_analysis_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def stress_text(text: str, seed: int) -> str:
    rng = random.Random(seed)
    replacements = {
        "env": "CONFIG_TOKEN",
        "environment": "configuration",
        "job": "background task",
        "endpoint": "route",
        "dto": "data object",
        "review": "case",
        "ticket": "item",
        "project": "service",
        "module": "component",
    }
    stressed = text
    for old, new in replacements.items():
        stressed = re.sub(old, new, stressed, flags=re.IGNORECASE)
    lines = stressed.splitlines()
    nonessential = [line for line in lines if line.strip() and not line.startswith("changed_files:")]
    rng.shuffle(nonessential)
    kept = [line for line in lines if line.startswith("changed_files:")]
    noisy = kept + nonessential
    noisy.append("// harmless formatting note")
    return "\n".join(noisy)


def stress_test(version: str = "v0_4", input_mode: str = DEFAULT_INPUT_MODE) -> dict:
    model = load_model(input_mode)
    rows = read_jsonl(mode_dir(input_mode) / "test.jsonl")
    stressed = []
    for index, row in enumerate(rows):
        copy = dict(row)
        copy["input_text"] = stress_text(row["input_text"], index)
        stressed.append(copy)
    predictions, latency = predict_rows(stressed, model)
    metrics = compute_metrics(stressed, predictions, latency, model)
    write_report(REPORTS_DIR / "hf_stress_test_v0_4.md", f"HF Stress Test v0.4 {input_mode}", metrics)
    lines = (REPORTS_DIR / "hf_stress_test_v0_4.md").read_text(encoding="utf-8").splitlines()
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Binary robustness is measured by precision, recall, F1, false positives, and false negatives. Fine-grained robustness is measured by positive target/scenario accuracy, negative subtype accuracy, negative reason group accuracy, and macro scenario F1.",
        "",
        "The expected pattern is that binary documentation-update detection remains more robust than fine-grained target or subtype prediction. Fine-grained labels are more sensitive to lexical and template changes.",
    ])
    (REPORTS_DIR / "hf_stress_test_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return metrics


def stable_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def write_split_leakage_check(input_mode: str = DEFAULT_INPUT_MODE) -> dict:
    splits = {split: read_jsonl(mode_dir(input_mode) / f"{split}.jsonl") for split in ["train", "validation", "test"]}
    project_sets = {split: {row["project_id"] for row in rows} for split, rows in splits.items()}
    project_overlaps = {
        "train_validation": sorted(project_sets["train"] & project_sets["validation"]),
        "train_test": sorted(project_sets["train"] & project_sets["test"]),
        "validation_test": sorted(project_sets["validation"] & project_sets["test"]),
    }
    input_hashes = {split: Counter(stable_hash(row["input_text"]) for row in rows) for split, rows in splits.items()}
    diff_hashes = {split: Counter(stable_hash(row.get("code_diff") or "") for row in rows) for split, rows in splits.items()}
    near_duplicates = []
    repeated_diffs = []
    for left, right in [("train", "validation"), ("train", "test"), ("validation", "test")]:
        near_duplicates.extend((left, right, h) for h in sorted(set(input_hashes[left]) & set(input_hashes[right]))[:20])
        repeated_diffs.extend((left, right, h) for h in sorted(set(diff_hashes[left]) & set(diff_hashes[right]))[:20])
    lines = [
        "# Dataset Split Leakage Check v0.4",
        "",
        f"Input mode: `{input_mode}`",
        "",
        "## Project ID Overlap",
        "",
    ]
    for name, values in project_overlaps.items():
        lines.append(f"- `{name}`: {len(values)} overlap(s)" + (f" -> {', '.join(values[:10])}" if values else ""))
    lines.extend(["", "## Near-Duplicate Input Text Hashes Across Splits", ""])
    lines.extend([f"- `{left}` / `{right}`: `{h}`" for left, right, h in near_duplicates] or ["None found."])
    lines.extend(["", "## Repeated Code Diff Template Hashes Across Splits", ""])
    lines.extend([f"- `{left}` / `{right}`: `{h}`" for left, right, h in repeated_diffs] or ["None found."])
    lines.extend(["", "## Scenario Distribution Per Split", ""])
    for split, rows in splits.items():
        counts = Counter(row["scenario_type_label"] for row in rows)
        lines.append(f"### {split}")
        lines.extend(f"- `{label}`: {count}" for label, count in sorted(counts.items()))
    lines.extend(["", "## Project Distribution Per Split", ""])
    for split, rows in splits.items():
        counts = Counter(row["project_id"] for row in rows)
        lines.append(f"### {split}")
        lines.extend(f"- `{label}`: {count}" for label, count in sorted(counts.items()))
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "dataset_split_leakage_check_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"project_overlaps": project_overlaps, "near_duplicate_count": len(near_duplicates), "repeated_diff_hash_count": len(repeated_diffs)}


def read_predictions(split: str = "test", input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> list[dict]:
    path = prediction_path(split, input_mode, classifier_architecture)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_negative_subtype_error_analysis(input_mode: str = DEFAULT_INPUT_MODE, split: str = "test", classifier_architecture: str = "flat") -> dict:
    rows = read_jsonl(mode_dir(input_mode) / f"{split}.jsonl")
    predictions = read_predictions(split, input_mode, classifier_architecture)
    pred_by_id = {prediction["record_id"]: prediction for prediction in predictions}
    subtype_counts: dict[str, Counter] = defaultdict(Counter)
    group_counts: dict[str, Counter] = defaultdict(Counter)
    confusions = Counter()
    examples = []
    for row in rows:
        if row["docs_update_required_label"] == "true":
            continue
        pred = pred_by_id.get(row["id"])
        if not pred:
            continue
        gold_subtype = row["scenario_type_label"]
        pred_subtype = pred["scenario_type"]
        gold_group = negative_reason_group(gold_subtype)
        pred_group = negative_reason_group(pred_subtype)
        subtype_counts[gold_subtype]["total"] += 1
        subtype_counts[gold_subtype]["correct"] += int(pred_subtype == gold_subtype)
        group_counts[gold_group]["total"] += 1
        group_counts[gold_group]["correct"] += int(pred_group == gold_group)
        if pred_subtype != gold_subtype:
            confusions[(gold_subtype, pred_subtype)] += 1
            if not pred["docs_update_required"] and len(examples) < 12:
                examples.append((row["id"], gold_subtype, pred_subtype, gold_group, pred_group))
    lines = [
        "# HF Negative Subtype Error Analysis v0.4",
        "",
        f"Input mode: `{input_mode}`",
        f"Split: `{split}`",
        f"Classifier architecture: `{classifier_architecture}`",
        "",
        "Negative subtype errors are less severe than false positives or false negatives when binary classification is correct, because the system still correctly predicts that no documentation update is required. They are diagnostic labels for analysis, not patch-generation targets.",
        "",
        "## Negative Scenario Subtype Accuracy",
        "",
        "| Subtype | Support | Correct | Accuracy |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, counts in sorted(subtype_counts.items()):
        total = counts["total"]
        correct = counts["correct"]
        lines.append(f"| `{label}` | {total} | {correct} | {correct / total if total else 0.0:.4f} |")
    lines.extend(["", "## Negative Reason Group Accuracy", "", "| Group | Support | Correct | Accuracy |", "| --- | ---: | ---: | ---: |"])
    for label, counts in sorted(group_counts.items()):
        total = counts["total"]
        correct = counts["correct"]
        lines.append(f"| `{label}` | {total} | {correct} | {correct / total if total else 0.0:.4f} |")
    lines.extend(["", "## Top Confused Negative Subtype Pairs", ""])
    for (gold, pred), count in confusions.most_common(20):
        gold_total = subtype_counts[gold]["total"] or 1
        lines.append(f"- `{gold}` -> `{pred}`: {count} ({count / gold_total:.1%} of `{gold}`)")
    if not confusions:
        lines.append("None.")
    lines.extend(["", "## Binary Correct, Subtype Wrong Examples", "", "| Record | Gold subtype | Predicted subtype | Gold group | Predicted group |", "| --- | --- | --- | --- | --- |"])
    for record_id, gold, pred, gold_group, pred_group in examples:
        lines.append(f"| `{record_id}` | `{gold}` | `{pred}` | `{gold_group}` | `{pred_group}` |")
    if not examples:
        lines.append("| None |  |  |  |  |")
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "hf_negative_subtype_error_analysis_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "negative_subtypes": len(subtype_counts),
        "negative_groups": len(group_counts),
        "confusion_pairs": len(confusions),
    }


def refresh_embedding_report_from_predictions(input_mode: str = DEFAULT_INPUT_MODE, split: str = "test", classifier_architecture: str = "flat") -> dict:
    rows = read_jsonl(mode_dir(input_mode) / f"{split}.jsonl")
    predictions = read_predictions(split, input_mode, classifier_architecture)
    if not predictions:
        return {"refreshed": False, "reason": "prediction file missing"}
    latency_values = [float(pred.get("latency_seconds") or 0.0) for pred in predictions]
    fake_model = {
        "model_name": predictions[0].get("model_name", "unknown"),
        "input_mode": input_mode,
        "classifier_architecture": classifier_architecture,
        "classifier_type": predictions[0].get("classifier_type", "unknown"),
    }
    metrics = compute_metrics(rows, predictions, sum(latency_values) / len(latency_values) if latency_values else 0.0, fake_model)
    suffix = "" if classifier_architecture == "flat" else f"_{classifier_architecture}"
    write_report(REPORTS_DIR / f"hf_embedding_evaluation_v0_4_{input_mode}_{split}{suffix}.md", f"HF Embedding Evaluation v0.4 {input_mode} {split} {classifier_architecture}", metrics)
    return {"refreshed": True, "records": len(rows), "split": split, "input_mode": input_mode, "classifier_architecture": classifier_architecture}


def write_staged_vs_flat_comparison(input_mode: str = DEFAULT_INPUT_MODE, split: str = "test") -> dict:
    flat = read_metrics_report(REPORTS_DIR / f"hf_embedding_evaluation_v0_4_{input_mode}_{split}.md")
    staged = read_metrics_report(REPORTS_DIR / f"hf_embedding_evaluation_v0_4_{input_mode}_{split}_staged.md")
    lines = [
        "# HF Staged vs Flat Comparison v0.4",
        "",
        f"Input mode: `{input_mode}`",
        f"Split: `{split}`",
        "",
        "| Architecture | F1 | Positive scenario | Negative scenario | Negative reason group | Macro scenario F1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, metrics in [("flat", flat), ("staged", staged)]:
        if metrics:
            lines.append(
                f"| `{name}` | {float(metrics.get('docs_update_required_f1', 0.0)):.4f} | "
                f"{float(metrics.get('positive_scenario_type_accuracy', 0.0)):.4f} | "
                f"{float(metrics.get('negative_scenario_type_accuracy', 0.0)):.4f} | "
                f"{float(metrics.get('negative_reason_group_accuracy', 0.0)):.4f} | "
                f"{float(metrics.get('macro_scenario_f1', 0.0)):.4f} |"
            )
        else:
            lines.append(f"| `{name}` | not run | not run | not run | not run | not run |")
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "hf_staged_vs_flat_comparison_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"flat_available": bool(flat), "staged_available": bool(staged)}
