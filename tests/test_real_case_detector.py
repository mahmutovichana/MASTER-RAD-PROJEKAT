from __future__ import annotations

from docguard_external.real_case_detector import extract_real_case_signals, predict_real_case_runtime


def test_real_case_detector_detects_schema_contract_change() -> None:
    record = {
        "id": "REAL-SCHEMA",
        "changed_files": ["schemas/organization.schema.json", "src/validate.ts"],
        "code_diff": '''
+          "pluginInstallUrlPrefix": {
+            "type": "string",
+            "description": "URL prefix for auto-generating Agent Plugin install URLs."
+          }
''',
        "docs_before": "# Registry docs",
    }

    result = predict_real_case_runtime(record)

    assert result["docs_update_required"] is True
    assert result["doc_category"] in {"model_contract", "configuration", "api_reference"}
    assert result["decision_source"] == "real_case_detector"


def test_real_case_detector_detects_configuration_change() -> None:
    record = {
        "id": "REAL-CONFIG",
        "changed_files": ["config/cicerone.serve.toml", "src/cicerone/config/settings.py"],
        "code_diff": '''
+metrics_enabled = true
+metrics_token = ""
''',
        "docs_before": "# Serve mode",
    }

    result = predict_real_case_runtime(record)

    assert result["docs_update_required"] is True
    assert result["doc_category"] == "configuration"
    assert "configuration_change" in result["router_output"]["signals"]


def test_real_case_detector_detects_public_endpoint_change() -> None:
    record = {
        "id": "REAL-ENDPOINT",
        "changed_files": ["src/server.py"],
        "code_diff": '''
+@app.get("/metrics")
+def metrics():
+    return prometheus_metrics()
''',
        "docs_before": "# API",
    }

    result = predict_real_case_runtime(record)

    assert result["docs_update_required"] is True
    assert result["doc_category"] == "api_reference"


def test_real_case_detector_ignores_comment_only_change() -> None:
    record = {
        "id": "REAL-NOUPDATE",
        "changed_files": ["src/internal.ts"],
        "code_diff": '''
-// old internal helper comment
+// clearer internal helper comment
''',
        "docs_before": "# Internal docs",
    }

    result = predict_real_case_runtime(record)

    assert result["docs_update_required"] is False
    assert result["doc_category"] == "no_update"


def test_real_case_signals_do_not_require_gold_fields() -> None:
    record = {
        "id": "REAL-NOGOLD",
        "changed_files": ["packages/sdk/src/types.ts"],
        "code_diff": '''
+export type AgentNextStep = {
+  nextAction: string
+}
''',
        "docs_before": "# SDK",
    }

    signals = extract_real_case_signals(record)

    assert signals["schema_or_model_change"] is True
    assert "AgentNextStep" in signals["public_fields"]