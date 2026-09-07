from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib

from docguard_llm_v2.hf_backend import (
    HuggingFaceChatBackend,
)
from docguard_ml_v2.data_contract import (
    binary_eligible_rows,
    load_jsonl,
)
from docguard_llm_v2.pipeline import (
    load_config,
)
from scripts.evaluate_binary_v4_confirmation import (
    run as run_binary_confirmation,
)
from scripts.evaluate_category_v8_confirmation import (
    run as run_category_confirmation,
)
from scripts.run_frozen_stage3_v2_confirmation import (
    category_prediction,
    positive_probability,
    run_stage3_for_positive_row,
    validate_confirmation_partitions,
    validate_frozen_inputs,
)
from scripts.verify_gate3_classifier_freeze import (
    verify as verify_gate3,
)
from scripts.verify_gate4_stage3_freeze import (
    verify as verify_gate4,
)


DEFAULT_CONFIRMATION = (
    "experiments/consolidated_enriched_training_v2/"
    "gold/confirmation.jsonl"
)

DEFAULT_PARTITION = (
    "data/final_v2/partitions/"
    "canonical_repository_partitions/"
    "repository_partition_manifest.json"
)

DEFAULT_BINARY_MODEL = (
    "models/final_v2/gate3/"
    "binary_m1_gate3.joblib"
)

DEFAULT_BINARY_FREEZE = (
    "reports/final_v2/gate3/"
    "binary_classifier_freeze_manifest.json"
)

DEFAULT_CATEGORY_MODEL = (
    "models/final_v2/gate3/"
    "category_m1_gate3.joblib"
)

DEFAULT_CATEGORY_FREEZE = (
    "reports/final_v2/gate3/"
    "category_classifier_freeze_manifest.json"
)

DEFAULT_STAGE3_CONFIG = (
    "configs/stage3_semantic_generation_v2.json"
)

DEFAULT_STAGE3_FREEZE = (
    "reports/final_v2/gate4/"
    "GATE4_STAGE3_FREEZE_MANIFEST.json"
)

DEFAULT_PREREG = (
    "reports/final_v2/gate5/"
    "GATE5_PREREGISTRATION.json"
)

DEFAULT_OUTPUT = (
    "reports/final_v2/gate5/one_shot"
)

MASTER_RECEIPT = (
    "GATE5_MASTER_ONE_SHOT_RECEIPT.json"
)

STARTED_MARKER = (
    "GATE5_ONE_SHOT_STARTED.json"
)

EXPECTED_GATE4_CLOSURE = (
    "fc49c94d6c6e4c575299e7a4df15985bcea71484"
)

EXPECTED_BINARY_SHA = (
    "7d6a9263e1262c5c54db3d2e100209707"
    "c6a7681133fb1505f44125efa954462"
)

EXPECTED_CATEGORY_SHA = (
    "2d8123ac398568b5c9586b0f8d26d6c40"
    "79ddfebd504889b934f77bef65b9f59"
)

EXPECTED_GATE4_FREEZE_SHA = (
    "8d2d7911330d15d04e8b628200252e6c"
    "1a614344651596064b293b17b707076f"
)

EXPECTED_STAGE3_CONFIG_SHA = (
    "27c234a3f998c34256025b0d914ddf3fd"
    "2a202eb3466b37a25f5aed0283e3192"
)

EXPECTED_RUNTIME = {
    "python":
        "3.12.13",
    "torch":
        "2.10.0+cu128",
    "transformers":
        "5.0.0",
    "accelerate":
        "1.13.0",
    "cuda_device_count":
        2,
    "cuda_devices":
        [
            "Tesla T4",
            "Tesla T4",
        ],
}


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


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
        raise RuntimeError(
            f"Expected JSON object: {path}"
        )

    return payload


def write_json(
    path: Path,
    payload: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")


def append_jsonl_fsync(
    path: Path,
    row: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "a",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        handle.write(
            json.dumps(
                row,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )

        handle.flush()
        os.fsync(
            handle.fileno()
        )


def require_execute_one_shot(
    enabled: bool,
) -> None:
    if enabled is not True:
        raise RuntimeError(
            "Gate 5 confirmation execution requires "
            "explicit --execute-one-shot."
        )


def ensure_master_receipt_absent(
    output_root: Path,
) -> None:
    receipt = (
        output_root
        / MASTER_RECEIPT
    )

    if receipt.exists():
        raise RuntimeError(
            "Gate 5 master one-shot receipt already exists. "
            "Canonical rerun is forbidden."
        )


def validate_partial_output_state(
    output_root: Path,
) -> None:
    ensure_master_receipt_absent(
        output_root
    )

    if not output_root.exists():
        return

    entries = list(
        output_root.iterdir()
    )

    if not entries:
        return

    allowed_names = {
        STARTED_MARKER,
        "binary",
        "category",
        "stage3",
    }

    unexpected = [
        item.name
        for item in entries
        if item.name
        not in allowed_names
    ]

    if unexpected:
        raise RuntimeError(
            "Unexpected Gate 5 partial outputs: "
            f"{sorted(unexpected)}"
        )

    marker = (
        output_root
        / STARTED_MARKER
    )

    if (
        any(
            item.name
            != STARTED_MARKER
            for item in entries
        )
        and not marker.exists()
    ):
        raise RuntimeError(
            "Partial Gate 5 outputs exist without "
            "the one-shot started marker."
        )


def validate_preregistration(
    path: Path,
) -> dict[str, Any]:
    p = load_json(
        path
    )

    if (
        p.get("schema_version")
        != "gate5_preregistration_v1"
        or p.get("gate") != 5
        or p.get("status")
        != "PREPARED_NOT_ACTIVATED"
    ):
        raise RuntimeError(
            "Gate 5 preregistration contract mismatch."
        )

    boundary = p[
        "confirmation_boundary"
    ]

    if (
        boundary.get(
            "confirmation_sealed_before_gate5"
        )
        is not True
        or boundary.get(
            "confirmation_accessed_during_preregistration"
        )
        is not False
    ):
        raise RuntimeError(
            "Unsafe Gate 5 preregistration boundary."
        )

    upstream = p.get(
        "upstream"
    ) or {}

    if (
        upstream.get(
            "gate4_closure_commit"
        )
        != EXPECTED_GATE4_CLOSURE
    ):
        raise RuntimeError(
            "Gate 5 preregistration has the wrong "
            "Gate 4 closure identity."
        )

    binary_upstream = (
        upstream.get(
            "binary_model"
        )
        or {}
    )

    category_upstream = (
        upstream.get(
            "category_model"
        )
        or {}
    )

    stage3_upstream = (
        upstream.get(
            "stage3_config"
        )
        or {}
    )

    gate4_upstream = (
        upstream.get(
            "gate4_stage3_freeze_manifest"
        )
        or {}
    )

    if (
        binary_upstream.get(
            "sha256"
        )
        != EXPECTED_BINARY_SHA
        or binary_upstream.get(
            "threshold"
        )
        != 0.15
    ):
        raise RuntimeError(
            "Gate 5 preregistered Binary identity mismatch."
        )

    if (
        category_upstream.get(
            "sha256"
        )
        != EXPECTED_CATEGORY_SHA
    ):
        raise RuntimeError(
            "Gate 5 preregistered Category identity mismatch."
        )

    if (
        stage3_upstream.get(
            "sha256"
        )
        != EXPECTED_STAGE3_CONFIG_SHA
    ):
        raise RuntimeError(
            "Gate 5 preregistered Stage 3 config identity mismatch."
        )

    if (
        gate4_upstream.get(
            "sha256"
        )
        != EXPECTED_GATE4_FREEZE_SHA
    ):
        raise RuntimeError(
            "Gate 5 preregistered Gate 4 freeze identity mismatch."
        )

    one_shot = (
        p.get(
            "one_shot_contract"
        )
        or {}
    )

    if (
        one_shot.get(
            "canonical_runner"
        )
        != "scripts/run_gate5_one_shot_qwen.py"
        or one_shot.get(
            "explicit_execute_flag_required"
        )
        is not True
        or one_shot.get(
            "rerun_after_master_receipt_allowed"
        )
        is not False
        or one_shot.get(
            "master_receipt_written_last"
        )
        is not True
    ):
        raise RuntimeError(
            "Gate 5 one-shot preregistration mismatch."
        )

    binary_ci = p[
        "binary_confirmation"
    ][
        "confidence_intervals"
    ]

    category_ci = p[
        "category_confirmation"
    ][
        "confidence_intervals"
    ]

    for ci in (
        binary_ci,
        category_ci,
    ):
        if (
            ci.get("method")
            != "repository_cluster_bootstrap"
            or ci.get("sampling_unit")
            != "repository"
            or ci.get("n_bootstrap")
            != 2000
            or ci.get("seed")
            != 42
            or ci.get("alpha")
            != 0.05
        ):
            raise RuntimeError(
                "Gate 5 repository-bootstrap preregistration mismatch."
            )

    if (
        p[
            "binary_confirmation"
        ][
            "threshold"
        ]
        != 0.15
    ):
        raise RuntimeError(
            "Gate 5 frozen Binary threshold mismatch."
        )

    runtime = p[
        "stage3_confirmation"
    ][
        "frozen_runtime_contract"
    ]

    for key, expected in (
        EXPECTED_RUNTIME.items()
    ):
        if runtime.get(key) != expected:
            raise RuntimeError(
                "Gate 5 frozen runtime preregistration mismatch: "
                f"{key}"
            )

    return p


def validate_finalization_state(
    root: Path,
) -> dict[str, Any]:
    state = load_json(
        root
        / "reports/final_v2/"
          "finalization_state.json"
    )

    if (
        int(
            state.get(
                "current_gate",
                -1,
            )
        )
        != 5
        or state[
            "gate_statuses"
        ][
            "gate_4_stage3_retrieval_generation_study_and_freeze"
        ]
        != "PASS"
        or state[
            "gate_statuses"
        ][
            "gate_5_one_shot_confirmation"
        ]
        != "NOT_EXECUTED"
        or state.get(
            "confirmation_sealed"
        )
        is not True
    ):
        raise RuntimeError(
            "Gate 5 finalization state is not safe for one-shot execution."
        )

    if (
        state.get(
            "confirmation_results_accessed_by_gate_5",
            False,
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 5 confirmation-access state is already true."
        )

    return state


def validate_preconfirmation_frozen_state(
    *,
    root: Path,
    preregistration: Path,
    binary_model: Path,
    binary_freeze: Path,
    category_model: Path,
    category_freeze: Path,
    stage3_config: Path,
    stage3_freeze: Path,
    output_root: Path,
) -> dict[str, Any]:

    gate3 = verify_gate3(
        root
    )

    gate4 = verify_gate4(
        root
    )

    if gate3["status"] != "PASS":
        raise RuntimeError(
            "Gate 3 verifier failed."
        )

    if (
        gate4["status"] != "PASS"
        or gate4[
            "stage3_status"
        ]
        != "FROZEN"
    ):
        raise RuntimeError(
            "Gate 4 verifier failed."
        )

    prereg = validate_preregistration(
        preregistration
    )

    validate_finalization_state(
        root
    )

    ensure_master_receipt_absent(
        output_root
    )

    validate_partial_output_state(
        output_root
    )

    frozen = validate_frozen_inputs(
        binary_model=
            binary_model,
        binary_freeze_manifest=
            binary_freeze,
        category_model=
            category_model,
        category_freeze_manifest=
            category_freeze,
        stage3_config=
            stage3_config,
        stage3_freeze_manifest=
            stage3_freeze,
    )

    if (
        frozen[
            "binary"
        ][
            "model_sha256"
        ]
        != EXPECTED_BINARY_SHA
    ):
        raise RuntimeError(
            "Unexpected frozen Binary identity."
        )

    if (
        frozen[
            "category"
        ][
            "model_sha256"
        ]
        != EXPECTED_CATEGORY_SHA
    ):
        raise RuntimeError(
            "Unexpected frozen Category identity."
        )

    if (
        frozen[
            "stage3"
        ][
            "stage3_config_sha256"
        ]
        != EXPECTED_STAGE3_CONFIG_SHA
    ):
        raise RuntimeError(
            "Unexpected frozen Stage 3 config identity."
        )

    if (
        frozen[
            "stage3"
        ][
            "stage3_freeze_manifest_sha256"
        ]
        != EXPECTED_GATE4_FREEZE_SHA
    ):
        raise RuntimeError(
            "Unexpected Gate 4 freeze identity."
        )

    return {
        "preregistration":
            prereg,
        "frozen":
            frozen,
        "gate3":
            gate3,
        "gate4":
            gate4,
    }


def validate_runtime_environment() -> dict[str, Any]:
    import torch
    import transformers
    import accelerate

    actual = {
        "python":
            platform.python_version(),
        "torch":
            torch.__version__,
        "transformers":
            transformers.__version__,
        "accelerate":
            accelerate.__version__,
        "cuda_device_count":
            int(
                torch.cuda.device_count()
            ),
        "cuda_devices":
            [
                torch.cuda.get_device_name(
                    index
                )
                for index
                in range(
                    torch.cuda.device_count()
                )
            ],
    }

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA is required for Gate 5 one-shot Qwen execution."
        )

    for key, expected in (
        EXPECTED_RUNTIME.items()
    ):
        if actual.get(key) != expected:
            raise RuntimeError(
                "Gate 5 runtime mismatch: "
                f"{key}: "
                f"{actual.get(key)!r} != {expected!r}"
            )

    return actual


def validate_or_create_started_marker(
    *,
    output_root: Path,
    identities: dict[str, str],
) -> None:
    marker = (
        output_root
        / STARTED_MARKER
    )

    if marker.exists():
        old = load_json(
            marker
        )

        if old != identities:
            raise RuntimeError(
                "Existing Gate 5 partial attempt has different frozen identities."
            )

        return

    output_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_json(
        marker,
        identities,
    )


def validate_existing_eval_receipt(
    *,
    receipt_path: Path,
    expected_model_hash: str,
    confirmation_hash: str,
) -> None:
    receipt = load_json(
        receipt_path
    )

    if (
        receipt.get(
            "confirmation_evaluated"
        )
        is not True
        or receipt.get(
            "model_hash"
        )
        != expected_model_hash
        or receipt.get(
            "confirmation_dataset_sha256"
        )
        != confirmation_hash
    ):
        raise RuntimeError(
            f"Existing evaluation receipt mismatch: {receipt_path}"
        )

    policy = receipt.get(
        "bootstrap_policy"
    ) or {}

    if (
        policy.get("method")
        != "repository_cluster_bootstrap"
        or policy.get(
            "sampling_unit"
        )
        != "repository"
        or policy.get(
            "n_bootstrap"
        )
        != 2000
        or policy.get(
            "seed"
        )
        != 42
        or policy.get(
            "alpha"
        )
        != 0.05
    ):
        raise RuntimeError(
            f"Existing evaluation bootstrap mismatch: {receipt_path}"
        )


def run_or_resume_binary(
    *,
    confirmation: Path,
    partition_manifest: Path,
    model: Path,
    freeze_manifest: Path,
    output_dir: Path,
    confirmation_hash: str,
) -> None:
    receipt = (
        output_dir
        / "confirmation_evaluation_receipt.json"
    )

    if receipt.exists():
        validate_existing_eval_receipt(
            receipt_path=
                receipt,
            expected_model_hash=
                EXPECTED_BINARY_SHA,
            confirmation_hash=
                confirmation_hash,
        )

        for required in (
            "confirmation_predictions.jsonl",
            "confirmation_metrics.json",
        ):
            if not (
                output_dir
                / required
            ).is_file():
                raise RuntimeError(
                    "Incomplete resumed Binary evaluation."
                )

        return

    run_binary_confirmation(
        model_path=
            model,
        confirmation=
            confirmation,
        freeze_manifest=
            freeze_manifest,
        output_dir=
            output_dir,
        partition_manifest=
            partition_manifest,
        enforce_one_shot=
            True,
        allow_repeat_for_reproducibility=
            False,
    )


def run_or_resume_category(
    *,
    confirmation: Path,
    partition_manifest: Path,
    model: Path,
    freeze_manifest: Path,
    output_dir: Path,
    confirmation_hash: str,
) -> None:
    receipt = (
        output_dir
        / "confirmation_evaluation_receipt.json"
    )

    if receipt.exists():
        validate_existing_eval_receipt(
            receipt_path=
                receipt,
            expected_model_hash=
                EXPECTED_CATEGORY_SHA,
            confirmation_hash=
                confirmation_hash,
        )

        for required in (
            "confirmation_predictions.jsonl",
            "confirmation_metrics.json",
        ):
            if not (
                output_dir
                / required
            ).is_file():
                raise RuntimeError(
                    "Incomplete resumed Category evaluation."
                )

        return

    run_category_confirmation(
        model_path=
            model,
        confirmation=
            confirmation,
        freeze_manifest=
            freeze_manifest,
        output_dir=
            output_dir,
        partition_manifest=
            partition_manifest,
        enforce_one_shot=
            True,
        allow_repeat_for_reproducibility=
            False,
    )


def run_or_resume_stage3(
    *,
    source_rows: list[dict[str, Any]],
    confirmation_hash: str,
    partition_manifest_hash: str,
    binary_model_path: Path,
    category_model_path: Path,
    stage3_config_path: Path,
    stage3_freeze_hash: str,
    output_dir: Path,
    backend: Any,
) -> None:

    receipt_path = (
        output_dir
        / "stage3_confirmation_generation_receipt.json"
    )

    results_path = (
        output_dir
        / "stage3_confirmation_generation_results.jsonl"
    )

    checkpoint_path = (
        output_dir
        / "stage3_confirmation_generation_checkpoint.jsonl"
    )

    if receipt_path.exists():
        receipt = load_json(
            receipt_path
        )

        if (
            receipt.get(
                "confirmation_dataset_hash"
            )
            != confirmation_hash
            or receipt.get(
                "binary_model_hash"
            )
            != EXPECTED_BINARY_SHA
            or receipt.get(
                "category_model_hash"
            )
            != EXPECTED_CATEGORY_SHA
            or receipt.get(
                "stage3_freeze_manifest_hash"
            )
            != stage3_freeze_hash
        ):
            raise RuntimeError(
                "Existing Stage 3 completion receipt identity mismatch."
            )

        if not results_path.is_file():
            raise RuntimeError(
                "Stage 3 receipt exists but results are missing."
            )

        return

    rows = binary_eligible_rows(
        source_rows,
        allowed_partitions={
            "confirmation"
        },
    )

    binary_payload = joblib.load(
        binary_model_path
    )

    category_payload = joblib.load(
        category_model_path
    )

    binary_pipeline = (
        binary_payload["model"]
    )

    category_pipeline = (
        category_payload["model"]
    )

    threshold = float(
        binary_payload["threshold"]
    )

    if threshold != 0.15:
        raise RuntimeError(
            "Frozen Binary threshold is not 0.15."
        )

    config = load_config(
        stage3_config_path
    )

    existing_rows = (
        load_jsonl(
            checkpoint_path
        )
        if checkpoint_path.exists()
        else []
    )

    existing_by_case = {
        str(
            row.get("case_id")
            or ""
        ):
            row
        for row
        in existing_rows
    }

    if (
        len(existing_by_case)
        != len(existing_rows)
        or "" in existing_by_case
    ):
        raise RuntimeError(
            "Invalid Stage 3 confirmation checkpoint."
        )

    ordered_case_ids = [
        str(
            row.get("case_id")
            or ""
        )
        for row
        in rows
    ]

    if (
        len(set(ordered_case_ids))
        != len(ordered_case_ids)
        or "" in ordered_case_ids
    ):
        raise RuntimeError(
            "Duplicate/empty confirmation case IDs."
        )

    for row in rows:
        case_id = str(
            row["case_id"]
        )

        if case_id in existing_by_case:
            continue

        score = positive_probability(
            binary_pipeline,
            row,
        )

        binary_pred = (
            score >= threshold
        )

        result: dict[str, Any] = {
            "case_id":
                case_id,
            "repository":
                row.get("repository"),
            "language":
                row.get("language"),
            "frozen_binary_prediction":
                bool(binary_pred),
            "binary_probability":
                float(score),
            "binary_threshold":
                threshold,
            "frozen_category_prediction":
                None,
            "retrieval_context_available":
                False,
            "stage3_invoked":
                False,
            "final_status":
                "binary_negative_stage3_not_called",
            "llm_call_count":
                0,
            "latency_seconds":
                0.0,
            "generated_patch":
                None,
            "stage3_result":
                None,
        }

        if binary_pred:
            category, probabilities = (
                category_prediction(
                    category_pipeline,
                    row,
                )
            )

            stage3 = (
                run_stage3_for_positive_row(
                    row=
                        row,
                    category=
                        category,
                    llm_backend=
                        backend,
                    config=
                        config,
                )
            )

            final_status = str(
                stage3.get(
                    "final_status"
                )
                or ""
            )

            result.update(
                {
                    "frozen_category_prediction":
                        category,
                    "category_probabilities":
                        probabilities,
                    "retrieval_context_available":
                        final_status
                        != "retrieval_context_unavailable",
                    "stage3_invoked":
                        final_status
                        != "retrieval_context_unavailable",
                    "final_status":
                        final_status,
                    "llm_call_count":
                        int(
                            stage3.get(
                                "llm_call_count"
                            )
                            or 0
                        ),
                    "latency_seconds":
                        float(
                            stage3.get(
                                "latency_seconds"
                            )
                            or 0.0
                        ),
                    "generated_patch":
                        stage3.get(
                            "final_patch"
                        ),
                    "stage3_result":
                        stage3,
                }
            )

        append_jsonl_fsync(
            checkpoint_path,
            result,
        )

        existing_by_case[
            case_id
        ] = result

    ordered = [
        existing_by_case[
            case_id
        ]
        for case_id
        in ordered_case_ids
    ]

    if len(ordered) != len(rows):
        raise RuntimeError(
            "Incomplete Stage 3 confirmation execution."
        )

    with results_path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        for row in ordered:
            handle.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    status_counts = Counter(
        str(
            row.get(
                "final_status"
            )
            or ""
        )
        for row
        in ordered
    )

    error_counts: Counter[str] = Counter()
    safety_counts: Counter[str] = Counter()

    for row in ordered:
        stage3 = (
            row.get(
                "stage3_result"
            )
            or {}
        )

        error = (
            stage3.get(
                "execution_error"
            )
            or {}
        )

        if error:
            error_counts[
                str(
                    error.get(
                        "code"
                    )
                    or "unknown"
                )
            ] += 1

        for verifier_key in (
            "first_pass_verifier",
            "repair_verifier",
        ):
            verifier = (
                stage3.get(
                    verifier_key
                )
                or {}
            )

            for violation in (
                verifier.get(
                    "violations"
                )
                or []
            ):
                safety_counts[
                    str(
                        violation.get(
                            "code"
                        )
                        or "unknown"
                    )
                ] += 1

    positive_count = sum(
        bool(
            row.get(
                "frozen_binary_prediction"
            )
        )
        for row
        in ordered
    )

    context_available = sum(
        bool(
            row.get(
                "frozen_binary_prediction"
            )
        )
        and bool(
            row.get(
                "retrieval_context_available"
            )
        )
        for row
        in ordered
    )

    receipt = {
        "status":
            "COMPLETED_ONE_SHOT_STAGE3",
        "confirmation_dataset_hash":
            confirmation_hash,
        "repository_partition_manifest_hash":
            partition_manifest_hash,
        "binary_model_hash":
            EXPECTED_BINARY_SHA,
        "category_model_hash":
            EXPECTED_CATEGORY_SHA,
        "stage3_freeze_manifest_hash":
            stage3_freeze_hash,
        "processed_row_count":
            len(ordered),
        "frozen_binary_predicted_positive_count":
            positive_count,
        "retrieval_context_available_count":
            context_available,
        "retrieval_context_unavailable_count":
            positive_count
            - context_available,
        "stage3_invocation_count":
            context_available,
        "llm_call_count":
            sum(
                int(
                    row.get(
                        "llm_call_count"
                    )
                    or 0
                )
                for row
                in ordered
            ),
        "final_status_counts":
            dict(
                sorted(
                    status_counts.items()
                )
            ),
        "execution_error_counts":
            dict(
                sorted(
                    error_counts.items()
                )
            ),
        "safety_violation_counts":
            dict(
                sorted(
                    safety_counts.items()
                )
            ),
        "results_sha256":
            sha256_file(
                results_path
            ),
        "checkpoint_sha256":
            sha256_file(
                checkpoint_path
            ),
    }

    write_json(
        receipt_path,
        receipt,
    )


def output_hash_inventory(
    output_root: Path,
) -> dict[str, str]:
    inventory = {}

    for path in sorted(
        output_root.rglob("*")
    ):
        if not path.is_file():
            continue

        if path.name in {
            MASTER_RECEIPT,
            STARTED_MARKER,
        }:
            continue

        relative = str(
            path.relative_to(
                ROOT
            )
        ).replace(
            "\\",
            "/",
        )

        inventory[
            relative
        ] = sha256_file(
            path
        )

    return inventory


def source_hash_inventory() -> dict[str, str]:
    files = [
        "scripts/run_gate5_one_shot_qwen.py",
        "scripts/evaluate_binary_v4_confirmation.py",
        "scripts/evaluate_category_v8_confirmation.py",
        "scripts/run_frozen_stage3_v2_confirmation.py",
        "docguard_eval_v2/gate5_bootstrap.py",
        "docguard_eval_v2/reference_evaluation.py",
        "scripts/build_stage3_confirmation_samples_v2.py",
    ]

    return {
        relative:
            sha256_file(
                ROOT
                / relative
            )
        for relative
        in files
    }


def execute_one_shot(
    *,
    confirmation: Path,
    partition_manifest: Path,
    binary_model: Path,
    binary_freeze: Path,
    category_model: Path,
    category_freeze: Path,
    stage3_config: Path,
    stage3_freeze: Path,
    preregistration: Path,
    output_root: Path,
) -> dict[str, Any]:

    preflight = (
        validate_preconfirmation_frozen_state(
            root=
                ROOT,
            preregistration=
                preregistration,
            binary_model=
                binary_model,
            binary_freeze=
                binary_freeze,
            category_model=
                category_model,
            category_freeze=
                category_freeze,
            stage3_config=
                stage3_config,
            stage3_freeze=
                stage3_freeze,
            output_root=
                output_root,
        )
    )

    runtime = (
        validate_runtime_environment()
    )

    # Load exact frozen Qwen before opening confirmation.
    backend = HuggingFaceChatBackend(
        "Qwen/Qwen2.5-Coder-7B-Instruct",
        seed=42,
        require_cuda=True,
        max_input_tokens=4096,
    )

    # Confirmation is first opened here.
    source_rows = load_jsonl(
        confirmation
    )

    partition_info = (
        validate_confirmation_partitions(
            source_rows,
            partition_manifest,
        )
    )

    confirmation_hash = (
        sha256_file(
            confirmation
        )
    )

    identities = {
        "schema_version":
            "gate5_one_shot_started_v1",
        "confirmation_dataset_sha256":
            confirmation_hash,
        "repository_partition_manifest_sha256":
            partition_info[
                "repository_partition_manifest_hash"
            ],
        "binary_model_sha256":
            EXPECTED_BINARY_SHA,
        "binary_freeze_manifest_sha256":
            sha256_file(
                binary_freeze
            ),
        "category_model_sha256":
            EXPECTED_CATEGORY_SHA,
        "category_freeze_manifest_sha256":
            sha256_file(
                category_freeze
            ),
        "gate4_stage3_freeze_manifest_sha256":
            EXPECTED_GATE4_FREEZE_SHA,
        "gate5_preregistration_sha256":
            sha256_file(
                preregistration
            ),
    }

    validate_or_create_started_marker(
        output_root=
            output_root,
        identities=
            identities,
    )

    run_or_resume_binary(
        confirmation=
            confirmation,
        partition_manifest=
            partition_manifest,
        model=
            binary_model,
        freeze_manifest=
            binary_freeze,
        output_dir=
            output_root
            / "binary",
        confirmation_hash=
            confirmation_hash,
    )

    run_or_resume_category(
        confirmation=
            confirmation,
        partition_manifest=
            partition_manifest,
        model=
            category_model,
        freeze_manifest=
            category_freeze,
        output_dir=
            output_root
            / "category",
        confirmation_hash=
            confirmation_hash,
    )

    run_or_resume_stage3(
        source_rows=
            source_rows,
        confirmation_hash=
            confirmation_hash,
        partition_manifest_hash=
            partition_info[
                "repository_partition_manifest_hash"
            ],
        binary_model_path=
            binary_model,
        category_model_path=
            category_model,
        stage3_config_path=
            stage3_config,
        stage3_freeze_hash=
            EXPECTED_GATE4_FREEZE_SHA,
        output_dir=
            output_root
            / "stage3",
        backend=
            backend,
    )

    master = {
        "schema_version":
            "gate5_master_one_shot_receipt_v1",
        "status":
            "COMPLETED_ONE_SHOT_CONFIRMATION",
        **identities,
        "runtime":
            runtime,
        "source_sha256":
            source_hash_inventory(),
        "output_sha256":
            output_hash_inventory(
                output_root
            ),
        "confirmation_accessed":
            True,
        "master_receipt_written_last":
            True,
        "rerun_allowed":
            False,
    }

    write_json(
        output_root
        / MASTER_RECEIPT,
        master,
    )

    return master


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Canonical frozen Gate 5 one-shot confirmation runner."
        )
    )

    parser.add_argument(
        "--execute-one-shot",
        action="store_true",
        help=(
            "Required explicit authorization to open "
            "the sealed confirmation split."
        ),
    )

    parser.add_argument(
        "--confirmation",
        default=
            DEFAULT_CONFIRMATION,
    )

    parser.add_argument(
        "--repository-partition-manifest",
        default=
            DEFAULT_PARTITION,
    )

    parser.add_argument(
        "--binary-model",
        default=
            DEFAULT_BINARY_MODEL,
    )

    parser.add_argument(
        "--binary-freeze-manifest",
        default=
            DEFAULT_BINARY_FREEZE,
    )

    parser.add_argument(
        "--category-model",
        default=
            DEFAULT_CATEGORY_MODEL,
    )

    parser.add_argument(
        "--category-freeze-manifest",
        default=
            DEFAULT_CATEGORY_FREEZE,
    )

    parser.add_argument(
        "--stage3-config",
        default=
            DEFAULT_STAGE3_CONFIG,
    )

    parser.add_argument(
        "--stage3-freeze-manifest",
        default=
            DEFAULT_STAGE3_FREEZE,
    )

    parser.add_argument(
        "--preregistration",
        default=
            DEFAULT_PREREG,
    )

    parser.add_argument(
        "--output-root",
        default=
            DEFAULT_OUTPUT,
    )

    args = parser.parse_args()

    # This guard happens before any confirmation path is opened.
    require_execute_one_shot(
        args.execute_one_shot
    )

    result = execute_one_shot(
        confirmation=
            ROOT
            / args.confirmation,
        partition_manifest=
            ROOT
            / args.repository_partition_manifest,
        binary_model=
            ROOT
            / args.binary_model,
        binary_freeze=
            ROOT
            / args.binary_freeze_manifest,
        category_model=
            ROOT
            / args.category_model,
        category_freeze=
            ROOT
            / args.category_freeze_manifest,
        stage3_config=
            ROOT
            / args.stage3_config,
        stage3_freeze=
            ROOT
            / args.stage3_freeze_manifest,
        preregistration=
            ROOT
            / args.preregistration,
        output_root=
            ROOT
            / args.output_root,
    )

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
