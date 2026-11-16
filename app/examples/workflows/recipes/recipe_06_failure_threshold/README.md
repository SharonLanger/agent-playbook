# 06 · Count failures before applying a threshold

![Count failures before applying a threshold](diagram.svg)

[Static fallback](diagram-static.svg) · [Local viewer with pause](diagram.html)

Tolerate a bounded number of expected check failures. Keywords: captured outcomes, all-required join, aggregate failure.

## Run

Use the existing project interpreter (`app/.venv/bin/python`, Python 3.13, CrewAI 1.15.40). Open this folder's **run.py** in PyCharm and click Run, or invoke:

```bash
/absolute/path/to/app/.venv/bin/python /absolute/path/to/recipe_06_failure_threshold/run.py
```

The entry resolves input/assets beside themselves and work from another working directory. Edit `input.json` for the small local scenario. `run.py` prints step markers, `STATE_JSON=...` and, on success, `RESULT_JSON=...`. 

## Wiring and default outcome

`begin` starts five visibly named async methods, `check_a` through `check_e`. Their local `check` helper captures only `ExpectedCheckFailure` as data; unrelated exceptions still escape. Native `and_` waits for all five and calls `summarize`. Ordinary Python counts failures, retains all outcomes, then compares count >= threshold. Default A/B failures and threshold 3 return status returned with failures 2 (not five successful checks). At/above threshold, the summary remains in state and a clear ValueError exits the process nonzero. No early termination occurs.

## Try

1. Set `failed_checks` to ["A","B","C"] to fail exactly at threshold 3.
2. Set threshold to 2 with A/B failures.
3. Compare no failures with all five failures.

## Limits and copying

Copy this whole folder, including input and diagrams, and use an interpreter with the same installed pins. It imports only standard library, installed CrewAI/Pydantic, and its own `flow.py`. No application CLI/YAML, registry, agents, model keys or cloud services are needed. The entries set `CREWAI_DISABLE_TELEMETRY=true` and `CREWAI_TRACING_ENABLED=false` before importing CrewAI. These supported switches are not an OS network sandbox; CrewAI may create its normal local storage on import/construction. In restricted execution environments its installed LanceDB dependency may need socket permission even for initialization.

Typed local state validates the small demonstrated domain; delays are seconds in 0–1, loop bounds (where present) are 1–10. Async overlap demonstrates cooperative concurrency, not CPU parallelism or a performance guarantee. Ordered markers are teaching state, not durable event history. These recipes add no retries, recovery or production guarantees.

The diagram preserves the approved walkthrough's topology and example labels. Motion illustrates connectivity, not a measured trace; exclusive decision paths are alternatives. Loop-back annotations name backward transitions. Dashmotion 2.2.4 layout at ae2fe4f generated the local viewer, with script-free portable animated/static SVG exports. [MIT notice](DIAGRAM-LICENSE.txt) is retained. Python selection/counting rules are local policy; native CrewAI decorators own scheduling and joins.

## Official sources

- [CrewAI 1.15.40 Flow guide](https://github.com/crewAIInc/crewAI/blob/main/docs/v1.15.40/en/concepts/flows.mdx): typed state, listeners, async methods and routing.
- [Official routing patterns](https://github.com/crewAIInc/skills/blob/main/skills/build-flow/references/routing-patterns.md): joins, route labels and bounded loops; guidance may differ by version.

