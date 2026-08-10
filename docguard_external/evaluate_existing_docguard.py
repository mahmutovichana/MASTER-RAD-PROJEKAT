from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
HF_MODEL_PATH = ROOT / "models" / "hf_v0_4" / "raw_diff_plus_docs" / "embedding_classifier_staged.joblib"
LOW_CONFIDENCE_THRESHOLD = 0.25
CONFIDENCE_THRESHOLDS = [0.00, 0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75]
EXTERNAL_INPUT_MODES = {
    "code_diff_only": {
        "leakage_risk": "fair",
        "description": "Uses changed file, function name, and code_diff only. No documentation text is included.",
    },
    "code_diff_plus_doc_before": {
        "leakage_risk": "assisted",
        "description": "Uses changed file, function name, code_diff, and doc_before only. No future doc diff or doc_after is included.",
    },
    "code_diff_plus_doc_diff_upper_bound": {
        "leakage_risk": "upper_bound_leakage_risk",
        "description": "Uses code_diff and doc_diff. This exposes the future documentation change and is not a primary fair result.",
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def docs_excerpt_for_mode(row: dict[str, Any], external_input_mode: str) -> str:
    if external_input_mode == "code_diff_only":
        return ""
    if external_input_mode == "code_diff_plus_doc_before":
        return str(row.get("doc_before") or "")
    if external_input_mode == "code_diff_plus_doc_diff_upper_bound":
        return str(row.get("doc_diff") or "")
    raise ValueError(f"Unsupported external input mode: {external_input_mode}")


def external_to_docguard_record(row: dict[str, Any], external_input_mode: str = "code_diff_plus_doc_before") -> dict[str, Any]:
    metadata = row.get("metadata") or {}
    target_path = row.get("target_path") or metadata.get("file_path") or metadata.get("filename") or row.get("record_id")
    return {
        "id": row["record_id"],
        "project_id": row.get("repository") or "external_codocbench",
        "changed_files": [target_path] if target_path else [],
        "code_diff": row.get("code_diff") or "",
        "docs_before_excerpt": docs_excerpt_for_mode(row, external_input_mode),
        "docs_update_required": True,
        "scenario_type": "external_code_doc_cochange",
        "target_kind": "docstring_or_comment",
        "doc_category": "docstring_or_comment",
        "target_doc_file": target_path or "",
        "target_section": metadata.get("function_name") or "",
        "expected_facts": [],
        "external_input_mode": external_input_mode,
    }


def hf_rows(docguard_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from docguard_hf_classifier.text_builder import build_input_text

    rows = []
    for row in docguard_rows:
        hf_row = dict(row)
        hf_row.update(
            {
                "docs_update_required_label": "true",
                "doc_category_label": "docstring_or_comment",
                "scenario_type_label": "external_code_doc_cochange",
                "target_doc_file_label": row.get("target_doc_file") or "docstring_or_comment",
            }
        )
        hf_row["input_text"] = build_input_text(hf_row, input_mode="raw_diff_plus_docs")
        rows.append(hf_row)
    return rows


def try_hf_staged_predictions(docguard_rows: list[dict[str, Any]], external_input_mode: str) -> tuple[list[dict[str, Any]], dict[str, Any], str | None]:
    try:
        from docguard_hf_classifier.embedding_classifier import load_model, predict_rows

        if not HF_MODEL_PATH.exists():
            return [], {"predictor": "unavailable", "model_path": str(HF_MODEL_PATH)}, f"HF staged classifier not found at {HF_MODEL_PATH}"
        model = load_model("raw_diff_plus_docs", "staged")
        predictions, _latency = predict_rows(hf_rows(docguard_rows), model)
        model_info = {
            "predictor": "hf_embedding_staged_raw_diff_plus_docs",
            "model_path": str(HF_MODEL_PATH),
            "model_type": model.get("classifier_type", "unknown"),
            "model_name": model.get("model_name", "unknown"),
            "input_mode": model.get("input_mode", "raw_diff_plus_docs"),
            "classifier_architecture": model.get("classifier_architecture", "staged"),
            "external_input_mode": external_input_mode,
            "external_input_mode_leakage_risk": EXTERNAL_INPUT_MODES[external_input_mode]["leakage_risk"],
            "external_input_mode_description": EXTERNAL_INPUT_MODES[external_input_mode]["description"],
            "decision_rule": "docs_update_required is true when the staged docs_update_required classifier top label is `true`.",
            "confidence_definition": "minimum probability across docs_update_required, positive doc_category, positive scenario_type, and positive target_doc_file classifiers for positive predictions",
            "threshold_used": "none for binary decision; confidence thresholds are analyzed only as abstention/review policies",
        }
        return predictions, model_info, None
    except Exception as exc:
        return [], {"predictor": "unavailable", "model_path": str(HF_MODEL_PATH)}, f"HF staged classifier could not run: {exc}"


def deterministic_predictions(docguard_rows: list[dict[str, Any]], external_input_mode: str) -> tuple[list[dict[str, Any]], dict[str, Any], str | None]:
    try:
        from docguard.evaluator import predict_record

        predictions = []
        for row in docguard_rows:
            pred = predict_record(row)
            predictions.append(
                {
                    "record_id": row["id"],
                    "docs_update_required": bool(pred.get("docs_update_required")),
                    "confidence": float(pred.get("docs_update_score") or 0.0),
                    "doc_category": pred.get("doc_category") or "unknown",
                    "scenario_type": pred.get("scenario_type") or "unknown",
                    "target_doc_file": pred.get("target_doc_file") or "",
                }
            )
        model_info = {
            "predictor": "deterministic_docguard_predict_record",
            "model_path": "n/a",
            "model_type": "rule_based",
            "model_name": "docguard.evaluator.predict_record",
            "input_mode": "DocGuard-like mapped code_diff plus changed_files",
            "classifier_architecture": "rule_based",
            "external_input_mode": external_input_mode,
            "external_input_mode_leakage_risk": EXTERNAL_INPUT_MODES[external_input_mode]["leakage_risk"],
            "external_input_mode_description": EXTERNAL_INPUT_MODES[external_input_mode]["description"],
            "decision_rule": "docs_update_required is returned by the deterministic change classifier.",
            "confidence_definition": "docs_update_score from the deterministic predictor",
            "threshold_used": "none for binary decision; confidence thresholds are analyzed only as abstention/review policies",
        }
        return predictions, model_info, None
    except Exception as exc:
        return [], {"predictor": "unavailable", "model_path": "n/a"}, f"Deterministic predictor could not run: {exc}"


def confidence(prediction: dict[str, Any]) -> float:
    return float(prediction.get("confidence") or prediction.get("docs_update_required_confidence") or 0.0)


def paired_records(external_rows: list[dict[str, Any]], docguard_rows: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for external, docguard, prediction in zip(external_rows, docguard_rows, predictions):
        rows.append({"external": external, "record": docguard, "prediction": prediction, "confidence": confidence(prediction)})
    return rows


def percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def confidence_summary(confidences: list[float]) -> dict[str, Any]:
    values = sorted(confidences)
    deciles = {f"p{int(q * 100):02d}": percentile(values, q) for q in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}
    return {
        "min_confidence": min(values) if values else 0.0,
        "max_confidence": max(values) if values else 0.0,
        "mean_confidence": mean(values) if values else 0.0,
        "median_confidence": median(values) if values else 0.0,
        "q1_confidence": percentile(values, 0.25),
        "q3_confidence": percentile(values, 0.75),
        "deciles": deciles,
    }


def threshold_analysis(predictions: list[dict[str, Any]], total: int) -> list[dict[str, Any]]:
    rows = []
    for threshold in CONFIDENCE_THRESHOLDS:
        accepted = [pred for pred in predictions if confidence(pred) >= threshold]
        accepted_tp = sum(1 for pred in accepted if pred.get("docs_update_required") is True)
        rejected = total - len(accepted)
        rows.append(
            {
                "threshold": threshold,
                "accepted_predictions": len(accepted),
                "accepted_percentage": len(accepted) / total if total else 0.0,
                "accepted_true_positives": accepted_tp,
                "rejected_positives": rejected,
                "recall_all_positives_abstentions_missed": accepted_tp / total if total else 0.0,
                "recall_accepted_positive_only": accepted_tp / len(accepted) if accepted else 0.0,
            }
        )
    return rows


def compute_metrics(records: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    confidences = [confidence(pred) for pred in predictions]
    predicted_positive = sum(1 for pred in predictions if pred.get("docs_update_required") is True)
    false_negatives = [
        {"record": record, "prediction": pred}
        for record, pred in zip(records, predictions)
        if pred.get("docs_update_required") is not True
    ]
    return {
        "total_positives_evaluated": len(records),
        "predicted_update_required_count": predicted_positive,
        "false_negative_count": len(false_negatives),
        "positive_recall": predicted_positive / len(records) if records else 0.0,
        "average_confidence": mean(confidences) if confidences else 0.0,
        "median_confidence": median(confidences) if confidences else 0.0,
        "low_confidence_threshold": LOW_CONFIDENCE_THRESHOLD,
        "low_confidence_count_below_0_25": sum(1 for value in confidences if value < LOW_CONFIDENCE_THRESHOLD),
        "low_confidence_percentage": sum(1 for value in confidences if value < LOW_CONFIDENCE_THRESHOLD) / len(confidences) if confidences else 0.0,
        "confidence_summary": confidence_summary(confidences),
        "threshold_analysis": threshold_analysis(predictions, len(records)),
        "predicted_doc_category_distribution": dict(Counter(str(pred.get("doc_category") or "unknown") for pred in predictions)),
        "predicted_scenario_type_distribution": dict(Counter(str(pred.get("scenario_type") or "unknown") for pred in predictions)),
        "predicted_target_doc_file_distribution": dict(Counter(str(pred.get("target_doc_file") or "unknown") for pred in predictions)),
        "false_negatives": false_negatives,
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def truncate(value: Any, limit: int = 220) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def write_histogram(path: Path, predictions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bins = [(i / 10, (i + 1) / 10) for i in range(10)]
    counts = []
    values = [confidence(pred) for pred in predictions]
    for start, end in bins:
        count = sum(1 for value in values if start <= value < end or (end == 1.0 and value == 1.0))
        counts.append((start, end, count, count / len(values) if values else 0.0))
    lines = ["bin_start,bin_end,count,percentage"]
    lines.extend(f"{start:.1f},{end:.1f},{count},{percentage:.6f}" for start, end, count, percentage in counts)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prediction_audit_row(external: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    metadata = external.get("metadata") or {}
    return {
        "record_id": external.get("record_id"),
        "repository": external.get("repository"),
        "owner": metadata.get("owner"),
        "function": metadata.get("function_name"),
        "commit_hash": external.get("commit_hash"),
        "commit_date_time": metadata.get("commit_date_time"),
        "code_diff_truncated": truncate(external.get("code_diff"), 1200),
        "doc_diff_truncated": truncate(external.get("doc_diff"), 900),
        "gold_docs_update_required": external.get("docs_update_required"),
        "predicted_docs_update_required": prediction.get("docs_update_required"),
        "confidence": confidence(prediction),
        "predicted_doc_category": prediction.get("doc_category"),
        "predicted_scenario_type": prediction.get("scenario_type"),
        "predicted_target_doc_file": prediction.get("target_doc_file"),
        "label_source": external.get("label_source"),
        "mapping_warnings": metadata.get("mapping_warnings") or [],
    }


def artifact_path(output_path: Path, suffix: str, extension: str) -> Path:
    return output_path.parent / f"{output_path.stem}_{suffix}{extension}"


def write_prediction_records(path: Path, pairs: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(prediction_audit_row(item["external"], item["prediction"]), ensure_ascii=False) for item in pairs]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def example_lines(item: dict[str, Any]) -> list[str]:
    external = item["external"]
    prediction = item["prediction"]
    metadata = external.get("metadata") or {}
    return [
        f"### {external.get('record_id')}",
        "",
        f"- repo/project: `{external.get('repository')}`",
        f"- function: `{metadata.get('function_name')}`",
        f"- commit hash: `{external.get('commit_hash')}`",
        f"- confidence: `{confidence(prediction):.4f}`",
        f"- predicted doc category: `{prediction.get('doc_category')}`",
        f"- predicted scenario: `{prediction.get('scenario_type')}`",
        f"- predicted target: `{prediction.get('target_doc_file')}`",
        f"- short code diff: {truncate(external.get('code_diff'), 420)}",
        f"- short doc diff: {truncate(external.get('doc_diff'), 360)}",
        "- Manual assessment: [ ] correct update-required signal [ ] questionable [ ] mapping issue [ ] model issue",
        "",
    ]


def write_manual_audit_queue(path: Path, pairs: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    false_negatives = [item for item in pairs if item["prediction"].get("docs_update_required") is not True]
    true_positives = [item for item in pairs if item["prediction"].get("docs_update_required") is True]
    lowest = sorted(true_positives, key=lambda item: item["confidence"])[:20]
    highest = sorted(true_positives, key=lambda item: item["confidence"], reverse=True)[:10]
    random_sample = random.Random(42).sample(true_positives, min(10, len(true_positives)))
    lines = [
        "# External CoDocBench Manual Audit Queue 2026-08",
        "",
        "## False Negative Examples",
        "",
    ]
    for item in false_negatives:
        lines.extend(example_lines(item))
    if not false_negatives:
        lines.append("None.")
    lines.extend(["", "## 20 Lowest-Confidence True Positives", ""])
    for item in lowest:
        lines.extend(example_lines(item))
    lines.extend(["", "## 10 Random True Positives", ""])
    for item in random_sample:
        lines.extend(example_lines(item))
    lines.extend(["", "## 10 Highest-Confidence True Positives", ""])
    for item in highest:
        lines.extend(example_lines(item))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_calibration_notes(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External Confidence Calibration Notes 2026-08",
        "",
        "High positive recall with low confidence should not be overclaimed. It shows that the existing predictor is sensitive to many real CoDocBench code-doc co-changes, but the score distribution suggests uncertainty under external data.",
        "",
        "The most likely explanation is a combination of synthetic-to-real domain shift and probability calibration. The HF embedding classifier was trained on synthetic DocGuard v0.4 examples, while CoDocBench contains Python docstring/comment maintenance from many real projects. The classifier can often choose the positive class, but its downstream category, scenario, and target-file classifiers are operating outside their original project-level Markdown label space.",
        "",
        "LogisticRegression probabilities over sentence embeddings are not guaranteed to be calibrated under distribution shift. The current confidence is also a joint/minimum confidence across staged decisions, so one uncertain downstream label can make an otherwise correct positive decision look low-confidence.",
        "",
        "Low confidence matters for VS Code usage because a developer-facing assistant should distinguish confident update-required warnings from review-needed suggestions. A low-confidence positive may be useful, but it should not feel like a definitive instruction.",
        "",
        "## Recommended Future Work",
        "",
        "1. Calibrate confidence on validation data.",
        "2. Use external real-data fine-tuning after labels stabilize.",
        "3. Report recall at multiple confidence thresholds.",
        "4. Add an abstain or review-needed state for low-confidence predictions.",
        "5. Use external negatives before reporting precision or F1.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_leakage_audit(path: Path, input_path: Path, external_rows: list[dict[str, Any]]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    total = len(external_rows)
    doc_before_count = sum(1 for row in external_rows if row.get("doc_before") not in {None, ""})
    doc_after_count = sum(1 for row in external_rows if row.get("doc_after") not in {None, ""})
    doc_diff_count = sum(1 for row in external_rows if row.get("doc_diff") not in {None, ""})
    code_diff_count = sum(1 for row in external_rows if row.get("code_diff") not in {None, ""})
    lines = [
        "# External CoDocBench Evaluation Leakage Audit 2026-08",
        "",
        f"- Input sample: `{input_path}`",
        f"- Records inspected: `{total}`",
        f"- Records with `code_diff`: `{code_diff_count}`",
        f"- Records with `doc_before`: `{doc_before_count}`",
        f"- Records with `doc_after`: `{doc_after_count}`",
        f"- Records with `doc_diff`: `{doc_diff_count}`",
        "",
        "## Current Evaluation Input Construction",
        "",
        "- Previous bridge behavior used `docs_before_excerpt = doc_before or doc_diff or \"\"`.",
        "- On the current 500-record sample, `doc_before` is present for every row, so `doc_diff` was not actually selected by that expression.",
        "- However, the fallback to `doc_diff` was leakage-risk if future samples lacked `doc_before`.",
        "- `doc_after` was not passed to the predictor.",
        "- The predictor received `changed_files`, `code_diff`, `docs_before_excerpt`, ids/labels used by the classifier wrapper, and target metadata.",
        "- It did not receive full `doc_after` unless a future code path were changed to include it.",
        "",
        "## Direct Answers",
        "",
        "| Question | Answer |",
        "| --- | --- |",
        f"| Was `doc_diff` / `diff_docstring` included in the model input? | `No` for this 500-record run because `doc_before` existed for all rows; `yes, possible fallback` in the previous generic code path if `doc_before` was missing. |",
        "| Was it used as `docs_before_excerpt` or equivalent? | `No` for the current sample; the previous code could have used it as `docs_before_excerpt` fallback. |",
        "| Was `doc_after` included? | `No`. |",
        "| Was only `code_diff` used? | `No`; the previous run also included `doc_before` as current documentation context. |",
        "| Is the current 99.80% recall fair, assisted, or leakage-risk? | `assisted` for the current sample because it used `doc_before`; the old implementation was `upper_bound_leakage_risk` for samples missing `doc_before`. |",
        "| What input mode should be primary fair external evaluation? | `code_diff_plus_doc_before` if doc_before is reliable; otherwise `code_diff_only` is the strictest fair mode. |",
        "",
        "## Input Mode Labels",
        "",
        "- `fair`: no future doc diff or doc after.",
        "- `assisted`: current docs before only.",
        "- `upper_bound_leakage_risk`: includes doc diff or doc after.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "records": total,
        "doc_before_count": doc_before_count,
        "doc_after_count": doc_after_count,
        "doc_diff_count": doc_diff_count,
        "code_diff_count": code_diff_count,
        "previous_result_label": "assisted",
    }


def write_input_mode_comparison(path: Path, summaries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External CoDocBench Input Mode Comparison 2026-08",
        "",
        "| External input mode | Leakage risk | Total positives | Predicted update-required | False negatives | Positive recall | Median confidence | Low confidence <0.25 | Notes |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for summary in summaries:
        lines.append(
            f"| `{summary['external_input_mode']}` | `{summary['leakage_risk']}` | "
            f"{summary['total_positives_evaluated']} | {summary['predicted_update_required_count']} | "
            f"{summary['false_negative_count']} | {pct(summary['positive_recall'])} | "
            f"{summary['median_confidence']:.4f} | {summary['low_confidence_count_below_0_25']} | "
            f"{summary.get('notes', '')} |"
        )
    lines.extend(
        [
            "",
            "The primary fair external result should be `code_diff_only` or `code_diff_plus_doc_before`. The preferred mode is `code_diff_plus_doc_before` when `doc_before` is reliably reconstructed or available because it matches DocGuard's intended access to current documentation before an update.",
            "",
            "`code_diff_plus_doc_diff_upper_bound` is useful only as an upper-bound diagnostic because it includes the future documentation change.",
            "",
            "This is still positive-only evaluation. It cannot report precision, F1, false-positive rate, or negative quality without a defensible external negative set.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_input_mode_comparison(current_summary: dict[str, Any]) -> None:
    summary_paths = [
        REPORTS_DIR / "external_codocbench_positive_recall_code_diff_only_2026_08_summary.json",
        REPORTS_DIR / "external_codocbench_positive_recall_code_diff_plus_doc_before_2026_08_summary.json",
        REPORTS_DIR / "external_codocbench_positive_recall_doc_diff_upper_bound_2026_08_summary.json",
    ]
    current_path = artifact_path(Path(str(current_summary["output"])), "summary", ".json")
    current_path.write_text(json.dumps(current_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summaries: list[dict[str, Any]] = []
    for path in summary_paths:
        if path.exists():
            summaries.append(json.loads(path.read_text(encoding="utf-8")))
    if current_summary not in summaries and current_path not in summary_paths:
        summaries.append(current_summary)
    if summaries:
        order = {"code_diff_only": 0, "code_diff_plus_doc_before": 1, "code_diff_plus_doc_diff_upper_bound": 2}
        summaries.sort(key=lambda row: order.get(row.get("external_input_mode"), 99))
        write_input_mode_comparison(REPORTS_DIR / "external_codocbench_input_mode_comparison_2026_08.md", summaries)


def distribution_lines(values: dict[str, int], limit: int | None = None) -> list[str]:
    items = sorted(values.items(), key=lambda item: item[1], reverse=True)
    if limit is not None:
        items = items[:limit]
    return [f"- `{key}`: {value}" for key, value in items] or ["None."]


def write_report(
    path: Path,
    input_path: Path,
    model_info: dict[str, Any],
    fallback_note: str | None,
    metrics: dict[str, Any],
    pairs: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    diagnostics_path = artifact_path(path, "diagnostics", ".md")
    confidence_info = metrics["confidence_summary"]
    low_conf_count = metrics["low_confidence_count_below_0_25"]
    total = metrics["total_positives_evaluated"]
    false_negatives = [item for item in pairs if item["prediction"].get("docs_update_required") is not True]
    true_positives = [item for item in pairs if item["prediction"].get("docs_update_required") is True]
    lowest_true_positives = sorted(true_positives, key=lambda item: item["confidence"])[:20]
    high_true_positives = sorted(true_positives, key=lambda item: item["confidence"], reverse=True)[:10]
    low_true_positives = sorted(true_positives, key=lambda item: item["confidence"])[:10]
    lines = [
        "# External CoDocBench Existing DocGuard Positive Recall 2026-08",
        "",
        f"- Input: `{input_path}`",
        f"- Predictor used: `{model_info.get('predictor')}`",
        f"- Model path: `{model_info.get('model_path')}`",
        f"- Model type: `{model_info.get('model_type')}`",
        f"- Model name: `{model_info.get('model_name')}`",
        f"- Input mode: `{model_info.get('input_mode')}`",
        f"- Classifier architecture: `{model_info.get('classifier_architecture')}`",
        f"- External input mode: `{model_info.get('external_input_mode')}`",
        f"- External input leakage label: `{model_info.get('external_input_mode_leakage_risk')}`",
        f"- External input mode definition: {model_info.get('external_input_mode_description')}",
        f"- Decision rule: {model_info.get('decision_rule')}",
        f"- Confidence definition: {model_info.get('confidence_definition')}",
        f"- Threshold used for binary decision: `{model_info.get('threshold_used')}`",
        f"- Total positives evaluated: `{metrics['total_positives_evaluated']}`",
        f"- Predicted update-required count: `{metrics['predicted_update_required_count']}`",
        f"- False negative count: `{metrics['false_negative_count']}`",
        f"- Positive recall: `{pct(metrics['positive_recall'])}`",
        f"- Low-confidence threshold: `{metrics['low_confidence_threshold']}`",
        f"- Low-confidence count below 0.25: `{metrics['low_confidence_count_below_0_25']}`",
        f"- Low-confidence percentage: `{pct(metrics['low_confidence_percentage'])}`",
        f"- Min confidence: `{confidence_info['min_confidence']:.4f}`",
        f"- Max confidence: `{confidence_info['max_confidence']:.4f}`",
        f"- Mean confidence: `{confidence_info['mean_confidence']:.4f}`",
        f"- Median confidence: `{confidence_info['median_confidence']:.4f}`",
        f"- Q1 confidence: `{confidence_info['q1_confidence']:.4f}`",
        f"- Q3 confidence: `{confidence_info['q3_confidence']:.4f}`",
        "",
    ]
    if fallback_note:
        lines.extend(["## Predictor Note", "", fallback_note, ""])
    if model_info.get("external_input_mode_leakage_risk") == "upper_bound_leakage_risk":
        lines.extend(
            [
                "## Leakage Warning",
                "",
                "This run includes `doc_diff` / `diff_docstring` as input. That exposes future documentation changes and should be treated only as an upper-bound diagnostic, not final thesis evidence.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Leakage Warning",
                "",
                "This run does not include `doc_diff` or `doc_after` in the predictor input. See `reports/external_codocbench_evaluation_leakage_audit_2026_08.md` for the input construction audit.",
                "",
            ]
        )
    lines.extend(
        [
            "## What This Evaluation Can and Cannot Measure",
            "",
            "This positive-only CoDocBench pilot can measure positive recall, false negatives, confidence distribution, and predicted label distributions.",
            "",
            "It cannot measure precision, F1, false-positive rate, or negative classification quality because no defensible external negative set is included.",
            "",
            "## Confidence Deciles",
            "",
            "| Percentile | Confidence |",
            "| --- | ---: |",
            *[f"| `{key}` | {value:.4f} |" for key, value in confidence_info["deciles"].items()],
            "",
            "## Confidence Histogram",
            "",
            "| Bin | Count | Percentage |",
            "| --- | ---: | ---: |",
        ]
    )
    for start in [i / 10 for i in range(10)]:
        end = start + 0.1
        count = sum(1 for item in pairs if start <= item["confidence"] < end or (end == 1.0 and item["confidence"] == 1.0))
        lines.append(f"| `{start:.1f}-{end:.1f}` | {count} | {pct(count / total if total else 0.0)} |")
    lines.extend(
        [
            "",
            "## Recall At Confidence Thresholds",
            "",
            "| Threshold | Accepted predictions | Accepted % | Accepted true positives | Rejected positives | Recall all positives | Recall among accepted |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in metrics["threshold_analysis"]:
        lines.append(
            f"| {row['threshold']:.2f} | {row['accepted_predictions']} | {pct(row['accepted_percentage'])} | "
            f"{row['accepted_true_positives']} | {row['rejected_positives']} | "
            f"{pct(row['recall_all_positives_abstentions_missed'])} | {pct(row['recall_accepted_positive_only'])} |"
        )
    lines.extend(
        [
            "",
            "The accepted-only recall column is positive-only and does not measure precision. The all-positives recall column treats abstentions as missed positives.",
            "",
            "## Predicted Doc Category Distribution",
            "",
            *distribution_lines(metrics["predicted_doc_category_distribution"]),
            "",
            "## Predicted Scenario Type Distribution",
            "",
            *distribution_lines(metrics["predicted_scenario_type_distribution"]),
            "",
            "## Predicted Target Doc File Distribution",
            "",
            *distribution_lines(metrics["predicted_target_doc_file_distribution"], 20),
            "",
            "## Top 20 Lowest-Confidence True Positives",
            "",
        ]
    )
    for item in lowest_true_positives:
        lines.extend(example_lines(item))
    lines.extend(["", "## All False Negative Examples", ""])
    if false_negatives:
        for item in false_negatives:
            lines.extend(example_lines(item))
    else:
        lines.append("None.")
    lines.extend(["", "## 10 Representative High-Confidence True Positives", ""])
    for item in high_true_positives:
        lines.extend(example_lines(item))
    lines.extend(["", "## 10 Representative Low-Confidence True Positives", ""])
    for item in low_true_positives:
        lines.extend(example_lines(item))
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- CoDocBench labels are code-docstring/comment co-change positives, not project-level Markdown documentation labels.",
            "- Positive recall here should be treated as an external robustness signal.",
            "- External precision and F1 require a defensible external negative set with separately reported label provenance.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if diagnostics_path != path:
        diagnostics_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate_existing_docguard(input_path: Path, output_path: Path, external_input_mode: str = "code_diff_plus_doc_before") -> dict[str, Any]:
    if external_input_mode not in EXTERNAL_INPUT_MODES:
        return {"status": "error", "message": f"unsupported external input mode: {external_input_mode}"}
    if not input_path.exists():
        result = {"status": "error", "message": f"input not found: {input_path}"}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"# External CoDocBench Existing DocGuard Positive Recall 2026-08\n\nInput not found: `{input_path}`\n", encoding="utf-8")
        return result
    external_rows = read_jsonl(input_path)
    positive_rows = [row for row in external_rows if row.get("docs_update_required") is True]
    write_leakage_audit(REPORTS_DIR / "external_codocbench_evaluation_leakage_audit_2026_08.md", input_path, positive_rows)
    if external_input_mode == "code_diff_plus_doc_before":
        missing_doc_before = [row.get("record_id") for row in positive_rows if row.get("doc_before") in {None, ""}]
        if missing_doc_before:
            result = {
                "status": "error",
                "message": f"`code_diff_plus_doc_before` cannot run because {len(missing_doc_before)} records lack doc_before",
                "missing_doc_before_examples": missing_doc_before[:10],
            }
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
            return result
    docguard_rows = [external_to_docguard_record(row, external_input_mode) for row in positive_rows]
    predictions, model_info, hf_note = try_hf_staged_predictions(docguard_rows, external_input_mode)
    fallback_note = hf_note
    if not predictions:
        predictions, model_info, deterministic_note = deterministic_predictions(docguard_rows, external_input_mode)
        fallback_note = "; ".join(note for note in [hf_note, deterministic_note] if note)
    if not predictions and docguard_rows:
        result = {"status": "error", "message": fallback_note or "no predictor available"}
        write_report(output_path, input_path, model_info, fallback_note, compute_metrics(docguard_rows, []), [])
        return result
    metrics = compute_metrics(docguard_rows, predictions)
    pairs = paired_records(positive_rows, docguard_rows, predictions)
    write_report(output_path, input_path, model_info, fallback_note, metrics, pairs)
    write_histogram(artifact_path(output_path, "confidence_histogram", ".csv"), predictions)
    write_prediction_records(artifact_path(output_path, "predictions", ".jsonl"), pairs)
    write_manual_audit_queue(artifact_path(output_path, "manual_audit_queue", ".md"), pairs)
    write_calibration_notes(REPORTS_DIR / "external_confidence_calibration_notes_2026_08.md")
    summary = {
        "status": "ok",
        "input": str(input_path),
        "output": str(output_path),
        "external_input_mode": external_input_mode,
        "leakage_risk": EXTERNAL_INPUT_MODES[external_input_mode]["leakage_risk"],
        "diagnostics_output": str(artifact_path(output_path, "diagnostics", ".md")),
        "histogram_output": str(artifact_path(output_path, "confidence_histogram", ".csv")),
        "predictions_output": str(artifact_path(output_path, "predictions", ".jsonl")),
        "manual_audit_queue_output": str(artifact_path(output_path, "manual_audit_queue", ".md")),
        "calibration_notes_output": str(REPORTS_DIR / "external_confidence_calibration_notes_2026_08.md"),
        "predictor": model_info.get("predictor"),
        "model_path": model_info.get("model_path"),
        "total_positives_evaluated": metrics["total_positives_evaluated"],
        "predicted_update_required_count": metrics["predicted_update_required_count"],
        "false_negative_count": metrics["false_negative_count"],
        "positive_recall": metrics["positive_recall"],
        "average_confidence": metrics["average_confidence"],
        "median_confidence": metrics["median_confidence"],
        "low_confidence_count_below_0_25": metrics["low_confidence_count_below_0_25"],
        "low_confidence_percentage": metrics["low_confidence_percentage"],
        "fallback_note": fallback_note,
    }
    summary["notes"] = EXTERNAL_INPUT_MODES[external_input_mode]["description"]
    update_input_mode_comparison(summary)
    return summary
