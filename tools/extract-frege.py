# -*- coding: utf-8 -*-
# Frege module, German sources:
#  bs - Begriffsschrift (1879), Vorwort, IA OCR #11388662, emended
#  gl - Grundlagen der Arithmetik (1884), PG #48312: Einleitung, §§1-4,
#       §§87-91, §§106-109
#  sb - Ueber Sinn und Bedeutung (1892), complete, DTA transcription
#       frege_sinn_1892 (long s normalized, Frege's footnotes attached)
import io, json, re

OUT = {}

# ------------------------------------------------------------------- bs
t = io.open('begriffsschrift.txt', encoding='utf-8').read()
lines = t.split('\n')[32:283]
paras, cur = [], []
for ln in lines:
    s = ln.strip()
    if not s:
        if cur: paras.append(' '.join(cur)); cur = []
        continue
    if re.fullmatch(r'[IVX]+|\*|Vorwort\.', s):      # page numbers, marks
        continue
    if s.startswith('*)'):                            # footnote
        if cur: paras.append(' '.join(cur)); cur = []
        cur = ['[FN]' + s[2:].strip()]
        continue
    cur.append(s)
if cur: paras.append(' '.join(cur))
def clean_bs(s):
    s = re.sub(r'(\w)- (\w)', r'\1\2', s)
    for a, b in [('dureh', 'durch'), ('Sehluss', 'Schluss'), ('mehre ', 'mehrere '),
                 ('Beschaftenheit', 'Beschaffenheit'), ('Begrifis', 'Begriffs'),
                 ('Zahlbegrifl', 'Zahlbegriff'), ('/o- gische', 'logische'),
                 ('/o-gische', 'logische'), ('so Konnte', 'so konnte'),
                 ('errathen,', 'errathen,')]:
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()
paras = [clean_bs(p) for p in paras if len(clean_bs(p)) > 2]
# attach footnotes to preceding paragraph
bs_units = []
for p in paras:
    if p.startswith('[FN]'):
        if bs_units:
            bs_units[-1]['fn'] = p[4:]
        continue
    bs_units.append({'orig': p})
OUT['bs'] = bs_units
print('bs paras:', len(bs_units), '| first:', bs_units[0]['orig'][:60])
print('bs last:', bs_units[-1]['orig'][:80])

# ------------------------------------------------------------------- gl
g = io.open('grundlagen.txt', encoding='utf-8').read()
glines = g.split('\n')

def gl_block(lo, hi):
    ps, cur = [], []
    for ln in glines[lo:hi]:
        s = ln.strip()
        if not s:
            if cur: ps.append(' '.join(cur)); cur = []
            continue
        if s.startswith('[') and s.endswith(']') and len(s) < 12:
            continue
        cur.append(s)
    if cur: ps.append(' '.join(cur))
    out = []
    for p in ps:
        p = re.sub(r'\[\d+\]', '', p)
        p = p.replace('_', '')
        p = re.sub(r'\s+', ' ', p).strip()
        if len(p) > 2 and not re.fullmatch(r'[IV]+\. .*|\d+', p):
            out.append(p)
    return out

# Einleitung: lines 464..775 (0-based: 463..775); §-blocks located by scan
def sec_bounds(want):
    bounds = {}
    for i, ln in enumerate(glines):
        m = re.match(r'^§ (\d+)\.', ln.strip())
        if m: bounds[int(m.group(1))] = i
    return bounds
B = sec_bounds(None)
gl_units = []
for p in gl_block(463, B[1]):
    gl_units.append({'orig': p, 'part': 'Einleitung'})
FN_LINE = next(i for i, ln in enumerate(glines) if ln.strip() == 'Fußnoten:')
def add_secs(a, b):
    for k in range(a, b + 1):
        lo, hi = B[k], B.get(k + 1, FN_LINE)
        ps = gl_block(lo, hi)
        # first para starts with '§ k.'
        for j, p in enumerate(ps):
            gl_units.append({'orig': re.sub(r'^§ \d+\.\s*', '', p),
                             'part': f'§ {k}' + ('' if j == 0 else f' (Forts. {j})')})
add_secs(1, 4)
add_secs(87, 91)
add_secs(106, 109)
OUT['gl'] = gl_units
print('gl units:', len(gl_units), '| parts:', sorted(set(u['part'].split(' (')[0] for u in gl_units)))

# ------------------------------------------------------------------- sb
s = io.open('sinn.txt', encoding='utf-8').read()
i0 = s.find('Die Gleichheit **)')
i1 = s.find('die Urteile verſchieden ſind.')
body = s[i0:i1 + len('die Urteile verſchieden ſind.')]
# split into pages at [NN/00NN] markers
pages = re.split(r'\[\d+/\d+\]', body)
text_paras = []        # list of paragraph strings (with inline *) markers)
fn_by_marker = []      # (marker, text) in reading order
for pg in pages:
    plines = pg.split('\n')
    paras, cur = [], []
    for ln in plines:
        x = ln.strip()
        if not x or x == '_':
            if cur: paras.append(' '.join(cur)); cur = []
            continue
        if re.fullmatch(r'G\. Frege:|Über Sinn und Bedeutung\.|Zeitſchrift.*|\d+', x):
            continue
        cur.append(x)
    if cur: paras.append(' '.join(cur))
    in_fn = False
    for p in paras:
        m = re.match(r'^(\*{1,3})\)\s*(.*)', p)
        if m:
            in_fn = True
            fn_by_marker.append([m.group(1) + ')', m.group(2)])
            continue
        if in_fn:
            # continuation of a footnote across paragraphs is rare; footnotes
            # sit at page bottom, so everything after the first marker on a
            # page is footnote material unless it starts a new page
            fn_by_marker[-1][1] += ' ' + p
            continue
        text_paras.append(p)

def norm(x):
    x = x.replace('ſ', 's')
    x = re.sub(r'(\w)¬\s+(\w)', r'\1\2', x)
    x = re.sub(r'(\w)- (\w)', r'\1\2', x)
    x = re.sub(r'\s+', ' ', x)
    return x.strip()

# merge page-break splits: paragraph not ending in sentence-final punct
merged = []
for p in text_paras:
    p = norm(p)
    if merged and not re.search(r'[.!?:“]\s*$', merged[-1]):
        merged[-1] += ' ' + p
    else:
        merged.append(p)
fns = [(mk, norm(tx)) for mk, tx in fn_by_marker]
# attach footnotes: in reading order, each footnote belongs to the earliest
# unit (not yet claimed for the same marker instance) containing the marker
sb_units = [{'orig': p} for p in merged]
used = [0] * len(sb_units)
for mk, tx in fns:
    for idx, u in enumerate(sb_units):
        if mk in u['orig'] and (mk + ')') not in u['orig']:
            key = 'fn' if 'fn' not in u else 'fn2'
            if key == 'fn2' and 'fn2' in u: continue
            u[key] = tx
            if key == 'fn': break
            break
    else:
        print('UNATTACHED FN:', mk, tx[:60])
OUT['sb'] = sb_units
print('sb units:', len(sb_units), '| fns:', len(fns))
print('sb first:', sb_units[0]['orig'][:80])
print('sb last :', sb_units[-1]['orig'][-80:])
json.dump(OUT, io.open('frege-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
