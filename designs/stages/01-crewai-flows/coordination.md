# Coordination with the CLI refactor

## Implementation baseline — 2026-11-12

PR #28 is merged at `e5438169c620974193ecb88439c79aff8d836bf4`; its final head was
`48df8160cefcc58b9300427fe3e2a165a62a774c`. Main's package version was 0.0.11.
PR #29 merged at `4754bf4b03ef122e5e248ce1f6f5f600c2212f15` before this implementation.
The runtime work starts from that merged tree, preserving the final parser, tooling package,
pinned-uv resolver, path normalization, release decomposition and discovery parameter.

The release extension exports dependencies inside build_wheel while the committed archive
still exists, then installs/checks those dependencies through install_release. Completion
still requires successful installed verification; failed builds remain unverified. The CLI
forwards raw workflow arguments, leaving validation to the selected installation.

The application changes version from 0.0.11 to 0.1.0 for Stage 01. CrewAI CLI depends on uv;
a constraint keeps that transitive tool at the project's existing 0.13.6 pin. No refactor
work or user version increment was reverted. The earlier snapshot below is retained as history.

# Earlier design-review snapshot

Checked 2026-11-12. Repository: SharonLanger/agent-playbook.
Main reviewed: `4c9e74dcaf6897f6337f367dbbf17177bbada6c1` (version 0.0.10).
[PR #28](https://github.com/SharonLanger/agent-playbook/pull/28) reviewed head:
`abdb0ae17927648eaee44e11a9d8b3b596075f0c` (open; 14 changed files).
The first read contained only the handoff. A second read before publishing this design found
implementation code. The complete published diff was reviewed; it is not yet in main.

## Published changes and integration points

| Refactor area | Observed code at this head | Stage 01 interaction |
|---|---|---|
| Consistent tooling imports | `tooling/__init__.py`, package-qualified imports, script entry bootstrap | Reuse it; do not restore test-level sys.path patches |
| Pinned uv discovery | `tooling/toolchain.py`: `pinned_uv`, `private_uv_path`, `UV_VERSION` | Reuse resolver for locked dependency installation |
| Smaller release operations | Source validation, archive/wheel build, manifest, install and installed verification are extracted functions | Extend the install/build evidence boundaries, keeping the same completion gate |
| Parser / argv | `build_parser()` and `main(argv=None)` | Add workflow/input options to the existing parser |
| Output-path normalization | `--output` resolved in CLI before forwarding | Preserve caller-relative path semantics |
| Release discovery | `find_release(..., releases_dir=None)` | Preserve selection; add workflow argv forwarding separately |
| Regression coverage | New resolver, CLI output, explicit directory and failed-verification cases | Preserve these and add Stage 01 behavior coverage |

The published code still installs only the application wheel with `--no-deps`.
`install_release` is the current integration point, but exporting the archived lockfile also
requires coordination with `build_wheel`'s temporary archive lifetime. Do not export from a
mutable checkout after archive disposal. The Stage 01 implementation can adjust those helper
signatures together rather than freezing private APIs in this proposal.

Main currently has no runtime dependencies and installs the application wheel with `--no-deps`.
The refactor leaves this behavior unchanged. Stage 01 explicitly proposes installing
locked runtime dependencies before the wheel. Coordinate this extension after the refactor;
do not remove reproducibility checks or silently rely on the development virtualenv.

## Compatibility we retain

`check` and selectors, `format`, `test`, `version`, `version patch`, `release [--output]`,
`run --version`, and direct-script entry points remain supported. No additional tool registry
or global utils module. The new workflow arguments must reach the selected release as argv
entries without shell concatenation; a raw JSON string remains one entry. Validate workflow
input inside the selected application, not against the launching checkout's newer schema.

No runtime/tooling files are edited in this documentation branch. Do not merge PR #28 into
this design branch solely for convenience; inspect its final tree and rebase/reconcile later.
The PR description reports its handoff removed from the final diff, which now contains only
application code/tests. This branch does not alter the other agent's cleanup.

## Before approving implementation

Re-fetch PR #28's head, changed files and main. Record new SHAs here/findings, inspect any changed
CLI/release contracts, and reconcile affected design statements. Do this again before code
work if the refactor changes after design review. A snapshot is not an ongoing synchronization
promise. No message has been sent to the other agent or posted on PR #28.
