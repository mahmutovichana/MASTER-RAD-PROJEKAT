from __future__ import annotations

from pathlib import Path

from docguard_external.github_api_cache import GitHubApiCache


def test_github_api_cache_roundtrip(tmp_path: Path) -> None:
    cache = GitHubApiCache(tmp_path / "cache")
    url = "https://api.github.com/repos/example/repo/pulls/1"
    accept = "application/vnd.github+json"
    payload = {"number": 1, "title": "Demo"}

    assert cache.get_json(url, accept=accept) is None

    cache.set_json(url, payload, accept=accept)

    assert cache.get_json(url, accept=accept) == payload
    assert cache.stats()["cached_json_files"] == 1


def test_github_api_cache_separates_accept_headers(tmp_path: Path) -> None:
    cache = GitHubApiCache(tmp_path / "cache")
    url = "https://api.github.com/repos/example/repo/pulls/1"

    cache.set_json(url, {"kind": "json"}, accept="application/vnd.github+json")
    cache.set_json(url, {"kind": "diff"}, accept="application/vnd.github.diff")

    assert cache.get_json(url, accept="application/vnd.github+json") == {"kind": "json"}
    assert cache.get_json(url, accept="application/vnd.github.diff") == {"kind": "diff"}