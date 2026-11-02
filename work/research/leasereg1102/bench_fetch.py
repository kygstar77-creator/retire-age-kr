import re,json,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("koreaaptland","224461350780"),("imaginably","224454194363"),("lsjid0924","224459205654"),("mnrocket","224446612627"),("semulotsemay","224457771074"),("simple_232","224457894299"),("manksw","224460108935"),("interpret_","224454078484")]
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
    kw={k:(k in txt) for k in ["결정문","등기부","전입","대항력","우선변제","비용","송달료","전자소송","임대인","고지","보증보험","HUG","2023","대법원","확정일자","주민등록"]}
    out.append(dict(url=f"https://blog.naver.com/{b}/{n}",title=t and html.unescape(t.group(1)),chars=len(txt),imgs=imgs,tables=tables,kw=kw,head=txt[:250],tail=txt[-200:]))
json.dump(out,open("bench_raw/posts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(json.dumps(o,ensure_ascii=False)[:900]);print()
