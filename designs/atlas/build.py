#!/usr/bin/env python3
"""Build/check the offline Atlas. Standard library only; never traverse examples."""
from pathlib import Path
import argparse
import base64
import hashlib
import html
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def source(path: str) -> Path:
    candidate = (ROOT / path).resolve()
    relative = candidate.relative_to(ROOT).as_posix()
    if relative == 'app/examples' or relative.startswith('app/examples/'):
        raise ValueError('Personal sandbox must not be accessed: ' + path)
    if not candidate.is_file():
        raise ValueError('Missing referenced file: ' + path)
    return candidate


def build() -> str:
    data = json.loads((HERE / 'catalog.json').read_text())
    if set(data['views']) != {'current', 'explorations'}:
        raise ValueError('Current and Explorations views are required')
    for mode, view in data['views'].items():
        nodes = view['levels']
        if nodes['repo']['parent'] is not None:
            raise ValueError('Repository must be the root')
        reached = set()
        def visit(key):
            if key in reached:
                return
            reached.add(key)
            node = nodes[key]
            expected = {'exploration'} if mode == 'explorations' else {'implemented', 'approved-design'}
            if node['status'] not in expected:
                raise ValueError('Invalid node status: ' + key)
            source(node['source'])
            ancestors = {key}
            parent = node['parent']
            while parent is not None:
                if parent in ancestors:
                    raise ValueError('Hierarchy cycle: ' + key)
                ancestors.add(parent)
                parent = nodes[parent]['parent']
            if node.get('diagram') and node['diagram'] not in data['diagrams']:
                raise ValueError('Missing diagram: ' + key)
            for block in node['blocks']:
                if block.get('to'):
                    visit(block['to'])
        visit('repo')
        if reached != set(nodes):
            raise ValueError('Unreachable architecture block')
        paths = [item['path'] for item in view['files']]
        if len(paths) != len(set(paths)):
            raise ValueError('Duplicate inventory paths')
        if any(p.startswith('app/examples/') and p != 'app/examples/' for p in paths):
            raise ValueError('Sandbox contents cannot be inventoried')
    register = source('designs/governance/guarded-files.md').read_text()
    guarded = re.findall(r'^- `(designs/[^`]+\.md)`', register, re.M)
    if not guarded:
        raise ValueError('Guard register is empty')
    # Check registered paths, not their historical heading: stale labels do not unguard them.
    for path in guarded:
        source(path)
    for path in ['designs/charter.md', 'designs/principles.md', 'designs/architecture.md',
                 'designs/project-structure.md', 'designs/governance/design-contract.md']:
        if path not in guarded or 'GUARDED' not in source(path).read_text():
            raise ValueError('Core guard missing: ' + path)
    inputs = sorted(set(data['sources'] + guarded))
    digest = hashlib.sha256()
    for path in inputs:
        digest.update(path.encode())
        digest.update(source(path).read_bytes())
    for diagram in data['diagrams'].values():
        for kind in ('static', 'animated'):
            path = 'designs/atlas/' + diagram[kind]
            raw = source(path).read_bytes()
            diagram[kind] = 'data:image/svg+xml;base64,' + base64.b64encode(raw).decode()
    data['source_fingerprint'] = digest.hexdigest()
    encoded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    return (HERE / 'template.html').read_text().replace('@@DATA@@', encoded).replace(
        '@@SNAPSHOT@@', html.escape(data['snapshot']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if references or generated output are stale')
    args = parser.parse_args()
    rendered = build()
    output = HERE / 'index.html'
    if args.check:
        if not output.exists() or output.read_text() != rendered:
            raise SystemExit('Atlas is stale. Run python designs/atlas/build.py and commit index.html.')
        print('Atlas references, hierarchy, guards, sandbox boundary and freshness: PASS')
    else:
        output.write_text(rendered)
        print('Built designs/atlas/index.html')


if __name__ == '__main__':
    main()
