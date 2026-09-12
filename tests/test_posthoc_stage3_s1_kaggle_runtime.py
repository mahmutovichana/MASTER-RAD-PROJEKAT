from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu import (
    FROZEN_SHA,
    assert_frozen_checkout,
    load_unique_jsonl,
    safe_model_row,
)


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/posthoc_stage3_s1"


def test_notebook_has_frozen_remote_checkout_lfs_secret_and_guard():
    notebook = json.loads((BASE / "notebooks/posthoc_stage3_s1_kaggle.ipynb").read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert FROZEN_SHA in source
    assert "git', 'rev-parse', 'HEAD" in source
    assert "git', 'lfs', 'pull'" in source
    assert "GIT_LFS_SKIP_SMUDGE" in source
    assert "UserSecretsClient().get_secret('HF_TOKEN')" in source
    assert "receipt.get('state') != 'CANARY_PASS'" in source
    assert "/kaggle/working/s1_development_return_artifacts.zip" in source


def test_notebook_never_prints_secret_value():
    text = (BASE / "notebooks/posthoc_stage3_s1_kaggle.ipynb").read_text(encoding="utf-8")
    assert "print(secret" not in text
    assert "print(os.environ['HF_TOKEN']" not in text


def test_frozen_checkout_mismatch_fails(monkeypatch, tmp_path):
    monkeypatch.setattr("experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu.git_head", lambda root: "0" * 40)
    with pytest.raises(RuntimeError, match="Frozen checkout mismatch"):
        assert_frozen_checkout(tmp_path)


def test_frozen_checkout_exact_passes(monkeypatch, tmp_path):
    monkeypatch.setattr("experiments.posthoc_stage3_s1.scripts.run_s1_development_gpu.git_head", lambda root: FROZEN_SHA)
    assert_frozen_checkout(tmp_path)


def test_resume_rejects_duplicate_completed_records(tmp_path):
    path = tmp_path / "results.jsonl"
    record = json.dumps({"run_key": "P1:case", "result": {"state": "ACCEPTED"}})
    path.write_text(record + "\n" + record + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Duplicate checkpoint key"):
        load_unique_jsonl(path, "run_key")


def test_return_packager_uses_exact_archive_path_and_required_outputs():
    source = (BASE / "scripts/package_s1_development_return.py").read_text(encoding="utf-8")
    assert 'Path("/kaggle/working/s1_development_return_artifacts.zip")' in source
    for name in ("canary_receipt.json", "runtime_manifest.json", "development_metrics.json", "retrieval_metrics.json", "generation_results.jsonl", "execution.log"):
        assert name in source


def test_canary_contract_includes_required_checks_and_terminal_states():
    source = (BASE / "scripts/kaggle_development_runner.py").read_text(encoding="utf-8")
    for phrase in ("CANARY_PASS", "CANARY_STOP", "deterministic_plan_json_repeat", "structured_critic_json", "single_bounded_repair", "peak_allocated_bytes", "peak_process_rss_bytes"):
        assert phrase in source


def test_local_non_cuda_canary_writes_explicit_stop(tmp_path):
    receipt = tmp_path / "canary.json"
    environment = dict(os.environ)
    environment.pop("HF_TOKEN", None)
    completed = subprocess.run(
        [sys.executable, "-m", "experiments.posthoc_stage3_s1.scripts.kaggle_development_runner", "--canary", "--receipt", str(receipt)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert json.loads(receipt.read_text(encoding="utf-8"))["state"] == "CANARY_STOP"
    assert "CANARY_STOP" in completed.stdout


def test_gpu_runner_caches_expensive_stages_and_checkpoints_25():
    source = (BASE / "scripts/run_s1_development_gpu.py").read_text(encoding="utf-8")
    for phrase in ("repository_corpus", "query_embedding", "document_embeddings", "lexical_scores", "dense_scores", "reranker_scores.jsonl", "model_call_cache.jsonl"):
        assert phrase in source
    assert "newly_completed % 25 == 0" in source


def test_gpu_runner_preserves_development_and_controlled_denominators():
    assert FROZEN_SHA == "38f9afb479f738081301172176d3133e4056bd7c"
    source = (BASE / "scripts/run_s1_development_gpu.py").read_text(encoding="utf-8")
    assert "MEMBERSHIP_COUNT = 200" in source
    assert "CONTROLLED_TARGET_COUNT = 79" in source
    assert '"natural_target_ground_truth": False' in source


def test_model_prompt_row_is_strictly_whitelisted():
    value = safe_model_row({"case_id": "x", "repository": "o/r", "code_diff_excerpt": "diff", "synthetic_target_doc_path": "forbidden.md", "reviewer_notes": "forbidden"})
    assert value["case_id"] == "x"
    assert "synthetic_target_doc_path" not in value
    assert "reviewer_notes" not in value


def test_no_forbidden_data_paths_or_human_fields_in_runtime_code():
    paths = list((BASE / "scripts").glob("*.py")) + [BASE / "notebooks/posthoc_stage3_s1_kaggle.ipynb"]
    forbidden = ("reports/final_v2/gate6", "gate6_primary_blind_review", "human_notes", "human_accept_as_is", "factual_correctness_score")
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert not any(value in text for value in forbidden), path
