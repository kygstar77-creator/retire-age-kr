# ymf: 코스피 한 달 급락 뒤 1년 — Yahoo ^KS11 월봉(1997-01~) 직접 계산
import json,datetime as D,statistics as S,os,sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d=json.load(open('raw/ks11_1mo.json'))['chart']['result'][0]
q=d['indicators']['quote'][0]; mon=[]
for i,t in enumerate(d['timestamp']):
    if q['close'][i] is None: continue
    dt=D.datetime.fromtimestamp(t,D.UTC)+D.timedelta(hours=9); k=(dt.year,dt.month)
    if mon and mon[-1][0]==k: mon[-1]=(k,q['close'][i]); continue
    mon.append((k,q['close'][i]))
res={}
for th in (-0.10,-0.15):
    ev=[]
    for i in range(1,len(mon)):
        r=mon[i][1]/mon[i-1][1]-1
        if r<=th and mon[i][0]!=(2026,10):
            f=mon[i+12][1]/mon[i][1]-1 if i+12<len(mon) else None
            nxt=[c for _,c in mon[i+1:i+13]]
            dd=min(nxt)/mon[i][1]-1 if len(nxt)==12 else None
            ev.append(dict(m='%d-%02d'%mon[i][0],ret=round(r*100,1),f12=None if f is None else round(f*100,1),more=None if dd is None else round(dd*100,1)))
    fs=[e['f12'] for e in ev if e['f12'] is not None]; mo=[e['more'] for e in ev if e['more'] is not None]
    res[str(th)]=dict(n=len(ev),n12=len(fs),up=sum(f>0 for f in fs),median=S.median(fs),min=min(fs),max=max(fs),more_n=sum(m<0 for m in mo),more_min=min(mo),ev=ev)
    print(th,{k:v for k,v in res[str(th)].items() if k!='ev'})
    for e in ev: print('  ',e)
print('months',len(mon),mon[0][0],mon[-1][0])
json.dump(res,open('calc_out.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
