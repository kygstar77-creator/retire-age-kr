# 66㎡ 띠(60~70㎡): 앞 1~7단지 묶음 vs 11단지 — 최근 1년·그 전 1년. 재료·제외 기준 calc.py와 같음
import json, os, glob, re, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); PY = 3.305785
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '11470_*_trade.json'))): rows += json.load(open(p, encoding='utf-8'))
ok = lambda r: not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
pp = lambda r: num(r['dealAmount']) / num(r['excluUseAr']) * PY; ar = lambda r: num(r['excluUseAr'])
ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth']); med = lambda v: st.median(v) if v else 0
MS = [r for r in rows if ok(r) and '목동신시가지' in r['aptNm'] and 60 <= ar(r) < 70]
dan = lambda r: int(re.search(r'\d+', r['aptNm'].replace('목동신시가지', '')).group())
for tag, a, b in [('최근 1년', 202511, 202611), ('그 전 1년', 202411, 202510)]:
    rs = [r for r in MS if a <= ymi(r) <= b]; f = [r for r in rs if dan(r) <= 7]; e = [r for r in rs if dan(r) == 11]
    s7 = [r for r in rs if dan(r) == 7]
    print(f'- {tag}: 앞 {len(f)}건 평당 {med([pp(r) for r in f]):,.0f} / 11단지 {len(e)}건 평당 {med([pp(r) for r in e]):,.0f} 한 채 {med([num(r["dealAmount"]) for r in e])/10000:.2f}억 → 앞이 {med([pp(r) for r in f])/med([pp(r) for r in e])*100-100:+.1f}% · 7단지 {len(s7)}건 평당 {med([pp(r) for r in s7]):,.0f} 한 채 {med([num(r["dealAmount"]) for r in s7])/10000:.2f}억 → 7이 11보다 평당 {med([pp(r) for r in s7])/med([pp(r) for r in e])*100-100:+.1f}%, 한 채 {(med([num(r["dealAmount"]) for r in s7])-med([num(r["dealAmount"]) for r in e]))/10000:.2f}억')
