import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const OUT_DIR = '/home/user/workspace/paper-trail/build/ui_states';
fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

const W = 1920, H = 1080, DSF = 1.5;
const APP_URL = 'http://127.0.0.1:3000/index.html';

async function getCenter(page, selector, index = 0) {
  return await page.evaluate(({ selector, index }) => {
    const els = Array.from(document.querySelectorAll(selector));
    const el = els[index];
    if (!el) return { x: 480, y: 340 };
    const r = el.getBoundingClientRect();
    return {
      x: Math.round(r.left + r.width / 2),
      y: Math.round(r.top + r.height / 2),
      w: Math.round(r.width),
      h: Math.round(r.height)
    };
  }, { selector, index });
}

async function waitViewerLoaded(page) {
  await page.waitForFunction(() => {
    const text = document.querySelector('#viewer')?.innerText || '';
    return !/Loading /i.test(text);
  }, { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(250);
}

async function hideTooltipAndPark(page) {
  await page.mouse.move(480, 95);
  await page.evaluate(() => {
    const tip = document.getElementById('tooltip');
    if (tip) tip.hidden = true;
  });
  await page.waitForTimeout(100);
}

async function snap(page, name) {
  const p = path.join(OUT_DIR, `${name}.png`);
  await page.screenshot({ path: p, fullPage: false });
  console.log(`Captured ${name}.png`);
  return p;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: W, height: H },
    deviceScaleFactor: DSF
  });
  const page = await context.newPage();
  await page.goto(APP_URL, { waitUntil: 'networkidle' });
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);

  const coords = {};

  // Nav buttons
  coords.nav_chart = await getCenter(page, '#nav button[data-section="chart"]');
  coords.nav_mechanism = await getCenter(page, '#nav button[data-section="mechanism"]');
  coords.nav_timeline = await getCenter(page, '#nav button[data-section="timeline"]');
  coords.nav_ledger = await getCenter(page, '#nav button[data-section="ledger"]');
  coords.nav_documents = await getCenter(page, '#nav button[data-section="documents"]');
  coords.nav_method = await getCenter(page, '#nav button[data-section="method"]');
  coords.wb_btn_primary = await getCenter(page, '#section-chart .wb-btn.primary');

  // 1 & 2. Default Two-Tracks Workbench view (Q1 2001 selected, both pages open)
  await snap(page, 'state_01_masthead_top');
  await snap(page, 'state_02_workspace_default');

  // Find exact coordinates of Q3 2000 (idx 6) and Q1 2001 (idx 8) on .chart-wrap svg
  const qCoords = await page.evaluate(() => {
    const svg = document.querySelector('#section-chart .chart-wrap svg');
    const hits = Array.from(svg.querySelectorAll('rect.hit'));
    // hits are 13 columns in order Q1 1999 (0) .. Q1 2002 (12)
    const centerHit = (idx) => {
      const el = hits[idx];
      if (!el) return { x: 500, y: 460 };
      const r = el.getBoundingClientRect();
      return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height * 0.35) };
    };
    return {
      q3_2000: centerHit(6),
      q1_2001: centerHit(8),
      q2_2001: centerHit(9)
    };
  });
  coords.q3_2000 = qCoords.q3_2000;
  coords.q1_2001 = qCoords.q1_2001;
  coords.q2_2001 = qCoords.q2_2001;

  // 3. Hover Q3 2000 on chart
  await page.mouse.move(coords.q3_2000.x, coords.q3_2000.y);
  await page.waitForTimeout(250);
  await snap(page, 'state_03_q3_2000_hover');

  // 4. Click Q3 2000 on chart & wait until both Q3 2000 pages finish loading
  await page.mouse.click(coords.q3_2000.x, coords.q3_2000.y);
  await page.evaluate(() => {
    window.PT.chart.select('2000Q3', false);
    window.PT.chart.openPair('2000Q3');
  });
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_04_q3_2000_selected');

  // 5. Click SHA-256 badge on left source page
  coords.sha_badge_left = await getCenter(page, '#viewer .sha-badge', 0);
  await page.mouse.click(coords.sha_badge_left.x, coords.sha_badge_left.y);
  await page.waitForTimeout(300);
  await snap(page, 'state_05_q3_2000_sha256_open');

  // 6. Hover Q1 2001 on chart
  await page.mouse.move(coords.q1_2001.x, coords.q1_2001.y);
  await page.waitForTimeout(250);
  await snap(page, 'state_06_q1_2001_hover');

  // 7. Click Q1 2001 on chart & wait until both Q1 2001 pages finish loading
  await page.mouse.click(coords.q1_2001.x, coords.q1_2001.y);
  await page.evaluate(() => {
    window.PT.chart.select('2001Q1', false);
    window.PT.chart.openPair('2001Q1');
  });
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_07_q1_2001_selected');

  // 8a. Click Pre-tax income metric tab
  coords.metric_pretax = await getCenter(page, '#section-chart .metric-tabs button[data-metric="pretax"]');
  await page.mouse.click(coords.metric_pretax.x, coords.metric_pretax.y);
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_08a_metric_pretax');

  // 8b. Click Capital expenditures metric tab
  coords.metric_capex = await getCenter(page, '#section-chart .metric-tabs button[data-metric="capex"]');
  await page.mouse.click(coords.metric_capex.x, coords.metric_capex.y);
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_08b_metric_capex');

  // 9. Click Line costs as a share of revenues metric tab
  coords.metric_ratio = await getCenter(page, '#section-chart .metric-tabs button[data-metric="er"]');
  await page.mouse.click(coords.metric_ratio.x, coords.metric_ratio.y);
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_09_metric_ratio');

  // Switch back to Line costs so the right viewer shows Q1 2001 10-Q p. 4 + Beresford p. 105
  coords.metric_line_costs = await getCenter(page, '#section-chart .metric-tabs button[data-metric="line_costs"]');
  await page.mouse.click(coords.metric_line_costs.x, coords.metric_line_costs.y);
  await waitViewerLoaded(page);

  // 10. Switch to Mechanism tab ("Mechanism" nav button)
  await page.mouse.click(coords.nav_mechanism.x, coords.nav_mechanism.y);
  await page.waitForTimeout(450);
  const mechBtns = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('#section-mechanism .gl-filter-bar button'));
    const getPos = (b) => {
      if (!b) return { x: 300, y: 240 };
      const r = b.getBoundingClientRect();
      return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), text: b.textContent.trim() };
    };
    return {
      all: getPos(btns[0]),
      phase1: getPos(btns[1]),
      phase2: getPos(btns[2]),
      q3_2001: getPos(btns.find(b => /Q3 .01|2001Q3|Q3 2001/i.test(b.textContent)) || btns[11])
    };
  });
  coords.mech_all_btn = mechBtns.all;
  coords.mech_phase1_btn = mechBtns.phase1;
  coords.mech_phase2_btn = mechBtns.phase2;
  coords.mech_q3_2001_btn = mechBtns.q3_2001;
  await snap(page, 'state_10_mechanism_all');

  // 11a. Click Phase I in Mechanism
  await page.mouse.click(coords.mech_phase1_btn.x, coords.mech_phase1_btn.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_11a_mechanism_phase1');

  // 11b. Click Phase II in Mechanism
  await page.mouse.click(coords.mech_phase2_btn.x, coords.mech_phase2_btn.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_11b_mechanism_phase2');

  // 11c. Click Q3 2001 in Mechanism
  await page.mouse.click(coords.mech_q3_2001_btn.x, coords.mech_q3_2001_btn.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_11c_mechanism_q3_2001');

  // 12a. Scroll #work-scroll down to show all 4 T-Accounts + Schematic 1 clearly
  await page.mouse.click(coords.mech_all_btn.x, coords.mech_all_btn.y);
  await waitViewerLoaded(page);
  await page.evaluate(() => {
    const tgrid = document.querySelector('#section-mechanism .t-accounts-grid');
    const sc = document.querySelector('#work-scroll');
    if (tgrid && sc) {
      sc.scrollTop = Math.max(0, tgrid.offsetTop - 55);
    }
  });
  await page.waitForTimeout(300);
  coords.tacc_proof_btn = await getCenter(page, '#section-mechanism .t-accounts-grid .t-cite, #section-mechanism .t-accounts-grid button', 1);
  await snap(page, 'state_12a_mechanism_taccounts');

  // 12b. Click Beresford proof link in T-Account (updates right viewer to Beresford p. 64 / 92!)
  await page.mouse.click(coords.tacc_proof_btn.x, coords.tacc_proof_btn.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_12b_taccount_jump_workspace');

  // 13a. Click Timeline nav tab
  await page.mouse.click(coords.nav_timeline.x, coords.nav_timeline.y);
  await waitViewerLoaded(page);
  coords.chron_audit_chip = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('#section-timeline button'));
    const b = btns.find(el => /discovery/i.test(el.textContent)) || btns[2] || btns[1];
    if (!b) return { x: 260, y: 190 };
    const r = b.getBoundingClientRect();
    return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), text: b.textContent.trim() };
  });
  await snap(page, 'state_13a_chronology_all');

  // 13b. Click Discovery filter chip in Timeline & open first discovery event's filing page
  await page.mouse.click(coords.chron_audit_chip.x, coords.chron_audit_chip.y);
  await page.waitForTimeout(300);
  const firstEventCite = await getCenter(page, '#section-timeline .ev button, #section-timeline .ev .chip', 0);
  await page.mouse.click(firstEventCite.x, firstEventCite.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_13b_chronology_audit');

  // 14a. Click Ledger nav tab
  await page.mouse.click(coords.nav_ledger.x, coords.nav_ledger.y);
  await waitViewerLoaded(page);
  coords.ledger_search = await getCenter(page, '#section-ledger input[type="search"]');
  coords.ledger_xlsx_btn = await getCenter(page, '#section-ledger .wb-btn.primary');
  await snap(page, 'state_14a_ledger_all');

  // 14b. Search Ledger for "2001Q1 line" and click first row to open its source pages
  await page.mouse.click(coords.ledger_search.x, coords.ledger_search.y);
  await page.fill('#section-ledger input[type="search"]', '2001Q1 line');
  await page.waitForTimeout(350);
  coords.ledger_first_row = await getCenter(page, '#section-ledger tbody tr.row', 0);
  await page.mouse.click(coords.ledger_first_row.x, coords.ledger_first_row.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_14b_ledger_capex_filter');

  // 15a. Click Documents nav tab
  await page.mouse.click(coords.nav_documents.x, coords.nav_documents.y);
  await waitViewerLoaded(page);
  await snap(page, 'state_15a_documents_register');

  // 15b. Click Method & limits nav tab
  await page.mouse.click(coords.nav_method.x, coords.nav_method.y);
  await waitViewerLoaded(page);
  coords.method_xlsx_btn = await getCenter(page, '#section-method .wb-btn.primary');
  await snap(page, 'state_15b_method_verification');

  // 16. Click Two tracks nav tab for final closing wide view (Q1 2001 selected with both primary pages open)
  await page.mouse.click(coords.nav_chart.x, coords.nav_chart.y);
  await page.evaluate(() => {
    window.PT.chart.select('2001Q1', false);
    window.PT.chart.openPair('2001Q1');
  });
  await waitViewerLoaded(page);
  await hideTooltipAndPark(page);
  await snap(page, 'state_16_closing_wide');

  fs.writeFileSync(path.join(OUT_DIR, 'manifest.json'), JSON.stringify(coords, null, 2));
  await browser.close();
})();
