from __future__ import annotations

import json
import urllib.error
from pathlib import Path

import joblib
import pytest

from docguard_external.github_client_v2 import GitHubClientV2, GlobalGitHubStop
from docguard_external.github_pr_dataset_builder import BuildConfig
from docguard_external.github_pr_dataset_builder_v2 import build_dataset_v2, collect_docs_before_neutral, stable_case_id
from docguard_llm_v2.document_retriever import retrieve_documents
from docguard_llm_v2.pipeline import generate_semantic_documentation_patch
from docguard_ml_v2.data_contract import binary_eligible_rows, category_eligible_rows, validate_final_gold_row
from docguard_ml_v2.metrics import bootstrap_metric_ci
from scripts.audit_final_v2_pre_experiment import run as audit_pre_experiment
from scripts.audit_human_review_complete_v2 import audit as audit_human_review
from scripts.finalize_human_gold_v2 import validate_completion_audit
from scripts.human_review_workflow_v2 import make_review_row, write_json, write_jsonl
from scripts.prefill_human_label_sheet_v2 import prefill_row
from scripts.run_frozen_stage3_v2_confirmation import run as run_stage3_confirmation


ROOT = Path(__file__).resolve().parents[1]


class Cache:
    def __init__(self, value=None):
        self.value = value

    def get_json(self, url, accept):
        return self.value

    def set_json(self, url, data, accept):
        self.value = data


class Response:
    def __init__(self, data):
        self.data = json.dumps(data).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.data


def test_github_client_pacing_and_cache_hit(monkeypatch):
    calls = []
    sleeps = []
    times = iter([0.0, 0.1, 0.4])

    def fake_urlopen(request, timeout):
        calls.append(request.full_url)
        return Response({"ok": True})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = GitHubClientV2(token="t", cache=None, min_request_interval_seconds=0.25, monotonic=lambda: next(times), sleeper=sleeps.append)
    client.request_json("https://api.github.test/a")
    client.request_json("https://api.github.test/b")
    assert len(calls) == 2
    assert sleeps == pytest.approx([0.15])
    cached = GitHubClientV2(token="t", cache=Cache({"cached": True}), min_request_interval_seconds=99, sleeper=sleeps.append)
    assert cached.request_json("https://api.github.test/c") == {"cached": True}
    assert cached.outbound_request_count == 0


def test_github_client_primary_and_secondary_rate_limits(monkeypatch):
    def primary(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 403, "rate", {"x-ratelimit-remaining": "0"}, None)

    monkeypatch.setattr("urllib.request.urlopen", primary)
    with pytest.raises(GlobalGitHubStop, match="primary_rate_limit"):
        GitHubClientV2(token="t", sleeper=lambda _s: None).request_json("https://api.github.test/a")

    attempts = {"count": 0}

    def secondary_then_ok(request, timeout):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise urllib.error.HTTPError(request.full_url, 403, "abuse", {"x-ratelimit-remaining": "10"}, None)
        return Response({"ok": True})

    monkeypatch.setattr("urllib.request.urlopen", secondary_then_ok)
    client = GitHubClientV2(token="t", sleeper=lambda _s: None)
    assert client.request_json("https://api.github.test/b") == {"ok": True}
    assert client.request_retry_count == 1


class TreeClient:
    max_discovered_documentation_paths = 20

    def get_tree_recursive(self, repo, ref):
        assert ref == "base"
        return [
            {"type": "blob", "path": "README.md"},
            {"type": "blob", "path": "website/docs/reviews.mdx"},
            {"type": "blob", "path": "src/app.py"},
        ]

    def get_file_text(self, repo, path, ref):
        data = {
            "README.md": "general project overview",
            "website/docs/reviews.mdx": "Reviews API uses REVIEW_WINDOW and /reviews endpoint.",
        }
        return data.get(path)


def test_base_sha_doc_discovery_nested_and_outcome_independent():
    docs_before, retrieved, policy, candidates = collect_docs_before_neutral(client=TreeClient(), repo="org/repo", ref="base", code_changed_files=["src/reviews.py"], max_chars=2000, max_files=5)
    assert "website/docs/reviews.mdx" in retrieved
    assert "base_sha_tree_documentation_discovery_v2" in policy
    assert all(item["source_ref"] == "base" for item in candidates)
    assert "Reviews API" in docs_before


def test_partial_candidate_output_preserved_and_no_gold_fields():
    class StopClient(TreeClient):
        def __init__(self):
            self.calls = 0

        def get_pull(self, repo, pr):
            self.calls += 1
            if self.calls > 1:
                raise GlobalGitHubStop("primary_rate_limit_exhausted")
            return {"title": "x", "base": {"sha": "base"}, "head": {"sha": "head"}}

        def get_pull_files(self, repo, pr):
            return [{"filename": "src/reviews.py", "patch": "+app.get('/reviews')", "additions": 1, "deletions": 0}]

    seeds = [{"repo": "org/a", "pr_number": 1, "url": "u1"}, {"repo": "org/b", "pr_number": 2, "url": "u2"}]
    cases, rejects = build_dataset_v2(seeds=seeds, client=StopClient(), config=BuildConfig(), max_cases=None)
    assert len(cases) == 1
    assert rejects[-1]["stop_reason"] == "primary_rate_limit_exhausted"
    assert not any(key.startswith("gold_") for key in cases[0])
    assert stable_case_id("Org/A", 1) == stable_case_id("org/a", 1)


def test_tfidf_retrieval_relevant_doc_beats_readme_noise_and_is_deterministic():
    candidates = [
        {"path": "README.md", "excerpt": "installation overview contribution guide"},
        {"path": "docs/reviews.md", "excerpt": "REVIEW_WINDOW controls /reviews retention window default 7d"},
    ]
    kwargs = {
        "predicted_category": "configuration",
        "analysis": {"change_summary": "Adds REVIEW_WINDOW", "supported_inferences": [{"claim": "REVIEW_WINDOW default 7d", "evidence_valid": True}]},
        "code_diff": "+process.env.REVIEW_WINDOW || '7d'",
        "documentation_context_candidates": candidates,
        "top_k": 2,
    }
    first = retrieve_documents(**kwargs)
    second = retrieve_documents(**kwargs)
    assert first["retrieval_method"] == "tfidf_cosine_semantic_ir_v2"
    assert first["top_k"][0].path == "docs/reviews.md"
    assert [item.path for item in first["top_k"]] == [item.path for item in second["top_k"]]


def final_row(**overrides):
    row = {
        "case_id": "c1",
        "repository": "org/repo",
        "partition": "development_train",
        "review_status": "approved",
        "human_review_complete": True,
        "label_source": "human_reviewed_final_v2",
        "gold_docs_update_required": True,
        "gold_doc_category": "other_documentation",
        "language": "python",
        "code_changed_files": ["src/a.py"],
        "code_diff_excerpt": "+x",
        "docs_before_excerpt": "",
    }
    row.update(overrides)
    return row


def test_ml_contract_fails_closed_and_keeps_binary_category_policy():
    for bad in [
        {"human_review_complete": None},
        {"human_review_complete": False},
        {"label_source": "suggested"},
        {"review_status": "pending"},
        {"gold_docs_update_required": "true"},
        {"partition": "confirmation"},
    ]:
        with pytest.raises(ValueError):
            validate_final_gold_row(final_row(**bad), allowed_partitions={"development_train"})
    assert binary_eligible_rows([final_row()])[0]["gold_doc_category"] == "other_documentation"
    assert category_eligible_rows([final_row()]) == []


def test_prefill_uses_only_safe_preoutcome_fields():
    row = {
        "language": "python",
        "code_changed_files": ["src/config.py"],
        "code_diff_excerpt": "+REVIEW_WINDOW = os.getenv('REVIEW_WINDOW')",
        "docs_before_excerpt": "Configuration docs",
        "docs_changed_files": ["docs/api.md"],
        "docs_diff_excerpt": "+outcome api docs",
        "docs_after_excerpt": "outcome",
        "collector_bucket": "code_and_docs",
        "gold_docs_update_required": False,
    }
    base = prefill_row(row)
    changed = prefill_row({**row, "docs_changed_files": ["docs/other.md"], "docs_diff_excerpt": "+different", "docs_after_excerpt": "different"})
    assert base["suggested_doc_category"] == changed["suggested_doc_category"]
    assert base["human_docs_update_required"] is None
    assert not any(key.startswith("gold_") for key in base)


class RecordingLLM:
    def __init__(self):
        self.calls = []

    def generate(self, messages, model=None, purpose=None, generation_options=None):
        self.calls.append((purpose, generation_options))
        if purpose == "analysis":
            return json.dumps({"change_summary": "x", "supported_inferences": [{"claim": "review window", "evidence_source": "code_diff", "evidence_quote": "REVIEW_WINDOW"}]})
        patch = "- `REVIEW_WINDOW` controls review behavior."
        if purpose == "writer":
            return json.dumps({"target_document_path": "docs/config.md", "target_section": "Config", "patch_markdown": "Document REVIEW_WINDOW.", "writer_confidence": 0.3})
        return json.dumps({"target_document_path": "docs/config.md", "target_section": "Config", "patch_markdown": patch, "writer_confidence": 0.8})


def test_stage3_config_options_reach_analysis_writer_and_repair():
    llm = RecordingLLM()
    result = generate_semantic_documentation_patch(
        docs_update_required=True,
        predicted_category="configuration",
        code_diff="+REVIEW_WINDOW = '7d'",
        docs_before="",
        documentation_context_candidates=[{"path": "docs/config.md", "excerpt": "Configuration", "source_ref": "base"}],
        llm_backend=llm,
        config={"analysis_model": "a", "writer_model": "w", "repair_model": "r", "temperature": 0.2, "max_tokens_analysis": 111, "max_tokens_writer": 222, "max_tokens_repair": 333, "top_k_documents": 1, "max_repair_attempts": 1},
    )
    assert result["repair_attempted"] is True
    assert [(purpose, opt.temperature, opt.max_tokens) for purpose, opt in llm.calls] == [("analysis", 0.2, 111), ("writer", 0.2, 222), ("repair", 0.2, 333)]


class FakeBinaryModel:
    classes_ = [0, 1]

    def __init__(self, score):
        self.score = score

    def predict_proba(self, rows):
        return [[1 - self.score, self.score] for _ in rows]


class FakeCategoryModel:
    classes_ = ["configuration"]

    def predict(self, rows):
        return ["configuration" for _ in rows]

    def predict_proba(self, rows):
        return [[1.0] for _ in rows]


def write_freeze(path: Path, model: Path, config_hash: str | None = None):
    write_json(path, {"confirmation_accessed": False, "hashes": {"model": sha256(model)}, "config_sha256": config_hash, "source_file_sha256": {}})


def sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_frozen_stage3_runner_guards_and_call_flow(tmp_path: Path):
    confirmation = tmp_path / "confirmation.jsonl"
    row = final_row(partition="confirmation", repository="org/repo", documentation_context_candidates=[{"path": "docs/config.md", "excerpt": "Configuration REVIEW_WINDOW", "source_ref": "base"}])
    write_jsonl(confirmation, [row])
    partition = tmp_path / "partition.json"
    write_json(partition, {"confirmation_sealed": True, "repository_assignments": {"org/repo": "confirmation"}})
    binary_model = tmp_path / "binary.joblib"
    category_model = tmp_path / "category.joblib"
    joblib.dump({"model": FakeBinaryModel(0.2), "threshold": 0.5}, binary_model)
    joblib.dump({"model": FakeCategoryModel()}, category_model)
    bf = tmp_path / "bf.json"
    cf = tmp_path / "cf.json"
    write_freeze(bf, binary_model)
    write_freeze(cf, category_model)
    cfg = tmp_path / "stage3.json"
    cfg.write_text((ROOT / "configs/stage3_semantic_generation_v2.json").read_text(encoding="utf-8"), encoding="utf-8")
    sf = tmp_path / "sf.json"
    write_json(sf, {"config_sha256": sha256(cfg), "source_file_sha256": {}})
    llm = RecordingLLM()
    out = tmp_path / "out"
    result = run_stage3_confirmation(confirmation=confirmation, repository_partition_manifest=partition, binary_model=binary_model, binary_freeze_manifest=bf, category_model=category_model, category_freeze_manifest=cf, stage3_config=cfg, stage3_freeze_manifest=sf, output_dir=out, llm_backend=llm, enforce_one_shot=True)
    assert result["receipt"]["positive_stage3_invocation_count"] == 0
    assert llm.calls == []
    joblib.dump({"model": FakeBinaryModel(0.9), "threshold": 0.5}, binary_model)
    write_freeze(bf, binary_model)
    out2 = tmp_path / "out2"
    run_stage3_confirmation(confirmation=confirmation, repository_partition_manifest=partition, binary_model=binary_model, binary_freeze_manifest=bf, category_model=category_model, category_freeze_manifest=cf, stage3_config=cfg, stage3_freeze_manifest=sf, output_dir=out2, llm_backend=llm, enforce_one_shot=True)
    assert llm.calls
    with pytest.raises(ValueError):
        run_stage3_confirmation(confirmation=confirmation, repository_partition_manifest=partition, binary_model=binary_model, binary_freeze_manifest=bf, category_model=category_model, category_freeze_manifest=cf, stage3_config=cfg, stage3_freeze_manifest=sf, output_dir=out2, llm_backend=RecordingLLM(), enforce_one_shot=True)


def test_completion_audit_receipt_and_stale_hash_rejected(tmp_path: Path):
    reviewed = make_review_row({"case_id": "c1", "repository": "org/repo", "pr_number": 1, "language": "python", "code_changed_files": ["src/a.py"], "code_diff_excerpt": "+x", "docs_before_excerpt": ""})
    reviewed.update({"review_status": "approved", "human_docs_update_required": True, "human_doc_category": "api_reference"})
    path = tmp_path / "review.jsonl"
    write_jsonl(path, [reviewed])
    errors, receipt = audit_human_review([reviewed], input_path=path)
    assert not errors
    audit_path = tmp_path / "audit.json"
    write_json(audit_path, receipt)
    validate_completion_audit(audit_path, path)
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_completion_audit(audit_path, path)


def test_bootstrap_auc_ap_reports_valid_replicates():
    ci = bootstrap_metric_ci(lambda yt, score: 1.0, [0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], seed=4, n_bootstrap=20)
    assert ci["valid_replicates"] > 0


def test_pre_experiment_audit_pass_and_intentional_failures():
    assert audit_pre_experiment()["status"] == "PASS"
    assert audit_pre_experiment({"bad": "router = True"})["status"] == "FAIL"
