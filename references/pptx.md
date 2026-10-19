# PPTX output

Use this when the user wants a real PowerPoint file. HTML stays the richer format (interactivity, fx, live motion
selector); say so once, then build the best PPTX the format allows. Same brief.json, same ledger, same voice rules.

## Two routes

1. **Native, editable (default for PPTX, and required when the file is for uploading, grading, or a client to edit).** Build with `scripts/pptx_kit.py` (python-pptx). Real text boxes, native charts
   the user can edit, shapes and connectors for diagrams, speaker notes, and transitions mapped from the motion level.
2. **Pixel-perfect from the HTML deck.** Only when the user says they care about the exact look more than editing: build the HTML deck,
   run `snapshot.py deck.html --res 2160` for 4K PNGs (they stay sharp on large displays), then place each PNG full-bleed on a slide with pptx_kit (`image(s, png, 0, 0, 1920, 1080)`)
   and copy the notes. Tell the user the slides are images.

## Native route

Write a small `build_pptx.py` next to brief.json that imports the kit and lays out each slide from the outline:

```python
import json, sys
sys.path.insert(0, r"<skill dir>/scripts")
from pptx_kit import Deck

brief = json.load(open("brief.json", encoding="utf-8"))
T = dict(bg="0F2B46", fg="D4E6F8", muted="7E9BB8", accent="FFB000",
         display="Bahnschrift", body="Segoe UI", mono="Consolas")
d = Deck(T)
s = d.slide(transition="fade")
d.text(s, 96, 380, 1500, 360, "The allowlist closed the last bypass", font="display", size=150, line=0.9, name="!!title")
d.notes(s, brief["slides"][0]["notes"])
d.save("deck.pptx")
```

Rules:
- Same layout archetypes and asymmetry as HTML. Positions are px on the 1920x1080 canvas.
- **Fonts must exist on the presenting machine.** python-pptx cannot embed fonts. Prefer faces that ship with Office or the
  OS (Georgia, Bahnschrift, Sitka, Segoe UI, Consolas, Cambria, Rockwell, Gill Sans MT on Office, Avenir and Helvetica Neue on
  Mac). If the direction needs a Google font, tell the user which fonts to install, with links. The banned-font rule from
  design.md still applies to the display face.
- Charts: `d.chart(s, "bar"|"column"|"line"|"donut", categories, {"Series": values}, x, y, w, h)` gives native charts with
  direct data labels and no gridlines. Values come from the ledger.
- Diagrams: `a = d.node(...)`, `d.edge(s, a, b)` connects with a curved arrow that stays attached when the user moves boxes.
- Motion level to transitions: Still = `none`, Minimal = `fade`, Smooth = `push` inside sections and `fade` elsewhere,
  Cinematic and Insane = `morph`. For Morph, give shapes that persist across adjacent slides the same name starting with
  `!!` (for example `name="!!title"`); PowerPoint then animates them between slides. Move, resize, or recolor them across
  slides for the effect.
- Speaker notes: write them once in brief.json `slides[].notes` and use them for both HTML `<aside class="notes">` and `d.notes()`.
- Font metrics differ from the HTML faces. After the first build, render the PPTX to images (below) and shrink any text that
  overflows its box; Georgia and other fallback serifs run wider than most display faces. `d.node()` shrinks long labels to fit.
- `d.save()` refuses to write if any text has dash characters or emoji. Also run the HTML lint ideas by eye: numbers from
  the ledger only, no generic titles.

## Check it

Render the PPTX to images to look at it: with PowerPoint installed on Windows, export via COM
(`$p = (New-Object -ComObject PowerPoint.Application).Presentations.Open($path, $true, $false, $false); $p.SaveAs($outDir, 18)`
saves PNGs); with LibreOffice, `soffice --headless --convert-to pdf deck.pptx`. Look at every slide for overflow, then fix.
