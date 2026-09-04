from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import tarfile
import tempfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

from docguard_ml_v2.data_contract import (
    PRIMARY_STAGE2_LABELS,
    SAFE_MODEL_FIELDS,
    category_eligible_rows,
    load_jsonl,
    serialize_model_row,
    validate_final_gold_row,
)
from docguard_ml_v2.gate2_study import (
    development_view_hash,
    load_fold_checkpoint,
    sha256_file,
)
from docguard_ml_v2.metrics import binary_metrics, category_metrics


EXPECTED = {
    "gold_sha256": "68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08",
    "config_sha256": "412f23974cac3fd6e2876da6858907f1fbbc5096c9f80f479e45715376976ee5",
    "development_view_sha256": "f01255edd74aa5153747c5468daf64b49b771f3b0ff38df72c0b054ea33d04b4",
    "binary_fold_sha256": "10b3b72dda396d8be9754709c26e3eae0d4821e5e45041c9adc741d8980f3042",
    "category_fold_sha256": "2692276dbafbcc1d8c4b50a1e8e6ae7d136fdeace404283ba6fbb1b7d5a6d292",
    "execution_commit": "ee7992192f685a390486079afe54570226dba05d",
    "preregistration_commit": "e89cedfa87edbc1469d467713451a9441aa1360f",
    "return_archive_sha256": "0b5840e1ce600f0df44f935f9c2ec9ce4608694e0dc0e73eb0f9a2e75b63abfd",
    "checkpoint_archive_sha256": "1528262a86aa175b20cc118699ae4c6e268c14aca0e1e38a15eb3b93900d9088",
    "embedding_sha256": "ca75376fb304f37c45c6a733450352d2eb6ca9f6117b56dd58d368016b70d1eb",
}


def canonical_json_sha(payload: Any) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def safe_archive_members(archive: Path) -> list[tarfile.TarInfo]:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
    if not members:
        raise RuntimeError("Gate 2 return archive is empty")
    seen: set[str] = set()
    for member in members:
        path = PurePosixPath(member.name)
        if member.name in seen or path.is_absolute() or ".." in path.parts:
            raise RuntimeError(f"Unsafe or duplicate archive member: {member.name}")
        if not member.isfile():
            raise RuntimeError(f"Only regular files are allowed in return archive: {member.name}")
        if "confirmation" in member.name.lower():
            raise RuntimeError(f"Prohibited confirmation artifact: {member.name}")
        seen.add(member.name)
    expected = {
        "gate2_embeddings/gate2_unixcoder_embeddings_manifest.json",
        "gate2_results/return_artifact_verification.json",
        "gate2_results/GATE2_RUN_REGISTRY.jsonl",
    }
    for task in ("binary", "category"):
        for family in ("M1", "M2", "M3"):
            expected.update({
                f"gate2_results/{task}_{family}_summary.json",
                f"gate2_results/{task}_{family}_oof.jsonl",
                *(f"gate2_results/{task}_{family}_fold{fold}.json" for fold in range(5)),
                *(f"gate2_results/{task}_{family}_fold{fold}_checkpoint.json" for fold in range(5)),
            })
    if seen != expected:
        raise RuntimeError(f"Unexpected return archive structure; missing={sorted(expected-seen)}, extra={sorted(seen-expected)}")
    return members


def extract_verified_return(archive: Path, destination: Path) -> None:
    members = safe_archive_members(archive)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    with tarfile.open(archive, "r:gz") as handle:
        for member in members:
            target = destination.joinpath(*PurePosixPath(member.name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            source = handle.extractfile(member)
            if source is None:
                raise RuntimeError(f"Could not read archive member {member.name}")
            with target.open("wb") as output:
                shutil.copyfileobj(source, output)


def load_development_without_confirmation(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    gold_dir = root / "experiments/consolidated_enriched_training_v2/gold"
    # Intentionally load only development files. The sealed confirmation file is never opened.
    rows = load_jsonl(gold_dir / "train.jsonl") + load_jsonl(gold_dir / "validation.jsonl")
    for row in rows:
        validate_final_gold_row(row, allowed_partitions={"development_train", "development_validation"})
    if len(rows) != 22166 or development_view_hash(rows) != EXPECTED["development_view_sha256"]:
        raise RuntimeError("Development-only universe identity mismatch")
    if len({str(row["case_id"]) for row in rows}) != len(rows):
        raise RuntimeError("Duplicate case IDs in frozen development universe")
    return rows, {
        "development_rows": len(rows),
        "confirmation_rows_excluded": 3747,
        "development_view_sha256": development_view_hash(rows),
        "confirmation_accessed": False,
    }


def load_fold_map(path: Path, task: str) -> dict[str, int]:
    result: dict[str, int] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["task"] != task:
                raise RuntimeError(f"Wrong task in {path}")
            repository = row["repository"].strip().lower()
            if repository in result:
                raise RuntimeError(f"Duplicate repository in {path}: {repository}")
            result[repository] = int(row["fold"])
    return result


def _assert_close(actual: Any, expected: Any, path: str = "root") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise RuntimeError(f"Metric structure mismatch at {path}")
        for key in expected:
            _assert_close(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise RuntimeError(f"Metric list mismatch at {path}")
        for index, value in enumerate(expected):
            _assert_close(actual[index], value, f"{path}[{index}]")
    elif isinstance(expected, float):
        if actual is None or not math.isclose(float(actual), expected, rel_tol=1e-11, abs_tol=1e-12):
            raise RuntimeError(f"Metric mismatch at {path}: {actual} != {expected}")
    elif actual != expected:
        raise RuntimeError(f"Value mismatch at {path}: {actual!r} != {expected!r}")


def recompute_metrics(task: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    gold = [row["gold"] for row in records]
    pred = [row["prediction"] for row in records]
    if task == "binary":
        scores = [float(row["probability"]) for row in records]
        result = binary_metrics([int(x) for x in gold], [int(x) for x in pred], scores)
        result["brier_score"] = float(brier_score_loss(gold, scores))
        result["macro_f1"] = float(category_metrics([str(x) for x in gold], [str(x) for x in pred], ["0", "1"])["macro_f1"])
        return result
    return category_metrics([str(x) for x in gold], [str(x) for x in pred], PRIMARY_STAGE2_LABELS)


def _load_oof(path: Path) -> list[dict[str, Any]]:
    rows = load_jsonl(path)
    if len({str(row["case_id"]) for row in rows}) != len(rows):
        raise RuntimeError(f"Duplicate OOF case ID in {path.name}")
    return rows


def validate_family(
    *, root: Path, source_dir: Path, task: str, family: str, task_rows: list[dict[str, Any]],
    fold_map: dict[str, int], embedding_sha: str,
) -> dict[str, Any]:
    prefix = f"{task}_{family}"
    summary_path = source_dir / f"{prefix}_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    oof_path = source_dir / f"{prefix}_oof.jsonl"
    if sha256_file(oof_path) != summary.get("oof_sha256"):
        raise RuntimeError(f"OOF SHA mismatch: {prefix}")
    records = _load_oof(oof_path)
    row_by_id = {str(row["case_id"]): row for row in task_rows}
    if set(row_by_id) != {str(row["case_id"]) for row in records} or len(records) != len(task_rows):
        raise RuntimeError(f"OOF membership mismatch: {prefix}")
    by_fold: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        case_id = str(record["case_id"])
        source = row_by_id[case_id]
        repository = str(source["repository"]).strip().lower()
        expected_gold: Any = int(bool(source["gold_docs_update_required"])) if task == "binary" else str(source["gold_doc_category"])
        if record["gold"] != expected_gold or str(record["repository"]).lower() != repository:
            raise RuntimeError(f"OOF gold/repository mismatch for {case_id}")
        if int(record["fold"]) != fold_map[repository]:
            raise RuntimeError(f"OOF fold mismatch for {case_id}")
        by_fold[int(record["fold"])].append(record)
    if set(by_fold) != set(range(5)):
        raise RuntimeError(f"Missing OOF fold: {prefix}")

    fold_primary: list[float] = []
    verified_folds: list[dict[str, Any]] = []
    for fold in range(5):
        fold_result_path = source_dir / f"{prefix}_fold{fold}.json"
        fold_result = json.loads(fold_result_path.read_text(encoding="utf-8"))
        checkpoint_path = source_dir / f"{prefix}_fold{fold}_checkpoint.json"
        expected_identity = {
            "task": task,
            "family": family,
            "outer_fold": fold,
            "gold_sha256": EXPECTED["gold_sha256"],
            "development_view_sha256": EXPECTED["development_view_sha256"],
            "scientific_config_sha256": EXPECTED["config_sha256"],
            "fold_assignment_sha256": EXPECTED[f"{task}_fold_sha256"],
        }
        if family in {"M2", "M3"}:
            expected_identity["embedding_artifact_sha256"] = embedding_sha
        checkpoint = load_fold_checkpoint(checkpoint_path, expected_identity=expected_identity)
        _assert_close(checkpoint["result"], fold_result, f"{prefix}.fold{fold}.checkpoint")
        _assert_close(summary["fold_results"][fold], fold_result, f"{prefix}.fold{fold}.summary")
        expected_ids = [str(row["case_id"]) for row in by_fold[fold]]
        if checkpoint["validation_case_ids"] != expected_ids:
            raise RuntimeError(f"Checkpoint case order mismatch: {prefix} fold {fold}")
        if checkpoint["validation_predictions"] != [row["prediction"] for row in by_fold[fold]]:
            raise RuntimeError(f"Checkpoint prediction mismatch: {prefix} fold {fold}")
        if task == "binary":
            _assert_close(checkpoint["validation_probabilities"], [row["probability"] for row in by_fold[fold]], f"{prefix}.probabilities")
        metrics = recompute_metrics(task, by_fold[fold])
        expected_metrics = fold_result["outer_metrics"]
        # The runner adds threshold to its binary metrics after calculation.
        if task == "binary":
            metrics["threshold"] = float(fold_result["selected_threshold"])
        _assert_close(metrics, expected_metrics, f"{prefix}.fold{fold}.outer_metrics")
        primary = float(metrics["mcc" if task == "binary" else "macro_f1"])
        fold_primary.append(primary)
        verified_folds.append({
            "fold": fold,
            "rows": len(by_fold[fold]),
            "repositories": len({str(row["repository"]).lower() for row in by_fold[fold]}),
            "primary": primary,
            "selected_config": fold_result["selected_config"],
            "selected_threshold": fold_result.get("selected_threshold"),
            "metrics": metrics,
        })
    primary = "mcc" if task == "binary" else "macro_f1"
    computed = {
        "task": task,
        "family": family,
        "eligible_rows": len(records),
        "folds": verified_folds,
        "outer_fold_primary": fold_primary,
        "primary_metric": primary,
        "primary_mean": float(np.mean(fold_primary)),
        "primary_std": float(np.std(fold_primary, ddof=0)),
        "primary_worst": float(np.min(fold_primary)),
        "primary_best": float(np.max(fold_primary)),
        "overall_oof_metrics": recompute_metrics(task, records),
        "oof_sha256": sha256_file(oof_path),
        "summary_sha256": sha256_file(summary_path),
        "confirmation_accessed": False,
    }
    for field in ("eligible_rows", "primary_metric", "primary_mean", "primary_std", "primary_worst", "primary_best"):
        _assert_close(computed[field], summary[field], f"{prefix}.summary.{field}")
    if summary.get("gold_sha256") != EXPECTED["gold_sha256"] or summary.get("development_view_sha256") != EXPECTED["development_view_sha256"] or summary.get("confirmation_accessed") is not False:
        raise RuntimeError(f"Summary identity mismatch: {prefix}")
    computed["records"] = records
    return computed


def validate_m0(root: Path, task: str, task_rows: list[dict[str, Any]], fold_map: dict[str, int]) -> dict[str, Any]:
    source = root / "reports/final_v2/gate2/partial_cpu"
    family = "M0"
    summary_path = source / f"{task}_{family}_summary.json"
    oof_path = source / f"{task}_{family}_oof.jsonl"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if sha256_file(oof_path) != summary["oof_sha256"]:
        raise RuntimeError(f"M0 OOF SHA mismatch for {task}")
    records = _load_oof(oof_path)
    row_by_id = {str(row["case_id"]): row for row in task_rows}
    if set(row_by_id) != {str(row["case_id"]) for row in records}:
        raise RuntimeError(f"M0 OOF membership mismatch for {task}")
    by_fold: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        source_row = row_by_id[str(record["case_id"])]
        repo = str(source_row["repository"]).strip().lower()
        expected_gold: Any = int(bool(source_row["gold_docs_update_required"])) if task == "binary" else str(source_row["gold_doc_category"])
        if record["gold"] != expected_gold or int(record["fold"]) != fold_map[repo]:
            raise RuntimeError(f"M0 identity mismatch for {record['case_id']}")
        by_fold[int(record["fold"])].append(record)
    folds = []
    primary_values = []
    for fold in range(5):
        metrics = recompute_metrics(task, by_fold[fold])
        fold_result = json.loads((source / f"{task}_M0_fold{fold}.json").read_text(encoding="utf-8"))
        if task == "binary":
            metrics["threshold"] = float(fold_result["outer_metrics"]["threshold"])
        _assert_close(metrics, fold_result["outer_metrics"], f"{task}.M0.fold{fold}")
        value = float(metrics["mcc" if task == "binary" else "macro_f1"])
        primary_values.append(value)
        folds.append({"fold": fold, "rows": len(by_fold[fold]), "primary": value, "metrics": metrics})
    result = {
        "task": task, "family": "M0", "eligible_rows": len(records), "folds": folds,
        "outer_fold_primary": primary_values, "primary_metric": "mcc" if task == "binary" else "macro_f1",
        "primary_mean": float(np.mean(primary_values)), "primary_std": float(np.std(primary_values)),
        "primary_worst": float(np.min(primary_values)), "primary_best": float(np.max(primary_values)),
        "overall_oof_metrics": recompute_metrics(task, records), "oof_sha256": sha256_file(oof_path),
        "summary_sha256": sha256_file(summary_path), "confirmation_accessed": False, "records": records,
    }
    for field in ("eligible_rows", "primary_metric", "primary_mean", "primary_std", "primary_worst", "primary_best"):
        _assert_close(result[field], summary[field], f"{task}.M0.{field}")
    return result


def choose_winner(families: dict[str, dict[str, Any]], tolerance: float = 0.005) -> dict[str, Any]:
    selectable = ["M1", "M2", "M3"]
    best = max(float(families[name]["primary_mean"]) for name in selectable)
    rows = []
    for rank, name in enumerate(selectable):
        mean = float(families[name]["primary_mean"])
        rows.append({
            "family": name, "primary_mean": mean, "primary_std": float(families[name]["primary_std"]),
            "primary_worst": float(families[name]["primary_worst"]), "primary_best": float(families[name]["primary_best"]),
            "difference_from_best_mean": best - mean, "inside_tolerance": (best - mean) <= tolerance + 1e-15,
            "simplicity_rank": rank,
        })
    candidates = [row for row in rows if row["inside_tolerance"]]
    winner = min(candidates, key=lambda row: (row["primary_std"], row["simplicity_rank"]))
    return {
        "primary_mean_tolerance": tolerance,
        "best_numerical_mean": best,
        "candidates": rows,
        "tie_break_sequence": ["inside 0.005 of best mean", "lower outer-fold standard deviation", "simplicity M1 < M2 < M3"],
        "selected_family": winner["family"],
        "reason": f"{winner['family']} is inside the 0.005 mean tolerance and has the lowest outer-fold standard deviation among eligible families; simplicity applies only if standard deviations tie.",
    }


def _confusion(task: str, records: list[dict[str, Any]]) -> np.ndarray:
    labels: list[Any] = [0, 1] if task == "binary" else list(PRIMARY_STAGE2_LABELS)
    index = {label: i for i, label in enumerate(labels)}
    cm = np.zeros((len(labels), len(labels)), dtype=np.int64)
    for row in records:
        cm[index[row["gold"]], index[row["prediction"]]] += 1
    return cm


def _primary_from_cm(task: str, cm: np.ndarray) -> float:
    if task == "binary":
        tn, fp, fn, tp = cm.ravel()
        denominator = math.sqrt(float((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
        return float((tp * tn - fp * fn) / denominator) if denominator else 0.0
    true_sum = cm.sum(axis=1)
    pred_sum = cm.sum(axis=0)
    tp = np.diag(cm)
    denom = true_sum + pred_sum
    f1 = np.divide(2 * tp, denom, out=np.zeros_like(tp, dtype=float), where=denom != 0)
    return float(np.mean(f1))


def repository_bootstrap(task: str, families: dict[str, dict[str, Any]], *, replicates: int = 2000, seed: int = 42) -> dict[str, Any]:
    repos = sorted({str(row["repository"]).lower() for row in families["M0"]["records"]})
    per_family: dict[str, np.ndarray] = {}
    for family, payload in families.items():
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in payload["records"]:
            grouped[str(row["repository"]).lower()].append(row)
        if set(grouped) != set(repos):
            raise RuntimeError(f"Repository universe mismatch in bootstrap: {task}/{family}")
        per_family[family] = np.stack([_confusion(task, grouped[repo]) for repo in repos])
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(repos), size=(replicates, len(repos)))
    values: dict[str, np.ndarray] = {}
    intervals: dict[str, Any] = {}
    for family, matrices in per_family.items():
        sampled = np.array([_primary_from_cm(task, matrices[indexes].sum(axis=0)) for indexes in draws])
        values[family] = sampled
        intervals[family] = {
            "point_estimate": _primary_from_cm(task, matrices.sum(axis=0)),
            "ci_low": float(np.quantile(sampled, 0.025)), "ci_high": float(np.quantile(sampled, 0.975)),
            "bootstrap_mean": float(np.mean(sampled)), "valid_replicates": int(len(sampled)),
        }
    paired: dict[str, Any] = {}
    for left, right in (("M1", "M2"), ("M1", "M3"), ("M2", "M3")):
        diff = values[left] - values[right]
        paired[f"{left}_minus_{right}"] = {
            "point_difference": intervals[left]["point_estimate"] - intervals[right]["point_estimate"],
            "ci_low": float(np.quantile(diff, 0.025)), "ci_high": float(np.quantile(diff, 0.975)),
            "probability_difference_gt_0": float(np.mean(diff > 0)), "probability_difference_eq_0": float(np.mean(diff == 0)),
            "valid_replicates": int(len(diff)),
        }
    return {"task": task, "replicates": replicates, "unit": "repository", "seed": seed, "interval": 0.95, "repositories": len(repos), "families": intervals, "paired": paired}


def slice_diagnostics(task: str, records: list[dict[str, Any]], rows_by_id: dict[str, dict[str, Any]], *, min_support: int = 100) -> dict[str, Any]:
    dimensions: dict[str, dict[str, list[dict[str, Any]]]] = {
        "language": defaultdict(list), "provenance_tier": defaultdict(list), "source_dataset": defaultdict(list),
        "label_source": defaultdict(list), "controlled_vs_natural": defaultdict(list), "natural_diversity": defaultdict(list),
    }
    for record in records:
        source = rows_by_id[str(record["case_id"])]
        provenance = str(source.get("provenance_tier") or "unknown")
        dimensions["language"][str(source.get("language") or "unknown").lower()].append(record)
        dimensions["provenance_tier"][provenance].append(record)
        dimensions["source_dataset"][str(source.get("consolidated_source_dataset") or "unknown")].append(record)
        dimensions["label_source"][str(source.get("label_source") or "unknown")].append(record)
        controlled = "controlled" if source.get("controlled_design_supervision") is True or source.get("label_source") == "controlled_design_label" else "natural"
        dimensions["controlled_vs_natural"][controlled].append(record)
        nd = "natural_diversity" if provenance == "natural_diversity_expansion_v1_reviewed" else "other"
        dimensions["natural_diversity"][nd].append(record)
    output: dict[str, Any] = {}
    for dimension, groups in dimensions.items():
        output[dimension] = {}
        for name, subset in sorted(groups.items()):
            output[dimension][name] = {
                "support": len(subset), "low_support": len(subset) < min_support,
                "metrics": recompute_metrics(task, subset),
            }
    repository_metrics = []
    grouped_repo: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped_repo[str(record["repository"]).lower()].append(record)
    for repo, subset in grouped_repo.items():
        repository_metrics.append({"repository": repo, "support": len(subset), "low_support": len(subset) < 20, "primary": _primary_from_cm(task, _confusion(task, subset))})
    values = np.array([row["primary"] for row in repository_metrics])
    output["repository_distribution"] = {
        "repositories": len(repository_metrics), "low_support_threshold": 20,
        "primary_quantiles": {"p0": float(np.min(values)), "p25": float(np.quantile(values, .25)), "p50": float(np.median(values)), "p75": float(np.quantile(values, .75)), "p100": float(np.max(values))},
        "per_repository": sorted(repository_metrics, key=lambda row: row["repository"]),
    }
    return output


def model_visible_collision_audit(rows: list[dict[str, Any]], fold_maps: dict[str, dict[str, int]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        payload = serialize_model_row(row).encode("utf-8")
        groups[hashlib.sha256(payload).hexdigest()].append(row)
    collisions = []
    for digest, members in groups.items():
        if len(members) < 2:
            continue
        folds = sorted({fold_maps["binary"][str(row["repository"]).strip().lower()] for row in members})
        labels = sorted({f"{bool(row['gold_docs_update_required'])}::{row['gold_doc_category']}" for row in members})
        collisions.append({"model_visible_sha256": digest, "rows": len(members), "case_ids": [str(row["case_id"]) for row in members], "folds": folds, "cross_fold": len(folds) > 1, "labels": labels, "conflicting_labels": len(labels) > 1})
    return {
        "groups": len(collisions), "rows": sum(group["rows"] for group in collisions),
        "cross_fold_groups": sum(group["cross_fold"] for group in collisions),
        "conflicting_label_groups": sum(group["conflicting_labels"] for group in collisions),
        "details": collisions,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def stripped(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {key: stripped(value) for key, value in payload.items() if key != "records"}
    if isinstance(payload, list):
        return [stripped(value) for value in payload]
    return payload
