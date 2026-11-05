# Paper Trail (A6) — rights and attribution

## Documents (all public record)

- **SEC / EDGAR filings and SEC enforcement documents** (47 of 57): works of the U.S. government or filings made public under the Exchange Act; sec.gov content is public domain. Includes WorldCom's Forms 10-Q/10-K/8-K as filed, the Special Investigative Committee report (Exhibit 99.1 to the June 9, 2003 Form 8-K), the SEC complaints, litigation releases, the SEC's brief and the court orders published by the SEC.
- **Department of Justice** (4): indictments and press statements published at justice.gov; U.S. government works.
- **Congress / GovInfo** (3): hearing records and a committee report; U.S. government works.
- **Bankruptcy Court Examiner reports** (2): court filings in In re WorldCom, Inc., No. 02-13533 (Bankr. S.D.N.Y.), hosted as PDFs by K&L Gates (files.klgates.com). Used as public court records; hosted copies cited by URL and hash.
- **United States v. Ebbers, 458 F.3d 110 (2d Cir. 2006)** (1): judicial opinion (public domain); text from Public.Resource.Org (law.resource.org).

Every document is cited by URL, access date (2026-10-14) and SHA-256 in `REGISTER.md` and `data/SHA256SUMS.txt`. Page images shown in the viewer are renders of the public PDFs; EDGAR pages are the filings' own text/HTML, including the Committee report's embedded exhibit images (`app/data/edgar-img/`).

## Fonts

- **Newsreader** (Production Type, Google Fonts) — SIL Open Font License 1.1.
- **IBM Plex Sans / IBM Plex Mono** (IBM) — SIL Open Font License 1.1.
Self-hosted as WOFF2 under `app/fonts/`.

## Code and tooling

- App: hand-written HTML/CSS/JS, no runtime dependencies.
- Build tools: Python 3 (requests, PyMuPDF for PDF text and page renders).
- QA and films only: Playwright (Chromium) for screenshots, verification crops and frame capture; ffmpeg (libx264) for encoding. None of this ships in the app.

## Not used

No third-party imagery, no stock photography, no generated images, no trademarks or logos, no soundtrack. No personal data beyond names in the public court record.
