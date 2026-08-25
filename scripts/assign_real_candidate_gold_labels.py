from __future__ import annotations

"""
LEGACY PREFILL/PROTOCOL EXPERIMENT ONLY.

This script is NOT AUTHORIZED TO PRODUCE FINAL V2 GOLD LABELS.
Final V2 gold labels must be produced only through the human-reviewed
workflow implemented by prefill_human_label_sheet_v2.py and
finalize_human_gold_v2.py.

Historical behavior is intentionally preserved for reproducibility.
"""

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

POSITIVE_TYPE = "code_and_docs_changed_needs_manual_validation"
NEGATIVE_TYPE = "code_only_test_or_fixture_candidate_negative_review"

PUBLIC_SURFACE_TERMS = {
    "api", "endpoint", "route", "routes", "controller", "openapi", "swagger",
    "graphql", "schema", "schemas", "sdk", "client", "public", "external",
    "webhook", "event", "events", "cli", "command", "option", "parameter",
    "config", "configuration", "setting", "settings", "env", "environment",
    "permission", "permissions", "auth", "oauth", "token", "security",
    "policy", "policies", "role", "roles", "rbac", "migration", "database",
    "db", "sql", "model", "models", "entity", "entities", "dto", "contract",
    "types", "interface", "breaking", "deprecated", "deprecation", "release",
    "changelog", "workflow", "setup", "install", "deployment", "integration",
}

NEGATIVE_TERMS = {
    "test", "tests", "spec", "fixture", "fixtures", "mock", "mocks",
    "ci", "workflow", "lint", "format", "prettier", "eslint", "ruff",
    "renovate", "dependabot", "bump", "dependency", "dependencies",
    "refactor", "cleanup", "typo", "style", "benchmark", "snapshot",
    "storybook", "stories",
}

CONFIG_FILES = {
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
    "tox.ini", "dockerfile", "docker-compose.yml", ".env.example", "tsconfig.json",
    "vite.config.ts", "next.config.js", "next.config.ts", "webpack.config.js",
}

CATEGORY_PATTERNS = [
    ("api_reference", re.compile(r"\b(api|endpoint|route|routes|controller|openapi|swagger|graphql|sdk|client|webhook)\b", re.I)),
    ("configuration", re.compile(r"\b(config|configuration|setting|settings|env|environment|option|parameter|flag)\b", re.I)),
    ("model_contract", re.compile(r"\b(schema|model|entity|dto|type|types|interface|contract|migration|database|sql|db)\b", re.I)),
    ("security", re.compile(r"\b(auth|oauth|token|security|permission|policy|role|rbac|passport|credential)\b", re.I)),
    ("developer_setup", re.compile(r"\b(setup|install|dependency|dependencies|build|dev server|local development|tooling)\b", re.I)),
    ("workflow_documentation", re.compile(r"\b(workflow|ci|pipeline|deployment|release|publish|automation)\b", re.I)),
    ("testing", re.compile(r"\b(test|tests|fixture|mock|spec|snapshot|e2e|integration test)\b", re.I)),
    ("changelog", re.compile(r"\b(changelog|release note|release|breaking|deprecated|deprecation)\b", re.I)),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def compact(value: Any, limit: int = 500) -> str:
    text = " ".join(str(value or "").split())
    return text[: limit - 3] + "..." if len(text) > limit else text


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value:
        return [str(value)]
    return []


def candidate_type(row: dict[str, Any]) -> str:
    if row.get("candidate_type"):
        return str(row["candidate_type"])
    evidence = row.get("candidate_evidence")
    if isinstance(evidence, dict) and evidence.get("candidate_type"):
        return str(evidence["candidate_type"])
    return "unknown"


def text_blob(row: dict[str, Any]) -> str:
    parts = [
        row.get("pr_title", ""),
        row.get("language", ""),
        " ".join(as_list(row.get("code_changed_files"))),
        " ".join(as_list(row.get("changed_files"))),
        " ".join(as_list(row.get("docs_changed_files"))),
        row.get("code_diff_excerpt", ""),
        row.get("docs_diff_excerpt", ""),
    ]
    return "\n".join(str(part or "") for part in parts)


def path_tokens(paths: list[str]) -> set[str]:
    tokens: set[str] = set()
    for path in paths:
        lower = path.lower()
        for part in re.split(r"[^a-zA-Z0-9_]+", lower):
            if part:
                tokens.add(part)
        name = lower.rsplit("/", 1)[-1]
        if name:
            tokens.add(name)
    return tokens


def all_paths_are_tests_or_internal(paths: list[str], title: str) -> bool:
    if not paths:
        return False
    lower_title = title.lower()
    if lower_title.startswith(("test", "tests", "chore(test", "chore(tests", "fix(test", "refactor(test")):
        return True

    test_markers = (
        "/test/", "/tests/", "__tests__", ".test.", ".spec.", "/fixtures/",
        "/fixture/", "/mocks/", "/mock/", "/snapshots/", ".stories.", "/stories/",
        "/benchmarks/", "/benchmark/",
    )
    non_test = []
    for path in paths:
        lower = path.lower()
        if not any(marker in lower for marker in test_markers):
            non_test.append(path)
    return len(non_test) == 0


def is_dependency_or_ci_only(row: dict[str, Any]) -> bool:
    title = str(row.get("pr_title") or "").lower()
    files = [p.lower() for p in as_list(row.get("code_changed_files"))]

    if title.startswith(("chore(deps", "build(deps", "deps:", "dependency", "bump ")):
        return True

    if title.startswith(("ci", "chore(ci", "build(ci")):
        return True

    if files and all(
        ("/.github/" in f or f.startswith(".github/") or "dependabot" in f or "renovate" in f)
        for f in files
    ):
        return True

    return False


def infer_category(row: dict[str, Any], positive: bool) -> str:
    if not positive:
        return "no_update"

    blob = text_blob(row)
    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(blob):
            return category

    docs = " ".join(as_list(row.get("docs_changed_files"))).lower()
    if "changelog" in docs or "release" in docs:
        return "changelog"
    if "readme" in docs or "getting-started" in docs:
        return "developer_setup"
    if "architecture" in docs or "design" in docs:
        return "architecture"
    if "api" in docs:
        return "api_reference"

    return "project_documentation"


def evidence_terms(row: dict[str, Any]) -> tuple[set[str], set[str]]:
    files = as_list(row.get("code_changed_files")) + as_list(row.get("changed_files"))
    blob = text_blob(row).lower()
    tokens = path_tokens(files)
    for term in PUBLIC_SURFACE_TERMS:
        if term in blob:
            tokens.add(term)
    negative_tokens = set()
    for term in NEGATIVE_TERMS:
        if term in blob:
            negative_tokens.add(term)
    return tokens & PUBLIC_SURFACE_TERMS, negative_tokens & NEGATIVE_TERMS


def label_row(row: dict[str, Any]) -> dict[str, Any]:
    ctype = candidate_type(row)
    title = str(row.get("pr_title") or "")
    files = as_list(row.get("code_changed_files"))

    public_hits, negative_hits = evidence_terms(row)

    reason_parts: list[str] = []
    confidence = "medium"
    positive: bool

    if ctype == POSITIVE_TYPE:
        positive = True
        confidence = "high"
        reason_parts.append("Code and documentation changed in the same merged PR.")
    elif ctype == NEGATIVE_TYPE:
        positive = False
        confidence = "high"
        reason_parts.append("Candidate is classified as test/fixture-only negative review.")
    elif all_paths_are_tests_or_internal(files, title):
        positive = False
        confidence = "high"
        reason_parts.append("Changed code paths are test/fixture/mock/story/benchmark oriented.")
    elif is_dependency_or_ci_only(row):
        positive = False
        confidence = "high"
        reason_parts.append("Change is dependency/CI/build automation oriented.")
    elif public_hits:
        positive = True
        confidence = "medium"
        reason_parts.append("Code/title/diff contains public-surface documentation signals: " + ", ".join(sorted(public_hits)[:12]) + ".")
    else:
        # Conservative default for general implementation-only code changes.
        positive = False
        confidence = "medium"
        if negative_hits:
            reason_parts.append("No strong public documentation signal; internal/maintenance terms present: " + ", ".join(sorted(negative_hits)[:12]) + ".")
        else:
            reason_parts.append("No strong public documentation signal found in changed files/title/diff excerpt.")

    category = infer_category(row, positive)
    copied = dict(row)
    copied["candidate_type"] = ctype
    copied["gold_docs_update_required"] = positive
    copied["gold_doc_category"] = category
    copied["gold_target_doc_file"] = None
    copied["gold_target_section"] = None
    copied["gold_patch_summary"] = (
        "Documentation update required based on protocol labeling evidence."
        if positive else None
    )
    copied["label_confidence"] = f"protocol_{confidence}"
    copied["label_source"] = "protocol_derived_large_scale_label_v1"
    copied["manual_label_notes"] = " ".join(reason_parts)
    return copied


def write_decisions_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "case_id", "source_url", "repository", "pr_number", "pr_title", "language",
        "candidate_type", "gold_docs_update_required", "gold_doc_category",
        "label_confidence", "label_source", "manual_label_notes",
        "code_changed_files", "docs_changed_files", "docs_before_excerpt_preview",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "case_id": row.get("case_id"),
                    "source_url": row.get("source_url"),
                    "repository": row.get("repository"),
                    "pr_number": row.get("pr_number"),
                    "pr_title": row.get("pr_title"),
                    "language": row.get("language"),
                    "candidate_type": row.get("candidate_type"),
                    "gold_docs_update_required": str(bool(row.get("gold_docs_update_required"))).lower(),
                    "gold_doc_category": row.get("gold_doc_category"),
                    "label_confidence": row.get("label_confidence"),
                    "label_source": row.get("label_source"),
                    "manual_label_notes": row.get("manual_label_notes"),
                    "code_changed_files": "; ".join(as_list(row.get("code_changed_files"))),
                    "docs_changed_files": "; ".join(as_list(row.get("docs_changed_files"))),
                    "docs_before_excerpt_preview": compact(row.get("docs_before_excerpt") or "", 600),
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign protocol-derived gold fields to real PR candidates.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--output-high-medium-jsonl", required=True)
    parser.add_argument("--decisions-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    labeled = [label_row(row) for row in rows]
    high_medium = [
        row for row in labeled
        if str(row.get("label_confidence")) in {"protocol_high", "protocol_medium"}
        and isinstance(row.get("gold_docs_update_required"), bool)
    ]

    summary = {
        "status": "ok",
        "input_records": len(rows),
        "labeled_records": len(labeled),
        "high_medium_records": len(high_medium),
        "gold_distribution": dict(Counter(str(row.get("gold_docs_update_required")) for row in labeled)),
        "label_confidence_counts": dict(Counter(str(row.get("label_confidence")) for row in labeled)),
        "gold_doc_category_counts": dict(Counter(str(row.get("gold_doc_category")) for row in labeled)),
        "candidate_type_counts": dict(Counter(str(row.get("candidate_type")) for row in labeled)),
        "language_counts": dict(Counter(str(row.get("language") or "unknown") for row in labeled)),
        "label_protocol": {
            "positive": [
                "code_and_docs co-change candidates",
                "code-only candidates with public-surface API/config/schema/security/CLI/model/workflow signals",
            ],
            "negative": [
                "test/fixture candidates",
                "test-only/internal/dependency/CI/build/refactor candidates",
                "code-only candidates without a strong public documentation signal",
            ],
            "model_input_boundary": "Labels may use audit context; model training must only use safe model input fields.",
        },
    }

    write_jsonl(Path(args.output_jsonl), labeled)
    write_jsonl(Path(args.output_high_medium_jsonl), high_medium)
    write_decisions_csv(Path(args.decisions_csv), labeled)
    write_json(Path(args.summary_json), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
