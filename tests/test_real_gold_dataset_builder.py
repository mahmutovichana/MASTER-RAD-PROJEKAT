from __future__ import annotations

from docguard_external.real_gold_dataset_builder import build_gold_dataset


def labeling_row(case_id: str, required: bool | None, confidence: str, category: str | None = None) -> dict:
    return {
        "case_id": case_id,
        "model_input": {
            "language": "typescript",
            "code_changed_files": ["src/api.ts"],
            "code_diff_excerpt": "+export type UserDto = { id: string }",
            "docs_before_excerpt": "# API",
        },
        "audit_labeling_context": {
            "source_url": "https://github.com/example/repo/pull/1",
            "repository": "example/repo",
            "pr_number": 1,
            "pr_title": "Demo",
            "docs_after_excerpt": "# API after",
            "candidate_evidence": {
                "candidate_type": "code_and_docs_changed_needs_manual_validation",
            },
        },
        "gold_label_to_fill": {
            "gold_docs_update_required": required,
            "gold_doc_category": category,
            "gold_target_doc_file": "README.md" if required else None,
            "gold_target_section": "API" if required else None,
            "label_confidence": confidence,
            "manual_label_notes": "audit note",
        },
    }


def test_build_gold_dataset_includes_high_and_medium_only() -> None:
    rows = [
        labeling_row("A", True, "high", "model_contract"),
        labeling_row("B", False, "medium", "no_update"),
        labeling_row("C", None, "ambiguous", "ambiguous"),
    ]

    included, excluded = build_gold_dataset(
        rows,
        included_confidences={"high", "medium"},
        label_source="test",
        exclude_empty_docs_before=False,
    )

    assert [row["case_id"] for row in included] == ["A", "B"]
    assert included[0]["gold_docs_update_required"] is True
    assert included[1]["gold_docs_update_required"] is False
    assert excluded[0]["reason"] == "confidence_not_included"


def test_flat_gold_record_does_not_include_docs_after_or_manual_notes() -> None:
    rows = [labeling_row("A", True, "high", "model_contract")]

    included, _excluded = build_gold_dataset(
        rows,
        included_confidences={"high"},
        label_source="test",
        exclude_empty_docs_before=False,
    )

    row = included[0]

    assert "docs_after_excerpt" not in row
    assert "docs_diff_excerpt" not in row
    assert "manual_label_notes" not in row
    assert row["label_source"] == "test"


def test_exclude_empty_docs_before_option() -> None:
    item = labeling_row("A", True, "high", "model_contract")
    item["model_input"]["docs_before_excerpt"] = ""

    included, excluded = build_gold_dataset(
        [item],
        included_confidences={"high"},
        label_source="test",
        exclude_empty_docs_before=True,
    )

    assert included == []
    assert excluded[0]["reason"] == "empty_docs_before_excluded"