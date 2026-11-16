# 같은 단지·같은 넓이 변화 — 두 기간 각 1건 이상(본문) vs 각 2건·3건 이상(흔들림 점검). S1 raw, 해제 뺌, 전용 80~85㎡.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def half(ym):
    y, m = divmod(ym, 100); return f'{y}{"상" if m <= 6 else "하"}'
k2 = C.defaultdict(lambda: C.defaultdict(list))
for code in ('41210', '11530', '11545'):
  for p in sorted(glob.glob(os.path.join(H, 'raw', code + '_*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType') or not (80 <= num(r['excluUseAr']) <= 85): continue
        k2[(code, r.get('aptSeq') or r['aptNm'], round(num(r['excluUseAr'])))][half(int(r['dealYear']) * 100 + int(r['dealMonth']))].append(num(r['dealAmount']))
for a, b in (('2023상', '2026하'), ('2024하', '2026하'), ('2025하', '2026상')):
    for code, nm in (('41210','광명'),('11530','구로'),('11545','금천')):
        out = []
        for mn in (1, 2, 3):
            rs = [st.median(v[b]) / st.median(v[a]) - 1 for k, v in k2.items() if k[0] == code and len(v[a]) >= mn and len(v[b]) >= mn]
            out.append(f"≥{mn}건 {st.median(rs)*100:+.1f}%({len(rs)})" if rs else f"≥{mn}건 -")
        print(a, '→', b, nm, ' · '.join(out))
