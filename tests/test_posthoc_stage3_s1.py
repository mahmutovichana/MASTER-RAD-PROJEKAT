from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from experiments.posthoc_stage3_s1.scripts.repository_corpus import (
    BareGitRepositoryProvider,
    DocumentChunk,
    assert_explicit_commit,
    candidate_priority,
    discover_candidates,
    is_documentation_path,
    parse_pre_change_marker,
    semantic_chunks,
)
from experiments.posthoc_stage3_s1.scripts.retrieval import hybrid_retrieve, rerank_top_documents
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import S1Agent, S1Configuration


ROOT = Path(__file__).resolve().parents[1]
S1 = ROOT / "experiments/posthoc_stage3_s1"


def chunk(path: str, text: str = "documentation") -> DocumentChunk:
    return DocumentChunk(path, "", (), text, 0)


def test_pre_change_commit_enforcement_and_marker():
    assert parse_pre_change_marker("<!-- docs/a.md @ " + "a" * 40 + " -->\ntext") == ("docs/a.md", "a" * 40)
    assert_explicit_commit("a" * 40)
    for forbidden in ("HEAD", "main", "origin/main", "abc123"):
        with pytest.raises(ValueError):
            assert_explicit_commit(forbidden)


def test_no_head_or_future_document_fallback_in_provider_source():
    source = (S1 / "scripts/repository_corpus.py").read_text(encoding="utf-8")
    assert '"HEAD"' not in source
    assert "fetch\", \"--no-tags\"" in source
    assert "origin\", *missing" in source


def test_repository_cache_correctness(tmp_path):
    provider = BareGitRepositoryProvider(tmp_path)
    assert provider.cache_path("owner/repo") == tmp_path / "owner__repo.git"
    assert provider.cache_path("owner/repo") == provider.cache_path("owner/repo")
    assert provider.cache_path("owner/other") != provider.cache_path("owner/repo")


def test_nearest_path_candidate_discovery():
    found = discover_candidates(["README.md", "pkg/README.md", "docs/api.md"], changed_paths=["pkg/src/a.ts"], code_diff="Widget API")
    assert found[0][0] == "pkg/README.md"
    assert candidate_priority("pkg/README.md", ["pkg/src/a.ts"]) == "A"


@pytest.mark.parametrize("path,expected", [
    ("docs/guide.md", True), ("README.rst", True), ("docs/manual.txt", True),
    ("node_modules/x/README.md", False), ("dist/docs.md", False), ("CHANGELOG.md", False), ("src/a.ts", False),
])
def test_documentation_file_filtering(path, expected):
    assert is_documentation_path(path) is expected


def test_deterministic_semantic_chunking():
    text = "# A\nalpha\n## B\nbeta\n# C\ngamma"
    one = semantic_chunks("README.md", text, max_chars=30)
    two = semantic_chunks("README.md", text, max_chars=30)
    assert one == two
    assert [item.heading for item in one] == ["A", "B", "C"]


class Dense:
    def encode(self, texts):
        return np.array([[1.0, float(i)] for i, _ in enumerate(texts)])


def test_lexical_and_dense_retrieval_interface():
    chunks = [chunk(f"docs/{i}.md", "configuration alpha" if i == 0 else "other") for i in range(12)]
    ranked = hybrid_retrieve("configuration alpha", chunks, dense_encoder=Dense(), lexical_top_k=5, dense_top_k=5)
    assert ranked
    assert any(item.chunk.path == "docs/0.md" for item in ranked)
    with pytest.raises(ValueError):
        hybrid_retrieve("x", chunks, dense_encoder=Dense(), lexical_top_k=7, dense_top_k=5)


class BadDense:
    def encode(self, texts):
        return np.ones((1, 2))


def test_dense_interface_rejects_wrong_row_count():
    with pytest.raises(ValueError):
        hybrid_retrieve("x", [chunk("a.md")], dense_encoder=BadDense(), lexical_top_k=5, dense_top_k=5)


class ReRank:
    def score(self, query, documents):
        return [0.0, 0.9, 0.8, 0.7][: len(documents)]


def test_reranker_interface_keeps_zero_and_three_distinct_documents():
    from experiments.posthoc_stage3_s1.scripts.retrieval import RankedChunk
    candidates = [RankedChunk(chunk(path), 0, 0) for path in ("a.md", "b.md", "c.md", "d.md")]
    result = rerank_top_documents("q", candidates, reranker=ReRank())
    assert [item.chunk.path for item in result] == ["b.md", "c.md", "d.md"]
    with pytest.raises(ValueError):
        rerank_top_documents("q", candidates, reranker=ReRank(), final_documents=2)


class EmptyBackend:
    def generate_json(self, **kwargs):
        raise AssertionError("must not be called")


def config():
    return S1Configuration(5, 5, 3, 0.5, "P1")


def test_target_abstention_without_candidates():
    result = S1Agent(EmptyBackend(), config()).run({}, [])
    assert result["state"] == "ABSTAINED_NO_TARGET"


class QueueBackend:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def generate_json(self, *, purpose, prompt):
        self.calls.append(purpose)
        return self.values.pop(0)


def base_values(final_decision="ABSTAIN"):
    return [
        {"target_document": "README.md", "target_section": "A", "confidence": 0.9, "evidence": ["x"], "abstain_reason": None},
        {"update_needed": True, "target_document": "README.md", "target_section": "A", "facts_to_document": ["alpha"], "facts_not_supported": [], "style_observations": [], "minimal_update_intent": "x", "change_type": "api", "developer_facing_effect": "alpha"},
        {"target_document": "README.md", "target_section": "A", "patch_markdown": "alpha"},
        {"grounded": False, "target_fit": True, "useful": True, "style_fit": True, "unsupported_claims": ["invented"], "unnecessary_content": [], "decision": "REPAIR", "repair_instructions": ["remove invented"]},
        {"target_document": "README.md", "target_section": "A", "patch_markdown": "alpha"},
        {"grounded": final_decision == "ACCEPT", "target_fit": True, "useful": True, "style_fit": True, "unsupported_claims": [] if final_decision == "ACCEPT" else ["still bad"], "unnecessary_content": [], "decision": final_decision, "repair_instructions": []},
    ]


def test_unsupported_claim_rejection_and_maximum_one_repair(monkeypatch):
    monkeypatch.setattr("experiments.posthoc_stage3_s1.scripts.s1_pipeline.deterministic_unsupported_claims", lambda *a, **k: [])
    backend = QueueBackend(base_values("ABSTAIN"))
    from experiments.posthoc_stage3_s1.scripts.retrieval import RankedChunk
    result = S1Agent(backend, config()).run({"code_diff_excerpt": "alpha"}, [RankedChunk(chunk("README.md", "alpha"), 1, 1, 1)])
    assert result["state"] == "ABSTAINED_UNSUPPORTED_CLAIMS"
    assert result["repair_count"] == 1
    assert backend.calls.count("repair") == 1
    assert backend.calls.count("final_critic") == 1


def test_deterministic_sample_membership_receipt():
    audit = json.loads((S1 / "phase0_retrieval_audit.json").read_text(encoding="utf-8"))
    paths = [ROOT / "reports/final_v2/gate4/primary_sample.jsonl", ROOT / "reports/final_v2/gate4/secondary_stress_sample.jsonl"]
    case_ids = []
    for path in paths:
        case_ids.extend(json.loads(line)["case_id"] for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    assert len(case_ids) == 200 == len(set(case_ids))
    assert hashlib.sha256("\n".join(case_ids).encode()).hexdigest() == audit["membership"]["ordered_case_id_sha256"]


def test_forbidden_gate6_human_score_access():
    forbidden = ("gate6/review", "gate6\\review", "human_notes", "human_accept_as_is", "factual_correctness_score")
    for path in (S1 / "scripts").glob("*.py"):
        text = path.read_text(encoding="utf-8").casefold()
        assert not any(term in text for term in forbidden), path


def test_notebook_and_config_are_valid_json():
    json.loads((S1 / "notebooks/posthoc_stage3_s1_kaggle.ipynb").read_text(encoding="utf-8"))
    config_value = json.loads((S1 / "configs/s1_frozen_candidate.json").read_text(encoding="utf-8"))
    assert config_value["confirmation_accessed"] is False
    assert config_value["selected_configuration"] is None
