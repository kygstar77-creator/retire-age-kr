# 10년 보유 손해 비율(거래일마다 산 경우) · 2006-01-02 값 위에 있던 날 비율 — ECOS 일별(raw_ecos.json), 지수 값만
import json, sys, bisect, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw_ecos.json', encoding='utf-8'))
for name in ('kosdaq', 'kospi'):
    rows = [r for r in d[name] if r[0] >= '20030102']; ds = [r[0] for r in rows]
    for Y in (5, 10):
        res = []
        for t, v in rows:
            tt = str(int(t[:4]) + Y) + t[4:]
            j = bisect.bisect_left(ds, tt)
            if j >= len(rows): break
            res.append((rows[j][1] / v - 1) * 100)
        print(name, f'{Y}년 보유', len(res), '번 · 손해', sum(x < 0 for x in res), f'({sum(x<0 for x in res)/len(res)*100:.1f}%) · 중간 {st.median(res):.1f}% · 최악 {min(res):.1f}% · 최고 {max(res):.1f}%')
q = [r for r in d['kosdaq'] if r[0] >= '20060102']
print('코스닥 2006-01-02(727.07) 뒤 거래일', len(q), '· 그 값보다 높게 끝난 날', sum(v > 727.07 for _, v in q), f'({sum(v>727.07 for _,v in q)/len(q)*100:.1f}%)')
