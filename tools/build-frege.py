# -*- coding: utf-8 -*-
# Build data/frege_texte.json from frege-draft.json + working translations.
import io, json, re, sys
sys.path.insert(0, '.')
from en_bs import BS_EN, BS_FN_EN
from en_gl import GL_EN
from en_sb import SB_EN, SB_FN_EN

d = json.load(io.open('frege-draft.json', encoding='utf-8'))

# small source repairs: journal colophon leaks
for u in d['sb']:
    u['orig'] = re.sub(r'\s*Ztschrft\. f\. Philos\. u\. philos\. Kritik\. 100 Bd\. 4\s*', ' ', u['orig'])
    for k in ('fn', 'fn2'):
        if k in u:
            u[k] = re.sub(r'\s*Zeitsch(rft)?\.?.*$', '', u[k]).strip()
for u in d['bs']:
    u['orig'] = u['orig'].replace('$ 3', '§ 3').replace('$6', '§ 6').replace('„Formelsprache', '„Formelsprache')

assert len(BS_EN) == len(d['bs']), (len(BS_EN), len(d['bs']))
assert len(GL_EN) == len(d['gl']), (len(GL_EN), len(d['gl']))
assert len(SB_EN) == len(d['sb']), (len(SB_EN), len(d['sb']))

def note_of(u, fn_en_map, idx=None):
    parts = []
    for k in ('fn', 'fn2'):
        if k not in u: continue
        de = u[k]
        en = None
        for pref, tx in fn_en_map.items():
            if isinstance(pref, str) and de.startswith(pref):
                en = tx; break
        if en is None and idx in fn_en_map:
            en = fn_en_map[idx]
        parts.append(f"Frege's footnote: „{de}“ — {en}" if en else f"Frege's footnote: „{de}“")
    return ' · '.join(parts) if parts else None

sections = []
n = 0
def mk_units(units, ens, cite_fn, fn_map):
    global n
    out = []
    for k, (u, en) in enumerate(zip(units, ens), 1):
        if isinstance(en, tuple):
            pref, txt = en
            o = u['orig'].lstrip('„»" ')
            assert o.startswith(pref.lstrip('„»" ')[:18]), (pref[:40], u['orig'][:40])
        else:
            txt = en
        n += 1
        v = {'n': n, 'k': k, 'orig': u['orig'], 'txt': txt, 'c': cite_fn(k, u)}
        if u.get('part'):
            v['label'] = u['part'].replace(' (Forts. ', ', continued (').replace(')', ')') if '(Forts.' in u['part'] else u['part']
        nt = note_of(u, fn_map, idx=k - 1)
        if nt: v['note'] = nt
        out.append(v)
    return out

# citation builders
def cite_bs(k, u): return f'BS, Vorwort [{k}]'
def cite_gl(k, u):
    p = u.get('part', '')
    base = 'Einl.' if p.startswith('Einleitung') else p.split(' (')[0]
    m = re.search(r'Forts\. (\d+)', p)
    j = int(m.group(1)) + 1 if m else 1
    if base == 'Einl.':
        return f'GL, Einl. [{k}]'
    return f'GL, {base}' + (f' [{j}]' if (m or True) and j > 1 else '')
def cite_sb(k, u): return f'SuB [{k}]'

bs_units = mk_units(d['bs'], BS_EN, cite_bs, BS_FN_EN)
gl_units = mk_units(d['gl'], GL_EN, cite_gl, {})
sb_units = mk_units(d['sb'], SB_EN, cite_sb, SB_FN_EN)

sections = [
 {'id': 'bs', 'titel': 'Begriffsschrift (1879) — Vorwort / Preface', 'units': bs_units},
 {'id': 'gl', 'titel': 'Die Grundlagen der Arithmetik (1884) — Einleitung, §§ 1–4, 87–91, 106–109',
  'units': gl_units},
 {'id': 'sb', 'titel': 'Über Sinn und Bedeutung (1892) — complete', 'units': sb_units},
]
out = {
 'id': 'frege',
 'autor': 'Gottlob Frege',
 'titel': 'Begriffsschrift (preface) · Grundlagen der Arithmetik (selections) · Über Sinn und Bedeutung',
 'jahr': 1892,
 'lang': 'de',
 'zitierweise': 'BS, Vorwort [k] / GL, § 87 / SuB [n]',
 'quelle': ("Begriffsschrift: Vorwort of the 1879 Halle edition, from the Internet Archive scan "
            "(OCR emended by hand). Grundlagen der Arithmetik: Breslau 1884, from the Project "
            "Gutenberg transcription #48312. Über Sinn und Bedeutung: Zeitschrift für Philosophie "
            "und philosophische Kritik 100 (1892), pp. 25–50, complete, from the Deutsches "
            "Textarchiv transcription of the journal printing (long s normalized). All public "
            "domain in the United States."),
 'hinweis': ("No public-domain English translation of any of these texts exists; all English in "
             "this module is an unofficial working translation made for this site — cite the "
             "German. 'Bedeutung' is rendered 'reference', 'Sinn' 'sense'. Frege's own footnotes "
             "are kept and marked in place; his reference apparatus is omitted. The paragraph "
             "numbers are editorial; Grundlagen sections carry Frege's § numbers. The "
             "two-dimensional Begriffsschrift notation is not reproduced (prose preface only), "
             "as announced on the method page."),
 'sections': sections,
}
json.dump(out, io.open('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/frege_texte.json', 'w', encoding='utf-8'), ensure_ascii=False)
import os
print('units:', n, 'size:', os.path.getsize('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/frege_texte.json'))
print('sample cites:', [u['c'] for u in gl_units[17:24]], '|', sb_units[0]['c'])
missing_fn = [u['n'] for u in sb_units if 'note' in u and '— None' in u['note']]
print('missing fn translations:', missing_fn)
