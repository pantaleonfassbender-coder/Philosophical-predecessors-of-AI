# Build the La Mettrie ship file: DP beads + three hand corrections + working
# translations for the seven paragraphs the 1912 Bussey translation omits.
import io, json, re

pairs = json.load(io.open('C:/Users/leofa/AppData/Local/Temp/aipred/lamettrie-aligned.json', encoding='utf-8'))

# --- correction 1: beads 81 (false omission) + 82 (2:1) -> one 2:1 bead
assert pairs[81][1] == '' and pairs[82][2] == 2
fr_merged = pairs[81][0] + ' ' + pairs[82][0]
pairs[81:83] = [[fr_merged, pairs[82][1], 2, 1]]

# --- correction 2: bead 35 (2:1 wrongly swallowing an omitted paragraph)
i35 = next(i for i, p in enumerate(pairs) if p[0].startswith('Quelle autre fureur'))
f = pairs[i35][0]
cut = f.find('Il ne faut que des yeux')
assert cut > 0
pairs[i35:i35+1] = [[f[:cut].strip(), '', 1, 0], [f[cut:].strip(), pairs[i35][1], 1, 1]]

# --- correction 3: bead with 'Mais comment en expliquer' (2:1 swallowing omission)
i156 = next(i for i, p in enumerate(pairs) if p[0].startswith('Mais comment en expliquer'))
f = pairs[i156][0]
cut = f.find('Nous sommes de vraies taupes')
assert cut > 0
pairs[i156:i156+1] = [[f[:cut].strip(), '', 1, 0], [f[cut:].strip(), pairs[i156][1], 1, 1]]

# --- working translations for the omitted paragraphs
TR = {
 'La grossesse': "Pregnancy, that desired rival of the pale complexion, is not content to bring in its train, as it most often does, the depraved tastes that accompany these two states: it has sometimes made the soul carry out the most frightful designs — the effects of a sudden mania which smothers even the natural law. Thus the brain, that womb of the mind, is perverted in its own way, along with that of the body.",
 'Quelle autre fureur': "What other fury, of man or of woman, in those whom continence and health pursue! It is a small thing for that timid and modest girl to have lost all shame and all modesty: she now regards incest no otherwise than a gallant woman regards adultery. If her needs find no prompt relief, they will not stop at the mere accidents of a uterine passion, at mania, and the rest: the unhappy creature will die of an ill for which there are so many physicians.",
 'Pourquoi la vue': "Why does the sight, or the mere idea, of a beautiful woman cause in us singular movements and desires? Does what then happens in certain organs come from the nature of those organs themselves? Not at all; but from the commerce, and the kind of sympathy, of these muscles with the imagination. There is here only a first spring, excited by the bene placitum of the ancients, or by the image of beauty, which excites another that lay fast asleep until the imagination woke it: and how does this come about, if not by the disorder and tumult of the blood and the spirits, which gallop with extraordinary promptness and swell the cavernous bodies?",
 "Puisqu'il est des communications": "Since there are evident communications between mother and child, and since it is hard to deny facts reported by Tulpius and by other writers as worthy of belief (there are none more so), we shall believe that it is by the same way that the foetus feels the impetuosity of the maternal imagination, as soft wax receives all sorts of impressions; and that the same traces, or longings, of the mother can imprint themselves on the foetus, without this being comprehensible, whatever Blondel and all his adherents may say. Thus we make honourable amends to Father Malebranche, far too much mocked for his credulity by authors who have not observed nature closely enough, and have wished to subject her to their ideas.",
 "J'en appelle": "I appeal to the good faith of our observers. Let them tell us whether it is not true that man is in his origin but a worm, which becomes a man as the caterpillar becomes a butterfly. The gravest authors have taught us how to go about seeing this little animal. All the curious have seen it, like Hartsoeker, in the seed of the man, and not in that of the woman; only fools have made a scruple of it. As each drop of sperm contains an infinity of these little worms, when they are launched toward the ovary only the most adroit or the most vigorous has the force to insinuate itself and implant itself in the egg supplied by the woman, which gives it its first nourishment. This egg, sometimes caught in the Fallopian tubes, is carried by these canals to the womb, where it takes root like a grain of wheat in the earth. But although it grows monstrous there by its nine months' growth, it differs in nothing from the eggs of other females, except that its skin (the amnion) never hardens, and dilates prodigiously — as one may judge by comparing foetuses found in place and near to hatching (which I have had the pleasure of observing in a woman who died a moment before delivery) with other little embryos very near their origin: for then it is always the egg in its shell, and the animal in the egg, which, hindered in its movements, seeks mechanically to see the light of day; and to succeed in this it begins by breaking with its head that membrane, from which it comes forth as the chicken, the bird, and so on come forth from theirs. I will add one observation that I find nowhere: that the amnion is no thinner for having been prodigiously stretched — like the womb in this, whose very substance swells with infiltrated juices, independently of the filling and unfolding of all its vascular folds.",
 'Voilà à peu près': "That is about all that is known of generation. That the parts which attract each other, which are made to unite together and to occupy this or that place, should all come together according to their nature, and that thus are formed the eyes, the heart, the stomach, and finally the whole body — as great men have written — is possible. But since experience abandons us in the midst of these subtleties, I shall suppose nothing, regarding everything that does not strike my senses as an impenetrable mystery. It is so rare that the two seeds meet in congress that I should be tempted to believe that the woman's seed is useless to generation.",
 'Mais comment en expliquer': "But how explain its phenomena without that convenient relation of parts, which accounts so well for the resemblances of children, now to the father and now to the mother? On the other hand, should the difficulty of an explanation outweigh a fact? It appears to me that it is the male that does everything, in a woman who sleeps as in the most lascivious. The arrangement of the parts would thus have been made from all eternity in the germ, or in the very worm, of the man. But all this is far above the reach of the most excellent observers. As they can seize nothing of it, they can no more judge of the mechanics of the formation and development of bodies, than a mole can judge of the road a stag can run.",
}
NOTE = ("This paragraph is silently omitted by the 1912 Bussey translation; the English here is an "
        "unofficial working translation made for this site.")

units = []
missing = 0
for f, e, a, b in pairs:
    u = {'orig': f, 'txt': e}
    if not e:
        key = next((k for k in TR if f.startswith(k)), None)
        assert key, f[:60]
        u['txt'] = TR[key]
        u['note'] = NOTE
        missing += 1
    units.append(u)
assert missing == 7, missing

# editorial parts for navigability
CUTS = [(0, 45, 'p1', 'The soul follows the body'),
        (45, 105, 'p2', 'Man among the animals'),
        (105, 139, 'p3', 'The springs of the machine'),
        (139, len(units), 'p4', 'Generation, and the conclusion')]
sections = []
n = 0
for lo, hi, sid, titel in CUTS:
    us = []
    for k, u in enumerate(units[lo:hi], 1):
        n += 1
        u2 = dict(u); u2['n'] = n; u2['k'] = k
        us.append(u2)
    sections.append({'id': sid, 'titel': titel, 'units': us})

out = {
 'id': 'lamettrie',
 'autor': 'Julien Offray de La Mettrie',
 'titel': "L'Homme Machine / Man a Machine (1747)",
 'jahr': 1747,
 'lang': 'fr',
 'zitierweise': 'HM [n]',
 'quelle': ("L'Homme Machine (Leyden: Elie Luzac, 1747). French text and Gertrude C. Bussey's English "
            'translation from the Open Court edition (Chicago, 1912), via the Project Gutenberg '
            'transcription #52090. Both public domain.'),
 'hinweis': ('The paragraph numbers are editorial and continuous; the four part titles are editorial. '
             'Alignment is paragraph-for-paragraph against the French; where the 1912 translation '
             'merges French paragraphs, they are shown merged. Seven paragraphs that the 1912 '
             'translation silently omits are restored with working translations, marked in place.'),
 'sections': sections,
}
json.dump(out, io.open('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/lamettrie_hommemachine.json', 'w', encoding='utf-8'), ensure_ascii=False)
import os
print('units:', n, 'omissions restored:', missing,
      'size:', os.path.getsize('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/lamettrie_hommemachine.json'))
