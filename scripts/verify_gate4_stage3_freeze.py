from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.verify_gate3_classifier_freeze import (
    verify as verify_gate3,
)


EXPECTED_FREEZE_SHA256 = (
    "8d2d7911330d15d04e8b628200252e6c"
    "1a614344651596064b293b17b707076f"
)

EXPECTED_EXECUTION_COMMIT = (
    "c3ddac2d64f71127082f66fba53850f64e071ec3"
)

EXPECTED_INPUT_SHA256 = (
    "0e72d7ac93e44a0035046ac65b808f84"
    "ac851a556e9e3ddc076f03bdba4bd1f8"
)

EXPECTED_RESULTS_SHA256 = (
    "b6614a90b6429ace634ed20118c30a235"
    "c34e2d9d144e528260549292d5f3792"
)

EXPECTED_ARCHIVE_SHA256 = (
    "95d53f9e5d99b4e456632fe22a5251e6"
    "abcce70851e2a2c57c7d9bde2156cd7b"
)

EXPECTED_CONFIG_SHA256 = (
    "27c234a3f998c34256025b0d914ddf3f"
    "d2a202eb3466b37a25f5aed0283e3192"
)

GATE4_ARTIFACT_EOL_CORRECTION_RELATIVE = (
    "reports/final_v2/gate4/"
    "GATE4_ARTIFACT_EOL_PORTABILITY_CORRECTION.json"
)

GATE4_ARTIFACT_EOL_CORRECTION_SCHEMA = (
    "gate4_artifact_eol_portability_correction_v1"
)

GATE5_PREREGISTRATION_SHA256 = (
    "dd4ed749774c144d3533128e93749fa003925dbdf73b1a121fee1a3fd40dc3b8"
)

EXPECTED_EOL_PORTABLE_ARTIFACTS = {
    "reports/final_v2/gate4/final_results/GATE4_DEVELOPMENT_ANALYSIS.md",
    "reports/final_v2/gate4/final_results/gate4_case_diagnostics.csv",
    "reports/final_v2/gate4/final_results/gate4_development_analysis_summary.json",
    "reports/final_v2/gate4/final_results/gate4_sample_summary.csv",
    "reports/final_v2/gate4/final_results/gate4_secondary_category_summary.csv",
    "reports/final_v2/gate4/final_results/postrun_verification_report.json",
}


EXPECTED_STATUS_COUNTS = {
    "accepted_after_repair": 1,
    "accepted_first_pass": 48,
    "human_review_required": 42,
    "retrieval_context_unavailable": 109,
}

EXPECTED_ERROR_COUNTS = {
    "input_token_budget_exceeded": 6,
    "invalid_structured_llm_output": 13,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line_number, line in enumerate(
            handle,
            start=1,
        ):
            if not line.strip():
                continue

            row = json.loads(line)

            if not isinstance(row, dict):
                raise RuntimeError(
                    f"Non-object JSONL row at "
                    f"{path}:{line_number}"
                )

            rows.append(row)

    return rows


def sha256_bytes(
    data: bytes,
) -> str:
    return hashlib.sha256(
        data
    ).hexdigest()


def lf_bytes(
    data: bytes,
) -> bytes:
    return data.replace(
        b"\r\n",
        b"\n",
    )


def crlf_from_lf(
    data: bytes,
) -> bytes:
    return lf_bytes(
        data
    ).replace(
        b"\n",
        b"\r\n",
    )


def load_gate4_artifact_eol_correction(
    root: Path,
) -> dict[str, Any]:
    path = (
        root
        / GATE4_ARTIFACT_EOL_CORRECTION_RELATIVE
    )

    if not path.is_file():
        raise RuntimeError(
            "Gate 4 artifact EOL portability "
            "correction is missing"
        )

    payload = load_json(
        path
    )

    if (
        payload.get("schema_version")
        != GATE4_ARTIFACT_EOL_CORRECTION_SCHEMA
        or payload.get("status")
        != "PASS"
        or payload.get("gate")
        != 4
        or payload.get("gate4_freeze_manifest_sha256")
        != EXPECTED_FREEZE_SHA256
        or payload.get("gate5_preregistration_sha256")
        != GATE5_PREREGISTRATION_SHA256
        or payload.get("confirmation_accessed")
        is not False
        or payload.get("confirmation_sealed")
        is not True
        or payload.get("gate5_execution_started")
        is not False
        or payload.get("scientific_content_changed")
        is not False
        or payload.get("stage3_configuration_changed")
        is not False
        or payload.get("stage3_model_changed")
        is not False
        or payload.get("generation_results_changed")
        is not False
        or payload.get("original_gate4_artifacts_modified")
        is not False
        or payload.get("original_gate4_artifact_manifest_modified")
        is not False
        or payload.get("original_gate4_freeze_manifest_modified")
        is not False
        or set(
            payload.get(
                "eol_portable_artifacts",
                [],
            )
        )
        != EXPECTED_EOL_PORTABLE_ARTIFACTS
    ):
        raise RuntimeError(
            "Gate 4 artifact EOL portability "
            "correction contract mismatch"
        )

    return payload


def verify_frozen_artifact_identity(
    *,
    root: Path,
    relative: str,
    item: dict[str, Any],
    correction: dict[str, Any],
) -> dict[str, Any]:
    path = (
        root
        / relative
    )

    if not path.is_file():
        raise RuntimeError(
            "Missing frozen Gate 4 artifact: "
            f"{relative}"
        )

    raw = path.read_bytes()

    expected_sha = (
        item[
            "sha256"
        ]
    )

    expected_bytes = int(
        item[
            "bytes"
        ]
    )

    if (
        sha256_bytes(
            raw
        )
        == expected_sha
        and len(raw)
        == expected_bytes
    ):
        return {
            "status":
                "PASS",
            "mode":
                "historical_raw_match",
        }

    record = (
        correction.get(
            "artifacts",
            {},
        ).get(
            relative
        )
        or {}
    )

    if (
        record.get(
            "mode"
        )
        != "canonical_git_lf_with_verified_crlf_equivalence"
        or record.get(
            "historical_frozen_sha256"
        )
        != expected_sha
        or int(
            record.get(
                "historical_frozen_bytes",
                -1,
            )
        )
        != expected_bytes
        or record.get(
            "text_semantic_equivalence_verified"
        )
        is not True
        or record.get(
            "lf_to_crlf_reconstruction_verified"
        )
        is not True
    ):
        raise RuntimeError(
            "Frozen Gate 4 artifact changed "
            "without a valid portability proof: "
            f"{relative}"
        )

    canonical_lf = lf_bytes(
        raw
    )

    if (
        sha256_bytes(
            canonical_lf
        )
        != record.get(
            "canonical_git_sha256_lf"
        )
        or len(
            canonical_lf
        )
        != int(
            record.get(
                "canonical_git_bytes_lf",
                -1,
            )
        )
    ):
        raise RuntimeError(
            "Frozen Gate 4 canonical LF identity "
            f"mismatch: {relative}"
        )

    historical_crlf = (
        crlf_from_lf(
            canonical_lf
        )
    )

    if (
        sha256_bytes(
            historical_crlf
        )
        != expected_sha
        or len(
            historical_crlf
        )
        != expected_bytes
        or record.get(
            "historical_reconstructed_sha256_crlf"
        )
        != expected_sha
        or int(
            record.get(
                "historical_reconstructed_bytes_crlf",
                -1,
            )
        )
        != expected_bytes
    ):
        raise RuntimeError(
            "Frozen Gate 4 historical CRLF "
            f"reconstruction mismatch: {relative}"
        )

    return {
        "status":
            "PASS",
        "mode":
            "canonical_git_lf_with_verified_crlf_equivalence",
        "canonical_lf_sha256":
            sha256_bytes(
                canonical_lf
            ),
        "historical_crlf_sha256":
            expected_sha,
    }


def verify_artifact_manifest_link_identity(
    *,
    artifact_manifest_path: Path,
    expected_sha: str,
    correction: dict[str, Any],
) -> dict[str, Any]:
    raw = (
        artifact_manifest_path
        .read_bytes()
    )

    if (
        sha256_bytes(
            raw
        )
        == expected_sha
    ):
        return {
            "status":
                "PASS",
            "mode":
                "historical_raw_match",
        }

    record = (
        correction.get(
            "artifact_manifest_link"
        )
        or {}
    )

    if (
        record.get(
            "historical_frozen_sha256"
        )
        != expected_sha
        or record.get(
            "mode"
        )
        != "canonical_git_lf_with_verified_crlf_equivalence"
    ):
        raise RuntimeError(
            "Freeze/artifact-manifest linkage mismatch"
        )

    canonical_lf = (
        lf_bytes(
            raw
        )
    )

    if (
        sha256_bytes(
            canonical_lf
        )
        != record.get(
            "canonical_git_sha256_lf"
        )
        or len(
            canonical_lf
        )
        != int(
            record.get(
                "canonical_git_bytes_lf",
                -1,
            )
        )
    ):
        raise RuntimeError(
            "Artifact-manifest canonical LF "
            "identity mismatch"
        )

    historical = (
        crlf_from_lf(
            canonical_lf
        )
    )

    if (
        sha256_bytes(
            historical
        )
        != expected_sha
        or record.get(
            "historical_reconstructed_sha256_crlf"
        )
        != expected_sha
        or len(
            historical
        )
        != int(
            record.get(
                "historical_reconstructed_bytes_crlf",
                -1,
            )
        )
    ):
        raise RuntimeError(
            "Artifact-manifest historical "
            "CRLF reconstruction mismatch"
        )

    return {
        "status":
            "PASS",
        "mode":
            "canonical_git_lf_with_verified_crlf_equivalence",
    }


def verify(
    root: Path = ROOT,
) -> dict[str, Any]:

    gate3 = verify_gate3(root)

    if (
        gate3["status"] != "PASS"
        or gate3["confirmation_accessed"] is not False
    ):
        raise RuntimeError(
            "Gate 3 upstream verification failed"
        )

    g4 = (
        root
        / "reports/final_v2/gate4"
    )

    freeze_path = (
        g4
        / "GATE4_STAGE3_FREEZE_MANIFEST.json"
    )

    if (
        sha256_file(freeze_path)
        != EXPECTED_FREEZE_SHA256
    ):
        raise RuntimeError(
            "Gate 4 freeze-manifest identity mismatch"
        )

    freeze = load_json(freeze_path)

    if (
        freeze.get("schema_version")
        != "gate4_stage3_freeze_v1"
        or freeze.get("gate") != 4
        or freeze.get("status") != "PASS"
        or freeze.get("stage3_status") != "FROZEN"
        or freeze.get("confirmation_accessed") is not False
        or freeze.get("confirmation_sealed") is not True
    ):
        raise RuntimeError(
            "Gate 4 freeze contract mismatch"
        )

    # ------------------------------------------------
    # Frozen Stage 3 configuration
    # ------------------------------------------------

    config_path = (
        root
        / "configs/stage3_semantic_generation_v2.json"
    )

    if (
        sha256_file(config_path)
        != EXPECTED_CONFIG_SHA256
    ):
        raise RuntimeError(
            "Frozen Stage 3 config hash mismatch"
        )

    config = load_json(config_path)

    expected_config = {
        "analysis_model":
            "Qwen/Qwen2.5-Coder-7B-Instruct",
        "writer_model":
            "Qwen/Qwen2.5-Coder-7B-Instruct",
        "repair_model":
            "Qwen/Qwen2.5-Coder-7B-Instruct",
        "pipeline_version":
            "stage3_semantic_generation_v2",
        "temperature": 0.1,
        "top_k_documents": 3,
        "max_repair_attempts": 1,
        "max_input_tokens": 4096,
        "max_tokens_analysis": 512,
        "max_tokens_writer": 512,
        "max_tokens_repair": 512,
    }

    if config != expected_config:
        raise RuntimeError(
            "Frozen Stage 3 settings mismatch"
        )

    if (
        freeze["stage3_config"]["sha256"]
        != EXPECTED_CONFIG_SHA256
        or freeze["stage3_config"]["settings"]
        != config
    ):
        raise RuntimeError(
            "Freeze/config linkage mismatch"
        )

    # ------------------------------------------------
    # External input + source identities
    # ------------------------------------------------

    input_path = (
        g4
        / "external_run_input_manifest.json"
    )

    if (
        sha256_file(input_path)
        != EXPECTED_INPUT_SHA256
    ):
        raise RuntimeError(
            "Gate 4 external-input hash mismatch"
        )

    external = load_json(input_path)

    if (
        external.get("confirmation_accessed") is not False
        or external.get("confirmation_paths_allowed") is not False
    ):
        raise RuntimeError(
            "Unsafe Gate 4 external-input boundary"
        )

    if (
        freeze["external_execution"][
            "input_manifest_sha256"
        ]
        != EXPECTED_INPUT_SHA256
    ):
        raise RuntimeError(
            "Freeze/input-manifest linkage mismatch"
        )

    source_hashes = freeze.get(
        "implementation_source_sha256",
        {},
    )

    if source_hashes != external.get(
        "source_sha256",
        {},
    ):
        raise RuntimeError(
            "Frozen implementation-source inventory mismatch"
        )

    for relative, expected_hash in source_hashes.items():
        actual = sha256_file(
            root / relative
        )

        if actual != expected_hash:
            raise RuntimeError(
                f"Frozen Stage 3 source mismatch: "
                f"{relative}"
            )

    # ------------------------------------------------
    # External results
    # ------------------------------------------------

    return_dir = (
        g4
        / "external_return"
    )

    results_path = (
        return_dir
        / "development_generation_results.jsonl"
    )

    checkpoint_path = (
        return_dir
        / "development_generation_checkpoint.jsonl"
    )

    receipt_path = (
        return_dir
        / "gate4_external_run_receipt.json"
    )

    archive_path = (
        return_dir
        / "gate4_external_return.zip"
    )

    archive_sha_path = (
        return_dir
        / "gate4_external_return.sha256"
    )

    if (
        sha256_file(results_path)
        != EXPECTED_RESULTS_SHA256
    ):
        raise RuntimeError(
            "Gate 4 result hash mismatch"
        )

    if (
        sha256_file(archive_path)
        != EXPECTED_ARCHIVE_SHA256
    ):
        raise RuntimeError(
            "Gate 4 return archive hash mismatch"
        )

    declared_archive_sha = (
        archive_sha_path
        .read_text(encoding="utf-8")
        .strip()
        .split()[0]
    )

    if declared_archive_sha != EXPECTED_ARCHIVE_SHA256:
        raise RuntimeError(
            "Gate 4 return SHA file mismatch"
        )

    results = load_jsonl(
        results_path
    )

    checkpoint = load_jsonl(
        checkpoint_path
    )

    if len(results) != 200:
        raise RuntimeError(
            "Gate 4 result row count mismatch"
        )

    if len(checkpoint) != 200:
        raise RuntimeError(
            "Gate 4 checkpoint row count mismatch"
        )

    run_keys = [
        str(row.get("run_key") or "")
        for row in results
    ]

    case_ids = [
        str(row.get("case_id") or "")
        for row in results
    ]

    if (
        len(set(run_keys)) != 200
        or "" in run_keys
        or len(set(case_ids)) != 200
        or "" in case_ids
    ):
        raise RuntimeError(
            "Gate 4 result identity/uniqueness mismatch"
        )

    status_counts = dict(
        sorted(
            Counter(
                str(
                    row.get("final_status")
                    or ""
                )
                for row in results
            ).items()
        )
    )

    if status_counts != EXPECTED_STATUS_COUNTS:
        raise RuntimeError(
            "Gate 4 status-count mismatch"
        )

    available = sum(
        bool(
            row.get(
                "retrieval_context_available"
            )
        )
        for row in results
    )

    if available != 91:
        raise RuntimeError(
            "Gate 4 context-availability mismatch"
        )

    total_calls = sum(
        int(
            row.get("llm_call_count")
            or 0
        )
        for row in results
    )

    if total_calls != 187:
        raise RuntimeError(
            "Gate 4 LLM-call count mismatch"
        )

    errors = Counter()

    for row in results:
        stage3 = row.get(
            "stage3_result"
        ) or {}

        error = (
            stage3.get(
                "execution_error"
            )
            or {}
        )

        if error:
            errors[
                str(
                    error.get("code")
                    or ""
                )
            ] += 1

        if (
            row.get("final_status")
            == "retrieval_context_unavailable"
        ):
            if (
                row.get(
                    "retrieval_context_available"
                ) is not False
                or int(
                    row.get(
                        "llm_call_count"
                    )
                    or 0
                ) != 0
            ):
                raise RuntimeError(
                    "No-context row violated zero-call contract"
                )

    if dict(
        sorted(errors.items())
    ) != EXPECTED_ERROR_COUNTS:
        raise RuntimeError(
            "Gate 4 execution-error count mismatch"
        )

    # ------------------------------------------------
    # Receipt
    # ------------------------------------------------

    receipt = load_json(
        receipt_path
    )

    if (
        receipt.get("status")
        != "COMPLETED_DEVELOPMENT_ONLY"
        or receipt.get("source_commit")
        != EXPECTED_EXECUTION_COMMIT
        or receipt.get(
            "input_manifest_sha256"
        ) != EXPECTED_INPUT_SHA256
        or receipt.get(
            "results_sha256"
        ) != EXPECTED_RESULTS_SHA256
        or receipt.get(
            "processed_rows"
        ) != 200
        or receipt.get(
            "stage3_invocation_count"
        ) != 91
        or receipt.get(
            "llm_call_count"
        ) != 187
        or receipt.get(
            "confirmation_accessed"
        ) is not False
    ):
        raise RuntimeError(
            "Gate 4 execution receipt mismatch"
        )

    if (
        receipt.get(
            "final_status_counts"
        )
        != EXPECTED_STATUS_COUNTS
        or receipt.get(
            "execution_error_counts"
        )
        != EXPECTED_ERROR_COUNTS
    ):
        raise RuntimeError(
            "Gate 4 receipt outcome mismatch"
        )

    runtime = receipt.get(
        "runtime",
        {},
    )

    if (
        runtime.get("model")
        != "Qwen/Qwen2.5-Coder-7B-Instruct"
        or runtime.get("precision") != "float16"
        or runtime.get("quantized") is not False
        or runtime.get("cuda_available") is not True
        or runtime.get("cuda_device_count") != 2
        or runtime.get("max_input_tokens") != 4096
    ):
        raise RuntimeError(
            "Gate 4 runtime identity mismatch"
        )

    # ------------------------------------------------
    # Canonical post-run verification
    # ------------------------------------------------

    final_results = (
        g4
        / "final_results"
    )

    postrun_path = (
        final_results
        / "postrun_verification_report.json"
    )

    postrun = load_json(
        postrun_path
    )

    if (
        postrun.get("status") != "PASS"
        or postrun.get(
            "confirmation_accessed"
        ) is not False
        or postrun.get(
            "processed_rows"
        ) != 200
        or postrun.get(
            "unique_run_keys"
        ) != 200
        or postrun.get(
            "context_available_total"
        ) != 91
        or postrun.get(
            "results_sha256"
        ) != EXPECTED_RESULTS_SHA256
        or postrun.get(
            "archive_sha256"
        ) != EXPECTED_ARCHIVE_SHA256
    ):
        raise RuntimeError(
            "Gate 4 post-run verification evidence mismatch"
        )

    # ------------------------------------------------
    # Development analysis
    # ------------------------------------------------

    analysis_path = (
        final_results
        / "gate4_development_analysis_summary.json"
    )

    analysis = load_json(
        analysis_path
    )

    if analysis.get("status") != "PASS":
        raise RuntimeError(
            "Gate 4 development analysis did not pass"
        )

    primary = analysis["primary"]
    secondary = analysis["secondary"]

    if (
        primary["sample_rows"] != 100
        or primary[
            "retrieval_context_available"
        ] != 8
        or primary[
            "retrieval_context_unavailable"
        ] != 92
        or primary[
            "conditional_generation"
        ]["accepted_total"] != 2
        or primary[
            "conditional_generation"
        ]["denominator_invoked"] != 8
    ):
        raise RuntimeError(
            "Gate 4 primary analysis mismatch"
        )

    if (
        secondary["sample_rows"] != 100
        or secondary[
            "retrieval_context_available"
        ] != 83
        or secondary[
            "retrieval_context_unavailable"
        ] != 17
        or secondary[
            "conditional_generation"
        ]["accepted_total"] != 47
        or secondary[
            "conditional_generation"
        ]["denominator_invoked"] != 83
    ):
        raise RuntimeError(
            "Gate 4 secondary analysis mismatch"
        )

    category = analysis[
        "secondary_by_predicted_category"
    ]

    expected_category = {
        "api_reference": (24, 1),
        "configuration": (20, 14),
        "developer_setup": (22, 17),
        "model_contract": (17, 15),
    }

    for label, (
        expected_context,
        expected_accepted,
    ) in expected_category.items():

        item = category[label]

        if (
            item[
                "retrieval_context_available"
            ] != expected_context
            or item[
                "conditional_generation"
            ]["accepted_total"]
            != expected_accepted
        ):
            raise RuntimeError(
                f"Gate 4 category result mismatch: "
                f"{label}"
            )

    # ------------------------------------------------
    # Artifact manifest
    # ------------------------------------------------

    artifact_manifest_path = (
        final_results
        / "artifact_manifest.json"
    )

    artifact_manifest = load_json(
        artifact_manifest_path
    )

    if (
        artifact_manifest.get("status")
        != "FROZEN"
        or artifact_manifest.get(
            "confirmation_accessed"
        ) is not False
    ):
        raise RuntimeError(
            "Gate 4 artifact manifest mismatch"
        )

    artifact_eol_correction = (
        load_gate4_artifact_eol_correction(
            root
        )
    )

    artifact_identity_results = {}

    for relative, item in (
        artifact_manifest.get(
            "artifacts",
            {}
        ).items()
    ):
        artifact_identity_results[
            relative
        ] = verify_frozen_artifact_identity(
            root=
                root,
            relative=
                relative,
            item=
                item,
            correction=
                artifact_eol_correction,
        )

    artifact_manifest_link_identity = (
        verify_artifact_manifest_link_identity(
            artifact_manifest_path=
                artifact_manifest_path,
            expected_sha=
                freeze[
                    "artifact_manifest"
                ][
                    "sha256"
                ],
            correction=
                artifact_eol_correction,
        )
    )

    correction_portable_artifacts = set(
        artifact_eol_correction.get(
            "eol_portable_artifacts",
            [],
        )
    )

    if (
        correction_portable_artifacts
        != EXPECTED_EOL_PORTABLE_ARTIFACTS
    ):
        raise RuntimeError(
            "Gate 4 portable-artifact inventory mismatch"
        )

    for relative in (
        EXPECTED_EOL_PORTABLE_ARTIFACTS
    ):
        record = (
            artifact_eol_correction.get(
                "artifacts",
                {},
            ).get(
                relative,
                {},
            )
        )

        if (
            record.get("mode")
            != "canonical_git_lf_with_verified_crlf_equivalence"
            or record.get(
                "text_semantic_equivalence_verified"
            )
            is not True
            or record.get(
                "lf_to_crlf_reconstruction_verified"
            )
            is not True
        ):
            raise RuntimeError(
                "Gate 4 portability proof record mismatch: "
                f"{relative}"
            )

    portable_count = len(
        correction_portable_artifacts
    )

    artifact_eol_portability = {
        "status":
            "PASS",
        "path":
            GATE4_ARTIFACT_EOL_CORRECTION_RELATIVE,
        "portable_artifact_count":
            portable_count,
        "portable_artifacts":
            sorted(
                EXPECTED_EOL_PORTABLE_ARTIFACTS
            ),
        "artifact_manifest_link":
            artifact_manifest_link_identity,
        "scientific_content_changed":
            False,
        "confirmation_accessed":
            False,
    }

    # ------------------------------------------------
    # External run lifecycle manifest
    # ------------------------------------------------

    run_manifest = load_json(
        g4 / "external_run_manifest.json"
    )

    if (
        run_manifest.get("status")
        != "COMPLETED_DEVELOPMENT_ONLY"
        or run_manifest.get(
            "results_present"
        ) is not True
        or run_manifest.get(
            "stage3_freeze_manifest_present"
        ) is not True
        or run_manifest.get(
            "confirmation_accessed"
        ) is not False
        or run_manifest.get(
            "source_commit"
        ) != EXPECTED_EXECUTION_COMMIT
        or run_manifest.get(
            "results_sha256"
        ) != EXPECTED_RESULTS_SHA256
        or run_manifest.get(
            "stage3_freeze_manifest_sha256"
        ) != EXPECTED_FREEZE_SHA256
    ):
        raise RuntimeError(
            "Gate 4 final external-run manifest mismatch"
        )

    # ------------------------------------------------
    # Finalization state
    # ------------------------------------------------

    state = load_json(
        root
        / "reports/final_v2/finalization_state.json"
    )

    if (
        state["gate_statuses"][
            "gate_4_stage3_retrieval_generation_study_and_freeze"
        ]
        != "PASS"
        or state["gate_statuses"][
            "gate_5_one_shot_confirmation"
        ]
        != "NOT_EXECUTED"
        or int(
            state["current_gate"]
        ) != 5
        or state[
            "confirmation_sealed"
        ] is not True
        or state.get(
            "confirmation_results_accessed_by_gate_4"
        ) is not False
        or state[
            "final_model_freeze_state"
        ][
            "stage3_freeze_manifest_present"
        ] is not True
    ):
        raise RuntimeError(
            "Gate 4 finalization-state mismatch"
        )

    if (
        state[
            "gate_4_summary"
        ][
            "freeze_manifest_sha256"
        ]
        != EXPECTED_FREEZE_SHA256
    ):
        raise RuntimeError(
            "Finalization-state freeze hash mismatch"
        )

    # ------------------------------------------------
    # Canonical map + methodology
    # ------------------------------------------------

    artifact_map = (
        root
        / "reports/final_v2/"
          "CANONICAL_ARTIFACT_MAP.md"
    ).read_text(
        encoding="utf-8"
    )

    for required in (
        "GATE4_STAGE3_FREEZE_MANIFEST.json",
        "gate4/final_results/",
        "verify_gate4_stage3_freeze.py",
    ):
        if required not in artifact_map:
            raise RuntimeError(
                "Canonical artifact map missing "
                f"{required}"
            )

    methodology = (
        g4
        / "GATE4_METHODOLOGY.md"
    ).read_text(
        encoding="utf-8"
    )

    if (
        "Status: **PASS / FROZEN**."
        not in methodology
    ):
        raise RuntimeError(
            "Gate 4 methodology not frozen"
        )

    return {
        "status": "PASS",
        "gate": 4,
        "stage3_status": "FROZEN",
        "freeze_manifest_sha256":
            EXPECTED_FREEZE_SHA256,
        "source_commit":
            EXPECTED_EXECUTION_COMMIT,
        "processed_rows": 200,
        "context_available": 91,
        "context_unavailable": 109,
        "stage3_invocation_count": 91,
        "llm_call_count": 187,
        "final_status_counts":
            EXPECTED_STATUS_COUNTS,
        "execution_error_counts":
            EXPECTED_ERROR_COUNTS,
        "primary_conditional_acceptance":
            "2/8",
        "secondary_conditional_acceptance":
            "47/83",
        "confirmation_accessed": False,
        "confirmation_sealed": True,
        "current_gate": 5,
        "gate5_status": "NOT_EXECUTED",
        "artifact_eol_portability_correction":
            artifact_eol_portability,
    }


def main() -> int:
    argparse.ArgumentParser().parse_args()

    print(
        json.dumps(
            verify(),
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
