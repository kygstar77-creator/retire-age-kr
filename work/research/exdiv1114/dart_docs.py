# 각 회사 마지막 '현금ㆍ현물배당결정'(정정 포함) 원문에서 배당구분·1주당 배당금·시가배당율·기준일·결정일을 뽑는다
import sys,json,urllib.request,zipfile,io,re,time,os
sys.path.insert(0,r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
k=apis.key('dart')
L=[o for o in json.load(open('raw/dart_divlist.json',encoding='utf-8')) if '자회사' not in o['report_nm']]
last={}
for o in sorted(L,key=lambda o:o['rcept_no']): last[o['corp_code']]=o
os.makedirs('raw/docs',exist_ok=True)
rows=[]
for i,o in enumerate(last.values()):
    fn=f"raw/docs/{o['rcept_no']}.txt"
    if os.path.exists(fn): t=open(fn,encoding='utf-8').read()
    else:
        try:
            b=urllib.request.urlopen(f"https://opendart.fss.or.kr/api/document.xml?crtfc_key={k}&rcept_no={o['rcept_no']}",timeout=30).read()
            z=zipfile.ZipFile(io.BytesIO(b)); t=' '.join(z.read(n).decode('utf-8','ignore') for n in z.namelist())
        except Exception as e:
            print('ERR',o['corp_name'],e); continue
        t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\s+',' ',t)
        open(fn,'w',encoding='utf-8').write(t); time.sleep(0.1)
    i=t.rfind('1. 배당구분'); tb=t[i:] if i>=0 else t  # 정정 공시는 '정정전/정정후' 표 뒤 본문만 읽는다
    g=lambda p: (re.search(p,tb) or [None,None])[1]
    rows.append(dict(o, kind=g(r'배당구분 (\S+)'), dps=g(r'1주당 배당금\(원\) 보통주식 ([\d,\.]+|-)'),
        yld=g(r'시가배당율\(%\) 보통주식 ([\d\.]+|-)'), rec=g(r'배당기준일 (\d{4}-\d{2}-\d{2})'), dec=g(r'이사회결의일\(결정일\) (\d{4}-\d{2}-\d{2})')))
    if i%100==0: print(i,rows[-1])
json.dump(rows,open('raw/dart_divrows.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
from collections import Counter
print(len(rows),Counter(r['kind'] for r in rows))
print(Counter((r['rec'] or 'None')[:7] for r in rows if r['kind']=='결산배당'))
