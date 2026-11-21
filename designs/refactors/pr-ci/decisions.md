# Decisions and alignment

2026-11-21. Sharon selected every-PR offline checks, local versioning and clone-and-build distribution. Main already supplies the local gate, wheel builder, checksum, clean installation and offline regression fixtures. The previous patch-only public CLI and stage-number convention are insufficient for his requested bumps.

| ID | Decision |
|---|---|
| D1 | One standard macOS runner with pinned Python 3.13.5 and uv 0.13.6. Evidence applies to that runner. Use the guard and Linux/Windows-neutral application contracts already in the repo. |
| D2 | Include Pyright, Ruff lint and format verification, maintained pytest, Atlas and wheel verification. Exclude every live service and provider, including future ones. No dependency on #57. |
| D3 | Keep hosted jobs dormant while private. After Sharon makes the repository public, verify the named check and configure main with an explicit administrator PR-only bypass. |
| D4 | Bump only for an intentional version. A patch is a compatible fix. A minor can add features or introduce documented breaking changes in 0.x. Major resets both lower fields and 1.0 is an explicit stability decision. |
| D5 | Build and identify local wheels by version, commit and SHA-256. No CD publisher, tags, registry, release drafts or automatic bumps. |
| D6 | Maintain a short dated list of merged PRs for each new version. Detailed release narratives are deferred. |

At the baseline, GitHub reported unprotected main, zero Actions runs and a private-plan ruleset restriction. #59 is merged. #57, #51 and #45 own separate work. Stage 00 contains historical local-only CI and stage-based versioning text. The design lists exact amendments before implementation. Relevant explorations introduce no CI or distribution prerequisite. Hosted execution, wheel identity for a new candidate and actual protection are unverified. The work is ready for a concrete design lock.
