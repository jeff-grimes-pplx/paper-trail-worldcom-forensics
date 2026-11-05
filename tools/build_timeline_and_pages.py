#!/usr/bin/env python3
"""Build data/timeline.json (anchor-verified) and render page images + highlight boxes for every cited PDF page.

For PDFs: page image (JPEG, 1400 px wide) is rendered with PyMuPDF for each cited page ±1 and for every page of
documents with <= 40 pages; highlight rectangles are computed with page.search_for(anchor) and stored normalised.
For EDGAR text/HTML documents the viewer renders the frozen page text/HTML itself, so no images are needed.
"""
import json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
import fitz
from timeline import EVENTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
REG = {r['id']: r for r in json.load(open(os.path.join(DATA, 'register.json')))}
IMG_DIR = os.path.join(DATA, 'pdf-pages'); os.makedirs(IMG_DIR, exist_ok=True)
PAGES = {}

def pages(doc):
    if doc not in PAGES:
        PAGES[doc] = json.load(open(os.path.join(DATA, 'pages', f'{doc}.json')))['pages']
    return PAGES[doc]

def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('’', "'").replace('‘', "'")).strip()

# ---- timeline ----
tl = []
for i, e in enumerate(EVENTS):
    p = pages(e['doc'])[e['page'] - 1]
    ok = norm(e['anchor']) in norm(p['text'])
    if not ok:
        print('!! timeline anchor not found:', e['doc'], e['page'], e['anchor'][:60])
    rec = dict(e); rec['id'] = f"ev{i+1:02d}"; rec['anchor_found'] = ok; rec['page_label'] = e.get('label') or p.get('label')
    rec['doc_title'] = REG[e['doc']]['title']; rec['url'] = REG[e['doc']]['url']
    tl.append(rec)
json.dump(tl, open(os.path.join(DATA, 'timeline.json'), 'w'), indent=1)
print(len(tl), 'timeline events;', sum(1 for t in tl if t['anchor_found']), 'anchors found')

# ---- cited pages ----
ledger = json.load(open(os.path.join(DATA, 'ledger.json')))['entries']
cited = {}
for e in ledger + tl:
    if e.get('doc') and e.get('page'):
        cited.setdefault(e['doc'], set()).add(e['page'])

# ---- render PDF pages & highlight boxes ----
highlights = {}  # (doc, page) -> {anchor: [rects]}
render_log = []
for doc_id, rec in REG.items():
    if rec['kind'] != 'pdf':
        continue
    pdf = fitz.open(os.path.join(ROOT, rec['local_path']))
    n = len(pdf)
    want = set()
    if n <= 40:
        want = set(range(1, n + 1))
    for pg in cited.get(doc_id, []):
        want.update({pg - 1, pg, pg + 1})
    want = {w for w in want if 1 <= w <= n}
    outdir = os.path.join(IMG_DIR, doc_id); os.makedirs(outdir, exist_ok=True)
    for pg in sorted(want):
        path = os.path.join(outdir, f'{pg}.jpg')
        if not os.path.exists(path):
            page = pdf[pg - 1]
            zoom = 1400 / page.rect.width
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY, alpha=False)
            pix.save(path, jpg_quality=72)
        render_log.append((doc_id, pg))
    # highlight boxes for anchors on cited pages
    for e in ledger + tl:
        if e.get('doc') == doc_id and e.get('page'):
            page = pdf[e['page'] - 1]
            W, H = page.rect.width, page.rect.height
            anchor = e['anchor']
            rects = page.search_for(anchor) or []
            if not rects:
                # try the first 40 characters, then the last 30 (OCR'd pages are noisy)
                for frag in (anchor[:40], anchor[-30:]):
                    rects = page.search_for(frag) or []
                    if rects:
                        break
            key = f"{doc_id}:{e['page']}"
            highlights.setdefault(key, {})[anchor] = [dict(x=r.x0 / W, y=r.y0 / H, w=(r.x1 - r.x0) / W, h=(r.y1 - r.y0) / H) for r in rects]
json.dump(highlights, open(os.path.join(DATA, 'pdf-highlights.json'), 'w'))
total_imgs = sum(len(files) for _, _, files in os.walk(IMG_DIR))
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(IMG_DIR) for f in fs)
print(f'rendered {len(render_log)} page images this run; {total_imgs} images on disk, {size/1e6:.1f} MB')
print('highlight keys', len(highlights), 'empty:', sum(1 for k, v in highlights.items() for a, r in v.items() if not r))
json.dump(dict(built=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), cited_pages={k: sorted(v) for k, v in cited.items()},
               images=total_imgs, image_bytes=size), open(os.path.join(DATA, 'pages_manifest.json'), 'w'), indent=1)
