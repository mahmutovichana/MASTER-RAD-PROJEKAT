from __future__ import annotations

import json
from pathlib import Path

from docguard_external.github_pr_seed_collector import (
    acquisition_exit_code,
    acquisition_summary,
    collect_seed_records,
    load_excluded_seed_identity,
)
import pytest

from scripts.audit_seed_repository_diversity_v2 import capped_rows, ensure_not_overwriting_raw, summarize
from scripts.discover_repository_universe_v2 import discover, eligible_repo
from scripts.merge_repository_universe_v2 import merge as merge_repositories
from scripts.merge_seed_shards_v2 import merge as merge_seed_shards


ROOT = Path(__file__).resolve().parents[1]


class OnePrClient:
    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100) -> list[dict]:
        if page > 1:
            return []
        return [{"number": 1, "html_url": f"https://github.com/{repo}/pull/1", "title": "Change", "merged_at": "2026-08-26T00:00:00Z"}]

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
        return [{"filename": "src/app.py", "additions": 1, "deletions": 0}]


def test_incomplete_target_and_language_minimum_are_partial() -> None:
    seeds = [{"repo": "org/repo", "language_hint": "python"}]

    summary = acquisition_summary(seeds=seeds, repos=[{"repo": "org/repo"}], target_total=2, minimum_language_counts={"python": 2})

    assert summary["status"] == "partial"
    assert summary["requirements_satisfied"] is False
    assert summary["target_total_deficit"] == 1
    assert summary["minimum_language_deficits"]["python"] == 1


def test_requirements_satisfied_true_only_when_all_conditions_pass() -> None:
    summary = acquisition_summary(
        seeds=[{"repo": "org/a", "language_hint": "python"}, {"repo": "org/b", "language_hint": "typescript"}],
        repos=[{"repo": "org/a"}, {"repo": "org/b"}],
        target_total=2,
        minimum_language_counts={"python": 1},
    )

    assert summary["status"] == "complete"
    assert summary["requirements_satisfied"] is True


def test_allow_partial_changes_exit_behavior_but_not_status(tmp_path: Path) -> None:
    assert acquisition_exit_code("partial", allow_partial=False) == 2
    assert acquisition_exit_code("partial", allow_partial=True) == 0
    assert acquisition_exit_code("complete", allow_partial=False) == 0


def test_existing_seed_files_and_duplicates_prevent_recollection(tmp_path: Path) -> None:
    existing = tmp_path / "existing.jsonl"
    existing.write_text(json.dumps({"repo": "org/repo", "pr_number": 1, "url": "https://github.com/org/repo/pull/1"}) + "\n", encoding="utf-8")
    excluded_keys, excluded_urls = load_excluded_seed_identity([existing])

    seeds, rejects = collect_seed_records(
        repos=[{"repo": "org/repo", "language_hint": "python"}],
        client=OnePrClient(),
        max_pages_per_repo=1,
        max_prs_per_repo=2,
        target_total=None,
        include_docs_only=False,
        include_other=False,
        max_changed_files=40,
        max_total_patch_lines=3000,
        sleep_seconds=0,
        excluded_pr_keys=excluded_keys,
        excluded_source_urls=excluded_urls,
    )

    assert seeds == []
    assert rejects[0]["reject_reason"] == "already_collected"


def test_duplicate_repo_pr_and_source_url_are_skipped() -> None:
    seeds, rejects = collect_seed_records(
        repos=[{"repo": "org/repo", "language_hint": "python"}, {"repo": "org/repo", "language_hint": "python"}],
        client=OnePrClient(),
        max_pages_per_repo=1,
        max_prs_per_repo=1,
        target_total=None,
        include_docs_only=False,
        include_other=False,
        max_changed_files=40,
        max_total_patch_lines=3000,
        sleep_seconds=0,
    )

    assert len(seeds) == 1
    assert any(row["reject_reason"] == "already_collected" for row in rejects)


def test_repository_discovery_excludes_forks_archived_and_deduplicates() -> None:
    assert eligible_repo({"full_name": "org/fork", "fork": True, "archived": False, "disabled": False, "pushed_at": "x", "updated_at": "x"}) is False
    assert eligible_repo({"full_name": "org/archive", "fork": False, "archived": True, "disabled": False, "pushed_at": "x", "updated_at": "x"}) is False

    class FakeSearch:
        def search_repositories(self, query: str, *, page: int, per_page: int):
            return [
                {"full_name": "org/repo", "fork": False, "archived": False, "disabled": False, "pushed_at": "x", "updated_at": "x", "created_at": "x", "stargazers_count": 500},
                {"full_name": "org/repo", "fork": False, "archived": False, "disabled": False, "pushed_at": "x", "updated_at": "x", "created_at": "x", "stargazers_count": 500},
                {"full_name": "org/fork", "fork": True, "archived": False, "disabled": False, "pushed_at": "x", "updated_at": "x", "created_at": "x", "stargazers_count": 500},
            ]

    rows, manifest = discover(FakeSearch(), per_language_target=3, per_page=10, max_pages=1, discovered_at="2026-08-26T00:00:00+00:00")

    assert len({row["repo"] for row in rows}) == 1
    assert manifest["duplicates_removed"] >= 1
    assert rows[0]["discovery_stratum"] == "medium_100_999"


def test_repository_merge_preserves_provenance(tmp_path: Path) -> None:
    old = tmp_path / "old.txt"
    new = tmp_path / "new.jsonl"
    old.write_text("Org/Repo,python\n", encoding="utf-8")
    new.write_text(json.dumps({"repo": "org/repo", "language_hint": "python", "provenance": ["discovered_repository_universe_v2"]}) + "\n", encoding="utf-8")

    rows, manifest = merge_repositories([old, new])

    assert len(rows) == 1
    assert "discovered_repository_universe_v2" in rows[0]["provenance"]
    assert manifest["duplicates_removed"] == 1


def test_seed_shard_merge_deduplicates_and_reports_conflict(tmp_path: Path) -> None:
    a = tmp_path / "a.jsonl"
    b = tmp_path / "b.jsonl"
    a.write_text(json.dumps({"repo": "org/repo", "pr_number": 1, "url": "https://github.com/org/repo/pull/1", "language_hint": "python"}) + "\n", encoding="utf-8")
    b.write_text(json.dumps({"repo": "org/repo", "pr_number": 1, "url": "https://github.com/org/repo/pull/1", "language_hint": "typescript"}) + "\n", encoding="utf-8")

    merged, conflicts, _manifest = merge_seed_shards([a, b])

    assert len(merged) == 1
    assert conflicts


def test_diversity_audit_uses_no_labels_and_capping_is_deterministic() -> None:
    rows = [
        {"repo": "org/a", "pr_number": 2, "language_hint": "python", "collector_bucket": "code_only"},
        {"repo": "org/a", "pr_number": 1, "language_hint": "python", "collector_bucket": "code_only"},
        {"repo": "org/b", "pr_number": 1, "language_hint": "typescript", "collector_bucket": "code_and_docs"},
    ]

    report = summarize(rows)
    first = capped_rows(rows, 1)
    second = capped_rows(list(reversed(rows)), 1)

    assert report["uses_gold_labels"] is False
    assert first == second
    assert len(first) == 2


def test_raw_merged_file_is_never_overwritten_by_capped_version(tmp_path: Path) -> None:
    raw = tmp_path / "merged.jsonl"

    with pytest.raises(ValueError, match="must not overwrite"):
        ensure_not_overwriting_raw(raw, raw)
