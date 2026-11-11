# 00.4 — pytest

From repository root, run the same bootstrap and activate app/.venv.

```sh
agent-playbook test
```

Read app/tests/test_greeting.py. Temporarily change the `greeting(None)` result in
src/agent_playbook/typing_example.py from `Hello, guest!` to `Hello, visitor!`.
Run `agent-playbook test`: the regression should fail. Undo just that edit and
rerun: all tests pass. This tests behavior; Pyright can accept either string.

`test` is development-only: it requires the source checkout and installed pytest.
In PyCharm, run module `agent_playbook.cli`, parameters `test`, interpreter app/.venv.
The command uses the interpreter that launched the CLI, not a global pytest.
