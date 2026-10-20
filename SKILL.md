---
name: stagecraft
description: Build art-directed presentations from real context (a codebase, docs, papers, notes, data, URLs) as a single-file HTML deck with a GSAP motion engine (live selector from Still to Insane, interactive diagrams, animated charts, canvas effects, presenter view) and/or a native editable PowerPoint .pptx. Every fact on a slide is traced to a source through a checked claim ledger. Use this whenever the user wants a presentation, slide deck, slides, keynote, pitch deck, talk, lecture, demo-day deck, project or thesis defense, paper walkthrough, architecture walkthrough, or "turn this repo/doc/paper into slides", even if they never say "stagecraft". When it was not invoked by name, confirm with the user in one line before using it.
---

# stagecraft

Decks that look like a top studio designed them and say only what the sources support. You write content and markup. The
bundled engine handles the stage, motion, interaction, and checks, so results stay strong on any model.

## 0. Confirm (unless invoked directly)

If the user typed `/stagecraft` or named this skill, go ahead. Otherwise ask one line first, for example:
"Want me to build this as a stagecraft deck (animated HTML with a motion selector, PPTX optional)?" Then wait.

## 1. Skim the sources

Find what the deck is built from: files or folders the user named, the current repo, attached PDFs, pasted notes, URLs.
Skim enough to propose a real thesis and real directions (README, entry points, abstract, headings). Deep reading comes in step 3.
Read `references/content.md` now if the sources are large or mixed.

## 2. Aesthetic interview

Read `references/interview.md` and run it: core concept, audience and setting, moodboard direction (three options from
`references/design.md`, tailored), format and default motion level. One round, using AskUserQuestion when available.
Skip what the user already answered. If they said to just build it, state your assumptions in a short paragraph and continue.

## 3. Claim ledger and outline

Read the sources properly. Write `presentations/<slug>/brief.json` (schema in `references/content.md`):
sources, claims with verbatim quotes and locators, and the slide outline with roles, assertion titles, layouts, and claim ids.
Content rules that keep runs consistent:
- Only facts from the sources and the user's own messages, unless the user allowed outside knowledge (`source_policy: augment`).
- Every number shown anywhere (slides, labels, tooltips, notes) appears in a claim, written the way the slide shows it.
- Quotes are copied exactly. The build verifies them against local files.

Show the outline (numbered titles, one line each, layout, key visual) and get a yes unless the user waived checkpoints.

## 4. Design system

From the chosen direction in `references/design.md`, write the theme: `:root` tokens (`--bg --fg --muted --accent
--accent-ink --font-display --font-body --font-mono`), font links, and one signature device. Define the system once (title
anchor, kicker, margins, footer, panel style, depth, accent moments) and reuse it on every slide; vary the composition of
the visual half, not the system. Use the direction's own faces unless the user chose something more extreme. Plan one or two bespoke components for the content
(`references/components.md` section 10). Read `references/motion.md` before tagging anything.

## 5. Write the deck source

Create `presentations/<slug>/deck.src.html`. Write only theme CSS, slides, notes, and optional hooks; the engine is injected
at build. Skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deck title</title>
<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
<style>
:root { --bg: #...; --fg: #...; --muted: #...; --accent: #...; --accent-ink: #...;
        --font-display: '...', serif; --font-body: '...', sans-serif; --font-mono: '...', monospace; }
/* one block per slide, scoped by a slide class: .s-cover { ... } */
</style>
</head>
<body data-motion="2">
<div class="kx-viewport"><div class="kx-stage">
  <section class="slide s-cover" id="cover" data-layout="poster" data-claims="C1" data-fx="dotgrid">
    <h1 data-anim="chars">Assertion title</h1>
    <p data-anim="lines" data-delay="0.7">One supporting sentence.</p>
    <aside class="notes"><p>What to say here.</p></aside>
  </section>
  <!-- more <section class="slide"> -->
</div></div>
<script>/* optional window.KX_ENTER hooks for bespoke components */</script>
</body>
</html>
```

Authoring rules:
- Design at 1920x1080 in px. Absolute positioning or CSS grid inside each slide. 96px outer margins unless `data-bleed`
  (also use `data-bleed` on decorative glow or texture layers that extend past the edge).
- Fill the frame: content on most slides reaches below y 760. Use `data-open` only on slides where emptiness is the point.
- Decorative numerals (folios, step markers, section numbers) go in `data-deco` elements so the number check skips them.
- Every slide has `id`, `data-layout`, `data-claims`, and `<aside class="notes">`.
- Tag motion with the `data-anim` vocabulary. Hero move first, supporting copy delayed, five to eight animated elements max.
- Interactivity where it explains something: clickable diagram nodes, tabs, hover rows, chart tooltips, step builds.
- Voice per `references/voice.md`: no dash characters at all, short declarative sentences, register matched to the audience, assertion titles.
- Look at `assets/example/deck.src.html` once for wiring patterns. Do not copy its look, palette, or fonts.

## 6. Build, look, fix

```bash
python <skill>/scripts/build.py presentations/<slug>/deck.src.html
python <skill>/scripts/snapshot.py presentations/<slug>/deck.html
```

- build.py lints and writes `deck.html` only with zero errors. Fix every error; fix warnings unless you have a reason.
- snapshot.py runs a layout audit in headless Chrome or Edge (offstage, clipped, overlapping, tiny, low-contrast text, empty bottom, diagram edges that miss their nodes) and
  saves `snapshots/contact.png` plus one PNG per slide. Open contact.png and look at it like an art director:
  Does every slide belong to one system? Is there a pop of accent color where it matters? Is any bottom third empty?
  Is the hierarchy obvious from across a room? Is anything cramped, orphaned, or floating? Do special glyphs render?
  Then read each slide's captions against its claims: the build checks numbers, not meaning.
  Fix, rebuild, re-snapshot. Two or three passes is normal.
- No Chrome or Edge: open `deck.html?audit` in a browser tool and read `window.__kxAudit`, then screenshot `deck.html?static&motion=0#N`.

## 7. Deliver

Tell the user, briefly:
- Where the files are: `deck.html` (present this), `deck.src.html` (edit this, then rebuild), `brief.json` (sources and claims).
- How to present: open in Chrome, `F` fullscreen, arrows or clicker to advance, `M` motion level, `N` notes with citations,
  `P` presenter window, `O` overview. `?motion=0` to `?motion=4` in the URL sets the level.
- Offline venue: rebuild with `--offline` to inline GSAP. PDF: `snapshot.py deck.html --pdf` (vector, sharp at any size).
  High-resolution PNGs: `snapshot.py deck.html --res 1440` (2K) or `--res 2160` (4K). The live deck is sharp on 2K and 4K
  displays as is.
- Any claims from model knowledge the build listed, so they can verify them.

## PPTX

When the user wants PowerPoint, read `references/pptx.md`. Same brief.json and voice rules; build natively with
`scripts/pptx_kit.py` (editable text, charts and diagrams, Morph transitions mapped from the motion level). Only use the
image-per-slide route when the user explicitly prefers exact looks over editing. For both formats, do HTML first, then PPTX from the same outline.

## Editing an existing deck

Edit `deck.src.html` (and brief.json for new facts), rebuild, re-snapshot. For a deck made elsewhere, extract its text into
brief.json as a source, then rebuild it in this system.

## Files

| file | read when |
|---|---|
| `references/interview.md` | step 2 |
| `references/content.md` | step 3, and any time content questions come up |
| `references/design.md` | steps 2 and 4 |
| `references/motion.md` | before tagging animations or writing hooks |
| `references/components.md` | diagrams, charts, code, bespoke components |
| `references/voice.md` | before writing any slide text or notes |
| `references/pptx.md` | PowerPoint output |
| `assets/engine.js`, `assets/engine.css` | never edit per deck; build.py inlines them |
| `assets/example/` | a small working deck with brief.json, for wiring reference |
