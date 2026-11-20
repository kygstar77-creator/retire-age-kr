# de1s_kofin 올리기 전 확인 — raw/etf_*.json(네이버 증권 ETF 분석 m.stock.naver.com/api/stock/<코드>/etfAnalysis, 2026-11-20 10:2x 받음, 기준일 2026.11.19) → prepub_1120.txt
import os, json, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
out = ['# de1s_kofin 올리기 전 확인 (calc_kofin.py, 2026-11-20) — 네이버 증권 ETF 분석 sectorPortfolioList·etfTop10MajorConstituentAssets, 기준일 2026.11.19',
       '# 롱폼 D-ETF-1(10/16 값): PLUS 고배당주 금융 54.85% · SOL 코리아고배당 45.8% · TIGER 은행고배당플러스TOP10 99.7% · PLUS 맨 위 DB손해보험 6.54·기업은행 5.44·우리금융지주 5.43']
for f in sorted(glob.glob(os.path.join(H, 'raw', 'etf_*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    w = {x['detailTypeCode']: x['weight'] for x in d['sectorPortfolioList']}
    top = [(t['itemName'], t['etfWeight']) for t in d['etfTop10MajorConstituentAssets'][:3]]
    out.append(f"{d['itemName']}({d['itemCode']}) 기준일 {d['navPerformanceReferenceDate']} | 금융 {w['FINANCIALS']:.2f}% → 화면 {round(w['FINANCIALS'], 1)}% | 맨 위 셋 " + ' · '.join(f'{a} {b}' for a, b in top))
out.append('바뀐 것: SOL 코리아고배당 금융 45.8% → 56.4%(롱폼 말에 숫자 없음, 화면만 새 값) · PLUS 맨 위 셋 같은 세 종목, 순서 2·3위 바뀜(우리금융지주 5.92 · 기업은행 5.65) — 말은 셋을 늘어놓을 뿐 순위 말 없음, 화면은 말 순서 그대로 셋 이름만')
out.append('그대로: PLUS 금융 절반 넘음(55.57) · TIGER 은행 거의 100%(99.23)')
open(os.path.join(H, 'prepub_1120.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
