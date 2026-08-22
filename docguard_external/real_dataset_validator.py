from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_MODEL_INPUT_FIELDS = {
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
}

AUDIT_ONLY_FIELDS = {
    "source_url",
    "repository",
    "pr_number",
    "pr_title",
    "pr_state",
    "merged_at",
    "base_sha",
    "head_sha",
    "changed_files",
    "docs_changed_files",
    "docs_diff_excerpt",
    "docs_after_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "label_confidence",
    "manual_label_notes",
    "candidate_evidence",
    "audit_labeling_context",
    "gold_label_to_fill",
    "labeling_guidance",
    "allowed_model_input_fields",
    "audit_only_fields",
}

VALID_LABEL_CONFIDENCE = {
    "needs_manual_review",
    "high",
    "medium",
    "low",
    "ambiguous",
    "exclude",
    "",
    None,
}

VALID_DOC_CATEGORIES = {
    "api_reference",
    "model_contract",
    "configuration",
    "testing_instructions",
    "workflow_documentation",
    "architecture_flow",
    "developer_setup",
    "changelog",
    "no_update",
    "ambiguous",
    "",
    None,
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


def _safe_bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
        if lowered in {"", "none", "null"}:
            return None
    return None


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None:
        return []
    return [str(value)]


def get_case_id(row: dict[str, Any], index: int) -> str:
    return str(row.get("case_id") or f"row-{index}")


def get_model_input(row: dict[str, Any]) -> dict[str, Any]:
    """
    Supports two structures:

    1. Candidate/manual-case style:
       {
         "language": ...,
         "code_changed_files": ...,
         "code_diff_excerpt": ...,
         "docs_before_excerpt": ...
       }

    2. Labeling-pack style:
       {
         "model_input": {
            "language": ...,
            ...
         }
       }
    """
    nested = row.get("model_input")
    if isinstance(nested, dict):
        return dict(nested)

    return {
        "language": row.get("language"),
        "code_changed_files": row.get("code_changed_files") or [],
        "code_diff_excerpt": row.get("code_diff_excerpt") or "",
        "docs_before_excerpt": row.get("docs_before_excerpt") or "",
    }


def get_gold_label(row: dict[str, Any]) -> dict[str, Any]:
    nested = row.get("gold_label_to_fill")
    if isinstance(nested, dict):
        return dict(nested)

    return {
        "gold_docs_update_required": row.get("gold_docs_update_required"),
        "gold_doc_category": row.get("gold_doc_category"),
        "gold_target_doc_file": row.get("gold_target_doc_file"),
        "gold_target_section": row.get("gold_target_section"),
        "gold_patch_summary": row.get("gold_patch_summary"),
        "label_confidence": row.get("label_confidence"),
        "manual_label_notes": row.get("manual_label_notes"),
    }


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_model_input_shape(case_id: str, model_input: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    extra_keys = set(model_input) - ALLOWED_MODEL_INPUT_FIELDS
    missing_keys = ALLOWED_MODEL_INPUT_FIELDS - set(model_input)

    if extra_keys:
        errors.append(f"{case_id}: model_input contains forbidden keys: {sorted(extra_keys)}")

    if missing_keys:
        errors.append(f"{case_id}: model_input missing required keys: {sorted(missing_keys)}")

    for audit_key in AUDIT_ONLY_FIELDS:
        if audit_key in model_input:
            errors.append(f"{case_id}: audit-only key leaked into model_input: {audit_key}")

    if not _nonempty_string(model_input.get("language")):
        errors.append(f"{case_id}: model_input.language is empty")

    if not _as_list(model_input.get("code_changed_files")):
        errors.append(f"{case_id}: model_input.code_changed_files is empty")

    if not _nonempty_string(model_input.get("code_diff_excerpt")):
        errors.append(f"{case_id}: model_input.code_diff_excerpt is empty")

    return errors


def validate_no_high_risk_value_leakage(case_id: str, row: dict[str, Any], model_input: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    model_blob = json.dumps(model_input, ensure_ascii=False, sort_keys=True)

    high_risk_values: list[tuple[str, Any]] = []

    for key in ["docs_after_excerpt", "gold_patch_summary", "manual_label_notes"]:
        high_risk_values.append((key, row.get(key)))

    audit_context = row.get("audit_labeling_context")
    if isinstance(audit_context, dict):
        high_risk_values.append(("audit_labeling_context.docs_after_excerpt", audit_context.get("docs_after_excerpt")))

    gold = row.get("gold_label_to_fill")
    if isinstance(gold, dict):
        high_risk_values.append(("gold_label_to_fill.gold_patch_summary", gold.get("gold_patch_summary")))
        high_risk_values.append(("gold_label_to_fill.manual_label_notes", gold.get("manual_label_notes")))

    for key, value in high_risk_values:
        if value is None:
            continue
        text = str(value).strip()
        if len(text) >= 20 and text in model_blob:
            errors.append(f"{case_id}: high-risk audit value leaked into model_input from {key}")

    return errors


def validate_gold_label(case_id: str, row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    gold = get_gold_label(row)

    label_confidence = gold.get("label_confidence")
    doc_category = gold.get("gold_doc_category")
    required = _safe_bool_or_none(gold.get("gold_docs_update_required"))

    if label_confidence not in VALID_LABEL_CONFIDENCE:
        errors.append(f"{case_id}: invalid label_confidence: {label_confidence}")

    if doc_category not in VALID_DOC_CATEGORIES:
        errors.append(f"{case_id}: invalid gold_doc_category: {doc_category}")

    if label_confidence in {"high", "medium"}:
        if required is None:
            errors.append(f"{case_id}: high/medium confidence label must set gold_docs_update_required")
        if required is True and doc_category in {None, "", "no_update", "ambiguous"}:
            errors.append(f"{case_id}: positive high/medium label must set a concrete gold_doc_category")
        if required is False and doc_category not in {"no_update", None, ""}:
            errors.append(f"{case_id}: negative high/medium label should use no_update or empty category")

    return errors


def validate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_case_ids: set[str] = set()

    language_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    repository_counts: Counter[str] = Counter()

    for index, row in enumerate(rows, start=1):
        case_id = get_case_id(row, index)

        if case_id in seen_case_ids:
            errors.append(f"{case_id}: duplicate case_id")
        seen_case_ids.add(case_id)

        model_input = get_model_input(row)
        gold = get_gold_label(row)

        errors.extend(validate_model_input_shape(case_id, model_input))
        errors.extend(validate_no_high_risk_value_leakage(case_id, row, model_input))
        errors.extend(validate_gold_label(case_id, row))

        language_counts[str(model_input.get("language") or "unknown")] += 1
        confidence_counts[str(gold.get("label_confidence"))] += 1
        category_counts[str(gold.get("gold_doc_category"))] += 1
        label_counts[str(_safe_bool_or_none(gold.get("gold_docs_update_required")))] += 1

        repository = row.get("repository")
        if not repository:
            audit_context = row.get("audit_labeling_context")
            if isinstance(audit_context, dict):
                repository = audit_context.get("repository")
        repository_counts[str(repository or "unknown")] += 1

        if not _nonempty_string(str(model_input.get("docs_before_excerpt") or "")):
            warnings.append(f"{case_id}: docs_before_excerpt is empty")

    return {
        "status": "ok" if not errors else "failed",
        "records": len(rows),
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "language_counts": dict(language_counts),
        "label_confidence_counts": dict(confidence_counts),
        "gold_label_counts": dict(label_counts),
        "gold_category_counts": dict(category_counts),
        "repository_counts": dict(repository_counts),
        "unique_case_ids": len(seen_case_ids),
        "allowed_model_input_fields": sorted(ALLOWED_MODEL_INPUT_FIELDS),
        "audit_only_fields": sorted(AUDIT_ONLY_FIELDS),
    }


def write_markdown_report(path: Path, validation: dict[str, Any], input_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# DocGuard Real Dataset Validation Report",
        "",
        f"- Input: `{input_path}`",
        f"- Status: `{validation['status']}`",
        f"- Records: `{validation['records']}`",
        f"- Error count: `{validation['error_count']}`",
        f"- Warning count: `{validation['warning_count']}`",
        "",
        "## Leakage Boundary",
        "",
        "Allowed model input fields:",
        "",
    ]

    for field in validation["allowed_model_input_fields"]:
        lines.append(f"- `{field}`")

    lines.extend(["", "Audit-only fields:", ""])

    for field in validation["audit_only_fields"]:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Distribution Summary",
            "",
            f"- Language counts: `{validation['language_counts']}`",
            f"- Label confidence counts: `{validation['label_confidence_counts']}`",
            f"- Gold label counts: `{validation['gold_label_counts']}`",
            f"- Gold category counts: `{validation['gold_category_counts']}`",
            f"- Repository counts: `{validation['repository_counts']}`",
            "",
            "## Errors",
            "",
        ]
    )

    if validation["errors"]:
        for error in validation["errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings", ""])

    if validation["warnings"]:
        for warning in validation["warnings"][:500]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- This validator does not assign labels.",
            "- It checks dataset structure, leakage safety, basic label consistency, and reporting readiness.",
            "- `docs_after_excerpt`, gold fields, source URL, docs-changed files, and manual notes must remain outside model input.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DocGuard real PR candidate/labeling datasets.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    rows = load_jsonl(input_path)
    validation = validate_rows(rows)

    write_json(Path(args.output_json), validation)
    write_markdown_report(Path(args.report), validation, input_path)

    print(json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True))

    return 0 if validation["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())