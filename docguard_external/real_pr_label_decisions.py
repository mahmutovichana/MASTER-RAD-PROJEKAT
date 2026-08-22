from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


LABEL_COLUMNS = [
    "case_id",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "label_confidence",
    "manual_label_notes",
]

CONTEXT_COLUMNS = [
    "source_url",
    "repository",
    "pr_number",
    "pr_title",
    "language",
    "candidate_type",
    "code_file_count",
    "docs_file_count",
    "has_docs_before_excerpt",
    "has_docs_after_excerpt",
]

DOC_CATEGORY_OPTIONS = {
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
}

LABEL_CONFIDENCE_OPTIONS = {
    "high",
    "medium",
    "low",
    "ambiguous",
    "exclude",
    "needs_manual_review",
    "",
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


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _safe_bool_or_blank(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return "true"
    if lowered in {"false", "0", "no", "n"}:
        return "false"
    return ""


def _parse_bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    if lowered in {"", "none", "null", "needs_manual_review"}:
        return None
    raise ValueError(f"Invalid boolean label value: {value}")


def _truncate(value: Any, limit: int) -> str:
    text = _safe_str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def get_model_input(row: dict[str, Any]) -> dict[str, Any]:
    value = row.get("model_input")
    if isinstance(value, dict):
        return value
    return {
        "language": row.get("language"),
        "code_changed_files": row.get("code_changed_files") or [],
        "code_diff_excerpt": row.get("code_diff_excerpt") or "",
        "docs_before_excerpt": row.get("docs_before_excerpt") or "",
    }


def get_audit_context(row: dict[str, Any]) -> dict[str, Any]:
    value = row.get("audit_labeling_context")
    if isinstance(value, dict):
        return value
    return {
        "source_url": row.get("source_url"),
        "repository": row.get("repository"),
        "pr_number": row.get("pr_number"),
        "pr_title": row.get("pr_title"),
        "docs_changed_files": row.get("docs_changed_files") or [],
        "docs_diff_excerpt": row.get("docs_diff_excerpt") or "",
        "docs_after_excerpt": row.get("docs_after_excerpt") or "",
        "candidate_evidence": row.get("candidate_evidence") or {},
    }


def get_gold(row: dict[str, Any]) -> dict[str, Any]:
    value = row.get("gold_label_to_fill")
    if isinstance(value, dict):
        return value
    return {
        "gold_docs_update_required": row.get("gold_docs_update_required"),
        "gold_doc_category": row.get("gold_doc_category"),
        "gold_target_doc_file": row.get("gold_target_doc_file"),
        "gold_target_section": row.get("gold_target_section"),
        "gold_patch_summary": row.get("gold_patch_summary"),
        "label_confidence": row.get("label_confidence") or "needs_manual_review",
        "manual_label_notes": row.get("manual_label_notes") or "",
    }


def build_decision_row(row: dict[str, Any]) -> dict[str, str]:
    model_input = get_model_input(row)
    context = get_audit_context(row)
    gold = get_gold(row)
    evidence = context.get("candidate_evidence") or {}

    return {
        "case_id": _safe_str(row.get("case_id")),
        "source_url": _safe_str(context.get("source_url")),
        "repository": _safe_str(context.get("repository")),
        "pr_number": _safe_str(context.get("pr_number")),
        "pr_title": _truncate(context.get("pr_title"), 220),
        "language": _safe_str(model_input.get("language")),
        "candidate_type": _safe_str(evidence.get("candidate_type")),
        "code_file_count": _safe_str(len(model_input.get("code_changed_files") or [])),
        "docs_file_count": _safe_str(len(context.get("docs_changed_files") or [])),
        "has_docs_before_excerpt": "true" if _safe_str(model_input.get("docs_before_excerpt")).strip() else "false",
        "has_docs_after_excerpt": "true" if _safe_str(context.get("docs_after_excerpt")).strip() else "false",
        "gold_docs_update_required": _safe_bool_or_blank(gold.get("gold_docs_update_required")),
        "gold_doc_category": _safe_str(gold.get("gold_doc_category")),
        "gold_target_doc_file": _safe_str(gold.get("gold_target_doc_file")),
        "gold_target_section": _safe_str(gold.get("gold_target_section")),
        "gold_patch_summary": _safe_str(gold.get("gold_patch_summary")),
        "label_confidence": _safe_str(gold.get("label_confidence") or "needs_manual_review"),
        "manual_label_notes": _safe_str(gold.get("manual_label_notes")),
    }


def export_decision_csv(
    *,
    input_jsonl: Path,
    output_csv: Path,
    limit: int | None = None,
) -> dict[str, Any]:
    rows = load_jsonl(input_jsonl)
    if limit is not None:
        rows = rows[:limit]

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = CONTEXT_COLUMNS + LABEL_COLUMNS[1:]

    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id"] + [field for field in fieldnames if field != "case_id"])
        writer.writeheader()
        for row in rows:
            writer.writerow(build_decision_row(row))

    return {
        "status": "ok",
        "mode": "export",
        "input_jsonl": str(input_jsonl),
        "output_csv": str(output_csv),
        "records": len(rows),
        "note": "Fill only the gold_* / label_confidence / manual_label_notes columns. Context columns are audit-only and must not become model input.",
    }


def load_decisions_csv(path: Path) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            case_id = _safe_str(row.get("case_id")).strip()
            if not case_id:
                continue
            if case_id in decisions:
                raise ValueError(f"Duplicate case_id in decision CSV at line {line_number}: {case_id}")

            confidence = _safe_str(row.get("label_confidence")).strip()
            category = _safe_str(row.get("gold_doc_category")).strip()

            if confidence not in LABEL_CONFIDENCE_OPTIONS:
                raise ValueError(f"{case_id}: invalid label_confidence: {confidence}")

            if category not in DOC_CATEGORY_OPTIONS:
                raise ValueError(f"{case_id}: invalid gold_doc_category: {category}")

            decisions[case_id] = {
                "gold_docs_update_required": _parse_bool_or_none(row.get("gold_docs_update_required")),
                "gold_doc_category": category or None,
                "gold_target_doc_file": _safe_str(row.get("gold_target_doc_file")).strip() or None,
                "gold_target_section": _safe_str(row.get("gold_target_section")).strip() or None,
                "gold_patch_summary": _safe_str(row.get("gold_patch_summary")).strip() or None,
                "label_confidence": confidence or "needs_manual_review",
                "manual_label_notes": _safe_str(row.get("manual_label_notes")).strip(),
            }

    return decisions


def apply_decisions(
    *,
    input_jsonl: Path,
    decisions_csv: Path,
    output_jsonl: Path,
    only_labeled: bool = False,
) -> dict[str, Any]:
    rows = load_jsonl(input_jsonl)
    decisions = load_decisions_csv(decisions_csv)

    updated_rows: list[dict[str, Any]] = []
    missing_decisions: list[str] = []

    for row in rows:
        case_id = _safe_str(row.get("case_id"))
        decision = decisions.get(case_id)

        if decision is None:
            missing_decisions.append(case_id)
            if not only_labeled:
                updated_rows.append(row)
            continue

        label_confidence = decision.get("label_confidence")
        has_label = label_confidence in {"high", "medium", "low", "ambiguous", "exclude"}

        if only_labeled and not has_label:
            continue

        copied = dict(row)
        copied["labeling_status"] = "labeled" if has_label else "needs_manual_review"
        copied["gold_label_to_fill"] = decision

        updated_rows.append(copied)

    write_jsonl(output_jsonl, updated_rows)

    confidence_counts = Counter(
        str(get_gold(row).get("label_confidence"))
        for row in updated_rows
    )
    label_counts = Counter(
        str(get_gold(row).get("gold_docs_update_required"))
        for row in updated_rows
    )
    category_counts = Counter(
        str(get_gold(row).get("gold_doc_category"))
        for row in updated_rows
    )

    return {
        "status": "ok",
        "mode": "apply",
        "input_jsonl": str(input_jsonl),
        "decisions_csv": str(decisions_csv),
        "output_jsonl": str(output_jsonl),
        "input_records": len(rows),
        "decision_rows": len(decisions),
        "output_records": len(updated_rows),
        "missing_decisions": len(missing_decisions),
        "only_labeled": only_labeled,
        "label_confidence_counts": dict(confidence_counts),
        "gold_docs_update_required_counts": dict(label_counts),
        "gold_doc_category_counts": dict(category_counts),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export/apply compact manual label decisions for DocGuard real PR labeling packs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Export compact CSV decision sheet from labeling JSONL.")
    export_parser.add_argument("--input-jsonl", required=True)
    export_parser.add_argument("--output-csv", required=True)
    export_parser.add_argument("--limit", type=int, default=None)

    apply_parser = subparsers.add_parser("apply", help="Apply completed CSV label decisions back to labeling JSONL.")
    apply_parser.add_argument("--input-jsonl", required=True)
    apply_parser.add_argument("--decisions-csv", required=True)
    apply_parser.add_argument("--output-jsonl", required=True)
    apply_parser.add_argument("--only-labeled", action="store_true")

    args = parser.parse_args()

    if args.command == "export":
        result = export_decision_csv(
            input_jsonl=Path(args.input_jsonl),
            output_csv=Path(args.output_csv),
            limit=args.limit,
        )
    elif args.command == "apply":
        result = apply_decisions(
            input_jsonl=Path(args.input_jsonl),
            decisions_csv=Path(args.decisions_csv),
            output_jsonl=Path(args.output_jsonl),
            only_labeled=args.only_labeled,
        )
    else:
        raise ValueError(f"Unsupported command: {args.command}")

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())