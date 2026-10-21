# 경쟁 블로그 글 본문·날짜·사진 수·댓글 수 받기(2026-10-20, h1walkcafe1020 bench.md용). 남의 문장은 bench에 옮기지 않고 틀만 본다.
import sys, re, json, urllib.request, html
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36'}
out = []
for u in sys.argv[1:]:
    b, n = re.search(r'naver\.com/([^/]+)/(\d+)', u).groups()
    s = urllib.request.urlopen(urllib.request.Request(f'https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
    t = re.search(r'<meta property="og:title" content="([^"]*)"', s); t = html.unescape(t.group(1)) if t else ''
    j = s.find('blog_date'); date = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s[j:j+80])).replace('blog_date">', '').strip()[:20]
    k = s.find('class="se-main-container"'); body = s[k:k+200000]; e = body.find('post_footer'); body = body[:e if e > 0 else 80000]
    txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body)))
    imgs = len(re.findall(r'se-image-resource', body))
    cmt = re.search(r'"commentCount"\s*:\s*(\d+)', s) or re.search(r'commentCount[^0-9]{0,40}(\d+)', s)
    out.append(dict(url=u, title=t, date=date, cmt=cmt.group(1) if cmt else '', chars=len(txt), imgs=imgs, head=txt[:350], tail=txt[-350:]))
    print(json.dumps(out[-1], ensure_ascii=False)); print()
json.dump(out, open('bench_raw/posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
