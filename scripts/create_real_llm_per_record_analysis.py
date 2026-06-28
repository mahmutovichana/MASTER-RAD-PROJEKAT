from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docguard_llm.evaluator import evaluate_predictions, read_jsonl, write_model_report
from docguard_llm.label_normalizer import add_normalized_fields


DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
MODEL_KEY = "qwen2_5_coder_0_5b"
PREDICTION_PATH = DATA_DIR / f"llm_predictions_v0_3_validation_transformers_local_{MODEL_KEY}.jsonl"
REPORT_PATH = REPORTS_DIR / f"real_llm_per_record_analysis_v0_3_{MODEL_KEY}.md"
EVAL_REPORT_PATH = REPORTS_DIR / f"llm_evaluation_v0_3_transformers_local_{MODEL_KEY}.md"


def excerpt(text: str, limit: int = 700) -> str:
    text = text or ""
    return text if len(text) <= limit else text[:limit] + "\n..."


def classify(record: dict, prediction: dict) -> str:
    if prediction.get("parse_error"):
        return "parse failure"
    gold = bool(record["docs_update_required"])
    pred = bool(prediction["docs_update_required"])
    if gold and not pred:
        return "false negative"
    if not gold and pred:
        return "false positive"
    category_ok = prediction["normalized_doc_category"] == record["doc_category"]
    target_ok = prediction["normalized_target_doc_file"] == record["target_doc_file"]
    scenario_ok = prediction["normalized_scenario_type"] == record["scenario_type"]
    if scenario_ok and category_ok and target_ok:
        return "correct"
    if category_ok and target_ok:
        return "semantically close"
    if category_ok and not target_ok:
        return "wrong target file"
    if not category_ok and target_ok:
        return "wrong category"
    return "wrong category and target file"


def main() -> int:
    predictions = read_jsonl(PREDICTION_PATH)
    records = read_jsonl(DATA_DIR / "validation.jsonl")[: len(predictions)]
    enriched = [add_normalized_fields(prediction, record) for record, prediction in zip(records, predictions)]
    metrics = evaluate_predictions(records, enriched)
    write_model_report(EVAL_REPORT_PATH, MODEL_KEY, "validation", "transformers_local", metrics)
    lines = [
        f"# Real LLM Per-Record Analysis v0.3: {MODEL_KEY}",
        "",
        f"- prediction_file: `{PREDICTION_PATH.relative_to(ROOT)}`",
        f"- records: {len(enriched)}",
        f"- docs_update_required F1: {metrics['docs_update_required_f1']:.2%}",
        f"- doc_category accuracy: {metrics['doc_category_accuracy']:.2%}",
        f"- target_doc_file accuracy: {metrics['target_doc_file_accuracy']:.2%}",
        f"- scenario_type accuracy: {metrics['scenario_type_accuracy']:.2%}",
        f"- parse errors: {metrics['parse_error_count']}",
        f"- average latency seconds: {metrics['average_latency_seconds']:.2f}" if metrics["average_latency_seconds"] is not None else "- average latency seconds: n/a",
        "",
    ]
    for index, (record, prediction) in enumerate(zip(records, enriched), start=1):
        lines.extend([
            f"## {index}. {record['id']}",
            "",
            f"- gold docs_update_required: `{record['docs_update_required']}`",
            f"- predicted docs_update_required: `{prediction['docs_update_required']}`",
            f"- gold scenario_type: `{record['scenario_type']}`",
            f"- raw scenario_type: `{prediction.get('raw_scenario_type', prediction.get('scenario_type', ''))}`",
            f"- normalized scenario_type: `{prediction['normalized_scenario_type']}`",
            f"- gold doc_category: `{record['doc_category']}`",
            f"- raw doc_category: `{prediction.get('raw_doc_category', prediction.get('doc_category', ''))}`",
            f"- normalized doc_category: `{prediction['normalized_doc_category']}`",
            f"- gold target_doc_file: `{record['target_doc_file']}`",
            f"- raw target_doc_file: `{prediction.get('raw_target_doc_file', prediction.get('target_doc_file', ''))}`",
            f"- normalized target_doc_file: `{prediction['normalized_target_doc_file']}`",
            f"- parse_error: `{prediction.get('parse_error')}`",
            f"- latency_seconds: `{prediction.get('latency_seconds')}`",
            f"- interpretation: **{classify(record, prediction)}**",
            "",
            "Raw output excerpt:",
            "",
            "```text",
            excerpt(prediction.get("raw_model_output", "")),
            "```",
            "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    # Keep enriched rows in place so downstream figure/report generation sees normalized fields.
    PREDICTION_PATH.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in enriched) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
