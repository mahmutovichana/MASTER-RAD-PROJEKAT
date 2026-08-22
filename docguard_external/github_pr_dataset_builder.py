from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_MODEL_INPUT_FIELDS = [
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]

AUDIT_ONLY_FIELDS = [
    "source_url",
    "repository",
    "pr_number",
    "pr_title",
    "pr_state",
    "merged_at",
    "base_sha",
    "head_sha",
    "changed_files",
    "docs_changed_files",
    "docs_diff_excerpt",
    "docs_after_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
    "label_confidence",
    "manual_label_notes",
    "candidate_evidence",
]

DOC_EXTENSIONS = {
    ".md",
    ".mdx",
    ".rst",
    ".adoc",
    ".txt",
}

CODE_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".java",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".kt",
    ".kts",
    ".swift",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".scala",
    ".sql",
    ".graphql",
    ".proto",
    ".prisma",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".env",
    ".dockerfile",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".mp4",
    ".mov",
    ".mp3",
    ".wav",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
}

DEFAULT_DOC_PATHS = [
    "README.md",
    "README.rst",
    "README.adoc",
    "docs/README.md",
    "docs/index.md",
    "docs/getting-started.md",
    "docs/configuration.md",
    "docs/api.md",
    "CHANGELOG.md",
]


@dataclass(frozen=True)
class BuildConfig:
    max_code_diff_chars: int = 9000
    max_docs_chars: int = 5000
    max_docs_files: int = 3
    sleep_seconds: float = 0.0


class GitHubApiError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str | None = None, timeout_seconds: int = 30) -> None:
        self.token = token
        self.timeout_seconds = timeout_seconds

    def _request_json(self, url: str, *, accept: str = "application/vnd.github+json") -> Any:
        headers = {
            "Accept": accept,
            "User-Agent": "DocGuard-Real-PR-Dataset-Builder",
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

    def get_pull(self, repo: str, pr_number: int) -> dict[str, Any]:
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        data = self._request_json(url)
        if not isinstance(data, dict):
            raise GitHubApiError(f"Unexpected PR payload for {repo}#{pr_number}")
        return data

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page = 1

        while True:
            url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}"
            data = self._request_json(url)

            if not isinstance(data, list):
                raise GitHubApiError(f"Unexpected PR files payload for {repo}#{pr_number}")

            files.extend(item for item in data if isinstance(item, dict))

            if len(data) < 100:
                break

            page += 1
            if page > 20:
                raise GitHubApiError(f"Too many changed-file pages for {repo}#{pr_number}")

        return files

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        encoded_path = urllib.parse.quote(path, safe="/")
        encoded_ref = urllib.parse.quote(ref, safe="")
        url = f"https://api.github.com/repos/{repo}/contents/{encoded_path}?ref={encoded_ref}"

        try:
            data = self._request_json(url)
        except GitHubApiError as exc:
            message = str(exc)
            if "HTTP 404" in message:
                return None
            raise

        if not isinstance(data, dict):
            return None

        if data.get("type") != "file":
            return None

        encoding = data.get("encoding")
        content = data.get("content")

        if encoding != "base64" or not isinstance(content, str):
            return None

        try:
            raw = base64.b64decode(content)
        except Exception:
            return None

        if b"\x00" in raw[:1000]:
            return None

        return raw.decode("utf-8", errors="replace")


def parse_pr_url(url: str) -> tuple[str, int]:
    pattern = r"https?://github\.com/([^/\s]+/[^/\s]+)/pull/(\d+)"
    match = re.search(pattern, url.strip())
    if not match:
        raise ValueError(f"Could not parse GitHub PR URL: {url}")
    return match.group(1), int(match.group(2))


def normalize_seed_record(seed: dict[str, Any], *, index: int) -> dict[str, Any]:
    url = str(seed.get("url") or seed.get("source_url") or "").strip()
    repo = str(seed.get("repo") or seed.get("repository") or "").strip()
    pr_value = seed.get("pr_number") or seed.get("pull_request") or seed.get("pr")

    if url:
        parsed_repo, parsed_pr = parse_pr_url(url)
        repo = repo or parsed_repo
        pr_number = int(pr_value or parsed_pr)
    else:
        if not repo or pr_value is None:
            raise ValueError(f"Seed record #{index} must contain either url/source_url or repo + pr_number.")
        pr_number = int(pr_value)
        url = f"https://github.com/{repo}/pull/{pr_number}"

    return {
        "seed_index": index,
        "url": url,
        "repo": repo,
        "pr_number": pr_number,
        "language_hint": str(seed.get("language_hint") or seed.get("language") or "").strip(),
        "notes": str(seed.get("notes") or "").strip(),
    }


def load_seed_records(path: Path) -> list[dict[str, Any]]:
    seeds: list[dict[str, Any]] = []

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
                    raise ValueError(f"Seed line must be a JSON object at {path}:{line_number}")
                seeds.append(normalize_seed_record(raw, index=len(seeds) + 1))
        return seeds

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            seeds.append(normalize_seed_record({"url": stripped}, index=len(seeds) + 1))

    return seeds


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _suffix(path: str) -> str:
    lower = path.lower()
    if lower.endswith("dockerfile"):
        return ".dockerfile"
    return Path(lower).suffix


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def is_binary_path(path: str) -> bool:
    return _suffix(path) in BINARY_EXTENSIONS


def is_docs_path(path: str) -> bool:
    normalized = normalize_path(path).lower()
    basename = normalized.rsplit("/", 1)[-1]

    if is_binary_path(normalized):
        return False

    if normalized.startswith("docs/"):
        return True

    if basename.startswith("readme."):
        return True

    if basename in {"changelog.md", "changes.md", "history.md", "contributing.md", "usage.md"}:
        return True

    if _suffix(normalized) in {".md", ".mdx", ".rst", ".adoc"}:
        return True

    return False


def is_code_path(path: str) -> bool:
    normalized = normalize_path(path).lower()

    if is_binary_path(normalized):
        return False

    if is_docs_path(normalized):
        return False

    return _suffix(normalized) in CODE_EXTENSIONS


def is_test_or_fixture_path(path: str) -> bool:
    normalized = normalize_path(path).lower()
    parts = re.split(r"[/_.\-]+", normalized)

    if any(part in {"test", "tests", "testing", "__tests__", "spec", "mocks", "mock", "fixtures", "fixture", "stories"} for part in parts):
        return True

    return normalized.endswith(
        (
            ".test.ts",
            ".test.tsx",
            ".spec.ts",
            ".spec.tsx",
            ".test.js",
            ".spec.js",
            "_test.py",
            "test.py",
            ".stories.tsx",
            ".stories.ts",
        )
    )


def infer_language_from_files(files: list[str], language_hint: str = "") -> str:
    if language_hint:
        return language_hint

    counts: dict[str, int] = {}

    mapping = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".java": "java",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".kt": "kotlin",
        ".kts": "kotlin",
        ".swift": "swift",
        ".sql": "sql",
    }

    for file_path in files:
        language = mapping.get(_suffix(file_path))
        if language:
            counts[language] = counts.get(language, 0) + 1

    if not counts:
        return "unknown"

    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]


def truncate_text(text: str, limit: int) -> str:
    if limit <= 0:
        return ""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def patch_for_file(file_record: dict[str, Any]) -> str:
    filename = str(file_record.get("filename") or "")
    patch = str(file_record.get("patch") or "")

    if not filename or not patch:
        return ""

    return f"diff --git a/{filename} b/{filename}\n--- a/{filename}\n+++ b/{filename}\n{patch}".strip()


def combine_file_patches(files: list[dict[str, Any]], *, limit: int) -> str:
    chunks: list[str] = []

    for item in files:
        patch = patch_for_file(item)
        if patch:
            chunks.append(patch)

    return truncate_text("\n\n".join(chunks), limit)


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        clean = normalize_path(value)
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)

    return result


def collect_docs_text(
    *,
    client: Any,
    repo: str,
    ref: str,
    preferred_paths: list[str],
    max_chars: int,
    max_files: int,
) -> str:
    selected_paths = unique_preserve_order(preferred_paths + DEFAULT_DOC_PATHS)
    chunks: list[str] = []
    remaining = max_chars

    for path in selected_paths:
        if remaining <= 0:
            break

        if not is_docs_path(path):
            continue

        try:
            text = client.get_file_text(repo, path, ref)
        except GitHubApiError:
            continue

        if not text:
            continue

        chunk_limit = max(400, remaining)
        chunk = truncate_text(text, chunk_limit)
        chunks.append(f"<!-- {path} @ {ref} -->\n{chunk}")
        remaining = max_chars - len("\n\n".join(chunks))

        if len(chunks) >= max_files:
            break

    return truncate_text("\n\n".join(chunks), max_chars)


def summarize_candidate_type(*, code_files: list[str], docs_files: list[str], code_diff: str) -> str:
    if code_files and docs_files:
        return "code_and_docs_changed_needs_manual_validation"

    if code_files and not docs_files:
        if all(is_test_or_fixture_path(path) for path in code_files):
            return "code_only_test_or_fixture_candidate_negative_review"
        return "code_only_needs_manual_validation"

    if docs_files and not code_files:
        return "docs_only_skip_or_review"

    if not code_diff.strip():
        return "no_textual_code_patch"

    return "uncertain_needs_manual_validation"


def build_candidate_case(
    *,
    seed: dict[str, Any],
    client: Any,
    case_id: str,
    config: BuildConfig,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    repo = seed["repo"]
    pr_number = int(seed["pr_number"])

    try:
        pull = client.get_pull(repo, pr_number)
        files = client.get_pull_files(repo, pr_number)
    except Exception as exc:
        reject = {
            "case_id": case_id,
            "source_url": seed["url"],
            "repository": repo,
            "pr_number": pr_number,
            "reject_reason": "github_fetch_failed",
            "error": str(exc),
        }
        return None, reject

    changed_files = unique_preserve_order([str(item.get("filename") or "") for item in files])
    code_file_records = [item for item in files if is_code_path(str(item.get("filename") or ""))]
    docs_file_records = [item for item in files if is_docs_path(str(item.get("filename") or ""))]

    code_changed_files = unique_preserve_order([str(item.get("filename") or "") for item in code_file_records])
    docs_changed_files = unique_preserve_order([str(item.get("filename") or "") for item in docs_file_records])

    code_diff_excerpt = combine_file_patches(code_file_records, limit=config.max_code_diff_chars)
    docs_diff_excerpt = combine_file_patches(docs_file_records, limit=config.max_code_diff_chars)

    if not code_changed_files:
        reject = {
            "case_id": case_id,
            "source_url": seed["url"],
            "repository": repo,
            "pr_number": pr_number,
            "reject_reason": "no_code_files_changed",
            "changed_files": changed_files,
        }
        return None, reject

    if not code_diff_excerpt.strip():
        reject = {
            "case_id": case_id,
            "source_url": seed["url"],
            "repository": repo,
            "pr_number": pr_number,
            "reject_reason": "missing_textual_code_patch",
            "code_changed_files": code_changed_files,
            "changed_files": changed_files,
        }
        return None, reject

    base = pull.get("base") or {}
    head = pull.get("head") or {}
    base_sha = str(base.get("sha") or "")
    head_sha = str(head.get("sha") or "")

    docs_before_excerpt = ""
    docs_after_excerpt = ""

    if base_sha:
        docs_before_excerpt = collect_docs_text(
            client=client,
            repo=repo,
            ref=base_sha,
            preferred_paths=docs_changed_files,
            max_chars=config.max_docs_chars,
            max_files=config.max_docs_files,
        )

    if head_sha and docs_changed_files:
        docs_after_excerpt = collect_docs_text(
            client=client,
            repo=repo,
            ref=head_sha,
            preferred_paths=docs_changed_files,
            max_chars=config.max_docs_chars,
            max_files=config.max_docs_files,
        )

    additions = sum(int(item.get("additions") or 0) for item in files)
    deletions = sum(int(item.get("deletions") or 0) for item in files)

    language = infer_language_from_files(code_changed_files, seed.get("language_hint") or "")
    candidate_type = summarize_candidate_type(
        code_files=code_changed_files,
        docs_files=docs_changed_files,
        code_diff=code_diff_excerpt,
    )

    case = {
        "case_id": case_id,
        "source_url": seed["url"],
        "repository": repo,
        "pr_number": pr_number,
        "pr_title": str(pull.get("title") or ""),
        "pr_state": str(pull.get("state") or ""),
        "merged_at": pull.get("merged_at"),
        "base_sha": base_sha,
        "head_sha": head_sha,
        "language": language,
        "code_changed_files": code_changed_files,
        "code_diff_excerpt": code_diff_excerpt,
        "docs_before_excerpt": docs_before_excerpt,

        # Audit-only metadata and future labeling fields.
        "changed_files": changed_files,
        "docs_changed_files": docs_changed_files,
        "docs_diff_excerpt": docs_diff_excerpt,
        "docs_after_excerpt": docs_after_excerpt,
        "gold_docs_update_required": None,
        "gold_doc_category": None,
        "gold_target_doc_file": None,
        "gold_target_section": None,
        "gold_patch_summary": None,
        "label_confidence": "needs_manual_review",
        "manual_label_notes": "",
        "candidate_evidence": {
            "builder_version": "github_pr_dataset_builder_v1",
            "candidate_type": candidate_type,
            "code_files_changed": bool(code_changed_files),
            "docs_files_changed": bool(docs_changed_files),
            "code_file_count": len(code_changed_files),
            "docs_file_count": len(docs_changed_files),
            "total_changed_file_count": len(changed_files),
            "test_or_fixture_code_file_count": sum(1 for path in code_changed_files if is_test_or_fixture_path(path)),
            "all_code_files_are_tests_or_fixtures": all(is_test_or_fixture_path(path) for path in code_changed_files),
            "additions": additions,
            "deletions": deletions,
            "has_docs_before_excerpt": bool(docs_before_excerpt.strip()),
            "has_docs_after_excerpt": bool(docs_after_excerpt.strip()),
        },
        "allowed_model_input_fields": ALLOWED_MODEL_INPUT_FIELDS,
        "audit_only_fields": AUDIT_ONLY_FIELDS,
    }

    return case, None


def build_dataset(
    *,
    seeds: list[dict[str, Any]],
    client: Any,
    config: BuildConfig,
    max_cases: int | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cases: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []

    for index, seed in enumerate(seeds, start=1):
        if max_cases is not None and len(cases) >= max_cases:
            break

        case_id = f"GH-CAND-{index:04d}"
        case, reject = build_candidate_case(
            seed=seed,
            client=client,
            case_id=case_id,
            config=config,
        )

        if case is not None:
            cases.append(case)

        if reject is not None:
            rejects.append(reject)

        if config.sleep_seconds > 0:
            time.sleep(config.sleep_seconds)

    return cases, rejects


def count_by_nested_key(rows: list[dict[str, Any]], key_path: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for row in rows:
        value: Any = row
        for key in key_path:
            if not isinstance(value, dict):
                value = None
                break
            value = value.get(key)

        label = str(value)
        counts[label] = counts.get(label, 0) + 1

    return dict(sorted(counts.items(), key=lambda item: item[0]))


def write_report(
    *,
    path: Path,
    cases: list[dict[str, Any]],
    rejects: list[dict[str, Any]],
    input_path: Path,
    output_path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# DocGuard Real GitHub PR Candidate Dataset Builder Report",
        "",
        "This report describes a real public GitHub PR candidate dataset created for later manual validation.",
        "The builder does not assign final gold labels and does not use synthetic data.",
        "",
        f"- Seed input: `{input_path}`",
        f"- Candidate output: `{output_path}`",
        f"- Accepted candidate records: `{len(cases)}`",
        f"- Rejected seed records: `{len(rejects)}`",
        "",
        "## Leakage Policy",
        "",
        "Allowed model input fields:",
        "",
    ]

    for field in ALLOWED_MODEL_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(["", "Audit-only fields:", ""])

    for field in AUDIT_ONLY_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "## Candidate Counts",
            "",
            f"- Candidate type counts: `{count_by_nested_key(cases, ['candidate_evidence', 'candidate_type'])}`",
            f"- Language counts: `{count_by_nested_key(cases, ['language'])}`",
            f"- Label confidence counts: `{count_by_nested_key(cases, ['label_confidence'])}`",
            "",
            "## Accepted Candidates",
            "",
            "| Case | Repository | PR | Language | Code files | Docs files | Candidate type | Title |",
            "| --- | --- | ---: | --- | ---: | ---: | --- | --- |",
        ]
    )

    for row in cases:
        evidence = row.get("candidate_evidence") or {}
        title = str(row.get("pr_title") or "").replace("|", "\\|").replace("\n", " ")
        if len(title) > 120:
            title = title[:117] + "..."

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('case_id')}`",
                    f"`{row.get('repository')}`",
                    f"`{row.get('pr_number')}`",
                    f"`{row.get('language')}`",
                    f"`{len(row.get('code_changed_files') or [])}`",
                    f"`{len(row.get('docs_changed_files') or [])}`",
                    f"`{evidence.get('candidate_type')}`",
                    title,
                ]
            )
            + " |"
        )

    if rejects:
        lines.extend(
            [
                "",
                "## Rejected Seeds",
                "",
                "| Case | Repository | PR | Reason |",
                "| --- | --- | ---: | --- |",
            ]
        )

        for row in rejects:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{row.get('case_id')}`",
                        f"`{row.get('repository')}`",
                        f"`{row.get('pr_number')}`",
                        f"`{row.get('reject_reason')}`",
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- This is a dataset construction step, not a model result.",
            "- Candidate labels are intentionally left as `needs_manual_review`.",
            "- Documentation-after text and documentation-file changes are stored only for audit/labeling.",
            "- Model-facing evaluation scripts must use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build real GitHub PR candidate records for DocGuard evaluation.")
    parser.add_argument("--input", required=True, help="JSONL seed file or TXT file with one GitHub PR URL per line.")
    parser.add_argument("--output", required=True, help="Output JSONL candidate file.")
    parser.add_argument("--rejects", default=None, help="Optional output JSONL for rejected seed records.")
    parser.add_argument("--report", required=True, help="Output Markdown report.")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--max-code-diff-chars", type=int, default=9000)
    parser.add_argument("--max-docs-chars", type=int, default=5000)
    parser.add_argument("--max-docs-files", type=int, default=3)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output_path.with_suffix(".rejects.jsonl")
    report_path = Path(args.report)

    token = os.getenv(args.github_token_env) or None

    seeds = load_seed_records(input_path)
    client = GitHubClient(token=token, timeout_seconds=args.timeout_seconds)
    config = BuildConfig(
        max_code_diff_chars=args.max_code_diff_chars,
        max_docs_chars=args.max_docs_chars,
        max_docs_files=args.max_docs_files,
        sleep_seconds=args.sleep_seconds,
    )

    cases, rejects = build_dataset(
        seeds=seeds,
        client=client,
        config=config,
        max_cases=args.max_cases,
    )

    write_jsonl(output_path, cases)
    write_jsonl(rejects_path, rejects)
    write_report(
        path=report_path,
        cases=cases,
        rejects=rejects,
        input_path=input_path,
        output_path=output_path,
    )

    result = {
        "status": "ok",
        "input": str(input_path),
        "output": str(output_path),
        "rejects": str(rejects_path),
        "report": str(report_path),
        "seed_records": len(seeds),
        "accepted_candidates": len(cases),
        "rejected_seeds": len(rejects),
        "candidate_type_counts": count_by_nested_key(cases, ["candidate_evidence", "candidate_type"]),
        "language_counts": count_by_nested_key(cases, ["language"]),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())