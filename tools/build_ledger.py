#!/usr/bin/env python3
"""Assemble the forensic ledger: reported figures (from the as-filed pages), the improper entries identified in the
adjudicated / investigative record, the company's restatement, and clearly labelled reconstructions.

Every cited value is re-checked against the frozen page text (anchor must be present on the cited page).
Outputs: data/ledger.json, data/series.json, data/verification_text.json
"""
import json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from curated import CURATED

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
REG = {r['id']: r for r in json.load(open(os.path.join(DATA, 'register.json')))}
PAGES = {}

def pages(doc):
    if doc not in PAGES:
        PAGES[doc] = json.load(open(os.path.join(DATA, 'pages', f'{doc}.json')))['pages']
    return PAGES[doc]

def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('’', "'")).strip()

def anchor_on_page(doc, page_n, anchor):
    p = pages(doc)[page_n - 1]
    return norm(anchor) in norm(p['text'])

def para_number(doc, anchor):
    """Paragraph number for html complaints: find the <li data-para> containing the anchor."""
    p = pages(doc)[0]
    html = p.get('html', '')
    a = norm(anchor)[:60]
    # crude: split on li boundaries
    for m in re.finditer(r'<li data-para="(\d+)">(.*?)</li>', html, flags=re.S):
        txt = norm(re.sub(r'<[^>]+>', ' ', m.group(2)).replace('&nbsp;', ' ').replace('&amp;', '&').replace("&#39;", "'"))
        if a in txt:
            return int(m.group(1))
    return None

QUARTERS = ['1999Q1','1999Q2','1999Q3','1999Q4','2000Q1','2000Q2','2000Q3','2000Q4','2001Q1','2001Q2','2001Q3','2001Q4','2002Q1']
METRIC_LABEL = {
    'revenue': 'Revenues', 'line_costs': 'Line costs', 'sga': 'Selling, general and administrative', 'da': 'Depreciation and amortization',
    'operating_income': 'Operating income', 'pretax_income': 'Income before income taxes and minority interests', 'net_income': 'Net income',
    'capex': 'Capital expenditures', 'capex_embratel_undersea': 'Capital expenditures, Embratel and undersea cables',
}

ledger = []
def add(**kw):
    kw.setdefault('unit', 'USD millions')
    ledger.append(kw)
    return kw

# ---- 1. reported, straight from the filings ----
raw = json.load(open(os.path.join(DATA, 'reported_raw.json')))
rep = {}
for r in raw:
    v = r['value']
    if r['metric'].startswith('capex'):
        v = abs(v)
    key = (r['period'], r['metric'])
    rep[key] = v
    anchor_val = r['anchor']
    add(id=f"rep:{r['period']}:{r['metric']}", track='reported', period=r['period'], metric=r['metric'], label=METRIC_LABEL.get(r['metric'], r['metric']),
        value=v, basis='As originally filed with the SEC', doc=r['doc'], page=r['page'], page_label=r['label'], doctype=r.get('doctype'), anchor=anchor_val,
        note=f"{REG[r['doc']]['form']} for {r['period']}: consolidated statements as filed (capital expenditures shown as a positive outflow).")

# ---- 2. derived Q4 figures: fiscal year (10-K) minus nine months (Q3 10-Q) ----
for yr in ('1999', '2000', '2001'):
    for metric in ('revenue', 'line_costs', 'sga', 'da', 'operating_income', 'pretax_income', 'net_income', 'capex'):
        fy = rep.get((f'{yr}FY', metric)); m9 = rep.get((f'{yr}M9', metric))
        if fy is None or m9 is None:
            continue
        add(id=f"der:{yr}Q4:{metric}", track='reported-derived', period=f'{yr}Q4', metric=metric, label=METRIC_LABEL[metric], value=fy - m9,
            basis='Derived from two filings', doc=None, page=None,
            formula=f"{yr}FY ({metric}) − {yr} nine months ({metric})", components=[f"rep:{yr}FY:{metric}", f"rep:{yr}M9:{metric}"],
            note='Fourth quarter was not separately presented in the 10-K; computed as the fiscal-year figure in the 10-K minus the nine-month figure in the third-quarter 10-Q. Any reclassification between the two filings flows into this number (see limitations).')
        rep[(f'{yr}Q4', metric)] = fy - m9

# capex is presented year-to-date in the Q2/Q3 10-Q cash-flow statements: derive the quarter
for yr in ('1999', '2000', '2001'):
    for q, hi, lo, hname, lname in ((f'{yr}Q2', f'{yr}H1', f'{yr}Q1', 'six months', 'first quarter'), (f'{yr}Q3', f'{yr}M9', f'{yr}H1', 'nine months', 'six months')):
        a = rep.get((hi, 'capex')); b = rep.get((lo, 'capex'))
        if a is None or b is None:
            continue
        add(id=f"der:{q}:capex", track='reported-derived', period=q, metric='capex', label=METRIC_LABEL['capex'], value=a - b, basis='Derived from two filings', doc=None, page=None,
            formula=f"{yr} {hname} capex − {yr} {lname} capex", components=[f"rep:{hi}:capex", (f"rep:{lo}:capex" if (lo, 'capex') in {(r['period'], r['metric']) for r in raw} else f"der:{lo}:capex")],
            note='Cash-flow statements in the second- and third-quarter 10-Qs are year-to-date; the quarter is the difference between consecutive year-to-date figures.')
        rep[(q, 'capex')] = a - b

# ---- 3. curated adjudicated / investigative / company-restatement values ----
for c in CURATED:
    ok = anchor_on_page(c['doc'], c['page'], c['anchor'])
    para = None
    if REG[c['doc']]['kind'] == 'html':
        para = para_number(c['doc'], c['anchor'])
    add(id=f"{c['track']}:{c['period']}:{c['metric']}", track=c['track'], period=c['period'], metric=c['metric'], label=c['metric'].replace('_', ' '),
        value=c['value'], basis=c['basis'], doc=c['doc'], page=c['page'], page_label=(f'¶ {para}' if para else c['label']), paragraph=para, anchor=c['anchor'],
        note=c['note'], mechanism=c.get('mechanism'), anchor_found=ok)
    if not ok:
        print('!! anchor NOT found:', c['doc'], c['page'], c['anchor'][:70])

# de-duplicate ids (several curated rows share period+metric, e.g. per-quarter rows are unique but summary rows may collide)
seen = {}
for e in ledger:
    if e['id'] in seen:
        seen[e['id']] += 1
        e['id'] = f"{e['id']}#{seen[e['id']]}"
    else:
        seen[e['id']] = 1

# ---- 4. reconstructions (clearly labelled) ----
adj = {e['period']: e for e in ledger if e['track'] == 'adjustment' and e['metric'] == 'line_cost_reduction' and e['period'] in QUARTERS}
revi = {e['period']: e for e in ledger if e['track'] == 'adjustment' and e['metric'] == 'revenue_improper' and e['period'] in QUARTERS}
revq = {e['period']: e for e in ledger if e['track'] == 'adjustment' and e['metric'] == 'revenue_questionable' and e['period'] in QUARTERS}
cap = {e['period']: e for e in ledger if e['track'] == 'adjustment' and e['metric'] == 'line_costs_capitalized' and e['period'] in QUARTERS}
series = {q: {} for q in QUARTERS}
for q in QUARTERS:
    r_lc = rep.get((q, 'line_costs')); r_pti = rep.get((q, 'pretax_income')); r_rev = rep.get((q, 'revenue')); r_capex = rep.get((q, 'capex'))
    a = adj.get(q); a_v = a['value'] if a else 0
    ri = revi.get(q); ri_v = ri['value'] if ri else 0
    rq = revq.get(q); rq_v = rq['value'] if rq else 0
    cp = cap.get(q); cp_v = cp['value'] if cp else 0
    rep_id = lambda m: (f"rep:{q}:{m}" if (q, m) in {(r['period'], r['metric']) for r in raw} else f"der:{q}:{m}")
    e1 = add(id=f"rec:{q}:line_costs", track='reconstructed', period=q, metric='line_costs', label='Line costs, corrected for improper reductions', value=r_lc + a_v,
             basis='Reconstruction (Paper Trail)', formula='reported line costs + improper line-cost reductions identified by the Special Investigative Committee',
             components=[rep_id('line_costs')] + ([a['id']] if a else []),
             note='Analytical reconstruction, not a company-restated figure. Adds back the quarter\'s improper accrual releases / capitalizations (Beresford report). Other restatement items (impairments, purchase accounting, international, etc.) are excluded.')
    e2 = add(id=f"rec:{q}:pretax_income", track='reconstructed', period=q, metric='pretax_income', label='Pre-tax income, corrected for improper line-cost reductions', value=r_pti - a_v,
             basis='Reconstruction (Paper Trail)', formula='reported pre-tax income − improper line-cost reductions (Special Investigative Committee)',
             components=[rep_id('pretax_income')] + ([a['id']] if a else []),
             note='Analytical reconstruction. Removes only the line-cost entries; the pre-tax effect of improper revenue entries is not separately quantified by quarter in the record and is therefore not deducted here.')
    e3 = add(id=f"rec:{q}:revenue", track='reconstructed', period=q, metric='revenue', label='Revenues, less improper revenue entries', value=r_rev - ri_v,
             basis='Reconstruction (Paper Trail)', formula='reported revenues − improper revenue entries (Special Investigative Committee)',
             components=[rep_id('revenue')] + ([ri['id']] if ri else []),
             note='Analytical reconstruction. The Committee\'s further $1.107 billion of "questionable" items is shown separately as a band, not deducted.')
    e4 = None
    if cp:
        e4 = add(id=f"rec:{q}:capex", track='reconstructed', period=q, metric='capex', label='Capital expenditures, less capitalized line costs', value=r_capex - cp_v,
                 basis='Reconstruction (Paper Trail)', formula='reported capital expenditures − line costs improperly capitalized (Special Investigative Committee)',
                 components=[rep_id('capex')] + [cp['id']],
                 note='Analytical reconstruction. For Q1 2001 the Committee states the actual spend was $1.691 billion against $2.235 billion reported, which matches 2,235 − 544.')
    series[q] = dict(
        revenue_reported=r_rev, revenue_corrected=r_rev - ri_v, revenue_improper=ri_v, revenue_questionable=rq_v,
        line_costs_reported=r_lc, line_costs_corrected=r_lc + a_v, line_cost_reduction=a_v, mechanism=(a['mechanism'] if a else None),
        pretax_reported=r_pti, pretax_corrected=r_pti - a_v,
        net_income_reported=rep.get((q, 'net_income')), operating_income_reported=rep.get((q, 'operating_income')),
        capex_reported=r_capex, capex_corrected=(r_capex - cp_v) if cp else None, capitalized=cp_v,
        er_reported=round(100 * r_lc / r_rev, 1), er_corrected=round(100 * (r_lc + a_v) / (r_rev - ri_v), 1),
        ids=dict(revenue=rep_id('revenue'), line_costs=rep_id('line_costs'), pretax=rep_id('pretax_income'), capex=rep_id('capex'),
                 adjustment=(a['id'] if a else None), revenue_improper=(ri['id'] if ri else None), capitalized=(cp['id'] if cp else None),
                 rec_line_costs=e1['id'], rec_pretax=e2['id'], rec_revenue=e3['id'], rec_capex=(e4['id'] if e4 else None)))

# ---- 5. annual reconciliation panel: three official totals ----
annual = {}
for yr in ('1999', '2000', '2001'):
    qs = [q for q in QUARTERS if q.startswith(yr)]
    annual[yr] = dict(
        quarterly_line_cost_reductions=sum(series[q]['line_cost_reduction'] for q in qs),
        committee_line_costs=next((e['value'] for e in ledger if e['track'] == 'committee_summary' and e['metric'] == 'committee_improper_line_costs' and e['period'] == f'{yr}FY'), None),
        committee_total=next((e['value'] for e in ledger if e['track'] == 'committee_summary' and e['metric'] == 'committee_improper_total' and e['period'] == f'{yr}FY'), None),
        company_aug8_pretax=next((e['value'] for e in ledger if e['track'] == 'company_disclosure' and e['metric'] == 'company_announced_pretax_reduction' and e['period'] == f'{yr}FY'), None),
        tenk_access_costs=next((e['value'] for e in ledger if e['track'] == 'restated' and e['metric'] == 'restatement_pretax_improper_reduction_of_access_costs' and e['period'] == f'{yr}FY'), None),
        tenk_total_pretax_adj=next((e['value'] for e in ledger if e['track'] == 'restated' and e['metric'] == 'restatement_pretax_total_restatement_adjustments' and e['period'] == f'{yr}FY'), None),
        reported_pretax=rep.get((f'{yr}FY', 'pretax_income')), reported_net_income=rep.get((f'{yr}FY', 'net_income')), reported_revenue=rep.get((f'{yr}FY', 'revenue')), reported_line_costs=rep.get((f'{yr}FY', 'line_costs')),
        restated_pretax=next((e['value'] for e in ledger if e['track'] == 'restated' and e['metric'] == 'restated_pretax_loss' and e['period'] == f'{yr}FY'), None),
        restated_net_income=next((e['value'] for e in ledger if e['track'] == 'restated' and e['metric'] == 'restated_net_loss' and e['period'] == f'{yr}FY'), None),
        restated_revenue=next((e['value'] for e in ledger if e['track'] == 'restated' and e['metric'] == 'restated_revenue' and e['period'] == f'{yr}FY'), None),
    )
annual['2002Q1'] = dict(quarterly_line_cost_reductions=series['2002Q1']['line_cost_reduction'],
                        committee_line_costs=next((e['value'] for e in ledger if e['track'] == 'committee_summary' and e['metric'] == 'committee_improper_line_costs' and e['period'] == '2002Q1'), None),
                        committee_total=next((e['value'] for e in ledger if e['track'] == 'committee_summary' and e['metric'] == 'committee_improper_total' and e['period'] == '2002Q1'), None),
                        company_aug8_pretax=next((e['value'] for e in ledger if e['track'] == 'company_disclosure' and e['metric'] == 'company_announced_pretax_reduction' and e['period'] == '2002Q1'), None))

# ---- 6. text verification of every cited value (anchor present on cited page) ----
ver = []
for e in ledger:
    if e.get('doc') and e.get('page'):
        ok = anchor_on_page(e['doc'], e['page'], e['anchor'])
        e['anchor_found'] = ok
        ver.append(dict(id=e['id'], doc=e['doc'], page=e['page'], page_label=e.get('page_label'), anchor=e['anchor'][:90], found=ok))
n_cited = len(ver); n_ok = sum(1 for v in ver if v['found'])
meta = dict(built=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), entries=len(ledger), cited=n_cited, anchors_found=n_ok,
            tracks={t: sum(1 for e in ledger if e['track'] == t) for t in sorted({e['track'] for e in ledger})})
json.dump(dict(meta=meta, entries=ledger), open(os.path.join(DATA, 'ledger.json'), 'w'), indent=0)
json.dump(dict(quarters=QUARTERS, series=series, annual=annual), open(os.path.join(DATA, 'series.json'), 'w'), indent=1)
json.dump(ver, open(os.path.join(DATA, 'verification_text.json'), 'w'), indent=0)
print(json.dumps(meta, indent=1))
print('NOT FOUND:', [v for v in ver if not v['found']][:10])
for q in QUARTERS:
    s = series[q]
    print(q, 'LC', s['line_costs_reported'], '->', s['line_costs_corrected'], '| PTI', s['pretax_reported'], '->', s['pretax_corrected'], '| REV', s['revenue_reported'], '->', s['revenue_corrected'], '| E/R', s['er_reported'], '->', s['er_corrected'])
print(json.dumps(annual, indent=1))
