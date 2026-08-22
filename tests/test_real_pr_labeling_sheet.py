from __future__ import annotations

import json
from pathlib import Path

from docguard_external.real_pr_labeling_sheet import (
    build_labeling_record,
    build_labeling_sheet,
    write_markdown_review_pack,
)


def sample_candidate() -> dict:
    return {
        "case_id": "GH-CAND-0001",
        "source_url": "https://github.com/example/repo/pull/123",
        "repository": "example/repo",
        "pr_number": 123,
        "pr_title": "Add user DTO and update API docs",
        "language": "typescript",
        "code_changed_files": ["src/api/user.ts"],
        "code_diff_excerpt": "+export type UserDto = { id: string }",
        "docs_before_excerpt": "# API\nOld docs",
        "changed_files": ["src/api/user.ts", "README.md"],
        "docs_changed_files": ["README.md"],
        "docs_diff_excerpt": "+Document UserDto.",
        "docs_after_excerpt": "# API\nOld docs\nDocument UserDto.",
        "gold_docs_update_required": None,
        "gold_doc_category": None,
        "gold_target_doc_file": None,
        "gold_target_section": None,
        "gold_patch_summary": None,
        "label_confidence": "needs_manual_review",
        "manual_label_notes": "",
        "candidate_evidence": {
            "candidate_type": "code_and_docs_changed_needs_manual_validation",
            "code_file_count": 1,
            "docs_file_count": 1,
        },
    }


def test_build_labeling_record_separates_model_input_from_audit_context() -> None:
    record = build_labeling_record(
        sample_candidate(),
        max_code_diff_chars=1000,
        max_docs_chars=1000,
    )

    assert record["case_id"] == "GH-CAND-0001"

    model_input = record["model_input"]
    audit_context = record["audit_labeling_context"]
    gold = record["gold_label_to_fill"]

    assert set(model_input) == {
        "language",
        "code_changed_files",
        "code_diff_excerpt",
        "docs_before_excerpt",
    }
    assert model_input["language"] == "typescript"
    assert "UserDto" in model_input["code_diff_excerpt"]

    assert audit_context["source_url"] == "https://github.com/example/repo/pull/123"
    assert audit_context["docs_changed_files"] == ["README.md"]
    assert "Document UserDto" in audit_context["docs_after_excerpt"]

    assert gold["gold_docs_update_required"] is None
    assert gold["label_confidence"] == "needs_manual_review"

    model_blob = json.dumps(model_input, ensure_ascii=False)

    assert "docs_after_excerpt" not in model_blob
    assert "gold_docs_update_required" not in model_blob
    assert "manual_label_notes" not in model_blob
    assert "source_url" not in model_blob


def test_build_labeling_sheet_keeps_record_count() -> None:
    rows = build_labeling_sheet(
        [sample_candidate(), sample_candidate()],
        max_code_diff_chars=1000,
        max_docs_chars=1000,
    )

    assert len(rows) == 2
    assert rows[0]["labeling_status"] == "needs_manual_review"


def test_write_markdown_review_pack(tmp_path: Path) -> None:
    rows = build_labeling_sheet(
        [sample_candidate()],
        max_code_diff_chars=1000,
        max_docs_chars=1000,
    )

    output = tmp_path / "review.md"
    write_markdown_review_pack(output, rows, Path("candidates.jsonl"))

    text = output.read_text(encoding="utf-8")

    assert "DocGuard Real PR Manual Labeling Pack" in text
    assert "Allowed Model Input Fields" in text
    assert "Audit context only" in text
    assert "GH-CAND-0001" in text