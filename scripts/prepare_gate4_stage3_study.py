from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_llm_v2.gate4_study import prepare_gate4


SOURCE_PATHS = [
    "docguard_llm_v2/change_analyzer.py",
    "docguard_llm_v2/context_adapter.py",
    "docguard_llm_v2/document_retriever.py",
    "docguard_llm_v2/documentation_writer.py",
    "docguard_llm_v2/gate4_study.py",
    "docguard_llm_v2/generation_options.py",
    "docguard_llm_v2/hf_backend.py",
    "docguard_llm_v2/pipeline.py",
    "docguard_llm_v2/prompt_templates.py",
    "docguard_llm_v2/provenance_verifier.py",
    "docguard_llm_v2/repair.py",
    "docguard_llm_v2/schemas.py",
    "scripts/prepare_gate4_stage3_study.py",
    "scripts/run_gate4_external_qwen.py",
]


if __name__ == "__main__":
    print(json.dumps(prepare_gate4(ROOT, source_paths=SOURCE_PATHS), indent=2, sort_keys=True))
