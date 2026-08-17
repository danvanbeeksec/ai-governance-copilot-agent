"""Generate Copilot-ready derivatives from pinned authoritative packages."""

from __future__ import annotations

import hashlib
import csv
import io
import json
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from ai_governance_control_framework import controls_text
from ai_governance_control_plane.service import GovernanceDecisionService


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = Path.cwd() / "generated"


def _resource_text(packaged_name: str, source_path: Path) -> str:
    packaged = files("ai_governance_copilot_agent").joinpath(
        "resources", packaged_name
    )
    try:
        return packaged.read_text()
    except FileNotFoundError:
        return source_path.read_text()


def _sources_lock() -> dict[str, Any]:
    content = _resource_text("sources.lock.yaml", ROOT / "sources.lock.yaml")
    return yaml.safe_load(content)


def _acceptance_scenarios() -> dict[str, Any]:
    content = _resource_text(
        "acceptance_scenarios.json",
        ROOT / "tests" / "fixtures" / "acceptance_scenarios.json",
    )
    return json.loads(content)


def _heading(value: str) -> str:
    return value.replace("_", " ").title()


def _render_controls(framework: dict[str, Any]) -> str:
    library = framework["library"]
    lines = [
        "# Independent AI Control Library for Copilot",
        "",
        "> Generated knowledge derivative. The AI Governance Control Framework is the control authority.",
        "> This file supports guidance and explanation. It does not determine risk tiers or legal compliance.",
        "",
        f"Framework version: {library['version']}",
        f"Framework status: {library['status']}",
        "",
        "## Framework limitations",
        "",
    ]
    lines.extend(f"- {item}" for item in library["limitations"])
    for control in framework["controls"]:
        metadata = control["applicability_metadata"]
        lines.extend(
            [
                "",
                f"## {control['control_id']}: {control['title']}",
                "",
                f"Domain: {_heading(control['domain'])}",
                f"Layer: {_heading(control['layer'])}",
                "",
                f"Objective: {control['objective']}",
                "",
                f"Requirement: {control['requirement']}",
                "",
                f"Applicability statement: {control['applicability']}",
                "",
                f"Applicability mode: {metadata['mode']}",
                f"Applicable contexts: {', '.join(metadata['contexts'])}",
                f"Applicability rationale: {metadata['rationale']}",
                "",
                "Evidence examples:",
            ]
        )
        lines.extend(f"- {item}" for item in control["evidence_examples"])
        lines.extend(
            [
                "",
                f"Implementation notes: {control['implementation_notes']}",
                f"Public references: {', '.join(control['references'])}",
            ]
        )
    return "\n".join(lines) + "\n"


def _render_intake(service: GovernanceDecisionService, control_plane_version: str) -> str:
    requirements = service.get_assessment_requirements().model_dump(mode="json")
    model = service.risk_model
    lines = [
        "# Guided AI Assessment Intake",
        "",
        f"> Generated from Control Plane {control_plane_version}. This guide gathers explicit facts but does not authorize",
        "> a language model to assign a deterministic risk tier.",
        "",
        "## Intake rules",
        "",
        "- Ask only for information the user can verify.",
        "- Never infer a missing value silently.",
        "- State an uncertain interpretation and its basis, then ask the user to confirm or replace it.",
        "- Do not ask the user for an assessment ID. That is a system-managed field.",
        "- If any required value remains missing or invalid, do not present a final tier.",
        "",
        "## Required user-provided facts",
        "",
    ]
    for item in requirements["fields"]:
        lines.extend([f"### {_heading(item['field'])}", "", item["question"]])
        if item["allowed_values"]:
            lines.extend(
                ["", "Supported values:", *[f"- `{value}`" for value in item["allowed_values"]]]
            )
        if item["accepts_multiple"]:
            lines.extend(["", "The user may select more than one value, or none."])
        lines.append("")
    lines.extend(
        [
            "## Tier interpretation",
            "",
            "- Tier 1 is the highest inherent-risk tier and requires the strongest governance attention.",
            "- Tier 2 represents elevated inherent risk.",
            "- Tier 3 is the lowest of the three inherent-risk tiers. It does not mean no risk or automatic approval.",
            "- Controls do not reduce the inherent tier in this model.",
            "- A qualified human owns the final decision.",
            "",
            f"Reference model: `{model['model']['id']}` version `{model['model']['version']}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_provenance(lock: dict[str, Any]) -> str:
    framework = lock["sources"]["framework"]
    plane = lock["sources"]["control_plane"]
    return f"""# Provenance and Use Boundaries

This knowledge bundle is a generated derivative. It is not a new control authority or decision engine.

## Authoritative control source

- Repository: `{framework['repository']}`
- Version: `{framework['version']}`
- Commit: `{framework['commit']}`

## Deterministic reference implementation

- Repository: `{plane['repository']}`
- Version: `{plane['version']}`
- Commit: `{plane['commit']}`

The Guidance Agent may explain controls, gather facts, identify missing information, and support human discussion. It must not represent model-generated reasoning as a deterministic Control Plane result. The Structured Assessment track is a versioned derivative that must be revalidated whenever either pinned source changes.

Use only fictional or synthetic information in public demonstrations. Outputs are not legal advice, certification, approval, or a substitute for qualified human review.
"""


def _expected_results(service: GovernanceDecisionService) -> dict[str, Any]:
    scenarios = _acceptance_scenarios()
    results: dict[str, Any] = {}
    for name, assessment in scenarios.items():
        evaluated = service.assess_ai_system(assessment).model_dump(mode="json")
        results[name] = {
            "final_tier": evaluated["decision"]["final_tier"],
            "applied_rules": [
                rule["rule_id"] for rule in evaluated["decision"]["applied_rules"]
            ],
            "applicable_control_ids": sorted(
                item["control"]["control_id"]
                for item in evaluated["recommendations"]["applicable_system_controls"]
            ),
            "undetermined_control_ids": sorted(
                item["control"]["control_id"]
                for item in evaluated["recommendations"]["undetermined_system_controls"]
            ),
        }
    return results


def _baseline_worksheet(model: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["autonomy_level", "information_sensitivity", "baseline_tier"])
    for autonomy, sensitivities in model["baseline_matrix"].items():
        for sensitivity, tier in sensitivities.items():
            writer.writerow([autonomy, sensitivity, tier])
    return output.getvalue()


def _elevation_worksheet(model: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["rule_id", "name", "conditions_json", "minimum_tier", "reason"])
    for rule in model["elevation_rules"]:
        writer.writerow(
            [
                rule["id"],
                rule["name"],
                json.dumps(rule["when"], sort_keys=True, separators=(",", ":")),
                rule["minimum_tier"],
                rule["reason"],
            ]
        )
    return output.getvalue()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build(output: Path = DEFAULT_OUTPUT) -> dict[str, str]:
    """Generate all committed derivatives and return their SHA-256 hashes."""
    framework = yaml.safe_load(controls_text())
    lock = _sources_lock()
    service = GovernanceDecisionService.from_packaged_resources()

    artifacts = {
        "knowledge/control-library.md": _render_controls(framework),
        "knowledge/guided-intake.md": _render_intake(
            service, lock["sources"]["control_plane"]["version"]
        ),
        "knowledge/provenance-and-boundaries.md": _render_provenance(lock),
        "structured-assessment/decision-specification.yaml": yaml.safe_dump(
            service.risk_model, sort_keys=False, width=100
        ),
        "structured-assessment/applicability-specification.yaml": yaml.safe_dump(
            service.methodology.model_dump(mode="json"), sort_keys=False, width=100
        ),
        "structured-assessment/baseline-matrix.csv": _baseline_worksheet(
            service.risk_model
        ),
        "structured-assessment/elevation-rules.csv": _elevation_worksheet(
            service.risk_model
        ),
        "validation/expected-results.json": json.dumps(
            _expected_results(service), indent=2, sort_keys=True
        )
        + "\n",
    }
    for relative, content in artifacts.items():
        _write(output / relative, content)

    hashes = {
        relative: hashlib.sha256(content.encode()).hexdigest()
        for relative, content in artifacts.items()
    }
    manifest = {
        "schema_version": "1.0",
        "generated_from": lock["sources"],
        "artifacts": hashes,
    }
    _write(output / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return hashes


def main() -> None:
    build()


if __name__ == "__main__":
    main()
