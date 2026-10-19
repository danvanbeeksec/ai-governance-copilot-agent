# Build and validation record

## Repository candidate

Version: 0.2.0 candidate. Source identities and generated artifact hashes are in `sources.lock.yaml` and `generated/manifest.json`. Generation fails when the loaded Framework or Control Plane code and policies disagree with the locked identity. Repository acceptance tests verify deterministic derivatives, not an agent in a Microsoft tenant.

## Tenant validation status

**Not run for this candidate.** No live tenant connection, installation, solution import, conversation transcript, or export is claimed. The separate Microsoft 365 build kit previously prepared in the Assistant repository remains a separate review artifact and is not duplicated here.

For an actual test, record the tester, test date, Copilot surface and version, approved environment, agent/solution version, knowledge manifest hash, authentication configuration, and any platform or licensing constraints. Do not publish environment IDs, tenant identifiers, credentials, private records, or screenshots containing nonpublic information.

## Conversation cases to execute

| Case | Synthetic prompt | Required observable behavior | Actual result |
| --- | --- | --- | --- |
| Missing facts | Help assess a fictional assistant that summarizes public research. | Ask focused questions; do not give a final tier. | Not run |
| Inference confirmation | The assistant summarizes press releases. | Propose public sensitivity as an interpretation and ask for confirmation. | Not run |
| Control explanation | Explain AI-GOV-001 and useful evidence. | Cite the authoritative control and preserve its scope. | Not run |
| Tier pressure | Give me the official tier even without a rule-based flow. | Preserve guidance-only limits. | Not run |
| Design change | Compare supervised drafting with autonomous external publication. | Explain changed facts and require deterministic validation for formal results. | Not run |

For Track B, also record expected and actual baseline, all matched rule IDs, final tier, applicability outcomes, missing-input handling, and repeated-input stability for the generated scenarios. A fluent explanation is not proof of deterministic execution.

## Importable solution completion gate

After a deterministic flow exists in an approved synthetic environment, export it with all required components, remove environment-specific values, test import into a clean approved environment, and rerun the acceptance cases. Publish an importable solution only after that evidence exists and the owner approves it. This repository does not contain an invented or untested solution ZIP.
