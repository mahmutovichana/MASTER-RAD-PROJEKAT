from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LANGUAGES = ["python", "typescript"]
STAR_STRATA = {
    "medium_100_999": "stars:100..999",
    "large_1000_9999": "stars:1000..9999",
    "very_large_10000_plus": "stars:>=10000",
}


class GitHubSearchClient:
    def __init__(self, token: str | None = None, timeout_seconds: int = 30) -> None:
        self.token = token
        self.timeout_seconds = timeout_seconds

    def search_repositories(self, query: str, *, page: int, per_page: int) -> list[dict[str, Any]]:
        url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
            {"q": query, "sort": "updated", "order": "desc", "per_page": per_page, "page": page}
        )
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "DocGuard-Final-V2-Repo-Discovery"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} from GitHub search: {body[:1000]}") from exc
        items = payload.get("items") if isinstance(payload, dict) else None
        return [item for item in items or [] if isinstance(item, dict)]


def eligible_repo(item: dict[str, Any]) -> bool:
    if item.get("fork") or item.get("archived") or item.get("disabled"):
        return False
    if not item.get("pushed_at") or not item.get("updated_at"):
        return False
    if not item.get("full_name"):
        return False
    return True


def normalize_repo(item: dict[str, Any], *, language: str, query: str, stratum: str, rank: int, discovered_at: str) -> dict[str, Any]:
    return {
        "repo": str(item.get("full_name")),
        "language_hint": language,
        "stars": int(item.get("stargazers_count") or 0),
        "fork": bool(item.get("fork")),
        "archived": bool(item.get("archived")),
        "disabled": bool(item.get("disabled")),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
        "discovery_query": query,
        "discovery_stratum": stratum,
        "discovery_rank": rank,
        "discovered_at": discovered_at,
        "provenance": ["discovered_repository_universe_v2"],
    }


def discover(client: Any, *, per_language_target: int, per_page: int, max_pages: int, discovered_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    queries: list[dict[str, str]] = []
    duplicates_removed = 0
    for language in LANGUAGES:
        per_stratum_target = max(1, per_language_target // len(STAR_STRATA))
        for stratum, stars in STAR_STRATA.items():
            query = f"language:{language} {stars} fork:false archived:false"
            queries.append({"language": language, "stratum": stratum, "query": query})
            rank = 0
            accepted_for_stratum = 0
            for page in range(1, max_pages + 1):
                for item in client.search_repositories(query, page=page, per_page=per_page):
                    rank += 1
                    if not eligible_repo(item):
                        continue
                    repo = str(item.get("full_name")).lower()
                    if repo in seen:
                        duplicates_removed += 1
                        continue
                    rows.append(normalize_repo(item, language=language, query=query, stratum=stratum, rank=rank, discovered_at=discovered_at))
                    seen.add(repo)
                    accepted_for_stratum += 1
                    if accepted_for_stratum >= per_stratum_target:
                        break
                if accepted_for_stratum >= per_stratum_target:
                    break
                time.sleep(0)
    manifest = {
        "queries": queries,
        "language_strata": STAR_STRATA,
        "languages": LANGUAGES,
        "repository_count": len(rows),
        "duplicates_removed": duplicates_removed,
        "per_language_target": per_language_target,
        "per_page": per_page,
        "max_pages": max_pages,
        "github_search_timestamp": discovered_at,
    }
    return rows, manifest


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_report(path: Path, rows: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    lines = [
        "# Final V2 Repository Discovery Report",
        "",
        f"- Repository count: `{len(rows)}`",
        f"- Language counts: `{dict(Counter(row['language_hint'] for row in rows))}`",
        f"- Strata counts: `{dict(Counter(row['discovery_stratum'] for row in rows))}`",
        f"- Duplicates removed: `{manifest['duplicates_removed']}`",
        "",
        "No labels or target classes are used during repository discovery.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover reproducible Final V2 repository universe via GitHub search.")
    parser.add_argument("--output", default="data/final_v2/repository_universe/discovered_repositories_v2.jsonl")
    parser.add_argument("--manifest", default="data/final_v2/repository_universe/discovery_manifest.json")
    parser.add_argument("--report", default="reports/final_v2/repository_discovery_v2.md")
    parser.add_argument("--per-language-target", type=int, default=300)
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()
    discovered_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    client = GitHubSearchClient(os.getenv(args.github_token_env) or None, args.timeout_seconds)
    rows, manifest = discover(client, per_language_target=args.per_language_target, per_page=args.per_page, max_pages=args.max_pages, discovered_at=discovered_at)
    output = Path(args.output)
    write_jsonl(output, rows)
    manifest["sha256"] = sha256_file(output)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_report(Path(args.report), rows, manifest)
    print(json.dumps({"status": "ok", "repositories": len(rows), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
