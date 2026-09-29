import json,sys,re,statistics as S,collections as C; sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('raw.json',encoding='utf-8'))['data']
def n(x): return float(re.sub(r'[^\d.]','',str(x or '0')) or 0)
def rows(ym,k): return [r for key,v in d.items() if key.split('_',2)[1]==ym and key.endswith(k) and (k!='offi_trade' or True) for r in v if not (k=='offi_trade' and 'offi_rent' in key)]
for ym in ('202609','202608'):
    T=[r for key,v in d.items() if f'_{ym}_offi_trade' in key for r in v]
    Rr=[r for key,v in d.items() if f'_{ym}_offi_rent' in key for r in v]
    canc=[r for r in T if r.get('cdealType')]; T2=[r for r in T if not r.get('cdealType')]
    pub=[r for r in T2 if r.get('buyerGbn')=='공공기관']
    print(f'== {ym} 매매 신고 {len(T)} 해제 {len(canc)} 남은 {len(T2)} 공공기관매수 {len(pub)} 전월세 {len(Rr)}')
    print('마지막 계약일', max((int(r['dealMonth']),int(r['dealDay'])) for r in T2))
    if ym=='202608': continue
    g=C.Counter((r['offiNm'],r['sggNm'],r['umdNm'],r['buildYear'],r['dealDay']) for r in pub); print('공공기관 매수 묶음',g.most_common(8))
    for key,cnt in g.most_common(3):
        xs=[r for r in pub if (r['offiNm'],r['sggNm'],r['umdNm'],r['buildYear'],r['dealDay'])==key]
        a=[n(r['dealAmount']) for r in xs]; ar=[n(r['excluUseAr']) for r in xs]
        print(' ',key,cnt,'가격중앙',S.median(a),'합',sum(a),'면적',min(ar),max(ar),'매도',C.Counter(r['slerGbn'] for r in xs))
    P=[r for r in T2 if r.get('buyerGbn')!='공공기관']
    py=lambda r:n(r['dealAmount'])/(n(r['excluUseAr'])/3.305785)
    print('일반 거래',len(P),'평당중앙',round(S.median(py(r) for r in P)),'한채중앙',S.median(n(r['dealAmount']) for r in P))
    bg=C.defaultdict(list)
    for r in P: bg[r['sggNm']].append(r)
    for s in sorted(bg,key=lambda s:-len(bg[s])): print('  ',s,len(bg[s]),'평당',round(S.median(py(r) for r in bg[s])),'한채',S.median(n(r['dealAmount']) for r in bg[s]))
    top=sorted(P,key=lambda r:-n(r['dealAmount']))[:3]
    for r in top: print('  최고',r['sggNm'],r['umdNm'],r['offiNm'],r['excluUseAr'],r['dealAmount'],r['floor'],r['buildYear'])
    cn=C.Counter((r['offiNm'],r['sggNm']) for r in P).most_common(5); print('  단지 거래 많은 곳',cn)
    M=[r for r in Rr if n(r.get('monthlyRent'))>0]; J=[r for r in Rr if n(r.get('monthlyRent'))==0]
    print('전월세',len(Rr),'월세',len(M),f'{len(M)/len(Rr)*100:.1f}%','월세중앙',S.median(n(r['monthlyRent']) for r in M),'월세보증금중앙',S.median(n(r['deposit']) for r in M),'전세',len(J),'전세중앙',S.median(n(r['deposit']) for r in J))
    br=C.defaultdict(list)
    for r in M: br[r['sggNm']].append(n(r['monthlyRent']))
    for s in sorted(br,key=lambda s:-S.median(br[s])): print('   월세',s,len(br[s]),S.median(br[s]))
    print('   전월세 구별 건수',C.Counter(r['sggNm'] for r in Rr).most_common())
