import json,glob,os,re,statistics,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
sgg=json.load(open('research/seoul_sgg.json',encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]','',s or '0') or 0)
out={}
for lawd,name in sgg.items():
    cx=collections.defaultdict(list); meta={}
    for ym in ('202607','202608','202609'):
        f=f'research/rt/{lawd}_{ym}_trade.json'
        if not os.path.exists(f): continue
        for r in json.load(open(f,encoding='utf-8')):
            nm=r.get('aptNm','').strip()
            try: a=float(r.get('excluUseAr'))
            except: continue
            if not nm or not (80<=a<86): continue
            if r.get('cdealType') or r.get('buyerGbn')=='공공기관': continue
            p=num(r.get('dealAmount'))
            if p<=0: continue
            cx[(nm,r.get('umdNm'))].append(p/(a/3.3058))
            meta[(nm,r.get('umdNm'))]=r.get('buildYear')
    rows=[(k,statistics.median(v),len(v),meta[k]) for k,v in cx.items() if len(v)>=2]
    if len(rows)<5: continue
    rows.sort(key=lambda x:x[1])
    lo,hi=rows[0],rows[-1]
    out[name]=dict(n=len(rows),deals=sum(r[2] for r in rows),med=statistics.median(r[1] for r in rows),
        lo=[lo[0][0],lo[0][1],round(lo[1]),lo[2],lo[3]],hi=[hi[0][0],hi[0][1],round(hi[1]),hi[2],hi[3]],ratio=round(hi[1]/lo[1],2),
        p25=statistics.quantiles([r[1] for r in rows],n=4)[0],p75=statistics.quantiles([r[1] for r in rows],n=4)[2])
json.dump(out,open('research/gap0928/gap.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for n,d in sorted(out.items(),key=lambda x:-x[1]['ratio']):
    print(f"{n} 단지{d['n']} 거래{d['deals']} 중앙{d['med']:.0f} 배수{d['ratio']} p75/p25 {d['p75']/d['p25']:.2f} | 싼 {d['lo']} | 비싼 {d['hi']}")
