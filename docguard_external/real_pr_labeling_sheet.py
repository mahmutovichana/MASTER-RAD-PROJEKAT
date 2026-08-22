from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_MODEL_INPUT_FIELDS = [
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]

AUDIT_LABELING_CONTEXT_FIELDS = [
    "source_url",
    "repository",
    "pr_number",
    "pr_title",
    "docs_changed_files",
    "docs_diff_excerpt",
    "docs_after_excerpt",
    "candidate_evidence",
]

GOLD_LABEL_FIELDS = [
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "label_confidence",
    "manual_label_notes",
]

DOC_CATEGORY_OPTIONS = [
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
]

LABEL_CONFIDENCE_OPTIONS = [
    "high",
    "medium",
    "low",
    "ambiguous",
    "exclude",
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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _safe_cell(value: Any, limit: int = 160) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\n", " ").replace("|", "\\|").replace("`", "\\`")
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3].rstrip() + "..."
    return text


def _truncate(value: Any, limit: int) -> str:
    text = str(value if value is not None else "")
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def build_labeling_record(
    candidate: dict[str, Any],
    *,
    max_code_diff_chars: int,
    max_docs_chars: int,
) -> dict[str, Any]:
    """
    Build one human-labeling record.

    Important:
    The labeling sheet may show audit context to the human reviewer.
    Evaluation/model scripts must still use only ALLOWED_MODEL_INPUT_FIELDS.
    """
    candidate_evidence = candidate.get("candidate_evidence") or {}

    return {
        "case_id": candidate.get("case_id"),
        "labeling_status": "needs_manual_review",

        "model_input": {
            "language": candidate.get("language"),
            "code_changed_files": candidate.get("code_changed_files") or [],
            "code_diff_excerpt": _truncate(candidate.get("code_diff_excerpt") or "", max_code_diff_chars),
            "docs_before_excerpt": _truncate(candidate.get("docs_before_excerpt") or "", max_docs_chars),
        },

        "audit_labeling_context": {
            "source_url": candidate.get("source_url"),
            "repository": candidate.get("repository"),
            "pr_number": candidate.get("pr_number"),
            "pr_title": candidate.get("pr_title"),
            "docs_changed_files": candidate.get("docs_changed_files") or [],
            "docs_diff_excerpt": _truncate(candidate.get("docs_diff_excerpt") or "", max_code_diff_chars),
            "docs_after_excerpt": _truncate(candidate.get("docs_after_excerpt") or "", max_docs_chars),
            "candidate_evidence": candidate_evidence,
        },

        "gold_label_to_fill": {
            "gold_docs_update_required": None,
            "gold_doc_category": None,
            "gold_target_doc_file": None,
            "gold_target_section": None,
            "gold_patch_summary": None,
            "label_confidence": "needs_manual_review",
            "manual_label_notes": "",
        },

        "labeling_guidance": {
            "gold_docs_update_required": "true if the code change should reasonably require project documentation update; false if it is internal/no-update; null if ambiguous.",
            "gold_doc_category_options": DOC_CATEGORY_OPTIONS,
            "label_confidence_options": LABEL_CONFIDENCE_OPTIONS,
            "important_rule": "Do not copy audit_labeling_context into model input. It is only for human validation and final scoring.",
        },

        "allowed_model_input_fields": ALLOWED_MODEL_INPUT_FIELDS,
        "audit_only_fields": AUDIT_LABELING_CONTEXT_FIELDS + GOLD_LABEL_FIELDS,
    }


def build_labeling_sheet(
    candidates: list[dict[str, Any]],
    *,
    max_code_diff_chars: int,
    max_docs_chars: int,
) -> list[dict[str, Any]]:
    return [
        build_labeling_record(
            candidate,
            max_code_diff_chars=max_code_diff_chars,
            max_docs_chars=max_docs_chars,
        )
        for candidate in candidates
    ]


def write_markdown_review_pack(path: Path, labeling_rows: list[dict[str, Any]], source_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    candidate_type_counts = Counter(
        str((row.get("audit_labeling_context") or {}).get("candidate_evidence", {}).get("candidate_type"))
        for row in labeling_rows
    )
    language_counts = Counter(
        str((row.get("model_input") or {}).get("language"))
        for row in labeling_rows
    )

    lines: list[str] = [
        "# DocGuard Real PR Manual Labeling Pack",
        "",
        "This file is for human validation of real public GitHub PR candidate cases.",
        "",
        "**Important:** this is not model input. It includes audit context such as documentation diffs and docs-after text so a human can assign gold labels. Model/evaluation scripts must use only the explicitly allowed model input fields.",
        "",
        f"- Source candidates: `{source_path}`",
        f"- Records to review: `{len(labeling_rows)}`",
        f"- Candidate type counts: `{dict(candidate_type_counts)}`",
        f"- Language counts: `{dict(language_counts)}`",
        "",
        "## Allowed Model Input Fields",
        "",
    ]

    for field in ALLOWED_MODEL_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Audit / Human Labeling Context",
            "",
        ]
    )

    for field in AUDIT_LABELING_CONTEXT_FIELDS + GOLD_LABEL_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Labeling Rules",
            "",
            "- Mark `gold_docs_update_required = true` only when the code change has visible user/developer/operator/API/data/config/testing/workflow documentation impact.",
            "- Mark `gold_docs_update_required = false` when the change is internal-only, test-only, fixture/mock/storybook-only, formatting-only, import-only, or implementation detail without documentation impact.",
            "- Use `label_confidence = high` only when the decision is clear.",
            "- Use `label_confidence = medium` when likely but not perfectly obvious.",
            "- Use `label_confidence = low` or `ambiguous` when absence/presence of docs is not enough to decide.",
            "- Use `exclude` for cases that are too large, unrelated, generated, binary-heavy, or impossible to judge from the extracted context.",
            "- Never use `docs_after_excerpt` as model input. It is only for gold label validation.",
            "",
            "## Compact Review Table",
            "",
            "| Case | Source | Language | Candidate type | Code files | Docs files | Current label |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )

    for row in labeling_rows:
        model_input = row.get("model_input") or {}
        context = row.get("audit_labeling_context") or {}
        evidence = context.get("candidate_evidence") or {}
        gold = row.get("gold_label_to_fill") or {}

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_safe_cell(row.get('case_id'), 80)}`",
                    _safe_cell(context.get("source_url"), 120),
                    f"`{_safe_cell(model_input.get('language'), 40)}`",
                    f"`{_safe_cell(evidence.get('candidate_type'), 80)}`",
                    f"`{len(model_input.get('code_changed_files') or [])}`",
                    f"`{len(context.get('docs_changed_files') or [])}`",
                    f"`{_safe_cell(gold.get('label_confidence'), 40)}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Detailed Review Cases", ""])

    for row in labeling_rows:
        model_input = row.get("model_input") or {}
        context = row.get("audit_labeling_context") or {}
        gold = row.get("gold_label_to_fill") or {}

        lines.extend(
            [
                f"### `{row.get('case_id')}`",
                "",
                f"- Source URL: {context.get('source_url')}",
                f"- Repository: `{context.get('repository')}`",
                f"- PR number: `{context.get('pr_number')}`",
                f"- PR title: {_safe_cell(context.get('pr_title'), 300)}",
                f"- Language: `{model_input.get('language')}`",
                f"- Code changed files: `{model_input.get('code_changed_files')}`",
                f"- Docs changed files: `{context.get('docs_changed_files')}`",
                "",
                "Gold label fields to fill:",
                "",
                "```json",
                json.dumps(gold, ensure_ascii=False, indent=2),
                "```",
                "",
                "Allowed model input — code diff excerpt:",
                "",
                "```diff",
                str(model_input.get("code_diff_excerpt") or ""),
                "```",
                "",
                "Allowed model input — docs before excerpt:",
                "",
                "```markdown",
                str(model_input.get("docs_before_excerpt") or ""),
                "```",
                "",
                "Audit context only — docs diff excerpt:",
                "",
                "```diff",
                str(context.get("docs_diff_excerpt") or ""),
                "```",
                "",
                "Audit context only — docs after excerpt:",
                "",
                "```markdown",
                str(context.get("docs_after_excerpt") or ""),
                "```",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_labeling_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    template = {
        "case_id": "GH-CAND-0001",
        "gold_docs_update_required": True,
        "gold_doc_category": "api_reference",
        "gold_target_doc_file": "README.md",
        "gold_target_section": "API",
        "gold_patch_summary": "Describe exactly what documentation should be updated.",
        "label_confidence": "high",
        "manual_label_notes": "Explain why this label is correct. This remains audit-only.",
    }
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report_summary(path: Path, labeling_rows: list[dict[str, Any]], source_path: Path, output_jsonl: Path, output_md: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "status": "ok",
        "source_candidates": str(source_path),
        "labeling_jsonl": str(output_jsonl),
        "labeling_markdown": str(output_md),
        "records": len(labeling_rows),
        "labeling_status_counts": dict(Counter(str(row.get("labeling_status")) for row in labeling_rows)),
        "language_counts": dict(Counter(str((row.get("model_input") or {}).get("language")) for row in labeling_rows)),
        "candidate_type_counts": dict(
            Counter(
                str((row.get("audit_labeling_context") or {}).get("candidate_evidence", {}).get("candidate_type"))
                for row in labeling_rows
            )
        ),
        "allowed_model_input_fields": ALLOWED_MODEL_INPUT_FIELDS,
        "audit_only_fields": AUDIT_LABELING_CONTEXT_FIELDS + GOLD_LABEL_FIELDS,
    }

    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a manual labeling pack from DocGuard real PR candidate records.")
    parser.add_argument("--input", required=True, help="Candidate JSONL produced by github_pr_dataset_builder.")
    parser.add_argument("--output-jsonl", required=True, help="Output JSONL labeling pack.")
    parser.add_argument("--output-md", required=True, help="Output Markdown human review pack.")
    parser.add_argument("--summary-json", required=True, help="Output JSON summary.")
    parser.add_argument("--template-json", default=None, help="Optional label template JSON path.")
    parser.add_argument("--max-code-diff-chars", type=int, default=9000)
    parser.add_argument("--max-docs-chars", type=int, default=5000)
    args = parser.parse_args()

    source_path = Path(args.input)
    candidates = load_jsonl(source_path)
    labeling_rows = build_labeling_sheet(
        candidates,
        max_code_diff_chars=args.max_code_diff_chars,
        max_docs_chars=args.max_docs_chars,
    )

    output_jsonl = Path(args.output_jsonl)
    output_md = Path(args.output_md)
    summary_json = Path(args.summary_json)

    write_jsonl(output_jsonl, labeling_rows)
    write_markdown_review_pack(output_md, labeling_rows, source_path)
    write_report_summary(summary_json, labeling_rows, source_path, output_jsonl, output_md)

    if args.template_json:
        write_labeling_template(Path(args.template_json))

    print(
        json.dumps(
            {
                "status": "ok",
                "input": str(source_path),
                "output_jsonl": str(output_jsonl),
                "output_md": str(output_md),
                "summary_json": str(summary_json),
                "records": len(labeling_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())