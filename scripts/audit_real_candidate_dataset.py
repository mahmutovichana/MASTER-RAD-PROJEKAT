from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def safe_div(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def get_candidate_type(row: dict[str, Any]) -> str:
    if row.get("candidate_type"):
        return str(row["candidate_type"])

    evidence = row.get("candidate_evidence")
    if isinstance(evidence, dict) and evidence.get("candidate_type"):
        return str(evidence["candidate_type"])

    audit = row.get("audit_labeling_context")
    if isinstance(audit, dict):
        evidence = audit.get("candidate_evidence")
        if isinstance(evidence, dict) and evidence.get("candidate_type"):
            return str(evidence["candidate_type"])

    return "unknown"


def get_list(row: dict[str, Any], key: str) -> list[str]:
    value = row.get(key)
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value:
        return [str(value)]
    return []


def top_counts(counter: Counter[str], limit: int = 25) -> dict[str, int]:
    return dict(counter.most_common(limit))


def build_audit(rows: list[dict[str, Any]], input_path: Path) -> dict[str, Any]:
    total = len(rows)
    repos = Counter(str(row.get("repository") or "unknown") for row in rows)
    languages = Counter(str(row.get("language") or "unknown") for row in rows)
    candidate_types = Counter(get_candidate_type(row) for row in rows)

    source_urls = [str(row.get("source_url") or "") for row in rows if row.get("source_url")]
    duplicate_source_urls = [
        url for url, count in Counter(source_urls).items()
        if count > 1
    ]

    missing_code_diff = sum(1 for row in rows if not str(row.get("code_diff_excerpt") or "").strip())
    missing_docs_before = sum(1 for row in rows if not str(row.get("docs_before_excerpt") or "").strip())
    has_docs_changed = sum(1 for row in rows if get_list(row, "docs_changed_files"))

    code_file_counts = [len(get_list(row, "code_changed_files")) for row in rows]
    docs_file_counts = [len(get_list(row, "docs_changed_files")) for row in rows]
    changed_file_counts = [len(get_list(row, "changed_files")) for row in rows]

    largest_repo, largest_repo_count = repos.most_common(1)[0] if repos else ("", 0)
    largest_repo_share = safe_div(largest_repo_count, total)

    warnings: list[str] = []

    if total < 8000:
        warnings.append("Candidate pool is below 8k records; consider collecting more seeds.")
    if largest_repo_share > 0.15:
        warnings.append(f"Largest repository share is high: {largest_repo} has {largest_repo_share:.2%} of records.")
    if safe_div(missing_code_diff, total) > 0.01:
        warnings.append("More than 1% of records have missing code_diff_excerpt.")
    if safe_div(missing_docs_before, total) > 0.50:
        warnings.append("More than 50% of records have missing docs_before_excerpt; this may weaken documentation-context modeling.")
    if len(languages) < 2:
        warnings.append("Dataset has fewer than two detected languages.")
    if duplicate_source_urls:
        warnings.append("Duplicate source_url values detected.")

    return {
        "status": "ok",
        "input": str(input_path),
        "records": total,
        "unique_repositories": len(repos),
        "unique_languages": len(languages),
        "candidate_type_counts": dict(candidate_types),
        "language_counts": dict(languages),
        "top_repositories": top_counts(repos, 30),
        "largest_repository": largest_repo,
        "largest_repository_count": largest_repo_count,
        "largest_repository_share": largest_repo_share,
        "missing_code_diff_excerpt": missing_code_diff,
        "missing_code_diff_excerpt_share": safe_div(missing_code_diff, total),
        "missing_docs_before_excerpt": missing_docs_before,
        "missing_docs_before_excerpt_share": safe_div(missing_docs_before, total),
        "records_with_docs_changed_files": has_docs_changed,
        "records_with_docs_changed_files_share": safe_div(has_docs_changed, total),
        "duplicate_source_url_count": len(duplicate_source_urls),
        "duplicate_source_url_examples": duplicate_source_urls[:25],
        "code_file_count_stats": {
            "min": min(code_file_counts) if code_file_counts else 0,
            "max": max(code_file_counts) if code_file_counts else 0,
            "avg": safe_div(sum(code_file_counts), len(code_file_counts)),
        },
        "docs_file_count_stats": {
            "min": min(docs_file_counts) if docs_file_counts else 0,
            "max": max(docs_file_counts) if docs_file_counts else 0,
            "avg": safe_div(sum(docs_file_counts), len(docs_file_counts)),
        },
        "changed_file_count_stats": {
            "min": min(changed_file_counts) if changed_file_counts else 0,
            "max": max(changed_file_counts) if changed_file_counts else 0,
            "avg": safe_div(sum(changed_file_counts), len(changed_file_counts)),
        },
        "warnings": warnings,
        "interpretation": {
            "candidate_pool_warning": "Candidate records are not evaluation labels.",
            "final_metric_rule": "Accuracy/F1 require labeled or reviewed records.",
            "model_input_boundary": "Only language, code_changed_files, code_diff_excerpt, and docs_before_excerpt may be used as model input.",
        },
    }


def write_markdown(path: Path, audit: dict[str, Any]) -> None:
    lines = [
        "# Real GitHub PR Candidate Dataset Audit",
        "",
        f"- Input: `{audit['input']}`",
        f"- Records: `{audit['records']}`",
        f"- Unique repositories: `{audit['unique_repositories']}`",
        f"- Unique languages: `{audit['unique_languages']}`",
        f"- Largest repository: `{audit['largest_repository']}` / `{audit['largest_repository_share']:.2%}`",
        f"- Missing code diff excerpt: `{audit['missing_code_diff_excerpt']}` / `{audit['missing_code_diff_excerpt_share']:.2%}`",
        f"- Missing docs-before excerpt: `{audit['missing_docs_before_excerpt']}` / `{audit['missing_docs_before_excerpt_share']:.2%}`",
        f"- Records with docs changed files: `{audit['records_with_docs_changed_files']}` / `{audit['records_with_docs_changed_files_share']:.2%}`",
        f"- Duplicate source URLs: `{audit['duplicate_source_url_count']}`",
        "",
        "## Candidate Type Counts",
        "",
        "```json",
        json.dumps(audit["candidate_type_counts"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Language Counts",
        "",
        "```json",
        json.dumps(audit["language_counts"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Top Repositories",
        "",
        "```json",
        json.dumps(audit["top_repositories"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Warnings",
        "",
    ]

    if audit["warnings"]:
        for warning in audit["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- No major dataset audit warnings.")

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "- This audit describes candidate records, not labeled evaluation results.",
            "- Accuracy, precision, recall, F1, ROC AUC, and PR AUC require labels.",
            "- Audit-only fields must not be used as model input.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a real GitHub PR candidate dataset.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    rows = load_jsonl(input_path)
    audit = build_audit(rows, input_path)

    write_json(Path(args.output_json), audit)
    write_markdown(Path(args.output_md), audit)

    print(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())