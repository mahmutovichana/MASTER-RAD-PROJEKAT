from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from docguard_ml.predict import load_model, predict

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


def evaluate(split: str) -> dict:
    model = load_model()
    records = read_jsonl(DATA_DIR / f"{split}.jsonl")
    tp = fp = fn = tn = pos = cat = target = scenario = neg = neg_ok = 0
    per_scenario: dict[str, Counter] = defaultdict(Counter)
    per_category: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        pred = predict(record, model)
        gold = bool(record["docs_update_required"])
        got = bool(pred["docs_update_required"])
        if gold and got: tp += 1
        elif not gold and got: fp += 1
        elif gold and not got: fn += 1
        else: tn += 1
        if gold:
            pos += 1
            cat += int(pred["doc_category"] == record["doc_category"])
            target += int(pred["target_doc_file"] == record["target_doc_file"])
            scenario += int(pred["scenario_type"] == record["scenario_type"])
        else:
            neg += 1
            neg_ok += int(not got and pred["doc_category"] == "no_update")
        per_scenario[record["scenario_type"]]["total"] += 1
        per_scenario[record["scenario_type"]]["correct"] += int(pred["scenario_type"] == record["scenario_type"])
        per_category[record["doc_category"]]["total"] += 1
        per_category[record["doc_category"]]["correct"] += int(pred["doc_category"] == record["doc_category"])
    p, r, f1 = binary(tp, fp, fn)
    metrics = {
        "ml_backend": model.get("backend", "fallback"),
        "total_records": len(records),
        "docs_update_required_precision": p,
        "docs_update_required_recall": r,
        "docs_update_required_f1": f1,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "positive_doc_category_accuracy": cat / pos if pos else 0.0,
        "positive_target_doc_file_accuracy": target / pos if pos else 0.0,
        "positive_scenario_type_accuracy": scenario / pos if pos else 0.0,
        "negative_classification_accuracy": neg_ok / neg if neg else 0.0,
        "macro_scenario_f1": sum(v["correct"] / v["total"] for v in per_scenario.values()) / len(per_scenario),
        "macro_doc_category_f1": sum(v["correct"] / v["total"] for v in per_category.values()) / len(per_category),
        "per_scenario": dict(per_scenario),
        "per_doc_category": dict(per_category),
    }
    return metrics


def write_reports(metrics: dict) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    lines = ["# ML Evaluation v0.4", "", "| Metric | Value |", "| --- | ---: |"]
    for key, value in metrics.items():
        if key.startswith("per_"):
            continue
        lines.append(f"| `{key}` | {value:.4f} |" if isinstance(value, float) else f"| `{key}` | {value} |")
    (REPORTS_DIR / "ml_evaluation_v0_4.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for name, filename in [("per_scenario", "ml_per_scenario_v0_4.md"), ("per_doc_category", "ml_per_doc_category_v0_4.md")]:
        rows = [f"# {name} v0.4", "", "| Label | Support | Correct | Accuracy |", "| --- | ---: | ---: | ---: |"]
        for label, counts in sorted(metrics[name].items()):
            acc = counts["correct"] / counts["total"] if counts["total"] else 0.0
            rows.append(f"| `{label}` | {counts['total']} | {counts['correct']} | {acc:.4f} |")
        (REPORTS_DIR / filename).write_text("\n".join(rows) + "\n", encoding="utf-8")
