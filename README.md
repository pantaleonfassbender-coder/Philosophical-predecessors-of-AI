# Calculemus — philosophical predecessors of AI

A research apparatus for the prehistory of the AI debate: the public-domain texts in which
reasoning first became reckoning, reckoning became algebra, algebra became a formal system —
together with the machines that made the idea tangible, and the philosophers who said it could
not be done. Built as a static site: paragraph-exact citation, cross-corpus concordance, no
tracking, no server functions.

The name is Leibniz's: when disputes arise, *Calculemus* — let us calculate.

## The programme

The corpus is built in stages along three lines. Status is tracked in `data/works.json` and on
the site's overview.

**The logic line** (direct ancestry of symbolic AI)

| Author | Text | Source | Status |
|---|---|---|---|
| Thomas Hobbes | *Leviathan* (1651), Introduction + Part I ch. I–V; later De Corpore I | Project Gutenberg #3207 (1651 spelling) | **shipped** |
| G. W. Leibniz | Anthology: ars combinatoria, characteristica / calculus ratiocinator fragments, binary arithmetic (1703), Monadology | Gerhardt (1875–90); Latta 1898 for English Monadology; working translations for the rest | planned |
| George Boole | *Laws of Thought* (1854), Preface + ch. I–III, XXII | Project Gutenberg #15114 (LaTeX), converted | **shipped** |
| Gottlob Frege | *Grundlagen der Arithmetik* (1884), *Über Sinn und Bedeutung* (1892), Begriffsschrift prose | 1879–92 originals (US-PD); working translations — no PD English exists | planned |

**The machine line**

| Author | Text | Source | Status |
|---|---|---|---|
| Blaise Pascal | Pensées, the arithmetical-machine fragment | French + Trotter (PD) | planned |
| Ada Lovelace | Notes on Menabrea's *Sketch of the Analytical Engine* (1843), incl. Note G | Taylor's Scientific Memoirs III | planned |
| W. S. Jevons | *On the Mechanical Performance of Logical Inference* (1870) | Phil. Trans. 160 | planned |
| C. S. Peirce | *Logical Machines* (1887) | American Journal of Psychology I (original printing) | planned |

**The counter-voices**

| Author | Text | Source | Status |
|---|---|---|---|
| René Descartes | *Discours de la méthode* (1637), Part V — the language test | French + PD English translation | planned |
| J. O. de La Mettrie | *L'Homme Machine* (1747) | French + the contemporary English translation of 1749 | planned |

Under consideration: a Ramon Llull prologue (Ars brevis selections) and Tractatus selections
(German + Ogden 1922, both pre-1930 US-PD).

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

Static site, no build step. `data/works.json` is the registry (three lines, status);
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
