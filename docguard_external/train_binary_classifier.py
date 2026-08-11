from __future__ import annotations

import json
from collections import Counter
from math import sqrt
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
    "specificity": 0.008,
    "balanced_accuracy": 0.504,
    "mcc": 0.06350006350009525,
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


def positive_scores_for_model(model: Pipeline, model_name: str, texts: list[str]) -> tuple[list[float], str]:
    classifier = model.named_steps["classifier"]
    if model_name == "tfidf_logreg" and hasattr(classifier, "predict_proba"):
        probabilities = model.predict_proba(texts)
        return [float(row[1]) for row in probabilities], "positive-class LogisticRegression probability; not externally calibrated"
    margins = model.decision_function(texts)
    if hasattr(margins, "tolist"):
        margins = margins.tolist()
    return [float(value) for value in margins], "LinearSVC positive-class decision margin; not calibrated probability"


def metric_values(y_true: list[int], y_pred: list[int], confidences: list[float] | None = None) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if tn + fp else 0.0
    recall = recall_score(y_true, y_pred, zero_division=0) if y_true else 0.0
    mcc_denominator = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    values = {
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "accuracy": accuracy_score(y_true, y_pred) if y_true else 0.0,
        "precision": precision_score(y_true, y_pred, zero_division=0) if y_true else 0.0,
        "recall": recall,
        "f1": f1_score(y_true, y_pred, zero_division=0) if y_true else 0.0,
        "false_positive_rate": fp / (fp + tn) if fp + tn else 0.0,
        "false_negative_rate": fn / (fn + tp) if fn + tp else 0.0,
        "specificity": specificity,
        "balanced_accuracy": (recall + specificity) / 2,
        "mcc": ((tp * tn) - (fp * fn)) / mcc_denominator if mcc_denominator else 0.0,
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
    y_validation = labels(validation_rows)
    y_train = labels(train_rows)
    for mode in INPUT_MODES:
        test_texts = [input_text(row, mode) for row in test_rows]
        validation_texts = [input_text(row, mode) for row in validation_rows]
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
            if validation_rows:
                validation_pred, validation_confidences, _validation_rule = scores_for_model(model, model_name, validation_texts)
                validation_metrics = metric_values(y_validation, validation_pred, validation_confidences)
            else:
                validation_metrics = metrics
            row = result_row(model_name, mode, f"default classifier decision; {confidence_rule}", metrics, evaluate_by_subset(test_rows, y_pred, confidences))
            all_results.append(row)
            trained_models.append(
                {
                    "model": model,
                    "model_name": model_name,
                    "input_mode": mode,
                    "metrics": metrics,
                    "validation_metrics": validation_metrics,
                    "confidence_rule": confidence_rule,
                }
            )
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
    best = max(trained_models, key=lambda item: (item["validation_metrics"]["f1"], item["validation_metrics"]["balanced_accuracy"]))
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best["model"],
            "model_name": best["model_name"],
            "input_mode": best["input_mode"],
            "metrics": best["metrics"],
            "validation_metrics": best["validation_metrics"],
            "label_polarity_status": "plausible_manual_verification_needed",
            "leakage_note": "Model inputs exclude new_comment_raw, doc_after, and doc_diff.",
        },
        model_output,
    )
    variant = report_variant(report_path)
    write_model_comparison(report_path, train_rows, validation_rows, test_rows, all_results, best, model_output, include_sentence_embeddings, variant)
    threshold_result = write_validation_threshold_tuning(best, validation_rows, test_rows, variant)
    write_zero_shot_comparison(best, variant)
    write_best_model_error_analysis(best, test_rows, variant)
    write_adaptation_interpretation(best, variant)
    write_thesis_evidence_map(best, variant)
    if variant == "combined_validation":
        write_validation_strategy_comparison(best, threshold_result)
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
        "best_specificity": best["metrics"]["specificity"],
        "best_balanced_accuracy": best["metrics"]["balanced_accuracy"],
        "best_mcc": best["metrics"]["mcc"],
        "best_validation_f1": best["validation_metrics"]["f1"],
    }


def report_variant(report_path: Path) -> str:
    return "combined_validation" if "combined_validation" in report_path.stem else "default"


def variant_report_path(variant: str, default_name: str, combined_name: str) -> Path:
    return REPORTS_DIR / (combined_name if variant == "combined_validation" else default_name)


def write_blocked_report(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# External Deep-JIT Binary Classifier Evaluation 2026-08\n\nTraining blocked.\n\n" + json.dumps(result, indent=2), encoding="utf-8")


def table_line(result: dict[str, Any]) -> str:
    metrics = result["combined"]
    return (
        f"| `{result['system']}` | `{result['input_mode']}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
        f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | "
        f"{pct(metrics['false_positive_rate'])} | {pct(metrics['false_negative_rate'])} | {pct(metrics['specificity'])} | "
        f"{pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} | {metrics['median_confidence_or_margin']:.4f} |"
    )


def subset_lines(result: dict[str, Any]) -> list[str]:
    lines = []
    for subset_name, metrics in result["by_subset"].items():
        lines.append(
            f"| `{result['system']}` | `{result['input_mode']}` | `{subset_name}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
            f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | "
            f"{pct(metrics['false_positive_rate'])} | {pct(metrics['specificity'])} | {pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} |"
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
    variant: str = "default",
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
        "- Best model selection: validation F1, with validation balanced accuracy as tie-breaker.",
        f"- Best validation F1: `{best['validation_metrics']['f1']:.4f}`",
        "- Label polarity status: `plausible_manual_verification_needed`",
        "- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.",
        "",
        "## Combined Test Metrics",
        "",
        "| System | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR | Specificity | Balanced accuracy | MCC | Median confidence/margin |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines.extend(table_line(result) for result in results)
    lines.extend(
        [
            "",
            "## Per-Subset Test Metrics",
            "",
            "| System | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
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
    comparison_path = variant_report_path(
        variant,
        "external_deep_jit_model_comparison_2026_08.md",
        "external_deep_jit_combined_validation_model_comparison_2026_08.md",
    )
    comparison_path.write_text(content, encoding="utf-8")


def write_zero_shot_comparison(best: dict[str, Any], variant: str = "default") -> None:
    path = variant_report_path(
        variant,
        "external_deep_jit_zero_shot_vs_trained_2026_08.md",
        "external_deep_jit_combined_validation_zero_shot_vs_trained_2026_08.md",
    )
    trained = best["metrics"]
    lines = [
        "# External Deep-JIT Zero-Shot vs Trained Classifier 2026-08",
        "",
        "| System | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| Existing synthetic-trained DocGuard zero-shot | {pct(ZERO_SHOT['accuracy'])} | {pct(ZERO_SHOT['precision'])} | {pct(ZERO_SHOT['recall'])} | {pct(ZERO_SHOT['f1'])} | {pct(ZERO_SHOT['false_positive_rate'])} | {pct(ZERO_SHOT['specificity'])} | {pct(ZERO_SHOT['balanced_accuracy'])} | {ZERO_SHOT['mcc']:.4f} |",
        f"| Best external-trained lightweight classifier (`{best['model_name']}`, `{best['input_mode']}`) | {pct(trained['accuracy'])} | {pct(trained['precision'])} | {pct(trained['recall'])} | {pct(trained['f1'])} | {pct(trained['false_positive_rate'])} | {pct(trained['specificity'])} | {pct(trained['balanced_accuracy'])} | {trained['mcc']:.4f} |",
        "",
        "Zero-shot transfer exposes a domain/task shift. The trained classifier may have similar or slightly lower F1, but its specificity, balanced accuracy, and MCC show a much healthier binary classifier. External training should be kept separate from the project-level synthetic DocGuard benchmark and interpreted as a code-comment consistency proxy adaptation.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def threshold_candidates(model_name: str, scores: list[float]) -> list[float]:
    if model_name == "tfidf_logreg":
        return [0.10, 0.20, 0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90]
    return [-1.0, -0.75, -0.50, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0]


def predictions_at_threshold(scores: list[float], threshold: float) -> list[int]:
    return [1 if score >= threshold else 0 for score in scores]


def threshold_row(threshold: float, y_true: list[int], scores: list[float]) -> dict[str, Any]:
    y_pred = predictions_at_threshold(scores, threshold)
    values = metric_values(y_true, y_pred, [abs(score) for score in scores])
    values["threshold"] = threshold
    values["predicted_positive_count"] = sum(y_pred)
    values["predicted_negative_count"] = len(y_pred) - sum(y_pred)
    return values


def write_validation_threshold_tuning(best: dict[str, Any], validation_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]], variant: str = "default") -> dict[str, Any] | None:
    path = variant_report_path(
        variant,
        "external_deep_jit_validation_threshold_tuning_2026_08.md",
        "external_deep_jit_combined_validation_threshold_tuning_2026_08.md",
    )
    if not validation_rows:
        path.write_text(
            "# External Deep-JIT Validation Threshold Tuning 2026-08\n\nValidation split unavailable. No threshold tuning was performed on test.\n",
            encoding="utf-8",
        )
        return None
    model = best["model"]
    mode = best["input_mode"]
    model_name = best["model_name"]
    validation_scores, score_rule = positive_scores_for_model(model, model_name, [input_text(row, mode) for row in validation_rows])
    y_validation = labels(validation_rows)
    candidates = threshold_candidates(model_name, validation_scores)
    validation_results = [threshold_row(threshold, y_validation, validation_scores) for threshold in candidates]
    selected = max(validation_results, key=lambda item: (item["balanced_accuracy"], item["f1"]))
    test_scores, _test_score_rule = positive_scores_for_model(model, model_name, [input_text(row, mode) for row in test_rows])
    test_result = threshold_row(selected["threshold"], labels(test_rows), test_scores)
    lines = [
        "# External Deep-JIT Validation Threshold Tuning 2026-08",
        "",
        f"- Model: `{model_name}`",
        f"- Input mode: `{mode}`",
        f"- Score rule: {score_rule}",
        "- Selection rule: choose threshold on validation by balanced accuracy, with F1 as tie-breaker.",
        f"- Selected validation threshold: `{selected['threshold']:.2f}`",
        "- Test set is used once after threshold selection; no threshold is tuned on test.",
        "",
        "## Validation Sweep",
        "",
        "| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in validation_results:
        lines.append(
            f"| {row['threshold']:.2f} | {row['predicted_positive_count']} | {row['predicted_negative_count']} | {row['tp']} | {row['fp']} | {row['tn']} | {row['fn']} | "
            f"{pct(row['accuracy'])} | {pct(row['precision'])} | {pct(row['recall'])} | {pct(row['f1'])} | {pct(row['false_positive_rate'])} | "
            f"{pct(row['specificity'])} | {pct(row['balanced_accuracy'])} | {row['mcc']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Test Result At Validation-Selected Threshold",
            "",
            "| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            f"| {test_result['threshold']:.2f} | {test_result['predicted_positive_count']} | {test_result['predicted_negative_count']} | {test_result['tp']} | {test_result['fp']} | {test_result['tn']} | {test_result['fn']} | "
            f"{pct(test_result['accuracy'])} | {pct(test_result['precision'])} | {pct(test_result['recall'])} | {pct(test_result['f1'])} | {pct(test_result['false_positive_rate'])} | "
            f"{pct(test_result['specificity'])} | {pct(test_result['balanced_accuracy'])} | {test_result['mcc']:.4f} |",
            "",
            "## Interpretation",
            "",
            "Threshold tuning is diagnostic because the score is not calibrated as a production probability. It is still useful for showing whether validation-set thresholding can trade recall for specificity without touching test labels.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"selected_threshold": selected["threshold"], "validation": selected, "test": test_result}


def write_best_model_error_analysis(best: dict[str, Any], test_rows: list[dict[str, Any]], variant: str = "default") -> None:
    path = variant_report_path(
        variant,
        "external_deep_jit_best_model_error_analysis_2026_08.md",
        "external_deep_jit_combined_validation_best_model_error_analysis_2026_08.md",
    )
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
        f"- Specificity: `{pct(metrics['specificity'])}`",
        f"- Balanced accuracy: `{pct(metrics['balanced_accuracy'])}`",
        f"- MCC: `{metrics['mcc']:.4f}`",
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


def write_adaptation_interpretation(best: dict[str, Any], variant: str = "default") -> None:
    path = variant_report_path(
        variant,
        "external_deep_jit_adaptation_interpretation_2026_08.md",
        "external_deep_jit_combined_validation_adaptation_interpretation_2026_08.md",
    )
    metrics = best["metrics"]
    lines = [
        "# External Deep-JIT Adaptation Interpretation 2026-08",
        "",
        "Existing DocGuard generalizes as a high-recall detector but not as a binary consistency classifier on Deep-JIT. External task-specific training is necessary for specificity.",
        "",
        f"The best lightweight external classifier is `{best['model_name']}` with `{best['input_mode']}` input. It reaches {pct(metrics['accuracy'])} accuracy, {pct(metrics['precision'])} precision, {pct(metrics['recall'])} recall, {pct(metrics['f1'])} F1, {pct(metrics['false_positive_rate'])} FPR, {pct(metrics['specificity'])} specificity, {pct(metrics['balanced_accuracy'])} balanced accuracy, and MCC {metrics['mcc']:.4f} on the Deep-JIT test split.",
        "",
        "Deep-JIT remains a proxy for code-comment consistency, not full Markdown documentation patching. This strengthens the thesis by showing why external validation matters: synthetic-only and positive-only evidence did not reveal the specificity problem.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_thesis_evidence_map(best: dict[str, Any], variant: str = "default") -> None:
    path = REPORTS_DIR / "thesis_evidence_map_2026_08.md"
    metrics = best["metrics"]
    lines = [
        "# Thesis Evidence Map 2026-08",
        "",
        "This document separates the evidence streams for the DocGuard MSc thesis so results are not overclaimed across tasks.",
        "",
        "| Evidence stream | Dataset | What it supports | Key result | What not to claim |",
        "| --- | --- | --- | --- | --- |",
        "| Controlled synthetic benchmark | DocGuard synthetic v0.4 | End-to-end DocGuard pipeline on controlled REST API documentation scenarios | Hybrid/HF embedding reports show perfect synthetic test performance | Do not treat this alone as real-world generalization because generator/template bias is possible. |",
        "| Real positive sensitivity | CoDocBench positive sample | The zero-shot model detects real code-doc/comment co-change positives | `code_diff_only` positive recall 100.00% on 500 positives | Do not report precision/F1/FPR because the sample is positive-only. |",
        "| Synthetic negative sanity | Synthetic no-update controls | The model is not constant-positive on in-domain synthetic negatives | 0/500 false positives in both tested input modes | Do not treat this as external negative evidence. |",
        "| External binary proxy zero-shot | Deep-JIT / DocChecker-style code-comment consistency | External binary proxy exposes domain/task shift | Accuracy 50.40%, recall 100.00%, FPR 99.20%, specificity 0.80%, MCC 0.0635 | Do not call this deployment-ready or project-level Markdown documentation performance. |",
        f"| External task-specific adaptation | Deep-JIT TF-IDF classifier | External training improves binary specificity on code-comment consistency | Accuracy {pct(metrics['accuracy'])}, precision {pct(metrics['precision'])}, recall {pct(metrics['recall'])}, FPR {pct(metrics['false_positive_rate'])}, specificity {pct(metrics['specificity'])}, MCC {metrics['mcc']:.4f} | Do not merge this into the main DocGuard synthetic benchmark or claim Markdown patch generation. |",
        "",
        "## Thesis-Safe Claims",
        "",
        "- DocGuard is a prototype NLP agent for code/documentation consistency analysis.",
        "- The controlled synthetic benchmark demonstrates that the pipeline can learn the intended detection, routing, categorization, and patch-targeting structure.",
        "- External positive validation shows strong sensitivity to real code-documentation co-change signals.",
        "- External binary proxy validation reveals that synthetic-trained zero-shot DocGuard over-predicts update needs on real consistent comments.",
        "- Task-specific external adaptation substantially improves specificity, showing that external calibration/training is necessary for practical binary consistency detection.",
        "",
        "## Claims To Avoid",
        "",
        "- Do not claim production readiness.",
        "- Do not report synthetic v0.4 metrics as final real-world performance.",
        "- Do not report CoDocBench positive recall as precision or F1.",
        "- Do not report Deep-JIT as full project-level Markdown API documentation evaluation.",
        "- Do not call Deep-JIT numeric label polarity fully confirmed until original documentation or preprocessing code explicitly confirms it.",
        "",
        "## Remaining Methodological Caveat",
        "",
        "Deep-JIT numeric label polarity remains `plausible_manual_verification_needed`. The current mapping is supported by sampled examples and task framing, but final thesis text should either cite an explicit polarity source or describe the mapping as manually audited and plausible.",
    ]
    if variant == "combined_validation":
        lines.extend(
            [
                "",
                "## Robustness Update",
                "",
                "A deterministic Summary validation carve-out robustness experiment was added to reduce Return-only validation bias. The combined-validation result should be considered the cleaner Deep-JIT model-selection setup if it remains consistent with the earlier Return-only-validation conclusion.",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_validation_strategy_comparison(best: dict[str, Any], threshold_result: dict[str, Any] | None) -> None:
    path = REPORTS_DIR / "external_deep_jit_validation_strategy_comparison_2026_08.md"
    metrics = best["metrics"]
    lines = [
        "# External Deep-JIT Validation Strategy Comparison 2026-08",
        "",
        "## Compared Setups",
        "",
        "| Setup | Validation composition | Best model | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        "| Previous Return-only validation | Return valid only | `tfidf_logreg + old_comment_plus_code_diff` | 68.72% | 73.41% | 58.71% | 65.24% | 21.27% | 78.73% | 68.72% | 0.3821 |",
        f"| Combined validation robustness | Return valid + deterministic Summary train carve-out | `{best['model_name']} + {best['input_mode']}` | {pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | {pct(metrics['false_positive_rate'])} | {pct(metrics['specificity'])} | {pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} |",
        "",
        "## Interpretation",
        "",
    ]
    previous_key = ("tfidf_logreg", "old_comment_plus_code_diff")
    if (best["model_name"], best["input_mode"]) == previous_key:
        lines.append("Model choice did not change. This suggests the previous conclusion is stable under the combined-validation robustness setup.")
    else:
        lines.append("Model choice changed. This indicates the earlier Return-only validation setup was sensitive to subset composition and the combined-validation result should be preferred.")
    lines.extend(
        [
            "",
            "The old Return-only validation result should be kept as a historical baseline. The combined-validation setup should become the cleaner thesis result because it includes Summary examples during validation while keeping Summary test untouched.",
        ]
    )
    if threshold_result:
        test = threshold_result["test"]
        lines.extend(
            [
                "",
                "## Combined-Validation Threshold Result",
                "",
                f"- Selected threshold: `{threshold_result['selected_threshold']:.2f}`",
                f"- Test accuracy: `{pct(test['accuracy'])}`",
                f"- Test precision: `{pct(test['precision'])}`",
                f"- Test recall: `{pct(test['recall'])}`",
                f"- Test F1: `{pct(test['f1'])}`",
                f"- Test FPR: `{pct(test['false_positive_rate'])}`",
                f"- Test specificity: `{pct(test['specificity'])}`",
                f"- Test MCC: `{test['mcc']:.4f}`",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
