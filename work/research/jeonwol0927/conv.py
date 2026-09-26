import sys,os,glob,json,collections,statistics,re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import heatmap_re as H
rows=[]
for f in glob.glob(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\rt\*_2026*_rent.json'):
    if '_offi_' in f: continue
    rows+=json.load(open(f,encoding='utf-8'))
rows=list({json.dumps(r,sort_keys=True,ensure_ascii=False):r for r in rows}.values()); print("dedup",len(rows))

C=collections.defaultdict(lambda:([],[]))
for r in rows:
    g=H.sgg_of(r); nm=(r.get('aptNm') or '').strip(); ar=H.num(r.get('excluUseAr'))
    if not g or not nm or ar<=0: continue
    d=H.num(r.get('deposit')); m=H.num(r.get('monthlyRent'))
    k=(g,nm,int(ar//5*5))
    if m==0: C[k][0].append(d)
    else: C[k][1].append((d,m))
per=collections.defaultdict(list); allv=[]
for k,(js,ws) in C.items():
    if len(js)<2 or not ws: continue
    J=statistics.median(js)
    for d,m in ws:
        if J-d < J*0.2: continue   # 보증금 차이가 너무 작으면 튄다
        v=m*12/(J-d)*100
        if 0<v<20: per[k[0]].append(v); allv.append(v)
print('pairs',len(allv),'seoul median',round(statistics.median(allv),2))
res=sorted(((statistics.median(v),g,len(v)) for g,v in per.items() if len(v)>=30),reverse=True)
for x in res: print(x[1],round(x[0],2),x[2])
