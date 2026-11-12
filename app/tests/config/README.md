# Configuration tests

`test_configuration.py` verifies file selection, nested local overrides, environment
precedence/references, startup validation, private errors, import ordering and reload
on the next invocation. The root test setup uses `tests/fixtures/offline.yaml` so
personal settings cannot silently change the test suite's network policy.
