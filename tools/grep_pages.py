#!/usr/bin/env python3
"""grep_pages.py <doc_id> <regex> [context_lines] — search a paginated document, print page n/label and matching lines."""
import json, re, sys
doc = json.load(open(f'data/pages/{sys.argv[1]}.json'))
rx = re.compile(sys.argv[2], re.I)
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
for p in doc['pages']:
    lines = p['text'].split('\n')
    for i, l in enumerate(lines):
        if rx.search(l):
            print(f"[n={p['n']} label={p.get('label')} {p.get('doctype','')}] " + ' | '.join(x.rstrip() for x in lines[max(0,i-ctx):i+ctx+1]))
