# 방배동 아파트 단지별 실거래 계산 — 원자료 work/research/rt/11650_<월>_{trade,rent}.json (국토부 RTMS, LAWD_CD=11650)
import json,collections,statistics as S,re,sys,os
sys.stdout.reconfigure(encoding='utf-8')
RT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','rt')
def num(x): return float(re.sub(r'[^\d.]','',str(x or '0')) or 0)
def load(kind,yms,drop=True):
    out=[];tot=0;dropped=0
    for ym in yms:
        for r in json.load(open(f'{RT}/11650_{ym}_{kind}.json',encoding='utf-8')):
            if r.get('umdNm','').strip()!='방배동': continue
            tot+=1
            if kind=='trade' and drop and (r.get('cdealType') or r.get('buyerGbn')=='공공기관'): dropped+=1; continue
            out.append(r)
    return out,tot,dropped
def k(r): return (r['aptNm'].strip(), round(num(r['excluUseAr'])))
def g(rows):
    d=collections.defaultdict(list)
    for r in rows: d[k(r)].append(num(r['dealAmount']))
    return d
cur,t,dr=load('trade',['202607','202608','202609']); print('2026 7~9월 방배동 매매 신고',t,'해제·공공 제외',dr,'남은',len(cur))
ly,t2,dr2=load('trade',['202507','202508','202509']); print('2025 7~9월',t2,dr2,len(ly))
old,t3,dr3=load('trade',['202110','202111','202112']); print('2021 10~12월',t3,dr3,len(old))
print('\n[2026 7~9월 거래 전부]')
for r in sorted(cur,key=lambda r:(r['aptNm'],num(r['excluUseAr']),r['dealMonth'],r['dealDay'])):
    print(r['aptNm'],r['excluUseAr'],r['dealAmount'],r['floor']+'층',f"{r['dealYear']}-{int(r['dealMonth']):02d}-{int(r['dealDay']):02d}",'준공',r['buildYear'])
C,L,O=g(cur),g(ly),g(old)
print('\n[단지·면적별 중앙값 비교] 단지,면적,2026건,2026중앙,2025건,2025중앙,변화%,2021건,2021중앙,변화%')
for key in sorted(C):
    c=S.median(C[key]); l=S.median(L[key]) if key in L else None; o=S.median(O[key]) if key in O else None
    print(key[0],key[1],len(C[key]),c, len(L.get(key,[])),l, f'{(c/l-1)*100:+.1f}' if l else '-', len(O.get(key,[])),o, f'{(c/o-1)*100:+.1f}' if o else '-')
allc=[num(r['dealAmount']) for r in cur]; print('\n2026 7~9월 전체 중앙값',S.median(allc),'최저',min(allc),'최고',max(allc))
rc,_,_=load('rent',['202607','202608','202609'])
print('rent keys',list(rc[0].keys()))
print('계약구분',collections.Counter(r.get('contractType','') for r in rc))
J=collections.defaultdict(list)
for r in rc:
    if num(r.get('monthlyRent'))==0 and r.get('contractType','')=='신규': J[k(r)].append(num(r['deposit']))
print('\n[전세 신규계약, 2026 7~9월] 단지,면적,건,중앙,최저,최고')
for key in sorted(J): print(key[0],key[1],len(J[key]),S.median(J[key]),min(J[key]),max(J[key]))
print('\n[전세가율 = 전세 신규 중앙값 / 매매 중앙값, 같은 단지·면적, 둘 다 있는 것만]')
for key in sorted(C):
    if key in J: print(key[0],key[1],f'{S.median(J[key])/S.median(C[key])*100:.1f}%')
