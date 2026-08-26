from __future__ import annotations

import io
import json
import subprocess
import sys
import urllib.error
from email.message import Message
from pathlib import Path

import pytest

from docguard_external.github_pr_seed_collector import (
    GitHubRequestError,
    GitHubSeedCollectorClient,
    GlobalAcquisitionStop,
    collect_seed_records,
)


ROOT = Path(__file__).resolve().parents[1]


class Clock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


class Response:
    status = 200

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self) -> "Response":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def headers(**values: str) -> Message:
    message = Message()
    for key, value in values.items():
        message[key.replace("_", "-")] = value
    return message


def http_error(url: str, code: int, body: str, hdrs: Message | None = None) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, "error", hdrs or Message(), io.BytesIO(body.encode("utf-8")))


def test_missing_token_require_authenticated_fails_before_any_request(tmp_path: Path) -> None:
    repos = tmp_path / "repos.txt"
    repos.write_text("org/repo,python\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "docguard_external.github_pr_seed_collector",
            "--repos",
            str(repos),
            "--output",
            str(tmp_path / "out.jsonl"),
            "--report",
            str(tmp_path / "report.md"),
            "--require-authenticated",
            "--github-token-env",
            "DOCGUARD_TEST_MISSING_TOKEN",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert payload["stop_reason"] == "missing_required_github_token"
    assert payload["authenticated"] is False


def test_authorization_header_is_sent_when_token_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    seen_headers = {}

    def fake_urlopen(request, timeout):
        seen_headers["authorization"] = request.get_header("Authorization")
        return Response([])

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = GitHubSeedCollectorClient(token="secret-token", min_request_interval_seconds=0)

    client.get_closed_pulls_page("org/repo", page=1)

    assert seen_headers["authorization"] == "Bearer secret-token"


def test_pacing_between_every_uncached_request(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = Clock()
    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: Response([]))
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0.25, monotonic=clock.monotonic, sleeper=clock.sleep)

    client.get_closed_pulls_page("org/repo", page=1)
    client.get_closed_pulls_page("org/repo", page=2)

    assert client.outbound_request_count == 2
    assert clock.sleeps == [0.25]


class HitCache:
    def __init__(self) -> None:
        self.cache_dir = Path(".")

    def get_json(self, url: str, *, accept: str):
        return []

    def set_json(self, url: str, data, *, accept: str) -> None:
        raise AssertionError("cache hit should not set")

    def stats(self) -> dict:
        return {}


def test_cache_hit_does_not_trigger_pacing_or_request(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_urlopen(request, timeout):
        raise AssertionError("cache hit should not call urlopen")

    monkeypatch.setattr("urllib.request.urlopen", fail_urlopen)
    clock = Clock()
    client = GitHubSeedCollectorClient(cache=HitCache(), min_request_interval_seconds=0.25, monotonic=clock.monotonic, sleeper=clock.sleep)

    assert client.get_closed_pulls_page("org/repo", page=1) == []
    assert client.cache_hit_count == 1
    assert client.outbound_request_count == 0
    assert clock.sleeps == []


def test_secondary_429_with_retry_after_honors_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = Clock()

    def fake_urlopen(request, timeout):
        raise http_error(request.full_url, 429, "You have triggered an abuse detection mechanism", headers(Retry_After="7", x_ratelimit_remaining="4999"))

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0, monotonic=clock.monotonic, sleeper=clock.sleep)

    with pytest.raises(GlobalAcquisitionStop):
        client.get_closed_pulls_page("org/repo", page=1)

    assert clock.sleeps[:3] == [7, 120, 240]
    assert client.request_retry_count == 3
    assert client.stop_reason == "secondary_rate_limit_exhausted"


def test_secondary_429_without_retry_after_waits_at_least_60(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = Clock()
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(http_error(request.full_url, 429, "secondary rate limit", headers(x_ratelimit_remaining="4999"))),
    )
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0, monotonic=clock.monotonic, sleeper=clock.sleep)

    with pytest.raises(GlobalAcquisitionStop):
        client.get_closed_pulls_page("org/repo", page=1)

    assert clock.sleeps[0] == 60


def test_primary_remaining_zero_and_401_stop_globally(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(http_error(request.full_url, 403, "API rate limit exceeded", headers(x_ratelimit_remaining="0", x_ratelimit_reset="1800000000"))),
    )
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0)
    with pytest.raises(GlobalAcquisitionStop):
        client.get_closed_pulls_page("org/repo", page=1)
    assert client.stop_reason == "primary_rate_limit_exhausted"
    assert client.rate_limit_snapshot["rate_limit_reset"] == 1800000000

    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: (_ for _ in ()).throw(http_error(request.full_url, 401, "Bad credentials")))
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0)
    with pytest.raises(GlobalAcquisitionStop):
        client.get_closed_pulls_page("org/repo", page=1)
    assert client.stop_reason == "authentication_failed"


def test_transient_500_retries_are_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"count": 0}
    clock = Clock()

    def fake_urlopen(request, timeout):
        calls["count"] += 1
        if calls["count"] <= 3:
            raise http_error(request.full_url, 500, "server error")
        return Response([])

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = GitHubSeedCollectorClient(min_request_interval_seconds=0, monotonic=clock.monotonic, sleeper=clock.sleep)

    assert client.get_closed_pulls_page("org/repo", page=1) == []
    assert client.request_retry_count == 3
    assert clock.sleeps == [2, 4, 8]


def test_rate_limit_error_is_never_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    class EmptyCache(HitCache):
        def get_json(self, url: str, *, accept: str):
            return None

        def set_json(self, url: str, data, *, accept: str) -> None:
            raise AssertionError("rate limit errors must not be cached")

    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout: (_ for _ in ()).throw(http_error(request.full_url, 429, "secondary rate limit", headers(x_ratelimit_remaining="4999"))),
    )
    client = GitHubSeedCollectorClient(cache=EmptyCache(), min_request_interval_seconds=0, sleeper=lambda seconds: None)

    with pytest.raises(GlobalAcquisitionStop):
        client.get_closed_pulls_page("org/repo", page=1)


class StopAfterFirstRepoClient:
    def __init__(self) -> None:
        self.stop_reason = None
        self.calls = 0

    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100):
        self.calls += 1
        if self.calls > 1:
            self.stop_reason = "secondary_rate_limit_exhausted"
            raise GlobalAcquisitionStop(self.stop_reason)
        return [{"number": 1, "html_url": f"https://github.com/{repo}/pull/1", "title": "Change", "merged_at": "2026-08-26T00:00:00Z"}]

    def get_pull_files(self, repo: str, pr_number: int):
        return [{"filename": "src/app.py", "additions": 1, "deletions": 0}]


def test_seeds_before_global_stop_are_preserved() -> None:
    seeds, rejects = collect_seed_records(
        repos=[{"repo": "org/a", "language_hint": "python"}, {"repo": "org/b", "language_hint": "python"}],
        client=StopAfterFirstRepoClient(),
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
    assert rejects == []


class IsolatedFailureClient(StopAfterFirstRepoClient):
    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100):
        if repo == "org/bad":
            raise GitHubRequestError(status_code=404, url="https://example.test", response_body="not found")
        return [{"number": 1, "html_url": f"https://github.com/{repo}/pull/1", "title": "Change", "merged_at": "2026-08-26T00:00:00Z"}]


def test_isolated_repository_failure_does_not_terminate_unrelated_collection() -> None:
    seeds, rejects = collect_seed_records(
        repos=[{"repo": "org/bad", "language_hint": "python"}, {"repo": "org/good", "language_hint": "python"}],
        client=IsolatedFailureClient(),
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
    assert any(row["reject_reason"] == "fetch_closed_pulls_failed" for row in rejects)
