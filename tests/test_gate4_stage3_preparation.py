from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from docguard_llm_v2.context_adapter import assert_generation_payload_safe, normalize_documentation_context
from docguard_llm_v2.gate4_study import BINARY_MODEL_SHA256, CATEGORY_MODEL_SHA256, primary_sample, secondary_stress_sample, sha256_file
from docguard_llm_v2.pipeline import generate_semantic_documentation_patch
from scripts.run_gate4_external_qwen import _result_row, pending_run_keys, validate_external_inputs
from scripts.verify_gate4_preparation import verify


ROOT = Path(__file__).resolve().parents[1]


class NoCallLLM:
    def generate(self, *args, **kwargs):
        raise AssertionError("LLM must not be called")


def prediction(case_id: str, category: str = "api_reference", context: bool = True, partition: str = "development_validation") -> dict:
    candidates = [{"path": "docs/api.md", "excerpt": "GET /items", "source_ref": "base"}] if context else []
    return {
        "case_id": case_id,
        "partition": partition,
        "frozen_binary_prediction": True,
        "frozen_category_prediction": category,
        "retrieval_context_available": context,
        "documentation_context_candidates": candidates,
    }


def test_numbered_context_adapter_and_no_pathless_docs_before_target():
    row = {
        "docs_before_excerpt": "Must never become a target by itself",
        "doc_context_01_path": "docs/config.md",
        "doc_context_01_excerpt": " PORT=8080 ",
        "doc_context_02_path": "",
        "doc_context_02_excerpt": "incomplete",
    }
    assert normalize_documentation_context(row) == [{"path": "docs/config.md", "excerpt": "PORT=8080", "source_ref": ""}]
    assert normalize_documentation_context({"docs_before_excerpt": "pathless"}) == []


def test_legacy_direct_and_nested_context_are_normalized_deduplicated_and_sorted():
    a = {"path": "docs/z.md", "excerpt": "Z", "source_ref": "base"}
    b = {"path": "docs/a.md", "excerpt": "A", "source_ref": "base"}
    row = {
        "documentation_context_candidates": [a, b, {"path": "", "excerpt": "bad"}],
        "generator_context": {"documentation_context_candidates": [a]},
        "retrieval_context": {"documentation_context_candidates": [b]},
    }
    assert normalize_documentation_context(row) == [b, a]


def test_reference_and_gold_fields_are_rejected_before_generation():
    with pytest.raises(ValueError, match="Forbidden fields"):
        assert_generation_payload_safe({"code_diff_excerpt": "+x", "gold_doc_category": "api_reference"})
    result = generate_semantic_documentation_patch(
        docs_update_required=True,
        predicted_category="api_reference",
        code_diff="+x",
        docs_before="",
        documentation_context_candidates=[{"path": "docs/a.md", "excerpt": "A", "source_ref": "base"}],
        llm_backend=NoCallLLM(),
        forbidden_context={"docs_after_excerpt": "reference"},
    )
    assert result["llm_call_count"] == 0
    assert result["final_status"] == "human_review_required"


def test_zero_context_has_explicit_status_and_zero_calls():
    result = generate_semantic_documentation_patch(
        docs_update_required=True,
        predicted_category="configuration",
        code_diff="+x",
        docs_before="pathless",
        documentation_context_candidates=[],
        llm_backend=NoCallLLM(),
    )
    assert result["final_status"] == "retrieval_context_unavailable"
    assert result["llm_call_count"] == 0
    assert result["final_patch"] is None


def test_primary_sampling_is_reproducible_and_happens_before_context_filtering():
    rows = [prediction(f"c-{index:03d}", context=index % 5 == 0) for index in range(130)]
    first = primary_sample(rows, seed=42)
    second = primary_sample(list(reversed(rows)), seed=42)
    assert [row["case_id"] for row in first] == [row["case_id"] for row in second]
    assert len(first) == 100
    assert any(not row["retrieval_context_available"] for row in first)


def test_secondary_stress_sampling_is_exact_and_reproducible():
    categories = ["api_reference", "configuration", "developer_setup", "model_contract"]
    rows = [prediction(f"{category}-{index:02d}", category, partition="development_train") for category in categories for index in range(30)]
    first = secondary_stress_sample(rows, seed=42)
    second = secondary_stress_sample(list(reversed(rows)), seed=42)
    assert first == second
    assert {category: sum(row["frozen_category_prediction"] == category for row in first) for category in categories} == {category: 25 for category in categories}


def test_resume_keys_do_not_duplicate_completed_cases():
    rows = [{"sample_name": "primary", "case_id": "a"}, {"sample_name": "primary", "case_id": "b"}]
    assert pending_run_keys(rows, [{"run_key": "primary::a"}]) == ["primary::b"]
    with pytest.raises(ValueError, match="Duplicate"):
        pending_run_keys(rows, [{"run_key": "primary::a"}, {"run_key": "primary::a"}])


def test_frozen_gate3_model_identity():
    assert sha256_file(ROOT / "models/final_v2/gate3/binary_m1_gate3.joblib") == BINARY_MODEL_SHA256
    assert sha256_file(ROOT / "models/final_v2/gate3/category_m1_gate3.joblib") == CATEGORY_MODEL_SHA256


def test_external_manifest_and_canonical_preparation_pass():
    manifest = ROOT / "reports/final_v2/gate4/external_run_input_manifest.json"
    parsed, rows, config = validate_external_inputs(ROOT, manifest)
    assert parsed["confirmation_accessed"] is False
    assert len(rows) == 200
    assert config["analysis_model"] == "Qwen/Qwen2.5-Coder-7B-Instruct"
    assert verify(ROOT)["status"] == "PASS"


def test_external_runner_fails_closed_on_invalid_llm_json(monkeypatch):
    import json as _json
    import scripts.run_gate4_external_qwen as runner

    class CountingBackend:
        def __init__(self):
            self.call_count = 0

    backend = CountingBackend()

    def fake_stage3(**kwargs):
        backend.call_count += 2
        raise _json.JSONDecodeError(
            "Unterminated string",
            '{"patch_markdown":"broken',
            18,
        )

    monkeypatch.setattr(
        runner,
        "generate_semantic_documentation_patch",
        fake_stage3,
    )

    row = prediction(
        "parse-failure-case",
        category="api_reference",
        context=True,
    )
    row["sample_name"] = "primary_natural_distribution"
    row["code_diff_excerpt"] = "+example"
    row["docs_before_excerpt"] = "existing docs"

    result = _result_row(
        row,
        backend=backend,
        config={},
    )

    assert result["final_status"] == "human_review_required"
    assert result["generated_patch"] is None
    assert result["llm_call_count"] == 2
    assert (
        result["stage3_result"]["execution_error"]["code"]
        == "invalid_structured_llm_output"
    )
