from __future__ import annotations

from docguard_llm.patch_quality import evaluate_patch_quality
from docguard_llm.patch_verifier import verify_patch


API_DIFF = "+router.post('/reviews', createReview);\n+res.status(201).json({ id: saved.id, reviewStatus: saved.status });"


def quality_for(patch: str | None, category: str = "api_reference", scenario: str = "new_endpoint") -> dict:
    verifier = verify_patch(patch, patch is not None, "docs/api.md", API_DIFF, "# API", category, scenario)
    return evaluate_patch_quality(
        patch_text=patch,
        code_diff=API_DIFF,
        docs_before="# API",
        target_doc_file="docs/api.md",
        doc_category=category,
        scenario_type=scenario,
        verifier_result=verifier,
    )


def test_grounded_minimal_patch_is_usable_or_excellent() -> None:
    result = quality_for(
        "@@ docs/api.md\n+### POST /reviews\n+Creates a review and returns `201`.\n+Response fields visible in the implementation: `id`, `reviewStatus`."
    )
    assert result["quality_label"] in {"usable", "excellent"}
    assert result["hallucination_risk"] == "low"
    assert result["usefulness_score"] >= 0.6


def test_hallucinated_patch_is_rejected_or_high_risk() -> None:
    result = quality_for(
        "@@ docs/api.md\n+### POST /reviews\n+Creates a review with request field `title`.\n+Status values: \"pending\", \"approved\"."
    )
    assert result["quality_label"] == "rejected"
    assert result["hallucination_risk"] == "high"


def test_generic_legacy_patch_is_low_usefulness() -> None:
    result = quality_for("@@ Documentation\n+new_endpoint.")
    assert result["quality_label"] in {"needs_review", "rejected"}
    assert result["usefulness_score"] <= 0.45
    assert any("generic" in reason for reason in result["quality_reasons"])


def test_no_update_empty_patch_is_excellent() -> None:
    result = evaluate_patch_quality(
        patch_text=None,
        code_diff="+const renamedInternalTotal = reviews.length;",
        docs_before="# API",
        target_doc_file="",
        doc_category="no_update",
        scenario_type="internal_variable_rename_no_behavior_change",
        verifier_result={"verifier_status": "pass", "warnings": [], "grounded_tokens_found": []},
    )
    assert result["quality_label"] == "excellent"
    assert result["hallucination_risk"] == "low"
