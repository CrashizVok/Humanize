#!/usr/bin/env python3
"""Flag surface-level AI writing tells in a Markdown or plain text file.

This only sees layer 2. It cannot measure the structural layer described in
references/narrative-structure.md, and a clean report is not a pass.

    python3 humanize-check.py --lang en README.md
    cat draft.md | python3 humanize-check.py --lang hu -
    python3 humanize-check.py --lang en --strict draft.md   # non-zero exit on findings
"""

import argparse
import re
import statistics
import sys
import unicodedata

STOCK_WORDS = {
    "en": [
        "delve", "delving", "tapestry", "pivotal", "crucial", "underscore",
        "underscores", "underscoring", "showcase", "showcases", "showcasing",
        "testament", "vibrant", "intricate", "intricacies", "foster", "fostering",
        "seamless", "seamlessly", "myriad", "plethora", "realm", "landscape",
        "navigate the", "harness the", "leverage", "robust solution",
        "cutting-edge", "groundbreaking", "game-changer", "unlock the",
        "elevate", "embark", "boasts", "nestled", "in the heart of",
        "it is important to note", "it's important to note",
        "in today's", "let's dive", "let's explore", "let's break this down",
        "at its core", "the real question is", "here's the thing",
        "i hope this helps", "great question", "you're absolutely right",
        "as an ai", "as of my last", "when it comes to", "in the world of",
        "ever-evolving", "rapidly evolving", "stands as", "serves as",
    ],
    "hu": [
        "napjainkban", "a mai rohanó világban", "a digitális korban",
        "egyre inkább", "nem véletlen, hogy", "mindannyian tudjuk",
        "elengedhetetlen", "kulcsfontosságú", "létfontosságú",
        "kiemelkedő jelentőségű", "meghatározó szerepet játszik",
        "alapvető fontosságú", "rendkívül fontos",
        "átfogó megoldás", "hatékony megoldás", "testre szabott", "letisztult",
        "felhasználóbarát", "innovatív", "gördülékeny", "zökkenőmentes",
        "a legmodernebb", "prémium minőségű",
        "érdemes megjegyezni", "fontos kiemelni", "mindazonáltal", "ezen felül",
        "összességében elmondható", "mindent egybevetve", "a jövő fényes",
        "merüljünk el", "legyünk őszinték", "a nap végén",
        "lehetőségek tárháza",
    ],
}

# The "kerül" passive and nominalization, Hungarian only.
HU_PASSIVE = re.compile(
    r"\b\w+(?:ásra|ésre|tatásra|tetésre)\s+kerül(?:t|nek|tek|het|ne)?\b", re.I
)

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿]"
)
BOLD_LABEL_ITEM = re.compile(
    r"^\s*(?:[-*+]|\d+\.)\s+\*\*[^*]{2,40}(?:\*\*\s*:|:\*\*)"
)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
NOT_JUST_EN = re.compile(
    r"\b(?:it'?s |this is |that'?s )?not (?:just|only|merely|simply)\b[^.]{0,80}?,?\s*(?:but|it'?s)\b",
    re.I,
)
NOT_JUST_HU = re.compile(r"\bnem (?:csupán|csak|pusztán|egyszerűen)\b[^.]{0,80}?,\s*hanem\b", re.I)
TRIPLE = re.compile(r"\b[\w'-]+, [\w'-]+,? (?:and|és|valamint) [\w'-]+\b")
# The placeholder the skill drops where a real detail is missing. If one survives into a
# finished file, something unsourced was about to ship.
MARKER = re.compile(r"\[\[\?.*?\]\]|\[\[\?[^\n]*")

# A closing that announces the point instead of making it. Two shapes, and both are
# checked across the whole last paragraph rather than only its first sentence: four
# test rounds produced "Ez a lényeg:" at the end, the same sentence moved to the
# middle, "Szóval a DMARC nem egy pipa a listán", and then "És itt a lényeg:" three
# words in, which an opener-only check walked straight past.
CLOSING_OPENER = {
    "hu": re.compile(r"^\s*(?:Szóval|Tehát|Végül is|Összegezve|Összefoglalva|"
                     r"Ez az a|Erre érdemes|Amit ebből érdemes)\b", re.I),
    "en": re.compile(r"^\s*(?:So,|To sum up|In conclusion|In short|Bottom line|"
                     r"That'?s (?:the|what|why)|Here'?s (?:the|what))\b", re.I),
}
CLOSING_PHRASE = {
    "hu": re.compile(r"\b(?:itt a lényeg|ez a lényeg|a lényeg az|a lényeg pedig|"
                     r"a tanulság|a konklúzió|a legfontosabb az)\b", re.I),
    "en": re.compile(r"\b(?:the point is|here'?s the point|the takeaway|what this means|"
                     r"the real lesson|the bottom line)\b", re.I),
}

# An ordinary claim dressed as a saying (surface §32). Kept narrow on purpose: these
# shapes are the ones that turned up in testing, not every metaphor.
APHORISM = {
    "hu": re.compile(
        r"\b(?:a|az)\s+[\w-]+(?:\s+[\w-]+){0,3}\s(?:tükre|nyelve|valutája|motorja|gerince)\b",
        re.I),
    "en": re.compile(
        r"\b(?:only as good as|is the (?:language|currency|backbone|lifeblood|engine|mirror) of)\b",
        re.I),
}


def strip_noise(lines):
    """Blank out code fences, indented code, frontmatter, inline code and URLs.

    Returns a list the same length as the input so line numbers stay honest.
    """
    out = []
    in_fence = False
    in_front = False
    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if i == 0 and line.strip() == "---":
            in_front = True
            out.append("")
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            out.append("")
            continue
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence or line.startswith("    ") or line.startswith("\t"):
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", " ", line)
        line = re.sub(r"https?://\S+", " ", line)
        line = re.sub(r"\]\([^)]*\)", "] ", line)
        out.append(line)
    return out


def is_heading(line):
    return bool(re.match(r"^#{1,6}\s+\S", line))


def title_case_heading(line):
    text = re.sub(r"^#{1,6}\s+", "", line).strip()
    text = re.sub(r"[*_`]", "", text)
    words = [w for w in re.split(r"\s+", text) if w]
    if len(words) < 4:
        return False
    small = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on",
             "or", "the", "to", "vs", "with"}
    candidates = [w for w in words[1:] if w.lower() not in small and w[:1].isalpha()]
    if len(candidates) < 3:
        return False
    capped = sum(1 for w in candidates if w[:1].isupper() and not w.isupper())
    return capped >= len(candidates) - 1


def prose_lines(clean):
    for i, line in enumerate(clean, start=1):
        s = line.strip()
        if not s or is_heading(s) or s.startswith(">") or s.startswith("|"):
            continue
        yield i, s


def sentences_of(clean):
    body = " ".join(
        s for _, s in prose_lines(clean) if not re.match(r"^(?:[-*+]|\d+\.)\s", s)
    )
    return [t.strip() for t in SENTENCE_SPLIT.split(body) if len(t.split()) > 1]


def paragraphs_of(clean):
    paras, cur = [], []
    for line in clean:
        s = line.strip()
        if not s:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if is_heading(s) or s.startswith(("|", ">", "-", "*", "+")) or re.match(r"^\d+\.", s):
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(" ".join(cur))
    return paras


def check(text, lang, fmt="prose"):
    lines = text.splitlines()
    clean = strip_noise(lines)
    findings = []

    def add(line_no, code, message, excerpt=""):
        findings.append((line_no, code, message, excerpt.strip()[:90]))

    for i, s in prose_lines(clean):
        low = s.lower()

        if lang == "en":
            for m in re.finditer(r"—|–|(?<= )--(?= )", s):
                add(i, "dash", "em/en dash or double hyphen (English text)", s[max(0, m.start() - 30):m.end() + 30])
            if "“" in s or "”" in s:
                add(i, "quotes", "curly quotation marks", s)
        else:
            for m in re.finditer(r"—", s):
                add(i, "dash", "hosszú kötőjel (—); magyarul gondolatjel (–) kell", s[max(0, m.start() - 30):m.end() + 30])
            for m in re.finditer(r"(?<=\w) - (?=\w)", s):
                add(i, "dash", "kötőjel gondolatjel helyett; használj – jelet", s[max(0, m.start() - 30):m.end() + 30])
            # A quoted code value keeps straight quotes: "Pending", "queued", "delayed"
            # are identifiers, and „Pending” would be wrong. Only flag quoted material
            # that reads as Hungarian text: more than one word, or one word carrying a
            # Hungarian accent.
            for m in re.finditer(r'"([^"\n]{1,60})"', s):
                inner = m.group(1).strip()
                if " " in inner or re.search(r"[áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", inner):
                    add(i, "quotes", "egyenes idézőjel; magyarul „ ” kell", m.group(0))
            for m in HU_PASSIVE.finditer(s):
                add(i, "passive", '"kerül" passzív; írd cselekvő alakban', m.group(0))

        for word in STOCK_WORDS[lang]:
            for m in re.finditer(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", low):
                add(i, "word", f"stock AI phrase: {word}", s[max(0, m.start() - 25):m.end() + 25])

        for m in MARKER.finditer(s):
            add(i, "marker", "unresolved [[? ]] marker: a real detail is still missing", m.group(0))
        for m in APHORISM[lang].finditer(s):
            add(i, "aphorism", "claim dressed as a saying; state the claim instead", m.group(0))
        if EMOJI.search(s):
            add(i, "emoji", "emoji used as decoration", s)
        if BOLD_LABEL_ITEM.match(clean[i - 1]):
            add(i, "boldlist", "bold-label list item", s)

        pat = NOT_JUST_EN if lang == "en" else NOT_JUST_HU
        for m in pat.finditer(s):
            add(i, "notjust", "not-X-but-Y construction", m.group(0))
        if fmt != "speech":
            for m in TRIPLE.finditer(s):
                add(i, "triple", "three-item series; check it is not a forced triple", m.group(0))

    for i, line in enumerate(clean, start=1):
        if is_heading(line.strip()) and lang == "en" and title_case_heading(line.strip()):
            add(i, "titlecase", "heading looks like Title Case", line.strip())

    paras_for_close = [p for p in paragraphs_of(clean) if p.strip()]
    if paras_for_close:
        last = paras_for_close[-1]
        first_of_last = SENTENCE_SPLIT.split(last)[0]
        if CLOSING_OPENER[lang].match(first_of_last):
            add(0, "closing", "the last paragraph opens by summing up: "
                              f'"{first_of_last[:60]}"')
        m = CLOSING_PHRASE[lang].search(last)
        if m:
            add(0, "closing", "the closing announces the point instead of making it: "
                              f'"{m.group(0)}"')

    stats = {}
    sents = sentences_of(clean)
    if len(sents) >= 6:
        lengths = [len(s.split()) for s in sents]
        sd = statistics.pstdev(lengths)
        stats["sentences"] = len(lengths)
        stats["mean_len"] = round(statistics.mean(lengths), 1)
        stats["stdev_len"] = round(sd, 1)
        stats["short_under_8"] = sum(1 for n in lengths if n < 8)
        stats["long_over_25"] = sum(1 for n in lengths if n > 25)
        if sd < 6:
            add(0, "burstiness", f"low sentence-length variation (stdev {sd:.1f}, want 6+)")
        if stats["short_under_8"] == 0:
            add(0, "burstiness", "no sentence under 8 words")
        if stats["long_over_25"] == 0 and fmt != "speech":
            add(0, "burstiness", "no sentence over 25 words")
        run = 1
        for a, b in zip(lengths, lengths[1:]):
            run = run + 1 if abs(a - b) <= 3 else 1
            if run == 4:
                add(0, "burstiness", "run of 4+ sentences of near-identical length")
                run = 1

        # A bare article says nothing about repetition, and in Hungarian "a" opens a
        # great many perfectly varied sentences. When the first word is an article,
        # key on the first two words instead.
        articles = {"a", "az", "the", "an", "egy"}
        openers = {}
        for s in sents:
            words = [re.sub(r"[^\w-]", "", w).lower() for w in s.split()[:2]]
            words = [w for w in words if w]
            if not words:
                continue
            first = words[0]
            if first in articles and len(words) > 1:
                first = " ".join(words[:2])
            openers[first] = openers.get(first, 0) + 1
        top, count = max(openers.items(), key=lambda kv: kv[1])
        if count >= 4 and count / len(sents) > 0.25:
            add(0, "monotony", f'{count} of {len(sents)} sentences open with "{top}"')

    paras = paragraphs_of(clean)
    shapes = [(len(SENTENCE_SPLIT.split(p)), len(p.split()) // 20) for p in paras]
    run = 1
    for a, b in zip(shapes, shapes[1:]):
        run = run + 1 if a == b else 1
        if run == 3:
            add(0, "shape", "3+ consecutive paragraphs with the same shape")
            run = 1

    return findings, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help='file to check, or "-" for stdin')
    ap.add_argument("--lang", choices=["en", "hu"], default="en")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is flagged")
    ap.add_argument(
        "--format",
        choices=["prose", "speech"],
        default="prose",
        help="speech drops the long-sentence and triple checks, which invert when spoken",
    )
    args = ap.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
        name = "<stdin>"
    else:
        with open(args.path, encoding="utf-8") as fh:
            text = fh.read()
        name = args.path

    text = unicodedata.normalize("NFC", text)
    findings, stats = check(text, args.lang, args.format)

    for line_no, code, message, excerpt in sorted(findings, key=lambda f: (f[0], f[1])):
        where = f"{name}:{line_no}" if line_no else f"{name}"
        print(f"{where}: [{code}] {message}" + (f"  |  {excerpt}" if excerpt else ""))

    by_code = {}
    for _, code, _, _ in findings:
        by_code[code] = by_code.get(code, 0) + 1

    print()
    if stats:
        print(
            f"{stats['sentences']} sentences, mean {stats['mean_len']} words, "
            f"stdev {stats['stdev_len']}, {stats['short_under_8']} under 8, "
            f"{stats['long_over_25']} over 25"
        )
    if by_code:
        print("flags: " + ", ".join(f"{k}={v}" for k, v in sorted(by_code.items())))
    else:
        print("no surface flags")
    if by_code.get("marker"):
        print(
            f"{by_code['marker']} unresolved marker(s): ask the user for those details, "
            "cut the claim, or mark it as hypothetical. Do not fill them in."
        )
    if args.format == "speech":
        print("Speech mode: the long-sentence and triple checks are off, they invert when spoken.")
    print("This checks layer 2 only. The structural layer is not machine-checkable here.")

    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
