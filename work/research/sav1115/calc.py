# sav1115 계산 — 한국은행 ECOS 121Y002(예금은행 수신금리, 신규취급액 기준) + 금감원 finlife 은행 적금(202610 공시)
import json,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('raw/ecos_rates.json',encoding='utf-8'))
sav=dict(d['BEABAA2122']); dep=dict(d['BEABAA2118']); base=dict(d['base'])
print('[ECOS] 9월 정기적금(1-2년)',sav['202609'],'· 정기예금(1년)',dep['202609'],'· 차',round(sav['202609']-dep['202609'],2),'· 기준금리',base['202609'])
print('[ECOS] 1년 전 2025-09 적금',sav['202509'],'예금',dep['202509'],'→ 적금 +',round(sav['202609']-sav['202509'],2),'예금 +',round(dep['202609']-dep['202509'],2))
m=sorted(set(sav)&set(dep)); lo=[t for t in m if sav[t]<dep[t]]
print('[ECOS] 2012-01~2026-09',len(m),'달 중 적금<예금',len(lo),'달',round(len(lo)/len(m)*100,1),'%')
# 구간: 기준금리 오른 시기 vs 내린 시기
def runs(ts):
    out=[];s=ts[0];p=ts[0]
    for t in ts[1:]:
        y,mm=int(p[:4]),int(p[4:]);n=f'{y+(mm==12)}{(mm%12)+1:02d}'
        if t!=n: out.append((s,p)); s=t
        p=t
    out.append((s,p)); return out
print('[ECOS] 적금<예금 이어진 구간',runs(lo))
for t in ['201707','201811','202108','202301','202507','202607','202609']: print('  기준금리',t,base.get(t))
fin=json.load(open('raw/fin_saving.json',encoding='utf-8'));b={(x['fin_co_no'],x['fin_prdt_cd']):x for x in fin['base']}
r=[(b[(o['fin_co_no'],o['fin_prdt_cd'])]['kor_co_nm'],b[(o['fin_co_no'],o['fin_prdt_cd'])]['fin_prdt_nm'],o['rsrv_type_nm'],o['intr_rate'],o['intr_rate2']) for o in fin['opt'] if o['save_trm']=='12']
print('[finlife] 공시월',sorted(set(x['dcls_month'] for x in fin['base'])),'1년 줄',len(r),'은행',len(set(x[0] for x in r)))
print('[finlife] 기본 가운데값',st.median([x[3] for x in r]),'최고',max(x[3] for x in r),'· 우대 포함 최고',max(x[4] for x in r))
print('[finlife] 최고금리 7% 상품',[x[:2] for x in r if x[4]>=7])
print('[finlife] 최고금리 6% 이상',sum(x[4]>=6 for x in r),'· 기본 3.5% 이상',sum(x[3]>=3.5 for x in r))
print('[finlife] 7% 상품 기본금리',[(x[1],x[3]) for x in r if x[4]>=7])
# 이자: 월 30만원 12개월 단리, 세금 15.4%
for rate in (3.21,3.57,7.0):
    i=300000*rate/100*78/12; print(f'[이자] 월 30만원 1년 {rate}% 세전 {i:,.0f} 세후 {i*(1-0.154):,.0f} · 넣은 돈 360만원 대비 세전 {i/3600000*100:.2f}%')
