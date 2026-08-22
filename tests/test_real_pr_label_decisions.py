from __future__ import annotations

import csv
import json
from pathlib import Path

from docguard_external.real_pr_label_decisions import (
    apply_decisions,
    export_decision_csv,
    load_decisions_csv,
)


def sample_labeling_row(case_id: str = "GH-CAND-0001") -> dict:
    return {
        "case_id": case_id,
        "labeling_status": "needs_manual_review",
        "model_input": {
            "language": "typescript",
            "code_changed_files": ["src/api/user.ts"],
            "code_diff_excerpt": "+export type UserDto = { id: string }",
            "docs_before_excerpt": "# API",
        },
        "audit_labeling_context": {
            "source_url": "https://github.com/example/repo/pull/123",
            "repository": "example/repo",
            "pr_number": 123,
            "pr_title": "Add user DTO",
            "docs_changed_files": ["README.md"],
            "docs_diff_excerpt": "+Document UserDto",
            "docs_after_excerpt": "# API\nDocument UserDto",
            "candidate_evidence": {
                "candidate_type": "code_and_docs_changed_needs_manual_validation",
            },
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
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_export_decision_csv(tmp_path: Path) -> None:
    input_jsonl = tmp_path / "labeling.jsonl"
    output_csv = tmp_path / "decisions.csv"
    write_jsonl(input_jsonl, [sample_labeling_row()])

    result = export_decision_csv(input_jsonl=input_jsonl, output_csv=output_csv)

    assert result["status"] == "ok"
    assert output_csv.exists()

    with output_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert rows[0]["case_id"] == "GH-CAND-0001"
    assert rows[0]["source_url"] == "https://github.com/example/repo/pull/123"
    assert rows[0]["label_confidence"] == "needs_manual_review"


def test_apply_decisions_updates_gold_label(tmp_path: Path) -> None:
    input_jsonl = tmp_path / "labeling.jsonl"
    decisions_csv = tmp_path / "decisions.csv"
    output_jsonl = tmp_path / "labeled.jsonl"

    write_jsonl(input_jsonl, [sample_labeling_row()])

    decisions_csv.write_text(
        "\n".join(
            [
                "case_id,source_url,repository,pr_number,pr_title,language,candidate_type,code_file_count,docs_file_count,has_docs_before_excerpt,has_docs_after_excerpt,gold_docs_update_required,gold_doc_category,gold_target_doc_file,gold_target_section,gold_patch_summary,label_confidence,manual_label_notes",
                "GH-CAND-0001,https://github.com/example/repo/pull/123,example/repo,123,Add user DTO,typescript,code_and_docs_changed_needs_manual_validation,1,1,true,true,true,model_contract,README.md,API,Document UserDto,high,Visible DTO contract changed",
            ]
        ),
        encoding="utf-8",
    )

    result = apply_decisions(
        input_jsonl=input_jsonl,
        decisions_csv=decisions_csv,
        output_jsonl=output_jsonl,
    )

    assert result["status"] == "ok"
    assert result["output_records"] == 1

    row = json.loads(output_jsonl.read_text(encoding="utf-8").strip())

    assert row["labeling_status"] == "labeled"
    assert row["gold_label_to_fill"]["gold_docs_update_required"] is True
    assert row["gold_label_to_fill"]["gold_doc_category"] == "model_contract"
    assert row["gold_label_to_fill"]["label_confidence"] == "high"


def test_load_decisions_csv_rejects_invalid_confidence(tmp_path: Path) -> None:
    decisions_csv = tmp_path / "bad.csv"
    decisions_csv.write_text(
        "\n".join(
            [
                "case_id,gold_docs_update_required,gold_doc_category,gold_target_doc_file,gold_target_section,gold_patch_summary,label_confidence,manual_label_notes",
                "GH-CAND-0001,true,model_contract,README.md,API,Patch,bad_confidence,notes",
            ]
        ),
        encoding="utf-8",
    )

    try:
        load_decisions_csv(decisions_csv)
    except ValueError as exc:
        assert "invalid label_confidence" in str(exc)
    else:
        raise AssertionError("Expected invalid label_confidence to raise ValueError")