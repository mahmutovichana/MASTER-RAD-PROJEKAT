from __future__ import annotations

import hashlib
import json
import platform
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, f1_score
from sklearn.pipeline import Pipeline

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, category_eligible_rows, serialize_model_row
from docguard_ml_v2.features import SafeTextTransformer
from docguard_ml_v2.gate2_closure import EXPECTED, load_development_without_confirmation, load_fold_map, sha256_file
from docguard_ml_v2.metrics import binary_metrics, category_metrics


GATE2_COMMIT = "eb9448648f52b6d0156e8d905ba516c0e5b008e1"
SERIALIZER = "docguard_ml_v2.data_contract.serialize_model_row"
CLASSES = {"binary": [0, 1], "category": list(PRIMARY_STAGE2_LABELS)}


def vectorizer(config: dict[str, Any]) -> TfidfVectorizer:
    spec = config["families"]["M1"]
    return TfidfVectorizer(
        analyzer=spec["analyzer"], ngram_range=tuple(spec["ngram_range"]),
        min_df=int(spec["min_df"]), max_features=int(spec["max_features"]),
        sublinear_tf=bool(spec["sublinear_tf"]),
    )


def classifier(task: str, *, c_value: float, class_weight: str | None, config: dict[str, Any]) -> LogisticRegression:
    return LogisticRegression(
        C=c_value, class_weight=class_weight, max_iter=int(config["linear_classifier"]["max_iter"]),
        random_state=int(config["seed"]), solver=config["linear_classifier"]["binary_solver" if task == "binary" else "category_solver"],
    )


def threshold_metrics(y: list[int], scores: list[float], threshold: float) -> dict[str, Any]:
    pred = [int(value >= threshold) for value in scores]
    result = binary_metrics(y, pred, scores)
    result["macro_f1"] = float(f1_score(y, pred, average="macro", zero_division=0))
    result["brier_score"] = float(brier_score_loss(y, scores))
    return {"threshold": float(threshold), **result}


def choose_threshold(y: list[int], scores: list[float], grid: list[float]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sweep = [threshold_metrics(y, scores, float(threshold)) for threshold in grid]
    selected = max(sweep, key=lambda item: (item["mcc"], item["balanced_accuracy"], item["f1"], -abs(item["threshold"] - 0.5), -item["threshold"]))
    return selected, sweep


def candidate_key(c_value: float, class_weight: str | None) -> str:
    return f"C={c_value:g}|class_weight={'none' if class_weight is None else class_weight}"


def select_full_development(
    *, task: str, rows: list[dict[str, Any]], fold_map: dict[str, int], config: dict[str, Any], progress=print,
) -> dict[str, Any]:
    labels: list[Any] = [int(bool(row["gold_docs_update_required"])) for row in rows] if task == "binary" else [str(row["gold_doc_category"]) for row in rows]
    texts = [serialize_model_row(row) for row in rows]
    candidates = [(float(c), weight) for c in config["linear_classifier"]["C"] for weight in config["linear_classifier"]["class_weight"]]
    predictions: dict[str, list[Any]] = {candidate_key(*candidate): [None] * len(rows) for candidate in candidates}
    probabilities: dict[str, list[float]] = {candidate_key(*candidate): [float("nan")] * len(rows) for candidate in candidates}
    fold_audit = []
    for fold in range(5):
        val_idx = np.array([index for index, row in enumerate(rows) if fold_map[str(row["repository"]).strip().lower()] == fold])
        val_set = set(val_idx.tolist())
        train_idx = np.array([index for index in range(len(rows)) if index not in val_set])
        train_repos = {str(rows[index]["repository"]).strip().lower() for index in train_idx}
        val_repos = {str(rows[index]["repository"]).strip().lower() for index in val_idx}
        if train_repos & val_repos:
            raise RuntimeError("Gate 3 tuning repository leakage")
        vec = vectorizer(config)
        x_train = vec.fit_transform([texts[index] for index in train_idx])
        x_val = vec.transform([texts[index] for index in val_idx])
        progress(f"Gate 3 {task}: OOF fold {fold + 1}/5, train={len(train_idx)}, validation={len(val_idx)}, features={x_train.shape[1]}")
        for c_value, class_weight in candidates:
            key = candidate_key(c_value, class_weight)
            clf = classifier(task, c_value=c_value, class_weight=class_weight, config=config)
            clf.fit(x_train, [labels[index] for index in train_idx])
            pred = clf.predict(x_val).tolist()
            for index, value in zip(val_idx, pred): predictions[key][int(index)] = value.item() if hasattr(value, "item") else value
            if task == "binary":
                classes = list(clf.classes_); positive = classes.index(1)
                score = clf.predict_proba(x_val)[:, positive]
                for index, value in zip(val_idx, score): probabilities[key][int(index)] = float(value)
        fold_audit.append({"fold": fold, "train_rows": len(train_idx), "validation_rows": len(val_idx), "train_repositories": len(train_repos), "validation_repositories": len(val_repos), "repository_overlap": 0})
    ranked = []
    all_evidence = []
    for c_value, class_weight in candidates:
        key = candidate_key(c_value, class_weight)
        if any(value is None for value in predictions[key]): raise RuntimeError(f"Incomplete OOF predictions: {key}")
        if task == "binary":
            if any(not np.isfinite(value) for value in probabilities[key]): raise RuntimeError(f"Incomplete OOF probabilities: {key}")
            selected_threshold, sweep = choose_threshold([int(value) for value in labels], probabilities[key], config["tasks"]["binary"]["threshold_grid"])
            rank = (selected_threshold["mcc"], selected_threshold["balanced_accuracy"], selected_threshold["f1"], -abs(selected_threshold["threshold"] - 0.5), -c_value, str(class_weight), -1.0)
            metrics = selected_threshold
            evidence = {"candidate": {"C": c_value, "class_weight": class_weight}, "selected_threshold": selected_threshold["threshold"], "selected_metrics": selected_threshold, "threshold_sweep": sweep}
        else:
            metrics = category_metrics([str(value) for value in labels], [str(value) for value in predictions[key]], PRIMARY_STAGE2_LABELS)
            rank = (metrics["macro_f1"], metrics["weighted_f1"], metrics["accuracy"], -c_value, str(class_weight), -1.0)
            evidence = {"candidate": {"C": c_value, "class_weight": class_weight}, "selected_metrics": metrics}
        ranked.append((rank, key, evidence)); all_evidence.append(evidence)
    _, selected_key, selected = max(ranked, key=lambda item: item[0])
    return {
        "schema_version": "gate3_full_development_oof_selection_v1", "task": task,
        "purpose": "freeze-time hyperparameter and threshold selection only; not an additional evaluation estimate",
        "method": "Five-fold repository-grouped OOF predictions over the immutable Gate 2 outer-fold assignment, using only the preregistered M1 C/class_weight and threshold grids.",
        "row_count": len(rows), "repository_count": len(set(fold_map)), "fold_assignment_sha256": EXPECTED[f"{task}_fold_sha256"],
        "seed": int(config["seed"]), "confirmation_accessed": False, "fold_audit": fold_audit,
        "candidate_grid": [{"C": c, "class_weight": w} for c, w in candidates], "candidate_results": all_evidence,
        "ranking_rule": config["tasks"]["binary"]["threshold_tie_break"] + "_then_lower_C_then_class_weight_string" if task == "binary" else "highest_macro_f1_then_weighted_f1_then_accuracy_then_lower_C_then_class_weight_string",
        "selected_candidate_key": selected_key, "selected": selected,
    }


def build_pipeline(task: str, selection: dict[str, Any], config: dict[str, Any]) -> Pipeline:
    selected = selection["selected"]["candidate"]
    return Pipeline([
        ("safe_text", SafeTextTransformer()), ("tfidf", vectorizer(config)),
        ("classifier", classifier(task, c_value=float(selected["C"]), class_weight=selected["class_weight"], config=config)),
    ])


def fit_and_check(task: str, rows: list[dict[str, Any]], selection: dict[str, Any], config: dict[str, Any]) -> tuple[Pipeline, dict[str, Any]]:
    labels = [int(bool(row["gold_docs_update_required"])) for row in rows] if task == "binary" else [str(row["gold_doc_category"]) for row in rows]
    first = build_pipeline(task, selection, config); first.fit(rows, labels)
    second = build_pipeline(task, selection, config); second.fit(rows, labels)
    sample_indexes = np.linspace(0, len(rows) - 1, num=min(128, len(rows)), dtype=int)
    sample = [rows[int(index)] for index in sample_indexes]
    pred_equal = np.array_equal(first.predict(sample), second.predict(sample))
    proba_equal = np.allclose(first.predict_proba(sample), second.predict_proba(sample), rtol=0.0, atol=1e-12)
    vec_equal = np.array_equal(first.named_steps["tfidf"].get_feature_names_out(), second.named_steps["tfidf"].get_feature_names_out())
    coef_equal = np.allclose(first.named_steps["classifier"].coef_, second.named_steps["classifier"].coef_, rtol=0.0, atol=1e-12)
    audit = {"standard": "prediction/numerical equivalence; byte identity not required for joblib serialization", "sample_rows": len(sample), "predictions_exact": bool(pred_equal), "probabilities_atol_1e-12": bool(proba_equal), "vocabulary_exact": bool(vec_equal), "coefficients_atol_1e-12": bool(coef_equal), "status": "PASS" if pred_equal and proba_equal and vec_equal and coef_equal else "FAIL"}
    if audit["status"] != "PASS": raise RuntimeError(f"{task} deterministic rebuild check failed")
    return first, audit


def model_payload(task: str, model: Pipeline, selection: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "docguard_final_v2_gate3_classifier_v1", "task": task, "family": "M1",
        "model": model, "threshold": selection["selected"].get("selected_threshold") if task == "binary" else None,
        "classes": CLASSES[task], "safe_fields": list(SAFE_MODEL_FIELDS), "serializer": SERIALIZER,
        "confirmation_accessed": False,
    }


def environment_metadata() -> dict[str, Any]:
    return {"python": platform.python_version(), "sklearn": sklearn.__version__, "numpy": np.__version__, "joblib": joblib.__version__}
