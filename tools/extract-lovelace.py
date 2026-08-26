# Menabrea's Sketch of the Analytical Engine, translated by Ada Lovelace, with
# her Notes A-G (Taylor's Scientific Memoirs III, 1843), from the IA OCR of
# india.history.resource.53369.
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/aipred/taylor3b.txt', encoding='utf-8', errors='replace').read()

BOUNDS = [
 ('memoir', "Menabrea's Sketch of the Analytical Engine (translated by A.A.L.)", 1578789, 1633598),
 ('noteA', 'Note A', 1633623, 1670710),
 ('noteB', 'Note B', 1670710, 1685152),
 ('noteC', 'Note C', 1685152, 1688137),
 ('noteD', 'Note D', 1688137, 1703309),
 ('noteE', 'Note E', 1703309, 1727269),
 ('noteF', 'Note F', 1727269, 1734161),
 ('noteG', 'Note G', 1734161, 1760154),
]

def is_junkline(s):
    if re.fullmatch(r'[\W\d]{1,10}', s): return True                       # page numbers
    letters = [c for c in s if c.isalpha()]
    if not letters: return True
    upr = sum(1 for c in letters if c.isupper()) / len(letters)
    if upr > 0.75 and re.search(r'MENABREA|ANALYTICAL|ENGINE|TRANSLATOR|BABBAGE|SCIENTIFIC|MEMOIRS', s.upper()):
        return True                                                        # running heads
    if upr > 0.8 and re.search(r'\d{3}', s):
        return True
    return False

def mathiness(s):
    """share of characters that are digits/operators/greek-ish — used to spot
    displayed formulas and tables the OCR cannot carry."""
    if not s: return 0
    m = sum(1 for c in s if c.isdigit() or c in '+-=×xX*/^()<>{}[]|.,;:~_')
    return m / len(s)

def extract(lo, hi, sid):
    lines = t[lo:hi].split('\n')
    paras, cur = [], []
    in_fn = False
    def flush():
        nonlocal cur
        s = ' '.join(cur)
        s = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', s)
        s = re.sub(r'\s+', ' ', s).strip()
        if len(s) > 2:
            paras.append(s)
        cur = []
    for ln in lines:
        s = ln.strip()
        if not s:
            flush(); in_fn = False
            continue
        if is_junkline(s):
            in_fn = False
            continue
        if re.match(r'^[\*\u2020\u2021]\s?\S', s):     # footnote line (*, †, ‡)
            in_fn = True
            continue
        if in_fn:
            continue
        if s.startswith(('Nore ', 'Note A.', 'Note B.', 'Note C.', 'Note D.', 'Note E.', 'Note F.', 'Note G.')):
            continue
        cur.append(s)
    flush()
    # merge page-break splits
    merged = []
    for s in paras:
        if merged and (not re.search(r'[.!?:\u201d\u2019]\s*$', merged[-1]) or s[:1].islower()):
            merged[-1] += ' ' + s
            continue
        merged.append(s)
    # replace formula-heavy paragraphs by a placeholder marker
    out = []
    for s in merged:
        if mathiness(s) > 0.38 and len(s) > 25:
            if out and out[-1].endswith('[formula omitted]'):
                continue
            out.append('[formula omitted]')
        else:
            out.append(s)
    return out

sections = []
n = 0
for sid, titel, lo, hi in BOUNDS:
    paras = extract(lo, hi, sid)
    units = []
    for k, p in enumerate(paras, 1):
        n += 1
        units.append({'n': n, 'k': k, 'txt': p})
    sections.append({'id': sid, 'titel': titel, 'units': units})
    print(f"{sid:8s} {len(units):3d} units  first: {paras[0][:60] if paras else '—'}")

json.dump({'sections': sections}, io.open('C:/Users/leofa/AppData/Local/Temp/aipred/lovelace-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('total', n)
