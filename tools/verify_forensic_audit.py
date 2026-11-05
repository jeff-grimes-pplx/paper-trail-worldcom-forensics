#!/usr/bin/env python3
"""WorldCom Primary-Source Forensic Audit Verification & Institutional Workbook Suite.

Programmatically validates:
  1. All 57 primary SEC EDGAR, DOJ, Bankruptcy Examiner, and Court filings against SHA-256 digests (3,119 pages, 9,137,625 chars).
  2. All 453 ledger values (379 page-cited primary proofs + 74 derived/reconstructed values and component formulas).
  3. All 47 primary-source timeline events and verbatim anchor texts.
  4. All 13 quarterly restatement arithmetic equations (Q1 1999 - Q1 2002):
     Reported + Accrual Releases + Capitalized Prepaid Capacity = Restated/Corrected Actual.
  5. Generates:
     - data/forensic_verification_report.json
     - data/WorldCom_Forensic_Audit_Ledger.csv
     - data/WorldCom_Forensic_Audit_Workbook.xlsx (6-tab institutional openpyxl workbook with live Excel formulas)
"""
import csv
import datetime
import hashlib
import json
import os
import re
import shutil
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
APP_DATA = os.path.join(ROOT, "app", "data")


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\u2019", "'").replace("’", "'").replace("‘", "'")).strip()


def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    register = json.load(open(os.path.join(DATA, "register.json")))
    reg_by_id = {r["id"]: r for r in register}
    ledger_obj = json.load(open(os.path.join(DATA, "ledger.json")))
    entries = ledger_obj["entries"]
    by_id = {e["id"]: e for e in entries}
    series_obj = json.load(open(os.path.join(DATA, "series.json")))
    quarters = series_obj["quarters"]
    q_series = series_obj["series"]
    annual = series_obj["annual"]
    timeline = json.load(open(os.path.join(DATA, "timeline.json")))
    pagecounts = json.load(open(os.path.join(DATA, "pagecounts.json")))
    visual_ver = json.load(open(os.path.join(DATA, "verification.json")))
    visual_map = {r["id"]: r for r in visual_ver.get("rows", [])}

    # 1. Verify all 57 SHA-256 digests and paginated page counts
    sha_Lines = [l.strip() for l in open(os.path.join(DATA, "SHA256SUMS.txt")) if l.strip()]
    sha_expected = {}
    for line in sha_Lines:
        digest, relpath = line.split(None, 1)
        sha_expected[relpath.strip()] = digest.strip()

    doc_checks = []
    pages_cache = {}
    total_pages = 0
    total_chars = 0
    for doc in register:
        rel = doc["local_path"]
        full = os.path.join(ROOT, rel)
        exists = os.path.exists(full)
        actual_sha = compute_sha256(full) if exists else None
        expected_sha = sha_expected.get(rel, doc.get("sha256"))
        sha_ok = (actual_sha == expected_sha == doc.get("sha256"))
        pjson = json.load(open(os.path.join(DATA, "pages", f"{doc['id']}.json")))
        pages_cache[doc["id"]] = pjson["pages"]
        n_pages = len(pjson["pages"])
        n_chars = sum(len(p.get("text", "")) for p in pjson["pages"])
        total_pages += n_pages
        total_chars += n_chars
        doc_checks.append({
            "id": doc["id"],
            "form": doc.get("form", doc.get("kind")),
            "filed": doc.get("filed"),
            "pages": n_pages,
            "chars": n_chars,
            "bytes": doc.get("bytes"),
            "sha256": actual_sha,
            "sha256_match": sha_ok,
        })
        assert sha_ok, f"SHA-256 mismatch on {doc['id']}: {actual_sha} != {expected_sha}"

    # 2. Verify all 453 ledger entries (379 cited + 74 derived/reconstructed)
    cited_ok = 0
    cited_total = 0
    derived_ok = 0
    derived_total = 0

    for e in entries:
        if e.get("doc") and e.get("page"):
            cited_total += 1
            pg_list = pages_cache[e["doc"]]
            assert 1 <= e["page"] <= len(pg_list), f"Page out of range for {e['id']}"
            pg_text = pg_list[e["page"] - 1]["text"]
            found = norm(e["anchor"]) in norm(pg_text)
            assert found, f"Anchor missing for {e['id']} on {e['doc']} p.{e['page']}"
            cited_ok += 1
        else:
            derived_total += 1
            comps = e.get("components", [])
            assert len(comps) >= 1, f"Derived entry {e['id']} has no components"
            for cid in comps:
                assert cid in by_id, f"Missing component {cid} for {e['id']}"
            if e["track"] == "reported-derived":
                c0, c1 = by_id[comps[0]]["value"], by_id[comps[1]]["value"]
                assert abs((c0 - c1) - e["value"]) < 1e-6, f"Derived subtraction mismatch on {e['id']}"
            elif e["track"] == "reconstructed":
                c0 = by_id[comps[0]]["value"]
                c1 = by_id[comps[1]]["value"] if len(comps) > 1 else 0.0
                if e["metric"] == "line_costs":
                    assert abs((c0 + c1) - e["value"]) < 1e-6, f"Reconstructed line_costs mismatch on {e['id']}"
                else:
                    assert abs((c0 - c1) - e["value"]) < 1e-6, f"Reconstructed subtraction mismatch on {e['id']}"
            derived_ok += 1

    # 3. Verify all 47 timeline events
    timeline_ok = 0
    for ev in timeline:
        pg_list = pages_cache[ev["doc"]]
        pg_text = pg_list[ev["page"] - 1]["text"]
        assert norm(ev["anchor"]) in norm(pg_text), f"Timeline anchor missing: {ev['id']}"
        timeline_ok += 1

    # 4. Verify quarterly restatement equations across all 13 quarters (Q1 1999 - Q1 2002)
    quarterly_audit = []
    sum_accrual_releases = 0.0
    sum_cap_reductions = 0.0
    sum_cap_ppe = 0.0
    sum_rev_improper = 0.0
    sum_rev_questionable = 0.0

    for q in quarters:
        s = q_series[q]
        mech = s.get("mechanism")
        lc_rep = s["line_costs_reported"]
        lc_red = s["line_cost_reduction"] or 0.0
        lc_cor = s["line_costs_corrected"]
        accrual_rel = lc_red if mech == "accrual_release" else 0.0
        cap_red = lc_red if mech == "capitalization" else 0.0
        cap_ppe = s.get("capitalized") or 0.0
        other_cap_adj = cap_red - cap_ppe

        # Equation 1: Reported Line Costs + Accrual Releases + Capitalized Prepaid Capacity Reductions = Restated/Corrected Line Costs
        eq_lc_ok = abs((lc_rep + accrual_rel + cap_red) - lc_cor) < 1e-6
        assert eq_lc_ok, f"Line cost equation failed for {q}"

        # Equation 2: Pre-Tax Income Reported - (Accrual Releases + Capitalized Reductions) = Corrected Pre-Tax Income
        pti_rep = s["pretax_reported"]
        pti_cor = s["pretax_corrected"]
        eq_pti_ok = abs((pti_rep - (accrual_rel + cap_red)) - pti_cor) < 1e-6
        assert eq_pti_ok, f"Pre-tax equation failed for {q}"

        # Equation 3: Revenue Reported - Improper Revenue = Corrected Revenue
        rev_rep = s["revenue_reported"]
        rev_imp = s["revenue_improper"] or 0.0
        rev_quest = s["revenue_questionable"] or 0.0
        rev_cor = s["revenue_corrected"]
        eq_rev_ok = abs((rev_rep - rev_imp) - rev_cor) < 1e-6
        assert eq_rev_ok, f"Revenue equation failed for {q}"

        # Equation 4: CapEx Reported - Capitalized Line Costs = Corrected CapEx (when applicable)
        cx_rep = s["capex_reported"]
        cx_cor = s["capex_corrected"] if s["capex_corrected"] is not None else cx_rep
        eq_cx_ok = abs((cx_rep - cap_ppe) - cx_cor) < 1e-6
        assert eq_cx_ok, f"CapEx equation failed for {q}"

        # Equation 5: Line-cost-to-revenue E/R ratios
        er_rep = round(100.0 * lc_rep / rev_rep, 1)
        er_cor = round(100.0 * lc_cor / rev_cor, 1)
        assert abs(er_rep - s["er_reported"]) < 1e-6 and abs(er_cor - s["er_corrected"]) < 1e-6

        sum_accrual_releases += accrual_rel
        sum_cap_reductions += cap_red
        sum_cap_ppe += cap_ppe
        sum_rev_improper += rev_imp
        sum_rev_questionable += rev_quest

        quarterly_audit.append({
            "quarter": q,
            "mechanism": mech or "none",
            "line_costs_reported_m": lc_rep,
            "accrual_release_m": accrual_rel,
            "capitalized_line_cost_reduction_m": cap_red,
            "capitalized_ppe_transfer_m": cap_ppe,
            "other_line_cost_adj_m": other_cap_adj,
            "line_costs_corrected_m": lc_cor,
            "pretax_reported_m": pti_rep,
            "pretax_corrected_m": pti_cor,
            "revenue_reported_m": rev_rep,
            "revenue_improper_m": rev_imp,
            "revenue_questionable_m": rev_quest,
            "revenue_corrected_m": rev_cor,
            "capex_reported_m": cx_rep,
            "capex_corrected_m": cx_cor,
            "er_reported_pct": er_rep,
            "er_corrected_pct": er_cor,
            "equations_verified": True,
        })

    assert sum_accrual_releases == 3297.0, f"Expected $3,297M accrual releases, got {sum_accrual_releases}"
    assert sum_cap_reductions == 3883.0, f"Expected $3,883M capitalization reductions, got {sum_cap_reductions}"
    assert sum_cap_ppe == 3506.0, f"Expected $3,506M PP&E capitalized, got {sum_cap_ppe}"
    assert (sum_accrual_releases + sum_cap_reductions) == 7180.0
    assert sum_rev_improper == 958.0
    assert sum_rev_questionable == 1107.0

    report = {
        "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "status": "ALL_CHECKS_PASSED",
        "summary": {
            "primary_documents_verified": len(doc_checks),
            "sha256_checksums_matched": sum(1 for d in doc_checks if d["sha256_match"]),
            "total_pages_paginated": total_pages,
            "total_characters_extracted": total_chars,
            "ledger_entries_total": len(entries),
            "page_cited_entries_verified": cited_ok,
            "derived_reconstructed_entries_verified": derived_ok,
            "visual_spot_checks_matched": sum(1 for r in visual_ver.get("rows", []) if r["result"] == "match"),
            "timeline_events_verified": timeline_ok,
            "quarters_reconciled": len(quarterly_audit),
            "phase1_accrual_releases_m": sum_accrual_releases,
            "phase2_capitalized_reductions_m": sum_cap_reductions,
            "phase2_ppe_capex_transfers_m": sum_cap_ppe,
            "cumulative_line_cost_fraud_m": sum_accrual_releases + sum_cap_reductions,
            "cumulative_improper_revenue_m": sum_rev_improper,
            "cumulative_questionable_revenue_m": sum_rev_questionable,
        },
        "quarterly_reconciliation": quarterly_audit,
    }

    report_path = os.path.join(DATA, "forensic_verification_report.json")
    json.dump(report, open(report_path, "w"), indent=2)

    # 5. Write CSV export of all 453 ledger rows
    csv_path = os.path.join(DATA, "WorldCom_Forensic_Audit_Ledger.csv")
    csv_cols = [
        "id", "period", "track", "metric", "label", "value_usd_millions", "unit",
        "mechanism", "basis", "formula", "components", "doc_id", "doc_short",
        "form", "filed_date", "page_seq", "printed_page_label", "anchor_verified",
        "visual_verification", "anchor_excerpt", "source_url", "file_sha256", "note"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(csv_cols)
        for e in entries:
            doc = reg_by_id.get(e.get("doc")) if e.get("doc") else None
            vv = visual_map.get(e["id"])
            w.writerow([
                e["id"],
                e["period"],
                e["track"],
                e["metric"],
                e["label"],
                e["value"],
                e.get("unit", "USD millions"),
                e.get("mechanism", ""),
                e.get("basis", ""),
                e.get("formula", ""),
                "; ".join(e.get("components", [])),
                e.get("doc", ""),
                doc.get("short", "") if doc else "",
                doc.get("form", "") if doc else "",
                doc.get("filed", "") if doc else "",
                e.get("page", ""),
                e.get("page_label", ""),
                "TRUE" if e.get("anchor_found") else ("DERIVED" if not e.get("doc") else "FALSE"),
                vv["result"] if vv else "",
                e.get("anchor", ""),
                doc.get("url", "") if doc else "",
                doc.get("sha256", "") if doc else "",
                e.get("note", ""),
            ])

    # 6. Build Multi-Tab Institutional Excel Workbook (.xlsx)
    xlsx_path = os.path.join(DATA, "WorldCom_Forensic_Audit_Workbook.xlsx")
    build_workbook(
        xlsx_path, report, quarterly_audit, annual, entries, register,
        reg_by_id, timeline, pagecounts, visual_map
    )

    # Sync to app/data and workspace root
    os.makedirs(APP_DATA, exist_ok=True)
    shutil.copy2(report_path, os.path.join(APP_DATA, "forensic_verification_report.json"))
    shutil.copy2(csv_path, os.path.join(APP_DATA, "WorldCom_Forensic_Audit_Ledger.csv"))
    shutil.copy2(xlsx_path, os.path.join(APP_DATA, "WorldCom_Forensic_Audit_Workbook.xlsx"))
    shutil.copy2(xlsx_path, "/home/user/workspace/WorldCom_Forensic_Audit_Workbook.xlsx")

    print("=== WORLDCOM FORENSIC AUDIT VERIFICATION COMPLETE ===")
    print(json.dumps(report["summary"], indent=2))


def build_workbook(xlsx_path, report, quarterly_audit, annual, entries, register, reg_by_id, timeline, pagecounts, visual_map):
    wb = openpyxl.Workbook()
    # Styles
    f_title = Font(name="Calibri", size=14, bold=True, color="15140F")
    f_sub = Font(name="Calibri", size=10, italic=True, color="4E4B43")
    f_sec = Font(name="Calibri", size=11, bold=True, color="15140F")
    f_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    f_data = Font(name="Calibri", size=10, color="15140F")
    f_mono = Font(name="Consolas", size=9.5, color="15140F")
    f_rep = Font(name="Calibri", size=10, bold=True, color="27496D")
    f_true = Font(name="Calibri", size=10, bold=True, color="8E2C25")
    f_tot = Font(name="Calibri", size=10, bold=True, color="15140F")
    f_link = Font(name="Consolas", size=9, color="27496D", underline="single")

    fill_hdr = PatternFill("solid", fgColor="1F242B")
    fill_subhdr = PatternFill("solid", fgColor="EBE6D9")
    fill_zebra = PatternFill("solid", fgColor="F8F5EE")
    fill_tot = PatternFill("solid", fgColor="E2DCCB")
    fill_fraud1 = PatternFill("solid", fgColor="F4E8E6")
    fill_fraud2 = PatternFill("solid", fgColor="EFE0DD")

    thin = Side(border_style="thin", color="CFC8B4")
    double_b = Side(border_style="double", color="15140F")
    top_thin = Side(border_style="thin", color="15140F")
    b_grid = Border(left=thin, right=thin, top=thin, bottom=thin)
    b_total = Border(top=top_thin, bottom=double_b, left=thin, right=thin)

    # ---------------------------------------------------------
    # TAB 1: Executive_Audit_Summary
    # ---------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Executive_Audit_Summary"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "PAPER TRAIL — WORLDCOM, INC. (1999–2002) FORENSIC ACCOUNTING RECONSTRUCTION"
    ws1["A1"].font = f_title
    ws1["A2"] = (
        f"Verified across {report['summary']['primary_documents_verified']} primary SEC/DOJ/Court filings "
        f"({report['summary']['total_pages_paginated']:,} pages) · "
        f"{report['summary']['ledger_entries_total']} ledger values ({report['summary']['page_cited_entries_verified']} page-cited) · "
        f"All {report['summary']['sha256_checksums_matched']}/57 SHA-256 digests verified"
    )
    ws1["A2"].font = f_sub

    ws1["A4"] = "PART I: QUARTERLY RECONCILIATION & RESTATEMENT ARITHMETIC PROOF ($ MILLIONS)"
    ws1["A4"].font = f_sec

    headers1 = [
        "Quarter", "Fraud Phase / Mechanism",
        "Reported Line Costs (10-Q/10-K)", "Improper Accrual Releases (Phase I)",
        "Improper Capitalized Line Costs (Phase II)", "Restated / Corrected Line Costs (Actual)",
        "Line-Cost Fraud Gap", "Of Which: Transferred to PP&E CapEx",
        "Reported Pre-Tax Income", "Corrected Pre-Tax Income (Ex-Line-Cost Fraud)",
        "Reported Revenues", "Improper 'Close the Gap' Revenues",
        "Corrected Revenues", "Questionable Revenues (Memo)",
        "Reported CapEx", "Corrected CapEx",
        "Reported E/R Ratio (%)", "Corrected E/R Ratio (%)"
    ]
    for col_idx, h in enumerate(headers1, 1):
        c = ws1.cell(row=5, column=col_idx, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws1.row_dimensions[5].height = 30

    for i, qa in enumerate(quarterly_audit):
        r = 6 + i
        mech_label = (
            "Phase I: Accrual Release (GL 2140 → GL 5100)" if qa["mechanism"] == "accrual_release"
            else "Phase II: Prepaid Capacity CapEx (GL 5100 → GL 1650)" if qa["mechanism"] == "capitalization"
            else "Baseline (No Line-Cost Entry Identified)"
        )
        ws1.cell(row=r, column=1, value=qa["quarter"]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r, column=2, value=mech_label)
        ws1.cell(row=r, column=3, value=qa["line_costs_reported_m"])
        ws1.cell(row=r, column=4, value=qa["accrual_release_m"])
        ws1.cell(row=r, column=5, value=qa["capitalized_line_cost_reduction_m"])
        # Live Excel formula: Reported + Accrual Release + Capitalized Reduction
        ws1.cell(row=r, column=6, value=f"=C{r}+D{r}+E{r}")
        ws1.cell(row=r, column=7, value=f"=F{r}-C{r}")
        ws1.cell(row=r, column=8, value=qa["capitalized_ppe_transfer_m"])
        ws1.cell(row=r, column=9, value=qa["pretax_reported_m"])
        ws1.cell(row=r, column=10, value=f"=I{r}-G{r}")
        ws1.cell(row=r, column=11, value=qa["revenue_reported_m"])
        ws1.cell(row=r, column=12, value=qa["revenue_improper_m"])
        ws1.cell(row=r, column=13, value=f"=K{r}-L{r}")
        ws1.cell(row=r, column=14, value=qa["revenue_questionable_m"])
        ws1.cell(row=r, column=15, value=qa["capex_reported_m"])
        ws1.cell(row=r, column=16, value=f"=O{r}-H{r}")
        ws1.cell(row=r, column=17, value=f"=ROUND(C{r}/K{r}*100,1)")
        ws1.cell(row=r, column=18, value=f"=ROUND(F{r}/M{r}*100,1)")

        row_fill = fill_fraud1 if qa["mechanism"] == "accrual_release" else (fill_fraud2 if qa["mechanism"] == "capitalization" else fill_zebra)
        for c_i in range(1, 19):
            cell = ws1.cell(row=r, column=c_i)
            cell.font = f_rep if c_i in (3, 9, 11, 15) else (f_true if c_i in (6, 7, 10, 13, 16) else f_data)
            cell.fill = row_fill
            cell.border = b_grid
            if c_i >= 3 and c_i <= 16:
                cell.number_format = "#,##0;(#,##0);\"-\""
            elif c_i in (17, 18):
                cell.number_format = "0.0\"%\""

    # Totals row
    tr = 6 + len(quarterly_audit)
    ws1.cell(row=tr, column=1, value="TOTAL (13Q)").alignment = Alignment(horizontal="center")
    ws1.cell(row=tr, column=2, value="Cumulative 1999Q1 – 2002Q1")
    for c_i in range(3, 17):
        col_let = get_column_letter(c_i)
        ws1.cell(row=tr, column=c_i, value=f"=SUM({col_let}6:{col_let}{tr-1})")
    ws1.cell(row=tr, column=17, value=f"=ROUND(C{tr}/K{tr}*100,1)")
    ws1.cell(row=tr, column=18, value=f"=ROUND(F{tr}/M{tr}*100,1)")
    for c_i in range(1, 19):
        cell = ws1.cell(row=tr, column=c_i)
        cell.font = f_tot
        cell.fill = fill_tot
        cell.border = b_total
        if 3 <= c_i <= 16:
            cell.number_format = "#,##0;(#,##0);\"-\""
        elif c_i in (17, 18):
            cell.number_format = "0.0\"%\""

    # Part II: Annual Official Totals Comparison
    ar_start = tr + 3
    ws1.cell(row=ar_start, column=1, value="PART II: ANNUAL RECONCILIATION ACROSS OFFICIAL INVESTIGATIONS & 2004 RESTATEMENT ($ MILLIONS)").font = f_sec
    ann_headers = [
        "Period", "Quarterly Line-Cost Entries (Chart)", "Special Committee: Line Costs (p. 17)",
        "Special Committee: All Areas (p. 17)", "Company 8-K (Aug 8, 2002)",
        "2002 10-K: Access-Cost Restatement", "Reported Pre-Tax Income (10-K)",
        "Restated Pre-Tax Income (2002 10-K)", "Reported Net Income (10-K)", "Restated Net Loss (2002 10-K)"
    ]
    for c_i, h in enumerate(ann_headers, 1):
        c = ws1.cell(row=ar_start + 1, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws1.row_dimensions[ar_start + 1].height = 28

    for idx, pkey in enumerate(["1999", "2000", "2001", "2002Q1"]):
        r = ar_start + 2 + idx
        a = annual[pkey]
        vals = [
            pkey,
            a.get("quarterly_line_cost_reductions"),
            a.get("committee_line_costs"),
            a.get("committee_total"),
            a.get("company_aug8_pretax"),
            -a["tenk_access_costs"] if a.get("tenk_access_costs") is not None else None,
            a.get("reported_pretax"),
            a.get("restated_pretax"),
            a.get("reported_net_income"),
            a.get("restated_net_income"),
        ]
        for c_i, v in enumerate(vals, 1):
            cell = ws1.cell(row=r, column=c_i, value=v)
            cell.font = f_data
            cell.border = b_grid
            if c_i > 1:
                cell.number_format = "#,##0;(#,##0);\"—\""

    # ---------------------------------------------------------
    # TAB 2: GL_Journal_Entry_Trace
    # ---------------------------------------------------------
    ws2 = wb.create_sheet("GL_Journal_Entry_Trace")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "GENERAL-LEDGER DOUBLE-ENTRY JOURNAL TRACE (1999–Q1 2002)"
    ws2["A1"].font = f_title
    ws2["A2"] = "Traces every improper top-side general-ledger entry documented in the Special Investigative Committee Report (Beresford et al., 2003) and SEC Enforcement Complaints."
    ws2["A2"].font = f_sub

    gl_headers = [
        "Quarter", "Fraud Device", "Debit Account (GL)", "Credit Account (GL)",
        "Improper Line-Cost Entry ($M)", "Of Which: Capitalized to PP&E ($M)",
        "Improper Revenue Entry ($M)", "Questionable Revenue ($M)",
        "Directing / Booking Officers Cited", "Primary Proof Document", "Cited Page", "Verbatim Filing Anchor"
    ]
    for c_i, h in enumerate(gl_headers, 1):
        c = ws2.cell(row=4, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws2.row_dimensions[4].height = 28

    officers_by_q = {
        "1999Q1": "Ebbers / Sullivan / Corporate Unallocated Revenue Accounting",
        "1999Q2": "Sullivan / Myers / Yates (First-Level Line-Cost Accrual Release)",
        "1999Q3": "Sullivan / Myers / Yates (First-Level Line-Cost Accrual Release)",
        "1999Q4": "Sullivan / Myers / Yates / Vinson (International & Telco Accrual Release)",
        "2000Q1": "Sullivan / Myers / Yates / Vinson / Normand (Domestic Telco Accrual Release)",
        "2000Q2": "Sullivan / Myers / Yates / Vinson / Normand (Domestic Telco Accrual Release)",
        "2000Q3": "Sullivan / Myers / Yates / Vinson / Normand (Accrual & Reserve Release)",
        "2000Q4": "Sullivan / Myers / Yates / Vinson / Normand (Tax Reserve $407M & Accrual Release)",
        "2001Q1": "Ebbers / Sullivan / Myers / Yates / Vinson / Normand ('Prepaid Capacity' CapEx)",
        "2001Q2": "Ebbers / Sullivan / Myers / Yates / Vinson / Normand ('Prepaid Capacity' CapEx)",
        "2001Q3": "Ebbers / Sullivan / Myers / Yates / Vinson / Normand ('Prepaid Capacity' CapEx)",
        "2001Q4": "Ebbers / Sullivan / Myers / Yates / Vinson / Normand ('Prepaid Capacity' CapEx)",
        "2002Q1": "Ebbers / Sullivan / Myers / Yates / Vinson / Normand ('Prepaid Capacity' CapEx)",
    }
    gl_rows = []
    for qa in quarterly_audit:
        q = qa["quarter"]
        mech = qa["mechanism"]
        adj_e = next((x for x in entries if x["id"] == f"adjustment:{q}:line_cost_reduction"), None)
        rev_e = next((x for x in entries if x["id"] == f"adjustment:{q}:revenue_improper"), None)
        cite_e = adj_e or rev_e
        if mech == "accrual_release":
            dev = "Phase I: Release Line-Cost Accruals"
            dr = "GL 2140 Accrued Carrier Liabilities & Reserves"
            cr = "GL 5100 Line Cost Expense"
        elif mech == "capitalization":
            dev = "Phase II: Capitalize 'Prepaid Capacity' to PP&E"
            dr = "GL 1650 Construction in Progress / PP&E"
            cr = "GL 5100 Line Cost Expense"
        else:
            dev = "Baseline (Corporate Unallocated Revenue Only)"
            dr = "GL 1120 Accounts Receivable / Unbilled"
            cr = "GL 4090 Corporate Unallocated Revenue"
        gl_rows.append((
            q, dev, dr, cr,
            qa["accrual_release_m"] + qa["capitalized_line_cost_reduction_m"],
            qa["capitalized_ppe_transfer_m"],
            qa["revenue_improper_m"],
            qa["revenue_questionable_m"],
            officers_by_q.get(q, "Sullivan / Myers / Yates"),
            cite_e.get("doc", "beresford-report") if cite_e else "beresford-report",
            f"p. {cite_e['page']} ({cite_e.get('page_label', '')})" if cite_e else "",
            cite_e.get("anchor", "") if cite_e else "",
        ))
    for i, gr in enumerate(gl_rows):
        r = 5 + i
        for c_i, val in enumerate(gr, 1):
            cell = ws2.cell(row=r, column=c_i, value=val)
            cell.font = f_data
            cell.border = b_grid
            if c_i in (5, 6, 7, 8):
                cell.number_format = "#,##0;(#,##0);\"-\""
    tr2 = 5 + len(gl_rows)
    ws2.cell(row=tr2, column=1, value="TOTAL").font = f_tot
    ws2.cell(row=tr2, column=2, value="1999Q1 – 2002Q1 General-Ledger Totals").font = f_tot
    for c_i in (5, 6, 7, 8):
        col_let = get_column_letter(c_i)
        ws2.cell(row=tr2, column=c_i, value=f"=SUM({col_let}5:{col_let}{tr2-1})")
    for c_i in range(1, 13):
        c = ws2.cell(row=tr2, column=c_i)
        c.font = f_tot
        c.fill = fill_tot
        c.border = b_total
        if c_i in (5, 6, 7, 8):
            c.number_format = "#,##0;(#,##0);\"-\""

    # ---------------------------------------------------------
    # TAB 3: Forensic_Ledger_453
    # ---------------------------------------------------------
    ws3 = wb.create_sheet("Forensic_Ledger_453")
    ws3.views.sheetView[0].showGridLines = True
    ws3["A1"] = "COMPLETE 453-VALUE PAGE-ANCHORED FORENSIC LEDGER"
    ws3["A1"].font = f_title
    ws3["A2"] = "379 page-cited primary values + 74 derived/reconstructed values with component formulas."
    ws3["A2"].font = f_sub

    l_headers = [
        "Ledger ID", "Period", "Track", "Metric", "Label", "Value ($M / %)", "Unit",
        "Mechanism", "Formula / Basis", "Components", "Document ID", "Document Short",
        "Page (Seq)", "Printed Page", "Anchor Verified", "Visual Check", "Verbatim Anchor", "Source URL"
    ]
    for c_i, h in enumerate(l_headers, 1):
        c = ws3.cell(row=4, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws3.row_dimensions[4].height = 26

    for i, e in enumerate(entries):
        r = 5 + i
        doc = reg_by_id.get(e.get("doc")) if e.get("doc") else None
        vv = visual_map.get(e["id"])
        row_vals = [
            e["id"], e["period"], e["track"], e["metric"], e["label"], e["value"],
            e.get("unit", "USD millions"), e.get("mechanism", ""),
            e.get("formula") or e.get("basis", ""),
            ", ".join(e.get("components", [])),
            e.get("doc", ""), doc.get("short", "") if doc else "",
            e.get("page", ""), e.get("page_label", ""),
            "VERIFIED" if e.get("anchor_found") else ("FORMULA" if not e.get("doc") else "UNVERIFIED"),
            vv["result"].upper() if vv else "",
            e.get("anchor", ""),
            doc.get("url", "") if doc else ""
        ]
        for c_i, val in enumerate(row_vals, 1):
            cell = ws3.cell(row=r, column=c_i, value=val)
            cell.font = f_mono if c_i in (1, 11, 17) else (f_link if c_i == 18 and val else f_data)
            cell.border = b_grid
            if c_i == 6:
                cell.number_format = "#,##0.0;(#,##0.0);0" if "pct" in e["metric"] else "#,##0;(#,##0);0"

    # ---------------------------------------------------------
    # TAB 4: Restatement_2002_10K
    # ---------------------------------------------------------
    ws4 = wb.create_sheet("Restatement_2002_10K")
    ws4.views.sheetView[0].showGridLines = True
    ws4["A1"] = "COMPANY RESTATEMENT BRIDGE BY CATEGORY (2002 FORM 10-K, NOTE 2, P. F-26, FILED MARCH 12, 2004)"
    ws4["A1"].font = f_title
    ws4["A2"] = "Pre-tax effect ($ millions) for Fiscal Years 2000 and 2001 across all 10 restatement categories."
    ws4["A2"].font = f_sub

    r_headers = ["Category", "Metric Key", "FY 2000 ($M)", "FY 2001 ($M)", "Combined 2000–2001 ($M)", "Filing Citation", "Printed Page"]
    for c_i, h in enumerate(r_headers, 1):
        c = ws4.cell(row=4, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
    cats = [
        ("Previously reported pre-tax income", "restatement_pretax_previously_reported"),
        ("Impairment of goodwill and PP&E", "restatement_pretax_impairment"),
        ("Improper reduction of access costs (line costs)", "restatement_pretax_improper_reduction_of_access_costs"),
        ("Purchase accounting adjustments", "restatement_pretax_purchase_accounting"),
        ("Long-lived asset adjustments", "restatement_pretax_long_lived_asset_adjustments"),
        ("International adjustments", "restatement_pretax_international"),
        ("Revenue-related adjustments", "restatement_pretax_revenue_related_adjustments"),
        ("Adjustments to accrued liabilities", "restatement_pretax_adjustments_to_accrued_liabilities"),
        ("Embratel and Avantel adjustments", "restatement_pretax_embratel_and_avantel"),
        ("Unclassified income / (expense)", "restatement_pretax_unclassified_income_expense"),
        ("Other adjustments", "restatement_pretax_other"),
        ("Total restatement adjustments", "restatement_pretax_total_restatement_adjustments"),
        ("Pre-tax loss as restated", "restatement_pretax_pretax_loss_as_restated"),
    ]
    for i, (label, mkey) in enumerate(cats):
        r = 5 + i
        e00 = next((x for x in entries if x["track"] == "restated" and x["metric"] == mkey and x["period"] == "2000FY"), None)
        e01 = next((x for x in entries if x["track"] == "restated" and x["metric"] == mkey and x["period"] == "2001FY"), None)
        ws4.cell(row=r, column=1, value=label)
        ws4.cell(row=r, column=2, value=mkey).font = f_mono
        ws4.cell(row=r, column=3, value=e00["value"] if e00 else None).number_format = "#,##0;(#,##0);\"-\""
        ws4.cell(row=r, column=4, value=e01["value"] if e01 else None).number_format = "#,##0;(#,##0);\"-\""
        ws4.cell(row=r, column=5, value=f"=C{r}+D{r}").number_format = "#,##0;(#,##0);\"-\""
        ws4.cell(row=r, column=6, value="Form 10-K · FY 2002 (10k-2002)")
        ws4.cell(row=r, column=7, value="F-26 (seq p. 129)")
        is_bold = mkey in ("restatement_pretax_previously_reported", "restatement_pretax_total_restatement_adjustments", "restatement_pretax_pretax_loss_as_restated")
        for c_i in range(1, 8):
            c = ws4.cell(row=r, column=c_i)
            c.border = b_total if is_bold else b_grid
            if is_bold:
                c.font = f_tot
                c.fill = fill_tot

    # ---------------------------------------------------------
    # TAB 5: Primary_Document_Register
    # ---------------------------------------------------------
    ws5 = wb.create_sheet("Primary_Document_Register")
    ws5.views.sheetView[0].showGridLines = True
    ws5["A1"] = "PRIMARY SOURCE DOCUMENT REGISTER (57 PUBLIC FILINGS, 3,119 PAGES, SHA-256 VERIFIED)"
    ws5["A1"].font = f_title

    d_headers = ["Doc ID", "Short Title", "Full Title", "Role", "Authority", "Form / Kind", "Filing Date", "Pages", "Characters", "Bytes", "SHA-256 Digest", "Source URL"]
    for c_i, h in enumerate(d_headers, 1):
        c = ws5.cell(row=3, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
    for i, d in enumerate(register):
        r = 4 + i
        pc = pagecounts.get(d["id"], {})
        vals = [
            d["id"], d.get("short", ""), d["title"], d.get("role", ""), d.get("authority", ""),
            d.get("form") or d.get("kind", ""), d.get("filed", ""),
            pc.get("pages", 0), pc.get("chars", 0), d.get("bytes", 0),
            d.get("sha256", ""), d.get("url", "")
        ]
        for c_i, v in enumerate(vals, 1):
            c = ws5.cell(row=r, column=c_i, value=v)
            c.font = f_mono if c_i in (1, 11) else (f_link if c_i == 12 else f_data)
            c.border = b_grid
            if c_i in (8, 9, 10):
                c.number_format = "#,##0"

    # ---------------------------------------------------------
    # TAB 6: Chronology_47_Events
    # ---------------------------------------------------------
    ws6 = wb.create_sheet("Chronology_47_Events")
    ws6.views.sheetView[0].showGridLines = True
    ws6["A1"] = "FORENSIC CHRONOLOGY — 47 PRIMARY-SOURCE-ANCHORED EVENTS (1999–2006)"
    ws6["A1"].font = f_title

    t_headers = ["Event ID", "Date", "Category", "Headline", "Narrative Summary", "Document ID", "Document Title", "Page", "Printed Label", "Anchor Verified", "Verbatim Anchor"]
    for c_i, h in enumerate(t_headers, 1):
        c = ws6.cell(row=3, column=c_i, value=h)
        c.font = f_hdr
        c.fill = fill_hdr
    for i, ev in enumerate(timeline):
        r = 4 + i
        vals = [
            ev["id"], ev["date"], ev["kind"], ev["title"], ev["body"],
            ev["doc"], ev.get("doc_title", ""), ev["page"], ev.get("page_label", ""),
            "VERIFIED" if ev.get("anchor_found") else "FALSE", ev.get("anchor", "")
        ]
        for c_i, v in enumerate(vals, 1):
            c = ws6.cell(row=r, column=c_i, value=v)
            c.font = f_mono if c_i in (1, 6, 11) else f_data
            c.border = b_grid

    # Auto-size reasonable column widths across all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = max((len(str(cell.value or "")) for cell in col[:40]), default=10)
            ws.column_dimensions[col_letter].width = max(11, min(42, max_len + 3))

    wb.save(xlsx_path)


if __name__ == "__main__":
    main()
