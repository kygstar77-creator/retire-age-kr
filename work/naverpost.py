# 네이버 블로그·카페 발행기 — 화면 조작(computer-use) 없이 Playwright 전용 브라우저로 올린다.
# 사장님 웨일·크롬과 완전히 별개의 브라우저 프로필(NAVER_PROFILE)을 쓰므로 PC를 같이 써도 안 섞이고,
# 예약 루틴이 무인으로 돌릴 수 있다(화면 권한이 필요 없다).
#
#   python work/naverpost.py login              # 창을 띄운다. 사장님이 네이버에 로그인하면 닫는다(비밀번호는 사람이 친다)
#   python work/naverpost.py check              # 로그인 유지 여부
#   python work/naverpost.py blog  <pkg폴더>     # order.txt 순서대로 블로그 발행, 마지막 줄에 URL 출력
#   python work/naverpost.py cafe  <pkg폴더>     # 카페 발행
#   python work/naverpost.py pending           # 아직 안 올라간 묶음 목록(JSON 한 줄씩, 오래된 순)
#   python work/naverpost.py shot  <url> <파일>  # 디버그: 페이지 스크린샷
#
# pkg/order.txt 형식(글쓰기 회차가 만든다):
#   제목: title.txt
#   b00.txt / img/b1.png ... 한 줄에 하나, 순서대로
#   카테고리: 경제지식      (블로그)
#   태그: a, b, c           (블로그)
#   게시판: 자유게시판       (카페)
import sys, os, re, time, json, io, subprocess
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

PROFILE = os.environ.get('NAVER_PROFILE', r'C:\Users\강영준\Documents\naver_profile')
STATE = os.path.join(PROFILE, 'storage_state.json')   # 로그인 쿠키(세션 쿠키 포함). 프로필만으로는 창을 닫으면 사라진다
BLOG_ID = 'kygstar7777'
CAFE_ID = '31789001'
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '_shots')
os.makedirs(SHOTS, exist_ok=True)

LOCK = os.path.join(PROFILE, '.firemap.lock')   # 같은 프로필을 두 회차가 동시에 열면 크로미움이 죽는다 → 잠금 파일로 순서를 정한다(최대 15분 대기)

def _alive(pid):
    """잠금을 쥔 프로세스가 아직 살아 있나. 죽은 프로세스가 남긴 잠금 때문에 회차가 통째로 날아갔다(2026-09-23 18:32 실제 발생)."""
    try: pid = int(pid)
    except Exception: return False
    if os.name == 'nt':
        import ctypes
        h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
        if not h: return False
        ctypes.windll.kernel32.CloseHandle(h); return True
    try: os.kill(pid, 0); return True
    except OSError: return False

def acquire_lock(wait_sec=900):
    t0 = time.time()
    while True:
        try:
            if os.path.exists(LOCK):
                # 주인이 죽었으면 바로 버린다. 나이만 보면 죽은 잠금을 30분이나 기다리다 회차를 놓친다.
                try: owner = open(LOCK, encoding='utf-8').read().strip()
                except Exception: owner = ''
                if not _alive(owner) or time.time() - os.path.getmtime(LOCK) > 1800:
                    print(f'죽은 잠금 제거 (PID {owner or "?"})'); os.remove(LOCK)
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, str(os.getpid()).encode()); os.close(fd); return True
        except FileExistsError:
            if time.time() - t0 > wait_sec: raise RuntimeError(f'브라우저 프로필 잠금 대기 {wait_sec//60}분 초과')
            time.sleep(10)

def release_lock():
    try: os.remove(LOCK)
    except Exception: pass

def launch(p, headless):
    acquire_lock()
    import atexit; atexit.register(release_lock)
    ctx = p.chromium.launch_persistent_context(
        PROFILE, headless=headless, viewport={'width': 1400, 'height': 1000}, locale='ko-KR',
        args=['--disable-blink-features=AutomationControlled'])
    if os.path.exists(STATE):
        try: ctx.add_cookies(json.load(open(STATE, encoding='utf-8'))['cookies'])
        except Exception as e: print('쿠키 불러오기 실패:', e)
    return ctx

def shot(page, name):
    path = os.path.join(SHOTS, name + '.png'); page.screenshot(path=path, full_page=False); return path

def logged_in(page, deep=True):
    """쿠키도 화면도 못 믿는다. **쓰기 권한이 살아 있는지**를 본다.

    2026-09-24: 쿠키 이름만 보다가 만료를 놓쳤다 → 글쓰기 화면을 열어 보게 고쳤다.
    2026-09-25: 그것도 못 잡았다. 화면은 멀쩡히 열리고 제목·본문·사진까지 다 들어가는데
    **등록을 누르는 순간**에만 "로그인이 필요합니다" 대화상자와 서버 500이 떴다.
    그래서 카페가 10시간 넘게 "글은 다 쓰는데 등록만 안 되는" 상태로 멈춰 있었다.
    이제 카페 글쓰기 권한 API를 직접 두드려 본다 — 로그인이 풀리면 여기서 바로 드러난다."""
    names = {c['name'] for c in page.context.cookies('https://www.naver.com')}
    if not ('NID_AUT' in names and 'NID_SES' in names): return False
    if not deep: return True
    try:
        r = page.request.get(
            f'https://apis.naver.com/cafe-web/cafe-editor-api/v1/cafes/{CAFE_ID}/menus/write-info',
            headers={'Referer': f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/write'})
        if r.status in (401, 403): return False
        if r.status < 400: return True
        # 이 경로가 바뀌었을 수 있다. 그때는 글쓰기 화면으로 되짚는다(예전 방식).
        page.goto(f'https://blog.naver.com/{BLOG_ID}/postwrite', wait_until='domcontentloaded')
        page.wait_for_timeout(4000)
        return 'nidlogin' not in page.url and 'nid.naver.com' not in page.url
    except Exception as e:
        print('로그인 실검사 실패:', repr(e)[:90]); return True   # 못 재면 막지 않는다

def read_pkg(pkg):
    order = open(os.path.join(pkg, 'order.txt'), encoding='utf-8').read().splitlines()
    title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
    seq, meta = [], {}
    for line in order:
        s = line.strip()
        if not s or s.startswith('제목'): continue
        m = re.match(r'^(카테고리|태그|게시판)\s*[:：]\s*(.+)$', s)
        if m: meta[m.group(1)] = m.group(2).split('·')[0].strip(); continue   # '자유게시판 · 전체공개' 같은 꼬리 제거
        if s.startswith('블로그 발행') or s.startswith('카페 발행'): continue
        tok = s.split()[0]
        if re.search(r'\.(png|jpe?g|webp)$', tok, re.I):
            path = tok if os.path.isabs(tok) else os.path.normpath(os.path.join(pkg, '..', tok))
            # 묶음 안(pkg/img/…)에만 사진이 있는 경우도 받아 준다. 예전 묶음은 research/<주제>/img 에 두었다.
            if not os.path.isabs(tok) and not os.path.exists(path):
                alt = os.path.normpath(os.path.join(pkg, tok))
                if os.path.exists(alt): path = alt
            if not os.path.exists(path): raise FileNotFoundError('사진 없음: ' + path)
            seq.append(('img', path))
        elif tok.endswith('.txt'):
            seq.append(('text', open(os.path.join(pkg, tok), encoding='utf-8').read().strip()))
    return title, seq, meta

def ensure_plain(frame):
    # 취소선·굵게 같은 서식 버튼이 켜져 있으면 끈다(첫 실행에서 취소선이 켜진 채 본문이 들어갔다)
    for name in ('strikethrough', 'bold', 'italic', 'underline'):
        try:
            b = frame.locator(f'button[data-name="{name}"]').first
            if b.count() and ('selected' in (b.get_attribute('class') or '') or b.get_attribute('aria-pressed') == 'true'):
                b.click(); frame.page.wait_for_timeout(100)
        except Exception: pass

def click_last_paragraph(frame):
    # 사진을 넣은 뒤에는 포커스가 업로드용 iframe에 남아 locator.click()으로는 글자가 안 들어간다(2026-09-22 실측: 카페 글 9편이 본문 없이 발행).
    # 마지막 '글 문단'(사진 설명 문단 제외)의 화면 좌표를 실제 마우스로 클릭해야 입력이 들어간다.
    page = frame.page
    para = frame.locator('.se-component.se-text .se-text-paragraph').last
    if not para.count(): para = frame.locator('.se-text-paragraph').last
    try: para.evaluate("e => e.scrollIntoView({block: 'center'})"); page.wait_for_timeout(200)
    except Exception: pass
    bb = para.bounding_box()
    if bb: page.mouse.click(bb['x'] + min(20, bb['width'] / 2), bb['y'] + bb['height'] / 2)
    else: para.click(force=True)
    page.wait_for_timeout(250)

def body_text_len(frame):
    # 빈 편집기의 안내문 '내용을 입력하세요.'는 글자로 세지 않는다(첫 조각 검증이 -3자로 틀렸던 원인)
    return frame.evaluate("() => [...document.querySelectorAll('.se-component.se-text .se-text-paragraph')].map(e=>e.innerText).filter(t=>t.trim()!=='내용을 입력하세요.').join('').replace(/[\\s\\u200b]+/g,'').length")

def type_text(frame, text):
    page = frame.page
    want = len(re.sub(r'\s+', '', text))
    for attempt in range(2):
        before = body_text_len(frame)
        click_last_paragraph(frame); ensure_plain(frame)
        for para in text.splitlines():
            if para.strip(): page.keyboard.insert_text(para); page.wait_for_timeout(120)
            page.keyboard.press('Enter'); page.wait_for_timeout(120)
        got = body_text_len(frame) - before
        if got >= want * 0.9: return
        print(f'본문 입력 확인 실패({got}/{want}자) — 다시 시도' if attempt == 0 else f'본문 입력 실패({got}/{want}자)')
    raise RuntimeError('본문 글자가 편집기에 안 들어감')

def insert_image(frame, path, photo_button):
    page = frame.page
    click_last_paragraph(frame)
    before = frame.locator('.se-component.se-image').count()
    with page.expect_file_chooser(timeout=15000) as fc:
        photo_button.click()
    fc.value.set_files(path)
    for _ in range(40):                    # 이미지 컴포넌트가 하나 늘 때까지 기다린다(최대 20초)
        page.wait_for_timeout(500)
        if frame.locator('.se-component.se-image').count() > before: break
    page.wait_for_timeout(800)

def close_popups(frame):
    page = frame.page
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    for sel in ['.se-help-panel-close-button', 'button.se-help-panel-close-button', '[class*="help"] button[class*="close"]',
                '.se-popup-button-cancel', 'button:has-text("취소")']:
        try:
            b = frame.locator(sel).first
            if b.count() and b.is_visible(timeout=800): b.click(); page.wait_for_timeout(400)
        except Exception: pass


def norm(t): return re.sub(r'[\s\W_]+', '', t or '')

UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}

def live_pairs(kind, pages=1):
    """올라가 있는 글의 (norm(제목), URL) 목록. 방금 올린 글까지 잡혀야 한다.
    블로그는 RSS를 쓰지 않는다. RSS가 늦게 갱신돼 22분 전에 올린 글이 안 보였고
    그 사이 같은 글이 한 번 더 올라갔다(2026-09-24 07:13·07:35 국채금리 글, 사장님이 화면으로 잡아 줌).
    PostTitleListAsync는 로그인 없이 되고 방금 올린 글도 바로 보인다."""
    import urllib.request, urllib.parse
    out = []
    try:
        for pg in range(1, pages + 1):
            if kind == 'blog':
                u = (f'https://blog.naver.com/PostTitleListAsync.naver?blogId={BLOG_ID}'
                     f'&viewdate=&currentPage={pg}&categoryNo=0&parentCategoryNo=&countPerPage=30')
                # 이 응답은 제대로 된 JSON이 아니다(제목에 \' 같은 escape가 섞여 json.load가 깨진다). 짝만 뽑아 쓴다.
                s = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
                got = re.findall(r'"logNo":"(\d+)","title":"([^"]*)"', s)
                if not got:
                    if pg == 1: raise RuntimeError('글 목록에서 제목을 못 뽑음')
                    break
                out += [(norm(urllib.parse.unquote_plus(t)), f'https://blog.naver.com/{BLOG_ID}/{no}') for no, t in got]
            else:
                u = (f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}'
                     f'&search.queryType=lastArticle&search.page={pg}&search.perPage=50')
                arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
                if not arts: break
                out += [(norm(a.get('subject', '')), f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/{a.get("articleId")}') for a in arts]
    except Exception as e:
        print(('블로그 글목록' if kind == 'blog' else '카페 API') + ' 실패:', repr(e)[:150])
    return out

def live_map(kind): return dict(live_pairs(kind))

def dup_titles(kind, pages=4):
    """같은 제목으로 두 번 올라간 글. 0이어야 한다. 값이 있으면 발행기가 또 중복을 냈다는 뜻."""
    seen = {}
    for t, u in live_pairs(kind, pages):
        seen.setdefault(t, set()).add(u)
    return {t: sorted(us) for t, us in seen.items() if len(us) > 1}

# 제목이 달라도 같은 대상을 또 쓰는 것을 잡는다.
# 2026-09-24: 03:46 "상계주공9단지 2,830세대 매매 5억 4,000부터…"와
# 13:21 "상계주공9단지 8월 실거래 12건…"이 같은 날 나갔다. 제목 완전일치 검사로는 안 잡힌다.
# 사장님 "상계주공만 왜 글을 쓰는 거야?"
_STOP = set('서울 아파트 오피스텔 전세 월세 배당 실거래 매매 단지 수익률 기준 이유 경우 확인 계산 비교 정리'.split())

# 약어는 대상이 아니다. 이걸 안 빼면 'ISA 연금저축'과 'ISA 배당'이 같은 대상으로 잡힌다.
_NOTICKER = {'ETF', 'API', 'GDP', 'CPI', 'PPI', 'FOMC', 'EPS', 'PER', 'PBR', 'ROE', 'ISA', 'IRP',
             'DSR', 'LTV', 'DTI', 'REIT', 'IPO', 'ETN', 'TDF', 'MMF', 'CMA', 'FED', 'EU', 'US'}

def subject_keys(title):
    """제목에서 '같은 대상'으로 볼 만한 말만 뽑는다 — 아파트 단지명과 종목 티커.
    동네·구 이름은 넣지 않는다. 히트맵 시리즈가 매일 구 이름을 달고 나가는데 그걸 막으면 안 된다.
    잘못 막는 쪽보다 못 막는 쪽이 낫다 — 잘못 막으면 발행이 멈춘다."""
    ks = set()
    for w in re.findall(r'[가-힣A-Za-z][가-힣A-Za-z0-9]+', title or ''):
        if re.search(r'주공|자이|래미안|푸르지오|아이파크|힐스테이트|편한세상|캐슬|더샵|센트레빌|리버뷰|단지', w):
            ks.add(w)                                            # 아파트 단지
        elif re.fullmatch(r'[A-Z]{2,5}', w) and w not in _NOTICKER:
            ks.add(w)                                            # 종목·ETF 티커
    return ks

def head_key(title, n=8):
    """제목 앞머리(숫자·공백 뺀 앞 n글자). 숫자만 바꾼 같은 글을 잡는다.
    2026-09-24: '재산세 계산기는 9만 9천원인데 고지서는 29만 9천원'과
    '재산세 계산기는 26만원인데 고지서는 62만원'이 한 시간 간격으로 나갔다.
    단지명도 티커도 안 겹쳐서 subject_keys로는 안 잡혔다. 앞머리는 '재산세계산기는'으로 같다."""
    s = re.sub(r'[\s\d,%·\-~]+', '', title or '')
    return s[:n]

def same_subject_today(kind, title):
    """최근 글 중 같은 대상·같은 주제를 다룬 것. 있으면 [(제목, URL, 겹친 것)]."""
    mine = subject_keys(title)
    hk = head_key(title)
    hits = []
    for raw, url in _raw_recent(kind):
        if norm(raw) == norm(title): continue      # 같은 글(재발행)은 already_up이 따로 잡는다
        both = mine & subject_keys(raw)
        if both: hits.append((raw, url, sorted(both)))
        elif len(hk) >= 6 and head_key(raw) == hk: hits.append((raw, url, [f'제목 앞머리 "{hk}"']))
    return hits

def _raw_recent(kind, n=24):
    """원제목 그대로의 최근 글 (제목, URL)."""
    import urllib.request, urllib.parse
    out = []
    try:
        if kind == 'blog':
            u = (f'https://blog.naver.com/PostTitleListAsync.naver?blogId={BLOG_ID}'
                 f'&viewdate=&currentPage=1&categoryNo=0&parentCategoryNo=&countPerPage=30')
            s = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf-8', 'ignore')
            out = [(urllib.parse.unquote_plus(t), f'https://blog.naver.com/{BLOG_ID}/{no}')
                   for no, t in re.findall(r'"logNo":"(\d+)","title":"([^"]*)"', s)]
        else:
            u = (f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}'
                 f'&search.queryType=lastArticle&search.page=1&search.perPage={n}')
            out = [(a.get('subject', ''), f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/{a.get("articleId")}')
                   for a in json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']]
    except Exception as e: print('최근 글 읽기 실패:', repr(e)[:120])
    return out

def cafe_boards():
    """카페에 실제로 있는 게시판 이름. 없는 게시판을 고르려다 회차가 날아가는 것을 막는다.
    2026-09-25 확인: 파이어맵 카페에는 '자유게시판' 하나뿐인데 묶음들이 '미국주식·배당' 같은
    이름을 달고 있었다. 글감 편성이 카페 구조보다 앞서 나간 것이다."""
    import urllib.request
    try:
        u = f'https://apis.naver.com/cafe-web/cafe2/SideMenuList?cafeId={CAFE_ID}'
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))
        ms = d.get('message', {}).get('result', {}).get('menus') or []
        return [m.get('menuName') for m in ms if m.get('menuType') == 'B' and m.get('menuName')]
    except Exception as e:
        print('게시판 목록 조회 실패:', repr(e)[:90]); return []

AUTHFAIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '_naver_auth_fail.txt')

def note_auth_fail(msg):
    """글쓰기 API가 인증으로 막힌 것을 남긴다. 다음 회차가 글을 다 쓴 뒤에야 알아채면 한 시간이 날아간다."""
    try:
        io.open(AUTHFAIL, 'w', encoding='utf-8').write(time.strftime('%Y-%m-%d %H:%M') + ' ' + msg[:300])
    except Exception: pass

def auth_fail_seen():
    """최근 6시간 안에 인증 실패가 있었으면 그 줄. 로그인에 성공하면 지운다."""
    try:
        if not os.path.exists(AUTHFAIL): return None
        if time.time() - os.path.getmtime(AUTHFAIL) > 6 * 3600: return None
        return io.open(AUTHFAIL, encoding='utf-8').read().strip()
    except Exception: return None

def alert_login(reason):
    """로그인이 막혔다는 걸 사장님 휴대폰으로 알린다(텔레그램).
    회차는 스스로 멈춘 걸 알릴 수 없고, 계기판은 사장님이 봐야 보인다.
    2026-09-25: 로그인이 13시간 막혀 블로그·카페 0편이었는데 아무도 몰랐다.
    같은 내용을 매시 보내면 알림이 무뎌지므로 6시간에 한 번만 보낸다."""
    stamp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '.login_alert')
    try:
        if os.path.exists(stamp) and time.time() - os.path.getmtime(stamp) < 6 * 3600: return
    except Exception: pass
    msg = ('[파이어맵] 네이버 로그인이 막혔습니다 - ' + str(reason)[:200] +
           '  /  PC에서 `py -3.12 work/naverpost.py login` 한 번만 해주시면 대기 원고가 바로 나갑니다.')
    try:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tgreport.py'),
                        'send', msg], timeout=60, capture_output=True)
        io.open(stamp, 'w', encoding='utf-8').write(time.strftime('%Y-%m-%d %H:%M'))
    except Exception as e:
        print('알림 실패:', e)

def already_up(kind, title):
    """이 제목이 이미 올라가 있으면 그 URL. 발행 직전과 실패 직후에 둘 다 본다."""
    return live_map(kind).get(norm(title))

def published_titles():
    return set(live_map('blog')), set(live_map('cafe'))

def list_pending():
    """work/research/*/pkg 중 아직 안 올라간 묶음. order.txt 첫 줄로 블로그/카페를 가른다."""
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research')
    blog_t, cafe_t = published_titles()
    out = []
    for d in sorted(os.listdir(base)):
        pkg = os.path.join(base, d, 'pkg')
        if not os.path.exists(os.path.join(pkg, 'order.txt')) or not os.path.exists(os.path.join(pkg, 'title.txt')): continue
        if os.path.exists(os.path.join(pkg, 'published.txt')): continue
        first = open(os.path.join(pkg, 'order.txt'), encoding='utf-8').readline()
        kind = 'cafe' if '카페' in first else 'blog'
        title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
        if norm(title) in (cafe_t if kind == 'cafe' else blog_t):
            open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write('already published (title matched)\n'); continue
        out.append({'kind': kind, 'pkg': pkg, 'title': title, 'mtime': os.path.getmtime(os.path.join(pkg, 'order.txt'))})
    out.sort(key=lambda x: x['mtime'])
    return out

# ---------- 블로그 ----------
def verify_body(frame, seq, label):
    """등록 직전 검증: 묶음의 글자 수·사진 수가 편집기에 실제로 들어갔는지. 모자라면 등록하지 않는다."""
    total = body_text_len(frame); want = sum(len(re.sub(r'\s+', '', v)) for k, v in seq if k == 'text')
    imgs = frame.locator('.se-component.se-image').count(); want_img = sum(1 for k, _ in seq if k == 'img')
    print(f'{label} 본문 {total}/{want}자, 사진 {imgs}/{want_img}장')
    if total < want * 0.9 or imgs < want_img: raise RuntimeError(f'{label} 본문이 덜 들어감 — 등록하지 않음')

def find_blog_url_by_title(title, tries=6, gap=15):
    """RSS에서 이 제목의 글을 찾아 주소를 준다. 발행 클릭 뒤 화면이 안 넘어갈 때 실제 등록 여부 확인용."""
    import urllib.request
    UA = {'User-Agent': 'Mozilla/5.0'}
    key = re.sub(r'\s+', '', title)[:14]
    for _ in range(tries):
        try:
            x = urllib.request.urlopen(urllib.request.Request(
                f'https://rss.blog.naver.com/{BLOG_ID}.xml', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
            for it in re.findall(r'<item>(.*?)</item>', x, re.S):
                t = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', it, re.S)
                l = re.search(r'<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', it, re.S)
                if t and l and key and key in re.sub(r'\s+', '', t.group(1)):
                    n = re.search(BLOG_ID + r'/(\d+)', l.group(1))
                    return f'https://blog.naver.com/{BLOG_ID}/{n.group(1)}' if n else l.group(1).split('?')[0]
        except Exception as e:
            print('RSS 확인 실패:', e)
        time.sleep(gap)
    return None


CAFE_NICK = '파이어맵'   # 카페에 글을 쓰는 우리 계정의 별명. 가드가 남의 글을 우리 발행으로 세지 않게 쓴다

MIN_GAP_MIN = 20   # 같은 매체에 이 시간 안에 또 올리지 않는다(한 회차 1편 규칙을 코드로 강제). 45분이었으나 늦게 끝난 회차가 다음 회차까지 막아 0편이 나와(2026-09-23 16시) 20분으로

def last_published_minutes(kind):
    """가장 최근 발행이 몇 분 전인지. 블로그는 RSS pubDate, 카페는 API writeDateTimestamp. 못 재면 None."""
    import urllib.request, email.utils
    UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
    try:
        if kind == 'blog':
            s = urllib.request.urlopen(urllib.request.Request(f'https://rss.blog.naver.com/{BLOG_ID}.xml', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
            # 채널 <pubDate>는 피드를 만든 시각(=지금)이라 <item> 뒤쪽만 본다. 안 그러면 항상 '0분 전'이 되어 블로그 발행이 영구히 막힌다(2026-09-23 확인)
            items = s.split('<item>', 1)
            if len(items) < 2: return None
            ts = max(email.utils.parsedate_to_datetime(d).timestamp() for d in re.findall(r'<pubDate>(.*?)</pubDate>', items[1]))
        else:
            # lastArticle은 카페 '전체' 최신 글이라 회원 글까지 섞인다. 우리 글만 골라야 한다.
            # 2026-09-25 11:37: 회원 글이 아니라 우리 글이 10분 전이어서 막힌 것은 맞았지만,
            # 카페에 회원이 늘면 남이 쓴 글 때문에 우리 발행이 막혀 0편이 난다. 글쓴이로 걸러 둔다.
            u = f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}&search.queryType=lastArticle&search.page=1&search.perPage=30'
            arts = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']
            ours = [a for a in arts if a.get('writerNickname') == CAFE_NICK]
            if not ours: return None          # 최근 30편에 우리 글이 없다 = 최근에 안 올렸다
            ts = max(a['writeDateTimestamp'] for a in ours) / 1000
        return (time.time() - ts) / 60
    except Exception as e:
        print('최근 발행 시각 확인 실패:', e); return None

# 회차 루틴이 --wait를 주면 거부하는 대신 남은 시간만큼 기다렸다 올린다.
# 왜 필요한가(2026-09-24 07시): 앞 회차가 07:13에 블로그를 올려서 07:14 발행이 거부됐고,
# 20분 뒤로 잡아 07:33에 다시 걸었더니 '20분 전'으로 또 경계에 걸렸다. 회차마다 사람이
# 시각을 계산해 재시도를 거는 방식은 이렇게 한 번씩 빗나간다. 기다리는 쪽이 0편을 막는다.
WAIT_MAX_MIN = 25   # 이보다 더 기다려야 하면 회차를 넘긴다

def jitter(kind):
    """발행 시각을 흩뜨린다. 매시 정각에 올리면 사람이 쓴 글로 안 보인다.

    네이버 공식(2016-07-12 '블로그 검색 저품질 관련 잘못된 소문 Top'):
      "정확하게 일정한 시간 간격을 두고 글을 쓰면 오히려 어뷰징으로 오판될 수 있습니다."
    같은 글에서 붙여넣기 자체는 괜찮다고 하면서도 조건을 달았다 —
      "글 작성 시각 간격과 글 길이를 고려해 평균적인 타자 속도를 계산합니다."
      "그 포스팅이 스팸 문서로 분류될 만큼 다량의 반복적 포스팅이 아니라면 문제가 되지 않습니다."
    우리는 매시 정각 · 붙여넣기 · 하루 24편으로 세 조건이 전부 겹쳤다(2026-09-24).
    그래서 회차마다 0~17분을 무작위로 쉰다. 정각에 몰리지 않게 하는 것이 목적이다."""
    if os.environ.get('NAVER_FORCE') == '1': return
    import random
    s = random.randint(0, 17 * 60)
    print(f'{kind} 발행 전 {s//60}분 {s%60}초 쉰다(정각 몰림 방지)', flush=True)
    time.sleep(s)

def rate_guard(kind, wait=False):
    if os.environ.get('NAVER_FORCE') == '1': return
    m = last_published_minutes(kind)
    if m is None or m >= MIN_GAP_MIN: return
    left = MIN_GAP_MIN - m
    if wait and left <= WAIT_MAX_MIN:
        print(f'{kind} 직전 발행이 {m:.0f}분 전 — {left:.1f}분 기다렸다 올린다', flush=True)
        time.sleep(left * 60 + 30)          # 경계에서 또 걸리지 않게 30초 더
        return
    raise RuntimeError(f'{kind} 직전 발행이 {m:.0f}분 전 — {MIN_GAP_MIN}분 안에는 같은 매체에 다시 올리지 않는다(한 회차 1편). 다음 회차에 올린다')

def post_blog(page, pkg, wait=False):
    jitter('blog'); rate_guard('blog', wait)
    title, seq, meta = read_pkg(pkg)
    page.goto(f'https://blog.naver.com/{BLOG_ID}/postwrite', wait_until='domcontentloaded')
    page.wait_for_timeout(6000)
    frame = page.main_frame
    for f in page.frames:
        if f != page.main_frame and 'postwrite' in f.url.lower(): frame = f
    close_popups(frame)
    t = frame.locator('.se-documentTitle .se-text-paragraph, .se-title-text').first
    t.click(); page.keyboard.insert_text(title); page.wait_for_timeout(300)
    photo = frame.locator('button[data-name="image"]').first
    for kind, val in seq:
        if kind == 'text': type_text(frame, val)
        else: insert_image(frame, val, photo)
    verify_body(frame, seq, '블로그')
    page.screenshot(path=os.path.join(SHOTS, 'blog_body.png'), full_page=True)
    # 발행 패널: 오른쪽 위 발행 버튼은 class가 publish_btn__..., 예약 버튼은 reserve_btn__... 라 구분한다
    frame.locator('button[class^="publish_btn"]').first.click(); page.wait_for_timeout(2500)
    shot(page, 'blog_publish_panel')
    # 패널 항목은 클래스명이 난수라 화면 문구로 잡는다(2026-09-22 패널 스크린샷 기준)
    want = meta.get('카테고리')
    if want:
        try:
            lbl = frame.get_by_text('카테고리', exact=True).first; box = lbl.bounding_box()
            if not frame.get_by_text(want, exact=True).first.is_visible(timeout=800):
                page.mouse.click(box['x'] + box['width'] + 200, box['y'] + box['height'] / 2); page.wait_for_timeout(700)
                frame.get_by_text(want, exact=True).last.click(); page.wait_for_timeout(500)
        except Exception as e: print('카테고리 선택 실패:', repr(e)[:120])
    try:
        frame.get_by_text('전체공개', exact=True).first.click(); page.wait_for_timeout(300)
    except Exception as e: print('전체공개 선택 실패:', repr(e)[:120])
    tags = [x.strip() for x in meta.get('태그', '').split(',') if x.strip()][:30]
    if tags:
        try:
            tagbox = frame.get_by_placeholder(re.compile('태그 입력')).first
            for tag in tags:
                tagbox.click(); page.keyboard.insert_text(tag); page.keyboard.press('Enter'); page.wait_for_timeout(250)
        except Exception as e: print('태그 입력 실패:', repr(e)[:120])
    shot(page, 'blog_publish_panel2')
    page.on('dialog', lambda d: d.accept())   # 카페와 같은 이유 — 네이티브 확인 창을 안 받으면 자동 취소된다
    # 2026-09-25: 9/24 21:09~9/25 11:30 사이 13시간 동안 블로그가 한 편도 안 나갔는데, 회차 기록에는
    # '발행 클릭 뒤 화면 이동 30초 초과'로만 남았다. 진짜 이유(네이버 글쓰기 API가 IP 확인으로 막음)는
    # 카페 쪽에서 먼저 드러났다 — 카페에만 응답 감시가 걸려 있었기 때문이다. 블로그에도 똑같이 건다.
    # 블로그가 먼저 막히면 note_auth_fail이 안 찍혀 check가 '로그인됨'이라 답하고 알림도 안 갔다.
    apierr = []
    def _watch_blog(resp):
        try:
            if resp.request.method in ('POST', 'PUT') and resp.status >= 400:
                body = resp.text()[:400]
                print('[발행 API]', resp.status, resp.url[:110])
                print('[발행 API 답]', body)
                apierr.append(body)
        except Exception: pass
    page.on('response', _watch_blog)
    frame.get_by_role('button', name=re.compile(r'^\s*발행\s*$')).last.click()
    # 발행 뒤 PostView.naver?...&logNo=NNN 또는 /kygstar7777/NNN 으로 이동한다
    try:
        page.wait_for_url(re.compile(r'logNo=\d+|blog\.naver\.com/' + BLOG_ID + r'/\d+'), timeout=30000)
    except Exception as e:
        # 2026-09-24 18시: 본문 2,172자·사진 6장이 다 들어간 뒤 네이버가 '페이지를 찾을 수 없습니다'를
        # 띄워 이동이 안 됐다. 화면만 보고 실패로 접으면 올라간 글을 두 번 올리거나 회차가 0편이 된다.
        # 실제로 올라갔는지는 RSS가 말해 준다.
        print('발행 후 이동 실패 — RSS로 실제 등록 여부를 확인한다:', repr(e)[:100])
        shot(page, 'blog_after_publish')
        url = find_blog_url_by_title(title)
        if url:
            print('RSS에 등록 확인:', url)
            return url
        for _ in range(10):
            if apierr: break
            page.wait_for_timeout(500)
        auth = [b for b in apierr if '인증 실패' in b or 'IP check' in b or '10004' in b or 'loginStat' in b]
        if auth:
            note_auth_fail(auth[0]); alert_login(auth[0])
            raise RuntimeError('네이버 로그인 IP 불일치 — 사람이 `py -3.12 work/naverpost.py login` 을 다시 해야 한다. '
                               '서버 답: ' + auth[0][:200])
        raise
    m = re.search(r'logNo=(\d+)', page.url) or re.search(BLOG_ID + r'/(\d+)', page.url)
    return f'https://blog.naver.com/{BLOG_ID}/{m.group(1)}' if m else page.url

# ---------- 카페 ----------
def post_cafe(page, pkg, wait=False):
    jitter('cafe'); rate_guard('cafe', wait)
    title, seq, meta = read_pkg(pkg)
    page.goto(f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/write', wait_until='domcontentloaded')
    page.wait_for_timeout(6000)
    frame = page.main_frame
    close_popups(frame)   # 임시등록 복구 팝업 등
    # 게시판 고르기. 묶음이 없는 게시판을 요구하면 드롭다운이 열린 채 멈춰 회차가 통째로 날아간다
    # (2026-09-25: 묶음이 '미국주식·배당'을 달라는데 카페에는 '자유게시판'뿐이라 9.4시간 빵꾸).
    # 실제로 있는 게시판을 API로 먼저 받아 두고, 없으면 첫째 게시판으로 넘어간다.
    # 글이 엉뚱한 판에 가는 것이 안 올라가는 것보다 낫다.
    want = meta.get('게시판', '자유게시판')
    boards = cafe_boards()
    pick = want if want in boards else (boards[0] if boards else want)
    if pick != want:
        print(f'게시판 "{want}" 없음 → "{pick}" 로 올린다 (있는 것: {boards})')
    # 고른 뒤 실제로 닫혔는지 본다. 2026-09-25 06:02 실측: 목록은 열렸는데 항목 클릭이 안 먹어
    # 버튼이 "게시판을 선택해 주세요." 그대로였고, 그 상태로 본문을 2분 동안 다 채운 뒤
    # 등록이 눌리지 않아 30초 이동 실패로만 보였다. 여기서 못 고르면 본문 넣기 전에 멈춘다.
    for i in range(3):
        page.locator('button:has-text("게시판을 선택해 주세요"), .FormSelectButton').first.click(); page.wait_for_timeout(900)
        try: page.get_by_text(pick, exact=True).last.click(timeout=5000)
        except Exception as e: print(f'게시판 항목 클릭 실패({i+1}/3):', repr(e)[:80])
        page.wait_for_timeout(700)
        if not page.locator('button:has-text("게시판을 선택해 주세요")').count(): break
        print(f'게시판이 안 골라졌다 — 다시 연다 ({i+1}/3)')
    else:
        shot(page, 'cafe_board_stuck')
        raise RuntimeError(f'게시판 "{pick}" 을 세 번 눌러도 안 골라졌다 (있는 것: {boards})')
    page.locator('textarea[placeholder*="제목"], input[placeholder*="제목"]').first.fill(title)
    frame = page.main_frame
    photo = page.locator('button[data-name="image"]').first
    for kind, val in seq:
        if kind == 'text': type_text(frame, val)
        else: insert_image(frame, val, photo)
    verify_body(frame, seq, '카페')
    shot(page, 'cafe_body')
    set_cafe_public(page)
    return submit_cafe(page, title)

def set_cafe_public(page):
    """공개 설정을 전체공개로. 라디오(name=public value=true)는 비활성이 아니다 — 2026-09-22 프로브로 확인.
    화면 조작 때는 클릭 지점이 어긋나 안 바뀐 것뿐이었다."""
    already = "() => { const r=document.querySelector('input[name=public][value=\"true\"]'); return !!(r && r.checked); }"
    if page.evaluate(already): print('전체공개: 이미 선택됨'); return True     # 수정 화면에서 이미 전체공개면 라벨이 클릭 불가한 <p>로 바뀐다
    try:
        page.get_by_text('공개 설정', exact=False).first.click(); page.wait_for_timeout(500)
    except Exception: pass
    lab = page.get_by_text('전체공개', exact=True).first
    try: lab.click(timeout=5000)                    # 일반 클릭(앱 상태까지 바뀐다). 프로브로 확인
    except Exception: lab.click(force=True)
    page.wait_for_timeout(600)
    ok = page.evaluate("() => { const r=document.querySelector('input[name=public][value=\"true\"]'); return !!(r && r.checked); }")
    print('전체공개:', '선택됨' if ok else '선택 실패')
    return ok

def submit_cafe(page, title=None):
    # 2026-09-25: 9시간 넘게 카페·블로그가 "등록 눌렀는데 화면이 안 넘어감"으로 전부 실패했다.
    # 원인은 확인 창이 DOM 요소가 아니라 window.confirm 이었다는 것이다. Playwright는 손잡이를
    # 안 걸어 두면 네이티브 대화상자를 자동으로 '취소'한다 — 그래서 등록이 조용히 없던 일이 되고
    # 화면은 글쓰기 그대로 남아 30초 뒤 이동 실패로만 보였다. 수정 화면(cafe_make_public)에는
    # 이미 손잡이가 있었는데 새 글 등록 쪽에만 빠져 있었다.
    page.on('dialog', lambda d: d.accept())
    # 등록이 왜 안 되는지는 화면이 아니라 서버 답이 말해 준다. 2026-09-25에 확인 창까지 제대로 눌렀는데도
    # 화면이 안 넘어갔다 — 그때 서버가 뭐라고 했는지 아무도 안 봤다. 글쓰기 API 응답을 받아 적는다.
    apierr = []
    def _watch(resp):
        try:
            if 'articles' in resp.url and resp.request.method in ('POST', 'PUT'):
                body = resp.text()[:400]
                print('[등록 API]', resp.status, resp.url[:110])
                print('[등록 API 답]', body)
                if resp.status >= 400: apierr.append(body)
        except Exception: pass
    page.on('response', _watch)
    page.get_by_role('button', name=re.compile(r'^\s*등록\s*$')).first.click()   # '임시등록'이 아니라 '등록'만
    page.wait_for_timeout(1500); shot(page, 'cafe_just_after_submit')   # 눌린 직후 화면(진단용)
    # 전체공개면 "이 글은 전체공개로 설정되어 있어요 ... 계속할까요?" 확인 창이 뜬다(2026-09-22 실측) → 확인
    # 2026-09-25: 예전에는 is_visible(timeout=3000)으로 봤다. Playwright의 is_visible은 즉시 판정이라
    # 창이 뜨기 전에 False가 나오고, 인자를 넘기면 예외가 나 except로 통째로 넘어갔다.
    # 그러면 확인 창이 그대로 남아 등록이 안 되고 30초 뒤 이동 실패로만 보인다. wait_for로 제대로 기다린다.
    # 2026-09-25 06:33 실측(cafe_just_after_submit.png): 확인 창은 window.confirm 이 아니라 화면 안의
    # 상자였다("이 글은 전체공개로 설정되어 있어요 … 계속할까요?" + 취소/확인). 창은 제대로 떴는데
    # 확인 버튼을 .last 로 잡은 것이 화면에 없는 버튼이라 클릭이 시간초과로 죽었고, except: pass 가
    # 그걸 통째로 삼켜 창이 그대로 남았다. 그래서 10시간 동안 '등록 눌렀는데 화면이 안 넘어감'으로만 보였다.
    # 보이는 확인 버튼을 골라 누르고, 실패하면 삼키지 말고 찍어 남긴다.
    try:
        page.get_by_text('계속할까요', exact=False).first.wait_for(state='visible', timeout=8000)
        btns = page.get_by_role('button', name=re.compile(r'^\s*확인\s*$'))
        hit = None
        for i in range(btns.count()):
            if btns.nth(i).is_visible(): hit = btns.nth(i); break
        if hit is None: hit = page.get_by_text('확인', exact=True).last
        hit.click(timeout=5000)
        print('전체공개 확인 창 — 확인을 눌렀다')
        page.wait_for_timeout(2500); shot(page, 'cafe_after_confirm')   # 확인 누른 직후(진단용)
    except Exception as e:
        print('확인 창 처리 실패:', repr(e)[:140]); shot(page, 'cafe_confirm_fail')
    # 등록 뒤 ArticleRead.nhn?...&articleid=NN 또는 .../articles/NN 또는 /firemap/NN 으로 이동한다
    # 2026-09-25 07:05: 10시간 동안 "등록 눌렀는데 화면이 안 넘어감"으로만 적히던 것의 진짜 이유는
    # 서버가 돌려준 이 답이었다 — {"errorCode":"10004","message":"NaverUser 인증 실패 …
    # 'Failure-[401:IP check failure]'"}. 쿠키는 살아 있어 읽기는 되는데 글쓰기 API가 IP를 보고 막는다.
    # 사람이 다시 로그인하는 것 말고는 길이 없다. 30초 시간초과로 뭉뚱그리지 말고 그대로 말한다.
    for _ in range(10):
        if apierr: break
        page.wait_for_timeout(500)
    auth = [b for b in apierr if '인증 실패' in b or 'IP check' in b or '10004' in b]
    if auth:
        shot(page, 'cafe_auth_fail')
        note_auth_fail(auth[0])
        alert_login(auth[0])   # 2026-09-25: 적어 두기만 하면 다음 check 회차까지 아무도 모른다. 막힌 그 자리에서 알린다.
        raise RuntimeError('네이버 로그인 IP 불일치 — 사람이 `py -3.12 work/naverpost.py login` 을 다시 해야 한다. '
                           '서버 답: ' + auth[0][:200])
    try:
        page.wait_for_url(re.compile(r'articleid=\d+|articles/\d+|cafe\.naver\.com/firemap/\d+', re.I), timeout=30000)
    except Exception as e:
        # 블로그에는 RSS로 실제 등록 여부를 되짚는 길이 있는데 카페에는 없었다(2026-09-25 회차에서 막힘).
        # 화면만 보고 실패로 접으면 이미 올라간 글을 다음 회차가 또 올린다. 목록으로 확인한다.
        print('등록 후 이동 실패 — 카페 목록으로 실제 등록 여부를 확인한다:', repr(e)[:100])
        shot(page, 'cafe_after_submit')
        if title:
            for _ in range(6):
                page.wait_for_timeout(5000)
                try:
                    up = already_up('cafe', title)
                except Exception:
                    up = None
                if up:
                    print('카페 목록에서 등록 확인:', up)
                    return up
        raise
    m = re.search(r'articleid=(\d+)', page.url, re.I) or re.search(r'articles/(\d+)', page.url) or re.search(r'firemap/(\d+)', page.url)
    return f'https://cafe.naver.com/firemap/{m.group(1)}' if m else page.url

def cafe_make_public(page, article_id):
    """이미 올라간 카페 글을 수정 화면에서 전체공개로 바꿔 다시 등록한다."""
    page.goto(f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/{article_id}', wait_until='domcontentloaded')
    page.wait_for_timeout(5000)
    # '수정'은 새 탭으로 열릴 수 있다 → 새 페이지가 생기면 그쪽을 쓴다
    ctx = page.context; before = set(ctx.pages)
    page.get_by_role('button', name=re.compile(r'^\s*수정\s*$')).first.click()
    page.wait_for_timeout(6000)
    new = [q for q in ctx.pages if q not in before]
    edit = new[0] if new else page
    edit.wait_for_load_state('domcontentloaded'); edit.wait_for_timeout(3000)
    shot(edit, 'cafe_edit_page')
    close_popups(edit.main_frame)
    # 옛 글은 구 SmartEditor(iframe 안, 버튼 '수정완료')로 열린다 → 프레임을 뒤져 처리
    legacy = None
    for fr in edit.frames:
        try:
            if fr.locator('input#all_open').count() and fr.locator('a#cafewritebtn').count():
                legacy = fr; break
        except Exception: pass
    if legacy is not None:
        edit.once('dialog', lambda d: d.accept())            # window.confirm 이면 확인
        legacy.locator('input#all_open').first.click(); edit.wait_for_timeout(300)
        ok = legacy.locator('input#all_open').first.is_checked()
        print('전체공개(구 편집기):', '선택됨' if ok else '선택 실패')
        legacy.locator('a#cafewritebtn').first.click()
        # 구 편집기는 iframe 안에서 저장돼 바깥 URL이 안 바뀐다. 저장 프레임이 사라질 때까지만 기다리고 API(openArticle)로 검증한다.
        for _ in range(20):
            edit.wait_for_timeout(1000)
            if not any('m=modify' in fr.url for fr in edit.frames): break
        return f'https://cafe.naver.com/firemap/{article_id}'
    if not set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
    return submit_cafe(edit)

def open_cafe_edit(page, article_id):
    """글 보기 → '수정' → 편집 페이지(새 탭이면 그쪽) 반환."""
    page.goto(f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/{article_id}', wait_until='domcontentloaded')
    page.wait_for_timeout(5000)
    ctx = page.context; before = set(ctx.pages)
    page.get_by_role('button', name=re.compile(r'^\s*수정\s*$')).first.click()
    page.wait_for_timeout(6000)
    new = [q for q in ctx.pages if q not in before]
    edit = new[0] if new else page
    edit.wait_for_load_state('domcontentloaded'); edit.wait_for_timeout(3000)
    close_popups(edit.main_frame)
    return edit

def rewrite_cafe(page, article_id, pkg):
    """본문이 빠진 채 올라간 글(2026-09-22 사고)을 같은 글 번호로 고친다: 수정 화면에서 본문을 비우고 묶음 순서대로 다시 넣는다."""
    title, seq, meta = read_pkg(pkg)
    edit = open_cafe_edit(page, article_id)
    frame = edit.main_frame
    if not frame.locator('.se-component').count(): raise RuntimeError('새 편집기가 아님(구 편집기 글은 rewrite 미지원)')
    click_last_paragraph(frame)
    edit.keyboard.press('Control+A'); edit.wait_for_timeout(200); edit.keyboard.press('Delete'); edit.wait_for_timeout(800)
    left = frame.locator('.se-component.se-image').count()
    if left: raise RuntimeError(f'본문 비우기 실패(사진 {left}장 남음)')
    photo = edit.locator('button[data-name="image"]').first
    for kind, val in seq:
        if kind == 'text': type_text(frame, val)
        else: insert_image(frame, val, photo)
    verify_body(frame, seq, f'카페 {article_id} 재작성')
    shot(edit, f'cafe_rewrite_{article_id}')
    if not set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
    return submit_cafe(edit)

PUBLISHED_JS = """() => { const c = document.querySelector('.se-main-container') || document.body;
  const t = [...c.querySelectorAll('.se-component.se-text .se-text-paragraph')].map(e=>e.innerText).join('').replace(/[\\s\\u200b]+/g,'').length;
  return {text: t, img: c.querySelectorAll('.se-component.se-image').length}; }"""

def verify_published(page, pkg):
    """발행된 실제 페이지의 글자 수·사진 수를 묶음과 대조한다. 편집기 안이 아니라 '올라간 글'을 본다.
    2026-09-22 사고: 편집기 스크린샷만 믿고 9편이 본문 없이 나갔다. 결과는 pkg/verify.txt에 남긴다."""
    title, seq, meta = read_pkg(pkg)
    pub = os.path.join(pkg, 'published.txt')
    if not os.path.exists(pub): return {'ok': False, 'why': 'published.txt 없음'}
    url = open(pub, encoding='utf-8').read().strip().splitlines()[-1]
    m = re.search(r'logNo=(\d+)|kygstar7777/(\d+)', url); c = re.search(r'firemap/(\d+)|articles/(\d+)|articleid=(\d+)', url, re.I)
    if m: page.goto(f'https://m.blog.naver.com/PostView.naver?blogId={BLOG_ID}&logNo={m.group(1) or m.group(2)}', wait_until='domcontentloaded')
    elif c: page.goto(f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/{c.group(1) or c.group(2) or c.group(3)}', wait_until='domcontentloaded')
    else: return {'ok': False, 'why': 'URL 형식 모름 ' + url}
    page.wait_for_timeout(4500)
    best = {'text': -1, 'img': 0}
    for fr in page.frames:
        try:
            r = fr.evaluate(PUBLISHED_JS)
            if r['text'] > best['text']: best = r
        except Exception: pass
    want = sum(len(re.sub(r'\s+', '', v)) for k, v in seq if k == 'text'); want_img = sum(1 for k, _ in seq if k == 'img')
    ok = best['text'] >= want * 0.9 and best['img'] >= want_img
    res = {'ok': ok, 'url': url, 'text': best['text'], 'want': want, 'img': best['img'], 'want_img': want_img}
    open(os.path.join(pkg, 'verify.txt'), 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False) + '\n')
    return res

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    # pending은 브라우저가 필요 없다 — live_pairs()가 평범한 HTTP로 올라간 제목을 받아 온다.
    # 그런데도 launch()를 거치느라 브라우저 잠금을 잡고 있었다. 2026-09-25 01:55 실측:
    # 잠금 주인이 pending(PID 919404)이었고, 그 뒤에서 blog 발행이 15분을 기다리다 시간 초과로 죽었다.
    # 회차마다 pending을 부르는 루틴이 여럿이라 발행이 계속 굶었다(0편 회차의 원인).
    if cmd == 'pending':
        for x in list_pending(): print(json.dumps({k: v for k, v in x.items() if k != 'mtime'}, ensure_ascii=False))
        return
    with sync_playwright() as p:
        if cmd == 'login':
            try: os.path.exists(AUTHFAIL) and os.remove(AUTHFAIL)
            except Exception: pass
            ctx = launch(p, headless=False); page = ctx.new_page()
            page.goto('https://nid.naver.com/nidlogin.login?url=https://www.naver.com/')
            page.wait_for_timeout(2500)
            # '로그인 상태 유지'를 미리 켜 둔다. 이게 꺼져 있으면 네이버가 만료일 없는 **세션 쿠키**를 줘서
            # 브라우저를 닫는 순간 사라진다. 우리는 파일로 되살려 쓰지만 하루이틀이면 풀린다 —
            # 2026-09-25에 카페가 11시간, 전날 블로그가 2시간 멈춘 원인이 전부 이것이었다.
            # 비밀번호는 사람이 친다. 여기서는 체크박스만 건드린다.
            try:
                box = page.locator('#keep, input[name="nvlong"], label:has-text("로그인 상태 유지") input').first
                if box.count():
                    if not box.is_checked():
                        box.check(force=True); page.wait_for_timeout(300)
                    print('로그인 상태 유지: 켬' if box.is_checked() else '로그인 상태 유지: 못 켬(직접 눌러 주세요)')
                else:
                    page.get_by_text('로그인 상태 유지', exact=False).first.click(); page.wait_for_timeout(300)
                    print('로그인 상태 유지: 눌렀다(글자 클릭)')
            except Exception as e:
                print('로그인 상태 유지를 못 켰다 — 창에서 직접 체크해 주세요:', repr(e)[:80])
            print('브라우저 창에서 네이버에 로그인하세요. 로그인이 확인되면 자동으로 닫힙니다(최대 10분).')
            for _ in range(120):
                page.wait_for_timeout(5000)
                if 'nidlogin' not in page.url and logged_in(page):
                    ctx.storage_state(path=STATE)
                    # 알림 쿨다운 도장을 여기서 지운다. 안 지우면 방금 푼 로그인이 6시간 안에 또 막혀도
                    # alert_login이 쿨다운에 걸려 조용히 넘어간다(2026-09-25 11:15 실측:
                    # 10:32에 찍힌 도장이 11:15 로그인 뒤에도 그대로 남아 있었다).
                    try:
                        stamp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '.login_alert')
                        os.path.exists(stamp) and os.remove(stamp)
                    except Exception: pass
                    print('로그인 확인. 쿠키 저장:', STATE); ctx.close(); return
            print('로그인 확인 실패(시간 초과)'); ctx.close(); sys.exit(1)
        ctx = launch(p, headless=(cmd != 'shot' and os.environ.get('NAVER_HEADED') != '1'))
        page = ctx.new_page()
        pkg = None
        try:
            if cmd == 'check':
                ok = logged_in(page)
                af = auth_fail_seen()
                if ok and af:
                    # 쿠키는 살아 있어도 글쓰기 API가 IP로 막으면 '로그인됨'은 거짓말이다(2026-09-25).
                    print('로그인 안 됨 — 쿠키는 있는데 글쓰기가 IP 확인에서 막혔다:', af)
                    print('사장님이 `py -3.12 work/naverpost.py login` 을 다시 해야 한다.')
                    alert_login(af)
                    sys.exit(2)
                if not ok: alert_login('쿠키가 만료됐다(로그인 화면으로 넘어간다)')
                print('로그인됨' if ok else '로그인 안 됨'); sys.exit(0 if ok else 2)
            if cmd == 'shot':
                page.goto(sys.argv[2], wait_until='domcontentloaded'); page.wait_for_timeout(5000)
                page.screenshot(path=sys.argv[3], full_page=True); print(sys.argv[3]); return
            if not logged_in(page): print('로그인 안 됨 — python work/naverpost.py login'); sys.exit(2)
            if cmd == 'verify':                       # python work/naverpost.py verify <pkg> [<pkg> ...]  또는 verify today
                pkgs = sys.argv[2:]
                if pkgs == ['today']:
                    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research'); day = time.strftime('%Y-%m-%d')
                    pkgs = [os.path.join(base, d, 'pkg') for d in os.listdir(base) if os.path.exists(os.path.join(base, d, 'pkg', 'published.txt'))
                            and time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(os.path.join(base, d, 'pkg', 'published.txt')))) == day]
                bad = 0
                for pk in pkgs:
                    r = verify_published(page, os.path.abspath(pk)); bad += (not r['ok'])
                    print(('OK  ' if r['ok'] else 'BAD ') + os.path.basename(os.path.dirname(pk)), json.dumps(r, ensure_ascii=False))
                sys.exit(1 if bad else 0)
            if cmd == 'rewrite':                      # python work/naverpost.py rewrite 45 work/research/sidejob/pkg
                print(rewrite_cafe(page, int(sys.argv[2]), os.path.abspath(sys.argv[3]))); return
            if cmd == 'public':                       # python work/naverpost.py public 35 36 37
                for aid in sys.argv[2:]:
                    try: print(aid, cafe_make_public(page, aid))
                    except Exception as e: print(aid, '실패:', repr(e)[:200]); shot(page, 'error_public_' + aid)
                return
            args = [a for a in sys.argv[2:] if a != '--wait']
            wait = '--wait' in sys.argv
            pkg = os.path.abspath(args[0])
            title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
            # 올리기 전에 같은 제목이 이미 올라가 있는지 본다. published.txt가 없어도 글은 올라가 있을 수 있다.
            up = already_up(cmd, title)
            if up:
                open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write(up + '\n')
                print('이미 올라가 있음 — 다시 올리지 않음'); print('URL', up); return
            # 제목이 달라도 같은 대상을 또 쓰는 것을 막는다. 사장님 2026-09-24 "상계주공만 왜 글을 쓰는 거야?"
            # 그날 03:46 "상계주공9단지 2,830세대 매매…"와 13:21 "상계주공9단지 8월 실거래…"가 같이 나갔다.
            # 일부러 이어 쓰는 연재면 --same-ok 를 붙인다.
            if '--same-ok' not in sys.argv:
                dup = same_subject_today(cmd, title)
                if dup:
                    print('같은 대상을 최근에 이미 썼다 — 올리지 않는다. 편성표의 다음 슬롯으로 간다.')
                    for t, u, keys in dup[:3]: print(f'  겹친 말 {keys} · {t[:46]} · {u}')
                    print('이어 쓰는 연재가 맞으면 --same-ok 를 붙여 다시 실행한다.')
                    sys.exit(3)
            url = post_blog(page, pkg, wait) if cmd == 'blog' else post_cafe(page, pkg, wait)
            open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write(url + '\n')
            print('URL', url)
        except Exception as e:
            # 발행 버튼까지 눌리고 그 뒤(주소 이동 대기 등)에서 터지면 글은 올라가 있다.
            # 이걸 실패로 돌려주면 다음 회차가 같은 글을 또 올린다(2026-09-24 07:13·07:35).
            if pkg and cmd in ('blog', 'cafe'):
                try:
                    t = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
                    up = already_up(cmd, t)
                    if up:
                        open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write(up + '\n')
                        print('발행 뒤 오류(' + repr(e)[:120] + ') — 글은 올라가 있어 성공으로 처리')
                        print('URL', up); return
                except Exception as e2: print('발행 확인 실패:', repr(e2)[:120])
            # 오류 메시지를 **먼저** 찍는다. 2026-09-25: 브라우저가 이미 닫힌 채로 오류가 나면
            # shot()이 TargetClosedError로 같이 죽어서, 정작 원인인 e가 한 줄도 안 남았다.
            # 로그에 Playwright 내부 traceback만 남고 "왜 실패했나"는 사라져 회차마다 원인을 못 찾았다.
            print('실패:', repr(e)[:300])
            try: print('스크린샷', shot(page, 'error_' + cmd))
            except Exception as e3: print('스크린샷 실패(브라우저가 이미 닫힘):', repr(e3)[:120])
            sys.exit(1)
        finally:
            ctx.close()

if __name__ == '__main__':
    main()
