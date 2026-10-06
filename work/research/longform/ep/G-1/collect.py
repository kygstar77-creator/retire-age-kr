# G-1 원자료 모으기(확인 필요 4건 중 기계로 받는 2건): 한국은행 ECOS 731Y001 원/달러 매매기준율(일) · 미 재무부 Daily Treasury Par Yield Curve 10 Yr(일)
# FRED DGS10은 10/6 접속 시간초과 → 같은 값의 원출처인 미 재무부 CSV(raw/ust_2025.csv·ust_2026.csv, curl로 받음)를 쓴다
import sys, json, os, urllib.request, csv, io
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw'); os.makedirs(D, exist_ok=True)
k = apis.key('ecos')
d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/400/731Y001/D/20250901/20261006/0000001')
fx = [(r['TIME'], float(r['DATA_VALUE'])) for r in d.get('StatisticSearch', {}).get('row', [])]
dgs = []
for y in (2025, 2026):
    for r in list(csv.DictReader(open(os.path.join(D, f'ust_{y}.csv'), encoding='utf-8')))[::-1]:
        m, dd, yy = r['Date'].split('/')
        if f'{yy}{m}{dd}' >= '20250901' and r['10 Yr']: dgs.append((f'{yy}{m}{dd}', float(r['10 Yr'])))
json.dump({'ECOS_731Y001_0000001_D': fx, 'UST_10Yr': dgs}, open(os.path.join(D, 'collect_20261006.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for name, s in [('USD/KRW', fx), ('UST 10Yr', dgs)]:
    print(name, len(s), s[:1], s[-3:], 'max', max(s, key=lambda x: x[1]), 'min', min(s, key=lambda x: x[1]))
