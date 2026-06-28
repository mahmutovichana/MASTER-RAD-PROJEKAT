from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from docguard_hf_classifier.dataset_export import HF_DATA_DIR, mode_dir, read_jsonl
from docguard_hf_classifier.label_maps import TASKS
from docguard_hf_classifier.text_builder import DEFAULT_INPUT_MODE, INPUT_MODES

ROOT = Path(__file__).resolve().parents[1]
BUNDLED_PYTHON_PACKAGES = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python"
if BUNDLED_PYTHON_PACKAGES.exists():
    sys.path.insert(0, str(BUNDLED_PYTHON_PACKAGES))
MODELS_DIR = ROOT / "models" / "hf_v0_4"
REPORTS_DIR = ROOT / "reports"
INSTALL_COMMAND = "python -m pip install sentence-transformers scikit-learn joblib"
PREDICTION_PATH_TEMPLATE = "hf_embedding_predictions_v0_4_{input_mode}_{split}.jsonl"
NEGATIVE_REASON_GROUPS = {
    "no_behavior_change_refactor": {
        "internal_variable_rename_no_behavior_change",
        "private_helper_refactor_no_flow_change",
        "helper_extraction_no_behavior_change",
        "internal_performance_refactor_no_documented_behavior_change",
        "type_alias_rename_no_contract_change",
    },
    "no_contract_change_textual": {
        "formatting_only_in_docs_or_code",
        "comments_reworded_no_contract_change",
        "log_message_change_no_user_visible_behavior",
    },
    "test_only_no_product_behavior": {"test_assertion_refactor_no_behavior_change"},
    "dependency_or_config_no_doc_impact": {
        "dev_dependency_patch_no_command_change",
        "config_refactor_no_new_env_var",
    },
    "docs_already_consistent": {"docs_already_updated"},
    "route_internal_no_contract_change": {"route_implementation_refactor_no_contract_change"},
}
NEGATIVE_SCENARIO_TO_GROUP = {
    scenario: group
    for group, scenarios in NEGATIVE_REASON_GROUPS.items()
    for scenario in scenarios
}


def architecture_suffix(classifier_architecture: str = "flat") -> str:
    return "" if classifier_architecture == "flat" else f"_{classifier_architecture}"


def model_path(input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> Path:
    return MODELS_DIR / input_mode / f"embedding_classifier{architecture_suffix(classifier_architecture)}.joblib"


def legacy_prediction_path(split: str) -> Path:
    return ROOT / "data" / f"hf_embedding_predictions_v0_4_{split}.jsonl"


def prediction_path(split: str, input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> Path:
    suffix = architecture_suffix(classifier_architecture)
    return ROOT / "data" / f"hf_embedding_predictions_v0_4_{input_mode}_{split}{suffix}.jsonl"


def negative_reason_group(scenario_type: str) -> str:
    return NEGATIVE_SCENARIO_TO_GROUP.get(scenario_type, "other_negative")


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


def train(version: str = "v0_4", model_name: str = "sentence-transformers/all-MiniLM-L6-v2", backend: str = "sentence_transformers", input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> dict:
    if version != "v0_4":
        raise ValueError("Only v0_4 is supported.")
    joblib, LogisticRegression, encoder_factory, _pairwise = require_embedding_dependencies(backend)
    if input_mode not in INPUT_MODES:
        raise ValueError(f"Unsupported input mode: {input_mode}")
    train_rows = read_jsonl(mode_dir(input_mode) / "train.jsonl")
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

    def slice_embeddings(indices: list[int]):
        return embeddings[indices] if hasattr(embeddings, "shape") else [embeddings[index] for index in indices]

    def fit_classifier(name: str, indices: list[int], y: list[str]) -> None:
        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
        clf.fit(slice_embeddings(indices), y)
        classifiers[name] = clf

    all_indices = list(range(len(train_rows)))
    positive_indices = [index for index, row in enumerate(train_rows) if row["docs_update_required_label"] == "true"]
    negative_indices = [index for index, row in enumerate(train_rows) if row["docs_update_required_label"] == "false"]
    if classifier_architecture == "staged":
        fit_classifier("docs_update_required", all_indices, labels(train_rows, "docs_update_required"))
        positive_rows = [train_rows[index] for index in positive_indices]
        negative_rows = [train_rows[index] for index in negative_indices]
        fit_classifier("positive_doc_category", positive_indices, labels(positive_rows, "doc_category"))
        fit_classifier("positive_target_doc_file", positive_indices, labels(positive_rows, "target_doc_file"))
        fit_classifier("positive_scenario_type", positive_indices, labels(positive_rows, "scenario_type"))
        fit_classifier("negative_reason_group", negative_indices, [negative_reason_group(row["scenario_type_label"]) for row in negative_rows])
        fit_classifier("negative_scenario_type", negative_indices, labels(negative_rows, "scenario_type"))
    else:
        for task in TASKS:
            task_indices = positive_indices if task == "target_doc_file" else all_indices
            task_rows = [train_rows[index] for index in task_indices]
            fit_classifier(task, task_indices, labels(task_rows, task))
    path = model_path(input_mode, classifier_architecture)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": version,
        "input_mode": input_mode,
        "classifier_architecture": classifier_architecture,
        "model_name": model_name,
        "classifier_type": "LogisticRegression",
        "classifiers": classifiers,
        "encoder": encoder_payload,
        "train_seconds": time.perf_counter() - started,
    }
    joblib.dump(payload, path)
    return {"model_path": str(path), "input_mode": input_mode, "classifier_architecture": classifier_architecture, "model_name": model_name, "classifier_type": "LogisticRegression", "records": len(train_rows), "backend": backend}


def load_model(input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> dict:
    try:
        import joblib
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"Missing classifier dependency `{exc.name}`. Install with: {INSTALL_COMMAND}") from exc
    path = model_path(input_mode, classifier_architecture)
    if not path.exists():
        raise RuntimeError(f"HF embedding classifier not found at {path}. Run `python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode {input_mode}`.")
    return joblib.load(path)


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
    architecture = model.get("classifier_architecture", "flat")
    for row, vector in zip(rows, vectors):
        docs_label, docs_conf, docs_top = predict_with_classifier(model["classifiers"]["docs_update_required"], vector)
        docs_required = docs_label == "true"
        if architecture == "staged" and docs_required:
            category, category_conf, category_top = predict_with_classifier(model["classifiers"]["positive_doc_category"], vector)
            scenario, scenario_conf, scenario_top = predict_with_classifier(model["classifiers"]["positive_scenario_type"], vector)
            target, target_conf, target_top = predict_with_classifier(model["classifiers"]["positive_target_doc_file"], vector)
            group, group_conf, group_top = "", 1.0, []
        elif architecture == "staged":
            scenario, scenario_conf, scenario_top = predict_with_classifier(model["classifiers"]["negative_scenario_type"], vector)
            group, group_conf, group_top = predict_with_classifier(model["classifiers"]["negative_reason_group"], vector)
            target, target_conf, target_top = "", docs_conf, [{"label": "no_update", "score": docs_conf}]
            category, category_conf, category_top = "no_update", docs_conf, [{"label": "no_update", "score": docs_conf}]
        elif docs_required:
            category, category_conf, category_top = predict_with_classifier(model["classifiers"]["doc_category"], vector)
            scenario, scenario_conf, scenario_top = predict_with_classifier(model["classifiers"]["scenario_type"], vector)
            target, target_conf, target_top = predict_with_classifier(model["classifiers"]["target_doc_file"], vector)
            group, group_conf, group_top = "", 1.0, []
        else:
            category, category_conf, category_top = predict_with_classifier(model["classifiers"]["doc_category"], vector)
            scenario, scenario_conf, scenario_top = predict_with_classifier(model["classifiers"]["scenario_type"], vector)
            target, target_conf, target_top = "", docs_conf, [{"label": "no_update", "score": docs_conf}]
            category = "no_update"
            group, group_conf, group_top = negative_reason_group(scenario), scenario_conf, []
        predictions.append({
            "record_id": row["id"],
            "docs_update_required": docs_required,
            "doc_category": category,
            "target_doc_file": target,
            "scenario_type": scenario,
            "negative_reason_group": group,
            "confidence": min(docs_conf, category_conf, scenario_conf, target_conf),
            "docs_update_required_confidence": docs_conf,
            "doc_category_confidence": category_conf,
            "target_doc_file_confidence": target_conf,
            "scenario_type_confidence": scenario_conf,
            "top3_doc_category": category_top,
            "top3_target_doc_file": target_top,
            "top3_scenario_type": scenario_top,
            "top3_negative_reason_group": group_top,
            "model_name": model["model_name"],
            "classifier_type": model["classifier_type"],
            "classifier_architecture": architecture,
            "latency_seconds": latency,
        })
    return predictions, latency


def binary(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def compute_metrics(rows: list[dict], predictions: list[dict], latency: float, model: dict) -> dict:
    tp = fp = fn = tn = pos = cat = target = pos_scenario = neg = neg_ok = neg_scenario = neg_group = overall_scenario = 0
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
            pos_scenario += int(pred["scenario_type"] == row["scenario_type_label"])
        else:
            neg += 1
            neg_ok += int(not got and pred["doc_category"] == "no_update")
            neg_scenario += int(pred["scenario_type"] == row["scenario_type_label"])
            neg_group += int(negative_reason_group(pred["scenario_type"]) == negative_reason_group(row["scenario_type_label"]))
        overall_scenario += int(pred["scenario_type"] == row["scenario_type_label"])
        per_scenario[row["scenario_type_label"]]["total"] += 1
        per_scenario[row["scenario_type_label"]]["correct"] += int(pred["scenario_type"] == row["scenario_type_label"])
        per_category[row["doc_category_label"]]["total"] += 1
        per_category[row["doc_category_label"]]["correct"] += int(pred["doc_category"] == row["doc_category_label"])
    p, r, f1 = binary(tp, fp, fn)
    return {
        "model_name": model["model_name"],
        "input_mode": model.get("input_mode", DEFAULT_INPUT_MODE),
        "classifier_architecture": model.get("classifier_architecture", "flat"),
        "classifier_type": model["classifier_type"],
        "total_records": len(rows),
        "docs_update_required_precision": p,
        "docs_update_required_recall": r,
        "docs_update_required_f1": f1,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "positive_doc_category_accuracy": cat / pos if pos else 0.0,
        "positive_target_doc_file_accuracy": target / pos if pos else 0.0,
        "overall_scenario_type_accuracy": overall_scenario / len(rows) if rows else 0.0,
        "positive_scenario_type_accuracy": pos_scenario / pos if pos else 0.0,
        "negative_scenario_type_accuracy": neg_scenario / neg if neg else 0.0,
        "negative_reason_group_accuracy": neg_group / neg if neg else 0.0,
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


def write_predictions(split: str, predictions: list[dict], input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> None:
    path = prediction_path(split, input_mode, classifier_architecture)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in predictions) + "\n", encoding="utf-8")
    if input_mode == "full_current":
        legacy_prediction_path(split).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def report_name(split: str, input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> str:
    suffix = architecture_suffix(classifier_architecture)
    return f"hf_embedding_evaluation_v0_4_{input_mode}_{split}{suffix}.md"


def evaluate(split: str = "validation", input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> tuple[dict, list[dict]]:
    model = load_model(input_mode, classifier_architecture)
    rows = read_jsonl(mode_dir(input_mode) / f"{split}.jsonl")
    predictions, latency = predict_rows(rows, model)
    metrics = compute_metrics(rows, predictions, latency, model)
    REPORTS_DIR.mkdir(exist_ok=True)
    write_report(REPORTS_DIR / report_name(split, input_mode, classifier_architecture), f"HF Embedding Evaluation v0.4 {input_mode} {split} {classifier_architecture}", metrics)
    if input_mode == "full_current" and classifier_architecture == "flat":
        write_report(REPORTS_DIR / f"hf_embedding_evaluation_v0_4_{split}.md", f"HF Embedding Evaluation v0.4 {split}", metrics)
    write_predictions(split, predictions, input_mode, classifier_architecture)
    return metrics, predictions


def load_predictions_by_id(split: str, input_mode: str = DEFAULT_INPUT_MODE, classifier_architecture: str = "flat") -> dict[str, dict]:
    path = prediction_path(split, input_mode, classifier_architecture)
    if not path.exists() and input_mode == "full_current":
        path = legacy_prediction_path(split)
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {row["record_id"]: row for row in rows}
