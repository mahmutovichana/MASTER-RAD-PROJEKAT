from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from docguard_hf_classifier.dataset_export import HF_DATA_DIR, read_jsonl
from docguard_hf_classifier.embedding_classifier import evaluate as evaluate_embeddings
from docguard_hybrid.doc_router import route

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


def write_error_analysis(split: str = "validation") -> None:
    metrics, predictions = evaluate_embeddings(split)
    rows = read_jsonl(HF_DATA_DIR / f"{split}.jsonl")
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

