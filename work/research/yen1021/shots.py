import re, sys, urllib.request, html
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36', 'Referer': 'https://m.blog.naver.com/'}
for i, (b, n) in enumerate([('luckyguni7','224447148775'),('press02','224445944128'),('editmagazine','224445808767'),('money_mento','224423684138')], 1):
    s = urllib.request.urlopen(urllib.request.Request(f'https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
    urls = re.findall(r'data-lazy-src="(https://[^"]+)"', s) or re.findall(r'class="se-image-resource[^"]*"[^>]*src="(https://[^"]+)"', s)
    urls = [html.unescape(u) for u in urls if 'pstatic' in u]
    print(b, len(urls))
    for k, u in enumerate(urls[:2]):
        u = re.sub(r'\?type=\w+', '?type=w773', u)
        try:
            open(f'bench_shots/c{i}_{k}.png', 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read()); print(' ok', k)
        except Exception as e: print(' fail', e)
