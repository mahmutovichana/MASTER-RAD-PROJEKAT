from __future__ import annotations

import json
from pathlib import Path

from docguard_external.github_pr_dataset_builder import (
    BuildConfig,
    build_candidate_case,
    build_dataset,
    infer_language_from_files,
    is_code_path,
    is_docs_path,
    load_seed_records,
    parse_pr_url,
    write_jsonl,
)


class FakeGitHubClient:
    def __init__(self) -> None:
        self.pull = {
            "title": "Add user DTO and update API docs",
            "state": "closed",
            "merged_at": "2026-08-21T10:00:00Z",
            "base": {"sha": "base123"},
            "head": {"sha": "head456"},
        }
        self.files = [
            {
                "filename": "src/api/user.ts",
                "status": "modified",
                "additions": 5,
                "deletions": 1,
                "patch": "@@ -1,3 +1,8 @@\n+export type UserDto = {\n+  id: string\n+}",
            },
            {
                "filename": "README.md",
                "status": "modified",
                "additions": 3,
                "deletions": 0,
                "patch": "@@ -10,3 +10,6 @@\n+Document UserDto.",
            },
        ]
        self.file_texts = {
            ("README.md", "base123"): "# Project\n\nOld API docs.",
            ("README.md", "head456"): "# Project\n\nOld API docs.\n\nDocument UserDto.",
        }

    def get_pull(self, repo: str, pr_number: int) -> dict:
        assert repo == "example/repo"
        assert pr_number == 123
        return self.pull

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
        assert repo == "example/repo"
        assert pr_number == 123
        return self.files

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        assert repo == "example/repo"
        return self.file_texts.get((path, ref))


def test_parse_pr_url() -> None:
    repo, pr_number = parse_pr_url("https://github.com/example/repo/pull/123")

    assert repo == "example/repo"
    assert pr_number == 123


def test_file_classification() -> None:
    assert is_code_path("src/api/user.ts") is True
    assert is_code_path("README.md") is False
    assert is_docs_path("README.md") is True
    assert is_docs_path("docs/api.md") is True
    assert is_docs_path("src/api/user.ts") is False


def test_infer_language_from_files() -> None:
    assert infer_language_from_files(["src/a.ts", "src/b.tsx"]) == "typescript"
    assert infer_language_from_files(["service/main.py"]) == "python"
    assert infer_language_from_files(["unknown/file.weird"]) == "unknown"
    assert infer_language_from_files(["service/main.py"], language_hint="python-custom") == "python-custom"


def test_build_candidate_case_from_fake_github_client() -> None:
    seed = {
        "url": "https://github.com/example/repo/pull/123",
        "repo": "example/repo",
        "pr_number": 123,
        "language_hint": "typescript",
    }

    case, reject = build_candidate_case(
        seed=seed,
        client=FakeGitHubClient(),
        case_id="GH-CAND-0001",
        config=BuildConfig(max_code_diff_chars=5000, max_docs_chars=2000),
    )

    assert reject is None
    assert case is not None
    assert case["case_id"] == "GH-CAND-0001"
    assert case["repository"] == "example/repo"
    assert case["pr_number"] == 123
    assert case["language"] == "typescript"
    assert case["code_changed_files"] == ["src/api/user.ts"]
    assert case["docs_changed_files"] == ["README.md"]
    assert "UserDto" in case["code_diff_excerpt"]
    assert "Old API docs" in case["docs_before_excerpt"]
    assert "Document UserDto" in case["docs_after_excerpt"]
    assert case["gold_docs_update_required"] is None
    assert case["label_confidence"] == "needs_manual_review"
    assert case["candidate_evidence"]["candidate_type"] == "code_and_docs_changed_needs_manual_validation"

    allowed_blob = json.dumps(
        {
            "language": case["language"],
            "code_changed_files": case["code_changed_files"],
            "code_diff_excerpt": case["code_diff_excerpt"],
            "docs_before_excerpt": case["docs_before_excerpt"],
        },
        ensure_ascii=False,
    )

    assert "docs_after_excerpt" not in allowed_blob
    assert "gold_docs_update_required" not in allowed_blob
    assert "manual_label_notes" not in allowed_blob


def test_build_dataset_rejects_doc_only_pr() -> None:
    class DocOnlyClient(FakeGitHubClient):
        def get_pull_files(self, repo: str, pr_number: int) -> list[dict]:
            return [
                {
                    "filename": "README.md",
                    "status": "modified",
                    "additions": 2,
                    "deletions": 0,
                    "patch": "@@ -1,2 +1,4 @@\n+Docs only.",
                }
            ]

    seeds = [
        {
            "url": "https://github.com/example/repo/pull/123",
            "repo": "example/repo",
            "pr_number": 123,
            "language_hint": "",
        }
    ]

    cases, rejects = build_dataset(
        seeds=seeds,
        client=DocOnlyClient(),
        config=BuildConfig(),
    )

    assert cases == []
    assert len(rejects) == 1
    assert rejects[0]["reject_reason"] == "no_code_files_changed"


def test_load_seed_records_from_jsonl(tmp_path: Path) -> None:
    seed_path = tmp_path / "seeds.jsonl"
    seed_path.write_text(
        json.dumps({"url": "https://github.com/example/repo/pull/123", "language_hint": "typescript"}),
        encoding="utf-8",
    )

    seeds = load_seed_records(seed_path)

    assert len(seeds) == 1
    assert seeds[0]["repo"] == "example/repo"
    assert seeds[0]["pr_number"] == 123
    assert seeds[0]["language_hint"] == "typescript"


def test_write_jsonl(tmp_path: Path) -> None:
    output = tmp_path / "out.jsonl"
    write_jsonl(output, [{"a": 1}, {"b": 2}])

    lines = output.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert json.loads(lines[0]) == {"a": 1}
    assert json.loads(lines[1]) == {"b": 2}