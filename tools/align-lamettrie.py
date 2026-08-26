# Align La Mettrie FR (1747) with Bussey's EN (1912) paragraph streams by
# Gale-Church-style DP over character lengths (beads 1:1, 1:2, 2:1).
import io, json, re, math

d = json.load(io.open('C:/Users/leofa/AppData/Local/Temp/aipred/lamettrie-draft.json', encoding='utf-8'))
fr = d['fr'][:173]          # drop trailing 'MAN A MACHINE.' heading
en = d['en'][:158]          # drop Natural History extracts + appendix

def clean(p):
    p = re.sub(r'\[\d+\]|\{\d+\}', '', p)
    p = re.sub(r'\s+', ' ', p).strip()
    return p
fr = [clean(p) for p in fr]
en = [clean(p) for p in en]

R = sum(len(p) for p in en) / sum(len(p) for p in fr)   # expected en/fr ratio

DEACC = str.maketrans('àâäéèêëîïôöùûüç', 'aaaeeeeiioouuuc')
def toks(p):
    ws = re.findall(r"[A-Za-zÀ-ÿ]{6,}", p.lower())
    return set(w.translate(DEACC)[:5] for w in ws)

FRT = [toks(p) for p in fr]
ENT = [toks(p) for p in en]

def cost(lf, le, tf, te):
    if lf == 0 or le == 0: return 10.0
    c = abs(math.log((le / lf) / R)) ** 2 * 8
    inter = len(tf & te)
    denom = min(len(tf), len(te)) or 1
    c -= 6.0 * (inter / denom)          # cognate-anchor bonus
    return c

INF = float('inf')
nf, ne = len(fr), len(en)
dp = [[INF] * (ne + 1) for _ in range(nf + 1)]
bk = [[None] * (ne + 1) for _ in range(nf + 1)]
dp[0][0] = 0
for i in range(nf + 1):
    for j in range(ne + 1):
        if dp[i][j] == INF: continue
        base = dp[i][j]
        # 1:1
        if i < nf and j < ne:
            c = base + cost(len(fr[i]), len(en[j]), FRT[i], ENT[j])
            if c < dp[i+1][j+1]: dp[i+1][j+1] = c; bk[i+1][j+1] = (1, 1)
        # 1:2  (one fr para -> two en paras)
        if i < nf and j + 1 < ne:
            c = base + cost(len(fr[i]), len(en[j]) + len(en[j+1]), FRT[i], ENT[j] | ENT[j+1]) + 1.2
            if c < dp[i+1][j+2]: dp[i+1][j+2] = c; bk[i+1][j+2] = (1, 2)
        # 2:1
        if i + 1 < nf and j < ne:
            c = base + cost(len(fr[i]) + len(fr[i+1]), len(en[j]), FRT[i] | FRT[i+1], ENT[j]) + 1.2
            if c < dp[i+2][j+1]: dp[i+2][j+1] = c; bk[i+2][j+1] = (2, 1)
        # 1:0 (fr paragraph omitted by the 1912 translation)
        if i < nf:
            c = base + 3.5
            if c < dp[i+1][j]: dp[i+1][j] = c; bk[i+1][j] = (1, 0)

# backtrack
beads = []
i, j = nf, ne
while i > 0 or j > 0:
    di, dj = bk[i][j]
    beads.append((i - di, i, j - dj, j))
    i, j = i - di, j - dj
beads.reverse()

pairs = []
for a, b, c, e in beads:
    pairs.append((' '.join(fr[a:b]), ' '.join(en[c:e]), b - a, e - c))

print('beads:', len(pairs), '| 1:1', sum(1 for p in pairs if p[2]==1 and p[3]==1),
      '| 1:2', sum(1 for p in pairs if p[3]==2), '| 2:1', sum(1 for p in pairs if p[2]==2))
# spot check the quote anchor and ends
for idx, (f, e, *_ ) in enumerate(pairs):
    if 'Non nostrum' in f:
        print('ANCHOR', idx, '|', f[:50], '||', e[:50])
print('FIRST:', pairs[0][0][:60], '||', pairs[0][1][:60])
print('LAST :', pairs[-1][0][:60], '||', pairs[-1][1][:60])
json.dump(pairs, io.open('C:/Users/leofa/AppData/Local/Temp/aipred/lamettrie-aligned.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
