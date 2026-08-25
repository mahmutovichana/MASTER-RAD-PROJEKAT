from __future__ import annotations

import argparse
import importlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Required for joblib custom transformers.
importlib.import_module("scripts.train_real_gold_classifier_v3_strict_raw")
importlib.import_module("scripts.train_real_doc_category_classifier_v4")

from scripts.run_real_docguard_ml_cascade import (
    build_model_row,
    load_binary_payload,
    load_category_payload,
    load_jsonl,
    predict_binary,
    predict_category,
    write_json,
    write_jsonl,
)


PATCH_CATEGORIES = [
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
]


def case_id_of(case: dict[str, Any]) -> str:
    return str(case.get("case_id") or case.get("id") or "unknown_case")


def screen_case(
    *,
    case: dict[str, Any],
    binary_payload: dict[str, Any],
    category_payload: dict[str, Any],
) -> dict[str, Any]:
    model_row = build_model_row(case)

    binary_prediction = predict_binary(binary_payload, model_row)
    predicted_positive = bool(binary_prediction["pred_docs_update_required"])

    if predicted_positive:
        category_prediction = predict_category(category_payload, model_row)
        pred_category = str(category_prediction["pred_doc_category"])
        category_confidence = category_prediction.get("category_confidence")
    else:
        pred_category = "no_update"
        category_confidence = None

    return {
        "case": case,
        "case_id": case_id_of(case),
        "pred_docs_update_required": predicted_positive,
        "binary_probability": binary_prediction.get("binary_probability"),
        "pred_doc_category": pred_category,
        "category_confidence": category_confidence,
    }


def balanced_predicted_category_sample(
    screened: list[dict[str, Any]],
    *,
    sample_size: int,
    seed: int,
) -> list[dict[str, Any]]:
    positives = [
        item
        for item in screened
        if item["pred_docs_update_required"]
        and item["pred_doc_category"] in PATCH_CATEGORIES
    ]

    if sample_size <= 0:
        raise ValueError("sample_size must be greater than zero")

    if len(positives) < sample_size:
        raise ValueError(
            f"Requested sample_size={sample_size}, but only "
            f"{len(positives)} eligible predicted-positive cases are available."
        )

    rng = random.Random(seed)

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in positives:
        groups[item["pred_doc_category"]].append(item)

    for category in PATCH_CATEGORIES:
        rng.shuffle(groups[category])

    non_empty_categories = [
        category
        for category in PATCH_CATEGORIES
        if groups[category]
    ]

    if not non_empty_categories:
        raise ValueError("No predicted-positive patch categories are available.")

    base_quota = sample_size // len(non_empty_categories)
    remainder = sample_size % len(non_empty_categories)

    selected: list[dict[str, Any]] = []
    used_case_ids: set[str] = set()

    for index, category in enumerate(non_empty_categories):
        quota = base_quota + (1 if index < remainder else 0)
        take = min(quota, len(groups[category]))

        for item in groups[category][:take]:
            selected.append(item)
            used_case_ids.add(item["case_id"])

    # If one category had fewer cases than its quota, redistribute the
    # remaining slots across all unused predicted-positive candidates.
    missing = sample_size - len(selected)

    if missing > 0:
        leftovers = [
            item
            for item in positives
            if item["case_id"] not in used_case_ids
        ]

        rng.shuffle(leftovers)

        for item in leftovers[:missing]:
            selected.append(item)
            used_case_ids.add(item["case_id"])

    if len(selected) != sample_size:
        raise RuntimeError(
            f"Sampling failed: expected {sample_size} cases, got {len(selected)}."
        )

    rng.shuffle(selected)
    return selected


def run(
    *,
    input_path: Path,
    output_dir: Path,
    binary_model_path: Path,
    category_model_path: Path,
    language_filter: str | None,
    sample_size: int,
    seed: int,
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

    screened = [
        screen_case(
            case=case,
            binary_payload=binary_payload,
            category_payload=category_payload,
        )
        for case in cases
    ]

    predicted_positive = [
        item for item in screened
        if item["pred_docs_update_required"]
    ]

    selected = balanced_predicted_category_sample(
        screened,
        sample_size=sample_size,
        seed=seed,
    )

    selected_cases = [item["case"] for item in selected]

    manifest_rows = [
        {
            "case_id": item["case_id"],
            "pred_docs_update_required": item["pred_docs_update_required"],
            "binary_probability": item["binary_probability"],
            "pred_doc_category": item["pred_doc_category"],
            "category_confidence": item["category_confidence"],
        }
        for item in selected
    ]

    output_dir.mkdir(parents=True, exist_ok=True)

    sample_path = output_dir / "llm_patch_eval_sample.jsonl"
    manifest_path = output_dir / "llm_patch_eval_manifest.jsonl"
    summary_path = output_dir / "llm_patch_eval_sample_summary.json"

    available_category_counts = Counter(
        item["pred_doc_category"]
        for item in predicted_positive
        if item["pred_doc_category"] in PATCH_CATEGORIES
    )

    selected_category_counts = Counter(
        item["pred_doc_category"]
        for item in selected
    )

    summary = {
        "status": "ok",
        "input": str(input_path),
        "sample": str(sample_path),
        "manifest": str(manifest_path),
        "language_filter": language_filter,
        "sample_size": sample_size,
        "seed": seed,
        "sampling_strategy": "balanced_by_predicted_category",
        "eligible_cases_after_language_filter": len(cases),
        "predicted_positive_cases": len(predicted_positive),
        "available_predicted_category_counts": dict(
            sorted(available_category_counts.items())
        ),
        "selected_predicted_category_counts": dict(
            sorted(selected_category_counts.items())
        ),
        "binary_model": str(binary_model_path),
        "category_model": str(category_model_path),
        "sampling_policy": {
            "gold_used_for_sampling": False,
            "docs_after_used_for_sampling": False,
            "manual_notes_used_for_sampling": False,
            "source_url_used_for_sampling": False,
            "sampling_uses_predicted_binary_label": True,
            "sampling_uses_predicted_category": True,
            "sampling_seed_fixed": True,
        },
    }

    write_jsonl(sample_path, selected_cases)
    write_jsonl(manifest_path, manifest_rows)
    write_json(summary_path, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a reproducible predicted-positive stratified sample "
            "for DocGuard LLM patch evaluation."
        )
    )

    parser.add_argument(
        "--input",
        default=(
            "reports/real_case_study/generated/splits_gold_4k_v1/"
            "real_pr_gold_4k_v1_locked_test.jsonl"
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="dataset_versions/llm_patch_eval_v1",
    )
    parser.add_argument(
        "--binary-model",
        default=(
            "models/real_gold_classifier_4k_v3_strict_raw/"
            "best_model.joblib"
        ),
    )
    parser.add_argument(
        "--category-model",
        default=(
            "models/"
            "real_doc_category_classifier_4k_v7_category_reviewed_v2_"
            "typescript_v4_ensemble/best_category_model.joblib"
        ),
    )
    parser.add_argument("--language-filter", default="typescript")
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    run(
        input_path=Path(args.input),
        output_dir=Path(args.output_dir),
        binary_model_path=Path(args.binary_model),
        category_model_path=Path(args.category_model),
        language_filter=args.language_filter,
        sample_size=args.sample_size,
        seed=args.seed,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())