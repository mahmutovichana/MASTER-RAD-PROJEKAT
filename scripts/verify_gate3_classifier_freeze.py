from __future__ import annotations

import argparse
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
    if sha256_file(evidence_path) != manifest.get("selection_evidence_sha256"):
        raise RuntimeError(f"{task} selection evidence hash mismatch")
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
    return {"task": task, "model_sha256": expected["sha256"], "selection_evidence_sha256": manifest["selection_evidence_sha256"], "status": "PASS"}


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
    binary=verify_classifier_manifest(root,root/"reports/final_v2/gate3/binary_classifier_freeze_manifest.json","binary"); category=verify_classifier_manifest(root,root/"reports/final_v2/gate3/category_classifier_freeze_manifest.json","category")
    overall_path=root/"reports/final_v2/gate3/GATE3_CLASSIFIER_FREEZE_MANIFEST.json"; overall=json.loads(overall_path.read_text())
    if overall.get("status")!="PASS" or overall.get("confirmation_accessed") is not False or overall.get("confirmation_sealed") is not True or overall.get("gate4_status")!="NOT_EXECUTED" or overall.get("selected_families")!={"binary":"M1","category":"M1"}: raise RuntimeError("Overall Gate 3 manifest mismatch")
    for task,item in (("binary",binary),("category",category)):
        linked=overall[task]; manifest_path=root/linked["path"]
        if linked["sha256"]!=sha256_file(manifest_path) or linked["model_sha256"]!=item["model_sha256"]: raise RuntimeError(f"Overall {task} manifest link mismatch")
    state=json.loads((root/"reports/final_v2/finalization_state.json").read_text())
    if state["gate_statuses"]["gate_3_final_classifier_selection_and_freeze"]!="PASS" or state["gate_statuses"]["gate_4_stage3_retrieval_generation_study_and_freeze"]!="NOT_EXECUTED" or state["current_gate"]!=4 or state.get("confirmation_results_accessed_by_gate_3") is not False or state["confirmation_sealed"] is not True: raise RuntimeError("Gate 3 finalization state mismatch")
    sample=rows[0]; forbidden={**sample,"docs_after_excerpt":"MUTATION","pr_title":"MUTATION","label_source":"MUTATION"}
    for task in ("binary","category"):
        payload=joblib.load(root/f"models/final_v2/gate3/{task}_m1_gate3.joblib"); model=payload["model"]
        a=model.predict_proba([sample]); b=model.predict_proba([forbidden])
        if not np.array_equal(a,b): raise RuntimeError(f"Forbidden fields altered {task} inference")
        empty={field:"" for field in SAFE_MODEL_FIELDS}; first=model.predict_proba([empty]); second=model.predict_proba([empty])
        if not np.array_equal(first,second): raise RuntimeError(f"Empty-field {task} inference is nondeterministic")
    return {"status":"PASS","gate":3,"binary":binary,"category":category,"development_rows":22166,"category_rows":4820,"confirmation_accessed":False,"confirmation_sealed":True,"gate4_status":"NOT_EXECUTED"}


def main()->int:
    argparse.ArgumentParser().parse_args(); print(json.dumps(verify(),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
