# -*- coding: utf-8 -*-
# Pascal, Pensées: five fragments (Brunschvicg 252, 339, 340, 346, 347),
# French from the fr.wikisource transcription of the Brunschvicg edition,
# English from W. F. Trotter's public-domain translation (PG #18269).
import io, json, re

s4 = io.open('pascal_s4.txt', encoding='utf-8').read()
s6 = io.open('pascal_s6.txt', encoding='utf-8').read()

def frag_fr(text, num):
    m = re.search(r'\b' + str(num) + r'\s*\[\s*\d+\s*\]\s*', text)
    assert m, num
    rest = text[m.end():]
    # end at next fragment number or apparatus arrow
    e = re.search(r'\n\s*\d{3}\s*\[|↑', rest)
    body = rest[:e.start()] if e else rest[:2000]
    body = re.sub(r'\[\s*\d+\s*\]', '', body)
    body = re.sub(r'\s+', ' ', body).strip()
    return body

def frag_en(num):
    t = io.open('trotter.txt', encoding='utf-8').read()
    m = re.search(r'\n' + str(num) + r'\n\n(.*?)\n\n\n', t, re.S)
    assert m, num
    return re.sub(r'\s+', ' ', m.group(1)).strip()

FRAGS = [(252, s4), (339, s6), (340, s6), (346, s6), (347, s6)]
units = []
for num, src in FRAGS:
    fr = frag_fr(src, num)
    en = frag_en(num)
    units.append({'br': num, 'orig': fr, 'txt': en})
    print(num, '| FR:', fr[:70])
    print('    | EN:', en[:70])
json.dump(units, io.open('pascal-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
