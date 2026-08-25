from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_real_docguard_ml_cascade import (
    compute_metrics,
    load_jsonl,
    write_json,
    write_jsonl,
)

from scripts.run_real_docguard_ml_cascade_llm_patch import (
    add_llm_metrics,
    candidate_is_acceptable,
    candidate_metrics,
    paired_candidate_metrics,
    safe_div,
    safe_mean,
)


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None

    ordered = sorted(values)
    index = max(
        0,
        min(
            len(ordered) - 1,
            math.ceil(q * len(ordered)) - 1,
        ),
    )
    return float(ordered[index])


def numeric_values(
    rows: list[dict[str, Any]],
    key: str,
) -> list[float]:
    output: list[float] = []

    for row in rows:
        value = row.get(key)
        if value is None:
            continue

        try:
            output.append(float(value))
        except (TypeError, ValueError):
            continue

    return output


def final_metrics(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    acceptable = [
        row
        for row in rows
        if candidate_is_acceptable(
            row.get("verifier_status"),
            row.get("quality_label"),
            row.get("hallucination_risk"),
        )
    ]

    def values(key: str) -> list[float]:
        return numeric_values(rows, key)

    return {
        "evaluated_cases": len(rows),
        "acceptable_cases": len(acceptable),
        "acceptable_rate": safe_div(
            len(acceptable),
            len(rows),
        ),
        "patch_final_source_counts": dict(
            Counter(
                str(row.get("patch_final_source"))
                for row in rows
            )
        ),
        "verifier_status_counts": dict(
            Counter(
                str(row.get("verifier_status"))
                for row in rows
            )
        ),
        "quality_label_counts": dict(
            Counter(
                str(row.get("quality_label"))
                for row in rows
            )
        ),
        "hallucination_risk_counts": dict(
            Counter(
                str(row.get("hallucination_risk"))
                for row in rows
            )
        ),
        "mean_groundedness_score": safe_mean(
            values("groundedness_score")
        ),
        "mean_minimality_score": safe_mean(
            values("minimality_score")
        ),
        "mean_readability_score": safe_mean(
            values("readability_score")
        ),
        "mean_usefulness_score": safe_mean(
            values("usefulness_score")
        ),
    }


def scope_metrics(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "cases": len(rows),
        "grounded_candidate": candidate_metrics(
            rows,
            "grounded",
        ),
        "qwen_candidate": candidate_metrics(
            rows,
            "llm",
        ),
        "paired_grounded_vs_qwen": paired_candidate_metrics(
            rows
        ),
        "final_cascade": final_metrics(rows),
    }


def merge_rows(
    original_rows: list[dict[str, Any]],
    retry_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    retry_by_id = {
        str(row.get("case_id")): row
        for row in retry_rows
    }

    if len(retry_by_id) != len(retry_rows):
        raise ValueError(
            "Retry predictions contain duplicate case_id values."
        )

    merged: list[dict[str, Any]] = []

    initial_success = 0
    replaced_from_retry = 0

    for original in original_rows:
        case_id = str(original.get("case_id"))

        if original.get("llm_generation_status") == "ok":
            row = dict(original)
            row["final_eval_generation_attempt"] = (
                "initial_success"
            )
            initial_success += 1
            merged.append(row)
            continue

        if case_id not in retry_by_id:
            raise ValueError(
                f"Missing retry result for failed case {case_id}"
            )

        retry = retry_by_id[case_id]

        if retry.get("llm_generation_status") != "ok":
            raise ValueError(
                f"Retry is not successful for case {case_id}: "
                f"{retry.get('llm_generation_status')}"
            )

        # Ensure retry was performed for the exact same upstream
        # binary/category prediction.
        if (
            retry.get("pred_docs_update_required")
            != original.get("pred_docs_update_required")
        ):
            raise ValueError(
                f"Binary prediction changed for case {case_id}"
            )

        if (
            retry.get("pred_doc_category")
            != original.get("pred_doc_category")
        ):
            raise ValueError(
                f"Category prediction changed for case {case_id}"
            )

        row = dict(retry)
        row["final_eval_generation_attempt"] = (
            "retry_after_hf_credit_exhaustion"
        )

        replaced_from_retry += 1
        merged.append(row)

    case_ids = [
        str(row.get("case_id"))
        for row in merged
    ]

    if len(case_ids) != len(set(case_ids)):
        raise ValueError(
            "Merged final predictions contain duplicate case IDs."
        )

    if len(merged) != len(original_rows):
        raise ValueError(
            "Merged evaluation does not preserve original sample size."
        )

    failures = [
        row
        for row in merged
        if row.get("llm_generation_status") != "ok"
    ]

    if failures:
        raise ValueError(
            f"Final evaluation still contains "
            f"{len(failures)} failed generations."
        )

    merge_info = {
        "original_cases": len(original_rows),
        "initial_successful_generations": initial_success,
        "retry_cases": len(retry_rows),
        "successful_retry_replacements": replaced_from_retry,
        "final_cases": len(merged),
        "final_successful_generations": (
            len(merged) - len(failures)
        ),
    }

    return merged, merge_info


def write_report(
    path: Path,
    summary: dict[str, Any],
) -> None:
    scopes = summary["scopes"]
    provider = summary["provider_reliability"]

    lines = [
        "# DocGuard LLM Patch Evaluation V1",
        "",
        "## Final protocol",
        "",
        "- Language: TypeScript",
        "- Frozen sample size: 100 predicted-positive cases",
        "- Model: Qwen/Qwen2.5-Coder-7B-Instruct",
        "- Temperature: 0.1",
        "- Max new tokens: 512",
        "- Sampling seed: 42",
        "- Gold labels were not used for generation or sampling.",
        "- Failed provider calls were retried without changing "
        "the model, prompt, sample, or generation parameters.",
        "",
        "## Provider reliability",
        "",
        f"- Initial successful generations: "
        f"{provider['initial_successful_generations']}",
        f"- Initial provider failures: "
        f"{provider['initial_provider_failures']}",
        f"- Successful retries: "
        f"{provider['successful_retries']}",
        f"- Final successful generations: "
        f"{provider['final_successful_generations']}/"
        f"{provider['final_cases']}",
        "",
    ]

    for scope_name, scope in scopes.items():
        lines.extend(
            [
                f"## Scope: {scope_name}",
                "",
                f"- Cases: {scope['cases']}",
                f"- Grounded acceptable rate: "
                f"{scope['grounded_candidate']['acceptable_rate']:.4f}",
                f"- Qwen acceptable rate: "
                f"{scope['qwen_candidate']['acceptable_rate']:.4f}",
                f"- Final cascade acceptable rate: "
                f"{scope['final_cascade']['acceptable_rate']:.4f}",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def run(
    *,
    original_predictions: Path,
    retry_predictions: Path,
    output_dir: Path,
) -> dict[str, Any]:
    original_rows = load_jsonl(original_predictions)
    retry_rows = load_jsonl(retry_predictions)

    merged, merge_info = merge_rows(
        original_rows,
        retry_rows,
    )

    all_metrics = add_llm_metrics(
        compute_metrics(merged),
        merged,
    )

    all_predicted_positive = [
        row
        for row in merged
        if row.get("pred_docs_update_required")
    ]

    gold_true_positive = [
        row
        for row in all_predicted_positive
        if row.get("gold_docs_update_required") is True
    ]

    upstream_correct = [
        row
        for row in all_predicted_positive
        if row.get("binary_correct") is True
        and row.get("category_correct") is True
    ]

    latencies = numeric_values(
        merged,
        "llm_latency_seconds",
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    predictions_path = (
        output_dir
        / "final_llm_patch_eval_predictions_100.jsonl"
    )
    summary_path = (
        output_dir
        / "final_llm_patch_eval_summary.json"
    )
    report_path = (
        output_dir
        / "final_llm_patch_eval_report.md"
    )

    provider_reliability = {
        "initial_cases": len(original_rows),
        "initial_successful_generations": sum(
            row.get("llm_generation_status") == "ok"
            for row in original_rows
        ),
        "initial_provider_failures": sum(
            row.get("llm_generation_status") != "ok"
            for row in original_rows
        ),
        "retry_cases": len(retry_rows),
        "successful_retries": sum(
            row.get("llm_generation_status") == "ok"
            for row in retry_rows
        ),
        "final_cases": len(merged),
        "final_successful_generations": sum(
            row.get("llm_generation_status") == "ok"
            for row in merged
        ),
        "final_generation_success_rate": safe_div(
            sum(
                row.get("llm_generation_status") == "ok"
                for row in merged
            ),
            len(merged),
        ),
        "mean_latency_seconds": (
            statistics.mean(latencies)
            if latencies else None
        ),
        "median_latency_seconds": (
            statistics.median(latencies)
            if latencies else None
        ),
        "p95_latency_seconds": percentile(
            latencies,
            0.95,
        ),
    }

    summary = {
        "status": "ok",
        "evaluation_version": "llm_patch_eval_v1_final",
        "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "backend": "huggingface_openai_compatible",
        "temperature": 0.1,
        "max_new_tokens": 512,
        "sample_size": len(merged),
        "sampling_seed": 42,
        "merge_info": merge_info,
        "provider_reliability": provider_reliability,
        "overall_metrics": all_metrics,
        "scopes": {
            "all_predicted_positive": scope_metrics(
                all_predicted_positive
            ),
            "gold_true_positive": scope_metrics(
                gold_true_positive
            ),
            "binary_and_category_correct": scope_metrics(
                upstream_correct
            ),
        },
        "methodology": {
            "sample_frozen_before_final_generation": True,
            "gold_used_for_sampling": False,
            "gold_used_for_generation": False,
            "docs_after_used_for_generation": False,
            "manual_notes_used_for_generation": False,
            "retry_changed_model": False,
            "retry_changed_prompt": False,
            "retry_changed_temperature": False,
            "retry_changed_sample": False,
            "retry_reason": (
                "Hugging Face HTTP 402 monthly included "
                "credit exhaustion"
            ),
            "classification_metrics_on_patch_sample_primary": False,
            "primary_binary_and_category_metrics": (
                "previously frozen full locked-test evaluations"
            ),
        },
        "outputs": {
            "predictions": str(predictions_path),
            "summary": str(summary_path),
            "report": str(report_path),
        },
    }

    write_jsonl(
        predictions_path,
        merged,
    )
    write_json(
        summary_path,
        summary,
    )
    write_report(
        report_path,
        summary,
    )

    print(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Finalize the frozen DocGuard Qwen patch "
            "evaluation by replacing provider-failed "
            "initial calls with successful retry results."
        )
    )

    parser.add_argument(
        "--original-predictions",
        required=True,
    )
    parser.add_argument(
        "--retry-predictions",
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "reports/real_case_study/generated/"
            "llm_patch_eval_v1_qwen_final_100"
        ),
    )

    args = parser.parse_args()

    run(
        original_predictions=Path(
            args.original_predictions
        ),
        retry_predictions=Path(
            args.retry_predictions
        ),
        output_dir=Path(
            args.output_dir
        ),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())