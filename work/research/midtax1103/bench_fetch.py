import re,json,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("moneytoday8","224462756284"),("linegym_","224462103595"),("kicpa_k","224462710069"),("econhanip","224462027582"),("sowontax","224462284422"),("nhjtax","224461350833")]
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
    kw={k:(k in txt) for k in ["연금","이자","배당","근로소득만","주택임대","분리과세","30%","100분의 30","50만","1천만","분납","추계","11월 30일","11월 15","12월","1월","가산세","납부지연"]}
    out.append(dict(url=f"https://blog.naver.com/{b}/{n}",title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,kw=kw,head=txt[:200],tail=txt[-160:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:800]);print()
