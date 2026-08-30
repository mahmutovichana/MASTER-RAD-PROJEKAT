from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SAFE_MODEL_FIELDS = ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"]
PRIMARY_STAGE2_LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
OTHER_DOCUMENTATION_LABEL = "other_documentation"
NO_UPDATE_LABEL = "no_update"
LABEL_SOURCE = "human_reviewed_final_v2"
ALLOWED_PARTITIONS = {"development_train", "development_validation", "confirmation"}
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
    raise ValueError(f"Expected real boolean value, got {value!r}")


def validate_final_gold_row(row: dict[str, Any], *, allowed_partitions: set[str] | None = None) -> None:
    row_id = str(row.get("case_id") or row.get("id") or "<unknown>")
    status = str(row.get("review_status") or "").strip().lower()
    if status != "approved":
        raise ValueError(f"{row_id}: review_status must be approved")
    if row.get("human_review_complete") is not True:
        raise ValueError(f"{row_id}: human_review_complete must be exactly true")
    if row.get("label_source") != LABEL_SOURCE:
        raise ValueError(f"{row_id}: label_source must be {LABEL_SOURCE}")
    if "gold_docs_update_required" not in row or not isinstance(row.get("gold_docs_update_required"), bool):
        raise ValueError(f"{row_id}: gold_docs_update_required must be a real boolean")
    category = str(row.get("gold_doc_category") or "")
    if category not in set(PRIMARY_STAGE2_LABELS) | {OTHER_DOCUMENTATION_LABEL, NO_UPDATE_LABEL}:
        raise ValueError(f"{row_id}: invalid gold_doc_category {category!r}")
    if row["gold_docs_update_required"] is False and category != NO_UPDATE_LABEL:
        raise ValueError(f"{row_id}: negative rows must use no_update")
    if row["gold_docs_update_required"] is True and category == NO_UPDATE_LABEL:
        raise ValueError(f"{row_id}: positive rows require a positive category")
    partition = str(row.get("partition") or "")
    if partition not in ALLOWED_PARTITIONS:
        raise ValueError(f"{row_id}: partition must be one of {sorted(ALLOWED_PARTITIONS)}")
    if allowed_partitions is not None and partition not in allowed_partitions:
        raise ValueError(f"{row_id}: partition {partition} is not allowed here")


def eligible_final_row(row: dict[str, Any], *, allowed_partitions: set[str] | None = None) -> bool:
    validate_final_gold_row(row, allowed_partitions=allowed_partitions)
    return True


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
        # serialize_model_row constructs the payload exclusively from
        # SAFE_MODEL_FIELDS and already rejects forbidden payload keys.
        # Do not scan legitimate code/docs text for strings such as
        # "pr_title": those may naturally occur in a diff and are not
        # evidence that the corresponding audit field entered the model.
        serialized = serialize_model_row(row)
        if not isinstance(serialized, str):
            raise ValueError(f"Serialized model row {index} is not text")


def binary_eligible_rows(rows: list[dict[str, Any]], *, allowed_partitions: set[str] | None = None) -> list[dict[str, Any]]:
    return [row for row in rows if eligible_final_row(row, allowed_partitions=allowed_partitions)]


def binary_labels(rows: list[dict[str, Any]]) -> list[int]:
    return [1 if bool_value(row.get("gold_docs_update_required")) else 0 for row in rows]


def category_scope_counts(rows: list[dict[str, Any]]) -> dict[str, int | float]:
    valid = [row for row in rows if eligible_final_row(row)]
    positive = [row for row in valid if bool_value(row.get("gold_docs_update_required"))]
    primary = [row for row in positive if str(row.get("gold_doc_category") or "") in PRIMARY_STAGE2_LABELS]
    other = [row for row in positive if str(row.get("gold_doc_category") or "") == OTHER_DOCUMENTATION_LABEL]
    return {
        "all_positive_rows": len(positive),
        "primary_stage2_eligible_rows": len(primary),
        "other_documentation_rows": len(other),
        "stage2_coverage_ratio": (len(primary) / len(positive)) if positive else 0.0,
    }


def category_eligible_rows(rows: list[dict[str, Any]], *, allowed_partitions: set[str] | None = None) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if eligible_final_row(row, allowed_partitions=allowed_partitions)
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
