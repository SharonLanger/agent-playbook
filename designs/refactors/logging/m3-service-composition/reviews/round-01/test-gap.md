# Round 01 test coverage review

Independent reviewer; configured model `gpt-6.2-sol`, serving ID unavailable. Frozen candidate: `319950acba1beabc36e9c3ed5dcac8126bffa1be`. Verdict: **CHANGES REQUIRED**.

- **TG-M3-01 required, SC-07:** POSIX tests prove eventual cleanup but would pass with immediate KILL, override all production cap/reserve constants, and do not prove TERM before KILL or production arithmetic. Strengthen signal/deadline assertions. `app/tests/tooling/test_service_cancellation.py`.
- **TG-M3-02 required, SC-06/08:** aggregate tests mock the supervisor while persistence/safety tests invoke a manager directly. Add actual aggregate CLI/coordinator/manager lifecycle with custom env, retained state, disabled-running status and unsafe Langfuse stop followed by real logging teardown. `test_service_selection.py`, `test_service_managers.py`.
- **TG-M3-03 required, SC-03/04/11:** explicit disabled-logging test calls raw helper rather than supported CLI. Exercise direct logs and aggregate logs-only CLI with absent Langfuse keys, process override and unchanged YAML. `test_service_managers.py`.
- **TG-M3-04 required, SC-08/09:** successful Compose identity lookup checks only stdout redaction; add marker-bearing stderr and assert both streams. `test_service_managers.py`.

Real POSIX outer start/status/stop, Ctrl-C, direct cleanup and no-down cases did run. Independent tooling-only run: 135 passed, one unchanged release-completion test failed with a different workflow error; baseline cause unverified. The coder's later full gate passed at this same SHA with a writable LanceDB scratch location. Daemon-free Compose syntax/identity and Atlas passed. Live Mac and LG-10 NOT RUN. Reviewer made no edits.
