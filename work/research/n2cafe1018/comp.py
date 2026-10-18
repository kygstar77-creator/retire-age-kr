import re, sys, urllib.request, html, json
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
src=open('raw/srch_내_연봉_순위.html',encoding='utf-8',errors='ignore').read()
L=[]
for m in re.finditer(r'blog\.naver\.com/([A-Za-z0-9_-]+)/(\d{9,})',src):
    if m.group(0) not in L: L.append(m.group(0))
L=L[:6]
KW=('국세청','천분위','백분위','국가데이터처','통계청','임금근로일자리','중위','평균','나이','연령','상위','계산기','엑셀','실수령','2024','2023')
out=[]
for i,x in enumerate(L):
    bid,no=x.split('/')[1:]
    u=f'https://m.blog.naver.com/PostView.naver?blogId={bid}&logNo={no}'
    try: t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','ignore')
    except Exception as e: print(bid,e); continue
    ti=re.search(r'<meta property="og:title" content="([^"]*)"',t); ti=html.unescape(ti.group(1)) if ti else ''
    body=re.findall(r'<div class="se-module se-module-text[^"]*">(.*?)</div>',t,re.S)
    txt=html.unescape(re.sub(r'<[^>]+>',' ',' '.join(body))); txt=re.sub(r'\s+',' ',txt)
    open(f'comp_{bid}_{no}.txt','w',encoding='utf-8').write(ti+'\n'+txt)
    img=len(re.findall(r'se-image-resource',t))
    kw={k:txt.count(k) for k in KW if txt.count(k)}
    out.append(dict(rank=i+1,url=f'https://blog.naver.com/{bid}/{no}',title=ti,chars=len(txt.replace(' ','')),img=img,kw=kw,head=txt[:200]))
    print(i+1,ti,'|',len(txt.replace(' ','')),img,kw)
json.dump(out,open('comp.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
