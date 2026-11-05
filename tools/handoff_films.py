#!/usr/bin/env python3
"""Append/refresh the 'Film shot list' section of handoff/HANDOFF.md from qa/film/shots-*.json and the encode logs."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'qa', 'film')
out = ['## Film shot list (exact clicks, from the capture logs)', '']
for v in (60, 30):
    shots = json.load(open(os.path.join(F, f'shots-{v}.json')))
    log = open(os.path.join(F, f'encode-{v}.log')).read()
    probe = dict(re.findall(r'^(\w+)=(.+)$', log, re.M))
    sums = dict((m.group(2).split('/')[-1], m.group(1)) for m in re.finditer(r'^([0-9a-f]{64})\s+(\S+)$', log, re.M))
    rf = re.search(r'^repofit: (.+?) size=(\d+)', log, re.M)
    out.append(f"### {v} s film — `paper-trail-{v}s.mp4` (conversation asset) · `films/paper-trail-{v}s-repofit.mp4` (repo copy)")
    out.append(f"Delivery: {probe.get('width')}×{probe.get('height')}, {probe.get('r_frame_rate', '').replace('/1', '')} fps, {probe.get('nb_frames')} frames, {float(probe.get('duration', 0)):.0f} s, {probe.get('codec_name')} {probe.get('pix_fmt')}, {int(probe.get('size', 0)) / 1e6:.1f} MB, silent — SHA-256 `{sums.get(f'paper-trail-{v}s.mp4')}`; clean master `paper-trail-{v}s-master.mp4` (crf 10, yuv444p) SHA-256 `{sums.get(f'paper-trail-{v}s-master.mp4')}`. Both are shared as assets in the build conversation. Repo copy `films/paper-trail-{v}s-repofit.mp4`: the same {shots['frames']} frames re-encoded with a bitrate target so both cuts fit the project repo's 5 GiB cap ({rf.group(1) if rf else '—'}; {int(rf.group(2)) / 1e6 if rf else 0:.1f} MB) — SHA-256 `{sums.get(f'paper-trail-{v}s-repofit.mp4')}`; static reading holds are visually identical to the delivery, fast camera moves are softer. Captured at {shots['viewport']}; clock: {shots['clock']}; zooms: {shots.get('zoom', '—')}.")
    out.append('')
    out.append('| Frame | Time | Action | Target (CSS selector) | Pointer (CSS px) | Viewer after |')
    out.append('|---|---|---|---|---|---|')
    pending = None
    for s in shots['shots']:
        what = s['what']
        if what.startswith('click:'):
            pending = s
            out.append(f"| {s['frame']} | {s['time']} | {what[6:].strip()} | `{s.get('target', '')}` | {s.get('x')}, {s.get('y')} | |")
        elif what.startswith('viewer:'):
            def desc(p):
                parts = []
                if p.get('strong'): parts.append('figure highlighted')
                if p.get('hl'): parts.append(f"{p['hl']} highlight mark{'s' if p['hl'] != 1 else ''}")
                return f"{p.get('title')} p. {p.get('page')} ({', '.join(parts) or 'no highlight'})"
            panes = '; '.join(desc(p) for p in s.get('panes', []) if p.get('title'))
            out[-1] = out[-1][:-2] + f" {what[7:].strip()}: {panes} |"
        elif what.startswith('scene:'):
            out.append(f"| {s['frame']} | {s['time']} | scene — {what[6:].strip()} | | | |")
        elif what.startswith('camera:'):
            z = s.get('zoom'); lab = what[7:].strip()
            detail = ' (zoom %s×, window centre %s, %s CSS px)' % (z, s.get('cx'), s.get('cy')) if z and z > 1 else ''
            out.append(f"| {s['frame']} | {s['time']} | camera — {lab}{detail} | | | |")
        elif what == 'end':
            out.append(f"| {s['frame']} | {s['time']} | end | | | |")
    out.append('')
p = os.path.join(ROOT, 'handoff', 'HANDOFF.md'); s = open(p).read()
s = re.sub(r'\n## Film shot list.*\Z', '\n', s, flags=re.S).rstrip('\n') + '\n\n' + '\n'.join(out)
open(p, 'w').write(s)
print('updated HANDOFF.md film shot list')
