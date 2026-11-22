# Local logging tooling

Checkout-only tools for the local VictoriaLogs service and explicit checks.

| File | Purpose |
|---|---|
| `manage.py` | Start, inspect or stop VictoriaLogs through `agent-playbook logs` |
| `compose.yaml` | Local VictoriaLogs container, network and retained volume |
| `logging_smoke.py` | Emit a synthetic record for manual ingestion/UI verification |
| `check_services.py` | Read-only checks of configured Langfuse and logging connections |

All commands below run from the repository root after bootstrap. For service
commands and configuration, see the [CLI guide](../../docs/cli.md#local-services)
and [application logging guide](../../docs/logging.md).

## Local logging smoke

This opt-in checkout tool emits one synthetic INFO record using the OpenTelemetry
SDK directly to VictoriaLogs. It is separate from normal workflow logging and
does not configure Langfuse or the application runner.

Use a local Docker daemon and local volume. Docker Engine 28+ is required for the
documented loopback publishing semantics (older engines have a same-L2 exposure
caveat). Install the Docker Compose plugin and bootstrap the application Python environment.
The earlier setup was checked with Docker CLI 29.9.2 and Compose 2.40.3 on Linux.
An initial Docker Desktop/macOS run failed to publish port 9428 on the former
internal-only network; the configuration now uses an ordinary bridge.
The logging refactor subsequently closed on accepted Mac service/workflow sanity
checks, including visible VictoriaLogs records. See the
[logging progress record](../../../designs/refactors/logging/progress.md) for
that acceptance and the detailed live checks still outstanding. Each synthetic
smoke run below requires its own record inspection to confirm delivery.

From the repository root:

```sh
docker version
docker compose version
docker context show
app/.venv/bin/agent-playbook logs --start
app/.venv/bin/agent-playbook logs --status
app/.venv/bin/python app/tooling/logging/logging_smoke.py --endpoint http://127.0.0.1:9428/insert/opentelemetry/v1/logs
```

Check that the selected Docker context uses your local daemon, not a remote host.
The logging CLI pins the project name to `agent-playbook-logging-smoke` and manages only VictoriaLogs. Use `app/.venv/bin/agent-playbook services --start` to select local components by enabled flags.
The only service is `victoriametrics/victoria-logs:v1.54.0`, with a local named
volume, seven-day retention, local Docker logging driver, loopback port 9428 and
one ordinary bridge network. Change `-retentionPeriod=7d` in this component's Compose file
to change retention. The ordinary bridge allows container outbound traffic;
localhost publishing restricts inbound access to this host, not outbound traffic.
This setup relies on local VictoriaLogs configuration and software behavior, not
an enforced outbound firewall. Do not attach it to Langfuse networks.

The explicit argument above is also the script's documented default. Only
`http://127.0.0.1[:PORT]/insert/opentelemetry/v1/logs` is accepted. If changing the
host port, update both the Compose publication and the argument. The Requests
session ignores environment proxies and refuses redirects; there is no remote
fallback. The probe uses SDK/exporter 1.45.2 and logging instrumentation 0.66b2
from `app/uv.lock`, a dedicated non-propagating logger and a dedicated provider.
The export timeout is five seconds. The probe also requests a five-second
force-flush timeout, but the pinned SDK batch processor currently ignores that
argument and flushes synchronously. SDK shutdown is attempted in `finally` (its
batch worker join has a 30-second SDK default). These are cleanup attempts, not a
delivery or hard whole-process deadline guarantee.

For port diagnosis, the matching `docker compose ps` output should show `127.0.0.1:9428->9428/tcp`; `9428/tcp` alone
means the host port was not published. `down` removes this component's container
and network but keeps the named volume; never use `down -v` here. Recreating the
network is necessary when moving from the old internal-only configuration.

Open <http://127.0.0.1:9428/select/vmui> after the script exits. Paste this LogsQL
query, replacing the value with the printed correlation:

```text
correlation_id:="PRINTED-UUID"
```

Inspect the matching record: message `Logging smoke check`, severity `INFO`,
`workflow_id=logging-smoke`, a synthetic `workflow_run_id`, and the printed
`correlation_id`. One unique correlation is generated per probe. Seeing this
actual record after cleanup is the smoke's integration acceptance. A zero exit,
SDK flush result or healthy UI alone does not establish delivery; the script
therefore always prints **Delivery unconfirmed** until you inspect the record.

If startup/export fails, inspect the service and retry the explicit probe after
fixing the local service:

```sh
app/.venv/bin/agent-playbook logs --status
docker compose -p agent-playbook-logging-smoke -f app/tooling/logging/compose.yaml ps
docker compose -p agent-playbook-logging-smoke -f app/tooling/logging/compose.yaml logs --tail 50 victorialogs
app/.venv/bin/agent-playbook logs --stop
```

Stopping retains the volume; successful smoke cleanup never deletes data. Batching
is in memory and can lose records. This checks synthetic data only, not durability,
outage recovery, disk bounds, security auditing or host-wide prevention of
forwarding. Never substitute prompts, credentials or whole configuration objects.

Selected project licenses are Apache-2.0:
[VictoriaLogs v1.54.0](https://github.com/VictoriaMetrics/VictoriaLogs/blob/v1.54.0/LICENSE),
[OTel SDK/exporter v1.45.2](https://github.com/open-telemetry/opentelemetry-python/blob/v1.45.2/LICENSE),
and [logging instrumentation v0.66b2](https://github.com/open-telemetry/opentelemetry-python-contrib/blob/v0.66b2/LICENSE).
These project licenses do not certify all transitive dependencies or container layers.


## Application integration and explicit checks

Application workflow logging is configured through the existing YAML loader; see
[Application logging](../../docs/logging.md) for defaults, helper calls, safe
failure behavior and limitations. Run the read-only diagnostic explicitly:

```bash
app/.venv/bin/python app/tooling/logging/check_services.py --config app/application.yaml
```

The VictoriaLogs check uses the selected release's `/health` endpoint (HTTP 200),
without writes, proxies or redirects; local direct deployment authentication is
not applicable. Health success is distinct from the smoke's ingestion/UI check.
