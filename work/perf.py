# 발행한 글이 실제로 읽히는지 재는 도구 — 이게 없으면 뭘 고쳐야 할지 알 수 없다.
# 사용: python work/perf.py [최근 블로그 N편=8]
# 재는 것 세 가지
#   1) 카페 글 조회수 (카페 API, 로그인 불필요)
#   2) 블로그 글이 제목 그대로 검색해서 나오는가 (= 색인됐는가)
#   3) 블로그·카페 글이 목표 검색어에서 몇 위인가
# 결과를 work/perf_log.json에 날짜별로 쌓아 추세를 본다.
import sys, os, re, json, glob, time, html, datetime, urllib.request, urllib.parse
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
        ds = re.search(r'<description>(.*?)</description>', it, re.S)
        if not t: continue
        out.append({'title': html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', t.group(1))).strip(),
                    'date': (d.group(1)[:16] if d else ''),
                    'desc': html.unescape(re.sub(r'<!\[CDATA\[|\]\]>|<[^>]+>', '', ds.group(1))) if ds else ''})
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

def pick_sentence(body):
    # 따옴표 검색에 쓸 본문 문장 하나. 원고와 RSS 요약 모두 같은 기준으로 고른다.
    ss = [x.strip() for x in re.split(r'(?<=다\.)\s+', body)
          if 25 <= len(x.strip()) <= 55 and '출처' not in x and '"' not in x and '.....' not in x]
    return ss[2] if len(ss) > 2 else (ss[-1] if ss else None)

def draft_index():
    """work/research/*/ 의 블로그 원고에서 {정규화한 제목: 본문 문장 하나}.
    색인 여부는 본문 문장을 따옴표로 검색해 우리 블로그가 잡히는지로 잰다."""
    out = {}
    base = os.path.join(HERE, 'research')
    if not os.path.isdir(base): return out
    for d in os.listdir(base):
        title, body = None, None
        # 지금 원고는 pkg/title.txt + pkg/b00~b0N.txt 조각이다 (2026-09-24 확인: 조각이 있는 폴더 47개 vs
        # 옛 blog.txt 3개). 옛 파일명만 보던 탓에 색인 판정을 거의 늘 RSS 요약으로 때웠고,
        # RSS에 없는 지난 글은 "본문 없어 못 잼"으로 아예 판정이 안 됐다.
        pkg = os.path.join(base, d, 'pkg')
        tp = os.path.join(pkg, 'title.txt')
        if os.path.exists(tp):
            try:
                title = open(tp, encoding='utf-8').read().strip()
                parts = sorted(glob.glob(os.path.join(pkg, 'b[0-9][0-9].txt')))
                body = '\n'.join(open(f, encoding='utf-8').read() for f in parts)
            except Exception:
                title, body = None, None
        if not body:
            for fn in ('blog.txt', 'blog_final.txt'):
                fp = os.path.join(base, d, fn)
                if not os.path.exists(fp): continue
                try: t = open(fp, encoding='utf-8').read()
                except Exception: continue
                lines = t.strip().split('\n'); title = lines[0].strip()
                body = '\n'.join(lines[1:]); break
        if not (title and body): continue
        body = re.sub(r'\[이미지[^\]]*\]', '', body)
        ss = [x.strip() for x in re.split(r'(?<=다\.)\s+', body)
              if 25 <= len(x.strip()) <= 55 and '출처' not in x and '"' not in x]
        if len(ss) > 2: out[norm(title)] = ss[2]
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
        # 원고가 없는 글(예전 글, 원고 파일명이 다른 글)은 RSS 본문 요약에서 문장을 뽑는다 — 2026-09-22 추가
        if not sent: sent = pick_sentence(b.get('desc', ''))
        if sent:
            idx = search_rank('"' + sent + '"', BLOGID, 'blog') is not None; time.sleep(0.5)
        # 제목 검색에 우리 글이 잡혔다면 네이버가 그 글을 아는 것이다 = 색인됨.
        # 본문 문장 따옴표 검색만으로 판정하던 때는 제목 검색 1위인 글도 '색인 안 됨'으로 적혔다
        # (2026-09-24 실측: 9/23 발행 3편이 제목 1위인데 본문 문장으로는 안 잡혔다).
        if r is not None: idx = True
        rank_s = ('%d위' % r) if r else '30위 밖'
        idx_s = {True: '색인됨', False: '색인 안 됨', None: '본문 없어 못 잼'}[idx]
        if r is None or r > 10: low += 1
        if idx is False: noidx += 1
        print('  %-6s | %-12s | %s | %s' % (rank_s, idx_s, b['date'], b['title'][:40]))
        today['blog'].append({'title': b['title'], 'date': b['date'], 'self_rank': r, 'indexed': idx})
    print('  --- 제목 검색 10위 밖: %d/%d편 · 색인 안 됨(본문 문장으로도 안 잡힘): %d편'
          % (low, len(today['blog']), noidx))
    print('      제목 검색 순위가 낮은 것은 색인 실패가 아니다. 색인 안 됨은 본문 문장으로도 안 잡힐 때만이다.')

    # --- 지난 글 다시 재기 (2026-09-24 추가)
    # 하루 12~15편을 올리므로 어제 글은 오늘이면 RSS 최근 N편 밖으로 밀려난다.
    # 그래서 지금까지 모든 글이 '발행 당일' 상태로만 기록됐고, 색인될 시간을 준 적이 없었다
    # (실측: 그날 발행분 12편 색인 0%). 색인은 며칠 걸리므로 지난 기록을 다시 재야 진짜 색인율이 나온다.
    seen = {norm(x['title']) for x in today['blog']}
    old_posts, stamp = {}, {}
    for day in sorted(log):
        for x in log[day].get('blog', []):
            k = norm(x.get('title', ''))
            if not k or k in seen: continue
            old_posts[k] = x; stamp.setdefault(k, day)
    # 아직 색인 안 된 글부터. **어제 글을 먼저 넣는다** — 브레이크 판단(mature)이 쓰는 숫자가
    # 어제 글 색인율이기 때문이다. 2026-09-26 13:36 실측: 09-24·25·26 사흘 연속 mature가
    # {n:5, indexed:4, rate:0.8}로 똑같았다. 아래 recheck 결과를 log[일자]['blog']에 되돌려
    # 쓰지 않아서, 발행 당일 indexed=False로 박힌 가장 오래된 8편이 매일 다시 잡혔고
    # 어제·그제 글은 영원히 표본에 못 들어왔다. 얼어붙은 숫자로 브레이크를 걸거나 풀 수 없다.
    yday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    unindexed = [v for k, v in old_posts.items() if not v.get('indexed')]
    unindexed.sort(key=lambda x: (stamp[norm(x['title'])] != yday,      # 어제 글 먼저
                                  stamp[norm(x['title'])]))            # 그다음 오래된 것부터
    todo = unindexed[:8]
    if todo:
        print('\n=== 지난 글 다시 재기 — 그때 색인 안 됐던 글이 지금은 잡히나')
        again = []
        for b in todo:
            first = stamp[norm(b['title'])]
            r = search_rank(b['title'], BLOGID, 'blog'); time.sleep(0.5)
            sent = drafts.get(norm(b['title']))
            idx = (search_rank('"' + sent + '"', BLOGID, 'blog') is not None) if sent else None
            if sent: time.sleep(0.5)
            if r is not None: idx = True
            print('  %-6s | %-12s | 발행 %s | %s'
                  % (('%d위' % r) if r else '30위 밖',
                     {True: '이제 색인됨', False: '아직 안 됨', None: '본문 없어 못 잼'}[idx],
                     first, b['title'][:36]))
            again.append({'title': b['title'], 'date': b.get('date', ''), 'self_rank': r,
                          'indexed': idx, 'first_seen': first})
            # 색인된 글은 원래 기록에 되돌려 써서 표본에서 빼낸다. 이걸 빼먹으면 같은 8편이
            # 매일 다시 잡히고 어제 글은 끝까지 안 들어온다(b는 log[일자]['blog']의 그 객체다).
            if idx:
                b['indexed'] = True
                if r is not None: b['self_rank'] = r
        got = sum(1 for x in again if x['indexed'])
        able = sum(1 for x in again if x['indexed'] is not None)
        if able: print('  --- 다시 잰 %d편 중 %d편이 뒤늦게 색인됐다 (%d%%)' % (able, got, round(got / able * 100)))
        today['recheck'] = again
        # 하루 지난 글 기준 색인율. 색인에는 하루쯤 걸리므로 '그날 발행분'을 그날 재면 언제나 낮게 나온다.
        # 2026-09-24 12:49 보고가 당일 글 16.7%를 근거로 "발행량을 줄여야 함" 브레이크를 걸었는데,
        # 같은 측정에서 어제 글은 5편 중 4편(80%)이 색인돼 있었다. 판단은 이 숫자로 한다.
        # 어제 글만 골라 센다. 섞어 세면 몇 달 전 글이 표본을 채워 어제 상태를 못 읽는다.
        yy = [x for x in again if x['first_seen'] == yday and x['indexed'] is not None]
        if yy:
            today['mature'] = {'n': len(yy), 'indexed': sum(1 for x in yy if x['indexed']),
                               'rate': round(sum(1 for x in yy if x['indexed']) / len(yy), 3),
                               'basis': '어제(%s) 글' % yday}
            print('  --- 브레이크 기준(어제 %s 글) %d편 중 %d편 색인 (%d%%)'
                  % (yday, len(yy), today['mature']['indexed'], round(today['mature']['rate'] * 100)))
        elif able:
            today['mature'] = {'n': able, 'indexed': got, 'rate': round(got / able, 3),
                               'basis': '어제 글 표본 없음 — 지난 글 전체'}

    # 언제 쟀는지 남긴다. 어제는 17:33, 오늘은 12:49에 재 놓고 같은 조건으로 견줬다(2026-09-24).
    today['at'] = time.strftime('%Y-%m-%d %H:%M')
    log[TODAY] = today
    json.dump(log, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n기록: work/perf_log.json (%d일치)' % len(log))

# rankwatch가 search_rank()만 가져다 쓴다. 가드가 없으면 import만 해도 측정이 통째로 돈다.
if __name__ == '__main__': main()
