# Stage 01 — Implementation verification

Configuration follow-up evidence is recorded separately in [configuration-findings.md](configuration-findings.md).
The 97-test/release measurements below describe the earlier implementation before external configuration.

Verified 2026-11-12 on Linux x86_64, Python 3.13.5. Sharon authorized all three independent
workflows in one implementation PR after merging the design. Mac/PyCharm acceptance and the
learning sessions remain pending; implementation verification is not a claim that learning
is complete. Earlier documentation-only findings are retained below as history.

## Baseline and versions

- Main/design merge: `4754bf4b03ef122e5e248ce1f6f5f600c2212f15` (PR #29).
- CLI refactor PR #28 is merged; its final changes and Sharon's 0.0.11 version were retained.
- Stage 01 version: **0.1.0**. CrewAI **1.15.40**, Pydantic **2.12.5**, uv **0.13.6**.
- CrewAI CLI includes a transitive uv dependency. A uv constraint keeps it at the existing
  project toolchain version instead of allowing a newer private executable to conflict.

## Executed checks

| Verification | Result |
|---|---|
| Full `agent-playbook check` | Pyright: 0 errors; Ruff lint/format: pass; **97 tests passed** |
| Actual kickoff: sequence | Exact string and ordered produce/decorate/finish events |
| Actual kickoff: state | Default 20/[3,5,20], custom 24/[10,8,24], zero multiplier, fresh independent runs |
| Actual kickoff: routing | Both routes; threshold 59/60; chosen method once, unchosen method never |
| Failure behavior | Domain and terminal-assignment exceptions propagate; successors/success output skipped; causes retained |
| Invalid inputs | Malformed/non-object JSON, unknown fields, bools/strings/floats and bounds rejected before steps |
| Source offline probe | Fresh Python process; socket/DNS attempts denied and recorded before app/framework import; zero attempts |
| Clean committed release | Archived lock exported; hashes enforced; 138 installed runtime packages consistent; all routes and invalid input verified |
| Installed release guards | Correct version/source/import location; developer commands reject with exit 2 |
| Installed offline probe | All three workflows/both routes pass with no API keys and zero audited socket/DNS attempts |
| Packaging | Application wheel excludes tooling/tests; isolated venv has no pytest, Pyright, Ruff or tooling module |
| Source-edit isolation | Temporary WF-01 edit appears in dev-run; selected installed 0.1.0 still returns original message; edit restored |
| Legacy release compatibility | Real pre-Stage 01 0.0.11 wheel: bare run succeeds; explicit workflow option returns its usage error (exit 2) |
| Bootstrap entry point | Run through Python 3.13 from /tmp; locked setup, default flow and complete 97-test gate pass |
| Documentation/tasks | 120 local Markdown links resolve; all 18 PyCharm task XML files parse; git diff whitespace check passes |

The offline probe uses Python's audit events; it is evidence for these exercised Python
execution paths, not an OS-enforced network sandbox or a guarantee for future native libraries.
The generated environment requires downloading dependencies unless they are already cached.

## Release identity and size

Release was exercised from clean local commit `fa19eb0824850dfd4d12cd03ea87c1e47e746f67`.
This checkout was reconstructed from the GitHub baseline for local verification. The PR's
GitHub commit has a different source SHA; its application tree matches the tested tree.
Only documentation/evidence was updated after this successful release verification.
Generated release folders and environments are ignored and are not included in the PR.

| Artifact | Measured logical bytes |
|---|---:|
| Application wheel | 17,359 |
| Installed runtime environment | 858,695,408 (about 819 MiB / 859 MB) |
| Full release directory | 859,102,634 |
| Exported production requirements | 77,312 |
| Archived lockfile | 311,875 |

These are Linux measurements; Mac builds can differ. The application wheel is small, but
CrewAI's transitive dependencies dominate installed size. The release contains the wheel,
locked dependency evidence and venv, not the whole repository. Accumulating releases also
accumulates environments; no automatic cleanup or pruning was added.

Wheel SHA-256: `49cd0593415408b9ef52eaa7fb3245581cd2474990076c5b9f07e7d4af8cc1cd`.
Requirements SHA-256: `99fb1fc30d3c3b63e7a4b5464eab05a3fc9364f9631edcf6bffd5afbf4779840`.
Lock SHA-256: `31d124975239acfa7fb24158e9a05167b37933c2121f6a3c73efebff75abc71c`.
All three were rechecked after execution; archived lock bytes matched the committed lock.

## Framework findings affecting the teaching code

- Synchronous kickoff returns the terminal value and propagates an ordinary failing listener's
  exception. No adapter that converts exceptions into successful result strings was needed.
- Typed initial_state preserves validated input and gives each invocation its own history.
  CrewAI adds its own internal ID. External schemas still reject injected IDs/history/results.
- `Flow[dict[str, object]]` triggered a framework state-serialization warning. WF-01 uses
  CrewAI's built-in `FlowState` instead: ID-only framework state, no custom application schema.
  The clean release was rebuilt and verified after this correction.
- A test subclass overriding a listener did not exercise the inherited routing graph as
  expected. The terminal-failure test instead runs the actual ConditionalRouteFlow and injects
  a state validator that fails during the selected terminal assignment. Independent workflow
  classes and composition remain the approach; graph inheritance is not a taught guarantee.
- Strict Pyright required a typed list factory (`list[int]`) for the state history. Global
  strictness was preserved; no ignore or broad cast was added to hide framework integration.

## Next learning/acceptance actions

Use `learning/00-reading-the-code.md`: Setup → Check → each named WF run/test pair. Read the
three detailed workflow guides while inspecting the actual implementation. Confirm Mac IDE
execution and embedded SVG playback with Sharon. No model credentials or additional design
choices are needed to start those sessions. Keep Stage 02 and real agents out of this PR.

---

# Earlier design-package checks

Checked 2026-11-12. This is evidence for the documentation PR, not Stage 01 acceptance.

## Repository coordination

Main inspected: `4c9e74dcaf6897f6337f367dbbf17177bbada6c1`, package version 0.0.10.
PR #28 rechecked at `abdb0ae17927648eaee44e11a9d8b3b596075f0c`, open with 14 changed files.
Its published code diff was read after the earlier handoff-only snapshot. The design reflects
its parser, package imports, uv resolver, release operations and discovery parameter.
The PR description reports its own full check/release verification; those application tests
were not rerun by this documentation task. The snapshot may change before implementation.

## Checks actually performed

- Pinned Dashmotion renderer produced five diagrams. Its bundled structural checker reported
  **0 violations for all five final HTML diagrams**; architecture was checked again after
  correcting the legend to entry/shared/workflow/run journey.
- Numeric label/padding review: removed long side labels on narrow vertical flows; retained
  wrapped node labels. The architecture's legend describes ownership rather than suggesting
  the workflow packages are databases. Branch diagrams only animate the selected route.
- All five static SVGs parse as XML and contain no script or animation elements. Moving-dot
  elements are omitted from static siblings.
- All local Markdown/HTML links resolve against the proposed files plus the reviewed main
  tree. Markdown fences are paired. No remote script/font/image dependencies were added.
- Node syntax checks passed for all five inline pause/reduced-motion scripts. Workflow step
  notes use native HTML disclosure controls and need no additional JavaScript.
- Five illustrative Python snippets parse syntactically. They were not executed against
  CrewAI and are not application tests.

No browser/screenshot verification was performed; Dashmotion's specified structural checker
and numeric review were used. Browser rendering, local motion controls and Mac/PyCharm viewing
remain for visual review. These checks do not prove runtime workflow behavior.

## Deliberate boundaries and next evidence

No application code, tests, dependencies, lockfile, version or IDE tasks changed. No Stage 01
quality gate or release was run because no Stage 01 runtime exists in this PR. No skill was
globally installed. Dashmotion was used from a separate authoring workspace; Animated SVG's
video pipeline is documented for future use and was not installed/run here.

Before implementation acceptance, record the chosen CrewAI/Pydantic versions, Python 3.13
compatibility, real kickoff return/error semantics, typing, state initialization, telemetry
controls, offline runtime probe, locked dependency installation and measured artifact sizes.
Record macOS IDE results separately from any Linux verification. Reconcile PR #28 again before
starting code. Do not turn these pending checks into success claims without execution evidence.

## Permanent-location correction

At Sharon's request, the complete package was moved to `designs/stages/01-crewai-flows/`.
All 30 stage files were retained. The design inventory now links its permanent reading guide;
agent instructions reserve `designs/temporary/` for disposable handoffs only. Approval and
implementation do not make this package eligible for deletion. Relative directory depth is
unchanged, so the existing lesson/diagram/policy links retain their targets. Local links were
rechecked after relocation; the diagram asset contents are unchanged from the checked versions.

## Animations embedded in Markdown

At Sharon's request, added five standalone `*-animated.svg` files and changed all 16 diagram
image embeds in the stage Markdown to use them. The reading guide, architecture, relevant
lessons, workflow contracts and diagram guide now show the animated assets in place. HTML
links are optional pause-control views; static SVG siblings are retained separately.

All five animated SVGs passed the Dashmotion checker with 0 violations. XML and local-link
checks passed (109 links). The SVGs preserve their HTML originals' connector and motion paths,
contain no scripts, event handlers or external references, and handle reduced motion in CSS.
This avoids reliance on the HTML viewer's JavaScript when an SVG is loaded as a Markdown image.
The authoring policy now requires direct animated SVG embeds for future explanations.

Actual playback in Sharon's Markdown/PyCharm viewer is not verified here. A viewer that suppresses
SVG motion, or a reduced-motion preference, can still display a static diagram. This limitation
is separate from the prior mistake of embedding the deliberately static files by default.

