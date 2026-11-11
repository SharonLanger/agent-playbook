# 00.3 — Static typing with Pyright

Goal: see a type error before executing Python. Keep your CLI from 00.2.

From repository root, macOS/Linux:

```sh
python3 app/tooling/bootstrap.py
source app/.venv/bin/activate
cd app
python -m pyright
```

Windows: `py -3 app/tooling/bootstrap.py`, then use `app/.venv/Scripts/python.exe`
with `-m pyright --project app/pyproject.toml` from repository root.

Edit `app/examples/typing_example.py`. Make **one change at a time**,
run Pyright, observe its diagnostic, then undo that change and rerun to zero errors.

| Experiment | Change | Expected diagnostic |
|---|---|---|
| Wrong argument | Append `Greeter().greet(42)` | int is incompatible with str |
| Wrong return | Replace greet's return with `return 42` | int is incompatible with declared str return |
| Optional value | Remove the `if name is None` block | str or None cannot be passed where str is required |

`str | None` resembles a nullable type in TypeScript/C#. The guard narrows it to
`str`. Unlike a Java compilation gate, Python itself can still execute code with
incorrect annotations: Pyright is a separate tool that must be run.

PyCharm: configure a Python run with **Module name** `pyright`, working directory
`<repo>/app`, and the existing `.venv` interpreter. Run it to see Pyright's output.
PyCharm's native editor inspections are separate; no Pyright editor integration
is installed or assumed. Actual PyCharm UI behavior requires your local check.

The Python Pyright distribution wraps Microsoft's checker and uses Node.js. It
uses an available Node installation or provisions one through its dependency;
initial provisioning needs network access. Bootstrap executes Pyright so this
happens within the single setup command. No mypy, pytest or Ruff in this substage.
