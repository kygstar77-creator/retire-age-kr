import re,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
for f in sorted(glob.glob('raw/pdf_*.txt')):
    t=re.sub(r'\s+',' ',open(f,encoding='utf-8').read())
    k=t.find('종목명 비중(%) 수량')
    if k<0: print(f,'NO PDF'); continue
    seg=t[k:k+6000]
    rows=re.findall(r'([^\d()][^()]{0,30}?) \((\w{6})\) ([\d.]+) ',seg)
    d={re.sub(r'^[d,.s-]+','',n).strip():float(w) for n,c,w in rows}
    two=d.get('삼성전자',0)+d.get('SK하이닉스',0)
    print(f[8:-4],'| 종목',len(rows),'| 삼성',d.get('삼성전자',0),'하닉',d.get('SK하이닉스',0),'합',round(two,1),'| 상위5',list(d.items())[:5])
    dt=re.search(r'(\d\d\.\d\d\.\d\d) 기준[^가-힣]{0,30}구성종목|구성종목\(PDF\)[^가-힣]{0,20}(\d\d\.\d\d\.\d\d)',t)
