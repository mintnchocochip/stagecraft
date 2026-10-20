# Motion: design it per deck

Motion is part of the design system, like type and color. Two decks about different subjects must not move the same way.
The engine gives you plumbing (levels, timing, steps, safe end states) and a set of presets. The presets are the
supporting cast for small things. The moves people remember are designed by you, for this subject, every time.

If a viewer could swap the motion between two of your decks and nobody would notice, the motion was a template.

## 1. Write the motion concept first

Before writing slides, add a `motion` block to brief.json. The build warns without it, and at Cinematic or Insane it
fails if the deck uses presets only.

```json
"motion": {
  "concept": "Slots that empty and refill. Things drop into gaps and settle with a small bounce, like an appointment landing in a calendar.",
  "feel": "quick, physical, a little playful; ease back.out and power3, durations 0.5 to 0.9s",
  "cut": "refill: the old slide drops out of its row, the new one falls into place from above",
  "signatures": [
    "cover: the word Filled drops into an empty outlined slot",
    "61% slide: the bar fills from the before value, then the number lands",
    "team: names slot into a grid one by one"
  ],
  "still": "body copy and source chips never move beyond a short fade"
}
```

Find the concept in the material, not in a list of effects. Ask:

- **What moves in this world?** Packets through gates, ink on paper, cards on a board, liquid filling, a camera on a set,
  a ledger adding rows, a signal on a scope, tiles clicking into a grid, a page being redlined.
- **What is the physics?** Heavy and slow (infrastructure, finance), springy (consumer, health), precise and stepped
  (protocols, state machines), drawn by hand (research, lab notes), glitchy (security, only if earned).
- **What is the one transformation the talk is about?** Before to after, empty to full, chaos to order, one to many.
  Make that transformation the signature move and use it at the two or three moments that matter.

Pick an ease family and a tempo for the deck and keep them. Snappy decks use `power3`/`power4` and `back.out` with short
durations. Calm decks use `expo.out` and `sine.inOut` with long durations. Mechanical decks use `steps(n)` or `power2.inOut`
with holds. Do not mix families without a reason.

## 2. Tools for authored motion

Use these for every hero moment. They respect the level selector, so design once at full strength.

### data-move: a declarative bespoke move

```html
<h1 data-move='{"y":160,"rotate":-4,"split":"words","stagger":0.06,"ease":"back.out(1.4)","dur":0.9}'>Empty slot. Filled.</h1>
<ul data-move='{"x":-80,"split":"children","stagger":0.12,"ease":"power3.out"}'>...</ul>
```

Any GSAP from-vars work (`x`, `y`, `xPercent`, `rotate`, `rotateX`, `scale`, `skewX`, `filter`, `transformOrigin`,
`clipPath`...). `split` is `lines`, `words`, `chars` or `children`. Opacity starts at 0 unless you set it. Distances,
angles and scale are authored for Insane and scaled down per level (Smooth gets half). Below Smooth it is a fade.

### data-keep: the same thing on two slides

Give an element on slide N and an element on slide N+1 the same `data-keep="id"`. On the cut, the new one travels from
the old one's box to its own (size and position). Use it for continuity: the big number shrinks into a chart label, the
diagram node grows into the next slide's headline, the logo moves to the corner. The slide cut becomes a fade unless the
slide sets `data-transition`. Do not also give the kept element a `data-anim`.

### KX_CUT: the deck's own slide transition

Set the default cut on `<body data-cut="name">` and override per slide with `data-transition="name"`. Write the cut once:

```html
<script>
window.KX_CUT = window.KX_CUT || {};
// The new slide falls into its row; the old one drops out below. dir is 1 forward, -1 back.
window.KX_CUT.refill = ({ from, to, dir, level, gsap, tl }) => {
  const d = [0, 0, 0.5, 0.8, 1][level];
  tl.fromTo(to, { yPercent: -40 * d * dir, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.7, ease: 'back.out(1.3)' })
    .to(from, { yPercent: 30 * d * dir, opacity: 0, duration: 0.45, ease: 'power3.in' }, 0);
  return 0.45;               // when slide content starts, as a fraction of the cut
};
</script>
```

Animate only `from` and `to` (and elements inside them, or overlays you add to `to` and remove at the end). The engine
clears transforms, clip paths and opacity on both slides when the cut ends. Custom cuts run from Smooth up; scale them by
`level`. Built-in cuts (`fade`, `slide`, `wipe`, `iris`, `zoom`, `shutter`) still exist; use one only when it fits the
concept, and never cycle through them. One deck usually needs one signature cut plus one for section openers.

### KX_ENTER: a choreographed component

For things a single tween cannot express (a queue filling, a token stream, a state machine stepping, a counter that
races and then corrects), register a hook keyed by the slide's `id`. It runs on slide entry with the level and gsap.

```html
<script>
window.KX_ENTER = window.KX_ENTER || {};
window.KX_ENTER['retry-loop'] = (slide, level, gsap) => {
  const dots = slide.querySelectorAll('.attempt');
  if (level === 0 || !gsap) { dots.forEach(d => d.classList.add('done')); return; }   // final static state
  const tl = gsap.timeline();
  dots.forEach((d, i) => tl.to(d, { backgroundColor: 'var(--accent)', duration: 0.3 }, i * (level >= 3 ? 0.35 : 0.2)));
  return tl;                    // or return a cleanup function if you start intervals or rAF loops
};
</script>
```

Hook rules: level 0 must produce the final state (screenshots, PDF and the audit use it). Scale intensity with `level`.
Return a timeline so the engine can finish it on navigation, or a cleanup function that stops loops. Put all scripts
(`KX_CUT`, `KX_ENTER`) in one `<script>` before `</body>` of the source file; build.py injects the engine after it.

## 3. Variety rules

1. **The hero move on each slide is chosen for that slide's content.** A number that is the point lands with weight. A
   process builds in its own order. A comparison moves the two sides against each other. A quote is read, not thrown.
2. **No two adjacent slides share a hero move.** Reusing the signature move at the two or three key moments is the point;
   reusing it on every slide is a template.
3. **Different decks, different signatures.** Do not carry a move from a previous deck unless the subject asks for it.
   Never default to scale-pop with overshoot, rotated line masks and a wipe on every deck.
4. **Insane is the concept at full strength, not more of the presets.** More physicality, longer arcs, more of the
   frame in motion, the cursor taking part (`data-depth`, `data-magnetic`, `data-tilt`, cursor-reactive fx). Still one
   idea. Smooth is the same idea, quieter.
5. **Restraint is a move too.** At least one moment per deck where almost nothing moves, so the big moments read.

## 4. Levels

The deck offers only the levels the user chose in the interview: `<body data-levels="0 2 4" data-motion="4">`. The
motion slider in the bottom-right lists only those levels and appears only while the pointer is over it (and briefly after
`M` changes the level). `M` cycles through the offered levels (Shift+M goes back). With one level offered, the slider is
hidden. `?motion=N` in the URL picks the nearest offered level. Still is always used for audit, static screenshots, PDF
and reduced motion, even when it is not offered. Design and test motion only for the offered levels; do not spend effort
on levels the user did not pick.

| level | name | what plays |
|---|---|---|
| 0 | Still | nothing; everything visible. Print, PDF, screen readers, reduced motion. |
| 1 | Minimal | short fades and crossfades only |
| 2 | Smooth | authored moves at half strength, presets, custom cuts, parallax on cuts |
| 3 | Cinematic | authored moves at 80%, built-in dramatic cuts if chosen, canvas fx, flow packets, cursor parallax |
| 4 | Insane | everything at full strength, cursor-reactive fx, magnetic and tilting elements |

Without GSAP (offline without `--offline`) the engine caps at Minimal and the deck still works.

## 5. Preset vocabulary (supporting cast)

Use presets for secondary elements: kickers, body copy, captions, list rows, small markers. On any element in a slide:

| attribute | effect |
|---|---|
| `data-anim="fade"` | fade, rising and de-blurring at higher levels |
| `data-anim="lines"` | line-by-line mask reveal (SplitText). Headings and short paragraphs. |
| `data-anim="chars"` | per-character reveal from level 3. Short display text only (under 30 characters). |
| `data-anim="scramble"` | text decodes from random glyphs from level 3. Plain text only. Codes and identifiers. |
| `data-anim="stagger"` | the element's children enter one by one |
| `data-anim="mask"` + `data-from="left|right|top|bottom"` | clip-path reveal of a block or image |
| `data-anim="draw"` | stroked SVG shapes draw themselves. Diagrams, line charts, underlines. |
| `data-anim="grow"` + `data-axis="x"` | bars grow from their baseline |
| `data-anim="pop"` | children scale in with overshoot. Small markers only, not whole blocks. |
| `data-anim="count"` | `[data-count]` numbers count up. Write the final value as the text too. |
| `data-delay="0.6"` | start time in seconds from slide entry (otherwise a short cascade in DOM order) |
| `data-dur="1.4"` | override duration |
| `data-min="3"` | only animate at this level or higher |
| `data-step="1"` | hidden until the presenter clicks (like a PowerPoint build). Numbers order the builds. |
| `data-depth="0.4"` | parallax layer on cuts and with the cursor (0.1 subtle, 0.6 strong) |
| `data-bleed` | intentionally extends past the slide edge; the audit ignores it |
| `data-deco` | decorative text (folios, ornament numerals); skipped by grounding and overlap checks |

Count example: `<span data-count="42.5" data-suffix="%" data-decimals="1">42.5%</span>`. Also `data-prefix`, `data-from`.

On the slide `<section>`: `data-transition="name"` (built-in or KX_CUT) and `data-fx="dotgrid|constellation|flowfield|grain"`
(canvas layer from level 3; color from `--fx`, then `--accent`). fx is seasoning: two or three slides per deck at most,
never behind dense text, and only the one that fits the concept.

## 6. Choreography basics

- One hero move per slide. Decide where the eye lands first and give that the biggest motion. Everything else is quieter and later.
- Order follows reading order. Hold supporting copy until the headline lands (`data-delay` 0.5 to 0.9s).
- Five to eight animated elements per slide at most. Animate groups, not every leaf. Lint warns above nine.
- Steps are for the presenter: use `data-step` when the speaker needs to talk before the next idea appears.
- Static screenshots, PDF and the audit render every step revealed, at level 0. A timer watchdog finishes any animation
  the browser did not run (background tabs), so content never stays hidden.
- Check the motion live, not only in snapshots: open the deck, press through it at the default level, and ask whether
  each move says something about the content.
