from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

from docguard_external.evaluate_existing_docguard import (
    EXTERNAL_INPUT_MODES,
    LOW_CONFIDENCE_THRESHOLD,
    artifact_path,
    confidence,
    confidence_summary,
    pct,
    read_jsonl,
    try_hf_staged_predictions,
    truncate,
    write_histogram,
)


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
SYNTHETIC_CANDIDATE_PATHS = [
    ROOT / "data" / "test.jsonl",
    ROOT / "data" / "validation.jsonl",
    ROOT / "data" / "train.jsonl",
    ROOT / "data" / "hf_v0_4" / "raw_diff_plus_docs" / "test.jsonl",
    ROOT / "data" / "hf_v0_4" / "raw_diff_plus_docs" / "validation.jsonl",
    ROOT / "data" / "hf_v0_4" / "raw_diff_plus_docs" / "train.jsonl",
]


def is_negative(row: dict[str, Any]) -> bool:
    return row.get("docs_update_required") is False or row.get("docs_update_required_label") == "false" or row.get("doc_category") == "no_update" or row.get("doc_category_label") == "no_update"


def docs_excerpt_for_mode(row: dict[str, Any], external_input_mode: str) -> str:
    if external_input_mode == "code_diff_only":
        return ""
    if external_input_mode == "code_diff_plus_doc_before":
        return str(row.get("docs_before_excerpt") or "")
    if external_input_mode == "code_diff_plus_doc_diff_upper_bound":
        return str(row.get("docs_after_gold_excerpt") or row.get("docs_before_excerpt") or "")
    raise ValueError(f"Unsupported external input mode: {external_input_mode}")


def load_synthetic_negative_records(limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    searched = []
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in SYNTHETIC_CANDIDATE_PATHS:
        searched.append(str(path))
        if not path.exists():
            continue
        for row in read_jsonl(path):
            record_id = str(row.get("id") or row.get("record_id") or "")
            if record_id in seen or not is_negative(row):
                continue
            seen.add(record_id)
            enriched = dict(row)
            enriched["_source_path"] = str(path)
            records.append(enriched)
            if len(records) >= limit:
                return records, searched
    return records, searched


def synthetic_to_docguard_record(row: dict[str, Any], external_input_mode: str) -> dict[str, Any]:
    target = row.get("target_doc_file") or row.get("target_doc_file_label") or ""
    if target == "no_update":
        target = ""
    return {
        "id": row.get("id") or row.get("record_id"),
        "project_id": row.get("project_id") or "synthetic_v0_4",
        "changed_files": row.get("changed_files") or [],
        "code_diff": row.get("code_diff") or "",
        "docs_before_excerpt": docs_excerpt_for_mode(row, external_input_mode),
        "docs_update_required": False,
        "scenario_type": row.get("scenario_type") or row.get("scenario_type_label") or "synthetic_negative",
        "target_kind": "synthetic_control",
        "doc_category": "no_update",
        "target_doc_file": target,
        "target_section": row.get("target_section") or "",
        "expected_facts": [],
        "external_input_mode": external_input_mode,
    }


def compute_negative_metrics(records: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    values = [confidence(pred) for pred in predictions]
    false_positives = [
        {"record": record, "prediction": pred, "confidence": confidence(pred)}
        for record, pred in zip(records, predictions)
        if pred.get("docs_update_required") is True
    ]
    predicted_positive = len(false_positives)
    total = len(records)
    return {
        "total_negative_records_evaluated": total,
        "predicted_update_required_count": predicted_positive,
        "false_positive_count": predicted_positive,
        "negative_accuracy": (total - predicted_positive) / total if total else 0.0,
        "false_positive_rate": predicted_positive / total if total else 0.0,
        "average_confidence": mean(values) if values else 0.0,
        "median_confidence": median(values) if values else 0.0,
        "low_confidence_count_below_0_25": sum(1 for value in values if value < LOW_CONFIDENCE_THRESHOLD),
        "confidence_summary": confidence_summary(values),
        "predicted_doc_category_distribution": dict(Counter(str(pred.get("doc_category") or "unknown") for pred in predictions)),
        "predicted_scenario_type_distribution": dict(Counter(str(pred.get("scenario_type") or "unknown") for pred in predictions)),
        "false_positives": false_positives,
    }


def example_lines(item: dict[str, Any]) -> list[str]:
    record = item["record"]
    prediction = item["prediction"]
    return [
        f"### {record.get('id')}",
        "",
        f"- project: `{record.get('project_id')}`",
        f"- source path: `{record.get('_source_path')}`",
        f"- gold scenario: `{record.get('scenario_type')}`",
        f"- predicted docs_update_required: `{prediction.get('docs_update_required')}`",
        f"- predicted doc category: `{prediction.get('doc_category')}`",
        f"- predicted scenario: `{prediction.get('scenario_type')}`",
        f"- confidence: `{confidence(prediction):.4f}`",
        f"- code_diff: {truncate(record.get('code_diff'), 420)}",
        f"- docs_before_excerpt: {truncate(record.get('docs_before_excerpt'), 300)}",
        "",
    ]


def write_negative_report(path: Path, input_mode: str, searched_paths: list[str], metrics: dict[str, Any], pairs: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    confidence_info = metrics["confidence_summary"]
    false_positives = sorted(metrics["false_positives"], key=lambda item: item["confidence"], reverse=True)
    all_pairs = sorted(pairs, key=lambda item: item["confidence"])
    high_conf = list(reversed(all_pairs))[:10]
    low_conf = all_pairs[:10]
    lines = [
        "# Synthetic Negative Sanity Control 2026-08",
        "",
        f"- Input mode: `{input_mode}`",
        f"- Control type: `synthetic negatives`, not an external negative set",
        f"- Total negative records evaluated: `{metrics['total_negative_records_evaluated']}`",
        f"- Predicted update-required count: `{metrics['predicted_update_required_count']}`",
        f"- False positive count: `{metrics['false_positive_count']}`",
        f"- Negative accuracy: `{pct(metrics['negative_accuracy'])}`",
        f"- False positive rate: `{pct(metrics['false_positive_rate'])}`",
        f"- Median confidence: `{metrics['median_confidence']:.4f}`",
        f"- Low confidence <0.25: `{metrics['low_confidence_count_below_0_25']}`",
        f"- Min confidence: `{confidence_info['min_confidence']:.4f}`",
        f"- Max confidence: `{confidence_info['max_confidence']:.4f}`",
        "",
        "## Dataset Paths Searched",
        "",
        *[f"- `{item}`" for item in searched_paths],
        "",
        "## Important Limitation",
        "",
        "This is a sanity control using existing synthetic negatives. It is useful for checking constant-positive behavior, but it is not a real external negative set and cannot support final external precision/F1.",
        "",
        "## Predicted Doc Category Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(metrics["predicted_doc_category_distribution"].items(), key=lambda item: item[1], reverse=True)],
        "",
        "## Predicted Scenario Type Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(metrics["predicted_scenario_type_distribution"].items(), key=lambda item: item[1], reverse=True)[:30]],
        "",
        "## Top False-Positive Examples",
        "",
    ]
    if false_positives:
        for item in false_positives[:20]:
            lines.extend(example_lines(item))
    else:
        lines.append("None.")
    lines.extend(["", "## 10 Low-Confidence Examples", ""])
    for item in low_conf:
        lines.extend(example_lines(item))
    lines.extend(["", "## 10 High-Confidence Examples", ""])
    for item in high_conf:
        lines.extend(example_lines(item))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_failure_report(path: Path, searched_paths: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Synthetic Negative Sanity Control 2026-08",
        "",
        "No suitable synthetic negative records were found. No metrics were produced.",
        "",
        "## Paths Searched",
        "",
        *[f"- `{item}`" for item in searched_paths],
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_combined_sanity_report() -> None:
    positive_paths = [
        REPORTS_DIR / "external_codocbench_positive_recall_code_diff_only_2026_08_summary.json",
        REPORTS_DIR / "external_codocbench_positive_recall_code_diff_plus_doc_before_2026_08_summary.json",
    ]
    negative_paths = [
        REPORTS_DIR / "synthetic_negative_control_code_diff_only_2026_08_summary.json",
        REPORTS_DIR / "synthetic_negative_control_code_diff_plus_doc_before_2026_08_summary.json",
    ]
    rows: list[dict[str, Any]] = []
    for path in positive_paths:
        if path.exists():
            item = json.loads(path.read_text(encoding="utf-8"))
            rows.append(
                {
                    "dataset": "CoDocBench",
                    "label_type": "external strong positives",
                    "input_mode": item["external_input_mode"],
                    "total": item["total_positives_evaluated"],
                    "predicted": item["predicted_update_required_count"],
                    "score": item["positive_recall"],
                    "error_count": item["false_negative_count"],
                    "error_label": "false negatives",
                    "median_confidence": item["median_confidence"],
                    "low_confidence": item["low_confidence_count_below_0_25"],
                    "interpretation": "positive recall only",
                }
            )
    for path in negative_paths:
        if path.exists():
            item = json.loads(path.read_text(encoding="utf-8"))
            rows.append(
                {
                    "dataset": "Synthetic v0.4",
                    "label_type": "synthetic negatives sanity control",
                    "input_mode": item["external_input_mode"],
                    "total": item["total_negative_records_evaluated"],
                    "predicted": item["predicted_update_required_count"],
                    "score": item["negative_accuracy"],
                    "error_count": item["false_positive_count"],
                    "error_label": "false positives",
                    "median_confidence": item["median_confidence"],
                    "low_confidence": item["low_confidence_count_below_0_25"],
                    "interpretation": "constant-positive sanity check, not external F1",
                }
            )
    if not rows:
        return
    lines = [
        "# External Positive vs Synthetic Negative Sanity 2026-08",
        "",
        "| Dataset | Label type | Input mode | Total records | Predicted update-required | Recall or negative accuracy | False negatives or false positives | Median confidence | Low confidence <0.25 | Interpretation |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['label_type']} | `{row['input_mode']}` | {row['total']} | {row['predicted']} | "
            f"{pct(row['score'])} | {row['error_count']} {row['error_label']} | {row['median_confidence']:.4f} | {row['low_confidence']} | {row['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "This table does not report final external F1. It checks whether the current predictor behaves as a constant-positive classifier when confronted with known synthetic no-update examples.",
        ]
    )
    (REPORTS_DIR / "external_positive_vs_synthetic_negative_sanity_2026_08.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate_synthetic_negatives(limit: int, external_input_mode: str, output_path: Path) -> dict[str, Any]:
    if external_input_mode not in EXTERNAL_INPUT_MODES:
        return {"status": "error", "message": f"unsupported external input mode: {external_input_mode}"}
    negatives, searched_paths = load_synthetic_negative_records(limit)
    if not negatives:
        write_failure_report(output_path, searched_paths)
        return {"status": "error", "message": "no suitable synthetic negatives found", "searched_paths": searched_paths}
    docguard_rows = [synthetic_to_docguard_record(row, external_input_mode) for row in negatives]
    predictions, model_info, error = try_hf_staged_predictions(docguard_rows, external_input_mode)
    if not predictions:
        write_failure_report(output_path, searched_paths)
        return {"status": "error", "message": error or "predictor unavailable", "searched_paths": searched_paths}
    metrics = compute_negative_metrics(negatives, predictions)
    pairs = [{"record": record, "prediction": pred, "confidence": confidence(pred)} for record, pred in zip(negatives, predictions)]
    write_negative_report(output_path, external_input_mode, searched_paths, metrics, pairs)
    write_histogram(artifact_path(output_path, "confidence_histogram", ".csv"), predictions)
    summary = {
        "status": "ok",
        "output": str(output_path),
        "external_input_mode": external_input_mode,
        "dataset": "synthetic_v0_4_negative_control",
        "model_path": model_info.get("model_path"),
        "total_negative_records_evaluated": metrics["total_negative_records_evaluated"],
        "predicted_update_required_count": metrics["predicted_update_required_count"],
        "false_positive_count": metrics["false_positive_count"],
        "negative_accuracy": metrics["negative_accuracy"],
        "false_positive_rate": metrics["false_positive_rate"],
        "average_confidence": metrics["average_confidence"],
        "median_confidence": metrics["median_confidence"],
        "low_confidence_count_below_0_25": metrics["low_confidence_count_below_0_25"],
        "searched_paths": searched_paths,
    }
    artifact_path(output_path, "summary", ".json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    update_combined_sanity_report()
    return summary
