# Boole, An Investigation of the Laws of Thought (1854), from the Project
# Gutenberg LaTeX transcription (#15114): Preface + chapters I, II, III, XXII.
# Boole's own numbered articles give the citation grid (LoT I.1 etc.).
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/aipred/boole_lot.tex', encoding='utf-8').read()
lines = t.split('\n')

BOUNDS = [
 ('pref', 'Preface', 157, 242),
 ('c1', 'Chapter I. Nature and Design of this Work', 435, 1319),
 ('c2', 'Chapter II. Of Signs in General, and of the Signs appropriate to the Science of Logic', 1319, 1958),
 ('c3', 'Chapter III. Derivation of the Laws of the Symbols of Logic from the Laws of the Operations of the Human Mind', 1958, 2473),
 ('c22', 'Chapter XXII. The Constitution of the Intellect', 18709, None),
]
END = t.find('\\backmatter')
end_line = t[:END].count('\n') if END > -1 else len(lines)

def detex(s):
    # footnotes dropped (recorded on the method page); allow one nesting level
    s = re.sub(r'\\footnote\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', s)
    s = s.replace('\\\\', ' ').replace('~', ' ')
    for _ in range(2):
        s = re.sub(r'\\(?:textit|emph|textsc|textbf|textrm|text)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', s)
    s = s.replace('\\times', ' × ').replace('\\div', ' ÷ ').replace('\\cdot', ' · ')
    s = s.replace('\\ldots', '…').replace('\\dots', '…')
    s = s.replace('\\{', '{').replace('\\}', '}')
    s = re.sub(r'\$\s*([^$]*?)\s*\$', lambda m: re.sub(r'\s+', ' ', m.group(1)), s)
    s = re.sub(r'\\\[(.*?)\\\]', lambda m: ' ' + m.group(1).strip() + ' ', s, flags=re.S)
    s = re.sub(r'\\(?:label|index|pageref|ref|hyperref)\{[^{}]*\}', '', s)
    s = re.sub(r'\\begin\{[^{}]*\}|\\end\{[^{}]*\}', ' ', s)
    s = re.sub(r'\\[A-Za-z]+\*?(\[[^\]]*\])?', ' ', s)
    s = s.replace('{', '').replace('}', '')
    s = s.replace('---', '—').replace('--', '–')
    s = s.replace('``', '\u201c').replace("''", '\u201d').replace('`', '\u2018')
    return s

sections = []
n = 0
for sid, titel, lo, hi in BOUNDS:
    hi = hi if hi else end_line
    seg = lines[lo+1:hi]
    paras, cur = [], []
    for ln in seg:
        st = ln.strip()
        if st.startswith(('\\chapter', '\\backmatter')) or st.startswith('%'):
            continue
        ln = re.sub(r'(?<!\\)%.*$', '', ln)
        if not ln.strip():
            if cur: paras.append(' '.join(cur)); cur = []
        else:
            cur.append(ln.strip())
    if cur: paras.append(' '.join(cur))
    cleaned = []
    for p in paras:
        c = re.sub(r'\s+', ' ', detex(p)).strip()
        if not c: continue
        # drop chapter-title remnants (all-caps lines)
        letters = [ch for ch in c if ch.isalpha()]
        if letters and len(c) < 90 and sum(1 for ch in letters if ch.isupper()) / len(letters) > 0.9:
            continue
        # equation-only fragments join the previous paragraph
        if cleaned and (len(letters) < 12 or (len(c) < 80 and not c[0].isupper() and not re.match(r'^\d+\.', c))):
            cleaned[-1] += ' ' + c
        else:
            cleaned.append(c)
    units, art = [], None
    for c in cleaned:
        m = re.match(r'^(\d{1,2})\.\s+(.*)', c)
        if m:
            art = int(m.group(1)); n += 1
            units.append({'n': n, 'art': art, 'txt': m.group(2)})
        else:
            n += 1
            units.append({'n': n, 'art': art, 'txt': c})
    sections.append({'id': sid, 'titel': titel, 'units': units})

for s in sections:
    arts = [u['art'] for u in s['units'] if u['art']]
    print(s['id'], len(s['units']), 'units; articles up to', max(arts) if arts else '—',
          '| first:', s['units'][0]['txt'][:70])
json.dump({'sections': sections}, io.open('C:/Users/leofa/AppData/Local/Temp/aipred/boole-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('total units', n)
