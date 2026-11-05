"""Curated values with provenance: the improper entries identified by the Special Investigative Committee
(Beresford report), the SEC's First Amended Complaint figures, the company's own announcements and the
company's restatement in the 2002 Form 10-K (filed March 2004).

Every record: period, metric, value (USD millions unless noted), source doc id, page n in our frozen copy,
printed page label, and an exact anchor string that must appear on that page (checked by build_ledger.py).
"""

B = 'beresford-report'
SEC = 'sec-amended-complaint-2002-11-05'
K02 = '10k-2002'

def rec(period, metric, value, doc, page, label, anchor, basis, note='', track='adjustment', **kw):
    d = dict(period=period, metric=metric, value=value, doc=doc, page=page, label=label, anchor=anchor,
             basis=basis, note=note, track=track)
    d.update(kw)
    return d

CURATED = []

# ---------------------------------------------------------------------------------------------------------
# 1. Improper reductions of line costs by quarter — Special Investigative Committee (Beresford report)
# ---------------------------------------------------------------------------------------------------------
# Accrual releases table, p.64:  "Total 40 131 329 493 679 828 797 3,297"
ACCRUAL = {'1999Q2': 40, '1999Q3': 131, '1999Q4': 329, '2000Q1': 493, '2000Q2': 679, '2000Q3': 828, '2000Q4': 797}
for q, v in ACCRUAL.items():
    CURATED.append(rec(q, 'line_cost_reduction', v, B, 69, '64', 'Total 40 131 329 493 679 828 797 3,297',
                       'Special Investigative Committee finding',
                       'Reductions to line costs from improper accrual releases (domestic, international, UK, other), table "Reductions to Line Costs from Accrual Releases".',
                       mechanism='accrual_release'))
CURATED.append(rec('1999-2000', 'line_cost_reduction_total', 3297, B, 69, '64', 'Total 40 131 329 493 679 828 797 3,297',
                   'Special Investigative Committee finding', 'Two-year total of improper accrual releases.', mechanism='accrual_release'))
# Domestic / international components (same table)
for q, v in {'1999Q2': 40, '1999Q3': 100, '1999Q4': 90, '2000Q1': 89, '2000Q2': 305, '2000Q3': 828, '2000Q4': 477}.items():
    CURATED.append(rec(q, 'accrual_release_domestic', v, B, 69, '64', 'Domestic 40 100 90 89 305 828 477 1,929',
                       'Special Investigative Committee finding', 'Domestic line cost accrual releases.', mechanism='accrual_release'))
for q, v in {'1999Q3': 31, '1999Q4': 239, '2000Q1': 370, '2000Q2': 374, '2000Q4': 170}.items():
    CURATED.append(rec(q, 'accrual_release_international', v, B, 69, '64', 'International — 31 239 370 374 — 170 1,184',
                       'Special Investigative Committee finding', 'International line cost accrual releases.', mechanism='accrual_release'))
CURATED.append(rec('2000Q1', 'accrual_release_uk', 34, B, 69, '64', 'UK — — — 34 — — — 34', 'Special Investigative Committee finding',
                   'Release of a UK accrued network expense liability ($33.6 million, April 2000).', mechanism='accrual_release'))
CURATED.append(rec('2000Q4', 'accrual_release_other', 150, B, 69, '64', 'Other — — — — — — 150 150', 'Special Investigative Committee finding',
                   'Transfer of $150 million from a prepaid expense asset account (wireless), Q4 2000.', mechanism='accrual_release'))
# Q4 2000: $407 million from the deferred federal income tax accrual applied against line costs (p.89)
CURATED.append(rec('2000Q4', 'accrual_release_tax_component', 407, B, 94, '89', 'released $407 million from the Tax group’s deferred federal income tax accrual account and applied it against line costs',
                   'Special Investigative Committee finding', 'Component of the Q4 2000 domestic release: deferred federal income tax accrual applied against line costs.', mechanism='accrual_release'))

# Capitalization era, 2001Q1–2002Q1: total reduction in line costs per quarter and the capitalized component
CAP = [
    ('2001Q1', 771, 544, 110, '105', 'WorldCom capitalized $544 million of line costs in the first quarter and, with other adjustments, reduced line costs by a total of $771 million'),
    ('2001Q2', 610, 560, 113, '108', 'WorldCom capitalized $560 million of operating line costs in the second quarter of 2001 and, with other adjustments, reduced line costs by a total of $610 million'),
    ('2001Q3', 743, 743, 115, '110', 'WorldCom capitalized an additional $743 million of operating line costs for the third quarter'),
    ('2001Q4', 941, 841, 119, '114', 'WorldCom reduced line costs by $941 million in the fourth quarter, capitalizing $841 million of that amount'),
    ('2002Q1', 818, 818, 121, '116', 'Vinson finally booked the entries that reduced line cost expense by $818\nmillion and capitalized the full amount'),
]
for q, total, cap, n, label, anchor in CAP:
    CURATED.append(rec(q, 'line_cost_reduction', total, B, n, label, anchor, 'Special Investigative Committee finding',
                       'Total improper reduction of line costs in the quarter (capitalization plus other adjustments).', mechanism='capitalization'))
    CURATED.append(rec(q, 'line_costs_capitalized', cap, B, n, label, anchor, 'Special Investigative Committee finding',
                       'Portion of the quarter\'s reduction booked to property, plant and equipment ("prepaid capacity").', mechanism='capitalization'))
# Q1 2001 reported vs actual capital expenditures (p.108)
CURATED.append(rec('2001Q1', 'capex_actual_per_committee', 1691, B, 113, '108', 'had $2.235 billion in capital expenditures instead of the $1.691 billion it actually spent',
                   'Special Investigative Committee finding', 'Capital expenditures actually spent in Q1 2001 versus the $2.235 billion reported.', mechanism='capitalization'))
# Line cost E/R ratio statements
CURATED.append(rec('2001Q1', 'line_cost_er_ratio_reported_pct', 42, B, 113, '108', 'resulting in a line cost E/R ratio of 42% rather than 50%',
                   'Special Investigative Committee finding', 'Reported line-cost-to-revenue ratio for Q1 2001 (42%) versus about 50% without the reduction.', mechanism='capitalization'))
CURATED.append(rec('2001Q1', 'line_cost_er_ratio_actual_pct', 50, B, 113, '108', 'resulting in a line cost E/R ratio of 42% rather than 50%',
                   'Special Investigative Committee finding', 'Line-cost-to-revenue ratio for Q1 2001 without the improper reduction.', mechanism='capitalization'))
# Summary statements (p.11): capitalization-era totals and pre-tax effects
CURATED.append(rec('2001Q1-2002Q1', 'line_cost_reduction_total', 3800, B, 16, '11', 'WorldCom improperly reduced its reported line costs by $3.8 billion, principally by capitalizing $3.5 billion of line costs',
                   'Special Investigative Committee finding', 'Approximate total, first quarter 2001 through first quarter 2002.', mechanism='capitalization'))
CURATED.append(rec('2001Q1-2002Q1', 'line_costs_capitalized_total', 3500, B, 16, '11', 'principally by capitalizing $3.5 billion of line costs',
                   'Special Investigative Committee finding', 'Approximate total capitalized.', mechanism='capitalization'))
CURATED.append(rec('2001Q2', 'pretax_income_without_capitalization', -401, B, 16, '11', 'the Company would have reported a $401 million pre-tax loss',
                   'Special Investigative Committee finding', 'Q2 2001 pre-tax result had $560 million not been capitalized (Committee analysis).', mechanism='capitalization'))
CURATED.append(rec('2001Q4', 'pretax_income_reported_per_committee', 401, B, 16, '11', 'WorldCom reported pre-tax income of $401 million instead of a pre-tax loss of $440 million',
                   'Special Investigative Committee finding', 'Q4 2001 pre-tax income as reported in company results (quarter not separately presented in the 10-K).', mechanism='capitalization'))
CURATED.append(rec('2001Q4', 'pretax_income_without_capitalization', -440, B, 16, '11', 'instead of a pre-tax loss of $440 million because it capitalized $841 million',
                   'Special Investigative Committee finding', 'Q4 2001 pre-tax result had $841 million not been capitalized.', mechanism='capitalization'))
CURATED.append(rec('2002Q1', 'pretax_income_without_capitalization', -578, B, 16, '11', 'allowed WorldCom to report pre-tax income of $240 million instead of a $578 million pre-tax loss',
                   'Special Investigative Committee finding', 'Q1 2002 pre-tax result had $818 million not been capitalized.', mechanism='capitalization'))

# ---------------------------------------------------------------------------------------------------------
# 2. Revenue entries by quarter (p.131)
# ---------------------------------------------------------------------------------------------------------
REV_IMPROPER = dict(zip(['1999Q1','1999Q2','1999Q3','1999Q4','2000Q1','2000Q2','2000Q3','2000Q4','2001Q1','2001Q2','2001Q3','2001Q4','2002Q1'],
                        [85,5,65,50,19,121,161,27,17,132,117,92,67]))
REV_QUESTIONABLE = dict(zip(REV_IMPROPER.keys(), [26,89,65,67,88,115,99,95,88,68,158,107,42]))
for q, v in REV_IMPROPER.items():
    CURATED.append(rec(q, 'revenue_improper', v, B, 136, '131', '85 5 65 50 19 121 161 27 17 132 117 92 67 958',
                       'Special Investigative Committee finding', 'Improper revenue entries (table "Improper Revenue Entries"); mostly booked to the Corporate Unallocated account after quarter close.', mechanism='revenue'))
for q, v in REV_QUESTIONABLE.items():
    CURATED.append(rec(q, 'revenue_questionable', v, B, 136, '131', '26 89 65 67 88 115 99 95 88 68 158 107 42 1,107',
                       'Special Investigative Committee finding', 'Additional revenue items the Committee\'s accounting advisors classified as questionable (table in footnote 23).', mechanism='revenue'))
CURATED.append(rec('1999Q1-2002Q1', 'revenue_improper_total', 958, B, 136, '131', '85 5 65 50 19 121 161 27 17 132 117 92 67 958',
                   'Special Investigative Committee finding', 'Total improper revenue entries identified.', mechanism='revenue'))
CURATED.append(rec('1999Q1-2002Q1', 'revenue_items_pretax_effect', 1248, B, 136, '131', 'the overall impact on pre-tax income for the $2.065 billion of the combined improper and questionable revenue items is approximately $1.248 billion',
                   'Special Investigative Committee finding', 'Estimated pre-tax effect of the combined $2.065 billion of improper and questionable revenue items (the rest were reclassifications).', mechanism='revenue'))

# ---------------------------------------------------------------------------------------------------------
# 3. Committee summary table by area and year (p.17)
# ---------------------------------------------------------------------------------------------------------
SUMMARY_ROWS = {
    'revenue': ('Revenue 4 205 328 358 67 958', [205, 328, 358, 67, 958]),
    'line_costs': ('Line Costs 5 598 2,870 3,063 798 7,329', [598, 2870, 3063, 798, 7329]),
    'sga': ('SG&A 6 46 283 181 25 535', [46, 283, 181, 25, 535]),
    'other': ('Other 7 89 393 (4 ) (50 ) 428', [89, 393, -4, -50, 428]),
    'total': ('TOTAL 938 3,874 3,598 840 9,250', [938, 3874, 3598, 840, 9250]),
}
for area, (anchor, vals) in SUMMARY_ROWS.items():
    for yr, v in zip(['1999FY', '2000FY', '2001FY', '2002Q1', '1999Q1-2002Q1'], vals):
        CURATED.append(rec(yr, f'committee_improper_{area}', v, B, 22, '17', anchor, 'Special Investigative Committee finding',
                           'Summary of improper income statement amounts by area (table, p.17). 2002 column = first quarter 2002.', track='committee_summary'))

# ---------------------------------------------------------------------------------------------------------
# 4. SEC First Amended Complaint (Nov 5, 2002): quarterly line-cost reductions and the "false statements" table
# ---------------------------------------------------------------------------------------------------------
SEC_PARA = [
    ('2000Q3', 828, 'reducing the third quarter 2000 line costs by approximately $828 million'),
    ('2000Q4', 407, 'reducing the fourth quarter 2000 line costs by approximately $407 million'),
    ('2001Q1', 771, 'fraudulent concealment of approximately $771 million in WorldCom\'s line cost expenses for that quarter'),
    ('2001Q2', 560, 'effectively erased approximately $560 million from its line cost expenses for the second quarter of 2001'),
    ('2001Q3', 743, 'effectively erased approximately $743 million from its line cost e'),
]
for q, v, anchor in SEC_PARA:
    CURATED.append(rec(q, 'sec_alleged_line_cost_reduction', v, SEC, 1, '¶', anchor, 'SEC allegation (First Amended Complaint; WorldCom consented to judgment without admitting or denying)',
                       'Improper reduction of line costs alleged for the quarter.', track='sec_alleged'))
# Rows of the table "WorldCom's False Statements in Filings With Commission" (after ¶ 25); anchor = the full row text as printed.
SEC_TABLE = [
    ('2000Q3', '10-Q, 3rd Q. 2000 $3.867 billion $1.736 billion $4.695 billion $908 million', 3867, 1736, 4695, 908),
    ('2000FY', '10-K, 2000 $15.462 billion $7.568 billion $16.697 billion $6.333 billion', 15462, 7568, 16697, 6333),
    ('2001Q1', '10-Q, 1st Q. 2001 $4.108 billion $988 million $4.879 billion $217 million', 4108, 988, 4879, 217),
    ('2001Q2', '10-Q, 2nd Q. 2001 $3.73 billion $159 million $4.29 billion $401 million loss', 3730, 159, 4290, -401),
    ('2001Q3', '10-Q, 3rd Q. 2001 $3.745 billion $845 million $4.488 billion $102 million', 3745, 845, 4488, 102),
    ('2001FY', '10-K, 2001 $14.739 billion $2.393 billion $17.754 billion $622 million loss', 14739, 2393, 17754, -622),
    ('2002Q1', '10-Q, 1st Q. 2002 $3.479 billion $240 million $4.297 billion $578 million loss', 3479, 240, 4297, -578),
]
for q, row, rlc, rpti, alc, apti in SEC_TABLE:
    form = row.split(' $')[0]
    CURATED.append(rec(q, 'sec_reported_line_costs', rlc, SEC, 1, '¶ 25 table', row, 'SEC allegation (First Amended Complaint)', f'"Reported Line Cost Expenses" column for {form}.', track='sec_alleged'))
    CURATED.append(rec(q, 'sec_reported_pretax_income', rpti, SEC, 1, '¶ 25 table', row, 'SEC allegation (First Amended Complaint)', f'"Reported Income (before Taxes and Minority Interests)" column for {form}.', track='sec_alleged'))
    CURATED.append(rec(q, 'sec_actual_line_costs', alc, SEC, 1, '¶ 25 table', row, 'SEC allegation (First Amended Complaint)', f'"Actual Line Cost Expenses" column for {form}.', track='sec_alleged'))
    CURATED.append(rec(q, 'sec_actual_pretax_income', apti, SEC, 1, '¶ 25 table', row, 'SEC allegation (First Amended Complaint)', f'"Actual Income (before Taxes and Minority Interests)" column for {form}; loss shown negative.', track='sec_alleged'))
CURATED.append(rec('1999Q1-2002Q1', 'sec_total_income_overstatement', 9000, SEC, 1, '¶1', 'materially overstated the income it reported in its financial statements by approximately $9 billion',
                   'SEC allegation (First Amended Complaint)', 'Approximate total overstatement of income, 1999 through Q1 2002, as acknowledged by WorldCom per the complaint.', track='sec_alleged'))

# ---------------------------------------------------------------------------------------------------------
# 5. Company announcements: 8-K June 25, 2002 and 8-K August 8, 2002
# ---------------------------------------------------------------------------------------------------------
CURATED.append(rec('2001FY', 'company_announced_capitalized_line_costs', 3055, '8k-2002-06-25', 5, '5', 'was $3.055 billion for 2001 and $797 million for first quarter 2002',
                   'Company disclosure (Form 8-K, June 25, 2002)', 'Transfers of line costs to capital accounts in 2001 announced on June 25, 2002.', track='company_disclosure'))
CURATED.append(rec('2002Q1', 'company_announced_capitalized_line_costs', 797, '8k-2002-06-25', 5, '5', 'was $3.055 billion for 2001 and $797 million for first quarter 2002',
                   'Company disclosure (Form 8-K, June 25, 2002)', 'Transfers of line costs to capital accounts in Q1 2002 announced on June 25, 2002 (later refined to $818 million).', track='company_disclosure'))
AUG8 = [('1999FY', 217, 209), ('2000FY', 2864, 3257), ('2001FY', 3216, 3382), ('2002Q1', 885, 835), ('1999Q1-2002Q1', 7182, 7683)]
for per, ebitda, pretax in AUG8:
    CURATED.append(rec(per, 'company_announced_ebitda_reduction', ebitda, '8k-2002-08-08', 6, '2', 'Total reduction in EBITDA             $  217       $ 2,864       $ 3,216       $  885        $ 7,182',
                       'Company disclosure (Form 8-K, August 8, 2002)', 'Cumulative reduction in previously reported EBITDA (June 25 and August 8 announcements).', track='company_disclosure'))
    CURATED.append(rec(per, 'company_announced_pretax_reduction', pretax, '8k-2002-08-08', 6, '2', 'reductions                         $  209       $ 3,257       $ 3,382       $  835        $ 7,683',
                       'Company disclosure (Form 8-K, August 8, 2002)', 'Total pre-tax income reductions announced through August 8, 2002.', track='company_disclosure'))

# ---------------------------------------------------------------------------------------------------------
# 6. Company restatement — 2002 Form 10-K (filed March 12, 2004), MD&A p.42 and Note 2 (F-26), statements F-5
# ---------------------------------------------------------------------------------------------------------
RESTATE_ROWS = [
    ('previously_reported', 'Previously reported (1) $ 35,121 $ 2,375 $ 39,020 $ 7,581', (35121, 2375, 39020, 7581)),
    ('impairment', 'Impairment — (12,592 ) — (47,180 )', (None, -12592, None, -47180)),
    ('improper_reduction_of_access_costs', 'Improper reduction of access costs — (2,933 ) 6 (1,827 )', (None, -2933, 6, -1827)),
    ('purchase_accounting', 'Purchase accounting 14 (2,273 ) (193 ) (3,567 )', (14, -2273, -193, -3567)),
    ('long_lived_asset_adjustments', 'Long lived asset adjustments — 2,750 — (1,713 )', (None, 2750, None, -1713)),
    ('international', 'International (749 ) (899 ) 18 (487 )', (-749, -899, 18, -487)),
    ('revenue_related_adjustments', 'Revenue related adjustments (1,204 ) (575 ) (36 ) (995 )', (-1204, -575, -36, -995)),
    ('adjustments_to_accrued_liabilities', 'Adjustments to accrued liabilities — (823 ) — (732 )', (None, -823, None, -732)),
    ('embratel_and_avantel', 'Embratel and Avantel 5,268 (35 ) 1,127 (325 )', (5268, -35, 1127, -325)),
    ('unclassified_income_expense', 'Unclassified income/(expense) — 383 — (426 )', (None, 383, None, -426)),
    ('other', 'Other (7 ) (506 ) 4 (750 )', (-7, -506, 4, -750)),
    ('total_restatement_adjustments', 'Total restatement adjustments $ 3,322 $ (17,503 ) $ 926 $ (58,002 )', (3322, -17503, 926, -58002)),
    ('discontinued_operations_adjustment', 'Discontinued operations adjustment (2) (775 ) 1,323 (602 ) 449', (-775, 1323, -602, 449)),
    ('revenue_as_restated', 'Revenue, as restated $ 37,668 $ 39,344', (37668, None, 39344, None)),
    ('minority_interest_adjustment', 'Minority interest adjustment (2) (669 ) 52', (None, -669, None, 52)),
    ('pretax_loss_as_restated', 'Pre-tax loss, as restated $ (14,474 ) $ (49,920 )', (None, -14474, None, -49920)),
]
for key, anchor, (rev01, pti01, rev00, pti00) in RESTATE_ROWS:
    for per, rv, pv in (('2001FY', rev01, pti01), ('2000FY', rev00, pti00)):
        if rv is not None:
            CURATED.append(rec(per, f'restatement_revenue_{key}', rv, K02, 130, 'F-26', anchor, 'Company restatement (2002 Form 10-K, Note 2)', 'Revenue column of the "Summary of restatement items" table.', track='restated'))
        if pv is not None:
            CURATED.append(rec(per, f'restatement_pretax_{key}', pv, K02, 130, 'F-26', anchor, 'Company restatement (2002 Form 10-K, Note 2)', 'Pre-tax income (loss) column of the "Summary of restatement items" table.', track='restated'))
# Restated statement of operations (F-5)
F5 = [
    ('revenue', 'Revenues $ 32,202 $ 37,668 $ 39,344', (32202, 37668, 39344)),
    ('access_costs', 'Access costs 14,651 16,015 16,903', (14651, 16015, 16903)),
    ('costs_of_services_and_products', 'Costs of services and products 4,339 5,377 5,092', (4339, 5377, 5092)),
    ('sga', 'Selling, general and administrative 9,179 10,660 10,337', (9179, 10660, 10337)),
    ('da', 'Depreciation and amortization 3,291 4,851 8,485', (3291, 4851, 8485)),
    ('ppe_impairment', 'Property, plant and equipment impairment charges 4,599 5,729 14,057', (4599, 5729, 14057)),
    ('goodwill_impairment', 'Goodwill and intangibles impairment charges 400 6,863 33,123', (400, 6863, 33123)),
    ('operating_loss', 'Operating loss (4,222 ) (11,444 ) (49,079 )', (-4222, -11444, -49079)),
    ('pretax_loss', 'cumulative effect of a change in accounting principle (9,190 ) (14,474 ) (49,920 )', (-9190, -14474, -49920)),
    ('net_loss', 'Net loss (9,173 ) (15,597 ) (48,909 )', (-9173, -15597, -48909)),
]
for key, anchor, (v02, v01, v00) in F5:
    for per, v in (('2002FY', v02), ('2001FY', v01), ('2000FY', v00)):
        CURATED.append(rec(per, f'restated_{key}', v, K02, 109, 'F-5', anchor, 'Company restatement (2002 Form 10-K, consolidated statements of operations)',
                           'Restated (2001, 2000) or first-reported (2002) figure, audited by KPMG.', track='restated'))
# Equity effects (F-34)
CURATED.append(rec('2001FY', 'restatement_effect_on_net_income', -17078, K02, 138, 'F-34', 'Effect of restatement adjustments on net income for the current period (17,078 ) (53,074 )',
                   'Company restatement (2002 Form 10-K, Note 2)', 'Reduction of previously reported 2001 net income.', track='restated'))
CURATED.append(rec('2000FY', 'restatement_effect_on_net_income', -53074, K02, 138, 'F-34', 'Effect of restatement adjustments on net income for the current period (17,078 ) (53,074 )',
                   'Company restatement (2002 Form 10-K, Note 2)', 'Reduction of previously reported 2000 net income.', track='restated'))
CURATED.append(rec('2001FY', 'restatement_total_equity_reduction', -70797, K02, 138, 'F-34', 'Total restatement adjustments (70,797 ) (53,558 )',
                   'Company restatement (2002 Form 10-K, Note 2)', 'Cumulative net reduction to shareholders\' equity at December 31, 2001.', track='restated'))
CURATED.append(rec('2001FY', 'restated_ppe', 21486, K02, 137, 'F-33', 'Property, plant and equipment 42,665 (1,052 ) (20,127 ) 21,486',
                   'Company restatement (2002 Form 10-K, Note 2)', 'PP&E at December 31, 2001: previously reported $42,665 million, restated $21,486 million.', track='restated'))
CURATED.append(rec('2001FY', 'previously_reported_ppe', 42665, K02, 137, 'F-33', 'Property, plant and equipment 42,665 (1,052 ) (20,127 ) 21,486',
                   'Company restatement (2002 Form 10-K, Note 2)', 'PP&E at December 31, 2001 as previously reported.', track='restated'))
CURATED.append(rec('2001FY', 'restated_goodwill', 2284, K02, 137, 'F-33', 'Goodwill and other intangibles, net 46,583 (322 ) (43,977 ) 2,284',
                   'Company restatement (2002 Form 10-K, Note 2)', 'Goodwill and other intangibles at December 31, 2001: previously reported $46,583 million, restated $2,284 million.', track='restated'))
CURATED.append(rec('2001FY', 'previously_reported_goodwill', 46583, K02, 137, 'F-33', 'Goodwill and other intangibles, net 46,583 (322 ) (43,977 ) 2,284',
                   'Company restatement (2002 Form 10-K, Note 2)', 'Goodwill and other intangibles at December 31, 2001 as previously reported.', track='restated'))
CURATED.append(rec('2001FY', 'restated_cash_from_operations', 2845, K02, 138, 'F-34', 'Net cash from operating activities $ 7,994 2,845 $ 7,666 4,227',
                   'Company restatement (2002 Form 10-K, Note 2)', '2001 net cash from operating activities: previously reported $7,994 million, restated $2,845 million.', track='restated'))
CURATED.append(rec('2001FY', 'previously_reported_cash_from_operations', 7994, K02, 138, 'F-34', 'Net cash from operating activities $ 7,994 2,845 $ 7,666 4,227',
                   'Company restatement (2002 Form 10-K, Note 2)', '2001 net cash from operating activities as previously reported.', track='restated'))
CURATED.append(rec('2000FY', 'restated_cash_from_operations', 4227, K02, 138, 'F-34', 'Net cash from operating activities $ 7,994 2,845 $ 7,666 4,227',
                   'Company restatement (2002 Form 10-K, Note 2)', '2000 net cash from operating activities: previously reported $7,666 million, restated $4,227 million.', track='restated'))
CURATED.append(rec('2000FY', 'previously_reported_cash_from_operations', 7666, K02, 138, 'F-34', 'Net cash from operating activities $ 7,994 2,845 $ 7,666 4,227',
                   'Company restatement (2002 Form 10-K, Note 2)', '2000 net cash from operating activities as previously reported.', track='restated'))
