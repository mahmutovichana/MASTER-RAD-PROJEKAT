from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_INCLUDED_CONFIDENCES = {"high", "medium"}

ALLOWED_MODEL_INPUT_FIELDS = {
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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def _safe_bool_or_none(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    if lowered in {"", "none", "null"}:
        return None
    raise ValueError(f"Invalid boolean value: {value}")


def _safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value is None:
        return []
    return [str(value)]


def get_model_input(row: dict[str, Any]) -> dict[str, Any]:
    nested = row.get("model_input")
    if isinstance(nested, dict):
        return dict(nested)

    return {
        "language": row.get("language"),
        "code_changed_files": row.get("code_changed_files") or [],
        "code_diff_excerpt": row.get("code_diff_excerpt") or "",
        "docs_before_excerpt": row.get("docs_before_excerpt") or "",
    }


def get_gold(row: dict[str, Any]) -> dict[str, Any]:
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


def get_audit_context(row: dict[str, Any]) -> dict[str, Any]:
    nested = row.get("audit_labeling_context")
    if isinstance(nested, dict):
        return dict(nested)

    return {
        "source_url": row.get("source_url"),
        "repository": row.get("repository"),
        "pr_number": row.get("pr_number"),
        "pr_title": row.get("pr_title"),
        "candidate_evidence": row.get("candidate_evidence") or {},
    }


def get_candidate_type(row: dict[str, Any]) -> str:
    audit = get_audit_context(row)
    evidence = audit.get("candidate_evidence")
    if isinstance(evidence, dict) and evidence.get("candidate_type"):
        return str(evidence["candidate_type"])
    return "unknown"


def flatten_gold_record(
    row: dict[str, Any],
    *,
    label_source: str,
) -> dict[str, Any]:
    model_input = get_model_input(row)
    gold = get_gold(row)
    audit = get_audit_context(row)

    required = _safe_bool_or_none(gold.get("gold_docs_update_required"))
    if required is None:
        raise ValueError(f"{row.get('case_id')}: gold_docs_update_required is not set")

    flat = {
        "case_id": str(row.get("case_id") or ""),
        "language": str(model_input.get("language") or "unknown"),
        "code_changed_files": _safe_list(model_input.get("code_changed_files")),
        "code_diff_excerpt": str(model_input.get("code_diff_excerpt") or ""),
        "docs_before_excerpt": str(model_input.get("docs_before_excerpt") or ""),
        "gold_docs_update_required": required,
        "gold_doc_category": gold.get("gold_doc_category"),
        "gold_target_doc_file": gold.get("gold_target_doc_file"),
        "gold_target_section": gold.get("gold_target_section"),
        "label_confidence": gold.get("label_confidence"),
        "label_source": label_source,
        "repository": audit.get("repository"),
        "pr_number": audit.get("pr_number"),
        "pr_title": audit.get("pr_title"),
        "source_url": audit.get("source_url"),
        "candidate_type": get_candidate_type(row),
    }

    leaked = sorted(key for key in flat if key not in {
        "case_id",
        "language",
        "code_changed_files",
        "code_diff_excerpt",
        "docs_before_excerpt",
        "gold_docs_update_required",
        "gold_doc_category",
        "gold_target_doc_file",
        "gold_target_section",
        "label_confidence",
        "label_source",
        "repository",
        "pr_number",
        "pr_title",
        "source_url",
        "candidate_type",
    })
    if leaked:
        raise AssertionError(f"Unexpected fields in flat gold record: {leaked}")

    return flat


def build_gold_dataset(
    rows: list[dict[str, Any]],
    *,
    included_confidences: set[str],
    label_source: str,
    exclude_empty_docs_before: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for row in rows:
        case_id = str(row.get("case_id") or "")
        model_input = get_model_input(row)
        gold = get_gold(row)
        confidence = str(gold.get("label_confidence") or "").strip()

        if confidence not in included_confidences:
            excluded.append(
                {
                    "case_id": case_id,
                    "reason": "confidence_not_included",
                    "label_confidence": confidence,
                }
            )
            continue

        try:
            required = _safe_bool_or_none(gold.get("gold_docs_update_required"))
        except ValueError as exc:
            excluded.append(
                {
                    "case_id": case_id,
                    "reason": "invalid_gold_boolean",
                    "error": str(exc),
                    "label_confidence": confidence,
                }
            )
            continue

        if required is None:
            excluded.append(
                {
                    "case_id": case_id,
                    "reason": "missing_gold_boolean",
                    "label_confidence": confidence,
                }
            )
            continue

        if exclude_empty_docs_before and not str(model_input.get("docs_before_excerpt") or "").strip():
            excluded.append(
                {
                    "case_id": case_id,
                    "reason": "empty_docs_before_excluded",
                    "label_confidence": confidence,
                }
            )
            continue

        included.append(flatten_gold_record(row, label_source=label_source))

    return included, excluded


def summarize(rows: list[dict[str, Any]], excluded: list[dict[str, Any]], *, input_path: Path, output_path: Path) -> dict[str, Any]:
    return {
        "status": "ok",
        "input": str(input_path),
        "output": str(output_path),
        "records_included": len(rows),
        "records_excluded": len(excluded),
        "gold_docs_update_required_counts": dict(Counter(str(row.get("gold_docs_update_required")) for row in rows)),
        "label_confidence_counts": dict(Counter(str(row.get("label_confidence")) for row in rows)),
        "gold_doc_category_counts": dict(Counter(str(row.get("gold_doc_category")) for row in rows)),
        "language_counts": dict(Counter(str(row.get("language")) for row in rows)),
        "repository_counts": dict(Counter(str(row.get("repository")) for row in rows)),
        "candidate_type_counts": dict(Counter(str(row.get("candidate_type")) for row in rows)),
        "excluded_reason_counts": dict(Counter(str(row.get("reason")) for row in excluded)),
        "model_input_fields": sorted(ALLOWED_MODEL_INPUT_FIELDS),
        "labeling_boundary": "Gold/audit fields are retained for evaluation metadata but only language, code_changed_files, code_diff_excerpt, and docs_before_excerpt are model-facing fields.",
    }


def write_markdown_report(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# DocGuard Real Gold Dataset Builder Report",
        "",
        f"- Input: `{summary['input']}`",
        f"- Output: `{summary['output']}`",
        f"- Records included: `{summary['records_included']}`",
        f"- Records excluded: `{summary['records_excluded']}`",
        "",
        "## Included Distribution",
        "",
        f"- Gold labels: `{summary['gold_docs_update_required_counts']}`",
        f"- Confidence: `{summary['label_confidence_counts']}`",
        f"- Categories: `{summary['gold_doc_category_counts']}`",
        f"- Languages: `{summary['language_counts']}`",
        f"- Candidate types: `{summary['candidate_type_counts']}`",
        f"- Repositories: `{summary['repository_counts']}`",
        "",
        "## Excluded Distribution",
        "",
        f"- Reasons: `{summary['excluded_reason_counts']}`",
        "",
        "## Boundary",
        "",
        "- This script does not call a model.",
        "- It does not use docs-after text as model input.",
        "- It flattens high-confidence/medium-confidence labeled records into the shape expected by the LLM judge and classifier experiments.",
        "- AI-assisted labels should be described as draft/silver labels unless manually reviewed.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a flat DocGuard real gold/silver dataset from labeled PR labeling packs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--excluded-output", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--included-confidences", default="high,medium")
    parser.add_argument("--label-source", default="ai_assisted_draft")
    parser.add_argument("--exclude-empty-docs-before", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    included_confidences = {
        item.strip()
        for item in args.included_confidences.split(",")
        if item.strip()
    }

    source_rows = load_jsonl(input_path)
    rows, excluded = build_gold_dataset(
        source_rows,
        included_confidences=included_confidences,
        label_source=args.label_source,
        exclude_empty_docs_before=args.exclude_empty_docs_before,
    )

    write_jsonl(output_path, rows)
    write_jsonl(Path(args.excluded_output), excluded)

    summary = summarize(rows, excluded, input_path=input_path, output_path=output_path)
    write_json(Path(args.summary_json), summary)
    write_markdown_report(Path(args.report), summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())