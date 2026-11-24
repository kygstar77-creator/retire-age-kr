# KOSPI-1 짝 글에만 넣는 새 계산(영상에 없음): ① 2026-02-02 무리(표에서 뺀 것) 지금 위치 ② 올해 -5% 날 다음 거래일 결과
# 원자료: 한국은행 ECOS 802Y001 코스피 일별 종가(원자료 한국거래소) — kospi_daily_1123.json(11/23 youtube-loop 다시 받음)
import json, statistics as st
d = json.load(open('kospi_daily_1123.json', encoding='utf-8'))
dt = [x[0] for x in d]; v = [x[1] for x in d]
ch = [None] + [v[i]/v[i-1]-1 for i in range(1, len(v))]
i0 = dt.index('20260202')
print('2/2 close', v[i0], 'prev', v[i0-1], 'chg %.2f%%' % (ch[i0]*100))
print('last', dt[-1], v[-1], 'vs 2/2 close %+.1f%%' % ((v[-1]/v[i0]-1)*100), 'vs prev %+.1f%%' % ((v[-1]/v[i0-1]-1)*100))
after = v[i0+1:]; mn = min(after); print('min after', dt[i0+1+after.index(mn)], mn, '%+.1f%%' % ((mn/v[i0]-1)*100))
# 전날 값 되찾기
for j in range(i0+1, len(v)):
    if v[j] >= v[i0-1]: print('recover', dt[j], j-i0, 'trading days'); break
n = len(v) - 1 - i0; print('trading days since 2/2:', n)
# 올해 -5% 날 다음 날
idx = [i for i in range(1, len(v)) if dt[i] >= '20260102' and ch[i] <= -0.05]
print('2026 -5% days', len(idx))
nxt = [ch[i+1] for i in idx if i+1 < len(v)]
print('next-day count', len(nxt), 'up', sum(1 for x in nxt if x > 0), 'down', sum(1 for x in nxt if x < 0), 'next +5%+', sum(1 for x in nxt if x >= 0.05), 'median %+.2f%%' % (st.median(nxt)*100))
print('consecutive -5% next', sum(1 for x in nxt if x <= -0.05))
