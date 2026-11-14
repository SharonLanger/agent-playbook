# Agent-playbook — Architecture Conversation Handover

**Prepared:** 2026-11-14  
**Purpose:** Give another agent in the Agent-playbook Project the complete *substantive context available to this assistant* from the architecture/refactor discussion, including reasoning, objections, proposed structures, code patterns, decisions, and unresolved questions.

> **Integrity notice:** This is a detailed reconstructed handover, **not a verbatim export** of the ChatGPT conversation. The assistant cannot retrieve a complete raw transcript through the tools available in this session. This file reflects the conversation visible in context and is not guaranteed to contain every utterance. Do not represent it as a word-for-word record. For a verbatim transcript, use ChatGPT Settings → Data Controls → Export Data and extract this conversation.

## How the receiving agent should use this document

1. Treat it as historical context, not an automatically approved implementation specification.
2. Distinguish **implemented**, **approved in discussion**, **proposed**, **challenged**, and **unresolved**.
3. Inspect the live GitHub repository and design documents before making changes. The handover cannot prove the current branch state.
4. Preserve the user's preference for constructive architectural pushback: identify unnecessary abstraction and portability assumptions, rather than simply agreeing.
5. The user wanted a subsequent agent to **organize future file/folder structure and create empty placeholder files**, but only after understanding the discussion. Confirm scope before changing guarded design documents or code.

## Project context and status at the time of discussion

- Project/repository: `SharonLanger/agent-playbook` on GitHub.
- Python application package: `app/src/agent_playbook/`.
- Existing workflow orchestration uses CrewAI. Three integrated example workflows: `wf_01_step_sequence`, `wf_02_shared_state`, `wf_03_conditional_route`.
- Longer-term ambition: reusable workflow runtime; agent roles (coder, reviewer, verifier); Claude Agent SDK and Codex backends; harness customization (tools, permissions, hooks, context, policies); observability, including Langfuse; deterministic validation; local releases.
- Existing design documents in `designs/` are guarded; stage-specific decisions should not be silently changed. The user requested the architectural proposal be documented and reviewed separately from future implementation.
- A prior assistant reported creating **draft PR #34**, https://github.com/SharonLanger/agent-playbook/pull/34, branch `refactor/runtime-structure-and-verification`, unmerged. The reported PR included the code refactor, a future-architecture Markdown proposal, review guide, and verification helper. Reported tests: 137 passing, typing/lint/format checks, CLI checks, clean bootstrap and isolated-release verification. **Verify this in GitHub rather than relying solely on the claim.**
- Reported proposal path in the PR: `designs/refactors/2026-11-12-runtime-structure/proposal.md`; review guide: `app/docs/refactor-review.md`; verification script: `app/tooling/verify_refactor.py`.

## 1. Initial problem: structure feels mixed and unclear

The user pointed to `releases/selection.py` and `application/runner.py`, asking for comparisons with mature agent projects (CrewAI, Langfuse, LangGraph, Prefect), multiple layout options, and a recommended refactor. The core distinction identified was **launching a previously installed application release** versus **executing a workflow inside an application**.

- `releases/selection.py` reportedly mixed release discovery, user-facing messages, environment setup, and process launch.
- `application/runner.py` performed workflow input validation, workflow selection/construction, kickoff, and result handling.
- Initial options explored: (1) one Python package grouped by responsibility; (2) explicit domain/application/infrastructure layering; (3) multiple installable packages. The preferred direction was one modular package, avoiding premature multi-package complexity.
- The user asked that recommendations reflect the **final target architecture**, not just the current small Stage 01 codebase.

## 2. Proposed application/release refactor

The preferred responsibility split became:

```text
app/
  application.yaml
  application.local.yaml       # optional ignored override
  src/
    agent_playbook/
      cli/
        parser.py             # CLI argument declaration
        commands.py           # dispatch, user-facing presentation
        development.py        # checkout-only developer commands bridge
      application/
        assembly.py           # config + integration wiring, prior to importing flows
        workflow_factory.py   # select and construct a fresh workflow
        workflow_runner.py    # validation, run lifecycle, kickoff, outcome
        results.py            # normalized application outcomes
      releases/
        discovery.py          # find/select completed local installations
        launcher.py           # launch the selected interpreter/process
      config/                 # Python config loading/validation code
      workflows/
        wf_01_step_sequence/
        wf_02_shared_state/
        wf_03_conditional_route/
  tooling/                    # development/build/check/release scripts
  tests/
  examples/
  docs/
  dist/                       # generated release artifacts, ignored
```

**Important reasoning:** `releases/` inside `src/agent_playbook/` contains *importable Python code that discovers and launches releases*, not release artifacts. `app/dist/` contains generated releases. `app/tooling/release.py` builds releases. These are distinct. One could instead move checkout-only release discovery/launch into `tooling/`, but simply moving the folder alongside `src/` would not create a coherent boundary. The assistant favored keeping it in the application package for now, noting that it may be shipped inside installed wheels even though installed releases do not themselves need release discovery.

**Configuration placement:** User challenged `app/configs/application.yaml` and preferred `app/application.yaml`. Assistant agreed: one shared YAML at the app root is sufficient; `app/application.local.yaml` may provide ignored local overrides; `app/src/agent_playbook/config/` remains Python code. A separate `configs/` directory becomes worthwhile only when multiple configuration files/profiles justify it. Migration should not silently ignore old local overrides.

## 3. Final target architecture: responsibility boundaries

The user wanted a future-oriented layout including reusable agent roles, execution backends, harness customization, custom tools, and observability. Proposed (not necessarily implemented) expansion:

```text
app/
  application.yaml
  application.local.yaml
  harnesses/                    # editable harness profiles/assets
  src/
    agent_playbook/
      cli/
        parser.py
        commands.py
        development.py
      application/
        assembly.py
        workflow_factory.py
        workflow_runner.py
        results.py
      releases/
        discovery.py
        launcher.py
      config/
      workflows/
        code_review/
          flow.py
          state.py
          steps/
            prepare.py
            implement.py
            review.py
            report.py
          context.py
          policies.py
          templates/
            report.md
        another_workflow/
          flow.py
          state.py
          steps.py
      agents/
        coder/
          agent.py
          models.py
          context.py
          validation.py
          event_handler.py
          prompts/
            instructions.md
        reviewer/
          agent.py
          models.py
          validation.py
          event_handler.py
          prompts/
            instructions.md
        verifier/                # future illustrative role
          ...
      execution/
        contracts.py            # provider-independent request/capabilities/results
        events.py               # normalized events
        harnesses/              # hooks, policy, permissions, context, capability wiring
        adapters/
          claude/
            executor.py
            event_mapper.py
          codex/
            executor.py
            event_mapper.py
      tools/                    # reusable callable tool implementations
      observability/
        adapters/
          langfuse/
  tooling/                      # developer/build tooling, not agent tools
  tests/
  examples/
  docs/
  dist/
```

This tree is **illustrative**, not a mandate to create every module now. The user explicitly appreciated the full expanded example because it made relationships visible; do not oversimplify the structure merely because the conceptual distinction was initially unclear. They prefer a **folder per agent role** with room for Python code, instructions, templates and future assets.

### Ownership rules

- **Workflow**: ordering, routing, state, retries, transitions, decision to call coder/reviewer/verifier; workflow-specific context and reporting. Keep workflow-specific helpers in its folder. Use descriptive filenames rather than a generic `utils.py` when possible. Extract shared logic only after genuine reuse.
- **Agent role (`agents/coder/`, `agents/reviewer/`, etc.)**: role-specific instructions, input preparation, expected output models, result validation, role-specific interpretation of events, and possibly Python scripts. **Not just Markdown prompts.** Role is not itself a separate LLM engine.
- **Execution adapter**: provider-specific SDK invocation, session management, native event/message translation, native hook/permission APIs, provider errors, cancellation and other provider-specific mechanics. The SDK's own agent loop is not reimplemented unnecessarily.
- **Harness**: runtime configuration and constraints (tools, hook policies, permissions, context, capability requirements); provider-specific application of those settings occurs in adapters.
- **Custom tools (`tools/`)**: reusable tool implementations and schemas. Distinguish tool *implementation* from role/harness *selection* of available tools.
- **Developer tooling (`app/tooling/`)**: build, setup, checks, release; not callable agent tools by default.
- **Application assembly**: connect configured workflows, role executors, harness policies and observability without turning the runner into a giant setup function.
- **Observability**: Langfuse adapter and provider-neutral event/trace information; role-specific semantic logs are different from low-level SDK execution logs.

## 4. Crucial discussion: callbacks and the Claude SDK agent loop

The user recalled the Claude Agent SDK pattern:

```python
async for message in query(prompt=..., options=...):
    # inspect message type, react to messages
    ...
```

They asked how coder and reviewer could supply different logic to run for each message, analogous to injecting an interface/virtual method. An initial example proposed `run_claude(..., on_message=handler)` and a coder-specific `CoderMessages.handle(message: ClaudeSDKMessage)`. The user identified the architectural flaw: **if the coder receives Claude-specific message types, it must understand Claude and will need separate Codex logic; the adapter adds little beyond wrapping `async for`.**

The assistant accepted this pushback. The corrected design:

```text
Claude SDK messages --> Claude adapter/event mapper --\
                                                 --> shared AgentEvent --> coder/reviewer/verifier handler
Codex native events --> Codex adapter/event mapper --/
```

An agent role's handler should normally consume **our event types**, not native Claude/Codex SDK messages. The adapter's value is substantive: native-to-common translation, lifecycle/session handling, request translation, capability enforcement, failures and controls.

Example shared handler signature (conceptual):

```python
async def on_event(self, event: AgentEvent) -> None:
    ...
```

This could be supplied as a callback or an object satisfying an interface/Protocol/ABC. The choice of injection mechanism is secondary to **not leaking provider types across the boundary**.

### Proposed normalized event vocabulary (exploratory)

- `AgentRequest`: task, instructions, required capabilities, execution limits.
- `TextProduced`: text with explicitly defined partial/complete semantics.
- `ActionCompleted`: action identity, outcome and available evidence.
- `ExecutionCompleted`: final result.
- `ExecutionFailed`: classified failure.
- Additional events can be added for genuinely reusable execution capabilities, such as `CommandCompleted` with command, exit code, stdout and stderr, **only where the provider can faithfully supply them**.

These names are **examples, not an approved schema**. Preserve distinctions between event observation and execution control: seeing a tool action in a stream does not automatically allow cancellation, approval or prevention. Permissions/interventions need separate supported SDK hooks or control APIs.

## 5. Major pushback: adding a verifier with extra requirements

The user asked: what happens when a new `verifier` agent needs extra data or events not needed by coder/reviewer? Would we need role-specific adapters or larger interfaces?

Three cases were distinguished:

1. **Role-specific final output** (verdict, checks performed, evidence, unresolved issues): belongs to verifier's output schema and validation. No provider event extension required if existing structured-result support suffices.
2. **Missing execution evidence** (e.g. command exit code, stdout/stderr): if providers expose it, extend shared events and both event mappers; verifier consumes the new event. This is a reusable capability, not automatically `ClaudeVerifierAdapter` and `CodexVerifierAdapter`.
3. **Provider cannot supply required evidence/control**: do not fabricate missing values or silently degrade. Declare optional evidence explicitly, or require a capability and reject incompatible providers **before execution**. An independent verification tool controlled by the application may be more authoritative than interpreting an agent's claim that tests passed.

**Key design principle:** every adapter accepted for a role must meet that role's *required* execution capabilities, but a single interface cannot magically make all native Claude features exist in Codex. Avoid asserting complete feature parity. Capability-based extensions are preferable to role-named adapter subclasses. Native-only extensions are permissible when portability is explicitly abandoned and documented.

**Open architectural work:** decide which normalized events, capability requirements, hook/control operations and evidence semantics actually matter; define contract tests that exercise both adapters; specify unsupported-capability behavior. No final event schema or cross-provider guarantees were approved in this conversation.

## 6. Logging, hooks and role-specific behavior

The user asked how a coder and reviewer could log different things even though both use the Claude SDK loop.

- Common execution events (session start, tool invocation, provider error, completion) should be handled consistently at the execution/observability boundary.
- Coder-specific semantic logging (files modified, test results) and reviewer-specific semantic logging (findings, severity, verdict) belongs to role interpretation of normalized events and results.
- When role-specific behavior must affect execution **during** a tool call, use explicit supported permission callbacks/hook policies, not merely a passive event handler.
- Avoid scattering `if role == "reviewer"` branches throughout the Claude adapter.
- If normalized events cannot express a required native feature, evaluate a capability extension or documented provider-specific escape hatch rather than leaking all native SDK messages into every role.

## 7. Python interface side question

The user asked if Python supports Java-like interfaces with two required methods and two default methods. Answer: yes, `abc.ABC` plus `@abstractmethod` for required methods, ordinary concrete base methods for inherited defaults, and `typing.override` for explicit overrides. Pyright statically checks abstract-class instantiation and override types; Python prevents instantiating classes with unimplemented abstract methods. `Protocol` is an alternative for structural typing without explicit inheritance. For required methods plus inherited default behavior, ABC is the direct fit.

Conceptual example:

```python
from abc import ABC, abstractmethod
from typing import override

class AgentAdapter(ABC):
    @abstractmethod
    def run(self, task: str) -> str: ...

    @abstractmethod
    def cancel(self) -> None: ...

    def name(self) -> str:
        return type(self).__name__

    def close(self) -> None:
        pass

class ClaudeAdapter(AgentAdapter):
    @override
    def run(self, task: str) -> str:
        return task

    @override
    def cancel(self) -> None:
        pass
```

This Python discussion did **not** settle whether the final execution contract should use ABC, Protocol, composition or callback interfaces.

## 8. External references suggested for studying existing normalization layers

The assistant identified these as relevant architecture references; the user had **not yet read or approved** any approach based on them:

1. Vercel AI SDK harnesses: https://vercel.com/changelog/program-agent-harnesses-with-ai-sdk ; https://github.com/vercel/ai/blob/main/content/docs/03-ai-sdk-harnesses/01-overview.mdx — shared harness abstraction and normalized streams for different agent runtimes; experimental status noted.
2. Triad Labs Harness SDK: https://github.com/Triad-Labs-Inc/harness-sdk ; https://github.com/Triad-Labs-Inc/harness-sdk/blob/main/docs/provider-adapters.md — adapter design, events, permissions, capability differences and common tests.
3. UnifiedAgentWrapper (Python): https://github.com/PentestGPT-Project/UnifedAgentWrapper — Claude query/Codex app-server event normalization and results.
4. InHarness agent-adapters: https://www.npmjs.com/package/@inharness-ai/agent-adapters — `AsyncIterable<UnifiedEvent>`, native versus synthesized events.
5. AgentDock adapter architecture: https://docs.agdc.dev/developer/agent-adapters — launch configuration, event translation, interactions and stop/resume.

**Verification caveat:** These were discussed as references, not locally run or vetted production dependencies. Recheck availability, license, maturity, source code, SDK versions and actual capability coverage before adopting anything.

## 9. Architecture/design preferences established by the user

- Wants thorough **folder/file trees** with nested modules to understand relationships; does not want the architecture artificially dumbed down.
- Wants strong, evidence-based **pushback**, especially about overengineering, interface leakage and false portability guarantees.
- Wants one modular project unless a compelling need for multiple installable packages appears.
- Prefers **one shared `app/application.yaml`**, with optional local override, over a `configs/` directory for one YAML.
- Likes separate subfolders for agent roles, expandable as roles become sophisticated.
- Prefers clear ownership: workflow versus role versus harness versus tool versus adapter versus observability.
- Wants decisions and open questions distinguished from exploratory proposals.
- In prior refactor task, explicitly requested a **draft PR without merging**, a future architecture Markdown document, and a temporary verification script that runs CLI/tests/build checks. The assistant reported doing this in PR #34.
- For this handover, user wants **one file** to attach to another agent inside the same ChatGPT Agent-playbook Project; no collection of separate files.

## 10. Remaining unresolved decisions and useful next steps

1. Confirm the actual contents/status of PR #34 and read current guarded designs.
2. Determine whether the receiving agent should create **empty future folders/files** in a separate draft PR, only a documentation tree, or something else. Avoid introducing empty implementation packages that suggest unsupported features are live.
3. Decide the first required cross-provider capabilities (event timing, tool lifecycle, usage, permission checks, cancellation, session controls, structured output, raw evidence).
4. Specify provider-neutral event types with semantic guarantees and explicit optional/unavailable fields.
5. Specify how role handlers subscribe to events and how active control/permission decisions are injected.
6. Decide which role-specific artifacts are prompts, Python logic, validation schemas, or callable tools.
7. Define shared adapter contract tests with provider fixtures and unsupported-capability cases.
8. Assess mature open-source normalization layers before committing to a fully custom one.
9. Keep observability's generic transport traces distinct from role-specific semantic results.
10. Preserve current workflow and release behavior and avoid modifying guarded stage-two implementation decisions without review.

## Suggested first prompt for the receiving agent

> Read this handover in full. It is a detailed reconstruction of the architecture conversation, not a verbatim export or an approved spec. Inspect the current Agent-playbook repository, its guarded design documents, and draft PR #34. First summarize (a) what exists, (b) what was proposed, (c) what remains unresolved, and (d) your recommended file/folder organization for the future agent/harness/adapter system. Do not implement or merge anything until I approve the scope. Challenge abstractions that do not earn their complexity, and do not assume Claude and Codex capabilities are identical.
