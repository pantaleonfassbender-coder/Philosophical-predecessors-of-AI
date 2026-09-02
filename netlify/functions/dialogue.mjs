/* Netlify Function — citation-bound answering over the Calculemus corpus.
   Calls the Claude Messages API (claude-sonnet-5). Reads ANTHROPIC_API_KEY
   from the environment (Netlify: Site configuration → Environment variables);
   ANTHROPIC_BASE_URL is honoured, so Netlify's AI Gateway works as an
   alternative. Nothing is stored or logged by this site.

   Note for maintainers: claude-sonnet-5 rejects `temperature`/`top_p`/`top_k`
   (removed on the 4.7+ generation) — do not add them back. Thinking runs
   adaptively by default; output_config.effort keeps the spend low. */

const MODEL = process.env.DIALOG_MODEL || "claude-sonnet-5";
const EFFORT = process.env.DIALOG_EFFORT || "low";

// Best-effort rate limiting (per warm function instance).
const WINDOW_MS = 60000, PER_IP = 6, GLOBAL = 40;
const ipHits = new Map();
let globalHits = [];
function allow(ip) {
  const now = Date.now();
  globalHits = globalHits.filter((t) => now - t < WINDOW_MS);
  if (globalHits.length >= GLOBAL) return false;
  const hits = (ipHits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (hits.length >= PER_IP) return false;
  hits.push(now); ipHits.set(ip, hits); globalHits.push(now);
  if (ipHits.size > 1000) ipHits.clear();
  return true;
}

const BASE = `You are a research instrument for "Calculemus: Philosophical Predecessors of AI", a public-domain corpus of the prehistory of the AI debate. Its sixteen modules run in four lines: the logic line (Llull's Ars brevis, Hobbes's Leviathan, a Leibniz anthology, Boole's Laws of Thought, Frege), the machine line (Pascal's Pensées fragments, Lovelace's Notes, Jevons 1870, Peirce 1887), the counter-voices (Descartes's Discours Part V, La Mettrie's L'Homme Machine, Kapp's Grundlinien einer Philosophie der Technik), and the narrative line of the animated word (Homer/Aristotle, a golem anthology from Tanach, Talmud, Sefer Yetzirah and Grimm 1808, Goethe's Zauberlehrling, Čapek's R.U.R.).

Binding rules:
1. Answer ONLY from the passages supplied. What is not in them, you do not assert — not even where you believe you know it. If the passages are thin, say so and name what is missing.
2. Attach the canonical citation to every substantive claim, in parentheses, in the exact form given with each passage — e.g. (Lev., ch. V [3]), (Mon. §17), (LoT II, art. 5), (Note G [7]), (PhT VIII [6]), (San. 65b), (SY 2:4), (ZfE 1808 [1]), (Zauberlehrling, st. 6), (RUR, Pred. [1]), (Il. XVIII 369–379), (Pol. I 4, 1253b33–1254a1). Never invent a citation.
3. Quote at most a short phrase — roughly a dozen words — inside quotation marks with its citation; otherwise paraphrase. Note where an English rendering is this site's unofficial working translation (the passages say so): quotations for scholarly use should be taken from the original.
4. The corpus spans three millennia and four genres of writing. Distinguish what a text says from what later texts make of it; where the works differ, set the difference out rather than harmonising it. Narrative sources (the fourth line) tell rather than argue — treat them as testimony of an imagination, not as doctrine.
5. Scholarly English. Two to five paragraphs. No hype, no anachronism dressed as fact.
6. Where useful, close with the passage a reader should go to next.`;

export default async (req, context) => {
  if (req.method !== "POST") return json({ error: "POST only." }, 405);

  const ip = (context && context.ip) || req.headers.get("x-nf-client-connection-ip") || "unknown";
  if (!allow(ip)) return json({ error: "Rate limit reached — try again in a minute." }, 429);

  let body;
  try { body = await req.json(); } catch { return json({ error: "Malformed JSON." }, 400); }

  const frage = String(body.frage || "").slice(0, 2000).trim();
  const passagen = Array.isArray(body.passagen) ? body.passagen.slice(0, 20) : [];
  const verlauf = Array.isArray(body.verlauf) ? body.verlauf.slice(-6) : [];

  if (frage.length < 5) return json({ error: "Send a formulated question." }, 400);
  if (!passagen.length) return json({ error: "No passages supplied." }, 400);

  const key = process.env.ANTHROPIC_API_KEY;
  const base = (process.env.ANTHROPIC_BASE_URL || "https://api.anthropic.com").replace(/\/$/, "");
  if (!key) {
    return json({
      error: "The answering endpoint is not configured. In Netlify, set ANTHROPIC_API_KEY under " +
             "Site configuration → Environment variables (or enable the AI Gateway). " +
             "The local retrieval works regardless — the passages found are listed below the question.",
    }, 503);
  }

  const contextBlock = passagen.map((p, i) =>
    `[${i + 1}] ${p.cite} — ${p.werk || ""}${p.wt ? " (working translation — cite the original)" : ""}\n` +
    String(p.text || "").slice(0, 2200)
  ).join("\n\n---\n\n");

  const messages = [];
  for (const m of verlauf.slice(0, -1)) {
    if (!m || !m.text) continue;
    messages.push({ role: m.rolle === "user" ? "user" : "assistant", content: String(m.text).slice(0, 1500) });
  }
  messages.push({ role: "user", content: `PASSAGES\n\n${contextBlock}\n\n---\n\nQUESTION\n${frage}` });

  try {
    const r = await fetch(`${base}/v1/messages`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 1600,
        output_config: { effort: EFFORT },
        system: BASE,
        messages,
      }),
    });
    if (!r.ok) {
      const detail = (await r.text()).slice(0, 300);
      return json({ error: `The answering endpoint reports: ${r.status} ${detail}` }, 502);
    }
    const d = await r.json();
    if (d.stop_reason === "refusal") {
      return json({ error: "The model declined to answer this question." }, 502);
    }
    const antwort = (d.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    return json({ antwort: antwort || "(empty answer)", modell: d.model || MODEL, verbrauch: d.usage || null });
  } catch (e) {
    return json({ error: "Upstream request failed: " + String(e && e.message ? e.message : e) }, 502);
  }
};

function json(o, status = 200) {
  return new Response(JSON.stringify(o), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

export const config = { path: "/.netlify/functions/dialogue" };
