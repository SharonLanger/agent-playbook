# Happy-path mock workflow exercise

Status: **DRAFT TEST/SCRIPT CONTRACT — nothing below is implemented yet.**
[Review entry point](README.md) · [Architecture/configuration](architecture.md)

## Proposed entry point

A maintained script under `app/tooling/observability/`, callable from the terminal
and a PyCharm run configuration. A candidate invocation is:

```text
# Proposed command; not available in the repository today.
python app/tooling/observability/seed_langfuse.py --config /path/to/smoke.yaml --runs 3
```

It loads the same validated configuration and uses the same observability adapter
that the future workflow context will receive. Reuse the merged context contract
where applicable; do not make a second workflow/context framework for the script.
It must not import personal examples or require a model/provider key.

## What the script sends

Use fresh run and trace identities on every invocation. Share a unique
`fixture_batch_id` across that command's runs for retrieval. Label every observation
with synthetic provenance such as `source=mock`, `fixture=langfuse-smoke` and
`workflow_id=mock-wf-02`. Do not label a simulated run as an actual CrewAI execution.

Each root is named `mock-wf-02` and has four sequential children:

| Observation | Recorded evidence |
|---|---|
| initialize | Initial value |
| add | Value and increment as input; computed sum as output |
| multiply | Sum and multiplier as input; product as output |
| finish | Final output |

The script performs deterministic Python arithmetic and measures actual local
execution timestamps; no LLM or real agent is invoked. First-run input is
`initial=3, increment=2, multiplier=4`, giving history `[3, 5, 20]` and output
`20`. Additional runs may use different explicit fixture inputs. The console
prints each run ID, trace ID, final value and trace URL.

Any optional slow-demo delay must be explicit and default to zero; never fabricate
timings, token usage, provider names or costs. The first acceptance scenario is
successful execution. A clearly labelled simulated failing step can follow later;
it is not required to establish the initial happy path.

## Happy path from setup to UI

1. Resolve and record compatible pinned images/SDK dependencies.
2. Start the local stack using the maintained Compose setup.
3. Open the UI, create an account/project and obtain project API keys.
   Manual initial setup is sufficient; headless provisioning is optional later.
4. Supply keys through the documented external configuration and environment.
5. Run the explicit smoke command; authenticate, then emit the mock batch.
6. Flush and poll the public read API by the emitted trace IDs until all expected
   roots and children are present, with a bounded deadline (proposed: 30 seconds).
7. Verify IDs, hierarchy, input/output and expected final values; print trace URLs
   only as successful verification after read-back passes.
8. In the UI inspect the root and four children, their inputs/outputs/durations
   and the synthetic/run metadata. Document the exact filtering controls present
   in the pinned UI rather than promising arbitrary custom-field filters.
9. Stop/start containers without removing volumes; retrieve one previously emitted
   trace again. It must still exist.

Use the selected server version's supported read endpoints/SDK methods. Read-back
must verify the child observations as well as a root record. A healthy web page,
successful auth or SDK flush alone does not satisfy the test. If the deadline
expires, report unverified/missing trace IDs and exit nonzero without exposing keys.
A rerun creates a new labelled batch; it never deletes older traces.

## Verification split

| Check | What proves success |
|---|---|
| Offline settings tests | Enabled settings require a valid endpoint/key references; disabled mode needs no keys/network; errors redact values |
| Offline observation contract | Correct parent relationships and per-run isolation; only allowlisted metadata is exported |
| Opt-in live smoke | API read-back confirms expected roots, children and values within the deadline |
| UI learning check | Sharon can open a returned URL and inspect nesting and evidence |
| Persistence check | Earlier trace remains queryable after restart with volumes preserved |
| Existing application gate | Strict types/lint/tests remain green and independent of Langfuse availability |

The offline gate uses independent test fixtures and a recording/no-export
implementation. It never starts Docker or depends on the personal sandbox.
The live smoke is an explicit integration check, not part of every `check`.

## Sequence and review gates

1. **Now:** review this draft and its workflow-refactor dependency.
2. **After workflow refactor merges:** reconcile context ownership, constructor and
   lifecycle names; identify any guarded logical changes and get their approval.
3. **After stage design approval:** implement local deployment/configuration,
   the narrow adapter and the explicit mock script.
4. Run offline checks, then the live smoke and persistence probe; record actual
   versions, commit, results and limitations.
5. Add official installation/configuration/troubleshooting guidance and the script's
   PyCharm task with implementation. Then review the UI together.
6. Only afterward design real workflow instrumentation and ordinary-log storage.

No environment has been provisioned, no project keys have been created and no
live trace has been exported as part of this draft documentation PR.

