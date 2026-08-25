from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MODULE_NAME = "scripts.train_real_gold_classifier_v3_strict_raw"
if __name__ == "__main__":
    sys.modules[MODULE_NAME] = sys.modules[__name__]

import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import FeatureUnion, Pipeline


SAFE_INPUT_FIELDS = [
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc

            if not isinstance(row, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")

            rows.append(row)

    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def gold_labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]

    if value is None:
        return []

    return [str(value)]


def normalize_text(value: Any) -> str:
    return str(value or "").replace("\x00", " ")


def normalize_path(path: str) -> str:
    normalized = path.strip().replace("\\", "/").lower()
    normalized = re.sub(r"/+", "/", normalized)
    return normalized


def raw_path_tokens(path: str) -> list[str]:
    normalized = normalize_path(path)
    parts = re.split(r"[/_.\-:@]+", normalized)
    return [part for part in parts if part]


def file_extension(path: str) -> str:
    normalized = normalize_path(path)
    name = normalized.rsplit("/", 1)[-1]

    if "." not in name:
        return "no_ext"

    return name.rsplit(".", 1)[-1]


def build_raw_path_text(row: dict[str, Any], *, heavy: bool = False) -> str:
    """
    Strict raw path representation.

    This intentionally does NOT create manual path flags such as:
    - path_flag_api_route
    - path_flag_schema_contract
    - path_flag_configuration
    - path_flag_cli
    - path_flag_test_or_fixture

    The model receives only lexical tokens derived from the actual file paths.
    """
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    files = safe_list(row.get("code_changed_files"))

    tokens: list[str] = [f"language_{language}"]

    for path in files:
        normalized = normalize_path(path)
        if not normalized:
            continue

        tokens.append(f"path_exact_{normalized}")
        tokens.append(f"path_ext_{file_extension(normalized)}")

        for token in raw_path_tokens(normalized):
            tokens.append(f"path_token_{token}")

        directories = normalized.split("/")[:-1]
        for directory in directories:
            if directory:
                tokens.append(f"path_dir_{directory}")

    text = " ".join(tokens)

    if heavy:
        return " ".join([text, text, text])

    return text


def build_full_raw_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    code_files = " ".join(safe_list(row.get("code_changed_files")))
    code_diff = normalize_text(row.get("code_diff_excerpt"))
    docs_before = normalize_text(row.get("docs_before_excerpt"))
    path_raw = build_raw_path_text(row, heavy=False)

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
            f"raw_path_text: {path_raw}",
            "code_diff_excerpt:",
            code_diff,
            "docs_before_excerpt:",
            docs_before,
        ]
    )


def build_code_only_raw_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    code_files = " ".join(safe_list(row.get("code_changed_files")))
    code_diff = normalize_text(row.get("code_diff_excerpt"))
    path_raw = build_raw_path_text(row, heavy=False)

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
            f"raw_path_text: {path_raw}",
            "code_diff_excerpt:",
            code_diff,
        ]
    )


def build_docs_before_raw_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    docs_before = normalize_text(row.get("docs_before_excerpt"))

    return "\n".join(
        [
            f"language: {language}",
            "docs_before_excerpt:",
            docs_before,
        ]
    )


class RawTextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str = "full") -> None:
        self.mode = mode

    def fit(self, X: list[dict[str, Any]], y: list[int] | None = None) -> "RawTextTransformer":
        return self

    def transform(self, X: list[dict[str, Any]]) -> list[str]:
        if self.mode == "full":
            return [build_full_raw_text(row) for row in X]

        if self.mode == "code":
            return [build_code_only_raw_text(row) for row in X]

        if self.mode == "docs_before":
            return [build_docs_before_raw_text(row) for row in X]

        if self.mode == "path_raw":
            return [build_raw_path_text(row, heavy=False) for row in X]

        if self.mode == "path_raw_heavy":
            return [build_raw_path_text(row, heavy=True) for row in X]

        raise ValueError(f"Unsupported text transformer mode: {self.mode}")


RawTextTransformer.__module__ = MODULE_NAME


def word_tfidf_raw(mode: str = "full", *, max_features: int = 80_000) -> Pipeline:
    return Pipeline(
        [
            ("text", RawTextTransformer(mode=mode)),
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.98,
                    max_features=max_features,
                    sublinear_tf=True,
                    strip_accents="unicode",
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def char_tfidf_raw(mode: str = "full", *, max_features: int = 100_000) -> Pipeline:
    return Pipeline(
        [
            ("text", RawTextTransformer(mode=mode)),
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    min_df=2,
                    max_features=max_features,
                    sublinear_tf=True,
                ),
            ),
        ]
    )


def path_tfidf_raw(*, heavy: bool = False, max_features: int = 50_000) -> Pipeline:
    mode = "path_raw_heavy" if heavy else "path_raw"

    return Pipeline(
        [
            ("text", RawTextTransformer(mode=mode)),
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 3),
                    min_df=1,
                    max_features=max_features,
                    sublinear_tf=True,
                    strip_accents="unicode",
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def make_logreg(
    *,
    class_weight: str | None,
    c_value: float,
    seed: int,
) -> LogisticRegression:
    return LogisticRegression(
        C=c_value,
        class_weight=class_weight,
        max_iter=5000,
        random_state=seed,
        solver="liblinear",
    )


def make_model_candidates(seed: int) -> dict[str, Pipeline]:
    """
    Strict-raw binary candidates.

    All candidates are ML-only:
    - no manual path flags
    - no rule-based routing
    - no docs-after input
    - no source URL / PR title / gold label input
    - no locked-test selection
    """
    candidates: dict[str, Pipeline] = {}
    c_values = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

    for c_value in c_values:
        candidates[f"word_logreg_c{c_value}"] = Pipeline(
            [
                ("features", word_tfidf_raw("full", max_features=100_000)),
                ("classifier", make_logreg(class_weight=None, c_value=c_value, seed=seed)),
            ]
        )

        candidates[f"word_logreg_balanced_c{c_value}"] = Pipeline(
            [
                ("features", word_tfidf_raw("full", max_features=100_000)),
                ("classifier", make_logreg(class_weight="balanced", c_value=c_value, seed=seed)),
            ]
        )

        candidates[f"word_char_logreg_balanced_c{c_value}"] = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf_raw("full", max_features=90_000)),
                            ("char", char_tfidf_raw("full", max_features=110_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(class_weight="balanced", c_value=c_value, seed=seed)),
            ]
        )

        candidates[f"path_raw_word_char_logreg_balanced_c{c_value}"] = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf_raw("full", max_features=80_000)),
                            ("char", char_tfidf_raw("full", max_features=100_000)),
                            ("path_raw", path_tfidf_raw(heavy=True, max_features=60_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(class_weight="balanced", c_value=c_value, seed=seed)),
            ]
        )

        candidates[f"code_docs_path_raw_logreg_balanced_c{c_value}"] = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("code_word", word_tfidf_raw("code", max_features=70_000)),
                            ("docs_word", word_tfidf_raw("docs_before", max_features=40_000)),
                            ("full_char", char_tfidf_raw("full", max_features=90_000)),
                            ("path_raw", path_tfidf_raw(heavy=True, max_features=60_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(class_weight="balanced", c_value=c_value, seed=seed)),
            ]
        )

    return candidates


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def matthews_corrcoef_binary(tp: int, fp: int, tn: int, fn: int) -> float:
    denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    if denominator == 0:
        return 0.0

    return ((tp * tn) - (fp * fn)) / denominator


def compute_metrics_from_labels(y_true: list[int], y_pred: list[int]) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for gold, pred in zip(y_true, y_pred):
        if gold == 1 and pred == 1:
            tp += 1
        elif gold == 0 and pred == 1:
            fp += 1
        elif gold == 0 and pred == 0:
            tn += 1
        elif gold == 1 and pred == 0:
            fn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)
    balanced_accuracy = (recall + specificity) / 2

    return {
        "total_cases": len(y_true),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": safe_div(tp + tn, len(y_true)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "balanced_accuracy": balanced_accuracy,
        "mcc": matthews_corrcoef_binary(tp=tp, fp=fp, tn=tn, fn=fn),
        "gold_distribution": dict(Counter(str(bool(value)) for value in y_true)),
        "pred_distribution": dict(Counter(str(bool(value)) for value in y_pred)),
    }


def ranking_metrics(y_true: list[int], probabilities: list[float]) -> dict[str, float | None]:
    if len(set(y_true)) < 2:
        return {
            "roc_auc": None,
            "average_precision": None,
        }

    return {
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "average_precision": float(average_precision_score(y_true, probabilities)),
    }


def metrics_at_threshold(
    y_true: list[int],
    probabilities: list[float],
    threshold: float,
) -> dict[str, Any]:
    y_pred = [1 if probability >= threshold else 0 for probability in probabilities]
    metrics = compute_metrics_from_labels(y_true, y_pred)
    metrics["threshold"] = threshold
    metrics.update(ranking_metrics(y_true, probabilities))
    return metrics


def objective_key(
    metrics: dict[str, Any],
    *,
    objective: str,
    min_precision: float,
    min_specificity: float,
) -> tuple[float, ...]:
    if objective == "constrained_f1":
        satisfies_constraints = (
            metrics["precision"] >= min_precision
            and metrics["specificity"] >= min_specificity
        )

        return (
            1.0 if satisfies_constraints else 0.0,
            metrics["f1"],
            metrics["mcc"],
            metrics["precision"],
            metrics["recall"],
            metrics["specificity"],
            metrics["balanced_accuracy"],
        )

    if objective == "mcc":
        return (
            metrics["mcc"],
            metrics["balanced_accuracy"],
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["specificity"],
        )

    if objective == "f1":
        return (
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["mcc"],
            metrics["specificity"],
        )

    if objective == "balanced_accuracy":
        return (
            metrics["balanced_accuracy"],
            metrics["mcc"],
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["specificity"],
        )

    raise ValueError(f"Unsupported selection objective: {objective}")


def select_threshold(
    *,
    y_true: list[int],
    probabilities: list[float],
    objective: str,
    min_precision: float,
    min_specificity: float,
) -> dict[str, Any]:
    candidates = [round(value / 100, 2) for value in range(5, 96, 5)]

    scored = [
        metrics_at_threshold(y_true, probabilities, threshold)
        for threshold in candidates
    ]

    best = max(
        scored,
        key=lambda item: objective_key(
            item,
            objective=objective,
            min_precision=min_precision,
            min_specificity=min_specificity,
        ),
    )

    constrained_candidates = [
        item
        for item in scored
        if item["precision"] >= min_precision
        and item["specificity"] >= min_specificity
    ]

    return {
        "objective": objective,
        "selected_threshold": best["threshold"],
        "selected_validation_metrics": best,
        "validation_sweep": scored,
        "constraints": {
            "min_precision": min_precision,
            "min_specificity": min_specificity,
            "satisfied_by_selected": (
                best["precision"] >= min_precision
                and best["specificity"] >= min_specificity
            ),
            "number_of_thresholds_satisfying_constraints": len(constrained_candidates),
        },
    }


def predict_positive_probability(model: Pipeline, rows: list[dict[str, Any]]) -> list[float]:
    probabilities = model.predict_proba(rows)
    classifier = model.named_steps["classifier"]
    classes = list(classifier.classes_)

    if 1 not in classes:
        raise ValueError(f"Trained model classes do not contain positive label 1: {classes}")

    positive_index = classes.index(1)

    return [float(item[positive_index]) for item in probabilities]


def evaluate_model(
    *,
    model_name: str,
    model: Pipeline,
    train_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    locked_test_rows: list[dict[str, Any]],
    selection_objective: str,
    min_precision: float,
    min_specificity: float,
) -> dict[str, Any]:
    y_train = gold_labels(train_rows)
    y_validation = gold_labels(validation_rows)
    y_locked_test = gold_labels(locked_test_rows)

    model.fit(train_rows, y_train)

    train_probabilities = predict_positive_probability(model, train_rows)
    validation_probabilities = predict_positive_probability(model, validation_rows)
    locked_test_probabilities = predict_positive_probability(model, locked_test_rows)

    threshold_selection = select_threshold(
        y_true=y_validation,
        probabilities=validation_probabilities,
        objective=selection_objective,
        min_precision=min_precision,
        min_specificity=min_specificity,
    )

    threshold = float(threshold_selection["selected_threshold"])

    metrics_by_split = {
        "train": metrics_at_threshold(y_train, train_probabilities, threshold),
        "validation": metrics_at_threshold(y_validation, validation_probabilities, threshold),
        "locked_test": metrics_at_threshold(y_locked_test, locked_test_probabilities, threshold),
    }

    return {
        "model_name": model_name,
        "threshold": threshold,
        "threshold_selection": threshold_selection,
        "metrics_by_split": metrics_by_split,
    }


def model_selection_key(result: dict[str, Any]) -> tuple[float, ...]:
    validation = result["metrics_by_split"]["validation"]
    constraints = result["threshold_selection"]["constraints"]

    return (
        1.0 if constraints["satisfied_by_selected"] else 0.0,
        validation["f1"],
        validation["mcc"],
        validation["precision"],
        validation["recall"],
        validation["specificity"],
        validation["balanced_accuracy"],
    )


def build_prediction_rows(
    *,
    model_name: str,
    threshold: float,
    train_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    locked_test_rows: list[dict[str, Any]],
    train_probabilities: list[float],
    validation_probabilities: list[float],
    locked_test_probabilities: list[float],
    selection_objective: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for split, rows, probabilities in [
        ("train", train_rows, train_probabilities),
        ("validation", validation_rows, validation_probabilities),
        ("locked_test", locked_test_rows, locked_test_probabilities),
    ]:
        for row, probability in zip(rows, probabilities):
            gold = bool_value(row.get("gold_docs_update_required"))
            pred = probability >= threshold

            output.append(
                {
                    "case_id": row.get("case_id"),
                    "repository": row.get("repository"),
                    "language": row.get("language"),
                    "dataset_split": split,
                    "gold_docs_update_required": gold,
                    "pred_docs_update_required": pred,
                    "binary_correct": pred == gold,
                    "pred_probability": probability,
                    "selected_threshold": threshold,
                    "selected_model_name": model_name,
                    "selection_objective": selection_objective,
                    "source_url": row.get("source_url"),
                    "code_changed_files": row.get("code_changed_files"),
                }
            )

    return output


def write_model_comparison_md(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Real Gold Classifier V3 Strict-Raw Model Comparison",
        "",
        f"- Selection objective: `{report['selection_objective']}`",
        f"- Best model: `{report['best_model_name']}`",
        f"- Best threshold: `{report['best_threshold']}`",
        "",
        "## Strict ML-only input policy",
        "",
        "The V3 strict-raw comparison uses only the following model input fields:",
        "",
    ]

    for field in SAFE_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "No manual `path_flag_*` features are used.",
            "",
            "Raw file paths are represented only as lexical tokens derived from `code_changed_files`.",
            "",
            "Audit-only fields such as `docs_after_excerpt`, `docs_diff_excerpt`, `source_url`, `pr_title`, `manual_label_notes`, and gold labels are not used as model input.",
            "",
            "Threshold selection and model selection use validation split only. Locked-test is used only for final reporting.",
            "",
            "## Model comparison",
            "",
            "| Model | Threshold | Val F1 | Val MCC | Val Precision | Val Recall | Val Specificity | Locked F1 | Locked Precision | Locked Recall | Locked Specificity | Locked MCC | Locked ROC AUC |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for result in report["model_results"]:
        validation = result["metrics_by_split"]["validation"]
        locked = result["metrics_by_split"]["locked_test"]

        lines.append(
            "| "
            f"{result['model_name']} | "
            f"{result['threshold']:.2f} | "
            f"{validation['f1']:.4f} | "
            f"{validation['mcc']:.4f} | "
            f"{validation['precision']:.4f} | "
            f"{validation['recall']:.4f} | "
            f"{validation['specificity']:.4f} | "
            f"{locked['f1']:.4f} | "
            f"{locked['precision']:.4f} | "
            f"{locked['recall']:.4f} | "
            f"{locked['specificity']:.4f} | "
            f"{locked['mcc']:.4f} | "
            f"{locked['roc_auc']:.4f} |"
        )

    best_locked = report["best_model_metrics_by_split"]["locked_test"]

    lines.extend(
        [
            "",
            "## Selected V3 result on locked test",
            "",
            f"- Accuracy: `{best_locked['accuracy']:.4f}`",
            f"- Precision: `{best_locked['precision']:.4f}`",
            f"- Recall: `{best_locked['recall']:.4f}`",
            f"- F1: `{best_locked['f1']:.4f}`",
            f"- Specificity: `{best_locked['specificity']:.4f}`",
            f"- False positive rate: `{best_locked['false_positive_rate']:.4f}`",
            f"- Balanced accuracy: `{best_locked['balanced_accuracy']:.4f}`",
            f"- MCC: `{best_locked['mcc']:.4f}`",
            f"- ROC AUC: `{best_locked['roc_auc']:.4f}`",
            f"- Average precision: `{best_locked['average_precision']:.4f}`",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    train_path: Path,
    validation_path: Path,
    locked_test_path: Path,
    output_dir: Path,
    model_output: Path,
    selection_objective: str,
    min_precision: float,
    min_specificity: float,
    seed: int,
) -> dict[str, Any]:
    train_rows = load_jsonl(train_path)
    validation_rows = load_jsonl(validation_path)
    locked_test_rows = load_jsonl(locked_test_path)

    if not train_rows:
        raise ValueError("Train split is empty.")
    if not validation_rows:
        raise ValueError("Validation split is empty.")
    if not locked_test_rows:
        raise ValueError("Locked-test split is empty.")

    models = make_model_candidates(seed=seed)
    model_results: list[dict[str, Any]] = []
    fitted_models: dict[str, Pipeline] = {}

    for model_name, model in models.items():
        print(f"=== Training {model_name} ===")

        result = evaluate_model(
            model_name=model_name,
            model=model,
            train_rows=train_rows,
            validation_rows=validation_rows,
            locked_test_rows=locked_test_rows,
            selection_objective=selection_objective,
            min_precision=min_precision,
            min_specificity=min_specificity,
        )

        model_results.append(result)
        fitted_models[model_name] = model

        validation = result["metrics_by_split"]["validation"]
        locked = result["metrics_by_split"]["locked_test"]

        print(
            json.dumps(
                {
                    "model_name": model_name,
                    "threshold": result["threshold"],
                    "validation_f1": validation["f1"],
                    "validation_precision": validation["precision"],
                    "validation_recall": validation["recall"],
                    "validation_specificity": validation["specificity"],
                    "validation_mcc": validation["mcc"],
                    "locked_f1": locked["f1"],
                    "locked_precision": locked["precision"],
                    "locked_recall": locked["recall"],
                    "locked_specificity": locked["specificity"],
                    "locked_mcc": locked["mcc"],
                    "locked_roc_auc": locked["roc_auc"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    best = max(model_results, key=model_selection_key)
    best_model_name = str(best["model_name"])
    best_model = fitted_models[best_model_name]
    best_threshold = float(best["threshold"])

    y_train = gold_labels(train_rows)
    y_validation = gold_labels(validation_rows)
    y_locked_test = gold_labels(locked_test_rows)

    train_probabilities = predict_positive_probability(best_model, train_rows)
    validation_probabilities = predict_positive_probability(best_model, validation_rows)
    locked_test_probabilities = predict_positive_probability(best_model, locked_test_rows)

    best_model_metrics_by_split = {
        "train": metrics_at_threshold(y_train, train_probabilities, best_threshold),
        "validation": metrics_at_threshold(y_validation, validation_probabilities, best_threshold),
        "locked_test": metrics_at_threshold(y_locked_test, locked_test_probabilities, best_threshold),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    model_output.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "model": str(model_output),
        "summary_json": str(output_dir / "best_model_summary.json"),
        "model_comparison_json": str(output_dir / "model_comparison.json"),
        "model_comparison_md": str(output_dir / "model_comparison.md"),
        "predictions_jsonl": str(output_dir / "best_model_predictions.jsonl"),
    }

    report = {
        "status": "ok",
        "model_version": "binary_v3_strict_raw",
        "selection_objective": selection_objective,
        "best_model_name": best_model_name,
        "best_threshold": best_threshold,
        "best_model_metrics_by_split": best_model_metrics_by_split,
        "best_threshold_selection": best["threshold_selection"],
        "model_results": model_results,
        "safe_input_fields": SAFE_INPUT_FIELDS,
        "row_counts": {
            "train": len(train_rows),
            "validation": len(validation_rows),
            "locked_test": len(locked_test_rows),
        },
        "class_distribution": {
            "train": dict(Counter(str(bool(value)) for value in y_train)),
            "validation": dict(Counter(str(bool(value)) for value in y_validation)),
            "locked_test": dict(Counter(str(bool(value)) for value in y_locked_test)),
        },
        "ml_only_policy": {
            "uses_rule_based_classifier": False,
            "uses_manual_path_flags": False,
            "uses_raw_paths_as_text": True,
            "uses_docs_after_as_input": False,
            "uses_gold_labels_as_input": False,
            "uses_source_url_as_input": False,
            "uses_pr_title_as_input": False,
            "uses_locked_test_for_model_selection": False,
            "threshold_selection_split": "validation",
            "model_selection_split": "validation",
        },
        "outputs": outputs,
    }

    prediction_rows = build_prediction_rows(
        model_name=best_model_name,
        threshold=best_threshold,
        train_rows=train_rows,
        validation_rows=validation_rows,
        locked_test_rows=locked_test_rows,
        train_probabilities=train_probabilities,
        validation_probabilities=validation_probabilities,
        locked_test_probabilities=locked_test_probabilities,
        selection_objective=selection_objective,
    )

    joblib.dump(
        {
            "model_type": "binary_v3_strict_raw",
            "model": best_model,
            "threshold": best_threshold,
            "best_model_name": best_model_name,
            "selection_objective": selection_objective,
            "safe_input_fields": SAFE_INPUT_FIELDS,
            "ml_only_policy": report["ml_only_policy"],
        },
        model_output,
    )

    write_json(Path(outputs["summary_json"]), report)
    write_json(Path(outputs["model_comparison_json"]), report)
    write_jsonl(Path(outputs["predictions_jsonl"]), prediction_rows)
    write_model_comparison_md(Path(outputs["model_comparison_md"]), report)

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train strict-raw ML-only binary documentation-update classifier."
    )
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument(
        "--selection-objective",
        default="constrained_f1",
        choices=["constrained_f1", "mcc", "f1", "balanced_accuracy"],
    )
    parser.add_argument("--min-precision", type=float, default=0.90)
    parser.add_argument("--min-specificity", type=float, default=0.60)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        output_dir=Path(args.output_dir),
        model_output=Path(args.model_output),
        selection_objective=args.selection_objective,
        min_precision=args.min_precision,
        min_specificity=args.min_specificity,
        seed=args.seed,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())