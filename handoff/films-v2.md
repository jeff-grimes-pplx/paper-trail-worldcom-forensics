# films-v2 — Paper Trail, the 45-second films (standard v2.1, October 17, 2026)

Two films cut from the same 2,700 captured frames: `paper-trail-45s-captioned.mp4` (the release candidate, section 7 captions burned in) and `paper-trail-45s.mp4` (clean), each with a crf 10 master. One continuous frame-stepped capture of the deployed app at commit `b3941e7` (bundle hash `2e73305a70b8e12d573b066a41402ae405d432ba7bde3f2dd0d29fc898a6ac21`, asset `ff234758-ad1c-4645-aea3-e3d4e3a664ad`, unchanged since the v2 pass and frozen), re-planned for v2.1: shots are joined by hard cuts between static framings, every click is at 4.5×, the back half restructures the Q2 2001 sequence as the brief's shot list asks (second quarter clicked and its two source pages shown), and the caption band (rows 0–239) carries only flat fills and hairlines of the interface whenever a caption is visible. Independent review of the captioned film against sections 3 and 7: PASS — no frame range breaks a rule in §3 or §7 (review-v21.md, 2026-10-17 10:27 UTC): zero breaks, six marginal items B1–B6 measured at or near a limit, five disclosure items C1–C5, all folded into these receipts (qa/film45/review-v21.md).

## 1. ffprobe
| file | codec/profile@level | width×height | r_frame_rate | avg_frame_rate | nb_frames | duration | nb_streams | pix_fmt |
|---|---|---|---|---|---|---|---|---|
| paper-trail-45s-captioned.mp4 | h264 High@42 | 1920×1080 | 60/1 | 60/1 | 2700 | 45.000000 s | 1 | yuv420p |
| paper-trail-45s.mp4 | h264 High@42 | 1920×1080 | 60/1 | 60/1 | 2700 | 45.000000 s | 1 | yuv420p |
| paper-trail-45s-master.mp4 | h264 High 4:4:4 Predictive@50 | 1920×1080 | 60/1 | 60/1 | 2700 | 45.000000 s | 1 | yuv444p |
| paper-trail-45s-captioned-master.mp4 | h264 High 4:4:4 Predictive@50 | 1920×1080 | 60/1 | 60/1 | 2700 | 45.000000 s | 1 | yuv444p |

No audio stream in any file (nb_streams = 1, the single stream is video). Encoder: ffmpeg libx264, preset slow, `-framerate 60 -r 60 -an`; films crf 17 yuv420p high@4.2 `-movflags +faststart`; masters crf 10 yuv444p. The two films are separate encodes of separate frame sets (clean PNGs; captioned PNGs = clean PNGs with rows 0–299 composited), so they are separate assets with their own hashes.

## 2. SHA-256 and bytes
| file | bytes | SHA-256 | asset |
|---|---|---|---|
| paper-trail-45s-captioned.mp4 (captioned release candidate (crf 17, yuv420p, +faststart)) | 3,559,441 | `991f90fab32df81281af6399d735285cc473239651547c8dba30d0ded3996091` | asset `48ef1046-d4b0-4ffa-8505-f41c8de2ec48` (“Paper Trail — 45 s film, captioned (release candidate)”) |
| paper-trail-45s.mp4 (clean film (crf 17, yuv420p, +faststart)) | 2,577,642 | `e116277514230937fc146a52e039828c5b0b1ddeac64aa8ae8231030e0f768b0` | asset `ee54671a-6512-4f63-a32a-b36428d949dd` (“Paper Trail — 45 s film”, new version; v3 was `7098c2db-5f0b-4a0c-a67c-9b900b57a6c8`) |
| paper-trail-45s-master.mp4 (clean master (crf 10, yuv444p)) | 3,911,023 | `50cd79bb47edfa9388a855f372423c8f41adc6bf87858ba62c9ec79709890f1f` | asset `d1de87ee-9e0d-4707-a867-0438ac8d4b26` (“Paper Trail — 45 s clean master”, new version; v3 was `de53fb5c-5140-4c20-a1f1-6511fa9546a7`) |
| paper-trail-45s-captioned-master.mp4 (captioned master (crf 10, yuv444p; QA reference, not an asset)) | 5,736,689 | `8d4e83b138b88181ec819c297b75caabccc9e070a342cc5f172d88276655f3d4` | not shared; QA reference (`qa/film/out/paper-trail-45s-captioned-master.mp4`) |

## 3. Beat list, cuts, camera moves and holds
Times are frame/60 (frame 0 = 0.000 s). Zoom is the camera factor relative to the 1600×900 CSS viewport (output scale = 1.2 × zoom; 1× = the whole viewport fills the 1920×1080 frame). Camera moves and pointer glides use minimum-jerk (quintic, 10t³−15t⁴+6t⁵) in-out easing, zoom interpolated in log space; a move samples the quintic on [ε, 1−ε] with the smallest ε at which its first and last frames still displace content by ≥ 1.5 output px (the CDP clip snaps to device pixels, so an untrimmed ease tail would repeat frames). Shots change by hard cuts between static framings (§5.5: cut-point PSNR below); no dissolves, fades or cards.

| # | start–end s | frames | subject | zoom | camera | pointer | band content (clean film) |
|---|---|---|---|---|---|---|---|
| 1 | 0.000–0.500 | 0–29 | chart at 3.5×: both tracks, Q2 2000–Q1 2002; the last five quarters still coincident (reveal pending) | 3.5× | static 0.5 s | parked below the plot, outside the window | chart-wrap top border (hairline) and the 5 $bn gridline |
| 2 | 0.500–1.600 | 30–95 | product reveal: Q1 2001–Q1 2002 lift to their reconstructed values (static camera) | 3.5× | static | parked, outside the window | — |
| 3 | 1.600–4.000 | 96–239 | hold on the two tracks | 3.5× | static 2.4 s | parked, outside the window | — |
| 4 | 4.000–5.000 | 240–299 | push in to the Q1 2001 point at 4.5×; the pointer rises into the Q1 2001 hit target from below | 3.5× | push-in 1.0 s minimum-jerk | eased approach from below the plot; hotspot 23 CSS px right of the dot, clear of the labels; the tooltip appears on entry | — |
| 5 | 5.000–8.000 | 300–479 | dwell on Q1 2001 with the product tooltip (Q1 2001 · Line costs, reported $4,108m, corrected $4,879m) | 4.5× | static 3.0 s | still, hover state visible | — |
| 6 | 8.000–10.850 | 480–650 | click Q1 2001: labels 4,108 reported · gap 771 · 4,879 corrected appear; both source pages open (off-camera) | 4.5× | static 2.65 s | real click; remains parked clear of the labels | — |
| 7 | 10.850–13.650 | 651–818 | 10-Q source identity: Form 10-Q · Q1 2001, page 4 of 59 (p. 4), banner Line costs · $4,108 million | 8.74× | cut; static 3.0 s | parked on the chart, outside this window | viewer top rule (hairline) and the head background |
| 8 | 13.650–16.700 | 819–1001 | 10-Q source figure: the filing's own row, 3,733 (2000) and 4,108 (2001) highlighted | 7.4× | cut; static 3.05 s | outside this window | blank table rows above the highlighted row |
| 9 | 16.700–21.200 | 1002–1271 | Committee passage (viewer p. 110, printed p. 105): "...reduced line costs by a total of $771 million." | 7.6× | cut; static 4.5 s | outside this window | banner/head background, the head rule (hairline) and the body's top padding |
| 10 | 21.200–25.733 | 1272–1543 | chart at 4.5× with the Q1 2001 labels: 4,879 · gap 771 · 4,108 (the arithmetic) | 4.5× | cut; static 4.5 s | parked where it clicked, clear of the labels | chart-wrap top border (hairline) |
| 11 | 25.733–26.533 | 1544–1591 | pan right at 4.5× while the pointer glides level to the Q2 2001 hit target (its tooltip appears on entry); the Q1 labels stay in view | 4.5× | pan 0.8 s minimum-jerk (cx 600 → 628, zoom and top unchanged) | eased level glide from the Q1 2001 hotspot to the Q2 2001 hotspot, between the two Q2 points, right of the Q1 labels | — |
| 12 | 26.533–27.833 | 1592–1669 | dwell on Q2 2001 with the product tooltip (Q2 2001 · Line costs, reported $3,730m, corrected $4,340m) | 4.5× | static 1.3 s | still, hover state visible | — |
| 13 | 27.833–28.033 | 1670–1681 | click Q2 2001: labels 3,730 reported · gap 610 · 4,340 corrected; both source pages change (off-camera) | 4.5× | static (holds to the cut, 2.17 s after the press) | real click; still while the dismissed tooltip fades (7 frames) | — |
| 14 | 28.033–28.633 | 1682–1717 | the pointer slides straight down inside the Q2 2001 column and parks below the new labels (camera static) | 4.5× | static | eased glide down (ease-tail trimmed so every frame moves the arrow ≥ 2 px); same hit column, so the dismissed tooltip does not reopen | — |
| 15 | 28.633–30.000 | 1718–1799 | hold at 4.5× with the Q2 2001 labels 4,340 · gap 610 · 3,730; the pointer parked below them | 4.5× | static 1.37 s | parked below the labels | — |
| 16 | 30.000–33.433 | 1800–2005 | Q2 10-Q source figure: the filing's row 3,776 · 3,730 · 7,509 with 3,730 highlighted (page 4 of 209) | 8.4× | cut; static 3.4 s | outside this window | blank table rows above the highlighted row |
| 17 | 33.433–37.000 | 2006–2219 | Committee passage (viewer p. 113, printed p. 108): heading "b. Second Quarter 2001" and "...reduced line costs by a total of $610 million" | 8.6× | cut; static 3.6 s | outside this window | page background between two paragraphs |
| 18 | 37.000–45.000 | 2220–2699 | final hold: chart at 3.5× with both tracks and the Q2 2001 labels 4,340 · gap 610 · 3,730 | 3.5× | cut; static 8.0 s (final payoff) | parked where it clicked, clear of the labels | chart-wrap top border (hairline) and the 5 $bn gridline |

Hard cuts (frame f = first frame of the new shot; PSNR Y of the encoded frame against its own PNG at f−1, f, f+1 — the encode does not smear the cut):

| cut | frame | t s | from → to | captioned film PSNR Y dB (f−1, f, f+1) | clean film | caption state at the cut |
|---|---|---|---|---|---|---|
| B1 10-Q header | 651 | 10.850 | 4.5× → 8.74× | 54.93, 55.91, 54.52 | 57.16, 56.96, 57.88 | caption 4 fading in (frame 1 of 12) |
| B2 10-Q row | 819 | 13.650 | 8.74× → 7.4× | 54.18, 53.38, 53.38 | 58.00, 58.45, 58.76 | caption 4 fully opaque |
| C Committee passage | 1002 | 16.700 | 7.4× → 7.6× | 57.73, 51.94, 52.26 | 58.97, 52.28, 52.96 | caption 5 fading in (frame 1 of 12) |
| D1 chart with the Q1 2001 labels | 1272 | 21.200 | 7.6× → 4.5× | 50.76, 54.83, 55.39 | 51.41, 55.41, 57.08 | caption 6 fading in (frame 1 of 12) |
| E1 Q2 10-Q row | 1800 | 30.000 | 4.5× → 8.4× | 55.85, 55.91, 54.98 | 56.96, 56.31, 56.81 | caption 8 fading in (frame 1 of 12) |
| E2 Committee passage, second quarter | 2006 | 33.433 | 8.4× → 8.6× | 56.53, 55.03, 53.96 | 56.98, 55.21, 55.54 | caption 9 fading in (frame 1 of 12) |
| F chart with the Q2 2001 labels | 2220 | 37.000 | 8.6× → 3.5× | 53.36, 56.19, 54.52 | 55.70, 57.00, 57.21 | caption 10 fading in (frame 1 of 12) |

Every cut lands inside a caption hold or exactly at a caption hand-off frame (captions 4, 5, 6, 8, 9 and 10 start their fade-in on the cut frame itself: the new shot and the new caption arrive together, and the outgoing caption's fade-out ran over the last 12 frames of the previous static shot). No caption changes during a camera move: the moves are frames 240–299, 1544–1591, the hand-offs 212–235, 433–456, 639–662, 990–1013, 1260–1283, 1503–1526, 1788–1811, 1994–2017, 2208–2231, 2448–2471.

Camera moves (from the per-frame trace):

| # | kind | frames | duration s | zoom from→to | cx from→to (css) | ε | peak speed note |
|---|---|---|---|---|---|---|---|
| 1 | push-in | 240–299 | 1.000 | 3.50→4.50 | 590.0→600.0 | 0.1083 | Q1 2001 point + tooltip at 4.5× |
| 2 | pan | 1544–1591 | 0.800 | 4.50→4.50 | 600.0→628.0 | 0.1823 | Q2 2001 point + tooltip at 4.5× |

Measured on the trace (v first/last = first and last per-frame velocity relative to the move's peak; peak at 0.5 = centre): move 1 push-in 1.000 s, v 0.166/0.166, peak at 0.51; move 2 pan 0.800 s, v 0.377/0.377, peak at 0.47.

Push-ins 1.000 s (rule 0.8–1.5 s); pans 0.800 s (rule ≤ 1.2 s). One subject per move: the push-in travels from the whole chart to the Q1 2001 point with the pointer arriving on the same frame; the pan slides one quarter to the right at constant zoom with the pointer gliding to the Q2 2001 point. Settles: the push-in ends at frame 300 and the Q1 click is at 480 (3.00 s later); the pan ends at 1592 and the Q2 click is at 1670 (1.30 s); the shortest camera-static gap before any cut is 2.80 s.

Rendered motion against the trace (reviewer measurements, `review-v21.md` B1–B2): the camera trace is a trimmed quintic (max residual 0.03 CSS px), but the CDP clip origin snaps to device pixels, so rendered content advances in integer steps that alternate around the eased path — during the push-in the 5 $bn gridline moves −2.1, +1.0, +2.9, +0.1, +3.1, −1.1 … px per frame (residual ≤ 3.3 px peak to peak); during the pan the chart translation is monotone in integer steps of 1–4 px. The Q2 2001 tooltip opens on pointer entry during the pan (pair 1557, mean |Δ| 10.3, the peak of a bell-shaped run 5.8 → 10.3 → 5.4, not an isolated pop) and follows the pointer in integer CSS px: its on-screen left edge steps 1 and 7 output px alternately over frames 1560–1575 and reverses by ±3 px seven times over 1580–1591 as the pointer decelerates against the still-moving camera. Both pass §3 as written (0 duplicate pairs, no cadence, no isolated pop); they are the visible cost of frame-stepped CDP clipping and are disclosed rather than smoothed. Smallest fix if wanted: enter the hit target after the pan settles, or position the tooltip in fractional CSS px.


Holds (camera static, from the trace; rule ≥ 1.2 s readable, final ≥ 2.0 s):

| hold | frames | duration s | what is read |
|---|---|---|---|
| 1–3 | 0–239 | 4.00 | chart at 3.5× → product reveal → hold on the two tracks |
| 4–6 | 299–650 | 5.87 | push in to the Q1 2001 point at 4.5×; the pointer rises into the Q1 2001 hit target from below → dwell on Q1 2001 with the product tooltip (Q1 2001 · Line costs, reported $4,108m, corrected $4,879m) → click Q1 2001 |
| 7–7 | 651–818 | 2.80 | 10-Q source identity |
| 8–8 | 819–1001 | 3.05 | 10-Q source figure |
| 9–9 | 1002–1271 | 4.50 | Committee passage (viewer p. 110, printed p. 105) |
| 10–10 | 1272–1543 | 4.53 | chart at 4.5× with the Q1 2001 labels |
| 11–15 | 1591–1799 | 3.48 | pan right at 4.5× while the pointer glides level to the Q2 2001 hit target (its tooltip appears on entry); the Q1 labels stay in view → dwell on Q2 2001 with the product tooltip (Q2 2001 · Line costs, reported $3,730m, corrected $4,340m) → click Q2 2001 → the pointer slides straight down inside the Q2 2001 column and parks below the new labels (camera static) → hold at 4.5× with the Q2 2001 labels 4,340 · gap 610 · 3,730; the pointer parked below them |
| 16–16 | 1800–2005 | 3.43 | Q2 10-Q source figure |
| 17–17 | 2006–2219 | 3.57 | Committee passage (viewer p. 113, printed p. 108) |
| 18–18 | 2220–2699 | 8.00 | final hold |

Shortest hold 2.80 s; final hold 480 frames = 8.00 s on the chart at 3.5× with the Q2 2001 labels and the pointer parked below them; the last frame is a product state (no fade, no card). The 0.5 s opening hold (frames 0–29) precedes the product reveal and is not a reading hold.

Structure against the brief's shot list. Opening chart at 3.5× with the product reveal (both tracks), push-in to 4.5× and the Q1 2001 click; its two source pages (10-Q header with the page input, the 10-Q row with 4,108 highlighted; the Committee passage with $771 million highlighted); back to the chart for the Q1 arithmetic; the second quarter (Q2 2001) is reached by a pan and a second real click, then its two source pages (the 10-Q row with 3,730 highlighted; the Committee passage with $610 million highlighted); the final hold shows both tracks with the Q2 2001 labels. The v2 cut's repeat of the open-the-page loop for Q1 2002 is gone; the quarter card and the timeline are not framed in this cut because no framing of either keeps the caption band clear (§7 note below).

## 4. Native frames at every click and readout beat, with measured text heights
Frames are the native 1920×1080 PNGs copied to `qa/film45/beats-v21/` (clean). Heights are measured on the clean frames; the captioned frames are identical from row 300 down, and the measured elements whose ink reaches rows 240–299 (the 4,879 label from row 255 in beats 6 and 10, the 10-Q title from row 250 in beat 7, the Q2 highlight from row 254 in beat 16) are only darkened by the scrim tail there, never clipped by or inside the band (rows 0–239). Every height is measured on the native frame: ink pixels inside the element's box are grouped into connected components (glyphs), the baseline is the modal glyph bottom, "tallest glyph" is the tallest connected component standing on that baseline (a digit or capital; for `gap 610` the digits, since its lowercase letters share the baseline), "x-height" the tallest repeated baseline height ≥ 3 px below it (derived from the font ratio and marked * where the string has no lowercase). "em" is the rendered font size in output px (CSS px × 1.2 × zoom). Rule: U = UI text ≥ 28 px, R = readout number ≥ 32 px (this film's readouts are ≥ 46 px as asked). Frame 1682 is the first frame after the Q2 click settles; the pointer still sits on its click hotspot there and its arrow covers the last two digits of the gap pill, so that row measures only the visible `gap 6`; the pill is measured unobstructed 36 frames later (frame 1718). Pointer over the Q2 labels, disclosed: the arrow covers the gap-pill digits for frames 1674–1694 (0.35 s) and, on its way down, up to 18 % of the ink of the last digit of 3,730 for frames 1695–1709 (0.25 s); every Q2 label is unobstructed from frame 1710 to the cut at 1800 (1.50 s) and again for the whole final hold (2220–2699, 8.0 s). The 4,340 label is never covered.

| beat | frame | element | text | font | css px | zoom | em px | tallest glyph px | x-height px | rule | ok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 300 | tooltip quarter | `Q1 2001` | IBM Plex Sans | 12 | 4.5× | 64.8 | 47 | 33.4* | U ≥ 28 | yes |
| 5 | 300 | tooltip reported | `reported $4,108m` | IBM Plex Mono | 11 | 4.5× | 59.4 | 44 | 32 | U ≥ 28 | yes |
| 5 | 300 | tooltip corrected | `corrected $4,879m` | IBM Plex Mono | 11 | 4.5× | 59.4 | 44 | 32 | U ≥ 28 | yes |
| 6 | 502 | reported label | `4,108` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 6 | 502 | corrected label | `4,879` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 6 | 502 | gap pill | `gap 771` | IBM Plex Mono | 11 | 4.5× | 59.4 | 41 | 30.7* | R ≥ 32 | yes |
| 7 | 651 | page input | `4` | IBM Plex Mono | 11.5 | 8.74× | 120.6 | 85 | 62.2* | U ≥ 28 | yes |
| 7 | 651 | banner label | `Line costs` | IBM Plex Sans | 12 | 8.74× | 125.9 | 88 | 65.0* | U ≥ 28 | yes |
| 7 | 651 | banner value | `$4,108 million` | IBM Plex Mono | 12 | 8.74× | 125.9 | 94 | 89 | R ≥ 32 | yes |
| 8 | 819 | highlighted 4,108 | `4,108` | IBM Plex Mono | 11.1 | 7.4× | 98.6 | 72 | 50.9* | R ≥ 32 | yes |
| 9 | 1002 | highlighted 771 | `771` | Times New Roman | 13 | 7.6× | 118.6 | 79 | 53.1* | R ≥ 32 | yes |
| 10 | 1272 | reported label | `4,108` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 10 | 1272 | corrected label | `4,879` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 10 | 1272 | gap pill | `gap 771` | IBM Plex Mono | 11 | 4.5× | 59.4 | 41 | 30.7* | R ≥ 32 | yes |
| 12 | 1592 | tooltip quarter | `Q2 2001` | IBM Plex Sans | 12 | 4.5× | 64.8 | 47 | 33.4* | U ≥ 28 | yes |
| 12 | 1592 | tooltip reported | `reported $3,730m` | IBM Plex Mono | 11 | 4.5× | 59.4 | 44 | 32 | U ≥ 28 | yes |
| 12 | 1592 | tooltip corrected | `corrected $4,340m` | IBM Plex Mono | 11 | 4.5× | 59.4 | 44 | 32 | U ≥ 28 | yes |
| 13 | 1682 | reported label | `3,730` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 13 | 1682 | corrected label | `4,340` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 13 | 1682 | gap pill | `gap 610` | IBM Plex Mono | 11 | 4.5× | 59.4 | 42 | 30.7* | R ≥ 32 | yes |
| 15 | 1718 | reported label | `3,730` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 15 | 1718 | corrected label | `4,340` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 15 | 1718 | gap pill | `gap 610` | IBM Plex Mono | 11 | 4.5× | 59.4 | 43 | 30.7* | R ≥ 32 | yes |
| 16 | 1800 | highlighted 3,730 | `3,730` | IBM Plex Mono | 8.6 | 8.4× | 86.3 | 64 | 44.5* | R ≥ 32 | yes |
| 17 | 2006 | highlighted 610 | `610` | Times New Roman | 13 | 8.6× | 134.2 | 91 | 60.1* | R ≥ 32 | yes |
| 18 | 2220 | reported label | `3,730` | IBM Plex Mono | 11 | 3.5× | 46.2 | 35 | 23.8* | R ≥ 32 | yes |
| 18 | 2220 | corrected label | `4,340` | IBM Plex Mono | 11 | 3.5× | 46.2 | 34 | 23.8* | R ≥ 32 | yes |
| 18 | 2220 | gap pill | `gap 610` | IBM Plex Mono | 11 | 3.5× | 46.2 | 35 | 23.8* | R ≥ 32 | yes |

28 elements measured across 12 beat frames; 0 below threshold. Smallest em 46.2 px.

Payoff (rule ≥ 48 px). The film's payoff number is the product's 4,340, the Q2 2001 reconstruction, delivered by the product at 4.5× in frames 1674–1799 (em 59.4 px; digit ink 41–43 px), held 2.10 s and never covered by the pointer; the same class of figure (4,879) appears at the same size in frames 484–650 and 1272–1543. On the em reading, the standard's primary size measure with glyph height as the secondary check ("UI text ≥ 28 px tall (x-height ≥ 14 px)"; captions "64 px at 1080p (cap height ≈ 47 px, x-height ≈ 36 px)"), it passes (59.4 ≥ 48); on an ink-only reading the digits would be 41–43 px, stated here for the record. The captions (64 px, cap 47) are not offered as payoff-size evidence. The final 8 s hold is the brief's chart-with-both-lines shot at 3.5×, framed so both tracks and all eight quarters fit: there the Q2 2001 labels are readouts at em 46.2 px (tallest glyph 34–35 px, rule R ≥ 32), and the film's closing caption is 11 (57 documents, 3,119 pages, 453 values). Independent ruling: not a payoff-size breach (review-v21.md §3).

| click | frame | zoom | pointer dwell before (s) | camera settled before (s) | camera hold after (s) |
|---|---|---|---|---|---|
| Q1 2001 on the two-track chart | 480 | 4.50× | 3.017 | 3.017 | 2.833 |
| Q2 2001 on the two-track chart | 1670 | 4.50× | 1.333 | 1.317 | 2.150 |

Both clicks at 4.5× (rule ≥ 2.2×), camera settled ≥ 0.3 s and pointer dwelling ≥ 0.3 s before mousedown, camera held ≥ 0.6 s after it while the product draws the value labels and swaps both document panes (off-camera; the panes are shown by the following cuts). After the Q2 click the camera stays static to the cut; only the pointer moves (a 36-frame glide down the clicked column, frames 1682–1717, so it is clear of every label from frame 1710 to the cut).

## 5. Motion profile (clean frames; the captioned frames add only the caption fades in rows 0–299)
Metric: mean |Δ| between consecutive frames on a 160×90 grey (BOX) downscale, 0–255 scale. "Duplicate" = the standard's literal threshold, mean |Δ| < 0.02; "identical" = no pixel differs by more than 2/255 at full resolution. Moving windows = frame pairs where the trace shows the camera moving (c), the pointer moving with a static camera (p), the product reveal running (r), or a click consequence in flight (k = mousedown pair and the seven pairs from the mouseup through the 120 ms tooltip fade); hard cuts are their own category (intended, excluded from the pop test); everything else is an intended static hold. A pop is an isolated spike > 8/255 that is > 2.5× both neighbours.

Pairs 2699 · moving-window pairs 226 · duplicates in moving windows 0 (0.00 %, rule < 2 %) · identical full-res pairs in moving windows 0 (0.00 %) · max mean |Δ| 33.36/255 at pair 1272 · isolated pops > 8 outside cuts: 0 · sustained > 8 runs: 7 · cadence hits (2:2 / 3:3 / 5:5 inside moving windows): 0 by the duplicate threshold, 0 by identity.

| window category | pairs | dup < 0.02/255 | identical full-res | min / median / max mean \|Δ\| /255 |
|---|---|---|---|---|
| camera | 108 | 0 | 0 | 0.196 / 2.12 / 10.39 |
| pointer | 36 | 0 | 0 | 0.052 / 0.24 / 0.31 |
| reveal | 66 | 0 | 0 | 0.163 / 0.20 / 0.66 |
| scroll | 0 | 0 | 0 | 0.000 / 0.00 / 0.00 |
| click | 16 | 0 | 0 | 0.179 / 5.06 / 9.19 |
| cut | 7 | 0 | 0 | 24.636 / 27.85 / 33.36 |
| static | 2466 | 2466 | 2465 | 0.000 / 0.00 / 0.00 |

| move | frames | pairs | dup < 0.02 | identical | min / median / max mean \|Δ\| |
|---|---|---|---|---|---|
| camera | 239–299 | 60 | 0 | 0 | 0.196 / 1.99 / 8.67 |
| camera | 1543–1591 | 48 | 0 | 0 | 0.562 / 2.15 / 10.39 |
| pointer only (camera static): park below the Q2 2001 labels | 1682–1718 | 35 | 0 | 0 | 0.052 / 0.25 / 0.31 |

Hard cuts (pair f = frames f−1→f): f651 24.87 (1,547,332 changed px); f819 27.85 (1,872,352 changed px); f1002 31.17 (1,351,615 changed px); f1272 33.36 (1,770,052 changed px); f1800 27.55 (1,896,337 changed px); f2006 24.64 (1,003,643 changed px); f2220 28.31 (1,671,889 changed px).

Click consequences, pair by pair (pair f = frames f−1→f): the mousedown pair carries the pointer's 0.92 press scale; mousedown+4 is the mouseup, when the product dismisses its preview tooltip (120 ms fade, frame-stepped), draws the value labels and gap pill and swaps both document panes. Measured, not smoothed:
- Q1 2001 on the two-track chart, mousedown f480, max mean |Δ| 9.02/255: f480 0.18 (6,288 px), f481 0.00 (0 px), f482 0.00 (0 px), f483 0.00 (0 px), f484 2.43 (427,883 px), f485 4.63 (438,383 px), f486 7.59 (460,679 px), f487 9.02 (471,557 px), f488 8.01 (471,099 px), f489 5.38 (451,626 px), f490 2.20 (411,943 px), f491 0.00 (0 px), f492 0.00 (0 px)
- Q2 2001 on the two-track chart, mousedown f1670, max mean |Δ| 9.19/255: f1670 0.18 (6,421 px), f1671 0.00 (0 px), f1672 0.00 (0 px), f1673 0.00 (0 px), f1674 3.34 (471,646 px), f1675 4.73 (437,677 px), f1676 7.74 (461,786 px), f1677 9.19 (468,196 px), f1678 8.15 (468,536 px), f1679 5.48 (451,779 px), f1680 2.24 (410,495 px), f1681 0.00 (0 px), f1682 0.06 (4,949 px)

Reveal (the product's own chart animation driven 8→13 over 66 frames, camera static, pairs f30–f95): 66 pairs, 0 below 0.02/255, 0 byte-identical; changed full-resolution pixels per pair 4,682–33,399 (median 5,174).

Isolated single-frame changes > 8/255 outside cuts: none.
Sustained > 8 runs (eased moves, every pair inside them moving): f279–279, f281–281, f283–283, f285–285, f487–488, f1557–1559, f1677–1678.

Encode fidelity against the PNG frames (ffmpeg psnr filter, 4:4:4 comparison, all 2,700 frames; per-frame logs `qa/film45/psnr-<file>.log`):

| file | frames compared | PSNR Y mean dB | PSNR Y min dB (frame) | PSNR avg (Y,U,V) mean dB | PSNR avg min dB |
|---|---|---|---|---|---|
| paper-trail-45s-captioned.mp4 | 2700 | 53.33 | 44.86 (287) | 50.52 | 45.96 |
| paper-trail-45s.mp4 | 2700 | 55.83 | 45.05 (287) | 51.27 | 46.20 |
| paper-trail-45s-master.mp4 | 2700 | 62.04 | 49.76 (287) | 61.35 | 52.13 |
| paper-trail-45s-captioned-master.mp4 | 2700 | 59.43 | 49.57 (287) | 59.60 | 51.96 |

The films' lower (Y,U,V) averages come from 4:2:0 chroma subsampling on the red and blue text and lines (the mandated pix_fmt); the luma figures are the ones to compare with the 4:4:4 masters.

Per second (k = click-consequence pairs):

| s | pairs | dup < 0.02 | identical | moving pairs (c/p/r/k) | moving dup < 0.02 | moving identical | max mean \|Δ\| /255 | max changed px |
|---|---|---|---|---|---|---|---|---|
| 0 | 59 | 29 | 28 | 30 (r) | 0 | 0 | 0.56 | 27,188 |
| 1 | 60 | 24 | 24 | 36 (r) | 0 | 0 | 0.66 | 33,399 |
| 2 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 3 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 4 | 60 | 0 | 0 | 60 (c) | 0 | 0 | 8.67 | 310,549 |
| 5 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 6 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 7 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 8 | 60 | 52 | 52 | 8 (c) | 0 | 0 | 9.02 | 471,557 |
| 9 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 10 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 24.87 | 1,547,332 |
| 11 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 12 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 13 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 27.85 | 1,872,352 |
| 14 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 15 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 16 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 31.17 | 1,351,615 |
| 17 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 18 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 19 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 20 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 21 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 33.36 | 1,770,052 |
| 22 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 23 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 24 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 25 | 60 | 44 | 44 | 16 (c) | 0 | 0 | 10.39 | 585,867 |
| 26 | 60 | 28 | 28 | 32 (c) | 0 | 0 | 7.09 | 567,259 |
| 27 | 60 | 53 | 53 | 7 (c) | 0 | 0 | 9.19 | 471,646 |
| 28 | 60 | 23 | 23 | 37 (cp) | 0 | 0 | 2.24 | 410,495 |
| 29 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 30 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 27.55 | 1,896,337 |
| 31 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 32 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 33 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 24.64 | 1,003,643 |
| 34 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 35 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 36 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 37 | 60 | 59 | 59 | 0 (-) | 0 | 0 | 28.31 | 1,671,889 |
| 38 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 39 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 40 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 41 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 42 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 43 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |
| 44 | 60 | 60 | 60 | 0 (-) | 0 | 0 | 0.00 | 0 |

## 6. Pointer/input log and capture method
Full log: `qa/film45/input-45v21.json` — 17 events (camera moves, cuts, pointer glides, mousedown/mouseup, the reveal) with frame, time, from/to, frame counts and peak speed, plus a per-frame trace of pointer x/y (CSS px), camera z/cx/cy and the tooltip box for all 2,700 frames. Two glides ride camera moves (the pointer is never the only thing moving at 1× there); one glide runs with a static camera (frames 1682–1717, down the clicked Q2 2001 column, ease-tail trimmed so its first and last frames move the arrow ≥ 2 output px — see the pointer-only row in §5). Peak pointer speed over the film: 717 px/s at 1× capture scale (rule ≤ 1,200); every glide decelerates to its target. Event names below are the capture's own labels: "clear of the number labels" describes the hotspot against the labels present on arrival (the quarter's own labels do not exist until it is clicked); after the Q2 click the arrow at that hotspot covers part of the new gap pill until the park glide moves it below the labels (frames 1674–1709, §4).

| event | frame | t s | detail |
|---|---|---|---|
| reveal — last five quarters of the product reveal | 30 | 0.500 | product reveal hook PT.film.reveal 8 → 13 over 66 frames (frame-stepped) |
| camera — Q1 2001 point + tooltip at 4.5× | 240 | 4.000 | camera 3.50× (590, 248.07) → 4.50× (600, 219.5) over 60 frames, ε 0.1083 |
| pointer-move — Q1 2001 hit target, clear of the number labels | 240 | 4.000 | move [562.6, 540] → [562.6, 221] over 60 frames, peak 718 px/s @1×, camera moving |
| mousedown — Q1 2001 on the two-track chart | 480 | 8.000 | mousedown at CSS (562.6, 221) on `.pt[data-q="2001Q1"] .hit`, zoom 4.50× |
| mouseup — Q1 2001 on the two-track chart | 484 | 8.067 | mouseup at CSS (562.6, 221) on `.pt[data-q="2001Q1"] .hit` |
| cut — B1 10-Q header | 651 | 10.850 | cut to 8.74× (cx 948.53, cy 152.99) |
| cut — B2 10-Q row | 819 | 13.650 | cut to 7.40× (cx 1448.11, cy 340.31) |
| cut — C Committee passage | 1002 | 16.700 | cut to 7.60× (cx 1300.5, cy 692.71) |
| cut — D1 chart with the Q1 2001 labels | 1272 | 21.200 | cut to 4.50× (cx 600, cy 219.5) |
| camera — Q2 2001 point + tooltip at 4.5× | 1544 | 25.733 | camera 4.50× (600, 219.5) → 4.50× (628, 219.5) over 48 frames, ε 0.1823 |
| pointer-move — Q2 2001 hit target, clear of the number labels | 1544 | 25.733 | move [562.6, 221] → [605, 221] over 48 frames, peak 119 px/s @1×, camera moving |
| mousedown — Q2 2001 on the two-track chart | 1670 | 27.833 | mousedown at CSS (605, 221) on `.pt[data-q="2001Q2"] .hit`, zoom 4.50× |
| mouseup — Q2 2001 on the two-track chart | 1674 | 27.900 | mouseup at CSS (605, 221) on `.pt[data-q="2001Q2"] .hit` |
| pointer-move — park below the Q2 2001 labels | 1682 | 28.033 | move [605, 221] → [605, 279] over 36 frames, peak 218 px/s @1×, camera static, ε 0.1042 (first frame 2.19 px) |
| cut — E1 Q2 10-Q row | 1800 | 30.000 | cut to 8.40× (cx 1384.5, cy 340.57) |
| cut — E2 Committee passage, second quarter | 2006 | 33.433 | cut to 8.60× (cx 1072.6, cy 714.33) |
| cut — F chart with the Q2 2001 labels | 2220 | 37.000 | cut to 3.50× (cx 600, cy 248.07) |

**Capture method (disclosure).** A frame-stepped render, not a real-time screen recording; nothing here measures GPU, network or real-time performance:
- Chromium (Playwright, `channel: chromium`) at 1600×900 CSS px, device scale factor 1.2, serving a local copy of the deployed commit over HTTP. Before frame 0 the capture selects Q1 1999 through the product's own `PT.chart.select`, scrolls the analysis column (`#work-scroll`) 120 CSS px so the chart sits directly under its metric tabs, and sets the film hook `PT.film.reveal(8)` so quarters 1999–2000 are already reconstructed; none of this is filmed. Frames 30–95 drive `PT.film.reveal` 8 → 13 (the last five quarters lift to their reconstructed values) in 66 equal steps with the camera static.
- The page clock is installed and advanced exactly 1000/60 ms per frame (`page.clock.install` + `runFor`). CSS transitions do not run on that clock, so the document's animation timeline is paused through CDP (`Animation.setPlaybackRate 0`) and every running transition is seeked forward 1000/60 ms per frame (10 transitions started, 80 seeks).
- Each frame is one CDP `Page.captureScreenshot` with a clip equal to the camera window, rasterised at scale 1.2 × zoom: zoomed frames are native 1920×1080 renders, not upscales; cuts are changes of that clip between two consecutive frames. The window never leaves the page.
- The pointer is an SVG arrow drawn in the page at the real Playwright mouse position, composited from the same input log that drives the real `mousemove`/`mousedown`/`mouseup` events (minimum-jerk timing; 0.92 scale while pressed). Hover states, the tooltip, labels and page highlights are the product's own; the two document panes change on the real clicks and are shown by the following cuts.
- Document pages load from the local copy in real time between frames (the frame clock waits), so no loading state is filmed. No overlays, no added text in the clean film, no audio. The captioned film is the clean frames plus the section 7 compositing described in §7.

## 7. Captions (section 7 receipts; captioned film only)
### 7.1 Caption table
| # | text | chars | in (first visible) | first opaque | last opaque | out (last visible) | opaque s | reading budget s (0.065 × chars) | beat |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WorldCom’s fraud, rebuilt from 57 public documents. | 51 | 0 | 0 | 211 | 223 | 3.533 | 3.315 | A · chart at 3.5×, product reveal, hold |
| 2 | Blue is what WorldCom filed. Red is what it spent. | 50 | 224 | 236 | 432 | 444 | 3.283 | 3.250 | A · chart hold, push-in to 4.5×, start of the dwell |
| 3 | Click a quarter to open the source pages. | 41 | 445 | 457 | 638 | 650 | 3.033 | 2.665 | A · dwell with the tooltip, click Q1 2001, hold |
| 4 | The 10-Q reports line costs of $4,108 million. | 46 | 651 | 663 | 989 | 1001 | 5.450 | 2.990 | B1 10-Q header · B2 10-Q table row |
| 5 | Investigators found $771 million in hidden costs. | 49 | 1002 | 1014 | 1259 | 1271 | 4.100 | 3.185 | C · Committee passage |
| 6 | 4,108 reported plus 771 hidden is 4,879. | 40 | 1272 | 1284 | 1502 | 1514 | 3.650 | 2.600 | D1 · chart at 4.5×, Q1 2001 labels |
| 7 | A second quarter, Q2 2001, opens the same way. | 46 | 1515 | 1527 | 1787 | 1799 | 4.350 | 2.990 | D1 end · D2 pan + pointer glide, dwell, click Q2 2001, pointer parks, hold |
| 8 | Its 10-Q reports line costs of $3,730 million. | 46 | 1800 | 1812 | 1993 | 2005 | 3.033 | 2.990 | E1 · Q2 10-Q table row |
| 9 | Investigators found another $610 million hidden. | 48 | 2006 | 2018 | 2207 | 2219 | 3.167 | 3.120 | E2 · Committee passage, second quarter |
| 10 | 3,730 reported plus 610 hidden is 4,340. | 40 | 2220 | 2232 | 2447 | 2459 | 3.600 | 2.600 | F · chart at 3.5×, Q2 2001 labels |
| 11 | 57 documents, 3,119 pages, 453 values. | 38 | 2460 | 2472 | 2699 | 2699 | 3.800 | 2.470 | F · final hold |

11 captions; hand-offs at frames 224, 445, 651, 1002, 1272, 1515, 1800, 2006, 2220, 2460: the outgoing caption fades over 12 frames (X−12…X−1), the incoming fades in over the next 12 (X…X+11), transitional opacities (k + 0.5)/12, so there is no caption-free frame and every hand-off takes 0.4 s. Caption 1 is fully opaque from frame 0 (no fade-in); caption 11 holds unchanged to frame 2699. Shortest opaque duration 3.033 s (captions 3 and 8; rule ≥ 3.0 s, opener ≥ 3.5 s); every caption's opaque duration exceeds its reading budget (largest budget 3.315 s). Each caption is one line; longest 51 characters (rule ≤ 52). Figures: 57 documents, $4,108 million, $771 million, 4,879, Q2 2001, $3,730 million, $610 million, 4,340, 3,119 pages and 453 values are the product's own strings (chart labels, document-pane highlights and the register counts; receipts in §9 and HANDOFF.md).

Caption 11's three figures are not on screen in this cut: the product's masthead line sits above the window top in every beat (no 1× shot). Receipt: the product masthead at 1× (`qa/film45/v21probe/masthead-1x.png`, taken from the local copy of commit b3941e7 at 1600×900 CSS, DSF 1.2, by `qa/film45/masthead1x.js`) reads "57 documents · 3,119 pages" / "453 values · 379 page-cited · 47 events" (`#mast-meta`, set by main.js from data/register.json, 57 entries; data/pagecounts.json, pages summing to 3,119; data/ledger.json meta.entries 453). Wording: captions 3, 5 and 9 keep the parent's script wording for A6 (captions-v2.1.md: "Click a quarter to open the source pages.", "Investigators found …"), an imperative and two past-tense findings; the reviewer notes the literal deviation from "present tense" (review-v21.md C3) with the meaning correct.

### 7.2 Render metrics per caption (measured on the captioned PNG at the first fully opaque frame)
| # | first opaque frame | ink x0–x1 (width) | ink rows | ink centre y | cap height px (rows of "H"-class glyphs) | text band luminance clean → after scrim (rule ≤ 0.25) | max after scrim while opaque |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 145–1771 (1627) | 118–180 | 149.0 | 47 ([121, 167]) | 0.9330 → 0.2302 | 0.2302 |
| 2 | 236 | 202–1717 (1516) | 118–180 | 149.0 | 47 ([121, 167]) | 0.9329 → 0.2302 | 0.2377 |
| 3 | 457 | 327–1589 (1263) | 118–180 | 149.0 | 47 ([121, 167]) | 0.9593 → 0.2374 | 0.2374 |
| 4 | 663 | 274–1643 (1370) | 114–180 | 147.0 | 47 ([121, 167]) | 0.8752 → 0.2141 | 0.2458 |
| 5 | 1014 | 223–1696 (1474) | 114–180 | 147.0 | 47 ([121, 167]) | 0.9150 → 0.2248 | 0.2248 |
| 6 | 1284 | 351–1565 (1215) | 118–180 | 149.0 | 47 ([121, 167]) | 0.9593 → 0.2374 | 0.2374 |
| 7 | 1527 | 207–1708 (1502) | 121–180 | 150.5 | 47 ([121, 167]) | 0.9593 → 0.2374 | 0.2374 |
| 8 | 1812 | 292–1627 (1336) | 114–180 | 147.0 | 47 ([121, 167]) | 0.9876 → 0.2458 | 0.2458 |
| 9 | 2018 | 219–1699 (1481) | 114–180 | 147.0 | 47 ([121, 167]) | 0.9876 → 0.2458 | 0.2458 |
| 10 | 2232 | 338–1579 (1242) | 118–180 | 149.0 | 47 ([121, 167]) | 0.9329 → 0.2302 | 0.2302 |
| 11 | 2472 | 349–1567 (1219) | 121–180 | 150.5 | 47 ([121, 167]) | 0.9329 → 0.2302 | 0.2302 |

Treatment: Inter SemiBold (weight 600) 64 px, white #FFFFFF, no box/outline/pill, one line centred at x = 960; baseline y = 168 so the cap box sits at rows 121–167 (cap height 47 px, rule 45–49) and the ink of a mixed-case line is centred on y ≈ 149 (rule "line centre y = 150", applied to the ink extent of the line; measured ink centres 147–150.5; the cap box is rows 121–167, centre 144, baseline 168); max ink width 1627 px (rule ≤ 1,760; two lines never needed). Shadow: black 65 %, offset 0/+3, Gaussian blur radius 7 (PIL ImageFilter.GaussianBlur on the glyph mask). Scrim: black, full width, alpha 0.75 from y = 0 to 200 then linear to 0 at y = 300 (light interface, one value for the film), multiplied by the caption's opacity so it fades with the caption. Font file `qa/film45/fonts/Inter-SemiBold.ttf` (419,744 bytes, SHA-256 `78a843fade9d4612a5567302fb595b56976eb5fcebf4fea5a5912d638bafcde3`; SIL OFL licence alongside). Quantisation float32/floor, rows ≥ 300 copied from the clean frame untouched.

Compositing method: Python 3 / Pillow + NumPy, per frame, before the encode (`qa/film45/caption45v21.py`; schedule `captions-45v21.json` written by the capture script from the beat timeline): glyph mask rendered with `ImageDraw.text` (anchor "ms"), shadow = the mask offset +3 px and Gaussian-blurred, then scrim × α, shadow × 0.65 α, text × α applied in that order to rows 0–299 of the clean PNG in float32 and floored to 8 bit. Nothing is re-timed: the captions are scheduled on the beat boundaries the film already had.

### 7.3 Band-clear confirmation (rows 0–239 of the clean frames while a caption is visible)
Rule: while a caption is visible no interface text, pointer or subject may sit in the band. Reviewer ruling for this build: chart-wrap borders and dashed gridlines (hairlines of flat fills) may sit in the band; tick/axis text, data lines, dots, labels, the gap pill, hatch, the tooltip and the pointer may not. Measured on every frame (`qa/film45/bandcheck45v21.py`, results `bandcheck-45v21.{json,md}`): darkest luma in the band, rows with ink (luma < 200), rows below luma 150 (dark ink: text, data lines, pointer), rows with chroma > 40 (red/blue series, yellow highlights), glyph-like connected components (≥ 5 × 3 px dark blobs), the capcheck intrusion fraction (|px − median| > 24) and the pointer tip row.

| beat | frames | zoom | window top (css) | band = css px | darkest luma | ink rows (luma<200) | rows<150 (frames) | chroma>40 (frames) | glyph-like comps | capcheck intrusion max | subject top row (data colour / dark ink) | pointer tip min row | declared band content |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0–29 | 3.50× | 119.5 | 57.1 | 196 | 43–239 (197 rows) | 0 | 0 | 0 | 0.0175 | 260 / 260 | not in frame | chart-wrap top border (hairline) and the 5 $bn gridline |
| 2 | 30–95 | 3.50× | 119.5 | 57.1 | 196 | 43–239 (197 rows) | 0 | 0 | 0 | 0.0175 | 260 / 260 | not in frame |  |
| 3 | 96–239 | 3.50× | 119.5 | 57.1 | 196 | 43–239 (197 rows) | 0 | 0 | 0 | 0.0175 | 260 / 260 | not in frame |  |
| 4 | 240–299 | 3.50× | 119.5 | 57.1 | 196 | 41–239 (199 rows) | 0 | 0 | 0 | 0.0250 | 259 / 259 | 549 |  |
| 5 | 300–479 | 4.50× | 119.5 | 44.4 | 199 | 53–56 (4 rows) | 0 | 0 | 0 | 0.0208 | 322 / 322 | 550 |  |
| 6 | 480–650 | 4.50× | 119.5 | 44.4 | 199 | 53–56 (4 rows) | 0 | 0 | 0 | 0.0208 | 255 / 256 | 550 |  |
| 7 | 651–818 | 8.74× | 101.5 | 22.9 | 174 | 143–152 (10 rows) | 0 | 0 | 0 | 0.0417 | 783 / 250 | not in frame | viewer top rule (hairline) and the head background |
| 8 | 819–1001 | 7.40× | 279.5 | 27.0 | 251 | none | 0 | 0 | 0 | 0.0000 | 292 / 347 | not in frame | blank table rows above the highlighted row |
| 9 | 1002–1271 | 7.60× | 633.5 | 26.3 | 199 | 99–105 (7 rows) | 0 | 0 | 0 | 0.0375 | 730 / 289 | not in frame | banner/head background, the head rule (hairline) and the body's top padding |
| 10 | 1272–1543 | 4.50× | 119.5 | 44.4 | 199 | 53–56 (4 rows) | 0 | 0 | 0 | 0.0208 | 255 / 256 | 550 | chart-wrap top border (hairline) |
| 11 | 1544–1591 | 4.50× | 119.5 | 44.4 | 199 | 53–59 (7 rows) | 0 | 0 | 0 | 0.0209 | 255 / 256 | 550 |  |
| 12 | 1592–1669 | 4.50× | 119.5 | 44.4 | 199 | 53–59 (7 rows) | 0 | 0 | 0 | 0.0209 | 255 / 256 | 550 |  |
| 13 | 1670–1681 | 4.50× | 119.5 | 44.4 | 199 | 53–59 (7 rows) | 0 | 0 | 0 | 0.0209 | 255 / 256 | 550 |  |
| 14 | 1682–1717 | 4.50× | 119.5 | 44.4 | 199 | 53–59 (7 rows) | 0 | 0 | 0 | 0.0209 | 332 / 332 | 552 |  |
| 15 | 1718–1799 | 4.50× | 119.5 | 44.4 | 199 | 53–59 (7 rows) | 0 | 0 | 0 | 0.0209 | 332 / 332 | 863 |  |
| 16 | 1800–2005 | 8.40× | 287.0 | 23.8 | 251 | none | 0 | 0 | 0 | 0.0000 | 254 / 313 | not in frame | blank table rows above the highlighted row |
| 17 | 2006–2219 | 8.60× | 662.0 | 23.3 | 251 | none | 0 | 0 | 0 | 0.0000 | 522 / 262 | not in frame | page background between two paragraphs |
| 18 | 2220–2699 | 3.50× | 119.5 | 57.1 | 196 | 43–239 (197 rows) | 0 | 0 | 0 | 0.0175 | 260 / 260 | 671 | chart-wrap top border (hairline) and the 5 $bn gridline |

Summary: 2700 frames, caption opacity > 0 on 2700 (caption-free frames: 0). Darkest band luma 174/255 (frame 651). Frames with any band pixel below luma 150: 0; with data-series/highlight chroma in the band: 0; with glyph-like components: 0; pointer tip inside the band: 0. capcheck intrusion fraction max 0.0417 (frame 651), frames above 0.002: 2097.
Clean vs captioned PNG frames (2700 compared): rows >= 300 identical on every frame: True (max |Δ| 0); rows 240–299 only darkened by the scrim tail on every frame: True.

Per caption (frames with caption opacity > 0):

| # | visible frames | darkest band luma | ink rows (luma < 200) | frames with rows < 150 | frames with chroma > 40 | glyph-like comps (max) | pointer tip in band (frames) | band |
|---|---|---|---|---|---|---|---|---|
| 1 | 0–223 | 196 | 43–239 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 2 | 224–444 | 196 | 41–239 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 3 | 445–650 | 199 | 53–56 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 4 | 651–1001 | 174 | 143–152 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 5 | 1002–1271 | 199 | 99–105 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 6 | 1272–1514 | 199 | 53–56 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 7 | 1515–1799 | 199 | 53–59 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 8 | 1800–2005 | 251 | none | 0 | 0 | 0 | 0 | top (y 0–240) |
| 9 | 2006–2219 | 251 | none | 0 | 0 | 0 | 0 | top (y 0–240) |
| 10 | 2220–2459 | 196 | 43–239 | 0 | 0 | 0 | 0 | top (y 0–240) |
| 11 | 2460–2699 | 196 | 43–239 | 0 | 0 | 0 | 0 | top (y 0–240) |

Whole film: darkest band luma 174/255 (frame 651; the chart-wrap border is rgb(207,200,180) ≈ luma 201 and the dashed gridlines are lighter); frames with any band pixel below luma 150: 0; with series/highlight chroma in the band: 0; with glyph-like components: 0; pointer tip inside the band: 0. Bottom-band exceptions: none — every caption uses the top band. The capcheck intrusion fraction peaks at 0.0417 (frame 651) and exceeds 0.002 on 2097 frames: that is the hairline content listed in the "declared band content" column (border rows and the 5 $bn gridline on the chart shots, the table rule on the 10-Q shots), which the ruling allows; its rows and luma are reported above so the reviewer can confirm nothing else is there.

Band geometry, why the shots are framed as they are: the band is 200/zoom CSS px below the window top. The chart's metric-tab row ends at y = 118.6 CSS and the Q1 2001 corrected label's ink starts at y = 166.2, so with the window top at 119.5 the Q1 labels clear the band only at zoom ≥ 4.2; both clicks are therefore at 4.5× (Q1 label ink at output row 252 > 240). The Q2 2001 tooltip (182 × 79 CSS, anchored +14/+14 from the pointer) only fits inside a 4.5× window whose centre is panned 28 CSS px right (cx 628), hence the pan instead of a pull-back; after the Q2 click the camera stays at 4.5× and the pointer glides down out of the new labels. Q1 2002 and Q4 2001 cannot be clicked band-clear because their tooltips would spill into the document pane (x ≥ 845 CSS). The quarter card, the timeline and the method panel have interface text within 200/zoom CSS px of any top edge that frames them, so they are not in this cut; the final figures are on the chart labels instead (caption 10 is the same shape as caption 6).

### 7.4 Clean vs captioned, frame by frame
PNG frames (2700 compared): rows ≥ 300 identical on every frame: True (max |Δ| 0); rows 240–299 only ever darkened (scrim tail) on every frame: True. The encoded films differ from each other only through that compositing and the encoder's own block decisions; the parent's `capcheck.py` on the two encoded films:

```
frames=2700 plateau_textdiff=164.84 outside_band_meanabsdiff: mean=0.122 max=0.548
band(y0-240) intrusion fraction (|px-median|>24) in CLEAN: max=0.0417 at f651, frames>0.002: 2097
band luminance (clean, y110-190) min=0.878 max=0.988; after scrim 0.75 -> max=0.247; after 0.40 -> max=0.593
segments (on = opacity>50%): idx, first_on, last_on, frames, secs, first_full(>=95%), fade_in_frames(10->90%), fade_out_frames, gap_before
C1: on f0-f217 (218 fr, 3.63 s) full@f-1 fade_in=0 fade_out=11 gap_before(<50%)=0 fr (0.00 s)
C2: on f230-f439 (210 fr, 3.50 s) full@f285 fade_in=11 fade_out=10 gap_before(<50%)=12 fr (0.20 s)
C3: on f450-f645 (196 fr, 3.27 s) full@f457 fade_in=10 fade_out=10 gap_before(<50%)=10 fr (0.17 s)
C4: on f657-f996 (340 fr, 5.67 s) full@f819 fade_in=11 fade_out=10 gap_before(<50%)=11 fr (0.18 s)
C5: on f1008-f1265 (258 fr, 4.30 s) full@f-1 fade_in=11 fade_out=11 gap_before(<50%)=11 fr (0.18 s)
C6: on f1277-f1509 (233 fr, 3.88 s) full@f1284 fade_in=10 fade_out=10 gap_before(<50%)=11 fr (0.18 s)
C7: on f1520-f1794 (275 fr, 4.58 s) full@f1527 fade_in=10 fade_out=10 gap_before(<50%)=10 fr (0.17 s)
C8: on f1805-f2000 (196 fr, 3.27 s) full@f1811 fade_in=9 fade_out=10 gap_before(<50%)=10 fr (0.17 s)
C9: on f2011-f2214 (204 fr, 3.40 s) full@f2018 fade_in=10 fade_out=10 gap_before(<50%)=10 fr (0.17 s)
C10: on f2226-f2453 (228 fr, 3.80 s) full@f2232 fade_in=10 fade_out=10 gap_before(<50%)=11 fr (0.18 s)
C11: on f2466-f2699 (234 fr, 3.90 s) full@f2472 fade_in=10 fade_out=0 gap_before(<50%)=12 fr (0.20 s)
C1 f0: first-glyph height=48 px rows 121-168; text rows 118-180 (centre 149); x 145-1771 (width 1626)
C2 f285: first-glyph height=47 px rows 121-167; text rows 118-180 (centre 149); x 202-1717 (width 1515)
C3 f457: first-glyph height=47 px rows 121-167; text rows 118-180 (centre 149); x 327-1589 (width 1262)
C4 f819: first-glyph height=47 px rows 121-167; text rows 114-180 (centre 147); x 274-1643 (width 1369)
C5 f1008: first-glyph height=3 px rows 121-123; text rows 119-167 (centre 143); x 229-1696 (width 1467)
C6 f1284: first-glyph height=47 px rows 121-167; text rows 118-180 (centre 149); x 352-1565 (width 1213)
C7 f1527: first-glyph height=47 px rows 121-167; text rows 121-180 (centre 150); x 207-1708 (width 1501)
C8 f1811: first-glyph height=47 px rows 121-167; text rows 114-180 (centre 147); x 292-1627 (width 1335)
C9 f2018: first-glyph height=47 px rows 121-167; text rows 114-180 (centre 147); x 219-1699 (width 1480)
C10 f2232: first-glyph height=47 px rows 121-167; text rows 118-180 (centre 149); x 339-1579 (width 1240)
C11 f2472: first-glyph height=47 px rows 121-167; text rows 121-180 (centre 150); x 350-1567 (width 1217)
```
(capcheck's "intrusion" is the hairline content described in §7.3; its luminance line is the whole 1,920-px-wide band, while the §7.2 figures are the text extent as section 7.5 asks. Its "first_full" search returned −1 for captions 1 and 5, so it measured those two at frame 0 (fully opaque: 48 px by its looser ink threshold, 47 px by §7.2) and at frame 1008 (caption 5 at 50 % opacity, hence the 3 px reading); measured directly on the first fully opaque frame 1014, caption 5's cap height is 47 px, rows 121–167, as in §7.2. Its "full@" frames for captions 2, 4 and 8 (285, 819, 1811) are where its own ≥ 95 % text-diff test first trips, not the §7.1 first-opaque frames (236, 663, 1812), and its fade_in counts of 10/11 frames measure the 10 → 90 % span of the ramp, not the 12-frame ramp itself. Band crops at the first opaque frames: `qa/film45/capcheck-v21/cap_frames/`, sheet `capsheet.png`.)

### 7.5 Reviewer question
Asked of the independent reviewer on the captioned film: "list every frame range that breaks a rule in sections 3 or 7, with the measured value". Verdict: PASS — no frame range breaks a rule in §3 or §7 (review-v21.md, 2026-10-17 10:27 UTC): zero breaks, six marginal items B1–B6 measured at or near a limit, five disclosure items C1–C5, all folded into these receipts. Review file: `qa/film45/review-v21.md`.

## 8. Contact sheets and final frames
`qa/film45/contact-45v21.jpg` (clean) and `qa/film45/v21c/contact-45v21.jpg` (captioned) — 45 frames each, one per second (frames 0, 60, …, 2640). `qa/film45/final-1x-v21.jpg` and `qa/film45/v21c/final-1x-v21.jpg` — frame 2699 at 1× (native 1920×1080). Caption first-opaque-frame sheet: `qa/film45/v21probe/cap-sheet-first-opaque.jpg`. Final hold: frames 2220–2699 (8.00 s) on the chart at 3.5× with the Q2 2001 labels.

## 9. Artifact pass (standard §4) and figures
Console check at commit `b3941e7` (`qa/film45/console-b3941e7.txt`; local copy of the deployed bundle on http://localhost:8731, Playwright Chromium, deviceScaleFactor 2): 0 console errors, 0 page errors and 0 failed requests at 1440×900, 1280×720 and 390×844 after load, the Q1 2001 selection (`PT.chart.select('2001Q1')`) and both document panes rendering their highlights. Clipping check on the same runs: no horizontal page overflow at any of the three widths; of the labels, tabs, legend entries, chips and card numbers tested, none is truncated except one designed case — at 390×844 the document-pane title "Special Investigative Committee report (2003)" is shortened with an ellipsis by its own `text-overflow: ellipsis; white-space: nowrap` rule (the full title is in the pane's citation chips and in the register). Anchored-value re-check at the same commit: 379/379 page-cited values open the cited page with the figure visible (`qa/verify-all.log`). Downloads (CSV ledger, JSON register) still open.

Every number in the films is reproduced by a receipt: Q1 2001 reported line costs $4,108m (Form 10-Q Q1 2001, p. 4 of 59, "Line costs 3,733 4,108"), improper reduction $771m (Special Investigative Committee report, viewer p. 110 = printed p. 105, "reduced line costs by a total of $771 million"), reconstruction 4,879 = 4,108 + 771; Q2 2001 reported $3,730m (Form 10-Q Q2 2001, p. 4 of 209, row "3,776 3,730 7,509 7,426"), improper reduction $610m (Committee report, viewer p. 113 = printed p. 108, "capitalized $560 million … reduced line costs by a total of $610 million"), reconstruction 4,340 = 3,730 + 610; register counts 57 documents · 3,119 pages · 453 values (379 page-cited, 47 events) from the app's own masthead line (`#mast-meta`, main.js: "57 documents · 3,119 pages" / "453 values · 379 page-cited · 47 events", computed from data/register.json, data/pagecounts.json and data/ledger.json meta) — see the verification table and `data/ledger` ids in HANDOFF.md. App unchanged: commit `b3941e7`, bundle hash `2e73305a70b8e12d573b066a41402ae405d432ba7bde3f2dd0d29fc898a6ac21` (method `cd app && find . -type f | sort | xargs sha256sum > manifest && sha256sum manifest`).
