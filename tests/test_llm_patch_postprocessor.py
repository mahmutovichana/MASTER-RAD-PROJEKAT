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
