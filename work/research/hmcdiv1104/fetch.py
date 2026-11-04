import sys,io,zipfile,re,html,urllib.request
sys.path.insert(0,'.'); import apis
k=apis.key('dart')
for r in sys.argv[1:]:
    b=urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={k}&rcept_no={r}',timeout=30).read()
    z=zipfile.ZipFile(io.BytesIO(b)); x=z.read(z.namelist()[0]).decode('utf-8','ignore')
    open(f'research/hmcdiv1104/raw/{r}.xml','w',encoding='utf-8').write(x)
    t=html.unescape(re.sub(r'<[^>]+>',' ',x)); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    open(f'research/hmcdiv1104/raw/{r}.txt','w',encoding='utf-8').write(t)
    print('==',r,len(t)); print(t[:1800])
