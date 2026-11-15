# CrewAI → Langfuse isolated research probe

Research date: 2026-11-14. This is a scratch experiment, not an application implementation or maintained application test suite. See the accompanying research report for the integration recommendation and limitations.

## Reproduce

Use Python 3.13 (tested 3.13.5), unzip into a disposable directory, then:

```bash
python3.13 -m venv .probe-venv
uv pip install --python .probe-venv/bin/python -r requirements.txt
uv pip check --python .probe-venv/bin/python
.probe-venv/bin/python probe.py
```

Installation needs package-index access. Running the probe does not require a Langfuse server, API key or model: the two fake local keys in its source are synthetic values. It uses Langfuse 5.2.0's public in-memory span exporter hook and its real default processor/filter; this does not prove server ingestion/UI mapping.

Expected observed result: 8 trace cases, 44 exported spans, 8 blocked socket/DNS attempts. The last count can vary with framework update-check caching/environment. The script blocks Python socket connects/DNS and records attempts, rather than claiming the framework attempted none. Observed requests were to pypi.org: the CrewAI console formatter invokes its version checker through the event bus. No outbound connection succeeded. This Python-level audit is not an OS sandbox.

The script sets the same two CrewAI flags mapped by the application's current config (disable telemetry, disable built-in tracing), but bypasses the actual application assembly/runner and its display behavior. This is not evidence that the configured application itself regressed offline behavior. It also removes ambient proxy settings and disables sampling loss with an explicit ALWAYS_ON provider. Tracing assertion results do not depend on a network call succeeding.

## Contents and provenance

- `probe.py`: full executable experiment; conditions fixture plus actual maintained Flow definitions.
- `results.json`: observed attributes, actual IDs, parentage, status and blocked-call stacks, plus all installed package versions.
- `requirements.txt`: exact 144-package isolated dependency closure (not a replacement application lockfile; not hash-locked).
- `source-manifest.json`: source baseline and content hashes.
- `agent_playbook/workflows/...`: eight necessary maintained source modules only. No private examples, application source edits, credentials, caches, environment or installed packages included.

Source: https://github.com/SharonLanger/agent-playbook at 44d69194f6add6f646795b14f7c3f43c656baeda. The modules are unmodified content copies, under namespace-package directories for isolated importing. Framework source dependency behavior is established by installed release wheels and hashes in the main report. The controlled failure uses a temporary mock of the maintained deterministic multiply helper; it does not modify the source files.

This probe asserts hierarchy/correlation/results for WF-01, WF-02, both WF-03 branches, a repeat, a failure, direct async kickoff and AND/OR conditions. It does not test the application's ABC wrapper/error translation, concurrent independent invocations, recovered failures, live model/tool behavior or Langfuse UI acceptance.
