from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from docguard_hybrid.hybrid_agent import predict
from docguard_hybrid.validator import validate_prediction

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def binary(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1


def evaluate_records(records: list[dict], decision_source: str = "router", hf_predictions_by_id: dict[str, dict] | None = None) -> tuple[dict, list[dict]]:
    predictions = [
        validate_prediction(predict(record, hf_prediction=(hf_predictions_by_id or {}).get(record["id"]) if decision_source == "hf_embedding" else None))
        for record in records
    ]
    tp = fp = fn = tn = 0
    pos_total = pos_cat = pos_target = pos_scenario = facts_total = facts_covered = 0
    neg_total = neg_correct = neg_reason = 0
    per_scenario: dict[str, Counter] = defaultdict(Counter)
    per_category: dict[str, Counter] = defaultdict(Counter)
    corrected = invalid = deterministic = llm_rewrite = 0
    router_ml_agree = router_llm_agree = router_hf_agree = 0
    latencies = []
    for record, pred in zip(records, predictions):
        gold = bool(record["docs_update_required"])
        got = bool(pred["docs_update_required"])
        if gold and got: tp += 1
        elif not gold and got: fp += 1
        elif gold and not got: fn += 1
        else: tn += 1
        if gold:
            pos_total += 1
            pos_cat += int(pred["doc_category"] == record["doc_category"])
            pos_target += int(pred["target_doc_file"] == record["target_doc_file"])
            pos_scenario += int(pred["scenario_type"] == record["scenario_type"])
            for fact in record.get("expected_facts", []):
                facts_total += 1
                facts_covered += int(fact.split()[0].lower() in (pred.get("generated_doc_patch") or "").lower())
        else:
            neg_total += 1
            neg_correct += int(not got and pred["doc_category"] == "no_update")
            neg_reason += int(bool(record.get("negative_reason")))
        per_scenario[record["scenario_type"]]["total"] += 1
        per_scenario[record["scenario_type"]]["correct"] += int(pred["scenario_type"] == record["scenario_type"])
        per_category[record["doc_category"]]["total"] += 1
        per_category[record["doc_category"]]["correct"] += int(pred["doc_category"] == record["doc_category"])
        corrected += int(bool(pred.get("corrected_target_doc_file")))
        invalid += int(bool(pred.get("invalid_source_file_target")))
        deterministic += int(bool(pred.get("deterministic_patch_used")))
        llm_rewrite += int(bool(pred.get("llm_patch_rewrite_used")))
        router_ml_agree += int(bool(pred.get("router_ml_agree")))
        router_llm_agree += int(bool(pred.get("router_llm_agree")))
        router_hf_agree += int(bool(pred.get("router_hf_agree")))
        latencies.append(float(pred.get("latency_seconds") or 0.0))
    precision, recall, f1 = binary(tp, fp, fn)
    sorted_latencies = sorted(latencies)
    def pct(p: float) -> float:
        if not sorted_latencies:
            return 0.0
        return sorted_latencies[min(len(sorted_latencies) - 1, int((len(sorted_latencies) - 1) * p))]
    metrics = {
        "total_records": len(records),
        "docs_update_required_precision": precision,
        "docs_update_required_recall": recall,
        "docs_update_required_f1": f1,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "true_positive_count": tp,
        "true_negative_count": tn,
        "positive_doc_category_accuracy": pos_cat / pos_total if pos_total else 0.0,
        "positive_target_doc_file_accuracy": pos_target / pos_total if pos_total else 0.0,
        "positive_scenario_type_accuracy": pos_scenario / pos_total if pos_total else 0.0,
        "positive_patch_fact_coverage": facts_covered / facts_total if facts_total else 0.0,
        "negative_classification_accuracy": neg_correct / neg_total if neg_total else 0.0,
        "false_positive_rate": fp / neg_total if neg_total else 0.0,
        "negative_reason_available_rate": neg_reason / neg_total if neg_total else 0.0,
        "macro_scenario_f1": sum(v["correct"] / v["total"] for v in per_scenario.values()) / len(per_scenario),
        "macro_doc_category_f1": sum(v["correct"] / v["total"] for v in per_category.values()) / len(per_category),
        "per_scenario": dict(per_scenario),
        "per_doc_category": dict(per_category),
        "average_latency_seconds": sum(latencies) / len(latencies) if latencies else 0.0,
        "p50_latency_seconds": pct(0.5),
        "p95_latency_seconds": pct(0.95),
        "router_llm_agreement_rate": router_llm_agree / len(records) if records else 0.0,
        "router_ml_agreement_rate": router_ml_agree / len(records) if records else 0.0,
        "router_hf_agreement_rate": router_hf_agree / len(records) if records else 0.0,
        "corrected_target_doc_file_count": corrected,
        "invalid_source_file_target_count": invalid,
        "deterministic_patch_used_count": deterministic,
        "llm_patch_rewrite_used_count": llm_rewrite,
        "decision_source": decision_source,
    }
    return metrics, predictions


def write_report(path: Path, metrics: dict) -> None:
    lines = ["# Hybrid Evaluation v0.4", "", "| Metric | Value |", "| --- | ---: |"]
    for key, value in metrics.items():
        if key.startswith("per_"):
            continue
        lines.append(f"| `{key}` | {value:.4f} |" if isinstance(value, float) else f"| `{key}` | {value} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
