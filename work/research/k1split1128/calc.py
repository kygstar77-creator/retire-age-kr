# k1split1128 — 코스피 하루 -5% 넘게 빠진 날(무리 첫날, 60거래일 안 다시 빠진 날은 같은 무리) 1천만원을
# 1·3·6·12번(21거래일 간격, 같은 금액)으로 넣고 첫날+252거래일(1년)·+504거래일(2년) 종가로 평가.
# KOSPI-1 calc3.py와 같은 정의(무리·간격·평가일). 지수 값만 — 배당·세금·수수료·보수 뺌, 안 넣은 돈 이자 0.
import json, statistics as st
rows = json.load(open('raw/kospi_daily_ecos_1126.json'))
ch = [(rows[i][0], rows[i][1], (rows[i][1]/rows[i-1][1]-1)*100, i) for i in range(1,len(rows))]
eps=[]; last=-999
for d,v,c,i in ch:
    if c<=-5:
        if i-last>60: eps.append((d,v,c,i))
        last=i
print('무리 첫날', len(eps), [e[0] for e in eps])
T=10_000_000
def val(i,n,h):
    end=rows[i+h][1]
    return sum((T/n)/rows[i+21*k][1] for k in range(n))*end
for h,lab in [(252,'1년'),(504,'2년')]:
    res={n:[] for n in (1,3,6,12)}; days=[]
    for d,v,c,i in eps:
        if i+h>=len(rows): continue
        days.append(d)
        for n in res: res[n].append(val(i,n,h))
    print(f'== {lab} 뒤 · {len(days)}번 · 마지막 첫날 {days[-1]}')
    for n,L in res.items():
        print(f'{n:>2}번: 중앙 {st.median(L)/1e4:,.0f}만 · 최저 {min(L)/1e4:,.0f}만 · 최고 {max(L)/1e4:,.0f}만 · 원금 넘은 {sum(x>T for x in L)}번 · 원금 아래 {sum(x<T for x in L)}번')
    best=[max(res, key=lambda n: res[n][k]) for k in range(len(days))]
    print('가장 많이 남은 방법 횟수', {n:best.count(n) for n in res})
    for k,d in enumerate(days):
        print(' ',d, ' · '.join(f'{n}번 {res[n][k]/1e4:,.0f}만' for n in res))
print('== 첫날 뒤 1년 안 가장 낮은 종가(첫날 종가 대비)')
for d,v,c,i in eps:
    if i+252>=len(rows): continue
    seg=rows[i:i+253]; lo=min(seg,key=lambda r:r[1])
    print(' ',d, f'첫날 {v:,.2f}', f'가장 낮은 {lo[0]} {lo[1]:,.2f}', f'{(lo[1]/v-1)*100:+.1f}%', f'1년 뒤 {(rows[i+252][1]/v-1)*100:+.1f}%')
