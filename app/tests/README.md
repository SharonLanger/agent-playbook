# Tests

Tests are grouped by the component they exercise: `cli`, `application`,
`workflows`, `execution`, `observability`, `config`, and `releases` mirror runtime
boundaries. `tooling` tests checkout-only developer tools; `examples` tests learning
exercises. Reserved directories contain a README until tests are needed.

Run all tests with `agent-playbook test` or the shared PyCharm **Tests** task.
The full **Check** task also checks source, tooling, examples and tests.
