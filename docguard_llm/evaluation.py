from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_llm_mock_patch_report(path: Path, predictions: list[dict[str, Any]], total_cases: int) -> None:
    examples = [row for row in predictions if row.get("llm_prompt")][:3]
    status_counts: dict[str, int] = {}
    for row in predictions:
        status = row.get("patch_verifier_status") or "not_applicable"
        status_counts[status] = status_counts.get(status, 0) + 1
    lines = [
        "# DocGuard LLM Mock Patch Generation Report 2026-08",
        "",
        "This report exercises the optional LLM patch-generation architecture with the mock backend. No HuggingFace model is downloaded or executed.",
        "",
        f"- cases evaluated: {total_cases}",
        f"- patch backend: `llm-mock`",
        f"- verifier status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "When a real HuggingFace instruction model is plugged in, the same prompt builder, postprocessor, and verifier remain in place. Only the generation backend changes from `mock` to `hf`.",
        "",
        "## Prompt Examples",
        "",
    ]
    for row in examples:
        lines.extend(
            [
                f"### `{row['case_id']}`",
                "",
                "Prompt:",
                "",
                "```text",
                row.get("llm_prompt", "")[:2500],
                "```",
                "",
                "Raw mock patch:",
                "",
                "```diff",
                row.get("llm_patch_raw", "") or "not_applicable",
                "```",
                "",
                "Postprocessed patch:",
                "",
                "```diff",
                row.get("generated_doc_patch", "") or "not_applicable",
                "```",
                "",
                f"Verifier: `{row.get('patch_verifier_status')}`; warnings: `{row.get('patch_verifier_warnings')}`; grounded tokens: `{row.get('grounded_tokens_found')}`",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
