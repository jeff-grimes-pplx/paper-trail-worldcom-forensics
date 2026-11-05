// Searchable ledger with provenance. Every row with a document opens its page; derived/reconstructed rows list their components.
import { DATA, fmt, TRACK_LABEL, TRACK_SHORT, docShort } from './data.js';
import { citeFromEntry } from './viewer.js';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const METRIC_LABEL = m => m.replace(/^restatement_/, 'restatement: ').replace(/^sec_alleged_/, 'SEC alleged: ').replace(/^sec_actual_/, 'SEC actual: ').replace(/^sec_reported_/, 'SEC: reported ').replace(/^committee_/, 'Committee: ').replace(/^company_announced_/, 'announced: ').replace(/_/g, ' ').replace(/\bsga\b/, 'SG&A').replace(/\bebitda\b/, 'EBITDA').replace(/\bpretax\b/, 'pre-tax').replace(/\bppe\b/i, 'PP&E');

export function renderLedger(root, viewer) {
  const all = DATA.ledger.entries; const verified = new Set((DATA.verification && DATA.verification.rows || []).filter(r => r.result === 'match').map(r => r.id));
  let q = '', track = 'all', period = 'all', sortKey = 'period', sortDir = 1, selected = null;
  const tracks = [...new Set(all.map(e => e.track))]; const periods = [...new Set(all.map(e => e.period))].sort();
  root.innerHTML = `<div class="sec-head-row">
      <div>
        <h2>Ledger</h2>
        <p class="lede">${all.length} values. ${DATA.ledger.meta.cited} carry a document, page and anchor text; the rest are arithmetic on cited values (fourth quarters derived from annual minus nine-month figures, and the corrected series) and list their components. Search by metric, period, document or note; click a row to open its page.</p>
      </div>
      <div class="workbook-strip" aria-label="Export complete forensic ledger">
        <span class="wb-kicker">One-Click Forensic Audit Export</span>
        <div class="wb-btns">
          <a class="wb-btn primary" href="data/WorldCom_Forensic_Audit_Workbook.xlsx" download="WorldCom_Forensic_Audit_Workbook.xlsx">↓ Excel Workbook (.xlsx · 6 tabs)</a>
          <a class="wb-btn" href="data/WorldCom_Forensic_Audit_Ledger.csv" download="WorldCom_Forensic_Audit_Ledger.csv">↓ CSV (453 rows)</a>
          <a class="wb-btn" href="data/ledger.json" download="WorldCom_Forensic_Ledger.json">↓ JSON</a>
        </div>
      </div>
    </div>
    <div class="ledger-tools"><input type="search" placeholder="Search — e.g. 2001Q1, line costs, Beresford, F-26, 3,055" aria-label="Search ledger">
      <select class="track" aria-label="Track"><option value="all">All tracks</option>${tracks.map(t => `<option value="${t}">${TRACK_LABEL[t] || t}</option>`).join('')}</select>
      <select class="period" aria-label="Period"><option value="all">All periods</option>${periods.map(p => `<option value="${p}">${p}</option>`).join('')}</select>
      <span class="ledger-count"></span></div>
    <div class="ledger-wrap"><table class="ledger"><colgroup><col style="width:68px"><col style="width:118px"><col><col style="width:78px"><col style="width:154px"><col style="width:74px"><col style="width:84px"></colgroup><thead><tr><th data-k="period">Period</th><th data-k="track">Track</th><th data-k="label">Item</th><th class="num" data-k="value">$m</th><th data-k="doc">Source</th><th>Page</th><th>Check</th></tr></thead><tbody></tbody></table></div>`;
  const input = root.querySelector('input'); const tsel = root.querySelector('.track'); const psel = root.querySelector('.period'); const tbody = root.querySelector('tbody'); const count = root.querySelector('.ledger-count');
  input.addEventListener('input', () => { q = input.value.trim().toLowerCase(); draw(); });
  tsel.addEventListener('change', () => { track = tsel.value; draw(); }); psel.addEventListener('change', () => { period = psel.value; draw(); });
  root.querySelectorAll('th[data-k]').forEach(th => th.addEventListener('click', () => { const k = th.dataset.k; if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; } draw(); }));

  function rows() {
    let list = all;
    if (track !== 'all') list = list.filter(e => e.track === track);
    if (period !== 'all') list = list.filter(e => e.period === period);
    if (q) { const terms = q.split(/\s+/); list = list.filter(e => { const d = e.doc ? DATA.byDoc.get(e.doc) : null; const hay = `${e.id} ${e.period} ${e.track} ${e.label} ${e.metric} ${e.value} ${fmt.m(e.value)} ${e.note || ''} ${e.formula || ''} ${d ? d.short + ' ' + d.title + ' ' + d.id : ''} ${e.page_label || ''} ${e.anchor || ''}`.toLowerCase(); return terms.every(t => hay.includes(t)); }); }
    const key = e => sortKey === 'value' ? e.value : sortKey === 'doc' ? (e.doc || '~') : sortKey === 'label' ? e.label : sortKey === 'track' ? e.track : e.period;
    return list.slice().sort((a, b) => { const ka = key(a), kb = key(b); return (ka < kb ? -1 : ka > kb ? 1 : a.id.localeCompare(b.id)) * sortDir; });
  }
  function draw() {
    const list = rows(); count.textContent = `${list.length} of ${all.length}`;
    const lim = list.slice(0, 600);
    tbody.innerHTML = lim.map(e => {
      const d = e.doc ? DATA.byDoc.get(e.doc) : null;
      const page = e.page_label && String(e.page_label).startsWith('¶') ? e.page_label : (e.page ? `p. ${e.page_label || e.page}` : '');
      const src = d ? `<span title="${esc(d.title)}">${esc(docShort(d))}</span>` : `<span class="muted">${esc((e.components || []).length ? 'from ' + e.components.length + ' cited value' + (e.components.length > 1 ? 's' : '') : '')}</span>`;
      const unit = e.unit && e.unit !== 'USD millions' ? ` <span class="muted small">${esc(e.unit)}</span>` : (/pct$/.test(e.metric) ? '%' : '');
      const item = e.label === e.metric.replace(/_/g, ' ') || e.label === METRIC_LABEL(e.metric) ? METRIC_LABEL(e.metric) : e.label;
      return `<tr class="row ${selected === e.id ? 'sel' : ''}" data-id="${e.id}" title="${esc(e.note || '')}"><td class="mono">${esc(e.period)}</td><td><span class="tag ${e.track}">${esc(TRACK_SHORT[e.track] || e.track)}</span></td><td class="item">${esc(item)}${e.formula ? `<span class="n">${esc(e.formula)}</span>` : ''}</td><td class="num mono">${fmt.m(e.value)}${unit}</td><td class="src">${src}</td><td class="src"><span class="pg">${esc(page)}</span></td><td>${verified.has(e.id) ? '<span class="ok">✓ visual</span>' : e.anchor_found ? '<span class="muted small">text</span>' : ''}</td></tr>`;
    }).join('') + (list.length > lim.length ? `<tr><td colspan="7" class="muted small">Showing the first ${lim.length}; refine the search to see the rest.</td></tr>` : '');
    tbody.querySelectorAll('tr.row').forEach(tr => tr.addEventListener('click', () => open(tr.dataset.id)));
  }
  function open(id) {
    const e = DATA.byId.get(id); if (!e) return; selected = id; tbody.querySelectorAll('tr.row').forEach(tr => tr.classList.toggle('sel', tr.dataset.id === id));
    if (e.doc) { viewer.show(citeFromEntry(e)); return; }
    const comps = (e.components || []).map(c => DATA.byId.get(c)).filter(Boolean);
    const cites = []; for (const c of comps) { if (c.doc) cites.push(citeFromEntry(c, `Component of ${e.label} (${e.period}): ${e.formula || ''}`)); else (c.components || []).forEach(cc => { const x = DATA.byId.get(cc); if (x && x.doc) cites.push(citeFromEntry(x, `Component of ${e.label} (${e.period})`)); }); if (cites.length >= 2) break; }
    if (cites.length) viewer.show(cites);
  }
  draw();
  return { search(text) { input.value = text; q = text.toLowerCase(); draw(); }, open };
}
