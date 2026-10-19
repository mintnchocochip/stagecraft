# Motion: levels, vocabulary, choreography

The engine does the animation. You tag elements and choose where motion goes. Do not hand-write GSAP for things the
vocabulary covers: the presets are tuned per level, respect reduced motion, and always land on the authored layout.

## The five levels

The viewer can switch live with `M` (Shift+M goes back) or the HUD in the bottom-right. `?motion=N` in the URL forces a
level. The deck's default is `<body data-motion="N">`. Pick the default from the interview; the audience can still change it.

| level | name | slide cut | element motion | extras |
|---|---|---|---|---|
| 0 | Still | hard cut | none, everything visible | for print, PDF, screen readers, reduced motion |
| 1 | Minimal | crossfade 0.45s | short fades | |
| 2 | Smooth | slide and fade 0.85s, parallax layers | line masks, staggers, drawn SVG, growing bars, counting numbers, marching dashes | the sensible default for most rooms |
| 3 | Cinematic | clip-path wipe 1.0s (or `data-transition`) | blur-in, rotated line masks, char reveals, scramble, image zoom-in masks | canvas fx, packets on flow paths, cursor parallax, tilt |
| 4 | Insane | rotates shutter, iris, wipe, zoom (or `data-transition`) | word and char choreography in 3D, elastic grows, pop with overshoot | stronger fx, cursor-reactive fields, magnetic elements |

Without GSAP (offline without `--offline`) the engine caps at Minimal and the deck still works.

## Vocabulary

On any element inside a slide:

| attribute | effect |
|---|---|
| `data-anim="fade"` | fade, rising and de-blurring at higher levels |
| `data-anim="lines"` | line-by-line mask reveal (SplitText). Use on headings and short paragraphs. |
| `data-anim="chars"` | per-character reveal from level 3, lines below that. Short display text only (under 30 characters). |
| `data-anim="scramble"` | text decodes from random glyphs from level 3. Plain text only, no child elements. |
| `data-anim="stagger"` | the element's children enter one by one. Lists, rows, nav, meta rows. |
| `data-anim="mask"` + `data-from="left|right|top|bottom"` | clip-path reveal of a block or image; inner image settles from a zoom at level 3+ |
| `data-anim="draw"` | every stroked SVG shape inside draws itself. Diagrams, line charts, underlines. |
| `data-anim="grow"` + `data-axis="x"` | bars grow from their baseline (children, or the element itself) |
| `data-anim="pop"` | children scale in with overshoot. Diagram nodes, markers, small tiles. |
| `data-anim="count"` | `[data-count]` numbers count up. Write the final value as the text too. |
| `data-delay="0.6"` | start time in seconds from slide entry (otherwise the engine cascades in DOM order) |
| `data-dur="1.4"` | override duration |
| `data-min="3"` | only animate at this level or higher; below it the element just appears |
| `data-step="1"` | hidden until the presenter clicks (like a PowerPoint build). Numbers order the builds. |
| `data-depth="0.4"` | parallax layer. Moves with transitions and the cursor (0.1 subtle, 0.6 strong). |
| `data-bleed` | intentionally extends past the slide edge; the audit ignores it |
| `data-deco` | decorative text (folios, ornament numerals); skipped by lint grounding and audit overlap |

Count example: `<span data-count="42.5" data-suffix="%" data-decimals="1">42.5%</span>`. Also `data-prefix`, `data-from`.

On the slide `<section>`:

| attribute | effect |
|---|---|
| `data-transition="wipe|iris|shutter|zoom|slide|fade"` | cut used when entering this slide at level 3+ |
| `data-fx="dotgrid|constellation|flowfield|grain"` | canvas layer from level 3. Color comes from `--fx` then `--accent` on the slide. |

## Choreography rules

1. **One hero move per slide.** Decide what the eye should land on first and give it the biggest motion. Everything else is quieter and later.
2. **Order follows reading order.** Kicker, then headline, then body, then the visual's details. Use `data-delay` to hold supporting copy until the headline has landed (0.5 to 0.9s).
3. **Five to eight animated elements per slide, at most.** Animate groups (`stagger` on the parent), not every leaf. Lint warns above nine.
4. **Match motion to meaning.** `draw` for things that connect, `grow` for quantities, `count` for one headline number, `mask` for reveals of images or panels, `scramble` for codes and identifiers, `chars` for a title that deserves a moment.
5. **Transitions mark structure.** Keep the default cut inside a section; set a distinct `data-transition` (shutter, iris) on section openers and the closing slide.
6. **fx is seasoning.** Two or three slides per deck at most: the cover, a section opener, the close. Never behind dense text.
7. **Steps are for the presenter.** Use `data-step` when the speaker needs to talk before the next idea appears: a second point, a diagram's second half, the answer to a question.

## Custom motion (bespoke components)

When the vocabulary cannot express a component (a token stream, a queue filling, a state machine stepping), register a hook.
Hooks are keyed by the slide's `id` (not a component name). It runs on slide entry with the current level and gsap (which may be null).

```html
<script>
window.KX_ENTER = window.KX_ENTER || {};
// <section class="slide" id="retry-loop"> ... </section>
window.KX_ENTER['retry-loop'] = (slide, level, gsap) => {
  const dots = slide.querySelectorAll('.attempt');
  if (level === 0 || !gsap) { dots.forEach(d => d.classList.add('done')); return; }   // final static state
  const tl = gsap.timeline();
  dots.forEach((d, i) => tl.to(d, { backgroundColor: 'var(--accent)', duration: 0.3 }, i * (level >= 3 ? 0.35 : 0.2)));
  return tl;                    // or return a cleanup function if you start intervals / rAF loops
};
</script>
```

Static screenshots, PDF and the audit render every `data-step` revealed at once, at level 0. A timer watchdog finishes
any animation the browser did not get to run (background tabs), so content never stays hidden.

Rules for hooks: level 0 must produce the final state (screenshots, PDF and the audit use it). Scale intensity with
`level`. Return a timeline so the engine can finish it on navigation, or a cleanup function that stops loops. Put hooks in
one `<script>` before `</body>` of the source file; build.py injects the engine after it.
