from __future__ import annotations

import json
from pathlib import Path

from docguard_external.github_pr_seed_collector import (
    classify_pr_files,
    collect_seed_records,
    load_repo_records,
    should_keep_seed,
)


class FakeSeedCollectorClient:
    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100) -> list[dict]:
        if page > 1:
            return []
        return [
            {
                "number": 1,
                "html_url": f"https://github.com/{repo}/pull/1",
                "title": "Add API docs with code change",
                "merged_at": "2026-08-21T10:00:00Z",
            },
            {
                "number": 2,
                "html_url": f"https://github.com/{repo}/pull/2",
                "title": "Closed but not merged",
                "merged_at": None,
            },
            {
                "number": 3,
                "html_url": f"https://github.com/{repo}/pull/3",
                "title": "Test fixture only",
                "merged_at": "2026-08-21T11:00:00Z",
            },
        ]

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
        if pr_number == 1:
            return [
                {"filename": "src/api/user.ts", "additions": 10, "deletions": 2},
                {"filename": "README.md", "additions": 5, "deletions": 1},
            ]
        if pr_number == 3:
            return [
                {"filename": "src/testing/fixtures/user.ts", "additions": 4, "deletions": 0},
            ]
        return []


def test_classify_pr_files_code_and_docs() -> None:
    files = [
        {"filename": "src/api/user.ts", "additions": 10, "deletions": 2},
        {"filename": "docs/api.md", "additions": 4, "deletions": 0},
    ]

    result = classify_pr_files(files)

    assert result["bucket"] == "code_and_docs"
    assert result["code_changed_files"] == ["src/api/user.ts"]
    assert result["docs_changed_files"] == ["docs/api.md"]


def test_classify_pr_files_test_fixture_only() -> None:
    files = [
        {"filename": "apps/web/src/testing/fixtures/auth.ts", "additions": 10, "deletions": 0},
        {"filename": "apps/web/src/features/auth/login-panel.stories.tsx", "additions": 5, "deletions": 0},
    ]

    result = classify_pr_files(files)

    assert result["bucket"] == "code_only_tests_or_fixtures"
    assert result["all_code_files_tests_or_fixtures"] is True


def test_should_keep_seed_rejects_large_patch() -> None:
    classification = {
        "bucket": "code_and_docs",
        "total_changed_file_count": 2,
        "additions": 5000,
        "deletions": 1,
    }

    keep, reason = should_keep_seed(
        classification=classification,
        include_docs_only=False,
        include_other=False,
        max_changed_files=40,
        max_total_patch_lines=3000,
    )

    assert keep is False
    assert reason == "too_large_patch"


def test_collect_seed_records_from_fake_client() -> None:
    repos = [{"repo": "example/repo", "language_hint": "typescript", "notes": ""}]

    seeds, rejects = collect_seed_records(
        repos=repos,
        client=FakeSeedCollectorClient(),
        max_pages_per_repo=1,
        max_prs_per_repo=10,
        target_total=None,
        include_docs_only=False,
        include_other=False,
        max_changed_files=40,
        max_total_patch_lines=3000,
        sleep_seconds=0,
    )

    assert len(seeds) == 2
    assert seeds[0]["repo"] == "example/repo"
    assert seeds[0]["collector_bucket"] == "code_and_docs"
    assert seeds[1]["collector_bucket"] == "code_only_tests_or_fixtures"
    assert any(row["reject_reason"] == "not_merged" for row in rejects)


def test_load_repo_records_from_txt(tmp_path: Path) -> None:
    repo_file = tmp_path / "repos.txt"
    repo_file.write_text(
        "example/repo,typescript\nother/project,python\n",
        encoding="utf-8",
    )

    rows = load_repo_records(repo_file)

    assert rows == [
        {"repo": "example/repo", "language_hint": "typescript", "notes": ""},
        {"repo": "other/project", "language_hint": "python", "notes": ""},
    ]


def test_load_repo_records_from_jsonl(tmp_path: Path) -> None:
    repo_file = tmp_path / "repos.jsonl"
    repo_file.write_text(
        json.dumps({"repo": "example/repo", "language_hint": "typescript", "notes": "demo"}),
        encoding="utf-8",
    )

    rows = load_repo_records(repo_file)

    assert rows == [{"repo": "example/repo", "language_hint": "typescript", "notes": "demo"}]