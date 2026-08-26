from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_eval_v2.reference_evaluation import sha256_file, write_json
from docguard_ml_v2.model_manifest import utc_now
from docguard_llm_v2.generation_options import options_for_purpose


REQUIRED_CONFIG_KEYS = {"pipeline_version", "analysis_model", "writer_model", "repair_model", "temperature", "max_tokens_analysis", "max_tokens_writer", "max_tokens_repair", "top_k_documents", "max_repair_attempts"}


def validate_config(cfg: dict) -> None:
    missing = sorted(REQUIRED_CONFIG_KEYS - set(cfg))
    if missing:
        raise ValueError(f"Stage 3 config is missing required runtime keys: {missing}")
    for purpose in ["analysis", "writer", "repair"]:
        options_for_purpose(cfg, purpose)
    if int(cfg["max_repair_attempts"]) < 0 or int(cfg["max_repair_attempts"]) > 1:
        raise ValueError("Final Stage 3 V2 supports at most one repair attempt")


def source_hashes(root: Path) -> dict[str, str]:
    files = sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)
    return {str(path.relative_to(root)).replace("\\", "/"): sha256_file(path) for path in files}


def run(config: Path, pipeline_source_root: Path, development_summary: Path, output: Path) -> dict:
    cfg = json.loads(config.read_text(encoding="utf-8"))
    validate_config(cfg)
    manifest = {
        "pipeline_version": cfg.get("pipeline_version"),
        "model_identifiers": {key: cfg.get(key) for key in ["analysis_model", "writer_model", "repair_model"]},
        "temperature": cfg.get("temperature"),
        "token_settings": {key: cfg.get(key) for key in ["max_tokens_analysis", "max_tokens_writer", "max_tokens_repair"]},
        "top_k": cfg.get("top_k_documents"),
        "repair_attempts": cfg.get("max_repair_attempts"),
        "runtime_generation_settings_supported": True,
        "backend_adapter_version": "docguard_llm_v2.generation_options.v1",
        "config_sha256": sha256_file(config),
        "source_file_sha256": source_hashes(pipeline_source_root),
        "development_summary_sha256": sha256_file(development_summary),
        "freeze_timestamp": utc_now(),
        "confirmation_accessed": False,
    }
    write_json(output, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze Stage 3 V2 generator configuration and source hashes.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--pipeline-source-root", required=True)
    parser.add_argument("--development-summary", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.config), Path(args.pipeline_source_root), Path(args.development_summary), Path(args.output)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
