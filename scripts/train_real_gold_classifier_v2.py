from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC


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


def split_path_tokens(path: str) -> list[str]:
    normalized = normalize_path(path)
    parts = re.split(r"[/_.\-:@]+", normalized)
    return [part for part in parts if part]


def file_extension(path: str) -> str:
    normalized = normalize_path(path)
    name = normalized.rsplit("/", 1)[-1]

    if "." not in name:
        return "no_ext"

    return name.rsplit(".", 1)[-1]


def path_flags(path: str) -> list[str]:
    normalized = normalize_path(path)
    tokens = split_path_tokens(normalized)
    joined = " ".join(tokens)

    flags: list[str] = []

    if any(token in {"test", "tests", "spec", "fixture", "fixtures", "mock", "mocks"} for token in tokens):
        flags.append("path_flag_test_or_fixture")

    if any(token in {"api", "apis", "endpoint", "endpoints", "route", "routes", "router"} for token in tokens):
        flags.append("path_flag_api_route")

    if any(token in {"schema", "schemas", "model", "models", "types", "typing", "interface", "interfaces"} for token in tokens):
        flags.append("path_flag_schema_contract")

    if any(token in {"config", "configs", "configuration", "settings", "env", "option", "options"} for token in tokens):
        flags.append("path_flag_configuration")

    if any(token in {"cli", "command", "commands", "bin"} for token in tokens):
        flags.append("path_flag_cli")

    if any(token in {"auth", "security", "permission", "permissions", "token", "jwt", "oauth"} for token in tokens):
        flags.append("path_flag_auth_security")

    if any(token in {"migration", "migrations", "database", "db", "sql"} for token in tokens):
        flags.append("path_flag_database_migration")

    if any(token in {"ui", "component", "components", "page", "pages", "view", "views"} for token in tokens):
        flags.append("path_flag_ui")

    if "readme" in joined or "docs" in tokens or "documentation" in tokens:
        flags.append("path_flag_docs_path")

    return flags


def build_path_text(row: dict[str, Any], *, heavy: bool = False) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    files = safe_list(row.get("code_changed_files"))

    tokens: list[str] = [f"language_{language}"]

    for path in files:
        normalized = normalize_path(path)
        extension = file_extension(normalized)
        path_tokens = split_path_tokens(normalized)

        tokens.append(f"path_exact_{normalized}")
        tokens.append(f"path_ext_{extension}")

        for token in path_tokens:
            tokens.append(f"path_token_{token}")

        for flag in path_flags(normalized):
            tokens.append(flag)

        directories = normalized.split("/")[:-1]
        for directory in directories:
            if directory:
                tokens.append(f"path_dir_{directory}")

    text = " ".join(tokens)

    if heavy:
        return " ".join([text, text, text])

    return text


def build_full_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    code_files = " ".join(safe_list(row.get("code_changed_files")))
    code_diff = normalize_text(row.get("code_diff_excerpt"))
    docs_before = normalize_text(row.get("docs_before_excerpt"))

    path_text = build_path_text(row, heavy=False)

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
            f"path_features: {path_text}",
            "code_diff_excerpt:",
            code_diff,
            "docs_before_excerpt:",
            docs_before,
        ]
    )


def build_code_only_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    code_files = " ".join(safe_list(row.get("code_changed_files")))
    code_diff = normalize_text(row.get("code_diff_excerpt"))

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
            "code_diff_excerpt:",
            code_diff,
        ]
    )


def build_docs_before_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    docs_before = normalize_text(row.get("docs_before_excerpt"))

    return "\n".join(
        [
            f"language: {language}",
            "docs_before_excerpt:",
            docs_before,
        ]
    )


class RowTextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str = "full") -> None:
        self.mode = mode

    def fit(self, X: list[dict[str, Any]], y: list[int] | None = None) -> "RowTextTransformer":
        return self

    def transform(self, X: list[dict[str, Any]]) -> list[str]:
        if self.mode == "full":
            return [build_full_text(row) for row in X]

        if self.mode == "code":
            return [build_code_only_text(row) for row in X]

        if self.mode == "docs_before":
            return [build_docs_before_text(row) for row in X]

        if self.mode == "path":
            return [build_path_text(row, heavy=False) for row in X]

        if self.mode == "path_heavy":
            return [build_path_text(row, heavy=True) for row in X]

        raise ValueError(f"Unsupported text transformer mode: {self.mode}")


def word_tfidf(mode: str = "full", *, max_features: int = 80_000) -> Pipeline:
    return Pipeline(
        [
            ("text", RowTextTransformer(mode=mode)),
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.98,
                    max_features=max_features,
                    sublinear_tf=True,
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def char_tfidf(mode: str = "full", *, max_features: int = 100_000) -> Pipeline:
    return Pipeline(
        [
            ("text", RowTextTransformer(mode=mode)),
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


def path_tfidf(*, heavy: bool = False, max_features: int = 40_000) -> Pipeline:
    return Pipeline(
        [
            ("text", RowTextTransformer(mode="path_heavy" if heavy else "path")),
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 3),
                    min_df=1,
                    max_features=max_features,
                    sublinear_tf=True,
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def make_logreg(*, class_weight: str | None = None, c_value: float = 1.0, seed: int = 42) -> LogisticRegression:
    return LogisticRegression(
        C=c_value,
        class_weight=class_weight,
        max_iter=3000,
        random_state=seed,
        solver="liblinear",
    )


def make_calibrated_linear_svc(*, class_weight: str | None = None, seed: int = 42) -> CalibratedClassifierCV:
    svc = LinearSVC(
        C=1.0,
        class_weight=class_weight,
        max_iter=5000,
        random_state=seed,
    )

    try:
        return CalibratedClassifierCV(estimator=svc, method="sigmoid", cv=3)
    except TypeError:
        return CalibratedClassifierCV(base_estimator=svc, method="sigmoid", cv=3)


def make_model_candidates(seed: int) -> dict[str, Pipeline]:
    return {
        "word_logreg": Pipeline(
            [
                ("features", word_tfidf("full")),
                ("classifier", make_logreg(seed=seed)),
            ]
        ),
        "word_logreg_balanced": Pipeline(
            [
                ("features", word_tfidf("full")),
                ("classifier", make_logreg(class_weight="balanced", seed=seed)),
            ]
        ),
        "char_logreg": Pipeline(
            [
                ("features", char_tfidf("full")),
                ("classifier", make_logreg(seed=seed)),
            ]
        ),
        "word_char_logreg": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(seed=seed)),
            ]
        ),
        "word_char_logreg_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(class_weight="balanced", seed=seed)),
            ]
        ),
        "path_heavy_word_char_logreg": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=60_000)),
                            ("char", char_tfidf("full", max_features=70_000)),
                            ("path", path_tfidf(heavy=True, max_features=40_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(seed=seed)),
            ]
        ),
        "path_heavy_word_char_logreg_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=60_000)),
                            ("char", char_tfidf("full", max_features=70_000)),
                            ("path", path_tfidf(heavy=True, max_features=40_000)),
                        ]
                    ),
                ),
                ("classifier", make_logreg(class_weight="balanced", seed=seed)),
            ]
        ),
        "linear_svc_word_char": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                        ]
                    ),
                ),
                ("classifier", make_calibrated_linear_svc(seed=seed)),
            ]
        ),
        "linear_svc_word_char_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                        ]
                    ),
                ),
                ("classifier", make_calibrated_linear_svc(class_weight="balanced", seed=seed)),
            ]
        ),
    }


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


def metrics_at_threshold(
    y_true: list[int],
    probabilities: list[float],
    threshold: float,
) -> dict[str, Any]:
    y_pred = [1 if probability >= threshold else 0 for probability in probabilities]
    metrics = compute_metrics_from_labels(y_true, y_pred)
    metrics["threshold"] = threshold
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
        if item["precision"] >= min_precision and item["specificity"] >= min_specificity
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
    classes = list(model.classes_)

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

            copied = dict(row)
            copied["dataset_split"] = split
            copied["selected_model_name"] = model_name
            copied["selection_objective"] = selection_objective
            copied["pred_probability"] = probability
            copied["pred_docs_update_required"] = pred
            copied["swept_threshold"] = threshold
            copied["swept_pred_docs_update_required"] = pred
            copied["swept_binary_correct"] = pred == gold

            output.append(copied)

    return output


def write_model_comparison_md(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Real Gold Classifier V2 Model Comparison",
        "",
        f"- Selection objective: `{report['selection_objective']}`",
        f"- Best model: `{report['best_model_name']}`",
        f"- Best threshold: `{report['best_threshold']}`",
        "",
        "## Leakage policy",
        "",
        "The V2 comparison uses only the following model input fields:",
        "",
    ]

    for field in SAFE_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "Audit-only fields such as `docs_after_excerpt`, `docs_diff_excerpt`, `source_url`, `pr_title`, "
            "`manual_label_notes`, and gold labels are not used as model input.",
            "",
            "## Model comparison",
            "",
            "| Model | Threshold | Val F1 | Val MCC | Val Precision | Val Recall | Val Specificity | Locked F1 | Locked Precision | Locked Recall | Locked Specificity | Locked MCC |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
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
            f"{locked['mcc']:.4f} |"
        )

    best_locked = report["best_model_metrics_by_split"]["locked_test"]

    lines.extend(
        [
            "",
            "## Selected V2 result on locked test",
            "",
            f"- Accuracy: `{best_locked['accuracy']:.4f}`",
            f"- Precision: `{best_locked['precision']:.4f}`",
            f"- Recall: `{best_locked['recall']:.4f}`",
            f"- F1: `{best_locked['f1']:.4f}`",
            f"- Specificity: `{best_locked['specificity']:.4f}`",
            f"- False positive rate: `{best_locked['false_positive_rate']:.4f}`",
            f"- Balanced accuracy: `{best_locked['balanced_accuracy']:.4f}`",
            f"- MCC: `{best_locked['mcc']:.4f}`",
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

        locked = result["metrics_by_split"]["locked_test"]
        print(
            json.dumps(
                {
                    "model_name": model_name,
                    "threshold": result["threshold"],
                    "locked_f1": locked["f1"],
                    "locked_precision": locked["precision"],
                    "locked_recall": locked["recall"],
                    "locked_specificity": locked["specificity"],
                    "locked_mcc": locked["mcc"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    best_result = max(model_results, key=model_selection_key)
    best_model_name = str(best_result["model_name"])
    best_threshold = float(best_result["threshold"])

    print(f"=== Refitting selected model: {best_model_name} ===")

    best_model = make_model_candidates(seed=seed)[best_model_name]
    y_train = gold_labels(train_rows)
    best_model.fit(train_rows, y_train)

    train_probabilities = predict_positive_probability(best_model, train_rows)
    validation_probabilities = predict_positive_probability(best_model, validation_rows)
    locked_test_probabilities = predict_positive_probability(best_model, locked_test_rows)

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

    output_dir.mkdir(parents=True, exist_ok=True)
    model_output.parent.mkdir(parents=True, exist_ok=True)

    best_predictions_path = output_dir / "best_model_predictions.jsonl"
    best_summary_path = output_dir / "best_model_summary.json"
    comparison_json_path = output_dir / "model_comparison.json"
    comparison_md_path = output_dir / "model_comparison.md"

    report = {
        "status": "ok",
        "train": str(train_path),
        "validation": str(validation_path),
        "locked_test": str(locked_test_path),
        "safe_input_fields": SAFE_INPUT_FIELDS,
        "selection_objective": selection_objective,
        "constraints": {
            "min_precision": min_precision,
            "min_specificity": min_specificity,
        },
        "split_sizes": {
            "train": len(train_rows),
            "validation": len(validation_rows),
            "locked_test": len(locked_test_rows),
        },
        "best_model_name": best_model_name,
        "best_threshold": best_threshold,
        "best_model_metrics_by_split": best_result["metrics_by_split"],
        "best_threshold_selection": best_result["threshold_selection"],
        "model_results": model_results,
        "outputs": {
            "model_output": str(model_output),
            "best_model_predictions": str(best_predictions_path),
            "best_model_summary": str(best_summary_path),
            "model_comparison_json": str(comparison_json_path),
            "model_comparison_md": str(comparison_md_path),
        },
        "interpretation": {
            "rule": "All model variants are trained on train only. Model and threshold selection are based on validation. Locked test is used only for final reporting.",
            "leakage_policy": "Only language, code_changed_files, code_diff_excerpt, and docs_before_excerpt are used as model input.",
        },
    }

    joblib.dump(
        {
            "model": best_model,
            "model_name": best_model_name,
            "threshold": best_threshold,
            "selection_objective": selection_objective,
            "safe_input_fields": SAFE_INPUT_FIELDS,
            "report": report,
        },
        model_output,
    )

    write_jsonl(best_predictions_path, prediction_rows)
    write_json(best_summary_path, report)
    write_json(comparison_json_path, report)
    write_model_comparison_md(comparison_md_path, report)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Train and compare V2 real gold classifier variants.")
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument(
        "--selection-objective",
        choices=["constrained_f1", "mcc", "f1", "balanced_accuracy"],
        default="constrained_f1",
    )
    parser.add_argument("--min-precision", type=float, default=0.90)
    parser.add_argument("--min-specificity", type=float, default=0.60)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    report = run(
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

    print(
        json.dumps(
            {
                "status": report["status"],
                "best_model_name": report["best_model_name"],
                "best_threshold": report["best_threshold"],
                "best_model_metrics_by_split": report["best_model_metrics_by_split"],
                "outputs": report["outputs"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())