#!/usr/bin/env python3
"""Generate handoff/REGISTER.md and handoff/VERIFICATION.md from data/*.json."""
import json, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, 'data', *p)
reg = json.load(open(D('register.json'))); pc = json.load(open(D('pagecounts.json')))
L = json.load(open(D('ledger.json'))); E = L['entries']
tl = json.load(open(D('timeline.json'))); events = tl['events'] if isinstance(tl, dict) else tl
V = json.load(open(D('verification.json')))
cited = collections.Counter(e['doc'] for e in E if e.get('doc')); evc = collections.Counter(e['doc'] for e in events)
order = {'reported': 0, 'restatement': 1, 'investigation': 2, 'disclosure': 3, 'enforcement': 4, 'court': 5, 'criminal': 6, 'congress': 7}
rows = sorted(reg, key=lambda d: (order.get(d['role'], 9), d.get('filed') or ''))
out = ['# Paper Trail — document register', '',
       f'{len(reg)} public primary documents, fetched on the access dates below and hashed (SHA-256 of the bytes as fetched; the same digests are in `data/SHA256SUMS.txt`). Pages were split at each filing\'s own page markers (`<PAGE>` in EDGAR text filings, page breaks in EDGAR HTML, physical pages in PDFs; single HTML documents are one "page" located by paragraph). "Values" is the number of ledger values citing the document; "Events" the number of timeline events citing it. Documents with neither are context documents kept for search and completeness.', '',
       f'Totals: {sum(p["pages"] for p in pc.values()):,} pages · {sum(p["chars"] for p in pc.values()):,} characters of extracted text · {sum(1 for e in E if e.get("doc"))} page-cited values · {len(events)} events.', '',
       '| # | Role | Document | Dated | Kind | Pages | Values | Events | Accessed | SHA-256 | URL |', '|---|---|---|---|---|---|---|---|---|---|---|']
for i, d in enumerate(rows, 1):
    p = pc.get(d['id'], {})
    out.append(f"| {i} | {d['role']} | {d['title'].replace('|', '/')} (`{d['id']}`) | {d.get('filed') or 'undated copy'} | {d['kind_label']} | {p.get('pages', '')} | {cited.get(d['id'], 0) or ''} | {evc.get(d['id'], 0) or ''} | {d['accessed'][:10]} | `{d['sha256']}` | {d['url']} |")
open(os.path.join(ROOT, 'handoff', 'REGISTER.md'), 'w').write('\n'.join(out) + '\n')
vo = [f'# Paper Trail — verification table ({V["sample_size"]} sampled values, {V["matches"]} match)', '', V['method'], '',
      f"Sample size {V['sample_size']}, matches {V['matches']}, built {V['built']}. Each row records the ledger id, the value as shown, the document and page as opened in the app, how the figure was located, and the crop that was read.", '',
      '| # | Ledger id | Value | Document | Page (as opened) | Located | Anchor (as cited) | Result | Crop |', '|---|---|---|---|---|---|---|---|---|']
for r in V['rows']:
    lab = f" ({r['page_label']})" if r.get('page_label') else ''
    vo.append(f"| {r['n']} | `{r['id']}` | {r['value_display']} | {r['doc_short']} | {r['page']}{lab} | {r['located']} | {r['anchor'][:90].replace('|', '/')}{'…' if len(r['anchor']) > 90 else ''} | {r['result']} | {r['crop']} |")
open(os.path.join(ROOT, 'handoff', 'VERIFICATION.md'), 'w').write('\n'.join(vo) + '\n')
print('REGISTER.md rows', len(rows), '· VERIFICATION.md rows', len(V['rows']))
