from __future__ import annotations

from docguard_llm.patch_verifier import verify_patch


def test_verifier_passes_grounded_patch() -> None:
    result = verify_patch(
        "@@ API\n+Document POST `/reviews`.",
        True,
        "docs/api.md",
        "+router.post('/reviews', createReview);",
        "# API",
    )
    assert result["verifier_status"] == "pass"
    assert "/reviews" in result["grounded_tokens_found"]


def test_verifier_fails_hallucinated_security_claim() -> None:
    result = verify_patch(
        "@@ API\n+Requires OAuth admin JWT.",
        True,
        "docs/api.md",
        "+router.post('/reviews', createReview);",
        "# API",
    )
    assert result["verifier_status"] == "fail"
    assert result["warnings"]
