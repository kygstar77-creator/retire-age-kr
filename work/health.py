# 계기판 — 파이어맵 전 영역을 한 자로 재고, 목표 대비 부족분(gap)을 순위로 낸다.
#   py -3.12 work/health.py            → 화면 출력 + work/health.json
# selfloop.py가 이걸 읽어 "이번 회차에 무엇을 고칠지"를 정한다. 사람이 고르지 않는다.
# 각 항목: value(실측) / target(목표) / weight(중요도) / how(못 미치면 무엇을 봐야 하는지)
import sys, os, re, json, glob, time, subprocess, statistics, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'research')
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}

def load(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def sh(*a, timeout=900):
    try:
        r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout, cwd=os.path.dirname(HERE))
        return (r.stdout or '') + (r.stderr or '')
    except Exception as e: return 'ERR ' + str(e)[:80]

def rss_today():
    try:
        s = urllib.request.urlopen(urllib.request.Request('https://rss.blog.naver.com/kygstar7777.xml', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
        return len([d for d in re.findall(r'<pubDate>(.*?)</pubDate>', s) if time.strftime('%d %b %Y') in d])
    except Exception: return None

CAFE_MIN_AGE_H = 24     # 조회를 잴 수 있는 최소 나이. 이보다 어린 글은 표본에서 뺀다

def cafe_today():
    """(오늘 편수, 24시간 지난 글의 조회 중앙값, 24시간 안 된 글의 조회 중앙값, 표본 수).

    2026-09-26: 조회 중앙값을 '최근 20편'으로 재고 있었다. 카페는 하루 4편을 올리므로
    최근 20편이면 18편이 21시간 안 된 글이고, 갓 올린 글은 조회가 0이다. 그래서 실측
    중앙값 0.5가 나왔는데, 같은 시각 24시간 지난 32편의 중앙값은 2.0(평균 3.97)이었다.
    발행을 잘할수록(새 글이 표본을 채울수록) 계기판이 나빠지는 셈이다 — 이 파일이 색인율
    (당일 글 -> 하루 지난 글)·방문(오늘 -> 마지막 완결일)에서 이미 두 번 고친 것과 같은 고장.
    textloop.py 는 처음부터 18시간 안 된 글을 빼고 24시간 시점으로 맞춰 견주고 있었다."""
    try:
        u = 'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=31789001&search.queryType=lastArticle&search.page=1&search.perPage=50'
        arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
        today = time.strftime('%Y-%m-%d'); now = time.time()
        n = sum(1 for a in arts if time.strftime('%Y-%m-%d', time.localtime(a['writeDateTimestamp'] / 1000)) == today)
        aged, fresh = [], []
        for a in arts:
            age_h = (now - a['writeDateTimestamp'] / 1000) / 3600
            (aged if age_h >= CAFE_MIN_AGE_H else fresh).append(a.get('readCount', 0))
        med = lambda xs: (statistics.median(xs) if xs else None)
        return n, med(aged), med(fresh), len(aged)
    except Exception: return None, None, None, 0

def _cafe_cap():
    """카페 하루 상한. 못 읽으면 None(막힌 회차로 치지 않는다)."""
    try:
        sys.path.insert(0, HERE)
        from naverpost import DAY_CAP
        return DAY_CAP.get('cafe')
    except Exception:
        return None


def main():
    M = []   # (영역, 항목, 값, 목표, 중요도, 어떻게 고치나)
    runs = load(os.path.join(HERE, 'runs_today.json'), {'runs': []})['runs']
    nb = sum(1 for r in runs if (r.get('blog') or {}).get('url')); nc = sum(1 for r in runs if (r.get('cafe') or {}).get('url'))
    # 발행 의무가 있는 회차만 센다. 감시기(:45)·보고 회차도 같은 파일에 append하는데
    # 그 회차는 발행이 일이 아니라서, 예전엔 2026-09-24 03시처럼 발행 3회차가 전부 2편씩
    # 나갔는데도 '0편 회차 3'으로 잡혀 일감표 1번을 계속 차지했다.
    def 발행회차(r):
        if r.get('role') in ('watchdog', 'report', 'improve'): return False
        return not re.match(r'\s*(감시기? 회차|보고 회차|자가발전 회차)', r.get('note') or '')
    def 냈나(r): return bool((r.get('blog') or {}).get('url') or (r.get('cafe') or {}).get('url'))
    zero_all = sum(1 for r in runs if 발행회차(r) and not 냈나(r))
    # 이미 끝난 장애까지 하루 종일 세지 않는다. 2026-09-25 00~10시 0편 6회는 전부
    # 네이버 IP 확인 차단 하나였고 11:30에 풀렸는데, 누적으로 세니 그 뒤로 정상 발행이
    # 이어져도 '0편 회차 6'이 일감표 1번을 하루 내내 차지해 실제 할 일을 밀어냈다.
    # 그래서 '마지막으로 발행에 성공한 회차 이후'의 0편만 센다 — 지금도 이어지는 고장만 남는다.
    last_ok = max((i for i, r in enumerate(runs) if 냈나(r)), default=-1)
    # 새벽 2~7시는 블로그를 쉬므로 올릴 수 있는 곳이 카페뿐인데, 그 시각에 카페가 이미
    # 하루 상한(DAY_CAP)에 닿아 있으면 그 회차는 무엇을 해도 0편이다 — 고장이 아니라 설계다.
    # 2026-09-26 04·05시 두 회차가 정확히 이 경우였는데 '0편 회차 2'로 잡혀 일감표 1번을
    # 차지했다. 회차가 닫을 수 없는 항목이 1번에 앉으면 실제 할 일이 밀린다(위 두 주석과 같은 사고).
    # 상한 자체가 지시서(24편)와 어긋나는 문제는 사람이 볼 일이라 tools-wanted.md에 따로 올라가 있다.
    def 막힌회차(i, r):
        h = r.get('hour')
        if h is None or not (2 <= h < 8): return False
        cap = _cafe_cap()
        if cap is None: return False
        return sum(1 for x in runs[:i] if (x.get('cafe') or {}).get('url')) >= cap
    blocked = [i for i, r in enumerate(runs) if i > last_ok and 발행회차(r) and not 냈나(r) and 막힌회차(i, r)]
    zero = sum(1 for i, r in enumerate(runs) if i > last_ok and 발행회차(r) and not 냈나(r) and i not in blocked)
    how_zero = '0편 사유를 없앤다(대기 묶음 3+3 유지가 가장 흔한 원인)'
    if zero_all > zero: how_zero += f' · 오늘 누적 {zero_all}회였으나 마지막 발행 성공 뒤로는 {zero}회(이미 끝난 장애는 빼고 센다)'
    if blocked: how_zero += f' · 새벽 카페 상한에 막혀 애초에 올릴 수 없던 회차 {len(blocked)}회는 빼고 센다'
    # 목표 편수는 naverpost.DAY_CAP(실측으로 건 하루 상한)을 따른다. 두 군데에 숫자를
    # 따로 적어 두면 어긋난다 — 2026-09-26 04시에 실제로 어긋났다. 카페 상한을 4편으로
    # 건 뒤에도 여기 목표가 24편으로 남아 있어, 일감표 1·2번이 영영 못 닫는 항목으로
    # 굳었고 회차마다 "카페 4/24 부족"을 띄워 막힌 벽에 계속 발행을 시도하게 만들었다.
    # 상한이 걸린 종류는 상한이 곧 목표다. 안 걸린 블로그는 새벽 2~7시를 쉬므로 18편.
    def 목표(kind, 기본):
        try:
            sys.path.insert(0, HERE)
            from naverpost import DAY_CAP
            return DAY_CAP.get(kind, 기본)
        except Exception:
            return 기본
    # 목표는 '하루가 끝났을 때'가 아니라 '지금 시각까지 나갔어야 할' 편수로 잰다.
    # 왜(2026-09-26 07시): 블로그는 새벽 2~7시를 일부러 쉬는데 목표가 18로 고정이라,
    # 07시에 2편이면 규정을 정확히 지킨 것인데도 부족분 2.667로 일감표 1번에 앉았다.
    # 새벽 여섯 회차가 내리 이 항목을 1번으로 받아 "0편 사유 확인"을 시켰고, 사유는
    # 매번 "쉬는 시간대라 안 올림"이었다. 회차가 닫을 수 없는 항목이 1번을 차지하면
    # 실제 할 일이 밀린다(위 주석들과 같은 사고가 네 번째다).
    # 블로그 슬롯은 00·01시와 08~23시 열여덟 자리. 지금 회차는 아직 진행 중이라 빼고,
    # 이미 지나간 슬롯만 센다. 하루가 다 돌면 18이 되어 종전과 같아진다.
    BLOG_SLOTS = [0, 1] + list(range(8, 24))
    def 지금까지목표(slots, cap):
        h = time.localtime().tm_hour
        due = sum(1 for x in slots if x < h)
        return min(due, cap) if cap else due
    blog_due = 지금까지목표(BLOG_SLOTS, 목표('blog', 18))
    M += [('발행', '오늘 블로그 편수', nb, blog_due, 3, f'지금 시각까지 나갔어야 할 {blog_due}편 기준(새벽 2~7시는 쉼) · 모자라면 회차 note에서 0편 사유 확인 → 대기 묶음·가드·시간초과'),
          ('발행', '오늘 카페 편수', nc, 목표('cafe', 24), 3, '위와 같음'),
          ('발행', '0편 회차 수', zero, 0, 3, how_zero)]
    pend = sh(os.path.join(HERE, 'naverpost.py'), 'pending')
    pb = len(re.findall(r'"kind": "blog"', pend)); pc = len(re.findall(r'"kind": "cafe"', pend))
    M += [('발행', '대기 묶음 블로그', pb, 3, 3, 'firemap-improve B/F 회차가 완성 묶음을 만든다'),
          ('발행', '대기 묶음 카페', pc, 3, 3, '위와 같음')]

    # 빵꾸 감시 — 2026-09-23 오후 내내 0편이었는데 아무도 몰랐다(예약이 오전까지만 있었다).
    # 회차 기록이 아니라 실제 네이버에서 잰다. 1이면 한 회차를 놓친 것.
    try:
        sys.path.insert(0, HERE); import naverpost as _np
        # 새벽 2~7시는 블로그를 일부러 쉰다(사장님 2026-09-25). watchdog은 이걸 알고 안 메우는데
        # 여기서는 안 봐서, 새벽마다 "블로그 빵꾸"가 일감표 1순위로 올라왔다. 쉬는 걸 빵꾸로 세지 않는다.
        _quiet = 2 <= time.localtime().tm_hour < 8
        for kind, ko in (('blog', '블로그'), ('cafe', '카페')):
            if _quiet and kind == 'blog':
                M.append(('발행', f'{ko} 발행 빵꾸', 0, 0, 3, '새벽 2~7시는 블로그를 쉬는 시간대라 빵꾸로 세지 않는다'))
                continue
            # 빵꾸 기준은 그 매체가 실제로 지켜야 하는 간격에서 끌어온다(2026-09-26).
            # 75분 고정이던 때: 카페는 하루 4편 상한이라 다섯 시간 간격이 정상인데도
            # 상한을 다 채운 날조차 스무 시간 내내 "빵꾸"로 떠서 일감표 1순위를 차지했다.
            # 계기판이 재촉하는데 발행기는 상한으로 막는, 서로 어긋난 두 기준이었다.
            gap = getattr(_np, 'GAP_MIN', {}).get(kind, 75)
            late = gap + 60                      # 회차가 늦게 끝나는 여유
            cap = getattr(_np, 'DAY_CAP', {}).get(kind)
            done = _np.published_today(kind) if cap else None
            if cap and done is not None and done >= cap:
                M.append(('발행', f'{ko} 발행 빵꾸', 0, 0, 3,
                          f'오늘 {done}편으로 상한({cap}편)을 채웠다 — 더 올리지 않는 게 맞다'))
                continue
            mm = _np.last_published_minutes(kind)
            if mm is not None:
                M.append(('발행', f'{ko} 발행 빵꾸({late}분 초과)', 1 if mm > late else 0, 0, 3,
                          f'지금 {mm/60:.1f}시간 전이 마지막. py -3.12 work/watchdog.py 로 즉시 메운다'))
    except Exception as e: print('빵꾸 측정 실패:', str(e)[:60])

    # 글 자가발전 — 규칙표가 낡으면 회차가 옛 규칙으로 쓴다
    tr = load(os.path.join(HERE, 'textrule.json'), {})
    if tr:
        try: old_h = (time.time() - time.mktime(time.strptime(tr['at'], '%Y-%m-%d %H:%M'))) / 3600
        except Exception: old_h = 99
        M.append(('품질', '글 규칙 낡음(12시간 초과)', 1 if old_h > 12 else 0, 0, 2, 'py -3.12 work/textloop.py 로 성과→규칙을 다시 뽑는다'))
        M.append(('품질', '카페 하루당 조회 중앙값', tr.get('cafe_median_per_day') or 0, 5, 2,
                  'work/research/textrule.md의 규칙을 회차가 실제로 따르는지 확인'))

    pkgs = [p for p in glob.glob(os.path.join(R, '*', 'pkg')) if os.path.exists(os.path.join(p, 'published.txt'))]
    recent = sorted(pkgs, key=lambda p: -os.path.getmtime(os.path.join(p, 'published.txt')))[:20]
    ver = [load(os.path.join(p, 'verify.txt'), {}) for p in recent]
    okv = sum(1 for v in ver if v and v.get('ok'))
    # 2026-09-24: 검증 비율이 check_gpt.txt만 세는 바람에 제미나이 무료 할당량(429)이 차는 날은
    # 모든 묶음이 selfcheck로 제대로 검증됐는데도 0.0으로 찍혔다. 그러면 일감표 맨 위에 영영 남고
    # 회차가 닫을 수 없는 항목이 된다. 사장님 지시(2026-09-23)대로 selfcheck도 검증으로 센다.
    # 다만 바깥 모델을 못 쓴 사실은 따로 보이게 남긴다 — 429가 숨지 않도록.
    def _has(p, *names): return any(os.path.exists(os.path.join(p, n)) for n in names)
    cc = sum(1 for p in recent if _has(p, 'check_gpt.txt', 'check_gemini.txt', 'check_self.txt'))
    ext = sum(1 for p in recent if _has(p, 'check_gpt.txt', 'check_gemini.txt'))
    M += [('품질', '최근 20편 실물검증 통과율', round(okv / max(1, len(recent)), 3), 0.95, 3, 'naverpost verify BAD → rewrite'),
          ('품질', '최근 20편 검증 비율(교차 또는 자체)', round(cc / max(1, len(recent)), 3), 1.0, 3, '검증 없이 발행한 회차 확인 → crosscheck 실패 시 selfcheck 필수'),
          ('품질', '최근 20편 바깥모델 교차검증 비율', round(ext / max(1, len(recent)), 3), 1.0, 1, '제미나이 429면 selfcheck로 대체됨 — 유료 키가 생기면 올라간다')]

    perf = load(os.path.join(HERE, 'perf_log.json'), {})
    if perf:
        last = perf[sorted(perf)[-1]]; b = last.get('blog', [])
        # 색인율은 '하루 지난 글'로 잰다. 그날 발행분을 그날 재면 색인될 시간이 없어 언제나 낮다
        # (2026-09-24: 당일 글 0% · 같은 측정에서 어제 글 80%). mature가 없으면 당일 값으로 두되 목표를 낮춘다.
        mt = last.get('mature')
        if mt:
            M.append(('검색', '색인율(하루 지난 글)', mt['rate'], 0.8, 3,
                      f"{mt['n']}편 중 {mt['indexed']}편 · 색인 안 된 글의 본문 문장 검색 → 유사문서·품질 확인"))
        # 순위도 색인율과 같은 이유로 '하루 지난 글'로 잰다. 색인이 안 된 글은 제목으로 검색해도
        # 안 잡히니 self_rank 가 None 이고, 그날 발행분은 거의 다 그 상태다 — 이 눈금을 당일 글로 재면
        # 0.0 에 붙박여 일감표 맨 위에 영영 남는다(2026-09-25 실측: 당일 12편 0/12, 같은 측정에서
        # 하루 지난 글 5편 중 4편이 10위 안 — 코픽스·10월배당·근로장려금 1위, 파이어나이 3위).
        # 색인율은 이미 mature 로 고쳐 놓고(9/24) 순위만 당일 글에 남아 있었다.
        rc = [x for x in (last.get('recheck') or []) if x.get('indexed') is not None]
        if rc:
            M.append(('검색', '제목검색 10위 안 비율(하루 지난 글)',
                      round(sum(1 for x in rc if (x.get('self_rank') or 99) <= 10) / len(rc), 3), 0.6, 2,
                      f'{len(rc)}편 기준 · 제목 규칙(series-plan)·toprank 항목 채우기'))
        if b:
            M += [('검색', '색인율(당일 글 — 참고용)', round(sum(1 for x in b if x.get('indexed')) / len(b), 3), 0.3, 1, '색인은 하루쯤 걸린다. 이 값이 낮은 것만으로 발행량을 줄이지 않는다')]
            if not rc:
                M.append(('검색', '제목검색 10위 안 비율(당일 글 — 하루 지난 글이 없어 대신 씀)',
                          round(sum(1 for x in b if (x.get('self_rank') or 99) <= 10) / len(b), 3), 0.6, 1,
                          '색인 전이라 낮게 나온다 — 다음 날 다시 잰다'))
    vis = load(os.path.join(HERE, 'visitors_log.json'), {})
    if vis:
        days = sorted(vis); today_v = vis[days[-1]]['today']
        # 2026-09-26: '오늘 방문'을 새벽에 재면 언제나 목표에 한참 못 미친다 — 하루가 막 시작해서다
        # (실측: 9/25 하루치 53(23:56 측정), 9/26 4(02:20 측정)). 그래서 매일 밤 이 항목이 일감표
        # 1순위로 올라왔고 회차는 '색인·순위를 올려라'라는, 한 회차에 닫을 수 없는 일을 또 받았다.
        # 색인율·순위에서 이미 같은 것을 고쳤다(당일 글 → 하루 지난 글). 방문도 똑같이 완결된 하루로 잰다.
        # report.py 도 같은 이유로 '잰 시각이 다르면 오늘 방문끼리 견주지 않는다'고 해 뒀다.
        td = time.strftime('%Y-%m-%d')
        done = [d for d in days if d < td]
        if done:
            dv = vis[done[-1]]
            M.append(('성장', '블로그 하루 방문(마지막 완결일)', dv['today'], 100, 3,
                      f"{done[-1]} {dv.get('at','')} 측정 · 색인·순위가 먼저. 발행량만 늘리면 안 오른다"))
            M.append(('성장', '블로그 오늘 방문(하루가 덜 지났다 — 참고용)', today_v, 100, 0,
                      f"{days[-1]} {vis[days[-1]].get('at','')} 측정 · 하루가 끝나야 견줄 수 있다"))
        else:
            M.append(('성장', '블로그 오늘 방문', today_v, 100, 3, '색인·순위가 먼저. 발행량만 늘리면 안 오른다'))
    ncafe, medread, medfresh, n_aged = cafe_today()
    if medread is not None:
        M.append(('성장', f'카페 조회 중앙값({CAFE_MIN_AGE_H}시간 지난 글)', medread, 50, 2,
                  f'{n_aged}편 기준 · 카페 축(커버드콜·배당·파이어 금액)·제목·회원 상호작용'))
    if medfresh is not None:
        M.append(('성장', f'카페 조회 중앙값({CAFE_MIN_AGE_H}시간 안 된 글 — 참고용)', medfresh, 50, 0,
                  '갓 올린 글은 조회가 0에서 시작한다 — 이 값이 낮은 것만으로 규칙을 바꾸지 않는다'))

    yt = sh(os.path.join(HERE, 'ytupload.py'), 'stats')
    vids = [int(v) for v in re.findall(r'\d{4}-\d{2}-\d{2}\s+(\d+)\s*회', yt)]
    # 2026-09-24: '최근 10편 조회 합계'는 새 영상을 올릴 때마다 떨어진다(새 영상은 조회 0이라
    # 조회가 쌓인 옛 영상을 10편 밖으로 밀어낸다). 실측 2089 -> 120 -> 6. 발행을 잘할수록 계기판이
    # 나빠지는 셈이라 채널 총조회(누적, 절대 안 줄어든다)로 바꿨다. loop.py 의 회차 판정도 같이 고쳤다.
    m_tot = re.search(r'총조회\s*(\d+)', yt)
    if m_tot: M.append(('영상', '채널 총조회(누적)', int(m_tot.group(1)), 50000, 2, '제목 규칙·썸네일 손잡이(design.json)·루프'))
    pub = len(re.findall(r'\|\s*public\s*\|', yt))
    M.append(('영상', '공개한 영상 수(최근 10편 중)', pub, 10, 2, '지금은 전부 private — 비공개면 조회가 영영 0이라 조정 효과를 잴 수 없다'))
    M.append(('영상', '올린 숏폼 수', len(glob.glob(os.path.join(R, 'shorts', '*.mp4'))), 10, 2, 'firemap-loop 6)에서 회차마다 한 편'))

    # 2026-09-24: 이 숫자가 2에서 멈춰 있었는데 그 2는 short.white·short.contrast 였다.
    # 둘 다 "더 밀면 글자가 죽는다"고 화면으로 확인해 한계를 박아 둔 자리다(loop.py CAPPED).
    # 풀지 않기로 한 것을 '미해결'로 세니 회차마다 끝난 판단을 다시 뒤지게 됐다. 갈라 센다.
    llog = load(os.path.join(HERE, 'loop_log.json'), [])
    last = llog[-1] if llog else {}
    gaps = last.get('gaps', [])
    capped = set(last.get('capped') or [])
    open_gaps = [g for g in gaps if f"{g.get('kind')}.{g.get('key')}" not in capped]
    M.append(('디자인', '경쟁 대비 미해결 차이 수', len(open_gaps), 0, 2,
              'loop.py RULE에 손잡이 추가 또는 thumbstat 측정 수정'))
    if capped:
        # 점수 0 — 줄일 것이 아니라 "이렇게 두기로 했다"를 보이게만 한다
        M.append(('디자인', '한계 확정(사람 눈으로 정함)', len(capped), len(capped), 0,
                  '다시 밀지 않는다 · 지금: ' + ', '.join(sorted(capped))))

    # 회차 자체가 멈췄나. 2026-09-24: 감시기 회차 하나가 새벽 3:52에 시작해 16시간 23분 동안
    # 안 끝났고, 예약은 앞 회차가 끝나야 다음을 돌리므로 그동안 감시기가 한 번도 안 돌았다.
    # 원고 재고를 채우는 유일한 장치가 멈춘 것인데 아무도 몰랐다. 사장님이 물어서야 찾았다.
    try:
        sys.path.insert(0, HERE)
        import beat
        st = beat.stuck()
        M.append(('회차', '예산 시간을 넘겨 멈춘 회차', len(st), 0, 3,
                  '예약 목록에서 running인 세션을 끊고(stop_session) 그 회차를 다시 돌린다'
                  + (' · 지금: ' + ', '.join(f'{t} {m}분' for t, m, _ in st[:3]) if st else '')))
        # 2026-09-25: 전에는 전부 6시간 하나로 쟀다. report는 하루 한 번, improve는 밤에 14시간
        # 쉬는 회차라 아무리 잘 돌아도 늘 잡혔고, 그래서 이 점수가 회차를 거듭해도 안 내려갔다.
        # 이제 회차마다 제 예약 간격(beat.GAP_OK)으로 잰다 — 줄일 수 있는 것만 센다.
        sl = beat.stale()
        M.append(('회차', '제 예약 간격을 넘도록 안 돈 회차', len(sl), 0, 2,
                  '그 회차 지시문에 beat.py start/end 가 있는지 · 예약이 꺼졌는지 확인'
                  + (' · 지금: ' + ', '.join(
                      f'{t}({"기록 없음" if hh is None else str(hh) + "시간째"}/정상 {g}시간)'
                      for t, hh, g in sl[:4]) if sl else '')))
        # 기계가 자서 예약이 통째로 빠진 구간. 사람이 고칠 것이 아니라 보이게만 한다.
        cut = [(t, beat.cut_off(t)) for t in beat.BUDGET]
        cut = [(t, hh) for t, hh in cut if hh]
        if cut:
            M.append(('회차', '기계가 꺼져 예약이 빠진 구간', len(cut), len(cut), 0,
                      '멈춘 회차가 아니다 · ' + ', '.join(f'{t} {hh}시간' for t, hh in cut)))
    except Exception as e: print('회차 맥박 점검 실패:', repr(e)[:90])

    # 만들어 놓고 아무 회차도 안 부르는 도구가 있나.
    # 2026-09-24 하루에만 이 패턴이 네 번 나왔다 — 오피스텔 단지표·건축물대장·유튜버 시리즈 조사,
    # 그리고 발굴 종목(결과를 파일로 안 남겨 분석이 못 썼다). 전부 사장님이 지적해서 알았다.
    # 지시문 어디에도 이름이 안 나오는 도구는 영영 안 돈다. 그걸 기계가 센다.
    try:
        skills = ''
        for sk in glob.glob(os.path.expanduser('~/.claude/scheduled-tasks/*/SKILL.md')):
            try: skills += open(sk, encoding='utf-8').read()
            except Exception: pass
        mine = [os.path.basename(f) for f in glob.glob(os.path.join(HERE, '*.py'))]
        # 다른 도구가 import해서 쓰는 것은 직접 불리지 않아도 된다
        srcs = ''.join(open(f, encoding='utf-8', errors='ignore').read() for f in glob.glob(os.path.join(HERE, '*.py')))
        orphan = [m for m in mine
                  if m not in skills and m[:-3] not in skills
                  and f'import {m[:-3]}' not in srcs and f'{m[:-3]}.py' not in srcs]
        M.append(('도구', '어느 회차도 안 부르는 도구', len(orphan), 0, 3,
                  '지시문에 넣어 회차가 돌게 하거나, 쓸모없으면 지운다'
                  + (' · 지금: ' + ', '.join(sorted(orphan)[:4]) if orphan else '')))
    except Exception as e: print('도구 점검 실패:', repr(e)[:90])

    # 부동산을 서울 밖에서도 보고 있나. 2026-09-24까지 실거래 602개 파일이 전부 서울(11)이었다.
    try:
        codes = {os.path.basename(f).split('_')[0] for f in glob.glob(os.path.join(R, 'rt', '*.json'))}
        codes = {c for c in codes if c.isdigit() and len(c) == 5}
        outside = len({c for c in codes if not c.startswith('11')})
        M.append(('자료', '서울 밖 시군구 실거래', outside, 10, 2,
                  'py -3.12 work/lawdscan.py 41 <월> 로 코드를 확인하고 rtmolit로 받는다'))
    except Exception: pass

    # 글 루프가 규칙을 만들기만 하고 채점을 못 하고 있나.
    # 2026-09-24: 30회 연속 "규칙 뒤 0편"으로 보류였는데 아무도 못 봤다. 계기판에 없었기 때문이다.
    tl = load(os.path.join(HERE, 'textloop_log.json'), []) or []
    streak = 0
    for r in reversed(tl):
        if '보류' in (r.get('verdict') or ''): streak += 1
        else: break
    # 적을수록 좋은 항목이다. 계기판의 gap 식은 '목표보다 모자란 것'만 재므로
    # 목표 6에 값 48이면 점수가 0으로 찍혔다(2026-09-24 확인). 목표 0에 초과분만 넣는다.
    M.append(('품질', '글 규칙 자기채점 보류가 이어진 회차(6회 초과분)', max(0, streak - 6), 0, 3,
              'textloop 판정이 왜 보류인지 verdict 문구를 읽는다 — 표본이 안 쌓인 것인지, 기준 잡는 식이 틀린 것인지'))

    # 같은 글이 두 번 올라간 적이 있나. 0이 아니면 발행기가 중복을 냈다는 뜻이다.
    # 2026-09-24 국채금리 글이 07:13·07:35 두 번 올라갔고 사장님이 화면으로 잡아 줬다. 이제 기계가 잡는다.
    try:
        sys.path.insert(0, HERE)
        from naverpost import dup_titles
        for kind, name in (('blog', '블로그'), ('cafe', '카페')):
            d = dup_titles(kind)
            M.append(('발행', f'{name} 같은 글 두 번 올라간 수', len(d), 0, 3,
                      '올라간 제목과 대조하고 올린다(naverpost already_up) · 겹친 글은 work/blogfix.py private 로 내린다'
                      + (' · 지금: ' + ', '.join(list(d)[:2]) if d else '')))
    except Exception as e: print('중복 검사 실패:', repr(e)[:120])

    tw = open(os.path.join(R, 'tools-wanted.md'), encoding='utf-8').read() if os.path.exists(os.path.join(R, 'tools-wanted.md')) else ''
    M.append(('도구', '사람 손 필요 항목', tw.count('| 대기 |'), 0, 1, '12:30 보고 "확인 필요"에 올린다'))
    bq = open(os.path.join(R, 'build-queue.md'), encoding='utf-8').read() if os.path.exists(os.path.join(R, 'build-queue.md')) else ''
    M.append(('도구', '만들기 대기열 미완', len(re.findall(r'^\d+\.', bq, re.M)) - bq.count('완료'), 0, 2, 'firemap-improve C 회차가 위에서부터 만든다'))

    # 루틴 권한 밖의 항목 — 사장님만 움직일 수 있다(키 발급·계정 가입·영상 공개 전환).
    # 이 둘은 점수가 높아도 회차가 닫을 수 없어, 일감표 1순위를 매번 차지하면서
    # 정작 루틴이 고칠 수 있는 항목(대기 묶음·안 쓰는 도구)을 밀어냈다(2026-09-24 19시 확인:
    # '사람 손 필요 항목' 4.0이 =변화없음으로 며칠째 1순위). 계기판에는 그대로 두되 주인을 표시한다.
    HUMAN = {'사람 손 필요 항목', '공개한 영상 수(최근 10편 중)'}
    rows = []
    for area, name, val, tgt, w, how in M:
        if val is None: continue
        gap = 0.0 if tgt == 0 and val == 0 else (abs(val - tgt) / max(abs(tgt), 1) if val < tgt or tgt == 0 else 0.0)
        if tgt == 0: gap = float(val)
        rows.append({'area': area, 'name': name, 'value': val, 'target': tgt, 'weight': w, 'gap': round(gap, 3), 'score': round(gap * w, 3), 'how': how,
                     'owner': '사람' if name in HUMAN else '루틴'})
    rows.sort(key=lambda r: -r['score'])
    out = {'at': time.strftime('%Y-%m-%d %H:%M'), 'items': rows}
    json.dump(out, open(os.path.join(HERE, 'health.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[계기판 {out['at']}]  영역별 부족분 순위 (점수 = 부족분 × 중요도)")
    for r in rows:
        flag = '■' if r['score'] >= 1 else ('·' if r['score'] > 0 else ' ')
        print(f"{flag} {r['score']:5.2f} [{r['area']}] {r['name']}: {r['value']} / 목표 {r['target']}")
    top = [r for r in rows if r['score'] > 0][:3]
    print('\n이번에 고칠 것:', ' | '.join(f"{t['name']} → {t['how']}" for t in top) if top else '없음(전 항목 목표 달성)')

if __name__ == '__main__': main()
