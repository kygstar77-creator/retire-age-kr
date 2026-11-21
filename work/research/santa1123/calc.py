# 산타랠리·12월 직접 계산 (2026-11-21 firemap-write-b) — 원자료 raw/*_20261121.json (야후 chart API 일별 종가)
import json, datetime, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(n):
    r = json.load(open(f'raw/{n}_20261121.json'))['chart']['result'][0]
    ts = r['timestamp']; c = r['indicators']['quote'][0]['close']
    out = []
    for t, v in zip(ts, c):
        if v is None: continue
        d = (datetime.datetime(1970,1,1) + datetime.timedelta(seconds=t + 9*3600)).date()  # 야후 ts=뉴욕 개장 무렵, +9h로 날짜 안전
        out.append((d, v))
    # 같은 날짜 중복 제거
    dd = {}
    for d, v in out: dd[d] = v
    return sorted(dd.items())
def pct(a, b): return (b / a - 1) * 100
def med(x): return st.median(x) if x else float('nan')
for name, first_year in [('gspc', 1928), ('ndx', 1986), ('sp500tr', 1988)]:
    S = load(name)
    print(f'=== {name}  {S[0][0]} ~ {S[-1][0]}  {S[-1][1]:.2f}')
    idx = {d: i for i, (d, v) in enumerate(S)}
    # 달 마지막 거래일 종가
    last = {}
    for d, v in S: last[(d.year, d.month)] = (d, v)
    months = sorted(last)
    mret = {}
    for i in range(1, len(months)):
        mret[months[i]] = pct(last[months[i-1]][1], last[months[i]][1])
    # 달별 상승 비율·중간
    print('달 | 해 수 | 오른 해 | 비율 | 중간 | 평균')
    for m in range(1, 13):
        xs = [r for (y, mm), r in mret.items() if mm == m and y >= first_year and (y, mm) != (2026, 11)]
        up = sum(1 for r in xs if r > 0)
        print(f'{m:2d} | {len(xs)} | {up} | {up/len(xs)*100:.1f}% | {med(xs):.2f} | {st.mean(xs):.2f}')
    # 산타 기간: 12월 마지막 5거래일 + 1월 첫 2거래일, 기준 = 그 앞 거래일 종가
    santa = {}
    for y in range(first_year, 2026):
        dec = [i for i, (d, v) in enumerate(S) if d.year == y and d.month == 12]
        jan = [i for i, (d, v) in enumerate(S) if d.year == y + 1 and d.month == 1]
        if len(dec) < 6 or len(jan) < 2: continue
        base = dec[-5] - 1; end = jan[1]
        santa[y] = (S[base][0], S[end][0], pct(S[base][1], S[end][1]))
    xs = [v[2] for v in santa.values()]
    up = sum(1 for r in xs if r > 0)
    print(f'산타 기간 {len(xs)}번 · 오른 번 {up} ({up/len(xs)*100:.1f}%) · 중간 {med(xs):.2f}% · 평균 {st.mean(xs):.2f}%')
    # 아무 7거래일
    allw = [pct(S[i][1], S[i+7][1]) for i in range(len(S) - 7) if S[i][0].year >= first_year and S[i+7][0] < datetime.date(2026, 1, 1)]
    up7 = sum(1 for r in allw if r > 0)
    print(f'아무 7거래일 {len(allw)}번 · 오른 {up7/len(allw)*100:.1f}% · 중간 {med(allw):.2f}% · 평균 {st.mean(allw):.2f}%')
    # 최근 10번 산타
    print('최근 산타:', ' '.join(f"{y}:{santa[y][2]:+.1f}" for y in sorted(santa)[-12:]))
    # 가장 나빴던/좋았던 산타
    w = sorted(santa.items(), key=lambda kv: kv[1][2])
    print('나쁜 3:', [(y, round(v[2], 1)) for y, v in w[:3]], '좋은 3:', [(y, round(v[2], 1)) for y, v in w[-3:]])
    # 11월이 빠진 해의 12월
    nd = [(y, mret[(y, 11)], mret[(y, 12)]) for y in range(first_year, 2026) if (y, 11) in mret and (y, 12) in mret]
    neg = [x for x in nd if x[1] < 0]; pos = [x for x in nd if x[1] >= 0]
    for lab, g in [('11월 빠진 해', neg), ('11월 오른 해', pos)]:
        dec = [x[2] for x in g]; u = sum(1 for r in dec if r > 0)
        print(f'{lab} {len(g)}번 · 12월 오른 {u} ({u/len(g)*100:.1f}%) · 12월 중간 {med(dec):.2f}%')
    # 11월 -3% 넘게 빠진 해
    big = [x for x in nd if x[1] <= -3]
    u = sum(1 for x in big if x[2] > 0)
    print(f'11월 -3% 이하 {len(big)}번 · 12월 오른 {u} · 목록', [(x[0], round(x[1],1), round(x[2],1)) for x in big])
    # 산타 빠진 해 → 다음 해(1~12월) 수익
    nxt = {}
    for y in santa:
        if (y, 12) in last and (y + 1, 12) in last and y + 1 <= 2025:
            nxt[y] = pct(last[(y, 12)][1], last[(y + 1, 12)][1])
    sn = [nxt[y] for y in nxt if santa[y][2] <= 0]; sp = [nxt[y] for y in nxt if santa[y][2] > 0]
    print(f'산타 빠진 해 {len(sn)}번 → 다음 해 오른 {sum(1 for r in sn if r>0)} 중간 {med(sn):.1f}% | 산타 오른 해 {len(sp)}번 → 다음 해 오른 {sum(1 for r in sp if r>0)} 중간 {med(sp):.1f}%')
    # 올해 11월 지금까지
    oct_end = last[(2026, 10)]
    print(f'2026 11월 지금까지: 10/31 {oct_end[0]} {oct_end[1]:.2f} → {S[-1][0]} {S[-1][1]:.2f} = {pct(oct_end[1], S[-1][1]):.2f}%')
    hi = max(S, key=lambda x: x[1]); print('최고 종가', hi[0], round(hi[1], 2), f'지금 {pct(hi[1], S[-1][1]):.1f}%')
    print()
