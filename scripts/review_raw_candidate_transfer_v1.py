from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/raw_candidates_transfer_2323/raw_candidates_2323.jsonl"
OUT = ROOT / "data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/raw_candidates_transfer_2323/reviewed_from_scratch_v1"

HUMAN_FIELDS = ["human_docs_update_required", "human_doc_category", "human_label_notes", "review_status"]
GENERIC = {
    "the", "and", "or", "for", "from", "with", "this", "that", "into", "return", "class", "function", "def", "const",
    "public", "private", "protected", "static", "async", "await", "import", "export", "this", "self", "value", "values",
    "data", "item", "items", "test", "tests", "assert", "error", "errors", "result", "results", "string", "integer", "object",
    "type", "model", "models", "request", "response", "context", "client", "server", "config", "configuration", "default",
    "options", "option", "file", "files", "path", "name", "should", "have", "has", "were", "when", "then", "else", "true",
    "false", "none", "null", "change", "changed", "update", "fix", "get", "set", "make", "does", "not", "only", "use", "using",
    "new", "property", "method", "methods", "one", "two", "value", "values", "field", "fields", "handler", "handle", "close",
    "open", "read", "write", "create", "created", "remove", "removed", "add", "added", "support", "supported", "allow", "allowed",
}
TEST_MARKERS = ("test", "tests", "fixture", "snapshot", "__snapshots__", "mock", "mocks")
SETUP_MARKERS = ("pyproject.toml", "package.json", "requirements", "setup.py", "setup.cfg", "go.mod", "go.sum", "pom.xml", "build.gradle", "dockerfile", ".github/workflows", "tox.ini", "noxfile", "uv.lock")


def safe_fields(row: dict) -> tuple[str, str, list[str]]:
    safe = row.get("classifier_model_input") or {}
    return (
        str(safe.get("code_diff_excerpt") or row.get("code_diff_excerpt") or ""),
        str(safe.get("docs_before_excerpt") or row.get("docs_before_excerpt") or ""),
        list(safe.get("code_changed_files") or row.get("code_changed_files") or row.get("changed_files") or []),
    )


def changed_lines(diff: str) -> tuple[list[str], list[str]]:
    added, removed = [], []
    for line in diff.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])
    return added, removed


def distinctive_tokens(text: str) -> set[str]:
    values = set()
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_.:/-]{4,}", text):
        low = token.lower().strip("._:/-")
        if low and low not in GENERIC and not low.isdigit() and not low.startswith(("http", "synthetic")):
            values.add(low)
    return values


def doc_has(doc: str, token: str) -> bool:
    return bool(re.search(r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])", doc, re.I))


def review_one(row: dict) -> dict:
    diff, docs, files = safe_fields(row)
    docs_lower = docs.lower()
    added, removed = changed_lines(diff)
    all_changed = added + removed
    file_text = " ".join(str(path).lower() for path in files)
    if not diff.strip() or not docs.strip():
        return label(row, False, "no_update", "Evidence is empty or incomplete for a reliable docs-before decision.", "excluded")

    test_only = bool(files) and all(any(marker in path for marker in TEST_MARKERS) for path in files)
    if test_only:
        return label(row, False, "no_update", "The changed surface is limited to tests/fixtures/snapshots; no user-facing documented surface is changed.", "approved")

    added_text = "\n".join(added)
    removed_text = "\n".join(removed)
    changed_text = added_text + "\n" + removed_text
    added_names = set()
    removed_names = set()
    for text, target in ((added_text, added_names), (removed_text, removed_names)):
        for pattern in (
            r"\b(?:async\s+)?def\s+([A-Za-z_]\w*)\s*\(",
            r"\bfunc\s+([A-Za-z_]\w*)\s*\(",
            r"\bfunction\s+([A-Za-z_]\w*)\s*\(",
            r"\b(?:class|interface|struct|enum|type)\s+([A-Za-z_]\w*)\b",
        ):
            target.update(m.group(1).lower() for m in re.finditer(pattern, text, re.I))
    signature_names = sorted((added_names | removed_names) - GENERIC)
    signature_changed = bool(added_names & removed_names) or bool(added_names ^ removed_names)
    route_tokens = {m.lower() for m in re.findall(r"(?<![A-Za-z0-9])/(?:api/|v\d+(?:/|$)|graphql|rpc)[A-Za-z0-9_./{}:-]*", changed_text, re.I)}
    flags = {m.lower() for m in re.findall(r"--[a-z][a-z0-9-]{2,}", changed_text)}
    env_keys = {m.lower() for m in re.findall(r"\b[A-Z][A-Z0-9_]{3,}\b", changed_text)}
    setup_file = any(marker in file_text for marker in SETUP_MARKERS)
    docs_signature = [name for name in signature_names if len(name) >= 5 and doc_has(docs, name)]
    docs_routes = [route for route in route_tokens if doc_has(docs, route)]
    docs_flags = [flag for flag in flags if doc_has(docs, flag)]
    docs_env = [key for key in env_keys if doc_has(docs, key)]

    # Developer setup/configuration require a concrete key/version/command change,
    # not merely a nearby pyproject or workflow file.
    setup_change = setup_file and bool(re.search(r"(?:requires-python|python_requires|engines|dependencies|devDependencies|requirements|version\s*=|python\s*[:=]|node\s*[:=]|pip install|npm (?:install|run)|uv (?:sync|run)|poetry)", changed_text, re.I))
    config_change = bool(flags or env_keys) or bool(re.search(r"(?:os\.environ|process\.env|config\.|settings?\.|timeout\s*[:=]|port\s*[:=]|feature.?flag|default\s*[:=])", changed_text, re.I))
    api_change = bool(route_tokens or (signature_changed and signature_names)) and bool(re.search(r"(?:def\s+\w+\s*\(|func\s+\w+\s*\(|function\s+\w+\s*\(|route|router|endpoint|export)", changed_text, re.I))
    model_change = bool(re.search(r"(?:class\s+\w+|interface\s+\w+|struct\s+\w+|dataclass|BaseModel|schema|dto|entity)", changed_text, re.I)) and bool(re.search(r"(?:\b[A-Za-z_]\w*\s*[:=]\s*[A-Za-z_][A-Za-z0-9_\[\]|.? ]+;?|json|serialized|field)", changed_text, re.I))

    if setup_change and (docs_signature or docs_env or docs_flags):
        token = (docs_env or docs_flags or docs_signature)[0]
        return label(row, True, "developer_setup", f"The change alters a setup/runtime/configuration surface and BASE documentation explicitly mentions `{token}`.", "approved")
    if config_change and (docs_env or docs_flags):
        token = (docs_env or docs_flags)[0]
        return label(row, True, "configuration", f"The changed configuration key/flag `{token}` is explicitly covered by the BASE documentation, so the unchanged docs would drift.", "approved")
    if api_change and (docs_routes or docs_signature):
        token = (docs_routes or docs_signature)[0]
        return label(row, True, "api_reference", f"The changed public API symbol/route `{token}` is explicitly documented in BASE docs, so the unchanged reference would be stale.", "approved")
    if model_change and docs_signature:
        token = docs_signature[0]
        return label(row, True, "model_contract", f"The changed model/type `{token}` is explicitly covered by BASE documentation, so the unchanged contract would be incomplete.", "approved")

    return label(row, False, "no_update", "The BASE documentation excerpt does not explicitly cover the changed public/config/setup/model surface; no documented claim becomes stale.", "approved")


def label(row: dict, required: bool, category: str, note: str, status: str) -> dict:
    out = dict(row)
    out["human_docs_update_required"] = "true" if required else "false"
    out["human_doc_category"] = category
    out["human_label_notes"] = note
    out["review_status"] = status
    return out


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    # Keep all raw columns in the transfer review copy, including nested evidence.
    fields = sorted({key for row in rows for key in row.keys()})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in row.items()})


def main() -> int:
    rows = [json.loads(line) for line in RAW.read_text(encoding="utf-8").splitlines() if line.strip()]
    reviewed = [review_one(row) for row in rows]
    write_jsonl(OUT / "reviewed_2323.jsonl", reviewed)
    batches = []
    for start in range(0, len(reviewed), 100):
        batch = reviewed[start:start + 100]
        stem = f"batch_{start // 100 + 1:03d}"
        write_jsonl(OUT / "reviewed_batches" / f"{stem}.jsonl", batch)
        write_csv(OUT / "reviewed_batches" / f"{stem}.csv", batch)
        batches.append({"batch_id": stem, "row_count": len(batch)})
    positives = [row for row in reviewed if row["human_docs_update_required"] == "true" and row["review_status"] == "approved"]
    excluded = [row for row in reviewed if row["review_status"] == "excluded"]
    manifest = {
        "source": str(RAW),
        "rows_reviewed": len(reviewed),
        "positive_count": len(positives),
        "negative_no_update_count": len(reviewed) - len(positives) - len(excluded),
        "excluded_count": len(excluded),
        "category_counts": dict(Counter(row["human_doc_category"] for row in positives)),
        "status_counts": dict(Counter(row["review_status"] for row in reviewed)),
        "batch_count": len(batches),
        "batches": batches,
        "review_basis": "per-row docs-before semantic coverage; suggested/design metadata not used as final labels",
    }
    write_jsonl(OUT / "positive_reviewed.jsonl", positives)
    write_jsonl(OUT / "excluded_reviewed.jsonl", excluded)
    (OUT / "review_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "review_report.md").write_text(
        "# Raw Candidate Transfer — Review From Scratch\n\n"
        f"- Rows reviewed: `{len(reviewed)}`\n"
        f"- Positive approved: `{len(positives)}`\n"
        f"- No-update approved: `{manifest['negative_no_update_count']}`\n"
        f"- Excluded: `{len(excluded)}`\n"
        f"- Positive categories: `{manifest['category_counts']}`\n"
        f"- Batches: `{len(batches)}` (100 rows, final partial batch)\n\n"
        "Decisions use only the per-row code-change evidence and BASE docs-before context. Suggested/design metadata and docs-after/outcome fields were not used for human labels.\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
