# 방배동 단지별 평당가 순위와 서초구 동별 비교 — 원자료 rt/11650_*_trade.json (국토부 RTMS)
import json,re,statistics as S,collections as C,os,sys
sys.stdout.reconfigure(encoding='utf-8')
RT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','rt')
def n(x): return float(re.sub(r'[^\d.]','',str(x or '0')) or 0)
def load(yms):
    o=[]
    for ym in yms: o+=json.load(open(f'{RT}/11650_{ym}_trade.json',encoding='utf-8'))
    return [r for r in o if not r.get('cdealType') and r.get('buyerGbn')!='공공기관']
cur=load(['202607','202608','202609']); ly=load(['202507','202508','202509'])
pp=lambda r:n(r['dealAmount'])/(n(r['excluUseAr'])/3.3058)
print('last deal',max((int(r['dealMonth']),int(r['dealDay'])) for r in cur))
for lab,rows in (('2026',cur),('2025',ly)):
    D=C.defaultdict(list)
    for r in rows: D[r['umdNm'].strip()].append(pp(r))
    print(lab,'서초구 전체',len(rows),round(S.median(pp(r) for r in rows)))
    for k,v in sorted(D.items(),key=lambda x:-S.median(x[1])): print(' ',lab,k,len(v),round(S.median(v)))
B=[r for r in cur if r['umdNm'].strip()=='방배동' and n(r['excluUseAr'])>=50]
G=C.defaultdict(list)
for r in B: G[(r['aptNm'].strip(),r['buildYear'])].append((pp(r),n(r['excluUseAr']),n(r['dealAmount'])))
print('\n방배동 전용50㎡이상',len(B),'평당중앙',round(S.median(pp(r) for r in B)))
for k,v in sorted(G.items(),key=lambda x:-S.median(a for a,_,_ in x[1])):
    print(k[0],k[1],len(v),round(S.median(a for a,_,_ in v)),[ (round(b),int(c)) for _,b,c in v])
L=[r for r in ly if r['umdNm'].strip()=='방배동' and n(r['excluUseAr'])>=50]
print('\n방배동 50㎡이상 1년 전',len(L),round(S.median(pp(r) for r in L)))
