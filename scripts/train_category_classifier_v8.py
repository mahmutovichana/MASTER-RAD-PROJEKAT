from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, assert_safe_rows_only, category_eligible_rows, category_labels, category_scope_counts, load_jsonl, write_json, write_jsonl
from docguard_ml_v2.features import char_tfidf, word_char_tfidf, word_tfidf
from docguard_ml_v2.metrics import category_metrics, majority_category_baseline, per_language_category_metrics
from docguard_ml_v2.model_manifest import runtime_versions, sha256_file


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def make_classifier(c_value: float, seed: int) -> LogisticRegression:
    return LogisticRegression(C=c_value, max_iter=4000, random_state=seed, solver="lbfgs")


def make_candidates(config: dict[str, Any]) -> dict[str, Pipeline]:
    seed = int(config["seed"])
    candidates: dict[str, Pipeline] = {}
    for c_value in [float(value) for value in config["hyperparameter_grid"]["C"]]:
        for min_df in [int(value) for value in config["hyperparameter_grid"]["min_df"]]:
            candidates[f"word_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", word_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
            candidates[f"char_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", char_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
            candidates[f"word_char_tfidf_logreg_c{c_value}_mindf{min_df}"] = Pipeline([("features", word_char_tfidf(min_df=min_df)), ("classifier", make_classifier(c_value, seed))])
    return candidates


def train_and_select(train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], config: dict[str, Any]) -> tuple[Pipeline, dict[str, Any], list[dict[str, Any]]]:
    y_train = category_labels(train_rows)
    y_val = category_labels(validation_rows)
    results: list[dict[str, Any]] = []
    fitted: dict[str, Pipeline] = {}
    seed = int(config["seed"])
    c_values = [float(value) for value in config["hyperparameter_grid"]["C"]]
    min_df_values = [int(value) for value in config["hyperparameter_grid"]["min_df"]]
    feature_factories = {
        "word_tfidf_logreg": word_tfidf,
        "char_tfidf_logreg": char_tfidf,
        "word_char_tfidf_logreg": word_char_tfidf,
    }
    for prefix, factory in feature_factories.items():
        for min_df in min_df_values:
            features = factory(min_df=min_df)
            x_train = features.fit_transform(train_rows)
            x_val = features.transform(validation_rows)
            for c_value in c_values:
                name = f"{prefix}_c{c_value}_mindf{min_df}"
                classifier = make_classifier(c_value, seed)
                classifier.fit(x_train, y_train)
                train_pred = [str(item) for item in classifier.predict(x_train)]
                val_pred = [str(item) for item in classifier.predict(x_val)]
                result = {
                    "model_name": name,
                    "model_selection_split": "development_validation",
                    "metrics_by_split": {
                        "development_train": category_metrics(y_train, train_pred, PRIMARY_STAGE2_LABELS),
                        "development_validation": category_metrics(y_val, val_pred, PRIMARY_STAGE2_LABELS),
                    },
                }
                results.append(result)
                fitted[name] = Pipeline([("features", features), ("classifier", classifier)])
    best = max(results, key=lambda item: (item["metrics_by_split"]["development_validation"]["macro_f1"], item["metrics_by_split"]["development_validation"]["weighted_f1"], item["metrics_by_split"]["development_validation"]["accuracy"]))
    return fitted[str(best["model_name"])], best, results


def run(*, train: Path, validation: Path, output_dir: Path, model_output: Path, config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    train_source = load_jsonl(train)
    validation_source = load_jsonl(validation)
    train_rows = category_eligible_rows(train_source, allowed_partitions={"development_train"})
    validation_rows = category_eligible_rows(validation_source, allowed_partitions={"development_validation"})
    assert_safe_rows_only(train_rows + validation_rows)
    model, best, model_results = train_and_select(train_rows, validation_rows, config)
    y_train = category_labels(train_rows)
    y_val = category_labels(validation_rows)
    train_pred = [str(item) for item in model.predict(train_rows)]
    val_pred = [str(item) for item in model.predict(validation_rows)]
    train_macro = best["metrics_by_split"]["development_train"]["macro_f1"]
    val_macro = best["metrics_by_split"]["development_validation"]["macro_f1"]
    train_acc = best["metrics_by_split"]["development_train"]["accuracy"]
    val_acc = best["metrics_by_split"]["development_validation"]["accuracy"]
    diagnostics = {"accuracy_gap": train_acc - val_acc, "macro_f1_gap": train_macro - val_macro, "warnings": []}
    if diagnostics["accuracy_gap"] > 0.15:
        diagnostics["warnings"].append("train_accuracy_validation_accuracy_gap_gt_0.15")
    if diagnostics["macro_f1_gap"] > 0.15:
        diagnostics["warnings"].append("train_macro_f1_validation_macro_f1_gap_gt_0.15")
    output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model_type": "category_v8", "model": model, "safe_model_fields": SAFE_MODEL_FIELDS, "labels": PRIMARY_STAGE2_LABELS, "config": config, "selected_model": best["model_name"]}, model_output)
    predictions = [
        {"case_id": row.get("case_id"), "repository": row.get("repository"), "language": row.get("language"), "split": split, "gold": gold, "prediction": pred}
        for split, rows, labels, preds in [
            ("development_train", train_rows, y_train, train_pred),
            ("development_validation", validation_rows, y_val, val_pred),
        ]
        for row, gold, pred in zip(rows, labels, preds)
    ]
    summary = {
        "status": "ok",
        "model_version": "category_v8",
        "selected_model": best["model_name"],
        "selection_metric": "macro_f1",
        "safe_model_fields": SAFE_MODEL_FIELDS,
        "allowed_primary_stage2_labels": PRIMARY_STAGE2_LABELS,
        "config": config,
        "config_sha256": sha256_file(config_path),
        "runtime_versions": runtime_versions(),
        "scope_counts": {"development_train": category_scope_counts(train_source), "development_validation": category_scope_counts(validation_source)},
        "majority_baseline": {"development_validation": majority_category_baseline(y_val, PRIMARY_STAGE2_LABELS)},
        "best_metrics": best["metrics_by_split"],
        "per_language": {"development_validation": per_language_category_metrics(validation_rows, y_val, val_pred, PRIMARY_STAGE2_LABELS)},
        "train_validation_gap": diagnostics,
        "model_results": model_results,
        "outputs": {"model": str(model_output), "summary": str(output_dir / "training_summary.json"), "predictions": str(output_dir / "development_predictions.jsonl")},
    }
    write_json(output_dir / "training_summary.json", summary)
    write_json(output_dir / "model_comparison.json", {"model_results": model_results})
    write_jsonl(output_dir / "development_predictions.jsonl", predictions)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Train Final Category V8 on development train/validation only.")
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
