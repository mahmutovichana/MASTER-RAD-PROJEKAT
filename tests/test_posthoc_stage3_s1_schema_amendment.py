from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from experiments.posthoc_stage3_s1.scripts.repository_corpus import DocumentChunk
from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_REVISION,
    RERANKER_MODEL_ID,
    RERANKER_REVISION,
    RankedChunk,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import (
    GENERATOR_MODEL_ID,
    GENERATOR_REVISION,
    S1Agent,
    S1Configuration,
    SchemaRetryingGenerator,
    StructuredSchemaError,
    validate_structured_output,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


VALID_CRITIC = {
    "grounded": True, "target_fit": True, "useful": True, "style_fit": True,
    "unsupported_claims": [], "unnecessary_content": [], "decision": "ACCEPT", "repair_instructions": [],
}
VALID_TARGET = {"target_document": "README.md", "target_section": "Usage", "confidence": 0.8, "evidence": ["diff"], "abstain_reason": None}
VALID_PLAN = {
    "update_needed": True, "target_document": "README.md", "target_section": "Usage", "change_type": "api",
    "developer_facing_effect": "documents alpha", "facts_to_document": ["alpha"], "facts_not_supported": [],
    "style_observations": [], "minimal_update_intent": "add alpha",
}
VALID_PATCH = {"target_document": "README.md", "target_section": "Usage", "patch_markdown": "alpha"}


class QueueBackend:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def generate_json(self, *, purpose, prompt):
        self.calls.append({"purpose": purpose, "prompt": prompt})
        return self.values.pop(0)


@pytest.mark.parametrize(
    "invalid",
    [
        {key: value for key, value in VALID_CRITIC.items() if key != "grounded"},
        {**VALID_CRITIC, "grounded": "yes"},
        {**VALID_CRITIC, "decision": "MAYBE"},
    ],
)
def test_schema_error_triggers_exactly_one_retry(invalid):
    backend = QueueBackend([invalid, dict(VALID_CRITIC)])
    wrapper = SchemaRetryingGenerator(backend)
    assert wrapper.generate_json(purpose="critic", prompt="same evidence") == VALID_CRITIC
    assert len(backend.calls) == 2
    assert backend.calls[1]["purpose"] == "critic_schema_correction"
    assert "ORIGINAL EVIDENCE AND PROMPT (unchanged):\nsame evidence" in backend.calls[1]["prompt"]
    assert "INITIAL JSON TO CORRECT WITHOUT CHANGING ITS DECISION" in backend.calls[1]["prompt"]
    assert wrapper.diagnostics == [{
        "purpose": "critic", "initial_schema_valid": False, "schema_retry_used": True,
        "schema_retry_valid": True, "schema_errors": wrapper.diagnostics[0]["schema_errors"],
    }]


def test_valid_first_response_does_not_retry():
    backend = QueueBackend([dict(VALID_CRITIC)])
    wrapper = SchemaRetryingGenerator(backend)
    assert wrapper.generate_json(purpose="critic", prompt="evidence") == VALID_CRITIC
    assert len(backend.calls) == 1
    assert wrapper.diagnostics[0]["schema_retry_used"] is False
    assert wrapper.diagnostics[0]["schema_retry_valid"] is None


def test_invalid_retry_fails_closed_without_python_defaulting():
    missing = {key: value for key, value in VALID_CRITIC.items() if key != "grounded"}
    backend = QueueBackend([dict(missing), dict(missing)])
    wrapper = SchemaRetryingGenerator(backend)
    with pytest.raises(StructuredSchemaError, match="after one correction retry"):
        wrapper.generate_json(purpose="critic", prompt="evidence")
    assert len(backend.calls) == 2
    assert "grounded" not in missing
    assert wrapper.diagnostics[0]["schema_retry_valid"] is False


@pytest.mark.parametrize("confidence", [-0.01, 1.01, True, "0.5"])
def test_target_confidence_bounds_and_type(confidence):
    assert validate_structured_output("target_decision", {**VALID_TARGET, "confidence": confidence})


@pytest.mark.parametrize("field", ["grounded", "target_fit", "useful", "style_fit"])
def test_critic_required_booleans(field):
    assert f"{field} must be bool" in validate_structured_output("critic", {**VALID_CRITIC, field: 1})


def test_schema_retry_does_not_increment_semantic_repair_count(monkeypatch):
    incomplete_target = {key: value for key, value in VALID_TARGET.items() if key != "evidence"}
    backend = QueueBackend([incomplete_target, dict(VALID_TARGET), dict(VALID_PLAN), dict(VALID_PATCH), dict(VALID_CRITIC)])
    monkeypatch.setattr("experiments.posthoc_stage3_s1.scripts.s1_pipeline.deterministic_unsupported_claims", lambda *args, **kwargs: [])
    candidate = RankedChunk(DocumentChunk("README.md", "Usage", ("Usage",), "alpha", 0), 1.0, 1.0, 1.0)
    agent = S1Agent(backend, S1Configuration(5, 5, 3, 0.5, "P1", max_repairs=1))
    result = agent.run({"code_diff_excerpt": "alpha"}, [candidate], document_corpus=[candidate.chunk])
    assert result["state"] == "ACCEPTED"
    assert result["repair_count"] == 0
    assert result["structured_call_diagnostics"][0]["schema_retry_used"] is True
    assert len(backend.calls) == 5


def test_semantic_repair_maximum_remains_one():
    S1Configuration(5, 5, 3, 0.5, "P1", max_repairs=1).validate()
    with pytest.raises(ValueError):
        S1Configuration(5, 5, 3, 0.5, "P1", max_repairs=2).validate()


def test_models_revisions_and_p1_p2_hashes_unchanged():
    assert (EMBEDDING_MODEL_ID, EMBEDDING_REVISION) == ("Qwen/Qwen3-Embedding-0.6B", "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3")
    assert (RERANKER_MODEL_ID, RERANKER_REVISION) == ("Qwen/Qwen3-Reranker-0.6B", "e61197ed45024b0ed8a2d74b80b4d909f1255473")
    assert (GENERATOR_MODEL_ID, GENERATOR_REVISION) == ("Qwen/Qwen2.5-Coder-14B-Instruct", "aedcc2d42b622764e023cf882b6652e646b95671")
    expected = {"P1_generation.txt": "c8d1ff147c7873c77ae20f631d979618e9d5296300350a9ff621b782cc963d1c", "P2_generation.txt": "7de26510a0b9380ad43da9e6dcb39557bc8ca4dbb131b3c0b798870b64a5d7d3"}
    for name, digest in expected.items():
        assert hashlib.sha256((BASE / "prompts" / name).read_bytes()).hexdigest() == digest


def test_amendment_receipt_preserves_access_boundaries():
    receipt = json.loads((BASE / "S1_PREDEVELOPMENT_AMENDMENT_01.json").read_text(encoding="utf-8"))
    assert receipt["development_results_seen"] is False
    assert receipt["confirmation_accessed"] is False
    assert receipt["gate6_row_level_human_data_accessed"] is False
    assert receipt["schema_correction_retries"] == 1
    assert receipt["semantic_max_repairs"] == 1
