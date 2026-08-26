from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any


class GlobalGitHubStop(Exception):
    def __init__(self, stop_reason: str, error: "GitHubOperationalError | None" = None) -> None:
        super().__init__(stop_reason)
        self.stop_reason = stop_reason
        self.error = error


class GitHubOperationalError(Exception):
    def __init__(self, *, status_code: int | None, url: str, body: str, headers: Any | None = None, original_error: Exception | None = None) -> None:
        super().__init__(f"HTTP {status_code} from {url}: {body[:500]}" if status_code else f"GitHub request failed {url}: {body}")
        self.status_code = status_code
        self.url = url
        self.body = body
        self.original_error = original_error
        self.retry_after = _int_header(headers, "Retry-After")
        self.rate_limit_remaining = _int_header(headers, "x-ratelimit-remaining")
        self.rate_limit_reset = _int_header(headers, "x-ratelimit-reset")
        self.rate_limit_resource = _str_header(headers, "x-ratelimit-resource")
        lower = (body + " " + str(getattr(original_error, "reason", "") or "") + " " + str(original_error or "")).lower()
        self.is_authentication_failure = status_code == 401
        self.is_primary_rate_limit = status_code in {403, 429} and self.rate_limit_remaining == 0
        self.is_secondary_rate_limit = status_code in {403, 429} and not self.is_primary_rate_limit and any(term in lower for term in ["secondary rate limit", "abuse detection", "abuse rate", "abuse", "rate"])
        self.is_transient = status_code in {500, 502, 503, 504} or status_code is None

    def snapshot(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "url": self.url,
            "retry_after": self.retry_after,
            "rate_limit_remaining": self.rate_limit_remaining,
            "rate_limit_reset": self.rate_limit_reset,
            "rate_limit_resource": self.rate_limit_resource,
            "is_authentication_failure": self.is_authentication_failure,
            "is_primary_rate_limit": self.is_primary_rate_limit,
            "is_secondary_rate_limit": self.is_secondary_rate_limit,
            "is_transient": self.is_transient,
        }


def _str_header(headers: Any | None, name: str) -> str | None:
    if headers is None:
        return None
    try:
        return headers.get(name) or headers.get(name.lower())
    except Exception:
        return None


def _int_header(headers: Any | None, name: str) -> int | None:
    value = _str_header(headers, name)
    if value in {None, ""}:
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


class GitHubClientV2:
    def __init__(
        self,
        *,
        token: str | None,
        timeout_seconds: int = 30,
        cache: Any | None = None,
        min_request_interval_seconds: float = 0.25,
        monotonic: Any = time.monotonic,
        sleeper: Any = time.sleep,
    ) -> None:
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.cache = cache
        self.min_request_interval_seconds = min_request_interval_seconds
        self.monotonic = monotonic
        self.sleeper = sleeper
        self.last_outbound_request_monotonic: float | None = None
        self.outbound_request_count = 0
        self.cache_hit_count = 0
        self.request_retry_count = 0
        self.total_backoff_seconds = 0.0
        self.operational_failures: Counter[str] = Counter()
        self.stop_reason: str | None = None
        self.stop_snapshot: dict[str, Any] = {}

    def _sleep(self, seconds: float) -> None:
        if seconds > 0:
            self.total_backoff_seconds += seconds
            self.sleeper(seconds)

    def _pace(self) -> None:
        now = float(self.monotonic())
        if self.last_outbound_request_monotonic is not None:
            wait = self.min_request_interval_seconds - (now - self.last_outbound_request_monotonic)
            if wait > 0:
                self.sleeper(wait)
                now = float(self.monotonic())
        self.last_outbound_request_monotonic = now

    def _request_uncached(self, url: str) -> Any:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "DocGuard-FinalV2"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        transient_delays = [2, 4, 8]
        secondary_delays = [60, 120, 240]
        transient_attempt = 0
        secondary_attempt = 0
        while True:
            self._pace()
            self.outbound_request_count += 1
            request = urllib.request.Request(url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    return json.loads(response.read().decode("utf-8", errors="replace"))
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                error = GitHubOperationalError(status_code=exc.code, url=url, body=body, headers=exc.headers, original_error=exc)
                self.operational_failures[str(exc.code)] += 1
                if error.is_authentication_failure:
                    self.stop_reason = "authentication_failed"
                    self.stop_snapshot = error.snapshot()
                    raise GlobalGitHubStop(self.stop_reason, error) from exc
                if error.is_primary_rate_limit:
                    self.stop_reason = "primary_rate_limit_exhausted"
                    self.stop_snapshot = error.snapshot()
                    raise GlobalGitHubStop(self.stop_reason, error) from exc
                if error.is_secondary_rate_limit:
                    if secondary_attempt >= len(secondary_delays):
                        self.stop_reason = "secondary_rate_limit_exhausted"
                        self.stop_snapshot = error.snapshot()
                        raise GlobalGitHubStop(self.stop_reason, error) from exc
                    delay = error.retry_after if error.retry_after is not None and secondary_attempt == 0 else secondary_delays[secondary_attempt]
                    secondary_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(float(delay))
                    continue
                if error.is_transient and transient_attempt < len(transient_delays):
                    delay = transient_delays[transient_attempt]
                    transient_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(float(delay))
                    continue
                raise error from exc
            except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
                error = GitHubOperationalError(status_code=None, url=url, body=str(exc), original_error=exc)
                self.operational_failures["network_or_timeout"] += 1
                if transient_attempt < len(transient_delays):
                    delay = transient_delays[transient_attempt]
                    transient_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(float(delay))
                    continue
                raise error from exc

    def request_json(self, url: str) -> Any:
        accept = "application/vnd.github+json"
        if self.cache is not None:
            cached = self.cache.get_json(url, accept=accept)
            if cached is not None:
                self.cache_hit_count += 1
                return cached
        data = self._request_uncached(url)
        if self.cache is not None:
            self.cache.set_json(url, data, accept=accept)
        return data

    def get_pull(self, repo: str, pr_number: int) -> dict[str, Any]:
        encoded = urllib.parse.quote(repo, safe="/")
        return self.request_json(f"https://api.github.com/repos/{encoded}/pulls/{int(pr_number)}")

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict[str, Any]]:
        encoded = urllib.parse.quote(repo, safe="/")
        return self.request_json(f"https://api.github.com/repos/{encoded}/pulls/{int(pr_number)}/files?per_page=100")

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        encoded_repo = urllib.parse.quote(repo, safe="/")
        encoded_path = urllib.parse.quote(path)
        data = self.request_json(f"https://api.github.com/repos/{encoded_repo}/contents/{encoded_path}?ref={urllib.parse.quote(ref)}")
        if not isinstance(data, dict) or data.get("type") != "file":
            return None
        import base64

        content = str(data.get("content") or "")
        encoding = str(data.get("encoding") or "")
        if encoding == "base64":
            return base64.b64decode(content).decode("utf-8", errors="replace")
        return content

    def get_tree_recursive(self, repo: str, ref: str) -> list[dict[str, Any]]:
        encoded = urllib.parse.quote(repo, safe="/")
        data = self.request_json(f"https://api.github.com/repos/{encoded}/git/trees/{urllib.parse.quote(ref)}?recursive=1")
        return list(data.get("tree") or []) if isinstance(data, dict) else []

    def stats(self) -> dict[str, Any]:
        return {
            "outbound_request_count": self.outbound_request_count,
            "cache_hit_count": self.cache_hit_count,
            "request_retry_count": self.request_retry_count,
            "total_backoff_seconds": self.total_backoff_seconds,
            "operational_failures": dict(self.operational_failures),
            "stop_reason": self.stop_reason,
            "stop_snapshot": self.stop_snapshot,
        }
