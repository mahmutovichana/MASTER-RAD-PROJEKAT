from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Required for joblib custom transformers.
importlib.import_module("scripts.train_real_gold_classifier_v3_strict_raw")
importlib.import_module("scripts.train_real_doc_category_classifier_v4")

from docguard_llm.grounded_patch_generator import (
    target_file_for_category,
    target_section_for_category,
)
from docguard_llm.llm_patch_pipeline import generate_llm_patch_candidate
from scripts.run_real_docguard_ml_cascade import (
    SAFE_INPUT_FIELDS,
    build_model_row,
    compute_metrics,
    evaluate_prediction,
    load_binary_payload,
    load_category_payload,
    load_jsonl,
    predict_binary,
    predict_category,
    write_json,
    write_jsonl,
    write_markdown_report,
)


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0

def safe_mean(values: list[float]) -> float:
    return float(sum(values) / len(values)) if values else 0.0


def candidate_is_acceptable(
    verifier_status: str | None,
    quality_label: str | None,
    hallucination_risk: str | None,
) -> bool:
    return bool(
        verifier_status in {"pass", "warn"}
        and quality_label != "rejected"
        and hallucination_risk in {"low", "medium"}
    )


def candidate_metrics(
    rows: list[dict[str, Any]],
    prefix: str,
) -> dict[str, Any]:
    positive_rows = [
        row
        for row in rows
        if row.get("pred_docs_update_required")
    ]

    verifier_key = f"{prefix}_verifier_status"
    quality_key = f"{prefix}_quality_label"
    risk_key = f"{prefix}_hallucination_risk"

    groundedness_key = f"{prefix}_groundedness_score"
    minimality_key = f"{prefix}_minimality_score"
    readability_key = f"{prefix}_readability_score"
    usefulness_key = f"{prefix}_usefulness_score"

    acceptable = [
        row
        for row in positive_rows
        if candidate_is_acceptable(
            row.get(verifier_key),
            row.get(quality_key),
            row.get(risk_key),
        )
    ]

    def numeric_values(key: str) -> list[float]:
        values: list[float] = []
        for row in positive_rows:
            value = row.get(key)
            if value is not None:
                values.append(float(value))
        return values

    return {
        "evaluated_cases": len(positive_rows),
        "verifier_status_counts": dict(
            Counter(
                str(row.get(verifier_key))
                for row in positive_rows
                if row.get(verifier_key) is not None
            )
        ),
        "quality_label_counts": dict(
            Counter(
                str(row.get(quality_key))
                for row in positive_rows
                if row.get(quality_key) is not None
            )
        ),
        "hallucination_risk_counts": dict(
            Counter(
                str(row.get(risk_key))
                for row in positive_rows
                if row.get(risk_key) is not None
            )
        ),
        "acceptable_rate": safe_div(
            len(acceptable),
            len(positive_rows),
        ),
        "mean_groundedness_score": safe_mean(
            numeric_values(groundedness_key)
        ),
        "mean_minimality_score": safe_mean(
            numeric_values(minimality_key)
        ),
        "mean_readability_score": safe_mean(
            numeric_values(readability_key)
        ),
        "mean_usefulness_score": safe_mean(
            numeric_values(usefulness_key)
        ),
    }


def paired_candidate_metrics(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    positive_rows = [
        row
        for row in rows
        if row.get("pred_docs_update_required")
    ]

    llm_wins = 0
    grounded_wins = 0
    ties = 0

    grounded_unacceptable_to_llm_acceptable = 0
    grounded_acceptable_to_llm_unacceptable = 0
    both_acceptable = 0
    both_unacceptable = 0

    usefulness_deltas: list[float] = []

    for row in positive_rows:
        llm_usefulness = float(
            row.get("llm_usefulness_score") or 0.0
        )
        grounded_usefulness = float(
            row.get("grounded_usefulness_score") or 0.0
        )

        delta = llm_usefulness - grounded_usefulness
        usefulness_deltas.append(delta)

        if delta > 1e-9:
            llm_wins += 1
        elif delta < -1e-9:
            grounded_wins += 1
        else:
            ties += 1

        llm_ok = candidate_is_acceptable(
            row.get("llm_verifier_status"),
            row.get("llm_quality_label"),
            row.get("llm_hallucination_risk"),
        )

        grounded_ok = candidate_is_acceptable(
            row.get("grounded_verifier_status"),
            row.get("grounded_quality_label"),
            row.get("grounded_hallucination_risk"),
        )

        if llm_ok and grounded_ok:
            both_acceptable += 1
        elif llm_ok and not grounded_ok:
            grounded_unacceptable_to_llm_acceptable += 1
        elif grounded_ok and not llm_ok:
            grounded_acceptable_to_llm_unacceptable += 1
        else:
            both_unacceptable += 1

    return {
        "evaluated_cases": len(positive_rows),
        "llm_usefulness_wins": llm_wins,
        "grounded_usefulness_wins": grounded_wins,
        "usefulness_ties": ties,
        "mean_llm_minus_grounded_usefulness": safe_mean(
            usefulness_deltas
        ),
        "grounded_unacceptable_to_llm_acceptable": (
            grounded_unacceptable_to_llm_acceptable
        ),
        "grounded_acceptable_to_llm_unacceptable": (
            grounded_acceptable_to_llm_unacceptable
        ),
        "both_acceptable": both_acceptable,
        "both_unacceptable": both_unacceptable,
    }

def add_llm_metrics(metrics: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    enriched = dict(metrics)

    enriched["patch_final_source_counts"] = dict(
        Counter(str(row.get("patch_final_source")) for row in rows)
    )
    enriched["llm_generation_status_counts"] = dict(
        Counter(str(row.get("llm_generation_status")) for row in rows)
    )
    enriched["llm_postprocess_status_counts"] = dict(
        Counter(str(row.get("llm_postprocess_status")) for row in rows)
    )

    predicted_positive = [row for row in rows if row.get("pred_docs_update_required")]
    llm_final = [row for row in predicted_positive if row.get("patch_final_source") == "llm"]
    fallback_final = [row for row in predicted_positive if row.get("patch_final_source") == "grounded_fallback"]

    enriched["llm_final_rate_for_predicted_positive"] = safe_div(len(llm_final), len(predicted_positive))
    enriched["grounded_fallback_rate_for_predicted_positive"] = safe_div(len(fallback_final), len(predicted_positive))

    acceptable_rows = [
        row
        for row in predicted_positive
        if row.get("verifier_status") in {"pass", "warn"}
        and row.get("hallucination_risk") in {"low", "medium"}
        and row.get("quality_label") != "rejected"
    ]
    enriched["acceptable_patch_rate_for_predicted_positive"] = safe_div(
        len(acceptable_rows),
        len(predicted_positive),
    )
    
    enriched["grounded_candidate_metrics"] = candidate_metrics(
        rows,
        "grounded",
    )

    enriched["llm_candidate_metrics"] = candidate_metrics(
        rows,
        "llm",
    )

    enriched["paired_candidate_comparison"] = paired_candidate_metrics(
        rows
    )

    return enriched


def run_one_case_llm(
    *,
    case: dict[str, Any],
    binary_payload: dict[str, Any],
    category_payload: dict[str, Any],
    patch_backend: str,
    patch_model: str | None,
    patch_temperature: float,
    patch_max_new_tokens: int,
    save_prompts: bool,
) -> dict[str, Any]:
    model_row = build_model_row(case)
    case_id = str(case.get("case_id") or case.get("id") or "unknown_case")

    binary_prediction = predict_binary(binary_payload, model_row)
    docs_required = bool(binary_prediction["pred_docs_update_required"])

    if docs_required:
        category_prediction = predict_category(category_payload, model_row)
        pred_category = str(category_prediction["pred_doc_category"])
        target_doc_file = target_file_for_category(pred_category)
        target_section = target_section_for_category(pred_category)
        scenario_type = f"ml_predicted_{pred_category}"

        patch_result = generate_llm_patch_candidate(
            docs_update_required=True,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            doc_category=pred_category,
            target_doc_file=target_doc_file,
            target_section=target_section,
            scenario_type=scenario_type,
            project_id=str(case.get("repository") or "real_case_study"),
            patch_backend=patch_backend,
            patch_model=patch_model,
            max_new_tokens=patch_max_new_tokens,
            temperature=patch_temperature,
            save_prompt=save_prompts,
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

        patch_result = generate_llm_patch_candidate(
            docs_update_required=False,
            code_diff=model_row["code_diff_excerpt"],
            docs_before=model_row["docs_before_excerpt"],
            doc_category="no_update",
            target_doc_file="",
            target_section="Documentation",
            scenario_type=scenario_type,
            project_id=str(case.get("repository") or "real_case_study"),
            patch_backend=patch_backend,
            patch_model=patch_model,
            max_new_tokens=patch_max_new_tokens,
            temperature=patch_temperature,
            save_prompt=save_prompts,
        )

    verifier = patch_result["verifier"]
    quality = patch_result["quality"]
    
    llm_verifier = patch_result.get("llm_verifier") or {}
    llm_quality = patch_result.get("llm_quality") or {}

    grounded_verifier = patch_result.get("grounded_verifier") or {}
    grounded_quality = patch_result.get("grounded_quality") or {}

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

        "patch_mode": f"llm_{patch_backend}",
        "patch_backend": patch_backend,
        "patch_model": patch_model or "",
        "patch_final_source": patch_result.get("final_patch_source"),
        "generated_doc_patch": patch_result.get("final_patch_text"),

        "llm_prompt": patch_result.get("llm_prompt") or "",
        "llm_prompt_metadata": patch_result.get("llm_prompt_metadata") or {},
        "llm_patch_raw": patch_result.get("llm_patch_raw") or "",
        "llm_generation_status": patch_result.get("llm_generation_status"),
        "llm_error_message": patch_result.get("llm_error_message") or "",
        "llm_latency_seconds": patch_result.get("llm_latency_seconds"),
        "llm_postprocess_status": patch_result.get("llm_postprocess_status"),
        "llm_postprocess_warnings": patch_result.get("llm_postprocess_warnings") or [],

        "grounded_patch_text": patch_result.get("grounded_patch_text"),
        "grounded_patch_status": patch_result.get("grounded_patch_status"),
        "grounded_postprocess_status": patch_result.get("grounded_postprocess_status"),
        "grounded_postprocess_warnings": patch_result.get("grounded_postprocess_warnings") or [],

        "raw_generated_patch": patch_result.get("final_patch_text"),
        "patch_generation_status": patch_result.get("final_generation_status"),
        "patch_generator_warnings": patch_result.get("patch_pipeline_warnings") or [],
        "postprocess_status": patch_result.get("postprocess_status"),
        "postprocess_warnings": patch_result.get("postprocess_warnings") or [],

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
            "llm_decides_binary_or_category": False,
        },
        
        "llm_verifier_status": llm_verifier.get("verifier_status"),
        "llm_verifier_warnings": llm_verifier.get("warnings") or [],
        "llm_quality_label": llm_quality.get("quality_label"),
        "llm_hallucination_risk": llm_quality.get("hallucination_risk"),
        "llm_groundedness_score": llm_quality.get("groundedness_score"),
        "llm_minimality_score": llm_quality.get("minimality_score"),
        "llm_readability_score": llm_quality.get("readability_score"),
        "llm_usefulness_score": llm_quality.get("usefulness_score"),
        "llm_quality_reasons": llm_quality.get("quality_reasons") or [],
        "grounded_verifier_status": grounded_verifier.get(
            "verifier_status"
        ),
        "grounded_verifier_warnings": grounded_verifier.get(
            "warnings"
        ) or [],
        "grounded_quality_label": grounded_quality.get("quality_label"),
        "grounded_hallucination_risk": grounded_quality.get(
            "hallucination_risk"
        ),
        "grounded_groundedness_score": grounded_quality.get(
            "groundedness_score"
        ),
        "grounded_minimality_score": grounded_quality.get(
            "minimality_score"
        ),
        "grounded_readability_score": grounded_quality.get(
            "readability_score"
        ),
        "grounded_usefulness_score": grounded_quality.get(
            "usefulness_score"
        ),
        "grounded_quality_reasons": grounded_quality.get(
            "quality_reasons"
        ) or [],
    }


def run(
    *,
    input_path: Path,
    output_dir: Path,
    binary_model_path: Path,
    category_model_path: Path,
    language_filter: str | None,
    case_limit: int | None,
    patch_backend: str,
    patch_model: str | None,
    patch_temperature: float,
    patch_max_new_tokens: int,
    save_prompts: bool,
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
        run_one_case_llm(
            case=case,
            binary_payload=binary_payload,
            category_payload=category_payload,
            patch_backend=patch_backend,
            patch_model=patch_model,
            patch_temperature=patch_temperature,
            patch_max_new_tokens=patch_max_new_tokens,
            save_prompts=save_prompts,
        )
        for case in cases
    ]

    metrics = add_llm_metrics(compute_metrics(rows), rows)

    output_dir.mkdir(parents=True, exist_ok=True)

    predictions_path = output_dir / "ml_cascade_llm_patch_predictions.jsonl"
    summary_path = output_dir / "ml_cascade_llm_patch_summary.json"
    report_path = output_dir / "ml_cascade_llm_patch_report.md"

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
        "patch_backend": patch_backend,
        "patch_model": patch_model,
        "patch_temperature": patch_temperature,
        "patch_max_new_tokens": patch_max_new_tokens,
        "save_prompts": save_prompts,
        "metrics": metrics,
        "methodology": {
            "patch_candidate_comparison": (
                "grounded deterministic candidate versus LLM candidate "
                "before final fallback selection"
            ),
            "patch_sample_classification_metrics_primary": False,
            "patch_sample_classification_metrics_note": (
                "Binary/category metrics produced on the patch-evaluation "
                "sample are diagnostic only. Primary classifier results "
                "remain the previously frozen full locked-test metrics."
            ),
            "cascade": [
                "binary_v3_strict_raw",
                "category_v7_reviewed",
                "allowed_fact_extraction",
                "grounded_patch_draft",
                "llm_patch_synthesis",
                "postprocess_patch",
                "verify_patch",
                "evaluate_patch_quality",
            ],
            "llm_decides_binary_or_category": False,
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
    parser = argparse.ArgumentParser(description="Run real DocGuard ML cascade with LLM patch synthesis.")
    parser.add_argument(
        "--input",
        default="reports/real_case_study/generated/splits_gold_4k_v1/real_pr_gold_4k_v1_locked_test.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/real_case_study/generated/ml_cascade_v2_llm_patch",
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
        "--patch-backend",
        default="mock",
        choices=["mock", "openai_compatible", "ollama", "hf"],
    )
    parser.add_argument("--patch-model", default=None)
    parser.add_argument("--patch-temperature", type=float, default=0.1)
    parser.add_argument("--patch-max-new-tokens", type=int, default=512)
    parser.add_argument("--save-prompts", action="store_true")

    args = parser.parse_args()

    run(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        binary_model_path=Path(args.binary_model),
        category_model_path=Path(args.category_model),
        language_filter=args.language_filter,
        case_limit=args.case_limit,
        patch_backend=args.patch_backend,
        patch_model=args.patch_model,
        patch_temperature=args.patch_temperature,
        patch_max_new_tokens=args.patch_max_new_tokens,
        save_prompts=args.save_prompts,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())