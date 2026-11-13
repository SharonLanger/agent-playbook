# Handoff: exclude the personal examples sandbox

Status: PLAN ONLY — no implementation changes made.
Requested by Sharon on 2026-11-13.
Repository: SharonLanger/agent-playbook.
Context: PR #34, branch `refactor/runtime-structure-and-verification`.
Inspected implementation: `30c8d96b16252d8c9d3238b2d9e29fea0bcc926e`. Recheck the current head before editing.

## Start here

Read AGENTS.md and the applicable design documents before implementing. This file
hands off the requested change; it does not merge PR #34 or approve unrelated work.
The current agent created only this handoff file. No code, tests, configurations,
protected documents, or example contents were changed.

## Required outcome

`app/examples/` is Sharon's personal sandbox. He may modify, break, or delete it.
Normal application tests, coverage, type checks, lint, formatting, setup,
verification and build/release must not execute or depend on its contents.
No future CI/CD gate should depend on it either.

Application test cases and their fixtures belong under `app/tests/` and exercise
the real implementation in `app/src/agent_playbook/`. Merely placing a test under
tests while importing examples does not satisfy this rule.

Keep explicit, voluntary lint and formatting available for examples. These commands
must never be called by the default gate, setup, release, or PR verification.
Do not delete the examples folder or rewrite its exercises as part of this task.

## Verified connections to remove

- `app/tooling/checks.py`: both test and full check explicitly invoke
  `pytest -q tests examples/workflows`; Ruff targets include examples.
- `app/pyproject.toml`: Pyright includes examples; pytest has no testpaths restriction.
- `app/tests/examples/test_greeting.py`: imports `examples.typing_example`.
- Setup, Release and Verify Refactor invoke the full gate and inherit those dependencies.
- `app/tooling/release.py`: whole-repository clean-status checks let changes to examples
  block releases; its temporary build archive currently includes the whole committed app tree.
- CLI help, examples/tests READMEs, CLI documentation and the guarded project structure
  describe examples as checked/tested.
- No GitHub Actions workflow was present at the inspected revision. Recheck before editing.

## Implementation checklist

- [ ] Audit references outside examples: source imports, tests, fixtures, check commands,
      test discovery, type/lint/format settings, build inputs, release preflight,
      IDE tasks, coverage settings if present, and any newly added CI configuration.
- [ ] Remove examples from default test, type, lint and formatting targets.
      Set default pytest discovery to application tests. Verify broad/default invocations
      cannot accidentally collect sandbox tests.
- [ ] Audit only the existing sandbox tests needed to classify their dependencies.
      This is a bounded migration audit, not permission to maintain the sandbox.
      EX-07/08 exercise their own example flows; retaining their counts is not a goal.
- [ ] If an existing test genuinely checks production code, compare it with current
      application cases. Move/adapt it into app/tests only when the scenario is missing.
      Keep fixtures in tests and import the real application implementation; do not
      copy production implementation into tests. Do not duplicate existing cases.
- [ ] Remove sandbox-only dependencies from the application suite, including the
      greeting exercise test. Do not copy sandbox tests into tests just to preserve counts.
- [ ] Ensure example changes, untracked files, broken syntax, or deletion cannot fail
      setup or release. Narrow release clean-status checks and archive inputs as needed,
      while retaining clean-commit and reproducibility protection for actual build inputs.
      Do not use a blanket dirty-build bypass or change general Git tracking behavior.
- [ ] Keep examples out of wheel and release build inputs. The application package
      already excludes them; verify that remains true.
- [ ] Preserve manual lint/format targeting as described below.
- [ ] Update operating instructions and future-agent boundaries; follow existing
      exact-diff approval requirements for protected documents.
- [ ] Record actual verification evidence and update any PR claims affected by the
      changed test population. The old 137-test result includes sandbox tests and
      must not be presented as the new application-only result.

## Preserve the useful application verification

Sharon explicitly likes the PR verification that runs the actual workflows through
the CLI with JSON input. Preserve WF-01 hello, WF-02 numeric input/result, WF-03 both
branches, and invalid-input/error behavior, for source and installed releases.

At the inspected revision, tooling/verify_runtime.py runs:
- WF-01 with {} => [Hello, workflow!]
- WF-02 with initial=3, increment=2, multiplier=4 => 20
- WF-03 with score=80 => pass; score=40 => needs_work
- WF-03 with score=101 => input error / exit 2

These paths exercise production code, not examples.
Place application acceptance test cases/fixtures under app/tests (for example,
tests/acceptance) if extracting assertions from tooling. Keep tooling as the
orchestration entry point for the existing Verify Refactor button, release build,
artifact hashes and installation checks. Preserve isolated-interpreter and offline
verification: installed checks must not silently import editable source.
Do not introduce a mandatory pytest dependency into installed production releases.

## Explicit manual lint and formatting

Yes, sandbox lint/format can remain available while automatic checks ignore it.
Prefer simple documented manual commands rather than a new automatic task.
The intended usage, from app/ with its interpreter, is:

```sh
python -m ruff check examples
python -m ruff format --check examples
python -m ruff format examples
```

The last command modifies files only when Sharon invokes it.
Validate these commands against the final exclusion configuration. If exclusion
settings also suppress explicit paths, provide a documented per-invocation override
or a dedicated opt-in command that retains the project's lint/format rules.
No default gate or release may invoke it. Do not add an automatic sandbox test task.

## Permanent rule to record

Proposed wording for AGENTS.md and the guarded project structure:

> app/examples/ is Sharon's personal sandbox. Do not inspect, modify, validate,
> or execute its contents unless explicitly requested for that task. Application
> code, automated tests, coverage, quality gates, setup and build/release processes
> must not depend on it. Application tests and fixtures belong under app/tests/
> and exercise the actual application implementation. Removing app/examples/
> must leave application behavior, collected application tests and application
> line/branch coverage unchanged. Explicit user-invoked sandbox lint/format is
> permitted and must remain outside all automated gates.

Align app/examples/README.md, app/examples/workflows/README.md, app/tests/README.md,
app/docs/cli.md and CLI help with that policy. Check the charter's general checking
scope for ambiguity; propose the minimum protected-document clarification needed.
Do not rewrite historical verification results as though the new behavior existed then.
Transfer the lasting decision into permanent docs before removing this temporary handoff.

## Acceptance evidence

Use disposable checkouts; never delete Sharon's working examples to test this.

1. Establish the final application-only collected test IDs and results.
2. Repeat with examples absent. Same application tests, same results.
3. Compare application line and branch coverage using the same environment/configuration
   when coverage measurement is available. Scope to src/agent_playbook. If no coverage
   tool is configured, state that and do not invent a coverage result.
4. Confirm normal check/format/setup/Verify Refactor and release work with examples absent
   and with intentionally invalid sandbox files or uncommitted sandbox-only changes.
   Keep required source/config cleanliness enforcement intact.
5. Confirm explicit sandbox lint detects a deliberate issue and explicit formatting works
   in a disposable sandbox, while the normal gate ignores it.
6. Confirm all three real workflow probes, both WF-03 routes, invalid-input behavior,
   installed import isolation and artifact exclusion remain verified.
7. Report any application case migrated and any duplicate avoided. Expect the total test
   count to decrease when sandbox exercises are removed; app coverage must not decrease.

No implementation or verification is claimed by this handoff.
