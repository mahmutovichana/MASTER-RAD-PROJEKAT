from __future__ import annotations

import argparse
import json
import os
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from docguard_external.github_pr_dataset_builder import (
    GitHubApiError,
    is_code_path,
    is_docs_path,
    is_test_or_fixture_path,
    unique_preserve_order,
)

from docguard_external.github_api_cache import GitHubApiCache


class GlobalAcquisitionStop(Exception):
    def __init__(self, stop_reason: str, error: "GitHubRequestError | None" = None) -> None:
        super().__init__(stop_reason)
        self.stop_reason = stop_reason
        self.error = error


class GitHubRequestError(Exception):
    def __init__(self, *, status_code: int | None, url: str, response_body: str, headers: Any | None = None, original_error: Exception | None = None) -> None:
        super().__init__(f"HTTP {status_code} from {url}: {response_body[:500]}" if status_code else f"GitHub request failed {url}: {response_body}")
        self.status_code = status_code
        self.url = url
        self.response_body = response_body
        self.original_error = original_error
        self.retry_after = _int_header(headers, "Retry-After")
        self.rate_limit_limit = _int_header(headers, "x-ratelimit-limit")
        self.rate_limit_remaining = _int_header(headers, "x-ratelimit-remaining")
        self.rate_limit_used = _int_header(headers, "x-ratelimit-used")
        self.rate_limit_reset = _int_header(headers, "x-ratelimit-reset")
        self.rate_limit_resource = _str_header(headers, "x-ratelimit-resource")
        body_lower = response_body.lower()
        self.is_authentication_failure = status_code == 401
        self.is_primary_rate_limit = status_code in {403, 429} and self.rate_limit_remaining == 0
        secondary_terms = ["secondary rate limit", "abuse detection", "abuse rate limit", "abuse rate limits"]
        self.is_secondary_rate_limit = status_code in {403, 429} and any(term in body_lower for term in secondary_terms) and self.rate_limit_remaining != 0
        self.is_transient = status_code in {500, 502, 503, 504} or status_code is None

    def snapshot(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "url": self.url,
            "retry_after": self.retry_after,
            "rate_limit_limit": self.rate_limit_limit,
            "rate_limit_remaining": self.rate_limit_remaining,
            "rate_limit_used": self.rate_limit_used,
            "rate_limit_reset": self.rate_limit_reset,
            "rate_limit_resource": self.rate_limit_resource,
            "is_primary_rate_limit": self.is_primary_rate_limit,
            "is_secondary_rate_limit": self.is_secondary_rate_limit,
            "is_authentication_failure": self.is_authentication_failure,
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


class GitHubSeedCollectorClient:
    def __init__(
        self,
        token: str | None = None,
        timeout_seconds: int = 30,
        cache: GitHubApiCache | None = None,
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
        self.api_failure_counts: Counter = Counter()
        self.stop_reason: str | None = None
        self.rate_limit_snapshot: dict[str, Any] = {}

    @property
    def authenticated(self) -> bool:
        return bool(self.token)

    def _sleep(self, seconds: float) -> None:
        if seconds > 0:
            self.total_backoff_seconds += seconds
            self.sleeper(seconds)

    def _pace_outbound_request(self) -> None:
        now = float(self.monotonic())
        if self.last_outbound_request_monotonic is not None:
            elapsed = now - self.last_outbound_request_monotonic
            wait = self.min_request_interval_seconds - elapsed
            if wait > 0:
                self.sleeper(wait)
                now = float(self.monotonic())
        self.last_outbound_request_monotonic = now

    def _request_json_uncached(self, url: str) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "DocGuard-Real-PR-Seed-Collector",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        transient_delays = [2, 4, 8]
        secondary_delays = [None, 120, 240]
        transient_attempt = 0
        secondary_attempt = 0
        while True:
            request = urllib.request.Request(url, headers=headers, method="GET")
            self._pace_outbound_request()
            self.outbound_request_count += 1
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    body = response.read().decode("utf-8", errors="replace")
                    return json.loads(body)
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                error = GitHubRequestError(status_code=exc.code, url=url, response_body=body, headers=exc.headers, original_error=exc)
                self.api_failure_counts[str(exc.code)] += 1
                if error.is_authentication_failure:
                    self.stop_reason = "authentication_failed"
                    self.rate_limit_snapshot = error.snapshot()
                    raise GlobalAcquisitionStop(self.stop_reason, error) from exc
                if error.is_primary_rate_limit:
                    self.stop_reason = "primary_rate_limit_exhausted"
                    self.rate_limit_snapshot = error.snapshot()
                    raise GlobalAcquisitionStop(self.stop_reason, error) from exc
                if error.is_secondary_rate_limit:
                    if secondary_attempt >= 3:
                        self.stop_reason = "secondary_rate_limit_exhausted"
                        self.rate_limit_snapshot = error.snapshot()
                        raise GlobalAcquisitionStop(self.stop_reason, error) from exc
                    delay = error.retry_after if secondary_attempt == 0 and error.retry_after is not None else (secondary_delays[secondary_attempt] or 60)
                    secondary_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(delay)
                    continue
                if error.is_transient and transient_attempt < 3:
                    delay = transient_delays[transient_attempt]
                    transient_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(delay)
                    continue
                raise error from exc
            except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
                error = GitHubRequestError(status_code=None, url=url, response_body=str(exc), headers=None, original_error=exc)
                self.api_failure_counts["network_or_timeout"] += 1
                if transient_attempt < 3:
                    delay = transient_delays[transient_attempt]
                    transient_attempt += 1
                    self.request_retry_count += 1
                    self._sleep(delay)
                    continue
                raise error from exc

    def _request_json(self, url: str) -> Any:
        accept = "application/vnd.github+json"

        if self.cache is not None:
            cached = self.cache.get_json(url, accept=accept)
            if cached is not None:
                self.cache_hit_count += 1
                return cached

        data = self._request_json_uncached(url)

        if self.cache is not None:
            self.cache.set_json(url, data, accept=accept)

        return data

    def get_closed_pulls_page(self, repo: str, *, page: int, per_page: int = 100) -> list[dict[str, Any]]:
        encoded_repo = urllib.parse.quote(repo, safe="/")
        url = (
            f"https://api.github.com/repos/{encoded_repo}/pulls"
            f"?state=closed&sort=updated&direction=desc&per_page={per_page}&page={page}"
        )
        data = self._request_json(url)
        if not isinstance(data, list):
            raise GitHubApiError(f"Unexpected closed PR payload for {repo}")
        return [item for item in data if isinstance(item, dict)]

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page = 1

        while True:
            encoded_repo = urllib.parse.quote(repo, safe="/")
            url = (
                f"https://api.github.com/repos/{encoded_repo}/pulls/{pr_number}/files"
                f"?per_page=100&page={page}"
            )
            data = self._request_json(url)
            if not isinstance(data, list):
                raise GitHubApiError(f"Unexpected PR files payload for {repo}#{pr_number}")

            files.extend(item for item in data if isinstance(item, dict))

            if len(data) < 100:
                break

            page += 1
            if page > 10:
                break

        return files


def load_repo_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                try:
                    raw = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
                if not isinstance(raw, dict):
                    raise ValueError(f"Repo seed line must be JSON object at {path}:{line_number}")
                repo = str(raw.get("repo") or raw.get("repository") or "").strip()
                if not repo:
                    raise ValueError(f"Missing repo/repository at {path}:{line_number}")
                records.append(
                    {
                        "repo": repo,
                        "language_hint": str(raw.get("language_hint") or raw.get("language") or "").strip(),
                        "notes": str(raw.get("notes") or "").strip(),
                    }
                )
        return records

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            parts = [part.strip() for part in stripped.split(",")]
            repo = parts[0]
            language_hint = parts[1] if len(parts) > 1 else ""

            if "/" not in repo:
                raise ValueError(f"Invalid repo at {path}:{line_number}: {repo}")

            records.append(
                {
                    "repo": repo,
                    "language_hint": language_hint,
                    "notes": "",
                }
            )

    return records


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def parse_minimum_language_counts(values: list[str]) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid --minimum-language-count value: {value}. Expected language=count.")
        language, count_text = value.split("=", 1)
        language_key = language.strip().lower()
        count = int(count_text)
        if not language_key or count < 0:
            raise ValueError(f"Invalid --minimum-language-count value: {value}")
        parsed[language_key] = count
    return parsed


def language_key(repo_record: dict[str, Any]) -> str:
    return str(repo_record.get("language_hint") or "unknown").strip().lower() or "unknown"


def language_counts(rows: list[dict[str, Any]]) -> Counter:
    return Counter(str(row.get("language_hint") or "unknown").strip().lower() or "unknown" for row in rows)


def seed_pr_key(row: dict[str, Any]) -> tuple[str, int] | None:
    repo = str(row.get("repo") or row.get("repository") or "").strip().lower()
    pr_number = row.get("pr_number") or row.get("pull_request") or row.get("pr")
    if not repo and (row.get("url") or row.get("source_url")):
        parsed = urllib.parse.urlparse(str(row.get("url") or row.get("source_url")))
        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) >= 4 and parts[2] == "pull":
            repo = f"{parts[0]}/{parts[1]}".lower()
            pr_number = parts[3]
    if not repo or pr_number is None:
        return None
    try:
        return repo, int(pr_number)
    except (TypeError, ValueError):
        return None


def seed_source_url(row: dict[str, Any]) -> str:
    return str(row.get("url") or row.get("source_url") or "").strip().lower()


def load_excluded_seed_identity(paths: list[Path]) -> tuple[set[tuple[str, int]], set[str]]:
    keys: set[tuple[str, int]] = set()
    urls: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                key = seed_pr_key(row)
                if key:
                    keys.add(key)
                url = seed_source_url(row)
                if url:
                    urls.add(url)
    return keys, urls


def acquisition_complete(seeds: list[dict[str, Any]], target_total: int | None, minimum_language_counts: dict[str, int]) -> bool:
    if target_total is None and not minimum_language_counts:
        return False
    if target_total is not None and len(seeds) < target_total:
        return False
    counts = language_counts(seeds)
    return all(counts.get(language, 0) >= minimum for language, minimum in minimum_language_counts.items())


def acquisition_summary(
    *,
    seeds: list[dict[str, Any]],
    repos: list[dict[str, Any]],
    target_total: int | None,
    minimum_language_counts: dict[str, int],
    stop_reason: str | None = None,
) -> dict[str, Any]:
    observed_language_counts = dict(language_counts(seeds))
    minimum_deficits = {
        language: max(0, requested - int(observed_language_counts.get(language, 0)))
        for language, requested in minimum_language_counts.items()
    }
    target_observed = len(seeds)
    target_deficit = max(0, (target_total or 0) - target_observed)
    complete = acquisition_complete(seeds, target_total, minimum_language_counts)
    repository_universe_exhausted = not complete and stop_reason is None
    return {
        "acquisition_complete": complete,
        "target_total_requested": target_total,
        "target_total_observed": target_observed,
        "target_total_deficit": target_deficit,
        "minimum_language_counts_requested": minimum_language_counts,
        "minimum_language_counts_observed": observed_language_counts,
        "minimum_language_deficits": minimum_deficits,
        "repository_universe_exhausted": repository_universe_exhausted,
        "requirements_satisfied": complete and stop_reason is None,
        "stop_reason": stop_reason,
        "status": "complete" if complete else "partial",
        "repositories_scanned": len(repos),
    }


def acquisition_exit_code(status: str, allow_partial: bool) -> int:
    if status == "partial" and not allow_partial:
        return 2
    return 0


def rate_limit_reset_utc(snapshot: dict[str, Any]) -> str | None:
    reset = snapshot.get("rate_limit_reset")
    if reset is None:
        return None
    try:
        return datetime.fromtimestamp(int(reset), UTC).replace(microsecond=0).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def language_aware_repo_order(repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for repo in repos:
        groups.setdefault(language_key(repo), []).append(repo)
    ordered: list[dict[str, Any]] = []
    languages = sorted(groups)
    max_len = max((len(group) for group in groups.values()), default=0)
    for index in range(max_len):
        for language in languages:
            if index < len(groups[language]):
                ordered.append(groups[language][index])
    return ordered


def classify_pr_files(files: list[dict[str, Any]]) -> dict[str, Any]:
    changed_files = unique_preserve_order([str(item.get("filename") or "") for item in files])
    code_files = unique_preserve_order([path for path in changed_files if is_code_path(path)])
    docs_files = unique_preserve_order([path for path in changed_files if is_docs_path(path)])

    test_or_fixture_count = sum(1 for path in code_files if is_test_or_fixture_path(path))
    all_code_files_tests_or_fixtures = bool(code_files) and test_or_fixture_count == len(code_files)

    if code_files and docs_files:
        bucket = "code_and_docs"
    elif code_files and all_code_files_tests_or_fixtures:
        bucket = "code_only_tests_or_fixtures"
    elif code_files and not docs_files:
        bucket = "code_only"
    elif docs_files and not code_files:
        bucket = "docs_only"
    else:
        bucket = "other_or_binary_only"

    additions = sum(int(item.get("additions") or 0) for item in files)
    deletions = sum(int(item.get("deletions") or 0) for item in files)

    return {
        "bucket": bucket,
        "changed_files": changed_files,
        "code_changed_files": code_files,
        "docs_changed_files": docs_files,
        "total_changed_file_count": len(changed_files),
        "code_file_count": len(code_files),
        "docs_file_count": len(docs_files),
        "test_or_fixture_code_file_count": test_or_fixture_count,
        "all_code_files_tests_or_fixtures": all_code_files_tests_or_fixtures,
        "additions": additions,
        "deletions": deletions,
    }


def should_keep_seed(
    *,
    classification: dict[str, Any],
    include_docs_only: bool,
    include_other: bool,
    max_changed_files: int,
    max_total_patch_lines: int,
) -> tuple[bool, str]:
    bucket = str(classification.get("bucket") or "")
    total_changed = int(classification.get("total_changed_file_count") or 0)
    additions = int(classification.get("additions") or 0)
    deletions = int(classification.get("deletions") or 0)
    total_patch_lines = additions + deletions

    if total_changed > max_changed_files:
        return False, "too_many_changed_files"

    if total_patch_lines > max_total_patch_lines:
        return False, "too_large_patch"

    if bucket in {"code_and_docs", "code_only", "code_only_tests_or_fixtures"}:
        return True, "accepted"

    if bucket == "docs_only":
        return include_docs_only, "docs_only_excluded" if not include_docs_only else "accepted"

    return include_other, "other_or_binary_only_excluded" if not include_other else "accepted"


def collect_seed_records(
    *,
    repos: list[dict[str, Any]],
    client: Any,
    max_pages_per_repo: int,
    max_prs_per_repo: int,
    target_total: int | None,
    include_docs_only: bool,
    include_other: bool,
    max_changed_files: int,
    max_total_patch_lines: int,
    sleep_seconds: float,
    minimum_language_counts: dict[str, int] | None = None,
    excluded_pr_keys: set[tuple[str, int]] | None = None,
    excluded_source_urls: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seeds: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []
    minimum_language_counts = minimum_language_counts or {}
    excluded_pr_keys = excluded_pr_keys or set()
    excluded_source_urls = excluded_source_urls or set()
    seen_pr_keys: set[tuple[str, int]] = set()
    seen_source_urls: set[str] = set()
    scan_repos = language_aware_repo_order(repos) if minimum_language_counts else repos

    for repo_record in scan_repos:
        repo = repo_record["repo"]
        language_hint = repo_record.get("language_hint") or ""
        kept_for_repo = 0

        for page in range(1, max_pages_per_repo + 1):
            if acquisition_complete(seeds, target_total, minimum_language_counts):
                return seeds, rejects

            try:
                pulls = client.get_closed_pulls_page(repo, page=page, per_page=100)
            except GlobalAcquisitionStop:
                return seeds, rejects
            except Exception as exc:
                rejects.append(
                    {
                        "repository": repo,
                        "reject_reason": "fetch_closed_pulls_failed",
                        "error": str(exc),
                    }
                )
                break

            if not pulls:
                break

            for pull in pulls:
                if acquisition_complete(seeds, target_total, minimum_language_counts):
                    return seeds, rejects

                if kept_for_repo >= max_prs_per_repo:
                    break

                pr_number = int(pull.get("number") or 0)
                if pr_number <= 0:
                    continue
                source_url = str(pull.get("html_url") or f"https://github.com/{repo}/pull/{pr_number}")
                pr_key = (repo.lower(), pr_number)
                normalized_url = source_url.lower()
                if pr_key in excluded_pr_keys or normalized_url in excluded_source_urls or pr_key in seen_pr_keys or normalized_url in seen_source_urls:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": source_url,
                            "reject_reason": "already_collected",
                        }
                    )
                    continue

                merged_at = pull.get("merged_at")
                if not merged_at:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": source_url,
                            "reject_reason": "not_merged",
                        }
                    )
                    continue

                try:
                    files = client.get_pull_files(repo, pr_number)
                except GlobalAcquisitionStop:
                    return seeds, rejects
                except Exception as exc:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": source_url,
                            "reject_reason": "fetch_pr_files_failed",
                            "error": str(exc),
                        }
                    )
                    continue

                classification = classify_pr_files(files)
                keep, reason = should_keep_seed(
                    classification=classification,
                    include_docs_only=include_docs_only,
                    include_other=include_other,
                    max_changed_files=max_changed_files,
                    max_total_patch_lines=max_total_patch_lines,
                )

                if not keep:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": source_url,
                            "reject_reason": reason,
                            "collector_bucket": classification["bucket"],
                            "collector_evidence": classification,
                        }
                    )
                    continue

                seeds.append(
                    {
                        "url": source_url,
                        "repo": repo,
                        "pr_number": pr_number,
                        "language_hint": language_hint,
                        "notes": "Collected by neutral repo-based merged-PR sampling; gold label not assigned.",
                        "collector_bucket": classification["bucket"],
                        "collector_evidence": classification,
                        "pr_title": pull.get("title") or "",
                        "merged_at": merged_at,
                    }
                )
                seen_pr_keys.add(pr_key)
                seen_source_urls.add(normalized_url)
                kept_for_repo += 1

                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)

            if kept_for_repo >= max_prs_per_repo:
                break

    return seeds, rejects


def count_values(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key)) for row in rows))


def write_report(path: Path, *, repos: list[dict[str, Any]], seeds: list[dict[str, Any]], rejects: list[dict[str, Any]], summary: dict[str, Any] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    bucket_counts = count_values(seeds, "collector_bucket")
    language_counts = count_values(seeds, "language_hint")
    repo_counts_per_language = {
        language: len({str(row.get("repo") or "") for row in seeds if str(row.get("language_hint") or "") == language})
        for language in language_counts
    }
    bucket_counts_per_language: dict[str, dict[str, int]] = {}
    for language in language_counts:
        bucket_counts_per_language[language] = dict(Counter(str(row.get("collector_bucket") or "") for row in seeds if str(row.get("language_hint") or "") == language))
    reject_counts = count_values(rejects, "reject_reason")

    lines: list[str] = [
        "# DocGuard Real PR Seed Collector Report",
        "",
        "This report summarizes neutral repo-based sampling of merged public GitHub PRs.",
        "",
        "The collector does not assign gold labels and does not decide whether documentation should be updated.",
        "It only creates seed PR URLs for the later candidate builder and manual validation workflow.",
        "",
        f"- Repositories scanned: `{len(repos)}`",
        f"- Seeds accepted: `{len(seeds)}`",
        f"- Rejected/skipped PRs: `{len(rejects)}`",
        f"- Acquisition status: `{(summary or {}).get('status', 'not_computed')}`",
        f"- Requirements satisfied: `{(summary or {}).get('requirements_satisfied', False)}`",
        f"- Target observed/requested: `{(summary or {}).get('target_total_observed', len(seeds))}` / `{(summary or {}).get('target_total_requested')}`",
        f"- Target deficit: `{(summary or {}).get('target_total_deficit', 0)}`",
        f"- Minimum language deficits: `{(summary or {}).get('minimum_language_deficits', {})}`",
        f"- Collector bucket counts: `{bucket_counts}`",
        f"- Language hint counts: `{language_counts}`",
        f"- Repository counts per language: `{repo_counts_per_language}`",
        f"- Candidate bucket counts per language: `{bucket_counts_per_language}`",
        f"- Reject reason counts: `{reject_counts}`",
        "",
        "## Methodological Boundary",
        "",
        "- This is real public GitHub PR sampling.",
        "- No synthetic examples are generated.",
        "- No final labels are assigned here.",
        "- `collector_bucket` is audit metadata for balancing and review planning, not a model label.",
        "- Final evaluation must use only the safe fields produced later by the candidate builder.",
        "",
        "## Accepted Seeds",
        "",
        "| PR | Repository | Bucket | Language hint | Title |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in seeds:
        title = str(row.get("pr_title") or "").replace("|", "\\|").replace("\n", " ")
        if len(title) > 140:
            title = title[:137] + "..."

        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("url") or ""),
                    f"`{row.get('repo')}`",
                    f"`{row.get('collector_bucket')}`",
                    f"`{row.get('language_hint')}`",
                    title,
                ]
            )
            + " |"
        )

    if rejects:
        lines.extend(
            [
                "",
                "## Reject Summary Sample",
                "",
                "| Repository | PR | Reason | Bucket |",
                "| --- | ---: | --- | --- |",
            ]
        )
        for row in rejects[:200]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{row.get('repository')}`",
                        f"`{row.get('pr_number')}`",
                        f"`{row.get('reject_reason')}`",
                        f"`{row.get('collector_bucket')}`",
                    ]
                )
                + " |"
            )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect real public GitHub PR seed URLs for DocGuard dataset building.")
    parser.add_argument("--repos", required=True, help="TXT or JSONL repository list.")
    parser.add_argument("--output", required=True, help="Output JSONL seed file.")
    parser.add_argument("--rejects", default=None, help="Optional JSONL reject/skipped file.")
    parser.add_argument("--report", required=True, help="Output Markdown report.")
    parser.add_argument("--target-total", type=int, default=None)
    parser.add_argument("--max-pages-per-repo", type=int, default=2)
    parser.add_argument("--max-prs-per-repo", type=int, default=20)
    parser.add_argument("--max-changed-files", type=int, default=40)
    parser.add_argument("--max-total-patch-lines", type=int, default=3000)
    parser.add_argument("--include-docs-only", action="store_true")
    parser.add_argument("--include-other", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=0.0, help="Deprecated for Final V2; sleeps after accepted seeds only. Use --min-request-interval-seconds for request-level pacing.")
    parser.add_argument("--minimum-language-count", action="append", default=[], help="Require at least language=count accepted seeds, e.g. python=6000. May be repeated.")
    parser.add_argument("--exclude-seed-file", action="append", default=[], help="Existing seed JSONL whose repo+PR/source URLs should be skipped. May be repeated.")
    parser.add_argument("--allow-partial", action="store_true", help="Return exit code 0 for partial acquisition while keeping JSON status='partial'.")
    parser.add_argument("--require-authenticated", action="store_true", help="Fail before the first GitHub API request if the configured token environment variable is missing.")
    parser.add_argument("--min-request-interval-seconds", type=float, default=0.25, help="Minimum spacing between uncached outbound GitHub API requests. Final V2 default is 0.25.")
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument(
        "--cache-dir",
        default="data/external/project_case_study/cache/github_api",
        help="Filesystem cache directory for GitHub API JSON responses.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable GitHub API response cache.")
    args = parser.parse_args()

    repo_path = Path(args.repos)
    output_path = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output_path.with_suffix(".rejects.jsonl")
    report_path = Path(args.report)

    repos = load_repo_records(repo_path)
    minimum_language_counts = parse_minimum_language_counts(args.minimum_language_count)
    excluded_pr_keys, excluded_source_urls = load_excluded_seed_identity([Path(path) for path in args.exclude_seed_file])
    token = os.getenv(args.github_token_env) or None
    if args.require_authenticated and not token:
        print(json.dumps({"status": "partial", "requirements_satisfied": False, "stop_reason": "missing_required_github_token", "authenticated": False, "github_token_env_name": args.github_token_env}, indent=2))
        return 2
    cache = None if args.no_cache else GitHubApiCache(Path(args.cache_dir))
    client = GitHubSeedCollectorClient(token=token, timeout_seconds=args.timeout_seconds, cache=cache, min_request_interval_seconds=args.min_request_interval_seconds)

    seeds, rejects = collect_seed_records(
        repos=repos,
        client=client,
        max_pages_per_repo=args.max_pages_per_repo,
        max_prs_per_repo=args.max_prs_per_repo,
        target_total=args.target_total,
        include_docs_only=args.include_docs_only,
        include_other=args.include_other,
        max_changed_files=args.max_changed_files,
        max_total_patch_lines=args.max_total_patch_lines,
        sleep_seconds=args.sleep_seconds,
        minimum_language_counts=minimum_language_counts,
        excluded_pr_keys=excluded_pr_keys,
        excluded_source_urls=excluded_source_urls,
    )
    summary = acquisition_summary(
        seeds=seeds,
        repos=repos,
        target_total=args.target_total,
        minimum_language_counts=minimum_language_counts,
        stop_reason=client.stop_reason,
    )

    write_jsonl(output_path, seeds)
    write_jsonl(rejects_path, rejects)
    write_report(report_path, repos=repos, seeds=seeds, rejects=rejects, summary=summary)

    result = {
        **summary,
        "repos": str(repo_path),
        "output": str(output_path),
        "rejects": str(rejects_path),
        "report": str(report_path),
        "accepted_seeds": len(seeds),
        "rejected_or_skipped": len(rejects),
        "collector_bucket_counts": count_values(seeds, "collector_bucket"),
        "language_hint_counts": count_values(seeds, "language_hint"),
        "minimum_language_counts": minimum_language_counts,
        "excluded_seed_files": args.exclude_seed_file,
        "excluded_pr_keys": len(excluded_pr_keys),
        "excluded_source_urls": len(excluded_source_urls),
        "repo_order_mode": "language_aware_round_robin" if minimum_language_counts else "sequential",
        "reject_reason_counts": count_values(rejects, "reject_reason"),
        "cache_dir": None if cache is None else str(cache.cache_dir),
        "cache_stats": None if cache is None else cache.stats(),
        "authenticated": client.authenticated,
        "github_token_env_name": args.github_token_env,
        "outbound_request_count": client.outbound_request_count,
        "cache_hit_count": client.cache_hit_count,
        "request_retry_count": client.request_retry_count,
        "total_backoff_seconds": client.total_backoff_seconds,
        "configured_min_request_interval_seconds": args.min_request_interval_seconds,
        "api_failure_counts": dict(client.api_failure_counts),
        "rate_limit_snapshot": client.rate_limit_snapshot,
        "rate_limit_reset_epoch": client.rate_limit_snapshot.get("rate_limit_reset"),
        "rate_limit_reset_utc": rate_limit_reset_utc(client.rate_limit_snapshot),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return acquisition_exit_code(str(result["status"]), args.allow_partial)


if __name__ == "__main__":
    raise SystemExit(main())
