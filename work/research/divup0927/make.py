import json,sys,os,urllib.request,datetime
sys.path.insert(0,'.'); sys.stdout.reconfigure(encoding='utf-8')
import blogimg
Y=json.load(open('research/divup0927/yahoo.json',encoding='utf-8'))
# 회사 발표문으로 확인한 이전·새 배당(분기, 리얼티인컴만 월)
D=[('TMUS','티모바일',1.02,1.17,'9/24',4),('GEHC','GE헬스케어',0.035,0.04,'9/22',4),('PM','필립모리스',1.47,1.60,'9/18',4),
   ('MSFT','마이크로소프트',0.91,0.98,'9/15',4),('USB','US뱅코프',0.52,0.54,'9/8',4),('VICI','비치 프로퍼티스',0.45,0.46,'9/3',4),
   ('OGE','OGE에너지',0.425,0.42875,'9/23',4),('O','리얼티인컴',0.2710,0.2715,'9/8',12)]
rows=[];rows2=[];out=[]
for t,k,a,b,dt,n in sorted(D,key=lambda x:-(x[3]/x[2])):
    y=Y[t];p=y['price'];up=(b/a-1)*100;yl=b*n/p*100;fromhi=(p/y['hi52']-1)*100;fromlo=(p/y['lo52']-1)*100
    out.append(f'{t} {k} 발표{dt} {a}->{b} 인상 {up:.2f}% 연 {b*n:.4f} 종가 {p} 배당률 {yl:.2f}% 52주고 {y["hi52"]} 대비 {fromhi:.1f}% 52주저 {y["lo52"]} 대비 +{fromlo:.1f}%')
    rows.append([f'{k}({t})',dt,f'{a:g}달러',f'{b:g}달러',f'{up:.1f}%'])
    rows2.append([f'{k}({t})',f'{p:.2f}달러',f'{yl:.2f}%',f'{fromhi:.0f}%'])
print('\n'.join(out))
open('research/divup0927/calc_result.txt','w',encoding='utf-8').write('\n'.join(out))
S='출처: 각 회사 배당 발표문 · 시세 야후 파이낸스(9월 25일 종가)'
blogimg.table('research/divup0927/pkg/img/02.png','9월에 배당을 올린 미국 종목 8곳',['종목','발표일','이전','새 배당','인상률'],rows,hl_col=4,src=S,note='리얼티인컴은 월 배당, 나머지는 분기 배당')
rows2.sort(key=lambda r:-float(r[2][:-1]))
blogimg.table('research/divup0927/pkg/img/03.png','새 배당 기준 배당률과 52주 최고가 대비',['종목','9월 25일 종가','배당률','52주 최고가 대비'],rows2,hl_col=2,src=S,note='배당률 = 새 배당을 1년으로 늘려 종가로 나눈 값')
# 티모바일 1년 주가
u='https://query1.finance.yahoo.com/v8/finance/chart/TMUS?range=1y&interval=1wk'
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20))['chart']['result'][0]
xs=[datetime.datetime.utcfromtimestamp(t).strftime('%y.%m') for t in d['timestamp']];ys=d['indicators']['quote'][0]['close']
pr=[(x,v) for x,v in zip(xs,ys) if v]
xs=[a for a,_ in pr];ys=[round(b,2) for _,b in pr]
blogimg.line('research/divup0927/pkg/img/04.png','티모바일 주가 1년(주간 종가)',xs,ys,marks=[(xs[-1],ys[-1],f'{ys[-1]:.0f}달러','red')],unit='달러',src='출처: 야후 파이낸스')
print('tmus weekly max',max(ys),xs[ys.index(max(ys))],'last',ys[-1],xs[-1])
