from __future__ import annotations

from docguard_external.real_dataset_validator import validate_rows


def test_validator_accepts_candidate_record_without_gold_label() -> None:
    rows = [
        {
            "case_id": "GH-CAND-0001",
            "language": "typescript",
            "code_changed_files": ["src/api.ts"],
            "code_diff_excerpt": "+export type UserDto = { id: string }",
            "docs_before_excerpt": "# API",
            "docs_after_excerpt": "# API\nDocument UserDto.",
            "gold_docs_update_required": None,
            "gold_doc_category": None,
            "label_confidence": "needs_manual_review",
        }
    ]

    result = validate_rows(rows)

    assert result["status"] == "ok"
    assert result["error_count"] == 0
    assert result["records"] == 1


def test_validator_rejects_audit_key_inside_nested_model_input() -> None:
    rows = [
        {
            "case_id": "GH-CAND-0001",
            "model_input": {
                "language": "typescript",
                "code_changed_files": ["src/api.ts"],
                "code_diff_excerpt": "+export type UserDto = { id: string }",
                "docs_before_excerpt": "# API",
                "docs_after_excerpt": "SHOULD_NOT_BE_HERE",
            },
            "gold_label_to_fill": {
                "gold_docs_update_required": None,
                "gold_doc_category": None,
                "label_confidence": "needs_manual_review",
            },
        }
    ]

    result = validate_rows(rows)

    assert result["status"] == "failed"
    assert any("audit-only key leaked" in error for error in result["errors"])


def test_validator_rejects_duplicate_case_ids() -> None:
    rows = [
        {
            "case_id": "DUP",
            "language": "python",
            "code_changed_files": ["a.py"],
            "code_diff_excerpt": "+print('a')",
            "docs_before_excerpt": "docs",
        },
        {
            "case_id": "DUP",
            "language": "python",
            "code_changed_files": ["b.py"],
            "code_diff_excerpt": "+print('b')",
            "docs_before_excerpt": "docs",
        },
    ]

    result = validate_rows(rows)

    assert result["status"] == "failed"
    assert any("duplicate case_id" in error for error in result["errors"])


def test_validator_checks_high_confidence_label_consistency() -> None:
    rows = [
        {
            "case_id": "GH-LABEL-0001",
            "language": "typescript",
            "code_changed_files": ["src/api.ts"],
            "code_diff_excerpt": "+export type UserDto = { id: string }",
            "docs_before_excerpt": "# API",
            "gold_docs_update_required": True,
            "gold_doc_category": "no_update",
            "label_confidence": "high",
        }
    ]

    result = validate_rows(rows)

    assert result["status"] == "failed"
    assert any("positive high/medium label" in error for error in result["errors"])