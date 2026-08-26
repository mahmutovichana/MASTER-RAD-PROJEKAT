from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
    roc_auc_score,
)

from docguard_ml_v2.data_contract import language_bucket


def binary_metrics(y_true: list[int], y_pred: list[int], scores: list[float] | None = None) -> dict[str, Any]:
    labels = [0, 1]
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    tn, fp, fn, tp = [int(value) for value in cm.ravel()]
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "specificity": float(specificity),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "roc_auc": None,
        "average_precision": None,
        "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "natural_prevalence": float(sum(y_true) / len(y_true)) if y_true else 0.0,
        "support": len(y_true),
        "gold_counts": dict(Counter(str(item) for item in y_true)),
        "pred_counts": dict(Counter(str(item) for item in y_pred)),
    }
    if scores is not None and len(set(y_true)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_true, scores))
        metrics["average_precision"] = float(average_precision_score(y_true, scores))
    return metrics


def category_metrics(y_true: list[str], y_pred: list[str], labels: list[str]) -> dict[str, Any]:
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)) if y_true else 0.0,
        "per_class": {
            label: {"precision": float(p), "recall": float(r), "f1": float(f), "support": int(s)}
            for label, p, r, f, s in zip(labels, precision, recall, f1, support)
        },
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).astype(int).tolist(),
        "support": len(y_true),
        "gold_counts": dict(Counter(y_true)),
        "pred_counts": dict(Counter(y_pred)),
    }


def per_language_binary_metrics(rows: list[dict[str, Any]], y_true: list[int], y_pred: list[int], scores: list[float] | None = None, min_support: int = 2) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for bucket in ["python", "typescript", "other"]:
        indexes = [idx for idx, row in enumerate(rows) if language_bucket(row) == bucket]
        if len(indexes) < min_support:
            output[bucket] = {"support": len(indexes), "reported": False}
            continue
        bucket_scores = None if scores is None else [scores[idx] for idx in indexes]
        output[bucket] = {"reported": True, **binary_metrics([y_true[idx] for idx in indexes], [y_pred[idx] for idx in indexes], bucket_scores)}
    return output


def per_language_category_metrics(rows: list[dict[str, Any]], y_true: list[str], y_pred: list[str], labels: list[str], min_support: int = 2) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for bucket in ["python", "typescript", "other"]:
        indexes = [idx for idx, row in enumerate(rows) if language_bucket(row) == bucket]
        if len(indexes) < min_support:
            output[bucket] = {"support": len(indexes), "reported": False}
            continue
        output[bucket] = {"reported": True, **category_metrics([y_true[idx] for idx in indexes], [y_pred[idx] for idx in indexes], labels)}
    return output


def majority_binary_baseline(y_true: list[int]) -> dict[str, Any]:
    majority = Counter(y_true).most_common(1)[0][0] if y_true else 0
    return {"majority_label": int(majority), "metrics": binary_metrics(y_true, [majority] * len(y_true))}


def majority_category_baseline(y_true: list[str], labels: list[str]) -> dict[str, Any]:
    majority = Counter(y_true).most_common(1)[0][0] if y_true else labels[0]
    return {"majority_label": majority, "metrics": category_metrics(y_true, [majority] * len(y_true), labels)}


def bootstrap_ci(metric_fn, y_true: list[Any], y_pred_or_score: list[Any], *, seed: int = 42, n_bootstrap: int = 200, alpha: float = 0.05) -> dict[str, float]:
    if not y_true:
        return {"low": 0.0, "high": 0.0}
    rng = np.random.default_rng(seed)
    values: list[float] = []
    n = len(y_true)
    for _ in range(n_bootstrap):
        indexes = rng.integers(0, n, size=n)
        try:
            values.append(float(metric_fn([y_true[i] for i in indexes], [y_pred_or_score[i] for i in indexes])))
        except Exception:
            continue
    if not values:
        return {"low": 0.0, "high": 0.0}
    return {"low": float(np.quantile(values, alpha / 2)), "high": float(np.quantile(values, 1 - alpha / 2))}

