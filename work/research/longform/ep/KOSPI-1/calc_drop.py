# 하루 하락 폭 상위 날 → 그날 종가 대비 1년 뒤(252 거래일) 값. 지난 값만, 예측 없음.
import json
rows = json.load(open('kospi_daily_ecos.json'))
out = []
for i in range(1, len(rows)):
    d, v = rows[i]; p = rows[i-1][1]
    ch = (v/p - 1)*100
    fut = rows[i+252][1] if i+252 < len(rows) else None
    out.append((ch, d, v, fut))
out.sort()
print('하루 하락 상위 15 (같은 해 몰림 주의)')
n=0
for ch, d, v, fut in out[:15]:
    f = f'{(fut/v-1)*100:+.1f}%' if fut else '1년 안 됨'
    print(f'{d} {ch:+.2f}% 종가 {v:,.2f} → 1년 뒤 {f}')
ok=[(fut/v-1)*100 for ch,d,v,fut in out if ch<=-5 and fut]
print('하루 -5% 이하 날 수', sum(1 for x in out if x[0]<=-5), '1년 뒤 오른 비율', sum(1 for x in ok if x>0), '/', len(ok))
print('기간', rows[0][0], '~', rows[-1][0], '마지막', rows[-1][1])
