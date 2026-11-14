# 카페 인기글 본문 읽기(전체공개만, articleapi) — silson24clm1114 11/14
import sys, json, re, html, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148', 'Referer': 'https://m.cafe.naver.com/'}
for cid, aid in [a.split('/') for a in sys.argv[1:]]:
    try: d = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{aid}?useCafeId=true', headers=H), timeout=25).read().decode('utf-8', 'ignore'))
    except Exception as e: print(cid, aid, 'ERR', e); continue
    a = (d.get('result') or {}).get('article') or {}
    h = a.get('contentHtml') or ''
    t = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)))
    t = '\n'.join(l.strip() for l in t.splitlines() if l.strip())
    imgs = len(re.findall(r'<img', h))
    open(f'bench_raw/cafe_{cid}_{aid}.txt', 'w', encoding='utf-8').write(a.get('subject', '') + '\n' + t)
    print(cid, aid, a.get('subject'), 'len', len(t), 'img', imgs, 'read', a.get('readCount'), 'cmt', a.get('commentCount'))
    print('  FIRST', t[:200].replace('\n', ' / ')); print('  LAST', t[-200:].replace('\n', ' / '))
