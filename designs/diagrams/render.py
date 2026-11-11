"""Regenerate paired animated/static architecture SVGs. Python standard library only."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
COLORS = {'flow':'#69d9ce','agent':'#f5ba77','observe':'#b4a3ff','failure':'#ff8d9a','neutral':'#a2b7ca'}


def render(name, number, title, subtitle, height, nodes, edges, notes):
    for animated in (False, True):
        parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}. Animation illustrates direction only; this is an architecture diagram, not live execution data.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0c1725"/><stop offset="1" stop-color="#15263a"/></linearGradient>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>
<style>text{{font-family:Inter,Arial,sans-serif}} .pulse{{filter:none}} @media(prefers-reduced-motion:reduce){{.pulse{{display:none}}}}</style>
<rect width="1200" height="{height}" rx="24" fill="url(#bg)"/>
<text x="40" y="43" fill="#69d9ce" font-size="13" font-weight="700" letter-spacing="2">AGENT PLAYBOOK  /  {number}</text>
<text x="40" y="91" fill="#f1f6fc" font-size="34" font-weight="700">{escape(title)}</text>
<text x="40" y="125" fill="#a2b7ca" font-size="17">{escape(subtitle)}</text>''']
        for idx, (path, kind, label, lx, ly) in enumerate(edges):
            c=COLORS[kind]
            parts.append(f'<path d="{path}" fill="none" stroke="{c}" stroke-opacity=".65" stroke-width="2" marker-end="url(#arrow)"/>')
            if label:
                width=len(label)*7.7+16
                parts.append(f'<rect x="{lx-8}" y="{ly-17}" width="{width}" height="24" rx="5" fill="#101e2e"/><text x="{lx}" y="{ly}" fill="{c}" font-size="14">{escape(label)}</text>')
            if animated:
                parts.append(f'<circle class="pulse" r="4" fill="{c}"><animateMotion path="{path}" dur="3.6s" begin="{-idx*.47}s" repeatCount="indefinite"/></circle>')
        for x,y,w,h,label,lines,kind in nodes:
            c=COLORS[kind]
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#192b40" stroke="{c}" stroke-opacity=".6"/><rect x="{x+1}" y="{y+17}" width="4" height="{h-34}" rx="2" fill="{c}"/><text x="{x+20}" y="{y+32}" fill="#f1f6fc" font-size="19" font-weight="700">{escape(label)}</text>')
            for i,line in enumerate(lines):
                parts.append(f'<text x="{x+20}" y="{y+58+i*22}" fill="#b9cada" font-size="15">{escape(line)}</text>')
        parts.append(f'<line x1="40" y1="{height-100}" x2="1160" y2="{height-100}" stroke="#34475c"/>')
        for i,line in enumerate(notes):
            parts.append(f'<text x="40" y="{height-70+i*24}" fill="#b9cada" font-size="15">{escape(line)}</text>')
        parts.append('</svg>')
        suffix='.animated.svg' if animated else '.svg'
        (ROOT/(name+suffix)).write_text('\n'.join(parts))


render('01-system', '01', 'The target system', 'Responsibilities and integration boundaries • one application, replaceable integrations', 1120, [
(40,170,300,100,'Configuration',['Providers, endpoints, secrets','Validated before execution'],'neutral'),
(450,170,300,100,'CLI / PyCharm',['Choose workflow and input','Start a run'],'flow'),
(860,170,300,100,'Workflow definitions',['Typed inputs, steps, routing','Completion and failure rules'],'neutral'),
(450,340,300,100,'Application runner',['Validate and assemble','Create run ID; return outcome'],'flow'),
(450,510,300,100,'CrewAI Flows',['Coordinate steps and branches','Own workflow execution state'],'flow'),
(40,710,300,100,'Python steps',['Deterministic transformations','Validation and ordinary logic'],'flow'),
(450,710,300,100,'Agent execution contract',['Task + execution settings','Structured result or error'],'agent'),
(860,510,300,100,'Observability contract',['Correlated execution events','Redacted, provider-neutral data'],'observe'),
(860,710,300,100,'Langfuse adapter',['Publish traces and spans','Inspect execution in its UI'],'observe'),
(400,910,220,80,'Claude adapter',['SDK-specific execution'],'agent'),
(650,910,220,80,'Codex adapter',['SDK-specific execution'],'agent'),
(900,910,220,80,'Test executor',['Controlled results/errors'],'agent')], [
('M340 220 H390 V390 H450','neutral','',0,0),('M600 270 V340','flow','',0,0),('M860 220 H810 V390 H750','neutral','',0,0),
('M600 440 V510','flow','start workflow',615,479),('M450 560 H190 V710','flow','execute',205,645),('M600 610 V710','agent','invoke agent step',615,665),
('M750 420 H795 V550 H860','observe','events',800,479),('M750 580 H860','observe','events',771,572),('M1010 610 V710','observe','publish',1025,665),
('M600 810 V860 H510 V910','agent','',0,0),('M600 860 H760 V910','agent','',0,0),('M760 860 H1010 V910','agent','select implementation',822,850)
], ['Teal: workflow control   •   Amber: execution implementations   •   Purple: observation', 'Adapter boxes express responsibilities; SDK language/process boundaries are chosen during integration.'])

render('02-execution','02','One workflow run','Control flow • validate, execute, inspect a result, and finish or handle failure',1030,[
(450,170,300,80,'Start run',['Workflow selection + input'],'flow'),
(450,300,300,80,'Validate and configure',['Input, required settings, provider'],'flow'),
(860,300,300,80,'Reject request',['Return actionable error'],'failure'),
(450,440,300,80,'Select workflow step',['Use state and routing rules'],'flow'),
(450,570,300,80,'Execute step',['Python logic or agent adapter'],'agent'),
(450,700,300,80,'Validate step result',['Update state; evaluate route'],'flow'),
(860,700,300,100,'Failure policy',['Bounded retry, fallback or fail','Never silently report success'],'failure'),
(450,840,300,80,'Finish run',['Output, run ID and exit status'],'flow')],[
('M600 250 V300','flow','',0,0),('M750 340 H860','failure','invalid',775,328),('M600 380 V440','flow','valid',615,417),
('M600 520 V570','flow','',0,0),('M600 650 V700','agent','result / error',615,685),('M750 740 H860','failure','error',785,727),
('M450 740 H340 V480 H450','flow','next step',260,550),('M600 780 V840','flow','complete',615,823),
('M1010 700 V610 H750','failure','retry if permitted',852,599),('M1010 800 V880 H750','failure','unrecovered',887,868)
],['Workflow policy decides retries and fallback. Exact retry counts and SDK cancellation behavior are explicit integration decisions.', 'This is a conceptual execution model, not a claim that crash recovery or durable checkpoints already exist.'])

render('03-observability','03','Follow the execution','Observation flow • connect the workflow run, its steps and agent sessions',900,[
(40,190,300,100,'Application runner',['Run started / completed / failed','run_id'],'flow'),
(450,190,300,100,'Workflow steps',['Step start, result, error','run_id + step_id'],'flow'),
(860,190,300,100,'Agent adapter',['Execution and session events','run_id + step_id + session_id'],'agent'),
(450,410,300,100,'Observability boundary',['Normalize, correlate, redact','Publish through selected adapter'],'observe'),
(450,630,300,100,'Langfuse trace',['Run → step → agent spans','Inspect timing, status and errors'],'observe'),
(860,630,300,100,'Workflow state',['Owned by workflow execution','Not reconstructed from traces'],'neutral')],[
('M190 290 V360 H530 V410','observe','run events',245,350),('M600 290 V410','observe','step events',615,348),('M1010 290 V360 H670 V410','observe','agent events',817,350),('M600 510 V630','observe','export',615,578)
],['Traces explain execution. They do not schedule steps or control the workflow.', 'Telemetry failure handling, redaction rules and retention limits must be specified before integration is accepted.'])
