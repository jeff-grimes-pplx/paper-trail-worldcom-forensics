// Mechanism explainer: three schematics of how the numbers were moved, each with the quarterly amounts and page citations.
import { DATA, fmt } from './data.js';
import { citeFromEntry } from './viewer.js';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function entries(track, metric) { return DATA.ledger.entries.filter(e => e.track === track && e.metric === metric && /^\d{4}Q\d$/.test(e.period)).sort((a, b) => a.period.localeCompare(b.period)); }
function pageEntry(page) { return DATA.ledger.entries.find(e => e.doc === 'beresford-report' && e.page === page); }

function miniBars(list, { x, y, w, h, max, second = null, labelEvery = 1 }) {
  const n = list.length; const bw = Math.min(34, (w / n) * 0.62); const gap = w / n; let out = `<g class="mini">`;
  list.forEach((e, i) => {
    const cx = x + gap * i + gap / 2; const bh = h * (e.value / max); const sec = second ? second.find(s => s.period === e.period) : null;
    out += `<g data-id="${e.id}">`;
    out += `<rect x="${cx - bw / 2}" y="${y + h - bh}" width="${bw}" height="${bh}"/>`;
    if (sec) { const sh = h * (sec.value / max); out += `<rect class="cap" x="${cx - bw / 2 + 2}" y="${y + h - sh}" width="${bw - 4}" height="${sh}" data-id="${sec.id}"/>`; }
    out += `<text class="v" x="${cx}" y="${y + h - bh - 3}" text-anchor="middle">${fmt.m(e.value)}</text>`;
    if (i % labelEvery === 0) out += `<text x="${cx}" y="${y + h + 11}" text-anchor="middle">${fmt.quarter(e.period)}</text>`;
    out += `<rect class="hit" x="${cx - gap / 2}" y="${y - 12}" width="${gap}" height="${h + 26}" data-id="${e.id}"><title>${fmt.quarter(e.period)}: $${fmt.m(e.value)}m — open the page</title></rect></g>`;
  });
  return out + `</g>`;
}

function box(x, y, w, h, cls, title, sub) {
  let o = `<rect class="box ${cls}" x="${x}" y="${y}" width="${w}" height="${h}" rx="2"/>`;
  o += `<text class="bt h" x="${x + 10}" y="${y + 18}">${esc(title)}</text>`;
  if (sub) sub.split('\n').forEach((s, i) => { o += `<text class="bs" x="${x + 10}" y="${y + 34 + i * 13}">${esc(s)}</text>`; });
  return o;
}
const DEFS = `<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#8e2c25"/></marker></defs>`;

export function renderMechanism(root, viewer) {
  const acc = entries('adjustment', 'line_cost_reduction').filter(e => e.mechanism === 'accrual_release');
  const cap = entries('adjustment', 'line_cost_reduction').filter(e => e.mechanism === 'capitalization');
  const capPart = entries('adjustment', 'line_costs_capitalized');
  const revI = entries('adjustment', 'revenue_improper'); const revQ = entries('adjustment', 'revenue_questionable');
  const cite = (page, label) => { const e = pageEntry(page); return `<button class="chip" data-doc="beresford-report" data-page="${page}" ${e ? `data-id="${e.id}"` : ''}>Special Committee report <span class="pg">p. ${label}</span></button>`; };

  root.innerHTML = `
    <h2>How the numbers were moved</h2>
    <p class="lede">Three devices, documented entry by entry in the Special Investigative Committee's report (filed with the SEC as an 8-K exhibit in June 2003) and alleged in the SEC's First Amended Complaint. Inspect the interactive General-Ledger Sankey & Double-Entry T-Accounts below, or click any bar to open the primary filing page.</p>

    <div class="mech gl-workbench" id="mech-gl-workbench">
      <div class="gl-wb-head">
        <div>
          <h3>Interactive General-Ledger Double-Entry Trace &amp; Sankey Flow</h3>
          <div class="when">Filter by fraud phase or individual quarter (Q2 1999 – Q1 2002) to trace every top-side debit and credit across the Income Statement and Balance Sheet</div>
        </div>
      </div>
      <div class="gl-filter-bar" role="tablist" aria-label="General ledger period filter"></div>
      <div class="gl-sankey-wrap"></div>
      <div class="t-accounts-grid"></div>
    </div>

    <div class="mech" id="mech-1">
      <h3>1 · Release the reserves</h3>
      <div class="when">Q2 1999 – Q4 2000 · $3,297 million</div>
      <svg viewBox="0 0 720 230">${DEFS}
        ${box(14, 22, 180, 62, 'liab', 'Line-cost accruals (liability)', 'estimates of bills not yet received\nfrom other carriers')}
        <path class="arrow" d="M196 53 L266 53"/><text class="flow" x="231" y="14" text-anchor="middle">"release"</text>
        ${box(270, 22, 180, 62, 'exp', 'Line cost expense  ↓', 'credited by the released amount,\nno analysis of the underlying bills')}
        <path class="arrow" d="M452 53 L522 53"/>
        ${box(526, 22, 180, 62, '', 'Pre-tax income  ↑', 'by the same amount, in the\nquarter the entry was booked')}
        <text class="bs" x="14" y="112">Reductions to line costs from accrual releases, by quarter ($m)</text>
        ${miniBars(acc, { x: 14, y: 120, w: 690, h: 84, max: 900 })}
      </svg>
      <p>The Committee describes three abuses: accruals released without any analysis of whether an excess existed; excess accruals kept as "rainy day funds" and released when results needed help; and accruals established for other purposes released against line costs — including, in Q4 2000, $407 million from the Tax group's deferred federal income tax accrual.</p>
      <div class="cites">${cite(69, '64')}${cite(94, '89')}${cite(14, '9')}</div>
    </div>

    <div class="mech" id="mech-2">
      <h3>2 · Move the expense onto the balance sheet</h3>
      <div class="when">Q1 2001 – Q1 2002 · $3,883 million of reductions, about $3.5 billion of it capitalized</div>
      <svg viewBox="0 0 720 250">${DEFS}
        ${box(14, 22, 180, 62, 'exp', 'Line cost expense  ↓', 'operating cost of leased\nnetwork capacity')}
        <path class="arrow" d="M196 53 L266 53"/><text class="flow" x="231" y="14" text-anchor="middle">"prepaid capacity"</text>
        ${box(270, 22, 180, 62, 'asset', 'Property, plant & equipment  ↑', 'round-dollar entries after the\nclose, with no support')}
        <path class="arrow grey" d="M452 53 L522 53"/>
        ${box(526, 22, 180, 62, '', 'Depreciated over years', 'and reported as capital spending:\ncapex overstated by the same sum')}
        <text class="bs" x="14" y="112">Reduction in line costs by quarter ($m); inner bar = amount capitalized</text>
        ${miniBars(cap, { x: 14, y: 120, w: 690, h: 96, max: 1000, second: capPart })}
      </svg>
      <p>With the reserves exhausted and the line-cost ratio heading past 50% of revenues, the Q1 2001 close was met by transferring $544 million of line costs to capital accounts — $771 million of reductions in total. The transfers continued every quarter until Internal Audit found them in May–June 2002. The entries were made by Betty Vinson and Troy Normand at the direction of Buford Yates, David Myers and Scott Sullivan.</p>
      <div class="cites">${cite(110, '105')}${cite(113, '108')}${cite(115, '110')}${cite(119, '114')}${cite(121, '116')}${cite(16, '11')}</div>
    </div>

    <div class="mech" id="mech-3">
      <h3>3 · "Close the Gap" on revenue</h3>
      <div class="when">1999 – Q1 2002 · $958 million improper, a further $1,107 million questionable</div>
      <svg viewBox="0 0 720 250">${DEFS}
        ${box(14, 22, 180, 62, 'rev', 'Revenue target', 'double-digit growth promised\nto analysts')}
        <path class="arrow grey" d="M196 53 L266 53"/><text class="flow" x="231" y="14" text-anchor="middle">the gap</text>
        ${box(270, 22, 180, 62, '', 'Actual monthly revenue (MonRev)', 'tracked by Business Operations\nand Revenue Accounting')}
        <path class="arrow" d="M452 53 L522 53"/><text class="flow" x="487" y="14" text-anchor="middle">after the close</text>
        ${box(526, 22, 180, 62, 'rev', 'Corporate Unallocated entries', 'large, round, late items that\nbridged the difference')}
        <text class="bs" x="14" y="112">Improper revenue entries by quarter ($m, labelled); light bars add the "questionable" items</text>
        ${miniBarsStacked(revI, revQ, { x: 14, y: 120, w: 690, h: 96, max: 300 })}
      </svg>
      <p>Revenue entries were smaller than the line-cost entries, but they were how the published growth rate was met. Most were booked to a "Corporate Unallocated" account after the quarter had closed, outside the normal revenue process; the Committee's advisors estimate the pre-tax effect of the combined $2.065 billion at about $1.248 billion.</p>
      <div class="cites">${cite(136, '131')}${cite(19, '14')}${cite(152, '147')}</div>
    </div>

    <div class="mech" id="mech-4">
      <h3>4 · Why it stayed hidden, and how it surfaced</h3>
      <p>The entries were top-side journal entries made after the operating units had closed their books, so the people running the network never saw them. Distribution of the monthly revenue report (MonRev) was limited and access to it closely guarded; management rejected Arthur Andersen's repeated requests for access to the computerized general ledger, and Andersen did not conduct substantive tests of capital expenditures. The capitalization was found by Internal Audit's capital-expenditure audit in May–June 2002, confirmed when the Controller admitted there was no support, taken to the Audit Committee on June 20, and announced on June 25, 2002.</p>
      <div class="cites">${cite(18, '13')}${cite(141, '136')}${cite(252, '247')}${cite(242, '237')}${cite(129, '124')}${cite(130, '125')}${cite(132, '127')}</div>
    </div>`;

  root.querySelectorAll('.mini [data-id]').forEach(el => el.addEventListener('click', () => { const e = DATA.byId.get(el.dataset.id); if (e) viewer.show(citeFromEntry(e)); }));
  root.querySelectorAll('.cites .chip').forEach(b => b.addEventListener('click', () => {
    const e = b.dataset.id ? DATA.byId.get(b.dataset.id) : null;
    if (e) viewer.show(citeFromEntry(e)); else viewer.show({ doc: b.dataset.doc, page: +b.dataset.page, label: 'Special Investigative Committee report', why: 'Cited page' });
  }));
  mountGLWorkbench(root.querySelector('#mech-gl-workbench'), viewer);
}

const OFFICERS_BY_Q = {
  '1999Q2': 'Scott Sullivan (CFO) · David Myers (Controller) · Buford Yates (Dir. General Accounting)',
  '1999Q3': 'Scott Sullivan (CFO) · David Myers (Controller) · Buford Yates (Dir. General Accounting)',
  '1999Q4': 'Scott Sullivan · David Myers · Buford Yates · Betty Vinson (International & Telco Accruals)',
  '2000Q1': 'Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2000Q2': 'Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2000Q3': 'Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2000Q4': 'Scott Sullivan · David Myers · Buford Yates · Tax Group ($407m Deferred Tax Reserve Release)',
  '2001Q1': 'Bernard Ebbers · Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2001Q2': 'Bernard Ebbers · Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2001Q3': 'Bernard Ebbers · Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2001Q4': 'Bernard Ebbers · Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
  '2002Q1': 'Bernard Ebbers · Scott Sullivan · David Myers · Buford Yates · Betty Vinson · Troy Normand',
};

function mountGLWorkbench(wbRoot, viewer) {
  if (!wbRoot) return;
  const filterBar = wbRoot.querySelector('.gl-filter-bar');
  const sankeyWrap = wbRoot.querySelector('.gl-sankey-wrap');
  const tGrid = wbRoot.querySelector('.t-accounts-grid');
  const S = DATA.series.series;
  const Q = DATA.series.quarters;

  const filters = [
    { key: 'ALL', label: 'All 13 Quarters ($7,180m)' },
    { key: 'PHASE1', label: 'Phase I · Accruals (Q2 99–Q4 00 · $3,297m)' },
    { key: 'PHASE2', label: 'Phase II · CapEx (Q1 01–Q1 02 · $3,883m)' },
    ...Q.filter(q => q !== '1999Q1').map(q => ({ key: q, label: fmt.quarter(q).replace(' 19', ' ’').replace(' 20', ' ’') })),
  ];

  let activeFilter = 'ALL';

  function getFilteredQuarters(k) {
    if (k === 'ALL') return Q;
    if (k === 'PHASE1') return Q.filter(q => S[q].mechanism === 'accrual_release');
    if (k === 'PHASE2') return Q.filter(q => S[q].mechanism === 'capitalization');
    return [k];
  }

  function openProofForFilter(k, focusType = 'line_costs') {
    const q = (k === 'ALL' || k === 'PHASE2') ? '2001Q1' : (k === 'PHASE1' ? '2000Q3' : k);
    const s = S[q];
    if (!s) return;
    if (focusType === 'revenue') {
      const repE = DATA.byId.get(s.ids.revenue);
      const adjE = s.ids.revenue_improper ? DATA.byId.get(s.ids.revenue_improper) : null;
      const cites = [];
      if (repE && repE.doc) cites.push(citeFromEntry(repE, `Reported Revenue · ${fmt.quarter(q)}`));
      else if (repE && repE.components) { const c = DATA.byId.get(repE.components[0]); if (c) cites.push(citeFromEntry(c)); }
      if (adjE) cites.push(citeFromEntry(adjE, `Improper "Close the Gap" Revenue · ${fmt.quarter(q)}`));
      if (cites.length) viewer.show(cites);
      return;
    }
    const repE = DATA.byId.get(s.ids.line_costs);
    const adjE = s.ids.adjustment ? DATA.byId.get(s.ids.adjustment) : null;
    const cites = [];
    if (repE && repE.doc) cites.push(citeFromEntry(repE, `Reported Line Costs · ${fmt.quarter(q)}`));
    else if (repE && repE.components) { const c = DATA.byId.get(repE.components[0]); if (c) cites.push(citeFromEntry(c)); }
    if (adjE) cites.push(citeFromEntry(adjE, `Improper General-Ledger Entry · ${fmt.quarter(q)}`));
    if (cites.length) viewer.show(cites);
  }

  function render(k) {
    activeFilter = k;
    filterBar.innerHTML = filters.map(f => `<button type="button" class="gl-fbtn ${f.key === k ? 'active' : ''}" data-fk="${f.key}">${esc(f.label)}</button>`).join('');
    filterBar.querySelectorAll('.gl-fbtn').forEach(b => b.addEventListener('click', () => render(b.dataset.fk)));

    const qs = getFilteredQuarters(k);
    let lcActual = 0, lcReported = 0, accRel = 0, capRed = 0, capPPE = 0, revImp = 0, revQuest = 0, ptiRep = 0, ptiCor = 0;
    qs.forEach(q => {
      const s = S[q];
      lcActual += s.line_costs_corrected || 0;
      lcReported += s.line_costs_reported || 0;
      if (s.mechanism === 'accrual_release') accRel += s.line_cost_reduction || 0;
      if (s.mechanism === 'capitalization') capRed += s.line_cost_reduction || 0;
      capPPE += s.capitalized || 0;
      revImp += s.revenue_improper || 0;
      revQuest += s.revenue_questionable || 0;
      ptiRep += s.pretax_reported || 0;
      ptiCor += s.pretax_corrected || 0;
    });
    const totalFraud = accRel + capRed;
    const otherCapAdj = capRed - capPPE;
    const scopeLabel = k === 'ALL' ? 'Cumulative 1999Q1–2002Q1 (13 Quarters)' : k === 'PHASE1' ? 'Phase I: Q2 1999 – Q4 2000 (7 Quarters)' : k === 'PHASE2' ? 'Phase II: Q1 2001 – Q1 2002 (5 Quarters)' : `${fmt.quarter(k)} Single-Quarter General-Ledger Trace`;
    const sampleQ = (k === 'ALL' || k === 'PHASE2') ? '2001Q1' : (k === 'PHASE1' ? '2000Q3' : k);
    const officers = OFFICERS_BY_Q[sampleQ] || 'Scott Sullivan (CFO) · David Myers (Controller) · Buford Yates (Dir. General Accounting)';

    // Proportional ribbon heights for SVG Sankey (left node = 152px tall, right boxes non-overlapping)
    const H_TOT = 148;
    const hRep = Math.max(44, Math.round(H_TOT * (lcReported / Math.max(1, lcActual))));
    const hFraudPool = Math.max(40, H_TOT - hRep);
    const hAcc = accRel > 0 ? Math.max(24, Math.round(hFraudPool * (accRel / Math.max(1, totalFraud)))) : 0;
    const hCap = capRed > 0 ? Math.max(24, hFraudPool - hAcc) : 0;

    const y0 = 16;
    const leftH = Math.max(116, hRep + hAcc + hCap);
    const boxRepH = Math.max(44, hRep);
    const boxAccH = hAcc > 0 ? Math.max(44, hAcc) : 0;
    const boxCapH = hCap > 0 ? Math.max(44, hCap) : 0;

    const yRepR = 14;
    const yAccR = yRepR + boxRepH + 10;
    const yCapR = hAcc > 0 ? (yAccR + boxAccH + 10) : (yRepR + boxRepH + 10);
    const maxRightY = hCap > 0 ? (yCapR + boxCapH) : (hAcc > 0 ? (yAccR + boxAccH) : (yRepR + boxRepH));
    const yRevBar = Math.max(y0 + leftH, maxRightY) + 12;
    const svgH = yRevBar + 42;

    const ribbon = (x1, y1a, y1b, x2, y2a, y2b, fill, stroke, flowType) => {
      const mx = (x1 + x2) / 2;
      return `<path class="sankey-ribbon" data-flow="${flowType}" d="M${x1},${y1a} C${mx},${y1a} ${mx},${y2a} ${x2},${y2a} L${x2},${y2b} C${mx},${y2b} ${mx},${y1b} ${x1},${y1b} Z" fill="${fill}" stroke="${stroke}" stroke-width="1"/>`;
    };

    let ribbonsSvg = '';
    let curLeftY = y0;
    // Ribbon 1: Reported Line Cost Expense
    ribbonsSvg += ribbon(230, curLeftY, curLeftY + hRep, 444, yRepR, yRepR + boxRepH, 'rgba(39,73,109,0.18)', 'rgba(39,73,109,0.55)', 'line_costs');
    curLeftY += hRep;
    // Ribbon 2: Phase I Accrual Releases
    if (hAcc > 0) {
      ribbonsSvg += ribbon(230, curLeftY, curLeftY + hAcc, 444, yAccR, yAccR + boxAccH, 'rgba(142,44,37,0.24)', 'rgba(142,44,37,0.75)', 'line_costs');
      curLeftY += hAcc;
    }
    // Ribbon 3: Phase II Capitalized Prepaid Capacity
    if (hCap > 0) {
      ribbonsSvg += ribbon(230, curLeftY, curLeftY + hCap, 444, yCapR, yCapR + boxCapH, 'rgba(142,44,37,0.34)', 'rgba(142,44,37,0.85)', 'line_costs');
    }

    sankeyWrap.innerHTML = `
      <div class="sankey-meta-row">
        <span class="sankey-scope"><b>${esc(scopeLabel)}</b> · Click any flow or T-account to open the primary filing proof in the dual viewer</span>
        <span class="sankey-officers">Officers cited: ${esc(officers)}</span>
      </div>
      <svg class="gl-sankey-svg" viewBox="0 0 740 ${svgH}" role="img" aria-label="General Ledger Double-Entry Sankey Flow">
        ${ribbonsSvg}
        <!-- Left Node: True Carrier Line Costs Incurred -->
        <g class="sankey-node" data-flow="line_costs">
          <rect x="14" y="${y0}" width="216" height="${leftH}" rx="3" fill="#f3efe4" stroke="#15140f" stroke-width="1.4"/>
          <text class="bt h" x="24" y="${y0 + 20}">Actual Carrier Line Costs</text>
          <text class="bs" x="24" y="${y0 + 36}">True network access &amp; lease bills</text>
          <text class="bt num true" x="24" y="${y0 + 58}" style="font-size:15px;font-weight:700">$${fmt.m(lcActual)}m</text>
          <text class="bs" x="24" y="${y0 + 75}">Reported: $${fmt.m(lcReported)}m (${((lcReported / Math.max(1, lcActual)) * 100).toFixed(1)}%)</text>
          <text class="bs" x="24" y="${y0 + 91}" style="fill:#8e2c25;font-weight:600">Hidden via GL entries: $${fmt.m(totalFraud)}m</text>
        </g>

        <!-- Right Node 1: Reported Line Cost Expense (GL 5100) -->
        <g class="sankey-node" data-flow="line_costs">
          <rect x="444" y="${yRepR}" width="282" height="${boxRepH}" rx="3" fill="rgba(39,73,109,0.09)" stroke="#27496d" stroke-width="1.3"/>
          <text class="bt h" x="454" y="${yRepR + 18}">GL 5100 · Reported Line Costs (10-Q/K)</text>
          <text class="bs" x="454" y="${yRepR + 34}">Filed Income Statement: <tspan style="font-weight:700;fill:#27496d">$${fmt.m(lcReported)}m</tspan></text>
        </g>

        ${hAcc > 0 ? `
        <!-- Right Node 2: Phase I Accrual Releases (GL 2140) -->
        <g class="sankey-node" data-flow="line_costs">
          <rect x="444" y="${yAccR}" width="282" height="${boxAccH}" rx="3" fill="rgba(142,44,37,0.11)" stroke="#8e2c25" stroke-width="1.3"/>
          <text class="bt h" x="454" y="${yAccR + 17}">GL 2140 · Accrued Liabilities Released</text>
          <text class="bs" x="454" y="${yAccR + 33}">DR Liability / CR Expense: <tspan style="font-weight:700;fill:#8e2c25">$${fmt.m(accRel)}m</tspan></text>
        </g>` : ''}

        ${hCap > 0 ? `
        <!-- Right Node 3: Phase II Capitalized Capacity (GL 1650) -->
        <g class="sankey-node" data-flow="line_costs">
          <rect x="444" y="${yCapR}" width="282" height="${boxCapH}" rx="3" fill="rgba(142,44,37,0.16)" stroke="#8e2c25" stroke-width="1.4"/>
          <text class="bt h" x="454" y="${yCapR + 17}">GL 1650 · "Prepaid Capacity" PP&amp;E CapEx</text>
          <text class="bs" x="454" y="${yCapR + 33}">DR PP&amp;E / CR Expense: <tspan style="font-weight:700;fill:#8e2c25">$${fmt.m(capRed)}m</tspan> ($${fmt.m(capPPE)}m CapEx)</text>
        </g>` : ''}

        <!-- Bottom Strip: Parallel Top-Side Revenue Manipulation (GL 4090) -->
        <g class="sankey-node" data-flow="revenue">
          <rect x="14" y="${yRevBar}" width="712" height="32" rx="3" fill="rgba(122,90,26,0.10)" stroke="#7a5a1a" stroke-width="1.1"/>
          <text class="bt h" x="24" y="${yRevBar + 20}">GL 4090 · Top-Side Revenue:</text>
          <text class="bs" x="716" y="${yRevBar + 20}" text-anchor="end"><tspan style="font-weight:700;fill:#8e2c25">$${fmt.m(revImp)}m improper</tspan> (+$${fmt.m(revQuest)}m questionable) · Pre-Tax: $${fmt.m(ptiRep)}m vs. ${ptiCor < 0 ? `($${fmt.m(Math.abs(ptiCor))}m)` : `$${fmt.m(ptiCor)}m`} actual</text>
        </g>
      </svg>
    `;

    sankeyWrap.querySelectorAll('[data-flow]').forEach(el => {
      el.style.cursor = 'pointer';
      el.addEventListener('click', () => openProofForFilter(k, el.dataset.flow));
    });

    // Render 4 Synchronized Double-Entry T-Accounts
    const citeQ = (k === 'ALL' || k === 'PHASE2') ? '2001Q1' : (k === 'PHASE1' ? '2000Q3' : k);
    const citeS = S[citeQ];
    const adjEntry = citeS && citeS.ids.adjustment ? DATA.byId.get(citeS.ids.adjustment) : null;
    const revEntry = citeS && citeS.ids.revenue_improper ? DATA.byId.get(citeS.ids.revenue_improper) : null;

    tGrid.innerHTML = `
      <div class="t-card">
        <div class="t-card-head">
          <span class="t-acct-code">GL 5100 · INCOME STATEMENT</span>
          <strong>Line Cost Expense</strong>
        </div>
        <div class="t-ledger">
          <div class="t-col dr">
            <div class="t-col-hdr">DEBIT (DR)</div>
            <div class="t-row"><span>Actual carrier bills</span><b class="num">$${fmt.m(lcActual)}m</b></div>
          </div>
          <div class="t-col cr">
            <div class="t-col-hdr">CREDIT (CR · IMPROPER)</div>
            <div class="t-row true"><span>Phase I Accrual Rel.</span><b class="num">($${fmt.m(accRel)}m)</b></div>
            <div class="t-row true"><span>Phase II CapEx Transf.</span><b class="num">($${fmt.m(capRed)}m)</b></div>
          </div>
        </div>
        <div class="t-card-foot">
          <span>Filed 10-Q/10-K Balance: <b class="num reported">$${fmt.m(lcReported)}m</b> (Understated by <b class="num true">$${fmt.m(totalFraud)}m</b>)</span>
          <button type="button" class="chip k-true" data-tflow="line_costs">Open Proof (${fmt.quarter(citeQ)}) ↗</button>
        </div>
      </div>

      <div class="t-card">
        <div class="t-card-head">
          <span class="t-acct-code">GL 2140 · BALANCE SHEET (PHASE I)</span>
          <strong>Accrued Carrier Liabilities &amp; Reserves</strong>
        </div>
        <div class="t-ledger">
          <div class="t-col dr">
            <div class="t-col-hdr">DEBIT (DR · IMPROPER DRAIN)</div>
            <div class="t-row true"><span>Unanalyzed releases</span><b class="num">$${fmt.m(accRel)}m</b></div>
          </div>
          <div class="t-col cr">
            <div class="t-col-hdr">CREDIT (CR)</div>
            <div class="t-row"><span>Est. carrier accruals</span><b class="num">Drained</b></div>
          </div>
        </div>
        <div class="t-card-foot">
          <span>Q2 1999 – Q4 2000 · Includes $407m Tax Reserve release in Q4 2000</span>
          <button type="button" class="chip k-true" data-tflow="phase1">Beresford p. ${adjEntry && citeS.mechanism === 'accrual_release' ? esc(adjEntry.page_label || adjEntry.page) : '64 / 92'} ↗</button>
        </div>
      </div>

      <div class="t-card">
        <div class="t-card-head">
          <span class="t-acct-code">GL 1650 · BALANCE SHEET (PHASE II)</span>
          <strong>Construction in Progress / PP&amp;E ("Prepaid Capacity")</strong>
        </div>
        <div class="t-ledger">
          <div class="t-col dr">
            <div class="t-col-hdr">DEBIT (DR · BOGUS ASSET)</div>
            <div class="t-row true"><span>Capitalized to PP&amp;E</span><b class="num">$${fmt.m(capPPE)}m</b></div>
            ${otherCapAdj > 0 ? `<div class="t-row true"><span>Other line-cost adj.</span><b class="num">$${fmt.m(otherCapAdj)}m</b></div>` : ''}
          </div>
          <div class="t-col cr">
            <div class="t-col-hdr">CREDIT (CR)</div>
            <div class="t-row"><span>Unsupported CapEx</span><b class="num">Overstated</b></div>
          </div>
        </div>
        <div class="t-card-foot">
          <span>Q1 2001 – Q1 2002 · Discovered by Cynthia Cooper's Internal Audit team (May 2002)</span>
          <button type="button" class="chip k-true" data-tflow="phase2">Beresford p. ${adjEntry && citeS.mechanism === 'capitalization' ? esc(adjEntry.page_label || adjEntry.page) : '105–116'} ↗</button>
        </div>
      </div>

      <div class="t-card">
        <div class="t-card-head">
          <span class="t-acct-code">GL 4090 · INCOME STATEMENT ("CLOSE THE GAP")</span>
          <strong>Corporate Unallocated Revenue Account</strong>
        </div>
        <div class="t-ledger">
          <div class="t-col dr">
            <div class="t-col-hdr">DEBIT (DR)</div>
            <div class="t-row"><span>Unbilled A/R &amp; top-side</span><b class="num">$${fmt.m(revImp)}m</b></div>
          </div>
          <div class="t-col cr">
            <div class="t-col-hdr">CREDIT (CR · POST-CLOSE)</div>
            <div class="t-row true"><span>Improper rev. entries</span><b class="num">$${fmt.m(revImp)}m</b></div>
            <div class="t-row"><span>Questionable items</span><b class="num">+$${fmt.m(revQuest)}m</b></div>
          </div>
        </div>
        <div class="t-card-foot">
          <span>MonRev tracked privately by Ebbers &amp; Sullivan; post-close entries bridged guidance gap</span>
          <button type="button" class="chip k-true" data-tflow="revenue">Beresford p. ${revEntry ? esc(revEntry.page_label || revEntry.page) : '131 / 147'} ↗</button>
        </div>
      </div>
    `;

    tGrid.querySelectorAll('[data-tflow]').forEach(btn => {
      btn.addEventListener('click', () => {
        const tf = btn.dataset.tflow;
        if (tf === 'phase1') openProofForFilter(k === 'ALL' || k === 'PHASE2' ? '2000Q3' : k, 'line_costs');
        else if (tf === 'phase2') openProofForFilter(k === 'ALL' || k === 'PHASE1' ? '2001Q1' : k, 'line_costs');
        else openProofForFilter(k, tf);
      });
    });
  }

  render('ALL');
}

function miniBarsStacked(a, b, { x, y, w, h, max }) {
  const n = a.length; const bw = Math.min(30, (w / n) * 0.62); const gap = w / n; let out = `<g class="mini">`;
  a.forEach((e, i) => {
    const cx = x + gap * i + gap / 2; const q = b.find(s => s.period === e.period); const ah = h * (e.value / max); const qh = q ? h * (q.value / max) : 0;
    out += `<g data-id="${e.id}"><rect x="${cx - bw / 2}" y="${y + h - ah}" width="${bw}" height="${ah}"/>`;
    if (q) out += `<rect class="q" x="${cx - bw / 2}" y="${y + h - ah - qh}" width="${bw}" height="${qh}" data-id="${q.id}"/>`;
    out += `<text class="v" x="${cx}" y="${y + h - ah - qh - 3}" text-anchor="middle">${fmt.m(e.value)}</text><text x="${cx}" y="${y + h + 11}" text-anchor="middle">${fmt.quarter(e.period).replace(' 20', ' ').replace(' 19', ' ')}</text>`;
    out += `<rect class="hit" x="${cx - gap / 2}" y="${y - 12}" width="${gap}" height="${h + 26}" data-id="${e.id}"><title>${fmt.quarter(e.period)}: improper $${fmt.m(e.value)}m${q ? `, questionable $${fmt.m(q.value)}m` : ''} — open the page</title></rect></g>`;
  });
  return out + `</g>`;
}
