# 래미안원베일리(서울 서초구 반포동, 2023년 준공) 실거래 직접 계산 — 2026-11-22 firemap-write-b
# 원자료: raw/11650_*_trade.json·_rent.json (fetch.py, 국토교통부 실거래 API 11/22 받음)
# 해제(cdealType 'O') 뺌. 84㎡대 = 전용 80~85㎡.
import json, glob, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(kind):
    rows=[]
    for p in sorted(glob.glob(f'raw/11650_*_{kind}.json')): rows+=json.load(open(p,encoding='utf-8'))
    return [r for r in rows if '원베일리' in r.get('aptNm','')]
amt=lambda r:int(r['dealAmount'].replace(',',''))/1e4
ym=lambda r:f"{r['dealYear']}-{int(r['dealMonth']):02d}"
T=[r for r in load('trade') if r.get('cdealType','')!='O']
X=[r for r in load('trade') if r.get('cdealType','')=='O']
print('해제 건수(전 기간)',len(X))
def band(r,lo,hi): return lo<=float(r['excluUseAr'])<hi
B84=[r for r in T if band(r,80,85.5)]
print('== §1 84㎡대 달마다(건수·최저·최고·차이)')
by=collections.defaultdict(list)
for r in B84: by[ym(r)].append(r)
for k in sorted(by):
    v=[amt(r) for r in by[k]]
    print(k,len(v),f'{min(v):.2f}',f'{max(v):.2f}',f'차 {max(v)-min(v):.2f}', f'가운데 {st.median(v):.2f}')
print('== §2 2026-05 84㎡대 건별')
for r in sorted(by['2026-05'],key=amt):
    print(r['dealDay'].rjust(2),'일',r['aptDong'] or '-','동',r['floor'].rjust(2),'층',r['excluUseAr'],f'{amt(r):.2f}억',r['dealingGbn'],'등기',r['rgstDate'] or '-')
print('== §3 최근 1년(2025-11~2026-10) 84㎡대')
Y=[r for r in B84 if '2025-11'<=ym(r)<='2026-10']
v=[amt(r) for r in Y]; print(len(Y),'건 가운데',f'{st.median(v):.2f}','최저',min(v),'최고',max(v))
print('달별 건수', collections.Counter(ym(r) for r in Y))
print('== §4 해마다 84㎡대 같은 달 최대 차이(그해 가장 큰 달)')
for y in ('2023','2024','2025','2026'):
    best=None
    for k in by:
        if k.startswith(y) and len(by[k])>=3:
            vv=[amt(r) for r in by[k]]; d=max(vv)-min(vv)
            if not best or d>best[1]: best=(k,d,len(vv),min(vv),max(vv))
    print(y,best)
print('== §5 층으로 나눈 2026-05 84㎡대')
lo=[amt(r) for r in by['2026-05'] if int(r['floor'])<=5]; hi=[amt(r) for r in by['2026-05'] if int(r['floor'])>=10]
print('1~5층',len(lo),lo and st.median(lo),'10층+',len(hi),hi and st.median(hi))
print('== §6 59㎡대 2026-05·최근 1년')
B59=[r for r in T if band(r,59,60.5)]
m=[amt(r) for r in B59 if ym(r)=='2026-05']; print('5월',len(m),m and (min(m),max(m)))
yy=[amt(r) for r in B59 if '2025-11'<=ym(r)<='2026-10']; print('1년',len(yy),yy and (st.median(yy),min(yy),max(yy)))
print('== §7 전세(월세 0) 84㎡대 최근 1년')
R=[r for r in load('rent') if band(r,80,85.5) and r.get('monthlyRent','0').replace(',','') in ('0','')]
RY=[r for r in R if '2025-11'<=ym(r)<='2026-10']
rv=[int(r['deposit'].replace(',',''))/1e4 for r in RY]
print(len(rv),'건 가운데',rv and f'{st.median(rv):.2f}', rv and (min(rv),max(rv)))
print('== §8 2026-06~11 84㎡대 (5월 뒤)')
for k in sorted(by):
    if k>='2026-06': print(k,len(by[k]),[f'{amt(r):.1f}' for r in by[k]])
