# Layer 1: structure

Everything in the "measured" columns comes from STORYSCOPE, "What Makes a Story Human?"
(COLM 2026): 10,272 writing prompts, each written once by a human author and once by each of
five models (Gemini 3 Flash, Kimi K2.5, DeepSeek V3.2, Claude Sonnet 4.6, GPT-5.4), giving
61,608 stories averaging 4,753 words. An LLM pipeline induced 304 narrative features grounded in
the NarraBench taxonomy; bootstrap SHAP over an XGBoost classifier picked out 30 that separate
human from AI stably across all five models. Those 30 are below.

## Why this layer exists

| Model | Features | Macro-F1 (human vs AI) |
|---|---|---|
| Narrative only (no style features at all) | 257 | 93.2% |
| Narrative + style | 304 | 96.0% |
| Style only | 39 | 85.8% |
| The 30 core narrative features alone | 30 | 84.8% |

Narrative structure alone recovers 97% of what the full model can do. And it is the part that
does not wash out: the authors ran LAMP (Chakrabarty et al. 2025, span-level removal of cliché,
redundant exposition and purple prose, with 25 few-shot examples from professional writers) over
278 AI stories, and the narrative classifier still caught them at 93.9%, down from 95.5%. A full
professional-grade surface edit cost the detector 1.6 points.

So: a lexical pass is cosmetics. Fix these first.

## The measurement, and what is extrapolation

The paper measured fiction. The **Measured** column is what it found in short stories. The
**In non-fiction** column is this skill's extension to documents, speeches, emails and posts. It
is reasoning by analogy, not a result. Where the two conflict, trust the measurement and treat
the extension as a prompt to look, not a rule to apply.

---

## AI-elevated: thematic over-determination

The single strongest cluster. AI writing explains its own meaning.

| Feature | Human | AI | Gap |
|---|---|---|---|
| Thematic explicitness and moralizing (1–5) | 3.28 | 3.94 | −0.65 |
| Moral / philosophical weighting (1–5) | 3.26 | 3.68 | −0.42 |
| Thematic unity (1–5) | 4.41 | 4.74 | −0.33 |
| Narrator explicitly comments on theme | 52% | 77% | −25 |
| Dialogue used for philosophical debate | 34% | 59% | −25 |
| References are vague implicit echoes | 50% | 72% | −22 |

**Measured:** a grieving character's arc ends with the narrator stating the lesson. Subplots and
flourishes all serve one central concern. Characters argue about meaning instead of about the
thing in front of them.

**In non-fiction:** the "why this matters" paragraph. The takeaway box that repeats the body. The
closing sentence that tells the reader what they just read. The section that exists only to tie
the piece together. The quote that is really the author's thesis in someone else's mouth.

**Directive:** cut the interpretation and keep the example. If an example does not carry the point
on its own, the example is wrong, not missing a gloss. Let one paragraph be about something that
does not serve the thesis. Thematic unity of 4.74 out of 5 is not a virtue; it is a fingerprint.

---

## AI-elevated: sensory and embodied performativity

| Feature | Human | AI | Gap |
|---|---|---|---|
| Emotion conveyed through embodied metaphor | 38% | 81% | −42 |
| Emotion conveyed through explicit labels | 29% | 8% | +21 (human) |
| Setting mirrors the character's inner state (1–5) | 3.58 | 4.07 | −0.49 |
| Environmental / ecological emphasis (1–5) | 2.83 | 3.21 | −0.38 |
| Olfactory imagery used | 57% | 82% | −26 |
| Sensory density (1–5) | 3.66 | 3.93 | −0.26 |
| Depth of interior access (1–5) | 3.67 | 3.93 | −0.26 |

**Measured:** where a human author writes that a character was afraid, AI renders fear as a
tightening chest, a cold sweat and a dimming lamp. AI reaches for smell far more often. The
weather agrees with the mood.

**In non-fiction:** the metaphor that dramatizes an ordinary technical fact. "The database
groaned under the load." The scene-setting opener about a Friday evening and cold coffee before
a post about connection pooling. Over-rendered atmosphere in a speech where a plain sentence
would land harder.

**Directive:** name the feeling in plain words some of the time. Humans do it 29% of the time and
AI 8%, so plainness is the underused option, not the lazy one. Stop making the environment agree
with the argument. Use one sense, not four.

---

## AI-elevated: structural streamlining

| Feature | Human | AI | Gap |
|---|---|---|---|
| Continuity of the main causal chain (1–5) | 3.92 | 4.20 | −0.28 |
| Resolution driven by the protagonist's choice | 46% | 69% | −23 |
| Central character introduced by external description | 30% | 52% | −22 |
| No subplots at all | 57% | 79% | −22 |
| Resolved through internal understanding | 27% | 47% | −21 |
| Pre-threat character investment (1–5) | 2.76 | 2.99 | −0.23 |
| Spatial granularity (ordinal) | 2.27 | 2.53 | −0.26 |
| Opening spatial grounding (ordinal) | 2.12 | 2.33 | −0.20 |

**Measured:** one track, no loose ends, the protagonist decides and the decision resolves it,
usually by understanding something. Everything is set up before it is needed.

**In non-fiction:** the tidy three-step incident story where the real one had a dead end and a
week of looking in the wrong place. "We identified the bottleneck and fixed it" where the truth
is a vendor changed a default and nobody noticed for six days. Every question the piece raises
gets answered inside the piece.

**Directive:** keep the wrong turn. Let an external cause do some of the work. Leave one thread
open and say so. A second thread that echoes the first is what human writing does twice as often
(thematically parallel subplots: 42% vs 21%).

---

## Human-elevated: naming things

| Feature | Human | AI | Gap |
|---|---|---|---|
| Explicit, named intertextual reference | 47% | 24% | +23 |
| Balanced mix of explicit and implicit reference | 37% | 16% | +21 |

**Measured:** humans name the book, the author, the myth. AI gestures at it. AI avoids naming
real brands, places and works.

**In non-fiction:** this is the most actionable line in the paper. AI writes "industry reports
suggest", "experts recommend", "studies show", "a major cloud provider". Humans write RFC 7208,
CVE-2024-3094, "Cloudflare changed this in their September post", "the 1.24.0 release",
"Tuesday morning".

**Directive:** every unnamed source is either named or cut.

This is the one directive in the file that can make writing worse, so it gets the longest
warning. "Name the specific thing" and "invent nothing" are in tension on every sentence where
you do not have the specific thing, and the cheapest way out is a name that sounds right:
a vendor, a version, a duration, a percentage. Observed in testing: asked for a LinkedIn post
about a real incident, a draft under this skill produced "the three months it usually takes a
Cloudflare migration checklist to get revisited" — a named vendor, a named artifact and a
number, none of them from anywhere. It read better than the vague version and it was false.

When you do not have the name, work the ladder in `SKILL.md` before you write: offer to look it
up, report what you found and let the user approve it, ask them directly if the search fails, and
announce anything you are about to invent before it reaches the page. The short version:
inventory what the piece needs, ask once up front about whatever is load-bearing, and if there
is no answer either cut the claim, write it openly as a hypothetical, or leave a `[[? … ]]`
marker where the real detail belongs. A vague sentence is a style problem; a fabricated one is
a lie with your name on it.

---

## Human-elevated: the reader is in the room

| Feature | Human | AI | Gap |
|---|---|---|---|
| Fourth-wall permeability (ordinal) | 0.67 | 0.39 | +0.28 |
| Frequency of direct reader address (ordinal) | 0.28 | 0.07 | +0.21 |

**Measured:** human writing acknowledges its audience as a co-participant, the aside to "you,
dear reader". AI writes as though no one is watching.

**In non-fiction:** "you will hit this the first time you rotate a key." "If you are reading this
because the alert fired at 3am, skip to the third section." In a speech: naming the room, the
occasion, the person who spoke before you.

**Directive:** one direct address or genuine aside, where it fits. One. This is a signal that
inverts fast when overused, and a reference doc is the wrong place for it.

---

## Human-elevated: time does not run straight

| Feature | Human | AI | Gap |
|---|---|---|---|
| Depth of recontextualization after a surprise (1–5) | 3.28 | 2.95 | +0.34 |
| Degree of chronological discontinuity (1–5) | 2.40 | 2.12 | +0.28 |
| Nonlinear framing for delayed disclosure (1–5) | 1.96 | 1.68 | +0.28 |
| Anachrony intensity (1–5) | 2.58 | 2.31 | +0.27 |

**Measured:** a human mystery opens at the funeral and spirals backward through decades. AI tells
the same story from the first clue to the grand reveal.

**In non-fiction:** the post that opens with the definition, then the history, then the setup,
then finally the problem. The incident writeup in timestamp order. The talk that spends four
minutes on context before the first interesting sentence.

**Directive:** open at the symptom, the number that was wrong, the moment it broke. Backfill.
Let a fact introduced late change how an earlier paragraph reads, and do not flag it for the
reader when it does.

---

## Human-elevated: range

| Feature | Human | AI | Gap |
|---|---|---|---|
| Location variety scope (ordinal) | 1.34 | 1.08 | +0.26 |
| Dialogue-to-narration proportion (1–5) | 2.95 | 2.70 | +0.24 |
| Thematically parallel subplots | 42% | 21% | +22 |
| Protagonist framed as morally ambivalent | 59% | 38% | +21 |
| Emotion conveyed through explicit labels | 29% | 8% | +21 |

**Measured:** human stories span more places, carry more dialogue relative to narration, and are
far more willing to leave the protagonist morally mixed. AI resolves the judgment.

**In non-fiction:** the recommendation with no stated cost. The tool comparison where the one
being recommended has no real drawback. The case study where the customer is simply right.

**Directive:** state the thing you dislike about your own recommendation, in your own voice, not
as a "Limitations" section. Ambivalence at 59% versus 38% is the second-largest categorical gap
in the entire table after embodied emotion.

---

## Rarity: the check to run last

The paper operationalizes originality as statistical rarity in narrative feature space: the mean
Euclidean distance to a story's 25 nearest neighbors. Human stories come out rarer, mean
percentile 0.71 against 0.49 for AI (AUC 0.73, Cohen's d 0.83). At the prompt level, the human
version is rarer than all five AI versions 57.8% of the time.

But the tails overlap. In the top 1% rarest test stories there are 42 human and 41 AI. Rarity is
a tendency, not a wall, and this matters for how you use it: the goal is not to be strange. It is
that AI defaults to the modal choice at every fork, and thirty modal choices in a row is the
tell.

**The check:** after the draft, list the structural decisions you made — where it opens, what
resolves it, how many threads, whose fault it was, whether anything is left open, how time runs.
Count how many were the first thing that came to mind. Move two of them to a less common option
that is still true. If nothing can move without becoming false, say so and leave it.

## Per-source note

Six-way authorship attribution from narrative features alone reaches 68.4% macro-F1 (77.3% with
style). Human writing is the most distinctive source (88.5% F1 without style), and Claude is the
most distinctive of the five models (77.1%), with GPT next (73.0%); DeepSeek, Gemini and Kimi
blur together at 55–60%. Each model also has its own "fingerprint" features — 26 for Claude, 11
each for GPT and Gemini, 7 for DeepSeek, 3 for Kimi, against 32 for human writing.

The practical reading: models have converged on a shared narrative region well separated from
human writing, and being the most distinguishable model in that cluster is not an advantage here.
