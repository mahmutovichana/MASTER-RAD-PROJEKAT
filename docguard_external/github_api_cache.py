from __future__ import annotations

import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any


class GitHubApiCache:
    """
    Small filesystem JSON cache for GitHub API GET responses.

    This is dataset infrastructure only:
    - prevents repeated API calls for the same URL,
    - enables resumable dataset construction,
    - reduces GitHub rate-limit pressure.

    It does not assign labels and it is not a model/rule detector.
    """

    def __init__(self, cache_dir: Path | str) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _key(self, url: str, *, accept: str) -> str:
        raw = json.dumps(
            {
                "url": url,
                "accept": accept,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _path(self, url: str, *, accept: str) -> Path:
        key = self._key(url, accept=accept)
        prefix = key[:2]
        directory = self.cache_dir / prefix
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{key}.json"

    def get_json(self, url: str, *, accept: str) -> Any | None:
        path = self._path(url, accept=accept)

        if not path.exists():
            return None

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

        if not isinstance(payload, dict):
            return None

        if payload.get("schema") != "docguard_github_api_cache_v1":
            return None

        return payload.get("data")

    def has_json(self, url: str, *, accept: str) -> bool:
        return self._path(url, accept=accept).exists()

    def set_json(self, url: str, data: Any, *, accept: str) -> None:
        path = self._path(url, accept=accept)

        payload = {
            "schema": "docguard_github_api_cache_v1",
            "created_at_unix": time.time(),
            "url": url,
            "accept": accept,
            "data": data,
        }

        with self._lock:
            temp_path = path.with_suffix(f".{threading.get_ident()}.tmp")
            temp_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            temp_path.replace(path)

    def stats(self) -> dict[str, Any]:
        files = list(self.cache_dir.glob("*/*.json"))
        total_bytes = sum(path.stat().st_size for path in files if path.exists())

        return {
            "cache_dir": str(self.cache_dir),
            "cached_json_files": len(files),
            "approx_bytes": total_bytes,
        }
