#!/usr/bin/env python3
"""
Render Showcase #43 Audit v2 Long-Form Narrated & Captioned Video (136.0s, 1920x1080, 30fps, H.264 MP4).
"""
import json
import math
import os
import subprocess
import wave
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/home/user/workspace/paper-trail")
STATES_DIR = ROOT / "build" / "ui_states"
NARR_DIR = ROOT / "build" / "narration"
OUT_DIR = ROOT / "films"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUT_DIR / "paper-trail-worldcom-audit-v2-showcase.mp4"
SHARED_MP4 = Path("/home/user/workspace/Paper_Trail_WorldCom_Forensic_Workbench_Showcase.mp4")

FPS = 30
OW, OH = 1920, 1080
SW, SH = 2880, 1620  # 1.5x supersampled Playwright states

with open(STATES_DIR / "manifest.json") as f:
    M = json.load(f)

with open(ROOT / "build" / "shots.json") as f:
    SHOTS_TEXT = {s["id"]: s["vo"] for s in json.load(f)["shots"]}

# 16 scenes totaling 136.00s (4,080 frames @ 30fps), every scene 7.3s - 9.4s
SCENES = [
    {
        "id": "S01", "dur": 8.50,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [(0.0, "state_01_masthead_top")],
        "cursor": [(0.0, 210, 285), (2.2, 121, 266), (5.0, 320, 415), (7.8, 650, 395), (8.5, 650, 395)],
        "clicks": [],
        "callout": (1.8, 8.2, (18, 308, 972, 702))
    },
    {
        "id": "S02", "dur": 8.90,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [(0.0, "state_02_workspace_default")],
        "cursor": [(0.0, 650, 395), (2.2, 1480, 320), (5.5, 1480, 785), (8.9, 1480, 785)],
        "clicks": [],
        "callout": (1.5, 8.5, (1012, 92, 1906, 960))
    },
    {
        "id": "S03", "dur": 7.30,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_02_workspace_default"),
            (1.4, "state_03_q3_2000_hover"),
            (2.7, "state_04_q3_2000_selected")
        ],
        "cursor": [
            (0.0, 1480, 785),
            (1.3, M["q3_2000"]["x"], M["q3_2000"]["y"]),
            (2.7, M["q3_2000"]["x"], M["q3_2000"]["y"]),
            (4.2, 480, 95),
            (7.3, 480, 95)
        ],
        "clicks": [(2.7, M["q3_2000"]["x"], M["q3_2000"]["y"])]
    },
    {
        "id": "S04", "dur": 9.40,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [(0.0, "state_04_q3_2000_selected")],
        "cursor": [
            (0.0, 480, 95),
            (2.0, 85, 815),
            (4.6, 235, 815),
            (7.2, 415, 815),
            (9.4, 415, 815)
        ],
        "clicks": [],
        "callout": (1.0, 9.0, (18, 732, 972, 962))
    },
    {
        "id": "S05", "dur": 9.00,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_04_q3_2000_selected"),
            (2.4, "state_05_q3_2000_sha256_open")
        ],
        "cursor": [
            (0.0, 415, 815),
            (2.2, M["sha_badge_left"]["x"], M["sha_badge_left"]["y"]),
            (2.5, M["sha_badge_left"]["x"], M["sha_badge_left"]["y"]),
            (4.6, 1595, 320),
            (6.8, 1590, 875),
            (9.0, 1590, 875)
        ],
        "clicks": [(2.4, M["sha_badge_left"]["x"], M["sha_badge_left"]["y"])],
        "callout": (1.2, 8.6, (1012, 92, 1906, 955))
    },
    {
        "id": "S06", "dur": 8.00,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_04_q3_2000_selected"),
            (1.6, "state_06_q1_2001_hover"),
            (2.8, "state_07_q1_2001_selected")
        ],
        "cursor": [
            (0.0, 1590, 875),
            (1.5, M["q1_2001"]["x"], M["q1_2001"]["y"]),
            (2.8, M["q1_2001"]["x"], M["q1_2001"]["y"]),
            (4.2, 480, 95),
            (8.0, 480, 95)
        ],
        "clicks": [(2.8, M["q1_2001"]["x"], M["q1_2001"]["y"])]
    },
    {
        "id": "S07", "dur": 9.30,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [(0.0, "state_07_q1_2001_selected")],
        "cursor": [
            (0.0, 480, 95),
            (2.2, 235, 835),
            (5.2, 1625, 320),
            (7.4, 1480, 785),
            (9.3, 1480, 785)
        ],
        "clicks": [],
        "callout": (1.0, 8.9, (18, 732, 972, 962))
    },
    {
        "id": "S08", "dur": 9.10,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_07_q1_2001_selected"),
            (2.0, "state_08a_metric_pretax"),
            (5.1, "state_08b_metric_capex")
        ],
        "cursor": [
            (0.0, 1480, 785),
            (1.9, M["metric_pretax"]["x"], M["metric_pretax"]["y"]),
            (2.1, M["metric_pretax"]["x"], M["metric_pretax"]["y"]),
            (4.9, M["metric_capex"]["x"], M["metric_capex"]["y"]),
            (5.2, M["metric_capex"]["x"], M["metric_capex"]["y"]),
            (6.6, 480, 95),
            (9.1, 480, 95)
        ],
        "clicks": [
            (2.0, M["metric_pretax"]["x"], M["metric_pretax"]["y"]),
            (5.1, M["metric_capex"]["x"], M["metric_capex"]["y"])
        ]
    },
    {
        "id": "S09", "dur": 8.50,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_08b_metric_capex"),
            (1.8, "state_09_metric_ratio")
        ],
        "cursor": [
            (0.0, 480, 95),
            (1.7, M["metric_ratio"]["x"], M["metric_ratio"]["y"]),
            (1.9, M["metric_ratio"]["x"], M["metric_ratio"]["y"]),
            (3.8, 650, 515),
            (6.2, 480, 95),
            (8.5, 480, 95)
        ],
        "clicks": [(1.8, M["metric_ratio"]["x"], M["metric_ratio"]["y"])]
    },
    {
        "id": "S10", "dur": 8.20,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_09_metric_ratio"),
            (1.5, "state_10_mechanism_all")
        ],
        "cursor": [
            (0.0, 480, 95),
            (1.4, M["nav_mechanism"]["x"], M["nav_mechanism"]["y"]),
            (1.6, M["nav_mechanism"]["x"], M["nav_mechanism"]["y"]),
            (3.8, 260, 515),
            (6.2, 520, 600),
            (8.2, 520, 600)
        ],
        "clicks": [(1.5, M["nav_mechanism"]["x"], M["nav_mechanism"]["y"])],
        "callout": (2.0, 7.8, (18, 198, 972, 740))
    },
    {
        "id": "S11", "dur": 7.90,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_10_mechanism_all"),
            (1.6, "state_11a_mechanism_phase1"),
            (3.8, "state_11b_mechanism_phase2"),
            (5.7, "state_11c_mechanism_q3_2001")
        ],
        "cursor": [
            (0.0, 520, 600),
            (1.5, M["mech_phase1_btn"]["x"], M["mech_phase1_btn"]["y"]),
            (1.7, M["mech_phase1_btn"]["x"], M["mech_phase1_btn"]["y"]),
            (3.7, M["mech_phase2_btn"]["x"], M["mech_phase2_btn"]["y"]),
            (3.9, M["mech_phase2_btn"]["x"], M["mech_phase2_btn"]["y"]),
            (5.6, M["mech_q3_2001_btn"]["x"], M["mech_q3_2001_btn"]["y"]),
            (5.8, M["mech_q3_2001_btn"]["x"], M["mech_q3_2001_btn"]["y"]),
            (7.9, 480, 95)
        ],
        "clicks": [
            (1.6, M["mech_phase1_btn"]["x"], M["mech_phase1_btn"]["y"]),
            (3.8, M["mech_phase2_btn"]["x"], M["mech_phase2_btn"]["y"]),
            (5.7, M["mech_q3_2001_btn"]["x"], M["mech_q3_2001_btn"]["y"])
        ],
        "callout": (0.8, 7.5, (18, 198, 972, 740))
    },
    {
        "id": "S12", "dur": 7.50,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_12a_mechanism_taccounts"),
            (2.8, "state_12b_taccount_jump_workspace")
        ],
        "cursor": [
            (0.0, 480, 95),
            (2.6, 310, 268),
            (2.9, 310, 268),
            (5.0, 1480, 785),
            (7.5, 1480, 785)
        ],
        "clicks": [(2.8, 310, 268)],
        "callout": (0.6, 7.1, (18, 108, 972, 482))
    },
    {
        "id": "S13", "dur": 8.50,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_12b_taccount_jump_workspace"),
            (1.4, "state_13a_chronology_all"),
            (3.8, "state_13b_chronology_audit")
        ],
        "cursor": [
            (0.0, 1480, 785),
            (1.3, M["nav_timeline"]["x"], M["nav_timeline"]["y"]),
            (1.5, M["nav_timeline"]["x"], M["nav_timeline"]["y"]),
            (3.7, M["chron_audit_chip"]["x"], M["chron_audit_chip"]["y"]),
            (3.9, M["chron_audit_chip"]["x"], M["chron_audit_chip"]["y"]),
            (6.0, 1420, 310),
            (8.5, 1420, 310)
        ],
        "clicks": [
            (1.4, M["nav_timeline"]["x"], M["nav_timeline"]["y"]),
            (3.8, M["chron_audit_chip"]["x"], M["chron_audit_chip"]["y"])
        ]
    },
    {
        "id": "S14", "dur": 8.40,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_13b_chronology_audit"),
            (1.4, "state_14a_ledger_all"),
            (3.8, "state_14b_ledger_capex_filter")
        ],
        "cursor": [
            (0.0, 1420, 310),
            (1.3, M["nav_ledger"]["x"], M["nav_ledger"]["y"]),
            (1.5, M["nav_ledger"]["x"], M["nav_ledger"]["y"]),
            (3.6, M["ledger_search"]["x"], M["ledger_search"]["y"]),
            (3.9, M["ledger_search"]["x"], M["ledger_search"]["y"]),
            (6.0, 480, 95),
            (8.4, 480, 95)
        ],
        "clicks": [
            (1.4, M["nav_ledger"]["x"], M["nav_ledger"]["y"]),
            (3.8, M["ledger_search"]["x"], M["ledger_search"]["y"])
        ]
    },
    {
        "id": "S15", "dur": 8.70,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_14b_ledger_capex_filter"),
            (1.3, "state_15a_documents_register"),
            (4.4, "state_15b_method_verification")
        ],
        "cursor": [
            (0.0, 480, 95),
            (1.2, M["nav_documents"]["x"], M["nav_documents"]["y"]),
            (1.4, M["nav_documents"]["x"], M["nav_documents"]["y"]),
            (4.3, M["nav_method"]["x"], M["nav_method"]["y"]),
            (4.5, M["nav_method"]["x"], M["nav_method"]["y"]),
            (6.2, M["method_xlsx_btn"]["x"], M["method_xlsx_btn"]["y"]),
            (8.7, M["method_xlsx_btn"]["x"], M["method_xlsx_btn"]["y"])
        ],
        "clicks": [
            (1.3, M["nav_documents"]["x"], M["nav_documents"]["y"]),
            (4.4, M["nav_method"]["x"], M["nav_method"]["y"])
        ]
    },
    {
        "id": "S16", "dur": 8.90,
        "cam0": (960, 540, 1.00), "cam1": (960, 540, 1.00),
        "states": [
            (0.0, "state_15b_method_verification"),
            (1.3, "state_16_closing_wide")
        ],
        "cursor": [
            (0.0, M["method_xlsx_btn"]["x"], M["method_xlsx_btn"]["y"]),
            (1.2, M["nav_chart"]["x"], M["nav_chart"]["y"]),
            (1.4, M["nav_chart"]["x"], M["nav_chart"]["y"]),
            (3.4, 480, 95),
            (8.9, 480, 95)
        ],
        "clicks": [(1.3, M["nav_chart"]["x"], M["nav_chart"]["y"])]
    }
]


def mj(t: float) -> float:
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    return t * t * t * (10.0 + t * (-15.0 + 6.0 * t))


def interp_cursor(pts, t):
    if t <= pts[0][0]:
        return pts[0][1], pts[0][2]
    if t >= pts[-1][0]:
        return pts[-1][1], pts[-1][2]
    for i in range(len(pts) - 1):
        t0, x0, y0 = pts[i]
        t1, x1, y1 = pts[i + 1]
        if t0 <= t <= t1:
            u = mj((t - t0) / max(1e-6, t1 - t0))
            return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return pts[-1][1], pts[-1][2]


def build_audio(out_wav: Path):
    """Build 48kHz stereo master audio: ElevenLabs Chris voiceover + subtle warm archival room tone + crisp UI clicks."""
    sr = 48000
    total_dur = sum(s["dur"] for s in SCENES)
    total_samples = int(round(total_dur * sr))
    mix = np.zeros((total_samples, 2), dtype=np.float32)

    # 1. Subtle warm archival harmonic drone / room presence (-38 dBFS)
    t = np.arange(total_samples, dtype=np.float32) / sr
    pad = (
        0.008 * np.sin(2 * np.pi * 110.0 * t)
        + 0.005 * np.sin(2 * np.pi * 165.0 * t + 0.4)
        + 0.003 * np.sin(2 * np.pi * 220.0 * t + 1.1)
    )
    # Slow breathing envelope
    env = 0.75 + 0.25 * np.sin(2 * np.pi * 0.08 * t)
    # Fade in first 1.0s and fade out last 1.5s
    fade_in = np.clip(t / 1.0, 0.0, 1.0)
    fade_out = np.clip((total_dur - t) / 1.5, 0.0, 1.0)
    pad = pad * env * fade_in * fade_out
    mix[:, 0] += pad
    mix[:, 1] += pad * 0.96

    # 2. Place each scene's ElevenLabs Chris narration + UI click sounds
    cur_t = 0.0
    for sc in SCENES:
        sid = sc["id"]
        mp3_path = NARR_DIR / f"{sid}.mp3"
        wav_tmp = NARR_DIR / f"{sid}_48k.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp3_path), "-ar", str(sr), "-ac", "1", "-f", "wav", str(wav_tmp)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        with wave.open(str(wav_tmp), "rb") as wf:
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)
            vo = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

        # Normalize peak of each segment gently so Chris is consistent across all 16 scenes
        peak = np.max(np.abs(vo)) if len(vo) else 1.0
        if peak > 0.01:
            vo = vo * (0.78 / peak)

        # Start VO at +0.22s into the scene
        start_idx = int(round((cur_t + 0.22) * sr))
        end_idx = min(total_samples, start_idx + len(vo))
        seg_len = end_idx - start_idx
        if seg_len > 0:
            mix[start_idx:end_idx, 0] += vo[:seg_len]
            mix[start_idx:end_idx, 1] += vo[:seg_len]

        # Add subtle tactile mechanical UI click sound at each click timestamp
        for (ct, _cx, _cy) in sc["clicks"]:
            c_idx = int(round((cur_t + ct) * sr))
            c_len = int(0.035 * sr)
            if c_idx + c_len < total_samples:
                ct_arr = np.arange(c_len, dtype=np.float32) / sr
                click_wave = (
                    0.16 * np.sin(2 * np.pi * 1450.0 * ct_arr) * np.exp(-ct_arr * 180.0)
                    + 0.10 * np.sin(2 * np.pi * 680.0 * ct_arr) * np.exp(-ct_arr * 110.0)
                )
                mix[c_idx:c_idx + c_len, 0] += click_wave
                mix[c_idx:c_idx + c_len, 1] += click_wave

        cur_t += sc["dur"]

    # Soft limiter and write 16-bit PCM WAV
    mix = np.tanh(mix * 1.15) * 0.88
    pcm = (np.clip(mix, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    print(f"Built master audio: {out_wav} ({total_dur:.2f}s)")


def make_caption_overlay(text: str, font) -> Image.Image:
    """Pre-render a 1920x160 RGBA bottom caption bar with an opaque dark pill and crisp wrapped text."""
    ov = Image.new("RGBA", (OW, 160), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)

    # Wrap text into 1 or 2 balanced lines (max ~68 chars per line)
    words = text.split()
    if len(text) <= 68:
        lines = [text]
    else:
        # Find split point closest to middle character count
        best_i = len(words) // 2
        best_diff = 9999
        for i in range(2, len(words) - 1):
            l1 = " ".join(words[:i])
            l2 = " ".join(words[i:])
            diff = abs(len(l1) - len(l2))
            if diff < best_diff:
                best_diff = diff
                best_i = i
        lines = [" ".join(words[:best_i]), " ".join(words[best_i:])]

    line_bboxes = [draw.textbbox((0, 0), ln, font=font) for ln in lines]
    line_widths = [b[2] - b[0] for b in line_bboxes]
    line_h = 33
    max_w = max(line_widths)
    total_text_h = len(lines) * line_h

    pad_x, pad_y = 28, 12
    pill_w = max_w + pad_x * 2
    pill_h = total_text_h + pad_y * 2
    x0 = (OW - pill_w) // 2
    y0 = 160 - 14 - pill_h
    x1 = x0 + pill_w
    y1 = y0 + pill_h

    # Subtle drop shadow + opaque dark charcoal pill (#11110F at 94% opacity) + warm cream border
    draw.rounded_rectangle([x0 + 2, y0 + 4, x1 + 2, y1 + 4], radius=14, fill=(0, 0, 0, 110))
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(17, 17, 15, 240), outline=(212, 203, 186, 185), width=2)

    cur_y = y0 + pad_y - 2
    for ln, lw in zip(lines, line_widths):
        tx = (OW - lw) // 2
        draw.text((tx, cur_y), ln, font=font, fill=(248, 245, 238, 255))
        cur_y += line_h

    return ov


def make_cursor_sprite() -> Image.Image:
    """Create a crisp high-DPI macOS/studio arrow pointer with white halo (48x48 RGBA)."""
    cur = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(cur)
    pts = [(4, 4), (4, 34), (12, 26), (19, 40), (24, 37), (17, 24), (28, 24)]
    d.polygon(pts, fill=(20, 20, 18, 255), outline=(255, 255, 255, 255))
    # Thicker white border by drawing lines
    for i in range(len(pts)):
        p1 = pts[i]
        p2 = pts[(i + 1) % len(pts)]
        d.line([p1, p2], fill=(255, 255, 255, 255), width=2)
    d.polygon(pts, fill=(20, 20, 18, 255))
    return cur


def main():
    audio_wav = ROOT / "build" / "audit_v2_master.wav"
    build_audio(audio_wav)

    # Load all UI state images (2880x1620 RGB)
    state_imgs = {}
    for png in STATES_DIR.glob("state_*.png"):
        state_imgs[png.stem] = Image.open(png).convert("RGB")
    print(f"Loaded {len(state_imgs)} supersampled UI state images ({SW}x{SH})")

    # Load font for bottom captions
    font_candidates = [
        "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Medium.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    font_path = next((p for p in font_candidates if os.path.exists(p)), None)
    cap_font = ImageFont.truetype(font_path, 26)

    caption_overlays = {
        sc["id"]: make_caption_overlay(SHOTS_TEXT[sc["id"]], cap_font)
        for sc in SCENES
    }
    cursor_sprite = make_cursor_sprite()

    total_frames = sum(int(round(sc["dur"] * FPS)) for sc in SCENES)
    print(f"Rendering {total_frames} frames ({total_frames / FPS:.2f}s @ {FPS}fps) -> {OUT_MP4}")

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{OW}x{OH}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", str(audio_wav),
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(OUT_MP4)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    global_f = 0
    for sc_idx, sc in enumerate(SCENES):
        n_frames = int(round(sc["dur"] * FPS))
        sid = sc["id"]
        cap_ov = caption_overlays[sid]
        cx0, cy0, z0 = sc["cam0"]
        cx1, cy1, z1 = sc["cam1"]
        states = sc["states"]

        for lf in range(n_frames):
            t = lf / FPS
            # Camera smooth transition over the first 1.6s of the scene, then locked steady
            cam_u = mj(min(1.0, t / 1.6))
            cx = cx0 + (cx1 - cx0) * cam_u
            cy = cy0 + (cy1 - cy0) * cam_u
            z = z0 + (z1 - z0) * cam_u

            # Determine active state (with 4-frame = 0.13s cross-dissolve on state change)
            active_name = states[0][1]
            prev_name = None
            blend_alpha = 1.0
            for st_t, st_name in states:
                if t >= st_t:
                    if st_t > 0 and (t - st_t) < 0.14:
                        prev_name = active_name
                        blend_alpha = (t - st_t) / 0.14
                    active_name = st_name

            base_img = state_imgs[active_name]
            if prev_name and prev_name != active_name:
                base_img = Image.blend(state_imgs[prev_name], base_img, blend_alpha)
            else:
                base_img = base_img.copy()

            # Draw cursor on the 2880x1620 canvas (1.5x of 1920x1080 coords)
            cur_x, cur_y = interp_cursor(sc["cursor"], t)
            sx, sy = int(round(cur_x * 1.5)), int(round(cur_y * 1.5))

            # Check if within 0.22s after a click for tactile click ripple
            for ct, clx, cly in sc["clicks"]:
                dt = t - ct
                if 0.0 <= dt <= 0.24:
                    prog = dt / 0.24
                    rad = int(10 + 28 * prog)
                    alpha = int(210 * (1.0 - prog))
                    ring_layer = Image.new("RGBA", (rad * 2 + 8, rad * 2 + 8), (0, 0, 0, 0))
                    rd = ImageDraw.Draw(ring_layer)
                    rd.ellipse([2, 2, rad * 2 + 4, rad * 2 + 4], outline=(142, 44, 37, alpha), width=4)
                    base_img.paste(ring_layer, (int(clx * 1.5) - rad - 3, int(cly * 1.5) - rad - 3), ring_layer)

            base_img.paste(cursor_sprite, (sx - 4, sy - 4), cursor_sprite)

            # Crop camera window from 2880x1620 supersampled image and downsample to 1920x1080
            if abs(z - 1.0) < 1e-3 and abs(cx - 960) < 1 and abs(cy - 540) < 1:
                frame_img = base_img.resize((OW, OH), Image.Resampling.BILINEAR)
            else:
                win_w = OW / z
                win_h = OH / z
                left = max(0.0, min(OW - win_w, cx - win_w / 2.0))
                top = max(0.0, min(OH - win_h, cy - win_h / 2.0))
                crop_box = (
                    int(round(left * 1.5)),
                    int(round(top * 1.5)),
                    int(round((left + win_w) * 1.5)),
                    int(round((top + win_h) * 1.5))
                )
                frame_img = base_img.crop(crop_box).resize((OW, OH), Image.Resampling.BILINEAR)

            # Composite screen-space bottom caption pill at y = OH - 160
            frame_img.paste(cap_ov, (0, OH - 160), cap_ov)

            proc.stdin.write(frame_img.tobytes())
            global_f += 1

        print(f"  Finished {sid} ({sc_idx + 1}/16) -> frame {global_f}/{total_frames}")

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace")
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed ({ret}):\n{stderr_out[-1500:]}")

    # Copy to top-level workspace for share_file
    import shutil
    shutil.copy2(OUT_MP4, SHARED_MP4)
    print(f"SUCCESS: Rendered {OUT_MP4} ({OUT_MP4.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    main()
