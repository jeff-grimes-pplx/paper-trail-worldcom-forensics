// Two-track quarterly chart + quarter card + annual reconciliation.
import { DATA, fmt } from './data.js';
import { citeFromEntry } from './viewer.js';

const METRICS = {
  line_costs: { title: 'Line costs', unit: '$bn', rep: 'line_costs_reported', cor: 'line_costs_corrected', corLabel: 'Corrected: reported plus the improper reductions identified by the Special Investigative Committee', above: true,
    note: 'Line costs are what WorldCom paid other carriers to carry its traffic — its largest expense. Reducing them was the heart of the fraud.' },
  pretax: { title: 'Pre-tax income', unit: '$bn', rep: 'pretax_reported', cor: 'pretax_corrected', corLabel: 'Corrected: reported minus the improper line-cost reductions (revenue items not deducted)', above: false,
    note: 'Pre-tax income as reported each quarter, and what it would have been without the line-cost entries alone.' },
  revenue: { title: 'Revenues', unit: '$bn', rep: 'revenue_reported', cor: 'revenue_corrected', corLabel: 'Corrected: reported minus the improper revenue entries; dashed = also minus the Committee\'s "questionable" items', above: false, extra: 'revenue_questionable',
    note: 'Revenue entries were smaller than the line-cost entries but were used to hit the published growth targets ("Close the Gap").' },
  capex: { title: 'Capital expenditures', unit: '$bn', rep: 'capex_reported', cor: 'capex_corrected', corLabel: 'Corrected: reported minus the line costs moved into property, plant and equipment', above: false,
    note: 'From Q1 2001 the capitalized line costs showed up as capital spending; the Committee found Q1 2001 spend was $1.691bn against $2.235bn reported.' },
  er: { title: 'Line costs as a share of revenues', unit: '%', rep: 'er_reported', cor: 'er_corrected', corLabel: 'Corrected ratio (corrected line costs ÷ corrected revenues)', above: true, pct: true,
    note: 'Analysts watched this ratio. The entries kept it near 42% when the real figure was heading past 50%.' },
};

export class TwoTrack {
  constructor(root, viewer, onSelect) {
    this.root = root; this.viewer = viewer; this.onSelect = onSelect; this.metric = 'line_costs'; this.selected = '2001Q1'; this.showGap = true;
    this.S = DATA.series; this.Q = this.S.quarters;
    root.innerHTML = `
      <div class="sec-head-row">
        <div>
          <h2>Two tracks, quarter by quarter</h2>
          <p class="lede">The blue line is what WorldCom filed with the SEC each quarter. The red line removes the improper entries later documented by the board's Special Investigative Committee, the SEC and the company itself. Select any quarter or metric to synchronize the filed page and the forensic proof page on the right.</p>
        </div>
        <div class="workbook-strip" aria-label="Download forensic audit artifacts">
          <span class="wb-kicker">Verified Audit Exports · 57/57 SHA-256 ✓</span>
          <div class="wb-btns">
            <a class="wb-btn primary" href="data/WorldCom_Forensic_Audit_Workbook.xlsx" download="WorldCom_Forensic_Audit_Workbook.xlsx" title="Download 6-tab institutional Excel forensic model with live formulas">↓ Audit Workbook (.xlsx)</a>
            <a class="wb-btn" href="data/WorldCom_Forensic_Audit_Ledger.csv" download="WorldCom_Forensic_Audit_Ledger.csv" title="Download all 453 page-anchored forensic ledger rows as CSV">↓ 453-Row Ledger (.csv)</a>
            <a class="wb-btn" href="data/forensic_verification_report.json" download="forensic_verification_report.json" title="Download programmatic SHA-256 and restatement verification JSON">↓ Verification (.json)</a>
          </div>
        </div>
      </div>
      <div class="metric-tabs" role="tablist"></div>
      <div class="chart-wrap"><svg role="img" aria-label="Reported versus corrected figures by quarter"></svg></div>
      <div class="legend"></div>
      <div class="quarter-card"></div>
      <h3>Annual: the official totals do not all measure the same thing</h3>
      <div class="annual"></div>
      <h3>The company's own restatement, by category (2002 Form 10-K, filed March 2004)</h3>
      <div class="restate"></div>`;
    this.tabs = root.querySelector('.metric-tabs'); this.svg = root.querySelector('svg'); this.legend = root.querySelector('.legend'); this.card = root.querySelector('.quarter-card');
    Object.entries(METRICS).forEach(([k, m]) => { const b = document.createElement('button'); b.textContent = m.title; b.dataset.metric = k; b.setAttribute('role', 'tab'); b.addEventListener('click', () => this.setMetric(k)); this.tabs.appendChild(b); });
    this.tip = document.getElementById('tooltip');
    new ResizeObserver(() => this.draw()).observe(root.querySelector('.chart-wrap'));
    this.setMetric('line_costs', false);
    this.renderAnnual(); this.renderRestatement();
  }

  setMetric(k, redraw = true) {
    if (!METRICS[k]) return; // D7: ignore unknown metric keys
    this.metric = k; this.tabs.querySelectorAll('button').forEach(b => b.classList.toggle('active', b.dataset.metric === k));
    const m = METRICS[k];
    this.legend.innerHTML = `<span><i class="sw reported"></i>Reported in the 10-Q / 10-K as filed</span><span><i class="sw true"></i>${m.corLabel}</span><span><i class="sw gap"></i>Gap</span>`;
    if (redraw) this.draw();
    this.renderCard();
    if (redraw && this.selected) this.openPair(this.selected, { reveal: false });
  }

  select(q, open = true) {
    if (q != null && !this.S.series[q]) return; // D7: ignore unknown quarters
    this.selected = q; this.draw(); this.renderCard();
    if (open) this.openPair(q, { reveal: true });
    if (this.onSelect) this.onSelect(q);
  }

  openPair(q, opts = { reveal: true }) {
    const s = this.S.series[q]; const m = METRICS[this.metric];
    const repKey = { line_costs: 'line_costs', pretax: 'pretax', revenue: 'revenue', capex: 'capex', er: 'line_costs' }[this.metric];
    const repEntry = DATA.byId.get(s.ids[repKey]);
    const adjKey = this.metric === 'revenue' ? 'revenue_improper' : this.metric === 'capex' ? 'capitalized' : 'adjustment';
    const adjEntry = s.ids[adjKey] ? DATA.byId.get(s.ids[adjKey]) : null;
    const cites = [];
    if (repEntry && repEntry.doc) cites.push(citeFromEntry(repEntry, `As reported · ${fmt.quarter(q)}`));
    else if (repEntry) { // derived Q4: open the 10-K component
      const comp = DATA.byId.get(repEntry.components[0]); if (comp) cites.push(citeFromEntry(comp, `Fiscal-year figure used to derive ${fmt.quarter(q)} (minus the nine-month figure)`));
    }
    if (adjEntry) cites.push(citeFromEntry(adjEntry, `Improper entry for ${fmt.quarter(q)} · Special Investigative Committee`));
    else cites.push({ empty: `No improper ${this.metric === 'revenue' ? 'revenue' : this.metric === 'capex' ? 'capitalization' : 'line-cost'} entry was identified for ${fmt.quarter(q)} in the Special Investigative Committee's report; the reported figure stands.` });
    if (cites.length) this.viewer.show(cites, opts);
  }

  draw() {
    const svg = this.svg; const wrap = svg.parentElement; const W = Math.max(320, wrap.clientWidth - 16); const H = W < 520 ? 300 : 400;
    const m = METRICS[this.metric]; const S = this.S.series; const Q = this.Q;
    const pad = { l: 54, r: 18, t: 20, b: 56 };
    const vals = []; Q.forEach(q => { const s = S[q]; if (s[m.rep] != null) vals.push(s[m.rep]); if (s[m.cor] != null) vals.push(s[m.cor]); if (m.extra && s[m.extra] != null) vals.push(s.revenue_corrected - s[m.extra]); });
    let lo = Math.min(...vals), hi = Math.max(...vals);
    if (!m.pct) { lo = Math.min(0, lo); } else { lo = Math.floor((lo - 2) / 5) * 5; hi = Math.ceil((hi + 2) / 5) * 5; }
    const span = hi - lo || 1; hi += span * 0.08; if (lo < 0) lo -= span * 0.05;
    // Optional reveal (used by the film capture and nothing else): the corrected line separates from the
    // reported line one quarter at a time. revealF == null draws the complete chart.
    const F = this.revealF; const easeIO = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    const cOf = (s, i) => { const c = s[m.cor]; if (c == null || F == null) return c; const r = s[m.rep]; if (r == null || F < i) return null; return r + (c - r) * easeIO(Math.max(0, Math.min(1, F - i))); };
    const x = i => pad.l + (W - pad.l - pad.r) * (i + 0.5) / Q.length;
    const y = v => pad.t + (H - pad.t - pad.b) * (1 - (v - lo) / (hi - lo));
    const ticks = niceTicks(lo, hi, 6);
    const fmtTick = v => m.pct ? `${v}%` : (v === 0 ? '0' : `${v < 0 ? '−' : ''}${Math.abs(v) / 1000}`);
    let out = `<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="rgba(142,44,37,0.10)"/><line x1="0" y1="0" x2="0" y2="6" stroke="rgba(142,44,37,0.55)" stroke-width="1.6"/></pattern></defs>`;
    // period bands
    const bands = W < 560 ? [{ a: 1, b: 7, l: 'Accruals released' }, { a: 8, b: 12, l: 'Capitalized' }] : [{ a: 1, b: 7, l: 'Accrual releases' }, { a: 8, b: 12, l: 'Line costs capitalized' }];
    bands.forEach(b => { const x0 = x(b.a) - (x(1) - x(0)) / 2, x1 = x(b.b) + (x(1) - x(0)) / 2; out += `<g class="band"><rect x="${x0}" y="${pad.t - 6}" width="${x1 - x0}" height="${H - pad.b - pad.t + 6}"/><text x="${(x0 + x1) / 2}" y="${H - pad.b + 44}" text-anchor="middle">${b.l}</text></g>`; });
    // grid + axis
    out += `<g class="grid">${ticks.map(t => `<line x1="${pad.l}" x2="${W - pad.r}" y1="${y(t)}" y2="${y(t)}"/>`).join('')}</g>`;
    out += `<g class="axis">${ticks.map(t => `<text x="${pad.l - 8}" y="${y(t) + 4}" text-anchor="end">${fmtTick(t)}</text>`).join('')}<text x="${pad.l - 8}" y="${pad.t - 8}" text-anchor="end">${m.unit}</text></g>`;
    if (lo < 0) out += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${y(0)}" y2="${y(0)}" stroke="#7d796d" stroke-width="1"/>`;
    // gap area
    const segs = [];
    Q.forEach((q, i) => { const s = S[q]; if (s[m.rep] != null && s[m.cor] != null && s[m.cor] !== s[m.rep]) segs.push({ i, r: s[m.rep], c: s[m.cor] }); });
    if (this.showGap && segs.length) {
      // build polygons over contiguous runs (include neighbours where equal so the shape closes on the line)
      let run = []; const runs = [];
      Q.forEach((q, i) => { const s = S[q]; const c = cOf(s, i); if (s[m.rep] != null && c != null) { run.push({ i, r: s[m.rep], c }); } else { if (run.length) runs.push(run); run = []; } });
      if (run.length) runs.push(run);
      runs.forEach(r => { const top = r.map(p => `${x(p.i)},${y(p.c)}`).join(' '); const bot = r.slice().reverse().map(p => `${x(p.i)},${y(p.r)}`).join(' '); out += `<polygon class="gap" points="${top} ${bot}"/>`; });
    }
    // extra dashed (revenue questionable)
    if (m.extra && F == null) { const pts = Q.filter(q => S[q].revenue_corrected != null).map((q, i) => `${x(Q.indexOf(q))},${y(S[q].revenue_corrected - S[q][m.extra])}`); out += `<polyline points="${pts.join(' ')}" fill="none" stroke="#c0564d" stroke-width="1.2" stroke-dasharray="4 3"/>`; }
    // lines
    const repPts = Q.map((q, i) => S[q][m.rep] != null ? `${x(i)},${y(S[q][m.rep])}` : null).filter(Boolean);
    out += `<polyline class="line-reported" points="${repPts.join(' ')}"/>`;
    let corRuns = [], cur = [];
    Q.forEach((q, i) => { const s = S[q]; const c = cOf(s, i); if (c != null) cur.push(`${x(i)},${y(c)}`); else { if (cur.length) corRuns.push(cur); cur = []; } }); if (cur.length) corRuns.push(cur);
    corRuns.forEach(r => { out += `<polyline class="line-true" points="${r.join(' ')}"/>`; });
    // points + labels + hits
    let gapLabel = '';
    Q.forEach((q, i) => {
      const s = S[q]; const sel = q === this.selected; const r = s[m.rep], c = cOf(s, i);
      out += `<g class="pt ${sel ? 'selected' : ''}" data-q="${q}">`;
      if (r != null) out += `<circle class="halo" cx="${x(i)}" cy="${y(r)}" r="10" fill="rgba(39,73,109,0.14)" opacity="0"/><circle class="dot" cx="${x(i)}" cy="${y(r)}" r="4" fill="#27496d"/>`;
      if (c != null && c !== r) out += `<circle class="halo" cx="${x(i)}" cy="${y(c)}" r="10" fill="rgba(142,44,37,0.14)" opacity="0"/><circle class="dot" cx="${x(i)}" cy="${y(c)}" r="4" fill="#8e2c25"/>`;
      if (sel && r != null) {
        const lab = v => m.pct ? `${v.toFixed(1)}%` : fmt.m(v);
        const above = m.above; // corrected is above reported for cost metrics
        const ry = y(r), cy = c != null ? y(c) : null;
        out += `<text class="val reported" x="${x(i)}" y="${above ? ry + 16 : ry - 10}" text-anchor="middle">${lab(r)}</text>`;
        if (cy != null && c !== r) out += `<text class="val true" x="${x(i)}" y="${above ? cy - 10 : cy + 16}" text-anchor="middle">${lab(c)}</text>`;
        if (c != null && c !== r && !m.pct) {
          // Gap label: a small paper-coloured pill so the lines never run through the text.
          // It sits inside the gap when the gap is tall enough, otherwise stacked above the
          // upper value label. Painted after all points so neighbouring dots never cover it.
          const gap = Math.abs(c - r); const txt = `gap ${fmt.m(gap)}`;
          const tw = txt.length * 6.7 + 10, th = 16; const inside = Math.abs(ry - cy) >= th + 10;
          const gy = inside ? (ry + cy) / 2 : Math.max(th / 2 + 2, Math.min(ry, cy) - 28);
          const gx = Math.max(pad.l, Math.min(x(i) - tw / 2, W - pad.r - tw));
          gapLabel = `<g class="gaplabel"><rect x="${gx}" y="${gy - th / 2}" width="${tw}" height="${th}" rx="3"/><text x="${gx + tw / 2}" y="${gy + 4}" text-anchor="middle">${txt}</text></g>`;
        }
      }
      out += `<rect class="hit" x="${x(i) - (x(1) - x(0)) / 2}" y="${pad.t - 6}" width="${x(1) - x(0)}" height="${H - pad.t - pad.b + 30}"/>`;
      out += `<text class="qlabel ${sel ? 'sel' : ''}" x="${x(i)}" y="${H - pad.b + 16}" text-anchor="middle">${q.slice(4)}</text>`;
      if (i === 0 || q.endsWith('Q1')) out += `<text class="qlabel ${sel ? 'sel' : ''}" x="${x(i)}" y="${H - pad.b + 29}" text-anchor="middle">${q.slice(0, 4)}</text>`;
      out += `</g>`;
    });
    out += gapLabel;
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.innerHTML = out;
    const hoverable = window.matchMedia('(hover: hover)').matches;
    svg.querySelectorAll('.pt').forEach(g => {
      g.addEventListener('click', () => { this.tip.hidden = true; this.select(g.dataset.q); this.tipDismissed = g.dataset.q; });
      if (hoverable) {
        // A click dismisses its preview. Tiny pointer movement inside the selected column must not reopen it.
        g.addEventListener('mousemove', e => { if (this.tipDismissed !== g.dataset.q) this.showTip(e, g.dataset.q); });
        g.addEventListener('mouseleave', () => { this.tip.hidden = true; if (this.tipDismissed === g.dataset.q) this.tipDismissed = null; });
      }
    });
  }

  showTip(e, q) {
    const s = this.S.series[q]; const m = METRICS[this.metric]; const lab = v => v == null ? '—' : (m.pct ? v.toFixed(1) + '%' : '$' + fmt.m(v) + 'm');
    this.tip.innerHTML = `<div><b>${fmt.quarter(q)}</b> · ${m.title}</div><div class="mono r">reported ${lab(s[m.rep])}</div>${s[m.cor] != null && s[m.cor] !== s[m.rep] ? `<div class="mono t">corrected ${lab(s[m.cor])}</div>` : '<div class="mono">no improper entry identified for this metric</div>'}<div class="small" style="opacity:.75;margin-top:3px">Click to open the source pages</div>`;
    this.tip.hidden = false; const tw = this.tip.offsetWidth; this.tip.style.left = Math.min(window.innerWidth - tw - 8, e.clientX + 14) + 'px'; this.tip.style.top = (e.clientY + 14) + 'px';
  }

  renderCard() {
    const q = this.selected; if (!q) { this.card.innerHTML = ''; this.card.hidden = true; return; } this.card.hidden = false;
    const s = this.S.series[q]; const m = METRICS[this.metric];
    const repKey = { line_costs: 'line_costs', pretax: 'pretax', revenue: 'revenue', capex: 'capex', er: 'line_costs' }[this.metric];
    const repEntry = DATA.byId.get(s.ids[repKey]);
    const adjKey = this.metric === 'revenue' ? 'revenue_improper' : this.metric === 'capex' ? 'capitalized' : 'adjustment';
    const adjEntry = s.ids[adjKey] ? DATA.byId.get(s.ids[adjKey]) : null;
    const recId = { line_costs: 'rec_line_costs', pretax: 'rec_pretax', revenue: 'rec_revenue', capex: 'rec_capex', er: null }[this.metric];
    const recEntry = recId && s.ids[recId] ? DATA.byId.get(s.ids[recId]) : null;
    const secMetric = this.metric === 'line_costs' ? 'sec_actual_line_costs' : this.metric === 'pretax' ? 'sec_actual_pretax_income' : null;
    const secEntry = secMetric ? DATA.ledger.entries.find(e => e.track === 'sec_alleged' && e.metric === secMetric && e.period === q) : null;
    const chip = (entry, cls = '') => {
      if (!entry) return '';
      if (!entry.doc) { const comps = (entry.components || []).map(id => DATA.byId.get(id)).filter(Boolean); return comps.map(c => chip(c, cls)).join(' '); }
      const d = DATA.byDoc.get(entry.doc); return `<button class="chip ${cls}" data-id="${entry.id}" title="${esc(d.title)}">${esc(d.short)} <span class="pg">${entry.page_label && String(entry.page_label).startsWith('¶') ? esc(entry.page_label) : 'p. ' + esc(entry.page_label || entry.page)}</span></button>`;
    };
    const val = v => v == null ? '—' : (m.pct ? v.toFixed(1) + '%' : `${v < 0 ? '(' : ''}$${Math.abs(v).toLocaleString('en-US')}m${v < 0 ? ')' : ''}`);
    const moneyVal = v => v == null ? '—' : `${v < 0 ? '(' : ''}$${Math.abs(v).toLocaleString('en-US')}m${v < 0 ? ')' : ''}`;
    const repV = s[m.rep], corV = s[m.cor]; const adjV = adjEntry ? adjEntry.value : null;
    const adjDisplay = adjEntry ? (m.pct && corV != null && repV != null ? `${moneyVal(adjV)} <span class="small muted">(+${(corV - repV).toFixed(1)} pp)</span>` : moneyVal(adjV)) : '<small>none identified</small>';
    const mech = s.mechanism === 'accrual_release' ? 'accrual release' : s.mechanism === 'capitalization' ? 'capitalized as "prepaid capacity"' : '';
    const accRel = s.mechanism === 'accrual_release' ? (s.line_cost_reduction || 0) : 0;
    const capRed = s.mechanism === 'capitalization' ? (s.line_cost_reduction || 0) : 0;
    const capPPE = s.capitalized || 0;
    let eqHtml = '';
    if (this.metric === 'line_costs') {
      eqHtml = `<div class="qc-equation"><span class="eq-kicker">Restatement Equation ✓</span><span class="eq-formula">Reported <b>$${fmt.m(s.line_costs_reported)}m</b> + Phase I Accrual Release <b>$${fmt.m(accRel)}m</b> + Phase II Capitalized Reduction <b>$${fmt.m(capRed)}m</b>${capPPE && capPPE !== capRed ? ` <span class="muted">($${fmt.m(capPPE)}m to PP&E + $${fmt.m(capRed - capPPE)}m other)</span>` : ''} = Restated Actual <b class="true">$${fmt.m(s.line_costs_corrected)}m</b></span></div>`;
    } else if (this.metric === 'pretax') {
      eqHtml = `<div class="qc-equation"><span class="eq-kicker">Restatement Equation ✓</span><span class="eq-formula">Reported Pre-Tax <b>${val(s.pretax_reported)}</b> − Accrual Releases <b>$${fmt.m(accRel)}m</b> − Capitalized Capacity <b>$${fmt.m(capRed)}m</b> = Corrected Pre-Tax <b class="true">${val(s.pretax_corrected)}</b></span></div>`;
    } else if (this.metric === 'revenue') {
      eqHtml = `<div class="qc-equation"><span class="eq-kicker">Restatement Equation ✓</span><span class="eq-formula">Reported Revenue <b>$${fmt.m(s.revenue_reported)}m</b> − Improper "Close the Gap" Entries <b>$${fmt.m(s.revenue_improper || 0)}m</b> = Corrected Revenue <b class="true">$${fmt.m(s.revenue_corrected)}m</b>${s.revenue_questionable ? ` <span class="muted">(plus $${fmt.m(s.revenue_questionable)}m questionable items)</span>` : ''}</span></div>`;
    } else if (this.metric === 'capex') {
      eqHtml = `<div class="qc-equation"><span class="eq-kicker">Restatement Equation ✓</span><span class="eq-formula">Reported CapEx <b>$${fmt.m(s.capex_reported)}m</b> − Capitalized "Prepaid Capacity" Line Costs <b>$${fmt.m(capPPE)}m</b> = Corrected CapEx <b class="true">$${fmt.m(s.capex_corrected != null ? s.capex_corrected : s.capex_reported)}m</b></span></div>`;
    } else if (this.metric === 'er') {
      eqHtml = `<div class="qc-equation"><span class="eq-kicker">E/R Ratio Identity ✓</span><span class="eq-formula">Reported <b>$${fmt.m(s.line_costs_reported)}m ÷ $${fmt.m(s.revenue_reported)}m = ${s.er_reported.toFixed(1)}%</b> → Corrected <b class="true">$${fmt.m(s.line_costs_corrected)}m ÷ $${fmt.m(s.revenue_corrected)}m = ${s.er_corrected.toFixed(1)}%</b> <span class="muted">(+${(s.er_corrected - s.er_reported).toFixed(1)} pp hidden expense share)</span></span></div>`;
    }
    this.card.innerHTML = `
      <div class="qc-head"><h3>${fmt.quarter(q)} · ${m.title}</h3><span class="small muted">${repEntry && repEntry.track === 'reported-derived' ? 'Q4 derived: fiscal year (10-K) minus nine months (Q3 10-Q)' : repEntry ? DATA.byDoc.get(repEntry.doc).title.replace(' (as filed)', '') : ''}</span></div>
      <div class="cell"><div class="lab">Reported</div><div class="v reported">${val(repV)}</div>${chip(repEntry, 'k-reported')}</div>
      <div class="cell"><div class="lab">${this.metric === 'revenue' ? 'Improper revenue entries' : this.metric === 'capex' ? 'Line costs capitalized' : 'Improper line-cost reduction'}${mech ? ` <span class="muted">· ${mech}</span>` : ''}</div><div class="v adj">${adjDisplay}</div>${adjEntry ? chip(adjEntry, 'k-true') : ''}</div>
      <div class="cell"><div class="lab">Corrected <span class="tag reconstructed">reconstruction</span></div><div class="v true">${val(corV)}</div>${recEntry && adjEntry ? `<span class="small muted num">= ${fmt.m(repV)} ${m.above ? '+' : '−'} ${fmt.m(Math.abs(adjV))}</span>` : recEntry ? `<span class="small muted">${esc(recEntry.formula)}</span>` : corV === repV ? '<span class="small muted">no adjustment this quarter</span>' : ''}</div>
      ${eqHtml}
      <div class="qc-foot">
        <button class="btn" data-act="pair">Open both pages</button>
        ${secEntry ? `<span>SEC First Amended Complaint puts the actual figure at <b class="num">${val(secEntry.value)}</b> ${chip(secEntry)}</span>` : ''}
        ${this.metric === 'line_costs' && q === '2001Q2' ? '<span class="muted">The SEC counted $560m (the capitalized part); the Committee counted $610m including other adjustments.</span>' : ''}
      </div>`;
    this.card.querySelectorAll('button.chip').forEach(b => b.addEventListener('click', ev => { ev.stopPropagation(); const e = DATA.byId.get(b.dataset.id); this.viewer.show(citeFromEntry(e)); }));
    this.card.querySelector('[data-act="pair"]').addEventListener('click', () => this.openPair(q));
  }

  renderAnnual() {
    const A = this.S.annual; const el = this.root.querySelector('.annual');
    const find = (track, metric, period) => DATA.ledger.entries.find(e => e.track === track && e.metric === metric && e.period === period);
    const cell = (entry, v) => entry ? `<button class="cite" data-id="${entry.id}">${fmt.m(v == null ? entry.value : v)}</button>` : (v == null ? '—' : fmt.m(v));
    const rows = [['1999', '1999FY'], ['2000', '2000FY'], ['2001', '2001FY'], ['Q1 2002', '2002Q1']].map(([lab, per]) => {
      const a = A[per === '2002Q1' ? '2002Q1' : per.slice(0, 4)];
      const comm = find('committee_summary', 'committee_improper_line_costs', per); const commT = find('committee_summary', 'committee_improper_total', per);
      const aug = find('company_disclosure', 'company_announced_pretax_reduction', per); const tenk = find('restated', 'restatement_pretax_improper_reduction_of_access_costs', per);
      return `<tr><td>${lab}</td><td class="num">${fmt.m(a.quarterly_line_cost_reductions)}</td><td class="num">${cell(comm)}</td><td class="num">${cell(commT)}</td><td class="num">${cell(aug)}</td><td class="num">${tenk ? cell(tenk, -tenk.value) : '—'}</td></tr>`;
    }).join('');
    el.innerHTML = `<table><thead><tr><th>Period</th><th class="num">Ledger: quarterly line-cost entries</th><th class="num">Committee: line costs</th><th class="num">Committee: all areas</th><th class="num">Company, Aug 8 2002</th><th class="num">2002 10-K: access costs</th></tr></thead><tbody>${rows}</tbody></table>
      <p class="note">$ millions. The first column sums the quarter-by-quarter line-cost entries used in the chart (Special Investigative Committee, pp. 64 and 105–116). The Committee's own annual table (p. 17) includes further line-cost items and other areas; the company's August 2002 announcement predates the Committee's work; the 2002 Form 10-K's restatement category is on a different (access-cost) basis and sits alongside $59.8bn of impairments. Click any figure to open its page.</p>`;
    el.querySelectorAll('button.cite').forEach(b => b.addEventListener('click', () => this.viewer.show(citeFromEntry(DATA.byId.get(b.dataset.id)))));
  }

  renderRestatement() {
    const el = this.root.querySelector('.restate');
    const cats = [['impairment', 'Impairment of goodwill and PP&E'], ['improper_reduction_of_access_costs', 'Improper reduction of access costs'], ['purchase_accounting', 'Purchase accounting'], ['long_lived_asset_adjustments', 'Long-lived asset adjustments'], ['international', 'International'], ['revenue_related_adjustments', 'Revenue-related adjustments'], ['adjustments_to_accrued_liabilities', 'Accrued liabilities'], ['embratel_and_avantel', 'Embratel and Avantel'], ['unclassified_income_expense', 'Unclassified income / (expense)'], ['other', 'Other']];
    const find = (metric, period) => DATA.ledger.entries.find(e => e.track === 'restated' && e.metric === metric && e.period === period);
    let html = '';
    ['2001FY', '2000FY'].forEach(per => {
      const prev = find('restatement_pretax_previously_reported', per); const tot = find('restatement_pretax_total_restatement_adjustments', per); const rest = find('restatement_pretax_pretax_loss_as_restated', per);
      const maxAbs = Math.max(...cats.map(([k]) => { const e = find(`restatement_pretax_${k}`, per); return e ? Math.abs(e.value) : 0; }));
      html += `<div class="bars" style="margin-top:14px"><div class="bl" style="font-family:var(--font-serif);font-size:16px;color:var(--ink)">${per.slice(0, 4)}</div><div class="small muted">pre-tax income: previously reported <button class="cite num" data-id="${prev.id}" style="border-bottom:1px dotted var(--true)">${fmt.m(prev.value)}</button> → restated <button class="cite num" data-id="${rest.id}" style="color:var(--true);border-bottom:1px dotted var(--true)">${fmt.m(rest.value)}</button></div><div class="bv">${fmt.m(tot.value)}</div>`;
      cats.forEach(([k, lab]) => { const e = find(`restatement_pretax_${k}`, per); if (!e) return; const w = Math.abs(e.value) / maxAbs * 100; html += `<button class="bl cite" data-id="${e.id}">${lab}</button><div class="bar"><i class="${e.value > 0 ? 'pos' : ''}" style="left:0;width:${w}%"></i></div><div class="bv">${fmt.m(e.value)}</div>`; });
      html += `</div>`;
    });
    html += `<p class="note">$ millions, pre-tax effect, from the "Summary of restatement items" table (Note 2, p. F-26). The red bars reduce income; the green bar increases it. The improper line-cost entries are one category of a far larger restatement: the write-down of goodwill from the MCI and other acquisitions dominates. Net loss as restated: 2001 $(15,597)m against $1,501m reported; 2000 $(48,909)m against $4,153m reported.</p>
      <p class="note">"Previously reported" here is the 2002 10-K's own column, whose footnote (1) reads "Certain amounts have been reclassified to conform to the current statement of operations presentation"; the chart and the SEC rows use the figures as originally filed (pre-tax income ${fmt.m(DATA.byId.get('rep:2001FY:pretax_income').value)} in the 2001 10-K and ${fmt.m(DATA.byId.get('rep:2000FY:pretax_income').value)} in the 2000 10-K, against ${fmt.m(DATA.byId.get('restated:2001FY:restatement_pretax_previously_reported').value)} and ${fmt.m(DATA.byId.get('restated:2000FY:restatement_pretax_previously_reported').value)} here).</p>`;
    el.innerHTML = html;
    el.querySelectorAll('.cite').forEach(b => b.addEventListener('click', () => this.viewer.show(citeFromEntry(DATA.byId.get(b.dataset.id)))));
  }
}

function niceTicks(lo, hi, n) {
  const span = hi - lo; const raw = span / n; const p = Math.pow(10, Math.floor(Math.log10(raw))); const steps = [1, 2, 2.5, 5, 10];
  let step = p; for (const s of steps) { if (raw / p <= s) { step = s * p; break; } }
  const out = []; for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) out.push(+v.toFixed(6)); return out;
}
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
