# 경쟁 글 본문 받기(공개 모바일 페이지) — 11/9 write k1pair1110
import re, html, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = ['gomdolfather/224454015611','realestatedevelopm/224455361675','healthtalkmentaltalk/224428198672','ac9832/224468632161','donsite/224415826174','luis_0727/224432233429']
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
