# 00.5 — Ruff

Bootstrap installs Ruff and runs checks without modifying source.
From repository root after environment activation:

```sh
python -m ruff check app/src app/tooling app/examples app/tests
python -m ruff format --check app/src app/tooling app/examples app/tests
```

Try one defect at a time in typing_example.py:

1. Add an unused `import math`. Lint reports an error. Remove it.
2. Change the guest string's double quotes to single quotes. Format verification
   reports the file would change. Run `python -m ruff format app/examples/typing_example.py`
   to restore canonical formatting.
3. Rerun both checks, Pyright and `agent-playbook test`.

Lint detects selected coding problems; formatting checks layout. Neither replaces
behavioral tests or static typing. No auto-fix is hidden in bootstrap. PyCharm can
run module `ruff` with the same arguments (paths relative to its working directory).
