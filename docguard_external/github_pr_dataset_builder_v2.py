from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from docguard_external.github_client_v2 import GitHubClientV2, GlobalGitHubStop
from docguard_external.github_api_cache import GitHubApiCache
from docguard_external.github_pr_dataset_builder import (
    DEFAULT_DOC_PATHS,
    BuildConfig,
    combine_file_patches,
    infer_language_from_files,
    is_code_path,
    is_docs_path,
    is_test_or_fixture_path,
    load_seed_records,
    summarize_candidate_type,
    truncate_text,
    unique_preserve_order,
)


SAFE_MODEL_INPUT_FIELDS = ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"]
AUDIT_ONLY_FIELDS = [
    "source_url",
    "repository",
    "pr_number",
    "pr_title",
    "merged_at",
    "base_sha",
    "head_sha",
    "changed_files",
    "docs_changed_files",
    "docs_diff_excerpt",
    "docs_after_excerpt",
    "candidate_evidence",
    "docs_before_retrieval_policy",
    "docs_before_retrieved_files",
    "documentation_context_candidates",
    "classifier_model_input",
    "generator_context",
]
FORBIDDEN_GOLD_FIELDS = {
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_target_doc_file",
    "gold_target_section",
    "gold_patch_summary",
}
DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".adoc", ".txt"}
DOC_LOCATIONS = ("docs/", "doc/", "documentation/", "website/docs/", "website/content/", "guides/", "reference/")
DOC_PREFIXES = ("readme", "contributing", "changelog")


def stable_case_id(repository: str, pr_number: int) -> str:
    normalized = f"{repository.strip().lower()}#{int(pr_number)}"
    return "DGPR-" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def neutral_doc_paths(code_changed_files: list[str], max_files: int) -> list[str]:
    paths = list(DEFAULT_DOC_PATHS)
    lowered = " ".join(code_changed_files).lower()
    if "api" in lowered:
        paths.append("docs/api.md")
    if "config" in lowered or ".env" in lowered:
        paths.append("docs/configuration.md")
    if "model" in lowered or "schema" in lowered:
        paths.append("docs/models.md")
    if "setup" in lowered or "package" in lowered:
        paths.append("docs/developer-setup.md")
    return unique_preserve_order(paths)[: max(max_files * 3, max_files)]


def is_candidate_doc_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    suffix = Path(normalized).suffix
    name = Path(normalized).name.lower()
    return suffix in DOC_EXTENSIONS and (normalized.startswith(DOC_LOCATIONS) or any(name.startswith(prefix) for prefix in DOC_PREFIXES))


def discover_base_doc_paths(*, client: Any, repo: str, ref: str, code_changed_files: list[str], max_discovered_paths: int) -> tuple[list[str], dict[str, Any]]:
    paths: list[str] = []
    provenance = {"method": "base_sha_tree_documentation_discovery_v2", "tree_ref": ref, "used_docs_changed_files": False, "truncated": False}
    try:
        tree = client.get_tree_recursive(repo, ref)
    except AttributeError:
        return neutral_doc_paths(code_changed_files, max_discovered_paths), {"method": "fallback_neutral_known_paths_client_has_no_tree_api", "tree_ref": ref, "used_docs_changed_files": False, "truncated": False}
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = str(item.get("path") or "")
        if is_candidate_doc_path(path):
            paths.append(path)
        if len(paths) >= max_discovered_paths:
            provenance["truncated"] = True
            break
    neutral = neutral_doc_paths(code_changed_files, max_discovered_paths)
    return unique_preserve_order(neutral + paths)[:max_discovered_paths], provenance


def collect_docs_before_neutral(*, client: Any, repo: str, ref: str, code_changed_files: list[str], max_chars: int, max_files: int) -> tuple[str, list[str], str, list[dict[str, str]]]:
    max_discovered_paths = int(getattr(client, "max_discovered_documentation_paths", 80))
    selected_paths, discovery = discover_base_doc_paths(client=client, repo=repo, ref=ref, code_changed_files=code_changed_files, max_discovered_paths=max_discovered_paths)
    chunks: list[str] = []
    retrieved: list[str] = []
    candidates: list[dict[str, str]] = []
    remaining = max_chars
    for path in selected_paths:
        if remaining <= 0 or len(retrieved) >= max_files:
            break
        try:
            text = client.get_file_text(repo, path, ref)
        except Exception:
            continue
        if not text:
            continue
        chunk = truncate_text(text, max(400, remaining))
        chunks.append(f"<!-- {path} @ {ref} -->\n{chunk}")
        retrieved.append(path)
        candidates.append({"path": path, "excerpt": chunk, "source_ref": ref, "retrieval_provenance": {**discovery, "path": path, "truncated_excerpt": len(text) > len(chunk)}})
        remaining = max_chars - len("\n\n".join(chunks))
    policy = f"{discovery['method']}_plus_code_path_hints_no_docs_changed_files_no_docs_after"
    return truncate_text("\n\n".join(chunks), max_chars), retrieved, policy, candidates


def collect_docs_after_audit(*, client: Any, repo: str, ref: str, docs_changed_files: list[str], max_chars: int, max_files: int) -> str:
    chunks: list[str] = []
    remaining = max_chars
    for path in unique_preserve_order(docs_changed_files):
        if remaining <= 0 or len(chunks) >= max_files:
            break
        if not is_docs_path(path):
            continue
        try:
            text = client.get_file_text(repo, path, ref)
        except Exception:
            continue
        if not text:
            continue
        chunks.append(f"<!-- {path} @ {ref} -->\n{truncate_text(text, max(400, remaining))}")
        remaining = max_chars - len("\n\n".join(chunks))
    return truncate_text("\n\n".join(chunks), max_chars)


def build_candidate_case_v2(*, seed: dict[str, Any], client: Any, config: BuildConfig) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    repo = seed["repo"]
    pr_number = int(seed["pr_number"])
    case_id = stable_case_id(repo, pr_number)
    try:
        pull = client.get_pull(repo, pr_number)
        files = client.get_pull_files(repo, pr_number)
    except GlobalGitHubStop:
        raise
    except Exception as exc:
        return None, {"case_id": case_id, "source_url": seed["url"], "repository": repo, "pr_number": pr_number, "reject_reason": "github_fetch_failed", "error": str(exc)}

    changed_files = unique_preserve_order([str(item.get("filename") or "") for item in files])
    code_file_records = [item for item in files if is_code_path(str(item.get("filename") or ""))]
    docs_file_records = [item for item in files if is_docs_path(str(item.get("filename") or ""))]
    code_changed_files = unique_preserve_order([str(item.get("filename") or "") for item in code_file_records])
    docs_changed_files = unique_preserve_order([str(item.get("filename") or "") for item in docs_file_records])
    code_diff_excerpt = combine_file_patches(code_file_records, limit=config.max_code_diff_chars)
    docs_diff_excerpt = combine_file_patches(docs_file_records, limit=config.max_code_diff_chars)
    if not code_changed_files:
        return None, {"case_id": case_id, "source_url": seed["url"], "repository": repo, "pr_number": pr_number, "reject_reason": "no_code_files_changed"}
    if not code_diff_excerpt.strip():
        return None, {"case_id": case_id, "source_url": seed["url"], "repository": repo, "pr_number": pr_number, "reject_reason": "missing_textual_code_patch"}
    base = pull.get("base") or {}
    head = pull.get("head") or {}
    base_sha = str(base.get("sha") or "")
    head_sha = str(head.get("sha") or "")
    docs_before_excerpt, retrieved_files, retrieval_policy, documentation_context_candidates = ("", [], "base_sha_missing_no_docs_retrieved", [])
    if base_sha:
        docs_before_excerpt, retrieved_files, retrieval_policy, documentation_context_candidates = collect_docs_before_neutral(
            client=client,
            repo=repo,
            ref=base_sha,
            code_changed_files=code_changed_files,
            max_chars=config.max_docs_chars,
            max_files=config.max_docs_files,
        )
    docs_after_excerpt = collect_docs_after_audit(client=client, repo=repo, ref=head_sha, docs_changed_files=docs_changed_files, max_chars=config.max_docs_chars, max_files=config.max_docs_files) if head_sha and docs_changed_files else ""
    additions = sum(int(item.get("additions") or 0) for item in files)
    deletions = sum(int(item.get("deletions") or 0) for item in files)
    language = infer_language_from_files(code_changed_files, seed.get("language_hint") or "")
    case = {
        "case_id": case_id,
        "source_url": seed["url"],
        "repository": repo,
        "pr_number": pr_number,
        "pr_title": str(pull.get("title") or ""),
        "merged_at": pull.get("merged_at"),
        "base_sha": base_sha,
        "head_sha": head_sha,
        "language": language,
        "code_changed_files": code_changed_files,
        "code_diff_excerpt": code_diff_excerpt,
        "docs_before_excerpt": docs_before_excerpt,
        "docs_before_retrieval_policy": retrieval_policy,
        "docs_before_retrieved_files": retrieved_files,
        "documentation_context_candidates": documentation_context_candidates,
        "classifier_model_input": {
            "language": language,
            "code_changed_files": code_changed_files,
            "code_diff_excerpt": code_diff_excerpt,
            "docs_before_excerpt": docs_before_excerpt,
        },
        "generator_context": {
            "documentation_context_candidates": documentation_context_candidates,
        },
        "changed_files": changed_files,
        "docs_changed_files": docs_changed_files,
        "docs_diff_excerpt": docs_diff_excerpt,
        "docs_after_excerpt": docs_after_excerpt,
        "candidate_evidence": {
            "builder_version": "github_pr_dataset_builder_v2",
            "candidate_type": summarize_candidate_type(code_files=code_changed_files, docs_files=docs_changed_files, code_diff=code_diff_excerpt),
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
        "safe_model_input_fields": SAFE_MODEL_INPUT_FIELDS,
        "audit_only_fields": AUDIT_ONLY_FIELDS,
    }
    forbidden = FORBIDDEN_GOLD_FIELDS & set(case)
    if forbidden:
        raise RuntimeError(f"V2 candidate emitted forbidden gold fields: {sorted(forbidden)}")
    return case, None


def duplicate_key(case: dict[str, Any]) -> tuple[str, int]:
    return (str(case.get("repository") or "").lower(), int(case.get("pr_number") or 0))


def build_dataset_v2(*, seeds: list[dict[str, Any]], client: Any, config: BuildConfig, max_cases: int | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cases: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []
    seen_prs: set[tuple[str, int]] = set()
    seen_urls: set[str] = set()
    seen_case_ids: set[str] = set()
    for seed in seeds:
        if max_cases is not None and len(cases) >= max_cases:
            break
        try:
            case, reject = build_candidate_case_v2(seed=seed, client=client, config=config)
        except GlobalGitHubStop as exc:
            rejects.append({"reject_reason": "github_operational_stop", "stop_reason": exc.stop_reason})
            break
        if reject is not None:
            rejects.append(reject)
        if case is not None:
            key = duplicate_key(case)
            url = str(case.get("source_url") or "")
            cid = str(case.get("case_id") or "")
            reasons = []
            if key in seen_prs:
                reasons.append("duplicate_repository_pr_number")
            if url in seen_urls:
                reasons.append("duplicate_source_url")
            if cid in seen_case_ids:
                reasons.append("duplicate_case_id")
            if reasons:
                rejects.append({**case, "reject_reason": ",".join(reasons)})
            else:
                cases.append(case)
                seen_prs.add(key)
                seen_urls.add(url)
                seen_case_ids.add(cid)
    return cases, rejects


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def count_nested(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "") for row in rows))


def write_report(path: Path, *, cases: list[dict[str, Any]], rejects: list[dict[str, Any]], client_stats: dict[str, Any] | None = None, status: str = "ok") -> None:
    lines = [
        "# DocGuard GitHub PR Candidate Builder V2 Report",
        "",
        "V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.",
        "",
        f"- Status: `{status}`",
        f"- Accepted candidates: `{len(cases)}`",
        f"- Rejected seeds: `{len(rejects)}`",
        f"- Operational/client stats: `{client_stats or {}}`",
        f"- Language counts: `{count_nested(cases, 'language')}`",
        "",
        "Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build leak-free Final V2 GitHub PR candidate records.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--rejects")
    parser.add_argument("--report", required=True)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--max-code-diff-chars", type=int, default=9000)
    parser.add_argument("--max-docs-chars", type=int, default=5000)
    parser.add_argument("--max-docs-files", type=int, default=3)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--require-authenticated", action="store_true")
    parser.add_argument("--min-request-interval-seconds", type=float, default=0.25)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--cache-dir", default="data/external/project_case_study/cache/github_api")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    token = os.getenv(args.github_token_env) or None
    if args.require_authenticated and not token:
        print(json.dumps({"status": "failed", "stop_reason": "missing_required_github_token", "accepted_candidates": 0}, indent=2))
        return 2
    cache = None if args.no_cache else GitHubApiCache(Path(args.cache_dir))
    client = GitHubClientV2(token=token, timeout_seconds=args.timeout_seconds, cache=cache, min_request_interval_seconds=args.min_request_interval_seconds)
    config = BuildConfig(args.max_code_diff_chars, args.max_docs_chars, args.max_docs_files, args.sleep_seconds)
    cases, rejects = build_dataset_v2(seeds=load_seed_records(Path(args.input)), client=client, config=config, max_cases=args.max_cases)
    output = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output.with_suffix(".rejects.jsonl")
    write_jsonl(output, cases)
    write_jsonl(rejects_path, rejects)
    status = "partial" if getattr(client, "stop_reason", None) else "ok"
    write_report(Path(args.report), cases=cases, rejects=rejects, client_stats=client.stats(), status=status)
    print(json.dumps({"status": status, "accepted_candidates": len(cases), "rejected_seeds": len(rejects), "output": str(output), "client_stats": client.stats()}, indent=2))
    return 0 if status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
