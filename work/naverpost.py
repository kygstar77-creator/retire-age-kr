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
import sys, os, re, time, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

PROFILE = os.environ.get('NAVER_PROFILE', r'C:\Users\강영준\Documents\naver_profile')
STATE = os.path.join(PROFILE, 'storage_state.json')   # 로그인 쿠키(세션 쿠키 포함). 프로필만으로는 창을 닫으면 사라진다
BLOG_ID = 'kygstar7777'
CAFE_ID = '31789001'
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '_shots')
os.makedirs(SHOTS, exist_ok=True)

def launch(p, headless):
    ctx = p.chromium.launch_persistent_context(
        PROFILE, headless=headless, viewport={'width': 1400, 'height': 1000}, locale='ko-KR',
        args=['--disable-blink-features=AutomationControlled'])
    if os.path.exists(STATE):
        try: ctx.add_cookies(json.load(open(STATE, encoding='utf-8'))['cookies'])
        except Exception as e: print('쿠키 불러오기 실패:', e)
    return ctx

def shot(page, name):
    path = os.path.join(SHOTS, name + '.png'); page.screenshot(path=path, full_page=False); return path

def logged_in(page):
    # 화면이 아니라 로그인 쿠키(NID_AUT·NID_SES)로 판정한다. 화면 파싱은 헤드리스에서 틀렸다.
    names = {c['name'] for c in page.context.cookies('https://www.naver.com')}
    return 'NID_AUT' in names and 'NID_SES' in names

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
    # 화면 아래 떠 있는 '글감 검색' 바가 마지막 문단을 가리면 클릭이 막힌다 → 가운데로 스크롤한 뒤 클릭, 그래도 막히면 강제 클릭
    para = frame.locator('.se-text-paragraph').last
    try: para.evaluate("e => e.scrollIntoView({block: 'center'})"); frame.page.wait_for_timeout(200)
    except Exception: pass
    try: para.click(timeout=4000)
    except Exception: para.click(force=True)
    frame.page.wait_for_timeout(200)

def type_text(frame, text):
    page = frame.page
    click_last_paragraph(frame); ensure_plain(frame)
    for para in text.split('\n'):
        if para.strip(): page.keyboard.insert_text(para); page.wait_for_timeout(120)
        page.keyboard.press('Enter'); page.wait_for_timeout(120)

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

def published_titles():
    import urllib.request, html
    UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
    blog, cafe = set(), set()
    try:
        s = urllib.request.urlopen(urllib.request.Request(f'https://rss.blog.naver.com/{BLOG_ID}.xml', headers=UA), timeout=20).read().decode('utf-8', 'ignore')
        for it in re.findall(r'<item>(.*?)</item>', s, re.S):
            t = re.search(r'<title>(.*?)</title>', it, re.S)
            if t: blog.add(norm(html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', t.group(1)))))
    except Exception as e: print('RSS 실패:', e)
    try:
        u = f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={CAFE_ID}&search.queryType=lastArticle&search.page=1&search.perPage=50'
        for a in json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))['message']['result']['articleList']:
            cafe.add(norm(a.get('subject', '')))
    except Exception as e: print('카페 API 실패:', e)
    return blog, cafe

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
def post_blog(page, pkg):
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
    frame.get_by_role('button', name=re.compile(r'^\s*발행\s*$')).last.click()
    # 발행 뒤 PostView.naver?...&logNo=NNN 또는 /kygstar7777/NNN 으로 이동한다
    page.wait_for_url(re.compile(r'logNo=\d+|blog\.naver\.com/' + BLOG_ID + r'/\d+'), timeout=30000)
    m = re.search(r'logNo=(\d+)', page.url) or re.search(BLOG_ID + r'/(\d+)', page.url)
    return f'https://blog.naver.com/{BLOG_ID}/{m.group(1)}' if m else page.url

# ---------- 카페 ----------
def post_cafe(page, pkg):
    title, seq, meta = read_pkg(pkg)
    page.goto(f'https://cafe.naver.com/ca-fe/cafes/{CAFE_ID}/articles/write', wait_until='domcontentloaded')
    page.wait_for_timeout(6000)
    frame = page.main_frame
    close_popups(frame)   # 임시등록 복구 팝업 등
    page.locator('button:has-text("게시판을 선택해 주세요"), .FormSelectButton').first.click(); page.wait_for_timeout(600)
    page.locator(f'text="{meta.get("게시판", "자유게시판")}"').first.click(); page.wait_for_timeout(500)
    page.locator('textarea[placeholder*="제목"], input[placeholder*="제목"]').first.fill(title)
    frame = page.main_frame
    photo = page.locator('button[data-name="image"]').first
    for kind, val in seq:
        if kind == 'text': type_text(frame, val)
        else: insert_image(frame, val, photo)
    shot(page, 'cafe_body')
    set_cafe_public(page)
    return submit_cafe(page)

def set_cafe_public(page):
    """공개 설정을 전체공개로. 라디오(name=public value=true)는 비활성이 아니다 — 2026-09-22 프로브로 확인.
    화면 조작 때는 클릭 지점이 어긋나 안 바뀐 것뿐이었다."""
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

def submit_cafe(page):
    page.get_by_role('button', name=re.compile(r'^\s*등록\s*$')).first.click()   # '임시등록'이 아니라 '등록'만
    # 전체공개면 "이 글은 전체공개로 설정되어 있어요 ... 계속할까요?" 확인 창이 뜬다(2026-09-22 실측) → 확인
    try:
        dlg = page.get_by_text('전체공개로 설정', exact=False).first
        if dlg.is_visible(timeout=3000):
            page.get_by_role('button', name=re.compile(r'^\s*확인\s*$')).last.click(); page.wait_for_timeout(500)
    except Exception: pass
    # 등록 뒤 ArticleRead.nhn?...&articleid=NN 또는 .../articles/NN 또는 /firemap/NN 으로 이동한다
    page.wait_for_url(re.compile(r'articleid=\d+|articles/\d+|cafe\.naver\.com/firemap/\d+', re.I), timeout=30000)
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

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    with sync_playwright() as p:
        if cmd == 'login':
            ctx = launch(p, headless=False); page = ctx.new_page()
            page.goto('https://nid.naver.com/nidlogin.login?url=https://www.naver.com/')
            print('브라우저 창에서 네이버에 로그인하세요. 로그인이 확인되면 자동으로 닫힙니다(최대 10분).')
            for _ in range(120):
                page.wait_for_timeout(5000)
                if 'nidlogin' not in page.url and logged_in(page):
                    ctx.storage_state(path=STATE)
                    print('로그인 확인. 쿠키 저장:', STATE); ctx.close(); return
            print('로그인 확인 실패(시간 초과)'); ctx.close(); sys.exit(1)
        ctx = launch(p, headless=(cmd != 'shot' and os.environ.get('NAVER_HEADED') != '1'))
        page = ctx.new_page()
        try:
            if cmd == 'check':
                ok = logged_in(page); print('로그인됨' if ok else '로그인 안 됨'); sys.exit(0 if ok else 2)
            if cmd == 'pending':
                for x in list_pending(): print(json.dumps({k: v for k, v in x.items() if k != 'mtime'}, ensure_ascii=False))
                return
            if cmd == 'shot':
                page.goto(sys.argv[2], wait_until='domcontentloaded'); page.wait_for_timeout(5000)
                page.screenshot(path=sys.argv[3], full_page=True); print(sys.argv[3]); return
            if not logged_in(page): print('로그인 안 됨 — python work/naverpost.py login'); sys.exit(2)
            if cmd == 'public':                       # python work/naverpost.py public 35 36 37
                for aid in sys.argv[2:]:
                    try: print(aid, cafe_make_public(page, aid))
                    except Exception as e: print(aid, '실패:', repr(e)[:200]); shot(page, 'error_public_' + aid)
                return
            pkg = os.path.abspath(sys.argv[2])
            url = post_blog(page, pkg) if cmd == 'blog' else post_cafe(page, pkg)
            open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write(url + '\n')
            print('URL', url)
        except Exception as e:
            path = shot(page, 'error_' + cmd); print('실패:', repr(e)[:300]); print('스크린샷', path); sys.exit(1)
        finally:
            ctx.close()

if __name__ == '__main__':
    main()
