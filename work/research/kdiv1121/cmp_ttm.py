# 같은 갈래 5개: 야후 분배 이벤트(2차①) ↔ 네이버 증권 etfAnalysis TTM(2차②) 대조, 2025-10 → 2026-10 월 분배 변화
import json, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
M = {'161510': '161510.KS', '279530': '0', '104530': '104530.KS', '466940': '466940.KS', '0105E0': '0105E0.KS'}
for c in ['161510', '279530', '104530', '466940', '0105E0']:
    n = json.load(open(f'raw/naver_etfan_{c}_1120.json', encoding='utf-8'))
    yf = f'raw/y_{c}.KS.json'  
    ev = []
    for f in ([yf] if yf else []):
        try:
            r = json.load(open(f))['chart']['result'][0]; ev = sorted((dt.datetime.fromtimestamp(int(k), dt.UTC).date(), v['amount']) for k, v in r.get('events', {}).get('dividends', {}).items())
        except Exception as e: print(c, 'yahoo ERR', e)
    last12 = [a for d, a in ev if d > dt.date(2025, 11, 20)]
    print(c, n['itemName'], n['issuerName'], '보수', n['totalFee'], '| 네이버', n['dividend'], '| 야후 최근12개월 합', round(sum(last12)), len(last12), '| 최근', ev[-14:] if ev else '없음')
