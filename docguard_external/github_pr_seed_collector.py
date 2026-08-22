from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from docguard_external.github_pr_dataset_builder import (
    GitHubApiError,
    is_code_path,
    is_docs_path,
    is_test_or_fixture_path,
    unique_preserve_order,
)


class GitHubSeedCollectorClient:
    def __init__(self, token: str | None = None, timeout_seconds: int = 30) -> None:
        self.token = token
        self.timeout_seconds = timeout_seconds

    def _request_json(self, url: str) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "DocGuard-Real-PR-Seed-Collector",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(url, headers=headers, method="GET")

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8", errors="replace")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GitHubApiError(f"HTTP {exc.code} from {url}: {body[:1000]}") from exc
        except Exception as exc:
            raise GitHubApiError(f"Failed GitHub request {url}: {exc}") from exc

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
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seeds: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []

    for repo_record in repos:
        repo = repo_record["repo"]
        language_hint = repo_record.get("language_hint") or ""
        kept_for_repo = 0

        for page in range(1, max_pages_per_repo + 1):
            if target_total is not None and len(seeds) >= target_total:
                return seeds, rejects

            try:
                pulls = client.get_closed_pulls_page(repo, page=page, per_page=100)
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
                if target_total is not None and len(seeds) >= target_total:
                    return seeds, rejects

                if kept_for_repo >= max_prs_per_repo:
                    break

                pr_number = int(pull.get("number") or 0)
                if pr_number <= 0:
                    continue

                merged_at = pull.get("merged_at")
                if not merged_at:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": pull.get("html_url"),
                            "reject_reason": "not_merged",
                        }
                    )
                    continue

                try:
                    files = client.get_pull_files(repo, pr_number)
                except Exception as exc:
                    rejects.append(
                        {
                            "repository": repo,
                            "pr_number": pr_number,
                            "source_url": pull.get("html_url"),
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
                            "source_url": pull.get("html_url"),
                            "reject_reason": reason,
                            "collector_bucket": classification["bucket"],
                            "collector_evidence": classification,
                        }
                    )
                    continue

                seeds.append(
                    {
                        "url": pull.get("html_url") or f"https://github.com/{repo}/pull/{pr_number}",
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
                kept_for_repo += 1

                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)

            if kept_for_repo >= max_prs_per_repo:
                break

    return seeds, rejects


def count_values(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key)) for row in rows))


def write_report(path: Path, *, repos: list[dict[str, Any]], seeds: list[dict[str, Any]], rejects: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    bucket_counts = count_values(seeds, "collector_bucket")
    language_counts = count_values(seeds, "language_hint")
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
        f"- Collector bucket counts: `{bucket_counts}`",
        f"- Language hint counts: `{language_counts}`",
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
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()

    repo_path = Path(args.repos)
    output_path = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output_path.with_suffix(".rejects.jsonl")
    report_path = Path(args.report)

    repos = load_repo_records(repo_path)
    token = os.getenv(args.github_token_env) or None
    client = GitHubSeedCollectorClient(token=token, timeout_seconds=args.timeout_seconds)

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
    )

    write_jsonl(output_path, seeds)
    write_jsonl(rejects_path, rejects)
    write_report(report_path, repos=repos, seeds=seeds, rejects=rejects)

    result = {
        "status": "ok",
        "repos": str(repo_path),
        "output": str(output_path),
        "rejects": str(rejects_path),
        "report": str(report_path),
        "repositories_scanned": len(repos),
        "accepted_seeds": len(seeds),
        "rejected_or_skipped": len(rejects),
        "collector_bucket_counts": count_values(seeds, "collector_bucket"),
        "language_hint_counts": count_values(seeds, "language_hint"),
        "reject_reason_counts": count_values(rejects, "reject_reason"),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())