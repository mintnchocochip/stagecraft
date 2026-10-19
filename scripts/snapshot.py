#!/usr/bin/env python3
"""Render a built deck with headless Chrome/Edge: layout audit, per-slide PNGs, a contact sheet, optional PDF.

usage: python snapshot.py deck.html [--out DIR] [--slides 1,3,5] [--pdf] [--no-shots]

Prints the audit (offstage, clipped, overlap, tiny-text, low-contrast) per slide.
Look at contact.png after every build; open single slide PNGs when something looks off.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = [
    os.environ.get("KX_CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def find_browser():
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "chrome", "msedge"):
        p = shutil.which(n)
        if p:
            return p
    sys.exit("snapshot: no Chrome/Edge/Chromium found. Set KX_CHROME to the browser path, or review the deck in a browser tool with ?audit")


def run(browser, args, url, profile):
    cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
           "--allow-file-access-from-files", f"--user-data-dir={profile}", "--force-device-scale-factor=1", *args, url]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out")
    ap.add_argument("--slides", help="comma list of 1-based slide numbers to shoot (default all)")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--no-shots", action="store_true")
    a = ap.parse_args()
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

    deck = Path(a.deck).resolve()
    out = Path(a.out).resolve() if a.out else deck.parent / "snapshots"
    out.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    url = deck.as_uri()
    profile = tempfile.mkdtemp(prefix="kx-chrome-")

    r = run(browser, ["--dump-dom", "--virtual-time-budget=9000", "--window-size=1920,1080"], url + "?audit", profile)
    m = re.search(r'<script type="application/json" id="kx-audit">(.*?)</script>', r.stdout, re.S)
    if not m:
        print("audit: no report produced (is this a built deck? did the engine throw?)")
        print(r.stderr[-1500:])
        sys.exit(1)
    rep = json.loads(m.group(1))
    total = sum(len(s["issues"]) for s in rep["report"])
    print(f"audit: {rep['slides']} slides, {total} layout issues")
    for s in rep["report"]:
        for i in s["issues"]:
            extra = {k: v for k, v in i.items() if k not in ("type", "el")}
            print(f"  slide {s['slide']} [{s.get('layout')}] {i['type']}: {i['el']} {json.dumps(extra) if extra else ''}")

    n = rep["slides"]
    want = [int(x) for x in a.slides.split(",")] if a.slides else list(range(1, n + 1))
    shots = []
    if not a.no_shots:
        for k in want:
            png = out / f"slide-{k:02d}.png"
            run(browser, [f"--screenshot={png}", "--window-size=1920,1080", "--virtual-time-budget=6000"], f"{url}?static&motion=0#{k}", profile)
            if png.exists():
                shots.append(png)
        try:
            from PIL import Image
            cols, tw = 4, 480
            th = tw * 1080 // 1920
            rows = (len(shots) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (40, 40, 40))
            for j, pth in enumerate(shots):
                im = Image.open(pth).convert("RGB").resize((tw, th))
                sheet.paste(im, (8 + (j % cols) * (tw + 8), 8 + (j // cols) * (th + 8)))
            sheet.save(out / "contact.png")
            print(f"contact sheet: {out / 'contact.png'}")
        except ImportError:
            print("contact sheet skipped (pip install pillow); per-slide PNGs are in", out)
        print(f"screenshots: {len(shots)} in {out}")

    if a.pdf:
        pdf = deck.with_suffix(".pdf")
        run(browser, [f"--print-to-pdf={pdf}", "--no-pdf-header-footer", "--virtual-time-budget=8000"], url + "?static&motion=0", profile)
        print(f"pdf: {pdf}" if pdf.exists() else "pdf: failed")
    shutil.rmtree(profile, ignore_errors=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
