from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline


SAFE_MODEL_INPUT_FIELDS = {
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(value)

    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None:
        return []
    return [str(value)]


def build_text(row: dict[str, Any]) -> str:
    """
    Only safe model-facing fields are used here.

    Gold labels, docs-after text, docs diff, source URL, PR title,
    manual notes, and audit fields are intentionally excluded.
    """
    language = str(row.get("language") or "unknown")
    changed_files = _safe_list(row.get("code_changed_files"))
    code_diff = str(row.get("code_diff_excerpt") or "")
    docs_before = str(row.get("docs_before_excerpt") or "")

    return "\n".join(
        [
            f"LANGUAGE: {language}",
            "CODE_CHANGED_FILES:",
            "\n".join(changed_files),
            "CODE_DIFF:",
            code_diff,
            "DOCS_BEFORE:",
            docs_before,
        ]
    )


def labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if _safe_bool(row.get("gold_docs_update_required")) else 0 for row in rows]


def make_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=0.95,
                    sublinear_tf=True,
                    max_features=80_000,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    solver="liblinear",
                    random_state=42,
                ),
            ),
        ]
    )


def predict_probabilities(model: Pipeline, rows: list[dict[str, Any]]) -> list[float]:
    texts = [build_text(row) for row in rows]
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(texts)
        return [float(item[1]) for item in probabilities]
    scores = model.decision_function(texts)
    return [1.0 / (1.0 + math.exp(-float(score))) for score in scores]


def predict_with_threshold(probabilities: list[float], threshold: float) -> list[int]:
    return [1 if probability >= threshold else 0 for probability in probabilities]


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def compute_metrics(gold: list[int], pred: list[int]) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(gold, pred, labels=[0, 1]).ravel()

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)

    return {
        "total_cases": len(gold),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "accuracy": safe_div(tp + tn, len(gold)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "gold_distribution": dict(Counter(str(bool(item)) for item in gold)),
        "pred_distribution": dict(Counter(str(bool(item)) for item in pred)),
    }


def choose_threshold(model: Pipeline, validation_rows: list[dict[str, Any]]) -> dict[str, Any]:
    gold = labels(validation_rows)
    probabilities = predict_probabilities(model, validation_rows)

    candidates = [round(value / 100, 2) for value in range(5, 96, 5)]
    best: dict[str, Any] | None = None

    for threshold in candidates:
        pred = predict_with_threshold(probabilities, threshold)
        metrics = compute_metrics(gold, pred)
        candidate = {
            "threshold": threshold,
            "metrics": metrics,
        }

        if best is None:
            best = candidate
            continue

        current_key = (
            metrics["f1"],
            metrics["precision"],
            metrics["recall"],
            metrics["accuracy"],
        )
        best_metrics = best["metrics"]
        best_key = (
            best_metrics["f1"],
            best_metrics["precision"],
            best_metrics["recall"],
            best_metrics["accuracy"],
        )

        if current_key > best_key:
            best = candidate

    assert best is not None
    return best


def build_predictions(
    *,
    model: Pipeline,
    rows: list[dict[str, Any]],
    threshold: float,
    split_name: str,
) -> list[dict[str, Any]]:
    probabilities = predict_probabilities(model, rows)
    pred = predict_with_threshold(probabilities, threshold)
    gold = labels(rows)

    output: list[dict[str, Any]] = []

    for row, probability, pred_label, gold_label in zip(rows, probabilities, pred, gold):
        output.append(
            {
                "case_id": row.get("case_id"),
                "dataset_split": split_name,
                "repository": row.get("repository"),
                "language": row.get("language"),
                "label_confidence": row.get("label_confidence"),
                "label_source": row.get("label_source"),
                "gold_docs_update_required": bool(gold_label),
                "pred_docs_update_required": bool(pred_label),
                "pred_probability": probability,
                "binary_correct": bool(gold_label) == bool(pred_label),
                "gold_doc_category": row.get("gold_doc_category"),
                "candidate_type": row.get("candidate_type"),
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
) -> dict[str, Any]:
    train_rows = load_jsonl(train_path)
    validation_rows = load_jsonl(validation_path)
    locked_test_rows = load_jsonl(locked_test_path)

    model = make_pipeline()
    model.fit([build_text(row) for row in train_rows], labels(train_rows))

    threshold_result = choose_threshold(model, validation_rows)
    threshold = float(threshold_result["threshold"])

    train_predictions = build_predictions(model=model, rows=train_rows, threshold=threshold, split_name="train")
    validation_predictions = build_predictions(model=model, rows=validation_rows, threshold=threshold, split_name="validation")
    locked_predictions = build_predictions(model=model, rows=locked_test_rows, threshold=threshold, split_name="locked_test")

    train_metrics = compute_metrics(
        [1 if row["gold_docs_update_required"] else 0 for row in train_predictions],
        [1 if row["pred_docs_update_required"] else 0 for row in train_predictions],
    )
    validation_metrics = compute_metrics(
        [1 if row["gold_docs_update_required"] else 0 for row in validation_predictions],
        [1 if row["pred_docs_update_required"] else 0 for row in validation_predictions],
    )
    locked_metrics = compute_metrics(
        [1 if row["gold_docs_update_required"] else 0 for row in locked_predictions],
        [1 if row["pred_docs_update_required"] else 0 for row in locked_predictions],
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    model_output.parent.mkdir(parents=True, exist_ok=True)

    predictions_path = output_dir / "real_gold_classifier_predictions.jsonl"
    report_json_path = output_dir / "real_gold_classifier_report.json"
    report_md_path = output_dir / "real_gold_classifier_report.md"

    all_predictions = train_predictions + validation_predictions + locked_predictions
    write_jsonl(predictions_path, all_predictions)
    joblib.dump(model, model_output)

    report = {
        "status": "ok",
        "model_type": "tfidf_logistic_regression",
        "model_output": str(model_output),
        "train_path": str(train_path),
        "validation_path": str(validation_path),
        "locked_test_path": str(locked_test_path),
        "predictions": str(predictions_path),
        "safe_model_input_fields": sorted(SAFE_MODEL_INPUT_FIELDS),
        "label_warning": "Labels are AI-assisted draft labels unless manually reviewed.",
        "selected_threshold_from_validation": threshold,
        "validation_threshold_selection_metrics": threshold_result["metrics"],
        "metrics": {
            "train": train_metrics,
            "validation": validation_metrics,
            "locked_test": locked_metrics,
        },
        "split_sizes": {
            "train": len(train_rows),
            "validation": len(validation_rows),
            "locked_test": len(locked_test_rows),
        },
    }

    write_json(report_json_path, report)
    write_markdown_report(report_md_path, report)

    return report


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_markdown_report(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# DocGuard Real Gold Classifier Report",
        "",
        "This report trains a non-rule-based classifier on labeled real public GitHub PR records.",
        "",
        f"- Model: `{report['model_type']}`",
        f"- Selected threshold from validation: `{report['selected_threshold_from_validation']}`",
        f"- Label warning: {report['label_warning']}",
        "",
        "## Safe Model Input Fields",
        "",
    ]

    for field in report["safe_model_input_fields"]:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Metrics",
            "",
            "| Split | Cases | Accuracy | Precision | Recall | F1 | Specificity | FPR | TP | FP | TN | FN |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for split in ["train", "validation", "locked_test"]:
        metrics = report["metrics"][split]
        lines.append(
            "| "
            + " | ".join(
                [
                    split,
                    str(metrics["total_cases"]),
                    pct(metrics["accuracy"]),
                    pct(metrics["precision"]),
                    pct(metrics["recall"]),
                    pct(metrics["f1"]),
                    pct(metrics["specificity"]),
                    pct(metrics["false_positive_rate"]),
                    str(metrics["true_positives"]),
                    str(metrics["false_positives"]),
                    str(metrics["true_negatives"]),
                    str(metrics["false_negatives"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- This is a trained classifier, not a rule-based detector.",
            "- Threshold selection uses validation only.",
            "- Locked-test metrics should be treated as draft until the locked-test labels are manually reviewed.",
            "- The model uses only language, changed code files, code diff excerpt, and docs-before excerpt.",
            "- Gold labels, docs-after text, PR titles, source URLs, docs diffs and manual notes are not used as model input.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Train/evaluate a DocGuard real-data binary classifier.")
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-output", required=True)
    args = parser.parse_args()

    result = run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        output_dir=Path(args.output_dir),
        model_output=Path(args.model_output),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())