# -*- coding: utf-8 -*-
# Ship files for stage 5: Pascal fragments, Jevons 1870 selections, Peirce 1887.
import io, json, re

REPO = 'C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo'
d = json.load(io.open('pj-draft.json', encoding='utf-8'))
P = d['peirce']; J = d['jevons']

# ---------------------------------------------------------------- Peirce
# reconstruct the print order: the OCR linearized page layout, interleaving
# footnotes and displayed formula blocks with the running text.
FO = '[formula display kept below]'
p5 = P[5]
head5 = p5[:p5.find(' : There are virtually no keys')]
head5 = head5.replace('Mr. Marquand s', "Mr. Marquand's")
tail5 = p5[p5.find('The face of the machine always shows'):]
keys = ('There are virtually no keys ex' + P[7][:1].replace('c', 'c', 1) if False else
        'There are virtually no keys ex' + P[7])
keys = keys.replace('ex' + 'cept', 'except')
peirce_units = [
 {'txt': P[0]},
 {'txt': P[1].replace('or D— CD', 'or D = CD').replace('or G— BC', 'or C = BC')
            .replace('explained. 1 The keys', 'explained. The keys')
            + ' [the machine’s display of the sixteen combinations is omitted]',
  'note': "Peirce's footnote: Phil. Trans. for 1870 — Jevons's memoir, shipped on this site."},
 {'txt': P[4]},
 {'txt': head5 + ' ' + keys,
  'note': "Peirce's footnote: “It would be equally true to say that the machine is based upon Mrs. Franklin's system.” — Christine Ladd-Franklin."},
 {'txt': tail5 + ' [figure omitted]'},
 {'txt': (P[6] + ' (A+B+C+D) (A+b+C+D) (A+b+C+d) (A+B+C+d) (A+B+c+D) (A+b+c+D) '
          '(a+B+c+D) (a+B+C+D) (a+B+C+d), which is the same as what is seen on the unshaded '
          'portions if we regard the small letters as affirmative and the capitals as negative, '
          'and interchange addition and multiplication, that is, as — ' + P[9].split(' Or, ')[0]
          + ' Or, looking at the unshaded portion, we may regard it as the negative of the '
          'above, or — ' + P[10].split(', or, what')[0] + ', or, what is the same thing, as — '
          + P[11])},
 {'txt': P[12].replace('"We see', 'We see')},
 {'txt': (P[8].split(' But in point of fact')[0] +
          ' But in point of fact neither of the machines really gives the conclusion of a pair '
          'of ' + P[13] + ' ' + P[14])},
 {'txt': P[15]},
 {'txt': P[16].replace('relations used; When', 'relations used. When')},
 {'txt': P[17]},
 {'txt': P[18]},
 {'txt': P[19]},
]

# ---------------------------------------------------------------- Jevons
def fix(k, t):
    reps = {
     1: [('apsOuds', 'ἀριθμός'), ('material sign Even', 'material sign. Even'), ('Ir is', 'It is')],
     3: [('cuiding', 'guiding'), ('elobes', 'globes'), ('mathematician,’', 'mathematician,')],
     5: [('tables;!', 'tables;'), ('aa machinery', 'machinery')],
     6: [('Ars instrumentalrs dirigens mentem nostram in cognitionem omnium wntelligrbilewm',
          'Ars instrumentalis dirigens mentem nostram in cognitionem omnium intelligibilium'),
         ('Nec manus nuda, nec Intellectus sibv permissus, muliwm valet ; Instrumentis et auailiis res perficitur ; quibus opus est, non minus ad intellectum, quam ad manum. Atque ut instrumenta manus motum aut cient, aut regunt; ita et Instrumenta mentis, Intellectur aut suggerunt aut cavent.',
          'Nec manus nuda, nec Intellectus sibi permissus, multum valet; Instrumentis et auxiliis res perficitur; quibus opus est, non minus ad intellectum, quam ad manum. Atque ut instrumenta manus motum aut cient, aut regunt; ita et instrumenta mentis, Intellectui aut suggerunt, aut cavent.'),
         ('need— Nec', 'need — Nec')],
     7: [('Jnstrwment', 'Instrument'), ('machine _ which', 'machine which'),
         ('inference ;*', 'inference;'), ('found.?', 'found.')],
     8: [('writers, The ancient', 'writers. The ancient')],
     9: [('(18477)', '(1847)'), ('work Of the Laws', 'work on the Laws'),
         ('generality :—Gwen certain', 'generality: — Given certain')],
     13: [('identical with rtself', 'identical with itself')],
     20: [('Abecedarvum', 'Abecedarium')],
     21: [('combinations..', 'combinations.')],
    }
    for a, b in reps.get(k, []):
        if a not in t: print(f'MISS jevons {k}: {a[:40]!r}')
        t = t.replace(a, b)
    return t

# art 5: excise the interleaved Napier footnote
t5 = J['5']
i = t5.find("principles of the ' Rabdologie")
j = t5.find('calculus of differences')
J['5'] = t5[:i] + 'principles of the ' + t5[j:]
# art 9: excise interleaved footnote remnant
t9 = J['9']
t9 = t9.replace(' the ing of terms; but it was merely of an illustrative character, and does not | seem to have been capable of performing any mechanical operations. logicians',
                ' the logicians')
t9 = t9.replace('any of the ing of terms; but it was merely of an illustrative character, and does not seem to have been capable of performing any mechanical operations. logicians',
                'any of the logicians')
J['9'] = t9
# art 10/11 split
t10 = J['10']
sp = t10.find(' 11, Having made')
art10 = t10[:sp]
art11 = t10[sp + 5:].replace('work on Pure Logic!', 'work on Pure Logic')\
    .replace('In a later work?', 'In a later work').replace('an areument', 'an argument')\
    .replace('may be.desired', 'may be desired')
# art 32 shortened
art32 = ("The Machine which has been actually finished is adapted to the solution of any "
         "problems not involving more than four distinct positive terms, indicated by A, B, C, D, "
         "with, of course, their corresponding negatives, a, b, c, d. The requisite combinations "
         "of the abecedarium are, therefore, sixteen in number (§ 20), and each combination is "
         "represented by a pair of square rods of baywood, united by a short piece of cord and "
         "slung over two round horizontal bars of wood, so as to balance each other and to slide "
         "freely and perpendicularly in wooden collars. [The detailed description of the "
         "mechanism, keyed to the plates of the memoir, is omitted; the plates are not "
         "reproduced.]")
# art 56: drop footnote remnant
t56 = J['56'].replace(', Deduction, the reader has to look elsewhere for processes which, according to Boole, must form the very basis of Deduction.', '.')
ORDER = [(1, J['1']), (2, J['2']), (3, J['3']), (4, J['4']), (5, J['5']), (6, J['6']),
         (7, J['7']), (8, J['8']), (9, J['9']), (10, art10), (11, art11), (12, J['12']),
         (13, J['13']), (17, J['17']), (20, J['20']), (21, J['21']), (31, J['31']),
         (32, art32), (55, J['55']), (56, t56)]
jevons_units = [{'art': k, 'txt': fix(k, t)} for k, t in ORDER]

# ---------------------------------------------------------------- Pascal
pas = json.load(io.open('pascal-draft.json', encoding='utf-8'))

# ------------------------------------------------------------------ ship
def ship(path, obj):
    json.dump(obj, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    import os; print(path.split('/')[-1], os.path.getsize(path))

n = 0
def units(lst, extra=None):
    global n
    out = []
    for k, u in enumerate(lst, 1):
        n += 1
        v = dict(u); v['n'] = n; v['k'] = k
        out.append(v)
    return out

n = 0
ship(f'{REPO}/data/pascal_pensees.json', {
 'id': 'pascal', 'autor': 'Blaise Pascal', 'titel': 'Pensées — five fragments on machine and thought',
 'jahr': 1670, 'lang': 'fr', 'zitierweise': 'Pens. 340 (Br.)',
 'quelle': ("Pensées (written before 1662, published 1670). French text after Léon Brunschvicg's "
            "edition, via the French Wikisource transcription; English by W. F. Trotter (1904, "
            "public domain), via the Project Gutenberg transcription #18269. Both public domain."),
 'hinweis': ("Five fragments selected for the argument of this site, cited by Brunschvicg's "
             "numbering, which both source editions share. Brunschvicg's apparatus is omitted."),
 'sections': [{'id': 'frag', 'titel': 'Fragments 252 · 339 · 340 · 346 · 347 (Brunschvicg)',
               'units': [dict(u, n=(i+1), k=(i+1), label=f'Brunschvicg {u["br"]}') for i, u in enumerate(pas)]}],
})
n = 0
ship(f'{REPO}/data/jevons_1870.json', {
 'id': 'jevons', 'autor': 'William Stanley Jevons',
 'titel': 'On the Mechanical Performance of Logical Inference (1870) — selections',
 'jahr': 1870, 'lang': 'en', 'zitierweise': 'MPL, art. 56',
 'quelle': ("Received by the Royal Society 16 October 1869, read 20 January 1870; Philosophical "
            "Transactions vol. 160 (1870), pp. 497–518. Text from the reprint in Pure Logic and "
            "Other Minor Works, ed. Robert Adamson and Harriet A. Jevons (London/New York: "
            "Macmillan, 1890), via the Internet Archive scan, OCR emended by hand. Public domain."),
 'hinweis': ("Jevons's own article numbers are kept and used for citation. Selected articles: 1–13 "
             "(the programme and its history, from the abacus through Pascal and Babbage to "
             "Boole), 17, 20–21 (the Abecedarium), 31–32 (the machine itself, abridged as marked), "
             "55–56 (Jevons's own assessment). The omitted articles carry the worked equations and "
             "the full mechanical description; the plates are not reproduced. Footnotes are "
             "omitted."),
 'sections': [{'id': 'mpl', 'titel': 'The memoir, in Jevons’s numbered articles (selection)',
               'units': [dict(u, n=(i+1), k=(i+1)) for i, u in enumerate(jevons_units)]}],
})
n = 0
ship(f'{REPO}/data/peirce_logical_machines.json', {
 'id': 'peirce', 'autor': 'Charles Sanders Peirce', 'titel': 'Logical Machines (1887)',
 'jahr': 1887, 'lang': 'en', 'zitierweise': 'LM [n]',
 'quelle': ("The American Journal of Psychology, vol. I, no. 1 (November 1887), pp. 165–170 — "
            "the original journal printing, digitized in JSTOR's Early Journal Content and "
            "mirrored at the Internet Archive. Public domain (the Collected Papers of 1931 ff. "
            "remain in copyright and are not used)."),
 'hinweis': ("Complete. The paragraph numbers are editorial. The article's two footnotes are "
             "kept as marked notes. The machine-face figure is omitted; Peirce's formula "
             "displays are kept inline, emended from the OCR. The print order of two passages, "
             "which the scan's page layout interleaved, has been restored."),
 'sections': [{'id': 'lm', 'titel': 'Logical Machines', 'units': [dict(u, n=(i+1), k=(i+1)) for i, u in enumerate(peirce_units)]}],
})
