import json,urllib.request
for cik in ['0001067839','0001378872']:
    r=urllib.request.Request(f'https://data.sec.gov/submissions/CIK{cik}.json',headers={'User-Agent':'firemap research kygstar77@gmail.com'})
    d=json.load(urllib.request.urlopen(r,timeout=30)); f=d['filings']['recent']
    print(cik,d['name'])
    n=0
    for i,fm in enumerate(f['form']):
        if fm in('497K','497','485BPOS','N-CSR','N-CSRS','497K1'):
            print(' ',fm,f['filingDate'][i],f['accessionNumber'][i],f['primaryDocument'][i]); n+=1
            if n>=8: break
