# Shared learning and root sandbox implementation, round 01

- Author role: Coder. Model: `gpt-6.2-sol`. Date: 2026-11-19.
- Draft PR [#59](https://github.com/SharonLanger/agent-playbook/pull/59), branch `docs/project-refactor`.
- Migration base `ef7b22492d6091c8c4b47c4226a24550a9b23ccb`.
- [Frozen candidate `b7d255dedaece9dae805b9a82338e68b8cdaa26d`](https://github.com/SharonLanger/agent-playbook/commit/b7d255dedaece9dae805b9a82338e68b8cdaa26d), tree `0ecb0f8b9e950ee5f85fc778ada57eeca757f832`.
- [Migration scope, approval and applied dispositions](../../../learning-sandbox-migration.md).

## Verification

| ID | Observed result |
| --- | --- |
| LSM01 | PASS. The 19 disposition rows match the exact two learning and 17 sandbox source paths. The old shared-learning directory has no tracked files. Root sandbox contains exactly eight Markdown files, including its two maintenance files. |
| LSM02 | PASS. The moved walkthrough matches its source after reverting the two diagram link edits. The existing target SVG parsed and the local viewer HTML resolved. The design index links to the new walkthrough and both stage teaching indexes. |
| LSM03 | PASS. After removing provenance framing and reversing the scoped link changes, all six moved document bodies match their source bytes. The three idea IDs, inspection revisions and draft approval caveats remain. The references treat former operational permissions and paths as historical. The reviewer keeps the explicit destination requirement. |
| LSM04 | PASS. The archived design and PR rules match source blobs `0f2950ad131a031a39070b4b1bdfaaf7f537fd30` and `80259fb4afa3f929f6c5a42e02aff2e2c136df06`. The existing relative link resolves within the archive. All seven placeholders are absent from the working tree and accessible at the pinned source revision. |
| LSM05 | PASS. Atlas generation and `python3 designs/atlas/build.py --check` succeeded. Current shows the moved walkthrough with draft PR attribution and omits sandbox internals. Explorations attributes the 19 former paths to the immutable main snapshot. The changed documents and Atlas HTML had 155 checked relative links, 4 checked anchors and 34 checked pinned references. An inbound link scan covered 211 candidate Markdown files without a live link to a retired path. |
| LSM06 | PASS. The Git tree matched the 38-path addition, removal and modification allowlist, or 29 entries when nine renames are recognized. The architecture diff changed one link. The project structure diff changed only the approved ownership rows. The application, stage, governance and earlier project-refactor review subtree hashes were identical. The whitespace check passed. Changed files contained no Drive URLs or any of the five unique identifiers from the ten original link targets. The published PR was verified open, draft and unmerged, and main remained at `cdbc06c2e9a9b87910b5145ac116aeb8a81e06e4`. |

Preflight rescanned 380 tracked design, source, configuration and template files for legacy path references without accessing personal examples. The application gate did not run because the task changed documentation only. The existing diagram assets were kept byte-identical. The generated Atlas was validated through its builder and link checks.

PRs #45 and #51 overlap on shared navigation or generated Atlas paths. PR #57 has no migration-path overlap. This publication changed only the authorized branch through an expected-head, non-force ref update. Independent review and Sharon's final disposition are tracked separately.
