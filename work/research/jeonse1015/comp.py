import re, sys, urllib.request, html, json
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
s = open('srch.html', encoding='utf-8', errors='ignore').read()
seen = []
for m in re.finditer(r'blog\.naver\.com/([a-zA-Z0-9_-]+)/(\d{9,})', s):
    k = (m.group(1), m.group(2))
    if k not in seen: seen.append(k)
out = []
for bid, no in seen[:7]:
    u = f'https://m.blog.naver.com/PostView.naver?blogId={bid}&logNo={no}'
    try: t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'ignore')
    except Exception as e: print(bid, e); continue
    ti = re.search(r'<meta property="og:title" content="([^"]*)"', t); ti = html.unescape(ti.group(1)) if ti else ''
    body = re.findall(r'<div class="se-module se-module-text[^"]*">(.*?)</div>', t, re.S)
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(body))); txt = re.sub(r'\s+', ' ', txt)
    img = len(re.findall(r'se-image-resource', t))
    dt = re.search(r'"publishDate"\s*:\s*"?([^",]+)', t) or re.search(r'class="blog_date"[^>]*>([^<]+)', t)
    kw = {k: txt.count(k) for k in ('같은 단지', '실거래', '보증금', '갱신', '신규', '구별', '성북')}
    out.append(dict(url=f'https://blog.naver.com/{bid}/{no}', title=ti, chars=len(txt.replace(' ', '')), img=img, kw=kw, head=txt[:300]))
    print(len(out), ti, f'https://blog.naver.com/{bid}/{no}', len(txt.replace(' ', '')), img, kw)
json.dump(out, open('comp.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
