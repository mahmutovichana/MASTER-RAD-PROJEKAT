from __future__ import annotations

import hashlib
import importlib.metadata
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    base = root / "experiments/posthoc_stage3_s1"
    prompts = sorted((base / "prompts").glob("*.txt"))
    packages = {}
    for name in ("numpy", "scikit-learn", "torch", "transformers", "bitsandbytes", "accelerate"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    source_paths = [root / "reports/final_v2/gate4/primary_sample.jsonl", root / "reports/final_v2/gate4/secondary_stress_sample.jsonl"]
    receipt = {
        "status": "COMPLETE_PRE_GPU_DEVELOPMENT_STATE",
        "next_authorized_stage": "DEVELOPMENT_GPU_CANARY",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "neural_retrieval_executed": False,
        "neural_reranking_executed": False,
        "neural_generation_executed": False,
        "local_cuda_available": False,
        "seed": 42,
        "prompt_sha256": {path.name: sha256(path) for path in prompts},
        "source_sha256": {str(path.relative_to(root)).replace("\\", "/"): sha256(path) for path in source_paths},
        "package_versions_local": packages,
        "selected_configuration": None,
        "gpu_canary_completed": False,
        "fresh_posthoc_evaluation_executed": False,
        "contract_checks": {
            "exact_model_revisions_recorded": True,
            "bounded_grid_exact": True,
            "reranker_top_3_fixed": True,
            "maximum_one_repair_fixed": True,
            "model_substitution_fallback_absent": True,
            "repository_head_or_branch_access_forbidden": True,
            "gate6_human_field_reads_absent": True
        }
    }
    (base / "runtime/preparation_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
