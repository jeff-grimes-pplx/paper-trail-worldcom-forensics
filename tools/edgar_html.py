"""Paginate an EDGAR HTML document at its own page-break markers and extract page text.

Pages are split on <p style="page-break-before:always"> (and <hr> variants) exactly as the
filing agent placed them, so page N here is the page number printed in the filing footer.
"""
import re, html, json, sys
from bs4 import BeautifulSoup

PB = re.compile(r'<(?:p|div|br)[^>]*page-break-(?:before|after)\s*:\s*always[^>]*>', re.I)

def split_pages(raw):
    parts = PB.split(raw)
    return parts

def table_to_text(tbl):
    rows=[]
    for tr in tbl.find_all('tr'):
        cells=[]
        for td in tr.find_all(['td','th']):
            s=td.get_text(' ', strip=True)
            s=re.sub(r'\s+',' ',s)
            if s: cells.append(s)
        if cells: rows.append('  '.join(cells))
    return '\n'.join(rows)

def page_text(fragment):
    soup=BeautifulSoup(fragment,'lxml')
    for t in soup.find_all('table'):
        t.replace_with(soup.new_string('\n'+table_to_text(t)+'\n'))
    txt=soup.get_text('\n')
    txt=html.unescape(txt).replace('\xa0',' ')
    txt=re.sub(r'[ \t]+',' ',txt)
    txt=re.sub(r'\n\s*\n+','\n',txt)
    return txt.strip()

def footer_page_number(txt):
    # last short numeric-ish line e.g. "97", "F-33", "A-12"
    lines=[l.strip() for l in txt.strip().split('\n') if l.strip()]
    for l in reversed(lines[-4:]):
        if re.fullmatch(r'(?:[A-Z]-)?\d{1,3}|[ivxlc]{1,6}', l): return l
    return None

if __name__=='__main__':
    src=sys.argv[1]; out=sys.argv[2]
    raw=open(src,encoding='latin-1').read()
    frags=split_pages(raw)
    pages=[]
    for i,f in enumerate(frags):
        t=page_text(f)
        pages.append({'seq':i+1,'label':footer_page_number(t),'text':t,'html':f})
    json.dump(pages,open(out,'w'))
    print(len(pages),'pages ->',out)
    print([p['label'] for p in pages][:60])
