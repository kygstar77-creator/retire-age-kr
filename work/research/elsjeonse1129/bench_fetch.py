# 경쟁 글 본문 받기 — '잠실엘스 전세' 블로그 탭 상위(toprank 11/26) + 부동산스터디(jaegebal 12730407) 주간 인기글 중 전세 제목. 11/27 elsjeonse1129
import re, html, urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, 'bench_raw')
P = ['307720/224492241424', 'illbuybanpoapt/224482887982', 'msmzzang2030/224492261140', 'hd1100id_/224491524399', '1stjohnny/224492546470', 'illbuybanpoapt/224476969798']
UA = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1'}
out = {}
for p in P:
    try:
        b = urllib.request.urlopen(urllib.request.Request('https://m.blog.naver.com/' + p, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
        m = re.search(r'<div class="se-main-container">(.*?)<div class="(?:post_footer|ssp-adcontent|comment)', b, re.S) or re.search(r'se-main-container(.*)', b, re.S)
        t = re.sub(r'<script.*?</script>|<style.*?</style>', '', m.group(1), flags=re.S)
        imgs = re.findall(r'data-lazy-src="([^"]+)"', m.group(1))
        t = html.unescape(re.sub(r'<[^>]+>', '\n', t)); t = '\n'.join(l.strip() for l in t.splitlines() if l.strip())
        cm = re.search(r'commentCount["\']?\s*[:=]\s*["\']?(\d+)', b)
        out[p] = {'len': len(t), 'img': len(imgs), 'first_img': imgs[0] if imgs else None, 'cmt': cm.group(1) if cm else None}
        open(os.path.join(B, p.replace('/', '_') + '.txt'), 'w', encoding='utf-8').write(t); print(p, out[p])
    except Exception as e: print(p, '실패', e)
H = {**UA, 'Referer': 'https://m.cafe.naver.com/'}
w = json.loads(urllib.request.urlopen(urllib.request.Request('https://apis.naver.com/cafe-web/cafe2/WeeklyPopularArticleList.json?cafeId=12730407', headers=H), timeout=20).read().decode('utf-8'))
json.dump(w, open(os.path.join(B, 'jaegebal_weekly.json'), 'w', encoding='utf-8'), ensure_ascii=False)
L = w.get('message', {}).get('result', {}).get('popularArticleList', [])
pick = [a for a in L if any(k in a.get('subject', '') for k in ('전세', '갭', '보증금'))]
print('주간 인기글', len(L), '편 · 전세 제목', len(pick), '편')
for a in pick[:8]:
    aid = a.get('articleid') or a.get('articleId')
    print(' ', aid, a.get('subject'), '조회', a.get('readCount'), '댓글', a.get('commentCount'))
for a in pick[:4]:
    aid = a.get('articleid') or a.get('articleId')
    u = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/12730407/articles/{aid}?useCafeId=true'
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read().decode('utf-8'))
        ar = d['result']['article']; c = ar.get('contentHtml', '')
        t = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', c, flags=re.S))); t = '\n'.join(l.strip() for l in t.splitlines() if l.strip())
        out[f'jaegebal/{aid}'] = {'subject': ar.get('subject'), 'len': len(t), 'read': ar.get('readCount'), 'cmt': ar.get('commentCount'), 'like': a.get('likeItCount'), 'img': c.count('<img')}
        open(os.path.join(B, f'jaegebal_{aid}.txt'), 'w', encoding='utf-8').write(ar.get('subject', '') + '\n' + t); print(aid, out[f'jaegebal/{aid}'])
    except Exception as e: print(aid, '실패', e)
json.dump(out, open(os.path.join(B, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
