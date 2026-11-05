#!/usr/bin/env python3
"""Fetch every primary document in the register, record sha256 / size / access time.

Usage: python3 tools/fetch_documents.py [--force]
Writes raw/docs/<id>.<ext> and data/register.json. Polite to SEC EDGAR (declared UA, <=2 req/s).
"""
import hashlib, json, os, sys, time, datetime, mimetypes
import requests
sys.path.insert(0, os.path.dirname(__file__))
from register import DOCS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'docs'); os.makedirs(RAW, exist_ok=True)
DATA = os.path.join(ROOT, 'data'); os.makedirs(DATA, exist_ok=True)
UA = {'User-Agent': 'Perplexity Computer research project (jeff.grimes@perplexity.ai)', 'Accept-Encoding': 'gzip, deflate'}
FORCE = '--force' in sys.argv
EXT = {'edgar-txt': 'txt', 'edgar-html': 'htm', 'pdf': 'pdf', 'html': 'htm'}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

register = []
for d in DOCS:
    ext = EXT[d['kind']]
    path = os.path.join(RAW, f"{d['id']}.{ext}")
    rec = dict(d)
    rec['local_path'] = os.path.relpath(path, ROOT)
    if not os.path.exists(path) or FORCE:
        for attempt in range(3):
            try:
                r = requests.get(d['url'], headers=UA, timeout=120)
                if r.status_code == 200 and len(r.content) > 500:
                    with open(path, 'wb') as f:
                        f.write(r.content)
                    rec['http_status'] = r.status_code
                    rec['content_type'] = r.headers.get('Content-Type')
                    rec['accessed'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
                    break
                else:
                    rec['http_status'] = r.status_code
                    print('  !! status', r.status_code, d['url'])
            except Exception as e:
                print('  !! error', e, d['url'])
            time.sleep(2 + attempt * 3)
        time.sleep(0.6)
    else:
        # keep earlier access metadata if present
        prev = {}
        try:
            prev = {x['id']: x for x in json.load(open(os.path.join(DATA, 'register.json')))}
        except Exception:
            pass
        for k in ('http_status', 'content_type', 'accessed'):
            if d['id'] in prev and k in prev[d['id']]:
                rec[k] = prev[d['id']][k]
    if os.path.exists(path):
        rec['sha256'] = sha256(path)
        rec['bytes'] = os.path.getsize(path)
        print(f"{d['id']:45s} {rec['bytes']:>10,d}  {rec['sha256'][:16]}")
    else:
        rec['missing'] = True
        print(f"{d['id']:45s} MISSING")
    register.append(rec)

json.dump(register, open(os.path.join(DATA, 'register.json'), 'w'), indent=1)
with open(os.path.join(DATA, 'SHA256SUMS.txt'), 'w') as f:
    for r in register:
        if 'sha256' in r:
            f.write(f"{r['sha256']}  {r['local_path']}\n")
print(len(register), 'documents;', sum(1 for r in register if 'missing' in r), 'missing')
