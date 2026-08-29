from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from docguard_external.github_client_v2 import GitHubClientV2, GitHubOperationalError, GlobalGitHubStop
from docguard_external.github_api_cache import GitHubApiCache
from docguard_external.document_retrieval_backends_v2 import AutoDocumentBackendClient, LocalGitDocumentBackend
from docguard_external.operational_profiler_v2 import ThreadSafeLatencyProfiler
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
CHECKPOINT_SCHEMA = "docguard_final_v2_candidate_builder_checkpoint_v1"
OPERATIONAL_PENDING_SCHEMA = "docguard_final_v2_operational_pending_v1"
OPERATIONAL_PENDING_RETRY_STATE = "pending"


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


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def pending_identity(repository: str, pr_number: int) -> str:
    return f"{repository.strip().lower()}#{int(pr_number)}"


def is_operational_exception(exc: Exception) -> bool:
    if isinstance(exc, GlobalGitHubStop):
        return True
    if isinstance(exc, (TimeoutError, OSError)):
        return True
    if isinstance(exc, GitHubOperationalError):
        return exc.status_code in {None, 401, 403, 429, 500, 502, 503, 504} or exc.is_transient or exc.is_secondary_rate_limit or exc.is_primary_rate_limit or exc.is_authentication_failure
    text = str(exc).lower()
    return any(
        term in text
        for term in [
            "timeout",
            "timed out",
            "network",
            "dns",
            "temporary failure",
            "connection",
            "rate limit",
            "authentication",
            "403",
            "429",
            "500",
            "502",
            "503",
            "504",
        ]
    )


def operational_failure_type(exc: Exception | None = None, *, stop_reason: str | None = None) -> str:
    if stop_reason:
        return stop_reason
    if isinstance(exc, GitHubOperationalError):
        if exc.status_code is None:
            return "network_or_timeout"
        if exc.is_authentication_failure:
            return "authentication_failed"
        if exc.is_primary_rate_limit:
            return "primary_rate_limit_exhausted"
        if exc.is_secondary_rate_limit:
            return "secondary_rate_limit"
        if exc.is_transient:
            return f"http_{exc.status_code}"
        return f"http_{exc.status_code}"
    if isinstance(exc, GlobalGitHubStop):
        return exc.stop_reason
    return "operational_failure"


def make_operational_pending(seed: dict[str, Any], *, input_index: int | None = None, exc: Exception | None = None, stop_reason: str | None = None, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    repo = str(seed.get("repo") or seed.get("repository") or "")
    pr_number = int(seed.get("pr_number") or 0)
    now = utc_now()
    previous_attempts = int((existing or {}).get("attempt_count") or 0)
    first_failed_at = str((existing or {}).get("first_failed_at") or now)
    status_code = getattr(exc, "status_code", None)
    return {
        "schema": OPERATIONAL_PENDING_SCHEMA,
        "input_index": input_index if input_index is not None else (existing or {}).get("input_index"),
        "seed": seed,
        "case_id": stable_case_id(repo, pr_number) if repo and pr_number else (existing or {}).get("case_id"),
        "repository": repo,
        "pr_number": pr_number,
        "source_url": str(seed.get("url") or seed.get("source_url") or ""),
        "operational_failure_type": operational_failure_type(exc, stop_reason=stop_reason),
        "last_error": str(exc or stop_reason or ""),
        "last_status_code": status_code,
        "first_failed_at": first_failed_at,
        "last_failed_at": now,
        "attempt_count": previous_attempts + 1,
        "retry_state": OPERATIONAL_PENDING_RETRY_STATE,
    }


def pending_key(row: dict[str, Any]) -> str:
    repo = str(row.get("repository") or (row.get("seed") or {}).get("repo") or "").lower()
    pr_number = int(row.get("pr_number") or (row.get("seed") or {}).get("pr_number") or 0)
    return pending_identity(repo, pr_number)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp_path, path)


def load_pending_queue(path: Path) -> list[dict[str, Any]]:
    rows = read_jsonl(path)
    by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        if str(row.get("retry_state") or OPERATIONAL_PENDING_RETRY_STATE) != OPERATIONAL_PENDING_RETRY_STATE:
            continue
        by_key[pending_key(row)] = row
    return [by_key[key] for key in sorted(by_key, key=lambda k: (int(by_key[k].get("input_index") or 10**12), k))]


def merge_pending_rows(existing: list[dict[str, Any]], new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {pending_key(row): row for row in existing}
    for row in new_rows:
        key = pending_key(row)
        prior = by_key.get(key)
        if prior is not None:
            row = make_operational_pending(row.get("seed") or {}, input_index=row.get("input_index"), exc=Exception(str(row.get("last_error") or "")), existing=prior)
            row["operational_failure_type"] = str(row.get("operational_failure_type") or prior.get("operational_failure_type") or "operational_failure")
            row["last_status_code"] = row.get("last_status_code") or prior.get("last_status_code")
        by_key[key] = row
    return [by_key[key] for key in sorted(by_key, key=lambda k: (int(by_key[k].get("input_index") or 10**12), k))]


def persist_pending_queue(path: Path, existing: list[dict[str, Any]], new_rows: list[dict[str, Any]], *, accepted: list[dict[str, Any]] | None = None, rejects: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows = merge_pending_rows(existing, new_rows)
    accepted_keys = {pending_identity(str(row.get("repository") or ""), int(row.get("pr_number") or 0)) for row in (accepted or [])}
    rejected_keys = {pending_identity(str(row.get("repository") or ""), int(row.get("pr_number") or 0)) for row in (rejects or [])}
    rows = [row for row in rows if pending_key(row) not in accepted_keys and pending_key(row) not in rejected_keys]
    write_jsonl_atomic(path, rows)
    return rows


def reject_is_operational(row: dict[str, Any]) -> bool:
    reason = str(row.get("reject_reason") or "")
    error = str(row.get("error") or row.get("last_error") or row.get("stop_reason") or "")
    combined = f"{reason} {error}".lower()
    if reason in {"github_operational_stop", "operational_pending"}:
        return True
    if reason == "github_fetch_failed":
        return any(term in combined for term in ["timeout", "network", "dns", "connection", "urlopen", "getaddrinfo", "errno", "rate limit", "authentication", "403", "429", "500", "502", "503", "504"])
    return False


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
        candidates.append({"path": path, "excerpt": generator_chunk, "source_ref": ref, "blob_sha": blob_sha, "retrieval_provenance": {**discovery, "path": path, "blob_sha": blob_sha, "discovery_source": record.get("discovery_source"), "selection_rank": len(candidates) + 1, "selection_score": list(doc_path_quality(path, code_changed_files, code_diff_excerpt)), "truncated_excerpt": len(text) > len(generator_chunk), "generator_pool_policy": "base_sha_broad_bounded_doc_pool_v2", "max_generator_doc_files": max_generator_doc_files, "max_generator_doc_chars_per_file": max_generator_doc_chars_per_file}})
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
    profiler = getattr(client, "profiler", None)
    try:
        with profiler.stage("pull_metadata_seconds") if profiler else nullcontext():
            pull = client.get_pull(repo, pr_number)
        with profiler.stage("pull_files_seconds") if profiler else nullcontext():
            files = client.get_pull_files(repo, pr_number)
    except GlobalGitHubStop:
        raise
    except Exception as exc:
        if is_operational_exception(exc):
            return None, {"case_id": case_id, "source_url": seed["url"], "repository": repo, "pr_number": pr_number, "reject_reason": "operational_pending", "error": str(exc), "_operational_pending": True}
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
        with profiler.stage("document_discovery_seconds") if profiler else nullcontext():
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
    with profiler.stage("audit_context_seconds") if profiler and head_sha and docs_changed_files else nullcontext():
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scientific_config_fingerprint(*, config: BuildConfig, max_cases: int | None = None) -> str:
    payload = {
        "schema": "docguard_final_v2_scientific_config_v1",
        "max_cases": max_cases,
        "max_code_diff_chars": config.max_code_diff_chars,
        "max_docs_chars": config.max_docs_chars,
        "max_docs_files": config.max_docs_files,
        "max_generator_doc_files": int(getattr(config, "max_generator_doc_files", 12)),
        "max_generator_doc_chars_per_file": int(getattr(config, "max_generator_doc_chars_per_file", 1500)),
        "max_generator_doc_total_chars": int(getattr(config, "max_generator_doc_total_chars", 18000)),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp_path, path)


def checkpoint_path(checkpoint_dir: Path, start_index: int, end_index: int) -> Path:
    return checkpoint_dir / f"chunk_{start_index:06d}_{end_index:06d}.json"


def load_checkpoint_chunks(*, checkpoint_dir: Path, input_hash: str, config_fingerprint: str, total_seed_count: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], int, int]:
    cases: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    completed_seed_count = 0
    checkpoint_count = 0
    for path in sorted(checkpoint_dir.glob("chunk_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema") != CHECKPOINT_SCHEMA:
            raise RuntimeError(f"incompatible checkpoint schema: {path}")
        if payload.get("input_sha256") != input_hash:
            raise RuntimeError(f"checkpoint input hash mismatch: {path}")
        if payload.get("scientific_config_fingerprint") != config_fingerprint:
            raise RuntimeError(f"checkpoint scientific config mismatch: {path}")
        if int(payload.get("total_seed_count") or -1) != total_seed_count:
            raise RuntimeError(f"checkpoint total seed count mismatch: {path}")
        start_index = int(payload.get("start_seed_index") or 0)
        end_index = int(payload.get("end_seed_index") or 0)
        if start_index != completed_seed_count:
            break
        cases.extend(list(payload.get("cases") or []))
        rejects.extend(list(payload.get("rejects") or []))
        pending.extend(list(payload.get("operational_pending") or []))
        completed_seed_count = end_index
        checkpoint_count += 1
    return cases, rejects, pending, completed_seed_count, checkpoint_count


def write_checkpoint_chunk(*, checkpoint_dir: Path, start_index: int, end_index: int, cases: list[dict[str, Any]], rejects: list[dict[str, Any]], operational_pending: list[dict[str, Any]] | None = None, input_hash: str, config_fingerprint: str, total_seed_count: int) -> None:
    pending = operational_pending or []
    payload = {
        "schema": CHECKPOINT_SCHEMA,
        "input_sha256": input_hash,
        "scientific_config_fingerprint": config_fingerprint,
        "total_seed_count": total_seed_count,
        "start_seed_index": start_index,
        "end_seed_index": end_index,
        "completed_seed_count": end_index,
        "completed_or_visited_seed_count": end_index,
        "last_completed_input_index": end_index - 1 if end_index else None,
        "accepted_count": len(cases),
        "scientific_rejected_count": len(rejects),
        "rejected_count": len(rejects),
        "operational_pending_count": len(pending),
        "cases": cases,
        "rejects": rejects,
        "operational_pending": pending,
    }
    atomic_write_json(checkpoint_path(checkpoint_dir, start_index, end_index), payload)


def write_progress_state(*, checkpoint_dir: Path, input_hash: str, config_fingerprint: str, total_seed_count: int, completed_seed_count: int, accepted_count: int, rejected_count: int, operational_pending_count: int, checkpoint_count: int, complete: bool) -> None:
    resolved_total = accepted_count + rejected_count
    unprocessed = max(total_seed_count - completed_seed_count, 0)
    atomic_write_json(
        checkpoint_dir / "progress_state.json",
        {
            "schema": "docguard_final_v2_candidate_builder_progress_v1",
            "input_sha256": input_hash,
            "scientific_config_fingerprint": config_fingerprint,
            "total_seed_count": total_seed_count,
            "completed_seed_count": completed_seed_count,
            "completed_or_visited_seed_count": completed_seed_count,
            "accepted_count": accepted_count,
            "scientific_rejected_count": rejected_count,
            "rejected_count": rejected_count,
            "operational_pending_count": operational_pending_count,
            "resolved_total": resolved_total,
            "unprocessed": unprocessed,
            "checkpoint_count": checkpoint_count,
            "status": "complete" if complete and operational_pending_count == 0 and unprocessed == 0 and resolved_total == total_seed_count else ("complete_with_operational_pending" if unprocessed == 0 and operational_pending_count > 0 else "partial"),
            "complete": complete and operational_pending_count == 0 and unprocessed == 0 and resolved_total == total_seed_count,
        },
    )


def progress_line(*, processed: int, total: int, accepted: int, rejected: int, pending: int, current: str, start_time: float, checkpoint_completed: int, client: Any) -> str:
    elapsed = max(time.time() - start_time, 0.001)
    rate = processed / elapsed * 60.0
    remaining = max(total - processed, 0)
    eta_seconds = remaining / max(processed / elapsed, 0.001)
    resolved = accepted + rejected
    unprocessed = max(total - processed, 0)
    stats = client.stats() if hasattr(client, "stats") else {}
    return (
        f"[FinalV2] {processed}/{total} visited ({processed / max(total, 1) * 100:.1f}%) "
        f"accepted={accepted} scientific_rejected={rejected} operational_pending={pending} resolved={resolved} unprocessed={unprocessed} current={current} "
        f"elapsed={time.strftime('%H:%M:%S', time.gmtime(elapsed))} "
        f"rate={rate:.1f} seeds/min ETA={time.strftime('%H:%M:%S', time.gmtime(eta_seconds))} "
        f"checkpoint={checkpoint_completed} REST outbound={stats.get('outbound_request_count', 0)} "
        f"REST cache hits={stats.get('cache_hit_count', 0)} blob cache hits={stats.get('blob_cache_hit_count', 0)} "
        f"git repo hits={stats.get('git_repository_cache_hit_count', 0)} git clones={stats.get('git_repository_init_count', 0)} "
        f"git fetches={stats.get('git_fetch_count', 0)} git tree reads={stats.get('git_tree_read_count', 0)} "
        f"git blob reads={stats.get('git_blob_read_count', 0)} REST fallbacks={stats.get('rest_fallback_count', 0)} "
        f"retries={stats.get('request_retry_count', 0)} failures={stats.get('operational_failures', {})}"
    )


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
            break
        if reject is not None and not reject.get("_operational_pending"):
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


def process_seed_for_checkpoint(*, index: int, seed: dict[str, Any], client: Any, config: BuildConfig) -> dict[str, Any]:
    profiler = getattr(client, "profiler", None)
    try:
        with profiler.stage("seed_total_seconds") if profiler else nullcontext():
            case, reject = build_candidate_case_v2(seed=seed, client=client, config=config)
        return {"index": index, "seed": seed, "case": case, "reject": reject, "global_stop": None}
    except GlobalGitHubStop as exc:
        return {"index": index, "seed": seed, "case": None, "reject": None, "global_stop": exc}


def build_dataset_v2_checkpointed(
    *,
    seeds: list[dict[str, Any]],
    client: Any,
    config: BuildConfig,
    input_hash: str,
    config_fingerprint: str,
    checkpoint_dir: Path,
    checkpoint_every: int = 50,
    progress_every: int = 25,
    resume: bool = False,
    max_cases: int | None = None,
    interrupt_after_seeds: int | None = None,
    operational_pending_path: Path | None = None,
    workers: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    total_seed_count = len(seeds)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    existing_pending = load_pending_queue(operational_pending_path) if operational_pending_path is not None else []
    if resume:
        cases, rejects, checkpoint_pending, start_index, checkpoint_count = load_checkpoint_chunks(checkpoint_dir=checkpoint_dir, input_hash=input_hash, config_fingerprint=config_fingerprint, total_seed_count=total_seed_count)
        existing_pending = merge_pending_rows(existing_pending, checkpoint_pending)
    else:
        existing = list(checkpoint_dir.glob("chunk_*.json"))
        if existing:
            raise RuntimeError(f"checkpoint directory is not empty; use --resume or choose a new directory: {checkpoint_dir}")
        cases, rejects, start_index, checkpoint_count = [], [], 0, 0
    seen_prs = {duplicate_key(case) for case in cases}
    seen_urls = {str(case.get("source_url") or "") for case in cases}
    seen_case_ids = {str(case.get("case_id") or "") for case in cases}
    chunk_start = start_index
    chunk_cases: list[dict[str, Any]] = []
    chunk_rejects: list[dict[str, Any]] = []
    chunk_pending: list[dict[str, Any]] = []
    pending_rows = list(existing_pending)
    start_time = time.time()
    processed = start_index
    checkpoint_every = max(int(checkpoint_every), 1)
    progress_every = max(int(progress_every), 1)
    workers = max(int(workers), 1)
    status = "ok"
    while processed < total_seed_count:
        if max_cases is not None and len(cases) >= max_cases:
            break
        chunk_end = min(processed + checkpoint_every, total_seed_count)
        chunk_inputs = list(enumerate(seeds[processed:chunk_end], start=processed))
        results: list[dict[str, Any]] = []
        if workers == 1:
            for index, seed in chunk_inputs:
                results.append(process_seed_for_checkpoint(index=index, seed=seed, client=client, config=config))
        else:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(process_seed_for_checkpoint, index=index, seed=seed, client=client, config=config) for index, seed in chunk_inputs]
                for future in as_completed(futures):
                    results.append(future.result())
        current = ""
        for result in sorted(results, key=lambda item: int(item["index"])):
            index = int(result["index"])
            seed = result["seed"]
            current = f"{seed.get('repo')}#{seed.get('pr_number')}"
            case = result["case"]
            reject = result["reject"]
            exc = result["global_stop"]
            if exc is not None:
                pending = make_operational_pending(seed, input_index=index, exc=exc, stop_reason=exc.stop_reason)
                pending_rows = merge_pending_rows(pending_rows, [pending])
                chunk_pending.append(pending)
                if operational_pending_path is not None:
                    persist_pending_queue(operational_pending_path, pending_rows, [], accepted=cases, rejects=rejects)
                status = "partial"
                processed = index + 1
                break
            if reject is not None and reject.get("_operational_pending"):
                pending = make_operational_pending(seed, input_index=index, exc=Exception(str(reject.get("error") or "")))
                pending["case_id"] = reject.get("case_id") or pending.get("case_id")
                pending["operational_failure_type"] = str(reject.get("operational_failure_type") or "operational_failure")
                pending_rows = merge_pending_rows(pending_rows, [pending])
                chunk_pending.append(pending)
                if operational_pending_path is not None:
                    persist_pending_queue(operational_pending_path, pending_rows, [], accepted=cases, rejects=rejects)
                reject = None
            if reject is not None:
                rejects.append(reject)
                chunk_rejects.append(reject)
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
                    duplicate_reject = {**case, "reject_reason": ",".join(reasons)}
                    rejects.append(duplicate_reject)
                    chunk_rejects.append(duplicate_reject)
                else:
                    cases.append(case)
                    chunk_cases.append(case)
                    seen_prs.add(key)
                    seen_urls.add(url)
                    seen_case_ids.add(cid)
            processed = index + 1
            if interrupt_after_seeds is not None and processed >= interrupt_after_seeds:
                raise RuntimeError("simulated interruption")
        profiler = getattr(client, "profiler", None)
        with profiler.stage("checkpoint_write_seconds") if profiler else nullcontext():
            write_checkpoint_chunk(checkpoint_dir=checkpoint_dir, start_index=chunk_start, end_index=processed, cases=chunk_cases, rejects=chunk_rejects, operational_pending=chunk_pending, input_hash=input_hash, config_fingerprint=config_fingerprint, total_seed_count=total_seed_count)
        checkpoint_count += 1
        write_progress_state(checkpoint_dir=checkpoint_dir, input_hash=input_hash, config_fingerprint=config_fingerprint, total_seed_count=total_seed_count, completed_seed_count=processed, accepted_count=len(cases), rejected_count=len(rejects), operational_pending_count=len(pending_rows), checkpoint_count=checkpoint_count, complete=False)
        chunk_start = processed
        chunk_cases = []
        chunk_rejects = []
        chunk_pending = []
        if processed % progress_every == 0 or status == "partial":
            print(progress_line(processed=processed, total=total_seed_count, accepted=len(cases), rejected=len(rejects), pending=len(pending_rows), current=current, start_time=start_time, checkpoint_completed=chunk_start, client=client), flush=True)
        if status == "partial":
            break
    complete = status == "ok" and (processed >= total_seed_count or (max_cases is not None and len(cases) >= max_cases))
    if operational_pending_path is not None:
        pending_rows = persist_pending_queue(operational_pending_path, pending_rows, [], accepted=cases, rejects=rejects)
    write_progress_state(checkpoint_dir=checkpoint_dir, input_hash=input_hash, config_fingerprint=config_fingerprint, total_seed_count=total_seed_count, completed_seed_count=processed, accepted_count=len(cases), rejected_count=len(rejects), operational_pending_count=len(pending_rows), checkpoint_count=checkpoint_count, complete=complete)
    final_status = "complete" if complete and not pending_rows else ("complete_with_operational_pending" if complete and pending_rows else status)
    return cases, rejects, {"status": final_status, "completed_seed_count": processed, "checkpoint_count": checkpoint_count, "resume_completed_seed_count": start_index, "operational_pending_count": len(pending_rows), "scientific_reject_count": len(rejects), "operational_pending_created_count": len(pending_rows)}


def recover_operational_rejects_from_checkpoints(*, checkpoint_dir: Path, operational_pending_path: Path) -> dict[str, Any]:
    pending_rows = load_pending_queue(operational_pending_path)
    migrated = 0
    scientific = 0
    for path in sorted(checkpoint_dir.glob("chunk_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        rejects = list(payload.get("rejects") or [])
        kept: list[dict[str, Any]] = []
        moved: list[dict[str, Any]] = []
        start = int(payload.get("start_seed_index") or 0)
        for offset, reject in enumerate(rejects):
            if reject_is_operational(reject):
                seed = reject.get("seed") or {"repo": reject.get("repository"), "pr_number": reject.get("pr_number"), "url": reject.get("source_url")}
                pending = make_operational_pending(seed, input_index=reject.get("input_index", start + offset), exc=Exception(str(reject.get("error") or reject.get("stop_reason") or "")), existing=None)
                pending["case_id"] = reject.get("case_id") or pending.get("case_id")
                pending["operational_failure_type"] = str(reject.get("stop_reason") or reject.get("operational_failure_type") or "historical_operational_reject")
                moved.append(pending)
            else:
                kept.append(reject)
        if moved:
            payload["rejects"] = kept
            payload["rejected_count"] = len(kept)
            payload["scientific_rejected_count"] = len(kept)
            existing_chunk_pending = list(payload.get("operational_pending") or [])
            merged_chunk_pending = merge_pending_rows(existing_chunk_pending, moved)
            payload["operational_pending"] = merged_chunk_pending
            payload["operational_pending_count"] = len(merged_chunk_pending)
            atomic_write_json(path, payload)
            pending_rows = merge_pending_rows(pending_rows, moved)
            migrated += len(moved)
        scientific += len(kept)
    pending_rows = persist_pending_queue(operational_pending_path, pending_rows, [])
    return {"migrated_operational_failures": migrated, "genuine_scientific_rejects": scientific, "operational_pending_count": len(pending_rows)}


def retry_operational_pending(*, pending_path: Path, output_path: Path, rejects_path: Path, client: Any, config: BuildConfig, max_pending_to_process: int | None = None) -> dict[str, Any]:
    pending_rows = load_pending_queue(pending_path)
    cases = read_jsonl(output_path)
    rejects = read_jsonl(rejects_path)
    accepted_keys = {pending_identity(str(row.get("repository") or ""), int(row.get("pr_number") or 0)) for row in cases}
    reject_keys = {pending_identity(str(row.get("repository") or ""), int(row.get("pr_number") or 0)) for row in rejects}
    remaining: list[dict[str, Any]] = []
    new_cases: list[dict[str, Any]] = []
    new_rejects: list[dict[str, Any]] = []
    retry_failures = 0
    resolved = 0
    processed = 0
    for pending in pending_rows:
        key = pending_key(pending)
        if key in accepted_keys or key in reject_keys:
            resolved += 1
            continue
        if max_pending_to_process is not None and processed >= max_pending_to_process:
            remaining.append(pending)
            continue
        processed += 1
        seed = pending.get("seed") or {"repo": pending.get("repository"), "pr_number": pending.get("pr_number"), "url": pending.get("source_url")}
        try:
            case, reject = build_candidate_case_v2(seed=seed, client=client, config=config)
        except GlobalGitHubStop as exc:
            remaining.append(make_operational_pending(seed, input_index=pending.get("input_index"), exc=exc, stop_reason=exc.stop_reason, existing=pending))
            retry_failures += 1
            continue
        if reject is not None and reject.get("_operational_pending"):
            remaining.append(make_operational_pending(seed, input_index=pending.get("input_index"), exc=Exception(str(reject.get("error") or "")), existing=pending))
            retry_failures += 1
        elif reject is not None:
            new_rejects.append(reject)
            reject_keys.add(key)
            resolved += 1
        elif case is not None:
            new_cases.append(case)
            accepted_keys.add(key)
            resolved += 1
    cases.extend(new_cases)
    rejects.extend(new_rejects)
    write_jsonl_atomic(output_path, cases)
    write_jsonl_atomic(rejects_path, rejects)
    write_jsonl_atomic(pending_path, remaining)
    return {"processed_pending": processed, "operational_pending_resolved_count": resolved, "operational_pending_retry_failure_count": retry_failures, "operational_pending_count": len(remaining), "accepted_added": len(new_cases), "scientific_rejects_added": len(new_rejects)}


def validate_final_v2_completion_state(*, total_input_seeds: int, accepted_count: int, scientific_reject_count: int, operational_pending_count: int, visited_count: int | None = None) -> dict[str, Any]:
    resolved_total = accepted_count + scientific_reject_count
    unprocessed = max(total_input_seeds - (visited_count if visited_count is not None else resolved_total + operational_pending_count), 0)
    complete = resolved_total == total_input_seeds and operational_pending_count == 0 and unprocessed == 0
    return {
        "status": "complete" if complete else ("complete_with_operational_pending" if unprocessed == 0 and operational_pending_count > 0 else "incomplete"),
        "total_input_seeds": total_input_seeds,
        "accepted_candidates": accepted_count,
        "scientific_rejects": scientific_reject_count,
        "operational_pending": operational_pending_count,
        "resolved_total": resolved_total,
        "unprocessed": unprocessed,
        "complete": complete,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def count_nested(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "") for row in rows))


def write_report(path: Path, *, cases: list[dict[str, Any]], rejects: list[dict[str, Any]], client_stats: dict[str, Any] | None = None, status: str = "ok", config: Any | None = None) -> None:
    stats = client_stats or {}
    lines = [
        "# DocGuard GitHub PR Candidate Builder V2 Report",
        "",
        "V2 candidate construction is leak-free with respect to final labels and PR outcome documentation routing.",
        "",
        f"- Status: `{status}`",
        f"- Accepted candidates: `{len(cases)}`",
        f"- Scientific rejects: `{len(rejects)}`",
        f"- Operational pending: `{stats.get('operational_pending_count', 0)}`",
        f"- Resolved total: `{len(cases) + len(rejects)}`",
        f"- Operational/client stats: `{stats}`",
        f"- Max generator doc files: `{getattr(config, 'max_generator_doc_files', 12) if config is not None else 12}`",
        f"- Max generator doc chars per file: `{getattr(config, 'max_generator_doc_chars_per_file', 1500) if config is not None else 1500}`",
        f"- Language counts: `{count_nested(cases, 'language')}`",
        "",
        "Candidate records contain no `gold_*` fields. `docs_before_excerpt` is retrieved from `base_sha` using neutral documentation paths and code-path hints only; it never prioritizes `docs_changed_files`, `docs_diff_excerpt`, or `docs_after_excerpt`.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def make_builder_client(*, token: str | None, timeout_seconds: int, cache: Any | None, min_request_interval_seconds: float, document_retrieval_backend: str = "rest", git_cache_dir: Path | None = None, rest_max_inflight: int = 1, profiler: ThreadSafeLatencyProfiler | None = None) -> Any:
    rest_client = GitHubClientV2(token=token, timeout_seconds=timeout_seconds, cache=cache, min_request_interval_seconds=min_request_interval_seconds, rest_max_inflight=rest_max_inflight, profiler=profiler)
    if document_retrieval_backend == "rest":
        return rest_client
    local_backend = LocalGitDocumentBackend(cache_dir=git_cache_dir or Path("data/external/project_case_study/cache/git_repos_final_v2"), timeout_seconds=timeout_seconds, profiler=profiler)
    return AutoDocumentBackendClient(rest_client=rest_client, local_backend=local_backend, mode=document_retrieval_backend)


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
    parser.add_argument("--git-cache-dir", default="data/external/project_case_study/cache/git_repos_final_v2")
    parser.add_argument("--document-retrieval-backend", choices=["rest", "local-git", "auto"], default="rest")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--checkpoint-dir")
    parser.add_argument("--checkpoint-every", type=int, default=50)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--rest-max-inflight", type=int, default=1)
    parser.add_argument("--operational-pending")
    parser.add_argument("--retry-operational-pending", action="store_true")
    parser.add_argument("--max-pending-to-process", type=int)
    parser.add_argument("--recover-operational-rejects", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    token = os.getenv(args.github_token_env) or None
    if args.require_authenticated and not token:
        print(json.dumps({"status": "failed", "stop_reason": "missing_required_github_token", "accepted_candidates": 0}, indent=2))
        return 2
    cache = None if args.no_cache else GitHubApiCache(Path(args.cache_dir))
    profiler = ThreadSafeLatencyProfiler()
    client = make_builder_client(token=token, timeout_seconds=args.timeout_seconds, cache=cache, min_request_interval_seconds=args.min_request_interval_seconds, document_retrieval_backend=args.document_retrieval_backend, git_cache_dir=Path(args.git_cache_dir), rest_max_inflight=args.rest_max_inflight, profiler=profiler)
    config = BuildConfigV2(args.max_code_diff_chars, args.max_docs_chars, args.max_docs_files, args.sleep_seconds, args.max_generator_doc_files, args.max_generator_doc_chars_per_file, args.max_generator_doc_total_chars)
    input_path = Path(args.input)
    seeds = load_seed_records(input_path)
    input_hash = sha256_file(input_path)
    config_fingerprint = scientific_config_fingerprint(config=config, max_cases=args.max_cases)
    output = Path(args.output)
    rejects_path = Path(args.rejects) if args.rejects else output.with_suffix(".rejects.jsonl")
    operational_pending_path = Path(args.operational_pending) if args.operational_pending else output.with_suffix(".operational_pending.jsonl")
    if args.recover_operational_rejects:
        if not args.checkpoint_dir:
            raise SystemExit("--recover-operational-rejects requires --checkpoint-dir")
        recovery = recover_operational_rejects_from_checkpoints(checkpoint_dir=Path(args.checkpoint_dir), operational_pending_path=operational_pending_path)
        print(json.dumps({"status": "ok", "recovery": recovery, "operational_pending": str(operational_pending_path)}, indent=2, ensure_ascii=False))
        return 0
    if args.retry_operational_pending:
        retry_stats = retry_operational_pending(pending_path=operational_pending_path, output_path=output, rejects_path=rejects_path, client=client, config=config, max_pending_to_process=args.max_pending_to_process)
        report_stats = client.stats()
        report_stats.update(retry_stats)
        write_report(Path(args.report), cases=read_jsonl(output), rejects=read_jsonl(rejects_path), client_stats=report_stats, status="retry_operational_pending", config=config)
        print(json.dumps({"status": "ok", "retry": retry_stats, "client_stats": report_stats}, indent=2, ensure_ascii=False))
        return 0
    checkpoint_stats: dict[str, Any] = {}
    if args.checkpoint_dir:
        cases, rejects, checkpoint_stats = build_dataset_v2_checkpointed(
            seeds=seeds,
            client=client,
            config=config,
            input_hash=input_hash,
            config_fingerprint=config_fingerprint,
            checkpoint_dir=Path(args.checkpoint_dir),
            checkpoint_every=args.checkpoint_every,
            progress_every=args.progress_every,
            resume=args.resume,
            max_cases=args.max_cases,
            operational_pending_path=operational_pending_path,
            workers=args.workers,
        )
    else:
        cases, rejects = build_dataset_v2(seeds=seeds, client=client, config=config, max_cases=args.max_cases)
    write_jsonl(output, cases)
    write_jsonl(rejects_path, rejects)
    pending_rows = load_pending_queue(operational_pending_path)
    status = checkpoint_stats.get("status") or ("partial" if getattr(client, "stop_reason", None) else "ok")
    client_stats = client.stats()
    client_stats.update(checkpoint_stats)
    client_stats["stage_profile"] = profiler.summary()
    client_stats["workers"] = args.workers
    client_stats["rest_max_inflight"] = args.rest_max_inflight
    client_stats["operational_pending_count"] = len(pending_rows)
    client_stats["scientific_reject_count"] = len(rejects)
    write_report(Path(args.report), cases=cases, rejects=rejects, client_stats=client_stats, status=status, config=config)
    print(json.dumps({"status": status, "accepted_candidates": len(cases), "rejected_seeds": len(rejects), "output": str(output), "client_stats": client_stats}, indent=2))
    return 0 if status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
