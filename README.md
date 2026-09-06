# Calculemus — philosophical predecessors of AI

A research apparatus for the prehistory of the AI debate: the public-domain texts in which
reasoning first became reckoning, reckoning became algebra, algebra became a formal system —
together with the machines that made the idea tangible, and the philosophers who said it could
not be done. Built as a static site: paragraph-exact citation, cross-corpus concordance, no
tracking — plus one optional server function, the citation-bound **Dialogue**
(`netlify/functions/dialogue.mjs`): a browser-side BM25 retrieval selects the bearing
paragraphs, and only these plus the question go to the Claude API (`claude-sonnet-5`), which
must answer from them alone, citation on every claim. Requires `ANTHROPIC_API_KEY` in the
Netlify environment; without it the retrieval still works and the answering degrades
gracefully. Data path: see the site's privacy page.

The name is Leibniz's: when disputes arise, *Calculemus* — let us calculate.

## The introductory essay

The site opens with a stand-alone scholarly introduction (*Calculemus: An Introduction to the
Philosophical Predecessors of Artificial Intelligence*, September 2026), reachable under
*Introduction*. It presents the four lines, the argument that runs through them, the reason
the corpus ends at the threshold of Turing, and the way the apparatus is meant to be used;
the first mention of each work links into its reader. Five curated **reading paths**
(*Paths*) offer guided routes through the corpus, each with a stated order and a guiding
question per station. The essay lives in
`data/introduction.json`, built by `tools/build-introduction.py` from the author's manuscript
(kept beside the repository, not in it), and is editorial matter under CC BY 4.0.

## The programme

The corpus is built in stages along four lines. Status is tracked in `data/works.json` and on
the site's overview. A per-module link list of the digitized sources is in
[SOURCES.md](SOURCES.md).

**The logic line** (direct ancestry of symbolic AI)

| Author | Text | Source | Status |
|---|---|---|---|
| Ramon Llull | *Ars brevis* (1308) — prologue, alphabet, first and fourth figure (the rotating wheels) | Strasbourg 1617 (Zetzner), IA scan, OCR emended; working translation | **shipped** |
| al-Khwārizmī | *The Algebra* (c. 820), author's preface and opening — the name behind *algorithm* | Rosen 1831 (PD English); Arabic printed in Rosen's edition, not yet carried | **shipped** |
| Ibn Khaldūn | The zāʾirja passages of the *Muqaddima* (1377) — the Arabic letter-machine, described and epistemically dismantled | Arabic via Arabic Wikisource; working translation (Rosenthal not consulted; de Slane PD as documentation) | **shipped** |
| Yijing (Xici zhuan) | Xici I.11 and II.2 — the binary generation of the trigrams that Leibniz read as his arithmetic anticipated | Chinese via Chinese Wikisource; Legge 1882 (PD) | **shipped** |
| Thomas Hobbes | *Leviathan* (1651), Introduction + Part I ch. I–V; later De Corpore I | Project Gutenberg #3207 (1651 spelling) | **shipped** |
| G. W. Leibniz | Anthology: Monadology (§§1–90), Explication de l'arithmétique binaire (1703), characteristica fragments incl. the calculemus passages, De arte combinatoria selections | PG #17641 (FR) + Latta 1898 (EN, PD); Gerhardt GM7 / GP IV+VII, OCR emended; working translations | **shipped** |
| George Boole | *Laws of Thought* (1854), Preface + ch. I–III, XXII | Project Gutenberg #15114 (LaTeX), converted | **shipped** |
| Gottlob Frege | Begriffsschrift Vorwort (1879), *Grundlagen* Einl. + §§ 1–4, 87–91, 106–109, *Über Sinn und Bedeutung* (1892) complete | IA scan (BS, OCR emended); PG #48312 (GL); DTA frege_sinn_1892 (SuB); working translations — no PD English exists | **shipped** |

**The machine line**

| Author | Text | Source | Status |
|---|---|---|---|
| Blaise Pascal | Pensées, five fragments on machine and thought (Br. 252, 339, 340, 346, 347) | fr.wikisource (Brunschvicg) + Trotter, PG #18269 | **shipped** |
| Ada Lovelace | Notes on Menabrea's *Sketch of the Analytical Engine* (1843), incl. Note G | Taylor's Scientific Memoirs III (IA scan, OCR emended) | **shipped** |
| W. S. Jevons | *On the Mechanical Performance of Logical Inference* (1870), 20 selected articles | Pure Logic and Other Minor Works (1890 reprint), IA scan, OCR emended | **shipped** |
| C. S. Peirce | *Logical Machines* (1887), complete | American Journal of Psychology I (original printing, JSTOR EJC/IA) | **shipped** |

**The counter-voices**

| Author | Text | Source | Status |
|---|---|---|---|
| René Descartes | *Discours de la méthode* (1637), Part V — the language test | PG #13846 (FR) + Veitch, PG #59 (EN), bilingual | **shipped** |
| J. O. de La Mettrie | *L'Homme Machine* (1747) | PG #52090: FR + Bussey 1912 EN, bilingual; 7 silently omitted paragraphs restored | **shipped** |
| Edgar Allan Poe | *Maelzel's Chess-Player* (1836), complete — the chess-Turk hoax as the boundary between calculation and judgment | Southern Literary Messenger II/5 via Wikisource, collated against the Poe Society of Baltimore's text | **shipped** |
| Ernst Kapp | *Grundlinien einer Philosophie der Technik* (1877), selections — organ projection, the telegraph/nervous-system chapter | IA/MDZ scan of the 1877 first edition, OCR emended, verified against page images; working translation | **shipped** |

**The animated word** (the narrative line: the tales that tell what the other lines argue)

| Author | Text | Source | Status |
|---|---|---|---|
| Homer · Aristotle | Iliad XVIII 369–379, 410–421 (the tripods, the golden handmaids) · Politics I 4, 1253b23–1254a1 (the argument from automation) | Greek via Greek Wikisource; Butler 1898 + Ellis (both PD) | **shipped** |
| Liezi | The automaton of Yan Shi (Book V, Tang wen), complete — the oldest full automaton narrative | Chinese via Chinese Wikisource; Giles 1912 (PD) | **shipped** |
| Golem — an anthology | Ps 139:16 · Sanhedrin 38b, 65b · Sefer Yetzirah 1–2 (selections) · Jacob Grimm, Zeitung für Einsiedler (1808) | Hebrew/Aramaic via Sefaria exports of the PD texts, working translations; Grimm transcribed from the MDZ page image of the 1808 printing | **shipped** |
| J. W. Goethe | Der Zauberlehrling (1797/98), complete | First printing (Musen-Almanach 1798) via Wikisource; Bowring 1853 (PD) | **shipped** |
| Karel Čapek | R.U.R. (1920), selections — the word "robot", the ending | Czech via Czech Wikisource (Aventinum 1920, PD); working translations | **shipped** |

A Tractatus module was considered and dropped: the corpus ends at the threshold of Turing.
An editorial **coda** (*After the threshold*) states what the corpus cannot contain — the
dialogical counter-voices of the twentieth century (Buber, Levinas), and, for the narrative
line, Wiener's *God and Golem, Inc.* — and why an anthology, as against a quarry, owes its
readers that declaration.

**The boundary is a rights fact:** Turing's papers of 1936 and 1950 remain in copyright
(until roughly 2032 and 2046). The apparatus therefore ends, deliberately, at the threshold.

## Rights

Everything shipped is in the United States public domain; the site is operated from the US,
whose rules govern its edition choices. Original texts qualify by age. Where no public-domain
English translation exists (Frege; Leibniz's computational texts), the site supplies its own
working translations, marked unofficial and dedicated to the public domain — cite the original.

| What | Files | Licence |
|---|---|---|
| Source code | `index.html`, `app.js`, `style.css` | MIT (`LICENSE`) |
| Editorial matter | work descriptions, method texts, this README | CC BY 4.0 |
| Editions & derived data | `data/*.json` (segmentation, numbering, working translations) | CC0 1.0; the underlying texts are public domain in their own right |
| Extraction tooling | `tools/*.py` | MIT |

## Structure

Static site, no build step. `data/works.json` is the registry (four lines, status);
`data/<work>.json` holds a shipped edition as `{sections: [{id, titel, units: [{n, k, art?,
label?, txt}]}]}` — `n` a global anchor, `k` the per-section paragraph number, `art` the
author's own article number where the original provides one (Boole), `label` the original
marginal note where the printing carries one (Hobbes 1651).

## Citing

> Pantaleon Fassbender, *Calculemus: Philosophical Predecessors of AI*,
> https://github.com/pantaleonfassbender-coder/Philosophical-predecessors-of-AI (accessed …).

When citing a passage, cite the printed original — the paragraph grids exist so that you can;
where a grid is this site's own (stated per module), name the site as the source of the
numbering.

---

Operated by a private individual; see the site's legal notice and privacy pages.
