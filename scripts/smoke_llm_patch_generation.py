from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_demo.run_project_evolution_flow import run
from docguard_llm.fact_extractor import extract_allowed_facts
from docguard_llm.llm_generator import generate_documentation_patch
from docguard_llm.patch_postprocessor import postprocess_patch
from docguard_llm.patch_verifier import verify_patch
from docguard_llm.prompt_builder import build_patch_prompt


def main() -> int:
    full_api_diff = "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id, reviewStatus: saved.status });"
    facts = extract_allowed_facts(full_api_diff, "# API", "api_reference", "new_endpoint")
    assert "/reviews" in facts["allowed_tokens"]
    assert "201" in facts["allowed_tokens"]
    assert "id" in facts["allowed_facts"]["response_fields"]
    assert "reviewStatus" in facts["allowed_facts"]["response_fields"]
    assert "title" not in facts["allowed_tokens"]
    prompt, metadata = build_patch_prompt(
        code_diff=full_api_diff,
        docs_before="# API Reference\n",
        target_doc_file="docs/api.md",
        doc_category="api_reference",
        scenario_type="new_endpoint",
        signals=["route_added"],
        router_reason="Matched positive signal `route_added`",
        project_id="atlas_review_api",
    )
    assert "/reviews" in prompt
    assert "Allowed facts extracted from the diff" in prompt
    assert "/reviews" in metadata["grounding_tokens"]
    generated = generate_documentation_patch(prompt, backend="mock")
    assert generated["generation_status"] == "ok"
    processed = postprocess_patch(generated["patch_text"], "docs/api.md")
    assert processed["postprocess_status"] == "ok"
    verified = verify_patch(processed["patch_text"], True, "docs/api.md", full_api_diff, "# API", "api_reference", "new_endpoint")
    assert verified["verifier_status"] in {"pass", "warn"}
    hallucinated = verify_patch(
        "@@ docs/api.md\n+### POST /reviews\n+Creates a review with request field `title`.\n+Returns `201` with `id`, `status`.\n+Status values: \"pending\", \"approved\".",
        True,
        "docs/api.md",
        full_api_diff,
        "# API",
        "api_reference",
        "new_endpoint",
    )
    assert hallucinated["verifier_status"] == "fail"
    with tempfile.TemporaryDirectory() as tmp:
        result = run(Path(tmp), patch_backend="llm-mock")
        assert result["status"] == "ok"
        assert (Path(tmp) / "docguard_llm_mock_patch_generation_report_2026_08.md").exists()
    print("llm patch generation smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
