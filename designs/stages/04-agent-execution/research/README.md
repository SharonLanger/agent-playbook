# Research references and reuse limits

Status: **preserved evidence and design references; no new dependency or copied third-party implementation selected.**

Start with the [decision board's reference register and research findings](../decisions.md#reference-register). It retains the native message/control comparisons, source blob SHAs, all five projects and P01–P11 with their changing acceptance status. [Revision 12](../history/revision-12/agent_playbook_execution_decision_board.md) preserves that record unchanged.

| Reference | Useful lesson | Boundary |
|---|---|---|
| Vercel AI SDK harnesses | Separate agent runtime from application-facing streams | Do not adopt the full TypeScript framework or presume experimental API stability. |
| Triad Labs Harness SDK | Adapter ownership, capability differences, permission-response translation and common contract tests | No automatic adoption of persistent sessions, queues, replay or the full event catalogue. |
| UnifiedAgentWrapper | Python organization and explicit message-to-event/result mapping | Preserve missing/unknown evidence; do not equate similarly named permission policies. |
| InHarness agent-adapters | Shared events and explicit native/synthesized capability differences | SDK-specific timing limits are not universal Codex limitations. |
| AgentDock | Adapter boundary and separate UI consumption | Historical license finding in the board requires rechecking before any reuse; design reference only. |

The [earlier repository exploration](../../../explorations/agent-execution/README.md) and [architecture notes](../../../explorations/agent-execution/architecture-notes.md) preserve broader alternatives: Protocol/iterator handles, more fields, controls, roles and helper modules. The active discussion subsequently chose the three ABCs and callback. Do not reintroduce all exploratory files because they appear in Atlas.

The research was source/document inspection, not live feature-parity testing. This PR preserves that research; it does not reverify every upstream claim. Before native implementation, select exact SDK/runtime versions, inspect actual types/fixtures, check reuse licensing when applicable and run provider-specific acceptance. No native SDK/version has been selected.

The fake should learn from this evidence while remaining small. A deterministic mapper test establishes local contract behavior only. Permission enforcement, cancellation and native timing require later native evidence.
