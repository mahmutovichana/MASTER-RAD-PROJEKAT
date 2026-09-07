from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, category_eligible_rows
from docguard_ml_v2.gate2_closure import EXPECTED, load_development_without_confirmation, sha256_file
from docguard_ml_v2.gate3_freeze import GATE2_COMMIT, SERIALIZER


EXPECTED_MODELS = {
    "binary": {"sha256": "7d6a9263e1262c5c54db3d2e100209707c6a7681133fb1505f44125efa954462", "rows": 22166, "C": 0.25, "class_weight": None, "threshold": 0.15, "classes": [0, 1]},
    "category": {"sha256": "2d8123ac398568b5c9586b0f8d26d6c4079ddfebd504889b934f77bef65b9f59", "rows": 4820, "C": 4.0, "class_weight": "balanced", "threshold": None, "classes": list(PRIMARY_STAGE2_LABELS), "class_counts": {"api_reference": 1477, "configuration": 1351, "developer_setup": 967, "model_contract": 1025}},
}
EXPECTED_PROVENANCE_SHA = "4289a53522e8c264a3a9a5994dd9df031d1238085c6ae70c94e3bada33dafdc6"


EOL_CORRECTION_RELATIVE = (
    "reports/final_v2/gate3/"
    "GATE3_SELECTION_EVIDENCE_EOL_PORTABILITY_CORRECTION.json"
)

EOL_CORRECTION_SCHEMA = (
    "gate3_selection_evidence_eol_portability_correction_v1"
)

EOL_EXPECTED = {
    "binary": {
        "canonical_lf_sha256":
            "2423ac5f4f3e0e9f1e8ad2561eadbedc3c3164fccd4ff8c5c4e4de0125898f48",
        "historical_crlf_sha256":
            "a369341ea2b680a559e2475b31ce7ac8d84e16b6b7c75488466ddb881b5108af",
    },
    "category": {
        "canonical_lf_sha256":
            "8628825d56f1abe0286f8d4656f9fd9a7aa2481948b1d3d5c1c82d3547f3e711",
        "historical_crlf_sha256":
            "ebbd5e2b8e5d45f46f7325f10153acd3a805af8590f7fb3241b3dc27e18b3ed2",
    },
}

GATE5_PREREGISTRATION_COMMIT = (
    "d12e4c00c008f86bc7025b9e6de15b977f51fd57"
)

GATE5_PREREGISTRATION_SHA256 = (
    "dd4ed749774c144d3533128e93749fa003925dbdf73b1a121fee1a3fd40dc3b8"
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _lf_bytes(data: bytes) -> bytes:
    return data.replace(
        b"\r\n",
        b"\n",
    )


def _crlf_from_lf(data: bytes) -> bytes:
    return _lf_bytes(data).replace(
        b"\n",
        b"\r\n",
    )


def _load_eol_correction(
    root: Path,
) -> dict[str, Any]:
    path = (
        root
        / EOL_CORRECTION_RELATIVE
    )

    if not path.is_file():
        raise RuntimeError(
            "Gate 3 selection-evidence EOL "
            "portability correction is missing"
        )

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if (
        payload.get("schema_version")
        != EOL_CORRECTION_SCHEMA
        or payload.get("status")
        != "PASS"
        or payload.get("confirmation_accessed")
        is not False
        or payload.get("confirmation_sealed")
        is not True
        or payload.get("gate5_execution_started")
        is not False
        or payload.get("scientific_content_changed")
        is not False
        or payload.get("selection_decision_changed")
        is not False
        or payload.get("frozen_models_changed")
        is not False
        or payload.get("frozen_thresholds_changed")
        is not False
        or payload.get("original_gate3_freeze_manifests_modified")
        is not False
        or payload.get("original_gate3_training_provenance_modified")
        is not False
        or payload.get("gate5_preregistration_commit")
        != GATE5_PREREGISTRATION_COMMIT
        or payload.get("gate5_preregistration_sha256")
        != GATE5_PREREGISTRATION_SHA256
    ):
        raise RuntimeError(
            "Gate 3 EOL portability correction contract mismatch"
        )

    return payload


def _verify_eol_correction_task(
    root: Path,
    task: str,
    manifest: dict[str, Any],
    evidence_path: Path,
) -> dict[str, Any]:
    correction = _load_eol_correction(
        root
    )

    item = (
        correction.get("artifacts", {})
        .get(task, {})
    )

    expected = EOL_EXPECTED[
        task
    ]

    if (
        item.get("path")
        != manifest.get(
            "selection_evidence_path"
        )
        or item.get(
            "canonical_git_sha256_lf"
        )
        != expected[
            "canonical_lf_sha256"
        ]
        or item.get(
            "historical_freeze_sha256_crlf"
        )
        != expected[
            "historical_crlf_sha256"
        ]
        or manifest.get(
            "selection_evidence_sha256"
        )
        != expected[
            "historical_crlf_sha256"
        ]
        or item.get(
            "json_semantic_equivalence_verified"
        )
        is not True
        or item.get(
            "lf_to_crlf_reconstruction_verified"
        )
        is not True
    ):
        raise RuntimeError(
            f"{task} selection evidence "
            "EOL correction metadata mismatch"
        )

    raw = evidence_path.read_bytes()

    lf = _lf_bytes(
        raw
    )

    crlf = _crlf_from_lf(
        lf
    )

    if (
        _sha256_bytes(lf)
        != expected[
            "canonical_lf_sha256"
        ]
    ):
        raise RuntimeError(
            f"{task} selection evidence "
            "canonical LF hash mismatch"
        )

    if (
        _sha256_bytes(crlf)
        != expected[
            "historical_crlf_sha256"
        ]
    ):
        raise RuntimeError(
            f"{task} selection evidence "
            "historical CRLF reconstruction mismatch"
        )

    if (
        json.loads(
            lf.decode("utf-8")
        )
        !=
        json.loads(
            crlf.decode("utf-8")
        )
    ):
        raise RuntimeError(
            f"{task} selection evidence "
            "JSON semantic equivalence mismatch"
        )

    return {
        "status":
            "PASS",
        "mode":
            "canonical_git_lf_with_verified_crlf_equivalence",
        "canonical_lf_sha256":
            expected[
                "canonical_lf_sha256"
            ],
        "historical_crlf_sha256":
            expected[
                "historical_crlf_sha256"
            ],
    }


def verify_selection_evidence_hash(
    root: Path,
    manifest: dict[str, Any],
    task: str,
    evidence_path: Path,
) -> dict[str, Any]:
    actual = sha256_file(
        evidence_path
    )

    historical = manifest.get(
        "selection_evidence_sha256"
    )

    if actual == historical:
        return {
            "status":
                "PASS",
            "mode":
                "historical_crlf_raw_match",
            "actual_sha256":
                actual,
            "historical_crlf_sha256":
                historical,
        }

    return _verify_eol_correction_task(
        root,
        task,
        manifest,
        evidence_path,
    )


def verify_eol_portability_correction(
    root: Path,
) -> dict[str, Any]:
    correction = _load_eol_correction(
        root
    )

    tasks: dict[str, Any] = {}

    for task in (
        "binary",
        "category",
    ):
        manifest_path = (
            root
            / "reports/final_v2/gate3"
            / f"{task}_classifier_freeze_manifest.json"
        )

        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        evidence_path = (
            root
            / manifest[
                "selection_evidence_path"
            ]
        )

        tasks[task] = (
            _verify_eol_correction_task(
                root,
                task,
                manifest,
                evidence_path,
            )
        )

        model_item = (
            correction.get(
                "models",
                {},
            ).get(
                task,
                {},
            )
        )

        expected_model = (
            EXPECTED_MODELS[
                task
            ][
                "sha256"
            ]
        )

        if (
            model_item.get(
                "path"
            )
            != manifest.get(
                "model_artifact_path"
            )
            or model_item.get(
                "sha256"
            )
            != expected_model
            or sha256_file(
                root
                / manifest[
                    "model_artifact_path"
                ]
            )
            != expected_model
        ):
            raise RuntimeError(
                f"{task} model changed during "
                "EOL portability correction"
            )

    return {
        "status":
            "PASS",
        "path":
            EOL_CORRECTION_RELATIVE,
        "scientific_content_changed":
            False,
        "confirmation_accessed":
            False,
        "tasks":
            tasks,
    }


CHILD_LINK_CORRECTION_RELATIVE = (
    "reports/final_v2/gate3/"
    "GATE3_CHILD_MANIFEST_LINK_EOL_PORTABILITY_CORRECTION.json"
)

CHILD_LINK_CORRECTION_SCHEMA = (
    "gate3_child_manifest_link_eol_portability_correction_v1"
)

CHILD_LINK_SPECIAL_LF_KEYS = (
    "source_commit",
    "source_commit_semantics",
    "training_provenance_path",
    "training_provenance_sha256",
)

CHILD_LINK_EXPECTED = {
    "binary": {
        "canonical_lf_sha256":
            "1d6556d09cfc50df2fd9ea09e7cbd07e9fbe2778d19aa7e0b479a3853ee393f2",
        "historical_mixed_eol_sha256":
            "0440a0a776ea388ea9953085d9e41e06c5a179208e105cd4ff452739ebc36fc0",
        "lf_only_lines":
            [54, 55, 56, 57],
    },
    "category": {
        "canonical_lf_sha256":
            "72645db87c50b0a78edce08731166c84b1c0c46ec130dd4a44800b6ff8a96a36",
        "historical_mixed_eol_sha256":
            "7959a014cac7bee961c47182bbf9fc035fda13a7d1873128562807a585b585fc",
        "lf_only_lines":
            [61, 62, 63, 64],
    },
}


def _load_child_link_correction(
    root: Path,
) -> dict[str, Any]:
    path = (
        root
        / CHILD_LINK_CORRECTION_RELATIVE
    )

    if not path.is_file():
        raise RuntimeError(
            "Gate 3 child-manifest link "
            "EOL portability correction is missing"
        )

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if (
        payload.get("schema_version")
        != CHILD_LINK_CORRECTION_SCHEMA
        or payload.get("status")
        != "PASS"
        or payload.get("confirmation_accessed")
        is not False
        or payload.get("confirmation_sealed")
        is not True
        or payload.get("gate5_execution_started")
        is not False
        or payload.get("scientific_content_changed")
        is not False
        or payload.get("selection_decision_changed")
        is not False
        or payload.get("frozen_models_changed")
        is not False
        or payload.get("frozen_thresholds_changed")
        is not False
        or payload.get("original_gate3_child_manifests_modified")
        is not False
        or payload.get("original_gate3_overall_manifest_modified")
        is not False
        or payload.get("gate5_preregistration_commit")
        != GATE5_PREREGISTRATION_COMMIT
        or payload.get("gate5_preregistration_sha256")
        != GATE5_PREREGISTRATION_SHA256
    ):
        raise RuntimeError(
            "Gate 3 child-manifest link "
            "portability correction contract mismatch"
        )

    rule = (
        payload.get(
            "historical_eol_rule"
        )
        or {}
    )

    if (
        rule.get("default")
        != "CRLF"
        or rule.get(
            "LF_only_json_keys"
        )
        != list(
            CHILD_LINK_SPECIAL_LF_KEYS
        )
    ):
        raise RuntimeError(
            "Gate 3 child-manifest historical "
            "EOL rule mismatch"
        )

    return payload


def _reconstruct_historical_child_manifest(
    canonical_lf: bytes,
) -> tuple[bytes, list[int]]:
    lines = (
        _lf_bytes(
            canonical_lf
        )
        .decode("utf-8")
        .splitlines()
    )

    output = bytearray()
    lf_only_lines: list[int] = []

    for line_number, line in enumerate(
        lines,
        start=1,
    ):
        stripped = line.lstrip()

        special = any(
            stripped.startswith(
                f'"{key}":'
            )
            for key in
            CHILD_LINK_SPECIAL_LF_KEYS
        )

        output.extend(
            line.encode("utf-8")
        )

        if special:
            output.extend(
                b"\n"
            )
            lf_only_lines.append(
                line_number
            )
        else:
            output.extend(
                b"\r\n"
            )

    return (
        bytes(output),
        lf_only_lines,
    )


def verify_child_manifest_link_hash(
    root: Path,
    task: str,
    linked: dict[str, Any],
    manifest_path: Path,
) -> dict[str, Any]:
    correction = (
        _load_child_link_correction(
            root
        )
    )

    item = (
        correction.get(
            "artifacts",
            {},
        ).get(
            task,
            {},
        )
    )

    expected = (
        CHILD_LINK_EXPECTED[
            task
        ]
    )

    if (
        item.get("path")
        != linked.get("path")
        or item.get(
            "canonical_git_sha256_lf"
        )
        != expected[
            "canonical_lf_sha256"
        ]
        or item.get(
            "historical_overall_link_sha256_mixed_eol"
        )
        != expected[
            "historical_mixed_eol_sha256"
        ]
        or item.get(
            "historical_lf_only_lines"
        )
        != expected[
            "lf_only_lines"
        ]
        or item.get(
            "historical_lf_only_json_keys"
        )
        != list(
            CHILD_LINK_SPECIAL_LF_KEYS
        )
        or item.get(
            "json_semantic_equivalence_verified"
        )
        is not True
        or item.get(
            "mixed_eol_reconstruction_verified"
        )
        is not True
        or linked.get(
            "sha256"
        )
        != expected[
            "historical_mixed_eol_sha256"
        ]
    ):
        raise RuntimeError(
            f"Overall {task} manifest "
            "link portability metadata mismatch"
        )

    raw = (
        manifest_path
        .read_bytes()
    )

    canonical_lf = (
        _lf_bytes(
            raw
        )
    )

    if (
        _sha256_bytes(
            canonical_lf
        )
        != expected[
            "canonical_lf_sha256"
        ]
    ):
        raise RuntimeError(
            f"Overall {task} child manifest "
            "canonical LF hash mismatch"
        )

    historical, lf_only_lines = (
        _reconstruct_historical_child_manifest(
            canonical_lf
        )
    )

    if (
        lf_only_lines
        != expected[
            "lf_only_lines"
        ]
    ):
        raise RuntimeError(
            f"Overall {task} child manifest "
            "mixed-EOL line profile mismatch"
        )

    if (
        _sha256_bytes(
            historical
        )
        != expected[
            "historical_mixed_eol_sha256"
        ]
    ):
        raise RuntimeError(
            f"Overall {task} child manifest "
            "historical mixed-EOL reconstruction mismatch"
        )

    if (
        json.loads(
            canonical_lf.decode(
                "utf-8"
            )
        )
        !=
        json.loads(
            historical.decode(
                "utf-8"
            )
        )
    ):
        raise RuntimeError(
            f"Overall {task} child manifest "
            "JSON semantic equivalence mismatch"
        )

    raw_hash = (
        _sha256_bytes(
            raw
        )
    )

    mode = (
        "historical_mixed_eol_raw_match"
        if raw_hash
        == expected[
            "historical_mixed_eol_sha256"
        ]
        else
        "canonical_git_lf_with_verified_mixed_eol_equivalence"
    )

    return {
        "status":
            "PASS",
        "mode":
            mode,
        "canonical_lf_sha256":
            expected[
                "canonical_lf_sha256"
            ],
        "historical_mixed_eol_sha256":
            expected[
                "historical_mixed_eol_sha256"
            ],
        "scientific_content_changed":
            False,
        "confirmation_accessed":
            False,
    }


def verify_child_manifest_link_portability(
    root: Path,
    overall: dict[str, Any],
) -> dict[str, Any]:
    tasks: dict[str, Any] = {}

    for task in (
        "binary",
        "category",
    ):
        linked = overall[
            task
        ]

        manifest_path = (
            root
            / linked[
                "path"
            ]
        )

        tasks[task] = (
            verify_child_manifest_link_hash(
                root,
                task,
                linked,
                manifest_path,
            )
        )

    return {
        "status":
            "PASS",
        "path":
            CHILD_LINK_CORRECTION_RELATIVE,
        "scientific_content_changed":
            False,
        "confirmation_accessed":
            False,
        "tasks":
            tasks,
    }


def assert_gate2_winners(payload: dict[str, Any]) -> None:
    if payload.get("binary", {}).get("selected_family") != "M1" or payload.get("category", {}).get("selected_family") != "M1":
        raise RuntimeError("Gate 2 winner mismatch")


def verify_classifier_manifest(root: Path, manifest_path: Path, task: str) -> dict[str, Any]:
    expected = EXPECTED_MODELS[task]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {
        "schema_version": "gate3_classifier_freeze_manifest_v1", "status": "FROZEN", "task": task,
        "selected_family": "M1", "selected_family_name": "canonical_char_tfidf_logistic_regression",
        "gate1_gold_sha256": EXPECTED["gold_sha256"], "gate2_closure_commit": GATE2_COMMIT,
        "gate2_return_archive_sha256": EXPECTED["return_archive_sha256"], "scientific_config_sha256": EXPECTED["config_sha256"],
        "safe_fields": list(SAFE_MODEL_FIELDS), "serializer": SERIALIZER, "confirmation_accessed": False,
        "training_provenance_sha256": EXPECTED_PROVENANCE_SHA,
    }
    for key, value in required.items():
        if manifest.get(key) != value: raise RuntimeError(f"{task} manifest mismatch: {key}")
    if manifest.get("source_commit") != GATE2_COMMIT or "upstream repository context" not in manifest.get("source_commit_semantics", ""):
        raise RuntimeError(f"{task} source provenance semantics mismatch")
    if manifest.get("training_data", {}).get("development_view_sha256") != EXPECTED["development_view_sha256"] or manifest["training_data"].get("eligible_rows") != expected["rows"] or manifest["training_data"].get("confirmation_excluded_rows") != 3747:
        raise RuntimeError(f"{task} training-data identity mismatch")
    if manifest.get("classifier", {}).get("C") != expected["C"] or manifest["classifier"].get("class_weight") != expected["class_weight"]:
        raise RuntimeError(f"{task} frozen classifier configuration mismatch")
    if manifest.get("final_threshold") != expected["threshold"]:
        raise RuntimeError(f"{task} frozen threshold mismatch")
    if manifest.get("classes") != expected["classes"] or (task == "category" and manifest.get("class_counts") != expected["class_counts"]):
        raise RuntimeError(f"{task} class contract mismatch")
    if not all(manifest.get("reproducibility", {}).get(key) is True for key in ("predictions_exact", "probabilities_atol_1e-12", "vocabulary_exact", "coefficients_atol_1e-12")) or manifest["reproducibility"].get("status") != "PASS":
        raise RuntimeError(f"{task} reproducibility evidence mismatch")
    provenance_path = root / manifest["training_provenance_path"]
    if sha256_file(provenance_path) != EXPECTED_PROVENANCE_SHA:
        raise RuntimeError(f"{task} training provenance hash mismatch")
    evidence_path = root / manifest["selection_evidence_path"]
    selection_evidence_verification = verify_selection_evidence_hash(
        root,
        manifest,
        task,
        evidence_path,
    )
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if evidence.get("task") != task or evidence.get("row_count") != expected["rows"] or evidence.get("confirmation_accessed") is not False or any(fold.get("repository_overlap") != 0 for fold in evidence.get("fold_audit", [])) or len(evidence.get("fold_audit", [])) != 5:
        raise RuntimeError(f"{task} selection evidence contract mismatch")
    selected = evidence.get("selected", {})
    if selected.get("candidate") != {"C": expected["C"], "class_weight": expected["class_weight"]} or selected.get("selected_threshold") != expected["threshold"]:
        raise RuntimeError(f"{task} selection evidence does not support frozen configuration")
    model_path = root / manifest["model_artifact_path"]
    if sha256_file(model_path) != expected["sha256"] or manifest.get("model_sha256") != expected["sha256"]:
        raise RuntimeError(f"{task} model artifact hash mismatch")
    payload = joblib.load(model_path)
    if payload.get("task") != task or payload.get("family") != "M1" or payload.get("safe_fields") != list(SAFE_MODEL_FIELDS) or payload.get("serializer") != SERIALIZER or payload.get("confirmation_accessed") is not False or payload.get("threshold") != expected["threshold"]:
        raise RuntimeError(f"{task} model payload contract mismatch")
    model = payload["model"]; vectorizer = model.named_steps["tfidf"]; classifier = model.named_steps["classifier"]
    if vectorizer.analyzer != "char_wb" or tuple(vectorizer.ngram_range) != (3, 5) or vectorizer.min_df != 1 or vectorizer.max_features != 80000 or vectorizer.sublinear_tf is not True:
        raise RuntimeError(f"{task} vectorizer mismatch")
    if classifier.C != expected["C"] or classifier.class_weight != expected["class_weight"] or classifier.random_state != 42 or list(classifier.classes_) != expected["classes"]:
        raise RuntimeError(f"{task} loaded classifier mismatch")
    return {
        "task": task,
        "model_sha256": expected["sha256"],
        "selection_evidence_sha256":
            manifest["selection_evidence_sha256"],
        "selection_evidence_verification":
            selection_evidence_verification,
        "status": "PASS",
    }


def verify(root: Path = PROJECT_ROOT) -> dict[str, Any]:
    if sha256_file(root/"experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl") != EXPECTED["gold_sha256"] or sha256_file(root/"configs/final_v2/gate2_model_study.json") != EXPECTED["config_sha256"]:
        raise RuntimeError("Gate 1/2 immutable identity mismatch")
    for task in ("binary", "category"):
        if sha256_file(root/f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv") != EXPECTED[f"{task}_fold_sha256"]: raise RuntimeError(f"{task} fold identity mismatch")
    gate2_summary=json.loads((root/"reports/final_v2/gate2/final_results/gate2_final_summary.json").read_text()); winners=json.loads((root/"reports/final_v2/gate2/final_results/winner_decision.json").read_text())
    if gate2_summary.get("status")!="PASS" or gate2_summary.get("confirmation_accessed") is not False or gate2_summary.get("raw_return_archive_sha256")!=EXPECTED["return_archive_sha256"]: raise RuntimeError("Gate 2 closure mismatch")
    assert_gate2_winners(winners)
    rows,view=load_development_without_confirmation(root); category_rows=category_eligible_rows(rows,allowed_partitions={"development_train","development_validation"})
    if len(rows)!=22166 or len(category_rows)!=4820 or view.get("confirmation_accessed") is not False: raise RuntimeError("Development-only universe mismatch")
    provenance_path=root/"reports/final_v2/gate3/GATE3_TRAINING_PROVENANCE.json"; provenance=json.loads(provenance_path.read_text())
    if sha256_file(provenance_path)!=EXPECTED_PROVENANCE_SHA or provenance.get("confirmation_accessed") is not False or provenance.get("gate4_status")!="NOT_EXECUTED": raise RuntimeError("Gate 3 provenance mismatch")
    for relative,expected_hash in provenance["implementation_source_hashes"].items():
        if sha256_file(root/relative)!=expected_hash: raise RuntimeError(f"Gate 3 implementation source mismatch: {relative}")
    eol_correction = verify_eol_portability_correction(root)
    binary=verify_classifier_manifest(root,root/"reports/final_v2/gate3/binary_classifier_freeze_manifest.json","binary"); category=verify_classifier_manifest(root,root/"reports/final_v2/gate3/category_classifier_freeze_manifest.json","category")
    overall_path=root/"reports/final_v2/gate3/GATE3_CLASSIFIER_FREEZE_MANIFEST.json"; overall=json.loads(overall_path.read_text())
    if overall.get("status")!="PASS" or overall.get("confirmation_accessed") is not False or overall.get("confirmation_sealed") is not True or overall.get("gate4_status")!="NOT_EXECUTED" or overall.get("selected_families")!={"binary":"M1","category":"M1"}: raise RuntimeError("Overall Gate 3 manifest mismatch")
    child_manifest_link_portability = verify_child_manifest_link_portability(
        root,
        overall,
    )
    for task,item in (("binary",binary),("category",category)):
        linked=overall[task]
        if linked["model_sha256"]!=item["model_sha256"]:
            raise RuntimeError(f"Overall {task} model link mismatch")
    state=json.loads((root/"reports/final_v2/finalization_state.json").read_text())
    gate4_status=state["gate_statuses"]["gate_4_stage3_retrieval_generation_study_and_freeze"]
    current_gate=int(state["current_gate"])
    valid_downstream_lifecycle=(
        (gate4_status in {"NOT_EXECUTED","IN_PROGRESS_EXTERNAL_COMPUTE_REQUIRED"} and current_gate==4)
        or
        (gate4_status=="PASS" and current_gate>=5)
    )
    if state["gate_statuses"]["gate_3_final_classifier_selection_and_freeze"]!="PASS" or not valid_downstream_lifecycle or state.get("confirmation_results_accessed_by_gate_3") is not False or state["confirmation_sealed"] is not True: raise RuntimeError("Gate 3 finalization state mismatch")
    sample=rows[0]; forbidden={**sample,"docs_after_excerpt":"MUTATION","pr_title":"MUTATION","label_source":"MUTATION"}
    for task in ("binary","category"):
        payload=joblib.load(root/f"models/final_v2/gate3/{task}_m1_gate3.joblib"); model=payload["model"]
        a=model.predict_proba([sample]); b=model.predict_proba([forbidden])
        if not np.array_equal(a,b): raise RuntimeError(f"Forbidden fields altered {task} inference")
        empty={field:"" for field in SAFE_MODEL_FIELDS}; first=model.predict_proba([empty]); second=model.predict_proba([empty])
        if not np.array_equal(first,second): raise RuntimeError(f"Empty-field {task} inference is nondeterministic")
    return {
        "status": "PASS",
        "gate": 3,
        "binary": binary,
        "category": category,
        "development_rows": 22166,
        "category_rows": 4820,
        "confirmation_accessed": False,
        "confirmation_sealed": True,
        "gate4_status": gate4_status,
        "current_gate": current_gate,
        "selection_evidence_eol_portability_correction":
            eol_correction,
        "child_manifest_link_eol_portability_correction":
            child_manifest_link_portability,
    }


def main()->int:
    argparse.ArgumentParser().parse_args(); print(json.dumps(verify(),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
