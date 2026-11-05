"""Document register for Paper Trail (A6) — WorldCom, Inc. accounting fraud, 1999–2002.

Every entry is a public primary document. `kind` controls pagination:
  edgar-txt  : EDGAR SGML/plain-text submission, paginated at the filing's own <PAGE> markers
  edgar-html : EDGAR HTML document, paginated at the filing's own page-break markers
  pdf        : PDF, physical pages
  html       : HTML page without inherent pagination (located by numbered paragraph / heading)
"""

EDGAR = "https://www.sec.gov/Archives/edgar/data/723527/"

def edgar_txt(doc_id, title, acc, form, period, filed, role, issuer="WorldCom, Inc."):
    return dict(id=doc_id, title=title, kind="edgar-txt", form=form, period=period, filed=filed,
                url=f"{EDGAR}{acc}.txt", index_url=f"{EDGAR}{acc.replace('-','')}/{acc}-index.htm",
                accession=acc, issuer=issuer, role=role, authority="company filing")

DOCS = [
    # ---- Company filings, as originally filed (the "reported" track) ----
    edgar_txt("10q-1999q1", "Form 10-Q, quarter ended March 31, 1999 (as filed)", "0000950134-99-004355", "10-Q", "1999Q1", "1999-05-17", "reported", "MCI WORLDCOM, Inc."),
    edgar_txt("10q-1999q2", "Form 10-Q, quarter ended June 30, 1999 (as filed)", "0000950134-99-007487", "10-Q", "1999Q2", "1999-08-16", "reported", "MCI WORLDCOM, Inc."),
    edgar_txt("10q-1999q3", "Form 10-Q, quarter ended September 30, 1999 (as filed)", "0000931763-99-003243", "10-Q", "1999Q3", "1999-11-15", "reported", "MCI WORLDCOM, Inc."),
    edgar_txt("10k-1999", "Form 10-K, fiscal year 1999 (as filed, with Exhibit 13 annual report)", "0000931763-00-000735", "10-K", "1999FY", "2000-03-30", "reported", "MCI WORLDCOM, Inc."),
    edgar_txt("10q-2000q1", "Form 10-Q, quarter ended March 31, 2000 (as filed)", "0000931763-00-001358", "10-Q", "2000Q1", "2000-05-15", "reported"),
    edgar_txt("10q-2000q2", "Form 10-Q, quarter ended June 30, 2000 (as filed)", "0000931763-00-002037", "10-Q", "2000Q2", "2000-08-14", "reported"),
    edgar_txt("10q-2000q3", "Form 10-Q, quarter ended September 30, 2000 (as filed)", "0000931763-00-002561", "10-Q", "2000Q3", "2000-11-14", "reported"),
    edgar_txt("10k-2000", "Form 10-K405, fiscal year 2000 (as filed, with Exhibit 13 annual report)", "0000912057-01-505916", "10-K405", "2000FY", "2001-03-30", "reported"),
    edgar_txt("10q-2001q1", "Form 10-Q, quarter ended March 31, 2001 (as filed)", "0001005477-01-003304", "10-Q", "2001Q1", "2001-05-15", "reported"),
    edgar_txt("10q-2001q2", "Form 10-Q, quarter ended June 30, 2001 (as filed)", "0001005477-01-500685", "10-Q", "2001Q2", "2001-08-14", "reported"),
    edgar_txt("10q-2001q3", "Form 10-Q, quarter ended September 30, 2001 (as filed)", "0001005477-01-502009", "10-Q", "2001Q3", "2001-11-14", "reported"),
    edgar_txt("10k-2001", "Form 10-K405, fiscal year 2001 (as filed, with Exhibit 13 annual report)", "0001005477-02-001226", "10-K405", "2001FY", "2002-03-13", "reported"),
    edgar_txt("10q-2002q1", "Form 10-Q, quarter ended March 31, 2002 (as filed)", "0000912057-02-020812", "10-Q", "2002Q1", "2002-05-15", "reported"),
    edgar_txt("8k-2002-02-07", "Form 8-K, February 7, 2002 — company loans and guaranties for Bernard J. Ebbers", "0000912057-02-004505", "8-K", "2002-02-07", "2002-02-07", "disclosure"),
    # ---- Company disclosures of the fraud and the restatement (the "corrected" track) ----
    edgar_txt("8k-2002-06-25", "Form 8-K, June 25, 2002 — announcement of $3.8 billion of improperly capitalized line costs", "0000912057-02-025338", "8-K", "2002-06-25", "2002-06-26", "disclosure"),
    edgar_txt("8k-2002-07-21", "Form 8-K, July 21, 2002 — Chapter 11 petition", "0000909518-02-000544", "8-K", "2002-07-21", "2002-07-22", "disclosure"),
    edgar_txt("8k-2002-08-08", "Form 8-K, August 8, 2002 — additional $3.3 billion of improper accounting entries (1999–2002)", "0000893750-02-000472", "8-K", "2002-08-08", "2002-08-09", "disclosure"),
    edgar_txt("8k-2002-08-14", "Form 8-K, August 14, 2002 — sworn statements of the CEO and CFO under the SEC's Section 21(a)(1) order (filings for 1999–Q1 2002 not accurate)", "0000893750-02-000483", "8-K", "2002-08-14", "2002-08-15", "disclosure"),
    edgar_txt("8k-2002-11-26", "Form 8-K, November 26, 2002 — settlement with the SEC (permanent injunction, consent)", "0000893750-02-000724", "8-K", "2002-11-26", "2002-11-27", "disclosure"),
    edgar_txt("8k-2003-07-07", "Form 8-K, July 7, 2003 — court approval of the SEC civil penalty settlement", "0000893750-03-000372", "8-K", "2003-07-07", "2003-07-08", "disclosure"),
    edgar_txt("8k-2003-03-13", "Form 8-K, March 13, 2003 — expected goodwill and asset write-downs", "0000893750-03-000190", "8-K", "2003-03-13", "2003-03-14", "disclosure"),
    dict(id="beresford-report", title="Report of Investigation by the Special Investigative Committee of the Board of Directors of WorldCom, Inc. (Beresford, Katzenbach, Rogers; counsel Wilmer Cutler & Pickering; accounting advisors PricewaterhouseCoopers), March 31, 2003 — filed as Exhibit 99.1 to Form 8-K, June 9, 2003",
         kind="edgar-html", form="8-K EX-99.1", period="1999–2002", filed="2003-06-09", url=f"{EDGAR}000093176303001862/dex991.htm",
         index_url=f"{EDGAR}000093176303001862/0000931763-03-001862-index.htm", accession="0000931763-03-001862", issuer="WorldCom, Inc. (Special Investigative Committee)", role="investigation", authority="board special committee report (public, filed with SEC)"),
    dict(id="10k-2002", title="Form 10-K, fiscal year 2002 (filed March 12, 2004) — includes the restated 2000 and 2001 financial statements", kind="edgar-html", form="10-K", period="2002FY (restates 2000, 2001)", filed="2004-03-12",
         url=f"{EDGAR}000119312504039709/d10k.htm", index_url=f"{EDGAR}000119312504039709/0001193125-04-039709-index.htm", accession="0001193125-04-039709", issuer="WorldCom, Inc. (MCI)", role="restatement", authority="company restatement"),
    # ---- SEC enforcement record ----
    dict(id="sec-complaint-2002-06-26", title="SEC v. WorldCom, Inc. — Complaint, 02 Civ. 4963 (JSR) (S.D.N.Y. filed June 26, 2002)", kind="html", filed="2002-06-26", url="https://www.sec.gov/litigation/complaints/complr17588.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (allegations)"),
    dict(id="sec-amended-complaint-2002-11-05", title="SEC v. WorldCom, Inc. — First Amended Complaint (S.D.N.Y. filed November 5, 2002)", kind="html", filed="2002-11-05", url="https://www.sec.gov/litigation/complaints/comp17829.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (allegations); injunctive relief later entered by consent"),
    dict(id="sec-sworn-statement-2002-07-01", title="WorldCom, Inc. — Sworn Statement pursuant to Section 21(a)(1) order (July 1, 2002)", kind="html", filed="2002-07-01", url="https://www.sec.gov/news/wcreponse.htm", issuer="WorldCom, Inc.", role="disclosure", authority="company sworn statement to SEC"),
    dict(id="sec-sworn-statement-rev-2002-07-08", title="WorldCom, Inc. — Revised Sworn Statement pursuant to Section 21(a)(1) order (July 8, 2002)", kind="html", filed="2002-07-08", url="https://www.sec.gov/news/extra/wcresponserev.htm", issuer="WorldCom, Inc.", role="disclosure", authority="company sworn statement to SEC"),
    dict(id="sec-press-2002-94", title="SEC Press Release 2002-94: SEC Charges WorldCom with $3.8 Billion Fraud (June 26, 2002)", kind="html", filed="2002-06-26", url="https://www.sec.gov/news/press/2002-94.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17588", title="SEC Litigation Release No. 17588 (June 27, 2002) — complaint filed against WorldCom", kind="html", filed="2002-06-27", url="https://www.sec.gov/litigation/litreleases/lr17588.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17594", title="SEC Litigation Release No. 17594 (June 28, 2002) — temporary restraining order and monitor", kind="html", filed="2002-06-28", url="https://www.sec.gov/litigation/litreleases/lr17594.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17753", title="SEC Litigation Release No. 17753 (September 26, 2002) — SEC v. David F. Myers", kind="html", filed="2002-09-26", url="https://www.sec.gov/litigation/litreleases/lr17753.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17771", title="SEC Litigation Release No. 17771 (October 7, 2002) — SEC v. Buford Yates, Jr.", kind="html", filed="2002-10-07", url="https://www.sec.gov/litigation/litreleases/lr17771.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17783", title="SEC Litigation Release No. 17783 (October 10, 2002) — SEC v. Betty L. Vinson and Troy M. Normand", kind="html", filed="2002-10-10", url="https://www.sec.gov/litigation/litreleases/lr17783.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17829", title="SEC Litigation Release No. 17829 (November 5, 2002) — First Amended Complaint", kind="html", filed="2002-11-05", url="https://www.sec.gov/litigation/litreleases/lr17829.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-17866", title="SEC Litigation Release No. 17866 (November 26, 2002) — Judgment of Permanent Injunction against WorldCom", kind="html", filed="2002-11-26", url="https://www.sec.gov/litigation/litreleases/lr17866.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-18219", title="SEC Litigation Release No. 18219 (July 7, 2003) — court approves $750 million penalty settlement", kind="html", filed="2003-07-07", url="https://www.sec.gov/litigation/litreleases/lr18219.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-18605", title="SEC Litigation Release No. 18605 (March 2, 2004) — SEC v. Scott D. Sullivan", kind="html", filed="2004-03-02", url="https://www.sec.gov/litigation/litreleases/lr18605.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-lr-19301", title="SEC Litigation Release No. 19301 (July 13, 2005) — SEC v. Bernard J. Ebbers", kind="html", filed="2005-07-13", url="https://www.sec.gov/litigation/litreleases/lr19301.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC release"),
    dict(id="sec-complaint-myers", title="SEC v. David F. Myers — Complaint (S.D.N.Y. September 26, 2002)", kind="html", filed="2002-09-26", url="https://www.sec.gov/litigation/complaints/comp17753.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (settled by consent)"),
    dict(id="sec-complaint-yates", title="SEC v. Buford Yates, Jr. — Complaint (S.D.N.Y. October 7, 2002)", kind="html", filed="2002-10-07", url="https://www.sec.gov/litigation/complaints/comp17771.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (settled by consent)"),
    dict(id="sec-complaint-vinson-normand", title="SEC v. Betty L. Vinson and Troy M. Normand — Complaint (S.D.N.Y. October 10, 2002)", kind="html", filed="2002-10-10", url="https://www.sec.gov/litigation/complaints/comp17783.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (settled by consent)"),
    dict(id="sec-complaint-sullivan", title="SEC v. Scott D. Sullivan — Complaint (S.D.N.Y. March 2, 2004)", kind="html", filed="2004-03-02", url="https://www.sec.gov/litigation/complaints/comp18605.htm", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (settled by consent)"),
    dict(id="sec-complaint-ebbers", title="SEC v. Bernard J. Ebbers — Complaint (S.D.N.Y. July 13, 2005)", kind="pdf", filed="2005-07-13", url="https://www.sec.gov/litigation/complaints/comp19301.pdf", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC pleading (settled by consent)"),
    dict(id="sdny-permanent-injunction-2002-11-26", title="SEC v. WorldCom — Judgment of Permanent Injunction (S.D.N.Y. November 26, 2002)", kind="pdf", filed="2002-11-26", url="https://www.sec.gov/spotlight/worldcom/wcjudg112602.pdf", issuer="U.S. District Court, S.D.N.Y. (Rakoff, J.)", role="court", authority="court judgment"),
    dict(id="sdny-opinion-2003-07-07", title="SEC v. WorldCom, Inc., 273 F. Supp. 2d 431 — Opinion and Order approving the $750 million civil penalty (S.D.N.Y. July 7, 2003)", kind="pdf", filed="2003-07-07", url="https://www.sec.gov/litigation/complaints/courtorder070703.pdf", issuer="U.S. District Court, S.D.N.Y. (Rakoff, J.)", role="court", authority="court opinion"),
    dict(id="sdny-final-judgment-2003-07-07", title="SEC v. WorldCom — Final Judgment as to Monetary Relief (S.D.N.Y. July 7, 2003)", kind="pdf", filed="2003-07-07", url="https://www.sec.gov/spotlight/worldcom/wcjudg070703.pdf", issuer="U.S. District Court, S.D.N.Y. (Rakoff, J.)", role="court", authority="court judgment"),
    dict(id="sec-brief-2003-06-06", title="SEC Memorandum in Support of Proposed Settlement of Claim for Civil Penalty (S.D.N.Y. June 6, 2003)", kind="pdf", filed="2003-06-06", url="https://www.sec.gov/spotlight/worldcom/wcombrief060603.pdf", issuer="U.S. Securities and Exchange Commission", role="enforcement", authority="SEC court filing"),
    # ---- Criminal record ----
    dict(id="doj-indictment-sullivan-myers-2002-08", title="United States v. Scott D. Sullivan and Buford Yates, Jr. — Indictment (S.D.N.Y., 02 Cr. 1144, August 2002)", kind="pdf", filed="2002-08-28", url="https://www.justice.gov/archive/dag/cftf/chargingdocs/worldcomindictment.pdf", issuer="U.S. Department of Justice (S.D.N.Y.)", role="criminal", authority="grand jury indictment"),
    dict(id="doj-indictment-ebbers-2004", title="United States v. Bernard J. Ebbers — Superseding Indictment S3 02 Cr. 1144 (BSJ) (S.D.N.Y. 2004; the copy published by the Department of Justice carries no filing date)", kind="pdf", filed=None, url="https://www.justice.gov/archive/dag/cftf/chargingdocs/ebberss504.pdf", issuer="U.S. Department of Justice (S.D.N.Y.)", role="criminal", authority="grand jury indictment"),
    dict(id="doj-ag-statement-2005-03-15", title="Statement of Attorney General Alberto R. Gonzales on the conviction of Bernard Ebbers (March 15, 2005)", kind="html", filed="2005-03-15", url="https://www.justice.gov/archive/opa/pr/2005/March/05_ag_122.htm", issuer="U.S. Department of Justice", role="criminal", authority="DOJ release"),
    dict(id="doj-sdny-ebbers-case", title="U.S. Attorney, S.D.N.Y. — United States v. Bernard Ebbers (case page: 25-year sentence imposed July 13, 2005)", kind="html", filed="2005-07-13", url="https://www.justice.gov/usao-sdny/united-states-v-bernard-ebbers", issuer="U.S. Department of Justice (S.D.N.Y.)", role="criminal", authority="DOJ case page"),
    dict(id="ca2-ebbers-2006", title="United States v. Ebbers, 458 F.3d 110 (2d Cir. July 28, 2006) — conviction and sentence affirmed", kind="html", filed="2006-07-28", url="https://law.resource.org/pub/us/case/reporter/F3/458/458.F3d.110.05-4059-.html", issuer="U.S. Court of Appeals for the Second Circuit", role="court", authority="appellate opinion (public domain text, Public.Resource.Org)"),
    # ---- Bankruptcy examiner and Congress ----
    dict(id="thornburgh-1", title="First Interim Report of Dick Thornburgh, Bankruptcy Court Examiner, In re WorldCom, Inc., Case No. 02-13533 (AJG) (Bankr. S.D.N.Y. November 4, 2002)", kind="pdf", filed="2002-11-04", url="https://files.klgates.com/files/upload/worldcom_examiner_report_firstinterim.pdf", issuer="Bankruptcy Court Examiner (Dick Thornburgh)", role="investigation", authority="court-appointed examiner report"),
    dict(id="thornburgh-2", title="Second Interim Report of Dick Thornburgh, Bankruptcy Court Examiner (Bankr. S.D.N.Y. June 9, 2003)", kind="pdf", filed="2003-06-09", url="https://files.klgates.com/files/upload/worldcom_report2.pdf", issuer="Bankruptcy Court Examiner (Dick Thornburgh)", role="investigation", authority="court-appointed examiner report"),
    dict(id="house-hearing-2002-07-08", title="Wrong Numbers: The Accounting Problems at WorldCom — Hearing before the House Committee on Financial Services, 107th Cong. (July 8, 2002), Serial No. 107-74", kind="pdf", filed="2002-07-08", url="https://www.govinfo.gov/content/pkg/CHRG-107hhrg83079/pdf/CHRG-107hhrg83079.pdf", issuer="U.S. House of Representatives", role="congress", authority="congressional hearing record"),
    dict(id="house-report-107-798", title="House Report 107-798 — Summary of Activities, Committee on Financial Services (incl. 'The WorldCom Fraud')", kind="pdf", filed="2003-01-02", url="https://www.govinfo.gov/content/pkg/CRPT-107hrpt798/pdf/CRPT-107hrpt798.pdf", issuer="U.S. House of Representatives", role="congress", authority="committee report"),
    dict(id="senate-hearing-2003-07-22", title="The WorldCom Case: Looking at Bankruptcy and Competition Issues — Hearing before the Senate Committee on the Judiciary, 108th Cong. (July 22, 2003), S. Hrg. 108-?", kind="pdf", filed="2003-07-22", url="https://www.govinfo.gov/content/pkg/CHRG-108shrg91564/pdf/CHRG-108shrg91564.pdf", issuer="U.S. Senate", role="congress", authority="congressional hearing record"),
]


SHORT = {
    "10q-1999q1": "Form 10-Q · Q1 1999", "10q-1999q2": "Form 10-Q · Q2 1999", "10q-1999q3": "Form 10-Q · Q3 1999", "10k-1999": "Form 10-K · FY 1999",
    "10q-2000q1": "Form 10-Q · Q1 2000", "10q-2000q2": "Form 10-Q · Q2 2000", "10q-2000q3": "Form 10-Q · Q3 2000", "10k-2000": "Form 10-K405 · FY 2000",
    "10q-2001q1": "Form 10-Q · Q1 2001", "10q-2001q2": "Form 10-Q · Q2 2001", "10q-2001q3": "Form 10-Q · Q3 2001", "10k-2001": "Form 10-K405 · FY 2001",
    "10q-2002q1": "Form 10-Q · Q1 2002", "8k-2002-02-07": "Form 8-K · Feb 7, 2002 (Ebbers loans)", "8k-2002-06-25": "Form 8-K · June 25, 2002 ($3.8bn)",
    "8k-2002-07-21": "Form 8-K · July 21, 2002 (Chapter 11)", "8k-2002-08-08": "Form 8-K · Aug 8, 2002 (+$3.3bn)", "8k-2002-08-14": "Form 8-K · Aug 14, 2002 (sworn statements)",
    "8k-2002-11-26": "Form 8-K · Nov 26, 2002 (SEC settlement)", "8k-2003-07-07": "Form 8-K · July 7, 2003 (penalty approved)", "8k-2003-03-13": "Form 8-K · Mar 13, 2003 (write-offs)",
    "beresford-report": "Special Investigative Committee report (2003)", "10k-2002": "Form 10-K · FY 2002 (restated 2000–01)",
    "sec-complaint-2002-06-26": "SEC complaint · June 26, 2002", "sec-amended-complaint-2002-11-05": "SEC First Amended Complaint · Nov 5, 2002",
    "sec-sworn-statement-2002-07-01": "WorldCom sworn statement to SEC · July 1, 2002", "sec-sworn-statement-rev-2002-07-08": "WorldCom revised sworn statement · July 8, 2002",
    "sec-press-2002-94": "SEC press release 2002-94", "sec-lr-17588": "SEC Lit. Rel. 17588", "sec-lr-17594": "SEC Lit. Rel. 17594", "sec-lr-17753": "SEC Lit. Rel. 17753 (Myers)",
    "sec-lr-17771": "SEC Lit. Rel. 17771 (Yates)", "sec-lr-17783": "SEC Lit. Rel. 17783 (Vinson, Normand)", "sec-lr-17829": "SEC Lit. Rel. 17829", "sec-lr-17866": "SEC Lit. Rel. 17866",
    "sec-lr-18219": "SEC Lit. Rel. 18219", "sec-lr-18605": "SEC Lit. Rel. 18605 (Sullivan)", "sec-lr-19301": "SEC Lit. Rel. 19301 (Ebbers)",
    "sec-complaint-myers": "SEC v. Myers · complaint", "sec-complaint-yates": "SEC v. Yates · complaint", "sec-complaint-vinson-normand": "SEC v. Vinson & Normand · complaint",
    "sec-complaint-sullivan": "SEC v. Sullivan · complaint", "sec-complaint-ebbers": "SEC v. Ebbers · complaint (2005)",
    "sdny-permanent-injunction-2002-11-26": "S.D.N.Y. · permanent injunction (Nov 26, 2002)", "sdny-opinion-2003-07-07": "S.D.N.Y. · Rakoff opinion (July 7, 2003)",
    "sdny-final-judgment-2003-07-07": "S.D.N.Y. · final judgment, monetary relief", "sec-brief-2003-06-06": "SEC settlement memorandum (June 6, 2003)",
    "doj-indictment-sullivan-myers-2002-08": "U.S. v. Sullivan & Yates · indictment (2002)", "doj-indictment-ebbers-2004": "U.S. v. Ebbers · superseding indictment",
    "doj-ag-statement-2005-03-15": "DOJ · Attorney General statement on Ebbers verdict", "doj-sdny-ebbers-case": "DOJ S.D.N.Y. · U.S. v. Ebbers case page", "ca2-ebbers-2006": "2d Cir. · United States v. Ebbers (2006)",
    "thornburgh-1": "Examiner Thornburgh · First Interim Report", "thornburgh-2": "Examiner Thornburgh · Second Interim Report",
    "house-hearing-2002-07-08": "House hearing · \"Wrong Numbers\" (July 8, 2002)", "house-report-107-798": "House Report 107-798", "senate-hearing-2003-07-22": "Senate Judiciary hearing (July 22, 2003)",
}
KIND_LABEL = {"edgar-txt": "EDGAR text filing, as filed", "edgar-html": "EDGAR HTML filing, as filed", "pdf": "PDF, physical pages", "html": "HTML document"}
for _d in DOCS:
    _d["short"] = SHORT.get(_d["id"], _d["title"][:40])
    _d["kind_label"] = KIND_LABEL[_d["kind"]]
