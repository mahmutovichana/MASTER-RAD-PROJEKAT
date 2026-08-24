from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MODULE_NAME = "scripts.train_real_doc_category_classifier_v4"
if __name__ == "__main__":
    sys.modules[MODULE_NAME] = sys.modules[__name__]

import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.pipeline import FeatureUnion, Pipeline


THESIS4_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

TARGET_CATEGORY_ALIASES = {
    "api": "api_reference",
    "api_endpoint": "api_reference",
    "api_endpoint_change": "api_reference",
    "api_reference": "api_reference",
    "endpoint": "api_reference",
    "request_response": "api_reference",
    "request_response_change": "api_reference",

    "configuration": "configuration",
    "configuration_change": "configuration",
    "config": "configuration",
    "settings": "configuration",
    "environment": "configuration",
    "env": "configuration",

    "developer_setup": "developer_setup",
    "setup": "developer_setup",
    "installation": "developer_setup",
    "install": "developer_setup",
    "cli": "developer_setup",
    "command": "developer_setup",
    "commands": "developer_setup",
    "testing": "developer_setup",
    "testing_instructions": "developer_setup",
    "testing_command_change": "developer_setup",
    "workflow": "developer_setup",
    "workflow_change": "developer_setup",
    "workflow_documentation": "developer_setup",
    "project_documentation": "developer_setup",

    "model_contract": "model_contract",
    "model": "model_contract",
    "data_model": "model_contract",
    "request_response_schema_change": "model_contract",
    "schema": "model_contract",
    "schemas": "model_contract",
    "type": "model_contract",
    "types": "model_contract",
    "interface": "model_contract",
    "interfaces": "model_contract",
    "contract": "model_contract",
    "security": "model_contract",
}

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


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


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


def normalize_category(value: Any) -> str | None:
    raw = str(value or "").strip().lower()

    if not raw or raw == "no_update" or raw == "not_available":
        return None

    normalized = TARGET_CATEGORY_ALIASES.get(raw, raw)

    if normalized in THESIS4_CATEGORIES:
        return normalized

    return None


def positive_category_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for row in rows:
        if not bool_value(row.get("gold_docs_update_required")):
            continue

        category = normalize_category(row.get("gold_doc_category"))

        if category is None:
            continue

        enriched = dict(row)
        enriched["category_label"] = category
        output.append(enriched)

    return output


def labels(rows: list[dict[str, Any]]) -> list[str]:
    return [str(row["category_label"]) for row in rows]


def build_full_raw_text(row: dict[str, Any]) -> str:
    language = normalize_text(row.get("language")).lower().strip() or "unknown"
    code_files = " ".join(safe_list(row.get("code_changed_files")))
    code_diff = normalize_text(row.get("code_diff_excerpt"))
    docs_before = normalize_text(row.get("docs_before_excerpt"))

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
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

    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
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


def build_raw_path_text(row: dict[str, Any], *, heavy: bool = False) -> str:
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


class RawTextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str = "full") -> None:
        self.mode = mode

    def fit(self, X: list[dict[str, Any]], y: list[str] | None = None) -> "RawTextTransformer":
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

        raise ValueError(f"Unsupported RawTextTransformer mode: {self.mode}")


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
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def make_logreg(
    *,
    c_value: float,
    class_weight: str | None,
    seed: int,
) -> LogisticRegression:
    return LogisticRegression(
        C=c_value,
        class_weight=class_weight,
        max_iter=5000,
        random_state=seed,
        solver="lbfgs",
    )


def make_category_model_candidates(seed: int) -> dict[str, Pipeline]:
    c_values = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    candidates: dict[str, Pipeline] = {}

    for c_value in c_values:
        candidates[f"word_logreg_c{c_value}"] = Pipeline(
            [
                ("features", word_tfidf_raw("full", max_features=100_000)),
                ("classifier", make_logreg(c_value=c_value, class_weight=None, seed=seed)),
            ]
        )

        candidates[f"word_logreg_balanced_c{c_value}"] = Pipeline(
            [
                ("features", word_tfidf_raw("full", max_features=100_000)),
                ("classifier", make_logreg(c_value=c_value, class_weight="balanced", seed=seed)),
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
                ("classifier", make_logreg(c_value=c_value, class_weight="balanced", seed=seed)),
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
                ("classifier", make_logreg(c_value=c_value, class_weight="balanced", seed=seed)),
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
                ("classifier", make_logreg(c_value=c_value, class_weight="balanced", seed=seed)),
            ]
        )

    return candidates


def per_class_metrics(y_true: list[str], y_pred: list[str]) -> dict[str, Any]:
    labels_sorted = sorted(THESIS4_CATEGORIES)

    report = classification_report(
        y_true,
        y_pred,
        labels=labels_sorted,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(y_true, y_pred, labels=labels_sorted)

    return {
        "labels": labels_sorted,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            labels=labels_sorted,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            y_true,
            y_pred,
            labels=labels_sorted,
            average="weighted",
            zero_division=0,
        ),
        "accuracy": safe_div(
            sum(1 for gold, pred in zip(y_true, y_pred) if gold == pred),
            len(y_true),
        ),
        "gold_distribution": dict(Counter(y_true)),
        "pred_distribution": dict(Counter(y_pred)),
    }


def predict_with_model(model: Pipeline, rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []

    return [str(item) for item in model.predict(rows)]


def predict_model_probabilities(
    model: Pipeline,
    rows: list[dict[str, Any]],
    labels_sorted: list[str],
) -> list[dict[str, float]]:
    if not rows:
        return []

    if not hasattr(model, "predict_proba"):
        predictions = predict_with_model(model, rows)
        return [
            {
                label: 1.0 if label == prediction else 0.0
                for label in labels_sorted
            }
            for prediction in predictions
        ]

    classifier = model.named_steps.get("classifier")
    classes = [str(item) for item in getattr(classifier, "classes_", [])]
    probabilities = model.predict_proba(rows)

    output: list[dict[str, float]] = []

    for row_probabilities in probabilities:
        raw = {
            category: float(probability)
            for category, probability in zip(classes, row_probabilities)
        }

        aligned = {
            category: float(raw.get(category, 0.0))
            for category in labels_sorted
        }

        total = sum(aligned.values())
        if total > 0:
            aligned = {key: value / total for key, value in aligned.items()}

        output.append(aligned)

    return output


def average_probability_maps(
    probability_sets: list[list[dict[str, float]]],
    *,
    labels_sorted: list[str],
    weights: list[float],
) -> list[dict[str, float]]:
    if not probability_sets:
        return []

    row_count = len(probability_sets[0])
    total_weight = sum(weights) if sum(weights) > 0 else float(len(weights))
    output: list[dict[str, float]] = []

    for row_index in range(row_count):
        combined = {label: 0.0 for label in labels_sorted}

        for model_index, model_probabilities in enumerate(probability_sets):
            weight = weights[model_index] if total_weight else 1.0
            row_probability = model_probabilities[row_index]

            for label in labels_sorted:
                combined[label] += weight * float(row_probability.get(label, 0.0))

        combined = {
            label: value / total_weight
            for label, value in combined.items()
        }

        total = sum(combined.values())
        if total > 0:
            combined = {label: value / total for label, value in combined.items()}

        output.append(combined)

    return output


def apply_class_multipliers(
    probability_maps: list[dict[str, float]],
    *,
    multipliers: dict[str, float],
    labels_sorted: list[str],
) -> list[dict[str, float]]:
    output: list[dict[str, float]] = []

    for probability_map in probability_maps:
        adjusted = {
            label: float(probability_map.get(label, 0.0)) * float(multipliers.get(label, 1.0))
            for label in labels_sorted
        }

        total = sum(adjusted.values())
        if total > 0:
            adjusted = {label: value / total for label, value in adjusted.items()}

        output.append(adjusted)

    return output


def labels_from_probabilities(
    probability_maps: list[dict[str, float]],
    *,
    labels_sorted: list[str],
) -> list[str]:
    predictions: list[str] = []

    for probability_map in probability_maps:
        predictions.append(
            max(
                labels_sorted,
                key=lambda label: float(probability_map.get(label, 0.0)),
            )
        )

    return predictions


def prediction_confidence(probability_map: dict[str, float], predicted_label: str) -> float | None:
    if not probability_map:
        return None

    return float(probability_map.get(predicted_label, 0.0))


def ranked_categories(probability_map: dict[str, float]) -> list[dict[str, float]]:
    return [
        {"category": category, "probability": probability}
        for category, probability in sorted(
            probability_map.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]


def model_selection_key(result: dict[str, Any]) -> tuple[float, ...]:
    validation = result["metrics_by_split"]["validation"]

    return (
        validation["macro_f1"],
        validation["weighted_f1"],
        validation["accuracy"],
    )


def optimize_class_multipliers(
    *,
    validation_probabilities: list[dict[str, float]],
    y_validation: list[str],
    labels_sorted: list[str],
    grid_values: list[float],
) -> dict[str, Any]:
    best_multipliers = {label: 1.0 for label in labels_sorted}
    best_predictions = labels_from_probabilities(
        apply_class_multipliers(
            validation_probabilities,
            multipliers=best_multipliers,
            labels_sorted=labels_sorted,
        ),
        labels_sorted=labels_sorted,
    )
    best_metrics = per_class_metrics(y_validation, best_predictions)
    best_key = (
        best_metrics["macro_f1"],
        best_metrics["weighted_f1"],
        best_metrics["accuracy"],
    )

    for values in itertools.product(grid_values, repeat=len(labels_sorted)):
        multipliers = {
            label: float(value)
            for label, value in zip(labels_sorted, values)
        }

        adjusted = apply_class_multipliers(
            validation_probabilities,
            multipliers=multipliers,
            labels_sorted=labels_sorted,
        )
        predictions = labels_from_probabilities(adjusted, labels_sorted=labels_sorted)
        metrics = per_class_metrics(y_validation, predictions)
        key = (
            metrics["macro_f1"],
            metrics["weighted_f1"],
            metrics["accuracy"],
        )

        if key > best_key:
            best_key = key
            best_metrics = metrics
            best_multipliers = multipliers

    return {
        "multipliers": best_multipliers,
        "validation_metrics": best_metrics,
        "selection_key": {
            "macro_f1": best_key[0],
            "weighted_f1": best_key[1],
            "accuracy": best_key[2],
        },
    }


def add_predictions(
    *,
    split_name: str,
    rows: list[dict[str, Any]],
    y_true: list[str],
    probability_maps: list[dict[str, float]],
    model_name: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    labels_sorted = sorted(THESIS4_CATEGORIES)
    y_pred = labels_from_probabilities(probability_maps, labels_sorted=labels_sorted)

    for row, gold, pred, probability_map in zip(rows, y_true, y_pred, probability_maps):
        output.append(
            {
                "case_id": row.get("case_id"),
                "repository": row.get("repository"),
                "language": row.get("language"),
                "dataset_split": split_name,
                "gold_doc_category": gold,
                "pred_doc_category": pred,
                "category_correct": gold == pred,
                "pred_confidence": prediction_confidence(probability_map, pred),
                "pred_probabilities": probability_map,
                "pred_ranked_categories": ranked_categories(probability_map),
                "selected_model_name": model_name,
                "source_url": row.get("source_url"),
                "code_changed_files": row.get("code_changed_files"),
            }
        )

    return output


def _json_block(payload: Any) -> list[str]:
    return [
        "```json",
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
    ]


def write_markdown_report(
    path: Path,
    *,
    metrics_by_model: dict[str, Any],
    ensemble_report: dict[str, Any],
    outputs: dict[str, str],
    summary: dict[str, Any],
) -> None:
    lines: list[str] = [
        "# Real PR Documentation Category Classifier V4 — ML-Only Ensemble",
        "",
        "## Purpose",
        "",
        "This experiment trains a second-stage documentation category classifier for positive documentation-update cases.",
        "",
        "The binary classifier decides whether documentation should be updated. This classifier predicts the documentation category after a positive update decision.",
        "",
        "## ML-only input policy",
        "",
        "The classifier uses only safe pre-decision input fields:",
        "",
    ]

    for field in SAFE_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "No category-specific hand-written prediction rules are used.",
            "",
            "Raw file paths are used only as raw lexical text. The model does not receive manually encoded features such as `path_flag_api_route`, `path_flag_configuration`, `path_flag_schema_contract`, or `path_flag_test_or_fixture`.",
            "",
            "## V4 method",
            "",
            "V4 uses a validation-selected soft-voting ensemble and validation-only probability calibration.",
            "",
            "The calibration step learns class multipliers on the validation split only. It does not inspect locked-test results and it does not use keyword rules.",
            "",
            "## Supported categories",
            "",
        ]
    )

    for category in sorted(THESIS4_CATEGORIES):
        lines.append(f"- `{category}`")

    lines.extend(
        [
            "",
            "## Dataset summary",
            "",
        ]
    )

    lines.extend(
        _json_block(
            {
                "row_counts": summary["row_counts"],
                "class_distribution": summary["class_distribution"],
                "language_filter": summary["language_filter"],
            }
        )
    )

    lines.extend(
        [
            "",
            "## Selected ensemble",
            "",
        ]
    )

    lines.extend(_json_block(ensemble_report["selected_ensemble"]))

    lines.extend(
        [
            "",
            "## Single-model comparison",
            "",
            "| Model | Validation macro-F1 | Validation weighted-F1 | Validation accuracy | Locked macro-F1 | Locked weighted-F1 | Locked accuracy |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for model_name, payload in metrics_by_model.items():
        validation = payload["metrics_by_split"]["validation"]
        locked = payload["metrics_by_split"]["locked_test"]

        lines.append(
            f"| `{model_name}` | "
            f"{validation['macro_f1']:.4f} | "
            f"{validation['weighted_f1']:.4f} | "
            f"{validation['accuracy']:.4f} | "
            f"{locked['macro_f1']:.4f} | "
            f"{locked['weighted_f1']:.4f} | "
            f"{locked['accuracy']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Ensemble metrics",
            "",
        ]
    )

    lines.extend(_json_block(ensemble_report["metrics_by_split"]))

    lines.extend(
        [
            "",
            "## Probability calibration",
            "",
        ]
    )

    lines.extend(_json_block(ensemble_report["calibration"]))

    lines.extend(
        [
            "",
            "## Outputs",
            "",
        ]
    )

    lines.extend(_json_block(outputs))

    lines.extend(
        [
            "",
            "## Methodological note",
            "",
            "This is a second-stage category classifier. It is trained and evaluated only on cases where documentation update is required and where the category can be harmonized into one of the supported thesis categories.",
            "",
            "Model selection, ensemble selection, and probability calibration use the validation split only. The locked-test split is used only for final reporting.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def run(
    *,
    train_path: Path,
    validation_path: Path,
    locked_test_path: Path,
    output_dir: Path,
    model_output: Path,
    seed: int,
    language_filter: str | None,
    ensemble_size: int,
    calibration_grid: list[float],
) -> dict[str, Any]:
    labels_sorted = sorted(THESIS4_CATEGORIES)

    raw_train = load_jsonl(train_path)
    raw_validation = load_jsonl(validation_path)
    raw_locked = load_jsonl(locked_test_path)

    if language_filter:
        language_filter_lower = language_filter.lower()
        raw_train = [
            row
            for row in raw_train
            if str(row.get("language") or "").lower() == language_filter_lower
        ]
        raw_validation = [
            row
            for row in raw_validation
            if str(row.get("language") or "").lower() == language_filter_lower
        ]
        raw_locked = [
            row
            for row in raw_locked
            if str(row.get("language") or "").lower() == language_filter_lower
        ]

    train_rows = positive_category_rows(raw_train)
    validation_rows = positive_category_rows(raw_validation)
    locked_rows = positive_category_rows(raw_locked)

    if not train_rows:
        raise ValueError("No positive category training rows found.")
    if not validation_rows:
        raise ValueError("No positive category validation rows found.")
    if not locked_rows:
        raise ValueError("No positive category locked-test rows found.")

    y_train = labels(train_rows)
    y_validation = labels(validation_rows)
    y_locked = labels(locked_rows)

    print(
        json.dumps(
            {
                "status": "loaded_category_rows",
                "language_filter": language_filter,
                "row_counts": {
                    "train": len(train_rows),
                    "validation": len(validation_rows),
                    "locked_test": len(locked_rows),
                },
                "class_distribution": {
                    "train": dict(Counter(y_train)),
                    "validation": dict(Counter(y_validation)),
                    "locked_test": dict(Counter(y_locked)),
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    candidates = make_category_model_candidates(seed)
    metrics_by_model: dict[str, Any] = {}
    fitted_models: dict[str, Pipeline] = {}

    for model_name, model in candidates.items():
        print(f"=== Training category model {model_name} ===")

        model.fit(train_rows, y_train)
        fitted_models[model_name] = model

        pred_train = predict_with_model(model, train_rows)
        pred_validation = predict_with_model(model, validation_rows)
        pred_locked = predict_with_model(model, locked_rows)

        metrics_by_split = {
            "train": per_class_metrics(y_train, pred_train),
            "validation": per_class_metrics(y_validation, pred_validation),
            "locked_test": per_class_metrics(y_locked, pred_locked),
        }

        metrics_by_model[model_name] = {
            "model_name": model_name,
            "metrics_by_split": metrics_by_split,
        }

        print(
            json.dumps(
                {
                    "model_name": model_name,
                    "validation_macro_f1": metrics_by_split["validation"]["macro_f1"],
                    "validation_weighted_f1": metrics_by_split["validation"]["weighted_f1"],
                    "validation_accuracy": metrics_by_split["validation"]["accuracy"],
                    "locked_macro_f1": metrics_by_split["locked_test"]["macro_f1"],
                    "locked_weighted_f1": metrics_by_split["locked_test"]["weighted_f1"],
                    "locked_accuracy": metrics_by_split["locked_test"]["accuracy"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    ranked_model_names = sorted(
        metrics_by_model,
        key=lambda name: model_selection_key(metrics_by_model[name]),
        reverse=True,
    )

    selected_model_names = ranked_model_names[: max(1, ensemble_size)]
    selected_models = [fitted_models[name] for name in selected_model_names]

    validation_weights = [
        max(metrics_by_model[name]["metrics_by_split"]["validation"]["macro_f1"], 1e-9)
        for name in selected_model_names
    ]

    def ensemble_probabilities(rows: list[dict[str, Any]]) -> list[dict[str, float]]:
        probability_sets = [
            predict_model_probabilities(model, rows, labels_sorted)
            for model in selected_models
        ]

        return average_probability_maps(
            probability_sets,
            labels_sorted=labels_sorted,
            weights=validation_weights,
        )

    raw_train_probabilities = ensemble_probabilities(train_rows)
    raw_validation_probabilities = ensemble_probabilities(validation_rows)
    raw_locked_probabilities = ensemble_probabilities(locked_rows)

    raw_train_pred = labels_from_probabilities(raw_train_probabilities, labels_sorted=labels_sorted)
    raw_validation_pred = labels_from_probabilities(raw_validation_probabilities, labels_sorted=labels_sorted)
    raw_locked_pred = labels_from_probabilities(raw_locked_probabilities, labels_sorted=labels_sorted)

    raw_ensemble_metrics_by_split = {
        "train": per_class_metrics(y_train, raw_train_pred),
        "validation": per_class_metrics(y_validation, raw_validation_pred),
        "locked_test": per_class_metrics(y_locked, raw_locked_pred),
    }

    calibration = optimize_class_multipliers(
        validation_probabilities=raw_validation_probabilities,
        y_validation=y_validation,
        labels_sorted=labels_sorted,
        grid_values=calibration_grid,
    )

    multipliers = calibration["multipliers"]

    calibrated_train_probabilities = apply_class_multipliers(
        raw_train_probabilities,
        multipliers=multipliers,
        labels_sorted=labels_sorted,
    )
    calibrated_validation_probabilities = apply_class_multipliers(
        raw_validation_probabilities,
        multipliers=multipliers,
        labels_sorted=labels_sorted,
    )
    calibrated_locked_probabilities = apply_class_multipliers(
        raw_locked_probabilities,
        multipliers=multipliers,
        labels_sorted=labels_sorted,
    )

    calibrated_train_pred = labels_from_probabilities(calibrated_train_probabilities, labels_sorted=labels_sorted)
    calibrated_validation_pred = labels_from_probabilities(calibrated_validation_probabilities, labels_sorted=labels_sorted)
    calibrated_locked_pred = labels_from_probabilities(calibrated_locked_probabilities, labels_sorted=labels_sorted)

    calibrated_ensemble_metrics_by_split = {
        "train": per_class_metrics(y_train, calibrated_train_pred),
        "validation": per_class_metrics(y_validation, calibrated_validation_pred),
        "locked_test": per_class_metrics(y_locked, calibrated_locked_pred),
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "category_model": str(model_output),
        "summary_json": str(output_dir / "category_classifier_summary.json"),
        "model_comparison_json": str(output_dir / "category_model_comparison.json"),
        "model_comparison_md": str(output_dir / "category_model_comparison.md"),
        "predictions_jsonl": str(output_dir / "category_predictions.jsonl"),
    }

    ensemble_report = {
        "selected_ensemble": {
            "selected_model_names": selected_model_names,
            "ensemble_size": len(selected_model_names),
            "weights_source": "validation_macro_f1",
            "validation_weights": {
                name: weight
                for name, weight in zip(selected_model_names, validation_weights)
            },
        },
        "raw_metrics_by_split": raw_ensemble_metrics_by_split,
        "calibrated_metrics_by_split": calibrated_ensemble_metrics_by_split,
        "metrics_by_split": calibrated_ensemble_metrics_by_split,
        "calibration": {
            "method": "validation_only_class_probability_multipliers",
            "grid_values": calibration_grid,
            "selected_multipliers": multipliers,
            "validation_metrics_after_calibration": calibration["validation_metrics"],
            "locked_test_policy": "final_reporting_only",
        },
    }

    predictions: list[dict[str, Any]] = []
    predictions.extend(
        add_predictions(
            split_name="train",
            rows=train_rows,
            y_true=y_train,
            probability_maps=calibrated_train_probabilities,
            model_name="v4_calibrated_soft_voting_ensemble",
        )
    )
    predictions.extend(
        add_predictions(
            split_name="validation",
            rows=validation_rows,
            y_true=y_validation,
            probability_maps=calibrated_validation_probabilities,
            model_name="v4_calibrated_soft_voting_ensemble",
        )
    )
    predictions.extend(
        add_predictions(
            split_name="locked_test",
            rows=locked_rows,
            y_true=y_locked,
            probability_maps=calibrated_locked_probabilities,
            model_name="v4_calibrated_soft_voting_ensemble",
        )
    )

    summary = {
        "status": "ok",
        "selected_model_name": "v4_calibrated_soft_voting_ensemble",
        "category_schema": "thesis4_ml_only_harmonized_targets",
        "categories": labels_sorted,
        "safe_input_fields": SAFE_INPUT_FIELDS,
        "language_filter": language_filter,
        "row_counts": {
            "train": len(train_rows),
            "validation": len(validation_rows),
            "locked_test": len(locked_rows),
        },
        "class_distribution": {
            "train": dict(Counter(y_train)),
            "validation": dict(Counter(y_validation)),
            "locked_test": dict(Counter(y_locked)),
        },
        "best_metrics_by_split": calibrated_ensemble_metrics_by_split,
        "raw_ensemble_metrics_by_split": raw_ensemble_metrics_by_split,
        "ensemble": ensemble_report["selected_ensemble"],
        "calibration": ensemble_report["calibration"],
        "outputs": outputs,
        "ml_only_policy": {
            "uses_category_specific_prediction_rules": False,
            "uses_manual_path_flags": False,
            "uses_raw_paths_as_text": True,
            "uses_target_label_harmonization": True,
            "uses_validation_only_probability_calibration": True,
            "uses_locked_test_for_selection": False,
        },
    }

    model_output.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model_type": "v4_calibrated_soft_voting_ensemble",
            "selected_models": [
                {
                    "model_name": name,
                    "model": model,
                    "validation_macro_f1": metrics_by_model[name]["metrics_by_split"]["validation"]["macro_f1"],
                }
                for name, model in zip(selected_model_names, selected_models)
            ],
            "selected_model_names": selected_model_names,
            "validation_weights": validation_weights,
            "class_multipliers": multipliers,
            "category_schema": "thesis4_ml_only_harmonized_targets",
            "categories": labels_sorted,
            "safe_input_fields": SAFE_INPUT_FIELDS,
            "language_filter": language_filter,
            "target_category_aliases": TARGET_CATEGORY_ALIASES,
            "model_selection": {
                "component_selection_split": "validation",
                "component_selection_metric": "macro_f1",
                "ensemble_weight_source": "validation_macro_f1",
                "calibration_split": "validation",
                "calibration_metric": "macro_f1",
                "locked_test_policy": "final_reporting_only",
            },
            "ml_only_policy": summary["ml_only_policy"],
        },
        model_output,
    )

    write_json(Path(outputs["summary_json"]), summary)
    write_json(Path(outputs["model_comparison_json"]), metrics_by_model)
    write_jsonl(Path(outputs["predictions_jsonl"]), predictions)
    write_markdown_report(
        Path(outputs["model_comparison_md"]),
        metrics_by_model=metrics_by_model,
        ensemble_report=ensemble_report,
        outputs=outputs,
        summary=summary,
    )

    print(
        json.dumps(
            {
                "status": "v4_complete",
                "selected_ensemble": ensemble_report["selected_ensemble"],
                "calibration": ensemble_report["calibration"],
                "validation": calibrated_ensemble_metrics_by_split["validation"],
                "locked_test": calibrated_ensemble_metrics_by_split["locked_test"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train an ML-only second-stage real PR documentation category classifier with soft-voting ensemble."
    )
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--language-filter", default=None)
    parser.add_argument("--ensemble-size", type=int, default=5)
    parser.add_argument(
        "--calibration-grid",
        default="0.5,0.75,1.0,1.25,1.5,2.0",
        help="Comma-separated validation-only class multiplier grid.",
    )

    args = parser.parse_args()

    summary = run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        output_dir=Path(args.output_dir),
        model_output=Path(args.model_output),
        seed=args.seed,
        language_filter=args.language_filter,
        ensemble_size=args.ensemble_size,
        calibration_grid=parse_float_list(args.calibration_grid),
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())