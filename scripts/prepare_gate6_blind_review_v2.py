from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import (
    BLIND_FORBIDDEN_FIELDS,
    HUMAN_DIMENSIONS,
    NO_OUTPUT_SYSTEM_FAILURE,
    build_blind_row,
    read_jsonl,
    sample_primary,
    sha256_file,
    write_json,
)

GATE5_SOURCE_REL = Path(
    "reports/final_v2/gate5/one_shot/stage3/"
    "stage3_confirmation_generation_results.jsonl"
)
PRIMARY_SAMPLE_REL = Path("reports/final_v2/gate6/samples/primary_natural_sample.jsonl")
SECONDARY_SAMPLE_REL = Path("reports/final_v2/gate6/samples/secondary_category_stress_sample.jsonl")
CONFIRMATION_REL = Path("experiments/consolidated_enriched_training_v2/gold/confirmation.jsonl")
OUTPUT_REL = Path("reports/final_v2/gate6")

REVIEW_COLUMNS = [
    "case_id",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "selected_target_document",
    "generated_documentation_patch",
    "review_status",
    *HUMAN_DIMENSIONS,
    "human_accept_as_is",
    "human_notes",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_bytes(root: Path, relative: Path) -> bytes:
    return subprocess.check_output(
        ["git", "cat-file", "blob", f"HEAD:{relative.as_posix()}"], cwd=root
    )


def load_jsonl_bytes(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]


def normalize_reviewer_text(value: Any) -> str:
    """Remove line-ending whitespace without changing reviewer-visible semantics."""
    return "\n".join(
        line.expandtabs(4).rstrip(" ") for line in str(value or "").splitlines()
    )


def markdown_protocol() -> str:
    dimensions = "\n".join(f"- `{dimension}`: integer 1--5." for dimension in HUMAN_DIMENSIONS)
    return f"""# Gate 6 Human Evaluation Protocol

Status: **FROZEN BEFORE HUMAN SCORES**
Scope: primary natural-distribution sample only (`n = 100`). The secondary stress sample is supplementary and must never be pooled into the primary estimate.

## Blind review contract

Reviewers receive only the case identifier, language, changed files, code-diff excerpt, documentation-before excerpt, selected target document, generated documentation patch, and reviewer-entry fields. Gold/reference labels, generation provenance, verifier outcomes, confidence, repair state, and the reason an output is absent are forbidden.

## Complete-case policy

Every one of the 100 sampled primary rows remains in Gate 6. A row with no accepted generated patch is preclassified as `{NO_OUTPUT_SYSTEM_FAILURE}`. It is complete/evaluated, not incomplete or excluded. Its five human-quality dimensions and accept-as-is judgment are structurally `N/A`, and it counts as a failure in the end-to-end accept-as-is estimate.

The end-to-end acceptance denominator is always all 100 primary rows. Human-quality means and distributions are conditional on rows with an actual generated output, and their denominator must be stated explicitly. Accept-as-is is reported twice: end-to-end over all 100 primary rows and conditional on output-bearing rows only. No-output rows are never assigned numeric quality scores.

## Output-bearing rows

For each actual output, the reviewer marks `review_status = approved`, completes all five dimensions, answers `human_accept_as_is` with `yes` or `no`, and may add notes.

{dimensions}
- `human_accept_as_is`: `yes` or `no`.
- `human_notes`: optional free text.

The 1--5 ratings are ordinal, with 1 the lowest and 5 the highest assessment for the named dimension. No Gate 6 result is calculated by this preparation step.
"""


def schema_payload() -> dict[str, Any]:
    properties: dict[str, Any] = {
        "case_id": {"type": "string"},
        "language": {"type": "string"},
        "code_changed_files": {"type": "string"},
        "code_diff_excerpt": {"type": "string"},
        "docs_before_excerpt": {"type": "string"},
        "selected_target_document": {"type": "string"},
        "generated_documentation_patch": {"type": "string"},
        "review_status": {"enum": ["pending", "approved", NO_OUTPUT_SYSTEM_FAILURE]},
        "human_accept_as_is": {"enum": ["", "yes", "no", "N/A"]},
        "human_notes": {"type": "string"},
    }
    for dimension in HUMAN_DIMENSIONS:
        properties[dimension] = {
            "oneOf": [
                {"type": "integer", "minimum": 1, "maximum": 5},
                {"type": "null"},
                {"const": "N/A"},
            ]
        }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Gate 6 primary blind human review row",
        "type": "object",
        "additionalProperties": False,
        "required": REVIEW_COLUMNS,
        "properties": properties,
        "allOf": [
            {
                "if": {"properties": {"review_status": {"const": NO_OUTPUT_SYSTEM_FAILURE}}},
                "then": {
                    "properties": {
                        "generated_documentation_patch": {"const": ""},
                        "human_accept_as_is": {"const": "N/A"},
                        **{dimension: {"const": "N/A"} for dimension in HUMAN_DIMENSIONS},
                    }
                },
            },
            {
                "if": {"properties": {"review_status": {"const": "approved"}}},
                "then": {
                    "properties": {
                        "human_accept_as_is": {"enum": ["yes", "no"]},
                        **{
                            dimension: {"type": "integer", "minimum": 1, "maximum": 5}
                            for dimension in HUMAN_DIMENSIONS
                        },
                    }
                },
            },
        ],
    }


def run(root: Path) -> dict[str, Any]:
    source_path = root / GATE5_SOURCE_REL
    primary_path = root / PRIMARY_SAMPLE_REL
    secondary_path = root / SECONDARY_SAMPLE_REL
    confirmation_path = root / CONFIRMATION_REL
    output_dir = root / OUTPUT_REL
    review_dir = output_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)

    worktree_bytes = source_path.read_bytes()
    canonical_bytes = git_blob_bytes(root, GATE5_SOURCE_REL)
    if worktree_bytes.replace(b"\r\n", b"\n") != canonical_bytes.replace(b"\r\n", b"\n"):
        raise RuntimeError("Gate 5 worktree and canonical blob differ beyond line endings.")

    canonical_rows = load_jsonl_bytes(canonical_bytes)
    reconstructed = sample_primary(canonical_rows, seed=42, target_size=100)
    primary = read_jsonl(primary_path)
    primary_ids = [str(row["case_id"]) for row in primary]
    reconstructed_ids = [str(row["case_id"]) for row in reconstructed]
    if reconstructed_ids != primary_ids:
        raise RuntimeError("Ordered primary membership differs from canonical reconstruction.")
    if len(primary_ids) != 100 or len(set(primary_ids)) != 100:
        raise RuntimeError("Primary sample must contain exactly 100 unique rows.")

    confirmation_by_id = {
        str(row["case_id"]): row
        for row in read_jsonl(confirmation_path)
        if str(row.get("case_id") or "") in set(primary_ids)
    }
    if set(confirmation_by_id) != set(primary_ids):
        raise RuntimeError("Frozen confirmation context is missing primary sample rows.")

    blind_rows: list[dict[str, Any]] = []
    for sample in primary:
        context = confirmation_by_id[str(sample["case_id"])]
        merged = {
            **sample,
            "code_changed_files": context.get("code_changed_files"),
            "code_diff_excerpt": context.get("code_diff_excerpt"),
            "docs_before_excerpt": context.get("docs_before_excerpt"),
        }
        blind = build_blind_row(merged)
        blind["code_changed_files"] = "\n".join(str(item) for item in (blind["code_changed_files"] or []))
        for field in (
            "code_changed_files",
            "code_diff_excerpt",
            "docs_before_excerpt",
            "selected_target_document",
            "generated_documentation_patch",
        ):
            blind[field] = normalize_reviewer_text(blind[field])
        if list(blind) != REVIEW_COLUMNS:
            blind = {column: blind.get(column) for column in REVIEW_COLUMNS}
        blind_rows.append(blind)

    no_output_count = sum(row["review_status"] == NO_OUTPUT_SYSTEM_FAILURE for row in blind_rows)
    scorable_count = sum(row["review_status"] == "pending" for row in blind_rows)
    if (no_output_count, scorable_count) != (86, 14):
        raise RuntimeError(f"Expected 86 no-output and 14 scorable rows, got {no_output_count} and {scorable_count}.")

    leaked_columns = sorted(set(REVIEW_COLUMNS) & BLIND_FORBIDDEN_FIELDS)
    if leaked_columns:
        raise RuntimeError(f"Forbidden reviewer columns: {leaked_columns}")
    if any(set(row) != set(REVIEW_COLUMNS) for row in blind_rows):
        raise RuntimeError("Reviewer rows do not match the frozen column contract.")

    protocol_path = output_dir / "GATE6_HUMAN_EVALUATION_PROTOCOL.md"
    prereg_path = output_dir / "GATE6_HUMAN_EVALUATION_PREREGISTRATION.json"
    schema_path = output_dir / "GATE6_REVIEW_SCHEMA.json"
    csv_path = review_dir / "gate6_primary_blind_review.csv"
    manifest_path = review_dir / "gate6_primary_blind_review_manifest.json"

    protocol_path.write_text(markdown_protocol(), encoding="utf-8", newline="\n")
    write_json(schema_path, schema_payload())
    prereg = {
        "schema_version": "gate6_human_evaluation_preregistration_v1",
        "status": "FROZEN_BEFORE_HUMAN_SCORES",
        "human_scores_accessed": False,
        "seed": 42,
        "primary_target_size": 100,
        "primary_sampling": "natural_distribution_random_predicted_positive",
        "primary_denominator_policy": "ALL_100_SAMPLED_ROWS",
        "no_output_policy": NO_OUTPUT_SYSTEM_FAILURE,
        "no_output_rows_are_complete": True,
        "no_output_human_ratings": "STRUCTURALLY_NA",
        "end_to_end_acceptance_denominator": 100,
        "conditional_quality_denominator": "ROWS_WITH_ACTUAL_GENERATED_OUTPUT",
        "report_acceptance_separately": ["end_to_end_all_primary", "conditional_output_rows"],
        "human_dimensions": HUMAN_DIMENSIONS,
        "accept_as_is_values": ["yes", "no"],
        "secondary_status": "SUPPLEMENTARY_ONLY_NOT_POOLED",
        "source_sample_path": PRIMARY_SAMPLE_REL.as_posix(),
        "gate5_source_path": GATE5_SOURCE_REL.as_posix(),
        "ordered_primary_membership_matches_canonical_blob": True,
    }
    write_json(prereg_path, prereg)

    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(blind_rows)

    status_counts = Counter(row["review_status"] for row in blind_rows)
    manifest = {
        "schema_version": "gate6_primary_blind_review_manifest_v1",
        "row_count": len(blind_rows),
        "no_output_system_failure_count": no_output_count,
        "scorable_output_count": scorable_count,
        "review_status_counts": dict(status_counts),
        "seed": 42,
        "source_sample_path": PRIMARY_SAMPLE_REL.as_posix(),
        "source_sample_sha256": sha256_file(primary_path),
        "stage3_source_sample_hash_recorded": sha256_bytes(worktree_bytes),
        "gate5_worktree_file_sha256": sha256_bytes(worktree_bytes),
        "gate5_canonical_git_blob_sha256": sha256_bytes(canonical_bytes),
        "gate5_eol_audit": {
            "worktree_crlf_count": worktree_bytes.count(b"\r\n"),
            "canonical_crlf_count": canonical_bytes.count(b"\r\n"),
            "normalized_bytes_identical": True,
            "difference_only_lf_vs_crlf": True,
        },
        "canonical_primary_reconstruction": {
            "seed": 42,
            "target_size": 100,
            "ordered_case_ids_identical": True,
        },
        "columns": REVIEW_COLUMNS,
        "reviewer_fields": [*HUMAN_DIMENSIONS, "human_accept_as_is", "human_notes", "review_status"],
        "forbidden_field_audit": {
            "result": "PASS",
            "forbidden_fields": sorted(BLIND_FORBIDDEN_FIELDS),
            "forbidden_columns_present": [],
            "no_output_reason_hidden": True,
        },
        "primary_secondary_separation": {
            "primary_rows_exported": 100,
            "secondary_rows_exported": 0,
            "secondary_sample_path": SECONDARY_SAMPLE_REL.as_posix(),
            "secondary_is_supplementary": True,
        },
        "review_sheet_sha256": {"csv": sha256_file(csv_path), "xlsx": None},
        "protocol_sha256": sha256_file(protocol_path),
        "preregistration_sha256": sha256_file(prereg_path),
        "schema_sha256": sha256_file(schema_path),
    }
    write_json(manifest_path, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze Gate 6 protocol and prepare the blind primary review CSV.")
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    args = parser.parse_args()
    print(json.dumps(run(Path(args.root)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
