#!/usr/bin/env python3
"""Extract the originally reported income-statement and capex figures from the as-filed 10-Q/10-K pages.

Output: data/reported_raw.json — one record per (doc, period, metric) with page number, printed page label,
the exact source line (anchor) and the parsed value in USD millions. Column positions are declared per filing
because the SEC text tables put the current period in different columns in different years.
"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# doc -> (income-statement page n, cash-flow page n, {period_key: column_index}) ; columns counted left→right among numeric tokens
FILINGS = {
    '10q-1999q1': dict(is_page=4, cf_page=5, cols={'1999Q1': 0}, cf_cols={'1999Q1': 0}),
    '10q-1999q2': dict(is_page=4, cf_page=5, cols={'1999Q2': 0, '1999H1': 2}, cf_cols={'1999H1': 0}),
    '10q-1999q3': dict(is_page=4, cf_page=5, cols={'1999Q3': 0, '1999M9': 2}, cf_cols={'1999M9': 0}),
    '10k-1999':   dict(is_page=69, cf_page=71, cols={'1999FY': 0}, cf_cols={'1999FY': 0}),
    '10q-2000q1': dict(is_page=4, cf_page=5, cols={'2000Q1': 0}, cf_cols={'2000Q1': 0}),
    '10q-2000q2': dict(is_page=4, cf_page=5, cols={'2000Q2': 0, '2000H1': 2}, cf_cols={'2000H1': 0}),
    '10q-2000q3': dict(is_page=4, cf_page=5, cols={'2000Q3': 0, '2000M9': 2}, cf_cols={'2000M9': 0}),
    '10k-2000':   dict(is_page=91, cf_page=93, cols={'2000FY': 2}, cf_cols={'2000FY': 2}),
    '10q-2001q1': dict(is_page=4, cf_page=5, cols={'2001Q1': 1}, cf_cols={'2001Q1': 1}),
    '10q-2001q2': dict(is_page=4, cf_page=5, cols={'2001Q2': 1, '2001H1': 3}, cf_cols={'2001H1': 1}),
    '10q-2001q3': dict(is_page=4, cf_page=5, cols={'2001Q3': 1, '2001M9': 3}, cf_cols={'2001M9': 1}),
    '10k-2001':   dict(is_page=78, cf_page=80, cols={'2001FY': 2}, cf_cols={'2001FY': 2}),
    '10q-2002q1': dict(is_page=4, cf_page=5, cols={'2002Q1': 1}, cf_cols={'2002Q1': 1}),
}
# For the 10-Ks the columns are (10-K 1999: 1999 1998 1997) -> 0 ; (10-K 2000: 2000 1999 1998)->0 ; (10-K 2001: 1999 2000 2001)->2
IS_METRICS = [
    ('revenue', re.compile(r'^\s*Revenues\b')),
    ('line_costs', re.compile(r'^\s*Line costs\b')),
    ('sga', re.compile(r'^\s*Selling, general and administrative\b')),
    ('da', re.compile(r'^\s*Depreciation and amortization\b')),
    ('operating_income', re.compile(r'^\s*Operating income')),
    ('pretax_income', re.compile(r'^\s*Income (?:\(loss\) )?before income taxes')),
    ('net_income', re.compile(r'^\s*Net income(?: \(loss\))?\s+[\(\$\d]')),
]
CF_METRICS = [('capex', re.compile(r'^\s*Capital expenditures\.*\s+[\(\$\d]')), ('capex_embratel_undersea', re.compile(r'^\s*Capital expenditures, Embratel'))]
NUM = re.compile(r'\(?\$?\s?-?[\d]{1,3}(?:,\d{3})*(?:\.\d+)?\)?|(?<=\s)--?(?=\s|$)')

def parse_numbers(s):
    vals = []
    for m in NUM.finditer(s):
        tok = m.group(0)
        if tok.strip() in ('-', '--'):
            vals.append(0.0); continue
        neg = tok.strip().startswith('(') and tok.strip().endswith(')')
        n = float(re.sub(r'[^\d.\-]', '', tok))
        vals.append(-n if neg else n)
    return vals

def extract_from_page(page, metrics, cols, doc, pretax_multiline=True):
    out = []
    lines = page['text'].split('\n')
    seen = set()
    for i, line in enumerate(lines):
        for metric, rx in metrics:
            if metric in seen or not rx.search(line):
                continue
            # numbers may sit on the next line when the label wraps (e.g., "Income before income taxes, minority interests and\n cumulative effect ... 2,317  988")
            label_part = line
            nums = parse_numbers(re.sub(r'^\s*[^\d\(\$\-]*', '', line))
            j = i
            while len(nums) < max(cols.values()) + 1 and j + 1 < len(lines) and j - i < 2:
                j += 1
                nums = parse_numbers(re.sub(r'^\s*[^\d\(\$\-]*', '', lines[j]))
            if len(nums) < max(cols.values()) + 1:
                continue
            seen.add(metric)
            for period, ci in cols.items():
                anchor = ' '.join(l.strip() for l in lines[i:j + 1])
                out.append(dict(doc=doc, period=period, metric=metric, value=nums[ci], page=page['n'], label=page.get('label'),
                                doctype=page.get('doctype'), anchor=re.sub(r'\s+', ' ', anchor)))
    return out

records = []
for doc, cfg in FILINGS.items():
    D = json.load(open(os.path.join(ROOT, 'data', 'pages', f'{doc}.json')))
    is_page = D['pages'][cfg['is_page'] - 1]
    cf_page = D['pages'][cfg['cf_page'] - 1]
    records += extract_from_page(is_page, IS_METRICS, cfg['cols'], doc)
    records += extract_from_page(cf_page, CF_METRICS, cfg['cf_cols'], doc)
json.dump(records, open(os.path.join(ROOT, 'data', 'reported_raw.json'), 'w'), indent=1)
for r in records:
    print(f"{r['doc']:11s} {r['period']:7s} {r['metric']:17s} {r['value']:>10,.0f}  p.{r['page']}({r['label']})  {r['anchor'][:70]}")
print(len(records), 'records')
