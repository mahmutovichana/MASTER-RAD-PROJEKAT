from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import joblib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Required so joblib can load custom sklearn transformers saved from these scripts.
importlib.import_module("scripts.train_real_gold_classifier_v3_strict_raw")
importlib.import_module("scripts.train_real_doc_category_classifier_v4")

from docguard_llm.grounded_patch_generator import (
    generate_grounded_patch,
    target_file_for_category,
    target_section_for_category,
)
from docguard_llm.patch_postprocessor import postprocess_patch
from docguard_llm.patch_quality import evaluate_patch_quality
from docguard_llm.patch_verifier import verify_patch


SAFE_INPUT_FIELDS = [
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]

SUPPORTED_CATEGORY_LABELS = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

CATEGORY_ALIASES = {
    "api": "api_reference",
    "api_endpoint": "api_reference",
    "api_endpoint_change": "api_reference",
    "request_response": "api_reference",
    "request_response_change": "api_reference",
    "request_response_schema_change": "model_contract",
    "schema": "model_contract",
    "schemas": "model_contract",
    "type": "model_contract",
    "types": "model_contract",
    "interface": "model_contract",
    "interfaces": "model_contract",
    "model": "model_contract",
    "data_model": "model_contract",
    "configuration": "configuration",
    "configuration_change": "configuration",
    "config": "configuration",
    "settings": "configuration",
    "environment": "configuration",
    "env": "configuration",
    "developer_setup": "developer_setup",
    "setup": "developer_setup",
    "installation": "developer_setup",
    "install": "developer_setup",
    "cli": "developer_setup",
    "command": "developer_setup",
    "commands": "developer_setup",
    "testing": "developer_setup",
    "testing_instructions": "developer_setup",
    "testing_command_change": "developer_setup",
    "workflow": "developer_setup",
    "workflow_change": "developer_setup",
    "workflow_documentation": "developer_setup",
    "project_documentation": "developer_setup",
    "no_update": "no_update",
    "not_available": "not_available",
    "": "not_available",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc

            if not isinstance(value, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")

            rows.append(value)

    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]

    if value is None:
        return []

    return [str(value)]


def normalize_category(value: Any) -> str:
    raw = str(value or "").strip().lower()
    return CATEGORY_ALIASES.get(raw, raw if raw else "not_available")


def build_model_row(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "language": str(case.get("language") or "unknown"),
        "code_changed_files": safe_list(case.get("code_changed_files")),
        "code_diff_excerpt": str(case.get("code_diff_excerpt") or ""),
        "docs_before_excerpt": str(case.get("docs_before_excerpt") or ""),
    }


def load_binary_payload(path: Path) -> dict[str, Any]:
    payload = joblib.load(path)

    if not isinstance(payload, dict):
        raise ValueError(f"Binary model payload must be a dict: {path}")

    if "model" not in payload or "threshold" not in payload:
        raise ValueError(f"Binary model payload missing model/threshold: {path}")

    return payload


def load_category_payload(path: Path) -> dict[str, Any]:
    payload = joblib.load(path)

    if not isinstance(payload, dict):
        raise ValueError(f"Category model payload must be a dict: {path}")

    required = {"selected_models", "validation_weights", "class_multipliers", "categories"}
    missing = sorted(key for key in required if key not in payload)

    if missing:
        raise ValueError(f"Category model payload missing keys {missing}: {path}")

    return payload


def predict_binary_probability(binary_payload: dict[str, Any], row: dict[str, Any]) -> float:
    model = binary_payload["model"]
    probabilities = model.predict_proba([row])
    classifier = model.named_steps.get("classifier")
    classes = list(getattr(classifier, "classes_", []))

    if 1 not in classes:
        raise ValueError(f"Binary model classes do not contain positive class 1: {classes}")

    positive_index = classes.index(1)
    return float(probabilities[0][positive_index])


def predict_binary(binary_payload: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    probability = predict_binary_probability(binary_payload, row)
    threshold = float(binary_payload["threshold"])
    prediction = probability >= threshold

    return {
        "pred_docs_update_required": bool(prediction),
        "binary_probability": probability,
        "binary_threshold": threshold,
        "binary_model_name": str(binary_payload.get("best_model_name") or binary_payload.get("model_type") or "binary_model"),
    }


def _single_model_category_probabilities(
    model: Any,
    row: dict[str, Any],
    categories: list[str],
) -> dict[str, float]:
    classifier = model.named_steps.get("classifier")
    classes = [str(item) for item in getattr(classifier, "classes_", [])]
    probabilities = model.predict_proba([row])[0]

    raw = {
        category: float(probability)
        for category, probability in zip(classes, probabilities)
    }

    aligned = {
        category: float(raw.get(category, 0.0))
        for category in categories
    }

    total = sum(aligned.values())
    if total > 0:
        aligned = {key: value / total for key, value in aligned.items()}

    return aligned


def predict_category(category_payload: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    categories = [str(item) for item in category_payload["categories"]]
    selected_models = category_payload["selected_models"]
    weights = [float(item) for item in category_payload["validation_weights"]]
    multipliers = {
        str(key): float(value)
        for key, value in dict(category_payload["class_multipliers"]).items()
    }

    if len(weights) != len(selected_models):
        raise ValueError("Category payload has inconsistent selected_models/validation_weights lengths.")

    total_weight = sum(weights) if sum(weights) > 0 else float(len(weights))
    combined = {category: 0.0 for category in categories}

    for model_item, weight in zip(selected_models, weights):
        model = model_item["model"]
        probs = _single_model_category_probabilities(model, row, categories)

        for category in categories:
            combined[category] += float(weight) * float(probs.get(category, 0.0))

    combined = {
        category: value / total_weight
        for category, value in combined.items()
    }

    adjusted = {
        category: combined.get(category, 0.0) * multipliers.get(category, 1.0)
        for category in categories
    }

    adjusted_total = sum(adjusted.values())
    if adjusted_total > 0:
        adjusted = {
            category: value / adjusted_total
            for category, value in adjusted.items()
        }

    pred_category = max(categories, key=lambda category: adjusted.get(category, 0.0))
    ranked = [
        {"category": category, "probability": probability}
        for category, probability in sorted(adjusted.items(), key=lambda item: item[1], reverse=True)
    ]

    return {
        "pred_doc_category": pred_category,
        "category_confidence": float(adjusted.get(pred_category, 0.0)),
        "category_probabilities": adjusted,
        "category_ranked": ranked,
        "category_model_name": str(category_payload.get("model_type") or "category_model"),
    }


def evaluate_prediction(case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    gold_docs_required = bool_value(case.get("gold_docs_update_required"))
    pred_docs_required = bool(prediction["pred_docs_update_required"])

    gold_category = normalize_category(case.get("gold_doc_category"))
    pred_category = normalize_category(prediction.get("pred_doc_category"))

    binary_evaluated = "gold_docs_update_required" in case
    binary_correct = pred_docs_required == gold_docs_required if binary_evaluated else None

    category_evaluated = bool(
        binary_evaluated
        and gold_docs_required
        and pred_docs_required
        and gold_category in SUPPORTED_CATEGORY_LABELS
    )
    category_correct = pred_category == gold_category if category_evaluated else None

    return {
        "gold_docs_update_required": gold_docs_required if binary_evaluated else None,
        "gold_doc_category_normalized": gold_category,
        "binary_evaluated": binary_evaluated,
        "binary_correct": binary_correct,
        "category_evaluated": category_evaluated,
        "category_correct": category_correct,
    }


def run_one_case(
    *,
    case: dict[str, Any],
    binary_payload: dict[str, Any],
    category_payload: dict[str, Any],
    patch_mode: str,
) -> dict[str, Any]:
    model_row = build_model_row(case)
    case_id = str(case.get("case_id") or case.get("id") or "unknown_case")

    binary_prediction = predict_binary(binary_payload, model_row)

    docs_required = bool(binary_prediction["pred_docs_update_required"])
    category_prediction: dict[str, Any]

    if docs_required:
        category_prediction = predict_category(category_payload, model_row)
        pred_category = str(category_prediction["pred_doc_category"])
        target_doc_file = target_file_for_category(pred_category)
        target_section = target_section_for_category(pred_category)
        scenario_type = f"ml_predicted_{pred_category}"

        patch_generated = generate_grounded_patch(
            docs_update_required=True,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            doc_category=pred_category,
            target_doc_file=target_doc_file,
            target_section=target_section,
            scenario_type=scenario_type,
        )

        postprocessed = postprocess_patch(
            patch_generated.get("patch_text"),
            target_doc_file,
            target_section,
        )

        patch_text = postprocessed.get("patch_text")

        verifier = verify_patch(
            patch_text,
            True,
            target_doc_file,
            model_row["code_diff_excerpt"],
            model_row["docs_before_excerpt"],
            pred_category,
            scenario_type,
            patch_generated.get("allowed_facts"),
        )

        quality = evaluate_patch_quality(
            patch_text=patch_text,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            target_doc_file=target_doc_file,
            doc_category=pred_category,
            scenario_type=scenario_type,
            verifier_result=verifier,
        )
    else:
        category_prediction = {
            "pred_doc_category": "no_update",
            "category_confidence": None,
            "category_probabilities": {},
            "category_ranked": [],
            "category_model_name": str(category_payload.get("model_type") or "category_model"),
        }
        pred_category = "no_update"
        target_doc_file = ""
        target_section = "Documentation"
        scenario_type = "ml_binary_no_update"

        patch_generated = generate_grounded_patch(
            docs_update_required=False,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            doc_category="no_update",
        )
        postprocessed = {
            "patch_text": None,
            "postprocess_status": "not_applicable",
            "warnings": [],
        }
        patch_text = None

        verifier = verify_patch(
            None,
            False,
            "",
            model_row["code_diff_excerpt"],
            model_row["docs_before_excerpt"],
            "no_update",
            scenario_type,
        )

        quality = evaluate_patch_quality(
            patch_text=None,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            target_doc_file="",
            doc_category="no_update",
            scenario_type=scenario_type,
            verifier_result=verifier,
        )

    evaluation = evaluate_prediction(
        case,
        {
            **binary_prediction,
            **category_prediction,
        },
    )

    return {
        "case_id": case_id,
        "repository": case.get("repository"),
        "source_url": case.get("source_url"),
        "language": model_row["language"],
        "code_changed_files": model_row["code_changed_files"],

        **evaluation,

        "pred_docs_update_required": docs_required,
        "binary_probability": binary_prediction["binary_probability"],
        "binary_threshold": binary_prediction["binary_threshold"],
        "binary_model_name": binary_prediction["binary_model_name"],

        "pred_doc_category": pred_category,
        "category_confidence": category_prediction.get("category_confidence"),
        "category_probabilities": category_prediction.get("category_probabilities"),
        "category_ranked": category_prediction.get("category_ranked"),
        "category_model_name": category_prediction.get("category_model_name"),

        "pred_target_doc_file": target_doc_file,
        "pred_target_section": target_section,
        "pred_scenario_type": scenario_type,

        "patch_mode": patch_mode,
        "generated_doc_patch": patch_text,
        "raw_generated_patch": patch_generated.get("patch_text"),
        "patch_generation_status": patch_generated.get("patch_status"),
        "patch_generator_warnings": patch_generated.get("generator_warnings") or [],
        "postprocess_status": postprocessed.get("postprocess_status"),
        "postprocess_warnings": postprocessed.get("warnings") or [],
        "verifier_status": verifier.get("verifier_status"),
        "verifier_warnings": verifier.get("warnings") or [],
        "grounded_tokens_found": verifier.get("grounded_tokens_found") or [],
        "quality_label": quality.get("quality_label"),
        "hallucination_risk": quality.get("hallucination_risk"),
        "groundedness_score": quality.get("groundedness_score"),
        "minimality_score": quality.get("minimality_score"),
        "readability_score": quality.get("readability_score"),
        "usefulness_score": quality.get("usefulness_score"),
        "quality_reasons": quality.get("quality_reasons") or [],

        "leakage_policy": {
            "safe_input_fields": SAFE_INPUT_FIELDS,
            "gold_used_for_prediction": False,
            "docs_after_used_for_prediction": False,
            "manual_notes_used_for_prediction": False,
            "source_url_used_for_prediction": False,
        },
    }


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = [row for row in rows if row.get("binary_evaluated")]

    tp = fp = tn = fn = 0
    for row in evaluated:
        gold = bool(row["gold_docs_update_required"])
        pred = bool(row["pred_docs_update_required"])

        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)
    accuracy = safe_div(tp + tn, len(evaluated))

    category_rows = [row for row in rows if row.get("category_evaluated")]
    category_correct = sum(1 for row in category_rows if row.get("category_correct"))

    patch_positive_rows = [row for row in rows if row.get("pred_docs_update_required")]
    patch_generated_rows = [row for row in patch_positive_rows if row.get("generated_doc_patch")]

    return {
        "total_cases": len(rows),
        "binary_evaluated_cases": len(evaluated),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "binary_accuracy": accuracy,
        "binary_precision": precision,
        "binary_recall": recall,
        "binary_f1": f1,
        "binary_specificity": specificity,
        "binary_false_positive_rate": safe_div(fp, fp + tn),
        "category_evaluated_cases": len(category_rows),
        "category_correct": category_correct,
        "category_accuracy_conditioned_on_true_positive": safe_div(category_correct, len(category_rows)),
        "predicted_positive_cases": len(patch_positive_rows),
        "patch_generated_for_predicted_positive": len(patch_generated_rows),
        "patch_generation_rate_for_predicted_positive": safe_div(len(patch_generated_rows), len(patch_positive_rows)),
        "verifier_status_counts": dict(Counter(str(row.get("verifier_status")) for row in rows)),
        "quality_label_counts": dict(Counter(str(row.get("quality_label")) for row in rows)),
        "hallucination_risk_counts": dict(Counter(str(row.get("hallucination_risk")) for row in rows)),
        "pred_category_counts": dict(Counter(str(row.get("pred_doc_category")) for row in rows)),
        "gold_category_counts": dict(Counter(str(row.get("gold_doc_category_normalized")) for row in rows)),
        "language_counts": dict(Counter(str(row.get("language")) for row in rows)),
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def safe_cell(value: Any, limit: int = 140) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("|", "\\|").replace("`", "\\`")
    text = " ".join(text.split())

    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."

    return text


def write_markdown_report(
    *,
    path: Path,
    metrics: dict[str, Any],
    rows: list[dict[str, Any]],
    input_path: Path,
    binary_model: Path,
    category_model: Path,
) -> None:
    lines: list[str] = [
        "# DocGuard ML Cascade Evaluation",
        "",
        "This report evaluates the end-to-end ML cascade:",
        "",
        "1. Binary documentation-update classifier",
        "2. Documentation-category classifier",
        "3. Grounded documentation patch generator",
        "4. Postprocessing, verifier, and patch-quality scoring",
        "",
        "Gold labels are used only after prediction for evaluation.",
        "",
        f"- Input: `{input_path}`",
        f"- Binary model: `{binary_model}`",
        f"- Category model: `{category_model}`",
        "",
        "## Leakage Policy",
        "",
        "Model-facing fields:",
        "",
    ]

    for field in SAFE_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "Not used for prediction: gold labels, source URL, docs-after text, manual notes, expected patch summary, or target labels.",
            "",
            "## Summary Metrics",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| total cases | {metrics['total_cases']} |",
            f"| binary evaluated cases | {metrics['binary_evaluated_cases']} |",
            f"| true positives | {metrics['true_positives']} |",
            f"| false positives | {metrics['false_positives']} |",
            f"| true negatives | {metrics['true_negatives']} |",
            f"| false negatives | {metrics['false_negatives']} |",
            f"| binary accuracy | {pct(metrics['binary_accuracy'])} |",
            f"| binary precision | {pct(metrics['binary_precision'])} |",
            f"| binary recall | {pct(metrics['binary_recall'])} |",
            f"| binary F1 | {pct(metrics['binary_f1'])} |",
            f"| binary specificity | {pct(metrics['binary_specificity'])} |",
            f"| binary FPR | {pct(metrics['binary_false_positive_rate'])} |",
            f"| category evaluated cases | {metrics['category_evaluated_cases']} |",
            f"| category correct | {metrics['category_correct']} |",
            f"| category accuracy conditioned on TP | {pct(metrics['category_accuracy_conditioned_on_true_positive'])} |",
            f"| predicted positive cases | {metrics['predicted_positive_cases']} |",
            f"| patch generated for predicted positives | {metrics['patch_generated_for_predicted_positive']} |",
            f"| patch generation rate | {pct(metrics['patch_generation_rate_for_predicted_positive'])} |",
            "",
            "## Guardrail Counts",
            "",
            f"- Verifier status counts: `{metrics['verifier_status_counts']}`",
            f"- Quality label counts: `{metrics['quality_label_counts']}`",
            f"- Hallucination risk counts: `{metrics['hallucination_risk_counts']}`",
            f"- Predicted category counts: `{metrics['pred_category_counts']}`",
            f"- Gold category counts: `{metrics['gold_category_counts']}`",
            f"- Language counts: `{metrics['language_counts']}`",
            "",
            "## Per-case Table",
            "",
            "| Case | Gold | Pred | Binary | Gold cat. | Pred cat. | Target | Verifier | Quality | Risk | Patch |",
            "| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{safe_cell(row.get('case_id'), 70)}`",
                    f"`{row.get('gold_docs_update_required')}`",
                    f"`{row.get('pred_docs_update_required')}`",
                    f"`{row.get('binary_correct')}`",
                    f"`{safe_cell(row.get('gold_doc_category_normalized'), 40)}`",
                    f"`{safe_cell(row.get('pred_doc_category'), 40)}`",
                    f"`{safe_cell(row.get('pred_target_doc_file'), 50)}`",
                    f"`{safe_cell(row.get('verifier_status'), 25)}`",
                    f"`{safe_cell(row.get('quality_label'), 25)}`",
                    f"`{safe_cell(row.get('hallucination_risk'), 25)}`",
                    f"`{bool(row.get('generated_doc_patch'))}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Case Details", ""])

    for row in rows:
        lines.extend(
            [
                f"### `{row.get('case_id')}`",
                "",
                f"- Repository: `{safe_cell(row.get('repository'), 120)}`",
                f"- Language: `{row.get('language')}`",
                f"- Gold docs update required: `{row.get('gold_docs_update_required')}`",
                f"- Predicted docs update required: `{row.get('pred_docs_update_required')}`",
                f"- Binary probability / threshold: `{row.get('binary_probability')}` / `{row.get('binary_threshold')}`",
                f"- Gold category: `{row.get('gold_doc_category_normalized')}`",
                f"- Predicted category: `{row.get('pred_doc_category')}`",
                f"- Category confidence: `{row.get('category_confidence')}`",
                f"- Target document: `{row.get('pred_target_doc_file')}`",
                f"- Verifier: `{row.get('verifier_status')}`",
                f"- Quality: `{row.get('quality_label')}`",
                f"- Hallucination risk: `{row.get('hallucination_risk')}`",
                "",
                "Generated patch:",
                "",
                "```diff",
                str(row.get("generated_doc_patch") or "not_applicable"),
                "```",
                "",
            ]
        )

        warnings = list(row.get("patch_generator_warnings") or [])
        warnings += list(row.get("postprocess_warnings") or [])
        warnings += list(row.get("verifier_warnings") or [])
        warnings += list(row.get("quality_reasons") or [])

        if warnings:
            lines.append("Warnings / reasons:")
            lines.append("")
            for warning in warnings[:12]:
                lines.append(f"- {warning}")
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    input_path: Path,
    output_dir: Path,
    binary_model_path: Path,
    category_model_path: Path,
    language_filter: str | None,
    case_limit: int | None,
    patch_mode: str,
) -> dict[str, Any]:
    binary_payload = load_binary_payload(binary_model_path)
    category_payload = load_category_payload(category_model_path)

    cases = load_jsonl(input_path)

    if language_filter:
        wanted = language_filter.strip().lower()
        cases = [
            case
            for case in cases
            if str(case.get("language") or "").strip().lower() == wanted
        ]

    if case_limit is not None:
        cases = cases[:case_limit]

    rows = [
        run_one_case(
            case=case,
            binary_payload=binary_payload,
            category_payload=category_payload,
            patch_mode=patch_mode,
        )
        for case in cases
    ]

    metrics = compute_metrics(rows)

    output_dir.mkdir(parents=True, exist_ok=True)

    predictions_path = output_dir / "ml_cascade_predictions.jsonl"
    summary_path = output_dir / "ml_cascade_summary.json"
    report_path = output_dir / "ml_cascade_report.md"

    summary = {
        "status": "ok",
        "input": str(input_path),
        "output_dir": str(output_dir),
        "predictions": str(predictions_path),
        "summary": str(summary_path),
        "report": str(report_path),
        "binary_model": str(binary_model_path),
        "category_model": str(category_model_path),
        "language_filter": language_filter,
        "case_limit": case_limit,
        "patch_mode": patch_mode,
        "metrics": metrics,
        "methodology": {
            "cascade": [
                "binary_v3_strict_raw",
                "category_v7_reviewed",
                "grounded_patch_generator",
                "postprocess_patch",
                "verify_patch",
                "evaluate_patch_quality",
            ],
            "gold_used_for_prediction": False,
            "docs_after_used_for_prediction": False,
            "manual_notes_used_for_prediction": False,
            "source_url_used_for_prediction": False,
            "safe_input_fields": SAFE_INPUT_FIELDS,
        },
    }

    write_jsonl(predictions_path, rows)
    write_json(summary_path, summary)
    write_markdown_report(
        path=report_path,
        metrics=metrics,
        rows=rows,
        input_path=input_path,
        binary_model=binary_model_path,
        category_model=category_model_path,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run real DocGuard ML cascade.")
    parser.add_argument(
        "--input",
        default="reports/real_case_study/generated/splits_gold_4k_v1/real_pr_gold_4k_v1_locked_test.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/real_case_study/generated/ml_cascade_v1_binary_v3_category_v7_grounded_patch",
    )
    parser.add_argument(
        "--binary-model",
        default="models/real_gold_classifier_4k_v3_strict_raw/best_model.joblib",
    )
    parser.add_argument(
        "--category-model",
        default="models/real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble/best_category_model.joblib",
    )
    parser.add_argument("--language-filter", default="typescript")
    parser.add_argument("--case-limit", type=int, default=None)
    parser.add_argument(
        "--patch-mode",
        default="grounded",
        choices=["grounded"],
    )

    args = parser.parse_args()

    run(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        binary_model_path=Path(args.binary_model),
        category_model_path=Path(args.category_model),
        language_filter=args.language_filter,
        case_limit=args.case_limit,
        patch_mode=args.patch_mode,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())