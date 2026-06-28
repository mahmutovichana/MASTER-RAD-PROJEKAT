from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from docguard_hf_classifier.dataset_export import HF_DATA_DIR, read_jsonl
from docguard_hf_classifier.label_maps import TASKS

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models" / "hf_v0_4"
REPORTS_DIR = ROOT / "reports"
INSTALL_COMMAND = "python -m pip install sentence-transformers scikit-learn joblib"
MODEL_PATH = MODELS_DIR / "embedding_classifier.joblib"
PREDICTION_PATH_TEMPLATE = "hf_embedding_predictions_v0_4_{split}.jsonl"


def require_embedding_dependencies(backend: str = "sentence_transformers") -> tuple[Any, Any, Any, Any]:
    try:
        import joblib
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import pairwise_distances
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing classifier dependency `{exc.name}`. Install with: {INSTALL_COMMAND}") from exc
    if backend == "sentence_transformers":
        try:
            from sentence_transformers import SentenceTransformer
        except ModuleNotFoundError as exc:
            raise RuntimeError(f"Missing embedding dependency `{exc.name}`. Install with: {INSTALL_COMMAND}") from exc
        return joblib, LogisticRegression, SentenceTransformer, pairwise_distances
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing transformers dependency `{exc.name}`. Install with: python -m pip install transformers torch scikit-learn joblib") from exc
    return joblib, LogisticRegression, (AutoTokenizer, AutoModel, torch), pairwise_distances


def encode_transformers(texts: list[str], model_name: str, bundle: tuple[Any, Any, Any]) -> list[list[float]]:
    AutoTokenizer, AutoModel, torch = bundle
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    vectors = []
    with torch.no_grad():
        for text in texts:
            batch = tokenizer(text, truncation=True, max_length=256, return_tensors="pt")
            output = model(**batch)
            mask = batch["attention_mask"].unsqueeze(-1)
            pooled = (output.last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
            vectors.append(pooled.squeeze(0).cpu().tolist())
    return vectors


def labels(rows: list[dict], task: str) -> list[str]:
    return [row[f"{task}_label"] for row in rows]


def train(version: str = "v0_4", model_name: str = "sentence-transformers/all-MiniLM-L6-v2", backend: str = "sentence_transformers") -> dict:
    if version != "v0_4":
        raise ValueError("Only v0_4 is supported.")
    joblib, LogisticRegression, encoder_factory, _pairwise = require_embedding_dependencies(backend)
    train_rows = read_jsonl(HF_DATA_DIR / "train.jsonl")
    texts = [row["input_text"] for row in train_rows]
    started = time.perf_counter()
    if backend == "sentence_transformers":
        encoder = encoder_factory(model_name)
        embeddings = encoder.encode(texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True)
        encoder_payload = {"backend": backend}
    else:
        embeddings = encode_transformers(texts, model_name, encoder_factory)
        encoder_payload = {"backend": backend}
    classifiers = {}
    for task in TASKS:
        task_rows = train_rows
        task_embeddings = embeddings
        if task == "target_doc_file":
            indices = [index for index, row in enumerate(train_rows) if row["docs_update_required_label"] == "true"]
            task_rows = [train_rows[index] for index in indices]
            task_embeddings = embeddings[indices] if hasattr(embeddings, "__getitem__") else [embeddings[index] for index in indices]
        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
        clf.fit(task_embeddings, labels(task_rows, task))
        classifiers[task] = clf
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": version,
        "model_name": model_name,
        "classifier_type": "LogisticRegression",
        "classifiers": classifiers,
        "encoder": encoder_payload,
        "train_seconds": time.perf_counter() - started,
    }
    joblib.dump(payload, MODEL_PATH)
    return {"model_path": str(MODEL_PATH), "model_name": model_name, "classifier_type": "LogisticRegression", "records": len(train_rows), "backend": backend}


def load_model() -> dict:
    try:
        import joblib
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing classifier dependency `{exc.name}`. Install with: {INSTALL_COMMAND}") from exc
    if not MODEL_PATH.exists():
        raise RuntimeError(f"HF embedding classifier not found at {MODEL_PATH}. Run `python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2`.")
    return joblib.load(MODEL_PATH)


def softmax(values: list[float]) -> list[float]:
    import math
    if not values:
        return []
    peak = max(values)
    exps = [math.exp(value - peak) for value in values]
    total = sum(exps) or 1.0
    return [value / total for value in exps]


def predict_with_classifier(clf: Any, vector: Any) -> tuple[str, float, list[dict]]:
    classes = [str(label) for label in clf.classes_]
    if hasattr(clf, "predict_proba"):
        probs = list(clf.predict_proba([vector])[0])
    elif hasattr(clf, "decision_function"):
        scores = clf.decision_function([vector])[0]
        if not isinstance(scores, list) and hasattr(scores, "tolist"):
            scores = scores.tolist()
        if isinstance(scores, (int, float)):
            scores = [-float(scores), float(scores)]
        probs = softmax([float(score) for score in scores])
    else:
        pred = str(clf.predict([vector])[0])
        return pred, 1.0, [{"label": pred, "score": 1.0}]
    ranked = sorted(zip(classes, probs), key=lambda item: item[1], reverse=True)
    return ranked[0][0], float(ranked[0][1]), [{"label": label, "score": float(score)} for label, score in ranked[:3]]


def encode_rows(rows: list[dict], model: dict) -> tuple[list[Any], float]:
    texts = [row["input_text"] for row in rows]
    started = time.perf_counter()
    model_name = model["model_name"]
    backend = model.get("encoder", {}).get("backend", "sentence_transformers")
    if backend == "sentence_transformers":
        try:
            from sentence_transformers import SentenceTransformer
        except ModuleNotFoundError as exc:
            raise RuntimeError(f"Missing embedding dependency `{exc.name}`. Install with: {INSTALL_COMMAND}") from exc
        encoder = SentenceTransformer(model_name)
        vectors = encoder.encode(texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True)
    else:
        _joblib, _LogisticRegression, encoder_bundle, _pairwise = require_embedding_dependencies("transformers")
        vectors = encode_transformers(texts, model_name, encoder_bundle)
    elapsed = time.perf_counter() - started
    return vectors, elapsed / len(rows) if rows else 0.0


def predict_rows(rows: list[dict], model: dict | None = None) -> tuple[list[dict], float]:
    model = model or load_model()
    vectors, latency = encode_rows(rows, model)
    predictions = []
    for row, vector in zip(rows, vectors):
        docs_label, docs_conf, docs_top = predict_with_classifier(model["classifiers"]["docs_update_required"], vector)
        docs_required = docs_label == "true"
        category, category_conf, category_top = predict_with_classifier(model["classifiers"]["doc_category"], vector)
        scenario, scenario_conf, scenario_top = predict_with_classifier(model["classifiers"]["scenario_type"], vector)
        if docs_required:
            target, target_conf, target_top = predict_with_classifier(model["classifiers"]["target_doc_file"], vector)
        else:
            target, target_conf, target_top = "", docs_conf, [{"label": "no_update", "score": docs_conf}]
            category = "no_update"
        predictions.append({
            "record_id": row["id"],
            "docs_update_required": docs_required,
            "doc_category": category,
            "target_doc_file": target,
            "scenario_type": scenario,
            "confidence": min(docs_conf, category_conf, scenario_conf, target_conf),
            "docs_update_required_confidence": docs_conf,
            "doc_category_confidence": category_conf,
            "target_doc_file_confidence": target_conf,
            "scenario_type_confidence": scenario_conf,
            "top3_doc_category": category_top,
            "top3_target_doc_file": target_top,
            "top3_scenario_type": scenario_top,
            "model_name": model["model_name"],
            "classifier_type": model["classifier_type"],
            "latency_seconds": latency,
        })
    return predictions, latency


def binary(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def compute_metrics(rows: list[dict], predictions: list[dict], latency: float, model: dict) -> dict:
    tp = fp = fn = tn = pos = cat = target = scenario = neg = neg_ok = 0
    per_scenario: dict[str, Counter] = defaultdict(Counter)
    per_category: dict[str, Counter] = defaultdict(Counter)
    for row, pred in zip(rows, predictions):
        gold = row["docs_update_required_label"] == "true"
        got = bool(pred["docs_update_required"])
        if gold and got: tp += 1
        elif not gold and got: fp += 1
        elif gold and not got: fn += 1
        else: tn += 1
        if gold:
            pos += 1
            cat += int(pred["doc_category"] == row["doc_category_label"])
            target += int(pred["target_doc_file"] == row["target_doc_file_label"])
            scenario += int(pred["scenario_type"] == row["scenario_type_label"])
        else:
            neg += 1
            neg_ok += int(not got and pred["doc_category"] == "no_update")
        per_scenario[row["scenario_type_label"]]["total"] += 1
        per_scenario[row["scenario_type_label"]]["correct"] += int(pred["scenario_type"] == row["scenario_type_label"])
        per_category[row["doc_category_label"]]["total"] += 1
        per_category[row["doc_category_label"]]["correct"] += int(pred["doc_category"] == row["doc_category_label"])
    p, r, f1 = binary(tp, fp, fn)
    return {
        "model_name": model["model_name"],
        "classifier_type": model["classifier_type"],
        "total_records": len(rows),
        "docs_update_required_precision": p,
        "docs_update_required_recall": r,
        "docs_update_required_f1": f1,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "positive_doc_category_accuracy": cat / pos if pos else 0.0,
        "positive_target_doc_file_accuracy": target / pos if pos else 0.0,
        "positive_scenario_type_accuracy": scenario / pos if pos else 0.0,
        "negative_classification_accuracy": neg_ok / neg if neg else 0.0,
        "macro_scenario_f1": sum(v["correct"] / v["total"] for v in per_scenario.values()) / len(per_scenario),
        "macro_doc_category_f1": sum(v["correct"] / v["total"] for v in per_category.values()) / len(per_category),
        "average_embedding_inference_latency_seconds": latency,
        "per_scenario": dict(per_scenario),
        "per_doc_category": dict(per_category),
    }


def write_report(path: Path, title: str, metrics: dict) -> None:
    lines = [f"# {title}", "", "| Metric | Value |", "| --- | ---: |"]
    for key, value in metrics.items():
        if key.startswith("per_"):
            continue
        lines.append(f"| `{key}` | {value:.4f} |" if isinstance(value, float) else f"| `{key}` | {value} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_predictions(split: str, predictions: list[dict]) -> None:
    path = ROOT / "data" / PREDICTION_PATH_TEMPLATE.format(split=split)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in predictions) + "\n", encoding="utf-8")


def evaluate(split: str = "validation") -> tuple[dict, list[dict]]:
    model = load_model()
    rows = read_jsonl(HF_DATA_DIR / f"{split}.jsonl")
    predictions, latency = predict_rows(rows, model)
    metrics = compute_metrics(rows, predictions, latency, model)
    REPORTS_DIR.mkdir(exist_ok=True)
    write_report(REPORTS_DIR / f"hf_embedding_evaluation_v0_4_{split}.md", f"HF Embedding Evaluation v0.4 {split}", metrics)
    write_predictions(split, predictions)
    return metrics, predictions


def load_predictions_by_id(split: str) -> dict[str, dict]:
    path = ROOT / "data" / PREDICTION_PATH_TEMPLATE.format(split=split)
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {row["record_id"]: row for row in rows}

