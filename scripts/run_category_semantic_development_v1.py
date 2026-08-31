from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import re
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import matplotlib
import numpy as np
from scipy import sparse
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from docguard_ml_v2.data_contract import CONTROLLED_DESIGN_LABEL_SOURCE, PRIMARY_STAGE2_LABELS


VERSION = "category_semantic_development_v1"
SEED = 42
LABELS = list(PRIMARY_STAGE2_LABELS)
SAFE_INPUT_FIELDS = {
    "code": ("language", "code_changed_files", "code_diff_excerpt"),
    "docs": ("docs_before_excerpt",),
}
FORBIDDEN_MODEL_FIELDS = {
    "repository",
    "pr_number",
    "gold_docs_update_required",
    "gold_doc_category",
    "human_docs_update_required",
    "human_doc_category",
    "human_label_notes",
    "suggested_docs_update_required",
    "suggested_doc_category",
    "suggested_notes",
    "label_source",
    "supervision_source",
    "provenance_tier",
    "case_origin",
    "controlled_design_supervision",
    "independent_human_reviewed",
    "owner_accepted_for_training",
    "review_status",
    "docs_after_excerpt",
    "docs_diff",
}
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
MODEL_LICENSE = "apache-2.0"
CHUNK_CHARS = 1_000
MAX_CHUNKS = 2
CLASSIFIER_FAMILIES = ("multinomial_logreg", "ovr_logreg", "calibrated_linear_svm")
REPRESENTATION_FAMILIES = ("semantic", "hybrid", "two_channel_lexical", "semantic_code_only")


def classifier_families_for(representation: str) -> tuple[str, ...]:
    if representation == "semantic_code_only":
        return ("multinomial_logreg", "ovr_logreg")
    return CLASSIFIER_FAMILIES


def reject_confirmation_path(path: Path) -> None:
    if "confirmation" in path.as_posix().lower():
        raise ValueError(f"Confirmation path is forbidden: {path}")


def reject_confirmation_row(row: dict[str, Any]) -> None:
    if str(row.get("partition") or "").lower() == "confirmation":
        raise ValueError(f"Confirmation row is forbidden: {row.get('case_id')}")


def load_development_jsonl(path: Path, expected_partition: str) -> list[dict[str, Any]]:
    reject_confirmation_path(path)
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            reject_confirmation_row(row)
            if row.get("partition") != expected_partition:
                raise ValueError(f"{path}:{line_number}: expected {expected_partition}, got {row.get('partition')}")
            rows.append(row)
    return rows


def sha256_path(path: Path) -> str:
    reject_confirmation_path(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_json_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_immutable_json(path: Path, payload: Any) -> None:
    """Create an immutable manifest, or prove a rerun matches it exactly."""
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != payload:
            raise ValueError(f"Immutable manifest mismatch: {path}")
        return
    write_json(path, payload)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def human_bytes(value: int) -> str:
    amount = float(value)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if amount < 1024 or unit == "GiB":
            return f"{amount:.2f} {unit}"
        amount /= 1024
    return f"{amount:.2f} GiB"


def directory_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [value] if value else []
    return []


def build_code_text(row: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"language: {str(row.get('language') or 'unknown').lower()}",
            "changed files:",
            "\n".join(list_value(row.get("code_changed_files"))),
            "code change:",
            str(row.get("code_diff_excerpt") or ""),
        ]
    )


def build_docs_text(row: dict[str, Any]) -> str:
    return str(row.get("docs_before_excerpt") or "")


def representation_field_audit() -> dict[str, Any]:
    used = set(SAFE_INPUT_FIELDS["code"]) | set(SAFE_INPUT_FIELDS["docs"])
    overlap = sorted(used & FORBIDDEN_MODEL_FIELDS)
    if overlap:
        raise ValueError(f"Forbidden model fields configured: {overlap}")
    return {
        "code_fields": list(SAFE_INPUT_FIELDS["code"]),
        "docs_fields": list(SAFE_INPUT_FIELDS["docs"]),
        "forbidden_fields_excluded": sorted(FORBIDDEN_MODEL_FIELDS),
        "repository_identity_excluded": "repository" not in used,
        "provenance_excluded": not bool(used & {"label_source", "supervision_source", "provenance_tier"}),
        "post_change_docs_excluded": not bool(used & {"docs_after_excerpt", "docs_diff"}),
    }


def is_primary_positive(row: dict[str, Any]) -> bool:
    return bool(row.get("gold_docs_update_required")) and str(row.get("gold_doc_category")) in LABELS


def is_controlled(row: dict[str, Any]) -> bool:
    return row.get("label_source") == CONTROLLED_DESIGN_LABEL_SOURCE or row.get("controlled_design_supervision") is True


def select_training_rows(rows: list[dict[str, Any]], controlled_enabled: bool) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if not is_primary_positive(row):
            continue
        controlled = is_controlled(row)
        if controlled and not controlled_enabled:
            continue
        if not controlled and row.get("independent_human_reviewed") is not True:
            continue
        selected.append(row)
    if not controlled_enabled and any(is_controlled(row) for row in selected):
        raise AssertionError("Controlled row entered natural-only scenario")
    if controlled_enabled and not any(is_controlled(row) for row in selected):
        raise AssertionError("Controlled-enabled scenario contains no controlled rows")
    return selected


def validate_validation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [row for row in rows if is_primary_positive(row)]
    if any(is_controlled(row) for row in selected):
        raise ValueError("Controlled rows are forbidden in natural development validation")
    return selected


def language_bucket(language: Any) -> str:
    value = str(language or "unknown").strip().lower()
    if value == "python":
        return "python"
    if value in {"typescript", "javascript", "tsx", "jsx"}:
        return "typescript_javascript"
    return "other"


def source_distribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {"row_count": len(rows), "categories": {}}
    for label in LABELS:
        subset = [row for row in rows if row.get("gold_doc_category") == label]
        result["categories"][label] = {
            "count": len(subset),
            "distinct_repository_count": len({str(row.get("repository")) for row in subset}),
            "language_counts": dict(sorted(Counter(language_bucket(row.get("language")) for row in subset).items())),
            "exact_language_counts": dict(sorted(Counter(str(row.get("language") or "unknown").lower() for row in subset).items())),
        }
    result["distinct_repository_count"] = len({str(row.get("repository")) for row in rows})
    result["language_counts"] = dict(sorted(Counter(language_bucket(row.get("language")) for row in rows).items()))
    result["exact_language_counts"] = dict(sorted(Counter(str(row.get("language") or "unknown").lower() for row in rows).items()))
    return result


def deterministic_chunks(text: str, chunk_chars: int = CHUNK_CHARS, max_chunks: int = MAX_CHUNKS) -> list[str]:
    normalized = re.sub(r"\x00", " ", str(text or "")).strip()
    if not normalized:
        return ["[empty]"]
    if len(normalized) <= chunk_chars:
        return [normalized]
    starts = np.linspace(0, max(0, len(normalized) - chunk_chars), num=max_chunks, dtype=int)
    return [normalized[int(start) : int(start) + chunk_chars] for start in starts]


def embedding_cache_key(model_name: str, revision: str, side: str, texts: list[str]) -> str:
    return stable_json_hash(
        {
            "model_name": model_name,
            "revision": revision,
            "side": side,
            "chunk_chars": CHUNK_CHARS,
            "max_chunks": MAX_CHUNKS,
            "content_hash": stable_json_hash(texts),
        }
    )


def encode_texts_cached(
    texts: list[str],
    *,
    side: str,
    model: Any,
    cache_dir: Path,
) -> tuple[np.ndarray, dict[str, Any]]:
    key = embedding_cache_key(MODEL_NAME, MODEL_REVISION, side, texts)
    target = cache_dir / f"{side}_{key}.npy"
    metadata = cache_dir / f"{side}_{key}.json"
    if target.exists() and metadata.exists():
        return np.load(target), json.loads(metadata.read_text(encoding="utf-8")) | {"cache_hit": True}

    cache_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    owners: list[int] = []
    for index, text in enumerate(texts):
        for chunk in deterministic_chunks(text):
            chunks.append(chunk)
            owners.append(index)
    started = time.perf_counter()
    chunk_vectors = model.encode(
        chunks,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
        device="cpu",
    ).astype(np.float32)
    output = np.zeros((len(texts), chunk_vectors.shape[1]), dtype=np.float32)
    counts = np.zeros(len(texts), dtype=np.float32)
    for owner, vector in zip(owners, chunk_vectors):
        output[owner] += vector
        counts[owner] += 1.0
    output /= np.maximum(counts[:, None], 1.0)
    norms = np.linalg.norm(output, axis=1, keepdims=True)
    output /= np.maximum(norms, 1e-12)
    np.save(target, output)
    payload = {
        "cache_key": key,
        "cache_hit": False,
        "model_name": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "side": side,
        "row_count": len(texts),
        "chunk_count": len(chunks),
        "embedding_dimension": int(output.shape[1]),
        "elapsed_seconds": time.perf_counter() - started,
        "content_hash": stable_json_hash(texts),
    }
    write_json(metadata, payload)
    return output, payload


def relational_semantic_features(code: np.ndarray, docs: np.ndarray) -> np.ndarray:
    if code.shape != docs.shape:
        raise ValueError(f"Embedding shape mismatch: {code.shape} vs {docs.shape}")
    cosine = np.sum(code * docs, axis=1, keepdims=True)
    return np.hstack([code, docs, np.abs(code - docs), code * docs, cosine]).astype(np.float32)


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def token_set(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def lexical_relational_scalars(rows: list[dict[str, Any]]) -> np.ndarray:
    values: list[list[float]] = []
    for row in rows:
        code_text = build_code_text(row)
        docs_text = build_docs_text(row)
        code_tokens = token_set(code_text)
        docs_tokens = token_set(docs_text)
        shared = code_tokens & docs_tokens
        union = code_tokens | docs_tokens
        identifiers = {token for token in code_tokens if "_" in token or any(char.isupper() for char in token)}
        path_tokens = token_set(" ".join(list_value(row.get("code_changed_files"))))
        values.append(
            [
                math.log1p(len(shared)),
                len(shared) / max(1, len(union)),
                len(shared) / max(1, min(len(code_tokens), len(docs_tokens))),
                len(identifiers & docs_tokens) / max(1, len(identifiers)),
                len(path_tokens & docs_tokens) / max(1, len(path_tokens)),
                math.log1p(len(code_text)),
                math.log1p(len(docs_text)),
            ]
        )
    return np.asarray(values, dtype=np.float32)


def labels_for(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.asarray([str(row["gold_doc_category"]) for row in rows])


def metric_bundle(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    normalized = matrix.astype(float) / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {
            label: {
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1": float(f1[index]),
                "support": int(support[index]),
            }
            for index, label in enumerate(LABELS)
        },
        "confusion_matrix": matrix.tolist(),
        "normalized_confusion_matrix": normalized.tolist(),
        "predicted_class_counts": dict(sorted(Counter(map(str, y_pred)).items())),
    }


def classifier(name: str) -> Any:
    if name == "multinomial_logreg":
        return LogisticRegression(C=1.0, solver="lbfgs", max_iter=2_000, random_state=SEED)
    if name == "ovr_logreg":
        return OneVsRestClassifier(LogisticRegression(C=1.0, solver="liblinear", max_iter=2_000, random_state=SEED))
    if name == "calibrated_linear_svm":
        return CalibratedClassifierCV(
            LinearSVC(C=1.0, random_state=SEED, max_iter=5_000, tol=1e-3), method="sigmoid", cv=3, n_jobs=1
        )
    raise ValueError(name)


def probabilities(model: Any, features: Any) -> np.ndarray:
    raw = np.asarray(model.predict_proba(features), dtype=float)
    classes = [str(value) for value in model.classes_]
    output = np.zeros((raw.shape[0], len(LABELS)), dtype=float)
    for source_index, label in enumerate(classes):
        output[:, LABELS.index(label)] = raw[:, source_index]
    return output


def fit_candidate(
    name: str,
    family: str,
    x_train: Any,
    y_train: np.ndarray,
    x_validation: Any,
    y_validation: np.ndarray,
    validation_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    started = time.perf_counter()
    model = classifier(family)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        model.fit(x_train, y_train)
    train_pred = model.predict(x_train)
    validation_pred = model.predict(x_validation)
    validation_prob = probabilities(model, x_validation)
    train_metrics = metric_bundle(y_train, train_pred)
    validation_metrics = metric_bundle(y_validation, validation_pred)
    payload = {
        "name": name,
        "classifier_family": family,
        "hyperparameters": {"C": 1.0, "class_weight": None, "resampling": None},
        "train": train_metrics,
        "validation": validation_metrics,
        "train_validation_macro_f1_gap": train_metrics["macro_f1"] - validation_metrics["macro_f1"],
        "fit_seconds": time.perf_counter() - started,
        "fit_warnings": [str(item.message) for item in caught],
        "selection_eligible": not bool(caught),
    }
    predictions: list[dict[str, Any]] = []
    for row, gold, predicted, scores in zip(validation_rows, y_validation, validation_pred, validation_prob):
        ranking = sorted(zip(LABELS, scores), key=lambda pair: float(pair[1]), reverse=True)
        predictions.append(
            {
                "case_id": row["case_id"],
                "gold": str(gold),
                "prediction": str(predicted),
                "correct": str(predicted) == str(gold),
                "confidence": float(ranking[0][1]),
                "top_2": [{"label": label, "probability": float(score)} for label, score in ranking[:2]],
                "probabilities": {label: float(scores[index]) for index, label in enumerate(LABELS)},
            }
        )
    return payload, predictions


def fit_vectorizers(
    train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    code_train = [build_code_text(row) for row in train_rows]
    code_validation = [build_code_text(row) for row in validation_rows]
    docs_train = [build_docs_text(row) for row in train_rows]
    docs_validation = [build_docs_text(row) for row in validation_rows]
    code_vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=20_000, sublinear_tf=True, dtype=np.float32
    )
    docs_vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=20_000, sublinear_tf=True, dtype=np.float32
    )
    code_train_matrix = code_vectorizer.fit_transform(code_train)
    code_validation_matrix = code_vectorizer.transform(code_validation)
    docs_train_matrix = docs_vectorizer.fit_transform(docs_train)
    docs_validation_matrix = docs_vectorizer.transform(docs_validation)
    train_scalars = sparse.csr_matrix(lexical_relational_scalars(train_rows))
    validation_scalars = sparse.csr_matrix(lexical_relational_scalars(validation_rows))
    return {
        "code_train": code_train_matrix,
        "code_validation": code_validation_matrix,
        "docs_train": docs_train_matrix,
        "docs_validation": docs_validation_matrix,
        "train_scalars": train_scalars,
        "validation_scalars": validation_scalars,
        "vocabulary_sizes": {
            "code": len(code_vectorizer.vocabulary_),
            "docs": len(docs_vectorizer.vocabulary_),
        },
    }


def bootstrap_delta(
    y_true: np.ndarray,
    baseline_pred: np.ndarray,
    candidate_pred: np.ndarray,
    *,
    iterations: int = 2_000,
) -> dict[str, Any]:
    rng = np.random.default_rng(SEED)
    macro: list[float] = []
    balanced: list[float] = []
    per_class: dict[str, list[float]] = {label: [] for label in LABELS}
    for _ in range(iterations):
        indices = rng.integers(0, len(y_true), len(y_true))
        gold = y_true[indices]
        base = baseline_pred[indices]
        candidate = candidate_pred[indices]
        macro.append(
            f1_score(gold, candidate, labels=LABELS, average="macro", zero_division=0)
            - f1_score(gold, base, labels=LABELS, average="macro", zero_division=0)
        )
        balanced.append(balanced_accuracy_score(gold, candidate) - balanced_accuracy_score(gold, base))
        base_f1 = precision_recall_fscore_support(gold, base, labels=LABELS, zero_division=0)[2]
        cand_f1 = precision_recall_fscore_support(gold, candidate, labels=LABELS, zero_division=0)[2]
        for index, label in enumerate(LABELS):
            per_class[label].append(float(cand_f1[index] - base_f1[index]))

    def summary(values: list[float]) -> dict[str, float]:
        array = np.asarray(values)
        return {
            "mean_delta": float(np.mean(array)),
            "ci_2_5": float(np.quantile(array, 0.025)),
            "ci_97_5": float(np.quantile(array, 0.975)),
            "probability_delta_gt_zero": float(np.mean(array > 0)),
        }

    return {
        "iterations": iterations,
        "seed": SEED,
        "paired_same_validation_cases": True,
        "macro_f1": summary(macro),
        "balanced_accuracy": summary(balanced),
        "per_class_f1": {label: summary(values) for label, values in per_class.items()},
        "developer_setup_uncertainty_warning": "developer_setup validation support is 19; its interval is necessarily wide and unstable.",
    }


def api_catchall(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    pairs = list(zip(map(str, y_true), map(str, y_pred)))
    return {
        "configuration_to_api_reference": sum(g == "configuration" and p == "api_reference" for g, p in pairs),
        "model_contract_to_api_reference": sum(g == "model_contract" and p == "api_reference" for g, p in pairs),
        "developer_setup_to_api_reference": sum(g == "developer_setup" and p == "api_reference" for g, p in pairs),
        "total_api_reference_false_positives": sum(g != "api_reference" and p == "api_reference" for g, p in pairs),
    }


def plot_outputs(output_dir: Path, results: list[dict[str, Any]], predictions: dict[str, list[dict[str, Any]]]) -> None:
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    ordered = sorted(results, key=lambda item: item["validation"]["macro_f1"], reverse=True)
    names = [item["name"] for item in ordered]

    plt.figure(figsize=(12, 7))
    plt.barh(names[::-1], [item["validation"]["macro_f1"] for item in ordered][::-1], color="#2f6f9f")
    plt.axvline(0.3817290905, color="#c44e52", linestyle="--", label="TF-IDF V8")
    plt.xlabel("Natural validation Macro-F1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures / "model_macro_f1_comparison.png", dpi=180)
    plt.close()

    top = ordered[:6]
    x = np.arange(len(LABELS))
    width = 0.8 / len(top)
    plt.figure(figsize=(12, 6))
    for index, item in enumerate(top):
        values = [item["validation"]["per_class"][label]["f1"] for label in LABELS]
        plt.bar(x + index * width, values, width, label=item["name"])
    plt.xticks(x + width * (len(top) - 1) / 2, LABELS, rotation=15)
    plt.ylabel("Natural validation F1")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(figures / "per_class_f1_comparison.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 7))
    y = np.arange(len(ordered))
    plt.scatter([item["train"]["macro_f1"] for item in ordered], y, label="train", marker="o")
    plt.scatter([item["validation"]["macro_f1"] for item in ordered], y, label="validation", marker="x")
    for idx, item in enumerate(ordered):
        plt.plot([item["validation"]["macro_f1"], item["train"]["macro_f1"]], [idx, idx], color="#999999")
    plt.yticks(y, names)
    plt.xlabel("Macro-F1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures / "train_validation_macro_f1_gap.png", dpi=180)
    plt.close()

    families = sorted({item["representation_family"] for item in results})
    deltas: list[float] = []
    labels: list[str] = []
    for family in families:
        natural = max(
            (
                item
                for item in results
                if item["representation_family"] == family
                and item["training_source"] == "natural_only"
                and item["selection_eligible"]
            ),
            key=lambda item: item["validation"]["macro_f1"],
        )
        augmented = next(
            item
            for item in results
            if item["representation_family"] == family
            and item["training_source"] == "natural_plus_controlled"
            and item["classifier_family"] == natural["classifier_family"]
        )
        labels.append(family)
        deltas.append(augmented["validation"]["macro_f1"] - natural["validation"]["macro_f1"])
    plt.figure(figsize=(8, 5))
    plt.bar(labels, deltas, color=["#55a868" if value >= 0 else "#c44e52" for value in deltas])
    plt.axhline(0, color="black", linewidth=0.8)
    plt.ylabel("Macro-F1 delta: controlled-enabled − natural-only")
    plt.tight_layout()
    plt.savefig(figures / "natural_vs_controlled_delta.png", dpi=180)
    plt.close()

    for family, filename in (("semantic", "best_semantic_normalized_confusion.png"), ("hybrid", "best_hybrid_normalized_confusion.png")):
        item = max(
            (
                candidate
                for candidate in results
                if candidate["representation_family"] == family and candidate["selection_eligible"]
            ),
            key=lambda value: value["validation"]["macro_f1"],
        )
        matrix = np.asarray(item["validation"]["normalized_confusion_matrix"])
        plt.figure(figsize=(7, 6))
        plt.imshow(matrix, vmin=0, vmax=1, cmap="Blues")
        plt.colorbar(label="Row-normalized proportion")
        plt.xticks(range(len(LABELS)), LABELS, rotation=25, ha="right")
        plt.yticks(range(len(LABELS)), LABELS)
        for i in range(len(LABELS)):
            for j in range(len(LABELS)):
                plt.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white" if matrix[i, j] > 0.5 else "black")
        plt.xlabel("Predicted")
        plt.ylabel("Gold")
        plt.title(item["name"])
        plt.tight_layout()
        plt.savefig(figures / filename, dpi=180)
        plt.close()


def baseline_predictions(path: Path, validation_ids: list[str]) -> dict[str, str]:
    reject_confirmation_path(path)
    mapping: dict[str, str] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            mapping[str(row["case_id"])] = str(row.get("predicted_category"))
    missing = sorted(set(validation_ids) - set(mapping))
    if missing:
        raise ValueError(f"Baseline predictions missing {len(missing)} validation IDs")
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Run development-only relational category experiments.")
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--baseline-predictions", type=Path, required=True)
    parser.add_argument("--baseline-config", type=Path, required=True)
    parser.add_argument("--baseline-model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--embedding-cache-dir", type=Path, required=True)
    parser.add_argument("--model-cache-dir", type=Path, required=True)
    args = parser.parse_args()

    for path in (args.train, args.validation, args.baseline_predictions, args.baseline_config, args.baseline_model):
        reject_confirmation_path(path)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    audit = representation_field_audit()

    train_all = load_development_jsonl(args.train, "development_train")
    validation_all = load_development_jsonl(args.validation, "development_validation")
    natural_train = select_training_rows(train_all, controlled_enabled=False)
    augmented_train = select_training_rows(train_all, controlled_enabled=True)
    controlled_train = [row for row in augmented_train if is_controlled(row)]
    validation_rows = validate_validation_rows(validation_all)
    validation_ids = [str(row["case_id"]) for row in validation_rows]
    y_validation = labels_for(validation_rows)
    baseline_map = baseline_predictions(args.baseline_predictions, validation_ids)
    baseline_pred = np.asarray([baseline_map[case_id] for case_id in validation_ids])
    baseline_metrics = metric_bundle(y_validation, baseline_pred)

    baseline_manifest = {
        "version": f"{VERSION}_immutable_baseline",
        "immutable": True,
        "confirmation_accessed": False,
        "train_case_ids": [str(row["case_id"]) for row in train_all],
        "validation_case_ids": [str(row["case_id"]) for row in validation_all],
        "category_validation_case_ids": validation_ids,
        "source_artifact_hashes": {
            str(args.train): sha256_path(args.train),
            str(args.validation): sha256_path(args.validation),
            str(args.baseline_predictions): sha256_path(args.baseline_predictions),
            str(args.baseline_config): sha256_path(args.baseline_config),
            str(args.baseline_model): sha256_path(args.baseline_model),
        },
        "config_hashes": {"baseline_category_v8": sha256_path(args.baseline_config)},
        "exact_provenance_counts": {
            "train_label_source": dict(sorted(Counter(str(row.get("label_source")) for row in train_all).items())),
            "train_supervision_source": dict(sorted(Counter(str(row.get("supervision_source")) for row in train_all).items())),
            "validation_label_source": dict(sorted(Counter(str(row.get("label_source")) for row in validation_all).items())),
            "validation_supervision_source": dict(sorted(Counter(str(row.get("supervision_source")) for row in validation_all).items())),
        },
        "exact_label_counts": {
            "train": dict(sorted(Counter(str(row.get("gold_doc_category")) for row in train_all).items())),
            "validation": dict(sorted(Counter(str(row.get("gold_doc_category")) for row in validation_all).items())),
            "category_train_natural": dict(sorted(Counter(str(row.get("gold_doc_category")) for row in natural_train).items())),
            "category_train_controlled": dict(sorted(Counter(str(row.get("gold_doc_category")) for row in controlled_train).items())),
            "category_validation": dict(sorted(Counter(str(row.get("gold_doc_category")) for row in validation_rows).items())),
        },
        "baseline_category_v8_metrics": baseline_metrics,
        "best_lexical_ablation": {
            "fields": ["code_changed_files", "code_diff_excerpt"],
            "validation_macro_f1": 0.387720216291645,
            "validation_balanced_accuracy": 0.406499066432793,
        },
    }
    write_immutable_json(output_dir / "baseline_manifest.json", baseline_manifest)

    manifest = {
        "version": VERSION,
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "confirmation_accessed": False,
        "immutable_baseline_manifest": "baseline_manifest.json",
        "immutable_baseline_hash": stable_json_hash(baseline_manifest),
        "safe_representation_audit": audit,
        "embedding": {
            "model_name": MODEL_NAME,
            "revision": MODEL_REVISION,
            "license": MODEL_LICENSE,
            "dimension": 384,
            "chunk_chars": CHUNK_CHARS,
            "max_chunks_per_side": MAX_CHUNKS,
        },
        "candidate_grid": {
            "representation_families": list(REPRESENTATION_FAMILIES),
            "training_sources": ["natural_only", "natural_plus_controlled"],
            "classifiers_by_representation": {
                representation: list(classifier_families_for(representation))
                for representation in REPRESENTATION_FAMILIES
            },
            "C": 1.0,
            "class_weight": None,
            "resampling": None,
        },
    }
    write_json(output_dir / "experiment_manifest.json", manifest)

    distribution = {
        "natural_training_primary_four": source_distribution(natural_train),
        "controlled_training_primary_four": source_distribution(controlled_train),
        "natural_validation_primary_four": source_distribution(validation_rows),
    }
    write_json(output_dir / "training_source_distribution.json", distribution)

    from sentence_transformers import SentenceTransformer

    model_download_before = directory_size(args.model_cache_dir)
    encoder = SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION, cache_folder=str(args.model_cache_dir), device="cpu")
    model_download_after = directory_size(args.model_cache_dir)
    combined_rows = augmented_train + validation_rows
    code_texts = [build_code_text(row) for row in combined_rows]
    docs_texts = [build_docs_text(row) for row in combined_rows]
    code_embeddings, code_cache = encode_texts_cached(code_texts, side="code", model=encoder, cache_dir=args.embedding_cache_dir)
    docs_embeddings, docs_cache = encode_texts_cached(docs_texts, side="docs", model=encoder, cache_dir=args.embedding_cache_dir)
    semantic_all = relational_semantic_features(code_embeddings, docs_embeddings)
    augmented_count = len(augmented_train)
    validation_semantic = semantic_all[augmented_count:]
    y_augmented = labels_for(augmented_train)
    natural_indices = np.asarray([index for index, row in enumerate(augmented_train) if not is_controlled(row)])
    y_natural = y_augmented[natural_indices]

    feature_sets: dict[tuple[str, str], tuple[Any, Any, np.ndarray, list[dict[str, Any]]]] = {}
    feature_sets[("semantic", "natural_only")] = (semantic_all[:augmented_count][natural_indices], validation_semantic, y_natural, natural_train)
    feature_sets[("semantic", "natural_plus_controlled")] = (semantic_all[:augmented_count], validation_semantic, y_augmented, augmented_train)
    feature_sets[("semantic_code_only", "natural_only")] = (code_embeddings[:augmented_count][natural_indices], code_embeddings[augmented_count:], y_natural, natural_train)
    feature_sets[("semantic_code_only", "natural_plus_controlled")] = (code_embeddings[:augmented_count], code_embeddings[augmented_count:], y_augmented, augmented_train)

    lexical_by_source: dict[str, dict[str, Any]] = {}
    for source_name, rows in (("natural_only", natural_train), ("natural_plus_controlled", augmented_train)):
        matrices = fit_vectorizers(rows, validation_rows)
        lexical_by_source[source_name] = matrices
        lexical_train = sparse.hstack(
            [matrices["code_train"], matrices["docs_train"], matrices["train_scalars"]], format="csr"
        )
        lexical_validation = sparse.hstack(
            [matrices["code_validation"], matrices["docs_validation"], matrices["validation_scalars"]], format="csr"
        )
        semantic_train = feature_sets[("semantic", source_name)][0]
        hybrid_train = sparse.hstack([matrices["code_train"], sparse.csr_matrix(semantic_train), matrices["train_scalars"]], format="csr")
        hybrid_validation = sparse.hstack([matrices["code_validation"], sparse.csr_matrix(validation_semantic), matrices["validation_scalars"]], format="csr")
        y_train = labels_for(rows)
        feature_sets[("two_channel_lexical", source_name)] = (lexical_train, lexical_validation, y_train, rows)
        feature_sets[("hybrid", source_name)] = (hybrid_train, hybrid_validation, y_train, rows)

    results: list[dict[str, Any]] = []
    prediction_sets: dict[str, list[dict[str, Any]]] = {}
    for representation in REPRESENTATION_FAMILIES:
        for source_name in ("natural_only", "natural_plus_controlled"):
            x_train, x_validation, y_train, _rows = feature_sets[(representation, source_name)]
            for family in classifier_families_for(representation):
                candidate_name = f"{representation}__{source_name}__{family}"
                print(f"Fitting {candidate_name}", flush=True)
                metrics, predictions = fit_candidate(
                    candidate_name, family, x_train, y_train, x_validation, y_validation, validation_rows
                )
                metrics["representation_family"] = representation
                metrics["training_source"] = source_name
                metrics["validation_case_ids_hash"] = stable_json_hash(validation_ids)
                results.append(metrics)
                prediction_sets[candidate_name] = predictions

    eligible_results = [item for item in results if item["selection_eligible"]]
    if not eligible_results:
        raise RuntimeError("No convergence-clean candidate is eligible for selection")
    ordered = sorted(results, key=lambda item: (item["selection_eligible"], item["validation"]["macro_f1"]), reverse=True)
    best_by_family = {
        family: max(
            (item for item in eligible_results if item["representation_family"] == family),
            key=lambda item: item["validation"]["macro_f1"],
        )["name"]
        for family in REPRESENTATION_FAMILIES
    }
    for item in results:
        item["api_catchall"] = api_catchall(
            y_validation, np.asarray([row["prediction"] for row in prediction_sets[item["name"]]])
        )
    model_comparison = {
        "primary_metric": "natural_development_validation_macro_f1",
        "baseline_category_v8": baseline_metrics,
        "best_lexical_ablation_macro_f1": 0.387720216291645,
        "best_candidate": ordered[0]["name"],
        "best_by_family": best_by_family,
        "candidates": ordered,
        "validation_membership_identical": len({item["validation_case_ids_hash"] for item in results}) == 1,
        "confirmation_accessed": False,
    }
    write_json(output_dir / "model_comparison.json", model_comparison)
    write_jsonl(output_dir / "validation_predictions.jsonl", (
        {"model": name, **row} for name, rows in prediction_sets.items() for row in rows
    ))

    baseline_dev_map = baseline_map
    developer_rows: list[dict[str, Any]] = []
    selected_comparison_models = [
        best_by_family["semantic"],
        max((item for item in eligible_results if item["representation_family"] == "semantic" and item["training_source"] == "natural_only"), key=lambda item: item["validation"]["macro_f1"])["name"],
        max((item for item in eligible_results if item["representation_family"] == "semantic" and item["training_source"] == "natural_plus_controlled"), key=lambda item: item["validation"]["macro_f1"])["name"],
        best_by_family["hybrid"],
    ]
    selected_comparison_models = list(dict.fromkeys(selected_comparison_models))
    pred_maps = {name: {row["case_id"]: row for row in prediction_sets[name]} for name in selected_comparison_models}
    for row in validation_rows:
        if row["gold_doc_category"] != "developer_setup":
            continue
        case_id = str(row["case_id"])
        item: dict[str, Any] = {
            "case_id": case_id,
            "gold": "developer_setup",
            "tfidf_v8_prediction": baseline_dev_map[case_id],
        }
        for model_name in selected_comparison_models:
            item[model_name] = pred_maps[model_name][case_id]
        developer_rows.append(item)
    write_json(output_dir / "developer_setup_comparison.json", {"support": 19, "models": selected_comparison_models, "cases": developer_rows})
    with (output_dir / "developer_setup_comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["case_id", "gold", "tfidf_v8_prediction"] + [f"{name}_prediction" for name in selected_comparison_models] + [f"{name}_confidence" for name in selected_comparison_models]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in developer_rows:
            flat = {"case_id": item["case_id"], "gold": item["gold"], "tfidf_v8_prediction": item["tfidf_v8_prediction"]}
            for name in selected_comparison_models:
                flat[f"{name}_prediction"] = item[name]["prediction"]
                flat[f"{name}_confidence"] = item[name]["confidence"]
            writer.writerow(flat)

    top_three = ordered[:3]
    api_payload = {
        "tfidf_v8": api_catchall(y_validation, baseline_pred),
        "best_three": {item["name"]: item["api_catchall"] for item in top_three},
    }
    write_json(output_dir / "api_catchall_comparison.json", api_payload)

    bootstrap_models = list(dict.fromkeys([ordered[0]["name"], best_by_family["semantic"], best_by_family["hybrid"], best_by_family["two_channel_lexical"]]))
    bootstrap_payload = {
        "baseline": "Category V8",
        "models": {
            name: bootstrap_delta(
                y_validation,
                baseline_pred,
                np.asarray([row["prediction"] for row in prediction_sets[name]]),
            )
            for name in bootstrap_models
        },
    }
    controlled_utility: dict[str, Any] = {}
    for representation in REPRESENTATION_FAMILIES:
        natural = max(
            (
                item
                for item in results
                if item["representation_family"] == representation
                and item["training_source"] == "natural_only"
                and item["selection_eligible"]
            ),
            key=lambda item: item["validation"]["macro_f1"],
        )
        augmented = next(
            item
            for item in results
            if item["representation_family"] == representation
            and item["training_source"] == "natural_plus_controlled"
            and item["classifier_family"] == natural["classifier_family"]
        )
        by_classifier: dict[str, Any] = {}
        for family in classifier_families_for(representation):
            natural_family = next(
                item for item in results
                if item["representation_family"] == representation
                and item["training_source"] == "natural_only"
                and item["classifier_family"] == family
            )
            augmented_family = next(
                item for item in results
                if item["representation_family"] == representation
                and item["training_source"] == "natural_plus_controlled"
                and item["classifier_family"] == family
            )
            natural_prediction = np.asarray([row["prediction"] for row in prediction_sets[natural_family["name"]]])
            augmented_prediction = np.asarray([row["prediction"] for row in prediction_sets[augmented_family["name"]]])
            by_classifier[family] = {
                "natural_model": natural_family["name"],
                "controlled_model": augmented_family["name"],
                "macro_f1_delta": augmented_family["validation"]["macro_f1"] - natural_family["validation"]["macro_f1"],
                "balanced_accuracy_delta": augmented_family["validation"]["balanced_accuracy"] - natural_family["validation"]["balanced_accuracy"],
                "per_class_f1_delta": {
                    label: augmented_family["validation"]["per_class"][label]["f1"] - natural_family["validation"]["per_class"][label]["f1"]
                    for label in LABELS
                },
                "paired_bootstrap_controlled_minus_natural": bootstrap_delta(
                    y_validation, natural_prediction, augmented_prediction
                ),
            }
        controlled_utility[representation] = {
            "comparison_policy": "hold_classifier_family_fixed_at_best_natural_only_family",
            "natural_model": natural["name"],
            "controlled_model": augmented["name"],
            "macro_f1_delta": augmented["validation"]["macro_f1"] - natural["validation"]["macro_f1"],
            "balanced_accuracy_delta": augmented["validation"]["balanced_accuracy"] - natural["validation"]["balanced_accuracy"],
            "per_class_f1_delta": {
                label: augmented["validation"]["per_class"][label]["f1"] - natural["validation"]["per_class"][label]["f1"]
                for label in LABELS
            },
            "by_classifier": by_classifier,
        }

    bootstrap_payload["controlled_vs_natural_same_classifier"] = {
        representation: payload["by_classifier"] for representation, payload in controlled_utility.items()
    }
    write_json(output_dir / "bootstrap_comparison.json", bootstrap_payload)
    plot_outputs(output_dir, results, prediction_sets)

    best = ordered[0]
    best_natural_only = max(
        (item for item in eligible_results if item["training_source"] == "natural_only"),
        key=lambda item: item["validation"]["macro_f1"],
    )
    best_predictions = np.asarray([row["prediction"] for row in prediction_sets[best["name"]]])
    semantic_best = next(item for item in results if item["name"] == best_by_family["semantic"])
    lexical_best = next(item for item in results if item["name"] == best_by_family["two_channel_lexical"])
    semantic_code_only_best = next(
        item
        for item in results
        if item["representation_family"] == "semantic_code_only"
        and item["training_source"] == "natural_only"
        and item["classifier_family"] == semantic_best["classifier_family"]
    )
    best_representation_utility = controlled_utility[best["representation_family"]]
    best_utility_pair = best_representation_utility["by_classifier"][best["classifier_family"]]
    controlled_bootstrap = best_utility_pair["paired_bootstrap_controlled_minus_natural"]
    controlled_recommended = (
        best_utility_pair["macro_f1_delta"] > 0
        and best_utility_pair["balanced_accuracy_delta"] > 0
        and controlled_bootstrap["macro_f1"]["ci_2_5"] > 0
    )
    recommendation = {
        "best_model": best["name"],
        "best_validation_macro_f1": best["validation"]["macro_f1"],
        "recommended_final_model_if_controlled_excluded": best_natural_only["name"],
        "recommended_final_model_macro_f1": best_natural_only["validation"]["macro_f1"],
        "recommended_final_model_balanced_accuracy": best_natural_only["validation"]["balanced_accuracy"],
        "semantic_better_than_tfidf_v8": semantic_best["validation"]["macro_f1"] > baseline_metrics["macro_f1"],
        "semantic_docs_relational_better_than_semantic_code_only": semantic_best["validation"]["macro_f1"] > semantic_code_only_best["validation"]["macro_f1"],
        "semantic_docs_relational_macro_f1_delta_vs_code_only": semantic_best["validation"]["macro_f1"] - semantic_code_only_best["validation"]["macro_f1"],
        "two_channel_better_than_concatenated_tfidf_v8": lexical_best["validation"]["macro_f1"] > baseline_metrics["macro_f1"],
        "controlled_utility": controlled_utility,
        "controlled_examples_recommended_for_final_training": controlled_recommended,
        "controlled_decision_rule": "retain only if matched-family Macro-F1 and balanced accuracy improve and paired-bootstrap Macro-F1 delta 95% CI excludes zero",
        "developer_setup_f1": best["validation"]["per_class"]["developer_setup"]["f1"],
        "api_catchall_best": api_catchall(y_validation, best_predictions),
        "remaining_problem": "combination_of_representation_natural_data_scarcity_and_domain_shift",
        "confirmation_accessed": False,
    }
    write_json(output_dir / "recommendation.json", recommendation)

    model_cache_size = directory_size(args.model_cache_dir)
    embedding_cache_size = directory_size(args.embedding_cache_dir)
    runtime = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "model_download_size_delta_bytes": model_download_after - model_download_before,
        "model_cache_size_bytes": model_cache_size,
        "embedding_cache_size_bytes": embedding_cache_size,
        "model_cache_size_human": human_bytes(model_cache_size),
        "embedding_cache_size_human": human_bytes(embedding_cache_size),
        "regenerable_and_safe_to_delete": [str(args.model_cache_dir), str(args.embedding_cache_dir)],
        "embedding_cache_entries": [code_cache, docs_cache],
    }
    write_json(output_dir / "runtime_and_disk.json", runtime)

    lines = [
        "# Category semantic development v1",
        "",
        "This development-only experiment compares relational semantic, hybrid, and two-channel lexical representations on the unchanged natural repository-disjoint validation set. Confirmation data was not accessed.",
        "",
        "## Best result",
        "",
        f"- Candidate: `{best['name']}`",
        f"- Natural validation Macro-F1: **{best['validation']['macro_f1']:.4f}**",
        f"- Balanced accuracy: **{best['validation']['balanced_accuracy']:.4f}**",
        f"- developer_setup F1: **{best['validation']['per_class']['developer_setup']['f1']:.4f}**",
        f"- Category V8 baseline Macro-F1: **{baseline_metrics['macro_f1']:.4f}**",
        f"- Recommended natural-only model: `{best_natural_only['name']}` (Macro-F1 **{best_natural_only['validation']['macro_f1']:.4f}**, balanced accuracy **{best_natural_only['validation']['balanced_accuracy']:.4f}**); augmented best is an experimental upper bound.",
        "",
        "## Controlled-data utility",
        "",
    ]
    for representation, payload in controlled_utility.items():
        lines.append(f"- `{representation}` Macro-F1 delta (controlled − natural): **{payload['macro_f1_delta']:+.4f}**")
    lines.extend(
        [
            "",
            "## Reproduction",
            "",
            "```powershell",
            "py scripts/run_category_semantic_development_v1.py --train experiments/consolidated_enriched_training_v2/gold/train.jsonl --validation experiments/consolidated_enriched_training_v2/gold/validation.jsonl --baseline-predictions reports/category_v8_development_diagnostics_v1/phases_1_5/category_v8_validation_error_analysis.jsonl --baseline-config configs/category_classifier_v8.json --baseline-model experiments/consolidated_enriched_training_v2/category_v8/category_v8.joblib --output-dir experiments/category_semantic_development_v1 --embedding-cache-dir data/external/embedding_cache/category_semantic_development_v1 --model-cache-dir data/external/embedding_cache/huggingface_models",
            "```",
            "",
            "Downloaded model and embedding matrices are regenerable, gitignored, and not part of the committed experiment artifacts.",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    table = [
        "# Model comparison",
        "",
        "| Candidate | Train source | Train Macro-F1 | Validation Macro-F1 | Balanced accuracy | developer_setup F1 | Gap |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in ordered:
        table.append(
            f"| `{item['name']}` | {item['training_source']} | {item['train']['macro_f1']:.4f} | {item['validation']['macro_f1']:.4f} | {item['validation']['balanced_accuracy']:.4f} | {item['validation']['per_class']['developer_setup']['f1']:.4f} | {item['train_validation_macro_f1_gap']:.4f} |"
        )
    (output_dir / "model_comparison.md").write_text("\n".join(table) + "\n", encoding="utf-8", newline="\n")

    final_report = [
        "# Phase 7 recommendation",
        "",
        "## Direct answers",
        "",
        f"1. Semantic better than TF-IDF V8: **{'yes' if recommendation['semantic_better_than_tfidf_v8'] else 'no'}**.",
        f"2. Two-channel lexical better than concatenated TF-IDF V8: **{'yes' if recommendation['two_channel_better_than_concatenated_tfidf_v8'] else 'no'}**.",
        f"3. Semantically represented docs_before improves over semantic code-only: **{'yes' if recommendation['semantic_docs_relational_better_than_semantic_code_only'] else 'no'}** (Macro-F1 delta **{recommendation['semantic_docs_relational_macro_f1_delta_vs_code_only']:+.4f}**).",
        f"4. Controlled-data deltas are reported in `recommendation.json`; they are retained only if natural-validation generalization improves.",
        f"5. Controlled examples recommended for final training: **{'yes' if recommendation['controlled_examples_recommended_for_final_training'] else 'no'}** under the predefined matched-family decision rule; recommended natural-only model: `{recommendation['recommended_final_model_if_controlled_excluded']}`.",
        f"6. Best developer_setup F1: **{best['validation']['per_class']['developer_setup']['f1']:.4f}**.",
        f"7. Best API false positives: **{recommendation['api_catchall_best']['total_api_reference_false_positives']}**, versus **{api_payload['tfidf_v8']['total_api_reference_false_positives']}** for TF-IDF V8.",
        "8. Remaining evidence indicates a combination of representation limitations, natural-data scarcity, and controlled-to-natural domain shift.",
        "9. Collect more natural positives only after model freeze review; prioritize categories with weak natural support and unstable F1.",
        "10. If acquisition resumes, prioritize natural developer_setup across more repositories, followed by model_contract and configuration repositories unlike the controlled templates.",
        "",
        "No confirmation evaluation, new acquisition, augmentation, or Stage 3 generation was performed.",
    ]
    (output_dir / "PHASE_7_RECOMMENDATION.md").write_text("\n".join(final_report) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"status": "ok", "best_model": best["name"], "best_macro_f1": best["validation"]["macro_f1"], "confirmation_accessed": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
