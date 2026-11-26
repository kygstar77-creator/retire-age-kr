# h6pair1128 계산 — raw/11680_<월>_{trade,rent}.json(국토부 실거래, fetch.py 2026-11-26 받음)
# §1 은마 매매 전체(해제·공공기관 뺌) · §2 평형별 계약 기간 묶음 가운데 값 · §3 월별 건수(은마·강남구 전체) · §4 은마 전월세 월별·순수전세 가운데 값 · §5 강남구 80~86㎡ 대조군
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
RT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'raw')
MS=['202510','202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610','202611']
def num(s): return float(str(s or '0').replace(',','') or 0)
def load(kind,ms=MS):
    out=[]
    for m in ms:
        d=json.load(open(os.path.join(RT,f'11680_{m}_{kind}.json'),encoding='utf-8')); out+=[r for r in d if isinstance(r,dict) and 'aptNm' in r]
    return out
def ymd(r): return f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}.{str(r['dealDay']).zfill(2)}"
ALL=load('trade')
E=[r for r in ALL if r['aptNm'].replace(' ','')=='은마' and r['umdNm']=='대치동']
canc=[r for r in E if r.get('cdealType')]
T=[r for r in E if not r.get('cdealType') and r.get('buyerGbn')!='공공기관']
print(f'# §1 은마 매매 {len(T)}건(해제 {len(canc)}건 뺌) · 계약월 {MS[0]}~{MS[-1]} · 직거래 {sum(1 for r in T if r.get("dealingGbn")=="직거래")}건')
g=collections.defaultdict(list)
for r in T: g[round(num(r['excluUseAr']))].append(r)
for a,rows in sorted(g.items()):
    rows.sort(key=ymd)
    print(f'\n## 전용 {a}㎡ {len(rows)}건')
    for r in rows: print(f"{ymd(r)} {num(r['dealAmount'])/1e4:.2f}억 {r['floor']}층 {r.get('dealingGbn','')}")
    am=[num(r['dealAmount']) for r in rows]
    print(f'최고 {max(am)/1e4:.2f}억 · 최저 {min(am)/1e4:.2f}억 · 중앙 {st.median(am)/1e4:.2f}억')
print('\n# §2 평형별 묶음 가운데 값')
G=[('2025.10~12',lambda d:d<'2026.01'),('2026.01~06',lambda d:'2026.01'<=d<'2026.07'),('2026.07~09',lambda d:'2026.07'<=d<'2026.10'),('2026.10~11',lambda d:d>='2026.10')]
for a,rows in sorted(g.items()):
    meds=[]
    for lab,f in G:
        v=[num(r['dealAmount'])/1e4 for r in rows if f(ymd(r))]; meds.append(st.median(v))
        print(f'{a}㎡ {lab}: {len(v)}건 가운데 {st.median(v):.2f}억 (최저 {min(v):.2f} 최고 {max(v):.2f})')
    print(f'{a}㎡ 첫→끝 {meds[0]:.2f}→{meds[-1]:.2f}억 ({meds[-1]-meds[0]:+.2f}억, {meds[-1]/meds[0]*100:.1f}%) · 인가 전 반년 몫 {meds[1]-meds[0]:+.2f}억({(meds[1]-meds[0])/(meds[-1]-meds[0])*100:.0f}%)')
print('\n# §3 월별 매매 건수 — 은마 · 강남구 아파트 전체(해제 뺌)')
ce=collections.Counter(ymd(r)[:7] for r in T)
ca=collections.Counter(ymd(r)[:7] for r in ALL if not r.get('cdealType'))
for k in sorted(ca): print(k,'은마',ce.get(k,0),'· 강남구',ca[k])
yr=[ca[k] for k in sorted(ca) if '2025.11'<=k<='2026.10']
print(f'강남구 2025.11~2026.10 {len(yr)}달 합 {sum(yr)} · 월 평균 {sum(yr)/len(yr):.1f} · 9~10월 평균 {(ca["2026.09"]+ca["2026.10"])/2:.1f}')
print(f'은마 2026.09~10 {ce["2026.09"]+ce["2026.10"]}건 / {len(T)}건 = {(ce["2026.09"]+ce["2026.10"])/len(T)*100:.0f}%')
R=[r for r in load('rent') if r['aptNm'].replace(' ','')=='은마' and r['umdNm']=='대치동']
print(f'\n# §4 은마 전월세 {len(R)}건 · 월별')
cr=collections.Counter(ymd(r)[:7] for r in R)
for k in sorted(cr): print(k,cr[k])
for a in (77,84):
    j=[num(r['deposit']) for r in R if round(num(r['excluUseAr']))==a and num(r.get('monthlyRent',0))==0]
    jn=[num(r['deposit']) for r in R if round(num(r['excluUseAr']))==a and num(r.get('monthlyRent',0))==0 and ymd(r)>='2026.07']
    if j: print(f'{a}㎡ 순수전세 {len(j)}건 가운데 {st.median(j)/1e4:.2f}억 · 2026.07~ {len(jn)}건 가운데 {st.median(jn)/1e4 if jn else 0:.2f}억')
print('\n# §5 강남구 80~86㎡ 대조군(1년 전 2025.10~12 ↔ 요즘 2026.10~11, 해제·공공기관·직거래 뺌)')
def ld(ms): return [r for r in load('trade',ms) if not r.get('cdealType') and r.get('buyerGbn')!='공공기관' and r.get('dealingGbn')!='직거래' and 80<=num(r['excluUseAr'])<=86]
def grp(rows):
    gg=collections.defaultdict(list)
    for r in rows: gg[(r['umdNm'],r['aptNm'].replace(' ',''))].append(num(r['dealAmount']))
    return gg
ga,gb=grp(ld(['202510','202511','202512'])),grp(ld(['202610','202611']))
rows=sorted((st.median(gb[k])/st.median(ga[k])-1,k,len(ga[k]),len(gb[k]),st.median(ga[k]),st.median(gb[k])) for k in ga if k in gb)
for p,k,na,nb,a,b in rows: print(f"{k[0]} {k[1]} · {na}건 {a/1e4:.2f}억 → {nb}건 {b/1e4:.2f}억 · {p*100:+.1f}%")
ps=[r[0] for r in rows]
print(f'단지 {len(rows)}곳 · 변화 가운데 값 {st.median(ps)*100:+.1f}% · 내린 곳 {sum(p<0 for p in ps)} · 오른 곳 {sum(p>0 for p in ps)}')
big=[r[0] for r in rows if r[2]>=2 and r[3]>=2]
print(f'양쪽 2건 이상 {len(big)}곳 · 가운데 값 {st.median(big)*100:+.1f}%')
print('\n# §6 5층 이상만 묶음 가운데 값')
for a,rows in sorted(g.items()):
    hi=[r for r in rows if int(r['floor'])>=5]
    for lab,f in G:
        v=[num(r['dealAmount'])/1e4 for r in hi if f(ymd(r))]
        print(f'{a}㎡ 5층+ {lab}: {len(v)}건 가운데 {st.median(v) if v else 0:.3f}억')
print('은마 월별 최다:', ce.most_common(2))
print('\n# §7 은마 순수전세(월세 0) 보증금 가운데 값 — 1년 전 묶음 ↔ 2026.07~')
for a in (77,84):
    for lab,f in [('2025.10~12',lambda d:d<'2026.01'),('2026.07~',lambda d:d>='2026.07')]:
        v=[num(r['deposit'])/1e4 for r in R if round(num(r['excluUseAr']))==a and num(r.get('monthlyRent',0))==0 and f(ymd(r))]
        print(f'{a}㎡ 전세 {lab}: {len(v)}건 가운데 {st.median(v):.3f}억')
