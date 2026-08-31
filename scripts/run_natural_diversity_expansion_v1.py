"""Natural Diversity Expansion V1 orchestration helpers.

This module deliberately separates repository discovery from acquisition.  The
discovery stage only uses repository metadata and documentation *path names*;
it never reads labels, docs-after, patch outcomes, or confirmation examples.
It creates a reviewable repository shortlist checkpoint before any GitHub PR
acquisition is attempted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ORIGIN = "natural_diversity_expansion_v1"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/final_v2/natural_diversity_expansion_v1"
FORBIDDEN_PATH_PARTS = {"confirmation", "docs_after", "outcome", "predictions"}
SURFACE_TERMS = {
    "developer_setup": ("install", "installation", "setup", "getting-started", "development", "build", "contributing"),
    "model_contract": ("schema", "model", "types", "type", "interface", "dto", "entity", "serialization", "openapi"),
    "configuration": ("config", "configuration", "settings", "environment", "options", "flags", "deployment"),
    "api_reference": ("api", "endpoint", "reference", "sdk", "client", "webhook", "graphql"),
}

# Curated, public, documentation-rich candidates.  They are only candidates;
# the API metadata and seen-universe audit decide eligibility.
CURATED_REPOSITORIES = [
    "pallets/flask", "psf/requests", "pytest-dev/pytest", "python-poetry/poetry",
    "pre-commit/pre-commit", "cookiecutter/cookiecutter", "tox-dev/tox", "noxflow/nox",
    "encode/httpx", "encode/starlette", "celery/celery", "locustio/locust",
    "sanic-org/sanic", "marshmallow-code/marshmallow", "joke2k/faker", "jazzband/pip-tools",
    "django/django", "pydantic/pydantic", "jupyter/notebook", "kedro-org/kedro",
    "vitejs/vite", "eslint/eslint", "prettier/prettier", "vitest-dev/vitest",
    "pnpm/pnpm", "changesets/changesets", "nestjs/nest", "prisma/prisma",
    "reduxjs/redux-toolkit", "TanStack/query", "storybookjs/storybook", "sveltejs/svelte",
    "remix-run/react-router", "vercel/next.js", "nuxt/nuxt", "vuejs/core",
    "DefinitelyTyped/DefinitelyTyped", "open-telemetry/opentelemetry-js",
    "grpc/grpc", "rust-lang/cargo", "astral-sh/ty", "astral-sh/ruff",
    "pypa/pip", "packaging/python-packaging", "dagster-io/dagster",
    "pallets/click", "pallets/werkzeug", "scikit-learn/scikit-learn", "numpy/numpy",
    "pandas-dev/pandas", "matplotlib/matplotlib", "sympy/sympy", "fastapi/fastapi",
    "sqlalchemy/sqlalchemy", "pytest-dev/pluggy", "hynek/structlog", "httpie/cli",
    "explosion/spaCy", "ray-project/ray", "prefecthq/prefect", "dask/dask",
    "streamlit/streamlit", "microsoft/pyright", "denoland/deno", "oven-sh/bun",
    "vercel/turbo", "remix-run/remix", "tailwindlabs/tailwindcss", "angular/angular-eslint",
    "open-telemetry/opentelemetry-js-contrib", "graphql/graphql-js", "apollographql/apollo-client",
    "facebook/react", "jestjs/jest", "webpack/webpack", "rollup/rollup", "yarnpkg/berry",
    "sindresorhus/ky", "nodejs/node", "microsoft/TypeScript", "storybookjs/storybook",
    "jupyterlab/jupyterlab", "openstack/openstacksdk", "ansible/ansible-runner", "cortexlabs/cortex",
    "pypa/hatch", "pypa/build", "pypa/twine", "pypa/virtualenv", "pytest-dev/pytest-cov",
    "pytest-dev/pytest-xdist", "encode/uvicorn", "python-trio/trio", "python/mypy",
    "pypa/pipx", "sphinx-doc/sphinx", "readthedocs/readthedocs.org", "mkdocs/mkdocs",
    "mkdocs-material/mkdocs-material", "pallets/jinja", "python-hyper/hypercorn",
    "textualize/textual", "Textualize/rich", "litestar-org/litestar", "sqlmodel/sqlmodel",
    "microsoft/playwright", "puppeteer/puppeteer", "cypress-io/cypress", "rushstack/rushstack",
    "nrwl/nx", "ionic-team/ionic-framework", "vuejs/pinia", "vuejs/vitepress", "unjs/unbuild",
    "unjs/nitro", "unjs/h3", "withastro/astro", "solidjs/solid", "sveltejs/kit",
    "denoland/fresh", "socketio/socket.io", "nodejs/undici", "expressjs/express",
    "fastify/fastify", "honojs/hono", "type-challenges/type-challenges", "open-telemetry/opentelemetry-js",
]


def norm_repo(value: Any) -> str:
    cleaned = str(value or "").strip().lower().removeprefix("https://github.com/").strip("/")
    return cleaned.removesuffix(".git").strip("/")


def forbidden_path(path: Path) -> bool:
    lowered = str(path).replace("\\", "/").lower()
    return any(part in lowered for part in FORBIDDEN_PATH_PARTS)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def extract_repositories_from_json(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {"repository", "repo", "full_name", "repository_name"} and isinstance(item, str):
                candidate = norm_repo(item)
                if re.fullmatch(r"[^/\s]+/[^/\s]+", candidate):
                    found.add(candidate)
            found.update(extract_repositories_from_json(item))
    elif isinstance(value, list):
        for item in value:
            found.update(extract_repositories_from_json(item))
    return found


def build_seen_universe() -> tuple[set[str], dict[str, list[str]]]:
    """Build a conservative repository universe without opening confirmation rows."""
    seen: set[str] = set()
    sources: dict[str, list[str]] = defaultdict(list)

    # The sealed partition manifest is metadata-only and gives the historical
    # confirmation repository set without reading the confirmation dataset.
    partition_manifest = ROOT / "data/final_v2/partitions/canonical_repository_partitions/repository_partition_manifest.json"
    if partition_manifest.exists():
        payload = load_json(partition_manifest)
        for repo in (payload.get("repository_assignments") or {}):
            repo = norm_repo(repo)
            if repo:
                seen.add(repo)
                sources[repo].append("sealed_repository_partition_manifest")

    # The canonical repository universe and partition manifest already cover
    # the full current natural corpus.  Restrict the supplemental scan to
    # lightweight repository manifests/lists; parsing every review JSONL would
    # unnecessarily load large diffs and could accidentally touch sealed data.
    roots = [ROOT / "data/final_v2/repository_universe", ROOT / "data/final_v2/expansion", ROOT / "data/final_v2/controlled_synthetic_positive_v1/repository_selection"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or forbidden_path(path):
                continue
            if path.suffix.lower() not in {".json", ".jsonl", ".txt"}:
                continue
            # Avoid recursively reading this expansion's own generated files.
            if OUT in path.parents:
                continue
            # Do not inspect candidate/review content.  Repository discovery
            # is intentionally metadata-only and source lists are sufficient.
            name = path.name.lower()
            rel_lower = str(path.relative_to(ROOT)).replace("\\", "/").lower()
            # Only repository-universe/discovery manifests and explicit repo
            # lists are supplemental sources.  This avoids loading thousands
            # of review rows and patch excerpts.
            allowed = ("repository_universe" in rel_lower or "repository_discovery" in rel_lower or "selected_repositories" in name or "explicit_repository_universe" in name)
            if not allowed:
                continue
            if any(fragment in name for fragment in ("candidate", "review", "batch", "seed", "patch", "prediction", "original_repository_pr_keys")):
                continue
            try:
                if path.suffix.lower() == ".jsonl":
                    rows = []
                    with path.open(encoding="utf-8") as handle:
                        for line in handle:
                            if line.strip():
                                try:
                                    rows.append(json.loads(line))
                                except json.JSONDecodeError:
                                    continue
                    repos = set().union(*(extract_repositories_from_json(row) for row in rows)) if rows else set()
                elif path.suffix.lower() == ".json":
                    repos = extract_repositories_from_json(load_json(path))
                else:
                    repos = set()
                    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                        candidate = norm_repo(line)
                        if re.fullmatch(r"[^/\s]+/[^/\s]+", candidate):
                            repos.add(candidate)
                for repo in repos:
                    seen.add(repo)
                    sources[repo].append(str(path.relative_to(ROOT)))
            except (OSError, UnicodeError, json.JSONDecodeError):
                continue
    return seen, {repo: sorted(set(items)) for repo, items in sources.items()}


class GitHubMetadata:
    def __init__(self, token: str | None, cache_dir: Path, timeout: int = 30) -> None:
        self.token = token
        self.cache_dir = cache_dir
        self.timeout = timeout
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.last_request = 0.0

    def get(self, path: str) -> tuple[dict[str, Any], dict[str, str]]:
        cache_key = hashlib.sha256(path.encode()).hexdigest() + ".json"
        cache_path = self.cache_dir / cache_key
        if cache_path.exists():
            return load_json(cache_path), {"cached": "true"}
        wait = 0.25 - (time.monotonic() - self.last_request)
        if wait > 0:
            time.sleep(wait)
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "DocGuard-Natural-Diversity-V1"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request("https://api.github.com" + path, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
                response_headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"GitHub metadata request failed for {path}: {exc}") from exc
        self.last_request = time.monotonic()
        cache_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return payload, response_headers


def docs_from_tree(tree: list[dict[str, Any]]) -> list[str]:
    patterns = re.compile(r"(^|/)(readme(?:\.[^/]*)?|contributing(?:\.[^/]*)?|development(?:\.[^/]*)?|install(?:ation)?(?:\.[^/]*)?|docs?/.*\.(?:md|mdx|rst|adoc|txt)|.*(?:api|config|schema|setup|reference|guide|types?).*\.(?:md|mdx|rst|adoc|txt))$", re.I)
    return sorted({str(item.get("path")) for item in tree if item.get("type") in {"blob", "file"} and patterns.search(str(item.get("path")))})


def profile_candidate(client: GitHubMetadata, repo: str, seen: set[str]) -> dict[str, Any] | None:
    if repo in seen:
        return None
    try:
        meta, headers = client.get(f"/repos/{urllib.parse.quote(repo, safe='/')}")
        if meta.get("fork") or meta.get("archived") or meta.get("disabled"):
            return None
        branch = str(meta.get("default_branch") or "main")
        # Use bounded root/``docs`` listings instead of recursive trees.  Some
        # very large repositories make a recursive tree request enormous and
        # discovery must remain a lightweight pre-acquisition checkpoint.
        root_payload, _ = client.get(f"/repos/{urllib.parse.quote(repo, safe='/')}/contents?ref={urllib.parse.quote(branch, safe='')}" )
        root_items = root_payload if isinstance(root_payload, list) else []
        tree = [{"type": item.get("type"), "path": item.get("path")} for item in root_items]
        for dirname in ("docs",):
            try:
                child_payload, _ = client.get(f"/repos/{urllib.parse.quote(repo, safe='/')}/contents/{dirname}?ref={urllib.parse.quote(branch, safe='')}" )
            except RuntimeError:
                continue
            if isinstance(child_payload, list):
                tree.extend({"type": item.get("type"), "path": f"{dirname}/{item.get('path')}"} for item in child_payload[:200])
        doc_files = docs_from_tree(tree)
        if len(doc_files) < 4:
            return None
        lower_paths = " ".join(doc_files).lower()
        signals = {surface: sum(term in lower_paths for term in terms) for surface, terms in SURFACE_TERMS.items()}
        covered = [surface for surface, count in signals.items() if count]
        if len(covered) < 2:
            return None
        language = str(meta.get("language") or "").lower()
        if language not in {"python", "javascript", "typescript"}:
            return None
        if language in {"javascript", "typescript"}:
            language_group = "typescript_javascript"
        else:
            language_group = language
        likely_surface = max(signals, key=lambda key: (signals[key], key))
        return {
            "repository": repo,
            "language": language,
            "language_group": language_group,
            "default_branch": branch,
            "stars": int(meta.get("stargazers_count") or 0),
            "forks": int(meta.get("forks_count") or 0),
            "size_kb": int(meta.get("size") or 0),
            "open_issues_count": int(meta.get("open_issues_count") or 0),
            "pushed_at": meta.get("pushed_at"),
            "documentation_file_count": len(doc_files),
            "documentation_files_sample": doc_files[:40],
            "documentation_surface_signals": signals,
            "surface_coverage": len(covered),
            "likely_surface_for_pilot": likely_surface,
            "expected_pr_volume_proxy": int(meta.get("open_issues_count") or 0),
            "metadata_cached": headers.get("cached") == "true",
            "acquisition_origin": ORIGIN,
            "selection_uses_labels": False,
        }
    except RuntimeError:
        return None


def select_shortlist(rows: list[dict[str, Any]], *, python_target: int = 10, ts_target: int = 10) -> list[dict[str, Any]]:
    rows = [row for row in rows if int(row.get("expected_pr_volume_proxy") or 0) >= 5]
    rows = sorted(rows, key=lambda row: (row["surface_coverage"], row["expected_pr_volume_proxy"], row["documentation_file_count"], row["stars"]), reverse=True)
    selected: list[dict[str, Any]] = []
    owners: Counter[str] = Counter()
    counts: Counter[str] = Counter()
    targets = {"python": python_target, "typescript_javascript": ts_target}
    for row in rows:
        group = row["language_group"]
        if counts[group] >= targets.get(group, 0):
            continue
        owner = row["repository"].split("/", 1)[0]
        if owners[owner] >= 2:
            continue
        row = dict(row)
        row["shortlist_rank"] = len(selected) + 1
        row["owner_cap_applied"] = 2
        selected.append(row)
        owners[owner] += 1
        counts[group] += 1
        if all(counts[group] >= targets[group] for group in targets):
            break
    return selected


def search_repository_names(client: GitHubMetadata, *, limit_per_language: int) -> list[str]:
    names: list[str] = []
    for language in ("python", "typescript"):
        query = urllib.parse.urlencode({"q": f"language:{language} stars:100..100000 fork:false archived:false size:<150000", "sort": "updated", "order": "desc", "per_page": min(limit_per_language, 100), "page": 1})
        try:
            payload, _ = client.get("/search/repositories?" + query)
        except RuntimeError:
            continue
        for item in payload.get("items", []) if isinstance(payload, dict) else []:
            repo = norm_repo(item.get("full_name")) if isinstance(item, dict) else ""
            if repo:
                names.append(repo)
    return names


def write_checkpoint(out: Path, *, seen: set[str], sources: dict[str, list[str]], candidates: list[dict[str, Any]], selected: list[dict[str, Any]], token_present: bool) -> None:
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "seen_repository_universe.json", {"repository_count": len(seen), "repositories": sorted(seen), "sources": sources, "confirmation_rows_accessed": False, "confirmation_examples_accessed": False})
    write_jsonl(out / "repository_profile_candidates.jsonl", candidates)
    write_json(out / "repository_overlap_audit.json", {"seen_repository_count": len(seen), "candidate_count": len(candidates), "selected_count": len(selected), "selected_overlap_count": sum(row["repository"] in seen for row in selected), "selected_repositories": [row["repository"] for row in selected], "overlap_policy": "reject_any_seen_repository", "confirmation_examples_accessed": False})
    write_jsonl(out / "repository_shortlist.jsonl", selected)
    write_json(out / "discovery_manifest.json", {"schema": "natural_diversity_expansion_v1_repository_discovery", "acquisition_origin": ORIGIN, "created_at": datetime.now(UTC).replace(microsecond=0).isoformat(), "seen_repository_count": len(seen), "candidate_profile_count": len(candidates), "selected_count": len(selected), "language_counts": dict(Counter(row["language_group"] for row in selected)), "surface_counts_by_signal": {surface: sum(bool(row["documentation_surface_signals"].get(surface)) for row in selected) for surface in SURFACE_TERMS}, "token_present_for_future_acquisition": token_present, "confirmation_accessed": False, "selection_fields_forbidden": ["human_label", "gold_label", "docs_after", "docs_diff", "outcome", "predictions"], "next_step": "authenticated_seed_collection_after_shortlist_review"})
    lines = ["# Checkpoint 01 — Natural Diversity Expansion V1 repository shortlist", "", f"Created: `{datetime.now(UTC).replace(microsecond=0).isoformat()}`", "", f"- Previously-seen repository universe: **{len(seen):,}**", f"- Metadata-profiled new candidates: **{len(candidates):,}**", f"- Selected shortlist: **{len(selected):,}**", f"- GITHUB_TOKEN present for acquisition: **{token_present}**", "- Confirmation examples accessed: **False**", "- Labels/outcomes/docs-after used for selection: **False**", "", "## Selected repositories", "", "| # | Repository | Language | Stars | Docs files | Covered surfaces | Likely pilot surface | PR-volume proxy |", "|---:|---|---|---:|---:|---|---|---:|"]
    for row in selected:
        covered = ", ".join(surface for surface, count in row["documentation_surface_signals"].items() if count)
        lines.append(f"| {row['shortlist_rank']} | `{row['repository']}` | {row['language']} | {row['stars']:,} | {row['documentation_file_count']} | {covered} | {row['likely_surface_for_pilot']} | {row['expected_pr_volume_proxy']:,} |")
    gate = "PASS — shortlist is ready for authenticated acquisition" if len(selected) >= 15 and token_present else "BLOCKED — do not start acquisition until at least 15 new repositories are profiled and an authenticated token is available"
    lines += ["", "## Gate", "", f"**{gate}.**", "", "This is a pre-acquisition checkpoint. No repository was cloned, no PR seed was downloaded, and no candidate was labeled. Acquisition must use authenticated, rate-limited BASE-SHA retrieval and preserve scientific rejects separately from operational pending."]
    (out / "CHECKPOINT_01_REPOSITORY_SHORTLIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def discover(args: argparse.Namespace) -> int:
    seen, sources = build_seen_universe()
    out = Path(args.output_dir)
    cache_dir = out / "discovery_cache"
    token = os.getenv(args.github_token_env) or None
    client = GitHubMetadata(token, cache_dir, args.timeout_seconds)
    candidates: list[dict[str, Any]] = []
    seen_candidate_names: set[str] = set()
    search_names = search_repository_names(client, limit_per_language=args.search_limit)
    # Curated names improve reproducibility; a bounded, cached search widens
    # diversity when the historical universe already contains popular stars.
    raw_names = list(CURATED_REPOSITORIES) + search_names
    for raw in raw_names:
        repo = norm_repo(raw)
        if not repo or repo in seen or repo in seen_candidate_names or " " in repo:
            continue
        seen_candidate_names.add(repo)
        profiled = profile_candidate(client, repo, seen)
        if profiled:
            candidates.append(profiled)
    selected = select_shortlist(candidates, python_target=args.python_target, ts_target=args.ts_target)
    write_checkpoint(out, seen=seen, sources=sources, candidates=candidates, selected=selected, token_present=bool(token))
    print(json.dumps({"status": "ok", "seen_repositories": len(seen), "profiled_candidates": len(candidates), "selected": [row["repository"] for row in selected], "token_present": bool(token), "checkpoint": str(out / "CHECKPOINT_01_REPOSITORY_SHORTLIST.md")}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover and checkpoint unseen repositories for Natural Diversity Expansion V1.")
    parser.add_argument("discover", nargs="?", default="discover")
    parser.add_argument("--output-dir", default=str(OUT))
    parser.add_argument("--github-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--python-target", type=int, default=10)
    parser.add_argument("--ts-target", type=int, default=10)
    parser.add_argument("--search-limit", type=int, default=40, help="Bounded GitHub search results per language used for metadata-only discovery.")
    args = parser.parse_args()
    if args.discover != "discover":
        parser.error("only the discover stage is available before checkpoint 01")
    return discover(args)


if __name__ == "__main__":
    raise SystemExit(main())
