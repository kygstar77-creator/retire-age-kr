# de1s_basket 11/13 올리기 전 확인 계산 — raw/etf_*.json(네이버 증권 ETF 분석 11/13) → longform/ep/D-ETF-1/calc_basket1113_out.txt
import os, json, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.normpath(os.path.join(H, '..', '..', 'longform', 'ep', 'D-ETF-1'))
out = ['# D-ETF-1 calc_basket1113_out (cardshorts/de1s_basket/calc_basket.py, 2026-11-13) — 네이버 증권 ETF 분석 sectorPortfolioList, 국내 미국배당다우존스 4종']
K = [('CONSUMER_STAPLES', '필수소비재'), ('HEALTHCARE', '헬스케어'), ('ENERGY', '에너지')]
rows = {}
for f in sorted(glob.glob(os.path.join(H, 'raw', 'etf_*.json'))):
    d = json.load(open(f, encoding='utf-8')); w = {x['detailTypeCode']: x['weight'] for x in d['sectorPortfolioList']}
    rows[d['itemName']] = w; s3 = sum(w[k] for k, _ in K)
    out.append(f"{d['itemName']} | " + ' · '.join(f'{n} {w[k]:.2f}' for k, n in K) + f' | 세 업종 합 {s3:.2f}')
for k, n in K:
    v = [w[k] for w in rows.values()]; out.append(f'{n} 범위 {min(v):.2f}~{max(v):.2f} → 반올림 {round(min(v),1)}~{round(max(v),1)} · 4종 차 {max(v)-min(v):.2f}%p')
s = [sum(w[k] for k, _ in K) for w in rows.values()]
out.append(f'세 업종 합 범위 {min(s):.2f}~{max(s):.2f} → 약 {round(sum(s)/len(s))}%')
open(os.path.join(EP, 'calc_basket1113_out.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
