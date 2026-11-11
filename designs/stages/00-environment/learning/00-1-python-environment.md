# 00.1 — Which Python executes my code?

Goal: prepare one environment, run `main()`, and debug it in PyCharm.
Follow [app/README.md](../../../../app/README.md) for the commands.

| Familiar concept | This exercise |
|---|---|
| Node runtime / JVM | Python interpreter; `.python-version` selects 3.13.5 |
| `package.json` / build metadata | `pyproject.toml` declares the project and supported Python range |
| Lockfile | `uv.lock` records the dependency resolution; currently no dependencies |
| Per-project dependencies | `.venv` isolates the interpreter environment and installed packages |
| Program entry point | `main()` called by the `if __name__ == "__main__"` guard |

uv prepares the environment; Python executes the source. No application build or
static type-checking gate exists yet. Python type annotations alone do not enforce
types at runtime. Running the file sets its `__name__` to `"__main__"`; importing
it defines the function without calling it.

1. Run bootstrap and locate the interpreter path it prints.
2. Run bootstrap again. Observe that the environment is reused.
3. Run the entry-point file independently with `.venv`'s Python.
4. Select that same interpreter in PyCharm and debug the `print` line.
5. Change the printed message locally and run again. Source execution immediately
   reflects your edit; restore it after the experiment.

Stop here. The next substage adds the application CLI to call this same `main()`.
