from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MODULE_NAME = "scripts.train_real_doc_category_classifier_v5_embeddings"
if __name__ == "__main__":
    sys.modules[MODULE_NAME] = sys.modules[__name__]

import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import Normalizer


THESIS4_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

TARGET_CATEGORY_ALIASES = {
    # Target-label harmonization only. These are NOT prediction rules.
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


def filter_by_language(rows: list[dict[str, Any]], language_filter: str | None) -> list[dict[str, Any]]:
    if not language_filter:
        return rows

    language_filter_lower = language_filter.lower()
    return [
        row
        for row in rows
        if str(row.get("language") or "").lower() == language_filter_lower
    ]


def oversample_train_rows(
    rows: list[dict[str, Any]],
    *,
    seed: int,
    strategy: str,
) -> list[dict[str, Any]]:
    if strategy == "none":
        return rows

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["category_label"]), []).append(row)

    if not grouped:
        return rows

    rng = random.Random(seed)

    if strategy == "max":
        target_count = max(len(items) for items in grouped.values())
    elif strategy.startswith("cap:"):
        cap = int(strategy.split(":", 1)[1])
        target_count = min(max(len(items) for items in grouped.values()), cap)
    else:
        raise ValueError(f"Unsupported oversample strategy: {strategy}")

    output: list[dict[str, Any]] = []

    for category, items in grouped.items():
        output.extend(items)

        if len(items) >= target_count:
            continue

        needed = target_count - len(items)
        output.extend(rng.choice(items) for _ in range(needed))

    rng.shuffle(output)
    return output


def build_full_text(row: dict[str, Any]) -> str:
    """
    Safe ML-only representation.

    Uses only:
    - language
    - code_changed_files
    - code_diff_excerpt
    - docs_before_excerpt

    It does not use docs-after, docs diff, gold category, target doc,
    PR title, source URL, manual notes, or audit-only fields.
    """
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


def build_code_text(row: dict[str, Any]) -> str:
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


def build_raw_path_text(row: dict[str, Any], *, heavy: bool = False) -> str:
    """
    Raw lexical path representation only.

    This is not a rule-based router. It does not add category flags such as
    api/config/schema/setup. It only tokenizes actual changed file paths.
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


class RowTextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mode: str = "full") -> None:
        self.mode = mode

    def fit(self, X: list[dict[str, Any]], y: list[str] | None = None) -> "RowTextTransformer":
        return self

    def transform(self, X: list[dict[str, Any]]) -> list[str]:
        if self.mode == "full":
            return [build_full_text(row) for row in X]

        if self.mode == "code":
            return [build_code_text(row) for row in X]

        if self.mode == "docs_before":
            return [build_docs_before_text(row) for row in X]

        if self.mode == "path_raw":
            return [build_raw_path_text(row, heavy=False) for row in X]

        if self.mode == "path_raw_heavy":
            return [build_raw_path_text(row, heavy=True) for row in X]

        raise ValueError(f"Unsupported text mode: {self.mode}")


RowTextTransformer.__module__ = MODULE_NAME


def word_tfidf(mode: str, *, max_features: int) -> Pipeline:
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
                    strip_accents="unicode",
                    token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
                ),
            ),
        ]
    )


def char_tfidf(mode: str, *, max_features: int) -> Pipeline:
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


def path_tfidf(*, heavy: bool, max_features: int) -> Pipeline:
    mode = "path_raw_heavy" if heavy else "path_raw"

    return Pipeline(
        [
            ("text", RowTextTransformer(mode=mode)),
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
    c_value: float,
    class_weight: str | None,
    seed: int,
) -> LogisticRegression:
    return LogisticRegression(
        C=c_value,
        class_weight=class_weight,
        max_iter=6000,
        random_state=seed,
        solver="lbfgs",
    )


def make_sparse_feature_union() -> FeatureUnion:
    return FeatureUnion(
        [
            ("word_full", word_tfidf("full", max_features=80_000)),
            ("char_full", char_tfidf("full", max_features=90_000)),
            ("path_raw", path_tfidf(heavy=True, max_features=50_000)),
        ]
    )


def make_split_feature_union() -> FeatureUnion:
    return FeatureUnion(
        [
            ("word_code", word_tfidf("code", max_features=70_000)),
            ("word_docs_before", word_tfidf("docs_before", max_features=40_000)),
            ("char_full", char_tfidf("full", max_features=90_000)),
            ("path_raw", path_tfidf(heavy=True, max_features=50_000)),
        ]
    )


def make_lsa_pipeline(
    *,
    features: FeatureUnion,
    n_components: int,
    c_value: float,
    class_weight: str | None,
    seed: int,
) -> Pipeline:
    return Pipeline(
        [
            ("features", features),
            ("svd", TruncatedSVD(n_components=n_components, random_state=seed)),
            ("normalize", Normalizer(copy=False)),
            ("classifier", make_logreg(c_value=c_value, class_weight=class_weight, seed=seed)),
        ]
    )


def make_category_model_candidates(seed: int) -> dict[str, Pipeline]:
    """
    V5 candidates.

    All candidates are ML-only:
    - sparse TF-IDF logistic regression
    - dense latent semantic embeddings through TF-IDF + TruncatedSVD
    - no category-specific rules
    - no per-category keyword flags
    - no locked-test selection
    """
    candidates: dict[str, Pipeline] = {}

    for c_value in [0.25, 0.5, 1.0, 2.0, 4.0]:
        candidates[f"sparse_word_char_path_logreg_balanced_c{c_value}"] = Pipeline(
            [
                ("features", make_sparse_feature_union()),
                ("classifier", make_logreg(c_value=c_value, class_weight="balanced", seed=seed)),
            ]
        )

    for n_components in [64, 128, 256]:
        for c_value in [0.5, 1.0, 2.0, 4.0]:
            candidates[f"lsa_full_{n_components}_logreg_balanced_c{c_value}"] = make_lsa_pipeline(
                features=make_sparse_feature_union(),
                n_components=n_components,
                c_value=c_value,
                class_weight="balanced",
                seed=seed,
            )

            candidates[f"lsa_split_{n_components}_logreg_balanced_c{c_value}"] = make_lsa_pipeline(
                features=make_split_feature_union(),
                n_components=n_components,
                c_value=c_value,
                class_weight="balanced",
                seed=seed,
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


def predict_probabilities(
    model: Pipeline,
    rows: list[dict[str, Any]],
    labels_sorted: list[str],
) -> list[dict[str, float]]:
    if not rows:
        return []

    if not hasattr(model, "predict_proba"):
        predictions = predict_with_model(model, rows)
        return [
            {label: 1.0 if label == prediction else 0.0 for label in labels_sorted}
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


def labels_from_probabilities(
    probability_maps: list[dict[str, float]],
    *,
    labels_sorted: list[str],
) -> list[str]:
    return [
        max(labels_sorted, key=lambda label: float(probability_map.get(label, 0.0)))
        for probability_map in probability_maps
    ]


def ranked_categories(probability_map: dict[str, float]) -> list[dict[str, float]]:
    return [
        {"category": category, "probability": probability}
        for category, probability in sorted(
            probability_map.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]


def top_k_accuracy(
    y_true: list[str],
    probability_maps: list[dict[str, float]],
    *,
    k: int,
) -> float:
    if not y_true:
        return 0.0

    correct = 0

    for gold, probability_map in zip(y_true, probability_maps):
        ranked = [
            item["category"]
            for item in ranked_categories(probability_map)[:k]
        ]
        if gold in ranked:
            correct += 1

    return safe_div(correct, len(y_true))


def metrics_from_probabilities(
    y_true: list[str],
    probability_maps: list[dict[str, float]],
) -> dict[str, Any]:
    labels_sorted = sorted(THESIS4_CATEGORIES)
    y_pred = labels_from_probabilities(probability_maps, labels_sorted=labels_sorted)
    metrics = per_class_metrics(y_true, y_pred)
    metrics["top2_accuracy"] = top_k_accuracy(y_true, probability_maps, k=2)
    return metrics


def model_selection_key(result: dict[str, Any]) -> tuple[float, ...]:
    validation = result["metrics_by_split"]["validation"]

    return (
        validation["macro_f1"],
        validation["weighted_f1"],
        validation.get("top2_accuracy", 0.0),
        validation["accuracy"],
    )


def add_predictions(
    *,
    split_name: str,
    rows: list[dict[str, Any]],
    y_true: list[str],
    probability_maps: list[dict[str, float]],
    model_name: str,
) -> list[dict[str, Any]]:
    labels_sorted = sorted(THESIS4_CATEGORIES)
    y_pred = labels_from_probabilities(probability_maps, labels_sorted=labels_sorted)

    output: list[dict[str, Any]] = []

    for row, gold, pred, probability_map in zip(rows, y_true, y_pred, probability_maps):
        ranked = ranked_categories(probability_map)
        output.append(
            {
                "case_id": row.get("case_id"),
                "repository": row.get("repository"),
                "language": row.get("language"),
                "dataset_split": split_name,
                "gold_doc_category": gold,
                "pred_doc_category": pred,
                "category_correct": gold == pred,
                "top2_contains_gold": gold in [item["category"] for item in ranked[:2]],
                "pred_confidence": float(probability_map.get(pred, 0.0)),
                "pred_probabilities": probability_map,
                "pred_ranked_categories": ranked,
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
    selected_model_name: str,
    metrics_by_model: dict[str, Any],
    best_metrics_by_split: dict[str, Any],
    summary: dict[str, Any],
    outputs: dict[str, str],
) -> None:
    lines: list[str] = [
        "# Real PR Documentation Category Classifier V5 — ML-Only Latent Embeddings",
        "",
        "## Purpose",
        "",
        "This experiment trains a second-stage documentation category classifier for positive documentation-update cases.",
        "",
        "The binary classifier decides whether documentation should be updated. This classifier predicts the documentation category after a positive update decision.",
        "",
        "## ML-only policy",
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
            "No manual path flags are used. Raw file paths are used only as lexical input text.",
            "",
            "V5 adds latent semantic embeddings through TF-IDF plus TruncatedSVD/LSA. This is an unsupervised dense representation learned from the training text, followed by supervised ML classifiers.",
            "",
            "Target-label harmonization affects only the target label `y`, not model input `X`.",
            "",
            "## Selected model",
            "",
            f"- selected model: `{selected_model_name}`",
            "- selection split: validation",
            "- selection metric: macro-F1, then weighted-F1, then top-2 accuracy, then accuracy",
            "- locked-test policy: final reporting only",
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
                "evaluation_language_filter": summary["evaluation_language_filter"],
                "train_language_filter": summary["train_language_filter"],
                "oversample_train": summary["oversample_train"],
            }
        )
    )

    lines.extend(
        [
            "",
            "## Model comparison",
            "",
            "| Model | Validation macro-F1 | Validation weighted-F1 | Validation top-2 acc | Validation accuracy | Locked macro-F1 | Locked weighted-F1 | Locked top-2 acc | Locked accuracy |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for model_name, payload in metrics_by_model.items():
        validation = payload["metrics_by_split"]["validation"]
        locked = payload["metrics_by_split"]["locked_test"]

        lines.append(
            f"| `{model_name}` | "
            f"{validation['macro_f1']:.4f} | "
            f"{validation['weighted_f1']:.4f} | "
            f"{validation.get('top2_accuracy', 0.0):.4f} | "
            f"{validation['accuracy']:.4f} | "
            f"{locked['macro_f1']:.4f} | "
            f"{locked['weighted_f1']:.4f} | "
            f"{locked.get('top2_accuracy', 0.0):.4f} | "
            f"{locked['accuracy']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Best model metrics by split",
            "",
        ]
    )
    lines.extend(_json_block(best_metrics_by_split))

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
            "Model selection uses the validation split only. The locked-test split is used only for final reporting.",
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
    seed: int,
    language_filter: str | None,
    train_language_filter: str,
    oversample_train: str,
) -> dict[str, Any]:
    labels_sorted = sorted(THESIS4_CATEGORIES)

    raw_train = load_jsonl(train_path)
    raw_validation = load_jsonl(validation_path)
    raw_locked = load_jsonl(locked_test_path)

    if train_language_filter == "same":
        raw_train = filter_by_language(raw_train, language_filter)
    elif train_language_filter == "all":
        raw_train = raw_train
    else:
        raw_train = filter_by_language(raw_train, train_language_filter)

    raw_validation = filter_by_language(raw_validation, language_filter)
    raw_locked = filter_by_language(raw_locked, language_filter)

    train_rows = positive_category_rows(raw_train)
    validation_rows = positive_category_rows(raw_validation)
    locked_rows = positive_category_rows(raw_locked)

    if not train_rows:
        raise ValueError("No positive category training rows found.")
    if not validation_rows:
        raise ValueError("No positive category validation rows found.")
    if not locked_rows:
        raise ValueError("No positive category locked-test rows found.")

    fit_rows = oversample_train_rows(train_rows, seed=seed, strategy=oversample_train)

    y_train = labels(train_rows)
    y_fit = labels(fit_rows)
    y_validation = labels(validation_rows)
    y_locked = labels(locked_rows)

    print(
        json.dumps(
            {
                "status": "loaded_category_rows",
                "evaluation_language_filter": language_filter,
                "train_language_filter": train_language_filter,
                "oversample_train": oversample_train,
                "row_counts": {
                    "train_original": len(train_rows),
                    "train_fit": len(fit_rows),
                    "validation": len(validation_rows),
                    "locked_test": len(locked_rows),
                },
                "class_distribution": {
                    "train_original": dict(Counter(y_train)),
                    "train_fit": dict(Counter(y_fit)),
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

        model.fit(fit_rows, y_fit)
        fitted_models[model_name] = model

        prob_train = predict_probabilities(model, train_rows, labels_sorted)
        prob_validation = predict_probabilities(model, validation_rows, labels_sorted)
        prob_locked = predict_probabilities(model, locked_rows, labels_sorted)

        metrics_by_split = {
            "train": metrics_from_probabilities(y_train, prob_train),
            "validation": metrics_from_probabilities(y_validation, prob_validation),
            "locked_test": metrics_from_probabilities(y_locked, prob_locked),
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
                    "validation_top2_accuracy": metrics_by_split["validation"]["top2_accuracy"],
                    "validation_accuracy": metrics_by_split["validation"]["accuracy"],
                    "locked_macro_f1": metrics_by_split["locked_test"]["macro_f1"],
                    "locked_weighted_f1": metrics_by_split["locked_test"]["weighted_f1"],
                    "locked_top2_accuracy": metrics_by_split["locked_test"]["top2_accuracy"],
                    "locked_accuracy": metrics_by_split["locked_test"]["accuracy"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    selected_model_name = max(
        metrics_by_model,
        key=lambda name: model_selection_key(metrics_by_model[name]),
    )
    selected_model = fitted_models[selected_model_name]

    prob_train = predict_probabilities(selected_model, train_rows, labels_sorted)
    prob_validation = predict_probabilities(selected_model, validation_rows, labels_sorted)
    prob_locked = predict_probabilities(selected_model, locked_rows, labels_sorted)

    best_metrics_by_split = {
        "train": metrics_from_probabilities(y_train, prob_train),
        "validation": metrics_from_probabilities(y_validation, prob_validation),
        "locked_test": metrics_from_probabilities(y_locked, prob_locked),
    }

    predictions: list[dict[str, Any]] = []
    predictions.extend(
        add_predictions(
            split_name="train",
            rows=train_rows,
            y_true=y_train,
            probability_maps=prob_train,
            model_name=selected_model_name,
        )
    )
    predictions.extend(
        add_predictions(
            split_name="validation",
            rows=validation_rows,
            y_true=y_validation,
            probability_maps=prob_validation,
            model_name=selected_model_name,
        )
    )
    predictions.extend(
        add_predictions(
            split_name="locked_test",
            rows=locked_rows,
            y_true=y_locked,
            probability_maps=prob_locked,
            model_name=selected_model_name,
        )
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    model_output.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "category_model": str(model_output),
        "summary_json": str(output_dir / "category_classifier_summary.json"),
        "model_comparison_json": str(output_dir / "category_model_comparison.json"),
        "model_comparison_md": str(output_dir / "category_model_comparison.md"),
        "predictions_jsonl": str(output_dir / "category_predictions.jsonl"),
    }

    summary = {
        "status": "ok",
        "selected_model_name": selected_model_name,
        "category_schema": "thesis4_ml_only_harmonized_targets",
        "categories": labels_sorted,
        "safe_input_fields": SAFE_INPUT_FIELDS,
        "evaluation_language_filter": language_filter,
        "train_language_filter": train_language_filter,
        "oversample_train": oversample_train,
        "row_counts": {
            "train_original": len(train_rows),
            "train_fit": len(fit_rows),
            "validation": len(validation_rows),
            "locked_test": len(locked_rows),
        },
        "class_distribution": {
            "train_original": dict(Counter(y_train)),
            "train_fit": dict(Counter(y_fit)),
            "validation": dict(Counter(y_validation)),
            "locked_test": dict(Counter(y_locked)),
        },
        "best_metrics_by_split": best_metrics_by_split,
        "outputs": outputs,
        "model_selection": {
            "selection_split": "validation",
            "selection_metric_order": [
                "macro_f1",
                "weighted_f1",
                "top2_accuracy",
                "accuracy",
            ],
            "locked_test_policy": "final_reporting_only",
        },
        "ml_only_policy": {
            "uses_category_specific_prediction_rules": False,
            "uses_manual_path_flags": False,
            "uses_raw_paths_as_text": True,
            "uses_target_label_harmonization": True,
            "uses_train_only_oversampling": oversample_train != "none",
            "uses_locked_test_for_selection": False,
            "representation": "tfidf_plus_truncated_svd_lsa_candidates",
        },
    }

    joblib.dump(
        {
            "model_type": "v5_ml_only_latent_embedding_classifier",
            "model": selected_model,
            "selected_model_name": selected_model_name,
            "category_schema": "thesis4_ml_only_harmonized_targets",
            "categories": labels_sorted,
            "safe_input_fields": SAFE_INPUT_FIELDS,
            "evaluation_language_filter": language_filter,
            "train_language_filter": train_language_filter,
            "oversample_train": oversample_train,
            "target_category_aliases": TARGET_CATEGORY_ALIASES,
            "model_selection": summary["model_selection"],
            "ml_only_policy": summary["ml_only_policy"],
        },
        model_output,
    )

    write_json(Path(outputs["summary_json"]), summary)
    write_json(Path(outputs["model_comparison_json"]), metrics_by_model)
    write_jsonl(Path(outputs["predictions_jsonl"]), predictions)
    write_markdown_report(
        Path(outputs["model_comparison_md"]),
        selected_model_name=selected_model_name,
        metrics_by_model=metrics_by_model,
        best_metrics_by_split=best_metrics_by_split,
        summary=summary,
        outputs=outputs,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train an ML-only documentation category classifier using latent semantic embeddings."
    )
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--language-filter", default=None)
    parser.add_argument(
        "--train-language-filter",
        default="same",
        help="Use 'same', 'all', or an explicit language name. Validation/locked still use --language-filter.",
    )
    parser.add_argument(
        "--oversample-train",
        default="max",
        help="Use 'none', 'max', or 'cap:<N>'. Oversampling is applied only to the training split.",
    )

    args = parser.parse_args()

    run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        output_dir=Path(args.output_dir),
        model_output=Path(args.model_output),
        seed=args.seed,
        language_filter=args.language_filter,
        train_language_filter=args.train_language_filter,
        oversample_train=args.oversample_train,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())