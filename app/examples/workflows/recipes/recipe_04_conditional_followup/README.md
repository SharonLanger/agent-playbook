# 04 · Decide after the first calculation

![Decide after the first calculation](diagram.svg)

[Static fallback](diagram-static.svg) · [Local viewer with pause](diagram.html)

Use a computed value to decide whether extra analysis is useful. Keywords: result-based routing, optional parallel follow-up.

## Run

Use the existing project interpreter (`app/.venv/bin/python`, Python 3.13, CrewAI 1.15.40). Open this folder's **run.py** in PyCharm and click Run, or invoke:

```bash
/absolute/path/to/app/.venv/bin/python /absolute/path/to/recipe_04_conditional_followup/run.py
/absolute/path/to/app/.venv/bin/python /absolute/path/to/recipe_04_conditional_followup/verify.py
```

Both entries resolve input/assets beside themselves and work from another working directory. Edit `input.json` for the small local scenario. `run.py` prints step markers, `STATE_JSON=...` and, on success, `RESULT_JSON=...`. Temporary `verify.py` checks defaults, variants, fresh-state isolation and direct/copied-folder entries. It remains for Sharon's hands-on review and will be deleted before merge.

## Wiring and default outcome

`calculate_sum` writes 12, then `choose_followup` compares it with threshold 10. The yes route runs `start_more`, async `find_minimum` / `find_maximum`, and their native `and_` join. The no route runs `keep_sum`. Chosen completion converges through native `or_` into `report`. Default is `{"sum":12,"min":2,"max":6}`. At or below threshold the min/max values are null and extra nodes do not run.

## Try

1. Set `threshold` to 12: equality uses sum only.
2. Set it to 13 for the below-threshold route.
3. Reverse min/max delays to inspect the join.

## Limits and copying

Copy this whole folder, including input and diagrams, and use an interpreter with the same installed pins. It imports only standard library, installed CrewAI/Pydantic, and its own `flow.py`. No application CLI/YAML, registry, agents, model keys or cloud services are needed. The entries set `CREWAI_DISABLE_TELEMETRY=true` and `CREWAI_TRACING_ENABLED=false` before importing CrewAI. These supported switches are not an OS network sandbox; CrewAI may create its normal local storage on import/construction. In restricted execution environments its installed LanceDB dependency may need socket permission even for initialization.

Typed local state validates the small demonstrated domain; delays are seconds in 0–1, loop bounds (where present) are 1–10. Async overlap demonstrates cooperative concurrency, not CPU parallelism or a performance guarantee. Ordered markers are teaching state, not durable event history. These recipes add no retries, recovery or production guarantees.

The diagram preserves the approved walkthrough's topology and example labels. Motion illustrates connectivity, not a measured trace; exclusive decision paths are alternatives. Loop-back annotations name backward transitions. Dashmotion 2.2.4 layout at ae2fe4f generated the local viewer, with script-free portable animated/static SVG exports. [MIT notice](DIAGRAM-LICENSE.txt) is retained. Python selection/counting rules are local policy; native CrewAI decorators own scheduling and joins.

## Official sources

- [CrewAI 1.15.40 Flow guide](https://github.com/crewAIInc/crewAI/blob/main/docs/v1.15.40/en/concepts/flows.mdx): typed state, listeners, async methods and routing.
- [Official routing patterns](https://github.com/crewAIInc/skills/blob/main/skills/build-flow/references/routing-patterns.md): joins, route labels and bounded loops; guidance may differ by version.
