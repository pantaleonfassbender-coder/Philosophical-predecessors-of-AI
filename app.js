/* Calculemus — router, data, views */
const D = { works: [], texts: {} };
const view = document.getElementById("view");

const esc = s => String(s ?? "").replace(/[&<>"']/g, m =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const el = h => { const t = document.createElement("template"); t.innerHTML = h.trim(); return t.content.firstElementChild; };
const LINIE = { logic: "The logic line", maschine: "The machine line", gegen: "The counter-voices" };
const LCOLOR = { logic: "var(--logic)", maschine: "var(--maschine)", gegen: "var(--gegen)" };

/* ------------------------------------------------------- citation grid */
/* Each shipped work defines how a unit is cited. */
const CITE = {
  hobbes: (sec, u) => {
    const rom = { intro: "Intro.", c1: "ch. I", c2: "ch. II", c3: "ch. III", c4: "ch. IV", c5: "ch. V" }[sec.id];
    return `Lev., ${rom} [${u.k}]`;
  },
  boole: (sec, u) => {
    const rom = { pref: "Pref.", c1: "I", c2: "II", c3: "III", c22: "XXII" }[sec.id];
    return u.art ? `LoT ${rom}, art. ${u.art}` : `LoT ${rom} [${u.k}]`;
  },
  descartes: (sec, u) => `Disc. V [${u.k}]`,
  leibniz: (sec, u) => ({ mon: `Mon. §${u.k}`, bin: `Arith. bin. [${u.k}]`,
    char: `GP VII [${u.k}]`, comb: `De arte comb. [${u.k}]` }[sec.id] || `[${u.n}]`),
  frege: (sec, u) => u.c || `[${u.n}]`,
  pascal: (sec, u) => `Pens. ${u.br} (Br.)`,
  jevons: (sec, u) => `MPL, art. ${u.art}`,
  peirce: (sec, u) => `LM [${u.n}]`,
  llull: (sec, u) => `AB [${u.n}]`,
  lamettrie: (sec, u) => `HM [${u.n}]`,
  kapp: (sec, u) => ({ vorwort: `PhT, Vorwort [${u.k}]`, c1: `PhT I [${u.k}]`, c2: `PhT II [${u.k}]`,
    c7: `PhT VII [${u.k}]`, c8: `PhT VIII [${u.k}]` }[sec.id] || `PhT [${u.n}]`),
  lovelace: (sec, u) => sec.id === "memoir" ? `Menabrea [${u.k}]` : `Note ${sec.id.slice(4)} [${u.k}]`,
};
const citeOf = (workId, sec, u) => (CITE[workId] || ((s, x) => `[${x.n}]`))(sec, u);

/* --------------------------------------------------------------- boot */
async function boot() {
  D.works = await fetch("data/works.json").then(r => r.json());
  const shipped = D.works.filter(w => w.status === "shipped");
  const res = await Promise.all(shipped.map(w => fetch(`data/${w.datei}.json`).then(r => r.json())));
  shipped.forEach((w, i) => D.texts[w.id] = res[i]);
  window.addEventListener("hashchange", route);
  route();
}
const ROUTES = {};
function route() {
  const h = (location.hash || "#/overview").slice(2).split("/");
  const name = h[0] || "overview";
  document.querySelectorAll("#nav a").forEach(a => a.classList.toggle("active", a.dataset.v === name));
  if (atlasStop) { atlasStop(); atlasStop = null; }
  view.innerHTML = ""; window.scrollTo(0, 0);
  (ROUTES[name] || viewOverview)(h.slice(1));
}

/* ============================================================ OVERVIEW */
function viewOverview() {
  const shipped = D.works.filter(w => w.status === "shipped").length;
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Research apparatus</span>
      <h1>Before the machines could speak, philosophers argued about them</h1>
      <p class="lede">The current debate about artificial intelligence — can machines think, understand,
      originate? — did not begin in 1956, nor in 1950. Its questions, and several of its best arguments,
      are three centuries older. This apparatus collects the public-domain sources of that prehistory in
      citable, searchable editions: the texts in which reasoning first became reckoning, reckoning became
      algebra, algebra became a formal system — together with the machines that made the idea tangible,
      and the philosophers who said it could not be done. It ends, deliberately, at the threshold of
      Turing.</p>
      <p class="fine">New here? The <a href="#/introduction">introductory essay</a> walks through the
      three lines, the argument that runs through them, and the way the apparatus is meant to be used.</p>
    </div>

    <div class="grid g3" style="margin-bottom:1.6rem">
      <div class="card linie-logic">
        <span class="tag" style="color:var(--logic)">The logic line</span>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">Llull's combinatorial wheels.
        Hobbes: reason is reckoning. Leibniz: a symbolic language and a calculus of thought.
        Boole: the laws of thought as algebra. Frege: the formal system itself. The direct
        ancestry of symbolic AI.</p>
      </div>
      <div class="card linie-maschine">
        <span class="tag" style="color:var(--maschine)">The machine line</span>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">Pascal's arithmetical machine,
        Lovelace's Notes on the Analytical Engine, Jevons's logical piano, Peirce on logical machines:
        where the idea met brass and cardboard — and met its first stated limits.</p>
      </div>
      <div class="card linie-gegen">
        <span class="tag" style="color:var(--gegen)">The counter-voices</span>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">Descartes's language test, which no
        machine was to pass; Leibniz's mill; Lovelace's objection; La Mettrie's radical retort that man
        himself is the machine — and Kapp's reversal: the machine is a projection of man. The arguments
        today's debate keeps rediscovering.</p>
      </div>
    </div>

    <h2>The corpus — ${shipped} of ${D.works.length} modules shipped, built in stages</h2>
    <div class="grid g2" id="worklist"></div>

    <p class="fine" style="margin-top:1.6rem">Every text is public domain in the United States; every
    paragraph carries a stable citation; the concordance searches all shipped texts at once. Where no
    public-domain English translation exists, this site supplies its own working translation, marked as
    such. The full account is on the <a href="#/method">method page</a>.</p>
  </div>`));
  const wl = view.querySelector("#worklist");
  for (const w of D.works) wl.append(workCard(w));
}

function workCard(w) {
  const open = w.status === "shipped";
  const card = el(`<div class="workcard card linie-${w.linie} ${open ? "" : "dim"}">
    <div style="display:flex;gap:.6rem;align-items:baseline;justify-content:space-between;flex-wrap:wrap">
      <strong style="font-family:var(--serif)">${esc(w.autor)}</strong>
      <span class="status ${w.status}">${w.status}</span>
    </div>
    <p class="fine" style="margin:.1rem 0 .3rem">${esc(w.leben)} · ${esc(w.sprachen)}</p>
    <h3 style="margin:.1rem 0 .3rem;font-size:1rem">${esc(w.titel)}</h3>
    <p style="font-size:.88rem;color:var(--fg2);margin:0">${esc(w.claim)}</p>
    ${open ? "" : `<p class="fine" style="margin:.4rem 0 0">Planned: ${esc(w.geplant || "")}</p>`}
  </div>`);
  if (open) card.onclick = () => location.hash = `#/works/${w.id}`;
  return card;
}

/* =============================================================== WORKS */
function viewWorks(args) {
  if (args && args[0]) return workReader(args[0], args[1]);
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">The corpus</span>
      <h1>Works</h1>
      <p class="lede">Three lines, one prehistory. Shipped modules open as paragraph-exact readers;
      the rest of the programme is listed with its sources and will follow in stages.</p>
    </div>
    ${Object.entries(LINIE).map(([k, t]) => `
      <h2 style="color:${LCOLOR[k]}">${t}</h2>
      <div class="grid g2" data-l="${k}"></div>`).join("")}
  </div>`));
  for (const w of D.works)
    view.querySelector(`[data-l="${w.linie}"]`).append(workCard(w));
}

function workReader(id, secId) {
  const w = D.works.find(x => x.id === id);
  const t = D.texts[id];
  if (!w || !t) { location.hash = "#/works"; return; }
  if (secId) return sectionReader(w, t, secId);
  view.append(el(`<div>
    <p class="fine"><a href="#/works">← All works</a></p>
    <div class="viewhead">
      <span class="tag" style="color:${LCOLOR[w.linie]}">${esc(w.autor)} · ${esc(String(t.jahr))}</span>
      <h1>${esc(t.titel)}</h1>
      <p class="lede">${esc(w.claim)}</p>
    </div>
    <div class="grid g2" id="toc"></div>
    <p class="fine" style="margin-top:1.2rem">${esc(t.quelle)} ${esc(t.hinweis || "")}</p>
  </div>`));
  const toc = view.querySelector("#toc");
  for (const s of t.sections) {
    const card = el(`<div class="workcard card linie-${w.linie}">
      <div style="display:flex;gap:.6rem;align-items:baseline;justify-content:space-between">
        <h3 style="margin:0;font-size:1rem">${esc(s.titel)}</h3>
        <span class="fine">${s.units.length} ¶</span></div>
    </div>`);
    card.onclick = () => location.hash = `#/works/${id}/${s.id}`;
    toc.append(card);
  }
}

function sectionReader(w, t, secId) {
  secId = secId.split("@")[0];
  const i = t.sections.findIndex(s => s.id === secId);
  if (i < 0) { location.hash = `#/works/${w.id}`; return; }
  const s = t.sections[i];
  const prev = t.sections[(i - 1 + t.sections.length) % t.sections.length];
  const next = t.sections[(i + 1) % t.sections.length];
  view.append(el(`<div>
    <p class="fine"><a href="#/works/${w.id}">← ${esc(w.kurz)}</a> ·
      <a href="#/works/${w.id}/${prev.id}">${esc(prev.titel.split('.')[0])}</a> ·
      <a href="#/works/${w.id}/${next.id}">${esc(next.titel.split('.')[0])}</a></p>
    <div class="viewhead">
      <span class="tag" style="color:${LCOLOR[w.linie]}">${esc(w.autor)} · ${esc(String(t.jahr))}</span>
      <h1 style="font-size:1.4rem">${esc(s.titel)}</h1>
      <p class="fine">${s.units.length} paragraphs · cited as shown on each paragraph</p>
    </div>
    <div id="langbar"></div>
    <div id="body"></div>
    <p class="fine">${esc(t.quelle)} ${esc(t.hinweis || "")}</p>
  </div>`));
  const bilingual = s.units.some(u => u.orig);
  const render = () => {
    view.querySelector("#body").innerHTML = s.units.map(u => unitHtml(w, s, u)).join("");
  };
  if (bilingual) {
    const bar = el(`<div class="toolbar" style="margin-bottom:1rem">
      ${["en", "orig", "both"].map(m => `<button class="chip ${LANG === m ? "on" : ""}" data-m="${m}">
        ${{ en: "English", orig: "Original", both: "Both" }[m]}</button>`).join(" ")}</div>`);
    bar.querySelectorAll("[data-m]").forEach(b => b.onclick = () => {
      LANG = b.dataset.m;
      bar.querySelectorAll("[data-m]").forEach(x => x.classList.toggle("on", x.dataset.m === LANG));
      render();
    });
    view.querySelector("#langbar").append(bar);
  }
  render();
  const anchor = (location.hash.split("@")[1] || "");
  if (anchor) document.getElementById("u" + anchor)?.scrollIntoView();
}

let LANG = "en"; /* language mode for bilingual readers: en | orig | both */

function unitHtml(w, s, u, hl) {
  const label = u.label ? `<p class="ulabel">${esc(u.label)}</p>` : "";
  const mk = raw => {
    let txt = esc(raw);
    if (hl) {
      const rx = new RegExp(hl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
      txt = txt.replace(rx, m => `<mark>${m}</mark>`);
    }
    return txt;
  };
  let body;
  if (!u.orig) body = `<p class="readable">${mk(u.txt)}</p>`;
  else if (LANG === "orig") body = `<p class="readable orig">${mk(u.orig)}</p>`;
  else if (LANG === "both") body =
    `<p class="readable orig" style="color:var(--fg2)">${mk(u.orig)}</p><p class="readable">${mk(u.txt)}</p>`;
  else body = `<p class="readable">${mk(u.txt)}</p>`;
  const note = u.note ? `<p class="fine" style="color:var(--acc)">${esc(u.note)}</p>` : "";
  return `<div class="unit" id="u${u.n}">
    <div style="display:flex;gap:.6rem;align-items:baseline"><span class="cite">${esc(citeOf(w.id, s, u))}</span></div>
    ${label}${body}${note}</div>`;
}

/* ======================================================== INTRODUCTION */
/* The introductory essay (data/introduction.json, built from the author's
   manuscript by tools/build-introduction.py). Italic markers *...* become
   <em>; the first mention of each work in the corpus links to its reader,
   so the essay doubles as a guided entrance. */
let INTRO = null;
const INTRO_LINKS = [
  ["Ars brevis", "#/works/llull"],
  ["Leviathan", "#/works/hobbes"],
  ["De arte combinatoria", "#/works/leibniz/comb"],
  ["arithmétique binaire", "#/works/leibniz/bin"],
  ["Monadology", "#/works/leibniz/mon"],
  ["Laws of Thought", "#/works/boole"],
  ["Begriffsschrift", "#/works/frege/bs"],
  ["Grundlagen der Arithmetik", "#/works/frege/gl"],
  ["Über Sinn und Bedeutung", "#/works/frege/sb"],
  ["Pensées", "#/works/pascal"],
  ["Note G", "#/works/lovelace/noteG"],
  ["On the Mechanical Performance of Logical Inference", "#/works/jevons"],
  ["Peirce (1887)", "#/works/peirce"],
  ["Discours de la méthode", "#/works/descartes"],
  ["L’Homme Machine", "#/works/lamettrie"],
  ["eleven modules", "#/works"],
  ["concordance", "#/concordance"],
  ["term atlas", "#/atlas"],
];
const em = s => esc(s).replace(/\*([^*]+)\*/g, "<em>$1</em>");

async function viewIntroduction() {
  if (!INTRO) INTRO = await fetch("data/introduction.json").then(r => r.json());
  const used = new Set();
  const fmt = s => {
    let h = em(s);
    for (const [phrase, href] of INTRO_LINKS) {
      if (used.has(phrase)) continue;
      const i = h.indexOf(phrase);
      if (i < 0) continue;
      used.add(phrase);
      h = h.slice(0, i) + `<a href="${href}">${phrase}</a>` + h.slice(i + phrase.length);
    }
    return h;
  };
  view.append(el(`<div class="essay">
    <div class="viewhead">
      <span class="tag">Introductory essay</span>
      <h1>${esc(INTRO.titel)}</h1>
      <p class="fine">${esc(INTRO.autor)} · ${esc(INTRO.datum)} · editorial matter of this site, CC BY 4.0</p>
      <p class="fine" style="max-width:46rem">${em(INTRO.note)
        .replace(/https?:\/\/[^\s]+/g, u => `<a href="${u}">${u}</a>`)}</p>
    </div>
    ${INTRO.abschnitte.map(a => `
      ${a.titel ? `<h2>${esc(a.titel)}</h2>` : ""}
      ${a.paras.map(p => `<p class="readable">${fmt(p)}</p>`).join("")}`).join("")}
    <div class="toolbar" style="margin:1.8rem 0">
      <a class="chip" href="#/works">Browse the works</a>
      <a class="chip" href="#/concordance">Search the concordance</a>
      <a class="chip" href="#/atlas">Open the atlas</a>
    </div>
    <div class="panel"><h2 style="margin-top:0">References</h2>
      <div class="refs">${INTRO.referenzen.map(r => `<p>${em(r)}</p>`).join("")}</div>
    </div>
  </div>`));
}

/* ========================================================= CONCORDANCE */
function viewConcordance() {
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Cross-corpus search</span>
      <h1>Concordance</h1>
      <p class="lede">Keyword in context across every shipped text, each hit resolved to its citation.
      New modules join the search as they ship.</p>
    </div>
    <div class="toolbar">
      <input class="grow" id="q" type="search" placeholder="Search word or phrase …">
      <button class="primary" id="go">Search</button>
    </div>
    <div id="out"></div>
    <div class="card" style="margin-top:1.4rem"><span class="tag">Starting points</span>
      <p style="margin:.5rem 0 0">${["reckoning", "reason", "machine", "signs", "language",
        "thought", "computation", "mind", "understanding", "engine"]
        .map(x => `<button class="chip" data-t="${x}">${x}</button>`).join(" ")}</p></div>
  </div>`));
  const out = view.querySelector("#out");
  const q = view.querySelector("#q");
  function run() {
    const term = q.value.trim();
    out.innerHTML = "";
    if (term.length < 3) { out.append(el(`<p class="fine">Type at least three characters.</p>`)); return; }
    const rx = new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
    let hits = 0;
    for (const w of D.works.filter(x => x.status === "shipped")) {
      const t = D.texts[w.id];
      for (const s of t.sections) for (const u of s.units) {
        rx.lastIndex = 0;
        let src = u.txt, m = rx.exec(u.txt);
        if (!m && u.orig) { rx.lastIndex = 0; m = rx.exec(u.orig); src = u.orig; }
        if (!m) continue;
        hits++;
        if (hits > 200) break;
        const a = Math.max(0, m.index - 90), b = Math.min(src.length, m.index + term.length + 130);
        const ctx = (a > 0 ? "…" : "") + src.slice(a, b) + (b < src.length ? "…" : "");
        out.append(el(`<div class="unit">
          <div style="display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap">
            <a class="cite" href="#/works/${w.id}/${s.id}@${u.n}">${esc(citeOf(w.id, s, u))}</a>
            <span class="fine">${esc(w.autor)}</span></div>
          <p class="readable" style="font-size:.95rem">${esc(ctx).replace(rx, x => `<mark>${x}</mark>`)}</p>
        </div>`));
      }
    }
    out.prepend(el(`<p class="fine">${hits}${hits > 200 ? "+ (first 200 shown)" : ""} hits.</p>`));
  }
  view.querySelector("#go").onclick = run;
  q.addEventListener("keydown", e => { if (e.key === "Enter") run(); });
  view.querySelectorAll("[data-t]").forEach(b => b.onclick = () => { q.value = b.dataset.t; run(); });
}

/* ============================================================== METHOD */
function viewMethod() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Transparency</span>
      <h1>Method, sources and limits</h1>
      <p class="lede">What this site is, where its texts come from, and what its editions do and do not claim.</p></div>

    <div class="panel"><h2>The rights position</h2>
      <p class="readable">Everything shipped here is in the United States public domain, and the site is
      operated from the United States, whose rules govern its edition choices. The original works qualify
      by age: Hobbes's Leviathan (1651), Boole's Laws of Thought (1854), and the further editions named
      per module. For works written in Latin, French or German, public-domain English translations are
      used where they exist (they are named per module); where none exists — notably for Frege and for
      Leibniz's specifically computational texts — this site supplies its own working translations, made
      directly from the originals, consulting no copyrighted translation, and dedicated to the public
      domain. They are labelled as unofficial throughout: cite the original.</p>
      <p class="readable">The boundary of the site is itself a rights fact: Turing's “On Computable
      Numbers” (1936) and “Computing Machinery and Intelligence” (1950) remain in copyright in the United
      States (until roughly 2032 and 2046 respectively), as do the classic mid-century AI papers. The
      apparatus therefore ends, deliberately, at the threshold — the last texts it can carry in full are
      those of the generation before the machines began to answer back.</p>
    </div>

    <div class="panel"><h2>Editions and segmentation</h2>
      <p class="readable"><strong>Hobbes.</strong> Leviathan, Introduction and Part I chapters I–V, from
      the Project Gutenberg transcription (#3207) of the 1651 London printing, whose spelling is
      preserved. The marginal side-notes of 1651 are kept as paragraph labels, and the paragraphs are
      numbered per chapter by this site (the 1651 printing numbers nothing); the citation form is
      <span class="mono">Lev., ch. V [k]</span>.</p>
      <p class="readable"><strong>Boole.</strong> An Investigation of the Laws of Thought, Preface and
      chapters I–III and XXII — the philosophical frame of the book — from the Project Gutenberg LaTeX
      transcription (#15114) of the 1854 London edition, converted to running text for this site.
      Boole's own article numbers within each chapter are kept and used for citation
      (<span class="mono">LoT II, art. 5</span>); unnumbered paragraphs continue the preceding article.
      Inline formulas are rendered as plain text (× for multiplication, / for fractions); displayed
      equations are folded into their paragraph; Boole's footnotes are omitted. Readers working on the
      symbolic detail should consult the printed edition — this module serves the argument, not the
      calculus.</p>
      <p class="readable"><strong>Descartes.</strong> Discours de la méthode, Part V, bilingual: the
      French text follows the Cousin edition's orthography (Project Gutenberg #13846), the English is
      John Veitch's public-domain translation (#59). The ten paragraph units follow the French
      paragraphing; where Veitch merges French paragraphs, his text has been divided at sentence
      boundaries to restore the alignment. Citation form <span class="mono">Disc. V [k]</span>.</p>
      <p class="readable"><strong>La Mettrie.</strong> L'Homme Machine (1747), bilingual and complete:
      the French text and Gertrude C. Bussey's English translation of 1912 (Open Court; Project
      Gutenberg #52090), aligned paragraph-for-paragraph — where the 1912 translation merges French
      paragraphs, they are shown merged. An editorial finding of this edition: the 1912 translation
      <em>silently omits seven paragraphs</em> of the French — those on pregnancy, continence, arousal,
      maternal impressions, and La Mettrie's spermist embryology of generation. This site restores all
      seven with its own working translations, marked in place; the omissions are bowdlerization, not
      textual variants. The four part titles are editorial, as is the continuous paragraph numbering;
      citation form <span class="mono">HM [n]</span>.</p>
      <p class="readable"><strong>Lovelace.</strong> Menabrea's Sketch of the Analytical Engine in Ada
      Lovelace's translation, with all of her Notes A–G, from Taylor's Scientific Memoirs vol. III
      (1843), pp. 666–731, digitized from the Internet Archive scan of the volume. The 1843 volume
      survives here only as rough OCR: the prose has been emended by hand against the sense of the
      passage (and, for the well-known passages, against the received text), but the displayed formulae
      and tables of the mathematical Notes cannot be carried by the scan — they are replaced by
      <span class="mono">[formula omitted]</span> and <span class="mono">[table omitted]</span> markers,
      and a few passages too damaged to restore are marked in place. For the mathematics, consult the
      printed original; the argumentative prose, including the whole of Note G, is complete. Footnotes
      are omitted. Citation forms <span class="mono">Menabrea [k]</span> and
      <span class="mono">Note G [k]</span>.</p>
      <p class="readable"><strong>Leibniz.</strong> An anthology in four parts. The Monadology (1714),
      complete in its 90 sections, bilingual: the French after the Project Gutenberg transcription
      #17641 (the 1909 Piat print, his apparatus omitted), the English being Robert Latta's
      public-domain translation of 1898, taken from the Wikisource transcription without his notes —
      the one part of this module whose English carries scholarly authority. The Explication de
      l'arithmétique binaire (1703) complete, French after Gerhardt (Mathematische Schriften VII,
      via the French Wikisource transcription), with a working translation; its tables are replaced
      by markers. The characteristica fragments — the alphabet of human thoughts, the calculemus
      passages of GP VII 200 and GP VII 125, with the manuscript's marginal note “Cum DEUS calculat
      … fit mundus” — and two selections from the De arte combinatoria of 1666, including Leibniz's
      explicit debt to Hobbes (“omne opus mentis nostrae esse computationem”), are given in Latin
      after Gerhardt's edition (OCR of the Internet Archive scans, emended by hand) with working
      translations. Citation forms <span class="mono">Mon. §17</span>,
      <span class="mono">Arith. bin. [n]</span>, <span class="mono">GP VII [k]</span>,
      <span class="mono">De arte comb. [k]</span>.</p>
      <p class="readable"><strong>Frege.</strong> Three texts, German with working translations —
      no public-domain English translation of any of them exists, so the English here is this
      site's own throughout, and carries no scholarly authority: cite the German. „Bedeutung“ is
      rendered “reference”, „Sinn“ “sense”, following no copyrighted translation. The
      Begriffsschrift is represented by its complete Vorwort (Halle 1879, from the Internet
      Archive scan, OCR emended) — the prose limit announced in advance stands: the
      two-dimensional notation cannot honestly be reconstructed from OCR and is not reproduced.
      The Grundlagen der Arithmetik (1884, from the Project Gutenberg transcription #48312) is
      given in selections chosen for the argument: the complete Einleitung with the three
      Grundsätze, §§ 1–4 (the task), §§ 87–91 (arithmetic as further-developed logic, the
      correction of Kant) and §§ 106–109 (the retrospect). Über Sinn und Bedeutung (Zeitschrift
      für Philosophie und philosophische Kritik 100, 1892, from the Deutsches Textarchiv
      transcription of the journal printing) is complete, with all of Frege's own footnotes kept
      in place — including the Aristotle footnote. Citation forms
      <span class="mono">BS, Vorwort [k]</span>, <span class="mono">GL, § 87</span>,
      <span class="mono">SuB [n]</span> (editorial paragraph numbers).</p>
      <p class="readable"><strong>Pascal.</strong> Five fragments of the Pensées chosen for the
      argument — the arithmetical machine (Br. 340) with its rider on will, thought as the mark of
      the human (339, 346), the thinking reed (347), and “we are as much automaton as mind” (252) —
      bilingual: French after Brunschvicg's edition via the French Wikisource transcription, English
      in W. F. Trotter's public-domain translation (Project Gutenberg #18269). Cited by Brunschvicg
      number: <span class="mono">Pens. 340 (Br.)</span>.</p>
      <p class="readable"><strong>Jevons.</strong> “On the Mechanical Performance of Logical
      Inference” (read January 1870), in selections keyed to Jevons's own article numbers
      (<span class="mono">MPL, art. 56</span>): articles 1–13 (the programme — abacus, Pascal,
      Babbage, the reform of logic, Boole), 17 and 20–21 (nothing mysterious in the symbols; the
      Abecedarium), 31–32 (the machine, abridged as marked), and 55–56 (Jevons's own sober
      assessment: the chief importance of the machine “is of a purely theoretical kind”). Text from
      the 1890 reprint in Pure Logic and Other Minor Works (Internet Archive scan, OCR emended);
      the omitted articles carry the worked equations and the mechanical detail, and the plates are
      not reproduced.</p>
      <p class="readable"><strong>Peirce.</strong> “Logical Machines”, complete, from the original
      printing in the American Journal of Psychology I (November 1887) — deliberately not from the
      Collected Papers of 1931 ff., which remain in copyright. Peirce's two footnotes are kept
      (one credits “Mrs. Franklin's system” — Christine Ladd-Franklin); his formula displays are
      kept inline and emended from the OCR; the machine-face figure is omitted; the print order of
      two passages interleaved by the scan's page layout has been restored. Citation form
      <span class="mono">LM [n]</span> (editorial paragraph numbers).</p>
      <p class="readable"><strong>Llull.</strong> A prologue module, not an edition: the invocation
      and prologue of the Ars brevis (1308), the alphabet B–K, the first figure, and the fourth
      figure — the three rotating wheels that generate 252 combinatorial chambers, the device
      Leibniz expressly named as the inspiration of his ars combinatoria (the connection stands in
      this corpus: De arte combinatoria is in the Leibniz module). Latin after the Strasbourg
      Zetzner edition of 1617 (Internet Archive scan), whose early-modern typography defeats OCR;
      the text has therefore been emended by hand against the standard textual tradition, and the
      modern critical edition (ROL), which remains in copyright, was not used. The English is a
      working translation made for this site. Citation form <span class="mono">AB [n]</span>.</p>
      <p class="readable"><strong>Kapp.</strong> Grundlinien einer Philosophie der Technik (Braunschweig
      1877), in selections chosen for the argument: excerpts of the Vorwort (including the declaration
      that man “will never confuse himself with a technical contrivance”), the close of chapter I, the
      core of chapter II — the coinage of “Organprojection”, with the doxographic survey of the
      projection concept omitted as marked — and excerpts of chapters VII (the steam-engine, Helmholtz
      on the borrowed concept of machine work, the “Maschinenwerdung des Menschen”) and VIII (the
      telegraph/nervous-system parallel, and the tool whose materials come “from the workshop of the
      mind itself”). German text from the Internet Archive/MDZ scan of the first edition — an Antiqua
      printing, so the OCR was serviceable; every damaged passage was verified letter-by-letter against
      the page images of the scan (the coinage passage itself crosses a page foot the OCR destroys).
      The 1877 orthography is preserved. No public-domain English translation exists; the English is
      this site's working translation, and the 2018 translation was not consulted. Citation forms
      <span class="mono">PhT, Vorwort [k]</span>, <span class="mono">PhT II [k]</span> etc.
      (editorial paragraph numbers per chapter).</p>
      <p class="readable"><strong>The Atlas.</strong> The Atlas view is a co-occurrence network: the
      leading content terms of the shipped English texts, linked when they appear in the same
      paragraph, weighted by pointwise mutual information, laid out by a small force simulation in the
      browser. It is a finding aid, not a semantic claim — the network is precomputed by an open script
      in the repository (<span class="mono">tools/build-network.py</span>), and every node resolves
      back to citable paragraphs.</p>
    </div>

    <div class="panel"><h2>The programme</h2>
      <p class="readable">The corpus was built in stages along three lines: the logic line (the
      Llull prologue, Hobbes, the Leibniz anthology, Boole, Frege), the machine line (Pascal's
      fragments, Lovelace's Notes of 1843 with Menabrea's Sketch, Jevons's memoir of 1870,
      Peirce's “Logical Machines” of 1887), and the counter-voices (Descartes's Discours Part V
      and La Mettrie's L'Homme Machine, both bilingual, joined in 2026 by Kapp's Grundlinien of
      1877) — twelve modules shipped. A Tractatus module, once under consideration, has been
      dropped: the corpus ends where the formal-system line hands over to the twentieth century.
      What the corpus cannot contain, and why, is the subject of the <a href="#/coda">coda</a>.</p>
    </div>

    <div class="panel"><h2>Known limits</h2>
      <ul style="color:var(--fg2);font-size:.93rem">
        <li>These are reading editions built from trusted transcriptions (Project Gutenberg) or from OCR
          of the original printings; residual transcription errors are possible and corrections are
          welcome via the repository.</li>
        <li>Paragraph numbering is editorial wherever the original printing numbers nothing; the method
          notes say so per work. Citations of this site should name it as the source of the numbering.</li>
        <li>The site presents selections chosen for the AI-prehistory argument, not complete works;
          what was selected and why is stated per module.</li>
        <li>Working translations, where they appear, are machine-generated for this site and carry no
          scholarly authority.</li>
      </ul>
      <p class="fine">Repository: <a href="https://github.com/pantaleonfassbender-coder/Philosophical-predecessors-of-AI">github.com/pantaleonfassbender-coder/Philosophical-predecessors-of-AI</a></p>
    </div>
  </div>`));
}

/* =============================================================== ATLAS */
/* Co-occurrence network of the leading terms across all shipped texts.
   Data precomputed by tools/build-network.py into data/network.json. */
let NET = null, atlasStop = null;

async function viewAtlas() {
  if (!NET) NET = await fetch("data/network.json").then(r => r.json());
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Term network</span>
      <h1>Atlas</h1>
      <p class="lede">The ${NET.nodes.length} leading content terms of the corpus, linked where they
      occur in the same paragraph. Colour is the line whose texts use the term most
      (<span style="color:var(--logic)">logic</span> ·
      <span style="color:var(--maschine)">machine</span> ·
      <span style="color:var(--gegen)">counter-voices</span>); size is frequency.
      Click a term for its neighbours and citations.</p></div>
    <div class="toolbar">
      <label class="fine" for="dens">Density</label>
      <select id="dens">
        <option value="140">sparse</option>
        <option value="260" selected>medium</option>
        <option value="420">dense</option>
      </select>
      <span class="fine" id="atlasinfo"></span>
    </div>
    <div class="card" style="padding:0;overflow:hidden"><canvas id="cv" style="width:100%;display:block;cursor:pointer"></canvas></div>
    <div id="sel"></div>
    <div class="card" style="margin-top:1.2rem"><span class="tag">Bridge terms</span>
      <p style="margin:.5rem 0 0" class="readable" style="font-size:.9rem">Terms carried by four or
      more of the works — the shared vocabulary in which the lines argue with each other:
      ${NET.bridges.map(b => `<button class="chip" data-b="${esc(b)}">${esc(b)}</button>`).join(" ")}</p></div>
  </div>`));
  const cv = view.querySelector("#cv");
  const selBox = view.querySelector("#sel");
  const densSel = view.querySelector("#dens");
  const W = Math.min(view.clientWidth || 900, 980), H = Math.max(460, Math.round(W * 0.62));
  const dpr = window.devicePixelRatio || 1;
  cv.width = W * dpr; cv.height = H * dpr; cv.style.height = H + "px";
  const cx = cv.getContext("2d"); cx.scale(dpr, dpr);

  const nodes = NET.nodes.map(n => ({ ...n,
    x: W / 2 + (Math.random() - 0.5) * W * 0.8, y: H / 2 + (Math.random() - 0.5) * H * 0.8,
    vx: 0, vy: 0, r: 3 + Math.sqrt(n.f) * 0.9 }));
  const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
  let edges = [], selected = null, tick = 0;

  function setDensity() {
    edges = NET.edges.slice(0, +densSel.value).map(e => ({ ...e, a: byId[e.s], b: byId[e.t] }))
      .filter(e => e.a && e.b);
    view.querySelector("#atlasinfo").textContent =
      `${nodes.length} terms · ${edges.length} links · from ${NET.n_units} paragraphs`;
    tick = 0;
  }
  setDensity();
  densSel.onchange = setDensity;

  function step() {
    /* simple force layout: pairwise repulsion, spring on edges, center pull */
    for (const n of nodes) { n.fx = 0; n.fy = 0; }
    for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      let dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy + 40;
      const f = 1400 / d2;
      const d = Math.sqrt(d2);
      dx /= d; dy /= d;
      a.fx += dx * f; a.fy += dy * f; b.fx -= dx * f; b.fy -= dy * f;
    }
    for (const e of edges) {
      let dx = e.b.x - e.a.x, dy = e.b.y - e.a.y;
      const d = Math.sqrt(dx * dx + dy * dy) || 1;
      const want = 60 + 700 / (e.w + 4);
      const f = (d - want) * 0.004 * Math.min(e.w, 6);
      dx /= d; dy /= d;
      e.a.fx += dx * f * d * 0.02; e.a.fy += dy * f * d * 0.02;
      e.b.fx -= dx * f * d * 0.02; e.b.fy -= dy * f * d * 0.02;
    }
    for (const n of nodes) {
      n.fx += (W / 2 - n.x) * 0.004; n.fy += (H / 2 - n.y) * 0.004;
      n.vx = (n.vx + n.fx) * 0.82; n.vy = (n.vy + n.fy) * 0.82;
      n.x += n.vx; n.y += n.vy;
      n.x = Math.max(14, Math.min(W - 14, n.x)); n.y = Math.max(14, Math.min(H - 14, n.y));
    }
  }

  const COLOR = { logic: "#6fa8dc", maschine: "#d9a441", gegen: "#c47a6d" };
  function draw() {
    cx.clearRect(0, 0, W, H);
    const neigh = new Set();
    if (selected) for (const e of edges) {
      if (e.a === selected) neigh.add(e.b);
      if (e.b === selected) neigh.add(e.a);
    }
    for (const e of edges) {
      const on = selected && (e.a === selected || e.b === selected);
      cx.strokeStyle = on ? "rgba(217,164,65,.55)" : "rgba(160,160,180,.13)";
      cx.lineWidth = on ? 1.4 : Math.min(1, 0.3 + e.w * 0.05);
      cx.beginPath(); cx.moveTo(e.a.x, e.a.y); cx.lineTo(e.b.x, e.b.y); cx.stroke();
    }
    for (const n of nodes) {
      const dimmed = selected && n !== selected && !neigh.has(n);
      cx.globalAlpha = dimmed ? 0.25 : 1;
      cx.fillStyle = COLOR[n.linie];
      cx.beginPath(); cx.arc(n.x, n.y, n.r, 0, 7); cx.fill();
      if (n === selected) { cx.strokeStyle = "#fff"; cx.lineWidth = 1.5; cx.stroke(); }
      if (!dimmed && (n.f > 25 || n === selected || neigh.has(n))) {
        cx.fillStyle = "rgba(233,230,224,.92)";
        cx.font = (n === selected ? "600 " : "") + "11px system-ui, sans-serif";
        cx.textAlign = "center";
        cx.fillText(n.id, n.x, n.y - n.r - 4);
      }
      cx.globalAlpha = 1;
    }
  }

  let raf;
  function loop() {
    if (tick < 260) { step(); tick++; }
    draw();
    raf = requestAnimationFrame(loop);
  }
  loop();
  atlasStop = () => cancelAnimationFrame(raf);

  function select(n) {
    selected = n;
    selBox.innerHTML = "";
    if (!n) return;
    const co = edges.filter(e => e.a === n || e.b === n)
      .map(e => ({ o: e.a === n ? e.b : e.a, c: e.c })).sort((a, b) => b.c - a.c).slice(0, 14);
    const wk = Object.entries(n.works).sort((a, b) => b[1] - a[1]);
    selBox.append(el(`<div class="card" style="margin-top:1.2rem">
      <div style="display:flex;gap:.8rem;align-items:baseline;flex-wrap:wrap">
        <h3 style="margin:0;color:${COLOR[n.linie]}">${esc(n.id)}</h3>
        <span class="fine">${n.f} paragraphs · in ${n.spread} of ${D.works.filter(w => w.status === "shipped").length} works</span></div>
      <p class="fine" style="margin:.4rem 0">${wk.map(([id, c]) => {
        const w = D.works.find(x => x.id === id);
        return `${esc(w ? w.kurz : id)}: ${c}`; }).join(" · ")}</p>
      <p style="margin:.4rem 0 0">${co.map(x =>
        `<button class="chip" data-b="${esc(x.o.id)}">${esc(x.o.id)} <span class="fine">${x.c}</span></button>`).join(" ")}</p>
      <p style="margin:.6rem 0 0">${n.cites.map(([wid, sid, un]) => {
        const w = D.works.find(x => x.id === wid);
        const t = D.texts[wid];
        const s = t && t.sections.find(x => x.id === sid);
        const u = s && s.units.find(x => x.n === un);
        return u ? `<a class="cite" href="#/works/${wid}/${sid}@${un}">${esc(citeOf(wid, s, u))}</a>` : "";
      }).join(" ")}</p>
    </div>`));
    selBox.querySelectorAll("[data-b]").forEach(b => b.onclick = () => select(byId[b.dataset.b]));
  }

  cv.onclick = ev => {
    const r = cv.getBoundingClientRect();
    const x = (ev.clientX - r.left) * (W / r.width), y = (ev.clientY - r.top) * (H / r.height);
    let best = null, bd = 400;
    for (const n of nodes) {
      const d = (n.x - x) ** 2 + (n.y - y) ** 2;
      if (d < bd && d < (n.r + 10) ** 2) { best = n; bd = d; }
    }
    select(best);
  };
  view.querySelectorAll("[data-b]").forEach(b => b.onclick = () => select(byId[b.dataset.b]));
}

/* ============================================================ PRIVACY */
function viewPrivacy() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Privacy</span>
      <h1>Privacy notice</h1>
      <p class="lede">Stated at the level of detail at which it is actually true.</p></div>
    <div class="panel"><h2>Who is responsible</h2>
      <p class="readable">This site is operated by a private individual from the United States; the
      details are in the <a href="#/imprint">legal notice</a>. It is a personal research project, not
      operated on behalf of any institution, and no data from it is passed to anyone.</p>
      <p class="readable">Because the site is reachable from the European Economic Area, this notice is
      written to satisfy the General Data Protection Regulation as well as United States law. Where the
      GDPR applies to a reader, the operator is the controller within the meaning of Article 4(7).</p></div>
    <div class="panel"><h2>What this site is, technically</h2>
      <p class="readable">A set of static files and nothing else: no server functions, no accounts, no
      forms, no newsletter. The site sets <strong>no cookies whatsoever</strong> and uses no analytics,
      advertising or third-party services of any kind; all fonts and scripts are served from this site
      itself. Opening any page therefore contacts exactly one host: the one in your address bar. Search
      runs entirely in your browser; nothing you type is transmitted anywhere.</p></div>
    <div class="panel"><h2>Server logs</h2>
      <p class="readable">The site is hosted by Netlify. Like any web host, Netlify's infrastructure
      records the requests it serves — typically IP address, timestamp, requested URL, HTTP status,
      transferred bytes, user-agent and referrer. This is technically unavoidable in delivering a
      website and is the only server-side collection that takes place; the operator does not analyse it.
      Where the GDPR applies, the legal basis is Article 6(1)(f) — the legitimate interest in delivering
      a functioning, secure website. Retention follows Netlify's own periods. The site is operated and
      hosted in the United States; for readers in the EEA this means request data are processed outside
      the EEA.</p></div>
    <div class="panel"><h2>Your rights</h2>
      <p class="readable">Where the GDPR applies, readers have the rights of access, rectification,
      erasure, restriction, objection and data portability (Articles 15–21) and the right to complain to
      a supervisory authority (Article 77). Since this site stores no personal data of its own, such
      requests will usually concern Netlify's logs; the operator will assist. Contact: the address in
      the <a href="#/imprint">legal notice</a>.</p></div>
  </div>`));
}

/* =============================================================== CODA */
/* Editorial closing note: what this anthology cannot contain, and why.
   Editorial matter, CC BY 4.0. */
function viewCoda() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag" style="color:var(--gegen)">Editorial</span>
      <h1>After the threshold</h1>
      <p class="lede">A coda on what this anthology cannot contain — and on the difference between
      an anthology and a quarry.</p></div>

    <div class="panel"><h2>An anthology, not a quarry</h2>
      <p class="readable">This apparatus carries extraction tools: a concordance that cuts across
      twelve works, an atlas that dissolves them into term co-occurrences. Used alone, such tools
      treat philosophy as a quarry — material to be broken out of context and carried off. But the
      direction of this site runs the other way. Every concordance hit and every atlas node resolves
      into a full paragraph, inside a whole section, inside a work that was chosen and ordered for a
      stated argument; every citation grid points away from this site, to the printed originals; the
      <a href="#/introduction">introduction</a> speaks in a named author's voice; what was selected
      and why is declared per module, what was altered is disclosed on the
      <a href="#/method">method page</a>, and even what was considered and dropped is on record. That
      is what makes a collection an anthology: it owns its selections — and its omissions.</p>
    </div>

    <div class="panel"><h2>What is missing, and why</h2>
      <p class="readable">The corpus ends, of legal necessity, at the threshold of Turing. But the
      same rights boundary excludes the twentieth century's strongest counter-voices. Martin Buber's
      <em>Ich und Du</em> (1923) grounds meaning in the dialogical encounter — the I–Thou that is a
      relation, not a content, and so cannot be stored. Emmanuel Levinas places the origin of ethics
      in the face of the Other — precisely that which does not survive detachment into text. Their
      works remain in copyright (Buber †1965, Levinas †1995); no module can carry them, and none
      pretends to.</p>
      <p class="readable">The corpus's own last counter-voice marks the same spot from inside.
      Kapp's organ projection (<a href="#/works/kapp">Grundlinien, 1877</a>) understands every
      technology, up to the tools made “from the workshop of the mind itself”, as a projection of
      the human — which is to say: as monologue made durable. A projection meets no one. Where
      projection ends, encounter begins; there this corpus ends too, and must.</p>
    </div>

    <div class="panel"><h2>The philosophical pact</h2>
      <p class="readable">Reading philosophy is not extraction but a bond. Rainer Otte has called it
      the <em>philosophical pact</em> between author and reader — in analogy to Philippe Lejeune's
      autobiographical pact: an implicit commitment to truth that deliberate deception would break,
      and that tools which detach sentences from their situation can dissolve without anyone
      noticing. The question whether an apparatus like this one — or, more sharply, a language
      model trained on such texts — keeps or breaks that pact cannot be settled by assertion. It
      can only be answered in the form of the thing itself: texts as wholes rather than snippets;
      translations marked unofficial; every editorial hand named — including the seven paragraphs a
      1912 translator silently dropped from La Mettrie, a broken pact this edition repairs; and
      numbering grids built so that the reader can leave. This apparatus wants to be left — in the
      direction of the books.</p>
      <p class="readable" style="color:var(--fg2)">Further reading: Martin Buber, <em>Ich und
      Du</em> (Leipzig 1923). — Emmanuel Levinas, <em>Totalité et infini</em> (The Hague 1961). —
      Philippe Lejeune, <em>Le pacte autobiographique</em> (Paris 1975). — Rainer Otte,
      <em>Selber denken. Philosophie im Alltag</em> (Frankfurt am Main: Humanities Online, 2023),
      on ChatGPT and the philosophical pact.</p>
    </div>
  </div>`));
}

/* ============================================================ IMPRINT */
function viewImprint() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Legal notice</span>
      <h1>Legal notice</h1>
      <p class="lede">Who operates this site, and how to reach them.</p></div>
    <div class="panel"><h2>Operator</h2>
      <p class="readable">
        Dr. Pantaleon Fassbender<br>
        16751 NE 5th Street<br>
        Williston, FL 32696<br>
        United States</p>
      <p class="readable">Email: <a href="mailto:pantaleonfassbender@gmail.com">pantaleonfassbender@gmail.com</a></p>
      <p class="readable">This site is a personal research project, operated and hosted in the United
      States by a private individual, and not on behalf of any institution, employer or publisher. There
      is no company behind it, and it carries no advertising and no sponsorship.</p>
      <p class="readable">Responsible for the content: Dr. Pantaleon Fassbender, at the address above.
      Data handling is set out in the <a href="#/privacy">privacy notice</a>.</p></div>
    <div class="panel"><h2>Rights in the texts</h2>
      <p class="readable">All texts shipped on this site are in the United States public domain; the
      full account, edition by edition, is on the <a href="#/method">method page</a>. The site's own
      editorial matter is released under CC BY 4.0, its code under the MIT licence, and its derived
      data and working translations under CC0 — see the repository's LICENSES file.</p></div>
  </div>`));
}

Object.assign(ROUTES, {
  overview: viewOverview, introduction: viewIntroduction, works: viewWorks,
  concordance: viewConcordance, atlas: viewAtlas, method: viewMethod,
  coda: viewCoda, privacy: viewPrivacy, imprint: viewImprint,
});
boot();
