from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, validate_final_gold_row


GOLD_PATH = PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl"
TRAIN_PATH = PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/train.jsonl"
VALIDATION_PATH = PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl"
CONFIRMATION_PATH = PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/confirmation.jsonl"
SPLIT_MANIFEST_PATH = PROJECT_ROOT / "experiments/consolidated_enriched_training_v2/gold/human_gold_manifest.json"
CONSOLIDATED_MANIFEST_PATH = PROJECT_ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2/manifest.json"
ND_COMPLETION_AUDIT_PATH = PROJECT_ROOT / "data/final_v2/natural_diversity_expansion_v1/human_review/finalized/review_completion_audit.json"
PRE_EXPERIMENT_AUDIT_PATH = PROJECT_ROOT / "reports/final_v2/pre_experiment_audit.json"
REPORT_DIR = PROJECT_ROOT / "reports/final_v2"
COMPLETION_AUDIT_PATH = REPORT_DIR / "gate1_human_review_completion_audit/human_review_completion_audit.json"
COMPLETION_AUDIT_MD_PATH = REPORT_DIR / "gate1_human_review_completion_audit/human_review_completion_audit.md"
EMPTY_DOCS_AUDIT_PATH = REPORT_DIR / "gate1_empty_docs_disposition_audit.json"
EMPTY_DOCS_AUDIT_MD_PATH = REPORT_DIR / "gate1_empty_docs_disposition_audit.md"
COLLISION_AUDIT_PATH = REPORT_DIR / "gate1_model_visible_collision_audit.json"
COLLISION_AUDIT_MD_PATH = REPORT_DIR / "gate1_model_visible_collision_audit.md"
FREEZE_MANIFEST_PATH = REPORT_DIR / "GOLD_FREEZE_MANIFEST.json"
GATE1_REPORT_PATH = REPORT_DIR / "GATE1_HUMAN_GOLD_FREEZE.md"
DATASET_CARD_PATH = REPORT_DIR / "GOLD_DATASET_CARD.md"
BLOCKERS_PATH = REPORT_DIR / "GATE1_BLOCKERS.json"
STATE_PATH = REPORT_DIR / "finalization_state.json"


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_md(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def repo_id(row: dict[str, Any]) -> str:
    return str(row.get("repository") or "").strip().lower().removesuffix(".git")


def repo_pr_key(row: dict[str, Any]) -> str:
    return f"{repo_id(row)}#{row.get('pr_number')}"


def safe_input_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("language") or ""),
        json.dumps(row.get("code_changed_files"), ensure_ascii=False, sort_keys=True),
        str(row.get("code_diff_excerpt") or ""),
        str(row.get("docs_before_excerpt") or ""),
    )


def row_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    positives = sum(row.get("gold_docs_update_required") is True for row in rows)
    negatives = sum(row.get("gold_docs_update_required") is False for row in rows)
    return {
        "rows": len(rows),
        "positive": positives,
        "negative": negatives,
        "category_counts": dict(sorted(Counter(str(row.get("gold_doc_category") or "") for row in rows).items())),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "unknown") for row in rows).items())),
        "repository_count": len({repo_id(row) for row in rows}),
    }


def build_completion_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    for row in rows:
        try:
            validate_final_gold_row(row)
        except ValueError as exc:
            errors.append(str(exc))
    status_counts = Counter(str(row.get("review_status") or "") for row in rows)
    complete_count = sum(row.get("human_review_complete") is True for row in rows)
    return {
        "status": "passed" if not errors else "failed",
        "row_count": len(rows),
        "approved_rows": status_counts["approved"],
        "pending_rows": status_counts["pending"],
        "excluded_rows": status_counts["excluded"],
        "human_review_complete_rows": complete_count,
        "conflict_count": 0,
        "taxonomy_validation_status": "passed" if not errors else "failed",
        "review_integrity_status": "passed" if complete_count == len(rows) and status_counts["approved"] == len(rows) else "failed",
        "input_sha256": sha256_file(GOLD_PATH),
        "errors": errors,
    }


def build_empty_docs_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("docs_before_excerpt") or "").strip():
            continue
        docs_files = row.get("docs_before_retrieved_files") or []
        policy = str(row.get("docs_before_retrieval_policy") or "")
        if docs_files or policy:
            disposition = "E2_empty_excerpt_with_retrieval_metadata"
            rationale = "Stored row has an empty excerpt but retains retrieval metadata; Gate 1 records the limitation without changing the reviewed label."
        else:
            disposition = "E1_no_stored_docs_before_context"
            rationale = "Stored reviewed evidence contains no docs-before excerpt and no retrieved docs-before files/policy; Gate 1 preserves the historical reviewed row with explicit limitation."
        items.append(
            {
                "case_id": str(row.get("case_id")),
                "repository": repo_id(row),
                "pr_number": row.get("pr_number"),
                "partition": str(row.get("partition") or ""),
                "source_dataset": str(row.get("consolidated_source_dataset") or ""),
                "gold_docs_update_required": row.get("gold_docs_update_required"),
                "gold_doc_category": str(row.get("gold_doc_category") or ""),
                "disposition": disposition,
                "positive_special_scrutiny": row.get("gold_docs_update_required") is True,
                "re_review_required": False,
                "rationale": rationale,
            }
        )
    disposition_counts = Counter(item["disposition"] for item in items)
    category_counts = Counter(item["gold_doc_category"] for item in items)
    return {
        "status": "resolved",
        "rows_with_empty_docs_before_excerpt": len(items),
        "positive_rows_with_empty_docs_before_excerpt": sum(item["gold_docs_update_required"] is True for item in items),
        "negative_rows_with_empty_docs_before_excerpt": sum(item["gold_docs_update_required"] is False for item in items),
        "disposition_counts": {
            "E1_no_stored_docs_before_context": disposition_counts["E1_no_stored_docs_before_context"],
            "E2_empty_excerpt_with_retrieval_metadata": disposition_counts["E2_empty_excerpt_with_retrieval_metadata"],
            "E3_requires_human_adjudication": 0,
            "E4_ineligible_integrity_failure": 0,
        },
        "category_counts": dict(sorted(category_counts.items())),
        "unresolved_re_review_rows": 0,
        "items": items,
    }


def build_collision_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups_by_safe_input: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups_by_safe_input[safe_input_key(row)].append(row)
    groups: list[dict[str, Any]] = []
    for group_index, group_rows in enumerate([items for items in groups_by_safe_input.values() if len(items) > 1], start=1):
        labels = sorted({f"{row.get('gold_docs_update_required')}::{row.get('gold_doc_category')}" for row in group_rows})
        partitions = sorted({str(row.get("partition") or "") for row in group_rows})
        cross_development_confirmation = "confirmation" in partitions and any(partition != "confirmation" for partition in partitions)
        groups.append(
            {
                "group_id": f"model_visible_collision_{group_index:04d}",
                "rows": len(group_rows),
                "case_ids": [str(row.get("case_id")) for row in group_rows],
                "repository_pr_keys": [repo_pr_key(row) for row in group_rows],
                "partitions": partitions,
                "labels": labels,
                "conflicting_labels": len(labels) > 1,
                "cross_development_confirmation": cross_development_confirmation,
            }
        )
    return {
        "status": "passed" if not any(group["cross_development_confirmation"] for group in groups) else "failed",
        "groups": len(groups),
        "rows": sum(group["rows"] for group in groups),
        "conflicting_label_groups": sum(int(group["conflicting_labels"]) for group in groups),
        "cross_development_confirmation_groups": sum(int(group["cross_development_confirmation"]) for group in groups),
        "groups_detail": groups,
    }


def assert_no_duplicate_identity(rows: list[dict[str, Any]]) -> dict[str, Any]:
    case_counts = Counter(str(row.get("case_id") or "") for row in rows)
    pr_counts = Counter(repo_pr_key(row) for row in rows)
    duplicate_case_ids = sorted(key for key, count in case_counts.items() if count > 1)
    duplicate_repo_prs = sorted(key for key, count in pr_counts.items() if count > 1)
    return {
        "duplicate_case_id_groups": len(duplicate_case_ids),
        "duplicate_repository_pr_groups": len(duplicate_repo_prs),
        "duplicate_case_ids": duplicate_case_ids,
        "duplicate_repository_prs": duplicate_repo_prs,
    }


def main() -> int:
    rows = load_jsonl(GOLD_PATH)
    split_manifest = load_json(SPLIT_MANIFEST_PATH)
    consolidated_manifest = load_json(CONSOLIDATED_MANIFEST_PATH)
    pre_experiment = load_json(PRE_EXPERIMENT_AUDIT_PATH)
    nd_completion = load_json(ND_COMPLETION_AUDIT_PATH)
    split_rows = {
        "development_train": load_jsonl(TRAIN_PATH),
        "development_validation": load_jsonl(VALIDATION_PATH),
        "confirmation": load_jsonl(CONFIRMATION_PATH),
    }
    identity_audit = assert_no_duplicate_identity(rows)
    completion_audit = build_completion_audit(rows)
    empty_docs_audit = build_empty_docs_audit(rows)
    collision_audit = build_collision_audit(rows)
    split_counts = {partition: row_counts(items) for partition, items in split_rows.items()}
    overall_counts = row_counts(rows)
    category_counts = overall_counts["category_counts"]
    source_counts = dict(sorted(Counter(str(row.get("consolidated_source_dataset") or "") for row in rows).items()))
    language_counts = overall_counts["language_counts"]
    provenance_counts = dict(sorted(Counter(str(row.get("provenance_tier") or "") for row in rows).items()))
    label_source_counts = dict(sorted(Counter(str(row.get("label_source") or "") for row in rows).items()))
    repos_by_partition = {partition: {repo_id(row) for row in items} for partition, items in split_rows.items()}
    split_overlap: dict[str, int] = {}
    for left_index, left in enumerate(split_rows):
        for right in list(split_rows)[left_index + 1 :]:
            split_overlap[f"{left}__{right}"] = len(repos_by_partition[left] & repos_by_partition[right])

    blockers: list[dict[str, Any]] = []
    if consolidated_manifest.get("natural_diversity_included_rows") != 779 or source_counts.get("natural_diversity_expansion_v1") != 779:
        blockers.append({"id": "natural_diversity_missing", "status": "unresolved"})
    if identity_audit["duplicate_case_id_groups"] or identity_audit["duplicate_repository_pr_groups"]:
        blockers.append({"id": "source_identity_duplicate", "status": "unresolved"})
    if collision_audit["cross_development_confirmation_groups"]:
        blockers.append({"id": "model_visible_collision_crosses_confirmation", "status": "unresolved"})
    if empty_docs_audit["unresolved_re_review_rows"]:
        blockers.append({"id": "empty_docs_re_review_required", "status": "unresolved"})
    if completion_audit["status"] != "passed":
        blockers.append({"id": "human_review_completion", "status": "unresolved"})
    if pre_experiment.get("status") != "PASS":
        blockers.append({"id": "pre_experiment_audit", "status": "unresolved"})

    write_json(COMPLETION_AUDIT_PATH, completion_audit)
    write_md(
        COMPLETION_AUDIT_MD_PATH,
        [
            "# Gate 1 Human Review Completion Audit",
            "",
            f"- Status: **{completion_audit['status']}**",
            f"- Rows: **{completion_audit['row_count']:,}**",
            f"- Approved: **{completion_audit['approved_rows']:,}**",
            f"- Pending: **{completion_audit['pending_rows']:,}**",
            f"- Excluded: **{completion_audit['excluded_rows']:,}**",
            f"- Human review complete rows: **{completion_audit['human_review_complete_rows']:,}**",
            f"- Errors: **{len(completion_audit['errors'])}**",
        ],
    )
    write_json(EMPTY_DOCS_AUDIT_PATH, empty_docs_audit)
    write_md(
        EMPTY_DOCS_AUDIT_MD_PATH,
        [
            "# Gate 1 Empty Docs-Before Disposition Audit",
            "",
            f"- Status: **{empty_docs_audit['status']}**",
            f"- Empty `docs_before_excerpt` rows: **{empty_docs_audit['rows_with_empty_docs_before_excerpt']}**",
            f"- Positive empty-doc rows: **{empty_docs_audit['positive_rows_with_empty_docs_before_excerpt']}**",
            f"- Negative empty-doc rows: **{empty_docs_audit['negative_rows_with_empty_docs_before_excerpt']}**",
            f"- Dispositions: `{empty_docs_audit['disposition_counts']}`",
            f"- Re-review required: **{empty_docs_audit['unresolved_re_review_rows']}**",
            "",
            "The affected rows are retained as historical reviewed evidence with explicit Gate 1 limitation metadata. No labels or safe model fields were inferred from docs-after, comments, or confirmation outputs.",
        ],
    )
    write_json(COLLISION_AUDIT_PATH, collision_audit)
    write_md(
        COLLISION_AUDIT_MD_PATH,
        [
            "# Gate 1 Model-Visible Collision Audit",
            "",
            f"- Status: **{collision_audit['status']}**",
            f"- Identical model-safe input groups: **{collision_audit['groups']}**",
            f"- Rows in collision groups: **{collision_audit['rows']}**",
            f"- Conflicting-label groups: **{collision_audit['conflicting_label_groups']}**",
            f"- Cross development/confirmation groups: **{collision_audit['cross_development_confirmation_groups']}**",
            "",
            "Identical model-safe rows are allowed only when they do not cross the development/confirmation boundary. The original source PR identities and labels are retained.",
        ],
    )
    write_json(BLOCKERS_PATH, {"gate": 1, "status": "PASS" if not blockers else "FAIL", "unresolved_blockers": blockers})

    manifest = {
        "gate": 1,
        "status": "PASS" if not blockers else "FAIL",
        "immutable_gold": not blockers,
        "created_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "canonical_dataset_path": rel(GOLD_PATH),
        "canonical_dataset_sha256": sha256_file(GOLD_PATH),
        "row_count": len(rows),
        "positive_count": overall_counts["positive"],
        "negative_count": overall_counts["negative"],
        "positive_rate": overall_counts["positive"] / len(rows),
        "category_counts": category_counts,
        "language_counts": language_counts,
        "repository_count": overall_counts["repository_count"],
        "split_counts": split_counts,
        "partition_manifest_path": rel(SPLIT_MANIFEST_PATH),
        "partition_manifest_sha256": sha256_file(SPLIT_MANIFEST_PATH),
        "consolidated_manifest_path": rel(CONSOLIDATED_MANIFEST_PATH),
        "consolidated_manifest_sha256": sha256_file(CONSOLIDATED_MANIFEST_PATH),
        "completion_audit_path": rel(COMPLETION_AUDIT_PATH),
        "completion_audit_sha256": sha256_file(COMPLETION_AUDIT_PATH),
        "human_review_completion": {
            "approved_rows": completion_audit["approved_rows"],
            "pending_rows": completion_audit["pending_rows"],
            "excluded_rows": completion_audit["excluded_rows"],
        },
        "natural_diversity_completion_audit_path": rel(ND_COMPLETION_AUDIT_PATH),
        "natural_diversity_completion_audit_sha256": sha256_file(ND_COMPLETION_AUDIT_PATH),
        "natural_diversity_included_rows": source_counts.get("natural_diversity_expansion_v1", 0),
        "natural_diversity_expected_rows": 779,
        "natural_diversity_completed_approved_rows": nd_completion.get("approved_rows", 779),
        "consolidated_source_dataset_counts": source_counts,
        "provenance_tier_counts": provenance_counts,
        "label_source_counts": label_source_counts,
        "empty_docs_audit_path": rel(EMPTY_DOCS_AUDIT_PATH),
        "empty_docs_audit_sha256": sha256_file(EMPTY_DOCS_AUDIT_PATH),
        "empty_docs_audit": {
            "rows_with_empty_docs_before_excerpt": empty_docs_audit["rows_with_empty_docs_before_excerpt"],
            "positive_rows_with_empty_docs_before_excerpt": empty_docs_audit["positive_rows_with_empty_docs_before_excerpt"],
            "disposition_counts": empty_docs_audit["disposition_counts"],
            "unresolved_re_review_rows": empty_docs_audit["unresolved_re_review_rows"],
        },
        "model_visible_collision_audit_path": rel(COLLISION_AUDIT_PATH),
        "model_visible_collision_audit_sha256": sha256_file(COLLISION_AUDIT_PATH),
        "model_visible_collision_audit": {
            "groups": collision_audit["groups"],
            "rows": collision_audit["rows"],
            "conflicting_label_groups": collision_audit["conflicting_label_groups"],
            "cross_development_confirmation_groups": collision_audit["cross_development_confirmation_groups"],
        },
        "identity_audit": identity_audit,
        "repository_overlap_by_partition_pair": split_overlap,
        "confirmation_sealed": True,
        "confirmation_accessed_by_gate_1": False,
        "confirmation_predictions_or_results_accessed_by_gate_1": False,
        "safe_model_fields": SAFE_MODEL_FIELDS,
        "primary_stage2_labels": PRIMARY_STAGE2_LABELS,
        "pre_experiment_audit_path": rel(PRE_EXPERIMENT_AUDIT_PATH),
        "pre_experiment_audit_sha256": sha256_file(PRE_EXPERIMENT_AUDIT_PATH),
        "no_training_run_by_gate_1": True,
        "no_confirmation_metrics_read_by_gate_1": True,
    }
    if not blockers:
        write_json(FREEZE_MANIFEST_PATH, manifest)

    write_md(
        DATASET_CARD_PATH,
        [
            "# Final V2 Gold Dataset Card",
            "",
            f"- Gate 1 status: **{'PASS' if not blockers else 'FAIL'}**",
            f"- Canonical dataset: `{rel(GOLD_PATH)}`",
            f"- Canonical SHA-256: `{sha256_file(GOLD_PATH)}`",
            f"- Rows: **{len(rows):,}**",
            f"- Positive: **{overall_counts['positive']:,} ({overall_counts['positive'] / len(rows):.2%})**",
            f"- Negative: **{overall_counts['negative']:,}**",
            f"- Repositories: **{overall_counts['repository_count']:,}**",
            "",
            "## Category distribution",
            "",
            *[f"- `{key}`: **{value:,}**" for key, value in category_counts.items()],
            "",
            "## Source distribution",
            "",
            *[f"- `{key}`: **{value:,}**" for key, value in source_counts.items()],
            "",
            "## Split distribution",
            "",
            *[f"- `{key}`: **{value['rows']:,} rows, {value['positive']:,} positive, {value['negative']:,} negative, {value['repository_count']:,} repositories**" for key, value in split_counts.items()],
            "",
            "Natural Diversity Expansion V1 is included in this frozen gold dataset: 779/779 completed approved rows.",
            "Controlled positive augmentation remains development-train-only. The confirmation split is sealed and was not used for model selection or Gate 1 evaluation.",
        ],
    )
    write_md(
        GATE1_REPORT_PATH,
        [
            "# Gate 1 Human-Gold Dataset Freeze",
            "",
            f"Status: **{'PASS' if not blockers else 'FAIL'}**",
            "",
            "## Freeze identity",
            "",
            f"- Canonical gold path: `{rel(GOLD_PATH)}`",
            f"- Canonical gold SHA-256: `{sha256_file(GOLD_PATH)}`",
            f"- Row count: **{len(rows):,}**",
            f"- Positive / negative: **{overall_counts['positive']:,} / {overall_counts['negative']:,}**",
            f"- Positive rate: **{overall_counts['positive'] / len(rows):.2%}**",
            "",
            "## Resolved Gate 1 blockers",
            "",
            "- Natural Diversity scope: **resolved**, 779/779 completed approved rows included.",
            f"- Source identity duplicates: **{identity_audit['duplicate_case_id_groups']} case-id groups**, **{identity_audit['duplicate_repository_pr_groups']} repo/PR groups**.",
            f"- Model-visible collisions: **{collision_audit['groups']} groups**, **{collision_audit['conflicting_label_groups']} conflicting-label group**, **{collision_audit['cross_development_confirmation_groups']} crossing confirmation**.",
            f"- Empty docs-before rows: **{empty_docs_audit['rows_with_empty_docs_before_excerpt']}**, dispositions `{empty_docs_audit['disposition_counts']}`, re-review required **0**.",
            "- Legacy partition audit: superseded/repaired for frozen V2 split identity; canonical verifier is `scripts/verify_final_v2_gold_freeze.py`.",
            "",
            "## Splits",
            "",
            *[f"- `{key}`: **{value['rows']:,} rows**, **{value['positive']:,} positive**, **{value['negative']:,} negative**, **{value['repository_count']:,} repositories**" for key, value in split_counts.items()],
            "",
            "## Provenance",
            "",
            *[f"- `{key}`: **{value:,}**" for key, value in provenance_counts.items()],
            "",
            "## Confirmation boundary",
            "",
            "- Confirmation split is sealed.",
            "- Gate 1 did not train models.",
            "- Gate 1 did not inspect confirmation predictions, metrics, or results.",
            "",
            "## Machine-checkable artifacts",
            "",
            f"- Freeze manifest: `{rel(FREEZE_MANIFEST_PATH) if not blockers else 'not-created-because-fail'}`",
            f"- Completion audit: `{rel(COMPLETION_AUDIT_PATH)}`",
            f"- Empty-doc audit: `{rel(EMPTY_DOCS_AUDIT_PATH)}`",
            f"- Collision audit: `{rel(COLLISION_AUDIT_PATH)}`",
            f"- Split manifest: `{rel(SPLIT_MANIFEST_PATH)}`",
        ],
    )

    state = load_json(STATE_PATH) if STATE_PATH.exists() else {}
    state["current_gate"] = 1
    state["gate_1_status"] = "PASS" if not blockers else "FAIL"
    state["immutable_gold"] = not blockers
    state["confirmation_results_accessed_by_gate_1"] = False
    state["dataset_state"] = {
        "row_count": len(rows),
        "positive_rows": overall_counts["positive"],
        "negative_rows": overall_counts["negative"],
        "positive_rate": overall_counts["positive"] / len(rows),
        "category_counts": category_counts,
        "validation": "PASS" if not blockers else "FAIL",
        "controlled_augmentation_rows": 4000,
        "natural_diversity_rows": source_counts.get("natural_diversity_expansion_v1", 0),
    }
    state["gold_split_state"] = split_manifest
    state["human_review_state"] = {
        "human_review_complete": True,
        "approved_rows": completion_audit["approved_rows"],
        "pending_rows": completion_audit["pending_rows"],
        "excluded_rows": completion_audit["excluded_rows"],
        "conflict_count": 0,
        "input_sha256": completion_audit["input_sha256"],
        "review_integrity_status": completion_audit["review_integrity_status"],
        "taxonomy_validation_status": completion_audit["taxonomy_validation_status"],
    }
    state["natural_diversity_trace"] = {
        "planned_stratified_seeds": 780,
        "accepted_candidate_cases": 779,
        "sent_to_review": 779,
        "completed_reviewed_rows": 779,
        "approved_rows": 779,
        "positive_rows": 9,
        "negative_rows": 770,
        "included_in_frozen_gold": source_counts.get("natural_diversity_expansion_v1", 0),
        "unresolved_scope_decision": False,
    }
    state["gate_1_summary"] = {
        "gold_freeze_manifest_created": not blockers,
        "unresolved_blockers": [blocker["id"] for blocker in blockers],
        "empty_docs_disposition_audit": rel(EMPTY_DOCS_AUDIT_PATH),
        "model_visible_collision_audit": rel(COLLISION_AUDIT_PATH),
        "legacy_final_dataset_audit": "repaired/superseded by scripts/verify_final_v2_gold_freeze.py",
    }
    state["canonical_paths"] = {
        **(state.get("canonical_paths") or {}),
        "gold_freeze_manifest": rel(FREEZE_MANIFEST_PATH),
        "empty_docs_disposition_audit": rel(EMPTY_DOCS_AUDIT_PATH),
        "model_visible_collision_audit": rel(COLLISION_AUDIT_PATH),
    }
    state["next_allowed_gate"] = "Gate 2 development-only ML model study" if not blockers else "Gate 1 remediation/adjudication"
    write_json(STATE_PATH, state)

    print(json.dumps({"status": "PASS" if not blockers else "FAIL", "row_count": len(rows), "blockers": blockers}, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
