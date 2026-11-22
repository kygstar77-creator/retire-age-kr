# 리츠 ETF 1억 넣었다면 — 분배금(세후 15.4% 뗌, 재투자 안 함)+남은 평가액. 야후 raw/*.json(fetch.py 11/22 받음).
# 사용: py -3.12 calc.py > calc_out.txt
import json,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
NAMES={'429740.KS':'PLUS K리츠','329200.KS':'TIGER 리츠부동산인프라','476800.KS':'KODEX 한국부동산리츠인프라','182480.KS':'TIGER 미국MSCI리츠(합성 H)','VNQ':'VNQ(참고, 달러)'}
def load(t):
    r=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[datetime.date.fromtimestamp(x) for x in r['timestamp']]; c=r['indicators']['quote'][0]['close']
    px=[(d,v) for d,v in zip(ts,c) if v]
    dv=sorted((datetime.date.fromtimestamp(x['date']),x['amount']) for x in r.get('events',{}).get('dividends',{}).values())
    return px,dv
def on_or_after(px,d):
    for x in px:
        if x[0]>=d: return x
def run(t,start,tax=0.154,amt=1e8):
    px,dv=load(t); s=on_or_after(px,start); e=px[-1]
    sh=amt/s[1]; got=[(d,a) for d,a in dv if s[0]<d<=e[0]]
    gross=sum(a for _,a in got)*sh; net=gross*(1-tax)
    val=sh*e[1]
    return dict(t=t,start=s[0],sp=s[1],end=e[0],ep=e[1],price_pct=(e[1]/s[1]-1)*100,n=len(got),per_share=sum(a for _,a in got),net=net,gross=gross,val=val,total=val+net,total_pct=(val+net)/amt*100-100,yld=sum(a for _,a in got)/s[1]*100)
for label,start in [('1년',datetime.date(2025,11,20)),('2년',datetime.date(2024,11,20)),('3년',datetime.date(2023,11,20))]:
    print('##',label,'시작',start)
    for t in NAMES:
        if t=='476800.KS' and start<datetime.date(2024,3,7): continue
        r=run(t,start,tax=0 if t=='VNQ' else 0.154)
        print(f"{NAMES[t]}: {r['start']} {r['sp']:.0f} → {r['end']} {r['ep']:.0f} 주가 {r['price_pct']:+.1f}% · 분배 {r['n']}번 1주 {r['per_share']:.0f}(시작가 대비 {r['yld']:.1f}%) · 1억 → 세후 분배 {r['net']/1e4:,.0f}만 + 평가 {r['val']/1e4:,.0f}만 = {r['total']/1e4:,.0f}만({r['total_pct']:+.1f}%)")
print('## 최근 12번 분배금(1주, 원)')
for t in ['429740.KS','329200.KS','476800.KS','182480.KS']:
    px,dv=load(t); last=dv[-12:]
    print(NAMES[t], [f"{d.strftime('%y.%m')} {a:.0f}" for d,a in last], '합',sum(a for _,a in last),'최저',min(a for _,a in last),'최고',max(a for _,a in last), f"지금가 {px[-1][1]:.0f} 대비 {sum(a for _,a in last)/px[-1][1]*100:.1f}%")
print('## 고점')
for t in ['429740.KS','329200.KS','476800.KS','182480.KS']:
    px,_=load(t); hi=max(px,key=lambda x:x[1]); print(NAMES[t],'최고',hi[0],f"{hi[1]:.0f}",'지금',f"{px[-1][1]:.0f}",f"{(px[-1][1]/hi[1]-1)*100:+.1f}%")
print('## 특별배당 반영 전 보통 달(2026년 6~8월 평균)로 1년 치면')
for t in ['429740.KS','476800.KS','329200.KS']:
    px,dv=load(t); n=[a for d,a in dv if datetime.date(2026,6,1)<=d<=datetime.date(2026,8,31)]
    m=sum(n)/len(n); print(NAMES[t],'6~8월',n,f'평균 {m:.1f} x12 = {m*12:.0f}원, 지금가 {px[-1][1]:.0f} 대비 {m*12/px[-1][1]*100:.1f}%')
    sp=[(d,a) for d,a in dv if d>=datetime.date(2026,9,1)]; print('   9월 뒤',[(str(d),a) for d,a in sp],'보통 달보다 더 받은 몫 합',round(sum(a-m for _,a in sp),1))
print('## 1억 세후 월 분배(지금가로 1억, 최근 12번 평균 / 보통 달)')
for t in ['429740.KS','476800.KS','329200.KS','182480.KS']:
    px,dv=load(t); last=dv[-12:]; sh=1e8/px[-1][1]
    n=[a for d,a in dv if datetime.date(2026,6,1)<=d<=datetime.date(2026,8,31)]; m=sum(n)/len(n)
    print(NAMES[t], f"최근12번 평균 월 {sum(a for _,a in last)/12*sh*0.846/1e4:.1f}만원 · 보통 달 {m*sh*0.846/1e4:.1f}만원")
