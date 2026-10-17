import re,html,urllib.request,urllib.parse,sys
sys.stdout.reconfigure(encoding='utf-8')
q=urllib.parse.quote('KRX 금 웃돈')
r=urllib.request.Request('https://m.search.naver.com/search.naver?ssc=tab.m_blog.all&query='+q,headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'})
t=urllib.request.urlopen(r,timeout=30).read().decode('utf-8','ignore')
open('research/g1whycafe1018/m_blog.html','w',encoding='utf-8').write(t)
seen=set()
for m in re.finditer(r'href="(https://(?:m\.)?blog\.naver\.com/[^"]+)"[^>]*>(.{0,400}?)</a>',t,re.S):
    s=html.unescape(re.sub(r'<[^>]+>','',m.group(2))).strip()
    if len(s)>10 and m.group(1) not in seen:
        seen.add(m.group(1)); print(m.group(1)[:75],'|',s[:80])
print(len(t))
