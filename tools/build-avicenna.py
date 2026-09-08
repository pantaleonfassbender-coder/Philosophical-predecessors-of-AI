# -*- coding: utf-8 -*-
# Build data/avicenna_isharat.json — Avicenna, the flying man:
# al-Ishārāt wa-l-tanbīhāt, the opening of the third namaṭ (on the soul).
#
# Arabic text transcribed by hand from the page images of Jacques Forget's
# edition (Kitāb al-ishārāt wa-l-tanbīhāt / "Le livre des théorèmes et des
# avertissements", Leiden: Brill, 1892), pp. 119–120 — Internet Archive scan
# kitbalishrtwaalt00avic (the 1892 typesetting is clean; its critical
# apparatus letters are omitted, its orthography kept). The genre markers of
# the print (tanbīh) are carried as unit labels. English: working translation
# made for this site (Goichon's French of 1951 and the modern English
# translations were not consulted). The two parallel versions in the De anima
# of the Shifāʾ (I.1 and V.7) are documented on the method page, not carried:
# their standard edition (Rahman 1959) remains in copyright and no
# public-domain printing of the Arabic was found.
import io, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

U = [
 {
  'label': 'Tanbīh',
  'orig': "ارجع الى نفسك وتأمّل هل اذا كنت صحيحا بل وعلى بعض احوالك غيرها بحيث تفطن للشيء فطنة صحيحة هل تغفل عن وجود ذاتك ولا تثبت نفسك، ما عندى انّ هذا يكون للمستبصر حتّى انّ النائم في نومه والسكران في سكره لا تعزب ذاته عن ذاته وان لم يثبت تمثّله لذاته في ذكره. ولو توهّمت ذاتك قد خُلقت اوّل خلقها صحيحة العقل والهيئة وفُرض انّها على جملة من الوضع والهيئة بحيث لا تُبصر اجزاؤها ولا تتلامس اعضاؤها بل هي منفرجة ومعلّقة لحظة مّا في هوآء طلق، وجدتها قد غفلت عن كلّ شيء الّا عن ثبوت انّيّتها.",
  'txt': "Return to yourself and consider: when you are sound — indeed even in certain other of your states — such that you discern a thing with sound discernment, are you ever unaware of the existence of your self, failing to affirm it? To my mind this does not happen to anyone of insight: even the sleeper in his sleep and the drunkard in his drunkenness do not have their self slip away from their self, though its representing of itself does not stand fixed in memory. And if you imagine your self created all at once, at the first of its creation sound in intellect and constitution, and suppose it so placed and disposed that its parts are not seen and its limbs do not touch one another but are spread apart, suspended for a moment in open air — you would find it unaware of everything except the affirming of its own existence.",
 },
 {
  'label': 'Tanbīh',
  'orig': "بماذا تُدرك حينئذ وقبله وبعده ذاتك وما المدرِك من ذاتك، أترى المدرِك احد مشاعرك مشاهدة ام عقلك وقوّة غير مشاعرك وما يناسبها، فان كان عقلك وقوّة غير مشاعرك بها تدرك أفبوسط تدرك ام بغير وسط، ما اظنّك تفتقر في ذلك حينئذ الى وسط فانّه لا وسط، فبقى ان تدرك ذاتك من غير افتقار الى قوّة اخرى والى وسط، فبقى ان يكون بمشاعرك او بباطنك بلا وسط، ثمّ انظر.",
  'txt': "By what, then — at that moment, before it, and after it — do you apprehend your self, and what is the apprehender in you? Do you think the apprehender is one of your senses, in direct witness, or your intellect — a power other than your senses and what belongs with them? And if it is your intellect, a power other than your senses, by which you apprehend: do you apprehend through an intermediary, or without one? I do not think you need any intermediary there — there is none. It remains, then, that you apprehend your self without need of a further power and without an intermediary; it remains that it is by your senses or by your inward self, without intermediary. Now consider.",
 },
 {
  'label': 'Tanbīh',
  'orig': "اتحصّل انّ المدرَك منك اهو ما يدركه بصرك من اهابك، لا فانّك ان انسلخت عنه وتبدّل عليك كنت انت انت، او هو ما تدركه بلمسك ايضا وليس ايضا الّا من ظواهر اعضائك، لا فانّ حالها ما سلف ومع ذلك فقد كنّا في الوجه الاوّل من الفرض اغفلنا الحواسّ عن افعالها فبيّن انّه ليس مدرَكك حينئذ عضوا من اعضائك كقلب او دماغ وكيف ويخفى عليك وجودهما الّا بالتشريح، ولا مدرَكك جملة من حيث هي جملة وذلك ظاهر لك ممّا تمتحنه من نفسك وممّا نبّهت عليه، فمدرَكك شيء آخر غير هذه الاشيآء التي قد لا تدركها وانت مدرك لذاتك والتي لا تجدها ضرورية في ان تكون انت، فمدرَكك ليس من عداد ما تدركه حسًّا بوجه من الوجوه ولا ممّا يشبه الحسّ ممّا سنذكره.",
  'txt': "Have you settled what it is of you that is apprehended? Is it what your sight apprehends of your skin? No — for were you stripped of it, and were it exchanged upon you, you would still be you. Or is it what you apprehend by your touch? That too is only the outward of your limbs — no, for their case is as before; and besides, in the first supposition we made the senses leave off their acts. So it is plain that what you apprehend then is not an organ among your organs, such as a heart or a brain — how should it be, when their very existence is hidden from you except by dissection? — nor is it the aggregate as aggregate: that is plain to you from what you may test in yourself and from what you have been reminded of. What you apprehend is, then, something other than these things — things you may fail to apprehend while you are apprehending your self, and which you do not find necessary for being you. So what is apprehended of you is not among what is apprehended by sense in any way, nor among what resembles sense, of which we shall speak.",
 },
 {
  'label': 'Tanbīh',
  'orig': "ولعلّك تقول انّما أُثبت ذاتي بوسط من فعلى، فيجب اذن ان يكون لك فعل تثبته في الفرض المذكور او حركة او غير ذلك ففي اعتبارنا الفرض المذكور جعلناك بمعزل من ذلك، وامّا بحسب الامر الاعمّ فانّ فعلك ان اثبتّه مطلقا فعلا فيجب ان تثبت منه فاعلا مطلقا لا خاصّا هو ذاتك بعينها، وان اثبتّه فعلا لك فلم تثبت به ذاتك بل ذاتك جزء من مفهوم فعلك من حيث هو فعلك فهو مثبت في الفهم قبله ولا اقلّ من ان يكون معه لا به، فذاتك مثبتة لا به.",
  'txt': "Perhaps you will say: I affirm my self only through an intermediary — through my act. Then you would need, in the supposition described, an act to affirm, or a motion, or something else; but in framing that supposition we set you apart from all of that. And taking the matter at its most general: if you affirm your act absolutely, as an act, then you must affirm from it an agent absolutely — not a particular one that is your very self. And if you affirm it as your act, then you have not affirmed your self through it: your self is part of the concept of your act insofar as it is your act, and so it stands affirmed in the understanding before it — at the least along with it, not through it. Your self, then, is affirmed — and not through your act.",
 },
]

out = {
 'id': 'avicenna',
 'autor': 'Avicenna (Ibn Sīnā)',
 'titel': 'The flying man: al-Ishārāt wa-l-tanbīhāt, Namaṭ III, opening (c. 1030)',
 'jahr': 1030,
 'lang': 'ar',
 'zitierweise': 'Ish. III [k]',
 'quelle': ("al-Ishārāt wa-l-tanbīhāt, the opening of the third namaṭ ('On the terrestrial "
            "and the celestial soul'). Arabic after Jacques Forget's edition (Leiden: Brill, "
            "1892), pp. 119–120, transcribed by hand from the page images of the Internet "
            "Archive scan; Forget's apparatus letters are omitted and the print's orthography "
            "kept. Public domain (composed c. 1030; edition 1892)."),
 'hinweis': ("The four opening reminders of the third namaṭ, complete. Paragraph numbers are "
             "editorial; the print's genre marker (tanbīh) is carried as a label. The English "
             "is this site's unofficial working translation, made directly from the Arabic — "
             "Goichon's French translation (1951) and the modern English translations were "
             "not consulted; cite the original. The two parallel versions of the argument in "
             "the De anima of the Shifāʾ (I.1 and V.7) are documented on the method page but "
             "not carried: their standard edition (Rahman 1959) remains in copyright, and no "
             "public-domain printing of that Arabic text was found."),
 'sections': [{
   'id': 'nm3',
   'titel': 'Namaṭ III, opening — the flying man and the reminders that follow',
   'units': [{'n': i + 1, 'k': i + 1, **u} for i, u in enumerate(U)],
 }],
}

path = os.path.join(REPO, 'data', 'avicenna_isharat.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '—', len(U), 'units')
