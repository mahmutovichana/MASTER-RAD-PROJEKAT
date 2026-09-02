from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from scipy import sparse
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, f1_score
from sklearn.model_selection import StratifiedGroupKFold

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, binary_labels, category_eligible_rows, category_labels, serialize_model_row
from docguard_ml_v2.gate2_study import (
    DEVELOPMENT_PARTITIONS,
    append_registry,
    assert_inner_repo_disjoint,
    assert_registered_family,
    load_config,
    load_development_rows,
    load_fold_map,
    sha256_file,
)
from docguard_ml_v2.metrics import binary_metrics, category_metrics


@dataclass(frozen=True)
class Candidate:
    C: float
    class_weight: str | None
    semantic_scale: float = 1.0

    def payload(self) -> dict[str, Any]:
        return {"C": self.C, "class_weight": self.class_weight, "semantic_scale": self.semantic_scale}


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True).strip()


def vectorizer(config: dict[str, Any]) -> TfidfVectorizer:
    spec = config["families"]["M1"]
    return TfidfVectorizer(
        analyzer=spec["analyzer"],
        ngram_range=tuple(spec["ngram_range"]),
        min_df=int(spec["min_df"]),
        max_features=int(spec["max_features"]),
        sublinear_tf=bool(spec["sublinear_tf"]),
    )


def relation_matrix(code: np.ndarray, docs: np.ndarray) -> np.ndarray:
    dot = np.sum(code * docs, axis=1)
    denom = np.linalg.norm(code, axis=1) * np.linalg.norm(docs, axis=1)
    cosine = np.divide(dot, denom, out=np.zeros_like(dot), where=denom > 0).reshape(-1, 1)
    return np.concatenate([code, docs, np.abs(code - docs), code * docs, cosine], axis=1).astype(np.float32, copy=False)


def load_semantic(embedding_dir: Path, rows: list[dict[str, Any]], config: dict[str, Any], development_hash: str) -> np.ndarray:
    manifest_path = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
    artifact_path = embedding_dir / "gate2_unixcoder_embeddings.npz"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["development_view_sha256"] != development_hash:
        raise RuntimeError("Embedding development-view hash mismatch")
    if manifest["encoder_revision"] != config["families"]["M2"]["encoder_revision"]:
        raise RuntimeError("Embedding encoder revision mismatch")
    if sha256_file(artifact_path) != manifest["artifact_sha256"]:
        raise RuntimeError("Embedding artifact hash mismatch")
    with np.load(artifact_path, allow_pickle=False) as payload:
        ids = payload["case_ids"].tolist()
        expected = [str(row["case_id"]) for row in rows]
        if ids != expected:
            raise RuntimeError("Embedding row-order alignment mismatch")
        return relation_matrix(payload["code"], payload["docs"])


def candidates(config: dict[str, Any], family: str) -> list[Candidate]:
    if family == "M0":
        return [Candidate(1.0, None, 1.0)]
    scales = config["families"]["M3"]["semantic_scale"] if family == "M3" else [1.0]
    return [
        Candidate(float(c), weight, float(scale))
        for c in config["linear_classifier"]["C"]
        for weight in config["linear_classifier"]["class_weight"]
        for scale in scales
    ]


def classifier(task: str, candidate: Candidate, config: dict[str, Any]) -> LogisticRegression:
    return LogisticRegression(
        C=candidate.C,
        class_weight=candidate.class_weight,
        max_iter=int(config["linear_classifier"]["max_iter"]),
        random_state=int(config["seed"]),
        solver=config["linear_classifier"]["binary_solver" if task == "binary" else "category_solver"],
    )


def threshold_result(y: list[int], scores: list[float], threshold: float) -> dict[str, Any]:
    pred = [int(value >= threshold) for value in scores]
    metrics = binary_metrics(y, pred, scores)
    metrics["macro_f1"] = float(f1_score(y, pred, average="macro", zero_division=0))
    metrics["brier_score"] = float(brier_score_loss(y, scores))
    return {"threshold": threshold, **metrics}


def choose_threshold(y: list[int], scores: list[float], grid: list[float]) -> dict[str, Any]:
    results = [threshold_result(y, scores, float(threshold)) for threshold in grid]
    return max(results, key=lambda item: (item["mcc"], item["balanced_accuracy"], item["f1"], -abs(item["threshold"] - 0.5), -item["threshold"]))


def inner_splits(rows: list[dict[str, Any]], labels: list[Any], outer_fold: int, config: dict[str, Any]) -> list[tuple[np.ndarray, np.ndarray]]:
    groups = np.asarray([str(row["repository"]).strip().lower() for row in rows])
    cv = StratifiedGroupKFold(n_splits=int(config["cross_validation"]["inner"]["splits"]), shuffle=True, random_state=int(config["seed"]) + outer_fold)
    result = list(cv.split(rows, labels, groups))
    required = set(labels)
    for train_idx, val_idx in result:
        assert_inner_repo_disjoint(rows, train_idx, val_idx)
        if set(labels[index] for index in train_idx) != required or set(labels[index] for index in val_idx) != required:
            raise RuntimeError("Preregistered inner CV produced a fold without every required class")
    return result


def matrices_for_fold(family: str, texts: list[str], semantic: np.ndarray | None, train_idx: np.ndarray, val_idx: np.ndarray, scale: float, config: dict[str, Any]):
    if family == "M2":
        assert semantic is not None
        return semantic[train_idx], semantic[val_idx], None
    vec = vectorizer(config)
    x_train_lex = vec.fit_transform([texts[index] for index in train_idx])
    x_val_lex = vec.transform([texts[index] for index in val_idx])
    if family == "M1":
        return x_train_lex, x_val_lex, vec
    assert semantic is not None
    x_train = sparse.hstack([x_train_lex, sparse.csr_matrix(semantic[train_idx] * scale)], format="csr")
    x_val = sparse.hstack([x_val_lex, sparse.csr_matrix(semantic[val_idx] * scale)], format="csr")
    return x_train, x_val, vec


def select_inner(task: str, family: str, rows: list[dict[str, Any]], labels: list[Any], semantic: np.ndarray | None, outer_fold: int, config: dict[str, Any]) -> tuple[Candidate, float | None, dict[str, Any]]:
    texts = [serialize_model_row(row) for row in rows]
    splits = inner_splits(rows, labels, outer_fold, config)
    all_candidates = candidates(config, family)
    predictions: dict[Candidate, list[Any]] = {candidate: [None] * len(rows) for candidate in all_candidates}
    probabilities: dict[Candidate, list[float]] = {candidate: [math.nan] * len(rows) for candidate in all_candidates}
    # Fit each lexical/scale matrix once per inner fold, then evaluate all C/weight choices.
    for train_idx, val_idx in splits:
        for scale in sorted({candidate.semantic_scale for candidate in all_candidates}):
            subset = [candidate for candidate in all_candidates if candidate.semantic_scale == scale]
            x_train, x_val, _ = matrices_for_fold(family, texts, semantic, train_idx, val_idx, scale, config)
            y_train = [labels[index] for index in train_idx]
            for candidate in subset:
                model = classifier(task, candidate, config)
                model.fit(x_train, y_train)
                pred = model.predict(x_val).tolist()
                for index, value in zip(val_idx, pred):
                    predictions[candidate][int(index)] = value
                if task == "binary":
                    classes = model.classes_.tolist()
                    score = model.predict_proba(x_val)[:, classes.index(1)].tolist()
                    for index, value in zip(val_idx, score):
                        probabilities[candidate][int(index)] = float(value)
    ranked: list[tuple[tuple[Any, ...], Candidate, float | None, dict[str, Any]]] = []
    for candidate in all_candidates:
        if any(value is None for value in predictions[candidate]):
            raise RuntimeError("Incomplete inner OOF predictions")
        if task == "binary":
            chosen = choose_threshold([int(value) for value in labels], probabilities[candidate], config["tasks"]["binary"]["threshold_grid"])
            key = (chosen["mcc"], chosen["balanced_accuracy"], chosen["f1"], -abs(chosen["threshold"] - 0.5), -candidate.C, str(candidate.class_weight), -candidate.semantic_scale)
            ranked.append((key, candidate, float(chosen["threshold"]), chosen))
        else:
            metrics = category_metrics([str(value) for value in labels], [str(value) for value in predictions[candidate]], list(PRIMARY_STAGE2_LABELS))
            key = (metrics["macro_f1"], metrics["weighted_f1"], metrics["accuracy"], -candidate.C, str(candidate.class_weight), -candidate.semantic_scale)
            ranked.append((key, candidate, None, metrics))
    _, selected, threshold, metrics = max(ranked, key=lambda item: item[0])
    return selected, threshold, metrics


def fit_outer(task: str, family: str, train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]], train_labels: list[Any], val_labels: list[Any], semantic_train: np.ndarray | None, semantic_val: np.ndarray | None, selected: Candidate, threshold: float | None, config: dict[str, Any]) -> tuple[dict[str, Any], list[Any], list[float] | None]:
    if family == "M0":
        model = DummyClassifier(strategy="most_frequent")
        x_train = np.zeros((len(train_rows), 1), dtype=np.float32)
        x_val = np.zeros((len(val_rows), 1), dtype=np.float32)
    else:
        texts_train = [serialize_model_row(row) for row in train_rows]
        texts_val = [serialize_model_row(row) for row in val_rows]
        indices_train = np.arange(len(train_rows))
        indices_val = np.arange(len(val_rows))
        if family == "M2":
            assert semantic_train is not None and semantic_val is not None
            x_train, x_val = semantic_train, semantic_val
        else:
            vec = vectorizer(config)
            lexical_train = vec.fit_transform(texts_train)
            lexical_val = vec.transform(texts_val)
            if family == "M1":
                x_train, x_val = lexical_train, lexical_val
            else:
                assert semantic_train is not None and semantic_val is not None
                x_train = sparse.hstack([lexical_train, sparse.csr_matrix(semantic_train * selected.semantic_scale)], format="csr")
                x_val = sparse.hstack([lexical_val, sparse.csr_matrix(semantic_val * selected.semantic_scale)], format="csr")
        model = classifier(task, selected, config)
    model.fit(x_train, train_labels)
    if task == "binary":
        classes = model.classes_.tolist()
        if 1 in classes:
            scores = model.predict_proba(x_val)[:, classes.index(1)].astype(float).tolist()
        else:
            scores = [0.0] * len(val_rows)
        effective_threshold = 0.5 if family == "M0" else float(threshold)
        pred = [int(value >= effective_threshold) for value in scores]
        metrics = threshold_result([int(value) for value in val_labels], scores, effective_threshold)
        return metrics, pred, scores
    pred = [str(value) for value in model.predict(x_val)]
    return category_metrics([str(value) for value in val_labels], pred, list(PRIMARY_STAGE2_LABELS)), pred, None


def run_family(task: str, family: str, rows: list[dict[str, Any]], semantic_all: np.ndarray | None, fold_path: Path, output_dir: Path, registry: Path, config: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    if task == "category":
        eligible_indexes = [index for index, row in enumerate(rows) if bool(row["gold_docs_update_required"]) and str(row["gold_doc_category"]) in PRIMARY_STAGE2_LABELS]
        task_rows = [rows[index] for index in eligible_indexes]
        semantic = None if semantic_all is None else semantic_all[eligible_indexes]
        labels: list[Any] = category_labels(task_rows)
    else:
        task_rows = rows
        semantic = semantic_all
        labels = binary_labels(task_rows)
    fold_map = load_fold_map(fold_path, task=task)
    outer_folds = sorted(set(fold_map.values()))
    oof_pred: list[Any] = [None] * len(task_rows)
    oof_score: list[float | None] = [None] * len(task_rows)
    fold_results: list[dict[str, Any]] = []
    source_commit = git_sha()
    for fold in outer_folds:
        run_id = f"gate2-{task}-{family}-fold{fold}-{source_commit[:12]}"
        base_record = {"run_id": run_id, "task": task, "family": family, "outer_fold": fold, "config": str(config), "random_seed": config["seed"], "source_commit": source_commit, "gold_sha": metadata["gold_sha256"], "encoder_revision": config["families"]["M2"]["encoder_revision"] if family in {"M2", "M3"} else None}
        append_registry(registry, {**base_record, "status": "STARTED", "started_unix": time.time()})
        try:
            val_idx = np.asarray([index for index, row in enumerate(task_rows) if fold_map[str(row["repository"]).strip().lower()] == fold], dtype=int)
            train_idx = np.asarray([index for index in range(len(task_rows)) if index not in set(val_idx.tolist())], dtype=int)
            assert_inner_repo_disjoint(task_rows, train_idx, val_idx)
            train_rows = [task_rows[index] for index in train_idx]
            val_rows = [task_rows[index] for index in val_idx]
            train_labels = [labels[index] for index in train_idx]
            val_labels = [labels[index] for index in val_idx]
            if family == "M0":
                selected, threshold, inner_metrics = Candidate(1.0, None), (0.5 if task == "binary" else None), {"baseline": "most_frequent"}
            else:
                selected, threshold, inner_metrics = select_inner(task, family, train_rows, train_labels, None if semantic is None else semantic[train_idx], fold, config)
            metrics, pred, scores = fit_outer(task, family, train_rows, val_rows, train_labels, val_labels, None if semantic is None else semantic[train_idx], None if semantic is None else semantic[val_idx], selected, threshold, config)
            for local, value in zip(val_idx, pred):
                oof_pred[int(local)] = value
            if scores is not None:
                for local, value in zip(val_idx, scores):
                    oof_score[int(local)] = value
            result = {"task": task, "family": family, "outer_fold": fold, "train_rows": len(train_idx), "validation_rows": len(val_idx), "train_repositories": len({task_rows[index]["repository"] for index in train_idx}), "validation_repositories": len({task_rows[index]["repository"] for index in val_idx}), "selected_config": selected.payload(), "selected_threshold": threshold, "inner_selection_metrics": inner_metrics, "outer_metrics": metrics}
            fold_results.append(result)
            result_path = output_dir / f"{task}_{family}_fold{fold}.json"
            result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            append_registry(registry, {**base_record, "status": "COMPLETED", "ended_unix": time.time(), "result_artifact_identity": sha256_file(result_path)})
        except Exception as exc:
            append_registry(registry, {**base_record, "status": "FAILED", "ended_unix": time.time(), "error": str(exc), "traceback": traceback.format_exc()})
            raise
    if any(value is None for value in oof_pred):
        raise RuntimeError("Incomplete outer OOF predictions")
    primary = "mcc" if task == "binary" else "macro_f1"
    values = [float(item["outer_metrics"][primary]) for item in fold_results]
    summary = {"task": task, "family": family, "eligible_rows": len(task_rows), "outer_folds": len(outer_folds), "primary_metric": primary, "primary_mean": float(np.mean(values)), "primary_std": float(np.std(values, ddof=0)), "primary_worst": float(np.min(values)), "primary_best": float(np.max(values)), "fold_results": fold_results, "gold_sha256": metadata["gold_sha256"], "development_view_sha256": metadata["development_view_sha256"], "confirmation_accessed": False}
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / f"{task}_{family}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    oof_path = output_dir / f"{task}_{family}_oof.jsonl"
    with oof_path.open("w", encoding="utf-8", newline="\n") as handle:
        for index, (row, gold, pred) in enumerate(zip(task_rows, labels, oof_pred)):
            payload = {"case_id": row["case_id"], "repository": row["repository"], "language": row.get("language"), "provenance_tier": row.get("provenance_tier"), "consolidated_source_dataset": row.get("consolidated_source_dataset"), "fold": fold_map[str(row["repository"]).strip().lower()], "gold": gold, "prediction": pred}
            if task == "binary":
                payload["probability"] = oof_score[index]
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    summary["summary_sha256"] = sha256_file(summary_path)
    summary["oof_path"] = str(oof_path)
    summary["oof_sha256"] = sha256_file(oof_path)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def run(config_path: Path, output_dir: Path, families: list[str], embedding_dir: Path | None) -> list[dict[str, Any]]:
    config = load_config(config_path)
    for family in families:
        assert_registered_family(config, family)
    rows, metadata = load_development_rows(config_path=config_path)
    semantic = None
    if any(family in {"M2", "M3"} for family in families):
        if embedding_dir is None:
            raise RuntimeError("M2/M3 require --embedding-dir")
        semantic = load_semantic(embedding_dir, rows, config, metadata["development_view_sha256"])
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = output_dir / "GATE2_RUN_REGISTRY.jsonl"
    results = []
    for task in ("binary", "category"):
        fold_path = PROJECT_ROOT / f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv"
        for family in families:
            print(json.dumps({"task": task, "family": family, "status": "STARTING"}), flush=True)
            results.append(run_family(task, family, rows, semantic, fold_path, output_dir, registry, config, metadata))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--embedding-dir")
    parser.add_argument("--families", nargs="+", required=True)
    args = parser.parse_args()
    results = run(Path(args.config), Path(args.output_dir), args.families, Path(args.embedding_dir) if args.embedding_dir else None)
    print(json.dumps({"status": "COMPLETE", "summaries": [{"task": item["task"], "family": item["family"], "primary_mean": item["primary_mean"]} for item in results]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
