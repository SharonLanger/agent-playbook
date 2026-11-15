import os
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'
os.environ['CREWAI_TRACING_ENABLED'] = 'false'
os.environ.pop('OTEL_SDK_DISABLED', None)
for key in ('HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy'):
    os.environ.pop(key, None)
import sys
import traceback
network_attempts = []
def audit(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo'):
        network_attempts.append({'event': event, 'host': str(args[0]) if event == 'socket.getaddrinfo' else 'socket', 'stack': traceback.format_stack(limit=30)})
        raise RuntimeError('network prohibited in research probe')
sys.addaudithook(audit)

import asyncio
import json
import importlib.metadata as im
from pathlib import Path
from unittest.mock import patch
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ALWAYS_ON
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from langfuse import Langfuse, propagate_attributes
from openinference.instrumentation.crewai import CrewAIInstrumentor
from crewai.flow.flow import Flow, start, listen, router, and_, or_
from agent_playbook.workflows.wf_01_step_sequence.flow import StepSequenceFlow
from agent_playbook.workflows.wf_02_shared_state.flow import SharedStateFlow
from agent_playbook.workflows.wf_03_conditional_route.flow import ConditionalRouteFlow

provider = TracerProvider(sampler=ALWAYS_ON)
exporter = InMemorySpanExporter()
client = Langfuse(public_key='pk-lf-research', secret_key='sk-lf-research', base_url='http://127.0.0.1:3000', tracer_provider=provider, span_exporter=exporter, environment='research')
instrumentor = CrewAIInstrumentor()
instrumentor.instrument(tracer_provider=provider)
assert instrumentor.is_instrumented_by_opentelemetry
results = []

def collect(label, expected_nodes, expected_result, result, expected_error=False):
    client.flush()
    spans = exporter.get_finished_spans()
    exporter.clear()
    rows = [{'name': s.name, 'trace_id': f'{s.context.trace_id:032x}', 'span_id': f'{s.context.span_id:016x}', 'parent_span_id': f'{s.parent.span_id:016x}' if s.parent else None, 'status': s.status.status_code.name, 'attributes': dict(s.attributes or {}), 'event_names': [e.name for e in s.events], 'scope': s.instrumentation_scope.name} for s in spans]
    root = next(s for s in spans if s.name == label)
    flow = [s for s in spans if s.name.endswith('.kickoff')]
    assert len(flow) == 1, (label, rows)
    assert flow[0].parent.span_id == root.context.span_id
    assert len({s.context.trace_id for s in spans}) == 1
    assert len({s.context.span_id for s in spans}) == len(spans)
    nodes = [s for s in spans if 'flow.node.name' in (s.attributes or {})]
    assert sorted(s.attributes['flow.node.name'] for s in nodes) == sorted(expected_nodes)
    assert all(s.parent.span_id == flow[0].context.span_id for s in nodes), rows
    assert all(json.loads(s.attributes.get('langfuse.trace.metadata.workflow_id')) == 'research-' + label for s in spans), rows
    assert all(json.loads(s.attributes.get('langfuse.trace.metadata.workflow_run_id')) == 'run-' + label for s in spans), rows
    assert len(spans) == 2 + len(expected_nodes)
    assert result == expected_result
    assert not trace.get_current_span().get_span_context().is_valid
    if expected_error:
        assert root.status.status_code.name == 'ERROR'
        assert flow[0].status.status_code.name == 'ERROR'
        assert any(s.status.status_code.name == 'ERROR' for s in nodes)
    results.append({'case': label, 'result': result, 'spans': rows})

def run(label, cls, expected_nodes, expected_result, inputs=None, error=False):
    result = None
    try:
        with client.start_as_current_observation(as_type='span', name=label) as root:
            with propagate_attributes(metadata={'workflow_id': 'research-' + label, 'workflow_run_id': 'run-' + label}):
                result = cls().kickoff(inputs=inputs)
                assert root.trace_id == f'{trace.get_current_span().get_span_context().trace_id:032x}'
    except ValueError:
        if not error:
            raise
    collect(label, expected_nodes, expected_result, result, error)

class ConditionsFlow(Flow):
    @start()
    def begin(self): return 1
    @listen(begin)
    async def left(self, value):
        await asyncio.sleep(0)
        return value + 1
    @listen(begin)
    async def right(self, value):
        await asyncio.sleep(0)
        return value + 2
    @listen(and_(left, right))
    def joined(self, value): return 9
    @listen(or_(joined, 'never'))
    def finish(self, value): return value

run('wf01', StepSequenceFlow, ['produce', 'decorate', 'finish'], '[Hello, workflow!]')
run('wf02', SharedStateFlow, ['initialize', 'add', 'multiply', 'finish'], 20)
run('wf03-pass', ConditionalRouteFlow, ['begin', 'choose', 'accept'], 'pass', {'score': 80})
run('wf03-revise', ConditionalRouteFlow, ['begin', 'choose', 'revise'], 'needs_work', {'score': 20})
run('wf02-repeat', SharedStateFlow, ['initialize', 'add', 'multiply', 'finish'], 20)
with patch('agent_playbook.workflows.wf_02_shared_state.steps.multiply', side_effect=ValueError('controlled research failure')):
    run('wf02-failure', SharedStateFlow, ['initialize', 'add', 'multiply'], None, error=True)
run('conditions', ConditionsFlow, ['begin', 'left', 'right', 'joined', 'finish'], 9)

async def async_run(label):
    with client.start_as_current_observation(as_type='span', name=label):
        with propagate_attributes(metadata={'workflow_id': 'research-' + label, 'workflow_run_id': 'run-' + label}):
            value = await ConditionalRouteFlow().kickoff_async(inputs={'score': 80})
    collect(label, ['begin', 'choose', 'accept'], 'pass', value)
asyncio.run(async_run('wf03-async'))

assert len({r['spans'][0]['trace_id'] for r in results}) == len(results)
instrumentor.uninstrument()
client.shutdown()
out = {'python': sys.version, 'packages': {d.metadata['Name']: d.version for d in im.distributions()}, 'network_attempts': network_attempts, 'cases': results}
Path(__file__).with_name('results.json').write_text(json.dumps(out, indent=2, default=str))
print('PASS:', len(results), 'trace cases;', sum(len(r['spans']) for r in results), 'exported spans;', len(network_attempts), 'blocked socket/DNS attempts')
