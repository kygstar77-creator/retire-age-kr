# 야후 종가 대조 — 네이버페이 증권 일별 시세(fchart) 2차 출처로 몇 곳 맞춰 본다
import urllib.request,re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
E={e['code']:e for e in json.load(open('raw/exday.json',encoding='utf-8'))}
bad=0;n=0;out=[]
for code in ['105560','055550','086790','316140','000270','005930','033780','071320','004090','005490','017670','030200','088980','003550','010950']:
    if code not in E: continue
    e=E[code]
    b=urllib.request.urlopen(f'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count=400&requestType=0',timeout=20).read().decode('euc-kr','ignore')
    d={x[0]:float(x[4]) for x in (r.split('|') for r in re.findall(r'data="([^"]+)"',b))}
    a=(d.get(e['prev'].replace('-','')),d.get(e['ex'].replace('-','')))
    ok=a[0] is not None and abs(a[0]-e['p0'])<1 and abs(a[1]-e['p1'])<1
    n+=1; bad+=not ok
    out.append(f"{e['name']} {e['prev']} 야후 {e['p0']:.0f} 네이버 {a[0]} | {e['ex']} 야후 {e['p1']:.0f} 네이버 {a[1]} {'같음' if ok else '다름'}")
out.append(f'대조 {n}곳 중 다름 {bad}')
print('\n'.join(out)); open('raw/naver_check.txt','w',encoding='utf-8').write('\n'.join(out))
