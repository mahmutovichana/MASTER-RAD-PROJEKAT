from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SAFE_MODEL_FIELDS = ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"]
PRIMARY_STAGE2_LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
OTHER_DOCUMENTATION_LABEL = "other_documentation"
NO_UPDATE_LABEL = "no_update"
AUDIT_OR_GOLD_ONLY_FIELDS = {
    "source_url",
    "pr_title",
    "docs_changed_files",
    "docs_diff_excerpt",
    "docs_after_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "human_label_notes",
    "manual_label_notes",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Expected JSON object at {path}:{line_number}")
            rows.append(row)
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def eligible_final_row(row: dict[str, Any]) -> bool:
    status = str(row.get("review_status") or "").strip().lower()
    if status in {"exclude", "excluded", "invalid"}:
        return False
    if row.get("exclude") is True or row.get("invalid") is True:
        return False
    if row.get("human_review_complete") is False:
        return False
    return "gold_docs_update_required" in row


def serialize_model_row(row: dict[str, Any]) -> str:
    payload = {field: row.get(field) for field in SAFE_MODEL_FIELDS}
    leaked = AUDIT_OR_GOLD_ONLY_FIELDS & set(payload)
    if leaked:
        raise ValueError(f"Audit/gold fields entered model payload: {sorted(leaked)}")
    language = str(payload.get("language") or "unknown").strip().lower() or "unknown"
    files_value = payload.get("code_changed_files") or []
    files = files_value if isinstance(files_value, list) else [files_value]
    code_files = " ".join(str(item).replace("\\", "/") for item in files if str(item).strip())
    return "\n".join(
        [
            f"language: {language}",
            f"code_changed_files: {code_files}",
            "code_diff_excerpt:",
            str(payload.get("code_diff_excerpt") or ""),
            "docs_before_excerpt:",
            str(payload.get("docs_before_excerpt") or ""),
        ]
    )


def assert_safe_rows_only(rows: list[dict[str, Any]]) -> None:
    for index, row in enumerate(rows, start=1):
        text = serialize_model_row(row)
        for forbidden in AUDIT_OR_GOLD_ONLY_FIELDS:
            if forbidden in text:
                raise ValueError(f"Forbidden field name leaked into serialized model row {index}: {forbidden}")


def binary_eligible_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if eligible_final_row(row)]


def binary_labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]


def category_scope_counts(rows: list[dict[str, Any]]) -> dict[str, int | float]:
    positive = [row for row in rows if eligible_final_row(row) and bool_value(row.get("gold_docs_update_required"))]
    primary = [row for row in positive if str(row.get("gold_doc_category") or "") in PRIMARY_STAGE2_LABELS]
    other = [row for row in positive if str(row.get("gold_doc_category") or "") == OTHER_DOCUMENTATION_LABEL]
    return {
        "all_positive_rows": len(positive),
        "primary_stage2_eligible_rows": len(primary),
        "other_documentation_rows": len(other),
        "stage2_coverage_ratio": (len(primary) / len(positive)) if positive else 0.0,
    }


def category_eligible_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if eligible_final_row(row)
        and bool_value(row.get("gold_docs_update_required"))
        and str(row.get("gold_doc_category") or "") in PRIMARY_STAGE2_LABELS
    ]


def category_labels(rows: list[dict[str, Any]]) -> list[str]:
    labels = [str(row.get("gold_doc_category") or "") for row in rows]
    invalid = sorted(set(labels) - set(PRIMARY_STAGE2_LABELS))
    if invalid:
        raise ValueError(f"Category V8 accepts only exact primary labels: {invalid}")
    return labels


def language_bucket(row: dict[str, Any]) -> str:
    language = str(row.get("language") or "other").strip().lower()
    if language in {"python", "typescript"}:
        return language
    return "other"

