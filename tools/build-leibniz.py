# -*- coding: utf-8 -*-
# Build data/leibniz_anthology.json:
#  mon  - Monadology, 90 sections, FR (PG #17641) / EN (Latta 1898, Wikisource
#         transcription of the PD translation)
#  bin  - Explication de l'arithmétique binaire (1703), FR (Gerhardt GM7
#         223-227 via the French Wikisource transcription) / working EN
#  char - characteristica / calculus fragments, Latin (Gerhardt GP VII, OCR
#         emended by hand) / working EN
#  comb - Dissertatio de arte combinatoria (1666), two selections, Latin
#         (Gerhardt GP IV, OCR emended) / working EN
import io, json, re

units_mon = json.load(io.open('mon-draft.json', encoding='utf-8'))

# ---------------------------------------------------------------- binaire
t = io.open('binaire.txt', encoding='utf-8').read()
t = re.sub(r'\{\\displaystyle[^}]*\}', '', t)
t = re.sub(r'\s+', ' ', t)
def cut(a, b):
    i = t.find(a); j = t.find(b, i)
    assert i >= 0 and j > i, (a[:30], b[:30])
    return t[i:j + len(b)].strip()

TO = '[table omitted]'
bin_fr = [
 cut("Le calcul ordinaire d’Arithmétique", "et dix fois mille par 10000, et ainsi de suite."),
 cut("Mais au lieu de la progression de dix en dix", "tant que l’on voudra.") + ' ' + TO,
 cut("On voit ici d’un coup d’oeil", "avec peu de pièces."),
 cut("Cette expressions des Nombres étant établie", "toutes sortes d’opérations.") + ' [tables omitted]',
 cut("Et toutes ces opérations sont si aisées", "sous les signes ☽ et") + ' ⊙.',
 cut("Cependant je ne recommande point", "il paroit partout un ordre merveilleux."),
 cut("Pour exemple, dans la Table", "est infiniment avantageuse."),
 cut("Ce qu’il y a de surprenant", "signifie le zéro ou 0.") + ' ' + TO,
 cut("Les Chinois ont perdu la signification", "d’autant plus curieuse."),
 cut("Le consentement des figures", "des Maures d’Espagne."),
 cut("Or comme l’on croit à la Chine", "d’aider l’esprit humain."),
]
bin_fr = [re.sub(r'\s+', ' ', x).replace('Cette expressions', 'Cette expression').strip() for x in bin_fr]

bin_en = [
 "The ordinary reckoning of arithmetic is done according to the progression from ten to ten. One makes use of ten characters, namely 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, which signify zero, one, and the following numbers up to nine inclusively. And then, on reaching ten, one begins again, writing ten as 10, ten times ten or a hundred as 100, ten times a hundred or a thousand as 1000, ten times a thousand as 10000, and so on.",
 "But instead of the progression from ten to ten, I have for several years employed the simplest progression of all, which goes from two to two, having found that it serves the perfection of the science of numbers. Thus I employ no characters in it other than 0 and 1, and then, on reaching two, I begin again. This is why two is here written 10, twice two or four as 100, twice four or eight as 1000, twice eight or sixteen as 10000, and so on. Here is the table of numbers in this fashion, which one may continue as far as one pleases. [table omitted]",
 "One sees here at a single glance the reason of a celebrated property of the double geometrical progression in whole numbers: that if one has only one of these numbers of each degree, one can compose from them all the other whole numbers below the double of the highest degree. For here it is as if one said, for example, that 111, or 7, is the sum of four, two and one, and that 1101, or 13, is the sum of eight, four and one. This property serves assayers to weigh all sorts of masses with few weights, and could serve in coinage to give several values with few pieces.",
 "This expression of numbers, once established, serves to carry out very easily all sorts of operations. [tables omitted]",
 "And all these operations are so easy that there is never any need to try or to guess anything, as must be done in ordinary division. Nor is there any need to learn anything by heart here, as must be done in ordinary reckoning, where one must know, for example, that 6 and 7 taken together make 13, and that 5 multiplied by 3 gives 15, according to the table of once one is one, which is called Pythagorean. But here all of that is found and proved from the source, as one sees in the preceding examples under the signs ☽ and ⊙.",
 "However, I do not at all recommend this manner of counting with a view to introducing it in place of the ordinary practice by ten. For besides the fact that we are accustomed to the latter, there is no need in it to learn what one has already learnt by heart: the practice by ten is thus shorter, and the numbers in it are less long. And if one were accustomed to go by twelve or by sixteen, there would be still more advantage in it. But reckoning by two, that is by 0 and by 1, in recompense for its length, is the most fundamental for science, and yields new discoveries which prove useful afterwards, even for the practice of numbers, and above all for geometry: the reason being that, the numbers being reduced to the simplest principles, such as 0 and 1, a wonderful order appears throughout.",
 "For example, in the table of numbers itself one sees in each column periods reigning which always begin again. In the first column it is 01, in the second 0011, in the third 00001111, in the fourth 0000000011111111, and so on. And small zeros have been put into the table to fill the void at the beginning of the column, and the better to mark these periods. Lines have also been drawn in the table, which mark that what these lines enclose always recurs beneath them. And it is found further that the square numbers, the cubes and the other powers, likewise the triangular numbers, the pyramidal numbers and the other figurate numbers, have similar periods as well, so that their tables can be written out at once, without calculating. And a prolixity at the beginning, which afterwards gives the means of sparing calculation and of going to infinity by rule, is infinitely advantageous.",
 "What is surprising in this reckoning is that this arithmetic by 0 and 1 is found to contain the mystery of the lines of an ancient king and philosopher named Fohy, who is believed to have lived more than four thousand years ago, and whom the Chinese regard as the founder of their empire and of their sciences. There are several linear figures attributed to him; they all come back to this arithmetic. But it suffices to set down here the Figure of the eight Cova, as it is called, which passes for fundamental, and to join to it the explanation, which is manifest, provided one notes first that a whole line — signifies unity or 1, and secondly that a broken line - - signifies zero or 0. [table omitted]",
 "The Chinese have lost the signification of the Cova, or lineations of Fohy, perhaps for more than a thousand years, and they have written commentaries upon them in which they have sought I know not what far-fetched meanings; so that the true explanation has now had to come to them from the Europeans. It happened thus: scarcely more than two years ago I sent to Father Bouvet, the celebrated French Jesuit who lives at Peking, my manner of counting by 0 and 1, and no more was needed for him to recognize in it the key to the figures of Fohy. So, writing to me on 14 November 1701, he sent me the great figure of that philosopher prince, which goes to 64, and leaves no further room to doubt the truth of our interpretation; so that it may be said that this Father has deciphered the enigma of Fohy by the help of what I had communicated to him. And as these figures are perhaps the most ancient monument of science in the world, this restitution of their meaning, after so great an interval of time, will appear all the more curious.",
 "The agreement between the figures of Fohy and my table of numbers is best seen when, in the table, one supplies the initial zeros, which seem superfluous but serve the better to mark the period of the column, as I have in fact supplied them with little rings, to distinguish them from the necessary zeros; and this accord gives me a high opinion of the depth of the meditations of Fohy. For what seems easy to us now was not so at all in those remote times. Binary or dyadic arithmetic is indeed very easy today, with little thought, because our manner of counting assists it greatly, since it seems that one merely cuts away the excess. But this ordinary arithmetic by ten does not seem very ancient; at least the Greeks and the Romans were ignorant of it and were deprived of its advantages. It seems that Europe owes its introduction to Gerbert, afterwards Pope under the name of Sylvester II, who had it from the Moors of Spain.",
 "Now, as it is believed in China that Fohy is also the author of the Chinese characters, though greatly altered by the passage of time, his essay in arithmetic suggests that something considerable with respect to numbers and ideas might yet be found in them, if one could unearth the foundation of the Chinese writing; the more so as it is believed in China that he had regard to numbers in establishing it. The Reverend Father Bouvet is strongly inclined to push this point, and very capable of succeeding in it in many ways. However, I do not know whether there was ever in the Chinese writing an advantage approaching the one that must necessarily be in a Characteristic which I project. It is that every reasoning which can be drawn from notions could be drawn from their characters by a manner of calculus, which would be one of the most important means of aiding the human mind.",
]
assert len(bin_fr) == len(bin_en)

# ------------------------------------------------------------------ char
char_units = [
 {'label': 'Historia et commendatio linguae charactericae universalis (GP VII, 185)',
  'orig': "Factum est autem nescio quo fato, ut ego adhuc puer in has cogitationes inciderem, quae, ut solent primae inclinationes, postea semper altissime infixae menti haesere.",
  'txt': "It came to pass, by I know not what fate, that while still a boy I fell into these thoughts; and, as first inclinations are wont to do, they afterwards remained always most deeply fixed in my mind."},
 {'label': 'Historia et commendatio (GP VII, 185)',
  'orig': "Cui studio cum intentius incumberem, incidi necessario in hanc contemplationem admirandam, quod scilicet excogitari posset quoddam Alphabetum cogitationum humanarum, et quod literarum hujus Alphabeti combinatione et vocabulorum ex ipsis factorum analysi omnia et inveniri et dijudicari possent.",
  'txt': "As I applied myself more intently to this study, I fell of necessity upon this wonderful reflection: that a certain alphabet of human thoughts could be devised, and that by the combination of the letters of this alphabet, and by the analysis of the words formed from them, everything could be both discovered and judged."},
 {'label': 'De scientia universali seu calculo philosophico (GP VII, 200)',
  'orig': "Sed ut redeam ad expressionem cogitationum per characteres, ita sentio nunquam controversias finiri neque sectis silentium imponi posse, nisi a ratiocinationibus complicatis ad calculos simplices, a vocabulis vagae incertaeque significationis ad characteres determinatos revocemur.",
  'txt': "But to return to the expression of thoughts by characters: I hold that controversies can never be ended, nor silence imposed on the sects, unless we are recalled from complicated reasonings to simple calculi, and from words of vague and uncertain signification to determinate characters."},
 {'label': 'De scientia universali (GP VII, 200)',
  'orig': "Id scilicet efficiendum est, ut omnis paralogismus nihil aliud sit quam error calculi, et ut sophisma, in hoc novae scripturae genere expressum, revera nihil aliud sit quam soloecismus vel barbarismus, ex ipsis grammatices hujus philosophicae legibus facile revincendus.",
  'txt': "What must be brought about, namely, is that every paralogism should be nothing other than an error of calculation, and that a sophism, expressed in this new kind of writing, should really be nothing other than a solecism or barbarism, easily refuted from the very laws of this philosophical grammar."},
 {'label': 'De scientia universali (GP VII, 200) — with the marginal note of the manuscript',
  'orig': "Quo facto, quando orientur controversiae, non magis disputatione opus erit inter duos philosophos, quam inter duos Computistas. Sufficiet enim calamos in manus sumere sedereque ad abacos, et sibi mutuo (accito si placet amico) dicere: calculemus.",
  'txt': "When that is done, then, when controversies arise, there will be no more need of disputation between two philosophers than between two accountants. It will be enough for them to take their pens in their hands, sit down at their abacuses, and say to one another (calling in a friend, if they like): let us calculate.",
  'note': "In the margin of this manuscript Leibniz noted: “Cum DEUS calculat et cogitationem exercet, fit mundus” — as God calculates and carries out his thought, the world comes to be."},
 {'label': 'Guilielmi Pacidii initia et specimina scientiae generalis (GP VII, 125)',
  'orig': "Modum ergo tradere aggredior, quo semper homines ratiocinationes suas in omni argumento ad calculi formam exhibere controversiasque omnes finire possunt, ut non jam clamoribus rem agere necesse sit, sed alter alteri dicere possit: calculemus.",
  'txt': "I therefore undertake to deliver a method by which men can always exhibit their reasonings, on any subject whatever, in the form of a calculus, and bring all controversies to an end; so that it will no longer be necessary to carry on the matter by shouting, but the one will be able to say to the other: let us calculate."},
]

# ------------------------------------------------------------------ comb
comb_units = [
 {'label': 'Title programme of the 1666 dissertation',
  'orig': "Dissertatio de arte combinatoria, in qua ex arithmeticae fundamentis complicationum ac transpositionum doctrina novis praeceptis exstruitur, et usus ambarum per universum scientiarum orbem ostenditur; nova etiam artis meditandi seu logicae inventionis semina sparguntur.",
  'txt': "A dissertation on the combinatorial art, in which, from the foundations of arithmetic, the doctrine of complications and transpositions is built up with new precepts, and the use of both is shown throughout the whole circle of the sciences; and in which, moreover, new seeds are sown of the art of meditating, that is, of a logic of invention."},
 {'label': 'The debt to Hobbes (GP IV, 64)',
  'orig': "Profundissimus principiorum in omnibus rebus scrutator Th. Hobbes merito posuit omne opus mentis nostrae esse computationem, sed hac vel summam addendo vel subtrahendo differentiam colligi (Elem. de Corp. P. I, c. 1, art. 2). Quemadmodum igitur duo sunt Algebraistarum et Analyticorum primaria signa + et −, ita duae quasi copulae est et non-est: illic componit mens, hic dividit.",
  'txt': "Thomas Hobbes, that most profound searcher of principles in all things, rightly laid down that every work of our mind is computation, and that by it we gather either a sum, by adding, or a difference, by subtracting (Elements of Philosophy, On Body, Part I, ch. 1, art. 2). As, therefore, the two primary signs of the algebraists and analysts are + and −, so there are as it were two copulas, 'is' and 'is-not': in the one case the mind compounds, in the other it divides."},
]

# ------------------------------------------------------------------ ship
sections = []
n = 0
def add(sid, titel, units):
    global n
    us = []
    for k, u in enumerate(units, 1):
        n += 1
        v = dict(u); v['n'] = n; v['k'] = k
        us.append(v)
    sections.append({'id': sid, 'titel': titel, 'units': us})

add('mon', 'La Monadologie / The Monadology (1714)',
    [{'orig': x['orig'], 'txt': x['txt']} for x in units_mon])
add('bin', "Explication de l'arithmétique binaire (1703)",
    [{'orig': f, 'txt': e} for f, e in zip(bin_fr, bin_en)])
add('char', 'The characteristic and the calculus of reason — fragments (Gerhardt VII)', char_units)
add('comb', 'De arte combinatoria (1666) — selections', comb_units)

out = {
 'id': 'leibniz',
 'autor': 'Gottfried Wilhelm Leibniz',
 'titel': 'Anthology: Monadology · binary arithmetic · characteristica · ars combinatoria',
 'jahr': 1714,
 'lang': 'fr/la',
 'zitierweise': 'Mon. §17 / Arith. bin. [n] / GP VII [k] / De arte comb. [k]',
 'quelle': ("Monadology: French text of 1714 after the Project Gutenberg transcription #17641 "
            "(Piat's 1909 print; his apparatus omitted), English by Robert Latta (1898, public "
            "domain), from the Wikisource transcription of his translation, without his notes. "
            "Explication de l'arithmétique binaire: French text after Gerhardt, Mathematische "
            "Schriften VII (1863), pp. 223–227, via the French Wikisource transcription. "
            "Fragments: Latin text after Gerhardt, Die philosophischen Schriften von G. W. "
            "Leibniz, vol. VII (1890) and vol. IV (1880), from the Internet Archive scans, "
            "OCR emended by hand. All sources public domain."),
 'hinweis': ("The Monadology keeps Leibniz's own section numbers (§1–§90); Latta's bracketed "
             "glosses of the French terms are his. All other English in this module is an "
             "unofficial working translation made for this site — cite the French or Latin. "
             "The tables and worked examples of the binary-arithmetic paper are replaced by "
             "'[table omitted]' markers; consult the printed original."),
 'sections': sections,
}
json.dump(out, io.open('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/leibniz_anthology.json', 'w', encoding='utf-8'), ensure_ascii=False)
import os
print('units:', n, 'size:', os.path.getsize('C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo/data/leibniz_anthology.json'))
