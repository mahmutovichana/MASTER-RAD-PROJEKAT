from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts.verify_gate3_classifier_freeze import assert_gate2_winners, verify, verify_classifier_manifest, verify_child_manifest_link_hash


ROOT = Path(__file__).resolve().parents[1]


def _sandbox_task(tmp_path: Path, task: str) -> tuple[Path, Path]:
    manifest_source=ROOT/f"reports/final_v2/gate3/{task}_classifier_freeze_manifest.json"
    manifest=json.loads(manifest_source.read_text())
    for relative in (manifest["model_artifact_path"],manifest["selection_evidence_path"],manifest["training_provenance_path"]):
        target=tmp_path/relative; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/relative,target)
    target_manifest=tmp_path/manifest_source.relative_to(ROOT); target_manifest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(manifest_source,target_manifest)
    correction_source=ROOT/"reports/final_v2/gate3/GATE3_SELECTION_EVIDENCE_EOL_PORTABILITY_CORRECTION.json"
    correction_target=tmp_path/correction_source.relative_to(ROOT)
    correction_target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(correction_source,correction_target)
    return tmp_path,target_manifest


def test_gate3_freeze_verifier_passes() -> None:
    result=verify()
    assert result["status"]=="PASS"
    assert result["confirmation_accessed"] is False
    assert result["gate4_status"]=="PASS"
    assert result["current_gate"] >= 5


def test_model_hash_corruption_rejected(tmp_path: Path) -> None:
    root,manifest_path=_sandbox_task(tmp_path,"binary"); manifest=json.loads(manifest_path.read_text()); (root/manifest["model_artifact_path"]).write_bytes(b"corrupt")
    with pytest.raises(RuntimeError,match="model artifact hash"): verify_classifier_manifest(root,manifest_path,"binary")


@pytest.mark.parametrize("field,value,match",[("final_threshold",0.20,"threshold"),("scientific_config_sha256","bad","scientific_config"),("safe_fields",["docs_after_excerpt"],"safe_fields"),("confirmation_accessed",True,"confirmation_accessed")])
def test_binary_manifest_corruption_rejected(tmp_path: Path,field: str,value,match: str) -> None:
    root,manifest_path=_sandbox_task(tmp_path,"binary"); manifest=json.loads(manifest_path.read_text()); manifest[field]=value; manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(RuntimeError,match=match): verify_classifier_manifest(root,manifest_path,"binary")


def test_category_class_contract_corruption_rejected(tmp_path: Path) -> None:
    root,manifest_path=_sandbox_task(tmp_path,"category"); manifest=json.loads(manifest_path.read_text()); manifest["classes"]=["api_reference"]; manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(RuntimeError,match="class contract"): verify_classifier_manifest(root,manifest_path,"category")


def test_gate2_winner_mismatch_rejected() -> None:
    with pytest.raises(RuntimeError,match="winner mismatch"): assert_gate2_winners({"binary":{"selected_family":"M2"},"category":{"selected_family":"M1"}})


def test_selection_evidence_lf_checkout_matches_historical_crlf_freeze(
    tmp_path: Path,
) -> None:
    root, manifest_path = _sandbox_task(
        tmp_path,
        "binary",
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    evidence = (
        root
        / manifest[
            "selection_evidence_path"
        ]
    )

    # Force the canonical Linux/Git LF representation.
    evidence.write_bytes(
        evidence.read_bytes().replace(
            b"\r\n",
            b"\n",
        )
    )

    result = verify_classifier_manifest(
        root,
        manifest_path,
        "binary",
    )

    assert (
        result[
            "selection_evidence_verification"
        ][
            "mode"
        ]
        ==
        "canonical_git_lf_with_verified_crlf_equivalence"
    )


def test_child_manifest_link_linux_lf_checkout_is_portable(
    tmp_path: Path,
) -> None:
    overall = json.loads(
        (
            ROOT
            / "reports/final_v2/gate3/"
              "GATE3_CLASSIFIER_FREEZE_MANIFEST.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    correction_source = (
        ROOT
        / "reports/final_v2/gate3/"
          "GATE3_CHILD_MANIFEST_LINK_EOL_PORTABILITY_CORRECTION.json"
    )

    correction_target = (
        tmp_path
        / correction_source.relative_to(
            ROOT
        )
    )

    correction_target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        correction_source,
        correction_target,
    )

    for task in (
        "binary",
        "category",
    ):
        linked = overall[
            task
        ]

        source = (
            ROOT
            / linked[
                "path"
            ]
        )

        target = (
            tmp_path
            / linked[
                "path"
            ]
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_bytes(
            source.read_bytes().replace(
                b"\r\n",
                b"\n",
            )
        )

        result = (
            verify_child_manifest_link_hash(
                tmp_path,
                task,
                linked,
                target,
            )
        )

        assert (
            result[
                "status"
            ]
            == "PASS"
        )

        assert (
            result[
                "mode"
            ]
            ==
            "canonical_git_lf_with_verified_mixed_eol_equivalence"
        )
