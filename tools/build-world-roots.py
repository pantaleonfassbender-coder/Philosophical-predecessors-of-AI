# -*- coding: utf-8 -*-
"""Build the four 'world roots' modules (September 2026):

  data/ibnkhaldun_zairja.json   - Ibn Khaldun on the za'irja (Muqaddima), logic line
  data/liezi_yanshi.json        - Liezi, the automaton of Yan Shi, narrative line
  data/khwarizmi_algebra.json   - al-Khwarizmi, Algebra, author's preface (Rosen 1831)
  data/yijing_binary.json       - Yijing, Xici: the binary generation of the trigrams

Originals are cut, by exact string markers, from live transcriptions of the
public-domain texts (Arabic Wikisource pageids 3950/1904; Chinese Wikisource);
running this script therefore requires network access. English translations,
Giles 1912 (PD) and Legge 1882 (PD) excerpts, and Rosen 1831 (PD) excerpts are
embedded below. Working translations are made directly from the originals;
Rosenthal's Muqaddima (1958) and all other copyrighted translations were not
consulted. Editorial omissions are marked in place.
"""
import io, json, re, urllib.request

def fetch_ws(host, pageid=None, page=None, prop="wikitext"):
    if pageid:
        url = f"https://{host}/w/api.php?action=parse&pageid={pageid}&prop={prop}&format=json"
    else:
        from urllib.parse import quote
        url = f"https://{host}/w/api.php?action=parse&page={quote(page)}&prop={prop}&format=json"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Calculemus-corpus-builder/1.0 (https://github.com/pantaleonfassbender-coder/Philosophical-predecessors-of-AI)"})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    t = d["parse"][prop]["*"]
    if prop != "wikitext":
        t = re.sub(r"<[^>]+>", "", t)
    return t

def cut(text, start, end):
    i = text.find(start)
    assert i >= 0, f"start marker not found: {start[:40]!r}"
    j = text.find(end, i)
    assert j >= 0, f"end marker not found: {end[:40]!r}"
    seg = text[i:j + len(end)]
    seg = re.sub(r"<ref>.*?</ref>", "", seg, flags=re.S)   # strip edition footnotes
    seg = re.sub(r"\s+", " ", seg).strip()
    return seg

def write(data, name):
    n = sum(len(s["units"]) for s in data["sections"])
    io.open(f"data/{name}.json", "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False))
    print(f"{name}: {n} units, {len(data['sections'])} sections")

# ================================================= IBN KHALDUN - THE ZA'IRJA
ar_pref = fetch_ws("ar.wikisource.org", pageid=3950)
ar_op = fetch_ws("ar.wikisource.org", pageid=1904)

ZP = []  # (start, end, english, note)
ZP.append(("ومن هذه القوانين الصّناعيّة", "وكشف غامضه.",
"Among these technical procedures for the extraction of hidden things — as they claim — is the zāʾirja, the one called “zāʾirja of the world”, ascribed to Abū l-ʿAbbās Sīdī Aḥmad as-Sabtī, one of the eminent Sufis of the Maghrib, who lived at the end of the sixth [twelfth] century in Marrakesh, in the days of Abū Yaʿqūb al-Manṣūr of the Almohad kings. It is a craft strange in its working. Many persons of distinction are eager to gain the hidden from it by its well-known, riddling operation, and are spurred thereby to solve its cipher and uncover its obscurity.",
"The device Ibn Khaldūn describes belongs to the same western-Mediterranean world, and the same generation-by-letters, as Llull's Ars — compare, in this corpus, the rotating figures of the Ars brevis and the letter wheel of Sefer Yetzirah 2:4–5."))
ZP.append(("وصورتها الّتي يقع العمل", "العامرة من الخالية",
"The form in which they work it is a great circle. Within it are concentric circles for the spheres, the elements, the things that come to be, the spiritual beings, and the other kinds of existents and sciences. Every circle is divided into the divisions of its sphere — the signs of the zodiac, or the elements, or others — and the lines of each division pass to the centre; they call them the chords. On every chord stand letters in sequence. Some are in the ciphers of the zimām, the number-signs used by the officials of the bureaus and the accountants of the Maghrib in this age; some in the ciphers of the ghubār [the “dust” numerals], familiar inside the zāʾirja. Between the circles stand the names of the sciences and the stations of being. And upon the circles stands a table of many cells intersecting in length and breadth: fifty-five cells in breadth and one hundred and thirty-one in length. Some of its sides have their cells filled, now with numbers and now with letters; some have their cells empty. The rule of those numbers in their positions is not known, nor the division that set apart the filled cells from the empty.",
"A generative apparatus described component by component: data circles, address lines (“chords”), two numeral systems, and a 55 × 131 table whose filling rule is hidden — an opaque model, operated without being understood."))
ZP.append(("وحافات الزّايرجة أبيات", "في هذه الزّايرجة وغيرها",
"Around the edges of the zāʾirja are verses in the metre aṭ-ṭawīl, rhyming on lām, containing the manner of drawing the sought from it — though they are of the nature of riddles, wanting clarity and plainness. On one side of the zāʾirja stands a verse ascribed to one of the great masters of foreknowledge of the Maghrib, Mālik b. Wuhayb, a scholar of Seville of the Almoravid age; and this is the verse they pass from hand to hand for the operation, to extract the answer from the question in this zāʾirja and in others.",
"The operating verse is the template of every answer: whatever comes out will be cast on its metre and rhyme — a constrained decoder, in the vocabulary of a later century."))
ZP.append(("فإذا أرادوا استخراج الجواب", "بهذه الزّايرجة",
"When they wish to extract the answer to some question, they write the question down and break it into its letters. They take the ascendant of that hour among the signs and their degrees, go to the chord of the zāʾirja that bounds the ascendant sign, from its beginning through the centre to the circumference opposite the ascendant, and take all the letters written upon it from first to last, and the numbers drawn between them; these they turn into letters by the reckoning of the jummal [letter-values], transposing, as the canon of their operation requires, units into tens and tens into hundreds and conversely, and set them with the letters of the question. Then they add everything on the chord that bounds the third sign from the ascendant, from its beginning to the centre only, doing with its numbers as with the first. Then they break into letters the verse that is the foundation and canon of the operation — the verse of Mālik b. Wuhayb given above — and set it apart. Then they multiply the number of the ascendant degree into the base of the sign (the base being with them the sign's distance from the last of the ranks, the reverse of the practice of the arithmeticians), and again into a further number they call the greatest base and the fundamental cycle, and with what has gathered they enter the cells of the table according to known canons, recorded operations and counted cycles, extracting some letters and dropping others, matching what they hold against the letters of the verse, transferring what is to be transferred to the letters of the question and its companions, casting the letters out by known numbers they call the cycles, and bringing out, at each cycle, the letter at which the cycle ends — until at the last there come out disjoined letters, which, joined in sequence, become words composed in a single verse: on the metre of the verse against which the work is matched, and on its rhyme — the verse of Mālik b. Wuhayb — as we shall relate in the chapter on the sciences, where the manner of working this zāʾirja is set out.",
"End-to-end: the question's own letters, mixed with the chord alphabet, cycled through the table, matched against the template verse — and the answer emerges as well-formed verse."))
ZP.append(("وقد رأينا كثيرا من الخواصّ يتهافتون", "غير مستنكر",
"We have seen many persons of distinction fling themselves upon extracting the hidden from it by these operations. They suppose that the conformity between answer and question — their agreement as discourse — is a proof of conformity with reality. That is not correct; for it has already passed before you that the hidden cannot be attained by any technical procedure whatever. The conformity in it between question and answer is in respect of intelligibility and agreement in the discourse: that the answer come out straight, or conforming to the question. That this should happen in this craft — through the breaking-up of the letters gathered from question and chords, the entering of the table with the numbers gathered from the multiplications, the extraction of some letters and the discarding of others, the repetition through the counted cycles, and the matching of it all, in sequence, against the letters of the verse — is nothing to be denied.",
"The distinction on which the whole analysis rests, made in 1377: an answer's being well-formed and question-conforming is a fact about discourse, not about the world. The debate over generated text still needs exactly this sentence."))
ZP.append(("وقد يقع الاطّلاع من بعض الأذكياء", "غير مرّة",
"Some keen minds may indeed come to see the correspondence (tanāsub) between these things, and so attain knowledge of the unknown. For the correspondence between things is the cause of obtaining the unknown from the known that is present to the soul, and a road to such attainment — above all for people of trained discipline, for discipline gives the mind strength in inference and increase in thought; the explanation of this has been given more than once.",
None))
ZP.append(("وكثير من النّاس تضيق مداركهم", "ذكاء وحدس",
"Many people, whose grasp is too narrow to credit this operation and its reaching of the sought, deny its soundness and suppose it a play of imaginings and delusions — as if the operator merely planted the letters of a verse of his own composing among the letters of question and chords, performed those manipulations without rule or proportion, and then produced the verse, pretending that the work had followed a governed procedure. This supposition is a corrupt fancy, forced on its holders by their falling short of the correspondence between things and of the disparity of perceptions and intellects: whoever lacks the capacity for a perception denies it. To refute them it suffices to witness the craft at work: it proceeds, beyond doubt for anyone of intelligence and acumen who engages it, by a uniform operation and a sound canon.",
"Neither oracle nor fraud: Ibn Khaldūn insists the procedure is real, rule-governed, and reproducible — and still no road to truth. There follows in the text a worked arithmetical puzzle, omitted here, by which he shows how a hidden proportion makes an unknown seem like foreknowledge."))
ZP.append(("والجواب الّذي يخرج منها فالسّرّ في خروجه منظوما", "في موضعه",
"As for the answer that comes out of it: the secret of its coming out in verse is, as it appears to me, only the matching against the letters of that verse — which is why the composition falls on its metre and its rhyme. And there is a proof: we have found other operations of theirs of this kind in which the matching with the verse was dropped — and the answer came out unversified, as you will see where this is spoken of in its place.",
"An ablation, seven centuries early: remove the template, and the output loses its form — therefore the form came from the template, not from the unseen."))
ZP.append(("وإذا تبيّن لك ذلك فالأعمال الواقعة في الزّايرجة", "لا تَعْلَمُونَ 2: 216.",
"When this has become clear to you: the operations of the zāʾirja are, all of them, only the extraction of the answer from the words of the question. For it is, as you have seen, the derivation of letters in one arrangement out of those very letters in another arrangement; and its secret is only a correspondence between the two, which one person sees and another does not. Whoever knows that correspondence finds it easy to extract the answer by those canons. The answer may, in another regard — by the purport of its words and their construction — indicate one of the two sides of the question, denial or affirmation; but that belongs to a different station: to the conformity of speech with what is outside. And to the knowledge of that there is no road from these operations. Human beings are veiled from it; God has kept its knowledge to Himself — “and God knows, and you know not” (Qurʾān 2:216).",
"The verdict: the answer is drawn from the question's own words in another ordering. Coherence is craft; truth about the world is beyond every such procedure."))

ZO = []
ZO.append(("كيفية العمل في استخراج أجوبة المسائل", "من بيت القصيد.",
"How to work the extraction of answers to questions from the zāʾirja of the world — by God's power — as transmitted from those we met who practise it. The question has three hundred and sixty answers, the number of the degrees; and the answers to one and the same question, under a particular ascendant, differ with the differing questions joined to the letters of the chords, and correspond, in the working, to the extraction of the letters from the model verse.",
"One question, three hundred and sixty possible answers, selected by the hour's ascendant: the operating manual begins by declaring the procedure's built-in variability."))
ZO.append(("فأول ذلك نفرض سؤالا عن الزايرجة", "أثناء حروف الأوتار ؟",
"First of all, we posit a question about the zāʾirja itself: is it an ancient science, or a recent invention? — with the ascendant in the first degree of Sagittarius, amid the letters of the chords.",
"The first question the operators put to the machine is about the machine. The transmitted answer, Ibn Khaldūn reports, came out in verse — attributing the science to Idrīs, that is: the device vouched for its own antiquity."))

zsec_pref = {"id": "pref", "titel": "Sixth Prefatory Discussion — the zāʾirja described and judged", "units": []}
n = 0
for (a, b, en, note) in ZP:
    n += 1
    u = {"n": n, "k": len(zsec_pref["units"]) + 1, "orig": cut(ar_pref, a, b), "txt": en}
    if note: u["note"] = note
    zsec_pref["units"].append(u)
zsec_op = {"id": "op", "titel": "Book VI — from the operating manual", "units": []}
for (a, b, en, note) in ZO:
    n += 1
    u = {"n": n, "k": len(zsec_op["units"]) + 1, "orig": cut(ar_op, a, b), "txt": en}
    if note: u["note"] = note
    zsec_op["units"].append(u)

write({
 "id": "zairja", "autor": "Ibn Khaldūn", "titel": "The zāʾirja: letter-machine and its critique (Muqaddima, 1377)",
 "jahr": 1377, "lang": "ar", "zitierweise": "Muq. I.6 [k] · Muq. VI [k]",
 "quelle": "Muqaddima (1377): the sixth prefatory discussion of Book One, and the operating manual appended to the sciences chapter of Book VI. Arabic text after the Arabic Wikisource transcription of the public-domain text. The public-domain French translation by de Slane (Prolégomènes, 1862–68) and Quatremère's Arabic edition (1858) document the same passages; Rosenthal's English translation (1958) remains in copyright and was not consulted.",
 "hinweis": "Selections chosen for the argument. The zāʾirja — the letter-combinatorial answering device of the medieval Maghrib — is described, defended against the charge of fraud, and epistemically dismantled by Ibn Khaldūn in one movement: the procedure is real and rule-governed; its answers are well-formed and question-conforming; and none of this reaches truth about the world. The English is this site's unofficial working translation, made directly from the Arabic — cite the original. Editorial omissions are marked in the notes.",
 "sections": [zsec_pref, zsec_op]}, "ibnkhaldun_zairja")

# ======================================================= LIEZI - YAN SHI
zh = fetch_ws("zh.wikisource.org", page="列子/湯問篇", prop="text")
LZ = [
 ("周穆王西巡狩", "信人也。",
"King Mu of Chou made a tour of inspection in the west. He crossed the K‘un-lun range, but turned back before he reached the Yen mountains. On his return journey, before arriving in China, a certain artificer was presented to him, by name Yen Shih. King Mu received him in audience, and asked what he could do. “I will do anything,” replied Yen Shih, “that your Majesty may please to command. But there is a piece of work, already finished, that I should like to submit first to your Majesty's inspection.” “Bring it with you to-morrow,” said the King, “and we will look at it together.” So Yen Shih called again the next day, and was duly admitted to the royal presence. “Who is that man accompanying you?” asked the King. “That, Sire, is my own handiwork. He can sing and he can act.” The King stared at the figure in astonishment. It walked with rapid strides, moving its head up and down, so that any one would have taken it for a live human being.",
"The oldest complete automaton narrative in world literature — and it opens, like every later one, with a demonstration before power."),
 ("巧夫顉其頤", "惟意所適。",
"The artificer touched its chin, and it began singing, perfectly in tune. He touched its hand, and it started posturing, keeping perfect time. It went through any number of movements suggested by its owner's fancy.",
None),
 ("王以爲實人也", "合會復如初見。",
"The King, looking on with his favourite concubine and the other inmates of his harem, could hardly persuade himself that it was not real. As the performance was drawing to an end, the automaton winked its eye and made sundry advances to the ladies in attendance on the King. This, however, threw the King into a passion, and he would have put Yen Shih to death on the spot had not the latter, in mortal terror, instantly pulled the automaton to pieces to let him see what it really was. And lo! it turned out to be merely a conglomeration of leather, wood, glue and paint, variously coloured white, black, red and blue. Examining it closely, the King found all the internal organs complete — liver, gall, heart, lungs, spleen, kidneys, stomach and intestines — and, over these again, muscles and bones and limbs with their joints, skin and teeth and hair, all of them artificial. Not a part but was fashioned with the utmost nicety and skill; and when it was put together again, the figure presented the same appearance as when first brought in.",
"The inspection scene: taken apart, the marvel is leather, wood, glue and paint — the walk into Leibniz's mill, two millennia before the Monadology, §17."),
 ("王試廢其心", "詔貳車載之以歸。",
"The King tried the effect of taking away the heart, and found that the mouth could no longer speak; he took away the liver, and the eyes could no longer see; he took away the kidneys, and the legs lost their power of locomotion. The King was delighted. Drawing a deep breath, he exclaimed: “Can it be that human skill is on a par with that of the great Author of Nature?” And forthwith he gave an order for two extra chariots, in which he took home with him the artificer and his handiwork.",
"Remove the heart, and speech fails: the organ-by-organ test of where the capacities sit. Compare Rava's created man, unmasked by silence (San. 65b), and Descartes's language test (Disc. V)."),
 ("夫班輸之雲梯", "而時執規矩。",
"Now, Pan Shu, with his cloud-scaling ladder, and Mo Ti, with his flying kite, thought that they had reached the limits of human achievement. But when Yen Shih's wonderful piece of work had been brought to their knowledge, the two philosophers never again ventured to boast of their accomplishments, and ceased to busy themselves so frequently with the square and compasses.",
"The engineers' reaction: before the made man, the ladder and the kite fall silent."),
]
units = []
for i, (a, b, en, note) in enumerate(LZ, 1):
    u = {"n": i, "k": i, "orig": cut(zh, a, b), "txt": en}
    if note: u["note"] = note
    units.append(u)
write({
 "id": "liezi", "autor": "Liezi", "titel": "The automaton of Yan Shi (Liezi V, Tang wen)",
 "jahr": "c. 4th c. BC – 4th c. AD", "lang": "zh", "zitierweise": "Liezi V [k]",
 "quelle": "Liezi, Book V (湯問, “The Questions of Tang”), Chinese text after the Chinese Wikisource transcription of the received text. English: Lionel Giles, Taoist Teachings from the Book of Lieh Tzŭ (Wisdom of the East, 1912), public domain; Giles's continuous rendering is divided here to match the Chinese paragraphs.",
 "hinweis": "The Liezi is a layered text: its materials reach back to the fourth century BC, its received form to the fourth century AD. The paragraph numbers are editorial. Giles's spelling (Chou, Yen Shih) is his own romanization; the artificer is Yan Shi, the king Mu of Zhou.",
 "sections": [{"id": "tw", "titel": "Tang wen — the artificer Yan Shi", "units": units}]}, "liezi_yanshi")

# ================================================ AL-KHWARIZMI - THE ALGEBRA
KW = [
 ("The learned in times which have passed away, and among nations which have ceased to exist, were constantly employed in writing books on the several departments of science and on the various branches of knowledge, bearing in mind those that were to come after them, and hoping for a reward proportionate to their ability, and trusting that their endeavours would meet with acknowledgment, attention, and remembrance — content as they were even with a small degree of praise; small, if compared with the pains which they had undergone, and the difficulties which they had encountered in revealing the secrets and obscurities of science. Some applied themselves to obtain information which was not known before them, and left it to posterity; others commented upon the difficulties in the works left by their predecessors, and defined the best method of study, or rendered the access to science easier or placed it more within reach; others again discovered mistakes in preceding works, and arranged that which was confused, or adjusted what was irregular, and corrected the faults of their fellow-labourers, without arrogance towards them, or taking pride in what they did themselves.",
"Knowledge as cumulative, corrigible, collaborative labour across nations that have ceased to exist — the ethos of science, stated in Baghdad around 820 as the preface to a book of procedures."),
 ("That fondness for science, by which God has distinguished the Imam al Mamun, the Commander of the Faithful — besides the caliphat which He has vouchsafed unto him by lawful succession, in the robe of which He has invested him, and with the honours of which He has adorned him — that affability and condescension which he shows to the learned, that promptitude with which he protects and supports them in the elucidation of obscurities and in the removal of difficulties, has encouraged me to compose a short work on Calculating by (the rules of) Completion and Reduction, confining it to what is easiest and most useful in arithmetic, such as men constantly require in cases of inheritance, legacies, partition, law-suits, and trade, and in all their dealings with one another, or where the measuring of lands, the digging of canals, geometrical computation, and other objects of various sorts and kinds are concerned.",
"“Completion and Reduction” renders al-jabr wa-l-muqābala: from al-jabr came the word algebra, and from the author's name — al-Khwārizmī, Latinized Algoritmi — the word algorithm. The rule-following procedure bears his name."),
 ("When I considered what people generally want in calculating, I found that it always is a number. I also observed that every number is composed of units, and that any number may be divided into units. Moreover, I found that every number, which may be expressed from one to ten, surpasses the preceding by one unit: afterwards the ten is doubled or tripled, just as before the units were: thus arise twenty, thirty, &c., until a hundred; then the hundred is doubled and tripled in the same manner as the units and the tens, up to a thousand; then the thousand can be thus repeated at any complex number; and so forth to the utmost limit of numeration.",
"The treatise opens by decomposing all calculation into number, and number into units — reduction to elementary operations, the gesture Hobbes will repeat for reason itself (“nothing but Reckoning”)."),
]
units = [{"n": i, "k": i, "txt": t, "note": note} for i, (t, note) in enumerate(KW, 1)]
write({
 "id": "khwarizmi", "autor": "al-Khwārizmī", "titel": "The Algebra (c. 820) — the author's preface and opening",
 "jahr": "c. 820", "lang": "ar", "zitierweise": "Alg. [k]",
 "quelle": "Kitāb al-jabr wa-l-muqābala (Baghdad, c. 820). English: Frederic Rosen, The Algebra of Mohammed ben Musa (London: Oriental Translation Fund, 1831), public domain; OCR of the Internet Archive scan, emended.",
 "hinweis": "A root module: the author's preface and the treatise's opening, in Rosen's public-domain translation of 1831. The Arabic text is printed in Rosen's edition (its Arabic section) and is not yet carried here; a future revision may add it. The paragraph numbers are editorial.",
 "sections": [{"id": "praef", "titel": "The author's preface and the opening of the treatise", "units": units}]}, "khwarizmi_algebra")

# ==================================================== YIJING - THE BINARY
x1 = fetch_ws("zh.wikisource.org", page="易傳/繫辭上", prop="text")
x2 = fetch_ws("zh.wikisource.org", page="易傳/繫辭下", prop="text")
YJ = [
 (x1, "是故易有太極", "吉凶生大業。",
"Therefore in (the system of) the Yî there is the Grand Terminus, which produced the two elementary Forms. Those two Forms produced the Four emblematic Symbols, which again produced the eight Trigrams. The eight trigrams served to determine the good and evil (issues of events), and from this determination was produced the (successful prosecution of the) great business (of life).",
"One, two, four, eight: successive doubling of paired forms. Leibniz, shown the hexagrams in Bouvet's letters from Beijing, read exactly this as his binary arithmetic anticipated — compare, in this corpus, the Explication de l'arithmétique binaire of 1703 and its “figures of Fohy”."),
 (x2, "古者包犧氏之王天下也", "以類萬物之情。",
"Anciently, when the rule of all under heaven was in the hands of Pâo-hsî, looking up, he contemplated the brilliant forms exhibited in the sky; and looking down, he surveyed the patterns shown on the earth. He marked the ornamental appearances on birds and beasts, and the (different) suitabilities of the soil. Near at hand, in his own person, he found things for consideration, and the same at a distance, in things in general. On this he devised the eight lineal figures of three lines each, to exhibit fully the spirit-like and intelligent operations (in nature), and to classify the qualities of the myriads of things.",
"Pâo-hsî is Fuxi (Fohy in Leibniz's spelling): the culture-founder who derives a complete symbolic system from the observation of patterns — the Yijing's own account of where notation comes from."),
]
units = []
for i, (src, a, b, en, note) in enumerate(YJ, 1):
    u = {"n": i, "k": i, "orig": cut(src, a, b), "txt": en, "note": note}
    units.append(u)
write({
 "id": "yijing", "autor": "Yijing (Xici zhuan)", "titel": "The trigrams and the binary: two passages of the Great Commentary",
 "jahr": "c. 3rd c. BC", "lang": "zh", "zitierweise": "Xici I/II [k]",
 "quelle": "Xici zhuan (the “Great Commentary” appended to the Zhouyi), Chinese text after the Chinese Wikisource transcription. English: James Legge, The Yî King (Sacred Books of the East XVI, 1882), public domain; OCR of the scan, emended.",
 "hinweis": "A bridge module, not an edition of the Yijing: the two passages through which the hexagrams entered the corpus's own history — Leibniz's binary arithmetic (already in the Leibniz module) was, by its author's account, a rediscovery of “Fohy's figures”. Legge's romanization (Yî, Pâo-hsî) is preserved.",
 "sections": [{"id": "xici", "titel": "Xici — the generation of the figures", "units": units}]}, "yijing_binary")
