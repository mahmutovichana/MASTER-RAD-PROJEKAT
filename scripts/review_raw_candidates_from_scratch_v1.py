import argparse
import collections
import hashlib
import json
import re
from pathlib import Path


HUMAN_FIELDS = {
    "human_docs_update_required",
    "human_doc_category",
    "human_label_notes",
    "review_status",
}

GENERIC = {
    "test", "tests", "true", "false", "none", "null", "self", "http", "https",
    "json", "xml", "yaml", "content", "closed", "open", "get", "post", "put",
    "patch", "delete", "request", "response", "client", "server", "data", "value",
    "name", "path", "body", "headers", "header", "status", "code", "error", "result",
    "config", "configuration", "settings", "default", "version", "options", "option",
    "string", "bytes", "dict", "list", "tuple", "object", "type", "class", "model",
    "field", "fields", "id", "url", "method", "run", "build", "install", "python",
    "node", "package", "packages", "module", "index", "main", "base", "common",
    "init", "close", "read", "write", "send", "receive", "handle", "process", "parse",
    "encode", "decode", "text", "stream", "connection", "transport", "auth", "token",
}

TEST_RE = re.compile(r"(^|/)(tests?|testdata|fixtures?|snapshots?|mocks?)(/|$)|(^|/)(test_|.*_test\.|.*\.snap$)", re.I)
SETUP_RE = re.compile(
    r"(^|/)(pyproject\.toml|setup\.py|setup\.cfg|requirements[^/]*\.txt|Pipfile|poetry\.lock|uv\.lock|"
    r"package\.json|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|go\.mod|go\.sum|pom\.xml|build\.gradle|"
    r"gradle\.properties|Cargo\.toml|Cargo\.lock|Dockerfile[^/]*|\.github/workflows/|tox\.ini|noxfile\.py|"
    r"Makefile|\.python-version|\.nvmrc|\.tool-versions)(/|$)",
    re.I,
)
CONFIG_PATH_RE = re.compile(r"(^|/)(\.env[^/]*|config[^/]*|settings[^/]*|conf[^/]*|values[^/]*|deployment[^/]*)(/|\.|$)", re.I)
ROUTE_RE = re.compile(r"(?<![A-Za-z0-9_])/(?:api/|v\d+(?:/|$)|graphql(?:/|$)|rpc(?:/|$))[A-Za-z0-9_./:{}?=&%+\-]*")
ENV_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
FLAG_RE = re.compile(r"--[a-z][a-z0-9-]{2,}")
MODEL_GENERIC = {"annotation", "errors", "extensions", "serialize", "when", "this", "possible", "change", "argument", "directives", "author", "query", "mutation", "form", "user", "project", "root", "scope", "host", "fragment", "returns", "that", "useful", "needs", "value", "values", "result", "results", "name", "type", "types", "data", "field", "fields"}
FUNC_RE = re.compile(r"\b(?:async\s+def|def|func|function)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
EXPORT_FUNC_RE = re.compile(r"\bexport\s+(?:default\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)")
CLASS_RE = re.compile(r"\b(?:class|interface|struct|enum|type)\s+([A-Z][A-Za-z0-9_]*)")
# Field declarations only (not ordinary assignments such as ``self.encoding =``).
FIELD_DECL_RE = re.compile(r"^\s{0,8}(?!self\.|this\.)(?!.*[(),])([a-zA-Z_][A-Za-z0-9_]*)\s*:\s*[A-Za-z_][A-Za-z0-9_<>\[\]|., ]*\s*$")
GO_FIELD_RE = re.compile(r"^\s{1,8}([A-Z][A-Za-z0-9_]*)\s+[A-Za-z_*][A-Za-z0-9_.*\[\]]*")
VERSION_RE = re.compile(r"\b(?:python|node|npm|java|go|rust|ruby|django|react|pytest|typescript|pnpm|yarn)[^\n]{0,30}?\b(?:\d+\.){1,2}\d+\b", re.I)
SCRIPT_RE = re.compile(r"\b(?:npm|yarn|pnpm|make|poetry|uv|pip|cargo|go)\s+(?:run|install|sync|build|test|serve|start|dev|check|fmt|vet|mod)\b[^\n]*", re.I)


def nested(row, key):
    inp = row.get("classifier_model_input")
    if isinstance(inp, dict) and inp.get(key) not in (None, ""):
        return inp.get(key)
    return row.get(key)


def changed_lines(diff):
    lines = []
    for raw in (diff or "").splitlines():
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("+") or raw.startswith("-"):
            text = raw[1:].strip()
            if text and not text.startswith("@@"):
                lines.append(text)
    return lines


def changed_sections(diff):
    """Return changed lines grouped by the file named in each diff section."""
    sections = collections.defaultdict(list)
    current = None
    for raw in (diff or "").splitlines():
        if raw.startswith("diff --git "):
            m = re.search(r" b/(.+)$", raw)
            current = m.group(1) if m else None
            continue
        if current and (raw.startswith("+") or raw.startswith("-")) and not raw.startswith(("+++", "---")):
            text = raw[1:]
            if text.strip() and not text.lstrip().startswith("@@"):
                sections[current].append(text)
    return sections


def distinctive(tok):
    t = tok.strip().strip("`'\"()[]{}:;,.\n").lower()
    if len(t) < 4 or t in GENERIC or t in {"handler", "authority", "scheme", "items", "files", "form", "project", "testing", "release", "security", "architecture", "queue", "scheduler", "format", "root", "create", "render", "host", "scope", "namespace", "dependency", "query", "user", "more", "copy_with", "click", "graphql", "websockets", "zttp", "route", "command"} or t.startswith("__"):
        return False
    if t.isdigit() or re.fullmatch(r"v\d+", t):
        return False
    return True


def docs_has(docs, token):
    if not token:
        return False
    # Exact identifier/key match; do not count substring matches.
    return re.search(r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])", docs, re.I) is not None


DOC_CONTEXT = {
    "api_reference": re.compile(r"\b(?:api|endpoint|route|routing|function|method|parameter|argument|client|request|response|webhook|graphql|sdk|public)\b", re.I),
    "configuration": re.compile(r"\b(?:environment|env(?:ironment)?|configuration|config|option|flag|setting|timeout|port|variable|proxy|certificate)\b", re.I),
    "developer_setup": re.compile(r"\b(?:install|installation|requirement|dependency|dependencies|python|node|npm|package|version|build|run|setup|quickstart|prerequisite)\b", re.I),
    "model_contract": re.compile(r"\b(?:model|schema|field|attribute|property|type|typed|dataclass|pydantic|interface|struct|entity|dto|serialization|json)\b", re.I),
}


def docs_supports(docs, token, category):
    """Require token plus category-specific documentation context in one excerpt."""
    if not docs_has(docs, token):
        return False
    pattern = DOC_CONTEXT.get(category)
    if pattern is None:
        return False
    # Prefer a local window around the token, rather than unrelated pooled docs.
    for m in re.finditer(r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])", docs, re.I):
        window = docs[max(0, m.start() - 260): min(len(docs), m.end() + 260)]
        codeish = bool(re.search(r"`[^`\n]{0,120}" + re.escape(token) + r"[^`\n]{0,120}`", window, re.I))
        codeish = codeish or bool(re.search(r"^\s*(?:>>>|\$|[-+]?\s*(?:GET|POST|PUT|PATCH|DELETE)\s+[^\n]*|[^\n]*\([^\n]*\))", window, re.I | re.M))
        if pattern.search(window) and codeish:
            return True
    return False


def docs_paths(row):
    paths = []
    for item in row.get("docs_before_retrieved_files") or []:
        if isinstance(item, dict) and item.get("path"):
            paths.append(str(item["path"]))
    return paths


def all_test_files(files):
    return bool(files) and all(TEST_RE.search(str(f).replace("\\", "/")) for f in files)


def non_test_files(files):
    return [str(f).replace("\\", "/") for f in files if not TEST_RE.search(str(f).replace("\\", "/"))]


def added_or_removed_diff(diff):
    return "\n".join(changed_lines(diff))


def choose_positive(row, files, diff, docs):
    """Return (category, evidence token, doc path) only for strong docs-before coverage."""
    if not docs or not diff or not files or all_test_files(files):
        return None
    code_files = non_test_files(files)
    if not code_files:
        return None
    sections = changed_sections(diff)
    # Ignore test/fixture-only hunks for public/config/model decisions. They
    # are useful evidence for a human but cannot themselves change user docs.
    non_test_sections = {f: ls for f, ls in sections.items() if not TEST_RE.search(f)}
    change = "\n".join(line for ls in non_test_sections.values() for line in ls)
    lower_files = " ".join(code_files).lower()

    # Developer setup has the highest priority, but only for a real setup/runtime
    # change and an explicit token/command/version that appears in docs-before.
    setup_files = [f for f in code_files if SETUP_RE.search(f) and not f.lower().startswith(".github/workflows/")]
    setup_file = bool(setup_files)
    if setup_file:
        setup_change = "\n".join(line for f, ls in sections.items() if f in setup_files for line in ls)
        setup_tokens = []
        setup_key_values = {}
        setup_tokens += [m.group(0) for m in SCRIPT_RE.finditer(setup_change)]
        setup_tokens += [m.group(0) for m in VERSION_RE.finditer(setup_change)]
        # Dependency names/keys from common manifest changes.
        for m in re.finditer(r"^\s*[\"']?([@A-Za-z0-9_.-]{2,})[\"']?\s*[:=]\s*[\"']?([^\"'\s,}]+)", setup_change, re.M):
            k, v = m.group(1), m.group(2)
            if k.lower() not in GENERIC and k.lower() not in {"uses", "run", "with", "name", "on", "jobs", "steps", "matrix"} and (re.search(r"\d", v) or k.lower() in {"scripts", "engines", "python", "node", "requires-python"}):
                setup_tokens.append(k)
                setup_key_values.setdefault(k, []).append(v)
        for tok in setup_tokens:
            # A dependency version bump alone does not require docs when the
            # docs only show an unpinned install command. Require the changed
            # version/range to be documented (or a genuinely changed command).
            if tok in setup_key_values:
                versions = [v for v in setup_key_values[tok] if re.search(r"\d", v)]
                if versions and not any(docs_has(docs, v) for v in versions):
                    continue
            # For a version string, prefer its containing setup phrase; exact
            # version alone is too generic.
            if docs_supports(docs, tok, "developer_setup"):
                return "developer_setup", tok, None

    # Configuration: explicit env var/CLI flag/config key changed in code.
    config_sections = {f: ls for f, ls in non_test_sections.items() if not re.match(r"(?:\.github/workflows/|\.readthedocs|\.pre-commit)", f, re.I)}
    config_change = "\n".join(line for ls in config_sections.values() for line in ls)
    configish = bool(CONFIG_PATH_RE.search(lower_files) or re.search(r"\b(?:os\.environ|getenv|process\.env|ENV\[|config\.|settings\.|feature[_ -]?flag)\b", config_change, re.I))
    if configish:
        toks = []
        # Environment keys count only when they occur in an env access/assignment
        # context; this avoids treating constants such as EXAMPLE as config.
        for line in config_change.splitlines():
            if re.search(r"(?:environ|getenv|process\.env|ENV\[|env(?:ironment)?\s*[:=])", line, re.I):
                toks += [m.group(0) for m in ENV_RE.finditer(line) if m.group(0).lower() not in GENERIC]
        toks += [m.group(0) for m in FLAG_RE.finditer(config_change) if m.group(0).lower() not in {"--help", "--version"}]
        # Dotted attributes such as ``config.verify`` are intentionally not
        # treated as externally documented configuration keys; only explicit
        # env/CLI/config-map keys qualify.
        for tok in toks:
            if distinctive(tok) and docs_supports(docs, tok, "configuration"):
                return "configuration", tok, None

    # Public API: route or public callable whose name is explicitly documented.
    api_toks = ROUTE_RE.findall(change)
    # Only changed definitions/signatures (not arbitrary mentions) can establish
    # a public API candidate. Nested local helpers are excluded by indentation.
    for line in change.splitlines():
        if re.match(r"^\s{0,4}(?:async\s+def|def|func|export\s+(?:default\s+)?function)\s+", line):
            api_toks += [m.group(1) for m in FUNC_RE.finditer(line)]
            api_toks += [m.group(1) for m in EXPORT_FUNC_RE.finditer(line)]
    for tok in api_toks:
        clean = tok.strip("/ ")
        if (tok.startswith("/") and len(clean) >= 4) or (distinctive(clean) and not clean.startswith("_")):
            if docs_supports(docs, clean, "api_reference"):
                return "api_reference", clean, None

    # Model contract: a public type/field declaration changed and the same type
    # or field is explicitly present in docs-before.
    modelish_file = bool(re.search(r"(^|/)(models?|schemas?|dto|entities?|types?|interfaces?)(/|[_-])", lower_files))
    decls = [m.group(1) for m in CLASS_RE.finditer(change) if distinctive(m.group(1))]
    fields = []
    for line in change.splitlines():
        m = FIELD_DECL_RE.match(line)
        if m and distinctive(m.group(1)):
            fields.append(m.group(1))
        m = GO_FIELD_RE.match(line)
        if m and distinctive(m.group(1)):
            fields.append(m.group(1))
    # Require an actual public type declaration or a field declaration. This
    # avoids interpreting ordinary method arguments/assignments as a schema.
    if modelish_file and (decls or fields):
        for tok in decls + fields:
            if tok.lower() in MODEL_GENERIC:
                continue
            if docs_supports(docs, tok, "model_contract"):
                return "model_contract", tok, None

    # Other documentation is deliberately narrow: only a documented workflow,
    # architecture, operations, security, or user-facing procedure is eligible.
    other_terms = re.findall(r"\b(?:queue|scheduler|migration|troubleshoot(?:ing)?|architecture)\b", change, re.I)
    path_blob = (" ".join(code_files) + " " + " ".join(docs_paths(row))).lower()
    other_terms = [t for t in other_terms if t.lower() in path_blob]
    if other_terms:
        for tok in other_terms:
            if docs_has(docs, tok):
                return "other_documentation", tok, None
    return None


def review_row(row):
    files = nested(row, "code_changed_files") or row.get("changed_files") or []
    diff = nested(row, "code_diff_excerpt") or ""
    docs = nested(row, "docs_before_excerpt") or ""
    if isinstance(files, str):
        files = [files]
    if not isinstance(files, list):
        files = []
    docs = str(docs or "")
    diff = str(diff or "")
    if not files or not diff or not docs.strip():
        required, category, status = False, "no_update", "excluded"
        note = "Evidence nije dovoljna za pouzdanu odluku (nedostaje code diff, lista fajlova ili docs-before sadržaj)."
    else:
        chosen = choose_positive(row, files, diff, docs)
        if chosen:
            category, token, _ = chosen
            required, status = True, "approved"
            path_text = docs_paths(row)
            suffix = f" Dokumentacijski trag: {path_text[0]}." if path_text else ""
            surface = {"api_reference": "javni API element", "configuration": "konfiguracijski element", "developer_setup": "setup/razvojni zahtjev", "model_contract": "javni model/schema element", "other_documentation": "dokumentovani workflow/operativni element"}[category]
            note = f"Promjena mijenja {surface} '{token}', a isti element je eksplicitno pokriven u docs-before; postojeći tekst bi zato postao zastario ili nepotpun ({category}).{suffix}"
        else:
            required, category, status = False, "no_update", "approved"
            if all_test_files(files):
                note = "Promjena je ograničena na testove/fixture/snapshot fajlove; postojeća dokumentacija ostaje tačna."
            else:
                note = "Promijenjena implementacija nije eksplicitno pokrivena postojećim docs-before sadržajem i ne čini postojeću dokumentaciju netačnom ili nepotpunom."
    out = dict(row)
    out.update({
        "human_docs_update_required": required,
        "human_doc_category": category,
        "human_label_notes": note,
        "review_status": status,
    })
    return out


def canonical_without_human(row):
    return {k: v for k, v in row.items() if k not in HUMAN_FIELDS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    src = Path(args.input)
    outdir = Path(args.output_dir)
    batches = outdir / "reviewed_batches"
    outdir.mkdir(parents=True, exist_ok=True)
    batches.mkdir(parents=True, exist_ok=True)
    reviewed_path = outdir / "reviewed_2323.jsonl"
    positive_path = outdir / "positive_reviewed.jsonl"
    excluded_path = outdir / "excluded_reviewed.jsonl"
    stats = collections.Counter()
    by_repo = collections.Counter()
    by_lang = collections.Counter()
    reason = collections.Counter()
    source_hash = hashlib.sha256()
    reviewed_hash = hashlib.sha256()
    rows = []
    with src.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            source_hash.update(line.encode("utf-8"))
            out = review_row(row)
            rows.append(out)
            reviewed_hash.update((json.dumps(canonical_without_human(out), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
            stats[(out["review_status"], out["human_doc_category"])] += 1
            by_repo[(row.get("repository") or "unknown", out["human_doc_category"])] += 1
            by_lang[(row.get("language") or "unknown", out["human_doc_category"])] += 1
            if out["review_status"] == "excluded":
                reason["insufficient evidence"] += 1
    shard_case_ids = {}
    for shard_file in sorted(src.parent.glob("candidates_*.jsonl")):
        shard = shard_file.stem.split("_")[-1]
        with shard_file.open("r", encoding="utf-8") as sf:
            shard_case_ids[shard] = {json.loads(line)["case_id"] for line in sf if line.strip()}
    shard_category_counts = {}
    for shard, ids in sorted(shard_case_ids.items()):
        shard_category_counts[shard] = dict(collections.Counter(r["human_doc_category"] for r in rows if r["case_id"] in ids))
    with reviewed_path.open("w", encoding="utf-8", newline="\n") as f_all, positive_path.open("w", encoding="utf-8", newline="\n") as f_pos, excluded_path.open("w", encoding="utf-8", newline="\n") as f_exc:
        for i, row in enumerate(rows, 1):
            text = json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            f_all.write(text)
            if row["human_docs_update_required"]:
                f_pos.write(text)
            if row["review_status"] == "excluded":
                f_exc.write(text)
            if (i - 1) % 100 == 0:
                batch_no = (i - 1) // 100 + 1
                # Delay writing until the batch is complete below.
        for start in range(0, len(rows), 100):
            bpath = batches / f"batch_{start // 100 + 1:03d}.jsonl"
            with bpath.open("w", encoding="utf-8", newline="\n") as bf:
                for row in rows[start:start + 100]:
                    bf.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    manifest = {
        "review_version": "review_raw_candidates_from_scratch_v1",
        "source": str(src),
        "row_count": len(rows),
        "status_counts": {f"{k[0]}::{k[1]}": v for k, v in sorted(stats.items())},
        "category_counts": dict(collections.Counter(r["human_doc_category"] for r in rows)),
        "language_counts": dict(collections.Counter(r.get("language") or "unknown" for r in rows)),
        "positive_category_counts": dict(collections.Counter(r["human_doc_category"] for r in rows if r["human_docs_update_required"])),
        "repository_category_counts": {repo: dict(sorted({cat: n for (rp, cat), n in by_repo.items() if rp == repo}.items())) for repo in sorted({rp for rp, _ in by_repo})},
        "language_category_counts": {lang: dict(sorted({cat: n for (lg, cat), n in by_lang.items() if lg == lang}.items())) for lang in sorted({lg for lg, _ in by_lang})},
        "shard_category_counts": shard_category_counts,
        "excluded_count": sum(1 for r in rows if r["review_status"] == "excluded"),
        "source_sha256": source_hash.hexdigest(),
        "reviewed_nonhuman_canonical_sha256": reviewed_hash.hexdigest(),
        "human_fields_added_only": sorted(HUMAN_FIELDS),
        "method": "Conservative per-row semantic coverage check using only code_changed_files, code_diff_excerpt and docs_before_excerpt. docs-after, comments, source URLs, and outcome metadata were not used.",
    }
    (outdir / "review_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Small auditable sample: five rows per category plus five no-update rows.
    sample_rows = []
    for cat in ["api_reference", "configuration", "developer_setup", "model_contract", "other_documentation", "no_update"]:
        sample_rows.extend([r for r in rows if r["human_doc_category"] == cat][:5])
    with (outdir / "decision_samples.jsonl").open("w", encoding="utf-8", newline="\n") as sf:
        for r in sample_rows:
            sf.write(json.dumps({k: r.get(k) for k in ["case_id", "repository", "pr_number", "language", "code_changed_files", "human_docs_update_required", "human_doc_category", "human_label_notes", "review_status"]}, ensure_ascii=False, separators=(",", ":")) + "\n")
    lines = [
        "# Raw candidate review (from scratch)", "",
        f"Rows reviewed: **{len(rows)}**", "",
        "This review uses only the safe evidence fields in the requested order: `code_changed_files`, `code_diff_excerpt`, then `docs_before_excerpt`. A positive label requires a changed public/config/setup/model token to be explicitly covered by docs-before. Generic terms and internal/test-only changes do not qualify.", "",
        "## Label distribution", "",
        "| Category | Count |", "|---|---:|",
    ]
    for cat, n in sorted(collections.Counter(r["human_doc_category"] for r in rows).items()):
        lines.append(f"| `{cat}` | {n} |")
    lines += ["", "## Review status", "", "| Status | Count |", "|---|---:|"]
    for st, n in sorted(collections.Counter(r["review_status"] for r in rows).items()):
        lines.append(f"| `{st}` | {n} |")
    lines += ["", "## Positive categories", "", "| Category | Count |", "|---|---:|"]
    for cat, n in sorted(collections.Counter(r["human_doc_category"] for r in rows if r["human_docs_update_required"]).items()):
        lines.append(f"| `{cat}` | {n} |")
    lines += ["", "## Languages", "", "| Language | Rows | Positive |", "|---|---:|---:|"]
    for lang in sorted({r.get("language") or "unknown" for r in rows}):
        subset = [r for r in rows if (r.get("language") or "unknown") == lang]
        lines.append(f"| `{lang}` | {len(subset)} | {sum(1 for r in subset if r['human_docs_update_required'])} |")
    lines += ["", "## Shards", "", "| Shard | Rows | Positive |", "|---|---:|---:|"]
    for shard, counts in sorted(shard_category_counts.items()):
        total = sum(counts.values())
        positive = total - counts.get("no_update", 0)
        lines.append(f"| `{shard}` | {total} | {positive} |")
    lines += ["", "## Integrity", "", "- Source rows were not modified.", "- Output preserves source field values and adds only the four human review fields.", "- No docs-after, comments, source URLs, or outcome metadata were used for decisions.", "- `decision_samples.jsonl` contains a compact audit sample; the full row-level rationale is in `reviewed_2323.jsonl` and the 24 batch files.", ""]
    (outdir / "review_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
