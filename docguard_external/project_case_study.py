from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "case_id",
    "source_project",
    "source_url",
    "commit_or_pr",
    "language",
    "change_type",
    "code_changed_files",
    "docs_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "manual_label_notes",
    "label_confidence",
    "allowed_model_input_fields",
    "audit_only_fields",
}
OPTIONAL_FIELDS = {"changed_files", "docs_after_excerpt", "gold_target_section", "gold_patch_summary"}
CHANGE_TYPES = {
    "api_endpoint_change",
    "validation_change",
    "request_response_schema_change",
    "configuration_change",
    "testing_command_change",
    "workflow_change",
    "documentation_already_updated",
    "internal_refactor_no_docs_needed",
}
DOC_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "testing",
    "workflow",
    "architecture",
    "data_model",
    "changelog",
    "none",
    "uncertain",
}
LABEL_CONFIDENCE = {"high", "medium", "low"}
MODEL_INPUT_FIELDS = {"code_changed_files", "code_diff_excerpt", "docs_before_excerpt", "language"}
AUDIT_ONLY_FIELDS = {
    "change_type",
    "changed_files",
    "docs_changed_files",
    "docs_after_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "manual_label_notes",
    "label_confidence",
}
DOCS_BEFORE_LEAKAGE_PHRASES = [
    "no markdown/rst/openapi documentation file was present",
    "no documentation files were present",
    "no documentation file was present",
    "no docs changed",
]


def is_documentation_file(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    name = normalized.rsplit("/", 1)[-1]
    return (
        name in {"readme.md", "readme.rst", "changelog.md", "changes.md"}
        or normalized.endswith((".md", ".rst"))
        or normalized.startswith("docs/")
        or "/docs/" in normalized
        or "openapi" in normalized
        or "swagger" in normalized
        or "api_contract" in normalized
        or "architecture" in normalized
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            rows.append({"__line__": line_number, "__json_error__": str(exc)})
            continue
        if isinstance(row, dict):
            row["__line__"] = line_number
            rows.append(row)
        else:
            rows.append({"__line__": line_number, "__json_error__": "record must be a JSON object"})
    return rows


def validate_record(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "__json_error__" in row:
        return [row["__json_error__"]]
    missing = sorted(REQUIRED_FIELDS - set(row))
    if missing:
        errors.append(f"missing required fields: {missing}")
    unknown = sorted(set(row) - REQUIRED_FIELDS - OPTIONAL_FIELDS - {"__line__"})
    if unknown:
        errors.append(f"unknown fields: {unknown}")
    if row.get("change_type") not in CHANGE_TYPES:
        errors.append(f"invalid change_type: {row.get('change_type')!r}")
    if row.get("gold_doc_category") not in DOC_CATEGORIES:
        errors.append(f"invalid gold_doc_category: {row.get('gold_doc_category')!r}")
    if row.get("label_confidence") not in LABEL_CONFIDENCE:
        errors.append(f"invalid label_confidence: {row.get('label_confidence')!r}")
    if not isinstance(row.get("gold_docs_update_required"), bool):
        errors.append("gold_docs_update_required must be boolean")
    if not isinstance(row.get("code_changed_files"), list) or not all(isinstance(item, str) and item for item in row.get("code_changed_files", [])):
        errors.append("code_changed_files must be a non-empty list of strings")
    if not isinstance(row.get("docs_changed_files"), list) or not all(isinstance(item, str) and item for item in row.get("docs_changed_files", [])):
        errors.append("docs_changed_files must be a list of strings")
    if "changed_files" in row and (
        not isinstance(row.get("changed_files"), list) or not all(isinstance(item, str) and item for item in row.get("changed_files", []))
    ):
        errors.append("changed_files must be a list of strings when present")
    misplaced_docs = [path for path in row.get("code_changed_files", []) if is_documentation_file(path)]
    if misplaced_docs:
        errors.append(f"code_changed_files contains documentation-looking files: {misplaced_docs}")
    misplaced_code = [path for path in row.get("docs_changed_files", []) if not is_documentation_file(path)]
    if misplaced_code:
        errors.append(f"docs_changed_files contains non-documentation-looking files: {misplaced_code}")
    if not isinstance(row.get("allowed_model_input_fields"), list):
        errors.append("allowed_model_input_fields must be a list")
    if not isinstance(row.get("audit_only_fields"), list):
        errors.append("audit_only_fields must be a list")
    allowed_inputs = set(row.get("allowed_model_input_fields") or [])
    audit_only = set(row.get("audit_only_fields") or [])
    invalid_inputs = sorted(allowed_inputs - MODEL_INPUT_FIELDS)
    if invalid_inputs:
        errors.append(f"allowed_model_input_fields contains unsupported fields: {invalid_inputs}")
    leakage_inputs = sorted(allowed_inputs & (AUDIT_ONLY_FIELDS | audit_only))
    if leakage_inputs:
        errors.append(f"allowed_model_input_fields contains audit-only/leakage fields: {leakage_inputs}")
    required_audit_fields = {"changed_files", "docs_changed_files", "change_type"} if "changed_files" in row else {"docs_changed_files", "change_type"}
    missing_audit_fields = sorted(required_audit_fields - audit_only)
    if missing_audit_fields:
        errors.append(f"audit_only_fields missing required audit-only fields: {missing_audit_fields}")
    if "change_type" not in audit_only:
        errors.append("change_type is manually assigned and must be listed in audit_only_fields")
    for blocked in ["changed_files", "docs_changed_files", "change_type", "docs_after_excerpt"]:
        if blocked in allowed_inputs:
            errors.append(f"{blocked} must not be allowed as model input")
    gold_inputs = sorted(field for field in allowed_inputs if field.startswith("gold_"))
    if gold_inputs:
        errors.append(f"gold fields must not be allowed as model input: {gold_inputs}")
    docs_before = str(row.get("docs_before_excerpt") or "").lower()
    if any(phrase in docs_before for phrase in DOCS_BEFORE_LEAKAGE_PHRASES):
        errors.append("docs_before_excerpt contains audit/leakage text about missing documentation files")
    if row.get("docs_after_excerpt"):
        if "docs_after_excerpt" not in audit_only:
            errors.append("docs_after_excerpt is present but not listed in audit_only_fields")
        if "docs_after_excerpt" in allowed_inputs:
            errors.append("docs_after_excerpt must not be allowed as model input")
    for field in ["case_id", "source_project", "source_url", "commit_or_pr", "language", "code_diff_excerpt", "manual_label_notes"]:
        if field in row and not str(row.get(field) or "").strip():
            errors.append(f"{field} must not be empty")
    if row.get("gold_docs_update_required") is False:
        if row.get("gold_doc_category") not in {"none", "uncertain"}:
            errors.append("negative cases should use gold_doc_category none or uncertain")
        if row.get("gold_target_doc_file") not in {None, "", "none", "uncertain"}:
            errors.append("negative cases should not provide a concrete gold_target_doc_file")
    if row.get("gold_docs_update_required") is True:
        if row.get("gold_doc_category") in {"none", None, ""}:
            errors.append("positive cases need a concrete gold_doc_category")
        if not str(row.get("gold_target_doc_file") or "").strip() or row.get("gold_target_doc_file") == "none":
            errors.append("positive cases need a concrete gold_target_doc_file or uncertain")
    return errors


def validate_project_cases(path: Path, report_path: Path | None = None) -> dict[str, Any]:
    if not path.exists():
        result = {"status": "error", "message": f"input not found: {path}", "records_checked": 0, "errors": []}
        if report_path:
            write_validation_report(report_path, result)
        return result
    rows = read_jsonl(path)
    errors = []
    case_ids = []
    for row in rows:
        row_errors = validate_record(row)
        case_id = row.get("case_id")
        if case_id:
            case_ids.append(case_id)
        if row_errors:
            errors.append({"line": row.get("__line__"), "case_id": case_id, "errors": row_errors})
    duplicates = sorted([case_id for case_id, count in Counter(case_ids).items() if count > 1])
    if duplicates:
        errors.append({"line": None, "case_id": None, "errors": [f"duplicate case_id values: {duplicates}"]})
    result = {
        "status": "ok" if not errors else "error",
        "input": str(path),
        "records_checked": len(rows),
        "errors": errors[:50],
        "change_type_distribution": dict(Counter(row.get("change_type") for row in rows if "__json_error__" not in row)),
        "label_distribution": dict(Counter(str(row.get("gold_docs_update_required")) for row in rows if "__json_error__" not in row)),
        "allowed_model_input_fields": sorted(MODEL_INPUT_FIELDS),
        "audit_only_fields": sorted(AUDIT_ONLY_FIELDS),
        "documentation_file_policy": "docs_changed_files and changed_files are audit-only; code_changed_files is the only file-list input allowed for future runners.",
    }
    if report_path:
        write_validation_report(report_path, result)
    return result


def write_validation_report(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DocGuard Project Case Study Template Validation 2026-08",
        "",
        f"- Input: `{result.get('input')}`",
        f"- Status: `{result.get('status')}`",
        f"- Records checked: `{result.get('records_checked')}`",
        f"- Change type distribution: `{result.get('change_type_distribution')}`",
        f"- Label distribution: `{result.get('label_distribution')}`",
        "",
        "## Leakage Policy",
        "",
        f"- Allowed model input fields: `{result.get('allowed_model_input_fields')}`",
        f"- Audit-only fields: `{result.get('audit_only_fields')}`",
        f"- Documentation file policy: {result.get('documentation_file_policy')}",
        "",
        "## Errors",
        "",
    ]
    if result.get("errors"):
        for error in result["errors"]:
            lines.append(f"- Line `{error.get('line')}`, case `{error.get('case_id')}`: {error.get('errors')}")
    else:
        lines.append("No validation errors found.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
