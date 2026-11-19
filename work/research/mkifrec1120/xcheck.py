# Yahoo 일별 종가를 네이버 금융 일별 시세와 대조 — 배당락 앞뒤 18개 날짜와 회복일
import json, re, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
nv = {}
for m in re.finditer(r'\["(\d{8})",\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)', open('raw/naver_sise.txt', encoding='utf-8', errors='ignore').read()):
    nv[m.group(1)] = (int(m.group(2)), int(m.group(5)))  # 시가, 종가
d = json.load(open('raw/yahoo.json'))['chart']['result'][0]; q = d['indicators']['quote'][0]
KST = dt.timezone(dt.timedelta(hours=9)); bad = 0; n = 0
for t, o, c in zip(d['timestamp'], q['open'], q['close']):
    k = dt.datetime.fromtimestamp(t, KST).strftime('%Y%m%d')
    if c and k in nv:
        n += 1
        if abs(nv[k][1] - c) > 0.5: bad += 1; print('다름', k, nv[k], c)
print('대조', n, '일 · 종가 다른 날', bad)
for k in ['20251226','20251229','20260626','20260629','20231226','20231227','20260213','20251119']:
    print(k, nv.get(k))
# 회복 점검: 6월 기준 마지막 받는 날 종가 이후 최고 종가
for day, base in [('20230628',12980),('20240626',12610),('20250626',11870),('20260626',10590)]:
    after = [v[1] for k, v in nv.items() if k > day]
    print(day, base, '그 뒤 최고 종가', max(after))
print('마지막', max(nv), nv[max(nv)])
