# M1 follow-ups discovered during implementation

These notes do not alter the approved contract at `045f9a0d98ccec1f200af6f80adb7d5eb45e66d5` or add acceptance criteria to the active M1 review.

## M1-FU-01 — SDK batch flush timeout is advisory

2026-11-16. Source inspection during M1 implementation found that the pinned OpenTelemetry SDK batch processor accepts `force_flush(timeout_millis)` but currently ignores that argument and exports synchronously (upstream TODO #4568). This affects the design's bounded-flush wording and LS-02 cleanup expectations: the probe supplies a five-second HTTP exporter timeout and attempts SDK flush/shutdown, but cannot promise a hard five-second whole-process deadline. Its SDK shutdown worker join has a default 30-second limit. The README and review evidence disclose this limit; no custom timeout/queue/transport was added.

Proposed later design clarification: distinguish the configured exporter request deadline, SDK flush argument and total process deadline, especially before M2 lifecycle acceptance. The active coder received and documented this finding during round 01. It requires no change to the frozen M1 design/test/plan and no extra M1 implementation scope under the current review disposition.
