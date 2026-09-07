from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from scripts.verify_gate3_classifier_freeze import (
    verify as verify_gate3,
)
from scripts.verify_gate4_stage3_freeze import (
    verify as verify_gate4,
)


GATE4_CLOSURE_COMMIT = (
    "fc49c94d6c6e4c575299e7a4df15985bcea71484"
)

BINARY_SHA = (
    "7d6a9263e1262c5c54db3d2e100209707"
    "c6a7681133fb1505f44125efa954462"
)

CATEGORY_SHA = (
    "2d8123ac398568b5c9586b0f8d26d6c40"
    "79ddfebd504889b934f77bef65b9f59"
)

GATE4_FREEZE_SHA = (
    "8d2d7911330d15d04e8b628200252e6c"
    "1a614344651596064b293b17b707076f"
)

STAGE3_CONFIG_SHA = (
    "27c234a3f998c34256025b0d914ddf3fd"
    "2a202eb3466b37a25f5aed0283e3192"
)

RESULT_FILENAMES = {
    "confirmation_predictions.jsonl",
    "confirmation_metrics.json",
    "confirmation_evaluation_receipt.json",
    "stage3_confirmation_generation_results.jsonl",
    "stage3_confirmation_generation_checkpoint.jsonl",
    "stage3_confirmation_generation_receipt.json",
    "GATE5_MASTER_ONE_SHOT_RECEIPT.json",
    "GATE5_ONE_SHOT_STARTED.json",
}


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(
                chunk
            )

    return digest.hexdigest()


def canonical_json_sha(
    payload: object,
) -> str:
    data = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(
        data
    ).hexdigest()


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


def verify_gate4_ancestor(
    root: Path,
) -> None:
    result = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            GATE4_CLOSURE_COMMIT,
            "HEAD",
        ],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Gate 4 closure commit is not an ancestor of HEAD."
        )


def verify(
    root: Path = ROOT,
) -> dict[str, Any]:

    # IMPORTANT:
    # This verifier intentionally never resolves, opens,
    # reads or hashes confirmation.jsonl.

    verify_gate4_ancestor(
        root
    )

    gate3 = verify_gate3(
        root
    )

    gate3_eol = (
        gate3.get(
            "selection_evidence_eol_portability_correction"
        )
        or {}
    )

    if (
        gate3_eol.get(
            "status"
        )
        != "PASS"
        or gate3_eol.get(
            "scientific_content_changed"
        )
        is not False
        or gate3_eol.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 3 selection-evidence "
            "EOL portability correction failed."
        )

    gate3_child_link = (
        gate3.get(
            "child_manifest_link_eol_portability_correction"
        )
        or {}
    )

    if (
        gate3_child_link.get(
            "status"
        )
        != "PASS"
        or gate3_child_link.get(
            "scientific_content_changed"
        )
        is not False
        or gate3_child_link.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 3 child-manifest link "
            "portability correction failed."
        )

    gate4 = verify_gate4(
        root
    )

    if (
        gate3.get(
            "status"
        )
        != "PASS"
        or gate3.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 3 upstream verification failed."
        )

    if (
        gate4.get(
            "status"
        )
        != "PASS"
        or gate4.get(
            "stage3_status"
        )
        != "FROZEN"
        or gate4.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 4 upstream verification failed."
        )

    gate5 = (
        root
        / "reports/final_v2/gate5"
    )

    prereg_path = (
        gate5
        / "GATE5_PREREGISTRATION.json"
    )

    preflight_path = (
        gate5
        / "GATE5_PREFLIGHT.md"
    )

    runner_path = (
        root
        / "scripts/run_gate5_one_shot_qwen.py"
    )

    bootstrap_path = (
        root
        / "docguard_eval_v2/gate5_bootstrap.py"
    )

    correction_path = (
        root
        / "reports/final_v2/gate3/"
          "GATE3_SELECTION_EVIDENCE_EOL_PORTABILITY_CORRECTION.json"
    )

    child_link_correction_path = (
        root
        / "reports/final_v2/gate3/"
          "GATE3_CHILD_MANIFEST_LINK_EOL_PORTABILITY_CORRECTION.json"
    )

    classifier_canary_path = (
        root
        / "reports/final_v2/gate5/"
          "GATE5_CLASSIFIER_RUNTIME_PORTABILITY_CANARY.json"
    )

    for required in (
        prereg_path,
        preflight_path,
        runner_path,
        bootstrap_path,
        correction_path,
        child_link_correction_path,
        classifier_canary_path,
    ):
        if not required.is_file():
            raise RuntimeError(
                f"Missing Gate 5 preflight artifact: {required}"
            )

    classifier_canary = load_json(
        classifier_canary_path
    )

    if (
        classifier_canary.get("schema_version")
        != "gate5_classifier_runtime_portability_canary_v1"
        or classifier_canary.get("status")
        != "REFERENCE_FROZEN_PRE_CONFIRMATION"
        or classifier_canary.get("confirmation_accessed")
        is not False
        or classifier_canary.get("confirmation_sealed")
        is not True
        or classifier_canary.get("development_only")
        is not True
        or classifier_canary.get("gate5_execution_started")
        is not False
        or classifier_canary.get("scientific_method_changed")
        is not False
        or classifier_canary.get("model_selection_changed")
        is not False
        or classifier_canary.get("threshold_changed")
        is not False
        or classifier_canary.get("source_runtime")
        != {'python': '3.14.0', 'sklearn': '1.8.0', 'numpy': '2.4.0', 'joblib': '1.5.3'}
        or classifier_canary.get("target_execution_runtime")
        != {'python': '3.12.13', 'sklearn': '1.8.0', 'numpy': '2.4.0', 'joblib': '1.5.3'}
        or canonical_json_sha(classifier_canary)
        != "c90881179b6c92df6ac0cca51c5bb9f84f2fd13140d41273e118a0cca0499439"
    ):
        raise RuntimeError(
            "Gate 5 classifier runtime portability "
            "canary contract mismatch."
        )

    for task, expected_model in (
        ("binary", BINARY_SHA),
        ("category", CATEGORY_SHA),
    ):
        item = (
            classifier_canary.get(
                "models",
                {},
            ).get(
                task,
                {},
            )
        )

        task_canary = (
            classifier_canary.get(
                "tasks",
                {},
            ).get(
                task,
                {},
            )
        )

        if (
            item.get("sha256")
            != expected_model
            or task_canary.get("sample_rows")
            != 128
            or len(
                task_canary.get(
                    "case_ids",
                    [],
                )
            )
            != 128
        ):
            raise RuntimeError(
                f"Gate 5 {task} classifier "
                "canary identity mismatch."
            )

    prereg = load_json(
        prereg_path
    )

    if (
        prereg.get(
            "schema_version"
        )
        != "gate5_preregistration_v1"
        or prereg.get(
            "gate"
        )
        != 5
        or prereg.get(
            "status"
        )
        != "PREPARED_NOT_ACTIVATED"
    ):
        raise RuntimeError(
            "Gate 5 preregistration state mismatch."
        )

    boundary = (
        prereg.get(
            "confirmation_boundary"
        )
        or {}
    )

    if (
        boundary.get(
            "confirmation_sealed_before_gate5"
        )
        is not True
        or boundary.get(
            "confirmation_accessed_during_preregistration"
        )
        is not False
        or boundary.get(
            "no_hashing_before_one_shot"
        )
        is not True
        or boundary.get(
            "no_sampling_before_one_shot"
        )
        is not True
        or boundary.get(
            "no_metric_computation_before_one_shot"
        )
        is not True
    ):
        raise RuntimeError(
            "Unsafe Gate 5 confirmation boundary."
        )

    upstream = (
        prereg.get(
            "upstream"
        )
        or {}
    )

    if (
        upstream.get(
            "gate4_closure_commit"
        )
        != GATE4_CLOSURE_COMMIT
    ):
        raise RuntimeError(
            "Gate 4 closure identity mismatch."
        )

    binary = (
        upstream.get(
            "binary_model"
        )
        or {}
    )

    category = (
        upstream.get(
            "category_model"
        )
        or {}
    )

    stage3 = (
        upstream.get(
            "stage3_config"
        )
        or {}
    )

    gate4_freeze = (
        upstream.get(
            "gate4_stage3_freeze_manifest"
        )
        or {}
    )

    if (
        binary.get(
            "sha256"
        )
        != BINARY_SHA
        or binary.get(
            "threshold"
        )
        != 0.15
        or category.get(
            "sha256"
        )
        != CATEGORY_SHA
        or stage3.get(
            "sha256"
        )
        != STAGE3_CONFIG_SHA
        or gate4_freeze.get(
            "sha256"
        )
        != GATE4_FREEZE_SHA
    ):
        raise RuntimeError(
            "Gate 5 preregistered frozen identity mismatch."
        )

    actual_binary = sha256_file(
        root
        / binary["path"]
    )

    actual_category = sha256_file(
        root
        / category["path"]
    )

    actual_stage3 = sha256_file(
        root
        / stage3["path"]
    )

    actual_gate4_freeze = sha256_file(
        root
        / gate4_freeze["path"]
    )

    if (
        actual_binary
        != BINARY_SHA
        or actual_category
        != CATEGORY_SHA
        or actual_stage3
        != STAGE3_CONFIG_SHA
        or actual_gate4_freeze
        != GATE4_FREEZE_SHA
    ):
        raise RuntimeError(
            "Actual frozen artifact identity mismatch."
        )

    for section_name in (
        "binary_confirmation",
        "category_confirmation",
    ):
        ci = (
            prereg[
                section_name
            ][
                "confidence_intervals"
            ]
        )

        if (
            ci.get(
                "method"
            )
            != "repository_cluster_bootstrap"
            or ci.get(
                "sampling_unit"
            )
            != "repository"
            or ci.get(
                "n_bootstrap"
            )
            != 2000
            or ci.get(
                "seed"
            )
            != 42
            or ci.get(
                "alpha"
            )
            != 0.05
        ):
            raise RuntimeError(
                f"Gate 5 bootstrap policy mismatch: {section_name}"
            )

    if (
        prereg[
            "binary_confirmation"
        ][
            "primary_metric"
        ]
        != "mcc"
        or prereg[
            "category_confirmation"
        ][
            "primary_metric"
        ]
        != "macro_f1"
    ):
        raise RuntimeError(
            "Gate 5 primary metric preregistration mismatch."
        )

    one_shot = (
        prereg.get(
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
            "post_confirmation_tuning_allowed"
        )
        is not False
        or one_shot.get(
            "master_receipt_written_last"
        )
        is not True
    ):
        raise RuntimeError(
            "Gate 5 one-shot contract mismatch."
        )

    runner_text = runner_path.read_text(
        encoding="utf-8"
    )

    if (
        "--execute-one-shot"
        not in runner_text
        or "require_execute_one_shot"
        not in runner_text
        or "GATE5_MASTER_ONE_SHOT_RECEIPT.json"
        not in runner_text
    ):
        raise RuntimeError(
            "Gate 5 runner explicit-execution guard missing."
        )

    if "--allow-repeat" in runner_text:
        raise RuntimeError(
            "Canonical Gate 5 runner exposes an allow-repeat CLI."
        )

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
        or state.get(
            "confirmation_sealed"
        )
        is not True
        or state.get(
            "confirmation_results_accessed_by_gate_5",
            False,
        )
        is not False
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
    ):
        raise RuntimeError(
            "Finalization state is not safely prepared for Gate 5."
        )

    summary = (
        state.get(
            "gate_5_summary"
        )
        or {}
    )

    if (
        summary.get(
            "status"
        )
        != "PREPARED_NOT_ACTIVATED"
        or summary.get(
            "confirmation_accessed"
        )
        is not False
        or summary.get(
            "execution_completed"
        )
        is not False
    ):
        raise RuntimeError(
            "Gate 5 summary mismatch."
        )

    output_root = (
        gate5
        / "one_shot"
    )

    found_results: list[str] = []

    if output_root.exists():
        for candidate in (
            output_root.rglob("*")
        ):
            if (
                candidate.is_file()
                and candidate.name
                in RESULT_FILENAMES
            ):
                found_results.append(
                    str(
                        candidate.relative_to(
                            root
                        )
                    )
                )

    if found_results:
        raise RuntimeError(
            "Gate 5 execution artifacts already exist: "
            f"{sorted(found_results)}"
        )

    artifact_map = (
        root
        / "reports/final_v2/"
          "CANONICAL_ARTIFACT_MAP.md"
    ).read_text(
        encoding="utf-8"
    )

    for required_path in (
        "reports/final_v2/gate5/GATE5_PREREGISTRATION.json",
        "reports/final_v2/gate5/GATE5_PREFLIGHT.md",
        "scripts/verify_gate5_preregistration.py",
        "scripts/run_gate5_one_shot_qwen.py",
        "docguard_eval_v2/gate5_bootstrap.py",
        "reports/final_v2/gate3/GATE3_SELECTION_EVIDENCE_EOL_PORTABILITY_CORRECTION.json",
        "reports/final_v2/gate3/GATE3_CHILD_MANIFEST_LINK_EOL_PORTABILITY_CORRECTION.json",
        "reports/final_v2/gate5/GATE5_CLASSIFIER_RUNTIME_PORTABILITY_CANARY.json",
    ):
        if required_path not in artifact_map:
            raise RuntimeError(
                "Canonical artifact map missing Gate 5 path: "
                f"{required_path}"
            )

    return {
        "status":
            "PASS",
        "gate":
            5,
        "preflight_status":
            "PREPARED_NOT_ACTIVATED",
        "gate4_closure_ancestor":
            True,
        "binary_model_sha256":
            BINARY_SHA,
        "category_model_sha256":
            CATEGORY_SHA,
        "gate4_stage3_freeze_sha256":
            GATE4_FREEZE_SHA,
        "stage3_config_sha256":
            STAGE3_CONFIG_SHA,
        "bootstrap_method":
            "repository_cluster_bootstrap",
        "bootstrap_replicates":
            2000,
        "bootstrap_seed":
            42,
        "current_gate":
            5,
        "gate5_execution":
            "NOT_EXECUTED",
        "confirmation_accessed":
            False,
        "confirmation_sealed":
            True,
        "execution_artifacts_present":
            False,
        "gate3_eol_portability_correction":
            "PASS",
        "gate3_eol_portability_correction_sha256":
            sha256_file(
                correction_path
            ),
        "gate3_child_manifest_link_portability":
            "PASS",
        "gate3_child_manifest_link_portability_sha256":
            sha256_file(
                child_link_correction_path
            ),
        "classifier_runtime_canary":
            "REFERENCE_FROZEN_PRE_CONFIRMATION",
        "classifier_runtime_canary_canonical_sha256":
            "c90881179b6c92df6ac0cca51c5bb9f84f2fd13140d41273e118a0cca0499439",
        "preregistration_sha256":
            sha256_file(
                prereg_path
            ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify Gate 5 preregistration without "
            "accessing the sealed confirmation split."
        )
    )

    parser.parse_args()

    print(
        json.dumps(
            verify(),
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
