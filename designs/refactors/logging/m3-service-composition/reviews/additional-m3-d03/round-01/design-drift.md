# Additional M3-D03 round 01 — design correctness/drift

Independent reviewer; configured model `gpt-6.2-sol`, serving ID unavailable. Reviewed frozen SHA `df64582af4e3accb4b0747e3c1b44a429d541a6b` without edits. Verdict: **CHANGES REQUIRED**.

**M3-D03 remains open, required.** The candidate verifies a container's immutable identity, project/service labels and startup credentials before attaching and repeats this for replacements. In follow mode it emits complete lines from `docker logs` stderr through the known-value redactor before checking command success. Docker's own failure diagnostics share that stream with container stderr. In a synthetic POSIX subprocess reproduction, a failed attached `docker logs --follow` emitted an unknown private marker on stderr; the CLI printed it, then printed the generic unavailable message and returned 1. Expected: withhold unverified Docker diagnostics while retaining safe verified container messages. Relevant code: `app/tooling/observability/logs.py` stream read and follow exit handling. Snapshot correctly suppresses captured output when `docker logs` exits nonzero.

Focused Langfuse suite 22 PASS; diff whitespace, Atlas and daemon-free Compose v2.40.3 smoke PASS. No real Docker daemon, Mac acceptance, personal examples or real secrets used. The passing checks did not establish the follow error boundary.
