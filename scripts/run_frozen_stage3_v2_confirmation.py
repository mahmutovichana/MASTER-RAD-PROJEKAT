from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib

from docguard_eval_v2.reference_evaluation import (
    generation_view,
    sha256_file,
    write_json,
    write_jsonl,
)
from docguard_ml_v2.data_contract import (
    binary_eligible_rows,
    load_jsonl,
    serialize_model_row,
)
from docguard_ml_v2.model_manifest import utc_now
from docguard_llm_v2.context_adapter import (
    normalize_documentation_context,
)
from docguard_llm_v2.hf_backend import (
    GenerationCudaOutOfMemory,
    InputTokenBudgetExceeded,
)
from docguard_llm_v2.pipeline import (
    generate_semantic_documentation_patch,
    load_config,
)


REFERENCE_FIELDS = {
    "docs_after",
    "docs_after_excerpt",
    "docs_diff_excerpt",
    "gold_patch_summary",
    "gold_docs_update_required",
    "gold_doc_category",
    "human_label_notes",
}


def load_json(
    path: Path,
) -> dict[str, Any]:
    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        payload,
        dict,
    ):
        raise ValueError(
            f"Expected JSON object: {path}"
        )

    return payload


def validate_classifier_freeze(
    *,
    model_path: Path,
    freeze_manifest_path: Path,
    task: str,
) -> dict[str, Any]:

    manifest = load_json(
        freeze_manifest_path
    )

    if (
        manifest.get("schema_version")
        != "gate3_classifier_freeze_manifest_v1"
    ):
        raise ValueError(
            f"Unexpected Gate 3 {task} freeze schema."
        )

    if manifest.get("status") != "FROZEN":
        raise ValueError(
            f"Gate 3 {task} manifest is not FROZEN."
        )

    if manifest.get("task") != task:
        raise ValueError(
            f"Gate 3 task mismatch: expected {task}."
        )

    if (
        manifest.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise ValueError(
            f"Gate 3 {task} freeze must state "
            "confirmation_accessed=false."
        )

    expected = manifest.get(
        "model_sha256"
    )

    if not expected:
        raise ValueError(
            f"Gate 3 {task} freeze is missing model_sha256."
        )

    actual = sha256_file(
        model_path
    )

    if actual != expected:
        raise ValueError(
            f"Gate 3 {task} model hash mismatch."
        )

    return {
        "manifest": manifest,
        "model_sha256": actual,
        "freeze_manifest_sha256":
            sha256_file(
                freeze_manifest_path
            ),
    }


def validate_stage3_freeze(
    *,
    stage3_config: Path,
    stage3_freeze_manifest: Path,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:

    freeze = load_json(
        stage3_freeze_manifest
    )

    if (
        freeze.get("schema_version")
        != "gate4_stage3_freeze_v1"
    ):
        raise ValueError(
            "Unexpected Gate 4 Stage 3 freeze schema."
        )

    if freeze.get("gate") != 4:
        raise ValueError(
            "Gate 4 freeze has invalid gate number."
        )

    if freeze.get("status") != "PASS":
        raise ValueError(
            "Gate 4 freeze status must be PASS."
        )

    if (
        freeze.get("stage3_status")
        != "FROZEN"
    ):
        raise ValueError(
            "Gate 4 Stage 3 status must be FROZEN."
        )

    if (
        freeze.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise ValueError(
            "Gate 4 freeze must state "
            "confirmation_accessed=false."
        )

    if (
        freeze.get(
            "confirmation_sealed"
        )
        is not True
    ):
        raise ValueError(
            "Gate 4 freeze must state "
            "confirmation_sealed=true."
        )

    frozen_config = freeze.get(
        "stage3_config"
    )

    if not isinstance(
        frozen_config,
        dict,
    ):
        raise ValueError(
            "Gate 4 freeze missing stage3_config object."
        )

    expected_config_sha = (
        frozen_config.get(
            "sha256"
        )
    )

    if not expected_config_sha:
        raise ValueError(
            "Gate 4 freeze missing "
            "stage3_config.sha256."
        )

    actual_config_sha = (
        sha256_file(
            stage3_config
        )
    )

    if (
        actual_config_sha
        != expected_config_sha
    ):
        raise ValueError(
            "Frozen Stage 3 config hash mismatch."
        )

    config_payload = load_json(
        stage3_config
    )

    if (
        frozen_config.get(
            "settings"
        )
        != config_payload
    ):
        raise ValueError(
            "Frozen Stage 3 config settings mismatch."
        )

    source_hashes = freeze.get(
        "implementation_source_sha256"
    )

    if (
        not isinstance(
            source_hashes,
            dict,
        )
        or not source_hashes
    ):
        raise ValueError(
            "Gate 4 freeze missing "
            "implementation_source_sha256."
        )

    for relative, expected_hash in (
        source_hashes.items()
    ):
        source_path = (
            project_root
            / relative
        )

        if not source_path.is_file():
            raise ValueError(
                "Frozen Stage 3 source file missing: "
                f"{relative}"
            )

        actual_hash = sha256_file(
            source_path
        )

        if actual_hash != expected_hash:
            raise ValueError(
                "Frozen Stage 3 source hash mismatch: "
                f"{relative}"
            )

    return {
        "manifest": freeze,
        "stage3_config_sha256":
            actual_config_sha,
        "stage3_freeze_manifest_sha256":
            sha256_file(
                stage3_freeze_manifest
            ),
        "implementation_source_sha256":
            dict(
                sorted(
                    source_hashes.items()
                )
            ),
    }


def validate_frozen_inputs(
    *,
    binary_model: Path,
    binary_freeze_manifest: Path,
    category_model: Path,
    category_freeze_manifest: Path,
    stage3_config: Path,
    stage3_freeze_manifest: Path,
) -> dict[str, Any]:

    binary = (
        validate_classifier_freeze(
            model_path=
                binary_model,
            freeze_manifest_path=
                binary_freeze_manifest,
            task="binary",
        )
    )

    category = (
        validate_classifier_freeze(
            model_path=
                category_model,
            freeze_manifest_path=
                category_freeze_manifest,
            task="category",
        )
    )

    stage3 = validate_stage3_freeze(
        stage3_config=
            stage3_config,
        stage3_freeze_manifest=
            stage3_freeze_manifest,
    )

    return {
        "binary": binary,
        "category": category,
        "stage3": stage3,
    }


def validate_confirmation_partitions(
    rows: list[dict[str, Any]],
    partition_manifest: Path,
) -> dict[str, Any]:

    partition = load_json(
        partition_manifest
    )

    if (
        partition.get(
            "confirmation_sealed"
        )
        is not True
    ):
        raise ValueError(
            "Repository partition manifest must "
            "have confirmation_sealed=true."
        )

    assignments = {
        str(repo).lower(): part
        for repo, part in (
            partition.get(
                "repository_assignments"
            )
            or {}
        ).items()
    }

    for row in rows:
        repository = str(
            row.get("repository")
            or ""
        ).lower()

        if (
            row.get("partition")
            != "confirmation"
            or assignments.get(
                repository
            )
            != "confirmation"
        ):
            raise ValueError(
                "Non-confirmation row detected: "
                f"{row.get('case_id')}"
            )

    return {
        "repository_partition_manifest_hash":
            sha256_file(
                partition_manifest
            ),
    }


def one_shot_guard(
    output_dir: Path,
    identities: dict[str, str],
    *,
    enforce: bool,
    allow_repeat: bool,
) -> None:

    receipt = (
        output_dir
        / "stage3_confirmation_generation_receipt.json"
    )

    if (
        not enforce
        or not receipt.exists()
    ):
        return

    old = load_json(
        receipt
    )

    keys = [
        "confirmation_dataset_hash",
        "binary_model_hash",
        "category_model_hash",
        "stage3_freeze_manifest_hash",
    ]

    same = all(
        old.get(key)
        == identities.get(key)
        for key in keys
    )

    if same and not allow_repeat:
        raise ValueError(
            "Frozen Stage 3 confirmation generation "
            "already ran for this frozen configuration "
            "and dataset."
        )


def positive_probability(
    model: Any,
    row: dict[str, Any],
) -> float:

    proba = model.predict_proba(
        [row]
    )[0]

    if hasattr(
        model,
        "named_steps",
    ):
        classes = list(
            model.named_steps[
                "classifier"
            ].classes_
        )
    else:
        classes = list(
            model.classes_
        )

    return float(
        proba[
            classes.index(1)
        ]
    )


def category_prediction(
    model: Any,
    row: dict[str, Any],
) -> tuple[
    str,
    dict[str, float],
]:

    label = str(
        model.predict(
            [row]
        )[0]
    )

    probabilities: dict[
        str,
        float,
    ] = {}

    if hasattr(
        model,
        "predict_proba",
    ):
        proba = model.predict_proba(
            [row]
        )[0]

        if hasattr(
            model,
            "named_steps",
        ):
            classes = list(
                model.named_steps[
                    "classifier"
                ].classes_
            )
        else:
            classes = list(
                model.classes_
            )

        probabilities = {
            str(cls):
                float(
                    proba[index]
                )
            for index, cls
            in enumerate(classes)
        }

    return (
        label,
        probabilities,
    )


def run_stage3_for_positive_row(
    *,
    row: dict[str, Any],
    category: str,
    llm_backend: Any,
    config: dict[str, Any],
) -> dict[str, Any]:

    candidates = (
        normalize_documentation_context(
            row
        )
    )

    safe_context = generation_view(
        {
            **row,
            "pred_doc_category":
                category,
        }
    )

    leaked = (
        REFERENCE_FIELDS
        & set(
            safe_context
        )
    )

    if leaked:
        raise RuntimeError(
            "Reference fields leaked into "
            f"generation view: {sorted(leaked)}"
        )

    if not candidates:
        return {
            "final_status":
                "retrieval_context_unavailable",
            "final_source":
                "none",
            "final_patch":
                None,
            "selected_document":
                None,
            "llm_call_count":
                0,
            "latency_seconds":
                0.0,
            "execution_error":
                None,
        }

    started = time.perf_counter()

    calls_before = int(
        getattr(
            llm_backend,
            "call_count",
            0,
        )
    )

    try:
        stage3 = (
            generate_semantic_documentation_patch(
                docs_update_required=True,
                predicted_category=
                    category,
                code_diff=str(
                    safe_context.get(
                        "code_diff_excerpt"
                    )
                    or ""
                ),
                docs_before=str(
                    safe_context.get(
                        "docs_before_excerpt"
                    )
                    or ""
                ),
                documentation_context_candidates=
                    candidates,
                llm_backend=
                    llm_backend,
                config=
                    config,
            )
        )

    except InputTokenBudgetExceeded as exc:
        calls_after = int(
            getattr(
                llm_backend,
                "call_count",
                calls_before,
            )
        )

        stage3 = {
            "final_status":
                "human_review_required",
            "final_source":
                "none",
            "final_patch":
                None,
            "selected_document":
                None,
            "llm_call_count":
                max(
                    0,
                    calls_after
                    - calls_before,
                ),
            "execution_error": {
                "code":
                    "input_token_budget_exceeded",
                "error_type":
                    type(exc).__name__,
                "message":
                    str(exc),
                "purpose":
                    exc.purpose,
                "input_tokens":
                    exc.input_tokens,
                "max_input_tokens":
                    exc.max_input_tokens,
            },
        }

    except GenerationCudaOutOfMemory as exc:
        calls_after = int(
            getattr(
                llm_backend,
                "call_count",
                calls_before,
            )
        )

        stage3 = {
            "final_status":
                "human_review_required",
            "final_source":
                "none",
            "final_patch":
                None,
            "selected_document":
                None,
            "llm_call_count":
                max(
                    0,
                    calls_after
                    - calls_before,
                ),
            "execution_error": {
                "code":
                    "cuda_out_of_memory",
                "error_type":
                    type(exc).__name__,
                "message":
                    str(exc),
                "purpose":
                    exc.purpose,
            },
        }

    except (
        json.JSONDecodeError,
        ValueError,
        TypeError,
    ) as exc:
        calls_after = int(
            getattr(
                llm_backend,
                "call_count",
                calls_before,
            )
        )

        stage3 = {
            "final_status":
                "human_review_required",
            "final_source":
                "none",
            "final_patch":
                None,
            "selected_document":
                None,
            "llm_call_count":
                max(
                    0,
                    calls_after
                    - calls_before,
                ),
            "execution_error": {
                "code":
                    "invalid_structured_llm_output",
                "error_type":
                    type(exc).__name__,
                "message":
                    str(exc),
            },
        }

    stage3["latency_seconds"] = (
        time.perf_counter()
        - started
    )

    return stage3


def run(
    *,
    confirmation: Path,
    repository_partition_manifest: Path,
    binary_model: Path,
    binary_freeze_manifest: Path,
    category_model: Path,
    category_freeze_manifest: Path,
    stage3_config: Path,
    stage3_freeze_manifest: Path,
    output_dir: Path,
    llm_backend: Any,
    enforce_one_shot: bool = False,
    allow_repeat_for_reproducibility:
        bool = False,
) -> dict[str, Any]:

    # Frozen identities are validated before
    # confirmation is opened.
    frozen = validate_frozen_inputs(
        binary_model=
            binary_model,
        binary_freeze_manifest=
            binary_freeze_manifest,
        category_model=
            category_model,
        category_freeze_manifest=
            category_freeze_manifest,
        stage3_config=
            stage3_config,
        stage3_freeze_manifest=
            stage3_freeze_manifest,
    )

    source_rows = load_jsonl(
        confirmation
    )

    partition_info = (
        validate_confirmation_partitions(
            source_rows,
            repository_partition_manifest,
        )
    )

    confirmation_hash = (
        sha256_file(
            confirmation
        )
    )

    identities = {
        "confirmation_dataset_hash":
            confirmation_hash,
        "binary_model_hash":
            frozen[
                "binary"
            ][
                "model_sha256"
            ],
        "category_model_hash":
            frozen[
                "category"
            ][
                "model_sha256"
            ],
        "stage3_freeze_manifest_hash":
            frozen[
                "stage3"
            ][
                "stage3_freeze_manifest_sha256"
            ],
    }

    one_shot_guard(
        output_dir,
        identities,
        enforce=
            enforce_one_shot,
        allow_repeat=
            allow_repeat_for_reproducibility,
    )

    rows = binary_eligible_rows(
        source_rows,
        allowed_partitions={
            "confirmation"
        },
    )

    binary_payload = joblib.load(
        binary_model
    )

    category_payload = joblib.load(
        category_model
    )

    binary_pipeline = (
        binary_payload["model"]
    )

    category_pipeline = (
        category_payload["model"]
    )

    threshold = float(
        binary_payload[
            "threshold"
        ]
    )

    if threshold != 0.15:
        raise ValueError(
            "Frozen Binary threshold changed "
            "from preregistered 0.15."
        )

    cfg = load_config(
        stage3_config
    )

    output_rows: list[
        dict[str, Any]
    ] = []

    status_counts: dict[
        str,
        int,
    ] = {}

    positive_count = 0
    stage3_invocation_count = 0
    llm_call_count = 0
    context_available_count = 0

    for row in rows:
        serialize_model_row(
            row
        )

        binary_score = (
            positive_probability(
                binary_pipeline,
                row,
            )
        )

        binary_pred = (
            binary_score
            >= threshold
        )

        result_row: dict[
            str,
            Any,
        ] = {
            "case_id":
                row.get("case_id"),
            "repository":
                row.get("repository"),
            "language":
                row.get("language"),
            "code_changed_files":
                row.get(
                    "code_changed_files"
                ),
            "code_diff_excerpt":
                row.get(
                    "code_diff_excerpt"
                ),
            "docs_before_excerpt":
                row.get(
                    "docs_before_excerpt"
                ),
            "frozen_binary_prediction":
                bool(binary_pred),
            "binary_probability":
                binary_score,
            "binary_threshold":
                threshold,
            "frozen_category_prediction":
                None,
            "category_probabilities":
                {},
            "retrieval_context_available":
                False,
            "stage3_invoked":
                False,
            "final_status":
                "binary_negative_stage3_not_called",
            "llm_call_count":
                0,
            "stage3_result":
                None,
            "generated_patch":
                None,
            "selected_retrieved_document":
                None,
            "safety_provenance_result":
                None,
        }

        if binary_pred:
            positive_count += 1

            category, category_probs = (
                category_prediction(
                    category_pipeline,
                    row,
                )
            )

            candidates = (
                normalize_documentation_context(
                    row
                )
            )

            context_available = bool(
                candidates
            )

            if context_available:
                context_available_count += 1

            stage3 = (
                run_stage3_for_positive_row(
                    row=row,
                    category=category,
                    llm_backend=
                        llm_backend,
                    config=cfg,
                )
            )

            if context_available:
                stage3_invocation_count += 1

            calls = int(
                stage3.get(
                    "llm_call_count"
                )
                or 0
            )

            llm_call_count += calls

            final_status = str(
                stage3.get(
                    "final_status"
                )
                or ""
            )

            status_counts[
                final_status
            ] = (
                status_counts.get(
                    final_status,
                    0,
                )
                + 1
            )

            result_row.update(
                {
                    "frozen_category_prediction":
                        category,
                    "category_probabilities":
                        category_probs,
                    "retrieval_context_available":
                        context_available,
                    "stage3_invoked":
                        context_available,
                    "final_status":
                        final_status,
                    "llm_call_count":
                        calls,
                    "stage3_result":
                        stage3,
                    "generated_patch":
                        stage3.get(
                            "final_patch"
                        ),
                    "selected_retrieved_document":
                        stage3.get(
                            "selected_document"
                        ),
                    "safety_provenance_result":
                        stage3.get(
                            "first_pass_verifier"
                        ),
                }
            )

        if (
            REFERENCE_FIELDS
            & set(
                result_row
            )
        ):
            raise RuntimeError(
                "Reference fields leaked into "
                "Stage 3 generation results."
            )

        output_rows.append(
            result_row
        )

    binary_negative_count = (
        len(rows)
        - positive_count
    )

    if binary_negative_count:
        status_counts[
            "binary_negative_stage3_not_called"
        ] = binary_negative_count

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_jsonl(
        output_dir
        / "stage3_confirmation_generation_results.jsonl",
        output_rows,
    )

    receipt = {
        **identities,
        **partition_info,

        "source_hashes":
            frozen[
                "stage3"
            ][
                "implementation_source_sha256"
            ],

        "stage3_config_sha256":
            frozen[
                "stage3"
            ][
                "stage3_config_sha256"
            ],

        "binary_freeze_manifest_hash":
            frozen[
                "binary"
            ][
                "freeze_manifest_sha256"
            ],

        "category_freeze_manifest_hash":
            frozen[
                "category"
            ][
                "freeze_manifest_sha256"
            ],

        "run_timestamp":
            utc_now(),

        "processed_row_count":
            len(rows),

        "frozen_binary_predicted_positive_count":
            positive_count,

        "retrieval_context_available_count":
            context_available_count,

        "retrieval_context_unavailable_count":
            positive_count
            - context_available_count,

        "stage3_invocation_count":
            stage3_invocation_count,

        "llm_call_count":
            llm_call_count,

        "final_status_counts":
            dict(
                sorted(
                    status_counts.items()
                )
            ),

        "repeat_for_reproducibility":
            bool(
                allow_repeat_for_reproducibility
            ),
    }

    write_json(
        output_dir
        / "stage3_confirmation_generation_receipt.json",
        receipt,
    )

    return {
        "status": "ok",
        "receipt": receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Frozen Stage 3 V2 confirmation "
            "generation infrastructure. "
            "Canonical Gate 5 execution uses "
            "run_gate5_one_shot_qwen.py."
        )
    )

    parser.add_argument(
        "--confirmation",
        required=True,
    )

    parser.add_argument(
        "--repository-partition-manifest",
        required=True,
    )

    parser.add_argument(
        "--binary-model",
        required=True,
    )

    parser.add_argument(
        "--binary-freeze-manifest",
        required=True,
    )

    parser.add_argument(
        "--category-model",
        required=True,
    )

    parser.add_argument(
        "--category-freeze-manifest",
        required=True,
    )

    parser.add_argument(
        "--stage3-config",
        required=True,
    )

    parser.add_argument(
        "--stage3-freeze-manifest",
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
    )

    raise SystemExit(
        "Infrastructure-only CLI. "
        "Do not execute confirmation here. "
        "Use the canonical Gate 5 one-shot runner."
    )


if __name__ == "__main__":
    main()
