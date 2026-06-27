from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from docguard.change_classifier import classify_facts
from docguard.diff_analyzer import analyze_record
from docguard.patch_generator import generate_patch


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def predict_record(record: dict) -> dict:
    facts = analyze_record(record)
    classification = classify_facts(facts)
    patch = generate_patch(
        facts,
        str(classification["scenario_type"]),
        bool(classification["docs_update_required"]),
    )
    predicted_scenario = str(classification["scenario_type"])
    predicted_docs = bool(classification["docs_update_required"])
    predicted_category = "api_reference" if predicted_scenario in {
        "new_endpoint",
        "changed_validation_min",
        "changed_auth_requirement",
        "added_response_field",
        "internal_refactor",
    } else "unknown"
    return {
        "id": record["id"],
        "project_id": record["project_id"],
        "docs_update_required": predicted_docs,
        "docs_update_score": 0.5 if predicted_scenario == "unknown_change" else 1.0 if predicted_docs else 0.0,
        "scenario_type": predicted_scenario,
        "doc_category": predicted_category,
        "target_doc_file": classification["target_doc_file"],
        "generated_doc_patch": patch,
        "facts": {
            "method": facts.method,
            "full_path": facts.full_path,
            "field": facts.field,
            "old_min": facts.old_min,
            "new_min": facts.new_min,
            "middleware": facts.middleware,
            "auth_description": facts.auth_description,
        },
    }


def binary_metrics(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def fact_covered(fact: str, prediction: dict) -> bool:
    patch = prediction.get("generated_doc_patch") or ""
    facts = prediction.get("facts", {})
    searchable = " ".join(str(value) for value in [patch, *facts.values()] if value is not None).lower()
    tokens = [
        token
        for token in re.split(r"[^A-Za-z0-9_]+", fact.lower())
        if len(token) >= 3 and token not in {"the", "and", "for", "with", "this", "that"}
    ]
    if not tokens:
        return True
    return any(token in searchable for token in tokens)


def patch_fact_coverage(records: list[dict], predictions: list[dict]) -> float:
    total = 0
    covered = 0
    for record, prediction in zip(records, predictions):
        for fact in record.get("expected_facts", []):
            total += 1
            if fact_covered(fact, prediction):
                covered += 1
    return covered / total if total else 0.0


def hallucination_count(record: dict, prediction: dict) -> int:
    patch = prediction.get("generated_doc_patch") or ""
    diff = record.get("code_diff", "")
    expected_text = " ".join(record.get("expected_facts", [])).lower()
    count = 0

    if "Authentication:" in patch and not re.search(r"require\w+", diff):
        count += 1
    if "### " in patch and not re.search(r"\+\w+Router\.(get|post|put|patch|delete)\(", diff):
        count += 1

    field_mentions = re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", patch)
    for field in field_mentions:
        if field in {"id", "name", "status"}:
            continue
        if field not in diff and field.lower() not in expected_text:
            count += 1
    return count


def evaluate_records(records: list[dict]) -> tuple[dict, list[dict]]:
    predictions = [predict_record(record) for record in records]

    tp = fp = fn = tn = 0
    scenario_correct = 0
    target_doc_correct = 0
    false_positive_count = 0
    false_negative_count = 0
    hallucinations = 0
    unknown_count = 0
    known_total = 0
    known_correct = 0
    per_scenario: dict[str, Counter] = defaultdict(Counter)
    per_category: dict[str, Counter] = defaultdict(Counter)
    doc_category_correct = 0
    known_scenarios = {
        "new_endpoint",
        "changed_validation_min",
        "changed_auth_requirement",
        "added_response_field",
        "internal_refactor",
    }

    for record, prediction in zip(records, predictions):
        gold_docs = bool(record["docs_update_required"])
        pred_docs = bool(prediction["docs_update_required"])
        if gold_docs and pred_docs:
            tp += 1
        elif not gold_docs and pred_docs:
            fp += 1
            false_positive_count += 1
        elif gold_docs and not pred_docs:
            fn += 1
            false_negative_count += 1
        else:
            tn += 1

        if prediction["scenario_type"] == record["scenario_type"]:
            scenario_correct += 1
            per_scenario[record["scenario_type"]]["correct"] += 1
        if prediction["scenario_type"] == "unknown_change":
            unknown_count += 1
        if record["scenario_type"] in known_scenarios:
            known_total += 1
            if prediction["scenario_type"] == record["scenario_type"]:
                known_correct += 1
        per_scenario[record["scenario_type"]]["total"] += 1
        if prediction.get("doc_category") == record.get("doc_category"):
            doc_category_correct += 1
            per_category[record["doc_category"]]["correct"] += 1
        per_category[record["doc_category"]]["total"] += 1

        if prediction["target_doc_file"] == record["target_doc_file"]:
            target_doc_correct += 1
        hallucinations += hallucination_count(record, prediction)

    docs_metrics = binary_metrics(tp, fp, fn)
    metrics = {
        "total_records": len(records),
        "docs_update_required_precision": docs_metrics["precision"],
        "docs_update_required_recall": docs_metrics["recall"],
        "docs_update_required_f1": docs_metrics["f1"],
        "scenario_type_accuracy": scenario_correct / len(records) if records else 0.0,
        "known_scenario_accuracy": known_correct / known_total if known_total else 0.0,
        "unknown_unsupported_scenario_count": unknown_count,
        "doc_category_accuracy": doc_category_correct / len(records) if records else 0.0,
        "target_doc_file_accuracy": target_doc_correct / len(records) if records else 0.0,
        "patch_fact_coverage": patch_fact_coverage(records, predictions),
        "false_positive_count": false_positive_count,
        "false_negative_count": false_negative_count,
        "hallucination_count": hallucinations,
        "true_positive_count": tp,
        "true_negative_count": tn,
    }
    metrics["per_scenario"] = {
        scenario: {
            "total": counts["total"],
            "correct": counts["correct"],
            "accuracy": counts["correct"] / counts["total"] if counts["total"] else 0.0,
        }
        for scenario, counts in sorted(per_scenario.items())
    }
    metrics["per_doc_category"] = {
        category: {
            "total": counts["total"],
            "correct": counts["correct"],
            "accuracy": counts["correct"] / counts["total"] if counts["total"] else 0.0,
        }
        for category, counts in sorted(per_category.items())
    }
    return metrics, predictions


def split_path(split: str) -> Path:
    if split not in {"train", "validation", "test"}:
        raise ValueError("split must be one of: train, validation, test")
    return DATA_DIR / f"{split}.jsonl"


def evaluate_split(split: str) -> tuple[dict, list[dict]]:
    return evaluate_records(read_jsonl(split_path(split)))


def write_predictions(path: Path, predictions: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(prediction, ensure_ascii=False) for prediction in predictions) + "\n",
        encoding="utf-8",
    )


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_report(path: Path, split: str, metrics: dict, version: str = "v0_3") -> None:
    display_version = version.replace("_", ".")
    v01 = {
        "docs_update_required_precision": 1.0,
        "docs_update_required_recall": 1.0,
        "docs_update_required_f1": 1.0,
        "scenario_type_accuracy": 1.0,
        "target_doc_file_accuracy": 1.0,
        "patch_fact_coverage": 0.8,
        "false_positive_count": 0,
        "false_negative_count": 0,
        "hallucination_count": 0,
    }
    lines = [
        "# Baseline Evaluation",
        "",
        f"- Dataset version used: {display_version}",
        f"- Split evaluated: {split}",
        "",
        "## Metric Table",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Records | {metrics['total_records']} |",
        f"| docs_update_required precision | {format_percent(metrics['docs_update_required_precision'])} |",
        f"| docs_update_required recall | {format_percent(metrics['docs_update_required_recall'])} |",
        f"| docs_update_required F1 | {format_percent(metrics['docs_update_required_f1'])} |",
        f"| scenario_type accuracy | {format_percent(metrics['scenario_type_accuracy'])} |",
        f"| known-scenario accuracy | {format_percent(metrics['known_scenario_accuracy'])} |",
        f"| unknown/unsupported scenario count | {metrics['unknown_unsupported_scenario_count']} |",
        f"| doc_category accuracy | {format_percent(metrics['doc_category_accuracy'])} |",
        f"| target_doc_file accuracy | {format_percent(metrics['target_doc_file_accuracy'])} |",
        f"| patch fact coverage | {format_percent(metrics['patch_fact_coverage'])} |",
        f"| false positives | {metrics['false_positive_count']} |",
        f"| false negatives | {metrics['false_negative_count']} |",
        f"| hallucination count | {metrics['hallucination_count']} |",
        "",
        f"## v0.1 vs {display_version} Comparison",
        "",
        f"| Metric | v0.1 value | {display_version} value | Interpretation |",
        "| --- | ---: | ---: | --- |",
        f"| docs_update_required precision | {format_percent(v01['docs_update_required_precision'])} | {format_percent(metrics['docs_update_required_precision'])} | Measures how often predicted documentation updates are correct. |",
        f"| docs_update_required recall | {format_percent(v01['docs_update_required_recall'])} | {format_percent(metrics['docs_update_required_recall'])} | Drops if unsupported positive changes are missed. |",
        f"| docs_update_required F1 | {format_percent(v01['docs_update_required_f1'])} | {format_percent(metrics['docs_update_required_f1'])} | Overall binary update-detection quality. |",
        f"| scenario_type accuracy | {format_percent(v01['scenario_type_accuracy'])} | {format_percent(metrics['scenario_type_accuracy'])} | {display_version} includes unsupported scenario types, so this should be lower. |",
        f"| target_doc_file accuracy | {format_percent(v01['target_doc_file_accuracy'])} | {format_percent(metrics['target_doc_file_accuracy'])} | All current records still target API docs. |",
        f"| patch fact coverage | {format_percent(v01['patch_fact_coverage'])} | {format_percent(metrics['patch_fact_coverage'])} | Lower coverage shows the baseline cannot generate patches for many {display_version} changes. |",
        f"| false positives | {v01['false_positive_count']} | {metrics['false_positive_count']} | Negative changes incorrectly flagged as doc updates. |",
        f"| false negatives | {v01['false_negative_count']} | {metrics['false_negative_count']} | Positive changes missed by the baseline. |",
        f"| hallucination count | {v01['hallucination_count']} | {metrics['hallucination_count']} | Unsupported changes should not trigger invented patches. |",
        "",
        "## Per-Scenario Performance",
        "",
        "| Scenario | Records | Correct | Accuracy |",
        "| --- | ---: | ---: | ---: |",
    ]
    for scenario, scenario_metrics in metrics["per_scenario"].items():
        lines.append(
            f"| `{scenario}` | {scenario_metrics['total']} | "
            f"{scenario_metrics['correct']} | {format_percent(scenario_metrics['accuracy'])} |"
        )
    lines.extend(["", "## Per-Doc-Category Performance", "", "| Category | Records | Correct | Accuracy |", "| --- | ---: | ---: | ---: |"])
    for category, category_metrics in metrics["per_doc_category"].items():
        lines.append(
            f"| `{category}` | {category_metrics['total']} | {category_metrics['correct']} | {format_percent(category_metrics['accuracy'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"The deterministic baseline remains strong on v0.1-style scenarios, but {display_version} introduces many unsupported high-level documentation change types. Those examples are intentionally classified as `unknown_change`, which makes scenario and doc-category accuracy lower and exposes where an NLP-assisted DocGuard agent should improve.",
            "",
            "## Limitations",
            "",
            "- The baseline relies on regex patterns and generated project conventions.",
            "- Auth descriptions are inferred from middleware names, not business documentation.",
            "- Generated patches are minimal and may not match the gold patch wording exactly.",
            "- The baseline is not expected to generalize to arbitrary real-world projects without additional parsing and NLP support.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
