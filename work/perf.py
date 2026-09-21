# 발행한 글이 실제로 읽히는지 재는 도구 — 이게 없으면 뭘 고쳐야 할지 알 수 없다.
# 사용: python work/perf.py [최근 블로그 N편=8]
# 재는 것 세 가지
#   1) 카페 글 조회수 (카페 API, 로그인 불필요)
#   2) 블로그 글이 제목 그대로 검색해서 나오는가 (= 색인됐는가)
#   3) 블로그·카페 글이 목표 검색어에서 몇 위인가
# 결과를 work/perf_log.json에 날짜별로 쌓아 추세를 본다.
import sys, os, re, json, time, html, datetime, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
CAFE_UA = dict(UA, Referer='https://cafe.naver.com/')
TODAY = datetime.date.today().isoformat()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
CLUBID = '31789001'
BLOGID = 'kygstar7777'

def get(u, headers=UA):
    return urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=20).read().decode('utf-8', 'ignore')

def cafe_posts(per=30):
    u = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=%s'
         '&search.queryType=lastArticle&search.page=1&search.perPage=%d' % (CLUBID, per))
    try:
        d = json.loads(get(u, CAFE_UA))
        return [{'title': a.get('subject', ''), 'read': a.get('readCount'), 'id': a.get('articleId')}
                for a in d['message']['result']['articleList']]
    except Exception as e:
        print('카페 조회 실패:', e); return []

def blog_posts(n):
    try:
        s = get('https://rss.blog.naver.com/%s.xml' % BLOGID)
    except Exception as e:
        print('블로그 RSS 실패:', e); return []
    out = []
    for it in re.findall(r'<item>(.*?)</item>', s, re.S)[:n]:
        t = re.search(r'<title>(.*?)</title>', it, re.S)
        d = re.search(r'<pubDate>(.*?)</pubDate>', it, re.S)
        if not t: continue
        out.append({'title': html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', t.group(1))).strip(),
                    'date': (d.group(1)[:16] if d else '')})
    return out

def search_rank(query, needle, tab):
    """네이버 검색 결과 30개 안에서 우리 링크가 몇 번째인지. 없으면 None."""
    u = 'https://search.naver.com/search.naver?ssc=tab.%s.all&query=%s' % (tab, urllib.parse.quote(query))
    try:
        s = get(u)
    except Exception:
        return None
    seen = []
    for l in re.findall(r'https?://(?:m\.)?(?:blog|cafe)\.naver\.com/[A-Za-z0-9_\-/]+', s):
        if l not in seen: seen.append(l)
    for i, l in enumerate(seen[:30], 1):
        if needle in l: return i
    return None

def norm(s):
    return re.sub(r'[\s\W_]+', '', s or '')

def draft_index():
    """work/research/*/ 의 블로그 원고에서 {정규화한 제목: 본문 문장 하나}.
    색인 여부는 본문 문장을 따옴표로 검색해 우리 블로그가 잡히는지로 잰다."""
    out = {}
    base = os.path.join(HERE, 'research')
    if not os.path.isdir(base): return out
    for d in os.listdir(base):
        for fn in ('blog.txt', 'blog_final.txt'):
            fp = os.path.join(base, d, fn)
            if not os.path.exists(fp): continue
            try: t = open(fp, encoding='utf-8').read()
            except Exception: continue
            lines = t.strip().split('\n')
            title = lines[0].strip()
            body = re.sub(r'\[이미지[^\]]*\]', '', '\n'.join(lines[1:]))
            ss = [x.strip() for x in re.split(r'(?<=다\.)\s+', body)
                  if 25 <= len(x.strip()) <= 55 and '출처' not in x and '"' not in x]
            if len(ss) > 2: out[norm(title)] = ss[2]
            break
    return out

def main():
    log = {}
    p = os.path.join(HERE, 'perf_log.json')
    if os.path.exists(p): log = json.load(open(p, encoding='utf-8'))
    today = {'cafe': [], 'blog': []}

    print('=== 카페 글 조회수 (파이어맵 카페)')
    cp = cafe_posts()
    if cp:
        reads = sorted(x['read'] for x in cp if isinstance(x['read'], int))
        today['cafe'] = [{'title': a['title'], 'read': a['read']} for a in cp]   # 전량 저장
        for a in sorted(cp, key=lambda x: -(x['read'] if isinstance(x['read'], int) else -1))[:12]:
            print('  %5s회  %s' % (a['read'], a['title'][:46]))                  # 표시는 상위 12편
        if reads:
            print('  --- %d편 중앙값 %d회, 최고 %d회' % (len(reads), reads[len(reads) // 2], reads[-1]))
            print('  비교: 파이어족 카페(회원 많은 곳) 600편 실측 중앙값 248회.')
            print('        우리 수치가 낮은 것은 글 품질이 아니라 카페 규모 때문일 수 있다 —')
            print('        회원이 적으면 무엇을 써도 조회수가 낮다. 그래서 아래 검색 순위를 같이 본다.')

    # 색인과 순위를 따로 잰다. 2026-09-21까지는 "제목 검색에 안 나오면 색인 실패"로 판정했는데 틀렸다.
    # 제목 검색에 안 나오던 9/20 글들이 본문 문장을 따옴표로 검색하면 우리 블로그로 잡혔다.
    # 네이버가 글을 알고는 있는데(색인됨) 제목 검색 순위에 안 올린 것이다.
    drafts = draft_index()
    print('\n=== 블로그 글 — 색인(본문 문장으로 잡히나)과 순위(제목 검색 몇 위)를 따로 본다')
    low = 0; noidx = 0
    for b in blog_posts(N):
        r = search_rank(b['title'], BLOGID, 'blog'); time.sleep(0.5)
        idx = None
        sent = drafts.get(norm(b['title']))
        if sent:
            idx = search_rank('"' + sent + '"', BLOGID, 'blog') is not None; time.sleep(0.5)
        rank_s = ('%d위' % r) if r else '30위 밖'
        idx_s = {True: '색인됨', False: '색인 안 됨', None: '원고 없어 못 잼'}[idx]
        if r is None or r > 10: low += 1
        if idx is False: noidx += 1
        print('  %-6s | %-12s | %s | %s' % (rank_s, idx_s, b['date'], b['title'][:40]))
        today['blog'].append({'title': b['title'], 'date': b['date'], 'self_rank': r, 'indexed': idx})
    print('  --- 제목 검색 10위 밖: %d/%d편 · 색인 안 됨(본문 문장으로도 안 잡힘): %d편'
          % (low, len(today['blog']), noidx))
    print('      제목 검색 순위가 낮은 것은 색인 실패가 아니다. 색인 안 됨은 본문 문장으로도 안 잡힐 때만이다.')

    log[TODAY] = today
    json.dump(log, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n기록: work/perf_log.json (%d일치)' % len(log))

main()
