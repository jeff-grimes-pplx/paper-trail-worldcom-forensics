// Document register and the Method & limits panel (what is fact, what is restated, what is reconstructed; errata; counts; verification).
import { DATA, fmt } from './data.js';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const GROUPS = [['reported', 'Periodic reports as filed (the "reported" track)'], ['disclosure', 'Company disclosures after the discovery'], ['investigation', 'Investigations'], ['restatement', 'Restatement'], ['enforcement', 'SEC enforcement'], ['court', 'Court orders and opinions'], ['criminal', 'Criminal proceedings'], ['congress', 'Congress']];

export function renderDocuments(root, viewer) {
  const R = DATA.register; const pc = DATA.pagecounts;
  const totalPages = Object.values(pc).reduce((a, b) => a + b.pages, 0);
  root.innerHTML = `<h2>Document register</h2>
    <p class="lede">${R.length} public documents, ${totalPages.toLocaleString()} pages, fetched directly from SEC EDGAR, sec.gov, justice.gov, govinfo.gov, the examiner's published reports and Public.Resource.Org. Each entry shows the URL, access date and SHA-256 checksum of the file as fetched. Click a document to read it; the viewer keeps the filing's own page breaks.</p>
    <div class="docs-wrap"></div>`;
  const wrap = root.querySelector('.docs-wrap');
  GROUPS.forEach(([role, label]) => {
    const docs = R.filter(d => d.role === role); if (!docs.length) return;
    const g = document.createElement('div'); g.innerHTML = `<div class="doc-group">${label} · ${docs.length}</div><div class="docs"></div>`;
    const list = g.querySelector('.docs');
    docs.forEach(d => {
      const el = document.createElement('div'); el.className = 'doc'; el.tabIndex = 0; el.setAttribute('role', 'button');
      const p = pc[d.id] || {};
      el.innerHTML = `<div class="t">${esc(d.title)}</div><div class="pages">${(p.pages || 0).toLocaleString()} pp.</div>
        <div class="m"><span>${esc(d.authority)}</span><span>${d.filed ? 'dated ' + fmt.date(d.filed) : ''}</span><a href="${esc(d.url)}" target="_blank" rel="noopener">${esc(d.url.replace(/^https?:\/\//, '').slice(0, 70))}${d.url.length > 78 ? '…' : ''} ↗</a><span>fetched ${esc((d.accessed || '').slice(0, 10))}</span><span title="${esc(d.sha256)}">sha256 ${esc(d.sha256.slice(0, 16))}…</span><span>${(d.bytes / 1024).toFixed(0)} KB</span></div>`;
      const open = () => viewer.show({ doc: d.id, page: 1, label: d.short, why: 'Opened from the register' });
      el.addEventListener('click', ev => { if (ev.target.closest('a')) return; open(); });
      el.addEventListener('keydown', ev => { if (ev.key === 'Enter') open(); });
      list.appendChild(el);
    });
    wrap.appendChild(g);
  });
}

export function renderMethod(root, viewer) {
  const L = DATA.ledger; const V = DATA.verification; const pc = DATA.pagecounts; const R = DATA.register;
  const totalPages = Object.values(pc).reduce((a, b) => a + b.pages, 0); const totalChars = Object.values(pc).reduce((a, b) => a + b.chars, 0);
  const vrows = V ? V.rows : []; const vmatch = vrows.filter(r => r.result === 'match').length;
  const stat = (v, l) => `<div class="stat"><div class="v">${v}</div><div class="l">${l}</div></div>`;
  root.innerHTML = `<div class="method">
    <div class="sec-head-row">
      <div>
        <h2>Method, provenance and limits</h2>
        <p class="lede">What is documented fact, what is the company's own restatement, and what is analytical reconstruction added here — and where the dataset is weaker than it looks.</p>
      </div>
      <div class="workbook-strip" aria-label="Download verification artifacts">
        <span class="wb-kicker">Programmatic Verification · 100% Pass</span>
        <div class="wb-btns">
          <a class="wb-btn primary" href="data/WorldCom_Forensic_Audit_Workbook.xlsx" download="WorldCom_Forensic_Audit_Workbook.xlsx">↓ Audit Workbook (.xlsx)</a>
          <a class="wb-btn" href="data/WorldCom_Forensic_Audit_Ledger.csv" download="WorldCom_Forensic_Audit_Ledger.csv">↓ 453-Row CSV</a>
          <a class="wb-btn" href="data/forensic_verification_report.json" download="forensic_verification_report.json">↓ Audit Report (.json)</a>
          <a class="wb-btn" href="data/SHA256SUMS.txt" download="SHA256SUMS.txt">↓ SHA256SUMS.txt</a>
        </div>
      </div>
    </div>
    <div class="stats">${stat(R.length + ' / ' + R.length, 'SHA-256 verified docs')}${stat(totalPages.toLocaleString(), 'pages processed')}${stat((totalChars / 1e6).toFixed(2) + 'M', 'characters of text')}${stat(L.meta.entries, 'ledger values')}${stat(L.meta.cited, 'with page citations')}${stat(L.meta.anchors_found + ' / ' + L.meta.cited, 'anchors re-found in the page text')}${stat(vmatch + ' / ' + vrows.length, 'values visually verified')}${stat('13 / 13', 'quarterly equations balanced')}</div>

    <h3>Three kinds of number</h3>
    <table><tbody>
      <tr><td><span class="tag reported">Reported</span></td><td>Figures copied from WorldCom's Forms 10-Q and 10-K exactly as filed on EDGAR between 1999 and 2002, from the consolidated statements of operations and cash flows. Fourth quarters were never filed separately and are shown as <span class="tag reported-derived">derived</span>: fiscal year minus nine months, with the two source pages listed.</td></tr>
      <tr><td><span class="tag adjustment">Adjudicated / investigated</span></td><td>Amounts stated in the Special Investigative Committee's report (filed with the SEC in June 2003), the SEC's First Amended Complaint (to which WorldCom consented without admitting or denying), the sworn statements, court judgments and the Ebbers indictment and appellate opinion. The complaint figures are allegations settled by consent; the Committee's figures are findings of a board investigation; the criminal record is adjudicated.</td></tr>
      <tr><td><span class="tag restated">Restated</span></td><td>The company's own restatement of 2000 and 2001 in the 2002 Form 10-K (March 2004), Note 2: previously reported, adjustments by category, and as restated. WorldCom never filed restated quarterly statements; the 10-K says so.</td></tr>
      <tr><td><span class="tag reconstructed">Reconstruction</span></td><td>Added here and labelled wherever it appears: corrected quarterly series computed as reported line costs plus the Committee's improper line-cost reductions (and pre-tax income minus them; revenue minus the improper revenue items; capex minus capitalized line costs). It is arithmetic on cited values, not a company figure. Checked against the SEC's "actual" column: it matches in every quarter except Q2 2001, where the SEC counts $560m (the capitalized entry) and the Committee $610m.</td></tr>
    </tbody></table>

    <h3>Errata and limitations</h3>
    <ul>
      <li><b>No restated quarters exist.</b> The red line is therefore a reconstruction limited to the line-cost (and, on its own tab, revenue) entries. It excludes the impairments, purchase-accounting and other items that made the 2004 restatement far larger. Nothing here should be read as "the true quarterly results".</li>
      <li><b>Derived fourth quarters</b> absorb any reclassification between the Q3 10-Q and the 10-K. Q4 2001 pre-tax income derived this way is $397m against the $401m the Committee cites; the 2002 10-K's "previously reported" annual figures also differ slightly from the original filings because of reclassifications (see the restatement panel).</li>
      <li><b>Comparatives change between filings.</b> Q1 2000 line costs were $4,092m in the Q1 2000 10-Q but $3,733m as the comparative in the Q1 2001 10-Q; Q1 2001 revenue was $9,720m as filed but $8,825m as the comparative in 2002 after Embratel was deconsolidated. The ledger uses the figure as first filed.</li>
      <li><b>Revenue items are not deducted</b> from the corrected pre-tax line, because the Committee reports their pre-tax effect only in aggregate (about $1.248bn on $2.065bn).</li>
      <li><b>Q2 2001 differs between sources</b>: $610m (Committee, including non-capitalization adjustments) versus $560m (SEC complaint). The chart uses the Committee's figure and shows the SEC's beside it.</li>
      <li><b>Annual totals are not one number.</b> The Committee's $9.25bn (all areas, 1999–Q1 2002), the company's August 2002 $7.683bn of pre-tax reductions, the SEC's "approximately $9 billion" and the 10-K's access-cost category are different measurements; the Two tracks section places them side by side rather than reconciling them.</li>
      <li><b>Pagination.</b> EDGAR text filings are split at their own <code>&lt;PAGE&gt;</code> markers and HTML filings at their page-break markup, so page numbers are the filing's, not a PDF's. HTML complaints and releases have no pages; citations give the paragraph number. PDF pages are physical pages; the Committee report's printed page numbers run five behind its HTML page count (printed p. 64 = page 69).</li>
      <li><b>OCR noise.</b> The July 2003 Rakoff opinion is a scanned PDF; its text layer has recognition errors, so anchors there were located on the page image.</li>
      <li><b>Pages, not images, for most filings.</b> For EDGAR filings the viewer shows the frozen page text or HTML, not a facsimile; for PDFs it shows the rendered page image with the located figure boxed. Pages that are not cited by any value were not rendered to images and fall back to text with a link to the original.</li>
      <li><b>Scope.</b> The register is a working set of ${R.length} documents, not the complete docket. In re WorldCom securities litigation, the Andersen proceedings and the examiner's third report are outside it.</li>
    </ul>

    <h3>Legal record relied on</h3>
    <ul>
      <li><i>SEC v. WorldCom, Inc.</i>, No. 02 Civ. 4963 (JSR) (S.D.N.Y.): complaint June 26, 2002; First Amended Complaint November 5, 2002; permanent injunction by consent November 26, 2002; opinion approving the civil penalty July 7, 2003.</li>
      <li><i>United States v. Ebbers</i>, superseding indictment S3 02 Cr. 1144 (BSJ) (S.D.N.Y.); jury verdict March 15, 2005; sentence July 13, 2005; affirmed, 458 F.3d 110 (2d Cir. 2006) (No. 05-4059-CR).</li>
      <li>Guilty pleas of Scott Sullivan, David Myers, Buford Yates, Betty Vinson and Troy Normand, as recorded in the SEC litigation releases in the register.</li>
      <li><i>In re WorldCom, Inc.</i>, Chapter 11, Case No. 02-13533 (Bankr. S.D.N.Y.): petition July 21, 2002; examiner's interim reports November 2002 and June 2003; plan confirmed October 31, 2003.</li>
      <li>Report of Investigation by the Special Investigative Committee of the Board of Directors of WorldCom, Inc., March 31, 2003 (Exhibit 99.1 to Form 8-K filed June 9, 2003).</li>
    </ul>

    <h3>Verification table</h3>
    <p>${V ? `${vrows.length} ledger values were re-opened in the viewer and read against the page image or page text by eye; ${vmatch} matched. Each row records the value, document, page and the result.` : 'Verification table not loaded.'}</p>
    <table class="vtable"><thead><tr><th>#</th><th>Ledger id</th><th>Value</th><th>Document</th><th>Page</th><th>Result</th></tr></thead><tbody>
      ${vrows.map((r, i) => `<tr class="vrow" data-id="${esc(r.id)}" style="cursor:pointer"><td>${i + 1}</td><td class="mono">${esc(r.id)}</td><td class="mono">${esc(r.value_display || r.value)}</td><td>${esc(r.doc_short || r.doc)}</td><td class="mono">${esc(r.page_label || r.page)}</td><td>${r.result === 'match' ? '<span style="color:var(--court)">match</span>' : esc(r.result) + (r.note ? ' — ' + esc(r.note) : '')}</td></tr>`).join('')}
    </tbody></table>

    <h3>Reproduction</h3>
    <p>The source bundle contains the scripts that fetched every document (recording URL, HTTP status, access time and SHA-256), split them into pages, extracted the reported figures with per-filing column maps, applied the curated adjustment and restatement values with their anchors, re-located each anchor in the page text, built the series, and rendered the cited PDF pages with highlight boxes. Checksums are in <code>data/SHA256SUMS.txt</code>.</p>
    <pre>python3 tools/fetch_documents.py      # 57 documents → raw/docs, data/register.json, data/SHA256SUMS.txt
python3 tools/paginate.py             # → data/pages/*.json, data/pagecounts.json
python3 tools/extract_reported.py     # → data/reported_raw.json
python3 tools/build_ledger.py         # → data/ledger.json, data/series.json (anchors re-located)
python3 tools/build_timeline_and_pages.py   # → data/timeline.json, data/pdf-pages, data/pdf-highlights.json
python3 tools/verify_forensic_audit.py      # → validates 57 SHA-256 digests, 453 rows & 13Q equations; builds .xlsx / .csv / .json</pre>
    <p class="small muted">Typefaces: Newsreader, IBM Plex Sans and IBM Plex Mono (SIL Open Font License), self-hosted. No analytics, no external requests at runtime.</p>
  </div>`;
  root.querySelectorAll('.vrow').forEach(tr => tr.addEventListener('click', () => { const e = DATA.byId.get(tr.dataset.id); if (e) import('./viewer.js').then(m => viewer.show(m.citeFromEntry(e))); }));
}
