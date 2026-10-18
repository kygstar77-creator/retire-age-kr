import json, glob, os, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
RT=r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\rt'
def num(s): return float(str(s or 0).replace(',','') or 0)
ms=sorted({os.path.basename(f).split('_')[1] for f in glob.glob(os.path.join(RT,'11470_2*_rent.json')) if os.path.basename(f).split('_')[1]>='202511'})
R=[]
for m in ms:
    f=os.path.join(RT,f'11470_{m}_rent.json'); d=json.load(open(f,encoding='utf-8')); R+=d if isinstance(d,list) else d.get('rows',[])
R=[r for r in R if r.get('umdNm')=='목동']
print(ms[0],ms[-1],len(R)); print(list(R[0].keys()))
cmp=json.load(open('cmp.json',encoding='utf-8'))
for c in cmp:
    a=c['apt']; ar=c['area']
    rs=[r for r in R if r['aptNm']==a and abs(num(r['excluUseAr'])-ar)<2.5 and num(r.get('monthlyRent'))==0]
    new=[r for r in rs if (r.get('contractType') or '')!='갱신']
    v=[num(r['deposit']) for r in new]
    print(a, ar, '전세(신규·월세0) n',len(v),'중앙',st.median(v) if v else None, '매매중앙',c['all'], '비율', round(st.median(v)/c['all']*100,1) if v else None, '갭', (c['all']-st.median(v)) if v else None)
