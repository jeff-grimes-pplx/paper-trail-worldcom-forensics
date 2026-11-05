# Paper Trail — verification table (44 sampled values, 44 match)

Seeded random sample (seed "A6-paper-trail", stratified: at least one value per cited document) of ledger values with a document citation. Each value was re-opened in the app viewer with Playwright (1440x900, DPR 2), the located figure was cropped (qa/verify/NN.png), and the crops were read by eye against the expected value on contact sheets (qa/verify/sheet-N.png). "located" records how the figure was found on the page: strong = exact figure highlighted inside the anchor text.

Sample size 44, matches 44, built 2026-10-14T23:37:25+00:00. Each row records the ledger id, the value as shown, the document and page as opened in the app, how the figure was located, and the crop that was read.

| # | Ledger id | Value | Document | Page (as opened) | Located | Anchor (as cited) | Result | Crop |
|---|---|---|---|---|---|---|---|---|
| 1 | `rep:1999Q1:operating_income` | 1,495 | Form 10-Q · Q1 1999 | 4 | strong | Operating income (loss) 1,495 (72) | match | qa/verify/01.png |
| 2 | `rep:1999H1:line_costs` | 8,053 | Form 10-Q · Q2 1999 | 4 | strong | Line costs 3,937 1,230 8,053 2,347 | match | qa/verify/02.png |
| 3 | `rep:1999M9:net_income` | 2,711 | Form 10-Q · Q3 1999 | 4 (4) | strong | Net income (loss) 1,107 (2,944) 2,711 (3,125) | match | qa/verify/03.png |
| 4 | `rep:1999FY:sga` | 8,935 | Form 10-K · FY 1999 | 69 (F-5) | strong | Selling, general and administrative 8,935 4,563 1,854 | match | qa/verify/04.png |
| 5 | `rep:2000Q1:da` | 1,147 | Form 10-Q · Q1 2000 | 4 (4) | strong | Depreciation and amortization 1,147 1,101 | match | qa/verify/05.png |
| 6 | `rep:2000H1:capex` | 5,197 | Form 10-Q · Q2 2000 | 5 (5) | strong | Capital expenditures (5,197) (3,702) | match | qa/verify/06.png |
| 7 | `rep:2000M9:line_costs` | 11,376 | Form 10-Q · Q3 2000 | 4 (4) | strong | Line costs 3,867 3,593 11,376 11,089 | match | qa/verify/07.png |
| 8 | `rep:2000FY:da` | 4,878 | Form 10-K405 · FY 2000 | 91 (F-4) | strong | Depreciation and amortization............................. 2,289 4,354 4,878 | match | qa/verify/08.png |
| 9 | `rep:2001Q1:pretax_income` | 988 | Form 10-Q · Q1 2001 | 4 (4) | strong | Income before income taxes, minority interests and cumulative effect of accounting change … | match | qa/verify/09.png |
| 10 | `rep:2001Q2:da` | 1,407 | Form 10-Q · Q2 2001 | 4 (4) | strong | Depreciation and amortization 1,186 1,407 2,333 2,742 | match | qa/verify/10.png |
| 11 | `rep:2001M9:sga` | 8,503 | Form 10-Q · Q3 2001 | 4 (4) | strong | Selling, general and administrative 3,081 2,517 7,847 8,503 | match | qa/verify/11.png |
| 12 | `rep:2001FY:sga` | 11,046 | Form 10-K405 · FY 2001 | 78 (F-4) | strong | Selling, general and administrative 8,935 10,597 11,046 | match | qa/verify/12.png |
| 13 | `rep:2002Q1:capex` | 1,280 | Form 10-Q · Q1 2002 | 5 (5) | strong | Capital expenditures (2,235) (1,280) | match | qa/verify/13.png |
| 14 | `adjustment:2001Q2:line_costs_capitalized` | 560 | Special Investigative Committee report (2003) | 113 (108) | strong | WorldCom capitalized $560 million of operating line costs in the second quarter of 2001 an… | match | qa/verify/14.png |
| 15 | `sec_alleged:2002Q1:sec_actual_line_costs` | 4,297 | SEC First Amended Complaint · Nov 5, 2002 | 1 (¶ 25 table) | strong | 10-Q, 1st Q. 2002 $3.479 billion $240 million $4.297 billion $578 million loss | match | qa/verify/15.png |
| 16 | `company_disclosure:2002Q1:company_announced_capitalized_line_costs` | 797 | Form 8-K · June 25, 2002 ($3.8bn) | 5 (5) | strong | was $3.055 billion for 2001 and $797 million for first quarter 2002 | match | qa/verify/16.png |
| 17 | `company_disclosure:2000FY:company_announced_ebitda_reduction` | 2,864 | Form 8-K · Aug 8, 2002 (+$3.3bn) | 6 (2) | strong | Total reduction in EBITDA             $  217       $ 2,864       $ 3,216       $  885     … | match | qa/verify/17.png |
| 18 | `restated:2001FY:restated_cash_from_operations` | 2,845 | Form 10-K · FY 2002 (restated 2000–01) | 138 (F-34) | strong | Net cash from operating activities $ 7,994 2,845 $ 7,666 4,227 | match | qa/verify/18.png |
| 19 | `rep:2000Q3:revenue` | 10,047 | Form 10-Q · Q3 2000 | 4 (4) | strong | Revenues $10,047 $8,996 $29,483 $26,586 | match | qa/verify/19.png |
| 20 | `restated:2001FY:restatement_revenue_revenue_related_adjustments` | (1,204) | Form 10-K · FY 2002 (restated 2000–01) | 130 (F-26) | strong | Revenue related adjustments (1,204 ) (575 ) (36 ) (995 ) | match | qa/verify/20.png |
| 21 | `restated:2000FY:restatement_pretax_revenue_related_adjustments` | (995) | Form 10-K · FY 2002 (restated 2000–01) | 130 (F-26) | strong | Revenue related adjustments (1,204 ) (575 ) (36 ) (995 ) | match | qa/verify/21.png |
| 22 | `rep:2001Q3:pretax_income` | 845 | Form 10-Q · Q3 2001 | 4 (4) | strong | Income before income taxes, minority interests and cumulative effect of accounting change … | match | qa/verify/22.png |
| 23 | `adjustment:2000Q1:line_cost_reduction` | 493 | Special Investigative Committee report (2003) | 69 (64) | strong | Total 40 131 329 493 679 828 797 3,297 | match | qa/verify/23.png |
| 24 | `committee_summary:1999FY:committee_improper_sga` | 46 | Special Investigative Committee report (2003) | 22 (17) | strong | SG&A 6 46 283 181 25 535 | match | qa/verify/24.png |
| 25 | `adjustment:2001Q3:line_cost_reduction` | 743 | Special Investigative Committee report (2003) | 115 (110) | strong | WorldCom capitalized an additional $743 million of operating line costs for the third quar… | match | qa/verify/25.png |
| 26 | `adjustment:2000Q1:accrual_release_uk` | 34 | Special Investigative Committee report (2003) | 69 (64) | strong | UK — — — 34 — — — 34 | match | qa/verify/26.png |
| 27 | `restated:2001FY:restatement_revenue_previously_reported` | 35,121 | Form 10-K · FY 2002 (restated 2000–01) | 130 (F-26) | strong | Previously reported (1) $ 35,121 $ 2,375 $ 39,020 $ 7,581 | match | qa/verify/27.png |
| 28 | `adjustment:1999Q3:accrual_release_international` | 31 | Special Investigative Committee report (2003) | 69 (64) | strong | International — 31 239 370 374 — 170 1,184 | match | qa/verify/28.png |
| 29 | `sec_alleged:2001Q3:sec_actual_pretax_income` | 102 | SEC First Amended Complaint · Nov 5, 2002 | 1 (¶ 25 table) | strong | 10-Q, 3rd Q. 2001 $3.745 billion $845 million $4.488 billion $102 million | match | qa/verify/29.png |
| 30 | `adjustment:1999Q2:accrual_release_domestic` | 40 | Special Investigative Committee report (2003) | 69 (64) | strong | Domestic 40 100 90 89 305 828 477 1,929 | match | qa/verify/30.png |
| 31 | `rep:1999M9:sga` | 6,530 | Form 10-Q · Q3 1999 | 4 (4) | strong | Selling, general and administrative 2,040 902 6,530 1,904 | match | qa/verify/31.png |
| 32 | `adjustment:2000Q1:accrual_release_domestic` | 89 | Special Investigative Committee report (2003) | 69 (64) | strong | Domestic 40 100 90 89 305 828 477 1,929 | match | qa/verify/32.png |
| 33 | `restated:2001FY:restatement_pretax_unclassified_income_expense` | 383 | Form 10-K · FY 2002 (restated 2000–01) | 130 (F-26) | strong | Unclassified income/(expense) — 383 — (426 ) | match | qa/verify/33.png |
| 34 | `restated:2001FY:restatement_effect_on_net_income` | (17,078) | Form 10-K · FY 2002 (restated 2000–01) | 138 (F-34) | strong | Effect of restatement adjustments on net income for the current period (17,078 ) (53,074 ) | match | qa/verify/34.png |
| 35 | `restated:2000FY:restated_net_loss` | (48,909) | Form 10-K · FY 2002 (restated 2000–01) | 109 (F-5) | strong | Net loss (9,173 ) (15,597 ) (48,909 ) | match | qa/verify/35.png |
| 36 | `rep:2001Q3:line_costs` | 3,745 | Form 10-Q · Q3 2001 | 4 (4) | strong | Line costs 3,867 3,745 11,376 11,171 | match | qa/verify/36.png |
| 37 | `rep:1999H1:operating_income` | 3,259 | Form 10-Q · Q2 1999 | 4 | strong | Operating income 1,764 495 3,259 423 | match | qa/verify/37.png |
| 38 | `sec_alleged:2000Q3:sec_alleged_line_cost_reduction` | 828 | SEC First Amended Complaint · Nov 5, 2002 | 1 (¶ 19) | strong | reducing the third quarter 2000 line costs by approximately $828 million | match | qa/verify/38.png |
| 39 | `sec_alleged:2001FY:sec_reported_line_costs` | 14,739 | SEC First Amended Complaint · Nov 5, 2002 | 1 (¶ 25 table) | strong | 10-K, 2001 $14.739 billion $2.393 billion $17.754 billion $622 million loss | match | qa/verify/39.png |
| 40 | `sec_alleged:2001Q1:sec_actual_line_costs` | 4,879 | SEC First Amended Complaint · Nov 5, 2002 | 1 (¶ 25 table) | strong | 10-Q, 1st Q. 2001 $4.108 billion $988 million $4.879 billion $217 million | match | qa/verify/40.png |
| 41 | `adjustment:2001Q2:revenue_improper` | 132 | Special Investigative Committee report (2003) | 136 (131) | strong | 85 5 65 50 19 121 161 27 17 132 117 92 67 958 | match | qa/verify/41.png |
| 42 | `rep:2001Q2:line_costs` | 3,730 | Form 10-Q · Q2 2001 | 4 (4) | strong | Line costs 3,776 3,730 7,509 7,426 | match | qa/verify/42.png |
| 43 | `rep:1999Q1:da` | 1,079 | Form 10-Q · Q1 1999 | 4 | strong | Depreciation and amortization 1,079 299 | match | qa/verify/43.png |
| 44 | `rep:1999FY:da` | 4,354 | Form 10-K · FY 1999 | 69 (F-5) | strong | Depreciation and amortization 4,354 2,289 1,066 | match | qa/verify/44.png |
