from __future__ import annotations

from docguard_llm.patch_postprocessor import postprocess_patch


def test_postprocessor_normalizes_plain_markdown() -> None:
    result = postprocess_patch("assistant: Document `/reviews`.", "docs/api.md", "Reviews")
    assert result["postprocess_status"] == "ok"
    assert result["patch_text"].startswith("@@ Reviews")
    assert "+Document `/reviews`." in result["patch_text"]


def test_postprocessor_rejects_unsupported_filename() -> None:
    result = postprocess_patch("@@ API\n+Update docs/models.md too.", "docs/api.md")
    assert result["postprocess_status"] == "fail"
    assert result["patch_text"] is None


def test_postprocessor_removes_noisy_model_labels_and_tables() -> None:
    result = postprocess_patch(
        "patch:\ndocs/api.md:\n| Field | Meaning |\n| --- | --- |\n| id | Review id |",
        "docs/api.md",
    )
    assert result["postprocess_status"] == "ok"
    assert "patch:" not in result["patch_text"].lower()
    assert "| --- |" not in result["patch_text"]


def test_postprocessor_truncates_prompt_leakage_after_patch() -> None:
    result = postprocess_patch(
        "```markdown\n## Environment Variables\n\n- `REVIEW_WINDOW` sets the review window and defaults to `7d`.\n"
        "Use this draft only if it is supported by the diff.\nCurrent documentation:\n```md\n# Configuration\n```",
        "docs/configuration.md",
        "Environment Variables",
    )

    assert result["postprocess_status"] == "ok"
    assert "REVIEW_WINDOW" in result["patch_text"]
    assert "Current documentation" not in result["patch_text"]
    assert any("prompt leakage" in warning for warning in result["warnings"])


def test_postprocessor_removes_repeated_target_section_heading() -> None:
    result = postprocess_patch(
        "## Environment Variables\n## Environment Variables\n- `REVIEW_WINDOW` sets the review window and defaults to `7d`.",
        "docs/configuration.md",
        "Environment Variables",
    )

    assert result["postprocess_status"] == "ok"
    assert result["patch_text"].count("Environment Variables") == 1
    assert "`REVIEW_WINDOW`" in result["patch_text"]
    assert any("section heading" in warning for warning in result["warnings"])
