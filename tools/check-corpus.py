# -*- coding: utf-8 -*-
"""Consistency check for the Calculemus corpus.

Verifies, across the registry, the edition files, app.js and the Atlas:
  1. every registry entry has its data file, and every data file its entry;
  2. unit numbering is complete, duplicate-free and per-section consistent;
  3. every shipped work has a CITE entry in app.js;
  4. every INTRO_LINKS phrase and Reading-Paths station resolves to an
     existing work/section, and every link phrase occurs in the essay;
  5. every Atlas node citation resolves to a real work/section/paragraph,
     and the Atlas paragraph count matches the corpus;
  6. no stale module counts survive in app.js or the introduction;
  7. every module is named in README.md, SOURCES.md and LICENSES.md.

Run from anywhere: python tools/check-corpus.py
Exit code 0 = clean; 1 = errors (warnings alone do not fail the check).
"""
import json, io, os, re, glob, sys

if hasattr(sys.stdout, 'reconfigure'):        # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

errors, warns = [], []
works = json.load(io.open('data/works.json', encoding='utf-8'))
app = io.open('app.js', encoding='utf-8').read()

# 1. registry <-> files
shipped = [w for w in works if w['status'] == 'shipped']
print(f'registry: {len(works)} entries, {len(shipped)} shipped')
texts = {}
for w in shipped:
    p = f"data/{w['datei']}.json"
    if not os.path.exists(p):
        errors.append(f'missing data file: {p}'); continue
    texts[w['id']] = json.load(io.open(p, encoding='utf-8'))
    for f in ('id', 'linie', 'autor', 'leben', 'kurz', 'titel', 'sprachen', 'claim', 'datei'):
        if not w.get(f):
            errors.append(f"{w['id']}: registry field {f} empty")
registered = {w['datei'] for w in works}
for p in glob.glob('data/*.json'):
    b = os.path.basename(p)[:-5]
    if b not in registered and b not in ('works', 'network', 'introduction'):
        warns.append(f'unregistered data file: {b}')

# 2. unit integrity
total_units = 0
for wid, t in texts.items():
    for s in t['sections']:
        if not s.get('units'):
            errors.append(f'{wid}/{s.get("id")}: no units')
        for k, u in enumerate(s['units'], start=1):
            if u.get('k') != k:
                warns.append(f'{wid}/{s["id"]}: k mismatch at n={u.get("n")}')
            if not (u.get('txt') or u.get('orig')):
                errors.append(f'{wid}/{s["id"]}: empty unit {u.get("n")}')
    ns = [u['n'] for s in t['sections'] for u in s['units']]
    if len(ns) != len(set(ns)):
        errors.append(f'{wid}: duplicate n values')
    total_units += len(ns)
    if t.get('id') != wid:
        errors.append(f'{wid}: inner id={t.get("id")}')
    for f in ('titel', 'jahr', 'zitierweise', 'quelle', 'hinweis'):
        if not t.get(f):
            warns.append(f'{wid}: module field {f} missing')
print('total units across corpus:', total_units)

# 3. CITE entries
m = re.search(r'const CITE = \{(.*?)\n\};', app, re.S)
cite_ids = set(re.findall(r'^\s{2}(\w+):', m.group(1), re.M))
for w in shipped:
    if w['id'] not in cite_ids:
        errors.append(f"no CITE entry for {w['id']}")

# 4a. linie keys
linien = {w['linie'] for w in works}
if not linien <= {'logic', 'maschine', 'gegen', 'wort'}:
    errors.append(f'unknown linie: {linien}')

# 4b. INTRO_LINKS + PATHS targets
sec_ids = {wid: {s['id'] for s in t['sections']} for wid, t in texts.items()}
mlinks = re.search(r'const INTRO_LINKS = \[(.*?)\n\];', app, re.S)
intro_links = re.findall(r'\["([^"]+)", "(#/[^"]+)"\]', mlinks.group(1))
for phrase, href in intro_links:
    mm = re.match(r'#/works/(\w+)(?:/(\w+))?$', href)
    if mm:
        wid, sid = mm.group(1), mm.group(2)
        if wid not in texts:
            errors.append(f'INTRO_LINK "{phrase}" -> unknown work {wid}')
        elif sid and sid not in sec_ids[wid]:
            errors.append(f'INTRO_LINK "{phrase}" -> unknown section {wid}/{sid}')
for href in re.findall(r'href: "(#/works/[^"@]+)"', app):
    parts = href[8:].split('/')
    wid = parts[0]; sid = parts[1] if len(parts) > 1 else None
    if wid not in texts:
        errors.append(f'PATHS href unknown work: {href}')
    elif sid and sid not in sec_ids[wid]:
        errors.append(f'PATHS href unknown section: {href}')

# 4c. link phrases occur in the essay
intro = json.load(io.open('data/introduction.json', encoding='utf-8'))
essay = ' '.join(p for s in intro['abschnitte'] for p in s['paras'])
plain = essay.replace('*', '')
for phrase, href in intro_links:
    if phrase not in plain:
        warns.append(f'INTRO_LINK phrase not in essay: "{phrase}"')

# 5. Atlas
net = json.load(io.open('data/network.json', encoding='utf-8'))
print('network n_units:', net['n_units'])
if net['n_units'] != total_units:
    errors.append(f'atlas out of date: n_units {net["n_units"]} != corpus {total_units} '
                  '(re-run tools/build-network.py)')
bad = 0
for node in net['nodes']:
    for wid, sid, un in node['cites']:
        t = texts.get(wid)
        s = t and next((x for x in t['sections'] if x['id'] == sid), None)
        if not s or not any(u['n'] == un for u in s['units']):
            bad += 1
if bad:
    errors.append(f'network: {bad} unresolvable cites')
else:
    print('network: all node cites resolve')

# 6. counts in prose (a number word directly before "modules" that isn't the real count)
COUNT_WORDS = {16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty',
               21: 'twenty-one', 22: 'twenty-two', 23: 'twenty-three', 24: 'twenty-four',
               25: 'twenty-five', 26: 'twenty-six', 27: 'twenty-seven', 28: 'twenty-eight'}
current = COUNT_WORDS.get(len(shipped))
if current:
    for n, wword in COUNT_WORDS.items():
        if n == len(shipped):
            continue
        for txt, name in ((app, 'app.js'), (essay, 'introduction')):
            if re.search(wword + r'(?: shipped)? modules', txt):
                errors.append(f'stale count in {name}: "{wword} ... modules" (corpus has {len(shipped)})')
    if f'{current} modules shipped' not in app:
        errors.append(f'method-page count is not "{current} modules shipped"')
else:
    warns.append(f'count-word table has no entry for {len(shipped)} — extend COUNT_WORDS')

# 7. every module named in the docs
readme = io.open('README.md', encoding='utf-8').read().lower()
sources = io.open('SOURCES.md', encoding='utf-8').read().lower()
lic = io.open('LICENSES.md', encoding='utf-8').read().lower()
KEY = {'hobbes': 'hobbes', 'leibniz': 'leibniz', 'boole': 'boole', 'frege': 'frege',
       'llull': 'llull', 'kircher': 'kircher', 'khwarizmi': 'rosen', 'zairja': 'zāʾirja',
       'yijing': 'yijing', 'pascal': 'pascal', 'lovelace': 'lovelace', 'jevons': 'jevons',
       'peirce': 'peirce', 'avicenna': 'avicenna', 'descartes': 'descartes',
       'lamettrie': 'mettrie', 'poe': 'poe', 'butler': 'butler', 'kapp': 'kapp',
       'liezi': 'liezi', 'automata': 'aristotle', 'golem': 'olem',
       'zauberlehrling': 'zauberlehrling', 'capek': 'apek', 'brazenhead': 'brazen'}
for wid in texts:
    key = KEY.get(wid)
    if not key:
        warns.append(f'doc-presence check has no key for new module "{wid}" — extend KEY')
        continue
    for name, txt in (('README', readme), ('SOURCES', sources), ('LICENSES', lic)):
        if key not in txt:
            errors.append(f'{wid} ({key}) missing in {name}')

print()
print('ERRORS:', len(errors))
for e in errors:
    print('  !!', e)
print('WARNINGS:', len(warns))
for w in warns:
    print('  ?', w)
sys.exit(1 if errors else 0)
