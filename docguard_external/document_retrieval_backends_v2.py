from __future__ import annotations

import hashlib
import json
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from docguard_external.operational_profiler_v2 import ThreadSafeLatencyProfiler


class LocalGitBackendError(Exception):
    pass


@dataclass
class LocalGitStats:
    git_repository_init_count: int = 0
    git_repository_cache_hit_count: int = 0
    git_fetch_count: int = 0
    git_fetch_failure_count: int = 0
    git_tree_read_count: int = 0
    git_blob_read_count: int = 0
    git_blob_read_failure_count: int = 0
    git_command_failure_count: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "git_repository_init_count": self.git_repository_init_count,
            "git_repository_cache_hit_count": self.git_repository_cache_hit_count,
            "git_fetch_count": self.git_fetch_count,
            "git_fetch_failure_count": self.git_fetch_failure_count,
            "git_tree_read_count": self.git_tree_read_count,
            "git_blob_read_count": self.git_blob_read_count,
            "git_blob_read_failure_count": self.git_blob_read_failure_count,
            "git_command_failure_count": self.git_command_failure_count,
        }


@dataclass
class LocalGitDocumentBackend:
    cache_dir: Path
    git_executable: str = "git"
    timeout_seconds: int = 120
    profiler: ThreadSafeLatencyProfiler | None = None
    stats_data: LocalGitStats = field(default_factory=LocalGitStats)
    _repo_dirs: dict[str, Path] = field(default_factory=dict)
    _repo_locks: dict[str, threading.RLock] = field(default_factory=dict)
    _repo_locks_guard: threading.Lock = field(default_factory=threading.Lock)
    _tree_cache: dict[tuple[str, str], list[dict[str, Any]]] = field(default_factory=dict)
    _blob_cache: dict[tuple[str, str], str | None] = field(default_factory=dict)
    _cache_lock: threading.Lock = field(default_factory=threading.Lock)
    tree_cache_hit_count: int = 0
    in_memory_blob_cache_hit_count: int = 0
    singleflight_wait_count: int = 0

    def _repo_lock(self, repo: str) -> threading.RLock:
        key = repo.strip().lower()
        with self._repo_locks_guard:
            if key not in self._repo_locks:
                self._repo_locks[key] = threading.RLock()
            return self._repo_locks[key]

    def repo_cache_path(self, repo: str) -> Path:
        normalized = repo.strip().lower()
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
        owner_repo = normalized.replace("/", "__")
        return self.cache_dir / f"{owner_repo}__{digest}.git"

    def _run_git(self, args: list[str], *, cwd: Path | None = None, timeout_seconds: int | None = None) -> subprocess.CompletedProcess[bytes]:
        try:
            return subprocess.run(
                [self.git_executable, *args],
                cwd=str(cwd) if cwd else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                timeout=timeout_seconds or self.timeout_seconds,
            )
        except Exception as exc:
            self.stats_data.git_command_failure_count += 1
            raise LocalGitBackendError(str(exc)) from exc

    def ensure_repository(self, repo: str) -> Path:
        start = time.perf_counter()
        lock = self._repo_lock(repo)
        waited = not lock.acquire(blocking=False)
        if waited:
            self.singleflight_wait_count += 1
            lock.acquire()
        try:
            if repo in self._repo_dirs:
                self.stats_data.git_repository_cache_hit_count += 1
                return self._repo_dirs[repo]
            path = self.repo_cache_path(repo)
            metadata_path = path.with_suffix(".metadata.json")
            if path.exists():
                self.stats_data.git_repository_cache_hit_count += 1
                self._repo_dirs[repo] = path
                return path
            path.parent.mkdir(parents=True, exist_ok=True)
            remote_url = f"https://github.com/{repo.strip()}.git"
            self._run_git(["clone", "--filter=blob:none", "--bare", remote_url, str(path)], timeout_seconds=self.timeout_seconds)
            metadata_path.write_text(
                json.dumps({"schema": "docguard_local_git_cache_v1", "repo": repo, "remote_url": remote_url}, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )
            self.stats_data.git_repository_init_count += 1
            self._repo_dirs[repo] = path
            return path
        finally:
            lock.release()
            if self.profiler is not None:
                self.profiler.record("git_repository_prepare_seconds", time.perf_counter() - start)

    def _commit_available(self, repo_dir: Path, ref: str) -> bool:
        try:
            self._run_git(["cat-file", "-e", f"{ref}^{{commit}}"], cwd=repo_dir, timeout_seconds=30)
            return True
        except LocalGitBackendError:
            return False

    def _fetch_exact_ref(self, repo_dir: Path, ref: str) -> None:
        try:
            self.stats_data.git_fetch_count += 1
            start = time.perf_counter()
            self._run_git(["fetch", "--depth=1", "origin", ref], cwd=repo_dir, timeout_seconds=self.timeout_seconds)
            if self.profiler is not None:
                self.profiler.record("git_fetch_seconds", time.perf_counter() - start)
        except LocalGitBackendError:
            self.stats_data.git_fetch_failure_count += 1
            raise

    def get_tree_recursive(self, repo: str, ref: str) -> list[dict[str, Any]]:
        key = (repo.strip().lower(), ref)
        with self._cache_lock:
            cached = self._tree_cache.get(key)
            if cached is not None:
                self.tree_cache_hit_count += 1
                return list(cached)
        start = time.perf_counter()
        lock = self._repo_lock(repo)
        waited = not lock.acquire(blocking=False)
        if waited:
            self.singleflight_wait_count += 1
            lock.acquire()
        try:
            with self._cache_lock:
                cached = self._tree_cache.get(key)
                if cached is not None:
                    self.tree_cache_hit_count += 1
                    return list(cached)
            repo_dir = self.ensure_repository(repo)
            if not self._commit_available(repo_dir, ref):
                self._fetch_exact_ref(repo_dir, ref)
                if not self._commit_available(repo_dir, ref):
                    raise LocalGitBackendError(f"missing commit {ref}")
            completed = self._run_git(["ls-tree", "-r", "-z", "--full-tree", ref], cwd=repo_dir)
            self.stats_data.git_tree_read_count += 1
            records: list[dict[str, Any]] = []
            for raw_entry in completed.stdout.split(b"\x00"):
                if not raw_entry:
                    continue
                meta, _, raw_path = raw_entry.partition(b"\t")
                parts = meta.decode("utf-8", errors="replace").split()
                if len(parts) < 3:
                    continue
                records.append({"mode": parts[0], "type": parts[1], "sha": parts[2], "path": raw_path.decode("utf-8", errors="replace")})
            with self._cache_lock:
                self._tree_cache[key] = list(records)
            return records
        finally:
            lock.release()
            if self.profiler is not None:
                self.profiler.record("git_tree_seconds", time.perf_counter() - start)

    def get_blob_text(self, repo: str, blob_sha: str) -> str | None:
        key = (repo.strip().lower(), blob_sha)
        with self._cache_lock:
            if key in self._blob_cache:
                self.in_memory_blob_cache_hit_count += 1
                return self._blob_cache[key]
        start = time.perf_counter()
        repo_dir = self.ensure_repository(repo)
        try:
            completed = self._run_git(["cat-file", "-p", blob_sha], cwd=repo_dir)
        except LocalGitBackendError:
            self.stats_data.git_blob_read_failure_count += 1
            raise
        self.stats_data.git_blob_read_count += 1
        text = completed.stdout.decode("utf-8", errors="replace")
        with self._cache_lock:
            self._blob_cache[key] = text
        if self.profiler is not None:
            self.profiler.record("git_blob_seconds", time.perf_counter() - start)
        return text

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        tree = self.get_tree_recursive(repo, ref)
        normalized = path.replace("\\", "/")
        for entry in tree:
            if str(entry.get("type") or "") == "blob" and str(entry.get("path") or "").replace("\\", "/") == normalized:
                return self.get_blob_text(repo, str(entry.get("sha") or ""))
        return None

    def stats(self) -> dict[str, int]:
        stats = self.stats_data.as_dict()
        stats["tree_cache_hit_count"] = self.tree_cache_hit_count
        stats["in_memory_blob_cache_hit_count"] = self.in_memory_blob_cache_hit_count
        stats["singleflight_wait_count"] = self.singleflight_wait_count
        return stats


class AutoDocumentBackendClient:
    def __init__(self, *, rest_client: Any, local_backend: LocalGitDocumentBackend | None = None, mode: str = "rest") -> None:
        self.rest_client = rest_client
        self.local_backend = local_backend
        self.mode = mode
        self.profiler = getattr(rest_client, "profiler", None)
        self.rest_fallback_count = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self.rest_client, name)

    def get_pull(self, repo: str, pr_number: int) -> dict[str, Any]:
        return self.rest_client.get_pull(repo, pr_number)

    def get_pull_files(self, repo: str, pr_number: int) -> list[dict[str, Any]]:
        return self.rest_client.get_pull_files(repo, pr_number)

    def get_tree_recursive(self, repo: str, ref: str) -> list[dict[str, Any]]:
        if self.mode == "rest":
            return self.rest_client.get_tree_recursive(repo, ref)
        if self.mode == "auto" and hasattr(self.rest_client, "get_cached_tree_recursive"):
            cached = self.rest_client.get_cached_tree_recursive(repo, ref)
            if cached is not None:
                return cached
        if self.local_backend is not None:
            try:
                return self.local_backend.get_tree_recursive(repo, ref)
            except Exception:
                if self.mode == "local-git":
                    raise
                self.rest_fallback_count += 1
        return self.rest_client.get_tree_recursive(repo, ref)

    def get_blob_text(self, repo: str, blob_sha: str) -> str | None:
        if self.mode == "rest":
            return self.rest_client.get_blob_text(repo, blob_sha)
        if self.mode == "auto" and hasattr(self.rest_client, "get_cached_blob_text"):
            cached = self.rest_client.get_cached_blob_text(repo, blob_sha)
            if cached is not None:
                return cached
        if self.local_backend is not None:
            try:
                return self.local_backend.get_blob_text(repo, blob_sha)
            except Exception:
                if self.mode == "local-git":
                    raise
                self.rest_fallback_count += 1
        return self.rest_client.get_blob_text(repo, blob_sha)

    def get_file_text(self, repo: str, path: str, ref: str) -> str | None:
        if self.mode == "rest":
            return self.rest_client.get_file_text(repo, path, ref)
        if self.mode == "auto" and hasattr(self.rest_client, "get_cached_file_text"):
            cached = self.rest_client.get_cached_file_text(repo, path, ref)
            if cached is not None:
                return cached
        if self.local_backend is not None:
            try:
                return self.local_backend.get_file_text(repo, path, ref)
            except Exception:
                if self.mode == "local-git":
                    raise
                self.rest_fallback_count += 1
        return self.rest_client.get_file_text(repo, path, ref)

    def stats(self) -> dict[str, Any]:
        stats = dict(self.rest_client.stats())
        stats["rest_fallback_count"] = self.rest_fallback_count
        if self.local_backend is not None:
            stats.update(self.local_backend.stats())
        return stats
