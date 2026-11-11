# Stage 00 — Findings

## 2026-11-11: Stage 00.1 bootstrap and runnable main

**Hypothesis:** one setup command can provision the environment and run main,
then be repeated without rewriting the committed dependency resolution.

**Implementation:** Python 3.13.5, uv 0.13.6, no application dependencies. Python
was narrowed from the interrupted branch's broad 3.12–3.13 range to the exercised
3.13 series; `.python-version` pins the exact patch. uv generated `uv.lock`.
Bootstrap requires Python 3.10+ with venv/ensurepip, reuses exactly matching uv
or installs it into `.bootstrap-tools`, and runs `uv sync --locked --python 3.13.5`.

### Executed evidence

Linux x86_64; bootstrap launcher Python 3.12.14; app Python 3.13.5:

| Check | Observed result |
|---|---|
| `uv lock --project agent-playbook/app` | Generated lockfile; one virtual project, zero third-party dependencies |
| `python3 app/scripts/bootstrap.py`, twice | First created `.venv`; second reused it; both printed the expected main message |
| `app/.venv/bin/python app/src/agent_playbook/__main__.py` from root | Expected message; exit 0 |
| Bootstrap with uv removed from PATH | Installed uv 0.13.6 into `.bootstrap-tools`; synced and ran main |
| Fresh app copy with no generated environments; path containing spaces; working directory `/`; PATH `/usr/bin:/bin` | Bootstrap installed private uv and created app environment; exit 0 on both first and second runs |
| Changed project version to 0.0.1 in disposable copy without updating lock | `--locked` rejected stale lockfile; bootstrap exit 1; main was not run |
| Added unavailable dependency in disposable offline copy | Resolution failure propagated as exit 1; lockfile bytes unchanged; main was not run |
| `git check-ignore` on environment, IDE, cache, secret and build paths | All intended generated paths ignored; `.env.example`, manifest and lockfile not ignored |

The expected message was `Agent Playbook — Stage 00.1: Python environment ready.`
Fresh copies contained only source/config files, with `.venv`, `.bootstrap-tools`
and caches excluded. Initial pip provisioning downloaded the uv wheel; fresh-copy
runs reused pip's download cache. Python 3.13.5 was already installed on this host.

### Limitations and next action

- PyCharm UI/run/debug, macOS and Windows have not been executed here.
- Automatic Python download when 3.13.5 is absent has not been exercised.
- No pytest/Pyright/Ruff or unified gate yet; these checks are smoke experiments.
- Git clone authentication was unavailable in this runtime. Repository inspection
  and publishing use the connected GitHub API; local verification uses the app
  source/config snapshot. This is not a claim of testing a full Git clone.
- User should run setup twice and debug main in PyCharm before accepting 00.1.

### Baseline observations

The handoff and current instruction authorize Stage 00.1, but approval/status
labels on main are stale. The plan's CrewAI import criterion contradicts its
explicit exclusion. Record these for separate baseline cleanup; no protected
architecture/plan, historical sandbox, CI, or future-substage tools were changed.

### Tool references

- [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- [Python management](https://docs.astral.sh/uv/guides/install-python/)
- [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

## 2026-11-11: Stage 00.1 acceptance and Stage 00.2 CLI

User reported running main and seeing the environment-ready output, then explicitly
approved merge and continuation. PR #17 merged; no claim of PyCharm breakpoint or
OS-specific verification is inferred from that report.

**Hypothesis:** the same bootstrap can expose `agent-playbook run` while preserving
00.1's main behavior. Added argparse CLI, a project console-script mapping and pinned
`uv_build==0.13.6` for editable installation. Regenerated the lock with uv 0.13.6.
This setup plumbing does not introduce the release workflow from 00.7.

**Executed on Linux:**

- Existing 00.1 environment: bootstrap installed the editable project, ran the CLI,
  and succeeded a second time. Output matched the unchanged main message.
- Installed CLI invoked from `/`: `run` and `--help` exit 0; missing command,
  unknown command and `run extra` each exit 2 with argparse diagnostics.
- `.venv/bin/python -m agent_playbook.cli run` from `/`: same output, exit 0.
- Fresh source/config copy in a path with spaces, no generated environments:
  bootstrap twice and independent CLI run from `/` all passed.
- No runtime dependencies or third-party CLI framework added. uv used its bundled
  compatible build backend. A filesystem hardlink warning fell back to successful
  file copies; no failure was suppressed.

**Pending:** user CLI acceptance and actual PyCharm UI/debug run. macOS/Windows
execution and automatic Python download remain unverified. pytest, Pyright and Ruff
are still deferred. Protected baselines and historical sandbox remain unchanged.

References: [uv project configuration](https://docs.astral.sh/uv/concepts/projects/config/)
and [build backend](https://docs.astral.sh/uv/concepts/build-backend/).

## 00.3 — Pyright strict (2026-11-11)

Installed pinned Pyright 1.1.407 through the same bootstrap. Strict mode checks
src/ and scripts/, including typed bootstrap helpers. Linux bootstrap and final
Pyright run passed with zero diagnostics. Each of three temporary mutations to
typing_example.py (wrong argument, wrong return, missing None guard) returned
nonzero with the expected type error; restored source passed again. CLI still
prints the original main message. Node v24.22.1 was already present: automatic
Node provisioning and PyCharm UI/editor integration are not claimed verified.
The type-checking exercise contains explicit PyCharm run-configuration guidance.

## 00.4 — pytest (2026-11-11)

Pinned pytest 8.4.2; added four tests for named/optional greetings and CLI run/error
behavior. Bootstrap and strict Pyright passed. `agent-playbook test` passed all
four tests, detected a deliberate guest-message regression (exit 1), then passed
after restoration. In an isolated editable environment installed without dev
dependencies, `test` exited 2 with a clear missing-pytest/bootstrap message.
No Ruff yet. Actual PyCharm test configuration remains for local user verification.

## 00.5 — Ruff (2026-11-11)

Pinned Ruff 0.14.4, selected E4/E7/E9/F/I lint rules and formatted existing source,
scripts and tests. Bootstrap executes read-only lint and format checks. An unused
import mutation failed lint; a quote-style mutation failed format verification;
both passed after restoration. Existing Pyright and four pytest tests remained
passing. During the earlier isolated missing-tool experiment, the first venv used
Python 3.12 and installation correctly refused it; retry with pinned Python 3.13.5
verified the intended missing-pytest error. No non-Linux/IDE validation claimed.

## 00.6 — Unified gate (2026-11-11)

`agent-playbook check` runs Pyright, Ruff lint, Ruff format verification and pytest
in that order, stopping at the first nonzero code. Bootstrap now invokes that gate.
Six tests include gate exit-code propagation/stopping and missing-tool behavior.
Executed real type, format and behavior mutations through the combined command:
each returned nonzero; restored source passed all four checks and six tests.
No files are automatically changed by check. PyCharm execution remains unverified.

### 00.6 output clarity (2026-11-11)

Added numbered tool sections, flushed headings before subprocess output, per-tool
PASS/FAIL and a final PASS/FAIL/NOT RUN summary. Tool diagnostics remain visible;
stderr joins stdout so it appears in the same section. The first failure still
stops execution and its exit code is preserved. Missing tools and launch errors
produce an explicit failed summary, without claiming later tools passed.

Executed against the pinned 00.6 app snapshot on Linux, using the existing pinned
development environment and an explicit source path. Strict Pyright, Ruff lint,
Ruff format and all 11 pytest tests passed. Regression tests cover failures at
each position, execution order, incomplete tool setup and a subprocess launch error.
Real temporary source mutations separately failed types, lint, formatting and
tests, producing respectively 3, 2, 1 and 0 NOT RUN results. Restored source passed
the complete gate. Actual PyCharm rendering and macOS execution remain unverified.

## 00.7 — Versioned Wheel release (2026-11-11)

Version 0.0.1. Added `version`, release.py and verify_wheel.py. Release creation
requires a clean Git checkout, runs the unified gate, archives the exact source
commit, injects commit metadata only into that archive, builds the Wheel, records
and verifies SHA-256, installs into a new isolated environment, verifies metadata
and import location, and confirms development commands are rejected.

Executed on Linux:

- Dirty checkout refused before building.
- Clean local verification snapshot passed all checks and 8 tests, then built
  agent_playbook-0.0.1-py3-none-any.whl and installed it non-editably in a fresh venv.
- Installed `run` and `version` worked from outside the repository. Import location
  was under the isolated environment's site-packages; `test` and `check` exited 2.
- Changed the development main message: development output changed, installed
  release output remained identical. Restored source afterward.
- A corrupted copy of the actual Wheel failed SHA-256 verification (exit 1).
- Final bootstrap passed the unified gate and 8 tests after restoration.

Evidence from this local verification build (not a published release):
source commit `e5acf5a5db4b8aaa4996d0c0233b8c765e659683`, Wheel SHA-256
`2c83fd5aa2c15d31d7d2b8a0b2517cc0f780ac8504bd9e17d0f08761834bd273`.
The local Git history is a verification snapshot, not the GitHub branch history;
GitHub cloning was unavailable, so source publishing uses its connected API.
Running release.py in the user's checkout will embed that checkout's actual Git
revision and produce its own digest. No artifact was uploaded to a package registry
or GitHub release. macOS, Windows and actual PyCharm UI remain unverified.

## Prepared PR stack

00.3 is the next user lesson. 00.4–00.7 are prebuilt dependent branches as explicitly
requested, not accepted stages. Review and merge one at a time. After each preceding
PR merges, retarget its successor to main and propagate any review changes forward
before acceptance. Stage architecture/plan and historical sandbox remain unchanged.

### 00.7 carry-forward of check output (2026-11-11)

Carried the 00.6 output/reporting fix and merged architecture documentation into
this dependent branch. Strict Pyright, Ruff lint/format and 13 tests passed on
Linux after integration. Wheel build/install experiments above were not rerun
for this console-reporting change.
