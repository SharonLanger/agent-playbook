# Additional RD-03 / TG-SC-05 correction — author record

Frozen design candidate: `c4e0951bd87c81e627d58127841494d4812732ab`. Scope: Sharon's one additional design correction and one verification round, limited to RD-03 and TG-SC-05. This report is published after the candidate; it does not alter it.

The correction updates only `design.md`, SC-07 in `test-cases.md`, and `implementation-plan.md`, plus the derived Atlas index. No runtime or Compose files were edited.

The aggregate `services` coordinator now owns its outer deadline and the currently active component process group. Direct component commands are supervised by the CLI. On aggregate timeout or Ctrl-C, the coordinator terminates the active group and its descendants, reaps the helper, returns failure, and starts no next component. Component Docker CLI descendants remain in that group. Cancellation never calls an implicit `docker compose down`. A component timeout within a still-live aggregate deadline can proceed to the sibling.

SC-07 uses shortened deadlines to force the outer deadline before the active start, status, and stop component deadline. It also exercises Ctrl-C, a TERM-resistant grandchild, registration races, direct component cancellation, normal helper exit with a stray descendant, and checks for no next component, probe, sleep, or implicit Docker down.

Evidence before freeze: Atlas build and freshness check passed; a disposable synthetic POSIX probe observed helper reaping and grandchild exit for start, status, stop, and interrupt. These are design/OS checks, not runtime acceptance. Runtime implementation and runtime tests were not started.
