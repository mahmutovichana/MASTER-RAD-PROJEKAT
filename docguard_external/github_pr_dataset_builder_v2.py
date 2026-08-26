from __future__ import annotations

import argparse
from dataclasses import dataclass
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
DOC_COMPONENTS = {"docs", "doc", "documentation", "guides", "reference"}
DOC_LOCATION_PAIRS = {("website", "docs"), ("website", "content")}
DOC_PREFIXES = ("readme", "contributing", "changelog")
EXCLUDED_DOC_PATH_COMPONENTS = {
    "__snapshots__",
    "baseline",
    "baselines",
    "build",
    "coverage",
    "dist",
    "fixture",
    "fixtures",
    "generated",
    "node_modules",
    "snapshot",
    "snapshots",
    "target",
    "test",
    "testdata",
    "tests",
    "vendor",
}
ARTIFACT_DOC_SUFFIXES = (".errors.txt", ".baseline.txt", ".sourcemap.txt", ".snap.txt")


@dataclass(frozen=True)
class BuildConfigV2:
    max_code_diff_chars: int = 9000
    max_docs_chars: int = 5000
    max_docs_files: int = 3
    sleep_seconds: float = 0.0
    max_generator_doc_files: int = 12
    max_generator_doc_chars_per_file: int = 1500
    max_generator_doc_total_chars: int = 18000


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


def normalized_path_components(path: str) -> list[str]:
    return [part for part in path.replace("\\", "/").lower().split("/") if part]


def is_excluded_doc_artifact_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    name = Path(normalized).name
    parts = normalized_path_components(path)
    if any(part in EXCLUDED_DOC_PATH_COMPONENTS for part in parts[:-1]):
        return True
    return any(name.endswith(suffix) for suffix in ARTIFACT_DOC_SUFFIXES)


def is_candidate_doc_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    suffix = Path(normalized).suffix
    name = Path(normalized).name.lower()
    if suffix not in DOC_EXTENSIONS:
        return False
    if is_excluded_doc_artifact_path(path):
        return False
    if any(name.startswith(prefix) for prefix in DOC_PREFIXES):
        return True
    parts = normalized_path_components(path)
    if any(part in DOC_COMPONENTS for part in parts[:-1]):
        return True
    return any(pair[0] in parts and pair[1] in parts for pair in DOC_LOCATION_PAIRS)


def path_tokens(path: str) -> set[str]:
    normalized = path.replace("\\", "/").lower()
    return {token for token in normalized.replace(".", "/").replace("-", "/").replace("_", "/").split("/") if token}


def doc_path_relevance(path: str, code_changed_files: list[str], code_diff_excerpt: str = "") -> tuple[int, int, str]:
    tokens = path_tokens(path)
    code_tokens = set()
    for code_path in code_changed_files:
        code_tokens |= path_tokens(code_path)
    diff_lower = code_diff_excerpt.lower()
    overlap = len(tokens & code_tokens) + sum(1 for token in tokens if len(token) > 2 and token in diff_lower)
    parts = [part for part in path.replace("\\", "/").lower().split("/") if part]
    nested_docs_bonus = 2 if any(part in DOC_COMPONENTS for part in parts[:-1]) and len(parts) > 2 else 0
    generic_penalty = 2 if Path(path.lower()).name.startswith(("readme", "changelog")) else 0
    return overlap + nested_docs_bonus - generic_penalty, len(parts), path


def doc_path_quality(path: str, code_changed_files: list[str], code_diff_excerpt: str = "") -> tuple[int, int, int, int, str]:
    normalized = path.replace("\\", "/").lower()
    parts = normalized_path_components(path)
    name = Path(normalized).name
    relevance, depth, _ = doc_path_relevance(path, code_changed_files, code_diff_excerpt)
    if ("website", "docs") in zip(parts, parts[1:]) or ("website", "content") in zip(parts, parts[1:]):
        family_score = 50
    elif any(part in {"docs", "doc", "documentation", "guides"} for part in parts[:-1]):
        family_score = 45
    elif name.startswith(DOC_PREFIXES):
        family_score = 40
    elif "reference" in parts[:-1]:
        family_score = 35
    else:
        family_score = 10
    first_party_score = 0 if any(part in EXCLUDED_DOC_PATH_COMPONENTS for part in parts[:-1]) else 5
    return family_score, relevance, first_party_score, depth, path


def discover_base_doc_paths(*, client: Any, repo: str, ref: str, code_changed_files: list[str], code_diff_excerpt: str = "", max_discovered_paths: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path_records: list[dict[str, Any]] = []
    tree_paths: set[str] = set()
    excluded_artifact_paths = 0
    discovery_limit = max(max_discovered_paths * 4, max_discovered_paths)
    provenance = {"method": "base_sha_tree_documentation_discovery_v2", "tree_ref": ref, "used_docs_changed_files": False, "tree_discovery_succeeded": True, "truncated": False}
    try:
        tree = client.get_tree_recursive(repo, ref)
    except AttributeError:
        records = [{"path": path, "blob_sha": None, "discovery_source": "fallback_neutral_probe"} for path in neutral_doc_paths(code_changed_files, max_discovered_paths)]
        return records, {"method": "fallback_neutral_known_paths_client_has_no_tree_api", "tree_ref": ref, "used_docs_changed_files": False, "tree_discovery_succeeded": False, "truncated": False, "selection_policy": "fallback_probe_neutral_known_paths_because_tree_unavailable"}
    except GlobalGitHubStop:
        raise
    except Exception:
        records = [{"path": path, "blob_sha": None, "discovery_source": "fallback_neutral_probe"} for path in neutral_doc_paths(code_changed_files, max_discovered_paths)]
        return records, {"method": "fallback_neutral_known_paths_tree_api_failed", "tree_ref": ref, "used_docs_changed_files": False, "tree_discovery_succeeded": False, "truncated": False, "selection_policy": "fallback_probe_neutral_known_paths_because_tree_failed"}
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = str(item.get("path") or "")
        tree_paths.add(path.replace("\\", "/").lower())
        if is_excluded_doc_artifact_path(path):
            excluded_artifact_paths += 1
            continue
        if is_candidate_doc_path(path):
            path_records.append({"path": path, "blob_sha": str(item.get("sha") or "") or None, "discovery_source": "base_sha_tree"})
        if len(path_records) >= discovery_limit:
            provenance["truncated"] = True
            break
    provenance["excluded_artifact_paths"] = excluded_artifact_paths
    provenance["selection_policy"] = "prefer_first_party_human_docs_then_root_project_docs_then_reference_plus_neutral_code_path_affinity"
    neutral = neutral_doc_paths(code_changed_files, max_discovered_paths)
    existing_neutral_records = [
        {"path": path, "blob_sha": None, "discovery_source": "base_sha_tree_existing_neutral_path"}
        for path in neutral
        if path.replace("\\", "/").lower() in tree_paths and path not in {record["path"] for record in path_records}
    ]
    by_path: dict[str, dict[str, Any]] = {}
    for record in path_records + existing_neutral_records:
        by_path.setdefault(str(record["path"]), record)
    ranked = sorted(by_path.values(), key=lambda record: tuple(-value if isinstance(value, int) else value for value in doc_path_quality(str(record["path"]), code_changed_files, code_diff_excerpt)))
    return ranked[:max_discovered_paths], provenance


def fetch_document_text(*, client: Any, repo: str, ref: str, path: str, blob_sha: str | None, content_cache: dict[tuple[str, str], str | None]) -> str | None:
    if blob_sha and hasattr(client, "get_blob_text"):
        cache_key = ("blob", f"{repo}:{blob_sha}")
        if cache_key not in content_cache:
            content_cache[cache_key] = client.get_blob_text(repo, blob_sha)
        return content_cache[cache_key]
    cache_key = ("path_ref", f"{repo}:{path}:{ref}")
    if cache_key not in content_cache:
        content_cache[cache_key] = client.get_file_text(repo, path, ref)
    return content_cache[cache_key]


def collect_docs_before_neutral(*, client: Any, repo: str, ref: str, code_changed_files: list[str], max_chars: int, max_files: int, code_diff_excerpt: str = "", max_generator_doc_files: int = 12, max_generator_doc_chars_per_file: int = 1500, max_generator_doc_total_chars: int = 18000) -> tuple[str, list[str], str, list[dict[str, Any]]]:
    max_discovered_paths = int(getattr(client, "max_discovered_documentation_paths", max(max_generator_doc_files * 8, 80)))
    selected_records, discovery = discover_base_doc_paths(client=client, repo=repo, ref=ref, code_changed_files=code_changed_files, code_diff_excerpt=code_diff_excerpt, max_discovered_paths=max_discovered_paths)
    chunks: list[str] = []
    retrieved: list[str] = []
    candidates: list[dict[str, Any]] = []
    classifier_remaining = max_chars
    generator_remaining = max_generator_doc_total_chars
    content_cache: dict[tuple[str, str], str | None] = {}
    for record in selected_records:
        if len(candidates) >= max_generator_doc_files or generator_remaining <= 0:
            break
        path = str(record.get("path") or "")
        blob_sha = str(record.get("blob_sha") or "") or None
        try:
            text = fetch_document_text(client=client, repo=repo, ref=ref, path=path, blob_sha=blob_sha, content_cache=content_cache)
        except Exception:
            continue
        if not text:
            continue
        generator_limit = min(max_generator_doc_chars_per_file, generator_remaining)
        generator_chunk = truncate_text(text, max(400, generator_limit))
        candidates.append({"path": path, "excerpt": generator_chunk, "source_ref": ref, "blob_sha": blob_sha, "retrieval_provenance": {**discovery, "path": path, "blob_sha": blob_sha, "discovery_source": record.get("discovery_source"), "selection_rank": len(candidates) + 1, "selection_score": doc_path_quality(path, code_changed_files, code_diff_excerpt), "truncated_excerpt": len(text) > len(generator_chunk), "generator_pool_policy": "base_sha_broad_bounded_doc_pool_v2", "max_generator_doc_files": max_generator_doc_files, "max_generator_doc_chars_per_file": max_generator_doc_chars_per_file}})
        generator_remaining -= len(generator_chunk)
        if classifier_remaining > 0 and len(retrieved) < max_files:
            classifier_chunk = truncate_text(text, max(400, classifier_remaining))
            chunks.append(f"<!-- {path} @ {ref} -->\n{classifier_chunk}")
            retrieved.append(path)
            classifier_remaining = max_chars - len("\n\n".join(chunks))
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
            code_diff_excerpt=code_diff_excerpt,
            max_chars=config.max_docs_chars,
            max_files=config.max_docs_files,
            max_generator_doc_files=int(getattr(config, "max_generator_doc_files", 12)),
            max_generator_doc_chars_per_file=int(getattr(config, "max_generator_doc_chars_per_file", 1500)),
            max_generator_doc_total_chars=int(getattr(config, "max_generator_doc_total_chars", 18000)),
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
            "max_generator_doc_files": int(getattr(config, "max_generator_doc_files", 12)),
            "max_generator_doc_chars_per_file": int(getattr(config, "max_generator_doc_chars_per_file", 1500)),
            "generator_documentation_candidate_count": len(documentation_context_candidates),
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


def write_report(path: Path, *, cases: list[dict[str, Any]], rejects: list[dict[str, Any]], client_stats: dict[str, Any] | None = None, status: str = "ok", config: Any | None = None) -> None:
    lines = [
        "# DocGuard GitHub PR Candidate Builder V2 Report",
        "",
        "V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.",
        "",
        f"- Status: `{status}`",
        f"- Accepted candidates: `{len(cases)}`",
        f"- Rejected seeds: `{len(rejects)}`",
        f"- Operational/client stats: `{client_stats or {}}`",
        f"- Max generator doc files: `{getattr(config, 'max_generator_doc_files', 12) if config is not None else 12}`",
        f"- Max generator doc chars per file: `{getattr(config, 'max_generator_doc_chars_per_file', 1500) if config is not None else 1500}`",
        f"- Language counts: `{count_nested(cases, 'language')}`",
        "",
        "Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
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
    parser.add_argument("--max-generator-doc-files", type=int, default=12)
    parser.add_argument("--max-generator-doc-chars-per-file", type=int, default=1500)
    parser.add_argument("--max-generator-doc-total-chars", type=int, default=18000)
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
    config = BuildConfigV2(args.max_code_diff_chars, args.max_docs_chars, args.max_docs_files, args.sleep_seconds, args.max_generator_doc_files, args.max_generator_doc_chars_per_file, args.max_generator_doc_total_chars)
    cases, rejects = build_dataset_v2(seeds=load_seed_records(Path(args.input)), client=client, config=config, max_cases=args.max_cases)
    output = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output.with_suffix(".rejects.jsonl")
    write_jsonl(output, cases)
    write_jsonl(rejects_path, rejects)
    status = "partial" if getattr(client, "stop_reason", None) else "ok"
    write_report(Path(args.report), cases=cases, rejects=rejects, client_stats=client.stats(), status=status, config=config)
    print(json.dumps({"status": status, "accepted_candidates": len(cases), "rejected_seeds": len(rejects), "output": str(output), "client_stats": client.stats()}, indent=2))
    return 0 if status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
