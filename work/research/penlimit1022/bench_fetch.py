import re,sys,json,subprocess,html
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("gjwlh","224434171968"),("jenny_tech","224442860791"),("anjdiqkqh","224434317196"),("sjajrh12131","224437863522"),("ya_nt","224439415074")]
out=[]
for b,n in posts:
    u=f"https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}"
    h=subprocess.run(["curl","-s","-A",UA,u],capture_output=True).stdout.decode("utf-8","ignore")
    open(f"bench_raw/blog_{b}.html","w",encoding="utf-8").write(h)
    t=re.search(r'<meta property="og:title" content="([^"]*)"',h)
    body=re.findall(r'<div class="se-module se-module-text[^>]*>(.*?)</div>\s*</div>',h,re.S)
    txt="\n".join(re.sub(r"<[^>]+>","",x) for x in body)
    txt=html.unescape(re.sub(r"\n\s*\n+","\n",txt)).strip()
    imgs=len(re.findall(r'se-module-image',h)); tables=len(re.findall(r'se-table',h))
    heads=re.findall(r'se-section-sectionTitle.*?<span[^>]*>(.*?)</span>',h,re.S)
    sym=re.search(r'"sympathyCount"\s*:\s*(\d+)',h); cm=re.search(r'"commentCount"\s*:\s*(\d+)',h)
    out.append(dict(url=u,title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,sym=sym and sym.group(1),cm=cm and cm.group(1),head=txt[:500],tail=txt[-400:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:1600]);print()
