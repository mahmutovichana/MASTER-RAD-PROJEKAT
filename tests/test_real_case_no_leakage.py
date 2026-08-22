from __future__ import annotations

import json

import pytest

from docguard_external.real_case_runner import assert_no_audit_values, build_runtime_record


def test_docs_after_and_gold_values_do_not_leak_into_runtime_payload() -> None:
    case = {
        "case_id": "LEAK-001",
        "language": "python",
        "code_changed_files": ["src/service.py"],
        "code_diff_excerpt": "+def calculate_new_value():\n+    return 42",
        "docs_before_excerpt": "# Current docs",
        "docs_after_excerpt": "UNIQUE_DOCS_AFTER_VALUE_MUST_NOT_LEAK",
        "gold_patch_summary": "UNIQUE_GOLD_PATCH_SUMMARY_MUST_NOT_LEAK",
        "manual_label_notes": "UNIQUE_MANUAL_NOTES_MUST_NOT_LEAK",
        "change_type": "UNIQUE_CHANGE_TYPE_MUST_NOT_LEAK",
        "docs_changed_files": ["README.md"],
        "gold_docs_update_required": True,
        "gold_doc_category": "configuration",
        "gold_target_doc_file": "README.md",
    }

    runtime = build_runtime_record(case)
    runtime_blob = json.dumps(runtime, ensure_ascii=False, sort_keys=True)

    assert "UNIQUE_DOCS_AFTER_VALUE_MUST_NOT_LEAK" not in runtime_blob
    assert "UNIQUE_GOLD_PATCH_SUMMARY_MUST_NOT_LEAK" not in runtime_blob
    assert "UNIQUE_MANUAL_NOTES_MUST_NOT_LEAK" not in runtime_blob
    assert "UNIQUE_CHANGE_TYPE_MUST_NOT_LEAK" not in runtime_blob

    assert_no_audit_values(case, runtime)


def test_no_leakage_guard_fails_when_audit_value_is_injected() -> None:
    case = {
        "case_id": "LEAK-002",
        "language": "typescript",
        "code_changed_files": ["src/a.ts"],
        "code_diff_excerpt": "+const safe = true",
        "docs_before_excerpt": "# Docs",
        "docs_after_excerpt": "UNIQUE_FORBIDDEN_DOCS_AFTER_TEXT",
    }

    runtime = build_runtime_record(case)
    runtime["bad_field"] = "UNIQUE_FORBIDDEN_DOCS_AFTER_TEXT"

    with pytest.raises(AssertionError):
        assert_no_audit_values(case, runtime)

def test_source_url_value_inside_allowed_excerpt_is_not_false_positive() -> None:
    source_url = "https://github.com/example/project/pull/123"

    case = {
        "case_id": "LEAK-003",
        "language": "typescript",
        "code_changed_files": ["src/routes.ts"],
        "code_diff_excerpt": f"+// Reference kept in code comment: {source_url}",
        "docs_before_excerpt": "# Docs",
        "source_url": source_url,
        "gold_docs_update_required": False,
        "gold_doc_category": "internal_refactor_no_docs_needed",
        "gold_target_doc_file": "",
        "docs_after_excerpt": "UNIQUE_DOCS_AFTER_STILL_MUST_NOT_LEAK",
        "manual_label_notes": "UNIQUE_MANUAL_NOTES_STILL_MUST_NOT_LEAK",
        "change_type": "UNIQUE_CHANGE_TYPE_STILL_MUST_NOT_LEAK",
    }

    runtime = build_runtime_record(case)

    # This should not raise, because source_url appears through allowed code_diff_excerpt,
    # not because the source_url metadata field was copied.
    assert_no_audit_values(case, runtime)