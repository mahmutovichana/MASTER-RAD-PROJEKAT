from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ALLOWED_BOOL_TRUE = {"true", "1", "yes", "y"}
ALLOWED_BOOL_FALSE = {"false", "0", "no", "n"}

ALLOWED_CATEGORIES = {
    "no_update",
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

ALLOWED_CONFIDENCE = {"high", "medium", "low"}


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


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    text = str(value or "").strip().lower()

    if text in ALLOWED_BOOL_TRUE:
        return True

    if text in ALLOWED_BOOL_FALSE:
        return False

    raise ValueError(f"Invalid boolean value: {value!r}")


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def matthews_corrcoef_binary(tp: int, fp: int, tn: int, fn: int) -> float:
    denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    if denominator == 0:
        return 0.0

    return ((tp * tn) - (fp * fn)) / denominator


def compute_binary_metrics(
    *,
    gold_values: list[bool],
    pred_values: list[bool],
) -> dict[str, Any]:
    tp = fp = tn = fn = 0

    for gold, pred in zip(gold_values, pred_values):
        if gold and pred:
            tp += 1
        elif not gold and pred:
            fp += 1
        elif not gold and not pred:
            tn += 1
        elif gold and not pred:
            fn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    specificity = safe_div(tn, tn + fp)
    balanced_accuracy = (recall + specificity) / 2

    return {
        "total_cases": len(gold_values),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": safe_div(tp + tn, len(gold_values)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "balanced_accuracy": balanced_accuracy,
        "mcc": matthews_corrcoef_binary(tp=tp, fp=fp, tn=tn, fn=fn),
        "gold_distribution": dict(Counter(str(value) for value in gold_values)),
        "pred_distribution": dict(Counter(str(value) for value in pred_values)),
    }


def cohen_kappa_binary(a_values: list[bool], b_values: list[bool]) -> dict[str, Any]:
    if len(a_values) != len(b_values):
        raise ValueError("Kappa inputs must have equal length.")

    total = len(a_values)

    if total == 0:
        return {
            "observed_agreement": 0.0,
            "expected_agreement": 0.0,
            "kappa": 0.0,
        }

    observed = sum(1 for a, b in zip(a_values, b_values) if a == b) / total

    a_counts = Counter(a_values)
    b_counts = Counter(b_values)

    expected = 0.0
    for value in [False, True]:
        expected += (a_counts[value] / total) * (b_counts[value] / total)

    if expected == 1.0:
        kappa = 1.0 if observed == 1.0 else 0.0
    else:
        kappa = (observed - expected) / (1 - expected)

    return {
        "observed_agreement": observed,
        "expected_agreement": expected,
        "kappa": kappa,
    }


def validate_review_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []

    seen_audit_ids: set[str] = set()
    seen_case_ids: set[str] = set()

    required_columns = {
        "audit_id",
        "case_id",
        "review_docs_update_required",
        "review_doc_category",
        "review_confidence",
        "review_notes",
    }

    for index, row in enumerate(rows, start=1):
        missing = sorted(required_columns - set(row.keys()))
        if missing:
            errors.append(f"Row {index}: missing columns: {missing}")
            continue

        audit_id = normalize_text(row.get("audit_id"))
        case_id = normalize_text(row.get("case_id"))

        if not audit_id:
            errors.append(f"Row {index}: missing audit_id")
        elif audit_id in seen_audit_ids:
            errors.append(f"Row {index}: duplicate audit_id {audit_id}")
        else:
            seen_audit_ids.add(audit_id)

        if not case_id:
            errors.append(f"Row {index}: missing case_id")
        elif case_id in seen_case_ids:
            errors.append(f"Row {index}: duplicate case_id {case_id}")
        else:
            seen_case_ids.add(case_id)

        try:
            review_bool = normalize_bool(row.get("review_docs_update_required"))
        except ValueError as exc:
            errors.append(f"Row {index}: {exc}")
            continue

        category = normalize_text(row.get("review_doc_category"))
        confidence = normalize_text(row.get("review_confidence")).lower()

        if category not in ALLOWED_CATEGORIES:
            errors.append(f"Row {index}: invalid review_doc_category {category!r}")

        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"Row {index}: invalid review_confidence {confidence!r}")

        if not review_bool and category != "no_update":
            errors.append(
                f"Row {index}: False review_docs_update_required must use no_update category."
            )

        if review_bool and category == "no_update":
            errors.append(
                f"Row {index}: True review_docs_update_required must not use no_update category."
            )

    return errors


def disagreement_type(protocol_label: bool, review_label: bool) -> str:
    if protocol_label == review_label:
        return "agree"

    if protocol_label and not review_label:
        return "protocol_true_review_false"

    return "protocol_false_review_true"


def index_key_rows(key_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}

    for row in key_rows:
        audit_id = normalize_text(row.get("audit_id"))
        if audit_id:
            indexed[audit_id] = row

    return indexed


def merge_review_and_key(
    *,
    review_rows: list[dict[str, Any]],
    key_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    key_by_audit_id = index_key_rows(key_rows)
    merged_rows: list[dict[str, Any]] = []

    for row in review_rows:
        audit_id = normalize_text(row.get("audit_id"))

        if audit_id not in key_by_audit_id:
            raise ValueError(f"Audit ID not found in key file: {audit_id}")

        key = key_by_audit_id[audit_id]

        review_label = normalize_bool(row.get("review_docs_update_required"))
        protocol_label = normalize_bool(key.get("gold_docs_update_required"))
        model_pred = normalize_bool(key.get("pred_docs_update_required"))

        merged = {
            "audit_id": audit_id,
            "case_id": normalize_text(row.get("case_id")),
            "repository": normalize_text(key.get("repository")),
            "language": normalize_text(key.get("language")),
            "candidate_type": normalize_text(key.get("candidate_type")),
            "dataset_split": normalize_text(key.get("dataset_split")),
            "review_docs_update_required": review_label,
            "review_doc_category": normalize_text(row.get("review_doc_category")),
            "review_confidence": normalize_text(row.get("review_confidence")).lower(),
            "review_notes": normalize_text(row.get("review_notes")),
            "protocol_docs_update_required": protocol_label,
            "protocol_doc_category": normalize_text(key.get("gold_doc_category")),
            "protocol_label_confidence": normalize_text(key.get("label_confidence")),
            "protocol_label_source": normalize_text(key.get("label_source")),
            "model_pred_docs_update_required": model_pred,
            "model_pred_probability": key.get("pred_probability"),
            "model_threshold": key.get("swept_threshold"),
            "protocol_review_disagreement_type": disagreement_type(protocol_label, review_label),
            "model_correct_against_review": model_pred == review_label,
            "model_correct_against_protocol": model_pred == protocol_label,
        }

        merged_rows.append(merged)

    return merged_rows


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "unknown") for row in rows))


def nested_disagreement_counts(rows: list[dict[str, Any]], group_key: str) -> dict[str, dict[str, int]]:
    output: dict[str, Counter[str]] = defaultdict(Counter)

    for row in rows:
        group = str(row.get(group_key) or "unknown")
        disagreement = str(row.get("protocol_review_disagreement_type") or "unknown")
        output[group][disagreement] += 1

    return {
        group: dict(counter)
        for group, counter in sorted(output.items())
    }


def category_agreement(rows: list[dict[str, Any]]) -> dict[str, Any]:
    positive_rows = [
        row
        for row in rows
        if row["review_docs_update_required"] and row["protocol_docs_update_required"]
    ]

    if not positive_rows:
        return {
            "positive_overlap_cases": 0,
            "category_agreement": 0.0,
        }

    agree = sum(
        1
        for row in positive_rows
        if row["review_doc_category"] == row["protocol_doc_category"]
    )

    return {
        "positive_overlap_cases": len(positive_rows),
        "category_agreement": safe_div(agree, len(positive_rows)),
        "review_category_distribution": count_by(positive_rows, "review_doc_category"),
        "protocol_category_distribution": count_by(positive_rows, "protocol_doc_category"),
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Blind Label Audit Evaluation",
        "",
        "## Input files",
        "",
        f"- Review CSV: `{report['review_csv']}`",
        f"- Key JSONL: `{report['key_jsonl']}`",
        "",
        "## Validation",
        "",
        f"- Status: `{report['validation']['status']}`",
        f"- Review rows: `{report['total_rows']}`",
        "",
        "## Review label distribution",
        "",
        "```json",
        json.dumps(report["review_distribution"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Protocol label distribution",
        "",
        "```json",
        json.dumps(report["protocol_distribution"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Review vs protocol labels",
        "",
        f"- Binary agreement: `{report['review_vs_protocol']['binary_agreement']:.4f}`",
        f"- Cohen's kappa: `{report['review_vs_protocol']['cohen_kappa']['kappa']:.4f}`",
        "",
        "```json",
        json.dumps(report["review_vs_protocol"]["confusion"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## V2 model vs human-corrected review labels",
        "",
        "```json",
        json.dumps(report["model_vs_review"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## V2 model vs protocol labels on the same audit sample",
        "",
        "```json",
        json.dumps(report["model_vs_protocol_on_same_sample"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Disagreements by language",
        "",
        "```json",
        json.dumps(report["review_vs_protocol"]["disagreements_by_language"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Disagreements by candidate type",
        "",
        "```json",
        json.dumps(report["review_vs_protocol"]["disagreements_by_candidate_type"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Methodological note",
        "",
        "This audit evaluates agreement between protocol-derived labels and the human-corrected review labels on a stratified subset. "
        "The model performance against review labels should be interpreted as an audit-subset estimate, not as a replacement for the frozen locked-test result.",
        "",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    review_csv: Path,
    key_jsonl: Path,
    output_json: Path,
    output_md: Path,
) -> dict[str, Any]:
    review_rows = load_csv(review_csv)
    key_rows = load_jsonl(key_jsonl)

    validation_errors = validate_review_rows(review_rows)

    if validation_errors:
        report = {
            "status": "invalid",
            "review_csv": str(review_csv),
            "key_jsonl": str(key_jsonl),
            "validation": {
                "status": "failed",
                "errors": validation_errors,
            },
        }
        write_json(output_json, report)
        raise ValueError(f"Review CSV validation failed with {len(validation_errors)} errors.")

    merged_rows = merge_review_and_key(review_rows=review_rows, key_rows=key_rows)

    review_values = [bool(row["review_docs_update_required"]) for row in merged_rows]
    protocol_values = [bool(row["protocol_docs_update_required"]) for row in merged_rows]
    model_values = [bool(row["model_pred_docs_update_required"]) for row in merged_rows]

    review_protocol_agree = sum(
        1
        for review, protocol in zip(review_values, protocol_values)
        if review == protocol
    )

    review_vs_protocol_metrics = compute_binary_metrics(
        gold_values=review_values,
        pred_values=protocol_values,
    )

    model_vs_review_metrics = compute_binary_metrics(
        gold_values=review_values,
        pred_values=model_values,
    )

    model_vs_protocol_metrics = compute_binary_metrics(
        gold_values=protocol_values,
        pred_values=model_values,
    )

    report = {
        "status": "ok",
        "review_csv": str(review_csv),
        "key_jsonl": str(key_jsonl),
        "total_rows": len(merged_rows),
        "validation": {
            "status": "ok",
            "errors": [],
        },
        "review_distribution": {
            "binary": count_by(merged_rows, "review_docs_update_required"),
            "category": count_by(merged_rows, "review_doc_category"),
            "confidence": count_by(merged_rows, "review_confidence"),
        },
        "protocol_distribution": {
            "binary": count_by(merged_rows, "protocol_docs_update_required"),
            "category": count_by(merged_rows, "protocol_doc_category"),
            "confidence": count_by(merged_rows, "protocol_label_confidence"),
            "source": count_by(merged_rows, "protocol_label_source"),
        },
        "review_vs_protocol": {
            "binary_agreement": safe_div(review_protocol_agree, len(merged_rows)),
            "cohen_kappa": cohen_kappa_binary(review_values, protocol_values),
            "confusion": review_vs_protocol_metrics,
            "category_agreement_on_positive_overlap": category_agreement(merged_rows),
            "disagreements_by_language": nested_disagreement_counts(merged_rows, "language"),
            "disagreements_by_candidate_type": nested_disagreement_counts(merged_rows, "candidate_type"),
            "disagreements_by_split": nested_disagreement_counts(merged_rows, "dataset_split"),
        },
        "model_vs_review": model_vs_review_metrics,
        "model_vs_protocol_on_same_sample": model_vs_protocol_metrics,
        "interpretation": {
            "review_label_role": "Human-corrected audit labels are used to estimate label quality on a stratified audit subset.",
            "primary_result_policy": "This audit does not replace the frozen 4k V2 locked-test result; it validates label quality and model behavior on the audit subset.",
        },
    }

    write_json(output_json, report)
    write_markdown(output_md, report)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate blind label audit review labels against the hidden key.")
    parser.add_argument("--review-csv", required=True)
    parser.add_argument("--key-jsonl", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)

    args = parser.parse_args()

    report = run(
        review_csv=Path(args.review_csv),
        key_jsonl=Path(args.key_jsonl),
        output_json=Path(args.output_json),
        output_md=Path(args.output_md),
    )

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())