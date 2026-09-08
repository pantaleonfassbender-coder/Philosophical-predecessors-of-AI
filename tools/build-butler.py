# Build data/butler_machines.json — Samuel Butler, the machine-evolution texts:
#
#   damm      "Darwin among the Machines" — The Press (Christchurch), 13 June 1863,
#             signed "Cellarius"; text via the Project Gutenberg transcription of
#             Canterbury Pieces (#3279).
#   bm1..bm3  "The Book of the Machines" — Erewhon, or Over the Range, chapters
#             XXIII-XXV; text via the Project Gutenberg transcription #1906
#             (the 1910 Fifield printing of Butler's revised text of 1901; in the
#             Truebner first edition of 1872 the machine chapters differ in
#             numbering and wording — cite the edition).
#
# Usage:
#   python tools/build-butler.py                  # fetch both texts from PG
#   python tools/build-butler.py cp.txt er.txt    # use local dumps (offline):
#                                                 #   cp.txt = pg3279.txt, er.txt = pg1906.txt
#
# The script prints the PG credits lines of both files so the edition statement
# can be verified against what Gutenberg actually digitized, and ends by printing
# the ready-made LICENSES.md / SOURCES.md entries for the shipping commit.
# After shipping: set the work's status to "shipped" in data/works.json and
# re-run tools/build-network.py so the Atlas picks the module up.
import io, json, os, re, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PG = {
    'canterbury': 'https://www.gutenberg.org/cache/epub/3279/pg3279.txt',
    'erewhon':    'https://www.gutenberg.org/cache/epub/1906/pg1906.txt',
}

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'calculemus-build/1.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8-sig')

def load(which, argpos):
    if len(sys.argv) > argpos:
        return io.open(sys.argv[argpos], encoding='utf-8-sig').read()
    return fetch(PG[which])

def strip_boilerplate(raw, name):
    # Keep only the text between the PG *** START / *** END markers,
    # but first show the credits so the edition can be checked by eye.
    for ln in raw.splitlines()[:30]:
        if re.search(r'credit|produced by|title:|release', ln, re.I):
            print(f'[{name} credits] {ln.strip()}')
    m = re.search(r'\*\*\* ?START OF[^\n]*\n(.*)\n\*\*\* ?END OF', raw, re.S)
    assert m, f'{name}: PG START/END markers not found'
    return m.group(1)

def paragraphs(block):
    out = []
    for p in re.split(r'\n\s*\n', block):
        p = re.sub(r'\s+', ' ', p).replace('_', '').strip()  # PG italics markers dropped
        if p:
            out.append(p)
    return out

# ------------------------------------------------- Darwin among the Machines
# In PG #3279 the essay headings are mixed-case lines ("Darwin Among the
# Machines"); the contents row carries a page number, so an exact line match
# finds the heading proper. The heading is followed by the 1914 editor's
# prefatory note (italic) and a bracketed dateline — editorial matter of the
# Fifield reprint, not Butler's text — so the letter is taken from the
# salutation ("SIR—…") to the Cellarius subscription.
cp = strip_boilerplate(load('canterbury', 1), 'pg3279')
lines = cp.splitlines()
start = next(i for i, ln in enumerate(lines)
             if ln.strip() == 'Darwin Among the Machines')
end = next(i for i in range(start + 1, len(lines))
           if lines[i].strip() == 'Lucubratio Ebria')
block = paragraphs('\n'.join(lines[start + 1:end]))
first = next(i for i, p in enumerate(block) if p.startswith('SIR'))
damm = block[first:]
sub = []
while damm and len(damm[-1]) < 40:      # fold "I am, Sir, etc.," + "CELLARIUS"
    sub.insert(0, damm.pop())
if sub:
    damm.append(' '.join(sub))
assert 5 <= len(damm) <= 25, f'letter looks wrong: {len(damm)} paragraphs'
assert any('mechanical life' in p for p in damm), 'expected phrase missing'
assert damm[-1].endswith('CELLARIUS'), 'subscription not where expected'
print(f'letter: {len(damm)} paragraphs')

# ------------------------------------------------- Erewhon XXIII-XXV
er = strip_boilerplate(load('erewhon', 2), 'pg1906')
def chap(n):
    m = re.search(rf'^CHAPTER {n}\b[^\n]*$', er, re.M)
    assert m, f'CHAPTER {n} heading not found'
    return m
c23, c24, c25, c26 = chap('XXIII'), chap('XXIV'), chap('XXV'), chap('XXVI')
assert 'MACHINES' in c23.group(0).upper() or \
       'MACHINES' in er[c23.end():c23.end() + 200].upper(), \
       'ch. XXIII does not look like The Book of the Machines'
CHAPTERS = [
    ('bm1', 'The Book of the Machines (Erewhon XXIII)',    c23, c24),
    ('bm2', 'The Machines — continued (Erewhon XXIV)',     c24, c25),
    ('bm3', 'The Machines — concluded (Erewhon XXV)',      c25, c26),
]

out = {
    'id': 'butler',
    'autor': 'Samuel Butler',
    'titel': 'Darwin among the Machines (1863) · The Book of the Machines (Erewhon)',
    'jahr': 1863,
    'lang': 'en',
    'zitierweise': 'But [n]',
    'quelle': ("Darwin among the Machines: The Press (Christchurch), 13 June 1863, signed "
               "'Cellarius'; text via the Project Gutenberg transcription #3279 (Canterbury "
               "Pieces, the 1914 Fifield reprint). The Book of the Machines: Erewhon, or Over the Range (London: "
               "Trübner, 1872), chapters XXIII–XXV in Butler's revised text of 1901, via the "
               "Project Gutenberg transcription #1906 (the 1910 Fifield printing). Both "
               "public domain (Butler †1902)."),
    'hinweis': ("The complete letter and the three machine chapters. Paragraph numbers are "
                "editorial and continuous. The Erewhon text is Butler's revision of 1901; "
                "the first edition of 1872 numbers and words the machine chapters "
                "differently — when citing, name the edition. The letter is carried after "
                "the 1914 Fifield reprint transcribed by Project Gutenberg — its editor's "
                "prefatory note and bracketed dateline are omitted as editorial matter — "
                "and the original newspaper printing was not consulted. Butler's italics "
                "are not carried."),
    'sections': [],
}

n = 0
def add_section(sid, titel, paras):
    global n
    units = []
    for k, p in enumerate(paras, start=1):
        n += 1
        units.append({'n': n, 'k': k, 'txt': p})
    out['sections'].append({'id': sid, 'titel': titel, 'units': units})

add_section('damm', 'Darwin among the Machines (The Press, 13 June 1863)', damm)
for sid, titel, a, b in CHAPTERS:
    paras = paragraphs(er[a.end():b.start()])
    assert len(paras) >= 5, f'{sid}: only {len(paras)} paragraphs'
    add_section(sid, titel, paras)

path = os.path.join(REPO, 'data', 'butler_machines.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '—', n, 'units,', len(out['sections']), 'sections')

print('''
--- for LICENSES.md (The texts themselves), on shipping ---
- **Butler**, "Darwin among the Machines" (The Press, Christchurch, 13 June 1863, signed
  'Cellarius') -- text via the Project Gutenberg transcription #3279 (Canterbury Pieces);
  *Erewhon* (London: Truebner, 1872), "The Book of the Machines", ch. XXIII-XXV of the
  revised text of 1901 -- via the Project Gutenberg transcription #1906 (1910 Fifield
  printing). Both public domain (Butler died 1902).

--- for SOURCES.md (The counter-voices), on shipping ---
### Samuel Butler -- machine evolution, twice told . `data/butler_machines.json`

- "Darwin among the Machines" (1863): Project Gutenberg #3279 (Canterbury Pieces) --
  <https://www.gutenberg.org/ebooks/3279>
- *Erewhon*, "The Book of the Machines" (ch. XXIII-XXV, revised text of 1901):
  Project Gutenberg #1906 -- <https://www.gutenberg.org/ebooks/1906>

--- then ---
1. set butler's status to "shipped" in data/works.json (and move the source note
   from "geplant" into the README table row);
2. run tools/build-network.py to rebuild the Atlas.
''')
