"""Build the self-contained local SVG gallery using standard Python only."""
from pathlib import Path

root=Path(__file__).resolve().parent
names=['01-system','02-execution','03-observability']
titles=['System structure','One workflow run','Observation flow']
views=[]
for i,name in enumerate(names):
    svg=(root/(name+'.animated.svg')).read_text()
    for ident in ['title','desc','bg','arrow']:
        svg=svg.replace(f'id="{ident}"',f'id="{name}-{ident}"').replace(f'#{ident})',f'#{name}-{ident})')
    svg=svg.replace('aria-labelledby="title desc"',f'aria-labelledby="{name}-title {name}-desc"')
    views.append(f'<section class="view" id="view-{i}" {"" if i==0 else "hidden"}>{svg}</section>')
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Playbook · Architecture</title><style>
*{box-sizing:border-box}body{margin:0;background:#08121e;color:#edf5ff;font-family:Arial,sans-serif}main{max-width:1280px;margin:auto;padding:32px 24px}header{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:24px}h1{font-size:25px;margin:0 0 8px}p{color:#a2b7ca;margin:0;line-height:1.5}nav,.controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}button{font:inherit;color:#c4d4e5;background:#14253a;border:1px solid #36516b;border-radius:8px;padding:11px 16px;cursor:pointer}button[aria-pressed="true"],button[aria-selected="true"]{background:#163f43;border-color:#69d9ce;color:#b7fff4}button:focus-visible{outline:3px solid #f5ba77;outline-offset:3px}.view svg{display:block;width:100%;height:auto}.static .pulse{display:none}footer{padding:20px 0;color:#a2b7ca;font-size:14px}@media(max-width:620px){main{padding:18px 10px}header{display:block}h1{font-size:22px}.controls{margin-top:18px}button{padding:10px;font-size:14px}}
</style></head><body><main><header><div><h1>Agent Playbook / Architecture</h1><p>The target system, one execution, and the evidence it leaves.</p></div><div class="controls"><button id="pause" aria-pressed="false">Pause motion</button><button id="static" aria-pressed="false">Static view</button></div></header><nav aria-label="Diagram selection">'''
html+=''.join(f'<button data-view="{i}" aria-pressed="{str(i==0).lower()}">{i+1:02} · {title}</button>' for i,title in enumerate(titles))
html+='</nav>'+''.join(views)+'''<footer>Illustrative motion · No live data · No external requests · Target design; see progress.md for implementation status.</footer></main><script>
const svgs=[...document.querySelectorAll('svg')];let paused=false;
document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.view').forEach((v,i)=>v.hidden=i!==Number(button.dataset.view));}));
document.querySelector('#pause').addEventListener('click',function(){paused=!paused;svgs.forEach(s=>paused?s.pauseAnimations():s.unpauseAnimations());this.setAttribute('aria-pressed',String(paused));this.textContent=paused?'Resume motion':'Pause motion';});
document.querySelector('#static').addEventListener('click',function(){const active=document.body.classList.toggle('static');this.setAttribute('aria-pressed',String(active));this.textContent=active?'Animated view':'Static view';});
</script></body></html>'''
(root/'index.html').write_text(html)
