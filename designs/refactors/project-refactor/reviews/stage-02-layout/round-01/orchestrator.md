# Stage 02 layout — round 1 disposition

Candidate: `ab94509cedf9f01eedaa32a4546ecdfafcc879e5`. Base: `13bebb0d824cf9b2d1794a0cbff2311fbd99489c`. PR [#67](https://github.com/SharonLanger/agent-playbook/pull/67), draft and unmerged. Orchestrator: originating design session; exact model identifier was not exposed. Coder and both independent reviewers were configured as `gpt-6.2-sol`.

**CHANGES REQUIRED.** [Coder evidence](implementation.md), [design-drift review](design-drift.md), and [test-gap review](test-gap.md) cover the same frozen candidate. Migration, guard, research-byte and link checks passed; semantic navigation review found the following required corrections.

| Finding | Disposition |
|---|---|
| DD01 / TG01 | Correct active Atlas labels so dated handoffs/reviews are identified as history and approved M4.1 contracts are not described as drafts. Preserve original verdicts. |
| DD02 / TG02 | Explicitly date the prior PR #59 layout table and map both former M4 subfolder names to their current locations. |
| DD03 | Keep the literal `#start-here` anchor but place it above the current reading order. |

The maintained Atlas check and path validation passing do not establish accurate status prose. Route these corrections to the same coder and review the next frozen candidate with both reviewers. Round 1 of 3 used; no merge authorized.
