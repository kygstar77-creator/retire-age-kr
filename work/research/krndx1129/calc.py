import json
c = json.load(open('raw/closes.json', encoding='utf-8'))
q, t, k, fx = c['QQQ'], c['133690.KS'], c['379810.KS'], c['KRW=X']
def peak(s, since='2025-01-01'):
    ks = sorted(x for x in s if x >= since); pk = max(ks, key=lambda d: s[d]); last = ks[-1]
    return pk, s[pk], last, s[last], (s[last]/s[pk]-1)*100
for n, s in (('QQQ', q), ('TIGER 133690', t), ('KODEX 379810', k), ('원달러', fx)):
    pk, pv, l, lv, dd = peak(s); print(f'{n}: 고점 {pk} {pv:,.2f} → {l} {lv:,.2f} 고점 대비 {dd:.1f}%')
# 같은 기간 원화로 바꾼 QQQ (QQQ*환율)
qk = {d: q[d]*fx[d] for d in q if d in fx}
pk, pv, l, lv, dd = peak(qk); print(f'QQQ×원달러: 고점 {pk} {pv:,.0f} → {l} {lv:,.0f} {dd:.1f}%')
# 한 달·석 달 변화
for since in ('2026-10-30', '2026-08-29', '2025-12-31'):
    def ch(s):
        ks = sorted(s); a = [d for d in ks if d <= since][-1]; return (s[ks[-1]]/s[a]-1)*100, a
    print(since, ' '.join(f'{n} {ch(s)[0]:+.1f}%({ch(s)[1]})' for n, s in (('QQQ', q), ('TIGER', t), ('KODEX', k), ('원달러', fx))))
# 일별: 한국 d 의 TIGER 등락 vs 그 전 미국 거래일 QQQ 등락
qd = sorted(q); td = sorted(t)
rows = []
for i in range(1, len(td)):
    d, p = td[i], td[i-1]
    us = [x for x in qd if x < d]
    if len(us) < 2: continue
    u1, u0 = us[-1], us[-2]
    if u1 < p: continue  # 그 사이 미국 거래 없으면 건너뜀
    rq = (q[u1]/q[u0]-1)*100; rt = (t[d]/t[p]-1)*100
    rows.append((d, u1, rq, rt))
import statistics as st
print('일 수', len(rows), '방향 같은 날', sum(1 for r in rows if (r[2] > 0) == (r[3] > 0)))
big = sorted(rows, key=lambda r: r[2])[:6] + sorted(rows, key=lambda r: -r[2])[:3]
for d, u, rq, rt in big: print(f'  미국 {u} QQQ {rq:+.2f}% → 한국 {d} TIGER {rt:+.2f}%')
for d, u, rq, rt in rows[-8:]: print(f'  최근 미국 {u} QQQ {rq:+.2f}% → 한국 {d} TIGER {rt:+.2f}%')
