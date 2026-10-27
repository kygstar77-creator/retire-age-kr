import re,json,subprocess,html
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("gn_youth","224290625219"),("kymuji","224441926353"),("minmin_3535","224439986621"),("nextground","224155963594"),("osan_si","224378720615"),("triumph9115","224444093372")]
out=[]
for b,n in posts:
    u=f"https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}"
    h=subprocess.run(["curl","-s","-A",UA,u],capture_output=True).stdout.decode("utf-8","ignore")
    t=re.search(r'<meta property="og:title" content="([^"]*)"',h)
    body=re.findall(r'<div class="se-module se-module-text[^>]*>(.*?)</div>\s*</div>',h,re.S)
    txt="\n".join(re.sub(r"<[^>]+>","",x) for x in body)
    txt=html.unescape(re.sub(r"\n\s*\n+","\n",txt)).strip()
    imgs=len(re.findall(r'se-module-image',h)); tables=len(re.findall(r'se-table',h))
    d=re.search(r'se_publishDate[^>]*>([^<]*)',h)
    out.append(dict(url=u,title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,date=d and d.group(1),head=txt[:350],tail=txt[-250:],mentions27=('1200만' in txt or '1,200만' in txt),mentions2027=('2027' in txt),m2026=('2026' in txt),m50=('50개월' in txt)))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:1100]);print()
