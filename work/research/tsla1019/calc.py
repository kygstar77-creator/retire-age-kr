import json,datetime,os
H=os.path.dirname(os.path.abspath(__file__))
y=json.load(open(os.path.join(H,'raw','y.json'),encoding='utf-8'))['chart']['result'][0]
ts=y['timestamp'];c=y['indicators']['quote'][0]['close']
days=[(datetime.datetime.fromtimestamp(t-4*3600, datetime.UTC).date(),v) for t,v in zip(ts,c) if v]
idx={d:i for i,(d,v) in enumerate(days)}
es=json.load(open(os.path.join(H,'raw','es.json'),encoding='utf-8'))['data']['earningsSurpriseTable']['rows']
print('발표(장 마감 뒤) · 실적 EPS/예상 · 발표일 종가 → 다음 날 종가 · 변화 · 5거래일 뒤')
for r in es:
    m,dd,yy=map(int,r['dateReported'].split('/'));d=datetime.date(yy,m,dd)
    i=idx[d];a=days[i][1];b=days[i+1][1];f=days[min(i+5,len(days)-1)][1]
    print(f"{d} · {r['eps']}/{r['consensusForecast']} ({r['percentageSurprise']}%) · {a:.2f} → {b:.2f} ({days[i+1][0]}) · {100*(b/a-1):+.2f}% · 5일 {100*(f/a-1):+.2f}%")
last=days[-1];print('최근 종가',last[0],round(last[1],2))
yr=[v for d,v in days if d>last[0]-datetime.timedelta(days=365)]
hi=max(yr);lo=min(yr);dh=[d for d,v in days if v==hi][0];dl=[d for d,v in days if v==lo][0]
print(f'52주 최고 {hi:.2f}({dh}) 최저 {lo:.2f}({dl}) · 최고 대비 {100*(last[1]/hi-1):+.2f}%')
ytd=[v for d,v in days if d.year==last[0].year][0];print(f'올해 첫 거래일 종가 {ytd:.2f} · 올해 {100*(last[1]/ytd-1):+.2f}%')
ly=[(d,v) for d,v in days if d<=last[0]-datetime.timedelta(days=365)][-1];print(f'1년 전 {ly[0]} {ly[1]:.2f} · {100*(last[1]/ly[1]-1):+.2f}%')
# 100만원 아닌 100주 아님: 1천만원 투자 시 다음날 변화 (원화 환산 X, 달러 기준 비율만)
print('1천만원 7월 다음 날 변화(달러 기준 비율):', round(10_000_000*(319.69/374.01-1)))
q=[(384122,480126,'인도'),(22496,28236,'매출(백만달러)'),(923,398,'영업이익(백만달러)')]
for a,b,n in q: print(n, a,'→',b, f'{100*(b/a-1):+.1f}%')
print('3분기 인도 vs 2분기', f'{100*(486532/480126-1):+.2f}%', 'vs 작년 3분기', f'{100*(486532/497099-1):+.2f}%')
