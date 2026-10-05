import sys, re, json, urllib.request, urllib.parse, html, os
sys.stdout.reconfigure(encoding='utf-8')
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
H=os.path.dirname(os.path.abspath(__file__))
out={}
for name,q in {'hfguar1006':'주택연금 보증료','retmid1005':'퇴직금 중간정산 세금'}.items():
    u='https://m.search.naver.com/search.naver?ssc=tab.m_cafe.all&sm=mtb_jum&query='+urllib.parse.quote(q)
    t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','ignore')
    open(os.path.join(H,f'raw_{name}.html'),'w',encoding='utf-8').write(t)
    urls=[];seen=set()
    for m in re.finditer(r'(https://search\.pstatic\.net/common/\?src=[^"\'\s<>]+?)(?=["\'\s<>])',t):
        x=html.unescape(m.group(1))
        if 'cafefiles' not in x and 'cafeptthumb' not in x and 'naver.net' not in x: continue
        if x in seen: continue
        seen.add(x); urls.append(x)
    print(name,len(t),len(urls))
    res=[]
    for i,x in enumerate(urls[:8],1):
        x2=re.sub(r'type=[^&]+','type=f192_192',x)
        fn=f'{name}_{i}.jpg'
        try:
            open(os.path.join(H,'comp',fn),'wb').write(urllib.request.urlopen(urllib.request.Request(x2,headers={'User-Agent':UA}),timeout=30).read())
            res.append({'u':x2,'link':x2,'file':fn,'src':f'm.search.naver.com ssc=tab.m_cafe.all q={q}'})
        except Exception as e: print('fail',e)
    out[name]=res
json.dump(out,open(os.path.join(H,'comp','comp.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
