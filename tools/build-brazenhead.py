# -*- coding: utf-8 -*-
# Build data/brazenhead.json — the brazen head, legend and critic:
#
#   fb     "How Fryer Bacon made a Brasen head to speake" — the brazen-head
#          chapter of The Famous Historie of Fryer Bacon (London: G. Purslowe
#          for F. Grove, [1627]), complete, in the original spelling, from the
#          EEBO-TCP transcription A01692 (the Text Creation Partnership
#          dedicates its transcriptions to the public domain). Miles's songs
#          are kept as verse.
#   naude  Gabriel Naudé, Apologie pour tous les grands personnages qui ont
#          esté faussement soupçonnez de magie (Paris: Targa, 1625), chap.
#          XVIII: the legend of Albert's speaking statue reported and
#          dismantled — transcribed by hand from the page images of the
#          Internet Archive scan (pp. 528-530 and 537); long s normalized,
#          the 1625 orthography (u/v, i/j) kept. English: working translation
#          made for this site.
#
# Usage:
#   python tools/build-brazenhead.py            # fetch the TCP XML from GitHub
#   python tools/build-brazenhead.py fryer.xml  # use a local dump
import io, json, os, re, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TCP = 'https://raw.githubusercontent.com/textcreationpartnership/A01692/master/A01692.xml'

if len(sys.argv) > 1:
    xml = io.open(sys.argv[1], encoding='utf-8').read()
else:
    req = urllib.request.Request(TCP, headers={'User-Agent': 'calculemus-build/1.0'})
    xml = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')

div = next(d for d in re.split(r'(?=<div type="part">)', xml)
           if 'Brasen head to speake' in d)
div = div[:div.find('<div type="part">', 10)] if div.count('<div type="part">') > 1 else div

def clean(t):
    t = t.replace('<g ref="char:EOLhyphen"/>', '')
    t = re.sub(r'<pb[^>]*/>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    return t

# The chapter's prose paragraphs enclose the tune-titles (<head>) and songs
# (<lg>); walk the whole chapter body, splitting it into prose / tune-title /
# verse tokens wherever those boundaries fall, so the songs become their own
# verse units rather than being folded into a paragraph.
body = div[div.find('</head>') + len('</head>'):]     # drop the chapter title
body = re.sub(r'</?p>', '', body)                      # paragraph wrappers gone

blocks = []          # ('p'|'v', text, label)
pending_head = None
pos = 0
for m in re.finditer(r'<head\b[^>]*>(.*?)</head>|<lg\b[^>]*>(.*?)</lg>', body, re.S):
    prose = re.sub(r'\s+', ' ', clean(body[pos:m.start()])).strip()
    if prose:
        blocks.append(('p', prose, None))
        pending_head = None
    if m.group(1) is not None:                         # a tune title
        pending_head = re.sub(r'\s+', ' ', clean(m.group(1))).strip()
    else:                                              # a song stanza
        lines = [re.sub(r'\s+', ' ', clean(l)).strip()
                 for l in re.findall(r'<l\b[^>]*>(.*?)</l>', m.group(2), re.S)]
        stanza = '\n'.join(lines)
        # merge consecutive stanzas (no prose between) into one song unit
        if blocks and blocks[-1][0] == 'v':
            blocks[-1] = ('v', blocks[-1][1] + '\n\n' + stanza, blocks[-1][2])
        else:
            blocks.append(('v', stanza, pending_head))
        pending_head = None
    pos = m.end()
tail = re.sub(r'\s+', ' ', clean(body[pos:])).strip()
if tail:
    blocks.append(('p', tail, None))

fb_units = []
for k, (kind, txt, label) in enumerate(blocks, start=1):
    u = {'n': k, 'k': k, 'txt': txt}
    if kind == 'v':
        u['verse'] = True
    if label:
        u['label'] = label
    fb_units.append(u)
assert any(u.get('verse') for u in fb_units), 'no verse blocks found'
assert any('Time is' in u['txt'] for u in fb_units), 'Time is scene missing'
print('chapbook blocks:', [(kind, len(t)) for kind, t, _ in blocks])

NAUDE = [
 {
  'orig': "Il ne reste donc maintenant qu'à refuter l'erreur de ceux qui se sont persuadez que l'on pouuoit forger des testes d'airain sous certaines constellations, lesquelles rendoient par apres des responses, & seruoient à ceux qui les possedoient de guide & de conduitte en toutes leurs affaires, comme vn certain Yepes dit que Henry de Villeine en auoit faict vne à Madrith qui fut brisée par le commandement de Iean 2. Roy de Castille: ce que Barthelemy Sibille & l'autheur de l'Image du monde asseurent pareillement de Virgile, Guillaume de Malmesbery de Syluestre, Iean Gouuerus de Robert de Lincolne, la populace d'Angleterre de Roger Baccon, & Tostat Euesque d'Auila, George Venitien, Delrio, Sibille, Raguseus, Delancre, & plusieurs autres qu'il seroit ennuyeux de specifier, d'Albert le Grand, lequel comme le plus expert auoit composé vn homme entier de cette sorte, ayant trauaillé trente ans sans discontinuation à le forger sous diuers aspects & constellations, les yeux par exemple, au recit du susdit Tostat en ses Commentaires sur l'Exode, lors que le Soleil estoit au signe du Zodiaque correspondant à vne telle partie, lesquels il fondoit de metaux meslangez ensemble & marquez des caracteres des mesmes signes & planetes & de leurs aspects diuers & necessaires; & ainsi la teste, le col, les espaules, les cuisses & les iambes façonnez en diuers temps & montez & reliez ensemble en forme d'homme, auoient cette industrie de reueler audit Albert la solution de toutes ses principales difficultez.",
  'txt': "It remains now only to refute the error of those who have persuaded themselves that heads of brass could be forged under certain constellations, which afterwards gave answers, and served those who possessed them as guide and direction in all their affairs: as a certain Yepes says that Enrique de Villena made one at Madrid, which was broken by command of John II, King of Castile; which Bartolomeo Sibylla and the author of the Image of the World affirm likewise of Virgil, William of Malmesbury of Sylvester, John Gower of Robert of Lincoln, the common people of England of Roger Bacon, and Tostado, Bishop of Ávila, Giorgio Veneto, Delrio, Sibylla, Raguseus, Delancre, and several others whom it would be tedious to specify, of Albert the Great — who, as the most expert, had composed an entire man of this sort, having laboured thirty years without interruption to forge him under divers aspects and constellations: the eyes, for example, by the account of the said Tostado in his commentaries on Exodus, when the Sun stood in the sign of the Zodiac corresponding to such a part; casting them of metals mingled together and marked with the characters of the same signs and planets and of their divers and necessary aspects; and thus the head, the neck, the shoulders, the thighs and the legs, fashioned at divers times and mounted and joined together in the form of a man, had this power: to reveal to the said Albert the solution of all his principal difficulties.",
 },
 {
  'orig': "A quoy, pour ne rien oublier de ce qui appartient à l'histoire de cette statuë, l'on adiouste qu'elle fut brisée & mise en pieces par S. Thomas, qui ne put supporter auec patience son trop grand babil & caquet.",
  'txt': "Whereto — that nothing be omitted of what belongs to the history of this statue — it is added that it was broken and dashed to pieces by St. Thomas, who could not bear with patience its excessive babble and prattle.",
 },
 {
  'orig': "Or pour iuger plus sainement ce que l'on doit croire de cette Androide d'Albert & de toutes ces testes merueilleuses, i'estime que l'on ne peut manquer de deduire l'origine de cette fable du Teraph des Hebrieux.",
  'txt': "Now, to judge more soundly what one ought to believe of this Android of Albert and of all these marvellous heads, I hold that one cannot fail to derive the origin of this fable from the teraph of the Hebrews.",
  'note': "The sentence continues; Naudé's derivation of the fable from the teraphim, and his refutation of the astrological mechanism, pp. 530–537, are omitted here. His 'Androide' is among the earliest occurrences of the word later adopted for artificial humans.",
 },
 {
  'orig': "De sorte que nous pouuons iuger asseurément qu'il est vray ce que le Prophete Royal a dit en ses Pseaumes, Simulachra gentium argentum & aurum, os habent & non loquentur, neque enim est spiritus in ore ipsorum.",
  'txt': "So that we may judge with assurance that what the Royal Prophet said in his Psalms is true: The idols of the nations are silver and gold; they have mouths, and shall not speak; neither is there any breath in their mouths.",
  'note': "Marginal reference of the print: Psal. 134. vers. 15 & 17 (Vulgate numbering).",
 },
]

n0 = len(fb_units)
naude_units = [{'n': n0 + k, 'k': k, **u} for k, u in enumerate(NAUDE, start=1)]

out = {
 'id': 'brazenhead',
 'autor': 'The brazen head — legend and critic',
 'titel': 'The brazen head: The Famous Historie of Fryer Bacon (1627) · Naudé, Apologie (1625)',
 'jahr': 1627,
 'lang': 'en',
 'zitierweise': 'FB [k] · Apol. [k]',
 'quelle': ("The Famous Historie of Fryer Bacon (London: G. Purslowe for F. Grove, [1627]), "
            "the brazen-head chapter complete, in the original spelling, from the EEBO-TCP "
            "transcription A01692 (dedicated to the public domain by the Text Creation "
            "Partnership). Gabriel Naudé, Apologie pour tous les grands personnages qui ont "
            "esté faussement soupçonnez de magie (Paris: François Targa, 1625), chap. XVIII, "
            "pp. 528–530 and 537, transcribed by hand from the page images of the Internet "
            "Archive scan; long s normalized, the 1625 orthography kept. Both public domain."),
 'hinweis': ("The legend and its critic, side by side — the corpus's pattern for automata "
             "tales since the Turk: carried is the debate, not a machine, for the head of "
             "the story never existed. The chapbook chapter is complete; Miles's mocking "
             "songs are kept as verse. Of Naudé's chapter, the report of the legend and "
             "the verdict are carried, his teraphim digression omitted as marked; his "
             "marginal source citations are omitted except as noted. Paragraph numbers "
             "are editorial and continuous across both sections. The English of the Naudé "
             "section is this site's unofficial working translation — cite the original."),
 'sections': [
   {'id': 'fb', 'titel': 'How Fryer Bacon made a Brasen head to speake (The Famous Historie, 1627)',
    'units': fb_units},
   {'id': 'naude', 'titel': "Naudé: the Androide of Albert, reported and dismantled (Apologie, 1625)",
    'units': naude_units},
 ],
}

path = os.path.join(REPO, 'data', 'brazenhead.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', n0 + len(NAUDE), 'units')
