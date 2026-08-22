from __future__ import annotations

import json
from pathlib import Path

from docguard_external.real_case_runner import build_runtime_record, run_evaluation


def test_build_runtime_record_uses_only_allowed_runtime_fields() -> None:
    case = {
        "case_id": "REAL-001",
        "language": "typescript",
        "code_changed_files": ["src/routes.ts"],
        "code_diff_excerpt": "+router.post('/reviews', createReview)",
        "docs_before_excerpt": "# API",
        "gold_docs_update_required": True,
        "gold_doc_category": "api",
        "gold_target_doc_file": "README.md",
        "docs_after_excerpt": "SECRET_DOCS_AFTER_SHOULD_NOT_LEAK",
        "manual_label_notes": "SECRET_MANUAL_NOTES_SHOULD_NOT_LEAK",
        "change_type": "SECRET_CHANGE_TYPE_SHOULD_NOT_LEAK",
        "docs_changed_files": ["README.md"],
        "changed_files": ["README.md", "src/routes.ts"],
    }

    runtime = build_runtime_record(case)

    assert runtime["id"] == "REAL-001"
    assert runtime["language"] == "typescript"
    assert runtime["changed_files"] == ["src/routes.ts"]
    assert runtime["code_diff"] == "+router.post('/reviews', createReview)"
    assert runtime["docs_before"] == "# API"

    forbidden_keys = {
        "gold_docs_update_required",
        "gold_doc_category",
        "gold_target_doc_file",
        "docs_after_excerpt",
        "manual_label_notes",
        "change_type",
        "docs_changed_files",
        "changed_files",
    }
    for key in forbidden_keys:
        if key == "changed_files":
            # Runtime needs changed_files, but it must come from code_changed_files only.
            assert runtime["changed_files"] == case["code_changed_files"]
        else:
            assert key not in runtime


def test_run_evaluation_creates_real_case_reports(tmp_path: Path) -> None:
    input_path = tmp_path / "manual_cases.jsonl"
    output_dir = tmp_path / "reports"

    rows = [
        {
            "case_id": "REAL-POSITIVE-001",
            "language": "typescript",
            "code_changed_files": ["src/routes.ts"],
            "code_diff_excerpt": "+router.post('/reviews', createReview)\n+res.status(201).json({ id: saved.id })",
            "docs_before_excerpt": "# API\nExisting endpoints.",
            "gold_docs_update_required": True,
            "gold_doc_category": "api",
            "gold_target_doc_file": "README.md",
            "docs_after_excerpt": "SHOULD_NOT_BE_USED",
            "manual_label_notes": "SHOULD_NOT_BE_USED",
            "change_type": "SHOULD_NOT_BE_USED",
            "docs_changed_files": ["README.md"],
            "changed_files": ["README.md", "src/routes.ts"],
        },
        {
            "case_id": "REAL-NEGATIVE-001",
            "language": "typescript",
            "code_changed_files": ["src/internal.ts"],
            "code_diff_excerpt": "-// old helper comment\n+// clearer helper comment",
            "docs_before_excerpt": "# Developer Notes",
            "gold_docs_update_required": False,
            "gold_doc_category": "internal_refactor_no_docs_needed",
            "gold_target_doc_file": "",
            "docs_after_excerpt": "SHOULD_NOT_BE_USED",
            "manual_label_notes": "SHOULD_NOT_BE_USED",
            "change_type": "SHOULD_NOT_BE_USED",
            "docs_changed_files": [],
            "changed_files": ["src/internal.ts"],
        },
    ]

    input_path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    result = run_evaluation(input_path=input_path, output_dir=output_dir)

    assert result["status"] == "ok"
    assert result["metrics"]["total_cases"] == 2
    assert (output_dir / "docguard_real_case_study_predictions.jsonl").exists()
    assert (output_dir / "docguard_real_case_study_evaluation_2026_08.md").exists()

    report = (output_dir / "docguard_real_case_study_evaluation_2026_08.md").read_text(encoding="utf-8")
    assert "DocGuard Real Project Case Study Evaluation" in report
    assert "Leakage Policy" in report
    assert "docs_after_excerpt" in report