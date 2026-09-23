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
import sys, os, re, json, glob, time, math, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
RULE = os.path.join(HERE, 'textrule.json'); RULE_MD = os.path.join(R, 'textrule.md')
LOG = os.path.join(HERE, 'textloop_log.json')
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
CAFE_ID = '31789001'; BLOG_ID = 'kygstar7777'
MIN_AGE_H = 18        # 이만큼 안 지난 글은 아직 성적을 매길 수 없다
MIN_N = 4             # 한쪽에 이만큼은 있어야 규칙으로 인정한다

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
        '제목이 문장으로 끝남': '있음' if re.search(r'(니다|습니다|까요|요)[.?]?$', t.strip()) else '없음',
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

def main():
    t0 = time.time(); now = time.time()
    idx = pkg_index()
    logs = load(LOG, []) or []

    # 카페 — 하루당 조회로 고친다
    cp = [p for p in cafe_posts() if (now - p['ts']) / 3600 >= MIN_AGE_H]
    for p in cp: p['score'] = p['read'] / max((now - p['ts']) / 86400, 0.75)
    cafe_rows = [{'title': p['title'], 'score': p['score'], 'h': handles(p, idx)} for p in cp]

    bp = [p for p in blog_posts() if (now - p['ts']) / 3600 >= MIN_AGE_H]
    blog_rows = [{'title': p['title'], 'score': p['score'], 'h': handles(p, idx)} for p in bp]

    cafe_found, cafe_note = compare(cafe_rows, '카페')
    blog_found, blog_note = compare(blog_rows, '블로그')

    # 5) 지난 규칙 판정 — 규칙을 적은 뒤에 올린 글의 성적이 그 전보다 나은가
    verdict = '(첫 회차)'
    if logs:
        prev = logs[-1]; cut = time.mktime(time.strptime(prev['at'], '%Y-%m-%d %H:%M'))
        after = [r['score'] for p, r in zip(cp, cafe_rows) if p['ts'] > cut]
        before = [r['score'] for p, r in zip(cp, cafe_rows) if p['ts'] <= cut]
        if len(after) >= MIN_N and len(before) >= MIN_N:
            a, b = statistics.median(after), statistics.median(before)
            verdict = f"규칙 적용 뒤 카페 하루당 조회 중앙값 {b:.1f} → {a:.1f} " + ('↑좋아짐' if a > b else ('=변화없음' if a == b else '↓나빠짐'))
        else:
            verdict = f'판정 보류 — 규칙 뒤 {len(after)}편, 앞 {len(before)}편으로 표본 부족'

    rule = {'at': time.strftime('%Y-%m-%d %H:%M'), 'cafe': cafe_found, 'blog': blog_found,
            'cafe_note': cafe_note, 'blog_note': blog_note, 'verdict': verdict,
            'cafe_median_per_day': round(statistics.median([r['score'] for r in cafe_rows]), 2) if cafe_rows else None}
    json.dump(rule, open(RULE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    md = ['# 글 규칙 (textloop 자동 생성 — 사람이 고치지 않는다)', '',
          f"측정 {rule['at']} · 카페 {len(cafe_rows)}편 · 블로그 {len(blog_rows)}편 · 18시간 안 된 글은 뺐다", '',
          f"지난 규칙 판정: {verdict}", '',
          '회차 루틴은 글을 쓰기 전에 이 파일을 읽고, 아래 규칙에 맞춰 제목·형식·사진 수를 정한다.', '',
          '## 카페', f'- {cafe_note}']
    md += [f"- {f['규칙']}  (표본 {f['표본']})" for f in cafe_found] or ['- 아직 뚜렷한 차이 없음']
    md += ['', '## 블로그', f'- {blog_note}']
    md += [f"- {f['규칙']}  (표본 {f['표본']})" for f in blog_found] or ['- 아직 뚜렷한 차이 없음']
    if cafe_rows:
        md += ['', '## 카페 잘된 글 (하루당 조회)']
        for r in sorted(cafe_rows, key=lambda x: -x['score'])[:6]:
            md.append(f"- {r['score']:.1f}/일 · {r['h']['주제축']}/{r['h']['형식']} · {r['title'][:44]}")
        md += ['', '## 카페 안된 글']
        for r in sorted(cafe_rows, key=lambda x: x['score'])[:4]:
            md.append(f"- {r['score']:.1f}/일 · {r['h']['주제축']}/{r['h']['형식']} · {r['title'][:44]}")
    os.makedirs(R, exist_ok=True); open(RULE_MD, 'w', encoding='utf-8').write('\n'.join(md) + '\n')

    logs.append({'at': rule['at'], 'sec': int(time.time() - t0), 'cafe_n': len(cafe_rows), 'blog_n': len(blog_rows),
                 'cafe_rules': len(cafe_found), 'blog_rules': len(blog_found), 'verdict': verdict,
                 'cafe_median_per_day': rule['cafe_median_per_day']})
    json.dump(logs[-300:], open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f"[글 루프 {rule['at']}] {int(time.time()-t0)}초 · 카페 {len(cafe_rows)}편 · 블로그 {len(blog_rows)}편")
    print(' ·', cafe_note)
    for f in cafe_found: print('   -', f['규칙'], f"(표본 {f['표본']})")
    print(' ·', blog_note)
    for f in blog_found: print('   -', f['규칙'], f"(표본 {f['표본']})")
    print(' · 판정:', verdict)
    print(' · 규칙표:', RULE_MD)

if __name__ == '__main__': main()
