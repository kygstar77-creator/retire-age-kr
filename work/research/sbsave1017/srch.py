import re, sys, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
q = urllib.parse.quote(sys.argv[1])
for u in (f'https://m.search.naver.com/search.naver?ssc=tab.m_blog.all&sm=mtb_jum&query={q}', f'https://m.search.naver.com/search.naver?where=m_blog&query={q}'):
    t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'ignore')
    open('srch.html', 'w', encoding='utf-8').write(t)
    urls = []
    for m in re.finditer(r'https?://(?:m\.)?blog\.naver\.com/([A-Za-z0-9_\-]+)/(\d{9,})', t):
        k = f'{m.group(1)}/{m.group(2)}'
        if k not in urls: urls.append(k)
    print(len(t), len(urls))
    if len(urls) >= 5: break
open('comp_list.txt', 'w').write('\n'.join('blog.naver.com/' + k for k in urls[:8]))
print(urls[:8])
