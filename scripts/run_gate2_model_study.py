from __future__ import annotations

import argparse
import concurrent.futures
import gc
import json
import math
import os
import subprocess
import sys
import threading
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
from threadpoolctl import threadpool_limits

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, binary_labels, category_eligible_rows, category_labels, serialize_model_row
from docguard_ml_v2.gate2_study import (
    DEVELOPMENT_PARTITIONS,
    append_registry,
    assert_inner_repo_disjoint,
    assert_registered_family,
    load_config,
    load_development_rows,
    load_fold_map,
    load_fold_checkpoint,
    sha256_file,
    write_fold_checkpoint,
)
from docguard_ml_v2.metrics import binary_metrics, category_metrics


@dataclass(frozen=True)
class Candidate:
    C: float
    class_weight: str | None
    semantic_scale: float = 1.0

    def payload(self) -> dict[str, Any]:
        return {"C": self.C, "class_weight": self.class_weight, "semantic_scale": self.semantic_scale}


_PRINT_LOCK = threading.Lock()


def emit(tag: str, **fields: Any) -> None:
    rendered = " ".join(f"{key}={value}" for key, value in fields.items())
    with _PRINT_LOCK:
        print(f"{tag} {rendered}".rstrip(), flush=True)


def rss_gb() -> float | None:
    try:
        page_size = os.sysconf("SC_PAGE_SIZE")
        resident_pages = int(Path("/proc/self/statm").read_text(encoding="ascii").split()[1])
        return resident_pages * page_size / (1024 ** 3)
    except (AttributeError, OSError, ValueError, IndexError):
        return None


def matrix_fields(matrix: Any) -> dict[str, Any]:
    shape = getattr(matrix, "shape", (None, None))
    return {
        "rows": shape[0],
        "features": shape[1],
        "nnz": getattr(matrix, "nnz", "dense"),
    }


class FitHeartbeat:
    def __init__(self, context: dict[str, Any], *, interval_seconds: float = 60.0):
        self.context = context
        self.interval_seconds = interval_seconds
        self._stop = threading.Event()
        self._started = 0.0
        self._thread: threading.Thread | None = None
        self._error: BaseException | None = None

    def __enter__(self) -> "FitHeartbeat":
        self._started = time.monotonic()
        if self.interval_seconds > 0:
            self._thread = threading.Thread(target=self._run, name="gate2-fit-heartbeat", daemon=True)
            self._thread.start()
        return self

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            try:
                emit(
                    "[HEARTBEAT]",
                    **self.context,
                    current_fit_elapsed_seconds=round(time.monotonic() - self._started, 1),
                    process_alive=True,
                    rss_gb=round(rss_gb(), 3) if rss_gb() is not None else "unavailable",
                )
            except BaseException as exc:
                self._error = exc
                return

    def __exit__(self, exc_type, exc, traceback_object) -> bool:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=max(1.0, min(self.interval_seconds, 5.0)))
        if self._error is not None and exc is None:
            raise RuntimeError("Gate 2 heartbeat failed") from self._error
        return False


class ExecutionProgress:
    def __init__(self, *, total_outer_folds: int, total_candidate_fits: int, recovered_outer_folds: int, recovered_candidate_fits: int):
        self.total_outer_folds = total_outer_folds
        self.total_candidate_fits = total_candidate_fits
        self.completed_outer_folds = recovered_outer_folds
        self.completed_candidate_fits = recovered_candidate_fits
        self.measured_fit_durations: list[float] = []
        self._lock = threading.Lock()

    def record_fit(self, duration: float) -> dict[str, Any]:
        with self._lock:
            self.completed_candidate_fits += 1
            self.measured_fit_durations.append(duration)
            average = float(np.mean(self.measured_fit_durations))
            remaining = max(0, self.total_candidate_fits - self.completed_candidate_fits)
            return {
                "candidate_fits_completed": f"{self.completed_candidate_fits}/{self.total_candidate_fits}",
                "structural_progress_percent": round(100.0 * self.completed_candidate_fits / self.total_candidate_fits, 2),
                "estimated_remaining_seconds": round(average * remaining, 1),
            }

    def record_outer_fold(self) -> dict[str, Any]:
        with self._lock:
            self.completed_outer_folds += 1
            return {"completed_outer_folds": f"{self.completed_outer_folds}/{self.total_outer_folds}"}


def fits_per_outer(config: dict[str, Any], family: str) -> int:
    if family == "M0":
        return 1
    inner = int(config["cross_validation"]["inner"]["splits"])
    return inner * len(candidates(config, family)) + 1


def resume_plan(
    *,
    rows: list[dict[str, Any]],
    families: list[str],
    output_dir: Path,
    config: dict[str, Any],
    metadata: dict[str, Any],
    resume: bool,
    force_rerun: bool,
    fold_paths: dict[str, Path] | None = None,
    tasks: tuple[str, ...] = ("binary", "category"),
) -> tuple[int, int, int, int]:
    total_outer = 0
    recovered_outer = 0
    total_fits = 0
    recovered_fits = 0
    next_work: tuple[str, str, int] | None = None
    for task in tasks:
        task_rows = category_eligible_rows(rows, allowed_partitions=DEVELOPMENT_PARTITIONS) if task == "category" else rows
        fold_path = (fold_paths or {}).get(task, PROJECT_ROOT / f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv")
        fold_map = load_fold_map(fold_path, task=task)
        fold_assignment_sha = sha256_file(fold_path)
        outer_folds = sorted(set(fold_map.values()))
        for family in families:
            complete = 0
            for fold in outer_folds:
                total_outer += 1
                total_fits += fits_per_outer(config, family)
                path = output_dir / f"{task}_{family}_fold{fold}_checkpoint.json"
                if resume and not force_rerun and path.exists():
                    expected_identity = {
                        "task": task,
                        "family": family,
                        "outer_fold": fold,
                        "gold_sha256": metadata["gold_sha256"],
                        "development_view_sha256": metadata["development_view_sha256"],
                        "scientific_config_sha256": metadata["scientific_config_sha256"],
                        "fold_assignment_sha256": fold_assignment_sha,
                    }
                    if family in {"M2", "M3"}:
                        expected_identity["embedding_artifact_sha256"] = metadata["embedding_artifact_sha256"]
                    checkpoint = load_fold_checkpoint(path, expected_identity=expected_identity)
                    expected_ids = [
                        str(row["case_id"])
                        for row in task_rows
                        if fold_map[str(row["repository"]).strip().lower()] == fold
                    ]
                    if checkpoint["validation_case_ids"] != expected_ids:
                        raise RuntimeError("Fold checkpoint validation case identity mismatch in resume plan")
                    complete += 1
                    recovered_outer += 1
                    recovered_fits += fits_per_outer(config, family)
                elif next_work is None:
                    next_work = (task, family, fold)
            emit("[RESUME PLAN]", task=task, family=family, complete=f"{complete}/{len(outer_folds)}")
    if next_work is None:
        emit("[RESUME NEXT]", status="all_requested_outer_folds_complete")
    else:
        emit("[RESUME NEXT]", task=next_work[0], family=next_work[1], outer_fold=f"{next_work[2] + 1}/5")
    emit(
        "[STRUCTURAL PROGRESS]",
        completed_outer_folds=f"{recovered_outer}/{total_outer}",
        candidate_fits_completed=f"{recovered_fits}/{total_fits}",
        structural_progress_percent=round(100.0 * recovered_fits / total_fits, 2),
    )
    return total_outer, total_fits, recovered_outer, recovered_fits


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


def load_semantic(embedding_dir: Path, rows: list[dict[str, Any]], config: dict[str, Any], development_hash: str, *, artifact_already_verified: bool = False) -> np.ndarray:
    manifest_path = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
    artifact_path = embedding_dir / "gate2_unixcoder_embeddings.npz"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["development_view_sha256"] != development_hash:
        raise RuntimeError("Embedding development-view hash mismatch")
    if manifest["encoder_revision"] != config["families"]["M2"]["encoder_revision"]:
        raise RuntimeError("Embedding encoder revision mismatch")
    if not artifact_already_verified:
        emit("[HASH START]", artifact=artifact_path, purpose="embedding_identity")
        hash_started = time.monotonic()
        if sha256_file(artifact_path) != manifest["artifact_sha256"]:
            raise RuntimeError("Embedding artifact hash mismatch")
        emit("[HASH DONE]", artifact=artifact_path, duration_seconds=round(time.monotonic() - hash_started, 3))
    relation_path = embedding_dir / "gate2_semantic_relation.float32.mmap"
    relation_manifest_path = embedding_dir / "gate2_semantic_relation_manifest.json"
    with np.load(artifact_path, allow_pickle=False) as payload:
        ids = payload["case_ids"].tolist()
        expected = [str(row["case_id"]) for row in rows]
        if ids != expected:
            raise RuntimeError("Embedding row-order alignment mismatch")
        code = payload["code"]
        docs = payload["docs"]
        shape = (len(rows), int(code.shape[1]) * 4 + 1)
        expected_bytes = int(np.prod(shape)) * np.dtype("float32").itemsize
        expected_relation_identity = {
            "schema_version": "gate2_semantic_relation_mmap_v1",
            "source_embedding_sha256": manifest["artifact_sha256"],
            "development_view_sha256": development_hash,
            "shape": list(shape),
            "dtype": "float32",
            "confirmation_accessed": False,
        }
        if relation_manifest_path.exists() or relation_path.exists():
            if not relation_manifest_path.exists() or not relation_path.exists():
                raise RuntimeError("Semantic relation mmap pair is incomplete")
            relation_manifest = json.loads(relation_manifest_path.read_text(encoding="utf-8"))
            for key, value in expected_relation_identity.items():
                if relation_manifest.get(key) != value:
                    raise RuntimeError(f"Semantic relation mmap identity mismatch: {key}")
            emit("[HASH START]", artifact=relation_path, purpose="relation_mmap_identity")
            hash_started = time.monotonic()
            relation_hash = sha256_file(relation_path)
            emit("[HASH DONE]", artifact=relation_path, duration_seconds=round(time.monotonic() - hash_started, 3))
            if relation_path.stat().st_size != expected_bytes or relation_hash != relation_manifest.get("artifact_sha256"):
                raise RuntimeError("Semantic relation mmap hash/size mismatch")
        else:
            emit("[RELATION MMAP START]", rows=len(rows), features=shape[1], dtype="float32")
            relation_started = time.monotonic()
            relation = np.memmap(relation_path, dtype="float32", mode="w+", shape=shape)
            for start in range(0, len(rows), 1024):
                stop = min(start + 1024, len(rows))
                relation[start:stop] = relation_matrix(code[start:stop], docs[start:stop])
            relation.flush()
            del relation
            relation_manifest = {**expected_relation_identity, "artifact_sha256": sha256_file(relation_path)}
            temporary = relation_manifest_path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(relation_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            temporary.replace(relation_manifest_path)
            emit("[RELATION MMAP DONE]", duration_seconds=round(time.monotonic() - relation_started, 3), artifact=relation_path)
    return np.memmap(relation_path, dtype="float32", mode="r", shape=shape)


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


def fit_candidate(
    *,
    task: str,
    family: str,
    candidate: Candidate,
    x_train: Any,
    x_val: Any,
    y_train: list[Any],
    outer_fold: int,
    inner_fold: int,
    candidate_ordinal: int,
    candidate_total: int,
    outer_started: float,
    config: dict[str, Any],
    progress: ExecutionProgress,
    heartbeat_seconds: float,
    candidate_workers: int,
) -> tuple[list[Any], list[float] | None]:
    context = {
        "task": task,
        "family": family,
        "outer_fold": f"{outer_fold + 1}/5",
        "inner_fold": f"{inner_fold + 1}/{config['cross_validation']['inner']['splits']}",
        "candidate_fit": f"{candidate_ordinal}/{candidate_total}",
        "C": candidate.C,
        "class_weight": candidate.class_weight,
        "semantic_scale": candidate.semantic_scale,
        "train_rows": x_train.shape[0],
        "validation_rows": x_val.shape[0],
        **matrix_fields(x_train),
    }
    emit("[FIT START]", **context)
    emit("[MODEL FIT START]", **context)
    model = classifier(task, candidate, config)
    started = time.monotonic()
    with FitHeartbeat(context, interval_seconds=heartbeat_seconds):
        model.fit(x_train, y_train)
    duration = time.monotonic() - started
    progress_fields = progress.record_fit(duration)
    emit(
        "[MODEL FIT DONE]",
        task=task,
        family=family,
        duration_seconds=round(duration, 3),
        n_iter=np.asarray(model.n_iter_).tolist(),
        rss_gb=round(rss_gb(), 3) if rss_gb() is not None else "unavailable",
    )
    emit(
        "[FIT DONE]",
        duration_seconds=round(duration, 3),
        n_iter=np.asarray(model.n_iter_).tolist(),
        candidate_progress=f"{candidate_ordinal}/{candidate_total}",
        candidate_percent=round(100.0 * candidate_ordinal / candidate_total, 1),
        outer_fold_elapsed_seconds=round(time.monotonic() - outer_started, 1),
        estimated_outer_fold_remaining_seconds=round(duration * max(0, candidate_total - candidate_ordinal) / candidate_workers, 1),
        **progress_fields,
    )
    emit("[PREDICT START]", task=task, family=family, outer_fold=f"{outer_fold + 1}/5", inner_fold=inner_fold + 1, candidate_fit=f"{candidate_ordinal}/{candidate_total}")
    predict_started = time.monotonic()
    predicted = model.predict(x_val).tolist()
    scores: list[float] | None = None
    if task == "binary":
        classes = model.classes_.tolist()
        scores = model.predict_proba(x_val)[:, classes.index(1)].astype(float).tolist()
    emit("[PREDICT DONE]", duration_seconds=round(time.monotonic() - predict_started, 3))
    del model
    return predicted, scores


def execute_candidate_jobs(jobs: list[Any], execute: Any, *, candidate_workers: int) -> list[Any]:
    if candidate_workers == 1:
        return [execute(job) for job in jobs]
    with concurrent.futures.ThreadPoolExecutor(max_workers=candidate_workers, thread_name_prefix="gate2-candidate") as executor:
        futures = [executor.submit(execute, job) for job in jobs]
        return [future.result() for future in futures]


def select_inner(
    task: str,
    family: str,
    rows: list[dict[str, Any]],
    labels: list[Any],
    semantic: np.ndarray | None,
    outer_fold: int,
    config: dict[str, Any],
    *,
    progress: ExecutionProgress,
    candidate_workers: int,
    heartbeat_seconds: float,
    outer_started: float,
) -> tuple[Candidate, float | None, dict[str, Any]]:
    texts = [serialize_model_row(row) for row in rows]
    splits = inner_splits(rows, labels, outer_fold, config)
    all_candidates = candidates(config, family)
    predictions: dict[Candidate, list[Any]] = {candidate: [None] * len(rows) for candidate in all_candidates}
    probabilities: dict[Candidate, list[float]] = {candidate: [math.nan] * len(rows) for candidate in all_candidates}
    # Fit the lexical block once per inner fold, but materialize only one semantic
    # scale at a time so M3 never retains three equivalent large sparse matrices.
    candidate_total = len(splits) * len(all_candidates)
    for inner_fold, (train_idx, val_idx) in enumerate(splits):
        emit("[INNER]", outer=f"{outer_fold + 1}/5", inner=f"{inner_fold + 1}/{len(splits)}", task=task, family=family)
        scales = sorted({candidate.semantic_scale for candidate in all_candidates})
        lexical_train = lexical_val = semantic_train_csr = semantic_val_csr = None
        if family == "M3":
            assert semantic is not None
            emit("[TFIDF START]", task=task, family=family, outer_fold=outer_fold + 1, inner_fold=inner_fold + 1)
            phase_started = time.monotonic()
            vec = vectorizer(config)
            lexical_train = vec.fit_transform([texts[index] for index in train_idx])
            lexical_val = vec.transform([texts[index] for index in val_idx])
            emit("[TFIDF DONE]", duration_seconds=round(time.monotonic() - phase_started, 3), **matrix_fields(lexical_train))
            emit("[SEMANTIC SLICE START]", task=task, family=family, outer_fold=outer_fold + 1, inner_fold=inner_fold + 1)
            phase_started = time.monotonic()
            semantic_train_csr = sparse.csr_matrix(semantic[train_idx])
            semantic_val_csr = sparse.csr_matrix(semantic[val_idx])
            emit("[SEMANTIC SLICE DONE]", duration_seconds=round(time.monotonic() - phase_started, 3), **matrix_fields(semantic_train_csr))
        y_train = [labels[index] for index in train_idx]
        for scale in scales:
            if family == "M3":
                assert semantic_train_csr is not None and semantic_val_csr is not None
                emit("[HYBRID MATRIX START]", task=task, family=family, outer_fold=outer_fold + 1, inner_fold=inner_fold + 1, semantic_scale=scale)
                phase_started = time.monotonic()
                # Registered scales are non-zero powers of two. Scale the private
                # fold CSR buffers only while hstack copies them, then restore
                # exactly; this avoids a second dense/CSR semantic copy.
                semantic_train_csr.data *= scale
                semantic_val_csr.data *= scale
                try:
                    x_train = sparse.hstack([lexical_train, semantic_train_csr], format="csr")
                    x_val = sparse.hstack([lexical_val, semantic_val_csr], format="csr")
                finally:
                    semantic_train_csr.data /= scale
                    semantic_val_csr.data /= scale
                emit("[HYBRID MATRIX DONE]", duration_seconds=round(time.monotonic() - phase_started, 3), **matrix_fields(x_train))
            else:
                phase_tag = "[TFIDF START]" if family == "M1" else "[SEMANTIC SLICE START]"
                emit(phase_tag, task=task, family=family, outer_fold=outer_fold + 1, inner_fold=inner_fold + 1)
                phase_started = time.monotonic()
                x_train, x_val, _ = matrices_for_fold(family, texts, semantic, train_idx, val_idx, scale, config)
                done_tag = "[TFIDF DONE]" if family == "M1" else "[SEMANTIC SLICE DONE]"
                emit(done_tag, duration_seconds=round(time.monotonic() - phase_started, 3), **matrix_fields(x_train))
            subset = [candidate for candidate in all_candidates if candidate.semantic_scale == scale]
            jobs: list[tuple[Candidate, int]] = []
            for candidate in subset:
                global_candidate_index = all_candidates.index(candidate)
                ordinal = inner_fold * len(all_candidates) + global_candidate_index + 1
                jobs.append((candidate, ordinal))

            def execute(job: tuple[Candidate, int]) -> tuple[Candidate, list[Any], list[float] | None]:
                candidate, ordinal = job
                pred, score = fit_candidate(
                    task=task,
                    family=family,
                    candidate=candidate,
                    x_train=x_train,
                    x_val=x_val,
                    y_train=y_train,
                    outer_fold=outer_fold,
                    inner_fold=inner_fold,
                    candidate_ordinal=ordinal,
                    candidate_total=candidate_total,
                    outer_started=outer_started,
                    config=config,
                    progress=progress,
                    heartbeat_seconds=heartbeat_seconds,
                    candidate_workers=candidate_workers,
                )
                return candidate, pred, score

            completed = execute_candidate_jobs(jobs, execute, candidate_workers=candidate_workers)
            for candidate, pred, score in completed:
                for index, value in zip(val_idx, pred):
                    predictions[candidate][int(index)] = value
                if task == "binary":
                    assert score is not None
                    for index, value in zip(val_idx, score):
                        probabilities[candidate][int(index)] = float(value)
            del x_train, x_val
        gc_started = time.monotonic()
        del lexical_train, lexical_val, semantic_train_csr, semantic_val_csr
        gc.collect()
        emit("[GC DONE]", duration_seconds=round(time.monotonic() - gc_started, 3), scope="inner_fold")
    ranked: list[tuple[tuple[Any, ...], Candidate, float | None, dict[str, Any]]] = []
    for candidate in all_candidates:
        if any(value is None for value in predictions[candidate]):
            raise RuntimeError("Incomplete inner OOF predictions")
        if task == "binary":
            emit("[THRESHOLD START]", task=task, family=family, outer_fold=outer_fold + 1, C=candidate.C, class_weight=candidate.class_weight, semantic_scale=candidate.semantic_scale)
            threshold_started = time.monotonic()
            chosen = choose_threshold([int(value) for value in labels], probabilities[candidate], config["tasks"]["binary"]["threshold_grid"])
            emit("[THRESHOLD DONE]", duration_seconds=round(time.monotonic() - threshold_started, 3), selected_threshold=chosen["threshold"])
            key = (chosen["mcc"], chosen["balanced_accuracy"], chosen["f1"], -abs(chosen["threshold"] - 0.5), -candidate.C, str(candidate.class_weight), -candidate.semantic_scale)
            ranked.append((key, candidate, float(chosen["threshold"]), chosen))
        else:
            metrics = category_metrics([str(value) for value in labels], [str(value) for value in predictions[candidate]], list(PRIMARY_STAGE2_LABELS))
            key = (metrics["macro_f1"], metrics["weighted_f1"], metrics["accuracy"], -candidate.C, str(candidate.class_weight), -candidate.semantic_scale)
            ranked.append((key, candidate, None, metrics))
    _, selected, threshold, metrics = max(ranked, key=lambda item: item[0])
    return selected, threshold, metrics


def fit_outer(
    task: str,
    family: str,
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    train_labels: list[Any],
    val_labels: list[Any],
    semantic_train: np.ndarray | None,
    semantic_val: np.ndarray | None,
    selected: Candidate,
    threshold: float | None,
    config: dict[str, Any],
    *,
    outer_fold: int,
    progress: ExecutionProgress,
    heartbeat_seconds: float,
) -> tuple[dict[str, Any], list[Any], list[float] | None]:
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
            emit("[TFIDF START]", task=task, family=family, outer_fold=outer_fold + 1, phase="outer")
            phase_started = time.monotonic()
            vec = vectorizer(config)
            lexical_train = vec.fit_transform(texts_train)
            lexical_val = vec.transform(texts_val)
            emit("[TFIDF DONE]", duration_seconds=round(time.monotonic() - phase_started, 3), phase="outer", **matrix_fields(lexical_train))
            if family == "M1":
                x_train, x_val = lexical_train, lexical_val
            else:
                assert semantic_train is not None and semantic_val is not None
                emit("[HYBRID MATRIX START]", task=task, family=family, outer_fold=outer_fold + 1, phase="outer", semantic_scale=selected.semantic_scale)
                phase_started = time.monotonic()
                x_train = sparse.hstack([lexical_train, sparse.csr_matrix(semantic_train * selected.semantic_scale)], format="csr")
                x_val = sparse.hstack([lexical_val, sparse.csr_matrix(semantic_val * selected.semantic_scale)], format="csr")
                emit("[HYBRID MATRIX DONE]", duration_seconds=round(time.monotonic() - phase_started, 3), phase="outer", **matrix_fields(x_train))
        model = classifier(task, selected, config)
    fit_context = {
        "task": task,
        "family": family,
        "outer_fold": f"{outer_fold + 1}/5",
        "phase": "outer_final_fit",
        "C": selected.C,
        "class_weight": selected.class_weight,
        "semantic_scale": selected.semantic_scale,
        **matrix_fields(x_train),
    }
    emit("[MODEL FIT START]", **fit_context)
    fit_started = time.monotonic()
    with FitHeartbeat(fit_context, interval_seconds=heartbeat_seconds):
        model.fit(x_train, train_labels)
    fit_duration = time.monotonic() - fit_started
    progress_fields = progress.record_fit(fit_duration)
    emit("[MODEL FIT DONE]", duration_seconds=round(fit_duration, 3), n_iter=np.asarray(getattr(model, "n_iter_", [])).tolist(), **progress_fields)
    emit("[PREDICT START]", task=task, family=family, outer_fold=f"{outer_fold + 1}/5", phase="outer")
    predict_started = time.monotonic()
    if task == "binary":
        classes = model.classes_.tolist()
        if 1 in classes:
            scores = model.predict_proba(x_val)[:, classes.index(1)].astype(float).tolist()
        else:
            scores = [0.0] * len(val_rows)
        effective_threshold = 0.5 if family == "M0" else float(threshold)
        pred = [int(value >= effective_threshold) for value in scores]
        metrics = threshold_result([int(value) for value in val_labels], scores, effective_threshold)
        emit("[PREDICT DONE]", duration_seconds=round(time.monotonic() - predict_started, 3), phase="outer")
        return metrics, pred, scores
    pred = [str(value) for value in model.predict(x_val)]
    emit("[PREDICT DONE]", duration_seconds=round(time.monotonic() - predict_started, 3), phase="outer")
    return category_metrics([str(value) for value in val_labels], pred, list(PRIMARY_STAGE2_LABELS)), pred, None


def run_family(
    task: str,
    family: str,
    rows: list[dict[str, Any]],
    semantic_all: np.ndarray | None,
    fold_path: Path,
    output_dir: Path,
    registry: Path,
    config: dict[str, Any],
    metadata: dict[str, Any],
    *,
    resume: bool,
    force_rerun: bool,
    progress: ExecutionProgress,
    candidate_workers: int,
    heartbeat_seconds: float,
) -> dict[str, Any]:
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
    fold_assignment_sha = sha256_file(fold_path)
    completed_at_start = sum((output_dir / f"{task}_{family}_fold{fold}_checkpoint.json").exists() for fold in outer_folds) if resume and not force_rerun else 0
    emit("[FAMILY]", task=task, family=family, completed_outer_folds=f"{completed_at_start}/{len(outer_folds)}", candidate_workers=candidate_workers)
    for fold in outer_folds:
        outer_started = time.monotonic()
        emit("[GATE2]", task=task, family=family, outer_fold=f"{fold + 1}/{len(outer_folds)}")
        run_id = f"gate2-{task}-{family}-fold{fold}-{source_commit[:12]}"
        base_record = {"run_id": run_id, "task": task, "family": family, "outer_fold": fold, "config": {"schema_version": config["schema_version"], "registered_family": family}, "random_seed": config["seed"], "source_commit": source_commit, "gold_sha": metadata["gold_sha256"], "encoder_revision": config["families"]["M2"]["encoder_revision"] if family in {"M2", "M3"} else None}
        val_idx = np.asarray([index for index, row in enumerate(task_rows) if fold_map[str(row["repository"]).strip().lower()] == fold], dtype=int)
        validation_indexes = set(val_idx.tolist())
        train_idx = np.asarray([index for index in range(len(task_rows)) if index not in validation_indexes], dtype=int)
        expected_case_ids = [str(task_rows[index]["case_id"]) for index in val_idx]
        checkpoint_path = output_dir / f"{task}_{family}_fold{fold}_checkpoint.json"
        checkpoint_identity = {
            "task": task,
            "family": family,
            "outer_fold": fold,
            "gold_sha256": metadata["gold_sha256"],
            "development_view_sha256": metadata["development_view_sha256"],
            "scientific_config_sha256": metadata["scientific_config_sha256"],
            "fold_assignment_sha256": fold_assignment_sha,
        }
        if family in {"M2", "M3"}:
            checkpoint_identity["embedding_artifact_sha256"] = metadata["embedding_artifact_sha256"]
        if resume and checkpoint_path.exists() and not force_rerun:
            checkpoint = load_fold_checkpoint(checkpoint_path, expected_identity=checkpoint_identity)
            if checkpoint["validation_case_ids"] != expected_case_ids:
                raise RuntimeError("Fold checkpoint validation case identity mismatch")
            for local, value in zip(val_idx, checkpoint["validation_predictions"]):
                oof_pred[int(local)] = value
            if task == "binary":
                probabilities = checkpoint.get("validation_probabilities")
                if probabilities is None:
                    raise RuntimeError("Binary fold checkpoint lacks probabilities")
                for local, value in zip(val_idx, probabilities):
                    oof_score[int(local)] = float(value)
            fold_results.append(checkpoint["result"])
            append_registry(registry, {**base_record, "status": "RESUMED_COMPLETED_FOLD", "ended_unix": time.time(), "result_artifact_identity": checkpoint["payload_sha256"]})
            print(json.dumps({"task": task, "family": family, "outer_fold": fold, "status": "RESUMED"}), flush=True)
            gc.collect()
            continue
        append_registry(registry, {**base_record, "status": "STARTED", "started_unix": time.time()})
        try:
            assert_inner_repo_disjoint(task_rows, train_idx, val_idx)
            train_rows = [task_rows[index] for index in train_idx]
            val_rows = [task_rows[index] for index in val_idx]
            train_labels = [labels[index] for index in train_idx]
            val_labels = [labels[index] for index in val_idx]
            if family == "M0":
                selected, threshold, inner_metrics = Candidate(1.0, None), (0.5 if task == "binary" else None), {"baseline": "most_frequent"}
            else:
                selected, threshold, inner_metrics = select_inner(
                    task,
                    family,
                    train_rows,
                    train_labels,
                    None if semantic is None else semantic[train_idx],
                    fold,
                    config,
                    progress=progress,
                    candidate_workers=candidate_workers,
                    heartbeat_seconds=heartbeat_seconds,
                    outer_started=outer_started,
                )
            metrics, pred, scores = fit_outer(
                task,
                family,
                train_rows,
                val_rows,
                train_labels,
                val_labels,
                None if semantic is None else semantic[train_idx],
                None if semantic is None else semantic[val_idx],
                selected,
                threshold,
                config,
                outer_fold=fold,
                progress=progress,
                heartbeat_seconds=heartbeat_seconds,
            )
            for local, value in zip(val_idx, pred):
                oof_pred[int(local)] = value
            if scores is not None:
                for local, value in zip(val_idx, scores):
                    oof_score[int(local)] = value
            result = {"task": task, "family": family, "outer_fold": fold, "train_rows": len(train_idx), "validation_rows": len(val_idx), "train_repositories": len({task_rows[index]["repository"] for index in train_idx}), "validation_repositories": len({task_rows[index]["repository"] for index in val_idx}), "selected_config": selected.payload(), "selected_threshold": threshold, "inner_selection_metrics": inner_metrics, "outer_metrics": metrics}
            fold_results.append(result)
            result_path = output_dir / f"{task}_{family}_fold{fold}.json"
            result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            checkpoint_started = time.monotonic()
            checkpoint = write_fold_checkpoint(checkpoint_path, {
                "status": "COMPLETE",
                **checkpoint_identity,
                "selected_config": selected.payload(),
                "selected_threshold": threshold,
                "validation_case_ids": expected_case_ids,
                "validation_predictions": pred,
                "validation_probabilities": scores,
                "result": result,
            })
            outer_fields = progress.record_outer_fold()
            emit(
                "[CHECKPOINT SAVED]",
                task=task,
                family=family,
                outer_fold=fold + 1,
                path=checkpoint_path,
                safe_resume_point=True,
                duration_seconds=round(time.monotonic() - checkpoint_started, 3),
                **outer_fields,
            )
            append_registry(registry, {**base_record, "status": "COMPLETED", "ended_unix": time.time(), "selected_config": selected.payload(), "selected_threshold": threshold, "result_artifact_identity": checkpoint["payload_sha256"]})
            print(json.dumps({"task": task, "family": family, "outer_fold": fold, "status": "COMPLETED"}), flush=True)
            del train_rows, val_rows, train_labels, val_labels, pred, scores
            gc.collect()
        except BaseException as exc:
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
    summary["oof_path"] = str(oof_path)
    summary["oof_sha256"] = sha256_file(oof_path)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def run(
    config_path: Path,
    output_dir: Path,
    families: list[str],
    embedding_dir: Path | None,
    *,
    resume: bool = False,
    force_rerun: bool = False,
    thread_limit: int | None = None,
    candidate_workers: int = 1,
    heartbeat_seconds: float = 60.0,
) -> list[dict[str, Any]]:
    config = load_config(config_path)
    if candidate_workers < 1:
        raise ValueError("candidate_workers must be at least 1")
    if heartbeat_seconds < 0:
        raise ValueError("heartbeat_seconds cannot be negative")
    for family in families:
        assert_registered_family(config, family)
    rows, metadata = load_development_rows(config_path=config_path)
    metadata["scientific_config_sha256"] = sha256_file(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    semantic = None
    if any(family in {"M2", "M3"} for family in families):
        if embedding_dir is None:
            raise RuntimeError("M2/M3 require --embedding-dir")
        embedding_manifest_path = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
        embedding_artifact_path = embedding_dir / "gate2_unixcoder_embeddings.npz"
        embedding_manifest = json.loads(embedding_manifest_path.read_text(encoding="utf-8"))
        emit("[HASH START]", artifact=embedding_artifact_path, purpose="pre_resume_embedding_identity")
        hash_started = time.monotonic()
        if sha256_file(embedding_artifact_path) != embedding_manifest.get("artifact_sha256"):
            raise RuntimeError("Embedding artifact hash mismatch before resume planning")
        emit("[HASH DONE]", artifact=embedding_artifact_path, duration_seconds=round(time.monotonic() - hash_started, 3))
        metadata["embedding_artifact_sha256"] = embedding_manifest["artifact_sha256"]
    total_outer, total_fits, recovered_outer, recovered_fits = resume_plan(
        rows=rows,
        families=families,
        output_dir=output_dir,
        config=config,
        metadata=metadata,
        resume=resume,
        force_rerun=force_rerun,
    )
    progress = ExecutionProgress(
        total_outer_folds=total_outer,
        total_candidate_fits=total_fits,
        recovered_outer_folds=recovered_outer,
        recovered_candidate_fits=recovered_fits,
    )
    if any(family in {"M2", "M3"} for family in families):
        assert embedding_dir is not None
        semantic = load_semantic(embedding_dir, rows, config, metadata["development_view_sha256"], artifact_already_verified=True)
    registry = output_dir / "GATE2_RUN_REGISTRY.jsonl"
    results = []
    with threadpool_limits(limits=thread_limit):
        for task in ("binary", "category"):
            fold_path = PROJECT_ROOT / f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv"
            for family in families:
                print(json.dumps({"task": task, "family": family, "status": "STARTING"}), flush=True)
                results.append(run_family(
                    task,
                    family,
                    rows,
                    semantic,
                    fold_path,
                    output_dir,
                    registry,
                    config,
                    metadata,
                    resume=resume,
                    force_rerun=force_rerun,
                    progress=progress,
                    candidate_workers=candidate_workers,
                    heartbeat_seconds=heartbeat_seconds,
                ))
                gc.collect()
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--embedding-dir")
    parser.add_argument("--families", nargs="+", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force-rerun", action="store_true")
    parser.add_argument("--thread-limit", type=int, help="Operational BLAS/OpenMP thread cap; does not change the registered models.")
    parser.add_argument("--candidate-workers", type=int, default=1, help="Execution-only parallel candidate fits sharing immutable fold matrices.")
    parser.add_argument("--heartbeat-seconds", type=float, default=60.0)
    args = parser.parse_args()
    results = run(
        Path(args.config),
        Path(args.output_dir),
        args.families,
        Path(args.embedding_dir) if args.embedding_dir else None,
        resume=args.resume,
        force_rerun=args.force_rerun,
        thread_limit=args.thread_limit,
        candidate_workers=args.candidate_workers,
        heartbeat_seconds=args.heartbeat_seconds,
    )
    print(json.dumps({"status": "COMPLETE", "summaries": [{"task": item["task"], "family": item["family"], "primary_mean": item["primary_mean"]} for item in results]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
