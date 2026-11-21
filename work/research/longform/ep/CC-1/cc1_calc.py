# CC-1 1억 계산 v2 (youtube-loop 2026-11-22) — 원문 대조 반영
#  KODEX 441640: 분배금 = 삼성자산운용 divid-info.do 50건(raw/kodex_divid_info_1122.json, 1차) · 종가 = 야후(삼성 product-earning 406일과 0원 차이, cmp_px_out_1122.txt)
#  TIGER 458730: 분배금 = 야후 + 2023-09-26 33원(야후 누락, 미래에셋 연간 합 2023 202 − 야후 169) · 종가 = 야후(2차, 운용사 일별 원표 못 받음 — 확인 안 함)
#  TIGER 끝값 11/20 14,505원 = 미래에셋 분배금 현황 화면 현재가(11/21 받음, raw tiger_dist_page_1121.txt 354행) 같은 값
#  가정: 시작일 종가로 1억 어치(소수 주), 분배금 15.4% 떼고, 받아 씀 = 현금으로 모음 / 다시 넣음 = 지급일 뒤 첫 거래일 종가로 삼. 매매 수수료·판 때 세금 뺌.
import json, datetime as dt
def ypx(t):
    out={}
    for f in (f'raw/{t}_chart_20261122.json', f'raw/{t}_recent_20261122.json'):   # 긴 기간 꼴은 11/18까지라 최근 1달(range=1mo)을 덧붙임
        r=json.load(open(f))['chart']['result'][0]
        out.update({dt.datetime.utcfromtimestamp(a+9*3600).date():c for a,c in zip(r['timestamp'],r['indicators']['quote'][0]['close']) if c})
    return out
def ydv(t):
    r=json.load(open(f'raw/{t}_chart_20261122.json'))['chart']['result'][0]
    return {dt.datetime.utcfromtimestamp(int(k)+9*3600).date():v['amount'] for k,v in r['events']['dividends'].items()}
K_px=ypx('441640.KS')   # 11/20 11,170 = 삼성 원문 같은 값
K_dv={}
for x in json.load(open('raw/kodex_divid_info_1122.json',encoding='utf-8'))['dividList']:
    b=dt.datetime.strptime(x['basicD'],'%Y%m%d').date(); p=dt.datetime.strptime(x['payD'],'%Y%m%d').date()
    K_dv[b]=(float(x['dividA']),p)
T_px=ypx('458730.KS'); T_dv={d:(a,d+dt.timedelta(days=4)) for d,a in ydv('458730.KS').items()}
T_dv[dt.date(2023,9,26)]=(33.0,dt.date(2023,10,5))
END=dt.date(2026,11,20)
if END not in T_px: print('TIGER 11/20 종가 없음 — 마지막 날', max(T_px))
def run(px,dv,start,reinv,tax=0.154):
    days=sorted(d for d in px if start<=d<=END); d0=days[0]; sh=1e8/px[d0]; cash=0; n=0; gross=0
    for b,(a,pay) in sorted(dv.items()):
        if b<=d0+dt.timedelta(days=1) or b>END: continue
        net=a*sh*(1-tax); n+=1; gross+=a
        if reinv:
            nd=[x for x in days if x>=pay]
            if nd: sh+=net/px[nd[0]]
            else: cash+=net
        else: cash+=net
    last=days[-1]; v=sh*px[last]
    return dict(시작=str(d0),끝=str(last),시작가=round(px[d0]),끝가=round(px[last]),분배횟수=n,주당분배합=round(gross),받은분배금_세후만원=round(cash/1e4),평가액만원=round(v/1e4),합만원=round((v+cash)/1e4))
for name,px,dv in [('KODEX 미국배당커버드콜액티브',K_px,K_dv),('TIGER 미국배당다우존스',T_px,T_dv)]:
    for s in [dt.date(2022,9,27),dt.date(2023,6,20),dt.date(2025,11,20)]:
        if s<min(px): continue
        for r in (False,True): print(name,s,'다시 넣음' if r else '받아 씀',run(px,dv,s,r))

# --- v2b (11/22 01시): 최대 낙폭(분배금 받아 씀 기준 합계 = 평가액 + 받은 분배금, 종가 기준) · 1억이면 매달 세후 분배금
def mdd(px,dv,start,tax=0.154):
    days=sorted(d for d in px if start<=d<=END); sh=1e8/px[days[0]]; cash=0; peak=0; worst=(0,None,None); pk_d=None
    evs=sorted((b,a) for b,(a,p) in dv.items() if b>days[0]+dt.timedelta(days=1))
    i=0
    for d in days:
        while i<len(evs) and evs[i][0]<=d: cash+=evs[i][1]*sh*(1-tax); i+=1
        tot=sh*px[d]+cash; pv=sh*px[d]
        if tot>peak: peak=tot; pk_d=d
        dd=tot/peak-1
        if dd<worst[0]: worst=(dd,pk_d,d)
    return round(worst[0]*100,1),str(worst[1]),str(worst[2])
def pxdd(px,start):
    days=sorted(d for d in px if start<=d<=END); peak=0; w=(0,None,None); pk=None
    for d in days:
        if px[d]>peak: peak=px[d]; pk=d
        if px[d]/peak-1<w[0]: w=(px[d]/peak-1,pk,d)
    return round(w[0]*100,1),str(w[1]),str(w[2])
for name,px,dv in [('KODEX',K_px,K_dv),('TIGER',T_px,T_dv)]:
    for s in [dt.date(2023,6,20),dt.date(2025,11,20)]:
        print(name,s,'합계 최대 낙폭(%·고점일·바닥일)',mdd(px,dv,s),'값만 최대 낙폭',pxdd(px,s))
sh=1e8/K_px[dt.date(2025,11,20)]
mon=[(str(b),a,round(a*sh*(1-0.154)/1e4,1)) for b,(a,p) in sorted(K_dv.items()) if dt.date(2025,11,21)<=b<=END]
print('KODEX 1억(2025-11-20 12,605원에 7,933주쯤) 매달 세후 만원:',mon)
sh=1e8/T_px[dt.date(2025,11,20)]
print('TIGER 1억 매달 세후 만원:',[(str(b),a,round(a*sh*(1-0.154)/1e4,1)) for b,(a,p) in sorted(T_dv.items()) if dt.date(2025,11,21)<=b<=END])
