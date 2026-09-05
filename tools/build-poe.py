# Build data/poe_maelzel.json from the Wikisource wikitext of
# "Maelzel's Chess-Player" (Southern Literary Messenger, April 1836).
# Input: a raw wikitext dump (action=raw) of en.wikisource.org's page,
# collated against the Edgar Allan Poe Society of Baltimore's Text-02
# of the same printing.
import io, json, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'poe_ws.txt'
REPO = 'C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo'

raw = io.open(SRC, encoding='utf-8').read()
paras = [p.strip() for p in raw.split('\n\n') if p.strip()]

def clean(p):
    notes = []
    def ref(m):
        notes.append(re.sub(r'\s+', ' ', m.group(1)).replace("''", '').strip())
        return ''
    p = re.sub(r'<!--.*?-->', '', p, flags=re.S)  # Wikisource editor comments
    p = re.sub(r'<ref>(.*?)</ref>', ref, p, flags=re.S)
    p = re.sub(r'\{\{smallcaps\|([^}]*)\}\}', r'\1', p)
    p = re.sub(r'\{\{[^}]*\}\}', '', p)
    p = re.sub(r'\[\[(?:[a-z]+:)?[^\]|]*\|([^\]]*)\]\]', r'\1', p)  # [[target|label]] -> label
    p = re.sub(r'\[\[Category:[^\]]*\]\]', '', p)
    p = re.sub(r'\[\[(?:[a-z]+:)[^\]]*\]\]', '', p)                 # interwiki without label
    p = re.sub(r'\[\[([^\]]*)\]\]', r'\1', p)                       # [[plain]] -> plain
    p = p.replace("''", '')                                         # italics markers dropped
    p = p.replace('&nbsp;', ' ')
    p = re.sub(r'\s+', ' ', p).strip()
    return p, notes

# paragraph indices in the dump: 0 header, 1..38 text, 39 '---', 40 refs, 41 license
text = []
for i in range(1, 39):
    p, notes = clean(paras[i])
    assert '[[' not in p and '{{' not in p and '<' not in p, (i, p[:120])
    u = {'txt': p}
    if notes:
        u['note'] = "Poe's note: " + ' — '.join(notes)
    text.append(u)

SECTIONS = [
    ('arg',  'Automata and the engine: the argument', 0, 5),
    ('hist', 'History and the exhibition',            5, 10),
    ('att',  'Earlier attempts at the secret',        10, 14),
    ('sol',  'The solution',                          14, 18),
    ('obs',  'The seventeen observations',            18, 38),
]

out = {
    'id': 'poe',
    'autor': 'Edgar Allan Poe',
    'titel': "Maelzel's Chess-Player (1836)",
    'jahr': 1836,
    'lang': 'en',
    'zitierweise': 'MCP [n]',
    'quelle': "Southern Literary Messenger, vol. II, no. 5 (April 1836), pp. 318–326 — the original magazine printing, via the Wikisource transcription of that printing, collated against the Edgar Allan Poe Society of Baltimore's text of the same issue. Public domain.",
    'hinweis': "Complete. Paragraph numbers are editorial and continuous. Poe's four footnotes are kept as marked notes; the magazine's woodcut (Poe's 'the cut above') is not reproduced, and his italics are not carried. Poe's factual slips about the Turk's history — the London tour of 1783–84 was Kempelen's, not Maelzel's — are left uncorrected as part of the record, as is his premise that chess cannot be mechanized, which the twentieth century refuted.",
    'sections': [],
}

n = 0
for sid, titel, a, b in SECTIONS:
    units = []
    for k, u in enumerate(text[a:b], start=1):
        n += 1
        units.append({'n': n, 'k': k, **u})
    out['sections'].append({'id': sid, 'titel': titel, 'units': units})

path = f'{REPO}/data/poe_maelzel.json'
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '—', n, 'units,', len(out['sections']), 'sections')
