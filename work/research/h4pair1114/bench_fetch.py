# 경쟁 글 본문·표지 받기(공개 모바일 페이지) — 11/14 h4pair1114 (k1pair1110 본뜸)
import re, html, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
P = ['mssmallrock/224471616726','psc1334/224466053959','kinhazk2/224471992324','engineer_ji/224472517553','westsun78/224472005901','somel7/224472855541']
UA={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1'}
out={}
for p in P:
    try:
        b=urllib.request.urlopen(urllib.request.Request('https://m.blog.naver.com/'+p,headers=UA),timeout=20).read().decode('utf-8','ignore')
    except Exception as e:
        print(p,'FAIL',e); continue
    m=re.search(r'<div class="se-main-container">(.*?)<div class="(?:post_footer|ssp-adcontent|comment)',b,re.S) or re.search(r'se-main-container(.*)',b,re.S)
    body=m.group(1) if m else ''
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S)
    imgs=re.findall(r'data-lazy-src="([^"]+)"',body)
    t=html.unescape(re.sub(r'<[^>]+>','\n',t)); t='\n'.join(l.strip() for l in t.splitlines() if l.strip())
    sym=re.search(r'sympathyCount["\']?\s*[:=]\s*["\']?(\d+)',b); cm=re.search(r'commentCount["\']?\s*[:=]\s*["\']?(\d+)',b)
    og=re.search(r'<meta property="og:image" content="([^"]+)"',b)
    tt=re.search(r'<meta property="og:title" content="([^"]+)"',b)
    first=imgs[0] if imgs else (html.unescape(og.group(1)) if og else None)
    out[p]={'title':html.unescape(tt.group(1)) if tt else None,'len':len(t),'img':len(imgs),'first_img':first,'og':html.unescape(og.group(1)) if og else None,'sym':sym.group(1) if sym else None,'cmt':cm.group(1) if cm else None}
    open('bench_raw/'+p.replace('/','_')+'.txt','w',encoding='utf-8').write(t)
    if first:
        try:
            d=urllib.request.urlopen(urllib.request.Request(first,headers={**UA,'Referer':'https://m.blog.naver.com/'}),timeout=20).read()
            fn='bench_raw/cover_'+p.split('/')[0]+'.jpg'; open(fn,'wb').write(d); out[p]['cover']=fn; out[p]['cover_bytes']=len(d)
        except Exception as e:
            out[p]['cover']='FAIL '+str(e)
    print(p,out[p])
json.dump(out,open('bench_raw/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
