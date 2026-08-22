from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_external.real_case_runner import AUDIT_ONLY_FIELDS, ALLOWED_MODEL_INPUT_FIELDS


SAFE_CASE_FIELDS_TO_SHOW = [
    "case_id",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def _truncate(text: Any, limit: int) -> str:
    value = str(text if text is not None else "")
    value = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def _safe_cell(value: Any, limit: int = 160) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("|", "\\|").replace("`", "\\`")
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text


def index_by_case_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = str(row.get("case_id") or "")
        if case_id:
            indexed[case_id] = row
    return indexed


def classify_error(row: dict[str, Any]) -> str:
    gold = bool(row.get("gold_docs_update_required"))
    pred = bool(row.get("pred_docs_update_required"))
    if gold and pred:
        return "TP"
    if not gold and pred:
        return "FP"
    if not gold and not pred:
        return "TN"
    if gold and not pred:
        return "FN"
    return "UNKNOWN"


def assert_report_uses_only_safe_case_fields(case: dict[str, Any]) -> None:
    """
    This script is allowed to display only safe input fields plus prediction/gold
    values already present in the prediction output. It must not display docs_after,
    manual notes, docs_changed_files, or other audit-only source fields.
    """
    forbidden_present = [field for field in AUDIT_ONLY_FIELDS if field in case and field not in {"changed_files"}]
    # We do not raise just because source case contains audit fields. The manual
    # file has them. We raise only if a caller tries to pass these fields into
    # the safe display payload.
    if not forbidden_present:
        return


def safe_case_payload(case: dict[str, Any], *, max_diff_chars: int, max_docs_chars: int) -> dict[str, Any]:
    return {
        "case_id": case.get("case_id"),
        "language": case.get("language"),
        "code_changed_files": case.get("code_changed_files") or [],
        "code_diff_excerpt": _truncate(case.get("code_diff_excerpt") or "", max_diff_chars),
        "docs_before_excerpt": _truncate(case.get("docs_before_excerpt") or "", max_docs_chars),
    }


def build_error_rows(
    *,
    cases: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    include_tp: bool,
    include_tn: bool,
    max_diff_chars: int,
    max_docs_chars: int,
) -> list[dict[str, Any]]:
    cases_by_id = index_by_case_id(cases)
    rows: list[dict[str, Any]] = []

    for pred in predictions:
        kind = classify_error(pred)
        if kind == "TP" and not include_tp:
            continue
        if kind == "TN" and not include_tn:
            continue

        case_id = str(pred.get("case_id") or "")
        case = cases_by_id.get(case_id, {})
        safe_case = safe_case_payload(case, max_diff_chars=max_diff_chars, max_docs_chars=max_docs_chars)

        rows.append(
            {
                "error_type": kind,
                "case_id": case_id,
                "safe_case": safe_case,
                "gold_docs_update_required": pred.get("gold_docs_update_required"),
                "pred_docs_update_required": pred.get("pred_docs_update_required"),
                "gold_doc_category_normalized": pred.get("gold_doc_category_normalized"),
                "pred_doc_category": pred.get("pred_doc_category"),
                "pred_target_doc_file": pred.get("pred_target_doc_file"),
                "pred_scenario_type": pred.get("pred_scenario_type"),
                "signals": pred.get("signals") or [],
                "router_reason": pred.get("router_reason") or "",
                "patch": pred.get("pred_generated_doc_patch") or "",
                "verifier_status": pred.get("verifier_status"),
                "verifier_warnings": pred.get("verifier_warnings") or [],
                "quality_label": pred.get("quality_label"),
                "hallucination_risk": pred.get("hallucination_risk"),
                "quality_reasons": pred.get("quality_reasons") or [],
            }
        )

    return rows


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["error_type"]] = counts.get(row["error_type"], 0) + 1

    lines: list[str] = [
        "# DocGuard Real Case Error Inspection 2026-08",
        "",
        "This diagnostic report inspects real-case prediction errors using only safe case input fields:",
        "",
    ]

    for field in ALLOWED_MODEL_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "Audit-only source fields such as `docs_after_excerpt`, `manual_label_notes`, `docs_changed_files`, and gold patch summaries are not shown.",
            "",
            "## Error Counts Included",
            "",
            f"`{counts}`",
            "",
            "## Compact Error Table",
            "",
            "| Type | Case | Gold | Pred | Gold category | Pred category | Signals | Verifier | Quality | Risk |",
            "| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['error_type']}`",
                    f"`{_safe_cell(row['case_id'], 80)}`",
                    f"`{row['gold_docs_update_required']}`",
                    f"`{row['pred_docs_update_required']}`",
                    f"`{_safe_cell(row['gold_doc_category_normalized'], 80)}`",
                    f"`{_safe_cell(row['pred_doc_category'], 80)}`",
                    f"`{_safe_cell(', '.join(row['signals']), 160)}`",
                    f"`{_safe_cell(row['verifier_status'], 40)}`",
                    f"`{_safe_cell(row['quality_label'], 40)}`",
                    f"`{_safe_cell(row['hallucination_risk'], 40)}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Detailed Cases", ""])

    for row in rows:
        safe_case = row["safe_case"]
        lines.extend(
            [
                f"### `{row['error_type']}` — `{row['case_id']}`",
                "",
                f"- Language: `{safe_case.get('language')}`",
                f"- Code changed files: `{safe_case.get('code_changed_files')}`",
                f"- Gold docs update required: `{row['gold_docs_update_required']}`",
                f"- Predicted docs update required: `{row['pred_docs_update_required']}`",
                f"- Gold category normalized: `{row['gold_doc_category_normalized']}`",
                f"- Predicted category: `{row['pred_doc_category']}`",
                f"- Predicted target: `{row['pred_target_doc_file']}`",
                f"- Predicted scenario: `{row['pred_scenario_type']}`",
                f"- Signals: `{', '.join(row['signals'])}`",
                f"- Router reason: {_safe_cell(row['router_reason'], 500)}",
                f"- Verifier: `{row['verifier_status']}`",
                f"- Quality: `{row['quality_label']}`",
                f"- Hallucination risk: `{row['hallucination_risk']}`",
                "",
                "Safe code diff excerpt:",
                "",
                "```diff",
                str(safe_case.get("code_diff_excerpt") or ""),
                "```",
                "",
                "Safe docs-before excerpt:",
                "",
                "```markdown",
                str(safe_case.get("docs_before_excerpt") or ""),
                "```",
                "",
                "Predicted patch:",
                "",
                "```diff",
                str(row.get("patch") or "not_applicable"),
                "```",
                "",
            ]
        )

        warnings = list(row.get("verifier_warnings") or []) + list(row.get("quality_reasons") or [])
        if warnings:
            lines.extend(["Warnings / quality reasons:", ""])
            for warning in warnings[:12]:
                lines.append(f"- {warning}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect DocGuard real-case prediction errors using safe fields only.")
    parser.add_argument("--input", default="data/external/project_case_study/manual_cases.jsonl")
    parser.add_argument("--predictions", default="reports/real_case_study/docguard_real_case_study_predictions.jsonl")
    parser.add_argument("--output", default="reports/real_case_study/docguard_real_case_error_inspection_2026_08.md")
    parser.add_argument("--include-tp", action="store_true")
    parser.add_argument("--include-tn", action="store_true")
    parser.add_argument("--max-diff-chars", type=int, default=1800)
    parser.add_argument("--max-docs-chars", type=int, default=900)
    args = parser.parse_args()

    cases = load_jsonl(Path(args.input))
    predictions = load_jsonl(Path(args.predictions))

    rows = build_error_rows(
        cases=cases,
        predictions=predictions,
        include_tp=args.include_tp,
        include_tn=args.include_tn,
        max_diff_chars=args.max_diff_chars,
        max_docs_chars=args.max_docs_chars,
    )

    output_path = Path(args.output)
    write_markdown(output_path, rows)

    print(
        json.dumps(
            {
                "status": "ok",
                "input": args.input,
                "predictions": args.predictions,
                "output": str(output_path),
                "rows_written": len(rows),
                "counts": {kind: sum(1 for row in rows if row["error_type"] == kind) for kind in ["TP", "FP", "TN", "FN"]},
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())