from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, category_eligible_rows
from docguard_ml_v2.gate2_closure import EXPECTED, load_development_without_confirmation, load_fold_map, sha256_file, write_json
from docguard_ml_v2.gate3_freeze import GATE2_COMMIT, SERIALIZER, environment_metadata, fit_and_check, model_payload, select_full_development


def _manifest(task: str, model_path: Path, evidence_path: Path, rows: list[dict], selection: dict, reproducibility: dict, config: dict, source_commit: str) -> dict:
    clf = joblib.load(model_path)["model"].named_steps["classifier"]
    vectorizer = joblib.load(model_path)["model"].named_steps["tfidf"]
    return {
        "schema_version": "gate3_classifier_freeze_manifest_v1", "status": "FROZEN", "task": task,
        "selected_family": "M1", "selected_family_name": config["families"]["M1"]["name"],
        "gate1_gold_sha256": EXPECTED["gold_sha256"], "gate2_closure_commit": GATE2_COMMIT,
        "gate2_return_archive_sha256": EXPECTED["return_archive_sha256"],
        "gate2_final_summary_sha256": sha256_file(PROJECT_ROOT/"reports/final_v2/gate2/final_results/gate2_final_summary.json"),
        "gate2_winner_decision_path": "reports/final_v2/gate2/final_results/winner_decision.json",
        "gate2_winner_decision_sha256": sha256_file(PROJECT_ROOT/"reports/final_v2/gate2/final_results/winner_decision.json"),
        "source_commit": source_commit, "scientific_config_sha256": EXPECTED["config_sha256"],
        "model_artifact_path": str(model_path.relative_to(PROJECT_ROOT)).replace("\\","/"), "model_sha256": sha256_file(model_path),
        "training_data": {"development_view_sha256": EXPECTED["development_view_sha256"], "eligible_rows": len(rows), "partitions": ["development_train","development_validation"], "confirmation_excluded_rows": 3747},
        "safe_fields": list(SAFE_MODEL_FIELDS), "serializer": SERIALIZER,
        "vectorizer": {"class": "sklearn.feature_extraction.text.TfidfVectorizer", "analyzer": vectorizer.analyzer, "ngram_range": list(vectorizer.ngram_range), "min_df": vectorizer.min_df, "max_features": vectorizer.max_features, "sublinear_tf": vectorizer.sublinear_tf, "vocabulary_size": len(vectorizer.vocabulary_)},
        "classifier": {"class": "sklearn.linear_model.LogisticRegression", "C": clf.C, "class_weight": clf.class_weight, "max_iter": clf.max_iter, "random_state": clf.random_state, "solver": clf.solver},
        "classes": [value.item() if hasattr(value,"item") else value for value in clf.classes_], "seed": config["seed"],
        "selection_evidence_path": str(evidence_path.relative_to(PROJECT_ROOT)).replace("\\","/"), "selection_evidence_sha256": sha256_file(evidence_path),
        "final_threshold": selection["selected"].get("selected_threshold") if task=="binary" else None,
        "threshold_selection_rule": config["tasks"]["binary"]["threshold_tie_break"] if task=="binary" else None,
        "class_counts": dict(sorted(__import__('collections').Counter(str(row["gold_doc_category"]) for row in rows).items())) if task=="category" else None,
        "dependencies": environment_metadata(), "reproducibility": reproducibility,
        "training_timestamp_utc": datetime.now(timezone.utc).isoformat(), "confirmation_accessed": False,
    }


def run(output: Path, model_dir: Path) -> dict:
    subprocess.run([sys.executable, str(PROJECT_ROOT/"scripts/verify_gate2_closure.py")], cwd=PROJECT_ROOT, check=True)
    state=json.loads((PROJECT_ROOT/"reports/final_v2/finalization_state.json").read_text()); winners=json.loads((PROJECT_ROOT/"reports/final_v2/gate2/final_results/winner_decision.json").read_text())
    if state["gate_0_status"]!="PASS" or state["gate_1_status"]!="PASS" or state["gate_statuses"]["gate_2_development_only_ml_model_study"]!="PASS" or state["confirmation_sealed"] is not True: raise RuntimeError("Upstream gates are not sealed PASS")
    if winners["binary"]["selected_family"]!="M1" or winners["category"]["selected_family"]!="M1": raise RuntimeError("Gate 2 winner mismatch")
    config_path=PROJECT_ROOT/"configs/final_v2/gate2_model_study.json"; config=json.loads(config_path.read_text())
    if sha256_file(config_path)!=EXPECTED["config_sha256"]: raise RuntimeError("Scientific config mismatch")
    rows,view=load_development_without_confirmation(PROJECT_ROOT); tasks={"binary":rows,"category":category_eligible_rows(rows,allowed_partitions={"development_train","development_validation"})}
    if len(tasks["binary"])!=22166 or len(tasks["category"])!=4820: raise RuntimeError("Gate 3 training row count mismatch")
    output.mkdir(parents=True,exist_ok=True); model_dir.mkdir(parents=True,exist_ok=True); source_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=PROJECT_ROOT,text=True).strip()
    manifests={}; selections={}; reproducibility={}
    for task in ("binary","category"):
        fold_path=PROJECT_ROOT/f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv"; fold_map=load_fold_map(fold_path,task)
        selection=select_full_development(task=task,rows=tasks[task],fold_map=fold_map,config=config)
        evidence_path=output/f"{task}_full_development_selection_evidence.json"; write_json(evidence_path,selection)
        model,audit=fit_and_check(task,tasks[task],selection,config); model_path=model_dir/f"{task}_m1_gate3.joblib"; joblib.dump(model_payload(task,model,selection),model_path,compress=3)
        manifest=_manifest(task,model_path,evidence_path,tasks[task],selection,audit,config,source_commit); manifest_path=output/f"{task}_classifier_freeze_manifest.json"; write_json(manifest_path,manifest)
        manifests[task]={"path":str(manifest_path.relative_to(PROJECT_ROOT)).replace("\\","/"),"sha256":sha256_file(manifest_path),"model_path":str(model_path.relative_to(PROJECT_ROOT)).replace("\\","/"),"model_sha256":sha256_file(model_path)}; selections[task]=selection; reproducibility[task]=audit
    overall={"schema_version":"gate3_classifier_freeze_v1","status":"PASS","gate":3,"upstream":{"gate0":"PASS","gate1":"PASS","gate2":"PASS","gate2_closure_commit":GATE2_COMMIT,"gold_sha256":EXPECTED["gold_sha256"],"gate2_return_archive_sha256":EXPECTED["return_archive_sha256"],"scientific_config_sha256":EXPECTED["config_sha256"]},"selected_families":{"binary":"M1","category":"M1"},"binary":manifests["binary"],"category":manifests["category"],"reproducibility":reproducibility,"confirmation_accessed":False,"confirmation_sealed":True,"gate4_status":"NOT_EXECUTED"}
    overall_path=output/"GATE3_CLASSIFIER_FREEZE_MANIFEST.json"; write_json(overall_path,overall)
    binary= json.loads((output/"binary_classifier_freeze_manifest.json").read_text()); category=json.loads((output/"category_classifier_freeze_manifest.json").read_text())
    report=f'''# Gate 3 Final Classifier Freeze\n\n**Status: PASS.** Gate 3 used development data only. Confirmation remained sealed; Gate 4 and Gate 5 were not executed.\n\n## Upstream evidence\n\n- Gate 0, Gate 1 and Gate 2: PASS\n- Gate 2 closure commit: `{GATE2_COMMIT}`\n- Frozen gold SHA-256: `{EXPECTED["gold_sha256"]}`\n- Gate 2 return SHA-256: `{EXPECTED["return_archive_sha256"]}`\n\n## Freeze-time selection procedure\n\nGate 2 selected M1 for both tasks. To obtain one final configuration without averaging fold-specific choices, Gate 3 generated repository-grouped OOF predictions over the immutable five Gate 2 folds for every candidate in the already-registered M1 grid. The registered metric and tie-break selected the final configuration. This is freeze-time tuning evidence, not a new evaluation estimate; Gate 2 nested CV remains the development evaluation.\n\n- Binary: C=`{binary["classifier"]["C"]}`, class_weight=`{binary["classifier"]["class_weight"]}`, threshold=`{binary["final_threshold"]}`, rows={binary["training_data"]["eligible_rows"]}.\n- Category: C=`{category["classifier"]["C"]}`, class_weight=`{category["classifier"]["class_weight"]}`, rows={category["training_data"]["eligible_rows"]}.\n- Category classes: {', '.join(PRIMARY_STAGE2_LABELS)}.\n\n## Artifacts\n\n- Binary model: `{binary["model_artifact_path"]}` (`{binary["model_sha256"]}`)\n- Category model: `{category["model_artifact_path"]}` (`{category["model_sha256"]}`)\n- Binary selection evidence: `{binary["selection_evidence_path"]}`\n- Category selection evidence: `{category["selection_evidence_path"]}`\n\n## Reproducibility and interpretation\n\nBoth pipelines passed a second deterministic rebuild: exact predictions and vocabulary, and probabilities/coefficients equal within `1e-12`. Joblib byte identity is not required because serialization metadata can vary.\n\nThe Gate 2 generalization limitation remains unchanged: aggregate scores are materially influenced by controlled augmentation; natural-only and Natural Diversity slices are substantially weaker. This finding did not reopen model selection.\n\nNo training-set score is reported as final evaluation. Gate 2 development CV remains the only current evaluation evidence.\n\n## Boundary\n\nConfirmation accessed: **NO**. Gate 4: **NOT_EXECUTED**. Gate 5: **NOT_EXECUTED**.\n'''
    (output/"GATE3_CLASSIFIER_FREEZE_REPORT.md").write_text(report,encoding="utf-8")
    return overall


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--output',default='reports/final_v2/gate3'); p.add_argument('--model-dir',default='models/final_v2/gate3'); a=p.parse_args(); result=run(PROJECT_ROOT/a.output,PROJECT_ROOT/a.model_dir); print(json.dumps({"status":result["status"],"confirmation_accessed":False,"gate4_status":"NOT_EXECUTED"},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
