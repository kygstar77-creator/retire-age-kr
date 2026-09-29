# 동 단위 아파트 실거래 계산 — 원자료 work/research/rt/<구코드>_<월>_{trade,rent}.json (국토부 RTMS)
# 쓰는 법: py -3.12 calc.py 11680 개포동
import json,collections,statistics as S,re,sys,os
sys.stdout.reconfigure(encoding='utf-8')
RT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','rt')
SGG,DONG=sys.argv[1],sys.argv[2]
def num(x): return float(re.sub(r'[^\d.]','',str(x or '0')) or 0)
def load(kind,yms,dong=DONG):
    out=[];tot=0;dropped=0
    for ym in yms:
        for r in json.load(open(f'{RT}/{SGG}_{ym}_{kind}.json',encoding='utf-8')):
            if dong and r.get('umdNm','').strip()!=dong: continue
            tot+=1
            if kind=='trade' and (r.get('cdealType') or r.get('buyerGbn')=='공공기관'): dropped+=1; continue
            out.append(r)
    return out,tot,dropped
def k(r): return (r['aptNm'].strip(), round(num(r['excluUseAr'])))
def g(rows):
    d=collections.defaultdict(list)
    for r in rows: d[k(r)].append(num(r['dealAmount']))
    return d
def py(r): return num(r['dealAmount'])/(num(r['excluUseAr'])/3.305785)
NOW=['202607','202608','202609']; LY=['202507','202508','202509']
cur,t,dr=load('trade',NOW); print(f'2026 7~9월 {DONG} 매매 신고',t,'해제·공공 제외',dr,'남은',len(cur))
ly,t2,dr2=load('trade',LY); print('2025 7~9월',t2,dr2,len(ly))
print('마지막 계약일', max(f"{r['dealYear']}-{int(r['dealMonth']):02d}-{int(r['dealDay']):02d}" for r in cur))
print('\n[2026 7~9월 거래 전부]')
for r in sorted(cur,key=lambda r:(r['aptNm'],num(r['excluUseAr']),r['dealMonth'],r['dealDay'])):
    print(r['aptNm'],r['excluUseAr'],r['dealAmount'],r['floor']+'층',f"{int(r['dealMonth'])}/{int(r['dealDay'])}",'준공',r['buildYear'],'평당',round(py(r)))
C,L=g(cur),g(ly)
print('\n[단지·면적별 중앙값 비교] 단지,면적,2026건,2026중앙,2025건,2025중앙,변화%')
for key in sorted(C):
    c=S.median(C[key]); l=S.median(L[key]) if key in L else None
    print(key[0],key[1],len(C[key]),c, len(L.get(key,[])),l, f'{(c/l-1)*100:+.1f}' if l else '-')
allc=[num(r['dealAmount']) for r in cur]; print('\n2026 7~9월 전체 중앙값',S.median(allc),'최저',min(allc),'최고',max(allc))
print('평당 중앙(전용50㎡이상)',round(S.median([py(r) for r in cur if num(r['excluUseAr'])>=50])),'건',len([r for r in cur if num(r['excluUseAr'])>=50]))
print('작년 평당 중앙(전용50㎡이상)',round(S.median([py(r) for r in ly if num(r['excluUseAr'])>=50])),'건',len([r for r in ly if num(r['excluUseAr'])>=50]))
print('\n[84~85㎡]')
for r in sorted([r for r in cur if 84<=num(r['excluUseAr'])<86],key=lambda r:-num(r['dealAmount'])):
    print(r['aptNm'],r['excluUseAr'],r['dealAmount'],r['floor']+'층',f"{int(r['dealMonth'])}/{int(r['dealDay'])}",r['buildYear'])
rc,_,_=load('rent',NOW)
J=collections.defaultdict(list)
for r in rc:
    if num(r.get('monthlyRent'))==0 and r.get('contractType','')=='신규': J[k(r)].append(num(r['deposit']))
print('\n[전세가율 = 전세 신규 중앙값 / 매매 중앙값, 같은 단지·면적]')
for key in sorted(C):
    if key in J: print(key[0],key[1],'매매',S.median(C[key]),'전세',S.median(J[key]),len(J[key]),'건',f'{S.median(J[key])/S.median(C[key])*100:.1f}%')
# 구 전체 동별
allg,_,_=load('trade',NOW,dong=None); ally,_,_=load('trade',LY,dong=None)
D=collections.defaultdict(list); DY=collections.defaultdict(list)
for r in allg:
    if num(r['excluUseAr'])>=50: D[r['umdNm'].strip()].append(py(r))
for r in ally:
    if num(r['excluUseAr'])>=50: DY[r['umdNm'].strip()].append(py(r))
print('\n[구 내 동별 평당 중앙(전용50↑)] 동,올해,건,작년')
for d in sorted(D,key=lambda d:-S.median(D[d])):
    if len(D[d])>=5: print(d,round(S.median(D[d])),len(D[d]),round(S.median(DY[d])) if DY.get(d) else '-')
print('구 전체',round(S.median([x for v in D.values() for x in v])),sum(len(v) for v in D.values()),round(S.median([x for v in DY.values() for x in v])))
