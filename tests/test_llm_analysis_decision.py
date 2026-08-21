from __future__ import annotations

from docguard_llm.analysis_decision import generate_analysis_decision


def test_llm_analysis_decision_parses_json(monkeypatch) -> None:
    def fake_generate(*args, **kwargs):
        return {
            "generation_status": "ok",
            "patch_text": (
                '{"docs_update_required": true, "target_doc_file": "docs/configuration.md", '
                '"scenario_type": "changed_default_config_value", "confidence": 0.91, '
                '"reason": "The diff changes the REVIEW_WINDOW default."}'
            ),
        }

    monkeypatch.setattr("docguard_llm.analysis_decision.generate_documentation_patch", fake_generate)

    decision = generate_analysis_decision(
        changed_files=["src/config.ts"],
        code_diff="+reviewWindow: process.env.REVIEW_WINDOW || '4d'",
        docs_before="- `REVIEW_WINDOW` defaults to `7d`.",
        backend="llm-openai-compatible",
        model_name="example/model",
    )

    assert decision["decision_status"] == "ok"
    assert decision["docs_update_required"] is True
    assert decision["doc_category"] == "configuration"
    assert decision["target_doc_file"] == "docs/configuration.md"
    assert decision["target_section"] == "Environment Variables"
    assert decision["scenario_type"] == "changed_default_config_value"


def test_llm_analysis_decision_rejects_unknown_target(monkeypatch) -> None:
    def fake_generate(*args, **kwargs):
        return {
            "generation_status": "ok",
            "patch_text": '{"docs_update_required": true, "target_doc_file": "docs/secrets.md"}',
        }

    monkeypatch.setattr("docguard_llm.analysis_decision.generate_documentation_patch", fake_generate)

    decision = generate_analysis_decision(
        changed_files=["src/config.ts"],
        code_diff="+reviewWindow: process.env.REVIEW_WINDOW || '4d'",
        docs_before="",
        backend="llm-openai-compatible",
        model_name="example/model",
    )

    assert decision["docs_update_required"] is False
    assert decision["doc_category"] == "no_update"
    assert decision["target_doc_file"] == ""
