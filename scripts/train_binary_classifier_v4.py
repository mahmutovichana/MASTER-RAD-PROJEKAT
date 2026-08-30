from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from docguard_ml_v2.data_contract import SAFE_MODEL_FIELDS, assert_safe_rows_only, binary_eligible_rows, binary_labels, load_jsonl, write_json, write_jsonl
from docguard_ml_v2.features import char_tfidf, word_char_tfidf, word_tfidf
from docguard_ml_v2.metrics import binary_metrics, majority_binary_baseline, per_language_binary_metrics
from docguard_ml_v2.model_manifest import runtime_versions, sha256_file


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def make_classifier(c_value: float, seed: int) -> LogisticRegression:
    return LogisticRegression(C=c_value, max_iter=4000, random_state=seed, solver="liblinear")


def make_candidates(config: dict[str, Any]) -> dict[str, Pipeline]:
    seed = int(config["seed"])
    c_values = [float(value) for value in config["hyperparameter_grid"]["C"]]
    min_df_values = [int(value) for value in config["hyperparameter_grid"]["min_df"]]
    candidates: dict[str, Pipeline] = {}
    for c_value in c_values:
        for min_df in min_df_values:
            candidates[f"word_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", word_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
            candidates[f"char_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", char_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
            candidates[f"word_char_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", word_char_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
    return candidates


def probabilities(model: Pipeline, rows: list[dict[str, Any]]) -> list[float]:
    proba = model.predict_proba(rows)
    classes = list(model.named_steps["classifier"].classes_)
    return [float(item[classes.index(1)]) for item in proba]


def threshold_grid(config: dict[str, Any]) -> list[float]:
    policy = config["threshold_policy"]
    return [round(float(value), 4) for value in policy.get("grid", [i / 100 for i in range(5, 96, 5)])]


def metrics_at_threshold(y_true: list[int], scores: list[float], threshold: float) -> dict[str, Any]:
    return {"threshold": threshold, **binary_metrics(y_true, [1 if score >= threshold else 0 for score in scores], scores)}


def selection_key(metrics: dict[str, Any]) -> tuple[float, ...]:
    return (metrics["mcc"], metrics["balanced_accuracy"], metrics["f1"], metrics["precision"], metrics["recall"], metrics["specificity"])


def train_and_select(*, train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], config: dict[str, Any]) -> tuple[Pipeline, dict[str, Any], list[dict[str, Any]]]:
    y_train = binary_labels(train_rows)
    y_val = binary_labels(validation_rows)
    model_results: list[dict[str, Any]] = []
    fitted: dict[str, Pipeline] = {}
    seed = int(config["seed"])
    c_values = [float(value) for value in config["hyperparameter_grid"]["C"]]
    min_df_values = [int(value) for value in config["hyperparameter_grid"]["min_df"]]
    feature_factories = {
        "word_tfidf_logreg": word_tfidf,
        "char_tfidf_logreg": char_tfidf,
        "word_char_tfidf_logreg": word_char_tfidf,
    }
    # Vectorization dominates runtime for large diffs. For a fixed feature
    # family/min_df pair the matrix is identical across C values, so fit it
    # once and evaluate every classifier on the same matrix.
    for prefix, factory in feature_factories.items():
        for min_df in min_df_values:
            features = factory(min_df=min_df)
            x_train = features.fit_transform(train_rows)
            x_val = features.transform(validation_rows)
            for c_value in c_values:
                name = f"{prefix}_c{c_value}_mindf{min_df}"
                classifier = make_classifier(c_value, seed)
                classifier.fit(x_train, y_train)
                classes = list(classifier.classes_)
                positive_index = classes.index(1)
                val_scores = [float(item[positive_index]) for item in classifier.predict_proba(x_val)]
                train_scores = [float(item[positive_index]) for item in classifier.predict_proba(x_train)]
                sweep = [metrics_at_threshold(y_val, val_scores, threshold) for threshold in threshold_grid(config)]
                best_threshold_result = max(sweep, key=selection_key)
                threshold = float(best_threshold_result["threshold"])
                result = {
                    "model_name": name,
                    "selected_threshold": threshold,
                    "threshold_selection_split": "development_validation",
                    "model_selection_split": "development_validation",
                    "validation_threshold_sweep": sweep,
                    "metrics_by_split": {
                        "development_train": metrics_at_threshold(y_train, train_scores, threshold),
                        "development_validation": metrics_at_threshold(y_val, val_scores, threshold),
                    },
                }
                model_results.append(result)
                fitted[name] = Pipeline([("features", features), ("classifier", classifier)])
    best = max(model_results, key=lambda item: selection_key(item["metrics_by_split"]["development_validation"]))
    return fitted[str(best["model_name"])], best, model_results


def run(*, train: Path, validation: Path, output_dir: Path, model_output: Path, config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    train_source = load_jsonl(train)
    validation_source = load_jsonl(validation)
    train_rows = binary_eligible_rows(train_source, allowed_partitions={"development_train"})
    validation_rows = binary_eligible_rows(validation_source, allowed_partitions={"development_validation"})
    assert len(train_rows) == len([row for row in train_source if row in train_rows])
    assert_safe_rows_only(train_rows + validation_rows)
    model, best, model_results = train_and_select(train_rows=train_rows, validation_rows=validation_rows, config=config)
    threshold = float(best["selected_threshold"])
    train_scores = probabilities(model, train_rows)
    validation_scores = probabilities(model, validation_rows)
    y_train = binary_labels(train_rows)
    y_val = binary_labels(validation_rows)
    train_pred = [1 if score >= threshold else 0 for score in train_scores]
    val_pred = [1 if score >= threshold else 0 for score in validation_scores]
    diagnostics = {
        "accuracy_gap": best["metrics_by_split"]["development_train"]["accuracy"] - best["metrics_by_split"]["development_validation"]["accuracy"],
        "f1_gap": best["metrics_by_split"]["development_train"]["f1"] - best["metrics_by_split"]["development_validation"]["f1"],
    }
    diagnostics["warnings"] = [name for name, value in diagnostics.items() if name.endswith("_gap") and isinstance(value, float) and value > 0.15]
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"model_type": "binary_v4", "model": model, "threshold": threshold, "safe_model_fields": SAFE_MODEL_FIELDS, "config": config, "selected_model": best["model_name"]}
    joblib.dump(payload, model_output)
    predictions = [
        {"case_id": row.get("case_id"), "repository": row.get("repository"), "language": row.get("language"), "split": split, "gold": int(gold), "prediction": int(pred), "probability": score}
        for split, rows, labels, preds, scores in [
            ("development_train", train_rows, y_train, train_pred, train_scores),
            ("development_validation", validation_rows, y_val, val_pred, validation_scores),
        ]
        for row, gold, pred, score in zip(rows, labels, preds, scores)
    ]
    summary = {
        "status": "ok",
        "model_version": "binary_v4",
        "selected_model": best["model_name"],
        "selected_threshold": threshold,
        "selection_metric": "mcc",
        "safe_model_fields": SAFE_MODEL_FIELDS,
        "config": config,
        "config_sha256": sha256_file(config_path),
        "runtime_versions": runtime_versions(),
        "row_counts": {"train_source": len(train_source), "train_used": len(train_rows), "validation_source": len(validation_source), "validation_used": len(validation_rows)},
        "class_counts": {"development_train": dict(Counter(y_train)), "development_validation": dict(Counter(y_val))},
        "natural_class_distribution_preserved": len(train_source) == len(train_rows) and len(validation_source) == len(validation_rows),
        "majority_baseline": {"development_validation": majority_binary_baseline(y_val)},
        "best_metrics": best["metrics_by_split"],
        "per_language": {"development_validation": per_language_binary_metrics(validation_rows, y_val, val_pred, validation_scores)},
        "train_validation_gap": diagnostics,
        "model_results": model_results,
        "outputs": {"model": str(model_output), "summary": str(output_dir / "training_summary.json"), "predictions": str(output_dir / "development_predictions.jsonl")},
    }
    write_json(output_dir / "training_summary.json", summary)
    write_json(output_dir / "model_comparison.json", {"model_results": model_results})
    write_jsonl(output_dir / "development_predictions.jsonl", predictions)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Train Final Binary V4 on development train/validation only.")
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    print(json.dumps(run(train=Path(args.train), validation=Path(args.validation), output_dir=Path(args.output_dir), model_output=Path(args.model_output), config_path=Path(args.config)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
