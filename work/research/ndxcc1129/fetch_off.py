# 운용사 원문 분배 표 저장: 삼성 divid-info API(KODEX 494300) + TIGER 표(fetch_div.py가 받은 raw/tiger_*_div_1127.txt). 11/27 write.
import json, re, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
d=urllib.request.urlopen(urllib.request.Request('https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFO6',headers={'User-Agent':'Mozilla/5.0','Referer':'https://m.samsungfund.com/'}),timeout=30).read()
open('raw/kodex_494300_divid_1127.json','wb').write(d)
off={'494300':[(x['basicD'][:4]+'-'+x['basicD'][4:6]+'-'+x['basicD'][6:],int(x['dividA']),int(x['taxDividA'])) for x in json.loads(d)['dividList']]}
for c in ['441680','486290']:
    s=open(f'raw/tiger_{c}_div_1127.txt',encoding='utf-8').read()
    off[c]=[(a,int(m.replace(',','')),int(t.replace(',',''))) for a,_,m,t in re.findall(r'(\d{4}-\d\d-\d\d) (\d{4}-\d\d-\d\d) ([\d,]+) ([\d,]+)',s)]
json.dump(off,open('official_div.json','w',encoding='utf-8'),ensure_ascii=False)
for c,v in off.items(): print(c,len(v),v[:2],v[-1], '2025-03:',[x for x in v if x[0].startswith('2025-03')])
