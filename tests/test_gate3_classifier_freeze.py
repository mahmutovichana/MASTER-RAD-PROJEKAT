from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts.verify_gate3_classifier_freeze import assert_gate2_winners, verify, verify_classifier_manifest


ROOT = Path(__file__).resolve().parents[1]


def _sandbox_task(tmp_path: Path, task: str) -> tuple[Path, Path]:
    manifest_source=ROOT/f"reports/final_v2/gate3/{task}_classifier_freeze_manifest.json"
    manifest=json.loads(manifest_source.read_text())
    for relative in (manifest["model_artifact_path"],manifest["selection_evidence_path"],manifest["training_provenance_path"]):
        target=tmp_path/relative; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/relative,target)
    target_manifest=tmp_path/manifest_source.relative_to(ROOT); target_manifest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(manifest_source,target_manifest)
    return tmp_path,target_manifest


def test_gate3_freeze_verifier_passes() -> None:
    result=verify(); assert result["status"]=="PASS"; assert result["confirmation_accessed"] is False; assert result["gate4_status"]=="NOT_EXECUTED"


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
