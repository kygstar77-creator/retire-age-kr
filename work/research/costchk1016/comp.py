import re, sys, urllib.request, html, json
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
s = open('toprank1.txt', encoding='utf-8').read()
seen = []
for m in re.finditer(r'blog\.naver\.com/([a-zA-Z0-9_-]+)/(\d{9,})', s):
    k = (m.group(1), m.group(2))
    if k not in seen: seen.append(k)
out = []
KW = ('생산자물가', '물가상승률', '수수료', '5분의 1', '20%', '분담금', '3분의 2', '처리기간', '60일', '총회', '구속력')
for bid, no in seen[:6]:
    u = f'https://m.blog.naver.com/PostView.naver?blogId={bid}&logNo={no}'
    try: t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'ignore')
    except Exception as e: print(bid, e); continue
    open(f'comp_{bid}_{no}.html', 'w', encoding='utf-8').write(t)
    ti = re.search(r'<meta property="og:title" content="([^"]*)"', t); ti = html.unescape(ti.group(1)) if ti else ''
    body = re.findall(r'<div class="se-module se-module-text[^"]*">(.*?)</div>', t, re.S)
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(body))); txt = re.sub(r'\s+', ' ', txt)
    open(f'comp_{bid}_{no}.txt', 'w', encoding='utf-8').write(ti + '\n' + txt)
    img = len(re.findall(r'se-image-resource', t))
    kw = {k: txt.count(k) for k in KW}
    out.append(dict(url=f'https://blog.naver.com/{bid}/{no}', title=ti, chars=len(txt.replace(' ', '')), img=img, kw=kw, head=txt[:300]))
    print(len(out), ti, f'https://blog.naver.com/{bid}/{no}', len(txt.replace(' ', '')), img, kw)
json.dump(out, open('comp.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
