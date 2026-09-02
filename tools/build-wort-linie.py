# Build the four modules of the fourth line, "The animated word":
#   data/golem_anthologie.json      - Tanach / Talmud / Sefer Yetzirah / Grimm 1808
#   data/goethe_zauberlehrling.json - Goethe, Der Zauberlehrling (first printing 1798)
#   data/automata_antike.json       - Homer, Iliad XVIII / Aristotle, Politics I 4
#   data/capek_rur.json             - Karel Capek, R.U.R. (1920), selections
#
# Sources:
#   Ps 139:16, Sanhedrin 38b + 65b (Vilna text), Sefer Yetzirah 1-2: Hebrew/Aramaic
#     via the Sefaria API text exports (the underlying texts are public domain);
#     English working translations made for this site, consulting no copyrighted
#     translation.
#   Grimm 1808: Zeitung fuer Einsiedler No. 7 (23 April 1808), col. 56, signed
#     "Mitgetheilt von Jakob Grimm in Cassel" - transcribed from the page image of
#     the MDZ scan of the original printing (bsb10858362, scan 00054); English
#     working translation for this site.
#   Zauberlehrling: first printing, Schiller's Musen-Almanach fuer das Jahr 1798,
#     pp. 32-37, via the German Wikisource transcription (orthography preserved);
#     English: Edgar Alfred Bowring, "The Pupil in Magic" (1853), public domain.
#   Iliad XVIII 369-379, 410-421: Greek via the Greek Wikisource transcription;
#     English: Samuel Butler (1898), public domain (PG #2199).
#   Politics I 1253b23-1254a1: Greek via the Greek Wikisource transcription
#     (Bekker text); English: William Ellis (PG #6762), public domain.
#   R.U.R.: Czech via the Czech Wikisource transcription of the Aventinum first
#     edition, Prague 1920 (PD, Capek +1938); English working translations for
#     this site - Paul Selver's 1923 stage version was not consulted.
import io, json

REPO = 'C:/Users/leofa/OneDrive/Desktop/AI Predecessors/repo'

def write(data, name):
    n = sum(len(s['units']) for s in data['sections'])
    io.open(f'{REPO}/data/{name}.json', 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False))
    print(f'{name}: {n} units, {len(data["sections"])} sections')

# =========================================================== GOLEM ANTHOLOGY
G = {"id": "golem", "autor": "Golem — an anthology", "titel": "The golem: Tanach · Talmud · Sefer Yetzirah · Grimm (1808)",
"jahr": "Tanach – 1808", "lang": "he", "zitierweise": "San. 65b [k]",
"quelle": "Ps 139:16 (Masoretic text), Sanhedrin 38b and 65b (Vilna printing) and Sefer Yetzirah 1–2 after the Sefaria text exports of the public-domain Hebrew/Aramaic texts; Jacob Grimm's notice after the original printing in the Zeitung für Einsiedler No. 7 (23 April 1808), col. 56, transcribed from the page image of the MDZ scan of the first printing.",
"hinweis": "An anthology of the golem tradition's primary layers, chosen for the argument: the word's single biblical occurrence, the two classical Talmudic passages (the created man who cannot speak; creation by the Book of Formation), the letter-combinatorics of the Sefer Yetzirah, and the 1808 notice through which Jacob Grimm carried the legend into Romantic literature. All English is this site's unofficial working translation, made from the originals and consulting no copyrighted translation — cite the originals. The later Prague legend of Rabbi Loew is a nineteenth-to-twentieth-century construction and is deliberately not carried here.",
"sections": []}

G["sections"].append({"id": "ps", "titel": "Psalm 139:16 — the word", "units": [
 {"n": 1, "k": 1, "label": "Ps 139:16",
  "orig": "גׇּלְמִ֤י ׀ רָ֘א֤וּ עֵינֶ֗יךָ וְעַֽל־סִפְרְךָ֮ כֻּלָּ֢ם יִכָּ֫תֵ֥בוּ יָמִ֥ים יֻצָּ֑רוּ (ולא) [וְל֖וֹ] אֶחָ֣ד בָּהֶֽם׃",
  "txt": "Thine eyes saw my unformed mass (golmi), and in thy book all of them were written — days that were fashioned, when as yet there was none of them.",
  "note": "The only occurrence of the word in the Hebrew Bible: golem as the yet-unformed body seen by God — matter before speech, written in a book before it lives."}]})

G["sections"].append({"id": "san", "titel": "Talmud Bavli — Sanhedrin 38b · 65b", "units": [
 {"n": 2, "k": 1, "label": "Sanhedrin 38b",
  "orig": "אָמַר רַבִּי יוֹחָנָן בַּר חֲנִינָא: שְׁתֵּים עֶשְׂרֵה שָׁעוֹת הָוֵי הַיּוֹם. שָׁעָה רִאשׁוֹנָה – הוּצְבַּר עֲפָרוֹ, שְׁנִיָּה – נַעֲשָׂה גּוֹלֶם, שְׁלִישִׁית – נִמְתְּחוּ אֵבָרָיו, רְבִיעִית – נִזְרְקָה בּוֹ נְשָׁמָה, חֲמִישִׁית – עָמַד עַל רַגְלָיו, שִׁשִּׁית – קָרָא שֵׁמוֹת, שְׁבִיעִית – נִזְדַּוְּוגָה לוֹ חַוָּה, שְׁמִינִית – עָלוּ לַמִּטָּה שְׁנַיִם וְיָרְדוּ אַרְבָּעָה, תְּשִׁיעִית – נִצְטַוָּוה שֶׁלֹּא לֶאֱכוֹל מִן הָאִילָן, עֲשִׂירִית – סָרַח, אַחַת עֶשְׂרֵה – נִידּוֹן, שְׁתֵּים עֶשְׂרֵה – נִטְרַד וְהָלַךְ לוֹ, שֶׁנֶּאֱמַר: ״אָדָם בִּיקָר בַּל יָלִין״.",
  "txt": "Rabbi Yochanan bar Chanina said: The day has twelve hours. In the first hour his dust was gathered; in the second he was made a golem; in the third his limbs were stretched out; in the fourth the soul was cast into him; in the fifth he stood on his feet; in the sixth he called the names; in the seventh Eve was joined to him; in the eighth they went up to the bed two and came down four; in the ninth he was commanded not to eat of the tree; in the tenth he sinned; in the eleventh he was judged; in the twelfth he was driven out and departed, as it is said: “Man abideth not in honour.”",
  "note": "Adam himself passes through the golem stage: the unformed mass is the second hour of every human being."},
 {"n": 3, "k": 2, "label": "Sanhedrin 65b",
  "orig": "אָמַר רָבָא: אִי בָּעוּ צַדִּיקֵי, בָּרוּ עָלְמָא, שֶׁנֶּאֱמַר: ״כִּי עֲוֹנוֹתֵיכֶם הָיוּ מַבְדִּלִים וְגוֹ׳״.",
  "txt": "Rava said: If the righteous wished, they could create a world, as it is said: “For your iniquities have separated between you and your God.”"},
 {"n": 4, "k": 3, "label": "Sanhedrin 65b — Rava's man",
  "orig": "רָבָא בְּרָא גַּבְרָא. שַׁדְּרֵיהּ לְקַמֵּיהּ דְּרַבִּי זֵירָא. הֲוָה קָא מִשְׁתַּעֵי בַּהֲדֵיהּ, וְלָא הֲוָה קָא מַהְדַּר לֵיהּ. אֲמַר לֵיהּ: מִן חַבְרַיָּא אַתְּ, הֲדַר לְעַפְרָיךְ.",
  "txt": "Rava created a man. He sent him to Rabbi Zeira. He spoke with him, and he did not answer him. He said to him: You are from the companions — return to your dust.",
  "note": "The language test, stated as narrative: the created man is unmasked because he cannot answer speech with speech. Compare, in this corpus, Descartes's Discours Part V — the same criterion, argued three centuries ago; told here more than a millennium earlier."},
 {"n": 5, "k": 4, "label": "Sanhedrin 65b — by the Book of Formation",
  "orig": "רַב חֲנִינָא וְרַב אוֹשַׁעְיָא הֲווֹ יָתְבִי כׇּל מַעֲלֵי שַׁבְּתָא, וְעָסְקִי בְּסֵפֶר יְצִירָה, וּמִיבְּרֵי לְהוּ עִיגְלָא תִּילְתָּא, וְאָכְלִי לֵיהּ.",
  "txt": "Rav Chanina and Rav Oshaya sat every Sabbath eve and busied themselves with the Sefer Yetzirah, and a third-grown calf was created for them, and they ate it.",
  "note": "The Talmud itself names the instrument: creation is worked by study of the Book of Formation — by letters."}]})

G["sections"].append({"id": "sy", "titel": "Sefer Yetzirah — the letters (selections)", "units": [
 {"n": 6, "k": 1, "label": "SY 1:1",
  "orig": "בשלשים ושתים נתיבות פליאות חכמה חקק יה יהוה צבאות אלהי ישראל אלהים חיים ומלך עולם אל שדי רחום וחנון רם ונשא שוכן עד מרום וקדוש שמו וברא את עולמו בשלשה ספרים בספר וספר וספור:",
  "txt": "By thirty-two wondrous paths of wisdom Yah, the LORD of hosts, the God of Israel, the living God and King of the world, El Shaddai, merciful and gracious, high and exalted, dwelling in eternity, whose name is holy, engraved — and created His world by three books: by writing (sefer), by number (sefar) and by speech (sippur)."},
 {"n": 7, "k": 2, "label": "SY 1:2",
  "orig": "עשר ספירות בלי מה ועשרים ושתים אותיות יסוד שלש אמות ושבע כפולות ושתים עשרה פשוטות:",
  "txt": "Ten sefirot of nothingness, and twenty-two foundation letters: three mothers, seven doubles and twelve simples."},
 {"n": 8, "k": 3, "label": "SY 2:2",
  "orig": "עשרים ושתים אותיות חקקן חצבן שקלן והמירן צרפן וצר בהם נפש כל היצור ונפש כל העתיד לצור:",
  "txt": "Twenty-two foundation letters: He engraved them, hewed them, weighed them, exchanged them, combined them — and formed with them the soul of all that is created and the soul of all that is yet to be formed.",
  "note": "Creation as letter-operations: engrave, hew, weigh, exchange, combine. The vocabulary of a symbol calculus, a millennium before Llull and Leibniz."},
 {"n": 9, "k": 4, "label": "SY 2:4",
  "orig": "עשרים ושתים אותיות יסוד קבועות בגלגל ברל\"א שערים וחוזר הגלגל פנים ואחור וזהו סימן לדבר אין בטובה למעלה מענג ואין ברעה למטה מנגע:",
  "txt": "Twenty-two foundation letters, fixed in a wheel with two hundred and thirty-one gates; and the wheel turns forward and backward. And this is the sign of the matter: there is nothing in good higher than delight (oneg), and nothing in evil lower than the plague (nega).",
  "note": "The rotating wheel of letters with its 231 gates — compare, in this corpus, the fourth figure of Llull's Ars brevis: three rotating circles, 252 chambers. Oneg and nega are the same three letters, permuted."},
 {"n": 10, "k": 5, "label": "SY 2:5",
  "orig": "כיצד שקלן והמירן אל\"ף עם כלם וכלם עם אל\"ף, בי\"ת עם כלם וכלם עם בי\"ת וחוזרת חלילה נמצא כל היצור וכל הדבור יוצא בשם אחד:",
  "txt": "How did He weigh and exchange them? Aleph with them all, and all of them with Aleph; Bet with them all, and all of them with Bet; and so it turns round and round; and it follows that all creation and all speech go out by one Name.",
  "note": "Exhaustive pairwise combination — the generative procedure itself. Removing the Aleph is what, in the later legend, turns truth (emet) into death (met)."}]})

G["sections"].append({"id": "grimm", "titel": "Jacob Grimm, Zeitung für Einsiedler (1808)", "units": [
 {"n": 11, "k": 1, "label": "Entstehung der Verlagspoesie — col. 56",
  "orig": "Die polnischen Juden machen nach gewissen gesprochenen Gebeten und gehaltenen Fasttägen, die Gestalt eines Menschen aus Thon oder Leimen, und wenn sie das wunderkräftige Schemhamphoras darüber sprechen, so muß er lebendig werden. Reden kann er zwar nicht, versteht aber ziemlich was man spricht und befiehlt. Sie heißen ihn Golem, und brauchen ihn zu einem Aufwärter, allerley Hausarbeit zu verrichten, allein er darf nimmer aus dem Hause gehen. An seiner Stirn steht geschrieben אמת aemaeth (Wahrheit, Gott) er nimmt aber täglich zu, und wird leicht größer und stärker denn alle Hausgenossen, so klein er anfangs gewesen ist. Daher sie aus Furcht vor ihm den ersten Buchstaben auslöschen, so daß nichts bleibt als מת maeth (er ist todt) worauf er zusammenfällt und wiederum in Ton aufgelöst wird.",
  "txt": "The Polish Jews, after certain spoken prayers and observed fast-days, make the figure of a man out of clay or loam, and when they speak the wonder-working Schemhamphoras over it, it must come to life. Speak it cannot, but it understands fairly well what one says and commands. They call it Golem and use it as a servant, to perform all manner of housework; only it may never leave the house. On its forehead stands written אמת aemaeth (truth, God); but it gains daily, and easily grows taller and stronger than all the members of the household, however small it was at first. Therefore, out of fear of it, they efface the first letter, so that nothing remains but מת maeth (he is dead), whereupon it collapses and is dissolved into clay again.",
  "note": "The animating and the killing inscription: one letter separates truth from death. The notice through which the legend entered Romantic literature — Arnim, Hoffmann and the nineteenth century read it here."},
 {"n": 12, "k": 2, "label": "The master crushed",
  "orig": "Einem ist sein Golem aber einmal so hoch geworden und hat ihn aus Sorglosigkeit immer wachsen lassen, daß er ihm nicht mehr an die Stirn reichen können. Da hat er aus der großen Angst dem Knecht geheißen, ihm die Stiefel auszuziehen, in der Meinung, daß er ihm beim Bücken an die Stirne reichen könne. Dies ist auch geschehen, und der erste Buchstab glücklich ausgethan worden, allein die ganze Leimlast fiel auf den Juden und erdrückte ihn. — Mitgetheilt von Jakob Grimm in Cassel.",
  "txt": "But one man's golem once grew so tall — he had carelessly let it keep growing — that he could no longer reach its forehead. In his great fear he bade the servant pull off his boots, thinking that as it bent down he could reach its forehead. This came to pass, and the first letter was successfully effaced; but the whole load of loam fell upon the Jew and crushed him. — Communicated by Jakob Grimm in Cassel.",
  "note": "The control problem in one sentence: the servant grew past the master's reach, and the shutdown itself was fatal."}]})

write(G, "golem_anthologie")

# ======================================================== DER ZAUBERLEHRLING
ZL_DE = [
"Hat der alte Hexenmeister,\nSich doch einmal wegbegeben!\nUnd nun sollen seine Geister\nAuch nach meinem Willen leben.\nSeine Wort und Werke\nMerkt ich, und den Brauch,\nUnd mit Geistesstärke\nThu ich Wunder auch.",
"Walle! walle!\nManche Strecke,\nDaß zum Zwecke,\nWasser fließe,\nUnd, mit reichem vollem Schwalle,\nZu dem Bade sich ergieße.",
"Und nun komm du alter Besen,\nNimm die schlechten Lumpenhüllen,\nBist schon lange Knecht gewesen,\nNun erfülle meinen Willen.\nAuf zwey Beinen stehe,\nOben sey ein Kopf,\nEile nun und gehe\nMit dem Wassertopf.",
"Walle! walle!\nManche Strecke,\nDaß, zum Zwecke,\nWasser fließe,\nUnd, mit reichem vollem Schwalle,\nZu dem Bade sich ergieße.",
"Seht er läuft zum Ufer nieder,\nWarlich ist schon an dem Flusse,\nUnd mit Blitzesschnelle wieder\nIst er hier mit raschem Gusse.\nSchon zum zweytenmale!\nWie das Becken schwillt!\nWie sich jede Schaale\nVoll mit Wasser füllt!",
"Stehe! Stehe!\nDenn wir haben\nDeiner Gaben\nVollgemessen! –\nAch ich merk es, wehe! wehe!\nHab ich doch das Wort vergessen!",
"Ach! das Wort, worauf am Ende\nEr das wird was er gewesen.\nAch er läuft und bringt behende,\nWärst du doch der alte Besen!\nImmer neue Güsse\nBringt er schnell herein,\nAch! und hundert Flüsse\nStürzen auf mich ein.",
"Nein nicht länger\nKann ichs lassen,\nWill ihn fassen.\nDas ist Tücke!\nAch! nun wird mir immer bänger!\nWelche Mine! welche Blicke!",
"O! du Ausgeburt der Hölle!\nSoll das ganze Haus ersaufen?\nSeh ich über jede Schwelle\nDoch schon Wasserströme laufen.\nEin verruchter Besen\nDer nicht hören will!\nStock! der du gewesen,\nSteh doch wieder still!",
"Willsts am Ende\nGar nicht lassen;\nWill dich fassen,\nWill dich halten,\nUnd das alte Holz behende\nMit dem scharfen Beile spalten.",
"Seht da kommt er schleppend wieder!\nWie ich mich nun auf dich werfe,\nGleich, o Kobold! liegst du nieder,\nKrachend trifft die glatte Schärfe.\nWarlich braf getroffen!\nSeht er ist entzwey,\nUnd nun kann ich hoffen,\nUnd ich athme frey!",
"Wehe! wehe!\nBeyde Theile\nStehn, in Eile,\nSchon als Knechte\nVöllig fertig in die Höhe!\nHelft mir ach ihr hohen Mächte!",
"Und sie laufen! Naß und nässer\nWirds im Saal und auf den Stufen,\nWelch entsetzliches Gewässer!\nHerr und Meister! hör mich rufen!\nAch! da kommt der Meister!\nHerr, die Noth ist groß,\nDie ich rief die Geister\nWerd ich nun nicht los.",
"„In die Ecke,\nBesen! Besen!\nSeyds gewesen.\nDenn als Geister\nRuft euch nur zu seinem Zwecke,\nErst hervor der alte Meister.“",
]
ZL_EN = [
"I am now, — what joy to hear it! —\nOf the old magician rid;\nAnd henceforth shall ev'ry spirit\nDo whate'er by me is bid;\nI have watch'd with rigour\nAll he used to do,\nAnd will now with vigour\nWork my wonders too.",
"Wander, wander\nOnward lightly,\nSo that rightly\nFlow the torrent,\nAnd with teeming waters yonder\nIn the bath discharge its current!",
"And now come, thou well-worn broom,\nAnd thy wretched form bestir;\nThou hast ever served as groom,\nSo fulfil my pleasure, sir!\nOn two legs now stand,\nWith a head on top;\nWaterpail in hand,\nHaste, and do not stop!",
"Wander, wander\nOnward lightly,\nSo that rightly\nFlow the torrent,\nAnd with teeming waters yonder\nIn the bath discharge its current!",
"See! he's running to the shore,\nAnd has now attain'd the pool,\nAnd with lightning speed once more\nComes here, with his bucket full!\nBack he then repairs;\nSee how swells the tide!\nHow each pail he bears\nStraightway is supplied!",
"Stop, for, lo!\nAll the measure\nOf thy treasure\nNow is right! —\nAh, I see it! woe, oh woe!\nI forget the word of might.",
"Ah, the word whose sound can straight\nMake him what he was before!\nAh, he runs with nimble gait!\nWould thou wert a broom once more!\nStreams renew'd for ever\nQuickly bringeth he;\nRiver after river\nRusheth on poor me!",
"Now no longer\nCan I bear him;\nI will snare him,\nKnavish sprite!\nAh, my terror waxes stronger!\nWhat a look! what fearful sight!",
"Oh, thou villain child of hell!\nShall the house through thee be drown'd?\nFloods I see that wildly swell,\nO'er the threshold gaining ground.\nWilt thou not obey,\nOh, thou broom accurs'd?\nBe thou still I pray,\nAs thou wert at first!",
"Will enough\nNever please thee?\nI will seize thee,\nHold thee fast,\nAnd thy nimble wood so tough,\nWith my sharp axe split at last.",
"See, once more he hastens back!\nNow, oh Cobold, thou shalt catch it!\nI will rush upon his track;\nCrashing on him falls my hatchet.\nBravely done, indeed!\nSee, he's cleft in twain!\nNow from care I'm freed,\nAnd can breathe again.",
"Woe, oh woe!\nBoth the parts,\nQuick as darts,\nStand on end,\nServants of my dreaded foe!\nOh, ye gods protection send!",
"And they run! and wetter still\nGrow the steps and grows the hall.\nLord and master hear me call!\nEver seems the flood to fill.\nAh, he's coming! see,\nGreat is my dismay!\nSpirits raised by me\nVainly would I lay!",
"“To the side\nOf the room\nHasten, broom,\nAs of old!\nSpirits I have ne'er untied\nSave to act as they are told.”",
]
NOTES = {
 6: "«Hab ich doch das Wort vergessen!» — the forgotten stop-command. Norbert Wiener made this stanza the emblem of the control problem of automatic machines; the AI-safety literature still calls it the sorcerer's-apprentice problem.",
 11: "Splitting the servant doubles it: the countermeasure multiplies the process it was meant to stop.",
 13: "«Die ich rief die Geister / Werd ich nun nicht los» — the line the whole later debate quotes.",
 14: "Only the master holds the revoking word: the spirits obey the one who can also call them back.",
}
zu = []
for i, (de, en) in enumerate(zip(ZL_DE, ZL_EN), 1):
    u = {"n": i, "k": i, "orig": de, "txt": en, "verse": True}
    if i in NOTES: u["note"] = NOTES[i]
    zu.append(u)
Z = {"id": "zauberlehrling", "autor": "Johann Wolfgang von Goethe", "titel": "Der Zauberlehrling (1797/98), complete",
"jahr": 1798, "lang": "de", "zitierweise": "Zauberlehrling, st. k",
"quelle": "First printing: Musen-Almanach für das Jahr 1798, ed. Friedrich Schiller (Tübingen: Cotta, 1798), pp. 32–37, via the German Wikisource transcription of the first printing; its orthography (zwey, Warlich, braf) is preserved. Public domain.",
"hinweis": "Complete, in its fourteen stanzas. The English is Edgar Alfred Bowring's public-domain translation of 1853 (“The Pupil in Magic”), given stanza for stanza.",
"sections": [{"id": "b", "titel": "Der Zauberlehrling — the ballad", "units": zu}]}
write(Z, "goethe_zauberlehrling")

# ===================================================== HOMER AND ARISTOTLE
A = {"id": "automata", "autor": "Homer · Aristotle", "titel": "The self-working tools: Iliad XVIII · Politics I 4",
"jahr": "c. 750 – c. 330 BC", "lang": "grc", "zitierweise": "Il. XVIII [k] · Pol. I 4 [k]",
"quelle": "Iliad XVIII 369–379 and 410–421, Greek after the Greek Wikisource transcription; English: Samuel Butler's public-domain prose translation of 1898 (Project Gutenberg #2199). Politics I, 1253b23–1254a1, Greek (Bekker text) after the Greek Wikisource transcription; English: William Ellis's public-domain translation (Project Gutenberg #6762).",
"hinweis": "The oldest artificial servants of the Western canon, and the philosopher who drew from them the first argument about automation and labour. Aristotle quotes the poet directly: the passage on Hephaestus' tripods is the very one given here.",
"sections": []}

A["sections"].append({"id": "il", "titel": "Iliad XVIII — Hephaestus' works", "units": [
 {"n": 1, "k": 1, "label": "XVIII 369–379 — the tripods", "verse": True,
  "orig": "Ἡφαίστου δ’ ἵκανε δόμον Θέτις ἀργυρόπεζα\nἄφθιτον ἀστερόεντα, μεταπρεπέ’ ἀθανάτοισι\nχάλκεον, ὅν ῥ’ αὐτὸς ποιήσατο κυλλοποδίων.\nτὸν δ’ εὗρ’ ἱδρώοντα ἑλισσόμενον περὶ φύσας\nσπεύδοντα· τρίποδας γὰρ ἐείκοσι πάντας ἔτευχεν\nἑστάμεναι περὶ τοῖχον ἐϋσταθέος μεγάροιο,\nχρύσεα δέ σφ’ ὑπὸ κύκλα ἑκάστῳ πυθμένι θῆκεν,\nὄφρά οἱ αὐτόματοι θεῖον δυσαίατ’ ἀγῶνα\nἠδ’ αὖτις πρὸς δῶμα νεοίατο, θαῦμα ἰδέσθαι.\nοἱ δ’ ἤτοι τόσσον μὲν ἔχον τέλος, οὔατα δ’ οὔ πω\nδαιδάλεα προσέκειτο· τά ῥ’ ἤρτυε, κόπτε δὲ δεσμούς.",
  "txt": "Meanwhile Thetis came to the house of Vulcan, imperishable, star-bespangled, fairest of the abodes in heaven, a house of bronze wrought by the lame god's own hands. She found him busy with his bellows, sweating and hard at work, for he was making twenty tripods that were to stand by the wall of his house, and he set wheels of gold under them all that they might go of their own selves to the assemblies of the gods, and come back again — marvels indeed to see. They were finished all but the ears of cunning workmanship which yet remained to be fixed to them: these he was now fixing, and he was hammering at the rivets.",
  "note": "αὐτόματοι — «of their own selves»: the word automaton enters literature here, as a property of a god's furniture."},
 {"n": 2, "k": 2, "label": "XVIII 410–421 — the golden handmaids", "verse": True,
  "orig": "Ἦ, καὶ ἀπ’ ἀκμοθέτοιο πέλωρ αἴητον ἀνέστη\nχωλεύων· ὑπὸ δὲ κνῆμαι ῥώοντο ἀραιαί.\nφύσας μέν ῥ’ ἀπάνευθε τίθει πυρός, ὅπλά τε πάντα\nλάρνακ’ ἐς ἀργυρέην συλλέξατο, τοῖς ἐπονεῖτο·\nσπόγγῳ δ’ ἀμφὶ πρόσωπα καὶ ἄμφω χεῖρ’ ἀπομόργνυ\nαὐχένα τε στιβαρὸν καὶ στήθεα λαχνήεντα,\nδῦ δὲ χιτῶν’, ἕλε δὲ σκῆπτρον παχύ, βῆ δὲ θύραζε\nχωλεύων· ὑπὸ δ’ ἀμφίπολοι ῥώοντο ἄνακτι\nχρύσειαι ζωῇσι νεήνισιν εἰοικυῖαι.\nτῇς ἐν μὲν νόος ἐστὶ μετὰ φρεσίν, ἐν δὲ καὶ αὐδὴ\nκαὶ σθένος, ἀθανάτων δὲ θεῶν ἄπο ἔργα ἴσασιν.\nαἱ μὲν ὕπαιθα ἄνακτος ἐποίπνυον·",
  "txt": "On this the mighty monster hobbled off from his anvil, his thin legs plying lustily under him. He set the bellows away from the fire, and gathered his tools into a silver chest. Then he took a sponge and washed his face and hands, his shaggy chest and brawny neck; he donned his shirt, grasped his strong staff, and limped towards the door. There were golden handmaids also who worked for him, and were like real young women, with sense and reason, voice also and strength, and all the learning of the immortals; these busied themselves as the king bade them.",
  "note": "νόος … αὐδὴ καὶ σθένος — mind, voice and strength: the golden maidens are granted precisely what Rava's created man lacks and what Descartes will deny to machines. Only a god's artefacts pass the test."}]})

A["sections"].append({"id": "pol", "titel": "Politics I 4 — the argument from automation", "units": [
 {"n": 3, "k": 1, "label": "1253b23–33",
  "orig": "ἐπεὶ οὖν ἡ κτῆσις μέρος τῆς οἰκίας ἐστὶ καὶ ἡ κτητικὴ μέρος τῆς οἰκονομίας (ἄνευ γὰρ τῶν ἀναγκαίων ἀδύνατον καὶ ζῆν καὶ εὖ ζῆν), ὥσπερ δὲ ταῖς ὡρισμέναις τέχναις ἀναγκαῖον ἂν εἴη ὑπάρχειν τὰ οἰκεῖα ὄργανα, εἰ μέλλει ἀποτελεσθήσεσθαι τὸ ἔργον, οὕτω καὶ τῷ οἰκονομικῷ. τῶν δ’ ὀργάνων τὰ μὲν ἄψυχα τὰ δὲ ἔμψυχα (οἷον τῷ κυβερνήτῃ ὁ μὲν οἴαξ ἄψυχον ὁ δὲ πρῳρεὺς ἔμψυχον· ὁ γὰρ ὑπηρέτης ἐν ὀργάνου εἴδει ταῖς τέχναις ἐστίν)· οὕτω καὶ τὸ κτῆμα ὄργανον πρὸς ζωήν ἐστι, καὶ ἡ κτῆσις πλῆθος ὀργάνων ἐστί, καὶ ὁ δοῦλος κτῆμά τι ἔμψυχον, καὶ ὥσπερ ὄργανον πρὸ ὀργάνων πᾶς ὑπηρέτης.",
  "txt": "As property is a part of the household, and the art of acquiring property a part of the management of a family — for without necessaries it is impossible to live, and to live well — and as in the settled arts the proper instruments must be at hand if the work is to be accomplished, so it is in household management. Now of instruments some are without life and some are alive: thus for the pilot of a ship the tiller is a lifeless instrument, the look-out man a living one; for a servant stands, in the arts, in the rank of an instrument. So too a possession is an instrument for living, property a multitude of instruments, and the slave a living possession — and every assistant is as it were an instrument prior to other instruments.",
  "note": "ὁ δοῦλος κτῆμά τι ἔμψυχον — «the slave is a living instrument»: the sentence to which the whole passage, and much of the later debate about machine labour, responds."},
 {"n": 4, "k": 2, "label": "1253b33–1254a1",
  "orig": "εἰ γὰρ ἠδύνατο ἕκαστον τῶν ὀργάνων κελευσθὲν ἢ προαισθανόμενον ἀποτελεῖν τὸ αὑτοῦ ἔργον, ὥσπερ τὰ Δαιδάλου φασὶν ἢ τοὺς τοῦ Ἡφαίστου τρίποδας, οὕς φησιν ὁ ποιητὴς αὐτομάτους θεῖον δύεσθαι ἀγῶνα, οὕτως αἱ κερκίδες ἐκέρκιζον αὐταὶ καὶ τὰ πλῆκτρα ἐκιθάριζεν, οὐδὲν ἂν ἔδει οὔτε τοῖς ἀρχιτέκτοσιν ὑπηρετῶν οὔτε τοῖς δεσπόταις δούλων.",
  "txt": "For if every instrument could accomplish its own work at command, or by anticipating the will — as the story goes of the statues of Daedalus, or the tripods of Hephaestus, which the poet says entered the assembly of the gods of their own accord — if thus the shuttle would weave and the plectrum play the lyre of themselves, then master-builders would need no assistants, and masters no slaves.",
  "note": "The counterfactual of full automation, stated once and for all: tools that obey the command, or anticipate it (προαισθανόμενον), would dissolve the relation of master and servant. The condition Aristotle thought impossible is the one the corpus's machine line begins to build."}]})
write(A, "automata_antike")

# ================================================================= R.U.R.
R = {"id": "capek", "autor": "Karel Čapek", "titel": "R.U.R. — Rossum's Universal Robots (1920), selections",
"jahr": 1920, "lang": "cs", "zitierweise": "RUR, Pred. [k] · RUR III [k]",
"quelle": "R.U.R. Rossumovi univerzální roboti. Kolektivní drama (Prague: Aventinum, 1920), Czech text via the Czech Wikisource transcription of the first edition. Public domain (Čapek †1938).",
"hinweis": "The threshold text of the line: written in Prague, where the golem legend had settled, it turns the made servant of myth into the manufactured worker of industry — and gives the twentieth century the word robot (from robota, compulsory labour; the word was suggested to Čapek by his brother Josef). Selections chosen for the argument. The English is this site's working translation from the Czech; Paul Selver's stage version of 1923 was not consulted.",
"sections": []}

R["sections"].append({"id": "pred", "titel": "Předehra — the making of the worker", "units": [
 {"n": 1, "k": 1, "label": "Domin and Helena Glory",
  "orig": "Domin: … A vyrábět umělé dělníky je stejné jako vyrábět naftové motory. Výroba má být co nejjednodušší a výrobek prakticky nejlepší. Co myslíte, jaký dělník je prakticky nejlepší?\n\nHelena: Nejlepší? Snad ten, který — který — když je poctivý — a oddaný.\n\nDomin: Ne, ale ten nejlacinější. Ten, který má nejmíň potřeb. Mladý Rossum vynalezl dělníka s nejmenším počtem potřeb. Musel ho zjednodušit. Vyhodil všechno, co neslouží přímo práci. Tím vlastně vyhodil člověka a udělal Robota. Drahá slečno Gloryová, Roboti nejsou lidé. Jsou mechanicky dokonalejší než my, mají úžasnou rozumovou inteligenci, ale nemají duši.",
  "txt": "Domin: … And to manufacture artificial workers is the same as to manufacture petrol engines. The production must be as simple as possible, and the product practically the best. What do you think — which worker is practically the best?\n\nHelena: The best? Perhaps the one who — who — when he is honest — and devoted.\n\nDomin: No: the cheapest one. The one with the fewest needs. Young Rossum invented the worker with the smallest number of needs. He had to simplify him. He threw out everything that does not serve work directly. In doing so he threw out the man, really, and made the Robot. My dear Miss Glory, Robots are not people. They are mechanically more perfect than we are, they have an astonishing rational intelligence, but they have no soul.",
  "note": "The first explanation of the word robot on any stage. The made servant is no longer conjured but costed: optimization, not incantation, strips the man out of the worker."},
 {"n": 2, "k": 2, "label": "The product of God",
  "orig": "Helena: Říká se, že člověk je výrobek boží.\n\nDomin: Tím hůř. Bůh neměl ani ponětí o moderní technice.",
  "txt": "Helena: They say that man is the product of God.\n\nDomin: So much the worse. God had no notion of modern technology.",
  "note": "La Mettrie's provocation, one industrial revolution later — and no longer a paradox but a sales argument."}]})

R["sections"].append({"id": "akt3", "titel": "Dějství třetí — the ending", "units": [
 {"n": 3, "k": 1, "label": "Alquist alone",
  "orig": "Alquist: … Rossume, Fabry, Galle, velicí vynálezci, co jste vynalezli velkého proti té dívce, proti tomu chlapci, proti tomu prvnímu páru, který vynašel lásku, pláč, úsměv milování, lásku muže a ženy? Přírodo, přírodo, život nezahyne! Kamarádi, Heleno, život nezahyne! Zase se začne z lásky, začne se nahý a maličký; ujme se v pustině, a nebude mu k ničemu, co jsme dělali a budovali, k ničemu města a továrny, k ničemu naše umění, k ničemu naše myšlenky, a přece nezahyne! Jen my jsme zahynuli. Rozvalí se domy a stroje, rozpadnou se systémy a jména velikých opadají jako listí; jen ty, lásko, vykveteš na rumišti a svěříš větrům semínko života. … Nezahyne! (rozpřáhne ruce) Nezahyne!",
  "txt": "Alquist: … Rossum, Fabry, Gall, great inventors — what did you ever invent that is great, against that girl, against that boy, against this first pair, who have invented love, weeping, the smile of loving, the love of man and woman? Nature, nature — life will not perish! Comrades, Helena, life will not perish! It will begin again out of love; it will begin naked and little; it will take root in the wilderness, and nothing we did and built will be of use to it, no use our cities and factories, no use our art, no use our thoughts — and yet it will not perish! Only we have perished. The houses and machines will fall in ruins, the systems will crumble, and the names of the great will drop away like leaves; only you, love, will blossom on the rubble and entrust to the winds the little seed of life. … It will not perish! (stretching out his arms) It will not perish!",
  "note": "The play's last word, at the threshold: after the makers and their manufacture, what cannot be manufactured — the encounter of two — begins the world again. Sixteen years later Turing's paper opens the corpus's other door; the apparatus ends here."}]})
write(R, "capek_rur")
