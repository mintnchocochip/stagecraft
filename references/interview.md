# The aesthetic interview

Run it after a quick skim of the sources and before any slide code. The point is to commit to a concept, an audience, and a
look with the user, so the build has a target. Ask everything in one round. Use the AskUserQuestion tool when available
(up to 4 questions per call, so use two calls back to back if needed); otherwise send one numbered message.

Do not ask what you can already tell from the request or the sources. If the user already said "10 slides for the board",
do not ask length or audience. If they said "just build it" or gave all answers, skip the interview and state your
assumptions in one short paragraph before building.

## Round 1 (always)

1. **Core concept.** Draft the one-sentence thesis from the sources and offer it plus one alternative angle. "Which story are we telling?"
   - e.g. "The allowlist closed the last bypass without slowing the agent" / "How the agent decides when to stop"
2. **Audience and setting.** Who is in the room and how it is consumed. Options tailored to the material, for example:
   - Live talk, speaker-led (low text, big moments)
   - Team review, read along (more self-contained slides)
   - Sent as a file and read alone (reading deck, denser, notes become body copy)
   - Investors or executives (outcome first)
3. **Moodboard direction.** Offer three directions from design.md that fit, each with a one-line feel and its fonts and colors,
   plus "Use my brand or moodboard" (they can paste a URL, brand book, screenshots, or adjectives). Make the three genuinely
   different: one restrained, one bold, one unexpected for the topic.
4. **Format and motion.** HTML deck (default), PPTX (editable in PowerPoint), or both. Default motion level: Minimal, Smooth,
   Cinematic, or Insane (the viewer can switch live in HTML).

## Round 2 (only when needed)

- Length or time slot, if not given.
- Must-include and must-avoid items (a slide the boss expects, a number that is sensitive).
- Images: use screenshots or figures from the sources, allow Unsplash photos, or no photos.
- Source policy: strict (only their material, the default) or augment (allowed to add outside context, marked for verification).

## Optional: show, do not tell

If the user is unsure about the look, or asks to see options, build three one-slide cover previews (same title, three
directions) as a mini deck at `presentations/<slug>/directions.src.html` with three `poster` slides, build it, take a
snapshot, and show the contact sheet. Let them pick or mix. Preview slides use real deck content, never labels like
"Option A" or "Style preview" on the slide itself.

## After the interview

Write brief.json (content.md), then show the outline: numbered titles, one line on what each proves, layout name, and key
visual. Ask for a yes or edits. This is the last checkpoint before the build unless the user wants to see a draft early.
