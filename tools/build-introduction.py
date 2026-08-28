# -*- coding: utf-8 -*-
"""Build data/introduction.json from the author's Word manuscript.

Source: Calculemus_Introduction.docx (Pantaleon Fassbender, August 2026),
kept beside the repository, not in it. The essay is the site's own
editorial matter and ships under CC BY 4.0 like the rest of it.

Structure read off the manuscript: front matter (title, byline, author
note) up to the repeated title; Heading-1 paragraphs open sections, with
the untitled opening section before the first heading; the paragraph
"References" starts the reference list. Italic runs are carried as *...*
markers, which the view renders as <em>; whitespace is moved outside the
markers so they always sit on word boundaries.

Usage: python tools/build-introduction.py [path-to-docx]
"""
import json, re, sys
import docx

SRC = sys.argv[1] if len(sys.argv) > 1 else "../Calculemus_Introduction.docx"
OUT = "data/introduction.json"


def para_md(p):
    parts = []
    for r in p.runs:
        if not r.text:
            continue
        it = bool(r.italic)
        if parts and parts[-1][1] == it:
            parts[-1][0] += r.text
        else:
            parts.append([r.text, it])
    out = ""
    for t, it in parts:
        if it:
            lead, core, trail = re.match(r"^(\s*)(.*?)(\s*)$", t, re.S).groups()
            out += lead + (f"*{core}*" if core else "") + trail
        else:
            out += t
    return re.sub(r"\s+", " ", out).strip()


d = docx.Document(SRC)
paras = [(p.style.name if p.style else "", para_md(p)) for p in d.paragraphs]
paras = [(st, t) for st, t in paras if t]

titel = paras[0][1]
autor = paras[1][1]
datum = next(t for _, t in paras if re.fullmatch(r"[A-Z][a-z]+ \d{4}", t))
note = next(t for _, t in paras if t.startswith("Author note:"))

# body starts after the repeated title
body_at = next(i for i, (_, t) in enumerate(paras[1:], 1) if t == titel) + 1
abschnitte, referenzen, cur, in_refs = [], [], {"titel": "", "paras": []}, False
for st, t in paras[body_at:]:
    if in_refs:
        referenzen.append(t)
    elif t == "References":
        in_refs = True
    elif st.startswith("Heading"):
        if cur["paras"]:
            abschnitte.append(cur)
        cur = {"titel": t, "paras": []}
    else:
        cur["paras"].append(t)
if cur["paras"]:
    abschnitte.append(cur)

assert referenzen and len(abschnitte) >= 6, "manuscript structure not recognised"

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"titel": titel, "autor": autor, "datum": datum, "note": note,
               "abschnitte": abschnitte, "referenzen": referenzen},
              f, ensure_ascii=False, indent=1)
print(f"{OUT}: {len(abschnitte)} sections, "
      f"{sum(len(a['paras']) for a in abschnitte)} paragraphs, "
      f"{len(referenzen)} references")
