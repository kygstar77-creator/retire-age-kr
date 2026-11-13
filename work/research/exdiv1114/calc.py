# 배당락일 하루 주가 변화 ÷ 1주당 배당금. 코스피 지수 등락을 뺀 값도 같이. 결과 calc_out.txt
import json,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8')
R=json.load(open('raw/dart_divrows.json',encoding='utf-8'))
E=json.load(open('raw/exday.json',encoding='utf-8'))
L=[]
P=lambda *a: (print(*a), L.append(' '.join(map(str,a))))
dec=[r for r in R if r['rec'] and r['rec']<'2026-01-01']; nxt=[r for r in R if r['rec'] and r['rec']>='2026-01-01']
P('## 1. 기준일 — 코스피 2025 사업연도 결산배당 결정',len(R),'곳')
P('12월 말(2025년) 기준일',len(dec),'곳',f'{len(dec)/len(R)*100:.1f}%',' / 2026년 1~4월 기준일',len(nxt),'곳',f'{len(nxt)/len(R)*100:.1f}%')
from collections import Counter
P('2026년 기준일 달별',sorted(Counter(r['rec'][:7] for r in nxt).items()))
num=lambda x: float(x.replace(',','')) if x and x not in('-',) else None
# 시가배당률 높은 쪽 비중
for name,g in (('12월',dec),('2026년',nxt)):
    y=[num(r['yld']) for r in g if num(r['yld'])]
    P(name,'시가배당률 가운데값',round(st.median(y),2),'% (',len(y),'곳)')
P()
P('## 2. 배당락일 하루 — 전날 종가 대비 하락폭 ÷ 1주당 배당금')
rows=[]
for e in E:
    d=num(e['dps'])
    if not d or not e['p0'] or not e['p1']: continue
    drop=e['p0']-e['p1']
    kret=(e['k1']/e['k0']-1) if e['k0'] and e['k1'] else 0
    adj=e['p0']*(1+kret)-e['p1']   # 지수만큼 움직였다면의 가격 대비 하락
    rows.append(dict(e,d=d,ratio=drop/d,adjr=adj/d,yl=d/e['p0']*100))
P('계산된 곳',len(rows))
for name,f in (('전체',lambda r:True),('12월 말 기준(락일 12/29)',lambda r:r['rec']<'2026-01-01'),('2026년 기준',lambda r:r['rec']>='2026-01-01'),('배당률 3% 이상',lambda r:r['yl']>=3),('배당률 5% 이상',lambda r:r['yl']>=5)):
    g=[r for r in rows if f(r)]
    if not g: continue
    P(f'{name}: {len(g)}곳 · 하락/배당금 가운데값 {st.median(r["ratio"] for r in g):.2f} · 지수 뺀 값 가운데값 {st.median(r["adjr"] for r in g):.2f} · 배당금보다 더 빠진 곳 {sum(r["ratio"]>1 for r in g)}곳({sum(r["ratio"]>1 for r in g)/len(g)*100:.0f}%) · 오히려 오른 곳 {sum(r["p1"]>r["p0"] for r in g)}곳({sum(r["p1"]>r["p0"] for r in g)/len(g)*100:.0f}%)')
P()
P('## 3. 12/29 코스피', [ (e['prev'],e['k0'],e['ex'],e['k1']) for e in E if e['ex']=='2025-12-29'][:1])
P('## 4. 배당률 5% 이상 상위 15곳(배당률 순)')
for r in sorted([r for r in rows if r['yl']>=5],key=lambda r:-r['yl'])[:15]:
    P(r['name'],r['rec'],'락일',r['ex'],'배당',r['d'],'전날',round(r['p0']),'당일',round(r['p1']),f"배당률 {r['yl']:.1f}% 하락/배당 {r['ratio']:.2f}")
P('## 5. 시가총액 큰 이름(예시)')
for nm in ('삼성전자','SK하이닉스','현대차','KB금융','신한지주','하나금융지주','우리금융지주','KT&G','SK텔레콤','KT','기아','POSCO홀딩스'):
    for r in rows:
        if r['name']==nm: P(nm,r['rec'],'락일',r['ex'],'배당',r['d'],'전날',round(r['p0']),'당일',round(r['p1']),f"하락/배당 {r['ratio']:.2f}")
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(L))
L.append('')
L.append('## 6. 배당금 발표(이사회 결정일)와 기준일 순서')
L.append(f"2026년 기준 {len(nxt)}곳 중 기준일 전에 결정 {sum(1 for r in nxt if r['dec'] and r['dec']<r['rec'])}곳 (같은 날 {sum(1 for r in nxt if r['dec']==r['rec'])})")
L.append(f"12월 말 기준 {len(dec)}곳 중 기준일 뒤에 결정 {sum(1 for r in dec if r['dec'] and r['dec']>r['rec'])}곳")
L.append('## 7. 배당락일 코스피')
for d0 in ('2025-12-29','2026-02-26'):
    e=[e for e in E if e['ex']==d0][0]; L.append(f"{e['prev']} {e['k0']:.2f} → {d0} {e['k1']:.2f} ({(e['k1']/e['k0']-1)*100:.1f}%)")
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(L))
