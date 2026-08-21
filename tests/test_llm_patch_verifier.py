from __future__ import annotations

from docguard_llm.patch_verifier import verify_patch


def test_verifier_passes_grounded_patch() -> None:
    result = verify_patch(
        "@@ docs/api.md\n+### POST /reviews\n+Creates a review and returns `201`.\n+Response fields visible in the implementation: `id`, `reviewStatus`.",
        True,
        "docs/api.md",
        "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id, reviewStatus: saved.status });",
        "# API",
        "api_reference",
        "new_endpoint",
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
        "api_reference",
        "new_endpoint",
    )
    assert result["verifier_status"] == "fail"
    assert result["warnings"]


def test_verifier_rejects_old_hallucinated_reviews_patch() -> None:
    result = verify_patch(
        "@@ docs/api.md\n+### POST /reviews\n+Creates a review with request field `title`.\n+Returns `201` with `id`, `status`.\n+Status values: \"pending\", \"approved\".",
        True,
        "docs/api.md",
        "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id, reviewStatus: saved.status });",
        "# API",
        "api_reference",
        "new_endpoint",
    )
    assert result["verifier_status"] == "fail"


def test_verifier_rejects_no_content_patch_for_visible_env_change() -> None:
    result = verify_patch(
        "@@ Environment Variables\n+No additional content is required.",
        True,
        "docs/configuration.md",
        "+  reviewWindow: process.env.REVIEW_WINDOW || '7d',",
        "# Configuration\n\n## Environment Variables\n\n- `PORT` controls the HTTP port.",
        "configuration",
        "added_environment_variable",
    )

    assert result["verifier_status"] == "fail"
    assert any("no content" in warning for warning in result["warnings"])
    assert any("REVIEW_WINDOW" in warning for warning in result["warnings"])
