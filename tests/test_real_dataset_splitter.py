from __future__ import annotations

from pathlib import Path

from docguard_external.real_dataset_splitter import (
    assign_repository_group_splits,
    check_repository_overlap,
    parse_split_fractions,
    split_dataset,
    write_jsonl,
)


def row(case_id: str, repo: str, language: str = "typescript") -> dict:
    return {
        "case_id": case_id,
        "repository": repo,
        "language": language,
        "code_changed_files": ["src/api.ts"],
        "code_diff_excerpt": "+export type UserDto = { id: string }",
        "docs_before_excerpt": "# API",
        "label_confidence": "needs_manual_review",
        "candidate_evidence": {"candidate_type": "code_only_needs_manual_validation"},
    }


def test_parse_split_fractions_default() -> None:
    fractions = parse_split_fractions(None)

    assert fractions == {
        "train": 0.70,
        "validation": 0.15,
        "locked_test": 0.15,
    }


def test_parse_split_fractions_custom() -> None:
    fractions = parse_split_fractions("train=0.6,validation=0.2,locked_test=0.2")

    assert fractions["train"] == 0.6
    assert fractions["validation"] == 0.2
    assert fractions["locked_test"] == 0.2


def test_repository_group_split_has_no_repo_overlap() -> None:
    rows = [
        row("A1", "repo/a"),
        row("A2", "repo/a"),
        row("B1", "repo/b"),
        row("B2", "repo/b"),
        row("C1", "repo/c"),
        row("C2", "repo/c"),
        row("D1", "repo/d"),
        row("D2", "repo/d"),
    ]

    splits = split_dataset(
        rows,
        seed=42,
        strategy="repository_group",
        fractions={"train": 0.5, "validation": 0.25, "locked_test": 0.25},
    )

    overlap = check_repository_overlap(splits)

    assert overlap["has_repository_overlap"] is False
    assert sum(len(split_rows) for split_rows in splits.values()) == len(rows)
    assert all(split_rows[0]["dataset_split"] == split_name for split_name, split_rows in splits.items() if split_rows)


def test_random_split_preserves_all_rows() -> None:
    rows = [row(f"R{i}", f"repo/{i % 3}") for i in range(20)]

    splits = split_dataset(
        rows,
        seed=123,
        strategy="random",
        fractions={"train": 0.7, "validation": 0.15, "locked_test": 0.15},
    )

    all_ids = sorted(item["case_id"] for split_rows in splits.values() for item in split_rows)

    assert all_ids == sorted(item["case_id"] for item in rows)


def test_assign_repository_group_splits_handles_single_repo() -> None:
    rows = [row(f"A{i}", "repo/a") for i in range(5)]

    splits = assign_repository_group_splits(
        rows,
        seed=42,
        fractions={"train": 0.7, "validation": 0.15, "locked_test": 0.15},
    )

    assert sum(len(split_rows) for split_rows in splits.values()) == 5


def test_write_jsonl(tmp_path: Path) -> None:
    output = tmp_path / "rows.jsonl"
    write_jsonl(output, [row("A", "repo/a"), row("B", "repo/b")])

    assert len(output.read_text(encoding="utf-8").splitlines()) == 2