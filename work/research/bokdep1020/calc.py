# bokdep1020 계산 — 원자료 raw/ecos_1020.json · raw/ecos_ktb3_daily.json · raw/finlife_deposit_1020.json (2026-10-20 조회)
import json
e=json.load(open('raw/ecos_1020.json',encoding='utf-8'))
k=dict((a,float(b)) for a,b,c in json.load(open('raw/ecos_ktb3_daily.json',encoding='utf-8')))
base=dict((a,float(b)) for a,b,c in e['base']); dep=dict((a,float(b)) for a,b,c in e['dep12'])
print('기준금리 월말', {m:base[m] for m in ['202512','202606','202607','202608','202609']})
print('1~2년 정기예금 신규', {m:dep[m] for m in ['202512','202601','202606','202607','202608']})
print('1~6월(기준금리 그대로) 예금 변화', round(dep['202606']-dep['202601'],2))
print('6→8월(기준금리 +0.50) 예금 변화', round(dep['202608']-dep['202606'],2), '7월', round(dep['202607']-dep['202606'],2),'8월', round(dep['202608']-dep['202607'],2))
print('국고채3년', k['20251230'],k['20260630'], '변화', round(k['20260630']-k['20251230'],3))
print('8/26→8/27', k['20260826'],k['20260827'], round(k['20260827']-k['20260826'],3), ' 7/15→7/16', k['20260715'],k['20260716'])
print('10/19', k['20261019'], ' 최근 최고', max((v,d) for d,v in k.items() if d>='20260801'))
cd=dict((a,float(b)) for a,b,c in e['cd91']); print('CD91 6/1',cd['20260601'],'10/19',cd['20261019'])
tax=0.154
for r in (3.6,3.65,3.85):
  print(f'1억 1년 {r}% 세후', round(1e8*r/100*(1-tax)))
print('0.25%p 세후 차이', round(1e8*0.0025*(1-tax)), ' 0.09%p', round(1e8*0.0009*(1-tax)))
f=json.load(open('raw/finlife_deposit_1020.json',encoding='utf-8'))
big=('국민은행','신한은행','하나은행','우리은행','농협은행주식회사')
for x in f:
  if x['기간']=='12' and any(b in (x['은행'] or '') for b in big) and x['금리유형']=='단리': print(x['공시월'],x['은행'],x['상품'],x['금리'],x['최고금리'])
