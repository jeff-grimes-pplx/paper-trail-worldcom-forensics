// Timeline of mechanism, disclosure, whistleblower and enforcement events, each opening its primary source page.
import { DATA, fmt } from './data.js';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const KINDS = [['all', 'All'], ['mechanism', 'Mechanism'], ['concealment', 'Concealment'], ['disclosure', 'Disclosure'], ['whistleblower', 'Discovery'], ['enforcement', 'SEC'], ['congress', 'Congress'], ['bankruptcy', 'Bankruptcy'], ['court', 'Court'], ['criminal', 'Criminal'], ['restatement', 'Restatement']];
const KIND_LABEL = Object.fromEntries(KINDS);

export function renderTimeline(root, viewer) {
  const events = DATA.timeline.slice().sort((a, b) => a.date.localeCompare(b.date));
  let filter = 'all'; let selected = null;
  root.innerHTML = `<h2>From the first entry to the last sentence</h2>
    <p class="lede">${events.length} dated events, each with the page of the primary document that records it: the Special Investigative Committee's report, SEC complaints and litigation releases, Congressional testimony, court opinions and the company's own filings.</p>
    <div class="tl-filters" role="tablist"></div><div class="tl"></div>`;
  const filters = root.querySelector('.tl-filters'); const list = root.querySelector('.tl');
  KINDS.forEach(([k, lab]) => { const n = k === 'all' ? events.length : events.filter(e => e.kind === k).length; if (!n) return; const b = document.createElement('button'); b.textContent = `${lab} ${n}`; b.dataset.kind = k; b.classList.toggle('active', k === filter); b.addEventListener('click', () => { filter = k; filters.querySelectorAll('button').forEach(x => x.classList.toggle('active', x.dataset.kind === k)); draw(); }); filters.appendChild(b); });

  function draw() {
    let html = ''; let year = null;
    events.filter(e => filter === 'all' || e.kind === filter).forEach(e => {
      const y = e.date.slice(0, 4); if (y !== year) { year = y; html += `<div class="year"><span>${y}</span></div>`; }
      const d = DATA.byDoc.get(e.doc);
      const pg = e.page_label && String(e.page_label).startsWith('¶') ? e.page_label : (d && d.kind === 'html' ? 'full text' : `p. ${e.page_label || e.page}`);
      html += `<div class="ev k-${e.kind} ${selected === e.id ? 'sel' : ''}" data-id="${e.id}" tabindex="0" role="button" aria-label="${esc(e.title)}">
        <div class="d">${fmt.date(e.date)}</div>
        <h3 class="t">${esc(e.title)}</h3>
        <p class="b">${esc(e.body)}</p>
        <div class="src"><span class="tag ${e.kind === 'court' || e.kind === 'criminal' ? 'court' : e.kind === 'enforcement' ? 'sec_alleged' : e.kind === 'mechanism' || e.kind === 'concealment' ? 'adjustment' : e.kind === 'disclosure' || e.kind === 'restatement' ? 'reported' : ''}">${KIND_LABEL[e.kind] || e.kind}</span><span class="chip" title="${esc(d ? d.title : '')}">${esc(d ? d.short : e.doc)} <span class="pg">${esc(pg)}</span></span><a class="small" href="${esc(e.url)}" target="_blank" rel="noopener">original ↗</a></div>
      </div>`;
    });
    list.innerHTML = html;
    list.querySelectorAll('.ev').forEach(el => {
      const open = () => { selected = el.dataset.id; list.querySelectorAll('.ev').forEach(x => x.classList.toggle('sel', x === el)); const e = events.find(v => v.id === selected); viewer.show({ doc: e.doc, page: e.page, anchor: e.anchor, label: e.title, why: `${fmt.date(e.date)} · ${KIND_LABEL[e.kind] || e.kind}` }); };
      el.addEventListener('click', ev => { if (ev.target.closest('a')) return; open(); });
      el.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); open(); } });
    });
  }
  draw();
  return { select(id) { selected = id; draw(); const el = list.querySelector(`.ev[data-id="${id}"]`); if (el) el.click(); } };
}
