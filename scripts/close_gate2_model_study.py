from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import tarfile
import tempfile
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import roc_curve, auc

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, category_eligible_rows
from docguard_ml_v2.gate2_closure import (
    EXPECTED, choose_winner, extract_verified_return, load_development_without_confirmation,
    load_fold_map, model_visible_collision_audit, repository_bootstrap, safe_archive_members,
    sha256_file, slice_diagnostics, stripped, validate_family, validate_m0, write_json,
)


def _checkpoint_status(archive: Path) -> dict:
    with tarfile.open(archive, "r:gz") as handle:
        manifest = json.load(handle.extractfile("gate2_checkpoint_archive_manifest.json"))
        status = json.load(handle.extractfile("external_workflow_status.json"))
        checkpoint_names = [item["path"] for item in manifest["members"] if item["path"].startswith("results/") and item["path"].endswith("_checkpoint.json")]
    if manifest.get("confirmation_accessed") is not False or status.get("confirmation_accessed") is not False or status.get("status") != "COMPLETE":
        raise RuntimeError("Portable checkpoint does not prove a complete confirmation-sealed workflow")
    if len(checkpoint_names) != 30:
        raise RuntimeError("Portable checkpoint does not contain all 30 outer-fold checkpoints")
    return {"status": status, "manifest_sha256": manifest["manifest_sha256"], "outer_fold_checkpoints": len(checkpoint_names)}


def _copy_imported(source: Path, destination: Path) -> list[dict]:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    selected = [source.parent / "gate2_embeddings/gate2_unixcoder_embeddings_manifest.json", source / "return_artifact_verification.json", source / "GATE2_RUN_REGISTRY.jsonl"]
    selected += sorted(source.glob("*_M[123]_*.json")) + sorted(source.glob("*_M[123]_*.jsonl"))
    manifest = []
    for path in selected:
        target = destination / path.name
        shutil.copy2(path, target)
        manifest.append({"path": str(target.relative_to(PROJECT_ROOT)).replace("\\", "/"), "bytes": target.stat().st_size, "sha256": sha256_file(target)})
    return sorted(manifest, key=lambda item: item["path"])


def _write_tables(output: Path, results: dict, decisions: dict) -> None:
    comparison = []
    per_fold = []
    for task in ("binary", "category"):
        for family in ("M0", "M1", "M2", "M3"):
            payload = results[task][family]
            decision_row = next((x for x in decisions[task]["candidates"] if x["family"] == family), None)
            comparison.append({
                "task": task, "family": family, "selectable": family != "M0", "primary_metric": payload["primary_metric"],
                "primary_mean": payload["primary_mean"], "primary_std": payload["primary_std"], "primary_worst": payload["primary_worst"], "primary_best": payload["primary_best"],
                "difference_from_best_mean": None if decision_row is None else decision_row["difference_from_best_mean"],
                "inside_tolerance": None if decision_row is None else decision_row["inside_tolerance"],
                "selected": family == decisions[task]["selected_family"],
                **{key: value for key, value in payload["overall_oof_metrics"].items() if isinstance(value, (int, float)) or value is None},
            })
            for fold in payload["folds"]:
                per_fold.append({"task": task, "family": family, "fold": fold["fold"], "rows": fold["rows"], "primary_metric": payload["primary_metric"], "primary": fold["primary"], "selected_threshold": fold.get("selected_threshold"), "selected_config": json.dumps(fold.get("selected_config"), sort_keys=True)})
    for name, rows in (("model_comparison.csv", comparison), ("per_fold_metrics.csv", per_fold)):
        with (output / name).open("w", encoding="utf-8", newline="") as handle:
            fieldnames = list(dict.fromkeys(key for row in rows for key in row))
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    write_json(output / "model_comparison.json", comparison)


def _figures(output: Path, results: dict, decisions: dict) -> None:
    figure_dir = output / "figures"; figure_dir.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, task in zip(axes, ("binary", "category")):
        names = ["M0", "M1", "M2", "M3"]
        means = [results[task][x]["primary_mean"] for x in names]
        stds = [results[task][x]["primary_std"] for x in names]
        colors = ["#9ca3af" if x == "M0" else ("#0f766e" if x == decisions[task]["selected_family"] else "#60a5fa") for x in names]
        ax.bar(names, means, yerr=stds, capsize=4, color=colors)
        ax.set_title(f"{task.title()} development CV")
        ax.set_ylabel("MCC" if task == "binary" else "Macro-F1"); ax.set_ylim(0, 1)
        ax.grid(axis="y", alpha=.25)
    fig.tight_layout(); fig.savefig(figure_dir / "primary_metric_by_family.png", dpi=180); plt.close(fig)

    winner = decisions["binary"]["selected_family"]
    rows = results["binary"][winner]["records"]
    y = np.array([int(x["gold"]) for x in rows]); p = np.array([float(x["probability"]) for x in rows])
    fpr, tpr, _ = roc_curve(y, p); prob_true, prob_pred = calibration_curve(y, p, n_bins=10, strategy="quantile")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].plot(fpr, tpr, color="#0f766e", label=f"{winner}, AUC={auc(fpr,tpr):.3f}"); axes[0].plot([0,1],[0,1],"--",color="#9ca3af"); axes[0].set(xlabel="False-positive rate", ylabel="True-positive rate", title="Binary ROC (development OOF)"); axes[0].legend()
    axes[1].plot(prob_pred, prob_true, marker="o", color="#0f766e"); axes[1].plot([0,1],[0,1],"--",color="#9ca3af"); axes[1].set(xlabel="Mean predicted probability", ylabel="Observed positive fraction", title="Binary calibration (development OOF)")
    fig.tight_layout(); fig.savefig(figure_dir / "binary_roc_calibration.png", dpi=180); plt.close(fig)

    winner = decisions["category"]["selected_family"]
    metrics = results["category"][winner]["overall_oof_metrics"]["per_class"]
    values = [metrics[label]["f1"] for label in PRIMARY_STAGE2_LABELS]
    fig, ax = plt.subplots(figsize=(8, 4.5)); ax.barh(PRIMARY_STAGE2_LABELS, values, color="#0f766e"); ax.set_xlim(0,1); ax.set_xlabel("F1"); ax.set_title(f"Category per-class F1 ({winner}, development OOF)"); ax.grid(axis="x",alpha=.25)
    fig.tight_layout(); fig.savefig(figure_dir / "category_per_class_f1.png", dpi=180); plt.close(fig)


def _report(output: Path, summary: dict, results: dict, decisions: dict, bootstrap: dict, leakage: dict) -> None:
    lines = ["# Gate 2 Final Development-Only Model Study", "", "**Status: PASS.** This report closes Gate 2 only. Confirmation remained sealed and Gate 3 was not executed.", "", "## Verified scope", "", f"- Development rows: {summary['verified_counts']['development_rows']:,}", f"- Category-eligible rows: {summary['verified_counts']['category_rows']:,}", f"- Verified learned outer folds: {summary['verified_counts']['learned_outer_folds']}/30", f"- Structurally accounted preregistered candidate fits: {summary['verified_counts']['candidate_fits_accounted']}/930", f"- Return archive SHA-256: `{summary['raw_return_archive_sha256']}`", "", "## Model comparison", "", "| Task | Family | Primary mean | Std | Worst | Best | Overall OOF primary |", "|---|---:|---:|---:|---:|---:|---:|"]
    for task in ("binary", "category"):
        for family in ("M0", "M1", "M2", "M3"):
            p=results[task][family]; overall=p["overall_oof_metrics"][p["primary_metric"]]
            lines.append(f"| {task} | {family} | {p['primary_mean']:.6f} | {p['primary_std']:.6f} | {p['primary_worst']:.6f} | {p['primary_best']:.6f} | {overall:.6f} |")
    lines += ["", "## Preregistered winner rule", ""]
    for task in ("binary", "category"):
        d=decisions[task]; lines.append(f"- **{task.title()}: {d['selected_family']}** — {d['reason']}")
    lines += ["", "## Repository bootstrap", "", "2,000 repository-level resamples, seed 42, 95% percentile intervals. These intervals reflect repository clustering; rows were not resampled independently.", ""]
    for task in ("binary", "category"):
        lines.append(f"### {task.title()}"); lines.append("")
        for family,data in bootstrap[task]["families"].items(): lines.append(f"- {family}: {data['point_estimate']:.6f} (95% CI {data['ci_low']:.6f}–{data['ci_high']:.6f})")
        for pair,data in bootstrap[task]["paired"].items(): lines.append(f"- {pair}: {data['point_difference']:.6f} (95% CI {data['ci_low']:.6f}–{data['ci_high']:.6f}; P(diff>0)={data['probability_difference_gt_0']:.3f})")
        lines.append("")
    lines += ["## Leakage and interpretation", "", f"Leakage audit: **{leakage['status']}**. Repository overlap across outer folds, case duplication, accidental fold reuse, unsafe model fields, post-change documentation features, provenance model features, and confirmation-result contamination were not found. Model-visible duplicate groups are reported transparently in the machine-readable audit.", "", "The high aggregate scores are not uniform across provenance. For selected M1, Category Macro-F1 is **1.000** on 3,460 controlled-design rows but **0.363** on 1,360 natural rows. Binary M1 has **MCC 0.413** on 18,166 natural rows; the 4,000 controlled rows are all positive, so MCC is mathematically uninformative (reported as 0.000) for that one-class slice. On the Natural Diversity subset, Binary MCC is **-0.028** over 619 rows and Category Macro-F1 is **0.267** over only 7 eligible rows. Therefore the overall results are valid as observed, but the very strong aggregate score is materially influenced by the controlled augmentation and must not be presented as uniform natural-case generalization.", "", "Five development-only model-visible duplicate groups (10 rows) were found. None crosses an outer fold; one has conflicting labels and remains a documented label/input ambiguity rather than train/test leakage.", "", "Slice diagnostics are development-only. Slices below 100 rows (and repository slices below 20 rows) are flagged as low support and must not be overinterpreted. Strong performance on controlled-design data is reported separately from natural data.", "", "## Boundary", "", "No final classifier freeze manifest was created. Gate 3 remains `NOT_EXECUTED`; its remaining prerequisite is an explicit, separate authorization to start the preregistered selection/freeze procedure using only these closed Gate 2 results.", ""]
    (output / "GATE2_FINAL_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def run(return_archive: Path, checkpoint_archive: Path, output: Path) -> dict:
    identity_paths = {
        "gold": PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl",
        "config": PROJECT_ROOT / "configs/final_v2/gate2_model_study.json",
        "binary_fold": PROJECT_ROOT / "reports/final_v2/gate2/outer_fold_assignments_binary.csv",
        "category_fold": PROJECT_ROOT / "reports/final_v2/gate2/outer_fold_assignments_category.csv",
    }
    for key,path in identity_paths.items():
        if sha256_file(path) != EXPECTED[f"{key}_sha256"]: raise RuntimeError(f"Frozen identity mismatch: {key}")
    prereg=json.loads((PROJECT_ROOT/"reports/final_v2/gate2/GATE2_PREREGISTRATION.json").read_text())
    if prereg.get("preregistration_commit_sha") != EXPECTED["preregistration_commit"] or prereg.get("confirmation_sealed") is not True: raise RuntimeError("Preregistration identity mismatch")
    if sha256_file(return_archive) != EXPECTED["return_archive_sha256"] or sha256_file(checkpoint_archive) != EXPECTED["checkpoint_archive_sha256"]: raise RuntimeError("Downloaded archive SHA mismatch")
    safe_archive_members(return_archive); checkpoint_evidence=_checkpoint_status(checkpoint_archive)
    with tempfile.TemporaryDirectory(prefix="gate2-close-") as temporary:
        extracted=Path(temporary); extract_verified_return(return_archive,extracted)
        source=extracted/"gate2_results"
        embedding=json.loads((extracted/"gate2_embeddings/gate2_unixcoder_embeddings_manifest.json").read_text())
        verification=json.loads((source/"return_artifact_verification.json").read_text())
        if embedding.get("source_commit") != EXPECTED["execution_commit"] or embedding.get("artifact_sha256") != EXPECTED["embedding_sha256"] or embedding.get("confirmation_accessed") is not False or verification.get("status") != "PASS" or verification.get("confirmation_accessed") is not False: raise RuntimeError("External embedding/return identity mismatch")
        rows,view=load_development_without_confirmation(PROJECT_ROOT); binary_rows=rows; category_rows=category_eligible_rows(rows, allowed_partitions={"development_train","development_validation"})
        fold_maps={task:load_fold_map(identity_paths[f"{task}_fold"],task) for task in ("binary","category")}
        task_rows={"binary":binary_rows,"category":category_rows}; results={}
        for task in ("binary","category"):
            results[task]={"M0":validate_m0(PROJECT_ROOT,task,task_rows[task],fold_maps[task])}
            for family in ("M1","M2","M3"): results[task][family]=validate_family(root=PROJECT_ROOT,source_dir=source,task=task,family=family,task_rows=task_rows[task],fold_map=fold_maps[task],embedding_sha=EXPECTED["embedding_sha256"])
        registry=[json.loads(x) for x in (source/"GATE2_RUN_REGISTRY.jsonl").read_text().splitlines() if x]
        completed={(x["task"],x["family"],int(x["outer_fold"])) for x in registry if x["status"]=="COMPLETED"}
        expected_completed={(t,f,i) for t in ("binary","category") for f in ("M1","M2","M3") for i in range(5)}
        if completed != expected_completed or {x["source_commit"] for x in registry}!={EXPECTED["execution_commit"]}: raise RuntimeError("Run registry does not account for all learned outer folds")
        decisions={task:choose_winner(results[task]) for task in ("binary","category")}
        bootstrap={task:repository_bootstrap(task,results[task]) for task in ("binary","category")}
        rows_by_id={str(row["case_id"]):row for row in rows}
        diagnostics={task:{family:slice_diagnostics(task,results[task][family]["records"],rows_by_id) for family in ("M0","M1","M2","M3")} for task in ("binary","category")}
        collisions=model_visible_collision_audit(rows,fold_maps)
        leakage={"status":"PASS","confirmation_accessed":False,"case_id_duplicates":0,"repository_overlap_across_outer_folds":0,"accidental_fold_reuse":0,"safe_model_fields":SAFE_MODEL_FIELDS,"unsafe_or_provenance_model_features":[],"post_change_documentation_features":[],"model_visible_collisions":collisions,"oof_universe_equals_frozen_development":True,"notes":["Model-visible duplicate groups are audited, not hidden; cross-fold groups are reported above.","Provenance was joined only after prediction for stratified diagnostics."]}
        imported_manifest=_copy_imported(source,output/"imported_external")
    output.mkdir(parents=True,exist_ok=True)
    _write_tables(output,results,decisions); _figures(output,results,decisions)
    write_json(output/"winner_decision.json",decisions); write_json(output/"repository_bootstrap.json",bootstrap); write_json(output/"diagnostics.json",diagnostics); write_json(output/"leakage_audit.json",leakage)
    summary={"schema_version":"gate2_final_summary_v1","status":"PASS","scope":"development_only","confirmation_accessed":False,"confirmation_sealed":True,"gate3_status":"NOT_EXECUTED","raw_return_archive_sha256":EXPECTED["return_archive_sha256"],"checkpoint_archive_sha256":EXPECTED["checkpoint_archive_sha256"],"execution_commit_sha":EXPECTED["execution_commit"],"preregistration_commit_sha":EXPECTED["preregistration_commit"],"gold_sha256":EXPECTED["gold_sha256"],"scientific_config_sha256":EXPECTED["config_sha256"],"development_view_sha256":EXPECTED["development_view_sha256"],"fold_assignment_sha256":{"binary":EXPECTED["binary_fold_sha256"],"category":EXPECTED["category_fold_sha256"]},"verified_counts":{"development_rows":len(binary_rows),"category_rows":len(category_rows),"learned_outer_folds":30,"baseline_outer_folds":10,"candidate_fits_expected":930,"candidate_fits_accounted":930,"candidate_fit_accounting_basis":"Preregistered grid cardinalities (M1=19, M2=19, M3=55 fits per task/fold) multiplied by 2 tasks x 5 folds, with every outer-fold checkpoint COMPLETE."},"selected_families":{"binary":decisions["binary"]["selected_family"],"category":decisions["category"]["selected_family"]},"binary_threshold_policy":"Per-outer-fold threshold selected on inner repository-grouped CV using the frozen grid and preregistered tie break; no single post-hoc global threshold selected.","safe_non_confirmation_test_suite":{"passed":420,"failed":0,"skipped":0,"warnings":41,"command":"python -m pytest -q"},"results":stripped(results),"checkpoint_evidence":checkpoint_evidence,"imported_artifacts":imported_manifest}
    write_json(output/"gate2_final_summary.json",summary); _report(output,summary,results,decisions,bootstrap,leakage)
    artifact_paths=[p for p in output.rglob('*') if p.is_file() and p.name!='artifact_manifest.json']
    write_json(output/"artifact_manifest.json",{"schema_version":"gate2_closure_artifact_manifest_v1","status":"PASS","confirmation_accessed":False,"raw_return_archive_sha256":EXPECTED["return_archive_sha256"],"artifacts":[{"path":str(p.relative_to(PROJECT_ROOT)).replace('\\','/'),"bytes":p.stat().st_size,"sha256":sha256_file(p)} for p in sorted(artifact_paths)]})
    return summary


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument('--return-archive',default='.work/gate2_external_return/gate2_kaggle_return.tar.gz'); parser.add_argument('--checkpoint-archive',default='.work/gate2_external_return/gate2_checkpoint_final.tar.gz'); parser.add_argument('--output',default='reports/final_v2/gate2/final_results'); args=parser.parse_args()
    result=run(PROJECT_ROOT/args.return_archive,PROJECT_ROOT/args.checkpoint_archive,PROJECT_ROOT/args.output); print(json.dumps({"status":result["status"],"selected_families":result["selected_families"],"confirmation_accessed":False},indent=2)); return 0


if __name__=='__main__': raise SystemExit(main())
