# Output formats

The structural layer is the same everywhere. What changes is which surface rules apply, and a few
of them invert. A speech and a reference doc fail in opposite directions.

## Speech and talks

The text will be heard once, at someone else's pace, with no way to re-read. That changes the
rules more than any other format.

**What inverts:**

- **Repetition is structure, not a tell.** Prose §11 says to fix repeated sentence openings. In a
  speech, a repeated opening is how an audience knows a list is a list. Keep it, use it
  deliberately, and use it three or four times rather than twice.
- **Short sentences stop being dramatic fragments.** §31 warns about a row of clipped sentences.
  Spoken, that row is pacing. The real limit is the breath: if you cannot say a sentence in one
  breath, split it.
- **The rule-of-three ban relaxes.** §10 exists because AI forces triples in prose. Spoken
  rhetoric has used the triple for two thousand years. One per speech, landed properly, is fine.

**What gets stricter:**

- No parentheses. They cannot be spoken. Make it a separate sentence or cut it.
- No dashes of any kind: a speaker has a pause, not a punctuation mark. Write the pause as a
  sentence break.
- No bullet lists in the delivered text. Write "three things go wrong here. First, ..." Nobody
  hears a hyphen.
- Numbers get spoken and rounded. "Roughly a third" beats "34.7%" unless the precision is the
  point. Write the number the way it is said.
- No nested clauses. The listener cannot go back to find the subject.

**What to add:**

- Name the room. The occasion, the person who spoke before, the thing everybody in the audience
  already knows. This is the speech version of the "reader is in the room" signal, and it is the
  single fastest way to make a talk stop sounding generated.
- Say the plain emotional word. "This part was genuinely annoying" lands; a rendered physical
  metaphor does not survive being spoken aloud.
- Name real things: the date, the customer, the version, the number that was wrong.

**What to cut:** the opening that explains what the talk will cover, and the closing that
summarizes what it covered. Both are AI thematic over-determination wearing a lanyard.

Watch for it moving rather than leaving. Across three test rounds the same closing survived
three rewrites: "Ez a lényeg:" at the end, then the same sentence relocated to the second
paragraph, then "Szóval a DMARC nem egy pipa a listán" back at the end, each time alongside a
metaphor doing the summarizing ("a céged mail-infrastruktúrájának a tükre"). Prose about it did
not shift the behaviour, so here is the mechanical version: **the last paragraph may not open
with Szóval, Tehát, Ez a lényeg, A lényeg, So, The point is or The takeaway.** End on the last
concrete thing you said, or on a question to the room. `humanize-check.py` flags that opening
and the saying-shaped claim beside it.

## Documents

- Headings in sentence case (§17).
- No bold-label bullet lists (§16). If a list needs labels, it needs a table.
- No "Conclusion" or "Summary" section that restates the body. End on the last real point.
- No "Key takeaways" box duplicating what the reader just read.
- Tables get a caption that says what the reader should notice, not a restatement of the title.
- Terminology stays fixed. §11 warns against synonym cycling in prose; in a technical document it
  is worse than a style problem, because two names for one thing reads as two things.
- Keep personality out. Rule 4 in `SKILL.md`: reference, legal, security and API text stays
  neutral. A humanized compliance sentence that gained a wink is worse than the original.

For documents in this repository, `CLAUDE.md`'s own conventions win over anything here.

## Blog posts

Use `marketing/prompts/blog-humanize-pass2.md`. It has the ZeroHook-specific constraints that are
not in this skill: the required section labels, the metadata header, the Meta Description limit of
150 characters, the practitioner "we" voice, and the cover image prompt. Apply the structural
layer first, then that prompt's rules, then the surface layer for anything it does not cover.

The `content-pipeline` skill already calls that prompt as part of the draft flow.

## Email

- The subject line is the one place where the surface layer matters most and the structural layer
  barely applies. Write it last, from the actual content.
- No "I hope this email finds you well" (§20). No "I wanted to reach out" as an opener.
- One ask, stated plainly, in the first three lines.
- Cold outreach has its own rules in `.claude/prompts/` via `/outreach`. This skill does not
  override them.

## Chat replies

When the persistent mode is on, chat replies are in scope. What that means in practice:

- Answer the question, then stop. No summary of the answer.
- No "Great question", no "You're absolutely right" (§22).
- No offering three follow-ups the user did not ask for.
- Do not announce that the mode is on or that you are applying it.
- Technical accuracy and directness still win over voice. If a plain terse answer is right, that
  is the humanized answer.

## PR and commit descriptions

- Say what changed and why, in the order a reviewer needs it.
- No "This PR introduces a comprehensive refactor that enhances...".
- The structural rule that matters here is naming: the issue number, the failing test, the version,
  the specific behavior that was wrong.
- Repository conventions for attribution footers and templates win over this skill.

## Where the context check matters most

Anything that leaves the building carries a claim about us, so the inventory in `SKILL.md` is not
optional for a LinkedIn post, a cold email, a talk, a customer-facing document or a blog draft.
An invented incident in a chat reply is a mistake you catch on the next line. The same sentence
in a published post is a claim about our own track record, made to people who cannot check it.
Ask before drafting those, every time the piece leans on a specific case you do not have.

## Never in scope

Code, identifiers, comments inside code, config files, JSON and YAML data, shell commands, test
output, log lines, file paths, quoted material, and any text the user supplied. Humanizing a
quotation falsifies it.
