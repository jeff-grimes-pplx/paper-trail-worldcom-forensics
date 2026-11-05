#!/usr/bin/env python3
"""Turn every fetched document into an ordered list of pages with text (and HTML where the
source is HTML), written to data/pages/<id>.json plus a summary in data/pagecounts.json.

Pagination rules (documented in the app's register panel):
  edgar-txt  : split at the filing's own <PAGE> markers (SGML page breaks); label = printed footer page number
  edgar-html : split at the filing's own page-break style markers; label = printed footer page number
  pdf        : physical PDF pages; label = printed page number when PyMuPDF text shows one, else sequence
  html       : one logical page; located by paragraph number / heading text
"""
import re, os, sys, json, html as htmlmod
sys.path.insert(0, os.path.dirname(__file__))
from bs4 import BeautifulSoup, Comment
import fitz  # PyMuPDF
from edgar_html import split_pages, page_text as html_page_text, footer_page_number

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(open(os.path.join(ROOT, 'data', 'register.json')))
OUT = os.path.join(ROOT, 'data', 'pages'); os.makedirs(OUT, exist_ok=True)
IMG = os.path.join(ROOT, 'data', 'edgar-img'); os.makedirs(IMG, exist_ok=True)

SGML_TAG = re.compile(r'</?(?:S|C|CAPTION|FN|F\d+|TABLE|PAGE)>', re.I)

def clean_sgml_text(t):
    t = SGML_TAG.sub('', t)
    t = re.sub(r'<[^>]{0,40}>', '', t)  # any other short tag
    t = htmlmod.unescape(t)
    t = t.replace('\r', '')
    return t.rstrip()

def paginate_edgar_txt(raw):
    pages = []
    docs = re.findall(r'<DOCUMENT>(.*?)</DOCUMENT>', raw, flags=re.S)
    for d in docs:
        dtype = re.search(r'<TYPE>([^\n<]+)', d); dtype = dtype.group(1).strip() if dtype else '?'
        fname = re.search(r'<FILENAME>([^\n<]+)', d); fname = fname.group(1).strip() if fname else ''
        if dtype.upper().startswith('GRAPHIC') or dtype.upper() in ('ZIP', 'EXCEL'):
            continue
        m = re.search(r'<TEXT>(.*?)</TEXT>', d, flags=re.S)
        body = m.group(1) if m else d
        if re.search(r'<html', body, flags=re.I):
            # occasional HTML exhibit inside a text submission: paginate at page breaks
            frags = split_pages(body)
            for f in frags:
                t = html_page_text(f)
                if t.strip():
                    pages.append(dict(doctype=dtype, filename=fname, text=t, label=footer_page_number(t)))
            continue
        for chunk in re.split(r'<PAGE>', body, flags=re.I):
            t = clean_sgml_text(chunk)
            if not t.strip():
                continue
            lines = [l for l in t.split('\n')]
            # printed page number: last non-empty line that is a bare number / roman / F-xx (possibly right-aligned)
            label = None
            for l in reversed(lines[-6:]):
                s = l.strip()
                if not s:
                    continue
                if re.fullmatch(r'(?:[A-Z]-)?\d{1,3}|[ivxlc]{1,6}|- ?\d{1,3} ?-|\(\d{1,3}\)', s):
                    label = s.strip('- ()')
                break
            pages.append(dict(doctype=dtype, filename=fname, text=t, label=label))
    return pages

def sanitize_fragment(frag, doc_id):
    soup = BeautifulSoup(frag, 'lxml')
    for tag in soup(['script', 'style', 'link', 'meta', 'iframe', 'object', 'embed', 'form', 'input']):
        tag.decompose()
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.lower().startswith('on') or attr.lower() in ('id', 'name', 'class', 'href', 'target'):
                if attr.lower() == 'href':
                    del tag.attrs[attr]
                elif attr.lower() != 'class':
                    del tag.attrs[attr]
            elif attr.lower() == 'style':
                st = tag.attrs[attr]
                if 'url(' in st.lower() or 'position' in st.lower() or 'expression' in st.lower():
                    del tag.attrs[attr]
        if tag.name == 'img':
            src = tag.get('src', '')
            base = os.path.basename(src)
            tag.attrs = {'src': f'./data/edgar-img/{doc_id}/{base}', 'alt': 'chart image from the as-filed exhibit', 'loading': 'lazy'}
    body = soup.body if soup.body else soup
    return ''.join(str(x) for x in body.contents)

def paginate_edgar_html(raw, doc_id):
    frags = split_pages(raw)
    pages = []
    for f in frags:
        t = html_page_text(f)
        if not t.strip():
            continue
        pages.append(dict(text=t, label=footer_page_number(t), html=sanitize_fragment(f, doc_id)))
    return pages

def paginate_pdf(path):
    doc = fitz.open(path)
    pages = []
    for i, p in enumerate(doc):
        t = p.get_text('text')
        label = None
        lines = [l.strip() for l in t.split('\n') if l.strip()]
        for l in (lines[-3:] if lines else []):
            if re.fullmatch(r'(?:- ?)?\d{1,3}(?: ?-)?', l):
                label = l.strip('- ')
        pages.append(dict(text=t, label=label or str(i + 1), width=p.rect.width, height=p.rect.height))
    return pages

def extract_html_main(raw):
    soup = BeautifulSoup(raw, 'lxml')
    main = soup.find('main') or soup.find(id='main-content') or soup.find('article') or soup.body or soup
    # sec.gov modern template: drop nav/aside/footer/breadcrumbs
    for tag in main(['nav', 'aside', 'footer', 'header', 'script', 'style', 'noscript', 'form', 'button', 'svg']):
        tag.decompose()
    for sel in ['.breadcrumb', '.usa-banner', '.region-sidebar', '.block-sec-social', '#block-sec-breadcrumbs', '.tags', '.print-link', '.usa-alert']:
        for t in main.select(sel):
            t.decompose()
    for c in main.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for tag in main.find_all(True):
        for attr in list(tag.attrs):
            if attr.lower().startswith('on') or attr.lower() in ('id', 'name', 'href', 'target', 'style', 'class'):
                del tag.attrs[attr]
        if tag.name == 'img':
            tag.decompose()
    # number <li> items inside <ol> (honouring start=) so the viewer can cite paragraph numbers
    for ol in main.find_all('ol'):
        try:
            n = int(ol.get('start', 1))
        except Exception:
            n = 1
        for li in ol.find_all('li', recursive=False):
            li['data-para'] = str(n); n += 1
    html_out = ''.join(str(x) for x in main.contents)
    text = main.get_text('\n')
    text = re.sub(r'[ \t\xa0]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text).strip()
    return html_out, text

counts = {}
for rec in REG:
    path = os.path.join(ROOT, rec['local_path'])
    kind = rec['kind']
    if kind == 'edgar-txt':
        raw = open(path, encoding='latin-1').read()
        pages = paginate_edgar_txt(raw)
    elif kind == 'edgar-html':
        raw = open(path, encoding='latin-1').read()
        pages = paginate_edgar_html(raw, rec['id'])
    elif kind == 'pdf':
        pages = paginate_pdf(path)
    else:
        b = open(path, 'rb').read()
        try:
            raw = b.decode('utf-8')
        except UnicodeDecodeError:
            raw = b.decode('cp1252', errors='replace')
        h, t = extract_html_main(raw)
        pages = [dict(text=t, label='1', html=h)]
    for i, p in enumerate(pages):
        p['n'] = i + 1
    json.dump(dict(id=rec['id'], kind=kind, title=rec['title'], url=rec['url'], pages=pages),
              open(os.path.join(OUT, rec['id'] + '.json'), 'w'))
    counts[rec['id']] = dict(pages=len(pages), chars=sum(len(p['text']) for p in pages))
    print(f"{rec['id']:45s} {kind:11s} pages={len(pages):4d} chars={counts[rec['id']]['chars']:>9,d}")
json.dump(counts, open(os.path.join(ROOT, 'data', 'pagecounts.json'), 'w'), indent=1)
print('TOTAL pages', sum(c['pages'] for c in counts.values()), 'chars', sum(c['chars'] for c in counts.values()))
