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
    </div>

    <div class="grid g3" style="margin-bottom:1.6rem">
      <div class="card linie-logic">
        <span class="tag" style="color:var(--logic)">The logic line</span>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">Hobbes: reason is reckoning.
        Leibniz: a symbolic language and a calculus of thought. Boole: the laws of thought as algebra.
        Frege: the formal system itself. The direct ancestry of symbolic AI.</p>
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
        himself is the machine. The arguments today's debate keeps rediscovering.</p>
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
    <div id="body"></div>
    <p class="fine">${esc(t.quelle)} ${esc(t.hinweis || "")}</p>
  </div>`));
  view.querySelector("#body").innerHTML = s.units.map(u => unitHtml(w, s, u)).join("");
  const anchor = (location.hash.split("@")[1] || "");
  if (anchor) document.getElementById("u" + anchor)?.scrollIntoView();
}

function unitHtml(w, s, u, hl) {
  const label = u.label ? `<p class="ulabel">${esc(u.label)}</p>` : "";
  let txt = esc(u.txt);
  if (hl) {
    const rx = new RegExp(hl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
    txt = txt.replace(rx, m => `<mark>${m}</mark>`);
  }
  return `<div class="unit" id="u${u.n}">
    <div style="display:flex;gap:.6rem;align-items:baseline"><span class="cite">${esc(citeOf(w.id, s, u))}</span></div>
    ${label}<p class="readable">${txt}</p></div>`;
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
        const m = rx.exec(u.txt);
        if (!m) continue;
        hits++;
        if (hits > 200) break;
        const a = Math.max(0, m.index - 90), b = Math.min(u.txt.length, m.index + term.length + 130);
        const ctx = (a > 0 ? "…" : "") + u.txt.slice(a, b) + (b < u.txt.length ? "…" : "");
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
    </div>

    <div class="panel"><h2>The programme</h2>
      <p class="readable">The corpus is built in stages along three lines. The logic line: Hobbes and
      Boole (shipped), then Leibniz (anthology: ars combinatoria, characteristica and calculus fragments,
      binary arithmetic, the Monadology with Latta's 1898 public-domain English), then Frege (Grundlagen
      der Arithmetik and Über Sinn und Bedeutung in German with working translations; the Begriffsschrift
      only in its prose parts, since its two-dimensional notation cannot honestly be reconstructed from
      OCR — a limit stated here in advance). The machine line: Lovelace's Notes of 1843 with Menabrea's
      Sketch, Jevons's paper of 1870, Peirce's “Logical Machines” of 1887 (from the original journal
      printing), and Pascal's fragment on the arithmetical machine. The counter-voices: Descartes's
      Discours Part V and La Mettrie's L'Homme Machine with the contemporary English translation of 1749.
      Two further modules are under consideration: a Llull prologue and Tractatus selections.</p>
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
  overview: viewOverview, works: viewWorks, concordance: viewConcordance,
  method: viewMethod, privacy: viewPrivacy, imprint: viewImprint,
});
boot();
