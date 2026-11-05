# Main flows

## 1. Two tracks chart & synchronized dual-pane viewer
- Start: index.html (`#chart`)
- Steps:
  1. Initial load selects `Q1 2001` on `Line costs` and opens `Form 10-Q · Q1 2001` (p. 4, `$4,108` highlighted) in top pane and `Special Investigative Committee report (2003)` (p. 110 / printed p. 105, `$771 million` highlighted) in bottom pane.
  2. Click another quarter on the chart (e.g. `Q3 2000` or `Q2 2001`).
  3. Click each metric tab (`Line costs`, `Pre-tax income`, `Revenues`, `Capital expenditures`, `Line costs as a share of revenues`).
  4. Click any figure in the Annual reconciliation table or 2002 Form 10-K Restatement bar chart.
- Expect:
  - Chart highlights the selected quarter (`gap 828` for Q3 2000 Line costs; `gap 610` for Q2 2001 Line costs).
  - Quarter card shows Reported, Improper reduction/entry, Corrected reconstruction, and the explicit restatement equation (`Reported + Accrual Releases + Capitalized Prepaid Capacity = Restated Actual`), plus clickable citation chips.
  - Clicking any quarter OR any metric tab updates BOTH panes of the right-hand source viewer with yellow line-item highlighting and verified SHA-256 digest badge.

## 2. Mechanism & Interactive General-Ledger Double-Entry Sankey / T-Account Trace
- Start: `#mechanism` (click `Mechanism` in header nav)
- Steps:
  1. Inspect the Interactive General-Ledger Double-Entry Flow & T-Account Workbench (`#mech-gl-workbench`).
  2. Click phase/quarter filter buttons (`All Fraud Quarters`, `Phase I: Accrual Releases`, `Phase II: Capitalized Capacity`, `Q3 2000`, `Q1 2001`, `Q4 2001`).
  3. Click a Sankey flow node/ribbon or a T-Account citation chip, and click a bar in the 4 mechanism schematics (`1 · Release the reserves`, `2 · Move the expense onto the balance sheet`, `3 · "Close the Gap" on revenue`, `4 · Why it stayed hidden`).
- Expect:
  - Sankey diagram and 4 Double-Entry T-Accounts (`GL 5100 Line Cost Expense`, `GL 2140 Accrued Liabilities`, `GL 1650 Construction in Progress / PP&E`, `GL 4090 Corporate Unallocated Revenue`) update dynamically to show exact Debit/Credit entries, officer chain of command (`Ebbers / Sullivan / Myers / Yates / Vinson / Normand`), and restatement equation.
  - Clicking any citation chip or mini-bar opens the exact primary document page in the viewer with yellow highlighting.

## 3. Timeline of 47 primary-source events
- Start: `#timeline` (click `Timeline` in header nav)
- Steps:
  1. Click category filter pills (`All 47`, `Mechanism`, `Discovery`, `SEC`, `Court`, `Criminal`, `Restatement`).
  2. Click an event card (e.g. Judge Rakoff's July 7, 2003 opinion `sdny-opinion-2003-07-07` or June 25, 2002 Form 8-K).
- Expect:
  - Timeline filters cleanly; clicking an event opens the corresponding EDGAR filing, HTML release, or rendered PDF page with highlight box in the right-hand viewer.

## 4. Searchable 453-row Ledger & One-Click Workbook Exports
- Start: `#ledger` (click `Ledger` in header nav)
- Steps:
  1. Type a query in the search input (e.g. `2001Q1`, `prepaid capacity`, `F-26`), filter by Track and Period, and click column headers to sort.
  2. Click any row in the table.
  3. Click the one-click export controls (`Export .xlsx`, `Export .csv`, `Export .json`).
- Expect:
  - Table filters and sorts all 453 rows cleanly; `✓ visual` badge stays on a single line without wrapping; clicking a row opens its cited page (or component pages for derived/reconstructed rows) in the viewer.
  - Export buttons trigger valid downloads of `WorldCom_Forensic_Audit_Workbook.xlsx`, `WorldCom_Forensic_Audit_Ledger.csv`, and `WorldCom_Forensic_Audit_Ledger.json`.

## 5. Document Register (57 filings) & Method / Verification
- Start: `#documents` and `#method`
- Steps:
  1. Click `Documents` in header nav and click any of the 57 primary filings.
  2. Click `Method & limits` in header nav and click any row in the visual verification table.
- Expect:
  - All 57 documents display their page count, authority, filing date, SHA-256 checksum, and direct link; clicking opens page 1 in the viewer.
  - Method section shows all summary stats, legal record, Python verification suite summary, and clickable verification table.
