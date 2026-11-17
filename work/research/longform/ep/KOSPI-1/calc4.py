# KOSPI-1 계산 4 — 댓글 질문 답(11/17): ① 무리 첫날 뒤 1년 안에 첫날 종가보다 더 내려간 적 있나 ② 2025 첫날·2025 마지막 날 대비 지금. ECOS 802Y001 종가만, 예측 없음.
import json, statistics as st
rows = json.load(open('kospi_daily_ecos.json'))
ch = [(rows[i][0], rows[i][1], (rows[i][1]/rows[i-1][1]-1)*100, i) for i in range(1, len(rows))]
eps = []; last = -999
for d, v, c, i in ch:
    if c <= -5:
        if i - last > 60: eps.append((d, v, i))
        last = i
lower = []
for d, v, i in eps:
    if i + 252 >= len(rows): continue
    mn = min(r[1] for r in rows[i+1:i+253])
    lower.append((d, round((mn / v - 1) * 100, 1)))
n = len(lower); k = sum(1 for _, x in lower if x < 0)
print('1년 다 지난 무리', n, '· 그 뒤 1년 안에 첫날 종가보다 더 내려간 무리', k)
print('더 내려간 폭(첫날 종가 대비 1년 안 최저) 중앙', st.median(x for _, x in lower), '%', lower)
y25 = [r for r in rows if r[0].startswith('2025')]
print('2025 첫날', y25[0], '2025 마지막', y25[-1], '지금', rows[-1], '2025 첫날 대비', round((rows[-1][1]/y25[0][1]-1)*100, 1), '%')
