import json,re,collections,statistics,sys
sys.stdout.reconfigure(encoding='utf-8')
num=lambda s:int(re.sub(r'[^\d]','',s or '0') or 0)
raw=json.load(open('research/aptmkt0929/raw.json',encoding='utf-8'))
city=lambda n:n.split()[0]
S={'202609':[], '202608':[]}; pub=collections.Counter(); cancel=collections.Counter()
for k,rows in raw.items():
    n,ym=k.split('|')
    if not rows: continue
    for r in rows:
        r['gu']=n; r['city']=city(n)
        if r.get('cdealType'): cancel[ym]+=1; continue
        if r.get('buyerGbn')=='공공기관': pub[ym]+=1; continue
        S[ym].append(r)
for ym in S: print(ym,'건수',len(S[ym]),'해제',cancel[ym],'공공기관',pub[ym],'중앙(만원)',statistics.median(num(r['dealAmount']) for r in S[ym]))
c9=collections.Counter(r['city'] for r in S['202609']); c8=collections.Counter(r['city'] for r in S['202608'])
for c,n in c9.most_common(): 
    m9=statistics.median(num(r['dealAmount']) for r in S['202609'] if r['city']==c)
    ps=[num(r['dealAmount'])/float(r['excluUseAr'])*3.3058 for r in S['202609'] if r['city']==c]
    print('시',c,n,'8월',c8[c],'중앙',m9,'평당중앙(만원)',round(statistics.median(ps)))
gx=collections.Counter(r['gu'] for r in S['202609']); print('구 상위',gx.most_common(6))
cx=collections.Counter((r['gu'],r['umdNm'],r['aptNm']) for r in S['202609']); print('단지 상위',cx.most_common(8))
for r in sorted(S['202609'],key=lambda r:-num(r['dealAmount']))[:6]: print('비싼',r['gu'],r['umdNm'],r['aptNm'],r['excluUseAr'],r['dealAmount'],'9/'+r['dealDay'],r['floor'],r['buildYear'],r.get('dealingGbn'))
d9=collections.Counter(int(r['dealDay']) for r in S['202609']); print('계약일 최대',max(d9))
