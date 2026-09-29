import sys,json,os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import apis
dv=apis.dividends('XOM',years=6)
print('배당(배당락일,금액) 최근 12:',dv[-12:])
d=apis._j('https://query1.finance.yahoo.com/v8/finance/chart/XOM?range=5y&interval=1wk',t=25)
r=d['chart']['result'][0]; m=r['meta']
print('meta',{k:m.get(k) for k in ['regularMarketPrice','regularMarketTime','fiftyTwoWeekHigh','fiftyTwoWeekLow','currency','exchangeName','longName']})
q=r['indicators']['quote'][0]['close']
json.dump({'ts':[__import__('datetime').datetime.utcfromtimestamp(t).strftime('%Y-%m-%d') for t in r['timestamp']],'close':q,'divs':dv},open('data.json','w',encoding='utf-8'),ensure_ascii=False)
d2=apis._j('https://query1.finance.yahoo.com/v8/finance/chart/XOM?range=1y&interval=1d',t=25)['chart']['result'][0]
c=[x for x in d2['indicators']['quote'][0]['close'] if x]; import datetime
ts=d2['timestamp']; print('1년 첫날',datetime.datetime.utcfromtimestamp(ts[0]).date(),c[0],'마지막',datetime.datetime.utcfromtimestamp(ts[-1]).date(),c[-1],'고',max(c),'저',min(c))
