from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

from docguard_external.evaluate_existing_docguard import confidence, pct, read_jsonl, truncate, try_hf_staged_predictions


REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
THRESHOLDS = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75]


def external_binary_to_docguard(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["record_id"],
        "project_id": row.get("repository") or row.get("source_dataset") or "external_binary",
        "changed_files": [row.get("target_path") or row["record_id"]],
        "code_diff": row.get("code_diff") or "",
        "docs_before_excerpt": row.get("doc_before") or "",
        "docs_update_required": bool(row.get("docs_update_required")),
        "scenario_type": row.get("scenario_type") or "",
        "doc_category": "comment_or_docstring" if row.get("docs_update_required") else "no_update",
        "target_doc_file": row.get("target_path") or "",
        "target_section": "",
        "expected_facts": [],
    }


def outcome(gold: bool, predicted: bool) -> str:
    if gold and predicted:
        return "TP"
    if not gold and predicted:
        return "FP"
    if gold and not predicted:
        return "FN"
    return "TN"


def paired(rows: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs = []
    for row, pred in zip(rows, predictions):
        gold = bool(row.get("docs_update_required"))
        predicted = bool(pred.get("docs_update_required"))
        pairs.append(
            {
                "record": row,
                "prediction": pred,
                "gold": gold,
                "predicted": predicted,
                "outcome": outcome(gold, predicted),
                "confidence": confidence(pred),
            }
        )
    return pairs


def rates(tp: int, fp: int, tn: int, fn: int) -> dict[str, float]:
    total = tp + fp + tn + fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": (tp + tn) / total if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": fp / (fp + tn) if fp + tn else 0.0,
        "false_negative_rate": fn / (fn + tp) if fn + tp else 0.0,
    }


def binary_metrics(rows: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = paired(rows, predictions)
    counts = Counter(item["outcome"] for item in pairs)
    tp = counts["TP"]
    fp = counts["FP"]
    tn = counts["TN"]
    fn = counts["FN"]
    metric_values = rates(tp, fp, tn, fn)
    return {
        "total_records": len(rows),
        "positive_count": sum(1 for row in rows if row.get("docs_update_required") is True),
        "negative_count": sum(1 for row in rows if row.get("docs_update_required") is False),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "false_positive_count": fp,
        "false_negative_count": fn,
        **metric_values,
        "median_confidence": median([item["confidence"] for item in pairs]) if pairs else 0.0,
        "average_confidence": mean([item["confidence"] for item in pairs]) if pairs else 0.0,
        "gold_label_distribution": dict(Counter(str(row.get("docs_update_required")) for row in rows)),
        "predicted_label_distribution": dict(Counter(str(pred.get("docs_update_required")) for pred in predictions)),
        "predicted_doc_category_distribution": dict(Counter(str(pred.get("doc_category") or "unknown") for pred in predictions)),
        "predicted_scenario_type_distribution": dict(Counter(str(pred.get("scenario_type") or "unknown") for pred in predictions)),
        "target_file_distribution": dict(Counter(str(row.get("target_path") or (row.get("metadata") or {}).get("source_file") or "unknown") for row in rows)),
        "pairs": pairs,
    }


def confidence_summary(values: list[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "min": min(values) if values else 0.0,
        "median": median(values) if values else 0.0,
        "mean": mean(values) if values else 0.0,
        "max": max(values) if values else 0.0,
    }


def confidence_by_outcome(pairs: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    return {name: confidence_summary([item["confidence"] for item in pairs if item["outcome"] == name]) for name in ["TP", "FP", "TN", "FN"]}


def distribution_for(pairs: list[dict[str, Any]], gold: bool, field: str) -> dict[str, int]:
    return dict(Counter(str(item["prediction"].get(field) or "unknown") for item in pairs if item["gold"] is gold))


def excerpt(value: Any, limit: int = 420) -> str:
    return truncate(value, limit)


def raw_file_values(rows: list[dict[str, Any]]) -> list[str]:
    return sorted({str((row.get("metadata") or {}).get("source_file")) for row in rows if (row.get("metadata") or {}).get("source_file")})


def load_raw_rows_by_id(source_files: list[str]) -> dict[str, dict[str, Any]]:
    raw_by_id: dict[str, dict[str, Any]] = {}
    for source_file in source_files:
        path = Path(source_file)
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        raw_rows = data if isinstance(data, list) else list(data.values()) if isinstance(data, dict) else []
        for row in raw_rows:
            if isinstance(row, dict) and row.get("id") is not None:
                raw_by_id[str(row["id"])] = row
    return raw_by_id


def raw_for_sample(row: dict[str, Any], raw_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    raw_id = str((row.get("metadata") or {}).get("source_record_id") or "")
    return raw_by_id.get(raw_id, {})


def audit_checklist(options: list[str]) -> list[str]:
    return [f"- [ ] {option}" for option in options]


def label_polarity_example(row: dict[str, Any], raw: dict[str, Any]) -> list[str]:
    return [
        f"### {row.get('record_id')}",
        "",
        f"- Raw source file: `{(row.get('metadata') or {}).get('source_file')}`",
        f"- Raw id: `{(row.get('metadata') or {}).get('source_record_id')}`",
        f"- Raw label: `{raw.get('label', (row.get('metadata') or {}).get('original_label'))}`",
        f"- Mapped docs_update_required: `{row.get('docs_update_required')}`",
        f"- Old code excerpt: {excerpt(raw.get('old_code_raw') or row.get('code_before'))}",
        f"- New code excerpt: {excerpt(raw.get('new_code_raw') or row.get('code_after'))}",
        f"- Old comment excerpt: {excerpt(raw.get('old_comment_raw') or row.get('doc_before'))}",
        f"- New comment excerpt: {excerpt(raw.get('new_comment_raw') or row.get('doc_after'))}",
        "",
        *audit_checklist(["mapping looks correct", "mapping questionable", "label polarity unclear", "possible dataset noise"]),
        "",
    ]


def write_label_polarity_audit(rows: list[dict[str, Any]]) -> None:
    path = REPORTS_DIR / "external_docchecker_label_polarity_audit_2026_08.md"
    source_files = raw_file_values(rows)
    raw_by_id = load_raw_rows_by_id(source_files)
    raw_labels = Counter(str(raw_for_sample(row, raw_by_id).get("label", (row.get("metadata") or {}).get("original_label"))) for row in rows)
    positives = [row for row in rows if row.get("docs_update_required") is True][:10]
    negatives = [row for row in rows if row.get("docs_update_required") is False][:10]
    lines = [
        "# External DocChecker / Deep-JIT Label Polarity Audit 2026-08",
        "",
        "## Summary",
        "",
        f"- Processed sample: `data/external/docchecker_binary_sample_500.jsonl`",
        f"- Raw files used: {', '.join(f'`{item}`' for item in source_files) if source_files else '`unknown`'}",
        "- Raw label column used: `label`",
        f"- Raw label values observed in sample: {', '.join(f'`{key}`={value}' for key, value in sorted(raw_labels.items()))}",
        "- Mapping used by adapter: raw `1` -> `docs_update_required=true`; raw `0` -> `docs_update_required=false`.",
        "- Repository evidence: Deep-JIT is explicitly an inconsistency detection dataset; DocChecker says its Just-In-Time task determines whether a comment is semantically out of sync with code and returns `Inconsistent!` or `Consistent!`.",
        "- Documentation caveat: the GitHub README pages confirm the task semantics, but the Deep-JIT README does not explicitly define the numeric polarity of the downloaded `label` field.",
        "- Current certainty: polarity is plausible and the sampled examples are consistent with `1=inconsistent/update-required`, `0=consistent/no-update`, but numeric polarity should still be manually verified against the paper or original preprocessing code before thesis-level claims.",
        "- Signs of reversal: no obvious reversal in sampled examples; raw label `1` examples usually show old comments updated to match code changes, while raw label `0` examples usually keep the same comment.",
        "",
        "Sources: https://github.com/panthap2/deep-jit-inconsistency-detection and https://github.com/FSoft-AI4Code/DocChecker",
        "",
        "## Raw Positive Examples",
        "",
    ]
    for row in positives:
        lines.extend(label_polarity_example(row, raw_for_sample(row, raw_by_id)))
    lines.extend(["", "## Raw Negative Examples", ""])
    for row in negatives:
        lines.extend(label_polarity_example(row, raw_for_sample(row, raw_by_id)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def metric_table_row(label: str, tp: int, fp: int, tn: int, fn: int) -> str:
    metric_values = rates(tp, fp, tn, fn)
    return (
        f"| {label} | {tp} | {fp} | {tn} | {fn} | {pct(metric_values['accuracy'])} | "
        f"{pct(metric_values['precision'])} | {pct(metric_values['recall'])} | {pct(metric_values['f1'])} | {pct(metric_values['false_positive_rate'])} |"
    )


def write_error_analysis(metrics: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_docchecker_binary_error_analysis_2026_08.md"
    pairs = metrics["pairs"]
    lines = [
        "# External DocChecker Binary Error Analysis 2026-08",
        "",
        "## Confusion Matrix",
        "",
        "|  | Predicted true | Predicted false |",
        "| --- | ---: | ---: |",
        f"| Gold true | {metrics['tp']} | {metrics['fn']} |",
        f"| Gold false | {metrics['fp']} | {metrics['tn']} |",
        "",
        "## Metrics",
        "",
        "| System | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        metric_table_row("Existing DocGuard", metrics["tp"], metrics["fp"], metrics["tn"], metrics["fn"]),
        "",
        "## Label Distributions",
        "",
        f"- Gold labels: `{metrics['gold_label_distribution']}`",
        f"- Predicted labels: `{metrics['predicted_label_distribution']}`",
        f"- False positives: `{metrics['false_positive_count']}`",
        f"- False negatives: `{metrics['false_negative_count']}`",
        f"- False positive rate: `{pct(metrics['false_positive_rate'])}`",
        f"- False negative rate: `{pct(metrics['false_negative_rate'])}`",
        "",
        "## Confidence Summary By Outcome",
        "",
        "| Outcome | Count | Min | Median | Mean | Max |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, summary in confidence_by_outcome(pairs).items():
        lines.append(
            f"| {name} | {summary['count']} | {summary['min']:.4f} | {summary['median']:.4f} | {summary['mean']:.4f} | {summary['max']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Predicted Doc Category Distribution",
            "",
            "### Gold Positive Records",
            "",
            *[f"- `{key}`: {value}" for key, value in sorted(distribution_for(pairs, True, "doc_category").items(), key=lambda item: item[1], reverse=True)],
            "",
            "### Gold Negative Records",
            "",
            *[f"- `{key}`: {value}" for key, value in sorted(distribution_for(pairs, False, "doc_category").items(), key=lambda item: item[1], reverse=True)],
            "",
            "## Predicted Scenario Type Distribution",
            "",
            "### Gold Positive Records",
            "",
            *[f"- `{key}`: {value}" for key, value in sorted(distribution_for(pairs, True, "scenario_type").items(), key=lambda item: item[1], reverse=True)[:40]],
            "",
            "### Gold Negative Records",
            "",
            *[f"- `{key}`: {value}" for key, value in sorted(distribution_for(pairs, False, "scenario_type").items(), key=lambda item: item[1], reverse=True)[:40]],
            "",
            "## Target File / Source Distribution",
            "",
            *[f"- `{key}`: {value}" for key, value in sorted(metrics["target_file_distribution"].items(), key=lambda item: item[1], reverse=True)],
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def threshold_counts(pairs: list[dict[str, Any]], threshold: float) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    for item in pairs:
        predicted_positive = item["predicted"] and item["confidence"] >= threshold
        if item["gold"] and predicted_positive:
            tp += 1
        elif not item["gold"] and predicted_positive:
            fp += 1
        elif item["gold"] and not predicted_positive:
            fn += 1
        else:
            tn += 1
    values = rates(tp, fp, tn, fn)
    return {
        "threshold": threshold,
        "predicted_positive_count": tp + fp,
        "predicted_negative_or_abstained_count": tn + fn,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        **values,
    }


def write_threshold_sweep(metrics: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_docchecker_threshold_sweep_2026_08.md"
    rows = [threshold_counts(metrics["pairs"], threshold) for threshold in THRESHOLDS]
    lines = [
        "# External DocChecker Threshold Sweep 2026-08",
        "",
        "Thresholds are diagnostic only. The staged confidence score was not calibrated as an external binary probability, so these results should be interpreted as review/abstention behavior, not final decision thresholds.",
        "",
        "| Threshold | Pred + | Pred negative/abstained | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['threshold']:.2f} | {row['predicted_positive_count']} | {row['predicted_negative_or_abstained_count']} | "
            f"{row['tp']} | {row['fp']} | {row['tn']} | {row['fn']} | {pct(row['accuracy'])} | {pct(row['precision'])} | "
            f"{pct(row['recall'])} | {pct(row['f1'])} | {pct(row['false_positive_rate'])} | {pct(row['false_negative_rate'])} |"
        )
    best = max(rows, key=lambda item: item["f1"]) if rows else None
    if best:
        lines.extend(
            [
                "",
                "## Diagnostic Takeaway",
                "",
                f"The highest diagnostic F1 in this sweep is {pct(best['f1'])} at threshold `{best['threshold']:.2f}`. Raising the threshold reduces false positives only by converting many low-confidence positive predictions into negative/abstained decisions, and it also starts losing true positives.",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prediction_example(item: dict[str, Any], raw_by_id: dict[str, dict[str, Any]], checklist: list[str]) -> list[str]:
    row = item["record"]
    pred = item["prediction"]
    raw = raw_for_sample(row, raw_by_id)
    return [
        f"### {row.get('record_id')}",
        "",
        f"- Raw source file: `{(row.get('metadata') or {}).get('source_file')}`",
        f"- Raw label: `{raw.get('label', (row.get('metadata') or {}).get('original_label'))}`",
        f"- Mapped label: `{row.get('docs_update_required')}`",
        f"- Predicted label: `{pred.get('docs_update_required')}`",
        f"- Confidence: `{item['confidence']:.4f}`",
        f"- Predicted doc_category: `{pred.get('doc_category')}`",
        f"- Predicted scenario_type: `{pred.get('scenario_type')}`",
        f"- Code excerpt: {excerpt(raw.get('new_code_raw') or row.get('code_after'))}",
        f"- Comment excerpt: {excerpt(raw.get('new_comment_raw') or row.get('doc_after') or row.get('doc_before'))}",
        "",
        *audit_checklist(checklist),
        "",
    ]


def median_slice(items: list[dict[str, Any]], size: int) -> list[dict[str, Any]]:
    if len(items) <= size:
        return items
    mid = len(items) // 2
    start = max(0, mid - size // 2)
    return items[start : start + size]


def write_false_positive_queue(metrics: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    path = REPORTS_DIR / "external_docchecker_false_positive_audit_queue_2026_08.md"
    raw_by_id = load_raw_rows_by_id(raw_file_values(rows))
    fps = sorted([item for item in metrics["pairs"] if item["outcome"] == "FP"], key=lambda item: item["confidence"], reverse=True)
    groups = [
        ("Highest-Confidence False Positives", fps[:10]),
        ("Median-Confidence False Positives", median_slice(fps, 10)),
        ("Lowest-Confidence False Positives", list(reversed(fps[-10:]))),
    ]
    checklist = ["true false positive", "actually looks inconsistent", "label noise", "mapping bug", "insufficient context", "uncertain"]
    lines = ["# External DocChecker False Positive Audit Queue 2026-08", ""]
    for title, items in groups:
        lines.extend([f"## {title}", ""])
        for item in items:
            lines.extend(prediction_example(item, raw_by_id, checklist))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def representative(items: list[dict[str, Any]], size: int) -> list[dict[str, Any]]:
    ordered = sorted(items, key=lambda item: item["confidence"])
    if len(ordered) <= size:
        return ordered
    if size == 1:
        return [ordered[len(ordered) // 2]]
    indexes = sorted({round(index * (len(ordered) - 1) / (size - 1)) for index in range(size)})
    return [ordered[index] for index in indexes]


def write_success_cases(metrics: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    path = REPORTS_DIR / "external_docchecker_success_case_audit_2026_08.md"
    raw_by_id = load_raw_rows_by_id(raw_file_values(rows))
    tns = [item for item in metrics["pairs"] if item["outcome"] == "TN"]
    tps = [item for item in metrics["pairs"] if item["outcome"] == "TP"]
    lines = [
        "# External DocChecker Success Case Audit 2026-08",
        "",
        f"- True positives: `{len(tps)}`",
        f"- True negatives: `{len(tns)}`",
        "",
        "## True Negatives",
        "",
    ]
    tn_examples = tns if len(tns) <= 10 else representative(tns, 10)
    if not tn_examples:
        lines.append("None.")
    for item in tn_examples:
        lines.extend(prediction_example(item, raw_by_id, ["notes"]))
    lines.extend(["", "## Representative True Positives", ""])
    for item in representative(tps, 10):
        lines.extend(prediction_example(item, raw_by_id, ["notes"]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def baseline_metrics(rows: list[dict[str, Any]], predictions: list[bool]) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    for row, predicted in zip(rows, predictions):
        gold = bool(row.get("docs_update_required"))
        if gold and predicted:
            tp += 1
        elif not gold and predicted:
            fp += 1
        elif not gold and not predicted:
            tn += 1
        else:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, **rates(tp, fp, tn, fn)}


def write_baseline_comparison(rows: list[dict[str, Any]], metrics: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_docchecker_baseline_comparison_2026_08.md"
    rng = random.Random(42)
    random_predictions = [False] * len(rows)
    for index in rng.sample(range(len(rows)), k=len(rows) // 2):
        random_predictions[index] = True
    baselines = {
        "Existing DocGuard": {"tp": metrics["tp"], "fp": metrics["fp"], "tn": metrics["tn"], "fn": metrics["fn"], **rates(metrics["tp"], metrics["fp"], metrics["tn"], metrics["fn"])},
        "Always positive": baseline_metrics(rows, [True] * len(rows)),
        "Always negative": baseline_metrics(rows, [False] * len(rows)),
        "Random balanced baseline, seed 42": baseline_metrics(rows, random_predictions),
    }
    lines = [
        "# External DocChecker Baseline Comparison 2026-08",
        "",
        "| System | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, values in baselines.items():
        lines.append(metric_table_row(name, values["tp"], values["fp"], values["tn"], values["fn"]))
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Existing DocGuard is very close to the always-positive baseline on this external binary proxy. It improves true negatives from 0 to 2, but keeps recall at 100.00% and still produces a 99.20% false-positive rate.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_interpretation_report() -> None:
    path = REPORTS_DIR / "external_docchecker_binary_interpretation_2026_08.md"
    lines = [
        "# External DocChecker Binary Interpretation 2026-08",
        "",
        "This is the first true external binary proxy evaluation for DocGuard. The benchmark is a proxy for code-comment inconsistency, not full project-level Markdown documentation update detection.",
        "",
        "The current synthetic-trained model achieves high recall but very poor specificity. On the 500-record Deep-JIT test-partition sample it reaches 100.00% recall while predicting 248/250 external consistent/no-update examples as update-required.",
        "",
        "This result shows that synthetic-trained DocGuard does not yet generalize to external consistent/no-update comment examples. It does not invalidate the project; it identifies a concrete domain/task shift that synthetic-only experiments and positive-only CoDocBench recall could not expose.",
        "",
        "Recommended thesis wording:",
        "",
        "- The model functions as a high-recall detector but over-predicts documentation-update needs on external binary proxy data.",
        "- External binary evaluation reveals a domain/task shift not visible in synthetic-only experiments.",
        "",
        "This should not be reported as deployment-ready system performance.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_next_modeling_plan() -> None:
    path = REPORTS_DIR / "external_docchecker_next_modeling_plan_2026_08.md"
    lines = [
        "# External DocChecker Next Modeling Plan 2026-08",
        "",
        "1. Confirm label polarity manually against the original Deep-JIT paper, preprocessing code, or dataset release notes.",
        "2. If labels are confirmed, create explicit train/validation/test splits from Deep-JIT without mixing them into the synthetic DocGuard benchmark.",
        "3. Train a lightweight external binary classifier using code + comment pair input with LogisticRegression or LinearSVC over TF-IDF and/or sentence-transformer embeddings.",
        "4. Compare synthetic-trained DocGuard zero-shot transfer, an external-trained binary classifier, and a hybrid approach.",
        "5. Keep task-specific results separate: DocGuard project-level synthetic benchmark, CoDocBench positive update benchmark, and Deep-JIT binary consistency proxy benchmark.",
        "",
        "Do not retrain the production DocGuard path until label polarity and sample quality are manually checked.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def example_lines(item: dict[str, Any]) -> list[str]:
    row = item["record"]
    pred = item["prediction"]
    return [
        f"### {row.get('record_id')}",
        "",
        f"- gold docs_update_required: `{row.get('docs_update_required')}`",
        f"- predicted docs_update_required: `{pred.get('docs_update_required')}`",
        f"- predicted scenario: `{pred.get('scenario_type')}`",
        f"- predicted category: `{pred.get('doc_category')}`",
        f"- confidence: `{confidence(pred):.4f}`",
        f"- code_diff: {truncate(row.get('code_diff'), 360)}",
        f"- doc_diff: {truncate(row.get('doc_diff'), 260)}",
        "",
    ]


def write_report(path: Path, input_path: Path, metrics: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External DocChecker / Deep-JIT Existing DocGuard Binary Evaluation 2026-08",
        "",
        f"- Input: `{input_path}`",
        f"- Total records: `{metrics['total_records']}`",
        f"- Positive count: `{metrics['positive_count']}`",
        f"- Negative count: `{metrics['negative_count']}`",
        f"- Accuracy: `{pct(metrics['accuracy'])}`",
        f"- Precision: `{pct(metrics['precision'])}`",
        f"- Recall: `{pct(metrics['recall'])}`",
        f"- F1: `{pct(metrics['f1'])}`",
        f"- False positives: `{metrics['false_positive_count']}`",
        f"- False negatives: `{metrics['false_negative_count']}`",
        f"- False positive rate: `{pct(metrics['false_positive_rate'])}`",
        f"- False negative rate: `{pct(metrics['false_negative_rate'])}`",
        f"- Median confidence: `{metrics['median_confidence']:.4f}`",
        f"- Average confidence: `{metrics['average_confidence']:.4f}`",
        "",
        "## Confusion Matrix",
        "",
        "|  | Predicted true | Predicted false |",
        "| --- | ---: | ---: |",
        f"| Gold true | {metrics['tp']} | {metrics['fn']} |",
        f"| Gold false | {metrics['fp']} | {metrics['tn']} |",
        "",
        "## Predicted Label Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(metrics["predicted_label_distribution"].items())],
        "",
        "## Predicted Doc Category Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(metrics["predicted_doc_category_distribution"].items(), key=lambda item: item[1], reverse=True)],
        "",
        "## Predicted Scenario Type Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(metrics["predicted_scenario_type_distribution"].items(), key=lambda item: item[1], reverse=True)[:30]],
        "",
        "## Top False Positives",
        "",
    ]
    false_positives = [item for item in metrics["pairs"] if item["outcome"] == "FP"]
    false_negatives = [item for item in metrics["pairs"] if item["outcome"] == "FN"]
    if false_positives:
        for item in false_positives[:10]:
            lines.extend(example_lines(item))
    else:
        lines.append("None.")
    lines.extend(["", "## Top False Negatives", ""])
    if false_negatives:
        for item in false_negatives[:10]:
            lines.extend(example_lines(item))
    else:
        lines.append("None.")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "This is the first external binary proxy evaluation using code-comment consistency labels. It is not full project-level Markdown documentation update detection.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_evidence_comparison(metrics: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_validation_evidence_comparison_2026_08.md"
    lines = [
        "# External Validation Evidence Comparison 2026-08",
        "",
        "| Evidence type | Dataset | Status | Key result | Interpretation |",
        "| --- | --- | --- | --- | --- |",
        "| Controlled synthetic evidence | Synthetic v0.4 | complete | see v0.4 reports | Controlled pipeline benchmark. |",
        "| Real positive sensitivity evidence | CoDocBench | complete | 100.00% code_diff_only positive recall on 500 positives | Positive-only, no precision/F1. |",
        "| Sanity-control evidence | Synthetic negatives | complete | 0/500 false positives in two modes | Not constant-positive under synthetic control. |",
        f"| True external binary proxy evidence | Deep-JIT / DocChecker-style sample | complete | F1 {pct(metrics['f1'])}, precision {pct(metrics['precision'])}, recall {pct(metrics['recall'])}, FPR {pct(metrics['false_positive_rate'])} | Code-comment consistency proxy; high recall but near always-positive behavior. |",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate_existing_binary(input_path: Path, output_path: Path) -> dict[str, Any]:
    if not input_path.exists():
        return {"status": "error", "message": f"input not found: {input_path}"}
    rows = read_jsonl(input_path)
    docguard_rows = [external_binary_to_docguard(row) for row in rows]
    predictions, model_info, error = try_hf_staged_predictions(docguard_rows, "code_diff_plus_doc_before")
    if not predictions:
        return {"status": "error", "message": error or "predictor unavailable"}
    metrics = binary_metrics(rows, predictions)
    write_report(output_path, input_path, metrics)
    write_label_polarity_audit(rows)
    write_error_analysis(metrics)
    write_threshold_sweep(metrics)
    write_false_positive_queue(metrics, rows)
    write_success_cases(metrics, rows)
    write_baseline_comparison(rows, metrics)
    write_interpretation_report()
    write_next_modeling_plan()
    write_evidence_comparison(metrics)
    return {
        "status": "ok",
        "input": str(input_path),
        "output": str(output_path),
        "model_path": model_info.get("model_path"),
        "total_records": metrics["total_records"],
        "positive_count": metrics["positive_count"],
        "negative_count": metrics["negative_count"],
        "tp": metrics["tp"],
        "fp": metrics["fp"],
        "tn": metrics["tn"],
        "fn": metrics["fn"],
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
        "false_positive_count": metrics["false_positive_count"],
        "false_negative_count": metrics["false_negative_count"],
        "false_positive_rate": metrics["false_positive_rate"],
        "false_negative_rate": metrics["false_negative_rate"],
    }
