from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from docguard_llm.llm_agent import predict
from docguard_llm.model_registry import list_models
from docguard_llm.prompt_builder import DATA_DIR, select_few_shot_examples


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
RULE_BASED_V03 = {
    "docs_update_required_precision": 1.0,
    "docs_update_required_recall": 0.5422,
    "docs_update_required_f1": 0.7032,
    "scenario_type_accuracy": 0.072,
    "doc_category_accuracy": 0.072,
    "target_doc_file_accuracy": 0.336,
    "patch_fact_coverage": 0.1169,
}

MOCK_WARNING = (
    "Important: This report was generated with the mock backend. Mock results validate the DocGuard LLM pipeline, "
    "but they do not represent real Hugging Face model quality. Real model results must be generated with "
    "transformers_local or text_generation_inference backends."
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def split_path(split: str) -> Path:
    if split not in {"train", "validation", "test"}:
        raise ValueError("split must be train, validation, or test")
    return DATA_DIR / f"{split}.jsonl"


def binary_metrics(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def fact_covered(fact: str, prediction: dict) -> bool:
    text = " ".join(str(prediction.get(k) or "") for k in ["generated_doc_patch", "change_intent_summary", "primary_documentation_reason"])
    text += " " + " ".join(prediction.get("expected_facts_covered") or [])
    tokens = [t for t in re.split(r"[^A-Za-z0-9_]+", fact.lower()) if len(t) >= 4]
    return bool(tokens) and any(token in text.lower() for token in tokens)


def hallucination_count(record: dict, prediction: dict) -> int:
    patch = prediction.get("generated_doc_patch") or ""
    diff = record.get("code_diff", "")
    count = 0
    if "Authentication:" in patch and "require" not in diff:
        count += 1
    if "FEATURE_FLAG" in patch and "FEATURE_FLAG" not in diff:
        count += 1
    return count


def evaluate_predictions(records: list[dict], predictions: list[dict]) -> dict:
    tp = fp = fn = tn = 0
    scenario_correct = category_correct = target_correct = parse_errors = hallucinations = 0
    confidence_sum = latency_sum = latency_count = 0.0
    covered = total_facts = 0
    per_scenario: dict[str, Counter] = defaultdict(Counter)
    per_category: dict[str, Counter] = defaultdict(Counter)
    for record, prediction in zip(records, predictions):
        gold = bool(record["docs_update_required"])
        pred = bool(prediction["docs_update_required"])
        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif gold and not pred:
            fn += 1
        else:
            tn += 1
        if prediction["scenario_type"] == record["scenario_type"]:
            scenario_correct += 1
            per_scenario[record["scenario_type"]]["correct"] += 1
        if prediction["doc_category"] == record["doc_category"]:
            category_correct += 1
            per_category[record["doc_category"]]["correct"] += 1
        if prediction["target_doc_file"] == record["target_doc_file"]:
            target_correct += 1
        for fact in record["expected_facts"]:
            total_facts += 1
            if fact_covered(fact, prediction):
                covered += 1
        parse_errors += int(bool(prediction["parse_error"]))
        hallucinations += hallucination_count(record, prediction)
        confidence_sum += float(prediction.get("confidence") or 0.0)
        if prediction.get("latency_seconds") is not None:
            latency_sum += float(prediction["latency_seconds"])
            latency_count += 1
        per_scenario[record["scenario_type"]]["total"] += 1
        per_category[record["doc_category"]]["total"] += 1
    binary = binary_metrics(tp, fp, fn)
    total = len(records) or 1
    return {
        "total_records": len(records),
        "docs_update_required_precision": binary["precision"],
        "docs_update_required_recall": binary["recall"],
        "docs_update_required_f1": binary["f1"],
        "scenario_type_accuracy": scenario_correct / total,
        "doc_category_accuracy": category_correct / total,
        "target_doc_file_accuracy": target_correct / total,
        "patch_fact_coverage": covered / total_facts if total_facts else 0.0,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "hallucination_count": hallucinations,
        "parse_error_count": parse_errors,
        "average_confidence": confidence_sum / total,
        "average_latency_seconds": latency_sum / latency_count if latency_count else None,
        "true_positive_count": tp,
        "true_negative_count": tn,
        "per_scenario": {k: {"total": v["total"], "correct": v["correct"], "accuracy": v["correct"] / v["total"] if v["total"] else 0.0} for k, v in sorted(per_scenario.items())},
        "per_doc_category": {k: {"total": v["total"], "correct": v["correct"], "accuracy": v["correct"] / v["total"] if v["total"] else 0.0} for k, v in sorted(per_category.items())},
    }


def evaluate_model(split: str, model_key: str, backend: str, limit: int | None = None, compact_prompt: bool = False) -> tuple[dict, list[dict]]:
    records = read_jsonl(split_path(split))
    if limit:
        records = records[:limit]
    examples = select_few_shot_examples()
    predictions = [predict(record, model_key, backend, examples, compact_prompt=compact_prompt) for record in records]
    return evaluate_predictions(records, predictions), predictions


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def fmt(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.2f}%" if value <= 1 else f"{value:.3f}"


def write_model_report(path: Path, model_key: str, split: str, backend: str, metrics: dict) -> None:
    lines = [
        f"# LLM Evaluation v0.3: {model_key}",
        "",
    ]
    if backend == "mock":
        lines.extend([f"> {MOCK_WARNING}", ""])
    lines.extend([
        f"- split: {split}",
        f"- backend: {backend}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Records | {metrics['total_records']} |",
        f"| docs_update_required precision | {fmt(metrics['docs_update_required_precision'])} |",
        f"| docs_update_required recall | {fmt(metrics['docs_update_required_recall'])} |",
        f"| docs_update_required F1 | {fmt(metrics['docs_update_required_f1'])} |",
        f"| scenario_type accuracy | {fmt(metrics['scenario_type_accuracy'])} |",
        f"| doc_category accuracy | {fmt(metrics['doc_category_accuracy'])} |",
        f"| target_doc_file accuracy | {fmt(metrics['target_doc_file_accuracy'])} |",
        f"| patch fact coverage | {fmt(metrics['patch_fact_coverage'])} |",
        f"| false positives | {metrics['false_positive_count']} |",
        f"| false negatives | {metrics['false_negative_count']} |",
        f"| hallucinations | {metrics['hallucination_count']} |",
        f"| parse errors | {metrics['parse_error_count']} |",
        f"| average confidence | {fmt(metrics['average_confidence'])} |",
        f"| average latency seconds | {metrics['average_latency_seconds'] or 0:.4f} |",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison_report(path: Path, split: str, model_metrics: dict[str, dict], backend: str = "mock") -> None:
    metrics = [
        "docs_update_required_precision",
        "docs_update_required_recall",
        "docs_update_required_f1",
        "scenario_type_accuracy",
        "doc_category_accuracy",
        "target_doc_file_accuracy",
        "patch_fact_coverage",
    ]
    keys = list(list_models())
    lines = ["# LLM Model Comparison v0.3", ""]
    if backend == "mock":
        lines.extend([f"> {MOCK_WARNING}", ""])
    model_headers = " | ".join(keys)
    model_alignment = " | ".join("---:" for _ in keys)
    lines.extend([
        f"Split: `{split}`",
        f"Backend: `{backend}`",
        "",
        f"| Metric | rule_based_v0_3 | {model_headers} | Best model | Interpretation |",
        f"| --- | ---: | {model_alignment} | --- | --- |",
    ])
    for metric in metrics:
        values = {key: model_metrics.get(key, {}).get(metric, 0.0) for key in keys}
        best = max(values, key=values.get)
        model_cells = " | ".join(fmt(values[key]) for key in keys)
        lines.append(
            f"| `{metric}` | {fmt(RULE_BASED_V03.get(metric, 0.0))} | {model_cells} | `{best}` | Mock backend validates plumbing; real model runs should replace these values. |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
