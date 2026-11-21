# S03.M1 — Eight standalone CrewAI recipes

## Authority and objective

Sharon approved all eight visual walkthroughs and their explanations on 2026-11-15, then explicitly requested this design/test/implementation package for another Codex agent. Approval quote: “I agree with everything. We can go ... just write the explanations of everything, requirement ... maximum three rounds.” He also required the same diagram at the start of each README, official links at the end, and temporary tests retained for his own use before deletion before merge.

This package translates that approval into a concrete batch. The outgoing handoff pins its exact commit; forwarding that handoff authorizes that revision. No implementation or native-framework verification was performed by the design session. Do not claim unobserved failure/cancellation semantics.

Build all eight recipes together; one implementation PR targets main. Use Python 3.13, CrewAI 1.15.40 and existing dependency pins. Inspect current main for drift; do not upgrade dependencies.

## Placement and hard boundaries

- New runtime/example/verification Python code exists ONLY in each recipe's folder under app/examples/workflows/recipes/.
- No application imports, registry entries, app/application.yaml use, agent SDKs, logging/Langfuse setup, shared execution context, global helper framework or new dependency.
- Shared index Markdown and design/review records may change. Diagram SVG/HTML assets belong beside their owning recipe. “Four files” means four core files, not a prohibition on requested diagrams or temporary verification.
- Move the existing eight ex_01...ex_08 folders into concepts/ without rewriting their behavior. Preserve their existing tests, notices, inputs and history. Fix path/link depth only where required. Do not refactor their Python code.
- Create/update concepts/README.md, recipes/README.md and workflows/README.md navigation. Path-only documentation/Atlas reference repairs caused by the approved move are permitted; identify every affected file. No unrelated guarded meaning change is authorized.
- Application checks, release inputs and official workflow registrations remain independent of examples. Never add examples to app/tests, default gates or the wheel.
- No logging work, real agents, retries/fallback, recovery framework, first-winner race, arbitrary dynamic worker pool or production guarantees.

The parent README owns requirements R01–R12 and the coverage map. This design adds B01–B09 below. If an inherited global summary implies integrated traces or permanent recipe tests, the explicit user instructions control this batch; record that reconciliation rather than implementing the superseded scope.

## Shared recipe contract

| ID | Requirement |
|---|---|
| B01 | Each folder contains README.md, flow.py, run.py and input.json, plus self-contained diagram assets. |
| B02 | run.py runs directly in PyCharm or with the project interpreter from any working directory; resolve inputs beside the file. Copying the folder elsewhere works with the same installed dependencies. No sibling/application imports. |
| B03 | README begins with the recipe title then the approved diagram immediately below, before narrative. Follow with use case, keywords, run instructions, default outcome, short wiring walkthrough, 1–3 edits to try, limitations/copy notes. End with relevant official documentation links. |
| B04 | Preserve the exact approved topology, branch labels and meaning in ../diagrams/approved-preview.html. Implement separate self-contained SVGs and static fallback, following designs/diagrams/AUTHORING.md. Keep readable sizing and layout; do not substitute a Mermaid code block or framework-generated hairball. Flow.plot can be optional, not the accepted diagram. |
| B05 | Use simple typed local state, async operations where demonstrating concurrency, native Flow decorators/routing, and small deterministic Python calculations. Native scheduling/joins must do the orchestration; do not replace the recipe with asyncio.gather or a custom scheduler hidden inside one node. |
| B06 | Print human-readable execution steps and a JSON-serializable final result/state. No custom application logger. Include enough state/order markers to inspect branch outputs, route, loop count and selected failure outcome. Keep terminal output useful without relying on unstable framework banners. |
| B07 | Avoid cloud calls and model keys. Apply existing supported CrewAI telemetry/tracing disable settings before CrewAI imports in standalone entries and verification. No network-sandbox guarantee; use documented switches and deterministic work. |
| B08 | Temporary verify.py per recipe runs independently and exits nonzero on failed assertions. It is committed/pushed for review and Sharon's use, outside application gates. Retain until Sharon has used it and final review reaches cleanup. Delete before implementation merge; retain immutable pre-cleanup evidence. |
| B09 | Published diagrams are explanations, not execution evidence. Mark Python selection/counting policies distinctly from native CrewAI wiring. Identify the actual tested version and observed limitations. |

Settings needed for a small standalone entry stay local. Do not introduce a central setup module. Prefer the four-file pattern; if a local extra support file is truly necessary, justify it in the report. Validate only the small input domain needed by each example, without building a configuration framework.

## Recipes and concrete behavior

C01–C08 map one-to-one to recipe_01...recipe_08 below. Stable test IDs live in test-cases.md. Concrete example values/tie rules are mechanical completions of the approved walkthrough, not claims that the framework supplies those policies.

### C01 — recipe_01_parallel_results

Input numbers default [2,4,6]. After input, two async branches compute sum and maximum; an all-required join reads both owned results and returns {sum:12,max:6}. A single terminal report runs once, only after both results are available. Keep branch results in separate state fields; don't assume a join argument automatically contains every result.

Use small editable branch delays to make overlap visible. Reverse completion order without changing the report. Teach parallel work, and-style joining, state and aggregation. Nonempty numeric input only.

### C02 — recipe_02_select_result

Two async branches produce candidates A/70 and B/90. Wait for BOTH, then return B/90 as the highest score. Input controls the two scores and branch delays. On a tie choose A deterministically and explain that small Python policy.

This is best-after-all, not first-to-finish or speculative execution. Both candidates run, neither is cancelled, and order cannot change the selected winner. Teach result selection after a native join.

### C03 — recipe_03_conditional_parallel

Input numbers [2,4,6] and mode basic/detailed. Route FIRST. Basic computes sum only. Detailed starts sum and maximum concurrently and joins them. Both paths converge exactly once into a report with the same keys: {mode,sum,max}, using null for max in basic mode.

Never wire a common all-required join to a node absent from the basic path. Teach route labels, chosen-path execution and convergence. Expected basic: sum12/max null; detailed: sum12/max6.

### C04 — recipe_04_conditional_followup

Compute sum first, then compare it to an input threshold default 10. If sum > threshold, start minimum and maximum concurrently, join, and return an expanded report. Otherwise return sum only. Common output keys {sum,min,max}; absent extra values are null.

Default [2,4,6] yields {sum:12,min:2,max:6}. At or below threshold, extra nodes do not run. This differs from C03: an actual calculation result selects the path rather than an input mode.

### C05 — recipe_05_parallel_failure

Start async branches A and B. A deliberately raises a recognizable ValueError when input fail_a is true (default); B performs simple delayed work. Successful variant fail_a=false joins both and returns a combined outcome.

In the failed variant, the overall call fails honestly and the direct process exits nonzero; no success report or successful all-required join is claimed. Preserve the exception/cause. Record whether B started/completed/cancelled when the native execution unwinds. Inspect both A-fails-before-B-finishes and B-finishes-before-A-fails. No forced cancellation or recovery mechanism may be added to manufacture an assumed framework outcome.

The approved diagram intentionally says sibling outcome “To verify.” Replace that annotation with a concise observed-version note only after verification, preserving topology and failure meaning. If the pinned framework cannot deliver the core fail-caller behavior without materially new control logic, stop and report the conflict; do not silently change design.

### C06 — recipe_06_failure_threshold

Five FIXED independent async checks produce named outcomes. input.json selects which check IDs fail and a failure_threshold default 3. Local expected check errors are captured as explicit failure outcomes; unrelated errors are not swallowed. Wait for all five, count failures, THEN evaluate failures >= threshold.

Below threshold, return all five outcomes, successes and recorded failures, without describing every check as successful. At/above threshold, retain the summary and raise a clear aggregate failure so run.py exits nonzero. Suggested default failed checks [A,B], demonstrating a tolerated two-failure result; editing to [A,B,C] demonstrates overall failure.

No early termination or cancellation. Threshold/counting is ordinary Python policy, not a claimed built-in CrewAI quorum feature. Keep separate named branches and native completion/join wiring visible.

### C07 — recipe_07_fixed_loop

Input iterations defaults to 3; support bounded positive values 1–10. Initialize counter0. Native routing triggers a work step, increments once, then routes back while counter < iterations. Return count and ordered per-iteration values. Default has exactly three work executions.

This must demonstrate a flow-level backward transition, not a Python for loop doing all work inside a single node. Use distinct method names and route-label namespaces. No fourth iteration or duplicate terminal report.

### C08 — recipe_08_revision_loop

No real coder/reviewer agents. Input accept_on_attempt defaults to 3 and max_attempts to 4, each 1–10; accept_on_attempt may exceed max_attempts to exercise exhaustion. Fake coder increments attempt and produces a simple revision value; fake reviewer decides accept if attempt >= accept_on_attempt. If accepted, finish. Otherwise check maximum: route back to coder if below maximum, else return an explicit limit_reached result.

Default: coder1/reviewer1, coder2/reviewer2, coder3/reviewer3, accepted. Exhaustion: accept_on_attempt5/max_attempts2 gives exactly two coder/reviewer pairs and limit_reached, not accepted. Acceptance on the final allowed attempt wins. limit_reached is a normal explicit business outcome, not an unhandled framework exception. Teach feedback, result-based routing and a hard bound.

## README and diagram delivery

The approved eight-diagram reference is retained at ../diagrams/approved-preview.html, with provenance in ../diagrams/README.md. Its selector order maps exactly to C01–C08. Export/recreate each as a portable diagram beside its recipe; keep branches, decision labels, displayed example values and meaning. Minor responsive spacing or wording needed for verified method names is allowed; no flow redesign.

Recommended final assets: diagram.svg (self-contained animation with reduced-motion behavior) and diagram-static.svg, with an optional tiny local viewer if needed. All assets must travel with a copied recipe. Render and inspect; follow the mandated authoring checker when using Dashmotion. Do not claim that rendering proves runtime behavior.

Official footer sources:
- https://github.com/crewAIInc/crewAI/blob/main/docs/v1.15.40/en/concepts/flows.mdx — repository's version-matched Flow guide. Select relevant headings after checking anchors.
- https://github.com/crewAIInc/skills/blob/main/skills/build-flow/references/routing-patterns.md — official routing examples, especially loops/nested joins; guidance may differ by version.
- https://docs.crewai.com/en/concepts/flows — current guide (resolved to v1.15.41 on 2026-11-15), supplementary rather than evidence for our pin.

Use 1–3 relevant links per README, explain the topic briefly, and retain notices for copied upstream material. Do not present current online documentation as proof of 1.15.40 failure semantics.

## Scope, documentation and acceptance

This is one milestone S03.M1 and one implementation PR. The approved eight-diagram/menu discussion supplies behavior; the focused tests record verification rather than expanding the product.

No blanket guarded changes. Path-only repairs resulting from concepts/ relocation are authorized by the folder agreement; enumerate them before applying. Other discovered conflicts are reported. The originating design session owns global Stage 03 roadmap/progress/Atlas semantic reconciliation and stage closeout; implementation reports may add pending changes rather than editing frozen design contracts.

Completion requires: eight runnable/copyable examples; faithful diagrams at README tops; footer sources; temporary checks available to Sharon; both independent reviews; truthful verification and final-review handoff. Implementation remains unmerged for Sharon/design-session review. Tests are removed in a subsequent, explicitly identified cleanup after hands-on acceptance; merge remains separately authorized.
