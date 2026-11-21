# CC-1 분배금 원문 대조 — 삼성 KODEX 441640 분배 이력(운용사) ↔ 야후, 미래에셋 TIGER 458730 연간 합(운용사) ↔ 야후 (youtube-loop 2026-11-22)
import json, urllib.request, datetime, collections
def yahoo(t):
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1640995200&period2=1795000000&interval=1d&events=div'
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
    json.dump(r,open(f'raw/{t}_chart_20261122.json','w'))
    r=r['chart']['result'][0]
    return {datetime.datetime.utcfromtimestamp(int(k)+9*3600).date():v['amount'] for k,v in r.get('events',{}).get('dividends',{}).items()}
d=json.load(open('raw/kodex_2ETFH4_1122.json',encoding='utf-8'))['info']['divideList']
sam={datetime.date(int(x['BASIC_D'][:4]),int(x['BASIC_D'][4:6]),int(x['BASIC_D'][6:])):x['DIVID_A'] for x in d}
y=yahoo('441640.KS')
print('삼성 건수',len(sam),min(sam),max(sam),'야후 건수',len(y),min(y),max(y))
# 같은 달끼리 맞대기
sm=collections.defaultdict(float); ym=collections.defaultdict(float)
for k,v in sam.items(): sm[(k.year,k.month)]+=v
for k,v in y.items(): ym[(k.year,k.month)]+=v
diff=[(m,sm.get(m),round(ym.get(m,0),2)) for m in sorted(set(sm)|set(ym)) if abs(sm.get(m,0)-ym.get(m,0))>0.5]
print('달별 다른 곳(삼성,야후):',diff)
print('삼성 연도 합',{yr:sum(v for k,v in sam.items() if k.year==yr) for yr in range(2022,2027)})
print('야후 연도 합',{yr:round(sum(v for k,v in y.items() if k.year==yr)) for yr in range(2022,2027)})
t=yahoo('458730.KS')
print('TIGER 야후 연도 합',{yr:round(sum(v for k,v in t.items() if k.year==yr)) for yr in range(2023,2027)},'건수',len(t))
print('TIGER 미래에셋 연도 합(2026.11.19 기준) 2023 202 · 2024 443 · 2025 430 · 2026 361')
# --- 2차: divid-info.do(50건, 2022-10~) 로 달별 다시 맞대기
dl=json.load(open('raw/kodex_divid_info_1122.json',encoding='utf-8'))['dividList']
sam2={datetime.date(int(x['basicD'][:4]),int(x['basicD'][4:6]),int(x['basicD'][6:])):float(x['dividA']) for x in dl}
s2=collections.defaultdict(float)
for k,v in sam2.items(): s2[(k.year,k.month)]+=v
print('divid-info 건수',len(sam2),min(sam2),max(sam2))
print('달별 다른 곳(삼성 divid-info, 야후):',[(m,s2.get(m),round(ym.get(m,0),2)) for m in sorted(set(s2)|set(ym)) if abs(s2.get(m,0)-ym.get(m,0))>0.5])
print('삼성 annualTrend 2022 153 · 2023 634 · 2024 934 · 2025 1130 · 2026 1083')
json.dump({str(k):v for k,v in sorted(sam2.items())},open('kodex_div_samsung.json','w'),ensure_ascii=False)
