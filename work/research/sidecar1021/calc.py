# 코스피(^KS11) 하루 등락률 ±4% 이상인 날 세기 — 야후 일별 종가(raw/ks11.json, 2026-10-21 받음). 오늘(10/21)은 장중이라 뺀다.
import json, datetime as D, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/ks11.json'))['chart']['result'][0]
rows = [(D.datetime.fromtimestamp(t, D.UTC).astimezone(D.timezone(D.timedelta(hours=9))).date(), x)
        for t, x in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if x]
rows = [r for r in rows if r[0] < D.date(2026, 10, 21)]
gaps = [(a[0], b[0]) for a, b in zip(rows, rows[1:]) if (b[0] - a[0]).days > 6]
print('기간', rows[0][0], '~', rows[-1][0], '거래일', len(rows), '6일 넘는 빈 곳', gaps[:10])
up = collections.Counter(); dn = collections.Counter(); ups = []; dns = []
for a, b in zip(rows, rows[1:]):
    r = (b[1] / a[1] - 1) * 100
    if r >= 4: up[b[0].year] += 1; ups.append((b[0], round(r, 2)))
    if r <= -4: dn[b[0].year] += 1; dns.append((b[0], round(r, 2)))
print('+4% 이상 합', sum(up.values()), ' -4% 이하 합', sum(dn.values()))
for y in sorted(set(up) | set(dn)): print(y, '상승', up[y], '하락', dn[y])
print('2026 상승일', [x for x in ups if x[0].year == 2026])
print('2026 하락일', [x for x in dns if x[0].year == 2026])
print('2026 거래일', sum(1 for r in rows if r[0].year == 2026))
