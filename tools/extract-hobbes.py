# Leviathan (1651), Gutenberg #3207: Introduction + Part I, ch. I-V.
# Units follow the original marginal side-notes, which Gutenberg prints as
# free-standing title-case lines; 1651 spelling is preserved.
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/aipred/leviathan.txt', encoding='utf-8').read()
lines = t.split('\n')

BOUNDS = [
 ('intro', 'The Introduction', 305, 395),
 ('c1', 'Chapter I. Of Sense', 395, 463),
 ('c2', 'Chapter II. Of Imagination', 463, 680),
 ('c3', 'Chapter III. Of the Consequence or Trayne of Imaginations', 680, 877),
 ('c4', 'Chapter IV. Of Speech', 877, 1232),
 ('c5', 'Chapter V. Of Reason, and Science', 1232, 1522),
]

def is_sidenote(s):
    s = s.strip()
    if not s or len(s) > 75: return False
    if s.endswith(('.', ',', ';', ':', '?')) and len(s.split()) > 9: return False
    words = s.replace('-', ' ').split()
    if not words: return False
    caps = sum(1 for w in words if w[0].isupper() or not w[0].isalpha())
    return caps / len(words) > 0.7 and not s.isupper()

def extract_section(seg, counter):
    units = []
    state = {'label': '', 'cur': [], 'n': counter}
    def flush():
        txt = ' '.join(l.strip() for l in state['cur'] if l.strip())
        txt = re.sub(r'\s+', ' ', txt).strip()
        emitted = False
        if txt:
            state['n'] += 1
            u = {'n': state['n'], 'txt': txt}
            if state['label']: u['label'] = state['label']
            units.append(u)
            emitted = True
        state['cur'] = []
        return emitted
    i = 0
    while i < len(seg):
        s = seg[i].strip()
        if not s:
            j = i + 1
            while j < len(seg) and not seg[j].strip(): j += 1
            emitted = flush()
            if j < len(seg) and is_sidenote(seg[j]):
                state['label'] = seg[j].strip()
                i = j + 1
            else:
                if emitted: state['label'] = ''
                i = j
            continue
        state['cur'].append(s)
        i += 1
    flush()
    return units, state['n']

sections, n = [], 0
for sid, titel, lo, hi in BOUNDS:
    seg = lines[lo:hi]
    seg = [l for l in seg if not l.strip().startswith(('CHAPTER', 'THE INTRODUCTION'))]
    units, n = extract_section(seg, n)
    sections.append({'id': sid, 'titel': titel, 'units': units})

for s in sections:
    print(s['id'], len(s['units']), 'units | labels:',
          [u.get('label', '—')[:28] for u in s['units'][:5]])
json.dump({'sections': sections}, io.open('C:/Users/leofa/AppData/Local/Temp/aipred/hobbes-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('total units', n)
