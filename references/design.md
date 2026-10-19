# Design: directions, layouts, type, color

Read this before writing any theme CSS. The goal is a deck that looks art-directed by a top studio, not generated. The
fastest way to look generated is to reach for the median choice at every decision. At each decision below, ask
"what would the median AI deck do here?" and do something more specific to this content.

## Contents
1. What gives a deck away as AI-made
2. Principles that make it look designed
3. Directions (moodboards)
4. Layout archetypes (1920x1080)
5. Typography rules
6. Color rules
7. Images and brand books

## 1. What gives a deck away as AI-made

Avoid every one of these. They are the visual equivalent of "delve".

- Centered title with three icon cards or three bullet columns underneath. The single biggest tell.
- Every slide on the same centered axis. Every slide the same layout with different words.
- Inter, Roboto, Poppins, Montserrat, Space Grotesk, system-ui. Purple or blue-violet gradients. Gradient text.
- Rounded cards with drop shadows and glassmorphism blur on everything. Pill badges everywhere.
- Emoji or generic line icons in colored circles standing in for ideas.
- "01 / 02 / 03" numbering on every block as decoration with no meaning.
- Titles like Overview, Introduction, Key Takeaways, Conclusion, Thank You, Q&A.
- Stock photos of handshakes, glowing brains, robots, abstract blue networks.
- Every element animating in at once with the same fade-up.
- Even, timid palettes: five colors at equal weight, nothing dominant.

## 2. Principles that make it look designed

1. **One idea per slide, stated as a sentence.** The title is the point, not the topic.
2. **Scale contrast is the design.** Headline 96 to 320px against body 26 to 32px and labels 18 to 22px. Three sizes, maybe four. Never a smooth ramp of six similar sizes.
3. **Asymmetry with intent.** Place the mass off-center: hard splits (7/5, 8/4, 3/9), a margin rail, a numeral bleeding off the edge. Leave 35 to 50 percent of the slide empty, and make the empty part feel chosen.
4. **One signature device per deck.** A thick accent rule, a giant italic numeral, a margin annotation column, a dimension line, an exposed grid. Repeat it so the deck feels authored by one hand. Pick it from the direction.
5. **A grid you can feel.** Use a 12-column grid with 96px outer margins and 24px gutters on the 1920 stage. Align edges to it. Break it once per slide at most, on purpose.
6. **Rules and type over boxes.** Separate content with hairlines, column rules and whitespace before you reach for cards. If you use a filled panel, use one, flat, full-bleed to an edge.
7. **Rhythm across the deck.** Alternate dense and sparse slides. Alternate light and dark (or paper and accent) grounds at section changes. Never two adjacent slides with the same `data-layout`.
8. **Specific visuals beat generic ones.** Draw the actual architecture, the actual numbers, the actual sequence. Invent one or two visual metaphors that only make sense for this content (see components.md, section "Bespoke components").
9. **Finish like print.** Optical sizes on variable fonts, `text-wrap: balance` on headings, `text-wrap: pretty` on body, tabular numbers in tables (`font-variant-numeric: tabular-nums`), hanging quotes, consistent baseline spacing.

## 3. Directions (moodboards)

Offer three of these in the interview, chosen to fit the content and audience, or invent a fourth from the user's moodboard. Each gives a full starting system. Adapt it: change one accent, swap one face, tune to the brand. Do not ship any of them verbatim twice in a row.

Font URLs: Google Fonts `https://fonts.googleapis.com/css2?family=Name:wght@400;700&display=swap`, Fontshare `https://api.fontshare.com/v2/css?f[]=clash-display@500,700&display=swap`.

**Broadsheet** (research findings, strategy, policy, papers for a general audience)
- Type: Newsreader or Instrument Serif display; Schibsted Grotesk body; IBM Plex Mono labels.
- Color: paper `#F3EFE6`, ink `#121212`, muted `#6B655B`, accent `#C3271B`.
- Device: column rules, datelines and kicker labels in mono caps, one drop cap per section opener.
- Motion: Smooth by default. `lines` titles, wipe cuts, `grain` fx on section openers.

**Brutalist Poster** (launches, manifestos, bold pitches, conference openers)
- Type: Archivo at width 125 weight 900 or Anton for display; Archivo 400 body; Space Mono labels.
- Color: bone `#F2EFE8` with black `#0A0A0A` and signal orange `#FF3B00`; or black ground with acid `#D7FF3A`.
- Device: type at 300 to 420px cropped by the slide edge (`data-bleed`), 8px rules, exposed grid lines.
- Motion: Cinematic or Insane. `chars` titles, shutter cuts, pop and elastic grows.

**Blueprint** (architecture, systems, codebases, infrastructure)
- Type: Big Shoulders Display or Familjen Grotesk display; IBM Plex Sans body; JetBrains Mono labels.
- Color: blueprint `#0F2B46`, line `#D4E6F8`, muted `#7E9BB8`, accent amber `#FFB000`.
- Device: faint 40px grid paper, dimension lines with ticks, callout leaders to labels, a title block in a corner.
- Motion: Smooth to Cinematic. `draw` for every diagram, `data-flow` packets on edges, `dotgrid` fx.

**Terminal Noir** (developer tools, CLIs, security, agents, infra)
- Type: Geist 600 tight or Martian Mono display; Geist body; Geist Mono or JetBrains Mono.
- Color: `#0A0A0A`, fg `#E8E6E3`, muted `#7A7672`, one accent: phosphor `#7CFF6B` or amber `#FFB454`.
- Device: real command lines and real output from the source, monospace tables, a blinking caret on the title only.
- Motion: Cinematic. `scramble` on short titles, `constellation` fx, code slides with step builds.

**Museum Placard** (brand, design, humanities, investor narrative, quiet luxury)
- Type: Cormorant Garamond 300 or Bodoni Moda display; Hanken Grotesk body; DM Mono captions.
- Color: `#F5F2EC`, ink `#1B1A17`, muted `#857F74`, accent bronze `#8A6A3B`.
- Device: an artifact framed alone with a small placard caption, huge margins, numbered plates.
- Motion: Minimal or Smooth. Slow `mask` reveals, fades, no fx.

**Data Newsroom** (metrics, results, benchmarks, evaluations)
- Type: Newsreader 600 display; Public Sans body; IBM Plex Mono for axes and sources.
- Color: `#F7F4EE`, ink `#1A1A1A`, muted `#77736B`, accent `#0F5499` with a red `#D6332A` for the one number that matters.
- Device: chart-first slides, direct labels on lines and bars (no legends), a source line under every chart.
- Motion: Smooth. `grow` bars, `draw` lines, `count` for headline numbers.

**Kinetic Swiss** (product, methodology, consulting, process)
- Type: Host Grotesk or Hanken Grotesk 800 display; same family 400 body; Fragment Mono labels.
- Color: white `#FFFFFF` or `#F2F2F2`, black `#111111`, red `#E30613`.
- Device: flush-left ragged-right text, oversized numerals, a red square or bar as the only ornament.
- Motion: Smooth to Cinematic. Wipe cuts, `lines`, `stagger` lists.

**Risograph Zine** (workshops, education, community, playful internal talks)
- Type: Bricolage Grotesque 800 display; Epilogue body; Azeret Mono labels.
- Color: paper `#F6F0E1`, ink `#1D1D1D`, fluorescent pink `#FF48B0`, riso blue `#0078BF`, yellow `#FFE800`.
- Device: misregistered overprint (duplicate the headline in a second ink, offset 6px, `mix-blend-mode: multiply`), halftone dots via `radial-gradient`.
- Motion: Insane fits. `pop`, elastic `grow`, shutter cuts in the accent ink.

**Lab Notebook** (academic papers, thesis defenses, ML research)
- Type: Instrument Serif display with italic emphasis; Geist body; JetBrains Mono.
- Color: `#FBFAF7` with a faint 32px grid, ink `#1F2328`, accent ink blue `#2F5BEA`, annotation red `#C8302C`.
- Device: margin annotations in the accent, figure numbers, citation chips that open the source in notes.
- Motion: Smooth. `draw` for plots and diagrams, `lines` titles, steps for derivations.

**Night Signal** (vision talks, keynote openers, AI and product launches)
- Type: Unbounded or Syne 800 display; Satoshi (Fontshare) body; Martian Mono labels.
- Color: `#08090B`, fg `#F2F0EA`, muted `#8B8A86`, one luminous accent `#FF5A1F` or `#00E0B8`.
- Device: a single soft glow behind the key element, giant numerals, deep black space.
- Motion: Cinematic or Insane. `flowfield` fx on openers, iris cuts, `chars` titles.

## 4. Layout archetypes (1920x1080)

Set `data-layout` on every slide to one of these names (or a new descriptive name). Plan the sequence in brief.json so no two neighbors match and a 10-slide deck uses at least 5.

| name | composition |
|---|---|
| `poster` | Huge headline set across the slide off-center, small meta row and a dek in opposite corners. Openers and section breaks. |
| `giant-number` | One number at 300 to 450px bleeding off one edge; a rail on the other side with the sentence that explains it. |
| `split-7-5` | Hard split. Big type or visual on 7 columns, supporting copy on 5, divided by a rule or a ground color change. |
| `margin-rail` | Content in columns 4 to 12, a narrow annotation rail in columns 1 to 3 with kicker, source and notes. |
| `broadsheet` | Two or three uneven text columns with column rules and a headline spanning them. Reading decks. |
| `diagram-rail` | Live diagram on the left 60 to 65 percent, detail rail on the right that changes when a node is clicked. |
| `index` | Big numbered rows (80px names) separated by rules, hover reveals a line of detail per row. |
| `chart-margin` | Chart on 8 columns with direct labels, a margin note on 3 columns that tells the reader what to see. |
| `quote-wall` | A verbatim quote from a source at 72 to 110px with hanging punctuation and a small attribution. |
| `bleed-image` | Image full-bleed on one side or behind, caption block in a solid panel. Only with real or licensed images. |
| `timeline-band` | A horizontal band across the middle with dated ticks; events above and below alternate. |
| `compare-toggle` | Before and after (or A and B) in one frame with tabs that swap the content in place. |
| `code-walk` | Real code from the source on the left at 22 to 26px, step builds highlight lines while the right side explains. |
| `statement` | One sentence at 110 to 160px on an accent or ink ground. Section closers and the final ask. |
| `mosaic` | Asymmetric grid of 3 to 5 unequal tiles (one dominant). Not a uniform bento. |

Skeleton for positioning: absolute positioning inside the slide is fine and often cleanest on a fixed stage. Use CSS grid
when rows must align. Always keep text inside 96px margins unless the element is marked `data-bleed`.

```css
.s-split { display: grid; grid-template-columns: 1fr 700px; }
.s-split .main { padding: 120px 72px 96px 96px; }
.s-split .side { background: var(--fg); color: var(--bg); padding: 120px 96px 96px 72px; }
```

## 5. Typography rules

- Two families plus a mono at most. Distinctive display face, quiet text face. Set the stack in `--font-display`, `--font-body`, `--font-mono`.
- Display: tight tracking (-0.02 to -0.05em), line-height 0.85 to 1.0, optical size high. Body: line-height 1.35 to 1.55, 26 to 32px, max 60 characters per line.
- Mono labels: uppercase, 18 to 22px, tracking +0.06 to +0.14em. Use them for kickers, axes, sources, folios.
- Use italics or a second weight for emphasis inside a headline, not color plus bold plus underline.
- Minimum on-slide text is 20px. The audit flags anything under 18px.
- Numbers in tables and charts: `font-variant-numeric: tabular-nums lining-nums`.
- If a brand book requires a banned face (Inter, Roboto), allow it with `<meta name="kx-allow-fonts" content="Inter">` and make the layout carry the character.

## 6. Color rules

- One dominant ground, one ink, one muted, one accent. Optionally a second accent used on at most one element per slide.
- The accent covers under 10 percent of a slide, except on `statement` slides where it can be the ground.
- Text contrast at least 4.5:1 under 36px and 3:1 above. Accents that fail at small sizes get an `--accent-ink` variant for text.
- Switch ground at section boundaries (paper to ink to accent) to mark structure.
- No gradients on text. Background gradients only as a subtle atmospheric layer, never purple to blue.

## 7. Images and brand books

- Use images from the user's sources first (screenshots, figures from the paper, product shots). Copy them next to the deck and reference them relatively.
- Stock photography (Unsplash) only when the user agrees. Credit the photographer in the slide notes. Never imply a stock photo shows the user's product or people.
- Never put text over a busy image without a solid or scrimmed panel.
- Brand book or brand site provided: extract its tokens (colors, faces, logo, voice rules) into `:root`, record them in brief.json under `brand`, and let the brand override the direction. Keep the layout ambition.
