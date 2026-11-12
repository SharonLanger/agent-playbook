# Workflow experiments — start here

These are independent learning sandboxes. Start at **01**, then compare **02 → 03 → 04**
to understand method names, returned data, router labels and your intentional collision.
Then explore the four patterns from CrewAI's routing-patterns page (**05–08**).

Open the repository in PyCharm with **app/.venv/bin/python** selected. Open an example's
**run.py** and click Run. No application CLI, runner, release or workflow registration is involved.
Use the existing bootstrap if that interpreter has not been set up yet. Each example also
runs with `python /absolute/path/to/example/run.py` using that interpreter from any directory.

| Order | Read first | Click Run here |
|---|---|---|
| 01 | [Sequence and return values](ex_01_step_sequence/README.md) | [ex_01_step_sequence/run.py](ex_01_step_sequence/run.py) |
| 02 | [Method references and method-name strings](ex_02_method_completion/README.md) | [ex_02_method_completion/run.py](ex_02_method_completion/run.py) |
| 03 | [Router labels select a branch](ex_03_router_labels/README.md) | [ex_03_router_labels/run.py](ex_03_router_labels/run.py) |
| 04 | [Your method-name and router-label collision](ex_04_name_collision/README.md) | [ex_04_name_collision/run.py](ex_04_name_collision/run.py) |
| 05 | [Bounded revision loop](ex_05_revision_loop/README.md) | [ex_05_revision_loop/run.py](ex_05_revision_loop/run.py) |
| 06 | [Wait for A and either B or C](ex_06_nested_conditions/README.md) | [ex_06_nested_conditions/run.py](ex_06_nested_conditions/run.py) |
| 07 | [Order routing in two decisions](ex_07_chained_routers/README.md) | [ex_07_chained_routers/run.py](ex_07_chained_routers/run.py) |
| 08 | [Routing, join and persisted state](ex_08_persisted_routing/README.md) | [ex_08_persisted_routing/run.py](ex_08_persisted_routing/run.py) |

## What is self-contained?

Every example owns its flow, state, input, integration settings, entry script, tests and diagrams.
You can copy one whole folder elsewhere and run it with the project's interpreter. Imports
are standard library, installed CrewAI/Pydantic, or files in that same folder. Nothing imports
agent_playbook or another example. Small settings loaders are intentionally duplicated to
make each experiment independent. Existing integrated WF-01/02/03 remain separate.

The location is `app/examples/workflows/`: the project's existing checkout-only examples
boundary. Examples do not ship in the application wheel. Tests live beside each example;
the existing **Test** and **Check** tasks include them. Run any `test_ex_XX.py` individually
in PyCharm as pytest. Formatting and strict type checking include these files too.

## Read the graph correctly

- A method reference in `@listen(method)` resolves in Python; a string passes an event name.
  CrewAI's method-completion names and router labels share a namespace.
- An ordinary method's return value is data. A router's returned string selects a route label.
- `self.state` assignments do not themselves emit those route labels.
- Graph edges describe dependencies. They do not promise ordering between unrelated listeners.
- `calls` is an explicitly maintained teaching list, not automatic history or a durable event store.
  Example 06 records starts/finishes across awaits; it demonstrates overlap, not CPU parallelism.
- Result is the final completed method's output; it is not necessarily a special terminal node.
  Examples 02/04/06 test relevant state/calls rather than impose a universal final-output order.
- Animated diagrams show possible paths, not recorded scheduling. Both router edges may be drawn
  although only one is selected per invocation. Browser viewers support pause and reduced motion.

## Official references and adaptations

- [CrewAI Routing Patterns](https://github.com/crewAIInc/skills/blob/main/skills/build-flow/references/routing-patterns.md):
  section 1 → example 05; section 2 → 06; section 3 → 07; section 4 → 08.
- [CrewAI Flow wiring guidance](https://github.com/crewAIInc/skills/blob/main/skills/build-flow/SKILL.md#3-wiring-start-listen-router):
  method names and route labels share a namespace; the source reports testing on 1.15.22/23.
- [Versioned Flow documentation](https://github.com/crewAIInc/crewAI/blob/main/docs/v1.15.40/en/concepts/flows.mdx).

These are attributed teaching adaptations written for our **CrewAI 1.15.40** pin, not a claim
that upstream samples are unchanged or universally valid. Example 08 replaces the upstream
real Crew/model call with deterministic Python work and stores SQLite inside its own folder.
This is exploratory learning beyond the three integrated Stage 01 workflow contracts;
it does not implement Stage 02 Langfuse or mark later stages complete.

The official sources differ on some `or_` descriptions: the Flow page shows repeated
notifications, while the routing guidance describes first-completion behavior with router
re-arming. Use the pinned-version tests and observed results here as evidence, not a blanket
claim for all CrewAI versions. Findings and limits are recorded in the stage's learning notes.

[Verification findings and scope](../../../designs/stages/01-crewai-flows/learning/08-independent-sandboxes.md).
