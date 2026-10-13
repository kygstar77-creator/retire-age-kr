import json,urllib.request,re,html
H={'User-Agent':'firemap research kygstar77@gmail.com'}
def doc(cik,acc,pd):
    u=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-","")}/{pd}'
    t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40).read().decode('utf8','ignore')
    t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(re.sub(r'\s+',' ',t)); return u,t
# QQQ
u,t=doc('1067839','0001193125-26-265096','d21745d497k.htm'); open('qqq_497k_0610.txt','w',encoding='utf8').write(t)
print(u,len(t)); 
for m in re.finditer(r'Total Annual Fund Operating Expenses',t): print(t[max(0,m.start()-300):m.start()+200]); break
# QQQM: scan trust II 497K filings
r=json.load(urllib.request.urlopen(urllib.request.Request('https://data.sec.gov/submissions/CIK0001378872.json',headers=H),timeout=30))['filings']['recent']
cand=[(r['filingDate'][i],r['accessionNumber'][i],r['primaryDocument'][i]) for i,f in enumerate(r['form']) if f=='497K'][:14]
for fd,acc,pd in cand:
    try:
        u,t=doc('1378872',acc,pd)
    except Exception as e: print('err',acc,e); continue
    if 'QQQM' in t[:3000] or 'Invesco NASDAQ 100 ETF' in t[:3000]:
        print('QQQM doc',fd,u); open('qqqm_497k.txt','w',encoding='utf8').write(t)
        for m in re.finditer(r'Total Annual Fund Operating Expenses',t): print(t[max(0,m.start()-300):m.start()+250]); break
        break
    else: print('skip',fd,pd,t[:100])
