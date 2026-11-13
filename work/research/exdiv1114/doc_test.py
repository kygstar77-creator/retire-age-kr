import sys,json,urllib.request,zipfile,io,re
sys.path.insert(0,r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
k=apis.key('dart')
L=json.load(open('raw/dart_divlist.json',encoding='utf-8'))
x=[o for o in L if o['corp_name']=='KB금융'] or L[:1]
print(x)
r=x[-1]['rcept_no']
b=urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={k}&rcept_no={r}',timeout=30).read()
z=zipfile.ZipFile(io.BytesIO(b))
for n in z.namelist():
    t=z.read(n).decode('utf-8','ignore')
    t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\s+',' ',t)
    print(n,len(t)); print(t[:2500])
