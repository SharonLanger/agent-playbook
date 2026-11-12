# Lesson 6 — Run the same workflow from source and a release

**These workflow options are implemented in Stage 01.**
Current checks, formatting, version and release commands already exist and remain unchanged.

## Workflow invocation

```sh
agent-playbook dev-run --workflow wf-01
agent-playbook dev-run --workflow wf-02 --input '{"initial":3,"increment":2,"multiplier":4}'
agent-playbook dev-run --workflow wf-03 --input '{"score":40}'
agent-playbook run --version 0.1.0 --workflow wf-03 --input '{"score":80}'
```

Use lowercase `wf-01`, `wf-02`, `wf-03` as stable CLI IDs. Uppercase display labels stay in
logs/documents. `--input` is a JSON object passed as one argument; shell single quotes preserve
its double quotes. In PyCharm enter the corresponding parameters in a Python module
configuration using `agent_playbook.cli`, the project interpreter and working directory app.

Absent `--workflow` defaults to wf-01. Absent `--input` uses that workflow's documented defaults.
Help lists the IDs and input fields; no new list command or workflow plugin system is needed.
The direct `python -m agent_playbook` entry point runs default WF-01.

## Who validates an installed run?

The editable launcher selects a release and forwards explicitly supplied workflow/input
arguments as separate subprocess arguments. The selected release validates them against its
own supported workflows. Never validate a new schema in the checkout and silently run an old
release with different semantics. Preserve `-I` and removal of PYTHONPATH/PYTHONHOME.

An older Stage 00 release still runs through a bare `run`. If explicit Stage 01 options are
sent to an older release that does not understand them, surface its nonzero usage error;
do not drop options or switch to editable code. Source selection and version selection are
independent choices. `version` reports the executable invoked, not the selected workflow.

## Development loop

1. Use Dev Run / a named WF task to see source changes immediately.
2. Use `test` and `check --types`, `--lint`, `--format` as needed.
3. Use `format` to fix formatting; review the resulting edits.
4. Run plain `check` for the full gate.
5. Change the version only when preparing a release; review and commit first.
6. Build `release`, then use `run` to execute the installed artifact.

For first Stage 01 release, explicitly set 0.1.0 using the existing version script. Future
patches use `version patch`. The Stage 01 implementation uses version 0.1.0.

## Why release needs extra work for CrewAI

The old application has no runtime dependencies. A new wheel imports CrewAI/Pydantic, so the
release environment must contain their locked production dependency closure. Keeping only
`pip install --no-deps <wheel>` would produce an incomplete installation. See architecture.md
for the locked export/install contract, and findings.md for the actual verification.

Acceptance includes starting all three flows from the release venv with no editable source
on its import path, then editing source and proving the old release remains unchanged. A
passing source test suite alone does not establish a usable release. Network may be needed
for dependency downloads; successful offline workflow execution is a separate verification.
