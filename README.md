# Paper Trail — WorldCom Primary-Source Forensic Accounting Workbench (`v1.0.0`)

**Live Public Web Application:** [https://www.perplexity.ai/computer/a/paper-trail-_yNHWK0cRkWuo.PU46ZkrQ](https://www.perplexity.ai/computer/a/paper-trail-_yNHWK0cRkWuo.PU46ZkrQ)

A primary-source forensic reconstruction of the WorldCom, Inc. accounting fraud (`1999–2002`) built directly from `57` original SEC EDGAR filings (`10-Q`, `10-K`, `8-K`), the Board of Directors' Special Investigative Committee Report (Beresford, Katzenbach & Rogers, June 2003), the SEC's First Amended Complaint, S.D.N.Y. court orders, DOJ criminal indictments, and the Bankruptcy Examiner's reports (`3,119` pages, `9,137,625` characters).

---

## Key Forensic Capabilities

1. **Synchronized Dual-Pane Evidence Architecture (`Two tracks` + `Source pages` Dual Viewer)**:
   - Selecting any quarter (`Q1 1999` through `Q1 2002`) or switching any metric (`Line costs`, `Pre-tax income`, `Revenues`, `Capital expenditures`, `Line costs as a share of revenues`) simultaneously highlights the reported vs. corrected divergence on the left and opens both:
     - **(a)** the original as-filed SEC `10-Q` / `10-K` statement of operations or cash flows page with yellow line-item highlighting and a clickable `SHA-256 ✓` verification badge, and
     - **(b)** the exact page of the Special Investigative Committee Report, SEC Enforcement Complaint, or 2002 Form 10-K Restatement that proves the improper general-ledger entry.
   - Displays the verified quarterly restatement equation (`Reported + Phase I Accrual Releases + Phase II Capitalized Capacity = Restated Actual`) directly in the quarter card.

2. **Interactive General-Ledger Double-Entry Sankey & T-Account Trace (`Mechanism`)**:
   - Filterable across `All 13 Quarters ($7,180m)`, `Phase I · Accrual Releases (Q2 1999 – Q4 2000 · $3,297m)`, `Phase II · Capitalized "Prepaid Capacity" (Q1 2001 – Q1 2002 · $3,883m / $3,506m PP&E CapEx)`, or any individual quarter (`Q2 1999` – `Q1 2002`).
   - Interactive SVG Sankey flow diagram and 4 synchronized Double-Entry T-Accounts (`GL 5100 Line Cost Expense`, `GL 2140 Accrued Carrier Liabilities & Reserves`, `GL 1650 Construction in Progress / PP&E`, `GL 4090 Corporate Unallocated Revenue`) with officer attribution (`Ebbers, Sullivan, Myers, Yates, Vinson, Normand`) and one-click filing proof links.

3. **Searchable 453-Row Page-Anchored Ledger & Institutional Audit Workbook (`Ledger` & `Method`)**:
   - `453` ledger values: `379` page-cited primary values (every single anchor verified in the extracted page text) + `74` arithmetic/reconstructed values with explicit component formulas.
   - `47` primary-source-anchored chronological events (`1999–2006`) across 10 legal and operational categories.
   - One-click export of the 6-tab institutional Excel workbook (`data/WorldCom_Forensic_Audit_Workbook.xlsx`), 453-row CSV (`data/WorldCom_Forensic_Audit_Ledger.csv`), and programmatic verification report (`data/forensic_verification_report.json`).

---

## Programmatic Verification Summary (`tools/verify_forensic_audit.py`)

| Check | Result | Detail |
| :--- | :--- | :--- |
| **Primary Filings Verified** | `57 / 57` | All 57 raw filings match `data/SHA256SUMS.txt` and `data/register.json` |
| **Corpus Paginated** | `3,119 pages` | `9,137,625` characters extracted at native EDGAR `<PAGE>` / HTML / PDF boundaries |
| **Ledger Values Reconciled** | `453 / 453` | `379` page-cited anchors located + `74` derived/reconstructed formulas verified |
| **Visual PDF/HTML Spot-Checks** | `44 / 44` | All 44 sampled values visually confirmed against rendered page crops |
| **Timeline Events Verified** | `47 / 47` | All 47 chronological events verified against primary filing pages |
| **Quarterly Restatement Equations** | `13 / 13` | `Q1 1999` – `Q1 2002` line costs, pre-tax income, revenues, capex, and E/R ratios balanced |
| **Phase I Accrual Releases (`Q2 99–Q4 00`)** | `$3,297.0M` | `$40M + $131M + $329M + $493M + $679M + $828M + $797M` |
| **Phase II Capitalized Reductions (`Q1 01–Q1 02`)** | `$3,883.0M` | `$771M + $610M + $743M + $941M + $818M` (`$3,506.0M` capitalized directly to PP&E) |
| **Cumulative Quarterly Line-Cost Fraud** | `$7,180.0M` | Phase I (`$3,297.0M`) + Phase II (`$3,883.0M`) |
| **Improper "Close the Gap" Revenue** | `$958.0M` | Plus `$1,107.0M` questionable items (`$2,065.0M` combined) |

---

## Reproduction Pipeline

```bash
python3 tools/fetch_documents.py            # Fetch all 57 primary filings & verify SHA-256 checksums
python3 tools/paginate.py                   # Split into 3,119 pages (data/pages/*.json, data/pagecounts.json)
python3 tools/extract_reported.py           # Extract as-filed 10-Q/10-K figures (data/reported_raw.json)
python3 tools/build_ledger.py               # Build 453-row ledger & quarterly series (data/ledger.json, data/series.json)
python3 tools/build_timeline_and_pages.py   # Build 47-event timeline & render 149 cited PDF page images
python3 tools/verify_forensic_audit.py      # Validate all 57 SHA-256 digests, 453 rows & 13Q equations; generate .xlsx / .csv / .json
```
