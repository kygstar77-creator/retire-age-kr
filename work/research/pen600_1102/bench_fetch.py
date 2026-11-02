import re,json,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("didl158","224459340077"),("flalspwlq","224459567908"),("monsterttch","224457132308"),("motionstrength","224451272138"),("ddeang233","224457773606"),("bae5271","224449816099")]
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
    kw={k:(k in txt) for k in ["이전","퇴직금","전환","1월","과세제외","12월 31일","산출세액","결정세액"]}
    out.append(dict(url=f"https://blog.naver.com/{b}/{n}",title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,kw=kw,head=txt[:250],tail=txt[-200:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:900]);print()
