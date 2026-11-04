import re,json,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[x.strip().split("/")[-2:] for x in open("bench_raw/urls.txt") if x.strip()]
out=[]
for b,n in posts:
    u=f"https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}"
    h=subprocess.run(["curl","-s","-A",UA,u],capture_output=True).stdout.decode("utf-8","ignore")
    t=re.search(r'<meta property="og:title" content="([^"]*)"',h)
    body=re.findall(r'<div class="se-module se-module-text[^>]*>(.*?)</div>\s*</div>',h,re.S)
    txt="\n".join(re.sub(r"<[^>]+>","",x) for x in body)
    txt=html.unescape(re.sub(r"\n\s*\n+","\n",txt)).strip()
    open(f"bench_raw/{b}_{n}.txt","w",encoding="utf-8").write(txt)
    imgs=len(re.findall(r'se-module-image',h)); tables=len(re.findall(r'se-table',h))
    dt=re.search(r'"publishDate"\s*:\s*"?([^",]+)',h) or re.search(r'class="blog_date"[^>]*>([^<]+)',h)
    kw={k:(k in txt) for k in ["2,500","11월 30","11월 26","15.4","12월 30","우선주","2우B","분리과세","고배당","종합과세","2천만","건강보험","건보료","피부양자","기준일","배당락","1만원","10,000"]}
    out.append(dict(url=f"https://blog.naver.com/{b}/{n}",title=t and html.unescape(t.group(1)),date=dt and dt.group(1),chars=len(txt),imgs=imgs,tables=tables,kw=kw,head=txt[:220],tail=txt[-200:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:900]);print()
