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

def main():
    cal = json.load(open(os.path.join(HERE, 'calendar.json'), encoding='utf-8'))
    cafe_done, blog_done = written()
    rows = []
    allkw = []
    for ev in cal['events']:
        a, b = parse(ev)
        dday = (a - TODAY).days           # 시작까지 남은 날
        end = (b - TODAY).days            # 종료까지 남은 날
        if end < 0: continue              # 이미 끝난 일정
        if dday > HORIZON: continue       # 너무 먼 일정
        allkw += ev['kw']
        rows.append({'ev': ev, 'a': a, 'b': b, 'dday': dday, 'end': end})
    V = vol(sorted(set(allkw)))
    print(f'=== {TODAY} 기준 앞으로 {HORIZON}일 안에 걸린 일정 {len(rows)}건\n')
    out = []
    for r in rows:
        ev = r['ev']
        v = max((V.get(k.replace(' ', ''), 0) for k in ev['kw']), default=0)
        best = max(ev['kw'], key=lambda k: V.get(k.replace(' ', ''), 0))
        wk = fresh(best); time.sleep(0.4)
        # 시의성 점수: 마감 전 lead일 안에 들어왔으면 만점, 진행 중이면 만점, 멀수록 감점
        if r['dday'] <= 0 <= r['end']: timing = 1.0            # 진행 중
        elif r['dday'] <= ev['lead']:  timing = 1.0            # 리드타임 안
        else:                          timing = max(0.2, ev['lead'] / max(1, r['dday']))
        comp = 1.0 if wk is None else max(0.3, 1 - wk / 10)    # 최근 글 많으면 감점
        inc = any(w in cafe_done for w in ev['kw'])
        inb = any(w in blog_done for w in ev['kw'])
        left = (0 if inb else 1) + (0 if inc else 1)      # 아직 안 쓴 매체 수
        vflag = v < 100                                    # 검색수가 가려진 키워드
        score = v * timing * comp * (0.15 if left == 0 else (0.6 if left == 1 else 1.0))
        out.append((score, v, timing, wk, (inb, inc), best, r, vflag))
    out.sort(key=lambda x: -x[0])
    for score, v, timing, wk, marks, best, r, vflag in out:
        ev = r['ev']; inb, inc = marks
        when = ('%02d/%02d' % (r['a'].month, r['a'].day)) + (('~%02d/%02d' % (r['b'].month, r['b'].day)) if r['b'] != r['a'] else '')
        state = '진행 중' if r['dday'] <= 0 <= r['end'] else ('D-%d' % r['dday'])
        todo = []
        if not inb: todo.append('블로그')
        if not inc: todo.append('카페')
        need = ('쓸 곳: ' + '·'.join(todo)) if todo else '둘 다 씀'
        warn = ' [날짜 미확인]' if ev['src'] == '미확인' else ''
        if vflag: warn += ' [검색수 조회 불가]'
        print('%9s  %s %7s | 검색 %7s | 최근7일글 %s/10 | %-16s | %s%s' % (format(int(score), ','), when, state, format(v, ','), wk if wk is not None else '?', need, ev['name'], warn))
        print('%11s  대표 검색어: %s · 근거: %s' % ('', best, ev['src']))
    print('')
    print('점수 = 검색수 x 시의성 x (1-경쟁) x (둘 다 썼으면 0.15, 한 곳만 0.6)')
    print('검색수 100 미만은 검색광고 API가 값을 가린 것 - 순위를 믿지 말고 사람이 판단할 것')

main()
