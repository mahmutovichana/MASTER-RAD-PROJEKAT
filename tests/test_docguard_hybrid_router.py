from __future__ import annotations

from docguard_hybrid.doc_router import route


def test_docs_already_updated_overrides_positive_route_signal() -> None:
    record = {
        "id": "ROUTER-DOCS-ALREADY-UPDATED",
        "changed_files": ["src/routes/reviews.ts"],
        "code_diff": "+router.post('/reviews', createReview);\n",
        "docs_before": "POST /reviews is already documented in the API reference.",
    }

    routed = route(record)

    assert routed["docs_update_required"] is False
    assert routed["candidate_doc_categories"] == ["no_update"]
    assert routed["candidate_target_doc_files"] == []
    assert routed["candidate_scenario_types"] == ["docs_already_updated"]
    assert "route_added" in routed["signals"]
    assert "docs_already_updated" in routed["signals"]


def test_route_added_still_routes_to_api_reference_without_docs_coverage() -> None:
    record = {
        "id": "ROUTER-NEW-ENDPOINT",
        "changed_files": ["src/routes/reviews.ts"],
        "code_diff": "+router.post('/reviews', createReview);\n",
        "docs_before": "# API Reference\n\nExisting endpoints are listed here.",
    }

    routed = route(record)

    assert routed["docs_update_required"] is True
    assert routed["candidate_doc_categories"] == ["api_reference"]
    assert routed["candidate_target_doc_files"] == ["docs/api.md"]
    assert routed["candidate_scenario_types"] == ["new_endpoint"]


def test_visible_env_var_already_in_docs_routes_to_no_update() -> None:
    record = {
        "id": "ROUTER-ENV-DOCS-COVERAGE",
        "changed_files": ["src/config.ts"],
        "code_diff": "+  reviewWindow: process.env.REVIEW_WINDOW || '7d',\n",
        "docs_before": "- `REVIEW_WINDOW` controls how long reviews stay open and defaults to `7d`.",
    }

    routed = route(record)

    assert routed["docs_update_required"] is False
    assert routed["candidate_scenario_types"] == ["docs_already_updated"]
    assert "added_env_var" in routed["signals"]
    assert "docs_already_updated" in routed["signals"]


def test_env_var_with_mismatched_documented_default_still_requires_update() -> None:
    record = {
        "id": "ROUTER-ENV-DOCS-DEFAULT-MISMATCH",
        "changed_files": ["src/config.ts", "docs/configuration.md"],
        "code_diff": "+  reviewWindow: process.env.REVIEW_WINDOW || '4d',\n",
        "docs_before": "- `REVIEW_WINDOW` sets the review window and defaults to `7d`.",
    }

    routed = route(record)

    assert routed["docs_update_required"] is True
    assert routed["candidate_doc_categories"] == ["configuration"]
    assert routed["candidate_target_doc_files"] == ["docs/configuration.md"]
    assert routed["candidate_scenario_types"] == ["changed_default_config_value"]
    assert "added_env_var" in routed["signals"]
    assert "config_default_change" in routed["signals"]
    assert "docs_already_updated" not in routed["signals"]


def test_express_app_route_is_detected_without_log_context_false_negative() -> None:
    record = {
        "id": "ROUTER-EXPRESS-APP-GET",
        "changed_files": ["src/server.ts"],
        "code_diff": (
            "+app.get('/ticket-health', (_req, res) => {\n"
            "+  res.status(200).json({ status: 'ok' });\n"
            "+});\n"
            " app.listen(env.port, () => {\n"
            "   console.log(`Demo API running on ${env.port}`);\n"
            " });\n"
        ),
        "docs_before": "# API Reference\n\n### POST /tickets\n\nCreates a ticket.",
    }

    routed = route(record)

    assert routed["docs_update_required"] is True
    assert routed["candidate_doc_categories"] == ["api_reference"]
    assert routed["candidate_scenario_types"] == ["new_endpoint"]
    assert "route_added" in routed["signals"]
    assert "log_message_change_no_user_visible_behavior" not in routed["signals"]
