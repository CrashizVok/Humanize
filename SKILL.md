---
name: humanize
description: |
  Make generated text read as if a person wrote it, in English or Hungarian.
  Works two ways: as a one-shot rewrite of a text or file, and as a persistent
  mode that stays on for the rest of the session and applies to every piece of
  human-read prose after it (documents, speeches, blog posts, emails, chat
  replies, PR descriptions). Use when asked to humanize, de-AI, rewrite so it
  does not sound like AI, "emberszerű", "ne legyen AI-ízű", or when /humanize is
  invoked. Fixes structural tells (thematic over-explaining, tidy causal chains,
  linear time, no named sources, no reader address) before surface tells (stock
  AI words, em dashes, rule of three, bold-label lists).
license: MIT
metadata:
  version: "1.0.0"
---

# Humanize

Two layers, in this order: **structure first, surface second.**

That order is the whole point of this skill. Chakrabarty et al.'s LAMP framework rewrites
AI text span by span to strip clichés, redundant exposition and purple prose. When the
STORYSCOPE authors ran it over AI stories, a classifier that sees only *narrative* features
(no style features at all) still caught them: 95.5% macro-F1 before the edit, 93.9% after.
A thorough surface pass moved the needle 1.6 points. The structural decisions are what
survive, so they are what this skill fixes first.

Source: "What Makes a Story Human?" (STORYSCOPE, COLM 2026) — 10,272 prompts, 61,608 stories,
six sources, 304 induced narrative features, 30 of them stable human-vs-AI markers.

## What this does not claim

This makes text read like a person wrote it. It does not make text undetectable, and it should
not be sold that way: in the same paper, supervised detectors on raw text hit 99.7–99.9%
macro-F1. If someone needs a guarantee about a detector, the honest answer is that nobody has one.

The paper measured **fiction** — short stories averaging 4,753 words. Every number quoted in
`references/narrative-structure.md` comes from that setting. The application to documents,
speeches and emails is an extension, marked as such there. Do not present the extension as a
measured result.

## Invocation

| Input | Behavior |
|---|---|
| `/humanize` (no argument), or "kapcsold be", "apply to everything from now on" | Turn the persistent mode **on**: write `.claude/.humanize-mode`, then confirm in one line. |
| `/humanize off`, "kapcsold ki", "stop humanizing" | Turn it **off**. Trim and lower-case the argument first: `off`, ` off`, `OFF`, `ki`, `stop` all mean off. |
| `/humanize <text>` | One-shot rewrite of that text. Return the rewrite and a short list of what was left alone and why. Mode state is untouched. |
| `/humanize <path>` | One-shot rewrite of that file, written back in place. Prose only: code blocks, YAML frontmatter, data, command output and link targets stay byte-identical. Then summarize what changed. |
| `/humanize status` | Report whether the mode is on, and print the state file. |

The switch is one script, and it is the only way to change or read the mode:

```sh
sh .claude/skills/humanize/scripts/mode.sh on
sh .claude/skills/humanize/scripts/mode.sh off
sh .claude/skills/humanize/scripts/mode.sh status
```

It prints `humanize mode: on` or `humanize mode: off`, always exits 0, and reports the state it
read back rather than the change it attempted. **Report what it printed, never what you asked
for.** Do not hand-roll the shell for this. Two live test rounds both ended with
"Failed to disable persistent humanize mode" next to a claim that the mode was off, because the
off path was a bare shell line and any part of it exiting non-zero looked like a failed switch.
Turning the mode off while telling the user it is off, or the reverse, is the worst bug this
skill can have: it decides whether everything they write next runs under these rules.

While the state file exists and its first line starts with `on`, a `UserPromptSubmit` hook
(`.claude/hooks/humanize-guard.sh`) reinjects `ACTIVE.md` on every turn, so the mode survives a
long session instead of fading. The file is gitignored: it is session state, not repository
content.

## Scope when the mode is on

**In scope:** anything a person reads as writing. Chat replies, documents, speeches and talks,
blog drafts, emails, release notes, PR and commit descriptions, report text, UI copy.

**Out of scope, left exactly as it is:** code, identifiers, comments inside code, config files,
JSON/YAML data, shell commands, test output, log lines, quoted material, file paths, and any
text the user supplied. Do not "improve" a quotation.

**Never overridden by this skill:** the repository's own conventions in `CLAUDE.md`, a house
style the user names, and the four rules below.

## Four rules above both layers

1. **Invent nothing.** No fact, name, number, date, quote, citation or source that is not in the
   source text or from the user. If a sentence needs a detail you do not have, ask or write a
   simpler sentence. Fiction is exempt, because inventing is the task there.
2. **Lose nothing.** You may cut dull passages, expand useful ones, merge or split paragraphs,
   and reorder freely. Every claim that went in comes out.
3. **Match the writer.** If the user provides a sample of their own writing, read it first and
   copy its habits: sentence length, word choice, punctuation, how paragraphs open. A sample
   beats every style rule here, including the dash rule.
4. **Personality only where it belongs.** Blog posts, essays, speeches, opinion: yes. Reference
   docs, legal text, security findings, API documentation: no. A humanized compliance sentence
   that gained a wink is worse than the original.

## Context check, before you write

Everything in Layer 1 pushes toward the specific: name the vendor, the version, the date, the
incident. That is the right direction, and it is also where this skill does its worst damage,
because when the specific thing is missing, supplying one is the smoothest move available. In
testing it supplied a customer whose DMARC dropped from reject to none during a Cloudflare
migration, caught three weeks later. None of it happened, and it reached a LinkedIn draft as a
statement about our own track record.

The fix is not another prohibition. It is having somewhere else to go. **Settle the specifics
before the draft, by asking.**

### Take inventory first

Before writing anything aimed at another reader — a post, an email, a speech, a document, a blog
draft, a talk — list what the piece needs that you do not already have:

- a number, a rate, a duration, a percentage
- a customer, a company, a person, a team
- an incident, a migration, an outage, a conversation, a "we once had a case where…"
- a date, a version, a release, a commit
- a source for any claim you are about to attribute to someone

For each one, point at where it comes from: the user's message, a file in this repository, a
document they gave you. Anything you cannot point at is missing.

### Then work the ladder

If something missing is **load-bearing** — the piece is weaker or dishonest without it — stop
before writing and go down these rungs in order. Do not skip a rung, and do not jump to the
bottom one because it is quicker.

**1. Offer to look it up.** Ask in one short block, at most four items, and say where you would
look: this repository, the files the user has given you, and the web if this session has search.
If it has neither, say so instead of implying you could have checked.

> A posztnak kellene egy valós eset. Utánanézzek a repóban és a neten, vagy megadod te?

**2. If they say yes, search, then report and stop.** Do not roll the findings straight into a
draft. List what you found, each with where it came from and a link where there is one, and say
plainly which parts are still missing. Then wait. The user approves the facts, and only the
approved ones go into the piece.

> Ezt találtam: … (forrás: …). Ezt nem találtam: … Jó így, vagy pontosítasz?

**2b. Never swap the ask silently.** The search often turns up something real and adjacent
rather than the thing that was asked for: a public vendor incident where a customer case was
wanted, a study of a different population, last year's figure. Adjacent and real beats invented,
so offer it — and say that it is a substitute, in the same breath. Observed in testing: asked for
a real customer case, a draft went straight to a documented Proofpoint DNS outage, correct in
every detail and checkable. Good judgement, no invention, and the user was never told the piece
had stopped being about their customers.

**3. If they reject what you found, or the search comes back empty, ask them for the facts.**
Directly, naming what you need. Do not treat a failed search as permission to fill the gap
yourself: a rejected finding and an invented one are the same sentence to the reader.

**4. If they have nothing and still want the piece, say what you are about to invent, before
you write it.** Two or three sentences, plain: this is the backstory I will use, these are the
numbers, none of it happened. Then write the piece with it. The announcement is the whole point
of this rung. An invented example the user chose, with their eyes open, is a legitimate draft;
the same example arriving unannounced inside finished text is the failure this skill exists to
stop.

> Nincs valós eset, szóval ezt találom ki: egy középvállalat DNS-migráció közben elveszti az
> MX-rekordját, két napig nem jön levél, a monitorozás szúrja ki. Ez kitalált. Megírom vele?

One line stays true on rung 4: the finished text may not name a real company, customer or person
as having lived through something invented. Keep it unnamed, or keep it openly hypothetical. If
the piece is going out publicly as a true story, say once that it is invented and let the user
decide; say it once, not three times, and then do as they ask.

Ask once per piece, up front, not question by question as you write. A draft interrupted four
times is worse than one clear question before it starts.

**Do not start the ladder** when the detail is decorative rather than load-bearing, when the user
already gave you the material, when it is a chat reply in a conversation you are both already
inside, or when the piece is explicitly fiction, a hypothetical, or a template. Asking about
everything is its own failure: it trains the user to wave you through, and then the guard is gone.

### If they never answer

Three exits, all honest, in this order: cut the claim and write around the mechanism; write it
openly as a hypothetical in the text itself, where "suppose a team rotates a key" reads as the
invention it is and "one customer rotated a key" does not; or leave a visible marker,
`[[? valós ügyfélpélda kell ide]]`, and list every marker under the draft.

Never the fourth thing, which is writing a plausible version and moving on.

### Markers during the draft

A gap that appears mid-draft does not warrant a new question. Drop a `[[? … ]]` marker, keep
writing, and collect the markers at the end. They are deliberately ugly so they cannot be missed,
and `humanize-check.py` flags any that survive into a finished file.

## Layer 1 — structure

Read `references/narrative-structure.md` before rewriting anything longer than a paragraph.
It holds the 30 core features with human/AI means, grouped into ten themes, each with a directive.

The six questions to answer about a draft, in order:

1. **Does it state its own point?** AI narrators spell out the theme 77% of the time; humans 52%.
   Cut the sentence that tells the reader what the previous paragraph meant.
2. **Is the causal chain too clean?** AI stories run tighter chains (4.20 vs 3.92 on a 1–5 scale),
   resolve through the protagonist's own choice 69% of the time (humans 46%), and carry no subplot
   79% of the time (humans 57%). Put back the dead end, the external cause, the second thread.
3. **Does anything get named?** Humans make specific, named references at nearly twice the AI rate
   (47% vs 24%). Name the RFC, the CVE, the version, the vendor, the date, the actual street.
   "Industry reports suggest" is the AI default.

   This directive has one failure mode, and it is the worst one in the skill: reaching for a
   name you do not have. A vague claim that you cannot source gets **cut**, never furnished with
   a plausible company, timeframe or statistic. Rule 1 wins every time the two pull apart, and
   they pull apart constantly, because the easiest way to satisfy "name it" is to make one up.

   Whole events count, not only names and numbers. A customer, an incident, a migration, a
   conversation, "we had a team that…" — if it did not happen, it cannot be asserted as though
   it did, however well it illustrates the point. An invented anecdote is harder to catch than
   an invented statistic because it carries no figure to check, and it does more damage, because
   it reaches readers as a claim about your own track record. This was observed twice in testing:
   a customer incident made up for a conference talk came back three prompts later, stated as
   fact, in a LinkedIn post. **An example you invented earlier in this conversation is not
   thereby sourced.** When a piece needs an illustration you do not have, write it as the
   hypothetical it is, or ask the user for a real one.
4. **Is the reader in the room?** Humans address the reader directly 28% of the time; AI 7%.
   One direct address or aside, where it fits.
5. **Does time run straight?** Humans use more time jumps (2.40 vs 2.12) and more revelations that
   force a re-read of what came before (3.28 vs 2.95). Start at the symptom, not the definition.
6. **Was every choice the obvious one?** Human stories sit in sparser regions of narrative feature
   space (mean rarity percentile 0.71 vs 0.49, Cohen's d 0.83). Find two structural defaults in
   your draft and move them to a less common option that is still true.

## Layer 2 — surface

`references/surface-patterns.md` holds the 35 numbered patterns from Wikipedia's "Signs of AI
writing" (WikiProject AI Cleanup), plus the burstiness rules from
`marketing/prompts/blog-humanize-pass2.md`. Run it after the structural pass, not instead of it.

One of those rules is applied wrong often enough to call out here. **Rhythm means vary, not
shorten.** Cutting the long sentences without writing any short ones collapses everything toward
the middle, which is the exact even, mid-length cadence that marks AI prose: you remove the
symptom the checker counts and deepen the one a reader hears. Measured on one matched pair in
testing, the humanized draft dropped from a sentence-length standard deviation of 10.1 to 5.4 and
from one sentence under eight words to none, while the mean fell from 24.5 words to 18.4. Every
long sentence had been tidied and nothing short was put back. A section wants both: something
under eight words and something over twenty-five, and the gap between them is the point.

It also holds the false-positive list. Read that part. Perfect grammar is not a tell, a single
em dash is not a tell, and a formal word is not a tell. Over-editing good writing is a failure
mode of this skill, not a safe default.

## Language

`references/hungarian.md` covers what the English rules miss in Hungarian, and reverses the ones
that do not transfer. The dash ban in surface pattern §14 is English-only: in Hungarian the
gondolatjel (–) is correct punctuation and the quotation marks are „ ”. Match the language of the
text being written, not the language of the request.

## Output format

`references/formats.md` has the per-format rules. Speech and documents differ more than they look:
repetition that is a tell in prose is structure in a speech, and a parenthesis that reads fine on
a page cannot be said out loud.

## The gate

Before returning any text, answer three questions. In persistent mode, answer them silently.

1. **What still reads as AI?** Name it or state that nothing does.
2. **Did the rewrite add or drop a fact, name, number, date, quote, citation or ranking?**
   Any addition or loss is an error, not a style choice. Go through every proper noun, number
   and date in the output one at a time and point to where it came from. A name you cannot trace
   to the source, the repository or the user is invented, however reasonable it sounds.
3. **Which of the six structural questions did this draft fail before the rewrite, and does it
   still fail any?**
4. **Does every item in every list have its own source?** Point at each one separately and name
   where it comes from. A list is where an invented item hides best, because the true members
   either side of it carry it through: observed in testing as "the exact record to paste, the
   host, the TTL", where record and host are real fields and TTL is not. If the real list has
   two items, write two.
5. **Does every clause say something?** Read each one alone and expand it into a full sentence
   without guessing what was meant. A clause that only works because you know the intention is
   not writing, it is a placeholder that reads like writing. This is the one failure that
   survives both layers and a fact-check, because there is nothing in it to be wrong about:
   observed in testing as the tagline "NIS2-ready DNS & email security audits, no enterprise
   price", where every word is true and the last three say nothing. Watch for it hardest
   wherever a character limit is forcing two ideas into one line.

**For a speech or a talk, running the checker is not optional.** Four test rounds asked for a
60-second talk, and four times the closing announced its own point: "Ez a lényeg:" at the end,
the same sentence moved to the middle, "Szóval a DMARC nem egy pipa a listán", then "És itt a
lényeg:" three words into the last paragraph. Each round added a paragraph of guidance and the
next round wrote it again. Instructions are not getting this one, so the talk goes through the
checker before it is returned, and a `closing` flag means rewrite the ending rather than explain
it. Run it on the text you are about to hand over:

For a measurable check on the surface layer:

```sh
python3 .claude/skills/humanize/scripts/humanize-check.py --lang en path/to/file.md
python3 .claude/skills/humanize/scripts/humanize-check.py --lang hu --format speech talk.md
```

`--format speech` drops the long-sentence requirement and the triple check, both of which invert
when the text is spoken. Without it the checker calls a well-paced talk under-written.

It is a hint generator, not a verdict. It flags dashes, stock words, bold-label lists, title-case
headings, "not just X but Y", forced triples, and low sentence-length variance. It cannot see the
structural layer at all, so a clean report is not a pass.

## How to return the result

- **Pasted text:** the rewrite, then a short note on what was left alone and why.
- **File:** write the final text only; summarize afterwards in chat.
- **Persistent mode:** just write well. No commentary, no announcement, no "here is the humanized
  version". The mode is not a topic of conversation.
- **Embedded in another task** (a commit message, a PR body, a doc a skill is producing):
  final text only.

## Related

- `.claude/skills/humanizer/` — the vendored blader/humanizer plugin (MIT). Surface layer only.
  This skill's `references/surface-patterns.md` is derived from it. Leave that directory alone;
  it has its own version history and validation script.
- `marketing/prompts/blog-humanize-pass2.md` — the ZeroHook blog voice pass, referenced from
  `references/formats.md` rather than copied.
