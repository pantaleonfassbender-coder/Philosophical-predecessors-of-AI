# Monadology: French from PG #17641 (Piat 1909 print of the 1714 text; his
# notes are indented and dropped), English from Latta 1898 (IA OCR of
# cu31924016874038; per-page footnote blocks dropped). Sections 1-90 align
# by Leibniz's own numbering.
import io, json, re

# ---------------- French (PG 17641) ----------------
fr_lines = io.open('monadologie_fr.txt', encoding='utf-8').read().split('\n')[3402:5220]
fr_secs = {}
cur_n, cur = None, []
def fflush():
    global cur
    if cur_n and cur:
        t = ' '.join(cur)
        t = re.sub(r'\[\d+\]', '', t)          # note refs
        t = re.sub(r'\s+', ' ', t).strip()
        fr_secs[cur_n] = t
    cur = []
for ln in fr_lines:
    if ln.startswith('    ') or ln.startswith('\t'):
        continue                                # Piat notes / citations
    s = ln.strip()
    if not s:
        continue
    m = re.match(r'^(\d{1,2})\.(?:\[\d+\])?\s*(.*)', s)
    if m and (cur_n is None or int(m.group(1)) == cur_n + 1):
        fflush()
        cur_n = int(m.group(1))
        cur = [m.group(2)]
    elif cur_n:
        if s == 'MONADOLOGIE':
            continue
        cur.append(s)
fflush()
print('FR sections:', len(fr_secs), 'missing:', [i for i in range(1, 91) if i not in fr_secs])

# ---------------- English (Latta OCR) ----------------
en_raw = io.open('latta.txt', encoding='utf-8').read().split('\n')[10610:13510]
# split into pages at running heads
HEAD = re.compile(r'^\s*(\d|[A-Za-z0-9]{1,4}\s+)?THE\s+MONADOLOG[YV]', re.I)
pages, page = [], []
for ln in en_raw:
    if HEAD.match(ln.strip()) or re.fullmatch(r'[0-9lIOo]{2,4}', ln.strip() or 'x'):
        pages.append(page); page = []
        continue
    page.append(ln)
pages.append(page)

FNMARK = re.compile(r"^[\^'\"*{~`‘’´«»]|^[0-9]\s+[a-z]")
en_secs = {}
cur_n, cur = None, []
def eflush():
    global cur
    if cur_n and cur:
        t = ' '.join(cur)
        t = re.sub(r'(\w)[-­]\s+(\w)', r'\1\2', t)
        t = re.sub(r'\s+', ' ', t).strip()
        en_secs[cur_n] = en_secs.get(cur_n, '')
        en_secs[cur_n] = (en_secs[cur_n] + ' ' + t).strip()
    cur = []
for page in pages:
    # paragraphs within page
    paras, p = [], []
    for ln in page:
        if not ln.strip():
            if p: paras.append(p); p = []
        else:
            p.append(ln.strip())
    if p: paras.append(p)
    in_fn = False
    for p in paras:
        # expectation-driven, OCR-tolerant match of the next section number
        # (1 may read l/I, 0 may read O/o, digits may be spaced, footnote
        # marks or stray characters may precede number and dot); checked on
        # every line, since page breaks sometimes glue sections together
        k0 = 1 if cur_n is None else cur_n + 1
        pat = r'\s*'.join('[1lI]' if c == '1' else ('[0Oo]' if c == '0' else re.escape(c))
                          for c in str(k0))
        rx = re.compile(r"^(?:[^\d]{1,4}\s+|\d\s+)?" + pat + r"[\s\^'\"«»~`´’*]*[.,]\s*(.*)")
        started_here = False
        for li, ln in enumerate(p):
            m = rx.match(ln)
            if m:
                eflush(); cur_n = k0; cur = [m.group(1)]
                in_fn = False; started_here = True
                # rebuild the pattern for the following number, in case the
                # next section also starts inside this same paragraph
                k0 = cur_n + 1
                pat = r'\s*'.join('[1lI]' if c == '1' else ('[0Oo]' if c == '0' else re.escape(c))
                                  for c in str(k0))
                rx = re.compile(r"^(?:[^\d]{1,4}\s+|\d\s+)?" + pat + r"[\s\^'\"«»~`´’*]*[.,]\s*(.*)")
                continue
            if li == 0 and not started_here and FNMARK.match(ln):
                in_fn = True
            if in_fn:
                continue
            if cur_n:
                cur.append(ln)
eflush()
print('EN sections:', len(en_secs), 'missing:', [i for i in range(1, 91) if i not in en_secs])

units = []
for i in range(1, 91):
    units.append({'n': i, 'orig': fr_secs.get(i, ''), 'txt': en_secs.get(i, '')})
json.dump(units, io.open('mon-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for i in (1, 17, 45, 90):
    print('---', i, 'FR:', fr_secs.get(i, '')[:70])
    print('       EN:', en_secs.get(i, '')[:70])
