# -*- coding: utf-8 -*-
# Re-extract Ueber Sinn und Bedeutung with page-accurate footnote attachment.
import io, json, re

s = io.open('sinn.txt', encoding='utf-8').read()
i0 = s.find('Die Gleichheit **)')
i1 = s.find('die Urteile verſchieden ſind.')
body = s[i0:i1 + len('die Urteile verſchieden ſind.')]
pages = re.split(r'\[\d+/\d+\]', body)

def norm(x):
    x = x.replace('ſ', 's')
    x = re.sub(r'(\w)¬\s+(\w)', r'\1\2', x)
    x = re.sub(r'(\w)- (\w)', r'\1\2', x)
    return re.sub(r'\s+', ' ', x).strip()

units = []          # {'orig': str, 'pages': set}
fns = []            # (page_idx, marker, text)
for pi, pg in enumerate(pages):
    paras, cur = [], []
    for ln in pg.split('\n'):
        x = ln.strip()
        if not x or x == '_':
            if cur: paras.append(' '.join(cur)); cur = []
            continue
        if re.fullmatch(r'G\. Frege:|Über Sinn und Bedeutung\.|\d+|\d+\*', x):
            continue
        cur.append(x)
    if cur: paras.append(' '.join(cur))
    in_fn = False
    for p in paras:
        m = re.match(r'^(\*{1,3})\)\s*(.*)', p)
        if m:
            in_fn = True
            fns.append([pi, m.group(1) + ')', norm(m.group(2))])
            continue
        if in_fn:
            fns[-1][2] += ' ' + norm(p)
            continue
        p = norm(p)
        # continuation across page break: previous unit not sentence-final
        if units and not re.search(r'[.!?:“]\s*$', units[-1]['orig']):
            units[-1]['orig'] += ' ' + p
            units[-1]['pages'].add(pi)
        else:
            units.append({'orig': p, 'pages': {pi}})

print('units:', len(units), 'fns:', len(fns))
for pi, mk, tx in fns:
    cands = [u for u in units if pi in u['pages'] and mk in u['orig']]
    if len(cands) != 1:
        print(f'  page {pi} {mk}: {len(cands)} candidates :: {tx[:60]}')
        continue
    u = cands[0]
    key = 'fn' if 'fn' not in u else ('fn2' if 'fn2' not in u else 'fn3')
    u[key] = tx
    j = u['orig'].find(mk)
    print(f'  {mk} -> unit …{u["orig"][max(0,j-45):j]!r} :: {tx[:60]}')

d = json.load(io.open('frege-draft.json', encoding='utf-8'))
d['sb'] = [{k: v for k, v in u.items() if k != 'pages'} for u in units]
json.dump(d, io.open('frege-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
