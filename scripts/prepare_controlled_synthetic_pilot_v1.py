from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.human_review_workflow_v2 import REVIEWER_FIELDS, load_jsonl, make_review_row, write_json, write_jsonl

CORPUS = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v1"
OUT = ROOT / "data/final_v2/controlled_synthetic_positive_v1"


def write_review_csv(path: Path, rows: list[dict]) -> None:
    # Keep the normal reviewer schema; synthetic provenance stays in JSONL and audit manifests.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEWER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            values = {}
            for field in REVIEWER_FIELDS:
                value = row.get(field, "")
                values[field] = json.dumps(value, ensure_ascii=False) if isinstance(value, list) else ("" if value is None else str(value))
            writer.writerow(values)


def provenance_audit() -> dict:
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    provenance = load_jsonl(CORPUS / "source_provenance.jsonl")
    by_source = Counter(row.get("source_dataset", "unknown") for row in provenance)
    protocol = {
        "natural_17880": "current_docs_before_review",
        "targeted_enrichment_1199": "current_docs_before_review",
        "historical_4k_unique": "historical_protocol_derived_not_current_protocol_reviewed",
        "historical_300_gold_unique": "historical_gold_not_current_protocol_reviewed",
    }
    report = {
        "audit_version": "current_training_provenance_audit_v1",
        "corpus_path": str(CORPUS),
        "manifest_version": manifest.get("version"),
        "row_count": manifest.get("row_count"),
        "positive_count": manifest.get("positive_count"),
        "negative_count": manifest.get("negative_count"),
        "positive_rate": manifest.get("positive_rate"),
        "source_counts_manifest": manifest.get("source_counts", {}),
        "source_counts_observed": dict(by_source),
        "source_label_protocol": protocol,
        "synthetic_cases_present": any(row.get("source_dataset") == "controlled_synthetic_positive_v1" for row in provenance),
        "interpretation": "The consolidated corpus is a training-enriched corpus. Only natural_17880 and targeted_enrichment_1199 carry the current docs-before protocol; historical sources are retained for augmentation but must be reported separately and should not be treated as current-protocol natural gold.",
        "integrity": {
            "manifest_validation_error_count": manifest.get("validation_error_count"),
            "unique_pr_count": manifest.get("unique_pr_count"),
            "duplicates_skipped": manifest.get("duplicates_skipped"),
            "duplicate_label_conflicts": manifest.get("duplicate_label_conflicts"),
        },
    }
    reports = ROOT / "reports/final_v2"
    reports.mkdir(parents=True, exist_ok=True)
    write_json(reports / "current_training_provenance_audit.json", report)
    md = [
        "# Current Training Provenance Audit",
        "",
        f"- Corpus rows: `{report['row_count']}`",
        f"- Positive rows: `{report['positive_count']}` (`{report['positive_rate']:.2%}`)",
        "",
        "## Source status",
        "",
        "| Source | Rows | Protocol status |",
        "|---|---:|---|",
    ]
    for source, count in report["source_counts_manifest"].items():
        md.append(f"| `{source}` | {count} | {protocol.get(source, 'unknown')} |")
    md += [
        "",
        "The corpus is suitable as a training-enrichment pool, but historical rows are explicitly not current-protocol natural gold. No controlled synthetic rows are included in this corpus yet. Original natural data remains untouched.",
        "",
        f"- Manifest validation errors: `{report['integrity']['manifest_validation_error_count']}`",
        f"- Duplicate rows skipped during consolidation: `{report['integrity']['duplicates_skipped']}`",
        f"- Duplicate label conflicts recorded: `{report['integrity']['duplicate_label_conflicts']}`",
    ]
    (reports / "current_training_provenance_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def review_batches(candidates: list[dict]) -> dict:
    rows = [make_review_row(row) for row in candidates]
    review_root = OUT / "human_review"
    write_jsonl(review_root / "prefilled.jsonl", rows)
    batch_dir = review_root / "review_batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    batches = []
    size = 50
    for offset in range(0, len(rows), size):
        batch = rows[offset:offset + size]
        number = offset // size + 1
        stem = f"batch_{number:03d}"
        write_jsonl(batch_dir / f"{stem}.jsonl", batch)
        write_review_csv(batch_dir / f"{stem}.csv", batch)
        batches.append({"batch_id": stem, "row_count": len(batch), "jsonl": f"{stem}.jsonl", "csv": f"{stem}.csv"})
    manifest = {
        "input": str(OUT / "cases/synthetic_candidates.jsonl"),
        "total_rows": len(rows),
        "batch_size": size,
        "batch_count": len(batches),
        "batches": batches,
        "review_status_initial": "pending",
        "synthetic_design_category_hidden_from_reviewer": True,
        "provenance_retained_in_prefilled_jsonl": True,
    }
    write_json(review_root / "review_batch_manifest.json", manifest)
    (review_root / "review_batch_report.md").write_text(
        "# Controlled Synthetic Positive Pilot Review Batches\n\n"
        f"- Rows: `{len(rows)}`\n- Batch size: `{size}`\n- Batches: `{len(batches)}`\n"
        "- All human labels start empty and `review_status=pending`.\n"
        "- Synthetic design category is not exposed as a reviewer label; provenance remains in `prefilled.jsonl`.\n",
        encoding="utf-8",
    )
    return manifest


def quality_audit(candidates: list[dict], rejects: list[dict], provenance: dict) -> dict:
    consolidated_repos = {row.get("repository") for row in load_jsonl(CORPUS / "source_provenance.jsonl")}
    categories = Counter(row.get("synthetic_category_by_design") for row in candidates)
    languages = Counter(row.get("language") for row in candidates)
    repos = Counter(row.get("repository") for row in candidates)
    selected_rows = load_jsonl(OUT / "repository_selection/selected_repositories.jsonl")
    selected_repo_names = [row.get("repository") for row in selected_rows]
    case_ids = [row.get("case_id") for row in candidates]
    duplicate_case_ids = len(case_ids) - len(set(case_ids))
    missing_fields = []
    required = ["case_id", "repository", "language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt", "synthetic_base_sha", "synthetic_head_sha", "synthetic_validation_status", "synthetic_syntax_validation"]
    for row in candidates:
        absent = [field for field in required if not row.get(field)]
        if absent:
            missing_fields.append({"case_id": row.get("case_id"), "fields": absent})
    docs_changed = [row.get("case_id") for row in candidates if any(str(path).lower().startswith(("docs/", "doc/", "documentation/")) for path in row.get("code_changed_files", []))]
    diff_file_mismatch = []
    for row in candidates:
        diff_paths = [line.split(" b/", 1)[1] for line in str(row.get("code_diff_excerpt", "")).splitlines() if line.startswith("diff --git a/") and " b/" in line]
        expected = [str(path) for path in row.get("code_changed_files", [])]
        if sorted(diff_paths) != sorted(expected):
            diff_file_mismatch.append({"case_id": row.get("case_id"), "expected": expected, "observed": diff_paths})
    bad_syntax = [row.get("case_id") for row in candidates if row.get("synthetic_syntax_validation") == "fail"]
    no_diff = [row.get("case_id") for row in candidates if not str(row.get("code_diff_excerpt", "")).strip()]
    no_docs = [row.get("case_id") for row in candidates if not str(row.get("docs_before_excerpt", "")).strip()]
    overlap = sorted({row.get("repository") for row in candidates} & consolidated_repos)
    audit = {
        "audit_version": "synthetic_case_quality_audit_v1",
        "candidate_count": len(candidates),
        "reject_count": len(rejects),
        "category_counts": dict(categories),
        "language_counts": dict(languages),
        "repository_counts": {name: repos.get(name, 0) for name in selected_repo_names},
        "selected_repository_count": len(selected_repo_names),
        "duplicate_case_id_count": duplicate_case_ids,
        "missing_required_field_rows": missing_fields,
        "docs_changed_file_rows": docs_changed,
        "diff_file_mismatch_rows": diff_file_mismatch,
        "syntax_fail_rows": bad_syntax,
        "empty_diff_rows": no_diff,
        "empty_docs_evidence_rows": no_docs,
        "repository_overlap_with_consolidated_corpus": overlap,
        "all_candidates_pre_review_valid": not any([duplicate_case_ids, missing_fields, docs_changed, diff_file_mismatch, bad_syntax, no_diff, no_docs, overlap]),
        "human_review_required": True,
        "design_category_not_final_gold": True,
        "training_only": True,
        "provenance_audit_summary": provenance,
    }
    write_json(OUT / "audits/synthetic_case_quality_audit.json", audit)
    lines = [
        "# Synthetic Case Quality Audit",
        "",
        f"- Candidates: `{len(candidates)}`",
        f"- Rejects: `{len(rejects)}`",
        f"- Pre-review automated gates: `{'PASS' if audit['all_candidates_pre_review_valid'] else 'FAIL'}`",
        f"- Human review required: `{audit['human_review_required']}`",
        "",
        "## Distribution",
        "",
        f"- Categories: `{dict(categories)}`",
        f"- Languages: `{dict(languages)}`",
        f"- Repositories (selected, including zero-candidate repos): `{audit['repository_counts']}`",
        "",
        "## Gate details",
        "",
        f"- Duplicate case IDs: `{duplicate_case_ids}`",
        f"- Missing required provenance/evidence: `{len(missing_fields)}`",
        f"- Documentation files changed: `{len(docs_changed)}`",
        f"- Diff/changed-file mismatches: `{len(diff_file_mismatch)}`",
        f"- Syntax failures: `{len(bad_syntax)}`",
        f"- Empty diffs: `{len(no_diff)}`",
        f"- Missing BASE docs evidence: `{len(no_docs)}`",
        f"- Repo overlaps with consolidated corpus: `{overlap}`",
        "",
        "Synthetic design categories are augmentation metadata only. A reviewer must independently approve or exclude every row before any training use; no validation/confirmation set is modified.",
    ]
    (OUT / "audits/synthetic_case_quality_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return audit


def main() -> int:
    provenance = provenance_audit()
    candidates = load_jsonl(OUT / "cases/synthetic_candidates.jsonl")
    rejects = load_jsonl(OUT / "cases/synthetic_rejects.jsonl")
    review_batches(candidates)
    audit = quality_audit(candidates, rejects, provenance)
    summary_path = OUT / "reports/pilot_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    summary.update({
        "human_review_rows": len(candidates),
        "human_review_batch_count": (len(candidates) + 49) // 50,
        "quality_audit_pass": audit["all_candidates_pre_review_valid"],
        "models_trained": False,
        "training_use": "pending_human_review",
        "repository_candidate_counts": audit["repository_counts"],
        "selected_repositories_with_candidates": sum(1 for count in audit["repository_counts"].values() if count),
        "reject_reason_counts": dict(Counter(row.get("reason") for row in rejects)),
        "output_root": str(OUT),
        "cache_root": r"C:\Users\mahmu\Desktop\controlled_synthetic_repo_cache_v1",
        "cache_file_count": sum(1 for _ in Path(r"C:\Users\mahmu\Desktop\controlled_synthetic_repo_cache_v1").rglob("*") if _.is_file()),
        "cache_bytes": sum(_.stat().st_size for _ in Path(r"C:\Users\mahmu\Desktop\controlled_synthetic_repo_cache_v1").rglob("*") if _.is_file()),
        "models_trained": False,
    })
    write_json(summary_path, summary)
    (OUT / "reports/pilot_summary.md").write_text(
        "# Controlled Synthetic Positive Pilot v1\n\n"
        f"- Selected repositories: `{summary.get('selected_count')}`\n"
        f"- Candidates: `{summary.get('candidate_count')}`\n"
        f"- Rejects: `{summary.get('reject_count')}`\n"
        f"- Category counts: `{summary.get('category_counts')}`\n"
        f"- Language counts: `{summary.get('language_counts')}`\n"
        f"- Candidate counts by selected repository: `{summary.get('repository_candidate_counts')}`\n"
        f"- Reject reasons: `{summary.get('reject_reason_counts')}`\n"
        f"- External snapshot cache: `{summary.get('cache_file_count')}` files / `{summary.get('cache_bytes')}` bytes\n"
        f"- Human review batches: `{summary.get('human_review_batch_count')}` (50 rows each)\n"
        f"- Automated quality gates: `{'PASS' if summary.get('quality_audit_pass') else 'FAIL'}`\n"
        "- Models trained in this phase: `False`\n"
        "- Synthetic cases are training augmentation only and remain pending independent human review.\n"
        f"- Output root: `{OUT}`\n"
        "- Review files: `human_review/prefilled.jsonl`, `human_review/review_batches/batch_001..004.{jsonl,csv}`\n"
        "- Quality evidence: `audits/synthetic_case_quality_audit.json/.md`\n",
        encoding="utf-8",
    )
    provenance_manifest = {
        "version": "controlled_synthetic_positive_v1",
        "case_origin": "controlled_synthetic_positive_v1",
        "synthetic_case": True,
        "training_only": True,
        "natural_validation_confirmation_excluded": True,
        "candidate_count": len(candidates),
        "reject_count": len(rejects),
        "category_counts": dict(Counter(row.get("synthetic_category_by_design") for row in candidates)),
        "language_counts": dict(Counter(row.get("language") for row in candidates)),
        "candidate_sha256": hashlib.sha256((OUT / "cases/synthetic_candidates.jsonl").read_bytes()).hexdigest(),
        "review_prefilled_sha256": hashlib.sha256((OUT / "human_review/prefilled.jsonl").read_bytes()).hexdigest(),
        "review_status_initial": "pending",
        "human_review_required": True,
    }
    write_json(OUT / "reports/provenance_manifest.json", provenance_manifest)
    print(json.dumps({"provenance": provenance, "quality_audit": audit}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
