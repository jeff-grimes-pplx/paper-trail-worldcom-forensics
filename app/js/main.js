// Paper Trail — entry point.
import { loadCore, DATA } from './data.js';
import { Viewer } from './viewer.js';
import { TwoTrack } from './chart.js';
import { renderMechanism } from './mechanism.js';
import { renderTimeline } from './timeline.js';
import { renderLedger } from './ledger.js';
import { renderDocuments, renderMethod } from './documents.js';

const $ = s => document.querySelector(s);

function showSection(name, push = true) {
  document.querySelectorAll('.section').forEach(s => s.classList.toggle('active', s.id === `section-${name}`));
  document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('active', b.dataset.section === name));
  $('#work-scroll').scrollTop = 0;
  if (push) history.replaceState(null, '', `#${name}`);
  window.dispatchEvent(new Event('resize'));
}

async function boot() {
  try { await loadCore(); } catch (err) { $('#section-chart').innerHTML = `<p class="lede">The dataset failed to load (${err.message}).</p>`; return; }
  const viewer = new Viewer($('#viewer'));
  window.PT = { DATA, viewer };
  const chart = new TwoTrack($('#section-chart'), viewer);
  const lazy = { mechanism: () => renderMechanism($('#section-mechanism'), viewer), timeline: () => renderTimeline($('#section-timeline'), viewer), ledger: () => renderLedger($('#section-ledger'), viewer), documents: () => renderDocuments($('#section-documents'), viewer), method: () => renderMethod($('#section-method'), viewer) };
  const done = {};
  const ensure = name => { if (lazy[name] && !done[name]) { done[name] = lazy[name]() || true; } return done[name]; };
  window.PT.chart = chart; window.PT.ensure = ensure; window.PT.showSection = n => { ensure(n); showSection(n); };
  // Film-capture hooks (deterministic frame stepping drives these; the app itself never calls them).
  window.PT.film = {
    reset() { chart.selected = null; chart.revealF = 0; chart.draw(); chart.renderCard(); viewer.setTwo(true); viewer.panes.forEach(p => p.empty('Select a quarter on the chart to open the filed page and the page that corrects it.')); },
    reveal(f) { chart.revealF = f; chart.draw(); },
    done() { chart.revealF = null; chart.draw(); },
  };

  document.querySelectorAll('#nav button').forEach(b => b.addEventListener('click', () => { ensure(b.dataset.section); showSection(b.dataset.section); }));
  const pc = DATA.pagecounts; const pages = Object.values(pc).reduce((a, b) => a + b.pages, 0);
  $('#mast-meta').innerHTML = `${DATA.register.length} documents · ${pages.toLocaleString()} pages<br>${DATA.ledger.meta.entries} values · ${DATA.ledger.meta.cited} page-cited · ${DATA.timeline.length} events`;

  // Default view: Q1 2001 line costs with both pages open — the quarter the capitalization began.
  chart.select('2001Q1', false);
  const isMobile = window.matchMedia('(max-width: 900px)').matches;
  if (!isMobile) chart.openPair('2001Q1');
  const hash = location.hash.replace('#', '');
  if (hash && lazy[hash]) { ensure(hash); showSection(hash, false); }
  // Pre-render the other sections after first paint so navigation is instant.
  const idle = window.requestIdleCallback || (fn => setTimeout(fn, 300));
  idle(() => { ['mechanism', 'timeline', 'ledger', 'documents', 'method'].forEach(ensure); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') $('#viewer').classList.remove('open'); });
  // Scroll affordances (mobile): fade the nav's right edge until it is scrolled to the end; label diagrams/tables that scroll sideways.
  const nav = $('#nav'); const navEnd = () => nav.classList.toggle('at-end', nav.scrollLeft + nav.clientWidth >= nav.scrollWidth - 2);
  nav.addEventListener('scroll', navEnd, { passive: true }); navEnd();
  const markScrollers = () => document.querySelectorAll('.mech, .annual').forEach(el => { if (el.clientWidth) el.classList.toggle('scroll-x', el.scrollWidth > el.clientWidth + 2); });
  new ResizeObserver(() => { navEnd(); markScrollers(); }).observe(document.body);
  window.addEventListener('resize', markScrollers); // showSection dispatches resize after switching sections
  idle(markScrollers);
}
boot();
