# Build Track B: Structured Assessment Agent

Track B adds a deterministic agent flow inside Copilot Studio. It does not require an external API or MCP server, but it does reproduce a versioned derivative of Control Plane logic inside Microsoft Power Platform.

Do not implement the tier calculation as a generative prompt. Microsoft describes agent flows as deterministic rule-based paths. Use variables, conditions, and data operations only.

## Derived specifications

- `generated/structured-assessment/decision-specification.yaml` contains the pinned baseline matrix and elevation rules.
- `generated/structured-assessment/applicability-specification.yaml` contains the pinned applicability evaluation contract.
- `generated/structured-assessment/baseline-matrix.csv` is a flow-construction worksheet with one row per baseline combination.
- `generated/structured-assessment/elevation-rules.csv` is a flow-construction worksheet with serialized conditions and required minimum tiers.
- `generated/validation/expected-results.json` contains results calculated by Control Plane 0.6.0 for the synthetic acceptance scenarios.

These files are generated artifacts. Do not edit them directly.

## Suggested flow boundary

Create one agent flow named `Evaluate AI Inherent Risk` with twelve user-provided inputs:

- system name
- business purpose
- accountable owner
- autonomy level
- information sensitivity
- human review
- action authority
- system access
- external reach
- reversibility
- decision impact
- agent capabilities

The flow should generate its own correlation ID. It should return status, baseline tier, every matched elevation rule, final tier, explanation, model version, and `human_review_required=true`.

## Deterministic algorithm

1. Validate that every required input is present and every enumerated value is supported.
2. If validation fails, return `needs_information` and no tier.
3. Select the baseline tier from the autonomy-level and information-sensitivity matrix.
4. Evaluate every elevation rule independently. Do not stop after the first match.
5. Apply each matched rule's minimum tier using the order Tier 1, Tier 2, Tier 3, where Tier 1 is highest.
6. Never lower the baseline tier.
7. Return every matched rule, including a rule that confirms an already-high tier.
8. Require qualified human review.

Use the CSV worksheets to build and peer-review the branches. They are implementation aids, not runtime knowledge sources. Preserve rule IDs in flow outputs so each result can be compared with the deterministic expected results.

## Applicability scope

Risk tiering and control applicability are separate calculations. Implement tiering first. Add automatic applicability only after the tier flow passes all acceptance scenarios.

Universal and conditional controls can be evaluated from the generated applicability specification. Controls marked `human_determination` must be returned for qualified review, not automatically marked applicable or not applicable.

## Solution lifecycle

Build the agent and flow inside a dedicated Power Platform solution so they can be versioned, exported, imported, and reviewed. Record Framework and Control Plane versions in the solution description.

When a pinned source changes:

1. regenerate this repository's artifacts;
2. review the specification diff;
3. update the agent flow;
4. run the complete acceptance suite;
5. obtain qualified approval; and
6. publish a new solution version.

## Completion criteria

The structured track is not complete merely because the agent returns a tier. It is complete when the flow produces the expected baseline, matched rules, final tier, provenance, and incomplete-input behavior for every synthetic scenario in this repository.
