# Logging progress

**Complete — 2026-11-21.** M1 configuration and smoke (#54), M2 application logging (#55), and M3 service controls (#65, design #57) merged. Sharon authorized closing the overall design in #51 on the following evidence.

- On the Mac, both individual start/status commands succeeded. A fresh workflow produced a Langfuse trace and VictoriaLogs records. Sharon also observed matching correlation IDs during a workflow run.
- The Mac sanity check was accepted for closeout. The detailed LG-10 chained-exception, ordering and shutdown checks and the full aggregate/restart matrix remain unverified live.
- The failed Docker live-follow diagnostic disclosure remains open in [#66](https://github.com/SharonLanger/agent-playbook/issues/66).
- [#37](https://github.com/SharonLanger/agent-playbook/issues/37) owns the doctor command using existing integration checks. Guided first-time setup is deferred. Broader renaming stays in #56.
