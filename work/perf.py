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

def quoted_found(sent, needle=BLOGID, tab='blog'):
    """본문 문장 따옴표 검색에 우리 글이 잡히나. True/False, 검색 자체가 실패하면 None(못 잼).
    2026-09-27: search_rank는 요청 실패·차단(작은 응답)도 None을 돌려줘서 색인 판정이
    '색인 안 됨'으로 적혔다. 못 잰 것을 안 된 것으로 세면 브레이크가 엉뚱하게 걸린다."""
    u = 'https://search.naver.com/search.naver?ssc=tab.%s.all&query=%s' % (tab, urllib.parse.quote('"' + sent + '"'))
    try:
        s = get(u)
    except Exception:
        return None
    if len(s) < 20000:          # 정상 결과 페이지는 30만 바이트대, 차단 응답은 수십 바이트(naver-scrape-limits)
        return None
    links = re.findall(r'https?://(?:m\.)?(?:blog|cafe)\.naver\.com/[A-Za-z0-9_\-/]+', s)
    return any(needle in l for l in links[:60])

def quoted_retry(sent):
    """quoted_found가 None(검색 막힘·작은 응답)이면 몇 초 쉬고 한 번 더.
    2026-09-29 13시 loop: 재측정 8편이 전부 '본문 없어 못 잼'으로 찍혔는데 원고 문장은 다 있었다 —
    연달아 검색하다 작은 응답을 받은 것. 같은 문장을 바로 다시 재면 False(색인 안 됨)로 잡혔다.
    못 잰 이유가 원고 없음인지 검색 막힘인지 섞이면 엉뚱한 곳을 고친다."""
    v = quoted_found(sent)
    if v is None:
        time.sleep(4)
        v = quoted_found(sent)
    return v

def why_none(sent):
    return '원고 없어 못 잼' if not sent else '검색 막혀 못 잼'

# 대조군 — 9/23 이전에 색인이 확인된 우리 글(2026-09-27 blog-noindex 실측). 이 글들도 안 잡히면
# 새 글 색인 0%는 '색인 안 됨'이 아니라 측정이 고장났거나 막힌 것이다. 9/26에 로그인 풀린 채 잰 0%로
# 반나절을 판 뒤 "다시 잴 때는 대조 검색을 같이 돌린다"고 적었는데, 손으로만 돌려서 04시 회차는 빠뜨렸다.
CONTROL_LOGNOS = ('224417955457', '224420188590', '224420736444')

def control_found():
    """블로그탭에서 블로그 아이디로 검색해 대조군 글이 하나라도 잡히나. True/False, 못 재면 None."""
    u = 'https://search.naver.com/search.naver?ssc=tab.blog.all&query=%s' % urllib.parse.quote(BLOGID)
    try:
        s = get(u)
    except Exception:
        return None
    if len(s) < 20000:
        return None
    return any(n in s for n in CONTROL_LOGNOS)

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
    ctl = control_found(); time.sleep(0.5)
    today['control'] = ctl
    print('\n=== 대조군(9/23 이전 색인 확인 글 %d편) — %s' % (len(CONTROL_LOGNOS),
          {True: '잡힌다 = 측정 살아 있음', False: '안 잡힌다 = 측정 고장·차단 의심, 아래 색인 숫자를 믿지 않는다',
           None: '검색 자체가 실패 = 못 잼, 아래 색인 숫자를 믿지 않는다'}[ctl]))
    print('\n=== 블로그 글 — 색인(본문 문장으로 잡히나)과 순위(제목 검색 몇 위)를 따로 본다')
    low = 0; noidx = 0
    for b in blog_posts(N):
        r = search_rank(b['title'], BLOGID, 'blog'); time.sleep(0.5)
        idx = None
        sent = drafts.get(norm(b['title']))
        # 원고가 없는 글(예전 글, 원고 파일명이 다른 글)은 RSS 본문 요약에서 문장을 뽑는다 — 2026-09-22 추가
        if not sent: sent = pick_sentence(b.get('desc', ''))
        if sent:
            idx = quoted_retry(sent); time.sleep(0.5)
        # 제목 검색에 우리 글이 잡혔다면 네이버가 그 글을 아는 것이다 = 색인됨.
        # 본문 문장 따옴표 검색만으로 판정하던 때는 제목 검색 1위인 글도 '색인 안 됨'으로 적혔다
        # (2026-09-24 실측: 9/23 발행 3편이 제목 1위인데 본문 문장으로는 안 잡혔다).
        if r is not None: idx = True
        rank_s = ('%d위' % r) if r else '30위 밖'
        idx_s = {True: '색인됨', False: '색인 안 됨', None: why_none(sent)}[idx]
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
            idx = quoted_retry(sent) if sent else None
            if sent: time.sleep(0.5)
            if r is not None: idx = True
            print('  %-6s | %-12s | 발행 %s | %s'
                  % (('%d위' % r) if r else '30위 밖',
                     {True: '이제 색인됨', False: '아직 안 됨', None: why_none(sent)}[idx],
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
    brake(today, log)


# ---------- 브레이크 ----------
# 2026-09-24 13:05 회차 기록에 이렇게 적혀 있다.
#   "perf 12편 색인 2/12(16.7%) — 어제 같은 시각 같은 조건 8/12(66.7%)에서 떨어져 브레이크 조건에 걸림"
# 걸렸다고 적고는 아무것도 멈추지 않았다. 그 뒤 사흘을 같은 속도로 계속 올렸다.
# 브레이크가 코드가 아니라 **보고에 쓰는 문장**이었기 때문이다. 읽는 사람이 없으면 아무 일도 안 생긴다.
# 그래서 파일로 남긴다. 발행기가 매 회차 이 파일을 읽어 맨 앞에 띄운다.
ALERT = os.path.join(HERE, 'research', '_ALERT.txt')
BRAKE_RATE = 0.50        # 어제 글 색인율이 이 아래면 경고. 9/23은 83%였다
BRAKE_MIN_N = 3          # 표본이 이보다 적으면 판단하지 않는다

def brake(today, log):
    """색인이 무너졌거나 측정이 멈췄으면 경고를 남긴다. 정상이면 경고를 지운다."""
    out = []
    if today.get('control') is not True:
        out.append('대조군(9/23 이전 글)이 검색에 안 잡힌다(%s) — 측정이 막혔을 수 있다, 이번 색인 숫자로 판단하지 않는다'
                   % today.get('control'))
    m = today.get('mature') or {}
    basis_ok = str(m.get('basis', '')).startswith('어제')
    if basis_ok and m.get('n', 0) >= BRAKE_MIN_N and m.get('rate', 1) < BRAKE_RATE:
        out.append('블로그 색인 급락 — 어제 글 %d편 중 %d편만 색인 (%d%%, 기준 %d%%)'
                   % (m['n'], m['indexed'], round(m['rate'] * 100), round(BRAKE_RATE * 100)))
    if m and not basis_ok:
        out.append('색인 측정 표본이 어제 글이 아니다(%s) — 이 숫자로는 판단하지 않는다' % m.get('basis'))

    # 같은 값이 이틀 반복되면 재는 것이 멈춘 것이다. 9/24·25·26 사흘 내내 {n:5,indexed:4}였다.
    sigs = []
    for d in sorted(log)[-3:]:
        mm = log[d].get('mature') or {}
        if mm.get('n') is not None: sigs.append((mm.get('n'), mm.get('indexed')))
    if len(sigs) >= 2 and len(set(sigs)) == 1:
        out.append('색인 수치가 %d일 연속 똑같다 %s — 재는 것이 멈췄는지 본다' % (len(sigs), sigs[0]))

    # 오늘 올린 글이 하나도 안 잡히는데 어제 것도 안 잡히면 둘을 같이 적어 둔다
    b = [x for x in (today.get('blog') or []) if isinstance(x, dict)]
    # 2026-09-29 13:49: 12편 중 10편이 '못 잼'(따옴표 검색이 도중에 막힘)이었는데 "12편 중 색인 0편"으로 적혔다.
    # 실제로 잰 것은 2편이다. 못 잰 글은 분모에서 빼고, 잰 글이 적으면 판단하지 않는다고 적는다.
    bm = [x for x in b if x.get('indexed') is not None]
    if b and len(bm) < len(b):
        out.append('오늘 블로그 %d편 중 %d편은 검색이 막혀 못 잼' % (len(b), len(b) - len(bm)))
    if bm and not any(x.get('indexed') for x in bm):
        out.append('오늘 잰 블로그 %d편 중 색인 0편%s' % (len(bm), '' if len(bm) >= BRAKE_MIN_N else ' (표본이 %d편 미만이라 판단하지 않는다)' % BRAKE_MIN_N))

    os.makedirs(os.path.dirname(ALERT), exist_ok=True)
    if out:
        txt = '[%s]\n' % time.strftime('%Y-%m-%d %H:%M') + '\n'.join('- ' + x for x in out) + '\n'
        open(ALERT, 'w', encoding='utf-8').write(txt)
        print('\n' + '!' * 60)
        print('브레이크 — work/research/_ALERT.txt')
        for x in out: print('  ! ' + x)
        print('!' * 60)
    else:
        if os.path.exists(ALERT): os.remove(ALERT); print('\n브레이크 해제 — 경고 없음')

def read_alert():
    """발행기·감시기가 회차 맨 앞에서 부른다. 경고가 있으면 그 줄들을, 없으면 빈 리스트."""
    try:
        t = open(ALERT, encoding='utf-8').read().strip()
        return [x[2:] for x in t.splitlines() if x.startswith('- ')]
    except Exception:
        return []

# rankwatch가 search_rank()만 가져다 쓴다. 가드가 없으면 import만 해도 측정이 통째로 돈다.
if __name__ == '__main__': main()
