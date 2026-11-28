# 경쟁 글 본문 받기 — 11/28 write krndx1129 (plusdiv1128 것 복사)
import re, html, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = ['healthy_life_365/224478632289','bennie87/224474322331','whduddnd49/224484618468','econote__/224466819987','tuttle0327/224483056762']
UA={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1'}
out={}
for p in P:
    b=urllib.request.urlopen(urllib.request.Request('https://m.blog.naver.com/'+p,headers=UA),timeout=20).read().decode('utf-8','ignore')
    m=re.search(r'<div class="se-main-container">(.*?)<div class="(?:post_footer|ssp-adcontent|comment)',b,re.S) or re.search(r'se-main-container(.*)',b,re.S)
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',m.group(1),flags=re.S)
    imgs=re.findall(r'data-lazy-src="([^"]+)"',m.group(1))
    t=html.unescape(re.sub(r'<[^>]+>','\n',t)); t='\n'.join(l.strip() for l in t.splitlines() if l.strip())
    sym=re.search(r'sympathyCount["\']?\s*[:=]\s*["\']?(\d+)',b); cm=re.search(r'commentCount["\']?\s*[:=]\s*["\']?(\d+)',b)
    out[p]={'len':len(t),'img':len(imgs),'first_img':imgs[0] if imgs else None,'sym':sym.group(1) if sym else None,'cmt':cm.group(1) if cm else None}
    open('bench_raw/'+p.replace('/','_')+'.txt','w',encoding='utf-8').write(t)
    print(p,out[p])
json.dump(out,open('bench_raw/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for p,v in out.items():
    if v['first_img']:
        u=v['first_img'].split('?')[0]+'?type=w773'
        try: open('bench_raw/'+p.replace('/','_')+'_first.png','wb').write(urllib.request.urlopen(urllib.request.Request(u,headers=dict(UA,Referer='https://m.blog.naver.com/')),timeout=20).read())
        except Exception as e: print('img fail',p,e)
