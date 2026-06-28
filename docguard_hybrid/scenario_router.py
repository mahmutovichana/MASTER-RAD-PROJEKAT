from __future__ import annotations


def choose_scenario(record: dict, router_output: dict) -> str:
    candidates = router_output.get("candidate_scenario_types") or []
    if candidates and candidates[0] != "unknown_change":
        return candidates[0]
    if not router_output.get("docs_update_required"):
        return record.get("scenario_type", "unknown_change")
    return candidates[0] if candidates else "unknown_change"
