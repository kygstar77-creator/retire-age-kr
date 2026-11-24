# 경쟁 글 본문 받기(공개 모바일 페이지) — 11/24 write-b decdiv1126 (dgro1125 틀)
import re, html, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = ['few_economy/224477589614','green8578/224488952363','loyal90/224474741222','nineman903/224478717119','dividendvending/224482199237']
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
        try:
            d=urllib.request.urlopen(urllib.request.Request(v['first_img'].split('?')[0]+'?type=w773',headers={**UA,'Referer':'https://m.blog.naver.com/'}),timeout=20).read()
            open('bench_raw/'+p.replace('/','_')+'_first.png','wb').write(d); print('img',p,len(d))
        except Exception as e: print('imgfail',p,e)
