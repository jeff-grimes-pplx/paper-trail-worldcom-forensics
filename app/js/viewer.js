// Document viewer: renders the frozen page (text / HTML / PDF image) at a citation and highlights the anchor.
import { DATA, loadPages, valueTexts } from './data.js';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const norm = s => s.replace(/[\u2018\u2019\u201B]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/\s+/g, ' ').trim();

function originalLink(doc, page, pageRec) {
  if (doc.kind === 'pdf') return `${doc.url}#page=${page}`;
  return doc.url;
}

/** Highlight `needle` inside `container` across text nodes, ignoring all whitespace differences. Returns the first <mark> or null. */
function highlightText(container, needle, cls = 'hl') {
  const want = norm(needle).replace(/\s+/g, '');
  if (!want) return null;
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement && n.parentElement.closest('script,style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  const map = []; let text = ''; let n;
  while ((n = walker.nextNode())) {
    const s = n.nodeValue.replace(/[\u2018\u2019\u201B]/g, "'").replace(/[\u201C\u201D]/g, '"');
    for (let i = 0; i < s.length; i++) { const ch = s[i]; if (/\s/.test(ch)) continue; text += ch; map.push({ node: n, off: i }); }
  }
  let idx = text.indexOf(want);
  if (idx < 0) idx = text.toLowerCase().indexOf(want.toLowerCase());
  if (idx < 0) return null;
  const end = idx + want.length;
  const ranges = []; let cur = null;
  for (let i = idx; i < end; i++) {
    const m = map[i]; if (!m) break;
    if (cur && cur.node === m.node) cur.end = m.off + 1; else { cur = { node: m.node, start: m.off, end: m.off + 1 }; ranges.push(cur); }
  }
  let first = null;
  for (let r = ranges.length - 1; r >= 0; r--) {
    const { node, start, end: e } = ranges[r];
    if (!node.parentNode) continue;
    const range = document.createRange(); range.setStart(node, start); range.setEnd(node, Math.min(e, node.nodeValue.length));
    const mark = document.createElement('mark'); mark.className = cls;
    try { range.surroundContents(mark); first = mark; } catch (err) { /* ignore */ }
  }
  return first;
}

export class DocPane {
  constructor(root) {
    this.root = root; this.doc = null; this.pages = null; this.page = 1; this.cite = null;
    root.className = 'docpane';
    root.innerHTML = `<div class="dp-head"><div class="dp-row1"><div class="dp-title"></div><div class="dp-kind"></div></div>
      <div class="dp-row2"><div class="dp-nav"><button class="prev" aria-label="Previous page">‹</button><input class="pg" aria-label="Page"><span class="lab"></span><button class="next" aria-label="Next page">›</button></div>
      <div class="dp-links"><button type="button" class="sha-badge" hidden title="Click to copy full 64-character SHA-256 filing digest"></button><a class="orig" target="_blank" rel="noopener">Open original ↗</a></div></div>
      <div class="dp-why" hidden></div></div>
      <div class="dp-body"><div class="dp-empty">Select a figure, an event or a document to open the page that supports it.</div></div>
      <div class="dp-foot"><span class="f1"></span><span class="f2"></span></div>`;
    this.$ = sel => root.querySelector(sel);
    this.$('.prev').addEventListener('click', () => this.goto(this.page - 1));
    this.$('.next').addEventListener('click', () => this.goto(this.page + 1));
    this.$('.pg').addEventListener('change', e => { const v = parseInt(e.target.value, 10); if (v) this.goto(v); });
    this.$('.pg').addEventListener('keydown', e => { if (e.key === 'Enter') { const v = parseInt(e.target.value, 10); if (v) this.goto(v); } });
    this.$('.sha-badge').addEventListener('click', () => {
      const btn = this.$('.sha-badge');
      const full = btn.dataset.sha || '';
      if (!full) return;
      if (navigator.clipboard) navigator.clipboard.writeText(full).catch(() => {});
      const prev = btn.textContent;
      btn.textContent = `Copied ${full.slice(0, 12)}…`;
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = prev; btn.classList.remove('copied'); }, 1500);
    });
  }

  /** cite: {doc, page, anchor, why, value, label, valueText?} */
  async open(cite) {
    this.cite = cite;
    const doc = DATA.byDoc.get(cite.doc);
    if (!doc) return;
    const body = this.$('.dp-body');
    if (!this.doc || this.doc.id !== doc.id || !this.pages) {
      this.doc = doc; this.pages = null;
      body.innerHTML = `<div class="dp-empty">Loading ${esc(doc.short)}…</div>`;
      this.$('.dp-title').textContent = doc.short; this.$('.dp-title').title = doc.title;
      this.$('.dp-kind').textContent = doc.kind_label;
      try { this.pages = (await loadPages(doc.id)).pages; } catch (err) { body.innerHTML = `<div class="dp-empty">Could not load this document (${esc(err.message)}).</div>`; return; }
      if (this.cite !== cite) return; // superseded
    }
    const p = Math.max(1, Math.min(this.pages.length, cite.page || 1));
    this.render(p, p === cite.page || !cite.page ? cite : { ...cite, page: p, why: `Requested page ${cite.page} is outside this document (${this.pages.length} pages); showing page ${p}.` });
  }

  /** Clear the pane with a short message (used when a pair has no second page). */
  empty(msg) {
    this.cite = null; this.doc = null; this.pages = null;
    this.$('.dp-title').textContent = ''; this.$('.dp-kind').textContent = ''; this.$('.pg').value = ''; this.$('.lab').textContent = ''; this.$('.orig').removeAttribute('href');
    const sb = this.$('.sha-badge'); if (sb) { sb.hidden = true; sb.textContent = ''; sb.dataset.sha = ''; }
    this.$('.dp-why').hidden = true; this.$('.dp-row2').hidden = true;
    this.$('.f1').textContent = ''; this.$('.f2').textContent = '';
    this.$('.dp-body').innerHTML = `<div class="dp-empty">${esc(msg || '')}</div>`;
  }

  goto(p) {
    if (!this.pages) return;
    p = Math.max(1, Math.min(this.pages.length, p));
    this.render(p, p === (this.cite && this.cite.page) ? this.cite : null);
  }

  render(p, cite) {
    const doc = this.doc, pages = this.pages, rec = pages[p - 1];
    this.page = p;
    const body = this.$('.dp-body');
    this.$('.pg').value = p;
    const printed = rec.label && rec.label !== String(p) ? `printed p. ${rec.label}` : (rec.label ? `p. ${rec.label}` : '');
    this.$('.lab').textContent = `of ${pages.length}${printed ? ' · ' + printed : ''}${rec.doctype && rec.doctype !== '10-Q' && rec.doctype !== '10-K' ? ' · ' + rec.doctype : ''}`;
    this.$('.orig').href = originalLink(doc, p, rec); this.$('.dp-row2').hidden = false;
    const sb = this.$('.sha-badge');
    if (sb && doc.sha256) {
      sb.hidden = false;
      sb.dataset.sha = doc.sha256;
      sb.textContent = `SHA-256 ✓ ${doc.sha256.slice(0, 10)}…`;
      sb.title = `Verified file SHA-256: ${doc.sha256} (click to copy)`;
    }
    const why = this.$('.dp-why');
    if (cite && (cite.why || cite.label)) {
      why.hidden = false;
      why.innerHTML = `<span>${cite.entryId ? `<code class="dp-entry-id">${esc(cite.entryId)}</code> ` : ''}<b>${esc(cite.label || '')}</b>${cite.value !== undefined && cite.value !== null ? ` · <span class="num">${esc(cite.valueDisplay || cite.value)}</span>` : ''}</span>` +
        (cite.why ? `<span>${esc(cite.why)}</span>` : '') + (cite.anchor ? `<span class="q">“${esc(cite.anchor.length > 110 ? cite.anchor.slice(0, 110) + '…' : cite.anchor)}”</span>` : '');
    } else { why.hidden = true; }
    this.$('.f1').textContent = `${doc.kind === 'edgar-txt' ? 'Pages split at the filing\'s own <PAGE> markers' : doc.kind === 'edgar-html' ? 'Pages split at the filing\'s own page breaks' : doc.kind === 'pdf' ? 'Physical PDF page' : 'Single HTML document; located by paragraph'}`;
    this.$('.f2').textContent = `sha256 ${doc.sha256.slice(0, 16)}… · filed ${doc.filed || ''}`;

    let sheet;
    if (doc.kind === 'edgar-txt') {
      sheet = document.createElement('div'); sheet.className = 'sheet txt';
      const pre = document.createElement('pre'); pre.textContent = rec.text; sheet.appendChild(pre);
      const maxLen = rec.text.split('\n').reduce((m, l) => Math.max(m, l.replace(/\s+$/, '').length), 0);
      sheet.dataset.maxlen = maxLen;
    } else if (doc.kind === 'edgar-html' || doc.kind === 'html') {
      sheet = document.createElement('div'); sheet.className = 'sheet html'; sheet.innerHTML = rec.html || `<pre>${esc(rec.text)}</pre>`;
      sheet.querySelectorAll('a').forEach(a => { a.removeAttribute('href'); });
    } else { // pdf
      sheet = document.createElement('div'); sheet.className = 'sheet pdf';
      const img = new Image(); img.alt = `${doc.short}, page ${p}`; img.decoding = 'async';
      const wrap = document.createElement('div'); wrap.style.position = 'relative'; wrap.appendChild(img);
      const showText = () => {
        wrap.innerHTML = `<div class="pdf-missing">Page image not bundled for this uncited page — showing the extracted text. <a href="${esc(doc.url)}#page=${p}" target="_blank" rel="noopener">Open the original PDF at page ${p} ↗</a></div><div class="pdf-text"></div>`;
        wrap.querySelector('.pdf-text').textContent = rec.text;
        if (cite && cite.anchor) highlightText(wrap.querySelector('.pdf-text'), cite.anchor);
      };
      img.addEventListener('error', showText);
      const bundled = DATA.pdfPages && DATA.pdfPages[doc.id];
      if (bundled && !bundled.includes(p)) showText(); else img.src = `data/pdf-pages/${doc.id}/${p}.jpg`;
      sheet.appendChild(wrap);
      if (cite && cite.anchor) {
        const hl = DATA.highlights[`${doc.id}:${p}`];
        const rects = hl && hl[cite.anchor];
        if (rects && rects.length) {
          rects.forEach(r => { const d = document.createElement('div'); d.className = 'hl'; d.style.left = (r.x * 100) + '%'; d.style.top = (r.y * 100) + '%'; d.style.width = (r.w * 100) + '%'; d.style.height = (r.h * 100) + '%'; wrap.appendChild(d); });
          this._scrollTarget = rects[0];
        }
      }
    }
    body.innerHTML = ''; body.appendChild(sheet);
    body.scrollTop = 0;
    if (sheet.dataset.maxlen) this.fitText(sheet);
    if (cite && cite.anchor && doc.kind !== 'pdf') {
      const mark = highlightText(sheet, cite.anchor);
      if (mark) {
        // emphasise the specific figure inside the highlighted span when we know it
        const vts = cite.valueTexts || (cite.value !== undefined ? valueTexts(cite.value) : []);
        const marks = [...sheet.querySelectorAll('mark.hl')];
        let strong = null;
        outer: for (const vt of vts) { for (const mk of marks) { strong = highlightText(mk, vt, 'hl strong'); if (strong) break outer; } }
        requestAnimationFrame(() => { const t = strong || mark; const bb = t.getBoundingClientRect(); const bodyRect = body.getBoundingClientRect(); body.scrollTop += bb.top - bodyRect.top - bodyRect.height * 0.38;
          const sh = sheet.classList.contains('txt') ? sheet : null; if (sh && sh.scrollWidth > sh.clientWidth) { sh.scrollLeft = Math.max(0, bb.left - sheet.getBoundingClientRect().left - sh.clientWidth * 0.6); } });
      }
    } else if (cite && cite.anchor && doc.kind === 'pdf' && this._scrollTarget) {
      const r = this._scrollTarget; const img = sheet.querySelector('img');
      const place = () => { const h = img.clientHeight || (img.naturalHeight * img.clientWidth / (img.naturalWidth || 1)); body.scrollTop = Math.max(0, r.y * h - body.clientHeight * 0.38); };
      if (img.complete && img.naturalHeight) place(); else img.addEventListener('load', place, { once: true });
      this._scrollTarget = null;
    }
  }
}

DocPane.prototype.fitText = function (sheet) {
  const body = this.$('.dp-body'); const pre = sheet.querySelector('pre'); const maxLen = +sheet.dataset.maxlen || 80;
  const avail = Math.max(240, body.clientWidth - 32 - 48);
  const size = Math.max(8.2, Math.min(11.6, avail / (maxLen * 0.602)));
  pre.style.fontSize = size.toFixed(2) + 'px';
  if (!this._fitBound) { this._fitBound = true; new ResizeObserver(() => { const sh = body.querySelector('.sheet.txt'); if (sh) this.fitText(sh); }).observe(body); }
};

export class Viewer {
  constructor(root) {
    this.root = root; this.panesEl = root.querySelector('#panes'); this.panes = [];
    this.layoutBtn = root.querySelector('#viewer-layout'); this.two = true;
    this.layoutBtn.addEventListener('click', () => this.setTwo(!this.two));
    root.querySelector('#viewer-close').addEventListener('click', () => root.classList.remove('open'));
    this.setTwo(true);
  }
  setTwo(two) {
    this.two = two; this.layoutBtn.textContent = two ? 'One page' : 'Two pages';
    this.panesEl.classList.toggle('two', two);
    while (this.panes.length < (two ? 2 : 1)) { const el = document.createElement('div'); this.panesEl.appendChild(el); this.panes.push(new DocPane(el)); }
    while (this.panes.length > (two ? 2 : 1)) { const p = this.panes.pop(); p.root.remove(); }
  }
  /** Show one citation (top pane) or a pair [a, b]. */
  show(cites, { reveal = true } = {}) {
    const list = Array.isArray(cites) ? cites : [cites];
    const mobile = window.matchMedia('(max-width: 900px)').matches;
    if (list.length > 1 && !this.two) this.setTwo(true);
    else if (mobile && list.length === 1 && this.two && list[0] && list[0].doc) this.setTwo(false);
    list.slice(0, this.panes.length).forEach((c, i) => { if (c && c.doc) this.panes[i].open(c); else if (c && c.empty) this.panes[i].empty(c.empty); });
    if (reveal && window.matchMedia('(max-width: 900px)').matches) this.root.classList.add('open');
  }
}

/** Build a citation object from a ledger entry. */
export function citeFromEntry(e, why) {
  if (!e || !e.doc) return null;
  const doc = DATA.byDoc.get(e.doc);
  return { entryId: e.id, track: e.track, doc: e.doc, page: e.page, anchor: e.anchor, label: e.label, value: e.value, valueDisplay: formatValue(e), why: why || `${TRACKWHY[e.track] || e.track} · ${periodText(e.period)}`, valueTexts: valueTexts(e.value), docShort: doc && doc.short };
}
const TRACKWHY = { reported: 'As reported', 'reported-derived': 'Derived', adjustment: 'Special Investigative Committee', committee_summary: 'Special Investigative Committee', sec_alleged: 'SEC First Amended Complaint', company_disclosure: 'Company announcement', restated: 'Company restatement', reconstructed: 'Reconstruction' };
function periodText(p) { const m = /^(\d{4})Q(\d)$/.exec(p); if (m) return `Q${m[2]} ${m[1]}`; if (/FY$/.test(p)) return `FY ${p.slice(0, 4)}`; return p; }
function formatValue(e) {
  if (e.unit && e.unit !== 'USD millions') return `${e.value} ${e.unit}`;
  if (/pct$/.test(e.metric)) return `${e.value}%`;
  const abs = Math.abs(e.value).toLocaleString('en-US', { maximumFractionDigits: 0 });
  return (e.value < 0 ? `($${abs})` : `$${abs}`) + ' million';
}
