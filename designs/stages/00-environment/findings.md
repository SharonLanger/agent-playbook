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
