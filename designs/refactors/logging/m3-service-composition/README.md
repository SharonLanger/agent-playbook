# Logging M3 — independent service composition

Behavioral design approved by Sharon on 2026-11-18 at `c516c94926af0355e387b3bbb92ac5d6118e7390`. Current package is a **design-completion proposal**, not an implementation or live verification claim.

## Reading order

1. [Design and approval record](design.md)
2. [Acceptance cases](test-cases.md)
3. [Implementation plan and design-completion gate](implementation-plan.md)

Base: main `cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4`, after merged Logging M1 and M2. Design workspace: [PR #51](https://github.com/SharonLanger/agent-playbook/pull/51), draft/open. Broad ACT rename: [issue #56](https://github.com/SharonLanger/agent-playbook/issues/56), excluded. M3 names only Docker components act-logs and act-langfuse.

## Current status

| Item | State |
|---|---|
| User-facing behavior | Approved |
| Compose ownership / configuration bridge / credential and volume migration details | Concrete proposal written; independent review and Sharon's approval pending |
| Test cases and implementation plan | Drafted to operationalize approved behavior; review with completed technical design |
| Runtime implementation and acceptance | Not started / NOT RUN |
| M2 LG-10 live acceptance | NOT RUN; must close before finalizing logging design PR #51 |

Keep the separate M3 PR draft/open. Do not merge it or PR #51. No source/package/CLI/path rename is part of this milestone.

## Scope and documentation assessment

Low code: reuse Docker Compose, current configuration/secret parsing, setup code and per-component checks. No new service manager framework, logging broker, collector or secret store. Public configuration/setup docs will change when behavior ships; this preparation PR adds design documents only. Existing Atlas input/status semantics are unchanged by this preparation package; integrate M3 discovery and regenerate Atlas when the completed design is returned. Do not classify it as implemented.

The general process is [stage/milestone workflow](../../../governance/stage-milestone-workflow.md) and [Codex handover rules](../../../governance/codex-handover-rules.md). This package owns M3 detail; the separate design PR owns shared logging history.
