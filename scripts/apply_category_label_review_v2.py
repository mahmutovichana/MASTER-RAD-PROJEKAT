from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


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

ALLOWED_REVIEW_DECISIONS = {
    "",
    "keep",
    "update",
    "exclude",
    "no_update",
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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def normalize_category(value: Any) -> str | None:
    raw = str(value or "").strip().lower()

    if not raw or raw in {"no_update", "not_available", "none", "null"}:
        return None

    normalized = TARGET_CATEGORY_ALIASES.get(raw, raw)

    if normalized in THESIS4_CATEGORIES:
        return normalized

    return None


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def load_review_decisions(path: Path) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        for line_number, row in enumerate(reader, start=2):
            case_id = str(row.get("case_id") or "").strip()
            if not case_id:
                continue

            if case_id in decisions:
                raise ValueError(f"Duplicate case_id in review CSV at line {line_number}: {case_id}")

            decision = str(row.get("review_decision") or "").strip().lower()
            if decision not in ALLOWED_REVIEW_DECISIONS:
                raise ValueError(
                    f"{case_id}: invalid review_decision={decision!r}. "
                    f"Allowed: {sorted(ALLOWED_REVIEW_DECISIONS)}"
                )

            review_category_raw = str(row.get("review_doc_category") or "").strip()
            review_category = normalize_category(review_category_raw)

            if decision == "update" and review_category is None:
                raise ValueError(
                    f"{case_id}: review_decision=update requires review_doc_category "
                    f"one of {sorted(THESIS4_CATEGORIES)}"
                )

            decisions[case_id] = {
                "case_id": case_id,
                "dataset_split": str(row.get("dataset_split") or "").strip(),
                "review_decision": decision,
                "review_doc_category": review_category,
                "review_notes": str(row.get("review_notes") or "").strip(),
                "current_gold_doc_category": str(row.get("current_gold_doc_category") or "").strip(),
            }

    return decisions


def apply_to_split(
    *,
    rows: list[dict[str, Any]],
    split_name: str,
    decisions: dict[str, dict[str, Any]],
    allow_locked_review: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output: list[dict[str, Any]] = []

    stats = Counter()
    category_before = Counter()
    category_after = Counter()

    for row in rows:
        case_id = str(row.get("case_id") or "").strip()
        current_category = normalize_category(row.get("gold_doc_category"))
        if current_category:
            category_before[current_category] += 1

        decision = decisions.get(case_id)

        if split_name == "locked_test":
            if decision and not allow_locked_review:
                raise ValueError(
                    f"Review CSV contains locked-test case {case_id}. "
                    "This is blocked by default to avoid locked-test leakage."
                )

            copied = dict(row)
            output.append(copied)

            after_category = normalize_category(copied.get("gold_doc_category"))
            if after_category:
                category_after[after_category] += 1
            stats["kept_locked_unchanged"] += 1
            continue

        if decision is None:
            copied = dict(row)
            output.append(copied)

            after_category = normalize_category(copied.get("gold_doc_category"))
            if after_category:
                category_after[after_category] += 1
            stats["kept_no_review"] += 1
            continue

        review_decision = str(decision["review_decision"])

        if review_decision in {"", "keep"}:
            copied = dict(row)
            copied["category_review_status"] = "reviewed_keep" if review_decision == "keep" else "not_explicitly_reviewed"
            copied["category_review_notes"] = decision.get("review_notes") or ""
            output.append(copied)

            after_category = normalize_category(copied.get("gold_doc_category"))
            if after_category:
                category_after[after_category] += 1
            stats["kept_reviewed"] += 1
            continue

        if review_decision == "exclude":
            stats["excluded_by_review"] += 1
            continue

        if review_decision == "no_update":
            copied = dict(row)
            copied["gold_docs_update_required"] = False
            copied["gold_doc_category"] = "no_update"
            copied["category_review_status"] = "reviewed_no_update"
            copied["category_review_notes"] = decision.get("review_notes") or ""
            output.append(copied)
            stats["changed_to_no_update"] += 1
            continue

        if review_decision == "update":
            review_category = decision["review_doc_category"]
            if review_category is None:
                raise AssertionError("update decision without review_doc_category should have been rejected earlier")

            copied = dict(row)
            copied["gold_docs_update_required"] = True
            copied["gold_doc_category"] = review_category
            copied["category_review_status"] = "reviewed_category_updated"
            copied["category_review_previous_category"] = current_category
            copied["category_review_notes"] = decision.get("review_notes") or ""
            output.append(copied)

            category_after[review_category] += 1
            stats["updated_category"] += 1
            continue

        raise AssertionError(f"Unhandled review decision: {review_decision}")

    return output, {
        "split": split_name,
        "input_rows": len(rows),
        "output_rows": len(output),
        "stats": dict(stats),
        "category_before": dict(category_before),
        "category_after": dict(category_after),
    }


def run(
    *,
    train_path: Path,
    validation_path: Path,
    locked_test_path: Path,
    review_csv: Path,
    output_dir: Path,
    allow_locked_review: bool,
) -> dict[str, Any]:
    decisions = load_review_decisions(review_csv)

    locked_decisions = [
        case_id
        for case_id, decision in decisions.items()
        if str(decision.get("dataset_split") or "") == "locked_test"
    ]
    if locked_decisions and not allow_locked_review:
        raise ValueError(
            f"Review CSV contains locked-test rows ({len(locked_decisions)}). "
            "Remove them or pass --allow-locked-review only for a separate non-final experiment."
        )

    train_rows = load_jsonl(train_path)
    validation_rows = load_jsonl(validation_path)
    locked_rows = load_jsonl(locked_test_path)

    train_out, train_summary = apply_to_split(
        rows=train_rows,
        split_name="train",
        decisions=decisions,
        allow_locked_review=allow_locked_review,
    )
    validation_out, validation_summary = apply_to_split(
        rows=validation_rows,
        split_name="validation",
        decisions=decisions,
        allow_locked_review=allow_locked_review,
    )
    locked_out, locked_summary = apply_to_split(
        rows=locked_rows,
        split_name="locked_test",
        decisions=decisions,
        allow_locked_review=allow_locked_review,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    train_output = output_dir / "real_pr_gold_4k_category_v2_train.jsonl"
    validation_output = output_dir / "real_pr_gold_4k_category_v2_validation.jsonl"
    locked_output = output_dir / "real_pr_gold_4k_category_v2_locked_test.jsonl"

    write_jsonl(train_output, train_out)
    write_jsonl(validation_output, validation_out)
    write_jsonl(locked_output, locked_out)

    summary = {
        "status": "ok",
        "review_csv": str(review_csv),
        "outputs": {
            "train": str(train_output),
            "validation": str(validation_output),
            "locked_test": str(locked_output),
        },
        "review_decision_counts": dict(Counter(str(item["review_decision"]) for item in decisions.values())),
        "split_summaries": {
            "train": train_summary,
            "validation": validation_summary,
            "locked_test": locked_summary,
        },
        "methodology": {
            "locked_test_modified": bool(allow_locked_review),
            "default_policy": "Locked test remains unchanged. Category review is applied only to train/validation.",
            "model_input_policy": "This script changes target labels only. It does not add prediction rules or model input features.",
        },
    }

    write_json(output_dir / "category_label_review_v2_apply_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply train/validation category label review decisions and keep locked test unchanged."
    )
    parser.add_argument("--train", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--locked-test", required=True)
    parser.add_argument("--review-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--allow-locked-review", action="store_true")

    args = parser.parse_args()

    run(
        train_path=Path(args.train),
        validation_path=Path(args.validation),
        locked_test_path=Path(args.locked_test),
        review_csv=Path(args.review_csv),
        output_dir=Path(args.output_dir),
        allow_locked_review=bool(args.allow_locked_review),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())