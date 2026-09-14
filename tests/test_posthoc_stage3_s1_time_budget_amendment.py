from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import (
    THRESHOLDS,
    assign_cases_to_workers,
    merge_reranker_sources,
    next_prompt_selection_population,
    paired_prompt_run_keys,
    prompt_selection_case_ids,
    reranker_worker_count,
    select_prompt_from_completed_blind_review,
    selected_prompt_missing_run_keys,
    write_blind_review,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


def frozen_rows():
    return [
        {"case_id": f"case-{index:03d}", "code_changed_files": [f"src/{index}.py"], "code_diff_excerpt": f"diff-{index}", "docs_before_excerpt": f"docs-{index}"}
        for index in range(200)
    ]


def test_initial_subset_is_deterministic_25_primary_and_25_secondary():
    rows = frozen_rows()
    selected = prompt_selection_case_ids(rows, 50)
    expected_primary = sorted(
        (row["case_id"] for row in rows[:100]), key=lambda case_id: hashlib.sha256(f"42:{case_id}".encode()).hexdigest()
    )[:25]
    expected_secondary = sorted(
        (row["case_id"] for row in rows[100:]), key=lambda case_id: hashlib.sha256(f"42:{case_id}".encode()).hexdigest()
    )[:25]
    assert selected == [*expected_primary, *expected_secondary]
    assert len(set(selected) & {row["case_id"] for row in rows[:100]}) == 25
    assert len(set(selected) & {row["case_id"] for row in rows[100:]}) == 25


def test_subset_is_independent_of_model_outputs():
    rows = frozen_rows()
    expected = prompt_selection_case_ids(rows, 100)
    for index, row in enumerate(rows):
        row.update({"reranker_score": index / 200, "critic": {"decision": "ACCEPT" if index % 2 else "ABSTAIN"}})
    assert prompt_selection_case_ids(rows, 100) == expected


def test_two_gpu_worker_assignment_is_frozen_index_modulo_two():
    rows = frozen_rows()
    assignments = assign_cases_to_workers(rows, {row["case_id"] for row in rows}, 2)
    assert assignments[0] == [row["case_id"] for row in rows[0::2]]
    assert assignments[1] == [row["case_id"] for row in rows[1::2]]
    assert reranker_worker_count(2) == 2


@pytest.mark.parametrize("device_count", [0, 1])
def test_fewer_than_two_gpus_uses_single_worker_fallback(device_count):
    assert reranker_worker_count(device_count) == 1


def record(case_id, score):
    return {"case_id": case_id, "candidate_indices": [0], "scores": {"0": score}}


def test_worker_shards_merge_in_original_frozen_order():
    rows = frozen_rows()[:4]
    expected = {row["case_id"]: [0] for row in rows}
    shard_zero = {rows[0]["case_id"]: record(rows[0]["case_id"], 0.1), rows[2]["case_id"]: record(rows[2]["case_id"], 0.3)}
    shard_one = {rows[1]["case_id"]: record(rows[1]["case_id"], 0.2), rows[3]["case_id"]: record(rows[3]["case_id"], 0.4)}
    merged = merge_reranker_sources(rows, expected, [shard_zero, shard_one])
    assert list(merged) == [row["case_id"] for row in rows]


def test_worker_shard_merge_rejects_duplicate_and_missing_cases():
    rows = frozen_rows()[:2]
    expected = {row["case_id"]: [0] for row in rows}
    first = {rows[0]["case_id"]: record(rows[0]["case_id"], 0.1)}
    with pytest.raises(RuntimeError, match="missing"):
        merge_reranker_sources(rows, expected, [first])
    with pytest.raises(RuntimeError, match="Duplicate"):
        merge_reranker_sources(rows, expected, [first, first])


def test_amendment03_adaptive_reranking_and_checkpoint_reuse_remain_active():
    source = (BASE / "scripts/run_s1_development_gpu.py").read_text(encoding="utf-8")
    retrieval = (BASE / "scripts/retrieval.py").read_text(encoding="utf-8")
    assert "load_valid_reranker_checkpoints" in source
    assert "if case_id in completed:" in source
    assert "self._score_adaptive" in retrieval
    assert "except self.torch.cuda.OutOfMemoryError" in retrieval
    assert "RERANKER_MAX_LENGTH = 8192" in retrieval


def paired_outcomes(rows):
    return {
        variant: {
            row["case_id"]: {
                "target_decision": {"target_document": f"docs/{row['case_id']}.md"},
                "patch": {"patch_markdown": f"{variant} patch for {row['case_id']}"},
            }
            for row in rows
        }
        for variant in ("P1", "P2")
    }


def test_phase_a_is_bounded_and_blind_then_stops(tmp_path):
    rows = frozen_rows()
    keys = paired_prompt_run_keys(rows, 50)
    selected_rows = {case_id for case_id in prompt_selection_case_ids(rows, 50)}
    assert len(keys) == 100
    assert {key.split(":", 1)[1] for key in keys} == selected_rows
    subset = [row for row in rows if row["case_id"] in selected_rows]
    review = write_blind_review(tmp_path, subset, paired_outcomes(subset))
    header = (tmp_path / "s1_development_blind_prompt_review.csv").read_text(encoding="utf-8-sig").splitlines()[0]
    assert "P1" not in header and "P2" not in header
    assert review["status"] == "BLIND_DEVELOPMENT_REVIEW_REQUIRED"
    source = (BASE / "scripts/run_s1_development_gpu.py").read_text(encoding="utf-8")
    assert '"state": "PROMPT_SELECTION_BLIND_REVIEW_REQUIRED"' in source
    assert "return 0" in source[source.index('print("PROMPT_SELECTION_BLIND_REVIEW_REQUIRED")'):]


REVIEW_FIELDS = [
    "review_item_id", "reviewer_preference",
    "reviewer_target_fit_A", "reviewer_target_fit_B", "reviewer_grounding_A", "reviewer_grounding_B",
    "reviewer_usefulness_A", "reviewer_usefulness_B", "reviewer_style_fit_A", "reviewer_style_fit_B",
]


def write_completed_review(tmp_path, rows, mappings):
    sheet = tmp_path / "review.csv"
    with sheet.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    mapping = tmp_path / "mapping.json"
    mapping.write_text(json.dumps({"rows": mappings}), encoding="utf-8")
    return sheet, mapping


def judgment_row(item, preference, a="yes", b="no"):
    row = {"review_item_id": item, "reviewer_preference": preference}
    for dimension in ("target_fit", "grounding", "usefulness", "style_fit"):
        row[f"reviewer_{dimension}_A"] = a
        row[f"reviewer_{dimension}_B"] = b
    return row


def test_human_preference_rule_wins_without_self_critic_metrics(tmp_path):
    sheet, mapping = write_completed_review(
        tmp_path,
        [judgment_row("r1", "A"), judgment_row("r2", "B"), judgment_row("r3", "A")],
        [
            {"review_item_id": "r1", "candidate_A": "P2", "candidate_B": "P1"},
            {"review_item_id": "r2", "candidate_A": "P1", "candidate_B": "P2"},
            {"review_item_id": "r3", "candidate_A": "P2", "candidate_B": "P1"},
        ],
    )
    result = select_prompt_from_completed_blind_review(sheet, mapping)
    assert result["selected_prompt_variant"] == "P2"
    assert result["selection_basis"] == "reviewer_preference"


def test_human_positive_judgments_break_preference_tie(tmp_path):
    sheet, mapping = write_completed_review(
        tmp_path,
        [judgment_row("r1", "A", "yes", "no"), judgment_row("r2", "A", "yes", "yes")],
        [
            {"review_item_id": "r1", "candidate_A": "P1", "candidate_B": "P2"},
            {"review_item_id": "r2", "candidate_A": "P2", "candidate_B": "P1"},
        ],
    )
    result = select_prompt_from_completed_blind_review(sheet, mapping)
    assert result["reviewer_preference_counts"] == {"P1": 1, "P2": 1}
    assert result["selected_prompt_variant"] == "P1"
    assert result["selection_basis"] == "total_human_positive_judgments"


def test_exact_human_tie_uses_deterministic_p1_tiebreaker(tmp_path):
    sheet, mapping = write_completed_review(
        tmp_path,
        [judgment_row("r1", "A", "yes", "yes"), judgment_row("r2", "A", "yes", "yes")],
        [
            {"review_item_id": "r1", "candidate_A": "P1", "candidate_B": "P2"},
            {"review_item_id": "r2", "candidate_A": "P2", "candidate_B": "P1"},
        ],
    )
    result = select_prompt_from_completed_blind_review(sheet, mapping)
    assert result["selected_prompt_variant"] == "P1"
    assert result["selection_basis"] == "preregistered_deterministic_tiebreaker"


def test_extension_is_next_25_and_never_exceeds_100():
    assert next_prompt_selection_population(50, 19) == 75
    assert next_prompt_selection_population(75, 19) == 100
    assert next_prompt_selection_population(100, 0) == 100
    assert next_prompt_selection_population(50, 20) == 50
    rows = frozen_rows()
    first = prompt_selection_case_ids(rows, 50)
    extended = prompt_selection_case_ids(rows, 75)
    maximum = prompt_selection_case_ids(rows, 100)
    assert extended[:50] == first
    assert maximum[:75] == extended
    assert (len(set(extended) & {row["case_id"] for row in rows[:100]}), len(set(extended) & {row["case_id"] for row in rows[100:]})) == (38, 37)
    assert len(paired_prompt_run_keys(rows, 100)) == 200


def test_phase_b_runs_selected_variant_only_and_completes_200():
    rows = frozen_rows()
    case_ids = [row["case_id"] for row in rows]
    paired = prompt_selection_case_ids(rows, 50)
    completed = {f"{variant}:{case_id}" for case_id in paired for variant in ("P1", "P2")}
    missing = selected_prompt_missing_run_keys(case_ids, "P2", completed)
    assert len(missing) == 150
    assert all(key.startswith("P2:") for key in missing)
    assert not any(key.startswith("P1:") for key in missing)
    assert len({*completed, *missing} & {f"P2:{case_id}" for case_id in case_ids}) == 200


def test_thresholds_confirmation_gate6_and_canonical_boundaries_unchanged():
    assert THRESHOLDS == (0.35, 0.50, 0.65)
    prereg = json.loads((BASE / "S1_PREREGISTRATION.json").read_text(encoding="utf-8"))
    assert prereg["confirmation_accessed"] is False
    assert prereg["gate6_row_level_human_data_accessed"] is False
    assert prereg["time_budget_execution_amendment"]["prompt_selection_source"] == "completed blind human review only"
