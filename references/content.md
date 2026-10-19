# Content: sources, the claim ledger, and the outline

The design can be wild. The content cannot. Every fact on a slide comes from a source the user gave (or approved), and
the build checks it. This is what makes two runs on the same sources say the same things.

## Source policy

Set `source_policy` in brief.json:

- `strict` (default): only the user's sources and what the user said in chat. No outside facts, no invented numbers, no
  "industry average" filler. If a slide needs a fact the sources do not have, leave it out or ask.
- `augment`: the user explicitly allowed outside knowledge ("add context", "fill gaps", "research this"). Facts from your own
  knowledge go in the ledger with a source of kind `model`. Facts from web research get a `url` source with the page as the ref.
  The build lists every `model` claim so you can tell the user what to verify.

The user's own words in chat are a source: add `{ "id": "U", "ref": "user, chat <date>", "kind": "user" }`.

## Reading sources

- **Codebase:** read the README, entry points, config, and the modules the talk is about. If the repo has a knowledge graph or
  map (graphify, a map skill, ARCHITECTURE.md), use it first. Pull real names, real numbers (limits, timeouts, counts), real
  call paths. Locator format: `path/to/file.py:120` or `file.py > function_name`.
- **Docs, markdown, notes:** quote headings and key sentences verbatim. Locator: section heading.
- **Papers (PDF):** extract text (pdftotext, pypdf, or the pdf skill). Use the paper's own figures, numbers, and wording for
  results. Locator: `p.7, Table 2` or `Section 4.2`. Never round a result differently from the paper.
- **Slides or .pptx to remake:** extract all text and notes first, then treat it as a source.
- **Web pages and videos:** only when given or allowed. Quote, with URL and timestamp or section as the locator.
- **Images:** list usable ones (screenshots, figures, logos). They are assets, not claims.

## brief.json

Write it next to the deck before any slide HTML. It is the single source of truth for content.

```json
{
  "title": "Guardrails that do not slow the agent down",
  "audience": "Backend engineers at the team review, know Python, have not read the agent code",
  "goal": "Approve shipping the curl allowlist to production",
  "source_policy": "strict",
  "register": "technical and plain; short declarative sentences; identifiers in mono",
  "format": "html",
  "motion_default": 2,
  "direction": "Terminal Noir, amber accent",
  "sources": [
    { "id": "S1", "ref": "cism/agent/guardrails.py", "kind": "code" },
    { "id": "S2", "ref": "docs/live-testing.md", "kind": "doc" },
    { "id": "U",  "ref": "user, chat 2026-10-19", "kind": "user" }
  ],
  "claims": [
    { "id": "C1", "text": "The agent caps AI turns at 12 per user turn", "source": "S1", "locator": "guardrails.py:41",
      "quote": "MAX_AI_TURNS = 12" }
  ],
  "slides": [
    { "id": "cover", "role": "cover", "title": "The allowlist closed the last bypass", "claims": [], "layout": "poster",
      "visual": "huge title, amber caret", "notes": "Open with the outcome." }
  ]
}
```

Field rules:
- `sources[].ref` is a path relative to brief.json, or a URL. `kind`: code, doc, paper, data, url, video, user, model.
- `claims[].text` is the fact in the exact wording and number format the slide will show ("1.2 s", "38%", "12 turns").
  The build checks every number that appears on a slide or in notes against claim texts and quotes.
- `claims[].quote` is copied verbatim from the source (whitespace may differ). For local text sources the build verifies the
  quote exists in the file. A paraphrase in `quote` fails the build. For PDFs and URLs, still quote exactly; the build cannot check those, so be careful.
- Derived numbers (a percentage you computed from two sourced numbers) get their own claim with `"source"` of the inputs'
  source and the arithmetic in `locator`, for example `"locator": "C3 / C4"`.
- `slides[]` is the outline. `role`: cover, point, mechanism, evidence, explain, compare, story, section, close. Every slide
  lists the claims it uses. Put the same ids in the slide's `data-claims` attribute so presenter notes show the citations.

## Outline rules

- Start from the goal: what should the audience do or believe at the end? Order slides as an argument toward it.
- Titles are assertions ("Retries dropped 38% after the allowlist"), never topics ("Results").
- One claim cluster per slide. If a slide needs more than three claims, it is two slides.
- Default lengths: lightning talk 5 to 8 slides, team review 8 to 14, conference talk 14 to 25. Respect what the user asked.
- A section opener every 4 to 6 slides in long decks. A clear close: the ask, the decision, or the one thing to remember.
  No "Thank you" or "Questions?" slide unless the user wants one; if so, make it a `statement` slide with contact or next step.
- Speaker notes on every slide: 2 to 5 sentences of what to say, written in the same voice rules as the slides.

Show the outline to the user (titles, one line each, layout, key visual) and get a yes before building the HTML. Skip this
confirmation only when the user said to go straight through.
