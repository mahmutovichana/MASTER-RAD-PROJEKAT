from __future__ import annotations

import json
from pathlib import Path

from scripts.evaluate_real_case_llm_judge import (
    build_llm_decision_prompt,
    build_safe_case_input,
    compute_metrics,
    parse_llm_json,
    run,
)


def test_llm_judge_safe_input_excludes_audit_fields() -> None:
    case = {
        "case_id": "GH-TEST-001",
        "language": "typescript",
        "code_changed_files": ["src/api.ts"],
        "code_diff_excerpt": "+export type UserDto = { id: string }",
        "docs_before_excerpt": "# API",
        "gold_docs_update_required": True,
        "gold_doc_category": "data_model",
        "gold_target_doc_file": "README.md",
        "docs_after_excerpt": "UNIQUE_DOCS_AFTER_SHOULD_NOT_LEAK",
        "manual_label_notes": "UNIQUE_MANUAL_NOTES_SHOULD_NOT_LEAK",
        "change_type": "UNIQUE_CHANGE_TYPE_SHOULD_NOT_LEAK",
        "docs_changed_files": ["README.md"],
        "source_url": "https://github.com/example/repo/pull/1",
    }

    safe_input = build_safe_case_input(case, max_diff_chars=1000, max_docs_chars=1000)
    prompt = build_llm_decision_prompt(safe_input)

    assert "UNIQUE_DOCS_AFTER_SHOULD_NOT_LEAK" not in prompt
    assert "UNIQUE_MANUAL_NOTES_SHOULD_NOT_LEAK" not in prompt
    assert "UNIQUE_CHANGE_TYPE_SHOULD_NOT_LEAK" not in prompt
    assert "gold_docs_update_required" not in prompt
    assert "gold_doc_category" not in prompt
    assert "gold_target_doc_file" not in prompt
    assert "docs_after_excerpt" not in prompt
    assert "docs_changed_files" not in prompt
    assert "source_url" not in prompt


def test_parse_llm_json_accepts_fenced_json() -> None:
    raw = """```json
{
  "docs_update_required": true,
  "confidence": 0.82,
  "documentation_area": "data_model",
  "rationale": "The diff adds a visible DTO field.",
  "evidence": ["UserDto", "id"]
}
```"""

    parsed = parse_llm_json(raw)

    assert parsed["docs_update_required"] is True
    assert parsed["documentation_area"] == "data_model"


def test_compute_metrics_counts_binary_values() -> None:
    rows = [
        {
            "gold_docs_update_required": True,
            "pred_docs_update_required": True,
            "decision_status": "ok",
            "documentation_area": "data_model",
        },
        {
            "gold_docs_update_required": True,
            "pred_docs_update_required": False,
            "decision_status": "ok",
            "documentation_area": "no_update",
        },
        {
            "gold_docs_update_required": False,
            "pred_docs_update_required": False,
            "decision_status": "ok",
            "documentation_area": "no_update",
        },
        {
            "gold_docs_update_required": False,
            "pred_docs_update_required": True,
            "decision_status": "ok",
            "documentation_area": "api",
        },
    ]

    metrics = compute_metrics(rows)

    assert metrics["true_positives"] == 1
    assert metrics["false_negatives"] == 1
    assert metrics["true_negatives"] == 1
    assert metrics["false_positives"] == 1


def test_mock_run_creates_report_without_external_model(tmp_path: Path) -> None:
    input_path = tmp_path / "cases.jsonl"
    output_dir = tmp_path / "out"

    cases = [
        {
            "case_id": "GH-MOCK-001",
            "language": "typescript",
            "code_changed_files": ["src/api.ts"],
            "code_diff_excerpt": "+export type UserDto = { id: string }",
            "docs_before_excerpt": "# Docs",
            "gold_docs_update_required": True,
            "docs_after_excerpt": "SHOULD_NOT_BE_USED",
            "manual_label_notes": "SHOULD_NOT_BE_USED",
            "change_type": "SHOULD_NOT_BE_USED",
        }
    ]
    input_path.write_text("\n".join(json.dumps(case) for case in cases), encoding="utf-8")

    result = run(
        input_path=input_path,
        output_dir=output_dir,
        backend="mock",
        model_name=None,
        case_limit=None,
        max_new_tokens=64,
        temperature=0.0,
        max_diff_chars=1000,
        max_docs_chars=1000,
    )

    assert result["status"] == "ok"
    assert Path(result["predictions"]).exists()
    assert Path(result["report"]).exists()