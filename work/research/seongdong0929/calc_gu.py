# 성동구 동별 아파트 매매 건수·평당가 — 2025년 7~9월 vs 2026년 7~9월 (국토부 RTMS 11200)
import json,collections,statistics as S,re,sys,os
sys.stdout.reconfigure(encoding='utf-8')
RT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','rt')
def num(x): return float(re.sub(r'[^\d.]','',str(x or '0')) or 0)
def load(yms):
    out=[];dr=0
    for ym in yms:
        for r in json.load(open(f'{RT}/11200_{ym}_trade.json',encoding='utf-8')):
            if r.get('cdealType') or r.get('buyerGbn')=='공공기관': dr+=1; continue
            out.append(r)
    return out,dr
import os as _o
M=_o.environ.get('MONTHS','789')
now,d1=load(['2026'+m.zfill(2) for m in ['07','08','09'] if m[-1] in M]); ly,d2=load(['2025'+m.zfill(2) for m in ['07','08','09'] if m[-1] in M])
print('성동구 2026 7~9월',len(now),'(제외',d1,') 2025 7~9월',len(ly),'(제외',d2,')')
for ym in ['202507','202508','202509','202607','202608','202609']:
    rows=[r for r in json.load(open(f'{RT}/11200_{ym}_trade.json',encoding='utf-8')) if not (r.get('cdealType') or r.get('buyerGbn')=='공공기관')]
    print(ym,len(rows),'마지막 계약일',max(int(r['dealDay']) for r in rows))
# 2025 9월은 9/22까지 계약분만 셈(올해와 같은 조건)
lastday=max([int(r['dealDay']) for r in now if int(r['dealMonth'])==9] or [31])
ly2=[r for r in ly if not (int(r['dealMonth'])==9 and int(r['dealDay'])>lastday)]
print('올해 9월 마지막 계약일',lastday,'→ 작년도 9월',lastday,'일까지로 자르면',len(ly2))
def py(r): return num(r['dealAmount'])/(num(r['excluUseAr'])/3.305785)
N=collections.defaultdict(list); L=collections.defaultdict(list)
for r in now: N[r['umdNm'].strip()].append(r)
for r in ly2: L[r['umdNm'].strip()].append(r)
print('동,올해건,작년건(같은 날짜까지),올해평당중앙(50↑),작년평당중앙(50↑)')
for d in sorted(set(N)|set(L),key=lambda d:-len(L.get(d,[]))):
    a=[py(r) for r in N.get(d,[]) if num(r['excluUseAr'])>=50]; b=[py(r) for r in L.get(d,[]) if num(r['excluUseAr'])>=50]
    print(d,len(N.get(d,[])),len(L.get(d,[])),round(S.median(a)) if len(a)>=3 else '-',round(S.median(b)) if len(b)>=3 else '-',len(a),len(b))
a=[py(r) for r in now if num(r['excluUseAr'])>=50]; b=[py(r) for r in ly2 if num(r['excluUseAr'])>=50]
print('구 전체 평당중앙',round(S.median(a)),len(a),round(S.median(b)),len(b))
print('\n[올해 거래 많은 단지]')
for (n,c) in collections.Counter(r['aptNm'].strip()+'|'+r['umdNm'] for r in now).most_common(10): print(n,c)
print('\n[올해 최고가 5]')
for r in sorted(now,key=lambda r:-num(r['dealAmount']))[:5]: print(r['umdNm'],r['aptNm'],r['excluUseAr'],r['dealAmount'],f"{r['dealMonth']}/{r['dealDay']}")
