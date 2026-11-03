import re,json,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("go_tax","224460584470"),("bigtiger001","224457382044"),("gari4004","224460500442"),("enjoyon2","224463107842"),("taxshin77","224451156309"),("dpnews2024","224457132355")]
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
    kw={k:(k in txt) for k in ["8천만","8,000만","3천만","1세대 1주택","6년","20년","100분의 70","70%","50%","60세","납부유예","담보","정상주택가격","정기예금","조합원 수","예정액","부과율","준공","조합설립","10년"]}
    out.append(dict(url=f"https://blog.naver.com/{b}/{n}",title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,kw=kw,head=txt[:200],tail=txt[-160:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:800]);print()
