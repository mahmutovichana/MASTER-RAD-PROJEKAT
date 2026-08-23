from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

from scripts.train_real_gold_classifier_v2 import (
    bool_value,
    char_tfidf,
    load_jsonl,
    path_tfidf,
    safe_div,
    word_tfidf,
    write_json,
    write_jsonl,
)


THESIS4_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

CATEGORY_ALIASES = {
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


def normalize_category(value: Any) -> str | None:
    raw = str(value or "").strip().lower()

    if not raw or raw == "no_update" or raw == "not_available":
        return None

    normalized = CATEGORY_ALIASES.get(raw, raw)

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


def make_category_model_candidates(seed: int) -> dict[str, Pipeline]:
    return {
        "word_char_logreg": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=80_000)),
                            ("char", char_tfidf("full", max_features=90_000)),
                        ]
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        class_weight=None,
                        max_iter=3000,
                        random_state=seed,
                        solver="lbfgs"
                    ),
                ),
            ]
        ),
        "word_char_logreg_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=80_000)),
                            ("char", char_tfidf("full", max_features=90_000)),
                        ]
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        class_weight="balanced",
                        max_iter=3000,
                        random_state=seed,
                        solver="lbfgs"
                    ),
                ),
            ]
        ),
        "path_raw_word_char_logreg_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                            ("path_raw", path_tfidf(raw_only=True, heavy=True, max_features=40_000)),
                        ]
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        class_weight="balanced",
                        max_iter=3000,
                        random_state=seed,
                        solver="lbfgs",
                    ),
                ),
            ]
        ),
        "path_heavy_word_char_logreg_balanced": Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", word_tfidf("full", max_features=70_000)),
                            ("char", char_tfidf("full", max_features=80_000)),
                            ("path", path_tfidf(heavy=True, max_features=40_000)),
                        ]
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        class_weight="balanced",
                        max_iter=3000,
                        random_state=seed,
                        solver="lbfgs"
                    ),
                ),
            ]
        ),
    }


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
        "macro_f1": f1_score(y_true, y_pred, labels=labels_sorted, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, labels=labels_sorted, average="weighted", zero_division=0),
        "accuracy": safe_div(sum(1 for gold, pred in zip(y_true, y_pred) if gold == pred), len(y_true)),
        "gold_distribution": dict(Counter(y_true)),
        "pred_distribution": dict(Counter(y_pred)),
    }


def predict_with_model(model: Pipeline, rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []

    return [str(item) for item in model.predict(rows)]


def write_markdown_report(
    path: Path,
    *,
    selected_model_name: str,
    metrics_by_model: dict[str, Any],
    best_metrics_by_split: dict[str, Any],
    outputs: dict[str, str],
) -> None:
    lines: list[str] = [
        "# Real PR Documentation Category Classifier V1",
        "",
        "## Purpose",
        "",
        "This experiment trains a second-stage classifier for positive documentation-update cases.",
        "The binary V2 classifier decides whether documentation should be updated; this classifier predicts the documentation-update category.",
        "",
        "Supported thesis categories:",
        "",
    ]

    for category in sorted(THESIS4_CATEGORIES):
        lines.append(f"- `{category}`")

    lines.extend(
        [
            "",
            "## Selected model",
            "",
            f"- selected model: `{selected_model_name}`",
            "- selection metric: validation macro-F1",
            "",
            "## Model comparison",
            "",
            "| Model | Validation macro-F1 | Validation weighted-F1 | Locked macro-F1 | Locked weighted-F1 |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for model_name, payload in metrics_by_model.items():
        validation = payload["metrics_by_split"]["validation"]
        locked = payload["metrics_by_split"]["locked_test"]
        lines.append(
            f"| `{model_name}` | "
            f"{validation['macro_f1']:.4f} | "
            f"{validation['weighted_f1']:.4f} | "
            f"{locked['macro_f1']:.4f} | "
            f"{locked['weighted_f1']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Best model metrics by split",
            "",
            "```json",
            json.dumps(best_metrics_by_split, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## Outputs",
            "",
            "```json",
            json.dumps(outputs, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## Methodological note",
            "",
            "This is a second-stage category classifier. It is trained and evaluated only on cases where documentation update is required and where the category can be normalized to one of the supported thesis categories.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def add_predictions(
    *,
    split_name: str,
    rows: list[dict[str, Any]],
    y_true: list[str],
    y_pred: list[str],
    model_name: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    for row, gold, pred in zip(rows, y_true, y_pred):
        output.append(
            {
                "case_id": row.get("case_id"),
                "repository": row.get("repository"),
                "language": row.get("language"),
                "dataset_split": split_name,
                "gold_doc_category": gold,
                "pred_doc_category": pred,
                "category_correct": gold == pred,
                "selected_model_name": model_name,
                "source_url": row.get("source_url"),
                "code_changed_files": row.get("code_changed_files"),
            }
        )

    return output


def run(
    *,
    train_path: Path,
    validation_path: Path,
    locked_test_path: Path,
    output_dir: Path,
    model_output: Path,
    seed: int,
    language_filter: str | None,
) -> dict[str, Any]:
    raw_train = load_jsonl(train_path)
    raw_validation = load_jsonl(validation_path)
    raw_locked = load_jsonl(locked_test_path)

    if language_filter:
        language_filter_lower = language_filter.lower()
        raw_train = [row for row in raw_train if str(row.get("language") or "").lower() == language_filter_lower]
        raw_validation = [row for row in raw_validation if str(row.get("language") or "").lower() == language_filter_lower]
        raw_locked = [row for row in raw_locked if str(row.get("language") or "").lower() == language_filter_lower]

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
                    "locked_macro_f1": metrics_by_split["locked_test"]["macro_f1"],
                    "locked_weighted_f1": metrics_by_split["locked_test"]["weighted_f1"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    selected_model_name = max(
        metrics_by_model,
        key=lambda name: (
            metrics_by_model[name]["metrics_by_split"]["validation"]["macro_f1"],
            metrics_by_model[name]["metrics_by_split"]["validation"]["weighted_f1"],
            metrics_by_model[name]["metrics_by_split"]["validation"]["accuracy"],
        ),
    )

    selected_model = fitted_models[selected_model_name]

    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": selected_model,
            "selected_model_name": selected_model_name,
            "category_schema": "thesis4",
            "categories": sorted(THESIS4_CATEGORIES),
            "language_filter": language_filter,
        },
        model_output,
    )

    best_metrics_by_split = metrics_by_model[selected_model_name]["metrics_by_split"]

    predictions = []
    predictions.extend(
        add_predictions(
            split_name="train",
            rows=train_rows,
            y_true=y_train,
            y_pred=predict_with_model(selected_model, train_rows),
            model_name=selected_model_name,
        )
    )
    predictions.extend(
        add_predictions(
            split_name="validation",
            rows=validation_rows,
            y_true=y_validation,
            y_pred=predict_with_model(selected_model, validation_rows),
            model_name=selected_model_name,
        )
    )
    predictions.extend(
        add_predictions(
            split_name="locked_test",
            rows=locked_rows,
            y_true=y_locked,
            y_pred=predict_with_model(selected_model, locked_rows),
            model_name=selected_model_name,
        )
    )

    output_dir.mkdir(parents=True, exist_ok=True)

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
        "category_schema": "thesis4",
        "categories": sorted(THESIS4_CATEGORIES),
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
        "best_metrics_by_split": best_metrics_by_split,
        "outputs": outputs,
    }

    write_json(Path(outputs["summary_json"]), summary)
    write_json(Path(outputs["model_comparison_json"]), metrics_by_model)
    write_jsonl(Path(outputs["predictions_jsonl"]), predictions)
    write_markdown_report(
        Path(outputs["model_comparison_md"]),
        selected_model_name=selected_model_name,
        metrics_by_model=metrics_by_model,
        best_metrics_by_split=best_metrics_by_split,
        outputs=outputs,
    )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a second-stage real PR documentation category classifier.")
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--language-filter", default=None)

    args = parser.parse_args()

    summary = run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        output_dir=Path(args.output_dir),
        model_output=Path(args.model_output),
        seed=args.seed,
        language_filter=args.language_filter,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())