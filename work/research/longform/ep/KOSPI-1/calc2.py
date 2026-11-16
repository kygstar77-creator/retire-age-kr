# KOSPI-1 계산 2 — 지난 값만(ECOS 802Y001 일별 종가). 예측 없음.
import json, statistics as st, collections
rows = json.load(open('kospi_daily_ecos.json'))
ch = [(rows[i][0], rows[i][1], (rows[i][1]/rows[i-1][1]-1)*100, i) for i in range(1,len(rows))]
# 1) 해마다 -5% 이하·-8% 이하 날 수
y5=collections.Counter(d[:4] for d,v,c,i in ch if c<=-5); y8=collections.Counter(d[:4] for d,v,c,i in ch if c<=-8)
print('해마다 하루 -5% 이하 날 수(0인 해 생략):', dict(sorted(y5.items())))
print('해마다 하루 -8% 이하 날 수:', dict(sorted(y8.items())))
# 2) 무리로 묶기: -5% 이하 날 중 앞 -5% 날과 60거래일 넘게 떨어진 첫날만
eps=[]; last=-999
for d,v,c,i in ch:
    if c<=-5:
        if i-last>60: eps.append((d,v,c,i))
        last=i
print('\n무리(60거래일 안 묶음) 첫날 수', len(eps))
res=[]
for d,v,c,i in eps:
    f1=rows[i+252][1] if i+252<len(rows) else None
    f3=rows[i+756][1] if i+756<len(rows) else None
    # 그날 종가를 다시 넘은 데 걸린 거래일(그 전날 종가 기준)
    prev=rows[i-1][1]; back=None
    for k in range(i+1,len(rows)):
        if rows[k][1]>=prev: back=k-i; break
    lo=min(r[1] for r in rows[i:i+253]) if i+1<len(rows) else v
    res.append((d,c,v,f1,f3,back,lo))
    print(f"{d} {c:+.2f}% 종가 {v:,.2f} | 1년 뒤 {'' if f1 is None else f'{(f1/v-1)*100:+.1f}%'} | 3년 뒤 {'' if f3 is None else f'{(f3/v-1)*100:+.1f}%'} | 전날 값 되찾기 {back}거래일 | 그 뒤 1년 최저 {(lo/v-1)*100:+.1f}%")
one=[(f1/v-1)*100 for d,c,v,f1,f3,b,lo in res if f1]
print('\n무리 첫날 1년 뒤: 편수', len(one), '오른 편', sum(x>0 for x in one), '중앙', round(st.median(one),1))
bk=[b for *_,b,lo in res if b]
print('전날 값 되찾기 거래일 중앙', st.median(bk), '최장', max(bk))
# 3) 1천만원 넣었다면(무리 첫날 종가) 1년 뒤 금액 중앙·최저·최고 (배당 뺀 지수 값만)
amt=sorted(round(10_000_000*(1+x/100)) for x in one)
print('1천만원 → 1년 뒤(지수만, 배당·세금·수수료 뺌) 최저', amt[0], '중앙', amt[len(amt)//2], '최고', amt[-1])
# 4) 2026년 흐름
y=[r for r in rows if r[0].startswith('2026')]
pk=max(y,key=lambda r:r[1]); lo=min(y,key=lambda r:r[1])
print('\n2026 첫날', y[0], '최고', pk, '최저', lo, '마지막', y[-1], '연초 대비', f'{(y[-1][1]/y[0][1]-1)*100:+.1f}%', '최고 대비', f'{(y[-1][1]/pk[1]-1)*100:+.1f}%')
up=sorted(ch,key=lambda x:-x[2])[:8]
print('하루 상승 상위 8:', [(d,round(c,2)) for d,v,c,i in up])
print('2026 하루 ±5% 넘은 날 수', sum(1 for d,v,c,i in ch if d.startswith('2026') and abs(c)>=5))
