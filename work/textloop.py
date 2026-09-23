# 글 자가발전 루프 — 사장님 2026-09-23 "숏폼뿐만이 아니라 블로그랑 카페도 자가발전 하라고".
#   py -3.12 work/textloop.py       → 한 바퀴 돌고 work/textrule.json + work/research/textrule.md 갱신
#
# 썸네일 루프(loop.py)가 하는 일을 글에 그대로 한다:
#   1) 수집  올린 글의 실제 성과 — 카페는 조회수, 블로그는 색인·제목검색 순위
#   2) 측정  글마다 '손잡이'를 뽑는다. 주제축·형식·제목 길이·제목 숫자·사진 수·본문 길이·발행 시각
#   3) 비교  잘 된 글과 안 된 글의 손잡이 값이 어떻게 다른지 센다
#   4) 규칙  차이가 크고 표본이 충분한 것만 규칙으로 적는다. 나머지는 '표본 부족'이라고 적는다
#   5) 판정  지난번에 적은 규칙을 따른 글이 실제로 더 잘 됐는지 본다. 아니면 규칙을 뺀다
#
# 중요: 조회수는 올린 지 오래될수록 쌓인다. 그래서 '하루당 조회'로 고치고, 18시간이 안 된 글은 제외한다.
#       이걸 안 하면 "새벽에 올린 글이 잘 된다" 같은 가짜 규칙이 나온다.
import sys, os, re, json, glob, time, math, statistics, urllib.request, hashlib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
RULE = os.path.join(HERE, 'textrule.json'); RULE_MD = os.path.join(R, 'textrule.md')
LOG = os.path.join(HERE, 'textloop_log.json')
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
CAFE_ID = '31789001'; BLOG_ID = 'kygstar7777'
MIN_AGE_H = 18        # 이만큼 안 지난 글은 아직 성적을 매길 수 없다
MIN_N = 4             # 한쪽에 이만큼은 있어야 규칙으로 인정한다
MAX_AGE_D = 30        # 이보다 오래된 글은 표본에서 뺀다. 블로그 표본 18편 중 6편이
                      # 95~655일 된 2024~2025년 옛 글이었다(2026-09-24 확인). 요즘 실력과 무관하다

def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def norm(s): return re.sub(r'[^\w가-힣]+', '', (s or '')).lower()

# ── 1) 수집 ────────────────────────────────────────────────────────────────
def cafe_posts(pages=3):
    out = []
    for pg in range(1, pages + 1):
        u = (f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}'
             f'&search.queryType=lastArticle&search.page={pg}&search.perPage=50')
        try: arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25))['message']['result']['articleList']
        except Exception as e: print('카페 API 실패:', str(e)[:80]); break
        if not arts: break
        for a in arts:
            ts = a['writeDateTimestamp'] / 1000
            out.append({'media': 'cafe', 'title': a.get('subject', ''), 'ts': ts, 'read': a.get('readCount', 0)})
    return out

def blog_posts():
    """블로그는 조회수를 주지 않는다. 대신 perf_log의 색인·제목검색 순위를 성적으로 쓴다."""
    perf = load(os.path.join(HERE, 'perf_log.json'), {})
    seen = {}
    for day in sorted(perf):                       # 같은 글은 최신 측정만 남긴다
        for b in (perf[day].get('blog') or []):
            seen[norm(b.get('title'))] = b
    out = []
    try:
        s = urllib.request.urlopen(urllib.request.Request(f'https://rss.blog.naver.com/{BLOG_ID}.xml', headers=UA), timeout=25).read().decode('utf-8', 'ignore')
        import email.utils
        for item in s.split('<item>')[1:]:
            t = re.search(r'<title>(.*?)</title>', item, re.S); d = re.search(r'<pubDate>(.*?)</pubDate>', item)
            if not (t and d): continue
            title = re.sub(r'<!\[CDATA\[|\]\]>', '', t.group(1)).strip()
            b = seen.get(norm(title))
            if not b: continue                     # 아직 성적을 안 잰 글은 뺀다
            score = (1.0 if b.get('indexed') else 0.0) + (1.0 if (b.get('self_rank') or 99) <= 10 else 0.0)
            out.append({'media': 'blog', 'title': title, 'ts': email.utils.parsedate_to_datetime(d.group(1)).timestamp(), 'score': score})
    except Exception as e: print('블로그 RSS 실패:', str(e)[:80])
    return out

# ── 2) 측정: 글마다 손잡이를 뽑는다 ────────────────────────────────────────
def pkg_index():
    """올린 묶음을 제목으로 찾을 수 있게 정리한다. 주제축·형식·사진 수·본문 길이는 묶음에만 있다."""
    idx = {}
    for pk in glob.glob(os.path.join(R, '*', 'pkg')):
        tf = os.path.join(pk, 'title.txt')
        if not os.path.exists(tf): continue
        try: title = open(tf, encoding='utf-8').read().strip()
        except Exception: continue
        body = 0
        for c in sorted(glob.glob(os.path.join(pk, 'c*.txt'))):
            try: body += len(re.sub(r'\s+', '', open(c, encoding='utf-8').read()))
            except Exception: pass
        def rd(n):
            p = os.path.join(pk, n)
            try: return open(p, encoding='utf-8').read().strip().splitlines()[0][:20]
            except Exception: return ''
        idx[norm(title)] = {'axis': rd('axis.txt') or None, 'form': rd('form.txt') or None,
                            'imgs': len(glob.glob(os.path.join(pk, 'img', '*'))), 'body': body}
    return idx

# 묶음에 주제축을 안 적은 옛 글이 49개 중 45개라 이 손잡이가 죽어 있었다(2026-09-23 확인).
# 제목에 실제로 쓰인 말로 축을 되살린다. 묶음의 axis.txt가 있으면 그쪽이 먼저다.
AXIS_WORDS = [
    ('배당·현금흐름', r'배당|분배금|커버드콜|JEPI|JEPQ|SCHD|QYLD|리얼티인컴|VOO|SPY|ETF'),
    ('부동산',        r'부동산|아파트|전세|월세|오피스텔|실거래|집값|청약|주택연금|전세가율'),
    ('연금·세금',     r'연금|IRP|세액공제|소득세|취득세|양도세|건강보험|종부세|금융소득'),
    ('금리·환율',     r'FOMC|금리|환율|점도표|물가|CPI|연준'),
    ('파이어·자산',   r'파이어|은퇴|순자산|자산|목표|모으기|\d+억'),
    ('종목',          r'삼성전자|테슬라|엔비디아|애플|나스닥|코스피|S&P'),
]

def title_end(t):
    """제목을 어떻게 끝냈나. 사장님 2026-09-23 "카페 제목에다가 왜 계속 다를 붙이는 거야?" —
    실측 결과 ~습니다로 끝낸 제목이 하루당 조회 중앙 0.5로 가장 낮았다(명사 끝 1.3, 물음 7.3)."""
    t = t.strip().rstrip('.')
    if re.search(r'(까요|나요|ㄹ까|가요|건가요)\??$', t): return '물음'
    if t.endswith('다'): return '다로 끝'          # 습니다·입니다뿐 아니라 '낮았다·늘었다' 같은 평서형도 같다
    return '명사로 끝'

def guess_axis(title):
    for name, pat in AXIS_WORDS:
        if re.search(pat, title, re.I): return name
    return None

def handles(post, idx):
    """제목·시각은 모든 글에서 뽑을 수 있다. 주제축·형식·사진·본문 길이는 묶음이 있어야만 안다.
    묶음이 없는 옛 글에 0이나 '미상'을 넣으면 '본문 0자가 안 좋다' 같은 가짜 규칙이 나온다 → None으로 비워 둔다."""
    t = post['title']; p = idx.get(norm(t))
    h = {
        '제목길이': len(t),
        '제목에 숫자': '있음' if re.search(r'\d', t) else '없음',
        '제목에 비교(vs·대)': '있음' if re.search(r'\bvs\b|\d\s*대\s*\d', t, re.I) else '없음',
        '제목 끝맺음': title_end(t),
        '발행 시각': time.localtime(post['ts']).tm_hour,
    }
    h.update({'주제축': (p and p['axis']) or guess_axis(t), '형식': (p and p['form']) or None,
              '사진 수': p['imgs'] if p else None, '본문 길이': p['body'] if p else None})
    return h

NUMERIC = {'제목길이', '사진 수', '본문 길이', '발행 시각'}

# ── 3~4) 비교해서 규칙으로 ─────────────────────────────────────────────────
def compare(rows, label):
    """성적 상위 1/3과 하위 1/3의 손잡이를 견준다. 표본이 모자라면 규칙으로 안 쓴다."""
    rows = sorted(rows, key=lambda r: -r['score'])
    n = len(rows); k = max(MIN_N, n // 3)
    if n < MIN_N * 2:
        return [], f'{label} 표본 {n}편 — {MIN_N*2}편은 돼야 견줄 수 있다. 규칙 없음'
    top, bot = rows[:k], rows[-k:]
    found = []
    keys = set().union(*[set(r['h']) for r in rows])
    for key in sorted(keys):
        # 값을 모르는 글(묶음이 없는 옛 글)은 이 손잡이에서 아예 뺀다
        if key in NUMERIC:
            a = [r['h'][key] for r in top if isinstance(r['h'].get(key), (int, float))]
            b = [r['h'][key] for r in bot if isinstance(r['h'].get(key), (int, float))]
            if len(a) < MIN_N or len(b) < MIN_N: continue
            ma, mb = statistics.median(a), statistics.median(b)
            if mb and abs(ma - mb) / max(abs(mb), 1) < 0.25: continue      # 25% 안쪽은 차이로 안 본다
            if ma == mb: continue
            found.append({'손잡이': key, '잘된 글': round(ma, 1), '안된 글': round(mb, 1), '표본': f'{len(a)}대{len(b)}',
                          '규칙': f'{key}은(는) {round(ma,1)} 쪽으로 맞춘다 (잘된 글 {round(ma,1)} vs 안된 글 {round(mb,1)})'})
        else:
            va = [str(r['h'][key]) for r in top if r['h'].get(key) not in (None, '', '미상')]
            vb = [str(r['h'][key]) for r in bot if r['h'].get(key) not in (None, '', '미상')]
            if len(va) < MIN_N or len(vb) < MIN_N: continue
            for val in set(va):
                pa = va.count(val) / len(va); pb = vb.count(val) / len(vb)
                if va.count(val) < 2: continue
                if pa - pb < 0.30: continue                                 # 30%포인트는 벌어져야 본다
                found.append({'손잡이': key, '잘된 글': f'{val} {pa:.0%}', '안된 글': f'{val} {pb:.0%}', '표본': f'{len(va)}대{len(vb)}',
                              '규칙': f'{key}은(는) "{val}"로 한다 (잘된 글의 {pa:.0%}, 안된 글의 {pb:.0%})'})
    found.sort(key=lambda f: -abs(0 if isinstance(f['잘된 글'], str) else f['잘된 글'] - f['안된 글']))
    return found, f'{label} {n}편 중 상위 {k}편과 하위 {k}편 비교'

def by_category(rows, label):
    """상·하위 1/3 비교는 한쪽에 몰린 값을 놓친다. 그래서 갈래별 중앙값도 따로 낸다.
    사장님이 눈으로 잡은 '제목 끝에 다 붙이기'를 상·하위 비교는 못 잡았다(2026-09-23)."""
    out = []
    for key in ('제목 끝맺음', '주제축', '형식'):
        g = {}
        for r in rows:
            v = r['h'].get(key)
            if v in (None, '', '미상'): continue
            g.setdefault(str(v), []).append(r['score'])
        g = {k: v for k, v in g.items() if len(v) >= 3}
        if len(g) < 2: continue
        rank = sorted(g.items(), key=lambda kv: -statistics.median(kv[1]))
        out.append({'손잡이': key,
                    '갈래': [{'값': k, '편수': len(v), '중앙': round(statistics.median(v), 1)} for k, v in rank],
                    '규칙': f'{key}: ' + ' > '.join(f'{k}({len(v)}편 {statistics.median(v):.1f})' for k, v in rank)
                             + f' — "{rank[0][0]}"로 쓰고 "{rank[-1][0]}"는 피한다'})
    return out

# ── 판정 ───────────────────────────────────────────────────────────────────
# 판정이 30회 연속 "규칙 뒤 0편"으로 보류됐다(2026-09-23 18:34 ~ 2026-09-24 08:10).
# 표본은 18시간 지난 글만 쓰는데 기준 시각을 직전 회차(1시간 전)로 잡았으니
# "기준 뒤에 쓴 글"은 산술적으로 언제나 0편이었다. 30회가 우연이 아니라 구조였다.
#
# 기준 뒤에 쓴 글도 18시간이 지나야 성적을 잴 수 있다. 그래서 쓸 수 있는 창은
# (기준 ~ 지금-18시간)뿐이고, 그 창에 MIN_N편이 들어오려면 기준이 그만큼 더 과거여야 한다.
# 기준을 '18시간보다 조금 전'으로 잡으면 창이 한 시간밖에 안 열려 또 0편이 된다.
# 그래서 후보 회차를 다 놓고 '창에 MIN_N편이 실제로 들어오는 것' 중 가장 최근을 고른다.
#
# 규칙 판정과 별개로 추세(trend)는 언제나 낸다. 글을 시간순 절반으로 갈라 견주는 것이라
# 회차 기록이 없어도 "요즘 글이 예전 글보다 나은가"는 답할 수 있다.
def _ts(at): return time.mktime(time.strptime(at, '%Y-%m-%d %H:%M'))

def rule_fp(*groups):
    """이번 규칙의 지문. 규칙이 실제로 바뀐 회차를 찾는 데 쓴다."""
    xs = []
    for g in groups: xs += [f.get('규칙', '') for f in (g or [])]
    return hashlib.md5('|'.join(sorted(xs)).encode('utf-8')).hexdigest()[:10]

def pick_cut(logs, now, posts):
    """판정 기준 시각. 앞뒤 양쪽에 MIN_N편이 실제로 들어오는 회차 중 가장 최근.
    규칙이 바뀐 회차가 그 조건을 만족하면 그쪽을 먼저 쓴다(규칙의 효과를 보는 것이 되므로)."""
    usable = now - MIN_AGE_H * 3600          # 이 시각보다 나중에 쓴 글은 아직 성적을 못 잰다
    ok = []
    for r in logs:
        c = _ts(r['at'])
        if c >= usable: continue
        after = sum(1 for p in posts if c < p['ts'] <= usable)
        before = sum(1 for p in posts if p['ts'] <= c)
        if after >= MIN_N and before >= MIN_N: ok.append(r)
    if not ok:
        span = (now - _ts(logs[0]['at'])) / 3600 if logs else 0
        need = MIN_AGE_H + MIN_N             # 시간당 1편 기준으로 이만큼은 쌓여야 첫 판정이 선다
        return None, f'기록 {span:.0f}시간치 — 앞뒤로 {MIN_N}편씩 갈리려면 {need}시간은 쌓여야 한다'
    changed = [r for r in ok if r.get('rule_changed')]
    r = changed[-1] if changed else ok[-1]
    return _ts(r['at']), r['at'] + (' 규칙 바뀐 회차' if changed else ' 회차')

def judge_side(cut, now, posts, rows, label):
    """기준 시각 앞뒤로 갈라 중앙값을 견준다. 성적을 잴 수 없는 최근 글은 양쪽 다에서 뺀다."""
    usable = now - MIN_AGE_H * 3600
    after = [r['score'] for p, r in zip(posts, rows) if cut < p['ts'] <= usable]
    before = [r['score'] for p, r in zip(posts, rows) if p['ts'] <= cut]
    if len(after) < MIN_N or len(before) < MIN_N:
        return f'{label} 보류(뒤 {len(after)}·앞 {len(before)}편)'
    a, b = statistics.median(after), statistics.median(before)
    arrow = '↑좋아짐' if a > b else ('=변화없음' if a == b else '↓나빠짐')
    return f'{label} {b:.2f} → {a:.2f} {arrow}(뒤 {len(after)}·앞 {len(before)}편)'

SNAP = os.path.join(HERE, 'read_snaps.json')
SNAP_AGE_H = 24        # 모든 글을 '올린 지 24시간' 시점으로 맞춰 견준다

def save_snaps(posts, now):
    """글마다 (측정 시각, 누적 조회)를 찍어 둔다. 나중에 같은 나이에서 견주기 위한 것.
    이걸 안 쌓으면 나이가 다른 글을 견주게 되고, '하루당 조회'가 신생 글을 부풀린다
    (2026-09-24: 34시간 글이 172시간 글보다 덜 읽혔는데 1.79 대 0.50으로 더 좋아 보였다)."""
    s = load(SNAP, {}) or {}
    for p in posts:
        rec = s.setdefault(norm(p['title']), {'ts': p['ts'], 'pts': []})
        if not rec['pts'] or now - rec['pts'][-1][0] > 1800:      # 30분에 한 번만 찍는다
            rec['pts'].append([round(now), p['read']])
            rec['pts'] = rec['pts'][-80:]
    try: json.dump(s, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception as e: print('스냅 저장 실패:', str(e)[:80])
    return s

def read_at(rec, age_h):
    """그 글이 age_h 시간 됐을 때의 누적 조회. 앞뒤 측정 사이는 선형 보간한다.
    아직 그 나이가 안 됐거나 그 나이를 걸치는 측정이 없으면 None."""
    pts = sorted(((m - rec['ts']) / 3600, r) for m, r in rec.get('pts', []))
    if len(pts) < 2: return None
    if pts[0][0] > age_h or pts[-1][0] < age_h: return None
    for (a1, r1), (a2, r2) in zip(pts, pts[1:]):
        if a1 <= age_h <= a2:
            if a2 == a1: return r2
            return r1 + (r2 - r1) * (age_h - a1) / (a2 - a1)
    return None

def trend_aged(posts, snaps, label, now):
    """같은 나이(24시간) 시점의 조회수로 예전 글과 최근 글을 견준다. 나이 편향이 없다.
    스냅샷이 쌓여야 쓸 수 있으므로, 모자라면 무엇이 모자란지 적는다."""
    got = []
    for p in posts:
        rec = snaps.get(norm(p['title']))
        v = read_at(rec, SNAP_AGE_H) if rec else None
        if v is not None: got.append((p['ts'], v))
    if len(got) < MIN_N * 2:
        return f'{label} 나이 맞춘 비교 보류 — {SNAP_AGE_H}시간 시점을 아는 글 {len(got)}편(필요 {MIN_N*2}편, 스냅샷 쌓는 중)'
    got.sort(); half = len(got) // 2
    b = statistics.median([v for _, v in got[:half]])
    a = statistics.median([v for _, v in got[half:]])
    arrow = '↑좋아짐' if a > b else ('=변화없음' if a == b else '↓나빠짐')
    return f'{label} {SNAP_AGE_H}시간 시점 조회 예전 {half}편 {b:.1f} → 최근 {len(got)-half}편 {a:.1f} {arrow}'

def trend(posts, rows, label, now):
    """성적을 잰 글을 시간순 앞 절반·뒤 절반으로 갈라 견준다.
    단, 두 묶음의 '나이'가 비슷할 때만 견준다.

    2026-09-24: 나이를 안 보고 견줬더니 카페가 0.50 → 1.79 "좋아짐"으로 나왔다. 거짓이었다.
    예전 22편은 172시간 된 글(누적 조회 중앙 4회), 최근 23편은 34시간 된 글(누적 2회)이었다.
    실제로는 최근 글이 덜 읽혔는데 '하루당'의 분모가 작아 높게 나온 것이다.
    나이가 2배 넘게 차이나면 견줄 수 없다고 적는다. 가짜 개선 신호를 규칙표에 올리지 않는다."""
    pair = sorted(zip(posts, rows), key=lambda x: x[0]['ts'])
    n = len(pair)
    if n < MIN_N * 2: return f'{label} 추세 보류({n}편)'
    half = n // 2
    age = lambda g: statistics.median([(now - p['ts']) / 3600 for p, _ in g])
    ao, an = age(pair[:half]), age(pair[half:])
    b = statistics.median([r['score'] for _, r in pair[:half]])
    a = statistics.median([r['score'] for _, r in pair[half:]])
    if max(ao, an) / max(min(ao, an), 1) >= 2:
        return (f'{label} 추세 보류 — 예전 {half}편은 {ao:.0f}시간, 최근 {n-half}편은 {an:.0f}시간 된 글이라 '
                f'나이가 달라 견줄 수 없다({b:.2f} vs {a:.2f}는 나이 차이지 실력 차이가 아니다)')
    arrow = '↑좋아짐' if a > b else ('=변화없음' if a == b else '↓나빠짐')
    return f'{label} 예전 {half}편({ao:.0f}h) {b:.2f} → 최근 {n-half}편({an:.0f}h) {a:.2f} {arrow}'

def main():
    t0 = time.time(); now = time.time()
    idx = pkg_index()
    logs = load(LOG, []) or []

    # 카페 — 하루당 조회로 고친다
    cafe_all = cafe_posts()
    cp = [p for p in cafe_all if MIN_AGE_H <= (now - p['ts']) / 3600 <= MAX_AGE_D * 24]
    for p in cp: p['score'] = p['read'] / max((now - p['ts']) / 86400, 0.75)
    cafe_rows = [{'title': p['title'], 'score': p['score'], 'h': handles(p, idx)} for p in cp]

    bp = [p for p in blog_posts() if MIN_AGE_H <= (now - p['ts']) / 3600 <= MAX_AGE_D * 24]
    blog_rows = [{'title': p['title'], 'score': p['score'], 'h': handles(p, idx)} for p in bp]

    cafe_found, cafe_note = compare(cafe_rows, '카페')
    blog_found, blog_note = compare(blog_rows, '블로그')
    cafe_cat = by_category(cafe_rows, '카페')
    blog_cat = by_category(blog_rows, '블로그')

    # 5) 지난 규칙 판정 — 규칙을 적은 뒤에 올린 글의 성적이 그 전보다 나은가
    fp = rule_fp(cafe_found, cafe_cat, blog_found, blog_cat)
    cut, cut_why = pick_cut(logs, now, cp + bp)
    if cut is None:
        verdict = '규칙 판정 보류 — ' + cut_why
    else:
        verdict = (f'{cut_why} 기준 · '
                   + judge_side(cut, now, cp, cafe_rows, '카페 하루당 조회')
                   + ' · ' + judge_side(cut, now, bp, blog_rows, '블로그 색인+순위'))
    # 규칙 판정이 보류여도 추세는 낸다. 이게 "발전하고 있나"에 대한 답이다.
    # 나이를 맞춘 비교(trend_aged)가 먼저다. 그게 아직 안 되면 나이를 밝힌 추세를 낸다.
    snaps = save_snaps(cafe_all, now)
    trends = (trend_aged(cp, snaps, '카페', now) + ' · '
              + trend(cp, cafe_rows, '카페 하루당 조회', now) + ' · '
              + trend(bp, blog_rows, '블로그 색인+순위', now))

    rule = {'at': time.strftime('%Y-%m-%d %H:%M'), 'cafe': cafe_found, 'blog': blog_found,
            'cafe_cat': cafe_cat, 'blog_cat': blog_cat,
            'cafe_note': cafe_note, 'blog_note': blog_note, 'verdict': verdict, 'trend': trends,
            'cafe_median_per_day': round(statistics.median([r['score'] for r in cafe_rows]), 2) if cafe_rows else None}
    json.dump(rule, open(RULE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    md = ['# 글 규칙 (textloop 자동 생성 — 사람이 고치지 않는다)', '',
          f"측정 {rule['at']} · 카페 {len(cafe_rows)}편 · 블로그 {len(blog_rows)}편 · {MIN_AGE_H}시간 안 된 글과 {MAX_AGE_D}일 넘은 글은 뺐다", '',
          f"추세: {trends}", '',
          f"지난 규칙 판정: {verdict}", '',
          '회차 루틴은 글을 쓰기 전에 이 파일을 읽고, 아래 규칙에 맞춰 제목·형식·사진 수를 정한다.', '',
          '## 카페', f'- {cafe_note}']
    md += [f"- {f['규칙']}  (표본 {f['표본']})" for f in cafe_found] or ['- 상·하위 비교에서는 뚜렷한 차이 없음']
    md += [f"- **{f['규칙']}**" for f in cafe_cat]
    md += ['', '## 블로그', f'- {blog_note}']
    md += [f"- {f['규칙']}  (표본 {f['표본']})" for f in blog_found] or ['- 상·하위 비교에서는 뚜렷한 차이 없음']
    md += [f"- **{f['규칙']}**" for f in blog_cat]
    if cafe_rows:
        md += ['', '## 카페 잘된 글 (하루당 조회)']
        for r in sorted(cafe_rows, key=lambda x: -x['score'])[:6]:
            md.append(f"- {r['score']:.1f}/일 · {r['h']['주제축']}/{r['h']['형식']} · {r['title'][:44]}")
        md += ['', '## 카페 안된 글']
        for r in sorted(cafe_rows, key=lambda x: x['score'])[:4]:
            md.append(f"- {r['score']:.1f}/일 · {r['h']['주제축']}/{r['h']['형식']} · {r['title'][:44]}")
    os.makedirs(R, exist_ok=True); open(RULE_MD, 'w', encoding='utf-8').write('\n'.join(md) + '\n')

    logs.append({'at': rule['at'], 'sec': int(time.time() - t0), 'cafe_n': len(cafe_rows), 'blog_n': len(blog_rows),
                 'cafe_rules': len(cafe_found), 'blog_rules': len(blog_found), 'verdict': verdict, 'trend': trends,
                 'fp': fp, 'rule_changed': bool(logs and logs[-1].get('fp') and logs[-1]['fp'] != fp),
                 'cafe_median_per_day': rule['cafe_median_per_day'],
                 'blog_median': round(statistics.median([r['score'] for r in blog_rows]), 2) if blog_rows else None})
    json.dump(logs[-300:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f"[글 루프 {rule['at']}] {int(time.time()-t0)}초 · 카페 {len(cafe_rows)}편 · 블로그 {len(blog_rows)}편")
    print(' ·', cafe_note)
    for f in cafe_found: print('   -', f['규칙'], f"(표본 {f['표본']})")
    for f in cafe_cat: print('   *', f['규칙'])
    print(' ·', blog_note)
    for f in blog_found: print('   -', f['규칙'], f"(표본 {f['표본']})")
    print(' · 추세:', trends)
    print(' · 판정:', verdict)
    print(' · 규칙표:', RULE_MD)

if __name__ == '__main__': main()
