# Voice: how slide text and notes read

Slides are read in two seconds from across a room. Notes are spoken aloud. Both should sound like a sharp person who knows
the material, talking to this audience. The build enforces the hard rules; the rest is on you.

## Hard rules (the build fails on these)

- No em dashes, en dashes, or spaced hyphens used as dashes. Not in titles, body, notes, tooltips, or alt text.
  Rewrite: two sentences, a comma, a colon, or parentheses. Ranges become "2019 to 2024" or "3 to 5".
- No emoji.
- No number that is not in the claim ledger.

## Sentence shape

- Short declarative sentences. Subject, verb, object. One idea each. Under 16 words on slides, under 24 in notes.
- Active voice. "The guardrail rejects the request", not "The request is rejected by the guardrail".
- No stacked clauses, no semicolon chains, no rhetorical questions as titles, no exclamation marks.
- No "it's not X, it's Y", "not just X but Y", "more than just". Say what it is.
- No triads for rhythm ("fast, simple, and powerful"). If there are really three things, list them plainly.
- Concrete over abstract. Name the file, the number, the person, the step.
- Keep the source's hedges. "~20%" or "an estimated 20%" becomes "about 20%" or "est. 20%", never a bare "20%".

## Vocabulary matched to the room

Decide the register from the audience and record it in brief.json `register`. Then hold it on every slide.

| audience | register | sounds like |
|---|---|---|
| engineers | technical, exact | "The allowlist parses argv before the shell sees it." Identifiers in mono, real names. |
| executives | outcome first | "Shipping this removes the last known bypass." Plain words, the decision, the cost. |
| researchers | precise, hedged where the source hedges | "Accuracy rose 4.1 points on the held-out set (Table 2)." Keep the paper's terms. |
| students | plain, stepwise | "First the request arrives. Then the agent checks it." Define a term the first time. |
| general public | everyday words | Replace jargon with what it does. One number per slide. |

Use the source's own terms for its own concepts. Do not rename a module, metric, or method to sound nicer.

## Banned words and phrases

delve, leverage, seamless, unlock, elevate, game-changer, revolutionize, tapestry, realm, harness the power, cutting-edge,
fast-paced, ever-evolving, landscape, empower, supercharge, next-level, embark, testament, paradigm shift, synergy, robust
solution, in today's world, dive into, deep dive, let's explore, at the end of the day, it's worth noting, furthermore,
moreover, in conclusion, a myriad of, plethora, transformative, unleash, journey, holistic, best-in-class, world-class,
state-of-the-art, mission-critical, pivotal, crucial role, navigate the.

The build warns on these. If the source itself uses one as a proper term (a product called Landscape), keep it.

## Titles

- A title is the claim of the slide in one line: "Retries fell 38% after the allowlist". Readers who see only titles should get the argument.
- 3 to 9 words. Sentence case. A period is fine on statement slides.
- Never: Overview, Introduction, Agenda, Background, Key Takeaways, Conclusion, Summary, Thank You, Q&A.

## Notes

Two to five sentences per slide. What to say, what to point at, what to click. Same voice rules. Notes can carry detail that
does not fit on the slide, still grounded in the ledger.
