# -*- coding: utf-8 -*-
# Peirce, "Logical Machines" (Am. J. Psychology I, 1887, pp. 165-170),
# complete, from the JSTOR Early-Journal-Content scan (jstor-80000263).
# Jevons, "On the Mechanical Performance of Logical Inference" (1870),
# selected articles, from Pure Logic and Other Minor Works (1890),
# IA purelogicothermi00jevo_0.
import io, json, re

# ------------------------------------------------------------- Peirce
t = io.open('peirce.txt', encoding='utf-8').read()
lines = t.split('\n')
i0 = next(i for i, ln in enumerate(lines) if ln.strip() == 'Logical Machines.')
i1 = next(i for i, ln in enumerate(lines) if ln.strip().startswith('C. S. Pkirce'))
paras, cur = [], []
for ln in lines[i0 + 1:i1]:
    s = ln.strip()
    if not s:
        if cur: paras.append(' '.join(cur)); cur = []
        continue
    if re.fullmatch(r'\d{2,3}\s*', s) or re.match(r'^PSYCHOLOGICAL LITERATURE', s) \
       or re.fullmatch(r'\d+\s+PSYCHOLOGICAL.*', s):
        continue
    cur.append(s)
if cur: paras.append(' '.join(cur))
def clean(s):
    s = re.sub(r'(\w)- (\w)', r'\1\2', s)
    for a, b in [(' pro- cedures', ' procedures'), ('parte of', 'parts of'),
                 ('or projective', 'of projective'), ('principle or the machine', 'principle of the machine'),
                 ('-j-', '+'), ('a-f-b', 'a+b'), ('— t and t c', '= t and tc'),
                 ('a+B+c + d', 'a+B+c+d'), ('need ;not', 'need not'),
                 ('is 1 to', 'is to'), ('abed', 'abcd'), ('aBCd-f abCd', 'aBCd+abCd'),
                 ('(a +B+C+D)', '(a+B+C+D)'), ('(a +B+C+ d)', '(a+B+C+d)'),
                 ('v on', 'von')]:
        s = s.replace(a, b)
    s = re.sub(r'\s+', ' ', s).strip()
    return s
# merge paragraphs split at page breaks (no sentence-final punct)
merged = []
for p in paras:
    p = clean(p)
    if len(p) < 3: continue
    if merged and not re.search(r'[.!?:—]\s*$', merged[-1]):
        merged[-1] += ' ' + p
    else:
        merged.append(p)
peirce = merged
print('peirce paras:', len(peirce))
for i, p in enumerate(peirce):
    print(f'  [{i}] {p[:64]}')

# ------------------------------------------------------------- Jevons
g = io.open('purelogic.txt', encoding='utf-8').read()
glines = g.split('\n')
# memoir spans from its half-title to the Note (line with 'Norte to § 7')
j0 = next(i for i, ln in enumerate(glines) if 'ON THE MECHANICAL PERFORMANCE' in ln and i > 7770)
j1 = next(i for i, ln in enumerate(glines) if ln.strip().startswith('Norte to'))
WANT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 20, 21, 31, 32, 55, 56]
arts = {}
cur_n, cur = None, []
def jflush():
    global cur
    if cur_n is not None and cur:
        s = ' '.join(cur)
        s = re.sub(r'(\w)- (\w)', r'\1\2', s)
        s = re.sub(r'\s+', ' ', s).strip()
        arts[cur_n] = arts.get(cur_n, '')
        arts[cur_n] = (arts[cur_n] + ' ' + s).strip()
    cur = []
in_fn = False
for ln in glines[j0 + 2:j1]:
    s = ln.strip()
    if not s:
        in_fn = False
        continue
    if re.match(r'^\d+\s+THE MECHANICAL|^OF LOGICAL INFERENCE|^\d+\s+MECHANICAL', s):
        continue
    m = re.match(r'^(\d{1,2})\.\s+([A-Z].*)', s)
    if m and (cur_n is None or (cur_n < int(m.group(1)) <= cur_n + 3)):
        jflush()
        cur_n = int(m.group(1))
        cur = [m.group(2)]
        in_fn = False
        continue
    if re.match(r'^[0-9]\s+[A-Z]', s) and len(s) < 90 and ('See ' in s or 'Professor' in s or 'Pure Logic' in s or 'Substitution' in s):
        in_fn = True
    if in_fn:
        continue
    if cur_n is not None:
        cur.append(s)
jflush()
print('jevons articles found:', sorted(arts))
missing = [k for k in WANT if k not in arts]
print('missing wanted:', missing)
sel = {k: arts[k] for k in WANT if k in arts}
json.dump({'peirce': peirce, 'jevons': sel},
          io.open('pj-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
