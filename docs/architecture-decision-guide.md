# Choose an implementation pattern

This kit supports organizations at different levels of AI integration readiness. No pattern is universally best.

| Pattern | External connection | Determinism | Primary use | Main limitation |
| --- | --- | --- | --- | --- |
| Guidance Agent | None | Low | Control education, guided intake, structured fact summaries | Must not claim authoritative tiers or control applicability |
| Structured Assessment Agent | None outside Microsoft Power Platform | Rule-based flow can be deterministic | Repeatable tiering inside Copilot Studio | Duplicates a versioned decision specification and requires revalidation |
| MCP-backed Assistant | Hosted MCP service | High | Reusable tested service across AI clients | Requires hosting, authentication, connector approval, and operational ownership |

## Recommended adoption path

Start with the Guidance Agent when the organization permits Copilot knowledge sources but does not permit external tools or custom connections. It provides immediate practitioner value and makes its limits visible.

Add the Structured Assessment track only when the organization needs repeatable tiering and can govern an agent flow as a derived implementation. The flow should contain only deterministic branching and data operations. Do not use a generative prompt to calculate the tier.

Use the MCP-backed Assistant when a central governance service, cross-client reuse, automated provenance validation, and one maintained implementation justify the infrastructure and connection controls.

## Authority boundaries

- Framework: authoritative control content and applicability metadata.
- Control Plane: authoritative reference implementation for deterministic validation, risk evaluation, control applicability, and comparison.
- Copilot kit: implementation guidance and generated derivatives.
- Copilot agent: conversation and presentation layer.
- Qualified human: final governance decision and organization-specific interpretation.

The Copilot implementation must never become an independently maintained control library.
