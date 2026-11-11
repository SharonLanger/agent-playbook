# 00.7 — Versioned isolated release

Run bootstrap and activate app/.venv. This lesson requires Git and a **clean,
committed checkout**. Release creation refuses uncommitted/untracked changes.

From repository root:

```sh
agent-playbook check
agent-playbook version
python app/scripts/release.py
```

Development reports version 0.0.1 and source `development`. The script checks the
clean checkout, runs the gate, archives the exact Git revision, embeds that revision
in the archived build source, builds one Wheel, records its SHA-256, verifies it,
and installs it non-editably into a clean environment. It runs the installed code
and checks its metadata, import location, and refusal of developer commands.
The source checkout's _build_info.py is not modified.

The final line identifies `app/dist/0.0.1-<commit-prefix>/`, or a numbered
`-2`, `-3`, and so on when you run Release again. It contains:

- The Wheel, `SHA256SUMS`, and `release.json` (version, source commit, file, hash).
- `venv/`, the independent installed release. `test` and `check` intentionally fail.

Run the same command again without changing parameters; it chooses the next free
folder and preserves existing output. An explicit `--output` must name a new folder.
No package registry upload or GitHub release is created.

After building, `agent-playbook run` selects the newest installed release. Use
`agent-playbook run --version 0.0.1` for the newest matching version, or
`agent-playbook dev-run` to run editable source. See [CLI and releases](../../../../app/docs/cli.md)
for all commands and selection rules.

## Verify and demonstrate independence

Replace `<release-dir>`, `<wheel>` and `<recorded-sha256>` with the printed values:

```sh
python app/scripts/verify_wheel.py <release-dir>/<wheel> <recorded-sha256>
<release-dir>/venv/bin/agent-playbook version
<release-dir>/venv/bin/agent-playbook run
```

Windows uses `<release-dir>/venv/Scripts/agent-playbook.exe`.

1. Change the message in app/src/agent_playbook/__main__.py locally.
2. Run the development `agent-playbook run`: it changes immediately.
3. Run the explicit installed release command: its message stays unchanged.
4. Undo only your message edit. Never discard unrelated edits.
5. Corrupt a **copy** of the Wheel and run verify_wheel.py with the original digest:
   verification must fail. Keep the original artifact intact.

A Wheel packages files; it is not a Java-like compiled binary. Version/commit
metadata is self-reporting. SHA-256 checks exact bytes against a trusted recorded
digest; it is not a signature or proof of who built the artifact. Keep digest and
artifact evidence together, and trust the digest source before installation.
