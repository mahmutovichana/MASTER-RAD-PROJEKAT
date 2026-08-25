from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from docguard_external.github_pr_dataset_builder import BuildConfig, load_seed_records
from docguard_external.github_pr_dataset_builder_v2 import build_dataset_v2, stable_case_id
from docguard_external.github_pr_seed_collector import collect_seed_records
from scripts.audit_final_dataset_v2 import audit as audit_final
from scripts.build_repository_partitions_v2 import assign_partitions
from scripts.finalize_human_gold_v2 import finalize_row
from scripts.merge_final_v2_review_sources import merge_sources
from scripts.migrate_human_reviewed_v1_to_v2 import migrate_row
from scripts.prefill_human_label_sheet_v2 import prefill_row


def base_row(case_id: str = "case-1", repo: str = "org/repo") -> dict:
    return {
        "case_id": case_id,
        "repository": repo,
        "source_url": f"https://github.com/{repo}/pull/{case_id[-1]}",
        "language": "python",
        "code_changed_files": ["src/api.py"],
        "code_diff_excerpt": "+app.get('/reviews')",
        "docs_before_excerpt": "# API",
        "docs_changed_files": ["docs/api.md"],
        "docs_diff_excerpt": "+Document reviews",
        "docs_after_excerpt": "# API\nGET /reviews",
        "pr_title": "Add reviews API",
    }


def test_prefill_cannot_emit_gold_fields() -> None:
    row = base_row()
    row["gold_docs_update_required"] = False

    result = prefill_row(row)

    assert not any(key.startswith("gold_") for key in result)
    assert "suggested_docs_update_required" in result
    assert result["review_status"] == ""
    assert result["human_docs_update_required"] is None


def test_finalizer_refuses_unreviewed_row() -> None:
    row = base_row()
    row.update({"review_status": "pending", "human_docs_update_required": True, "human_doc_category": "api_reference"})

    with pytest.raises(ValueError, match="approved"):
        finalize_row(row, 1)


def test_human_labels_exactly_become_gold_labels() -> None:
    row = base_row()
    row.update({"review_status": "approved", "human_docs_update_required": True, "human_doc_category": "configuration"})

    finalized = finalize_row(row, 1)

    assert finalized["gold_docs_update_required"] is True
    assert finalized["gold_doc_category"] == "configuration"
    assert finalized["label_source"] == "human_reviewed_final_v2"
    assert finalized["human_review_complete"] is True


def test_negative_row_becomes_no_update() -> None:
    row = base_row()
    row.update({"review_status": "approved", "human_docs_update_required": False, "human_doc_category": "api_reference"})

    finalized = finalize_row(row, 1)

    assert finalized["gold_docs_update_required"] is False
    assert finalized["gold_doc_category"] == "no_update"
    assert finalized["stage2_primary_eligible"] is False


def test_other_documentation_stays_binary_positive_but_stage2_ineligible() -> None:
    row = base_row()
    row.update({"review_status": "approved", "human_docs_update_required": True, "human_doc_category": "other_documentation"})

    finalized = finalize_row(row, 1)

    assert finalized["gold_docs_update_required"] is True
    assert finalized["gold_doc_category"] == "other_documentation"
    assert finalized["stage2_primary_eligible"] is False


def test_seen_repo_cannot_enter_confirmation() -> None:
    rows = [base_row("case-1", "org/a"), base_row("case-2", "org/b"), base_row("case-3", "org/c")]

    assignments = assign_partitions(rows, seed=7, confirmation_fraction=1.0, previously_seen={"org/a", "org/b"})

    assert assignments["org/a"] != "confirmation"
    assert assignments["org/b"] != "confirmation"
    assert assignments["org/c"] == "confirmation"


def test_stable_partition_reproducibility_and_natural_counts() -> None:
    rows = [base_row("case-1", "org/a"), base_row("case-2", "org/b"), base_row("case-3", "org/c")]
    rows[0]["gold_docs_update_required"] = True
    rows[1]["gold_docs_update_required"] = False
    rows[2]["gold_docs_update_required"] = False

    first = assign_partitions(rows, seed=42, confirmation_fraction=0.34, previously_seen=set())
    second = assign_partitions(rows, seed=42, confirmation_fraction=0.34, previously_seen=set())

    assert first == second
    assert [row["gold_docs_update_required"] for row in rows] == [True, False, False]


def test_repository_overlap_detection_in_audit() -> None:
    row = base_row()
    row.update(
        {
            "review_status": "approved",
            "human_review_complete": True,
            "label_source": "human_reviewed_final_v2",
            "gold_docs_update_required": True,
            "gold_doc_category": "api_reference",
        }
    )
    manifest = {"confirmation_sealed": True, "repository_assignments": {"org/repo": "development_train", "ORG/REPO": "confirmation"}}

    errors, _report = audit_final([row], manifest, [])

    assert any("repository partition overlap" in error for error in errors)


class LanguageFakeClient:
    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100) -> list[dict]:
        if page > 1:
            return []
        return [{"number": 1, "html_url": f"https://github.com/{repo}/pull/1", "title": "Code change", "merged_at": "2026-08-25T00:00:00Z"}]

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
        return [{"filename": "src/app.py", "additions": 1, "deletions": 0}]


def test_python_minimum_acquisition_does_not_alter_class_labels() -> None:
    repos = [
        {"repo": "org/ts1", "language_hint": "typescript"},
        {"repo": "org/ts2", "language_hint": "typescript"},
        {"repo": "org/py1", "language_hint": "python"},
    ]

    seeds, _rejects = collect_seed_records(
        repos=repos,
        client=LanguageFakeClient(),
        max_pages_per_repo=1,
        max_prs_per_repo=1,
        target_total=2,
        include_docs_only=False,
        include_other=False,
        max_changed_files=40,
        max_total_patch_lines=3000,
        sleep_seconds=0,
        minimum_language_counts={"python": 1},
    )

    assert len(seeds) >= 2
    assert any(row["language_hint"] == "python" for row in seeds)
    assert not any("gold_docs_update_required" in row for row in seeds)


class CandidateFakeClient:
    def get_pull(self, repo: str, pr_number: int) -> dict:
        return {
            "title": "Add API docs",
            "merged_at": "2026-08-25T00:00:00Z",
            "base": {"sha": "base123"},
            "head": {"sha": "head123"},
        }

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
        return [
            {"filename": "src/api.py", "patch": "+app.get('/reviews')", "additions": 1, "deletions": 0},
            {"filename": "docs/changed-only.md", "patch": "+Outcome docs", "additions": 1, "deletions": 0},
        ]

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        if ref == "base123" and path == "README.md":
            return "# Project\nBase documentation."
        if ref == "base123" and path == "docs/changed-only.md":
            return "# Leaky changed doc"
        if ref == "head123" and path == "docs/changed-only.md":
            return "# Outcome doc"
        return None


def test_stable_case_id_independent_of_input_order() -> None:
    assert stable_case_id("Org/Repo", 12) == stable_case_id("org/repo", 12)
    assert stable_case_id("org/repo", 12).startswith("DGPR-")


def test_v2_candidate_duplicate_pr_rejected_and_no_gold_fields() -> None:
    seeds = [
        {"url": "https://github.com/org/repo/pull/12", "repo": "org/repo", "pr_number": 12, "language_hint": "python"},
        {"url": "https://github.com/org/repo/pull/12", "repo": "org/repo", "pr_number": 12, "language_hint": "python"},
    ]

    cases, rejects = build_dataset_v2(seeds=seeds, client=CandidateFakeClient(), config=BuildConfig(), max_cases=None)

    assert len(cases) == 1
    assert any("duplicate_repository_pr_number" in row["reject_reason"] for row in rejects)
    assert not any(key.startswith("gold_") for key in cases[0])


def test_docs_changed_and_after_cannot_affect_docs_before_excerpt() -> None:
    seed_a = {"url": "https://github.com/org/repo/pull/12", "repo": "org/repo", "pr_number": 12, "language_hint": "python"}
    seed_b = dict(seed_a)

    cases_a, _ = build_dataset_v2(seeds=[seed_a], client=CandidateFakeClient(), config=BuildConfig(), max_cases=None)
    cases_b, _ = build_dataset_v2(seeds=[seed_b], client=CandidateFakeClient(), config=BuildConfig(), max_cases=None)
    cases_b[0]["docs_changed_files"] = ["docs/something-else.md"]
    cases_b[0]["docs_diff_excerpt"] = "+different"
    cases_b[0]["docs_after_excerpt"] = "# different outcome"

    assert cases_a[0]["docs_before_excerpt"] == cases_b[0]["docs_before_excerpt"]
    assert cases_a[0]["docs_before_retrieved_files"] == ["README.md"]
    assert "no_docs_changed_files" in cases_a[0]["docs_before_retrieval_policy"]


def test_partition_builder_does_not_require_labels_and_labels_do_not_affect_assignment() -> None:
    rows = [base_row("case-1", "org/a"), base_row("case-2", "org/b")]
    unlabeled = [dict(row) for row in rows]
    labeled = [dict(row, gold_docs_update_required=index == 0, gold_doc_category="api_reference") for index, row in enumerate(rows)]

    assert assign_partitions(unlabeled, seed=99, confirmation_fraction=0.5, previously_seen=set()) == assign_partitions(labeled, seed=99, confirmation_fraction=0.5, previously_seen=set())


def test_migration_preserves_decisions_and_maps_unsupported_positive_to_other_documentation() -> None:
    positive = dict(base_row(), gold_docs_update_required=True, gold_doc_category="security", manual_label_notes="reviewed")
    negative = dict(base_row("case-2", "org/other"), gold_docs_update_required=False, gold_doc_category="testing")

    migrated_positive = migrate_row(positive, 1)
    migrated_negative = migrate_row(negative, 2)

    assert migrated_positive["human_docs_update_required"] is True
    assert migrated_positive["original_human_doc_category"] == "security"
    assert migrated_positive["human_doc_category"] == "other_documentation"
    assert migrated_negative["human_docs_update_required"] is False
    assert migrated_negative["human_doc_category"] == "no_update"


def test_migration_refuses_without_human_review_attestation(tmp_path: Path) -> None:
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.jsonl"
    input_path.write_text(json.dumps(dict(base_row(), gold_docs_update_required=True, gold_doc_category="api_reference")) + "\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/migrate_human_reviewed_v1_to_v2.py", "--input", str(input_path), "--output", str(output_path)],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert not output_path.exists()


def test_no_old_category_forcibly_mapped_into_primary_four() -> None:
    for old_category in ["security", "testing", "workflow_documentation", "changelog", "architecture_flow", "project_documentation"]:
        migrated = migrate_row(dict(base_row(), gold_docs_update_required=True, gold_doc_category=old_category), 1)
        assert migrated["human_doc_category"] == "other_documentation"


def test_merge_detects_duplicate_conflicting_human_labels(tmp_path: Path) -> None:
    left = dict(base_row(), review_status="approved", human_docs_update_required=True, human_doc_category="api_reference")
    right = dict(base_row(), review_status="approved", human_docs_update_required=False, human_doc_category="no_update")
    left_path = tmp_path / "left.jsonl"
    right_path = tmp_path / "right.jsonl"
    left_path.write_text(json.dumps(left) + "\n", encoding="utf-8")
    right_path.write_text(json.dumps(right) + "\n", encoding="utf-8")

    _merged, conflicts, _manifest = merge_sources([left_path, right_path])

    assert conflicts
    assert conflicts[0]["conflict_reason"] == "duplicate_pr_with_conflicting_human_labels"


def test_finalizer_inherits_partition_instead_of_recalculating_it() -> None:
    row = base_row()
    row.update({"review_status": "approved", "human_docs_update_required": True, "human_doc_category": "api_reference"})

    finalized = finalize_row(row, 1, {"org/repo": "confirmation"})

    assert finalized["partition"] == "confirmation"


def test_confirmation_is_sealed_in_audit() -> None:
    row = base_row()
    row.update(
        {
            "review_status": "approved",
            "human_review_complete": True,
            "label_source": "human_reviewed_final_v2",
            "gold_docs_update_required": True,
            "gold_doc_category": "api_reference",
            "partition": "confirmation",
        }
    )

    errors, report = audit_final([row], {"confirmation_sealed": True, "repository_assignments": {"org/repo": "confirmation"}}, [])

    assert not errors
    assert report["confirmation_size"] == 1
