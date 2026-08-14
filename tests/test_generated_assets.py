from __future__ import annotations

import json
from pathlib import Path

import yaml
from ai_governance_control_framework import controls_text
from ai_governance_control_plane.service import GovernanceDecisionService

from ai_governance_copilot_agent import __version__
from ai_governance_copilot_agent.generator import ROOT, build


GENERATED = ROOT / "generated"


def test_release_and_source_versions_are_explicit():
    assert __version__ == "0.1.0"
    lock = yaml.safe_load((ROOT / "sources.lock.yaml").read_text())
    assert lock["sources"]["framework"]["version"] == "1.1.0"
    assert lock["sources"]["control_plane"]["version"] == "0.5.0"


def test_committed_derivatives_are_current(tmp_path: Path):
    expected_hashes = build(tmp_path)
    committed_manifest = json.loads((GENERATED / "manifest.json").read_text())
    assert committed_manifest["artifacts"] == expected_hashes
    for relative in expected_hashes:
        assert (GENERATED / relative).read_bytes() == (tmp_path / relative).read_bytes()


def test_control_knowledge_contains_every_authoritative_control():
    framework = yaml.safe_load(controls_text())
    knowledge = (GENERATED / "knowledge" / "control-library.md").read_text()
    for control in framework["controls"]:
        assert f"## {control['control_id']}: {control['title']}" in knowledge


def test_guided_intake_hides_managed_id_and_preserves_tier_meaning():
    intake = (GENERATED / "knowledge" / "guided-intake.md").read_text()
    assert "### Assessment Id" not in intake
    assert "Do not ask the user for an assessment ID" in intake
    assert "Tier 1 is the highest" in intake
    assert "Tier 3 is the lowest" in intake


def test_generated_decision_specification_matches_control_plane():
    service = GovernanceDecisionService.from_packaged_resources()
    generated = yaml.safe_load(
        (GENERATED / "structured-assessment" / "decision-specification.yaml").read_text()
    )
    assert generated == service.risk_model


def test_expected_results_are_control_plane_outputs():
    expected = json.loads(
        (GENERATED / "validation" / "expected-results.json").read_text()
    )
    assert expected["internal_assistant"]["final_tier"] == "tier_3"
    assert expected["internal_assistant"]["applied_rules"] == []
    assert expected["customer_system"]["final_tier"] == "tier_1"
    assert expected["customer_system"]["applied_rules"] == ["ER-003", "ER-004"]
    assert expected["autonomous_agent"]["applied_rules"] == ["ER-005"]


def test_guidance_instructions_do_not_claim_deterministic_execution():
    instructions = (ROOT / "agent" / "guidance-agent-instructions.md").read_text()
    assert "Do not calculate or claim a deterministic tier" in instructions
    assert "Do not ask the user for an assessment ID" in instructions
    assert "A qualified human owns every final governance decision" in instructions
