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

    for relative, item in (
        artifact_manifest.get(
            "artifacts",
            {}
        ).items()
    ):
        path = root / relative

        if not path.is_file():
            raise RuntimeError(
                f"Missing frozen Gate 4 artifact: "
                f"{relative}"
            )

        if (
            sha256_file(path)
            != item["sha256"]
            or path.stat().st_size
            != item["bytes"]
        ):
            raise RuntimeError(
                f"Frozen Gate 4 artifact changed: "
                f"{relative}"
            )

    if (
        freeze["artifact_manifest"]["sha256"]
        != sha256_file(
            artifact_manifest_path
        )
    ):
        raise RuntimeError(
            "Freeze/artifact-manifest linkage mismatch"
        )

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
