# M1 test cases

**Draft.** This is a small configuration sanity check, not a VictoriaLogs product test suite.

| ID | Scenario / level | Observable acceptance | Requirements |
|---|---|---|---|
| LS-01 | Compose configuration; local command | Config resolves with pinned image, local volume, loopback port and sole internal network; actual Docker/Compose versions recorded | LOG-23/24 |
| LS-02 | Synthetic emit and local UI; manual integration | One unique correlation record is found; expected message, severity, workflow/run/correlation fields are visible after script cleanup | LOG-01/04/19/25 |
| LS-03 | Endpoint validation; focused offline check | A non-loopback destination is rejected before export; no environment proxy or redirect is used by the configured session | LOG-24 |
| LS-04 | Scope review | No runner/Langfuse/workflow changes, global tracing setup, remote fallback, personal-sandbox dependency or unrequested services | LOG-09/14/20 |

LS-02 is NOT RUN until Docker is available. Health responses, a zero script exit, or a mocked exporter do not substitute for seeing the actual record. Use synthetic data only; no load/restart/rotation/disk-pressure/security audit in this milestone.

Run relevant repository checks for changed Python/dependencies; do not add tests that merely duplicate SDK internals. Record command, environment, result and limitations under implementation review evidence when work starts.
