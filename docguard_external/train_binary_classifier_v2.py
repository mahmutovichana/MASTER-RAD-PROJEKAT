from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

import joblib
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import MaxAbsScaler
from sklearn.svm import LinearSVC

from docguard_external.evaluate_existing_docguard import pct


REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
INPUT_MODES = ["old_comment_plus_code_diff", "code_diff_only", "old_comment_plus_old_new_code"]
FEATURE_SETS = ["word_tfidf", "char_tfidf", "word_char_tfidf", "manual_features_only", "word_char_tfidf_plus_manual_features"]
BASE_MODELS = ["logreg_balanced", "linear_svc_balanced", "sgd_log_loss_balanced", "sgd_modified_huber_balanced", "complement_nb"]
PREVIOUS_COMBINED = {
    "accuracy": 0.6641,
    "f1": 0.6412,
    "false_positive_rate": 0.2719,
    "mcc": 0.3310,
}
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
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if row.get("docs_update_required") is True else 0 for row in rows]


def subset(row: dict[str, Any]) -> str:
    return str(row.get("subset") or (row.get("metadata") or {}).get("subset") or "unknown")


def text_for_mode(row: dict[str, Any], mode: str) -> str:
    old_comment = row.get("old_comment_raw") or row.get("doc_before") or ""
    old_code = row.get("old_code_raw") or row.get("code_before") or ""
    new_code = row.get("new_code_raw") or row.get("code_after") or ""
    code_diff = row.get("code_diff") or ""
    if mode == "old_comment_plus_code_diff":
        return f"OLD_COMMENT:\n{old_comment}\n\nCODE_DIFF:\n{code_diff}"
    if mode == "code_diff_only":
        return f"CODE_DIFF:\n{code_diff}"
    if mode == "old_comment_plus_old_new_code":
        return f"OLD_COMMENT:\n{old_comment}\n\nOLD_CODE:\n{old_code}\n\nNEW_CODE:\n{new_code}"
    raise ValueError(f"unknown input mode: {mode}")


def tokens(text: str) -> set[str]:
    return {match.group(0).lower() for match in TOKEN_RE.finditer(text or "")}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class TextSelector(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str):
        self.mode = mode

    def fit(self, rows: list[dict[str, Any]], y: list[int] | None = None) -> "TextSelector":
        return self

    def transform(self, rows: list[dict[str, Any]]) -> list[str]:
        return [text_for_mode(row, self.mode) for row in rows]


class ManualFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str):
        self.mode = mode

    def fit(self, rows: list[dict[str, Any]], y: list[int] | None = None) -> "ManualFeatureExtractor":
        return self

    def transform(self, rows: list[dict[str, Any]]) -> sparse.csr_matrix:
        values = [self._features(row) for row in rows]
        return sparse.csr_matrix(values, dtype=float)

    def _features(self, row: dict[str, Any]) -> list[float]:
        old_comment = str(row.get("old_comment_raw") or row.get("doc_before") or "")
        old_code = str(row.get("old_code_raw") or row.get("code_before") or "")
        new_code = str(row.get("new_code_raw") or row.get("code_after") or "")
        code_diff = str(row.get("code_diff") or "")

        has_comment = self.mode in {"old_comment_plus_code_diff", "old_comment_plus_old_new_code"}
        has_old_new_code = self.mode == "old_comment_plus_old_new_code"
        visible_comment = old_comment if has_comment else ""
        visible_old_code = old_code if has_old_new_code else ""
        visible_new_code = new_code if has_old_new_code else ""

        added_lines = [line for line in code_diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
        removed_lines = [line for line in code_diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        comment_tokens = tokens(visible_comment)
        diff_tokens = tokens(code_diff)
        old_code_tokens = tokens(visible_old_code)
        new_code_tokens = tokens(visible_new_code)
        changed_code = "\n".join(added_lines + removed_lines)
        changed_tokens = tokens(changed_code)
        old_code_line_count = max(1, len(visible_old_code.splitlines()))
        changed_line_ratio = (len(added_lines) + len(removed_lines)) / old_code_line_count if has_old_new_code else 0.0

        comment_markers = ["return", "param", "throws"]
        code_markers = ["return", "param", "exception", "null", "none", "boolean", "list", "dict"]
        lowered_comment = visible_comment.lower()
        lowered_changed = changed_code.lower()
        return [
            math.log1p(len(visible_comment)),
            math.log1p(len(code_diff)),
            math.log1p(len(added_lines)),
            math.log1p(len(removed_lines)),
            jaccard(comment_tokens, diff_tokens),
            jaccard(comment_tokens, new_code_tokens),
            jaccard(comment_tokens, changed_tokens),
            jaccard(old_code_tokens, new_code_tokens),
            changed_line_ratio,
            *[1.0 if marker in lowered_comment else 0.0 for marker in comment_markers],
            *[1.0 if marker in lowered_changed else 0.0 for marker in code_markers],
        ]


def word_tfidf(max_features: int) -> Pipeline:
    return Pipeline(
        [
            ("text", TextSelector("old_comment_plus_code_diff")),
            ("tfidf", TfidfVectorizer(ngram_range=(1, 3), min_df=2, max_features=max_features, sublinear_tf=True)),
        ]
    )


def feature_union(mode: str, feature_set: str, max_features: int) -> FeatureUnion:
    word_features = max(1, max_features // 2) if "char" in feature_set else max_features
    char_features = max(1, max_features // 2)
    parts: list[tuple[str, Any]] = []
    if feature_set in {"word_tfidf", "word_char_tfidf", "word_char_tfidf_plus_manual_features"}:
        parts.append(
            (
                "word",
                Pipeline(
                    [
                        ("text", TextSelector(mode)),
                        ("tfidf", TfidfVectorizer(ngram_range=(1, 3), min_df=2, max_features=word_features, sublinear_tf=True)),
                    ]
                ),
            )
        )
    if feature_set in {"char_tfidf", "word_char_tfidf", "word_char_tfidf_plus_manual_features"}:
        parts.append(
            (
                "char",
                Pipeline(
                    [
                        ("text", TextSelector(mode)),
                        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=char_features, sublinear_tf=True)),
                    ]
                ),
            )
        )
    if feature_set in {"manual_features_only", "word_char_tfidf_plus_manual_features"}:
        parts.append(("manual", Pipeline([("manual", ManualFeatureExtractor(mode)), ("scale", MaxAbsScaler())])))
    if not parts:
        raise ValueError(f"unknown feature set: {feature_set}")
    return FeatureUnion(parts)


def classifier(model_name: str) -> Any:
    if model_name == "logreg_balanced":
        return LogisticRegression(class_weight="balanced", max_iter=1500, solver="liblinear")
    if model_name == "linear_svc_balanced":
        return LinearSVC(class_weight="balanced", max_iter=6000)
    if model_name == "calibrated_linear_svc":
        try:
            return CalibratedClassifierCV(estimator=LinearSVC(class_weight="balanced", max_iter=5000), cv=2)
        except TypeError:
            return CalibratedClassifierCV(base_estimator=LinearSVC(class_weight="balanced", max_iter=5000), cv=2)
    if model_name == "sgd_log_loss_balanced":
        return SGDClassifier(loss="log_loss", class_weight="balanced", alpha=1e-5, max_iter=2000, tol=1e-3, random_state=42)
    if model_name == "sgd_modified_huber_balanced":
        return SGDClassifier(loss="modified_huber", class_weight="balanced", alpha=1e-5, max_iter=2000, tol=1e-3, random_state=42)
    if model_name == "complement_nb":
        return ComplementNB(alpha=0.2)
    raise ValueError(f"unknown model: {model_name}")


def build_pipeline(mode: str, feature_set: str, model_name: str, max_features: int) -> Pipeline:
    return Pipeline([("features", feature_union(mode, feature_set, max_features)), ("classifier", classifier(model_name))])


def metric_values(y_true: list[int], y_pred: list[int], scores: list[float] | None = None) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if tn + fp else 0.0
    recall = recall_score(y_true, y_pred, zero_division=0) if y_true else 0.0
    denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
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
        "mcc": ((tp * tn) - (fp * fn)) / denominator if denominator else 0.0,
    }
    values["median_score_or_margin"] = median(scores) if scores else 0.0
    values["mean_score_or_margin"] = mean(scores) if scores else 0.0
    return values


def predictions_and_scores(model: Pipeline, rows: list[dict[str, Any]]) -> tuple[list[int], list[float], str]:
    preds = [int(value) for value in model.predict(rows)]
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(rows)
        return preds, [float(row[1]) for row in probabilities], "positive-class probability when available"
    if hasattr(model, "decision_function"):
        margins = model.decision_function(rows)
        if hasattr(margins, "tolist"):
            margins = margins.tolist()
        return preds, [float(value) for value in margins], "positive-class decision margin"
    return preds, [0.0 for _ in preds], "score unavailable"


def matrix_predictions_and_scores(model: Any, matrix: Any) -> tuple[list[int], list[float], str]:
    preds = [int(value) for value in model.predict(matrix)]
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(matrix)
        return preds, [float(row[1]) for row in probabilities], "positive-class probability when available"
    if hasattr(model, "decision_function"):
        margins = model.decision_function(matrix)
        if hasattr(margins, "tolist"):
            margins = margins.tolist()
        return preds, [float(value) for value in margins], "positive-class decision margin"
    return preds, [0.0 for _ in preds], "score unavailable"


def evaluate_by_subset(rows: list[dict[str, Any]], preds: list[int], scores: list[float]) -> dict[str, dict[str, Any]]:
    result = {}
    for name in sorted({subset(row) for row in rows}):
        indexes = [index for index, row in enumerate(rows) if subset(row) == name]
        result[name] = metric_values(
            [1 if rows[index].get("docs_update_required") is True else 0 for index in indexes],
            [preds[index] for index in indexes],
            [scores[index] for index in indexes],
        )
    return result


def metric_line(result: dict[str, Any], section: str) -> str:
    metrics = result[section]
    return (
        f"| `{result['model_name']}` | `{result['feature_set']}` | `{result['input_mode']}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
        f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | "
        f"{pct(metrics['false_positive_rate'])} | {pct(metrics['specificity'])} | {pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} |"
    )


def subset_lines(result: dict[str, Any]) -> list[str]:
    lines = []
    for name, metrics in result["test_by_subset"].items():
        lines.append(
            f"| `{result['model_name']}` | `{result['feature_set']}` | `{result['input_mode']}` | `{name}` | {metrics['tp']} | {metrics['fp']} | {metrics['tn']} | {metrics['fn']} | "
            f"{pct(metrics['accuracy'])} | {pct(metrics['precision'])} | {pct(metrics['recall'])} | {pct(metrics['f1'])} | {pct(metrics['false_positive_rate'])} | "
            f"{pct(metrics['specificity'])} | {pct(metrics['balanced_accuracy'])} | {metrics['mcc']:.4f} |"
        )
    return lines


def write_report(path: Path, train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], test_rows: list[dict[str, Any]], results: list[dict[str, Any]], best: dict[str, Any], model_output: Path, include_calibrated: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    best_test = best["test"]
    lines = [
        "# External Deep-JIT Classical V2 Model Comparison 2026-08",
        "",
        "This experiment is a stronger CPU-friendly classical baseline for the Deep-JIT / DocChecker-style external binary proxy. It does not replace the project-level DocGuard Markdown documentation task.",
        "",
        f"- Train records: `{len(train_rows)}`",
        f"- Validation records: `{len(validation_rows)}`",
        f"- Test records: `{len(test_rows)}`",
        f"- Train label distribution: `{dict(Counter(labels(train_rows)))}`",
        f"- Validation label distribution: `{dict(Counter(labels(validation_rows)))}`",
        f"- Test label distribution: `{dict(Counter(labels(test_rows)))}`",
        f"- Best saved model: `{model_output}`",
        f"- Best model: `{best['model_name']}`",
        f"- Best feature set: `{best['feature_set']}`",
        f"- Best input mode: `{best['input_mode']}`",
        "- Best model selection: validation MCC, with validation balanced accuracy and F1 as tie-breakers.",
        "- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.",
        f"- Calibrated LinearSVC included: `{include_calibrated}`",
        "",
        "## Best Test Result",
        "",
        f"- Accuracy: `{pct(best_test['accuracy'])}`",
        f"- Precision: `{pct(best_test['precision'])}`",
        f"- Recall: `{pct(best_test['recall'])}`",
        f"- F1: `{pct(best_test['f1'])}`",
        f"- FPR: `{pct(best_test['false_positive_rate'])}`",
        f"- Specificity: `{pct(best_test['specificity'])}`",
        f"- Balanced accuracy: `{pct(best_test['balanced_accuracy'])}`",
        f"- MCC: `{best_test['mcc']:.4f}`",
        "",
        "## Validation Metrics",
        "",
        "| Model | Feature set | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines.extend(metric_line(result, "validation") for result in sorted(results, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]), reverse=True))
    lines.extend(
        [
            "",
            "## Test Metrics",
            "",
            "| Model | Feature set | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    lines.extend(metric_line(result, "test") for result in sorted(results, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]), reverse=True))
    lines.extend(
        [
            "",
            "## Per-Subset Test Metrics",
            "",
            "| Model | Feature set | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in sorted(results, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]), reverse=True):
        lines.extend(subset_lines(result))
    lines.extend(
        [
            "",
            "## Comparison Against Previous Best",
            "",
            "| System | Accuracy | F1 | FPR | MCC |",
            "| --- | ---: | ---: | ---: | ---: |",
            f"| Previous combined-validation best (`tfidf_linear_svc`, `old_comment_plus_code_diff`) | {pct(PREVIOUS_COMBINED['accuracy'])} | {pct(PREVIOUS_COMBINED['f1'])} | {pct(PREVIOUS_COMBINED['false_positive_rate'])} | {PREVIOUS_COMBINED['mcc']:.4f} |",
            f"| Classical v2 best (`{best['model_name']}`, `{best['feature_set']}`, `{best['input_mode']}`) | {pct(best_test['accuracy'])} | {pct(best_test['f1'])} | {pct(best_test['false_positive_rate'])} | {best_test['mcc']:.4f} |",
            "",
            "## Comparison Against Zero-Shot DocGuard",
            "",
            "| System | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            f"| Existing synthetic-trained DocGuard zero-shot | {pct(ZERO_SHOT['accuracy'])} | {pct(ZERO_SHOT['precision'])} | {pct(ZERO_SHOT['recall'])} | {pct(ZERO_SHOT['f1'])} | {pct(ZERO_SHOT['false_positive_rate'])} | {pct(ZERO_SHOT['specificity'])} | {pct(ZERO_SHOT['balanced_accuracy'])} | {ZERO_SHOT['mcc']:.4f} |",
            f"| Classical v2 best | {pct(best_test['accuracy'])} | {pct(best_test['precision'])} | {pct(best_test['recall'])} | {pct(best_test['f1'])} | {pct(best_test['false_positive_rate'])} | {pct(best_test['specificity'])} | {pct(best_test['balanced_accuracy'])} | {best_test['mcc']:.4f} |",
            "",
            "## Interpretation",
            "",
            "The v2 baseline is selected without test tuning. It should be reported as an external code-comment consistency proxy result and kept separate from the main DocGuard agent benchmark.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_blocked_report(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# External Deep-JIT Classical V2 Model Comparison 2026-08\n\nTraining blocked.\n\n```json\n" + json.dumps(result, indent=2) + "\n```\n", encoding="utf-8")


def train_and_evaluate_v2(
    train_path: Path,
    validation_path: Path,
    test_path: Path,
    model_output: Path,
    report_path: Path,
    max_features: int = 120_000,
    include_calibrated_svc: bool = False,
    limit_train: int | None = None,
    input_modes: list[str] | None = None,
    feature_sets: list[str] | None = None,
    model_names: list[str] | None = None,
) -> dict[str, Any]:
    train_rows = read_jsonl(train_path)
    validation_rows = read_jsonl(validation_path)
    test_rows = read_jsonl(test_path)
    if limit_train is not None:
        train_rows = train_rows[:limit_train]
    if not train_rows or not validation_rows or not test_rows:
        result = {
            "status": "blocked",
            "message": "train, validation, and test files are required",
            "train_records": len(train_rows),
            "validation_records": len(validation_rows),
            "test_records": len(test_rows),
        }
        write_blocked_report(report_path, result)
        return result

    selected_input_modes = input_modes or INPUT_MODES
    selected_feature_sets = feature_sets or FEATURE_SETS
    selected_model_names = model_names or (BASE_MODELS + (["calibrated_linear_svc"] if include_calibrated_svc else []))
    invalid_modes = sorted(set(selected_input_modes) - set(INPUT_MODES))
    invalid_features = sorted(set(selected_feature_sets) - set(FEATURE_SETS))
    valid_models = set(BASE_MODELS) | {"calibrated_linear_svc"}
    invalid_models = sorted(set(selected_model_names) - valid_models)
    if invalid_modes or invalid_features or invalid_models:
        result = {
            "status": "blocked",
            "message": "invalid v2 selection",
            "invalid_input_modes": invalid_modes,
            "invalid_feature_sets": invalid_features,
            "invalid_models": invalid_models,
        }
        write_blocked_report(report_path, result)
        return result
    y_train = labels(train_rows)
    y_validation = labels(validation_rows)
    y_test = labels(test_rows)
    results: list[dict[str, Any]] = []
    trained: list[dict[str, Any]] = []

    for mode in selected_input_modes:
        for feature_set in selected_feature_sets:
            features = feature_union(mode, feature_set, max_features)
            x_train = features.fit_transform(train_rows, y_train)
            x_validation = features.transform(validation_rows)
            x_test = features.transform(test_rows)
            for model_name in selected_model_names:
                clf = classifier(model_name)
                clf.fit(x_train, y_train)
                validation_pred, validation_scores, score_rule = matrix_predictions_and_scores(clf, x_validation)
                test_pred, test_scores, _ = matrix_predictions_and_scores(clf, x_test)
                model = Pipeline([("features", features), ("classifier", clf)])
                item = {
                    "model_name": model_name,
                    "feature_set": feature_set,
                    "input_mode": mode,
                    "score_rule": score_rule,
                    "validation": metric_values(y_validation, validation_pred, validation_scores),
                    "test": metric_values(y_test, test_pred, test_scores),
                    "test_by_subset": evaluate_by_subset(test_rows, test_pred, test_scores),
                    "model": model,
                }
                results.append({key: value for key, value in item.items() if key != "model"})
                trained.append(item)

    best = max(trained, key=lambda row: (row["validation"]["mcc"], row["validation"]["balanced_accuracy"], row["validation"]["f1"]))
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best["model"],
            "model_name": best["model_name"],
            "feature_set": best["feature_set"],
            "input_mode": best["input_mode"],
            "validation_metrics": best["validation"],
            "test_metrics": best["test"],
            "selection_rule": "validation MCC, then validation balanced accuracy, then validation F1",
            "label_polarity_status": "plausible_manual_verification_needed",
            "leakage_note": "Model inputs exclude new_comment_raw, doc_after, and doc_diff.",
        },
        model_output,
    )
    serializable_best = {key: value for key, value in best.items() if key != "model"}
    write_report(report_path, train_rows, validation_rows, test_rows, results, serializable_best, model_output, include_calibrated_svc)
    return {
        "status": "ok",
        "train_records": len(train_rows),
        "validation_records": len(validation_rows),
        "test_records": len(test_rows),
        "report": str(report_path),
        "model_output": str(model_output),
        "best_model": best["model_name"],
        "best_feature_set": best["feature_set"],
        "best_input_mode": best["input_mode"],
        "selection_metric": "validation_mcc",
        "best_validation_mcc": best["validation"]["mcc"],
        "best_test_accuracy": best["test"]["accuracy"],
        "best_test_precision": best["test"]["precision"],
        "best_test_recall": best["test"]["recall"],
        "best_test_f1": best["test"]["f1"],
        "best_test_false_positive_rate": best["test"]["false_positive_rate"],
        "best_test_specificity": best["test"]["specificity"],
        "best_test_balanced_accuracy": best["test"]["balanced_accuracy"],
        "best_test_mcc": best["test"]["mcc"],
    }
