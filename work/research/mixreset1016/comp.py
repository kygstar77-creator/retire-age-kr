import re, sys, urllib.request, html, json
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
L = ['ac9832/224431515852','djlee118/224438719562','tmishaha/224434666617','healthtalkmentaltalk/224428198672','audmsdk/224437018739']
KW = ('재산정','잔액','가산금리','기준금리','계약서','2021','월 상환','금융채','코픽스')
out=[]
for x in L:
    bid,no=x.split('/')
    u=f'https://m.blog.naver.com/PostView.naver?blogId={bid}&logNo={no}'
    try: t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','ignore')
    except Exception as e: print(bid,e); continue
    ti=re.search(r'<meta property="og:title" content="([^"]*)"',t); ti=html.unescape(ti.group(1)) if ti else ''
    body=re.findall(r'<div class="se-module se-module-text[^"]*">(.*?)</div>',t,re.S)
    txt=html.unescape(re.sub(r'<[^>]+>',' ',' '.join(body))); txt=re.sub(r'\s+',' ',txt)
    open(f'comp_{bid}_{no}.txt','w',encoding='utf-8').write(ti+'\n'+txt)
    img=len(re.findall(r'se-image-resource',t))
    kw={k:txt.count(k) for k in KW}
    out.append(dict(url=f'https://blog.naver.com/{bid}/{no}',title=ti,chars=len(txt.replace(' ','')),img=img,kw=kw,head=txt[:250]))
    print(ti,len(txt.replace(' ','')),img,kw)
json.dump(out,open('comp.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
