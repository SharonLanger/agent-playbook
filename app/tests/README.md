# Tests

Tests are grouped by the component they exercise: `cli`, `application`,
`workflows`, `execution`, `observability`, `config`, and `releases` mirror runtime
boundaries. `tooling` tests checkout-only developer tools. Application tests and fixtures
must exercise `src/agent_playbook`, never import from `app/examples/`. Reserved
directories contain a README until tests are needed.

Run all tests with `agent-playbook test` or the shared PyCharm **Tests** task.
The full **Check** task checks source, tooling and tests. The personal
`app/examples/` sandbox is outside all automatic gates.
