# Stage 01 — Implementation and learning sequence

**Proposal for review. The documentation PR is complete before code starts.**
All lesson and workflow contracts are available now. Implement one substage per reviewable PR;
retain the runnable predecessor and update findings after each real verification.

| Substage | Principal task | Read first | Acceptance gate |
|---|---|---|---|
| 01.1 | First flow and required dependency setup | Basics; WF-01; release boundary | Compatible pins; two-step chain first, then terminal result; CLI/PyCharm and dependency-aware isolated release work |
| 01.2 | Typed state | State lesson; WF-02 | Exact arithmetic/history; fresh state on repeat; invalid input rejected |
| 01.3 | Conditional routing | Routing lesson; WF-03 | Both routes and threshold boundaries; unchosen branch never runs |
| 01.4 | Failure behavior | Failures/tests lesson | Input vs execution failures; deliberate injected error stops successors; meaningful exit codes |
| 01.5 | Complete-stage verification | Running/releasing; test plan | Full gate; all workflows in installed release; source isolation; measured size and local IDE confirmation |

The runtime dependency work is necessary plumbing for 01.1, not an additional learning topic
bundled into the first flow. Explain it in the release lesson and keep changes focused.
For 01.1 begin with produce→decorate; add finish/output once that behavior is understood.
WF-02 and WF-03 remain separate examples and never replace WF-01.

## Before the first implementation PR

1. Review this complete package with Sharon and resolve proposed CLI/input semantics.
2. Re-read main and PR #28; record its final commit or any still-open compatibility issue.
3. Promote this folder into the permanent stage path; mark architecture/plan approved only
   after approval. Do not replace the top-level target architecture.
4. Probe CrewAI compatibility with Python 3.13, synchronous kickoff return/errors, strict
   input validation, telemetry disablement and exact locked release dependency installation.
5. Record chosen pins and probe evidence in findings. If the approved design cannot be
   met, bring the concrete discrepancy for review rather than hiding it with casts/mocks.

## Every implementation substage

Add only its workflow/capability and relevant tests. Preserve public CLI checks, versioning,
release selection and twelve existing IDE tasks. Explain each edited file's owner. Run the
full gate and applicable release checks. Present actual output, the exercise to try in
PyCharm, and the next small step. Do not mark later substages implemented in advance.

## Completion and version

Current reviewed main is 0.0.10; this documentation PR does not change it. First Stage 01
release is 0.1.0 using the existing exact-version script; later verified iterations can use
`version patch`. Choose the bump in its implementation PR, review/commit metadata, then build.
No automatic commit/push, no GitHub Actions, no Langfuse, no real agents in Stage 01.
