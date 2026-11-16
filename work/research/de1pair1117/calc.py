# de1pair1117 계산 — raw/(2026-11-17 받음) → calc_out.txt
#  ① 슈왑 SCHD 보유(11/13) 업종 합산 vs 네이버 국내 4종 업종(기준 11/13) ② 상위 10종목 이름 겹침 ③ 국내 4종 기간 수익률(NAV) 차이
import json, csv, glob, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw'); out = []
MAP = {'Consumer Staples': 'CONSUMER_STAPLES', 'Health Care': 'HEALTHCARE', 'Energy': 'ENERGY', 'Information Technology': 'IT',
       'Industrials': 'INDUSTRIALS', 'Financials': 'FINANCIALS', 'Consumer Discretionary': 'CONSUMER_DISCRETIONARY',
       'Communication Services': 'COMMUNICATION', 'Materials': 'MATERIALS', 'Utilities': 'UTILITIES', 'Real Estate': 'REAL_ESTATE'}
KO = {'CONSUMER_STAPLES': '필수소비재', 'HEALTHCARE': '헬스케어', 'ENERGY': '에너지', 'IT': 'IT', 'INDUSTRIALS': '산업재',
      'FINANCIALS': '금융', 'CONSUMER_DISCRETIONARY': '경기소비재', 'COMMUNICATION': '통신', 'MATERIALS': '소재', 'UTILITIES': '유틸리티', 'REAL_ESTATE': '부동산'}
rows = list(csv.DictReader(open(os.path.join(R, 'schwab_SCHD_holdings_20261117.csv'), encoding='utf-8-sig')))
rows = [r for r in rows if r.get('Percent of Assets')]
sch = {}
for r in rows:
    k = MAP.get(r['Sector'], r['Sector'] or 'CASH'); sch[k] = sch.get(k, 0) + float(r['Percent of Assets'])
out.append(f"# SCHD 슈왑 보유 기준일 {rows[0]['As-Of-Date']} · 종목 {len(rows)}줄 · 합 {sum(float(r['Percent of Assets']) for r in rows):.2f}")
kr = {}
for f in sorted(glob.glob(os.path.join(R, 'etf_*_20261117.json'))):
    d = json.load(open(f, encoding='utf-8')); kr[d['itemName']] = d
out.append('# 업종 비중(%) — SCHD | ' + ' | '.join(kr))
gaps = []
for k in ['CONSUMER_STAPLES', 'HEALTHCARE', 'ENERGY', 'IT', 'INDUSTRIALS', 'FINANCIALS', 'CONSUMER_DISCRETIONARY', 'COMMUNICATION', 'MATERIALS', 'UTILITIES']:
    v = [{x['detailTypeCode']: x['weight'] for x in d['sectorPortfolioList']}.get(k, 0) for d in kr.values()]
    s = sch.get(k, 0); gaps.append(max(abs(s - x) for x in v)); dk = max(v) - min(v)
    out.append(f"{KO[k]} | SCHD {s:.2f} | 국내 {min(v):.2f}~{max(v):.2f} (4종 차 {dk:.2f}) | SCHD와 최대 차 {max(abs(s-x) for x in v):.2f}")
top3s = sum(sch.get(k, 0) for k in ['CONSUMER_STAPLES', 'HEALTHCARE', 'ENERGY'])
top3k = [sum({x['detailTypeCode']: x['weight'] for x in d['sectorPortfolioList']}.get(k, 0) for k in ['CONSUMER_STAPLES', 'HEALTHCARE', 'ENERGY']) for d in kr.values()]
out.append(f"세 업종 합 | SCHD {top3s:.2f} | 국내 {min(top3k):.2f}~{max(top3k):.2f}")
out.append(f"업종별 SCHD↔국내 최대 차 중 가장 큰 값 {max(gaps):.2f}%p")
def key(s): s = re.sub(r'[^A-Z0-9 ]', ' ', s.upper()); return [t for t in s.split() if t not in ('INC','CORP','CO','THE','CORPORATION','COMPANY','LTD','PLC','CLASS','A','B','HOLDINGS','GROUP','N','V')]
s10 = sorted(rows, key=lambda r: -float(r['Percent of Assets']))[:10]
out.append('# SCHD 상위 10: ' + ', '.join(f"{r['Symbol']} {float(r['Percent of Assets']):.2f}" for r in s10))
out.append(f"SCHD 상위 10 합 {sum(float(r['Percent of Assets']) for r in s10):.2f}")
for n, d in kr.items():
    t = [x['itemName'] for x in d['etfTop10MajorConstituentAssets']]
    hit = [x for x in t if any(key(x)[:1] == key(r['Name'])[:1] for r in rows)]
    hit10 = [x for x in t if any(key(x)[:1] == key(r['Name'])[:1] for r in s10)]
    out.append(f"{n} 상위10(네이버, 주식 수 순) {len(t)}개 중 SCHD 보유에 있음 {len(hit)} · SCHD 상위10에도 있음 {len(hit10)} — {', '.join(t)}")
out.append('# 국내 4종 NAV 수익률(%) 기준 ' + list(kr.values())[0]['navPerformanceReferenceDate'])
for p in ['M1', 'M3', 'M6', 'YTD', 'Y1']:
    v = {n: {x['periodTypeCode']: x['value'] for x in d['navPerformanceList']}.get(p) for n, d in kr.items()}
    vv = [x for x in v.values() if x is not None]
    out.append(f"{p} | " + ' · '.join(f"{n.split()[0]} {x}" for n, x in v.items()) + (f" | 차 {max(vv)-min(vv):.2f}%p" if len(vv) > 1 else ''))
for n, d in kr.items():
    out.append(f"{n} | 기초지수 {d['etfBaseIndex']} | 총보수 {d['totalFee']} | 순자산 {d['totalNav']} | 상장 {d['listedDate']} | 환헤지 {'안 함' if '환헤지를 하지 않' in d['etfSummary'] else '확인'}")
open(os.path.join(H, 'calc_out.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
