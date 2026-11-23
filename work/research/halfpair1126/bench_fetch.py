# 경쟁 글 본문 받기 — 블로그(toprank 상위, 공개 모바일 페이지) + 부동산스터디(jaegebal 12730407) 주간 인기글 전체공개 3편. 11/24 halfpair1126
import re, html, urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, 'bench_raw')
P = ['songdo-life/224474951053', 'songdo-life/224468614973', 'ssss6424/224487234023', 'tanxza2bdwo/224488682802', 'myfriendkmy/224488483435']
UA = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1'}
out = {}
for p in P:
    b = urllib.request.urlopen(urllib.request.Request('https://m.blog.naver.com/' + p, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
    m = re.search(r'<div class="se-main-container">(.*?)<div class="(?:post_footer|ssp-adcontent|comment)', b, re.S) or re.search(r'se-main-container(.*)', b, re.S)
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', m.group(1), flags=re.S)
    imgs = re.findall(r'data-lazy-src="([^"]+)"', m.group(1))
    t = html.unescape(re.sub(r'<[^>]+>', '\n', t)); t = '\n'.join(l.strip() for l in t.splitlines() if l.strip())
    cm = re.search(r'commentCount["\']?\s*[:=]\s*["\']?(\d+)', b)
    out[p] = {'len': len(t), 'img': len(imgs), 'first_img': imgs[0] if imgs else None, 'cmt': cm.group(1) if cm else None}
    open(os.path.join(B, p.replace('/', '_') + '.txt'), 'w', encoding='utf-8').write(t); print(p, out[p])
for aid in (6541040, 6541607, 6539851):
    u = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/12730407/articles/{aid}?useCafeId=true'
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={**UA, 'Referer': 'https://m.cafe.naver.com/'}), timeout=20).read().decode('utf-8'))
        a = d['result']['article']; c = a.get('contentHtml', '')
        t = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', c, flags=re.S))); t = '\n'.join(l.strip() for l in t.splitlines() if l.strip())
        out[f'jaegebal/{aid}'] = {'subject': a.get('subject'), 'len': len(t), 'read': a.get('readCount'), 'cmt': a.get('commentCount'), 'img': c.count('<img')}
        open(os.path.join(B, f'jaegebal_{aid}.txt'), 'w', encoding='utf-8').write(a.get('subject', '') + '\n' + t); print(aid, out[f'jaegebal/{aid}'])
    except Exception as e: print(aid, '실패', e)
json.dump(out, open(os.path.join(B, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
