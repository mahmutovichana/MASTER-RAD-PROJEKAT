from __future__ import annotations

import pytest

from docguard_llm.prompt_builder import build_patch_prompt


def test_patch_prompt_contains_safe_runtime_inputs() -> None:
    prompt, metadata = build_patch_prompt(
        code_diff="+router.post('/reviews', createReview);",
        docs_before="# API\n\nExisting docs.",
        target_doc_file="docs/api.md",
        doc_category="api_reference",
        scenario_type="new_endpoint",
        signals=["route_added"],
        router_reason="Matched positive signal",
        project_id="atlas_review_api",
    )
    assert "+router.post('/reviews', createReview);" in prompt
    assert "# API" in prompt
    assert "api_reference" in prompt
    assert "docs/api.md" in prompt
    assert "route_added" in prompt
    assert "Allowed facts extracted from the diff" in prompt
    assert "Do not add response fields unless they appear in allowed facts." in prompt
    assert "/reviews" in metadata["grounding_tokens"]
    assert "/reviews" in metadata["allowed_facts"]["route_paths"]


def test_patch_prompt_signature_rejects_forbidden_inputs() -> None:
    forbidden = {
        "gold_doc_category": "api_reference",
        "expected_facts": ["POST /reviews"],
        "expected_patch_summary": "Document endpoint",
        "docs_after": "Future docs",
    }
    with pytest.raises(TypeError):
        build_patch_prompt(
            code_diff="+router.post('/reviews', createReview);",
            docs_before="# API",
            target_doc_file="docs/api.md",
            doc_category="api_reference",
            scenario_type="new_endpoint",
            signals=["route_added"],
            router_reason="Matched positive signal",
            project_id="atlas_review_api",
            **forbidden,
        )
