# Microsoft platform notes

This kit targets Microsoft Copilot Studio's current standard agent experience. Microsoft changes platform terminology, features, licensing, and administrative requirements over time. Verify current Microsoft documentation before implementation.

As of the initial kit release:

- Copilot Studio supports uploaded Markdown and YAML files as agent knowledge sources.
- Uploaded files are stored in Dataverse and require Dataverse search in the environment.
- Agent flows provide deterministic rule-based execution and can be managed in Power Platform solutions.
- Flow actions consume Copilot Studio capacity outside applicable licensed-user and test-run exceptions.
- Sharing and organizational publication remain subject to environment permissions, licensing, authentication configuration, tenant policy, and administrator approval.

Official references:

- [Upload files as a knowledge source](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
- [Agent flows overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview)
- [Share agents with other users](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-share-bots)
- [Connect and configure an agent for Teams and Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams)
- [Connect an existing MCP server to an agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
