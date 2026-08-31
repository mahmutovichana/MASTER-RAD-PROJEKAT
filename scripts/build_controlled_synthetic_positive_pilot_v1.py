from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tomllib
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(r"C:\Users\mahmu\Desktop\controlled_synthetic_repo_cache_v1")
OUT = ROOT / "data/final_v2/controlled_synthetic_positive_v1"
REPOS = [
    ("pallets/flask", "python", "pallets__flask", "src/flask/app.py"),
    ("encode/httpx", "python", "encode__httpx", "httpx/_config.py"),
    ("pydantic/pydantic", "python", "pydantic__pydantic", "pydantic/main.py"),
    ("pytest-dev/pytest", "python", "pytest-dev__pytest", "src/_pytest/config/argparsing.py"),
    ("remix-run/react-router", "typescript", "remix-run__react-router", "packages/react-router/package.json"),
    ("koajs/koa", "javascript", "koajs__koa", "lib/application.js"),
    ("hapijs/hapi", "javascript", "hapijs__hapi", "lib/server.js"),
    ("trpc/trpc", "typescript", "trpc__trpc", "packages/server/src/unstable-core-do-not-import/procedureBuilder.ts"),
]
CATEGORY_TERMS = {
    "api_reference": ["api", "client", "request", "response", "endpoint", "route", "method"],
    "configuration": ["config", "configuration", "timeout", "default", "port", "environment", "settings"],
    "developer_setup": ["install", "installation", "setup", "getting started", "run", "build", "node", "python"],
    "model_contract": ["schema", "model", "payload", "field", "type", "interface", "object", "data"],
}


def run(*args: str, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def read_docs(repo: Path) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for path in repo.rglob("*"):
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        if path.suffix.lower() not in {".md", ".mdx", ".rst", ".txt"} and path.name.lower() not in {"readme", "readme.md", "readme.rst"}:
            continue
        rel = path.relative_to(repo).as_posix()
        if any(part in {"node_modules", ".git", "dist", "build"} for part in path.parts):
            continue
        try:
            docs.append((rel, path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            pass
    return docs


def choose_doc(docs: list[tuple[str, str]], category: str) -> tuple[str, str] | None:
    terms = CATEGORY_TERMS[category]
    ranked: list[tuple[int, str, str]] = []
    for path, text in docs:
        lower = text.lower()
        score = sum(lower.count(term) for term in terms)
        if path.lower().startswith("readme"):
            score += 2
        if score:
            ranked.append((score, path, text))
    if not ranked:
        return None
    _, path, text = max(ranked, key=lambda item: (item[0], -len(item[1])))
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if any(term in line.lower() for term in terms)]
    start = max(0, (hits[0] if hits else 0) - 3)
    return path, "\n".join(lines[start : start + 24])[:8000]


def mutate(original: str, category: str, variant: int, language: str) -> tuple[str, str] | None:
    if category == "developer_setup":
        patterns = [
            (r"requires-python\s*=\s*(['\"])(>=)(3\.\d+)\1", lambda m: f"requires-python = {m.group(1)}{m.group(2)}3.{int(m.group(3).split('.')[-1]) + variant % 3 + 1}{m.group(1)}"),
            (r'"node"\s*:\s*"(>=?\s*)(\d+)', lambda m: f'"node": "{m.group(1)}{int(m.group(2)) + 1 + variant % 3}'),
        ]
        for pattern, repl in patterns:
            changed, count = re.subn(pattern, repl, original, count=1)
            if count:
                return changed, "The supported runtime/setup requirement is raised while the BASE documentation remains unchanged."
        changed, count = re.subn(r'("(start|dev|build)"\s*:\s*")([^"\n]+)', lambda m: m.group(1) + m.group(3) + f"-synthetic-{variant}", original, count=1)
        if count:
            return changed, "The documented development command is changed in the project manifest while setup docs remain unchanged."

    if category == "configuration":
        def bump(match: re.Match[str]) -> str:
            value = match.group(1)
            try:
                return match.group(0).replace(value, str(float(value) + 1 + variant % 4))
            except ValueError:
                return match.group(0)
        for line in original.splitlines(keepends=True):
            if re.search(r"timeout|default|port|config|setting", line, re.I) and re.search(r"\b\d+(?:\.\d+)?\b", line):
                changed_line = re.sub(r"\b(\d+(?:\.\d+)?)\b", bump, line, count=1)
                if changed_line != line:
                    return original.replace(line, changed_line, 1), "A documented configuration default is changed in executable/configuration source while docs remain unchanged."

    if category == "api_reference":
        if language == "python":
            changed, count = re.subn(r"^([ \t]*def\s+[A-Za-z_]\w*\([^\n]*)(\):)", lambda m: m.group(1).rstrip(" )") + f", synthetic_option_{variant}: object | None = None" + m.group(2), original, count=1, flags=re.M)
            if count:
                return changed, "A new optional public callable parameter is added to the API signature while the API documentation remains unchanged."
        changed, count = re.subn(r"(function\s+[A-Za-z_]\w*\s*\([^\n]*)\)", lambda m: m.group(1) + f", syntheticOption{variant} = undefined)", original, count=1)
        if count:
            return changed, "A new optional public function parameter is added while the API documentation remains unchanged."

    if category == "model_contract":
        if language == "python":
            changed, count = re.subn(r"^(\s*class\s+[A-Za-z_]\w*\([^\n]*\):\s*$)", lambda m: m.group(1) + f"\n    synthetic_field_{variant}: str | None = None", original, count=1, flags=re.M)
            if count:
                return changed, "A serialized model field is added to a real model/class while the model documentation remains unchanged."
        changed, count = re.subn(r"^(\s*(?:export\s+)?(?:interface|type)\s+[A-Za-z_]\w*[^\n]*\{\s*$)", lambda m: m.group(1) + f"\n  syntheticField{variant}?: string;", original, count=1, flags=re.M)
        if count:
            return changed, "A field is added to a real public TypeScript contract while the schema documentation remains unchanged."
    return None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "repository_selection").mkdir(exist_ok=True)
    selected: list[dict] = []
    candidates: list[dict] = []
    rejects: list[dict] = []
    repo_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"accepted": 0, "rejected": 0})
    for repository, language, dirname, code_rel in REPOS:
        repo = CACHE / dirname
        base_sha = run("rev-parse", "HEAD", cwd=repo)
        docs = read_docs(repo)
        doc_paths = [path for path, _ in docs]
        selected.append({
            "repository": repository,
            "base_sha": base_sha,
            "language": language,
            "documentation_files": doc_paths[:200],
            "why_selected": "Active, non-archived, documented open-source project with a public source tree and setup/API/data-surface documentation.",
            "candidate_surfaces": ["api_reference", "configuration", "developer_setup", "model_contract"],
        })
        code_path = repo / code_rel
        if not code_path.exists():
            rejects.append({"repository": repository, "reason": "configured_code_target_missing", "code_path": code_rel})
            continue
        base_text = code_path.read_text(encoding="utf-8", errors="ignore")
        for category in ["api_reference", "configuration", "developer_setup", "model_contract"]:
            chosen_doc = choose_doc(docs, category)
            if not chosen_doc:
                for variant in range(1, 26):
                    rejects.append({"repository": repository, "category": category, "variant": variant, "reason": "no_documentation_evidence_candidate"})
                continue
            doc_path, doc_excerpt = chosen_doc
            target_path = code_path
            target_rel = code_rel
            if category == "developer_setup":
                setup_candidates = [repo / "pyproject.toml", repo / "package.json"]
                target_path = next((path for path in setup_candidates if path.exists()), code_path)
                target_rel = target_path.relative_to(repo).as_posix()
            target_text = target_path.read_text(encoding="utf-8", errors="ignore")
            for variant in range(1, 26):
                mutation = mutate(target_text, category, variant, language)
                if mutation is None:
                    rejects.append({"repository": repository, "category": category, "variant": variant, "reason": "no_safe_mutation_template"})
                    continue
                mutated, rationale = mutation
                if mutated == target_text:
                    rejects.append({"repository": repository, "category": category, "variant": variant, "reason": "empty_diff"})
                    continue
                target_path.write_text(mutated, encoding="utf-8", newline="\n")
                syntax_status = "not_run"
                if target_path.suffix == ".py":
                    check = subprocess.run(["python", "-m", "py_compile", str(target_path)], cwd=repo, capture_output=True, text=True)
                    syntax_status = "pass" if check.returncode == 0 else "fail"
                elif target_path.suffix == ".json":
                    try:
                        json.loads(target_path.read_text(encoding="utf-8"))
                        syntax_status = "pass"
                    except json.JSONDecodeError:
                        syntax_status = "fail"
                elif target_path.name == "pyproject.toml":
                    try:
                        with target_path.open("rb") as handle:
                            tomllib.load(handle)
                        syntax_status = "pass"
                    except (tomllib.TOMLDecodeError, OSError):
                        syntax_status = "fail"
                if syntax_status == "fail":
                    rejects.append({"repository": repository, "category": category, "variant": variant, "reason": "syntax_validation_failed"})
                    run("reset", "--hard", base_sha, cwd=repo)
                    continue
                run("add", "--", target_rel, cwd=repo)
                run("-c", "user.name=DocGuard Synthetic Builder", "-c", "user.email=synthetic@docguard.invalid", "commit", "-m", f"synthetic {category} case {variant}", cwd=repo)
                head_sha = run("rev-parse", "HEAD", cwd=repo)
                diff = run("diff", "--no-ext-diff", "--unified=3", f"{base_sha}..{head_sha}", cwd=repo)
                run("reset", "--hard", base_sha, cwd=repo)
                if not diff.strip() or "docs/" in diff.lower() and target_rel.lower().startswith("docs/"):
                    rejects.append({"repository": repository, "category": category, "variant": variant, "reason": "invalid_or_docs_diff"})
                    continue
                case_id = f"synthetic:{repository}:{category}:{variant}"
                candidates.append({
                    "case_id": case_id,
                    "repository": repository,
                    "language": language,
                    "pr_number": 900000 + len(candidates) + 1,
                    "code_changed_files": [target_rel],
                    "code_diff_excerpt": diff[:30000],
                    "docs_before_excerpt": doc_excerpt,
                    "docs_before_retrieved_files": [doc_path],
                    "documentation_context_candidates": [{"path": doc_path, "excerpt": doc_excerpt}],
                    "case_origin": "controlled_synthetic_positive_v1",
                    "acquisition_origin": "controlled_synthetic_positive_v1",
                    "synthetic_case": True,
                    "synthetic_generation_method": "real_repo_controlled_code_mutation",
                    "synthetic_base_sha": base_sha,
                    "synthetic_head_sha": head_sha,
                    "synthetic_category_by_design": category,
                    "synthetic_target_doc_path": doc_path,
                    "synthetic_target_doc_excerpt": doc_excerpt,
                    "synthetic_evidence_quote": doc_excerpt[:500],
                    "synthetic_change_rationale": rationale,
                    "synthetic_validation_status": "pre_review_pass",
                    "synthetic_syntax_validation": syntax_status,
                })
                repo_stats[repository]["accepted"] += 1

    # Keep the pilot contract exact: at most 50 accepted cases per design category.
    selected_candidates: list[dict] = []
    by_category: dict[str, int] = defaultdict(int)
    # Fill each design category in repository-round-robin order so the pilot
    # does not silently collapse onto the first repository in REPOS.
    selected_repo_names = [row["repository"] for row in selected]
    for category in ["api_reference", "configuration", "developer_setup", "model_contract"]:
        pool = [candidate for candidate in candidates if candidate["synthetic_category_by_design"] == category]
        for repository in selected_repo_names:
            for candidate in [item for item in pool if item["repository"] == repository]:
                if by_category[category] >= 50:
                    break
                selected_candidates.append(candidate)
                by_category[category] += 1
        if by_category[category] < 50:
            rejects.extend({"case_id": candidate["case_id"], "reason": "pilot_category_cap_50"} for candidate in pool if candidate not in selected_candidates)
    selected_ids = {candidate["case_id"] for candidate in selected_candidates}
    for candidate in candidates:
        if candidate["case_id"] not in selected_ids and not any(candidate["case_id"] == row.get("case_id") for row in rejects):
            rejects.append({"case_id": candidate["case_id"], "reason": "pilot_category_cap_50"})
    candidates = selected_candidates

    write_jsonl(OUT / "repository_selection/selected_repositories.jsonl", selected)
    (OUT / "repository_selection/selected_repositories.txt").write_text("\n".join(row["repository"] for row in selected) + "\n", encoding="utf-8")
    (OUT / "repository_selection/selection_report.md").write_text(
        "# Controlled Synthetic Positive Pilot — Repository Selection\n\n"
        "Eight active, documented repositories were selected outside the consolidated corpus (four Python and four TypeScript/JavaScript). Shallow BASE snapshots are kept outside the project repository cache.\n\n"
        + "\n".join(f"- `{row['repository']}` — `{row['language']}` — BASE `{row['base_sha']}`" for row in selected)
        + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUT / "cases/synthetic_candidates.jsonl", candidates)
    write_jsonl(OUT / "cases/synthetic_rejects.jsonl", rejects)
    provenance = {"case_origin": "controlled_synthetic_positive_v1", "synthetic_case": True, "candidate_count": len(candidates), "repo_count": len(selected)}
    (OUT / "reports/provenance_manifest.json").parent.mkdir(parents=True, exist_ok=True)
    (OUT / "reports/provenance_manifest.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    summary = {
        "selected_repositories": [row["repository"] for row in selected],
        "selected_count": len(selected),
        "candidate_count": len(candidates),
        "reject_count": len(rejects),
        "category_counts": dict(Counter(row["synthetic_category_by_design"] for row in candidates)),
        "language_counts": dict(Counter(row["language"] for row in candidates)),
        "repository_counts": {name: dict(values) for name, values in repo_stats.items()},
        "sha256_candidates": hashlib.sha256((OUT / "cases/synthetic_candidates.jsonl").read_bytes()).hexdigest(),
        "sha256_selected": hashlib.sha256((OUT / "repository_selection/selected_repositories.jsonl").read_bytes()).hexdigest(),
    }
    (OUT / "reports/pilot_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "reports/pilot_summary.md").write_text("# Controlled Synthetic Positive Pilot v1\n\n" + "\n".join(f"- {key}: `{value}`" for key, value in summary.items()), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
