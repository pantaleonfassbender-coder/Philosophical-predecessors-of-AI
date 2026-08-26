# Descartes, Discours de la methode (1637), Part V — French (Gutenberg #13846,
# Cousin edition orthography) parallel with Veitch's PD English (Gutenberg #59).
# Units are paragraphs; alignment is by paragraph order, verified by count.
import io, re, json

def paras_of(path, lo, hi, drop_first=0):
    lines = io.open(path, encoding='utf-8').read().split('\n')[lo:hi]
    out, cur = [], []
    for ln in lines:
        if not ln.strip():
            if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip()); cur = []
        else:
            cur.append(ln.strip())
    if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip())
    out = [p for p in out if len(p) > 2 and not re.fullmatch(r'[A-ZÈÉ .]+', p)]
    return out[drop_first:]

fr = paras_of('C:/Users/leofa/AppData/Local/Temp/aipred/descartes_fr.txt', 3816, 4285)
en = paras_of('C:/Users/leofa/AppData/Local/Temp/aipred/descartes_en.txt', 1090, 1566)
print('fr paras:', len(fr), '| en paras:', len(en))
for i in range(min(len(fr), len(en))):
    print(f"{i+1:2d} FR {fr[i][:58]}")
    print(f"   EN {en[i][:58]}")
json.dump({'fr': fr, 'en': en}, io.open('C:/Users/leofa/AppData/Local/Temp/aipred/descartes-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
