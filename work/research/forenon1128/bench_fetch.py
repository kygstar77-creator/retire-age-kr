# 경쟁 글 본문 받기 — '올림픽파크포레온 실거래가' 블로그 탭 상위(toprank 11/27) + 부동산스터디(jaegebal 12730407) 주간 인기글 중 포레온·둔촌·강동 제목. 11/27 forenon1128
import re, html, urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, 'bench_raw')
P = ['daehong1024/224488788157', 'aki_blog/224493287937', 'rkddnjs73/224482324957', 'ziplab365/224488885909', 'niceday150/224493360979']
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
open(os.path.join(B, 'jaegebal_weekly.json'), 'w', encoding='utf-8').write(json.dumps(w, ensure_ascii=False))
arts = w.get('message', {}).get('result', {}).get('articleList', [])
print('jaegebal 주간', len(arts))
for a in arts:
    s = a.get('subject', '')
    if re.search(r'포레온|둔촌|강동|올파포|입주장|실거주', s): print(' ', a.get('articleId'), a.get('readCount'), a.get('commentCount'), s[:70])
json.dump(out, open(os.path.join(B, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False)
