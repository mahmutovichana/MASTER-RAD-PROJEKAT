from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.svm import LinearSVC

from docguard_external.evaluate_existing_docguard import pct
from docguard_external.train_binary_classifier_v2 import labels, metric_values, subset, text_for_mode


ENCODERS = ["microsoft/unixcoder-base", "microsoft/codebert-base", "microsoft/graphcodebert-base"]
INPUT_MODES = ["old_comment_plus_code_diff", "code_diff_only"]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def cache_key(encoder_name: str, mode: str, path: Path, rows: list[dict[str, Any]]) -> str:
    payload = {
        "encoder": encoder_name,
        "mode": mode,
        "path": str(path),
        "records": len(rows),
        "first": rows[0].get("record_id") if rows else None,
        "last": rows[-1].get("record_id") if rows else None,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def mean_pool(last_hidden_state: Any, attention_mask: Any) -> Any:
    import torch

    mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    summed = torch.sum(last_hidden_state * mask, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9)
    return summed / counts


def load_encoder(name: str, device: str) -> tuple[Any, Any]:
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModel.from_pretrained(name)
    model.to(device)
    model.eval()
    return tokenizer, model


def embeddings_for_rows(
    rows: list[dict[str, Any]],
    source_path: Path,
    encoder_name: str,
    mode: str,
    cache_dir: Path,
    batch_size: int,
    device: str,
) -> np.ndarray:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{cache_key(encoder_name, mode, source_path, rows)}.npy"
    if cache_path.exists():
        return np.load(cache_path)
    import torch

    tokenizer, model = load_encoder(encoder_name, device)
    vectors = []
    texts = [text_for_mode(row, mode) for row in rows]
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
            encoded = {key: value.to(device) for key, value in encoded.items()}
            output = model(**encoded)
            if hasattr(output, "pooler_output") and output.pooler_output is not None:
                pooled = output.pooler_output
            else:
                pooled = mean_pool(output.last_hidden_state, encoded["attention_mask"])
            vectors.append(pooled.detach().cpu().numpy())
    matrix = np.vstack(vectors)
    np.save(cache_path, matrix)
    return matrix


def model_predictions(model: Any, matrix: np.ndarray) -> tuple[list[int], list[float]]:
    preds = [int(value) for value in model.predict(matrix)]
    if hasattr(model, "decision_function"):
        scores = model.decision_function(matrix)
        if hasattr(scores, "tolist"):
            scores = scores.tolist()
        return preds, [float(value) for value in scores]
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(matrix)
        return preds, [float(row[1]) for row in probabilities]
    return preds, [0.0 for _ in preds]


def subset_metrics(rows: list[dict[str, Any]], preds: list[int], scores: list[float]) -> dict[str, dict[str, Any]]:
    result = {}
    for name in sorted({subset(row) for row in rows}):
        indexes = [index for index, row in enumerate(rows) if subset(row) == name]
        result[name] = metric_values(
            [1 if rows[index].get("docs_update_required") is True else 0 for index in indexes],
            [preds[index] for index in indexes],
            [scores[index] for index in indexes],
        )
    return result


def write_blocked_report(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# External Deep-JIT Frozen Code Encoder Comparison 2026-08\n\n"
        "The frozen pretrained code-encoder baseline is blocked in this environment.\n\n"
        "```json\n"
        + json.dumps(result, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )


def metric_row(result: dict[str, Any], split_name: str) -> str:
    metrics = result[split_name]
    return (
        f"| `{result['encoder']}` | `{result['model']}` | `{result['input_mode']}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
        f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | "
        f"{pct(metrics['false_positive_rate'])} | {pct(metrics['specificity'])} | {pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} |"
    )


def write_report(path: Path, results: list[dict[str, Any]], best: dict[str, Any], cache_dir: Path) -> None:
    lines = [
        "# External Deep-JIT Frozen Code Encoder Comparison 2026-08",
        "",
        "Frozen pretrained code-model embeddings are used as features for lightweight classifiers. No future fields (`new_comment_raw`, `doc_after`, `doc_diff`) are used as model input.",
        "",
        f"- Best encoder: `{best['encoder']}`",
        f"- Best model: `{best['model']}`",
        f"- Best input mode: `{best['input_mode']}`",
        "- Selection rule: validation MCC, then validation balanced accuracy and F1.",
        f"- Embedding cache: `{cache_dir}`",
        "",
        "## Validation Metrics",
        "",
        "| Encoder | Model | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines.extend(metric_row(result, "validation") for result in results)
    lines.extend(
        [
            "",
            "## Test Metrics",
            "",
            "| Encoder | Model | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    lines.extend(metric_row(result, "test") for result in results)
    lines.extend(["", "## Per-Subset Test Metrics", ""])
    for name, metrics in best["test_by_subset"].items():
        lines.append(
            f"- `{name}`: accuracy {pct(metrics['accuracy'])}, F1 {pct(metrics['f1'])}, FPR {pct(metrics['false_positive_rate'])}, MCC {metrics['mcc']:.4f}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def train_code_encoder_binary(
    train_path: Path,
    validation_path: Path,
    test_path: Path,
    model_output: Path,
    report_path: Path,
    cache_dir: Path,
    batch_size: int = 8,
    encoder_name: str | None = None,
) -> dict[str, Any]:
    try:
        import torch
        import transformers  # noqa: F401
    except Exception as exc:
        result = {"status": "blocked", "reason": "missing_dependency", "detail": repr(exc)}
        write_blocked_report(report_path, result)
        return result

    train_rows = read_jsonl(train_path)
    validation_rows = read_jsonl(validation_path)
    test_rows = read_jsonl(test_path)
    if not train_rows or not validation_rows or not test_rows:
        result = {"status": "blocked", "reason": "missing_input_split"}
        write_blocked_report(report_path, result)
        return result

    device = "cuda" if torch.cuda.is_available() else "cpu"
    encoders = [encoder_name] if encoder_name else ENCODERS
    results: list[dict[str, Any]] = []
    trained: list[dict[str, Any]] = []
    y_train = labels(train_rows)
    y_validation = labels(validation_rows)
    y_test = labels(test_rows)

    try:
        for encoder in encoders:
            for mode in INPUT_MODES:
                train_vectors = embeddings_for_rows(train_rows, train_path, encoder, mode, cache_dir, batch_size, device)
                validation_vectors = embeddings_for_rows(validation_rows, validation_path, encoder, mode, cache_dir, batch_size, device)
                test_vectors = embeddings_for_rows(test_rows, test_path, encoder, mode, cache_dir, batch_size, device)
                for model_name, model in [
                    ("logreg_balanced", LogisticRegression(class_weight="balanced", max_iter=1000, solver="liblinear")),
                    ("linear_svc_balanced", LinearSVC(class_weight="balanced", max_iter=5000)),
                ]:
                    model.fit(train_vectors, y_train)
                    validation_pred, validation_scores = model_predictions(model, validation_vectors)
                    test_pred, test_scores = model_predictions(model, test_vectors)
                    item = {
                        "encoder": encoder,
                        "model": model_name,
                        "input_mode": mode,
                        "validation": metric_values(y_validation, validation_pred, validation_scores),
                        "test": metric_values(y_test, test_pred, test_scores),
                        "test_by_subset": subset_metrics(test_rows, test_pred, test_scores),
                        "fitted_model": model,
                    }
                    results.append({key: value for key, value in item.items() if key != "fitted_model"})
                    trained.append(item)
    except Exception as exc:
        result = {"status": "blocked", "reason": "encoder_runtime_failure", "detail": repr(exc), "device": device}
        write_blocked_report(report_path, result)
        return result

    best = max(trained, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]))
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "encoder": best["encoder"],
            "model_name": best["model"],
            "input_mode": best["input_mode"],
            "classifier": best["fitted_model"],
            "validation_metrics": best["validation"],
            "test_metrics": best["test"],
            "selection_rule": "validation MCC, then validation balanced accuracy, then validation F1",
        },
        model_output,
    )
    write_report(report_path, results, {key: value for key, value in best.items() if key != "fitted_model"}, cache_dir)
    return {
        "status": "ok",
        "device": device,
        "report": str(report_path),
        "model_output": str(model_output),
        "best_encoder": best["encoder"],
        "best_model": best["model"],
        "best_input_mode": best["input_mode"],
        "best_test_accuracy": best["test"]["accuracy"],
        "best_test_f1": best["test"]["f1"],
        "best_test_false_positive_rate": best["test"]["false_positive_rate"],
        "best_test_mcc": best["test"]["mcc"],
    }
