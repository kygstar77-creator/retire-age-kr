# 이번에 쓸 글 고르기 — 날짜(시의성) × 검색수 × 경쟁 × 이미 쓴 글 제외
# 사용: python work/pick.py [며칠치=45]
# 조회수는 검색수가 아니라 마감일이 만든다. 그래서 일정표를 1순위로 둔다.
import sys, json, os, re, time, datetime, urllib.request, urllib.parse, html, hmac, hashlib, base64
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
TODAY = datetime.date.today()
HORIZON = int(sys.argv[1]) if len(sys.argv) > 1 else 45

def kv():
    p = r'C:\Users\강영준\Documents\naver_searchad.txt'
    d = {}
    for line in open(p, encoding='utf-8-sig'):
        if '=' in line:
            k, v = line.strip().split('=', 1); d[k.strip().upper()] = v.strip()
    return d
K = kv()

def vol(words):
    """월간 검색수 합계(최대 5개씩)"""
    out = {}
    for i in range(0, len(words), 5):
        ts = str(int(time.time() * 1000)); uri = '/keywordstool'
        sig = base64.b64encode(hmac.new(K['SECRET_KEY'].encode(), f'{ts}.GET.{uri}'.encode(), hashlib.sha256).digest()).decode()
        q = urllib.parse.urlencode({'hintKeywords': ','.join(w.replace(' ', '') for w in words[i:i+5]), 'showDetail': '1'})
        req = urllib.request.Request('https://api.searchad.naver.com' + uri + '?' + q, headers={
            'X-Timestamp': ts, 'X-API-KEY': K['ACCESS_LICENSE'], 'X-Customer': K['CUSTOMER_ID'], 'X-Signature': sig})
        try:
            for r in json.load(urllib.request.urlopen(req, timeout=20))['keywordList']:
                n = lambda v: int(v) if str(v).isdigit() else 5
                out[r['relKeyword']] = n(r['monthlyPcQcCnt']) + n(r['monthlyMobileQcCnt'])
        except Exception:
            pass
        time.sleep(0.35)
    return out

def fresh(kw):
    """블로그 탭 상위 10개 중 최근 7일 글 수. 많을수록 경쟁이 세다."""
    try:
        s = urllib.request.urlopen(urllib.request.Request(
            'https://search.naver.com/search.naver?ssc=tab.blog.all&query=' + urllib.parse.quote(kw), headers=UA), timeout=18).read().decode('utf-8', 'ignore')
    except Exception:
        return None
    d = re.findall(r'>(\d{4}\.\d{1,2}\.\d{1,2}\.|\d+(?:일|시간|분|주|개월) 전|어제)<', s)[:10]
    if not d: return None
    wk = sum(1 for x in d if ('시간' in x or '분' in x or x == '어제' or (x.endswith('일 전') and int(x.split('일')[0]) <= 7)
                              or x == TODAY.strftime('%Y.%m.%d.')))
    return wk

def written():
    """이미 쓴 글 — (카페 제목들, 블로그 제목들). 양쪽 다 제목만 본다.
    본문까지 보면 스쳐 지나간 단어 하나로 '썼다'가 되어 카페가 전부 막힌다."""
    cafe = ''
    p = os.path.join(HERE, '..', 'src', 'firemap-v2', 'cafePosts.js')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        cafe = ' '.join(re.findall(r'title:\s*[\'"`](.*?)[\'"`]\s*,', s))
    blog = ''
    try:
        s = urllib.request.urlopen(urllib.request.Request('https://rss.blog.naver.com/kygstar7777.xml', headers=UA), timeout=18).read().decode('utf-8', 'ignore')
        blog = ' '.join(html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', x)) for x in re.findall(r'<title>(.*?)</title>', s, re.S))
    except Exception:
        pass
    return cafe, blog

def parse(ev):
    """일정을 (시작일, 종료일)로. 매년 반복이면 올해로 맞추고, 지났으면 내년."""
    s = ev['date']
    if s.startswith('매월'):
        day = int(re.search(r'(\d+)', s).group(1))
        d = TODAY.replace(day=day)
        if d < TODAY: d = (d.replace(day=1) + datetime.timedelta(days=32)).replace(day=day)
        return d, d
    parts = s.split('~')
    def one(x):
        x = x.strip()
        if re.match(r'^\d{4}-', x): return datetime.date(*map(int, x.split('-')))
        m, dd = map(int, x.split('-'))
        d = datetime.date(TODAY.year, m, dd)
        return d
    a = one(parts[0]); b = one(parts[-1])
    if b < TODAY and not re.match(r'^\d{4}-', parts[-1].strip()):
        a = a.replace(year=a.year + 1); b = b.replace(year=b.year + 1)
    return a, b

def mark(kw, cafe_done, blog_done):
    """이미 쓴 곳 표시. 감점하지 않는다 - 좋은 주제는 각도를 바꿔 여러 편 써도 된다.
    다만 같은 각도로 또 쓰면 네이버 유사문서 판독시스템이 복사글로 묶으니 각도를 바꾼다."""
    inb = any(w.replace(' ', '') in blog_done.replace(' ', '') for w in kw)
    inc = any(w.replace(' ', '') in cafe_done.replace(' ', '') for w in kw)
    if inb and inc: return '블로그·카페 씀'
    if inb: return '블로그 씀'
    if inc: return '카페 씀'
    return '아직 안 씀'

def section_cal(cal, cafe_done, blog_done):
    rows, allkw = [], []
    for ev in cal['events']:
        a, b = parse(ev)
        dday, end = (a - TODAY).days, (b - TODAY).days
        if end < 0 or dday > HORIZON: continue
        allkw += ev['kw']; rows.append({'ev': ev, 'a': a, 'b': b, 'dday': dday, 'end': end})
    V = vol(sorted(set(allkw)))
    out = []
    for r in rows:
        ev = r['ev']
        v = max((V.get(k.replace(' ', ''), 0) for k in ev['kw']), default=0)
        best = max(ev['kw'], key=lambda k: V.get(k.replace(' ', ''), 0))
        wk = fresh(best); time.sleep(0.4)
        if r['dday'] <= 0 <= r['end']: timing = 1.0
        elif r['dday'] <= ev['lead']:  timing = 1.0
        else:                          timing = max(0.2, ev['lead'] / max(1, r['dday']))
        comp = 1.0 if wk is None else max(0.3, 1 - wk / 10)
        out.append((v * timing * comp, v, wk, best, r))
    out.sort(key=lambda x: -x[0])
    print('=== A. 마감이 있는 주제 — 앞으로 %d일 (%d건)' % (HORIZON, len(out)))
    print('    점수 = 검색수 x 시의성 x (1-경쟁). 이미 쓴 것도 각도를 바꾸면 또 쓸 수 있다.\n')
    for score, v, wk, best, r in out:
        ev = r['ev']
        when = ('%02d/%02d' % (r['a'].month, r['a'].day)) + (('~%02d/%02d' % (r['b'].month, r['b'].day)) if r['b'] != r['a'] else '')
        state = '진행 중' if r['dday'] <= 0 <= r['end'] else ('D-%d' % r['dday'])
        warn = ' [날짜 미확인]' if ev['src'] == '미확인' else ''
        if v < 100: warn += ' [검색수 조회 불가]'
        print('%9s  %-13s %6s | %-4s | 검색 %7s | 최근7일글 %s/10 | %-13s | %s%s' % (
            format(int(score), ','), when, state, ev.get('axis', '?'), format(v, ','),
            wk if wk is not None else '?', mark(ev['kw'], cafe_done, blog_done), ev['name'], warn))
        print('%11s  대표 검색어: %s · 근거: %s' % ('', best, ev['src']))

def section_pool(cafe_done, blog_done):
    p = os.path.join(HERE, 'topics.json')
    if not os.path.exists(p):
        print('\n(topics.json 없음 — 상시 주제 건너뜀)'); return
    T = json.load(open(p, encoding='utf-8'))['topics']
    # 시세 조회형(quote)은 통합검색 최상단이 네이버 증권/환율 위젯이라 뒤로 민다. fire는 C에서 따로 낸다.
    hot = [t for t in T if t['axis'] != 'fire' and not t.get('quote')]
    hot.sort(key=lambda t: -t['vol'])
    head = hot[:26]
    dirty = False
    for t in head:                                  # 경쟁도 미측정이면 그 자리에서 재고 파일에 남긴다
        if t['week'] is None:
            t['week'] = fresh(t['kw']); dirty = True; time.sleep(0.4)
    if dirty:
        json.dump(json.load(open(p, encoding='utf-8')) | {'topics': T},
                  open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    head.sort(key=lambda t: -(t['vol'] * (1.0 if t['week'] is None else max(0.3, 1 - t['week'] / 10))))
    print('\n\n=== B. 마감은 없고 늘 수요가 있는 주제 (상위 14 / 글감형 %d건)' % len(hot))
    print('    점수 = 검색수 x (1-경쟁). A와 같은 자로 잰 게 아니니 A와 섞어서 비교하지 말 것.')
    print('    시세 조회형(XX주가·XX지수·XX환율) %d건은 뺐다 - 통합검색 최상단이 네이버 증권/환율 위젯이다.\n'
          % sum(1 for t in T if t.get('quote')))
    for t in head[:14]:
        s = t['vol'] * (1.0 if t['week'] is None else max(0.3, 1 - t['week'] / 10))
        print('%9s  %-10s | 검색 %7s | 최근7일글 %s/10 | %-13s | %s' % (
            format(int(s), ','), t['axis'], format(t['vol'], ','),
            t['week'] if t['week'] is not None else '?', mark([t['kw']], cafe_done, blog_done), t['kw']))
    fire = [t for t in T if t['axis'] == 'fire']
    fire.sort(key=lambda t: -t['vol'])
    print('\n\n=== C. 카페에서 읽히는 축 (fire) — 검색이 아니라 조회수로 가는 주제 (%d건)' % len(fire))
    print('    검색수가 작다고 나쁜 주제가 아니다. 파이어족 카페 실측 조회수 중앙값 248인데')
    print('    이 축(순자산·계층·파이어 금액·나이 비교)이 가장 높았다. 검색수로 줄세우지 말 것.\n')
    for t in fire[:10]:
        print('%9s  %-10s | 검색 %7s | %-13s | %s' % (
            '', t['axis'], format(t['vol'], ','), mark([t['kw']], cafe_done, blog_done), t['kw']))

def main():
    cal = json.load(open(os.path.join(HERE, 'calendar.json'), encoding='utf-8'))
    cafe_done, blog_done = written()
    section_cal(cal, cafe_done, blog_done)
    section_pool(cafe_done, blog_done)
    print('\n검색수 100 미만은 검색광고 API가 값을 가린 것 - 순위를 믿지 말고 사람이 판단할 것')
    print('축: ' + ' · '.join('%s=%s' % (k, v) for k, v in cal.get('axes', {}).items()))

main()
