# -*- coding: utf-8 -*-
# Build assets/plates/ and data/plates.json — one public-domain plate per
# module: title pages, frontispieces and diagrams from the same
# digitisations the editions cite, fetched page by page over IIIF (no full
# scans are downloaded or carried), plus Wikimedia Commons files where the
# pinned scan carries no usable image. Faithful reproduction of a
# public-domain two-dimensional work adds nothing licensable; every plate
# names its source, digitisation and leaf below.
#
# First tranche: ten modules. Named for later tranches: La Mettrie (a
# usable French 1748 title page has not been sighted on the Archive; the
# BIM 1749 English item refuses image access), Leibniz (the binary table
# of the 1703 Memoires printing), Jevons (the logic piano plate of the
# 1870 Philosophical Transactions paper), the world-roots and word-line
# modules. The brazen-head chapbook is EEBO: the TCP text is open, the
# images are not — no plate from that source.
#
# Usage: python tools/build-plates.py          (needs the network)
import io, json, os, urllib.request
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'assets', 'plates')
os.makedirs(OUT, exist_ok=True)

def ia(item, leaf, w=1400):
    return f"https://iiif.archive.org/iiif/{item}${leaf}/full/{w},/0/default.jpg"

PLATES = [
 { 'id': 'hobbes',
   'url': ia('leviathan00hobba', 5),
   'caption': "The engraved title of the 1651 London printing: the "
              "commonwealth as an artificial man, composed of its citizens.",
   'credit': "Leviathan (London: Andrew Crooke, 1651). Internet Archive "
             "leviathan00hobba, leaf 5. Public domain." },
 { 'id': 'descartes',
   'url': ia('discoursdelamet00desca', 5),
   'caption': "Title page of the anonymous first printing, Leiden 1637 — "
              "the Discours as preface to three essays of the method.",
   'credit': "Discours de la methode (Leyde: Ian Maire, 1637). Internet "
             "Archive discoursdelamet00desca, leaf 5. Public domain." },
 { 'id': 'boole',
   'url': ia('aninvestigation01boolgoog', 8),
   'caption': "Title page of the first edition, London 1854.",
   'credit': "An Investigation of the Laws of Thought (London: Walton and "
             "Maberly, 1854). Internet Archive aninvestigation01boolgoog, "
             "leaf 8. Public domain." },
 { 'id': 'llull',
   'url': ia('BIUSante_pharma_res011289', 26),
   'caption': "The opening of the Ars brevis with the prima figura: the "
              "nine principles B–K on the wheel, every pair joined by a "
              "line — the combinatorial art as a diagram.",
   'credit': "Ars brevis, in the Strasbourg edition of 1617 (Zetzner). "
             "Internet Archive BIUSante_pharma_res011289, leaf 26. Public "
             "domain." },
 { 'id': 'kircher',
   'url': ia('gri_33125008657112', 6),
   'caption': "The engraved frontispiece of 1669: divine Wisdom holds the "
              "tablet of the art's alphabet, light descending on the "
              "sciences below.",
   'credit': "Ars magna sciendi (Amsterdam: Jansson & Weyerstraet, 1669). "
             "Internet Archive gri_33125008657112 (Getty Research "
             "Institute), leaf 6. Public domain." },
 { 'id': 'frege',
   'url': ia('11388662', 22),
   'caption': "A page of the Begriffsschrift's two-dimensional notation — "
              "judgment stroke, conditional and negation drawn rather than "
              "written in line.",
   'credit': "Begriffsschrift (Halle: Nebert, 1879). Internet Archive "
             "11388662, leaf 22. Public domain." },
 { 'id': 'lovelace',
   'url': ia('india.history.resource.53369', 757),
   'wide': True,
   'caption': "The fold-out of Note G: “Diagram for the computation by the "
              "Engine of the Numbers of Bernoulli” — the table read today "
              "as the first published program. The Calcutta copy's sheet "
              "is stained and torn; it is carried as it survives.",
   'credit': "Taylor, Scientific Memoirs, vol. III (London 1843), fold-out "
             "at Note G. Internet Archive india.history.resource.53369, "
             "leaf 757. Public domain." },
 { 'id': 'poe',
   'url': "https://upload.wikimedia.org/wikipedia/commons/3/36/%E2%80%9CThe_Turk.%E2%80%9D_Engraving_in_Joseph_Friedrich_Racknitz%2C_Ueber_den_schachspieler_des_herrn_von_Kempelen_und_dessen_nachbildung_%282919837469%29.jpg",
   'caption': "Racknitz's engraving of the Turk with its cabinet opened — "
              "the exhibition Poe's essay reasons from.",
   'credit': "J. F. zu Racknitz, Ueber den Schachspieler des Herrn von "
             "Kempelen (Leipzig/Dresden 1789), plate. Smithsonian "
             "Libraries copy, via Wikimedia Commons. No known "
             "restrictions." },
 { 'id': 'kapp',
   'url': "https://api.digitale-sammlungen.de/iiif/image/v2/bsb11379066_00135/full/1400,/0/default.jpg",
   'caption': "The load-bearing lattice of the human femur, drawn as an "
              "engineer's truss — Kapp's key exhibit: the built structure "
              "unconsciously repeats the organ.",
   'credit': "Grundlinien einer Philosophie der Technik (Braunschweig "
             "1877). Bayerische Staatsbibliothek / MDZ bsb11379066, scan "
             "135. Public domain." },
 { 'id': 'capek',
   'url': "https://upload.wikimedia.org/wikipedia/commons/a/ad/Rosumovi_Univerz%C3%A1ln%C3%AD_Roboti_1920.jpg",
   'caption': "Cover of the first edition, Prague (Aventinum) 1920, "
              "designed by Josef Čapek — the word robot enters the world.",
   'credit': "R.U.R. — Rossum's Universal Robots (Prague 1920). Via "
             "Wikimedia Commons. Public domain in the United States "
             "(published 1920)." },
]

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':
        'calculemus-plates (philosophical-predecessors-of-ai.netlify.app)'})
    for attempt in range(4):
        try:
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as e:
            err = e
    raise err

reg = {}
for p in PLATES:
    im = Image.open(io.BytesIO(fetch(p['url']))).convert('RGB')
    if p.get('rotate'):
        im = im.rotate(p['rotate'], expand=True)
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, p['id'] + '.jpg'), quality=82, optimize=True)
    th = im.copy(); th.thumbnail((300, 480), Image.LANCZOS)
    th.save(os.path.join(OUT, p['id'] + '_t.jpg'), quality=80, optimize=True)
    reg[p['id']] = {'caption': p['caption'], 'credit': p['credit']}
    if p.get('wide'):
        reg[p['id']]['wide'] = True
    print('plate', p['id'], im.size)

path = os.path.join(REPO, 'data', 'plates.json')
json.dump(reg, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', len(reg), 'plates')
