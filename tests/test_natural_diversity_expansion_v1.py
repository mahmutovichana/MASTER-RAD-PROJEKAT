from __future__ import annotations

from scripts.run_natural_diversity_expansion_v1 import (
    CURATED_REPOSITORIES,
    docs_from_tree,
    forbidden_path,
    norm_repo,
    select_shortlist,
)
from scripts.finalize_natural_diversity_expansion_v1 import (
    FORBIDDEN_REVIEW_FIELDS,
    deterministic_repo_split,
    make_review_row,
)
from scripts.prepare_natural_diversity_pilot_v1 import round_robin_seeds


def profile(repo: str, group: str, *, owner: str | None = None, surface: str = "developer_setup") -> dict:
    owner = owner or repo.split("/", 1)[0]
    return {
        "repository": repo,
        "language_group": group,
        "surface_coverage": 3,
        "documentation_file_count": 10,
        "stars": 100,
        "expected_pr_volume_proxy": 20,
        "documentation_surface_signals": {surface: 1},
        "likely_surface_for_pilot": surface,
    }


def test_normalization_and_forbidden_paths() -> None:
    assert norm_repo("https://github.com/Org/Repo.git/") == "org/repo"
    assert forbidden_path("experiments/consolidated/cascade_confirmation/rows.jsonl")
    assert forbidden_path("data/docs_after_excerpt.jsonl")
    assert not forbidden_path("data/final_v2/repository_universe/manifest.json")


def test_docs_path_profile_accepts_github_file_and_blob_types() -> None:
    paths = docs_from_tree([
        {"type": "file", "path": "README.md"},
        {"type": "blob", "path": "docs/api_reference.rst"},
        {"type": "file", "path": "src/main.py"},
    ])
    assert paths == ["README.md", "docs/api_reference.rst"]


def test_shortlist_is_language_capped_and_owner_capped() -> None:
    rows = [profile("a/one", "python"), profile("a/two", "python"), profile("a/three", "python"), profile("b/one", "typescript_javascript"), profile("c/one", "typescript_javascript")]
    selected = select_shortlist(rows, python_target=2, ts_target=2)
    assert len(selected) == 4
    assert sum(row["language_group"] == "python" for row in selected) == 2
    assert sum(row["language_group"] == "typescript_javascript" for row in selected) == 2
    assert sum(row["repository"].startswith("a/") for row in selected) <= 2
    assert [row["shortlist_rank"] for row in selected] == [1, 2, 3, 4]


def test_curated_candidates_are_repository_names() -> None:
    assert all(" " not in item.strip() for item in CURATED_REPOSITORIES if item.strip())


def test_repository_split_is_deterministic_and_label_independent() -> None:
    repos = {f"org/repo-{index}" for index in range(10)}
    first = deterministic_repo_split(repos, seed=7)
    second = deterministic_repo_split(repos, seed=7)
    assert first == second
    assert list(first.values()).count("refresh_validation") == 2
    assert list(first.values()).count("development_train") == 8


def test_review_row_is_pending_and_excludes_audit_only_fields() -> None:
    candidate = {
        "case_id": "c1", "repository": "Org/Repo", "pr_number": 1,
        "source_url": "https://github.com/org/repo/pull/1", "base_sha": "abc",
        "docs_after_excerpt": "forbidden", "docs_diff_excerpt": "forbidden",
        "classifier_model_input": {
            "language": "python", "code_changed_files": ["app.py"],
            "code_diff_excerpt": "+x", "docs_before_excerpt": "setup",
        },
        "docs_before_retrieved_files": ["README.md"],
        "documentation_context_candidates": [],
    }
    review = make_review_row(candidate, surface="developer_setup", partition="development_train")
    assert review["review_status"] == "pending"
    assert review["label_source"] is None
    assert review["human_docs_update_required"] is None
    assert not (set(review) & FORBIDDEN_REVIEW_FIELDS)


def test_round_robin_seed_plan_caps_without_label_use() -> None:
    seeds = [
        {"repo": repo, "pr_number": index}
        for index in range(3)
        for repo in ("a/one", "b/two")
    ]
    ordered = round_robin_seeds(seeds, ["a/one", "b/two"], per_repo=2, minimum_per_repo=1)
    assert [(row["repo"], row["pr_number"]) for row in ordered] == [
        ("a/one", 0), ("b/two", 0), ("a/one", 1), ("b/two", 1)
    ]
