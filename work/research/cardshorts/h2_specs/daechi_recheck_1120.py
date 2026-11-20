import sys, json, os, statistics as st
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
D = os.path.dirname(os.path.abspath(__file__))
months = ['202511','202512'] + [f'2026{m:02d}' for m in range(1,12)]
allr = {}
for ym in months:
    fn = os.path.join(D, f'11680_{ym}_trade_1120.json')
    if not os.path.exists(fn):
        json.dump(rtmolit.fetch('trade', '11680', ym), open(fn,'w',encoding='utf-8'), ensure_ascii=False)
    allr[ym] = json.load(open(fn, encoding='utf-8'))
print({k: len(v) for k, v in allr.items()})
print(list(allr['202605'][0].keys()))
APT = {'은마': None, '래미안대치팰리스': None, '대치르엘': None}
def rows(win):
    out = {a: [] for a in APT}
    for ym in win:
        for r in allr[ym]:
            if r.get('umdNm','').strip() != '대치동': continue
            nm = r.get('aptNm','').strip()
            a = next((k for k in APT if nm == k or nm.startswith(k)), None)
            if not a: continue
            ar = float(r['excluUseAr'])
            if not (80 <= ar < 85.99): continue
            if (r.get('cdealType') or '').strip(): continue
            if '공공' in (r.get('buyerGbn') or ''): continue
            amt = rtmolit.num(r['dealAmount'])
            out[a].append((amt, ar, ym, r.get('floor'), r.get('dealingGbn'), nm))
    return out
for name, win in (('H-2 창 2025.11~2026.10', months[:12]), ('최근 창 2025.12~2026.11', months[1:])):
    o = rows(win); print('##', name)
    pp = {}
    for a, L in o.items():
        if not L: print(a, 0); continue
        ppy = st.median([amt / (ar / 3.3058) for amt, ar, *_ in L]); pp[a] = ppy
        print(a, len(L), '건 중앙', st.median([x[0] for x in L])/1e4, '억 · 평당', round(ppy), '만원 · names', {x[5] for x in L}, '· 직거래', sum('직거래' in (x[4] or '') for x in L))
    if all(k in pp for k in APT):
        print('은마 vs RDP', round((pp['은마']/pp['래미안대치팰리스']-1)*100,1), '% · 은마 vs 르엘', round((pp['은마']/pp['대치르엘']-1)*100,1), '%')
print('11월 거래:', [(x[0], x[3]) for a,L in rows(['202611']).items() for x in L])
