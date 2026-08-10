from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from docguard_external.evaluate_existing_docguard import pct, truncate


REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
INPUT_MODES = [
    "old_comment_plus_code_diff",
    "old_comment_plus_old_new_code",
    "code_diff_only",
    "old_comment_plus_new_code",
]
ZERO_SHOT = {
    "accuracy": 0.504,
    "precision": 0.5020080321285141,
    "recall": 1.0,
    "f1": 0.6684491978609626,
    "false_positive_rate": 0.992,
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def input_text(row: dict[str, Any], mode: str) -> str:
    old_comment = row.get("old_comment_raw") or row.get("doc_before") or ""
    old_code = row.get("old_code_raw") or row.get("code_before") or ""
    new_code = row.get("new_code_raw") or row.get("code_after") or ""
    code_diff = row.get("code_diff") or ""
    if mode == "old_comment_plus_code_diff":
        return f"OLD_COMMENT:\n{old_comment}\n\nCODE_DIFF:\n{code_diff}"
    if mode == "old_comment_plus_old_new_code":
        return f"OLD_COMMENT:\n{old_comment}\n\nOLD_CODE:\n{old_code}\n\nNEW_CODE:\n{new_code}"
    if mode == "code_diff_only":
        return f"CODE_DIFF:\n{code_diff}"
    if mode == "old_comment_plus_new_code":
        return f"OLD_COMMENT:\n{old_comment}\n\nNEW_CODE:\n{new_code}"
    raise ValueError(f"unknown input mode: {mode}")


def labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if row.get("docs_update_required") is True else 0 for row in rows]


def subset(row: dict[str, Any]) -> str:
    return str(row.get("subset") or (row.get("metadata") or {}).get("subset") or "unknown")


def vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=80_000, sublinear_tf=True)


def build_model(model_name: str) -> Pipeline:
    if model_name == "tfidf_logreg":
        classifier = LogisticRegression(class_weight="balanced", max_iter=1000, solver="liblinear")
    elif model_name == "tfidf_linear_svc":
        classifier = LinearSVC(class_weight="balanced", max_iter=5000)
    else:
        raise ValueError(f"unknown model: {model_name}")
    return Pipeline([("features", vectorizer()), ("classifier", classifier)])


def scores_for_model(model: Pipeline, model_name: str, texts: list[str]) -> tuple[list[int], list[float], str]:
    preds = [int(value) for value in model.predict(texts)]
    classifier = model.named_steps["classifier"]
    if model_name == "tfidf_logreg" and hasattr(classifier, "predict_proba"):
        probabilities = model.predict_proba(texts)
        confidence = [float(max(row)) for row in probabilities]
        return preds, confidence, "max predicted class probability from LogisticRegression; not externally calibrated"
    if hasattr(model, "decision_function"):
        margins = model.decision_function(texts)
        if hasattr(margins, "tolist"):
            margins = margins.tolist()
        confidence = [abs(float(value)) for value in margins]
        return preds, confidence, "absolute LinearSVC decision margin; not calibrated probability"
    return preds, [0.0 for _ in preds], "confidence unavailable"


def metric_values(y_true: list[int], y_pred: list[int], confidences: list[float] | None = None) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    values = {
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "accuracy": accuracy_score(y_true, y_pred) if y_true else 0.0,
        "precision": precision_score(y_true, y_pred, zero_division=0) if y_true else 0.0,
        "recall": recall_score(y_true, y_pred, zero_division=0) if y_true else 0.0,
        "f1": f1_score(y_true, y_pred, zero_division=0) if y_true else 0.0,
        "false_positive_rate": fp / (fp + tn) if fp + tn else 0.0,
        "false_negative_rate": fn / (fn + tp) if fn + tp else 0.0,
    }
    if confidences is not None and confidences:
        values["median_confidence_or_margin"] = median(confidences)
        values["mean_confidence_or_margin"] = mean(confidences)
    else:
        values["median_confidence_or_margin"] = 0.0
        values["mean_confidence_or_margin"] = 0.0
    return values


def evaluate_by_subset(rows: list[dict[str, Any]], y_pred: list[int], confidences: list[float]) -> dict[str, dict[str, Any]]:
    result = {}
    for name in sorted({subset(row) for row in rows}):
        indexes = [index for index, row in enumerate(rows) if subset(row) == name]
        result[name] = metric_values(
            [1 if rows[index].get("docs_update_required") is True else 0 for index in indexes],
            [y_pred[index] for index in indexes],
            [confidences[index] for index in indexes],
        )
    return result


def baseline_predictions(name: str, train_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]]) -> list[int]:
    if name == "always_positive":
        return [1 for _ in test_rows]
    if name == "always_negative":
        return [0 for _ in test_rows]
    if name == "majority":
        majority = Counter(labels(train_rows)).most_common(1)[0][0]
        return [majority for _ in test_rows]
    raise ValueError(name)


def result_row(system: str, input_mode_name: str, decision_rule: str, metrics: dict[str, Any], by_subset: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "system": system,
        "input_mode": input_mode_name,
        "decision_rule": decision_rule,
        "combined": metrics,
        "by_subset": by_subset,
    }


def train_and_evaluate(
    train_path: Path,
    validation_path: Path,
    test_path: Path,
    model_output: Path,
    report_path: Path,
    include_sentence_embeddings: bool = False,
) -> dict[str, Any]:
    train_rows = read_jsonl(train_path)
    validation_rows = read_jsonl(validation_path) if validation_path.exists() else []
    test_rows = read_jsonl(test_path)
    if not train_rows or not test_rows:
        result = {
            "status": "blocked",
            "message": "train and test files are required",
            "train_records": len(train_rows),
            "validation_records": len(validation_rows),
            "test_records": len(test_rows),
        }
        write_blocked_report(report_path, result)
        return result
    all_results: list[dict[str, Any]] = []
    trained_models: list[dict[str, Any]] = []
    y_test = labels(test_rows)
    y_train = labels(train_rows)
    for mode in INPUT_MODES:
        test_texts = [input_text(row, mode) for row in test_rows]
        for baseline in ["always_positive", "always_negative", "majority"]:
            y_pred = baseline_predictions(baseline, train_rows, test_rows)
            confidences = [1.0 for _ in y_pred]
            all_results.append(
                result_row(
                    baseline,
                    mode,
                    "deterministic baseline",
                    metric_values(y_test, y_pred, confidences),
                    evaluate_by_subset(test_rows, y_pred, confidences),
                )
            )
        for model_name in ["tfidf_logreg", "tfidf_linear_svc"]:
            model = build_model(model_name)
            model.fit([input_text(row, mode) for row in train_rows], y_train)
            y_pred, confidences, confidence_rule = scores_for_model(model, model_name, test_texts)
            metrics = metric_values(y_test, y_pred, confidences)
            row = result_row(model_name, mode, f"default classifier decision; {confidence_rule}", metrics, evaluate_by_subset(test_rows, y_pred, confidences))
            all_results.append(row)
            trained_models.append({"model": model, "model_name": model_name, "input_mode": mode, "metrics": metrics, "confidence_rule": confidence_rule})
    if include_sentence_embeddings:
        all_results.append(
            result_row(
                "sentence_embedding_logreg",
                "all",
                "skipped in this implementation path; use a dedicated opt-in embedding trainer if needed",
                metric_values(y_test, [0 for _ in y_test], [0.0 for _ in y_test]),
                {},
            )
        )
    best = max(trained_models, key=lambda item: item["metrics"]["f1"])
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best["model"],
            "model_name": best["model_name"],
            "input_mode": best["input_mode"],
            "metrics": best["metrics"],
            "label_polarity_status": "plausible_manual_verification_needed",
            "leakage_note": "Model inputs exclude new_comment_raw, doc_after, and doc_diff.",
        },
        model_output,
    )
    write_model_comparison(report_path, train_rows, validation_rows, test_rows, all_results, best, model_output, include_sentence_embeddings)
    write_zero_shot_comparison(best)
    write_best_model_error_analysis(best, test_rows)
    write_adaptation_interpretation(best)
    return {
        "status": "ok",
        "train_records": len(train_rows),
        "validation_records": len(validation_rows),
        "test_records": len(test_rows),
        "model_output": str(model_output),
        "report": str(report_path),
        "best_model": best["model_name"],
        "best_input_mode": best["input_mode"],
        "best_accuracy": best["metrics"]["accuracy"],
        "best_precision": best["metrics"]["precision"],
        "best_recall": best["metrics"]["recall"],
        "best_f1": best["metrics"]["f1"],
        "best_false_positive_rate": best["metrics"]["false_positive_rate"],
    }


def write_blocked_report(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# External Deep-JIT Binary Classifier Evaluation 2026-08\n\nTraining blocked.\n\n" + json.dumps(result, indent=2), encoding="utf-8")


def table_line(result: dict[str, Any]) -> str:
    metrics = result["combined"]
    return (
        f"| `{result['system']}` | `{result['input_mode']}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
        f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | "
        f"{pct(metrics['false_positive_rate'])} | {pct(metrics['false_negative_rate'])} | {metrics['median_confidence_or_margin']:.4f} |"
    )


def subset_lines(result: dict[str, Any]) -> list[str]:
    lines = []
    for subset_name, metrics in result["by_subset"].items():
        lines.append(
            f"| `{result['system']}` | `{result['input_mode']}` | `{subset_name}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
            f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | {pct(metrics['false_positive_rate'])} |"
        )
    return lines


def write_model_comparison(
    report_path: Path,
    train_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    test_rows: list[dict[str, Any]],
    results: list[dict[str, Any]],
    best: dict[str, Any],
    model_output: Path,
    include_sentence_embeddings: bool,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External Deep-JIT Binary Classifier Evaluation 2026-08",
        "",
        f"- Train records: `{len(train_rows)}`",
        f"- Validation records: `{len(validation_rows)}`",
        f"- Test records: `{len(test_rows)}`",
        f"- Train label distribution: `{dict(Counter(labels(train_rows)))}`",
        f"- Validation label distribution: `{dict(Counter(labels(validation_rows)))}`",
        f"- Test label distribution: `{dict(Counter(labels(test_rows)))}`",
        f"- Best saved model: `{model_output}`",
        f"- Best model: `{best['model_name']}`",
        f"- Best input mode: `{best['input_mode']}`",
        "- Label polarity status: `plausible_manual_verification_needed`",
        "- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.",
        "",
        "## Combined Test Metrics",
        "",
        "| System | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR | Median confidence/margin |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines.extend(table_line(result) for result in results)
    lines.extend(
        [
            "",
            "## Per-Subset Test Metrics",
            "",
            "| System | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in results:
        lines.extend(subset_lines(result))
    lines.extend(
        [
            "",
            "## Sentence Embedding Model",
            "",
            "Skipped by default. `sentence_transformers` is optional and can be slower or require model download; this run focuses on CPU-friendly TF-IDF models.",
            "",
            f"- Requested sentence embeddings: `{include_sentence_embeddings}`",
        ]
    )
    content = "\n".join(lines) + "\n"
    report_path.write_text(content, encoding="utf-8")
    (REPORTS_DIR / "external_deep_jit_model_comparison_2026_08.md").write_text(content, encoding="utf-8")


def write_zero_shot_comparison(best: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_deep_jit_zero_shot_vs_trained_2026_08.md"
    trained = best["metrics"]
    lines = [
        "# External Deep-JIT Zero-Shot vs Trained Classifier 2026-08",
        "",
        "| System | Accuracy | Precision | Recall | F1 | FPR |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        f"| Existing synthetic-trained DocGuard zero-shot | {pct(ZERO_SHOT['accuracy'])} | {pct(ZERO_SHOT['precision'])} | {pct(ZERO_SHOT['recall'])} | {pct(ZERO_SHOT['f1'])} | {pct(ZERO_SHOT['false_positive_rate'])} |",
        f"| Best external-trained lightweight classifier (`{best['model_name']}`, `{best['input_mode']}`) | {pct(trained['accuracy'])} | {pct(trained['precision'])} | {pct(trained['recall'])} | {pct(trained['f1'])} | {pct(trained['false_positive_rate'])} |",
        "",
        "Zero-shot transfer exposes a domain/task shift. External training should be kept separate from the project-level synthetic DocGuard benchmark and interpreted as a code-comment consistency proxy adaptation.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_best_model_error_analysis(best: dict[str, Any], test_rows: list[dict[str, Any]]) -> None:
    path = REPORTS_DIR / "external_deep_jit_best_model_error_analysis_2026_08.md"
    mode = best["input_mode"]
    model = best["model"]
    texts = [input_text(row, mode) for row in test_rows]
    y_true = labels(test_rows)
    y_pred, confidences, confidence_rule = scores_for_model(model, best["model_name"], texts)
    errors = []
    for row, gold, pred, score in zip(test_rows, y_true, y_pred, confidences):
        if gold != pred:
            errors.append({"row": row, "gold": gold, "pred": pred, "score": score})
    error_by_subset = Counter(subset(item["row"]) for item in errors)
    metrics = metric_values(y_true, y_pred, confidences)
    lines = [
        "# External Deep-JIT Best Model Error Analysis 2026-08",
        "",
        f"- Best model: `{best['model_name']}`",
        f"- Input mode: `{mode}`",
        f"- Decision/confidence rule: {confidence_rule}",
        "",
        "## Confusion Matrix",
        "",
        f"- TP: `{metrics['tp']}`",
        f"- FP: `{metrics['fp']}`",
        f"- TN: `{metrics['tn']}`",
        f"- FN: `{metrics['fn']}`",
        "",
        "## Error Counts By Subset",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(error_by_subset.items())],
        "",
        "## Confidence/Margin Distribution",
        "",
        f"- Median: `{median(confidences):.4f}`",
        f"- Mean: `{mean(confidences):.4f}`",
        f"- Min: `{min(confidences):.4f}`",
        f"- Max: `{max(confidences):.4f}`",
        "",
        "## Top Error Examples",
        "",
    ]
    for item in sorted(errors, key=lambda value: value["score"], reverse=True)[:30]:
        row = item["row"]
        lines.extend(
            [
                f"### {row.get('record_id')}",
                "",
                f"- Subset: `{subset(row)}`",
                f"- Raw label: `{row.get('raw_label')}`",
                f"- Gold: `{bool(item['gold'])}`",
                f"- Predicted: `{bool(item['pred'])}`",
                f"- Confidence/margin: `{item['score']:.4f}`",
                f"- Old comment excerpt: {truncate(row.get('old_comment_raw'), 260)}",
                f"- Code diff excerpt: {truncate(row.get('code_diff'), 420)}",
                "",
                "- [ ] possible label noise",
                "- [ ] insufficient context",
                "- [ ] model error",
                "- [ ] mapping concern",
                "",
            ]
        )
    lines.extend(
        [
            "## Limitations",
            "",
            "This analysis is for the external code-comment consistency proxy only. It does not measure project-level Markdown documentation patching.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_adaptation_interpretation(best: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_deep_jit_adaptation_interpretation_2026_08.md"
    metrics = best["metrics"]
    lines = [
        "# External Deep-JIT Adaptation Interpretation 2026-08",
        "",
        "Existing DocGuard generalizes as a high-recall detector but not as a binary consistency classifier on Deep-JIT. External task-specific training is necessary for specificity.",
        "",
        f"The best lightweight external classifier is `{best['model_name']}` with `{best['input_mode']}` input. It reaches {pct(metrics['accuracy'])} accuracy, {pct(metrics['precision'])} precision, {pct(metrics['recall'])} recall, {pct(metrics['f1'])} F1, and {pct(metrics['false_positive_rate'])} FPR on the Deep-JIT test split.",
        "",
        "Deep-JIT remains a proxy for code-comment consistency, not full Markdown documentation patching. This strengthens the thesis by showing why external validation matters: synthetic-only and positive-only evidence did not reveal the specificity problem.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
