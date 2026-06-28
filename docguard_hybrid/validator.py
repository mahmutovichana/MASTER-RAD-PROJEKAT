from __future__ import annotations

DOC_FILES = {"docs/api.md", "docs/architecture.md", "docs/models.md", "docs/developer-setup.md", "docs/testing.md", "docs/configuration.md", "docs/workflows.md", "CHANGELOG.md"}


def validate_prediction(prediction: dict) -> dict:
    row = dict(prediction)
    if not row.get("docs_update_required"):
        row["doc_category"] = "no_update"
        row["target_doc_file"] = ""
        row["generated_doc_patch"] = None
    elif row.get("target_doc_file") not in DOC_FILES:
        row["target_doc_file"] = "docs/api.md"
        row["corrected_target_doc_file"] = True
    return row
