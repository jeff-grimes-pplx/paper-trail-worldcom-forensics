// Data access for Paper Trail. Everything is static JSON produced by the tools/ pipeline.
const cache = new Map();

async function getJSON(path) {
  if (!cache.has(path)) {
    cache.set(path, fetch(path, { cache: 'force-cache' }).then(r => {
      if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`);
      return r.json();
    }).catch(err => { cache.delete(path); throw err; }));
  }
  return cache.get(path);
}

export const DATA = {
  register: null, byDoc: new Map(), ledger: null, byId: new Map(), series: null, timeline: null, highlights: null, pagecounts: null, verification: null, pdfPages: null,
};

export async function loadCore() {
  const [register, ledger, series, timeline, highlights, pagecounts, verification, pdfPages] = await Promise.all([
    getJSON('data/register.json'), getJSON('data/ledger.json'), getJSON('data/series.json'), getJSON('data/timeline.json'),
    getJSON('data/pdf-highlights.json'), getJSON('data/pagecounts.json'), getJSON('data/verification.json').catch(() => null), getJSON('data/pdf-pages/index.json').catch(() => null),
  ]);
  DATA.register = register; register.forEach(d => DATA.byDoc.set(d.id, d));
  DATA.ledger = ledger; ledger.entries.forEach(e => DATA.byId.set(e.id, e));
  DATA.series = series; DATA.timeline = timeline; DATA.highlights = highlights; DATA.pagecounts = pagecounts; DATA.verification = verification; DATA.pdfPages = pdfPages || {};
  return DATA;
}

export function loadPages(docId) { return getJSON(`data/pages/${docId}.json`); }

export const fmt = {
  m(v, { sign = false, dash = '—' } = {}) {
    if (v === null || v === undefined || Number.isNaN(v)) return dash;
    const abs = Math.abs(v); const s = abs.toLocaleString('en-US', { maximumFractionDigits: 0 });
    if (v < 0) return `(${s})`;
    return (sign && v > 0 ? '+' : '') + s;
  },
  bn(v, digits = 1) { if (v === null || v === undefined) return '—'; const s = (Math.abs(v) / 1000).toFixed(digits); return (v < 0 ? '−' : '') + '$' + s + 'bn'; },
  pct(v) { return v === null || v === undefined ? '—' : v.toFixed(1) + '%'; },
  quarter(q) { const m = /^(\d{4})Q(\d)$/.exec(q); return m ? `Q${m[2]} ${m[1]}` : q.replace('FY', ' (year)').replace('H1', ' (six months)').replace('M9', ' (nine months)'); },
  period(p) { if (/Q\d$/.test(p)) return fmt.quarter(p); if (/FY$/.test(p)) return p.slice(0, 4); return p; },
  date(d) {
    const m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(d); if (!m) return d;
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
    if (!m[2]) return m[1];
    if (!m[3]) return `${months[+m[2] - 1]} ${m[1]}`;
    return `${months[+m[2] - 1]} ${+m[3]}, ${m[1]}`;
  },
};

export const TRACK_LABEL = {
  'reported': 'Reported (as filed)', 'reported-derived': 'Reported, derived', 'adjustment': 'Special Committee finding', 'committee_summary': 'Special Committee summary',
  'sec_alleged': 'SEC amended complaint', 'company_disclosure': 'Company 8-K', 'restated': 'Company restatement (2004)', 'reconstructed': 'Reconstruction',
};

export const TRACK_SHORT = {
  'reported': 'Reported', 'reported-derived': 'Derived', 'adjustment': 'Committee finding', 'committee_summary': 'Committee summary',
  'sec_alleged': 'SEC complaint', 'company_disclosure': 'Company 8-K', 'restated': 'Restated (2004)', 'reconstructed': 'Reconstruction',
};
const SHORTEST = { 'beresford-report': 'Committee report (2003)', 'sec-amended-complaint-2002-11-05': 'SEC Am. Complaint (2002)', '10k-2002': 'Form 10-K · FY 2002' };
export function docShort(doc) { return SHORTEST[doc.id] || doc.short; }

export function valueTexts(v) {
  if (v === null || v === undefined) return [];
  const abs = Math.abs(v); const s = abs.toLocaleString('en-US', { maximumFractionDigits: 0 });
  const out = [];
  if (v < 0) { out.push(`(${s})`, `(${s} )`); }
  out.push(s);
  if (abs >= 1000) { const b = (abs / 1000); out.push(`$${b.toFixed(3)} billion`, `$${b.toFixed(1)} billion`, `$${b.toFixed(2)} billion`); }
  out.push(`$${s} million`);
  return out;
}
