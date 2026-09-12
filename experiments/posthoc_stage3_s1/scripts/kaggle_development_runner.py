from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import time
from pathlib import Path

from experiments.posthoc_stage3_s1.scripts.retrieval import QwenDenseEncoder, QwenReranker
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import QwenStructuredGenerator


def cuda_snapshot() -> dict:
    import torch

    return {
        "available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count(),
        "devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        "allocated_bytes": [torch.cuda.memory_allocated(i) for i in range(torch.cuda.device_count())],
        "reserved_bytes": [torch.cuda.memory_reserved(i) for i in range(torch.cuda.device_count())],
    }


def unload(value) -> None:
    import torch

    del value
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def run_canary(cache_dir: str) -> dict:
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the registered S1 canary")
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("HF_TOKEN is missing from the environment")
    started = time.monotonic()
    receipt = {"status": "RUNNING", "confirmation_accessed": False, "stages": [], "initial_cuda": cuda_snapshot()}
    dense = QwenDenseEncoder(cache_dir=cache_dir)
    shape = list(dense.encode(["changed configuration key", "configuration reference documentation"]).shape)
    receipt["stages"].append({"name": "embedding", "output_shape": shape, "cuda": cuda_snapshot()})
    del dense
    gc.collect()
    torch.cuda.empty_cache()
    reranker = QwenReranker(cache_dir=cache_dir)
    scores = reranker.score("new configuration key", ["API overview", "configuration key reference"])
    receipt["stages"].append({"name": "reranker", "score_count": len(scores), "cuda": cuda_snapshot()})
    del reranker
    gc.collect()
    torch.cuda.empty_cache()
    generator = QwenStructuredGenerator(cache_dir=cache_dir)
    value = generator.generate_json(purpose="canary", prompt='Return only this JSON object: {"canary": true}')
    receipt["stages"].append({"name": "generator", "valid_json_object": isinstance(value, dict), "cuda": cuda_snapshot()})
    del generator
    gc.collect()
    torch.cuda.empty_cache()
    receipt.update({"status": "PASS", "runtime_seconds": time.monotonic() - started, "final_cuda": cuda_snapshot()})
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="S1 sequential Kaggle GPU canary; no confirmation access")
    parser.add_argument("--canary", action="store_true", required=True)
    parser.add_argument("--cache-dir", default=os.environ.get("HF_HOME", "/kaggle/working/hf-cache"))
    parser.add_argument("--receipt", type=Path, default=Path("/kaggle/working/s1_canary_receipt.json"))
    args = parser.parse_args()
    receipt = run_canary(args.cache_dir)
    receipt["python"] = platform.python_version()
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "runtime_seconds": receipt["runtime_seconds"], "receipt": str(args.receipt)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
