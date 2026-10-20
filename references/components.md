# Components: interactive diagrams, charts, and bespoke pieces

Recipes are wiring, not looks. Restyle every one with the deck's tokens and direction. `assets/example/deck.src.html`
shows several of them working together (diagram with detail rail, hover index, bar chart with tooltips, tabs).

## Contents
1. Architecture or flow diagram (clickable)
2. Bar chart (HTML)
3. Line chart (SVG)
4. Donut (SVG arcs)
5. Headline metric
6. Code walkthrough with step highlights
7. Compare toggle
8. Timeline band
9. Hover index
10. Bespoke components

## 1. Architecture or flow diagram (clickable)

SVG on the stage, nodes as `<g data-node>`, edges as paths with `data-edge` listing both ends. Clicking a node dims
unrelated nodes, lights its edges, and shows the matching `[data-detail]` panel. Esc or a second click resets.

```html
<svg class="arch" viewBox="0 0 1200 640" data-anim="draw">
  <path class="edge" data-flow data-edge="api queue"/>
  <g class="node" data-node="api" data-links="queue" transform="translate(40 100)">
    <rect width="260" height="120"/><text x="24" y="54">gateway</text><text class="sub" x="24" y="90">auth, rate limit</text>
  </g>
  <!-- more nodes -->
</svg>
<div class="rail">
  <div data-detail="default"><h3>Click a component.</h3></div>
  <div data-detail="api" hidden><h3>Gateway</h3><p>Sourced detail here.</p></div>
</div>
```

- Leave `d` off edge paths. The engine routes each edge from the facing side of one node's `rect` to the other's, so ends
  always touch. Write `d` by hand only for a custom route; the audit flags `loose-edge` when its ends miss the nodes.
- Lay nodes on a grid (multiples of 20), each as a `g` with `transform="translate(x y)"` around one `rect`. Place them so
  no straight path between linked nodes crosses a third node.
- `data-flow` gives marching dashes at level 2 and moving packets at level 3+. `data-reverse` flips direction, `data-packets="3"` and `data-speed="1.5"` tune it.
- Mark the component the talk is about with a filled node (`.hot`). One per diagram.
- Style hooks: `.node.is-focus`, `.is-dim`, `[data-edge].is-lit` (engine sets the stroke to `--accent`).
- Keep labels at 22px or larger in SVG units at the slide's scale. Ten nodes is a lot; split big systems across two slides with a zoom-in.

## 2. Bar chart (HTML)

Bars as divs sized by a CSS variable. Direct labels, no legend, no gridlines. One highlighted bar in the accent.

```html
<div class="chart">
  <div class="row"><span class="lab">p50</span><div class="track"><div class="fill" style="--v:0.42" data-anim="grow" data-axis="x" data-tip="p50 latency, 420 ms"></div></div><span class="val">420 ms</span></div>
</div>
```
```css
.fill { height: 40px; width: calc(var(--v) * 100%); background: var(--fg); }
```
`--v` is value divided by the max. Vertical bars: `height: calc(var(--v) * 100%)` inside a fixed-height track and `data-anim="grow"` without `data-axis`.

## 3. Line chart (SVG)

Compute the points yourself from the ledger values: x maps evenly across the width, y = top + (1 - (v - min) / (max - min)) * height.
Label the last point of each line directly at its end.

```html
<svg viewBox="0 0 1100 520" class="line-chart">
  <g class="axis" data-deco><line x1="0" y1="480" x2="1100" y2="480"/></g>
  <path class="series" d="M0 400 L 275 330 L 550 300 L 825 180 L 1100 120" data-anim="draw"/>
  <g data-anim="pop" data-delay="1.2"><circle cx="1100" cy="120" r="9" class="end" data-tip="Q4: 3.1 s"/></g>
  <text x="1080" y="96" text-anchor="end" class="end-label">3.1 s</text>
</svg>
```
Use `vector-effect: non-scaling-stroke` on series paths if the SVG is stretched.

## 4. Donut (SVG arcs)

Draw each segment as its own arc path so `draw` animates the segment, not the full ring. For a circle of radius r at (cx, cy),
a segment from fraction a to b runs from angle t = 2π·f - π/2: point (cx + r·cos t, cy + r·sin t). Use the large-arc flag 1
when b - a > 0.5.

```html
<svg viewBox="0 0 600 600" data-anim="draw">
  <path d="M300 60 A 240 240 0 0 1 528.3 374.2" class="seg seg-a" data-tip="Agents, 30%"/>
  <path d="M528.3 374.2 A 240 240 0 1 1 300 60" class="seg seg-b" data-tip="Humans, 70%"/>
</svg>
```
```css
.seg { fill: none; stroke-width: 72; } .seg-a { stroke: var(--accent); } .seg-b { stroke: var(--muted); }
```
Put the headline number in the hole with `count`. Two to four segments; more than that wants a bar chart.

## 5. Headline metric

```html
<div class="metric"><span data-anim="count"><span data-count="38" data-suffix="%">38%</span></span>
  <p data-anim="fade" data-delay="0.6">fewer retries after the guardrail landed</p></div>
```
One headline number per slide at 240 to 420px. If there are four numbers, use an `index` or `mosaic` layout with one dominant.

## 6. Code walkthrough with step highlights

Real code from the source, verbatim. Highlight bars are `data-step` overlays so each click moves attention.

```html
<pre class="code"><code>...verbatim lines...</code></pre>
<div class="hl" data-step="1" style="top: 212px; height: 76px"></div>
<div class="note" data-step="1"><p>The cap is checked before the model is called.</p></div>
<div class="hl" data-step="2" style="top: 340px; height: 38px"></div>
```
```css
.code { font: 400 24px/38px var(--font-mono); }  /* fixed line-height makes overlay math exact: top = pad + line * 38 */
.hl { position: absolute; left: 80px; width: 1000px; background: color-mix(in srgb, var(--accent) 22%, transparent); mix-blend-mode: multiply; }
```
Keep it to 12 to 18 lines. Elide with a comment line (`# ...`) rather than shrinking the font.

## 7. Compare toggle

```html
<div data-tabs>
  <button data-tab="before">Before</button><button data-tab="after">After</button>
  <div data-pane="before">...</div><div data-pane="after" hidden>...</div>
</div>
```
Both panes share a layout so the swap reads as a change in place. The engine animates the incoming pane.

## 8. Timeline band

A horizontal rule across the slide at y about 560. Ticks as small vertical lines with mono dates. Events alternate above and
below the band. Wrap the event list in `data-anim="stagger"` and the rule in an SVG with `data-anim="draw"`. Mark "now" with the accent.

## 9. Hover index

Rows of `<li data-hover>` containing `.kx-on-hover` detail. The detail fades in on hover and focus. On a projector, also put
the most important detail in the notes, since the audience cannot hover.

## 10. Bespoke components

Every strong deck has one or two visuals that could only exist for this content. Invent them from the source material:

- An LLM agent talk might get a token stream that fills a context window jar, a relay baton passed between agents, a loop
  that lights each phase, a cache heatmap, an autonomy dial.
- A database migration talk might get rows physically moving between two tables, a lock icon that blocks a queue.
- A paper on sampling might get a live histogram that fills as dots drop into bins.

How to build one:
1. Name the mechanism in one sentence. Draw that mechanism, not a decoration.
2. Build the final state in HTML/SVG with CSS, so level 0, PDF and screenshots show it complete.
3. Animate with the vocabulary if possible (`draw`, `stagger`, `pop`, `grow`, `data-flow`). Otherwise add a `KX_ENTER` hook (see motion.md) that respects the level.
4. Make it interactive when that helps the explanation: click to step, hover to inspect, a toggle for before and after.
5. Every label and number in it comes from the ledger.
