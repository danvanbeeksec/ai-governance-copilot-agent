# Guided AI Assessment Intake

> Generated from Control Plane 0.6.0. This guide gathers explicit facts but does not authorize
> a language model to assign a deterministic risk tier.

## Intake rules

- Ask only for information the user can verify.
- Never infer a missing value silently.
- State an uncertain interpretation and its basis, then ask the user to confirm or replace it.
- Do not ask the user for an assessment ID. That is a system-managed field.
- If any required value remains missing or invalid, do not present a final tier.

## Required user-provided facts

### System Name

What is the AI system or use case called?

### Business Purpose

What business purpose will the AI system serve?

### Accountable Owner

Who is accountable for the AI system or use case?

### Autonomy Level

How independently can the AI system act?

Supported values:
- `autonomous`
- `conditionally_autonomous`
- `human_supervised`

### Information Sensitivity

What is the highest sensitivity of information it can process?

Supported values:
- `public`
- `internal`
- `confidential`
- `restricted`

### Human Review

When must a person review a meaningful action?

Supported values:
- `prior_to_each_meaningful_action`
- `checkpoints_or_exceptions`
- `no_prior_review`

### Action Authority

What is the most consequential action the system may take?

Supported values:
- `generate_only`
- `recommend`
- `modify_nonproduction`
- `modify_production`
- `execute_material_transaction`
- `safety_relevant_action`

### System Access

What level of access does the system have to organizational systems?

Supported values:
- `none`
- `standard`
- `privileged`

### External Reach

How broadly can the system interact outside its immediate environment?

Supported values:
- `none`
- `bounded`
- `broad`

### Reversibility

How difficult is it to reverse the system's material effects?

Supported values:
- `easy`
- `recoverable_with_effort`
- `difficult`

### Decision Impact

What is the highest potential impact of decisions it supports or makes?

Supported values:
- `none`
- `operational`
- `consequential`
- `regulated_or_consequential`

### Agent Capabilities

Which agent capabilities are enabled, if any?

Supported values:
- `external_tools`
- `external_communication`
- `delegation`
- `persistent_memory`

The user may select more than one value, or none.

## Tier interpretation

- Tier 1 is the highest inherent-risk tier and requires the strongest governance attention.
- Tier 2 represents elevated inherent risk.
- Tier 3 is the lowest of the three inherent-risk tiers. It does not mean no risk or automatic approval.
- Controls do not reduce the inherent tier in this model.
- A qualified human owns the final decision.

Reference model: `ai-governance-inherent-risk` version `0.1.0`.
