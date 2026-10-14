import sys, io, zipfile, urllib.request, re, html
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
k=apis.key('dart'); cc='00126362'
for y,rc in ((2025,'11011'),(2026,'11012')):
    d=apis._j(f'https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={k}&corp_code={cc}&bsns_year={y}&reprt_code={rc}')
    for x in d.get('list',[]):
        if '주당' in x.get('se','') : print(y,rc,x['se'],x.get('stock_knd'),x.get('thstrm'),x.get('frmtrm'),x.get('lwfr'))
b=urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={k}&rcept_no=20260814003578',timeout=60).read()
z=zipfile.ZipFile(io.BytesIO(b))
for n in z.namelist():
    s=z.read(n).decode('utf-8','ignore')
    t=html.unescape(re.sub(r'<[^>]+>',' ',s)); t=re.sub(r'\s+',' ',t)
    open('dart_h1_2026.txt','w',encoding='utf-8').write(t)
    print(n,len(t))
    i=t.find('사업의 개요'); print(t[i:i+2500])
