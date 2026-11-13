# Workflow contract design

Status: **Proposed implementation contract reflecting the agreed scope. Awaiting final document review and implementation authorization.**

## Ownership

| Component | Owns | Does not own |
|---|---|---|
| Assembly | Load application settings; apply CrewAI startup settings before framework imports | Workflow business rules |
| Registry | Stable implementation key to class reference | Configured workflow IDs, instances or plugin loading |
| Factory | Resolve selected YAML entry, validate its settings and construct a fresh compatible wrapper | Executing steps |
| Runner | JSON decoding; lifecycle calls in order; result and error boundary | Concrete flow types, workflow-ID branches |
| Workflow ABC | Shared public methods, transitions, read-only status/failure, validated-result access | CrewAI scheduling or persistence |
| Concrete wrapper | Workflow configuration/input/output rules; create its flow; call kickoff; serialize its result | Shared lifecycle bookkeeping |
| CrewAI flow | Decorators, step execution, routing and business state | CLI formatting |
| CLI | Arguments, output text and exit status | Workflow-specific schemas |

Preserve the existing assembly/factory/runner and release discovery/launcher split. Domain work that may eventually require recovery stays in CrewAI steps. Constructors and preparation validate configuration/input and construct objects; they do not run business steps.

## Class contract and typed result

Use `Workflow[OutputT_co]`, an ABC with a covariant result type. Every public lifecycle method is implemented once in the ABC and marked `@final`. Pyright enforces the override restriction statically; Python does not enforce `@final` at runtime. The underscore hook convention is not an access-control boundary.

| Public method called by runner | Required subclass hook | Contract |
|---|---|---|
| `prepare(data: Mapping[str, object]) -> None` | `_prepare(data: Mapping[str, object]) -> None` | Validate workflow input, construct fresh CrewAI flow |
| `execute() -> object` | `_execute() -> object` | Invoke kickoff and return raw output |
| `validate_output(output: object) -> OutputT_co` | `_validate_output(output: object) -> OutputT_co` | Validate/convert raw output, store and return typed result |
| `serialize_output() -> str` | `_serialize_output() -> str` | Read the stored validated result and produce CLI presentation |

All four hooks are abstract. Even an empty-input workflow explicitly checks that no fields were supplied. There is no default validation that silently succeeds.

The base provides read-only `status: WorkflowStatus`, `failure: WorkflowFailure | None` and `result: OutputT_co`. Reading result before successful validation raises an order error. Preserve valid `None` results using a distinct absence representation, such as an optional one-element tuple. After serialization failure the validated result may remain available, but the attempt is failed.

**Serialization refinement:** no output argument is passed to the serializer. It consumes the result already validated and stored by the same instance. This avoids accepting a replacement unvalidated value and keeps the generic result covariant: the public contract only produces OutputT_co; it does not accept it as an argument. The subclass serializes its typed `self.result`.

Proposed immutable result boundary:

`RunResult[OutputT_co](workflow_id: str, output: OutputT_co, serialized_output: str)`

A known `Workflow[ReviewResult]` exposes ReviewResult, including nested objects. The dynamic registry uses `Mapping[str, type[Workflow[object]]]`; the dynamic runner returns `RunResult[object]`. The actual object remains intact. The CLI prints serialized_output. No Any, unchecked casts, workflow unions or hardcoded string/integer restriction may hide this boundary. Pyright strict must prove the generic registry and a rich-result example before migration proceeds.

Constructors have a common keyword-only shape: `settings: CrewAISettings` and `config: Mapping[str, object]`. Subclasses that define a constructor call the base constructor and preserve that signature. The base initializes lifecycle state. Each implementation validates its own configuration into a strict typed model; the factory does not know those models. ABC inheritance alone does not prove constructor compatibility: registry construction tests instantiate every registered class with valid settings.

## Lifecycle

Define a shared WorkflowStatus enum. Each instance owns _status, initialized by the base constructor to CREATED. No global mutable instance or shared status is registered.

| Method | Required status | Before hook | After successful hook |
|---|---|---|---|
| prepare | CREATED | PREPARING | PREPARED |
| execute | PREPARED | EXECUTING | EXECUTED |
| validate_output | EXECUTED | VALIDATING_OUTPUT | OUTPUT_VALIDATED |
| serialize_output | OUTPUT_VALIDATED | SERIALIZING | COMPLETED |

FAILED is the terminal failure status for an ordinary exception raised during any hook. EXECUTED means kickoff returned; it does not mean the application has a valid presentable result. COMPLETED means validation and serialization also succeeded.

The shared method checks the precondition, sets the in-progress status, calls its hook, then records success or failure. An invalid-order call raises WorkflowOrderError before mutation or hook invocation. It leaves the existing status and failure record intact. Successful completed and failed instances cannot be restarted or reset in this version. A new explicit attempt gets a new instance; no automatic retry occurs.

The status is an in-memory wrapper lifecycle, not a durable record of which CrewAI step completed. It does not drive steps or resume a flow. Concurrent calls on the same instance are unsupported; enum checks are not thread synchronization. Re-entry after a transition to an in-progress status is rejected.

Catch Exception for normal lifecycle failure bookkeeping and re-raise with the original cause preserved. Preserve existing interruption semantics: KeyboardInterrupt, SystemExit and other BaseException interruptions propagate unchanged rather than becoming application failures. No persisted terminal status is promised after interruption/process death; discard that interrupted instance.

## Runner sequence and import order

1. Load and validate shared application configuration, including its raw workflows mapping.
2. Apply CrewAI startup settings before importing concrete framework/flow modules, then obtain the class registry.
3. Resolve the requested ID and validate only its selected entry. Reject missing/disabled entries and unknown implementation keys before steps run.
4. Construct the selected wrapper from the class registry and selected configuration.
5. Decode absent input as an empty object; otherwise require a JSON object.
6. Call prepare, execute, validate_output, then serialize_output in order.
7. Return immutable RunResult containing the validated object and serialized text.

Assembly may be arranged internally to return both application and CrewAI settings without loading twice. No public runner call may import concrete flows before configuration has been applied. Build the class registry lazily after assembly; wrapper modules defer CrewAI flow imports until needed. Unknown unused implementation strings do not trigger imports or validation.

The ordering changes the old unknown-ID-before-configuration behavior deliberately: shared configuration must be readable before configured IDs can be resolved. Replace that obsolete assertion with tests for the new sequence.

## YAML selection and configuration

Example target application configuration (the integrations block remains unchanged):

```yaml
workflows:
  wf-01:
    name: Step sequence
    implementation: step_sequence
  wf-02:
    name: Shared state
    implementation: shared_state
  wf-02-custom:
    name: Shared state with custom defaults
    implementation: shared_state
    config:
      defaults:
        initial: 10
        increment: -2
        multiplier: 3
  wf-03:
    name: Conditional route
    implementation: conditional_route
```

Python registration uses actual references: `{"shared_state": SharedStateWorkflow, ...}`. Renaming a class or moving its package changes Python references/imports. YAML changes only if the stable implementation key changes.

The proposed common entry fields are implementation (required nonempty string), name (optional nonempty string, otherwise display the ID), enabled (strict bool, default true), and config (mapping, default empty). Unknown entry fields fail when that entry is selected. Workflow IDs and implementation keys must be nonempty strings without surrounding whitespace; reject rather than silently normalize.

| Case | Defined behavior |
|---|---|
| Missing root workflows | Configuration error; no implicit legacy registry fallback |
| `workflows: {}` | Valid empty catalog; selecting any ID fails clearly |
| Null/list/scalar workflows | Shared configuration error |
| Missing selected workflow ID | Selection error before workflow steps |
| Null/list/scalar selected entry | Selected-entry configuration error |
| Missing config or `config: {}` | Implementation defaults |
| Null/list/scalar config | Selected configuration error |
| Disabled selected entry | Selection error, no kickoff |
| Unknown selected implementation | Configuration error, no kickoff |
| Invalid or unknown unused entry | Retain raw entry without resolving/constructing it; unrelated valid workflow remains runnable |
| Unknown shared top-level/integration fields | Shared configuration error |
| Unknown selected implementation settings/input fields | Reject strictly, report field/type without values |
| Duplicate YAML keys at any depth | Reject that YAML file before merging, even in an unused block |
| Unsafe YAML tags or YAML merge keys (`<<`) | Reject; local-overlay merging is the supported merge mechanism |

Use a SafeLoader-derived duplicate-key check without global loader mutation. Reject malformed/non-string mapping keys. Preserve path selection, local sibling overlay, documented environment overrides, per-run reload and redacted configuration errors.

Base and local YAML are parsed independently, then merged using the existing recursive map overlay. A local empty map is a no-op; it does not erase inherited entries/settings. Set enabled false to disable an inherited entry. Invalid explicit null is not treated as missing. Existing CrewAI environment overrides remain unchanged; do not invent workflow environment-variable conventions.

For initial workflow-specific configuration, use strict defaults models for WF-02 arithmetic fields and WF-03 score. Missing fields retain existing defaults. Valid runtime JSON fields override configured defaults; invalid runtime values fail instead of falling back. Validate configured defaults before merging input, so an invalid default cannot be hidden by a request override. WF-01 permits only an empty implementation configuration. WF-03's pass threshold remains its existing constant; no new configurable routing rule.

YAML selects supported Python behavior; it does not introduce methods or arbitrary executable code. Two configured aliases do not constitute a child/composite workflow.

## Errors and failure ownership

Keep a small error vocabulary: existing ConfigurationError; WorkflowInputError; WorkflowExecutionError; and WorkflowOrderError. Place shared workflow errors and WorkflowPhase with the workflow contract to avoid concrete workflows importing the application runner. Re-export old error imports temporarily only if useful for keeping tests readable; old installed-release compatibility is not required.

WorkflowPhase identifies PREPARE, EXECUTE, VALIDATE_OUTPUT or SERIALIZE_OUTPUT for lifecycle failures. Configuration, selection, decoding and construction failures are reported at their corresponding outer boundaries and may occur before a wrapper exists.

WorkflowFailure records the failing lifecycle phase and original exception for in-process inspection. Do not turn exception objects, raw request data or configuration values into telemetry payloads. The outward exception retains `__cause__`; safe messages name the phase, workflow and relevant field/type without echoing private values.

| Failure | Ownership and classification | CLI exit |
|---|---|---|
| Shared/selected configuration, missing implementation | Configuration boundary; no steps | 2 |
| Unknown/disabled configured ID | Selection boundary; no steps | 2 |
| Invalid JSON or explicit workflow input rejection | Input boundary; no steps | 2 |
| Unexpected constructor/setup defect | Construction/preparation execution failure | 1 |
| CrewAI kickoff/step exception | EXECUTE failure; downstream work does not run | 1 |
| Malformed final output | VALIDATE_OUTPUT failure; serializer not called | 1 |
| Serialization defect | SERIALIZE_OUTPUT failure; no success result | 1 |
| Wrong method order | WorkflowOrderError; no hook/state mutation; programming error | 1 |
| Valid needs_work decision | Successful business result | 0 |

Within _prepare, translate only input-schema errors into WorkflowInputError. Do not classify every ValueError or Pydantic ValidationError as bad user input: state/flow-construction defects are execution failures. During _execute, every ordinary exception is an execution failure even if it happens to be named WorkflowInputError. Translate at phase boundaries, not through one broad try/except covering the entire run.

Error wrapping must preserve the causal chain once per boundary, not repeatedly wrap an already classified failure in identical exceptions. A successful RunResult is created only after all lifecycle methods succeed.

## Existing workflows and result examples

WF-01 retains empty input and `[Hello, workflow!]`. WF-02 retains strict arithmetic inputs, mutable history owned by its CrewAI state and native integer output. Its serializer returns decimal text. WF-03 retains strict score input, threshold 60, exclusive pass/needs_work branches and the same result text.

For example, WF-02 _prepare validates NumberInput (after configured defaults), constructs NumberState and SharedStateFlow; _execute calls kickoff; _validate_output validates a strict integer, rejecting bool; _serialize_output returns `str(self.result)`. All status transitions come from the ABC.

Future rich results may be Pydantic models or validated dataclasses with nested values. Each workflow defines its serialization; a rich model may use JSON. No generic JSON encoder, --json switch or forced serialization of arbitrary objects is part of this refactor.

## Future boundaries

Context/Langfuse immediately follows as a separate design and implementation. Child workflows, persisted recovery, retries, async lifecycle and concurrent instance reuse are deferred. Keep data needed to continue within typed CrewAI state and keep logger/client/connection objects in the later context. These constraints preserve options; they do not claim recovery is already implemented.

## Pattern references

- [Python ABCs](https://docs.python.org/3.13/library/abc.html): abstract hooks and concrete base methods.
- [Python final](https://docs.python.org/3.13/library/typing.html#typing.final): static override protection.
- [Python Future](https://docs.python.org/3.13/library/concurrent.futures.html#future-objects): running/completion distinctions and invalid-state operations.
- [Spring AbstractApplicationContext](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/AbstractApplicationContext.html): a familiar Java Template Method example.
- [CrewAI Flows](https://docs.crewai.com/en/concepts/flows) and [checkpointing](https://docs.crewai.com/en/concepts/checkpointing): future recovery must use verified pinned-version capabilities, not our wrapper status.

References motivate the pattern; the transitions and policy above are Agent Playbook design decisions, not copied framework guarantees.
