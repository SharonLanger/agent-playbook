# Replaceability, component Compose and setup requirements

Source: Sharon's follow-up in the logging design conversation, 2026-11-15.

- Docker services are now acceptable; the earlier objection to another required service no longer excludes them. Outage/data-loss policy is still undecided.
- One Compose definition per component (Langfuse, logging, later application) and one general Compose entry point referencing them is accepted direction.
- Golden rule: VictoriaLogs must be easily removable/replacable without rewriting workflow/agent logging. Langfuse's existing native integration remains the separate exception. A broker is not required merely for abstraction; verify replacement rather than assuming similarly named SDKs are interchangeable.
- Prefer low/no custom code and configuration of existing tools. Explain any necessary glue before committing to it.
- Record action items for splitting/aggregating Compose, clearer prerequisites/installation, version checks, component or all-services setup, and setup integration.
- Logging needs an agent-playbook logs command with action flags analogous to existing langfuse management, including checks proving the configured path works. Exact installer/aggregate command names are proposals.
- New selected tools must offer Apache-2.0; MIT-only is not acceptable. Structlog's Apache-2.0 OR MIT option is disclosed, not described as Apache-only. Exact artifacts and transitive notices still require review.
- Research VictoriaLogs examples, UI, delivery agent, built-in versus custom responsibilities and smallest integration. This authorizes research/document updates, not runtime implementation, stack selection or merge.

Alignment: new requirements supplement LOG-01–14 and supersede the no-service restriction. Existing guarded context/native tracing and Stage 02 completion remain unchanged. The concrete collector/backend choice remains proposed. Documentation research supports a collector-config replacement boundary; an actual replacement probe has not run.
