"""카페 글을 네이버 공식 카페 글쓰기 API로 올린다(2026-09-30 전체 회의 배정, BACKLOG C7).

왜: 화면 조작(naverpost.py cafe)은 네이버 운영정책의 '자동화된 수단' 조항에 걸린다는 판정이 나왔다.
   공식 API(openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles)는 네이버가 열어 둔 길이다.
   10/2 21시 회의까지 옮기지 못하면 research/STOP_cafe 가 켜진다.

토큰: firemap.kr 의 네이버 로그인(앱 '카페에 올리기'와 같은 길)을 로그인된 발행 프로필로 한 번 지나간다.
   /naver-callback 으로 돌아오는 순간 code 를 가로채(앱이 먼저 써 버리면 한 번짜리 code가 사라진다)
   firemap.kr/naver-token 에 바꿔 달라고 한다. 시크릿은 Cloudflare 에만 있고 여기엔 없다.
   동의 화면이 나오면 누르지 않고 멈춘다(사람이 한 번 동의해야 한다 → tools-wanted).

제약(메모리 naver-cafe-api-limits, 2026-09-14 실측):
   본문의 <a>·<img> 태그, 큰따옴표 " → 403 code 999(내용 거부, 인증 문제 아님)
   그림은 파트 이름 0,1,2 로 여러 장 붙지만 전부 글 맨 앞에 몰린다
   필드 순서 subject → content → 그림, openyn 안 보내면 멤버 공개

쓰는 법:
   py -3.12 work/cafeapi.py token              토큰만 받아 본다(글 안 올림)
   py -3.12 work/cafeapi.py post <pkg> --dry   보낼 내용만 만들어 보여 준다(글 안 올림)
   py -3.12 work/cafeapi.py post <pkg>         올린다(발행 회차만)
"""
import os, re, sys, json, time, html, urllib.request, urllib.parse, secrets, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import naverpost as np_

SITE = 'https://firemap.kr'
TOKEN_FILE = os.path.join(np_.PROFILE, 'cafe_api_token.json')   # 저장소 밖(발행 프로필 폴더). 커밋되지 않는다
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', '_cafeapi_log.jsonl')
MAX_IMG = 3


def log(**kw):
    kw['at'] = datetime.datetime.now().isoformat(timespec='seconds')
    with open(LOG, 'a', encoding='utf-8') as f: f.write(json.dumps(kw, ensure_ascii=False) + '\n')


def _get_json(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def cached_token():
    try:
        t = json.load(open(TOKEN_FILE, encoding='utf-8'))
        if t.get('expires_at', 0) > time.time() + 300: return t['access_token']
    except Exception: pass
    return None


def get_token(headless=True):
    """로그인된 발행 프로필로 firemap.kr 네이버 로그인을 지나가 액세스 토큰을 받는다."""
    tok = cached_token()
    if tok: return tok
    cfg = _get_json(SITE + '/cafe-post')
    if not (cfg.get('enabled') and cfg.get('clientId')):
        raise RuntimeError('firemap.kr 카페 게시가 꺼져 있다(Pages 환경변수 NAVER_CLIENT_ID/SECRET)')
    state = secrets.token_hex(8)
    q = urllib.parse.urlencode({'response_type': 'code', 'client_id': cfg['clientId'],
                                'redirect_uri': SITE + '/naver-callback', 'state': state})
    auth_url = 'https://nid.naver.com/oauth2.0/authorize?' + q
    got = {}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = np_.launch(p, headless=headless)
        try:
            page = ctx.new_page()
            def grab(route):
                got['url'] = route.request.url
                route.fulfill(status=200, content_type='text/plain', body='ok')
            page.route('**/naver-callback*', grab)
            page.goto(auth_url, wait_until='domcontentloaded')
            for _ in range(40):
                if got: break
                page.wait_for_timeout(500)
            if not got:
                shot = np_.shot(page, 'cafeapi_auth')
                where = page.url[:120]
                body = ''
                try: body = page.inner_text('body')[:200].replace('\n', ' ')
                except Exception: pass
                kind = '동의 화면' if ('동의' in body or 'agree' in where) else ('로그인 풀림' if 'nidlogin' in where else '알 수 없음')
                log(step='token', ok=False, kind=kind, where=where, shot=shot)
                raise RuntimeError(f'인가 code 를 못 받았다({kind}) — {where} · 화면 {shot}')
        finally:
            ctx.close()
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(got['url']).query)
    if qs.get('state', [''])[0] != state: raise RuntimeError('state 불일치')
    if 'code' not in qs: raise RuntimeError('code 없음: ' + got['url'][:150])
    j = _get_json(SITE + '/naver-token', data=json.dumps({'code': qs['code'][0], 'state': state}).encode(),
                  headers={'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    if not j.get('access_token'): raise RuntimeError('토큰 교환 실패: ' + json.dumps(j)[:150])
    exp = time.time() + int(j.get('expires_in') or 3600)
    json.dump({'access_token': j['access_token'], 'expires_at': exp}, open(TOKEN_FILE, 'w', encoding='utf-8'))
    log(step='token', ok=True, expires_in=j.get('expires_in'))
    return j['access_token']


def menu_ids():
    """게시판 이름 → menuId. naverpost.cafe_boards 와 같은 공개 API."""
    u = f'https://apis.naver.com/cafe-web/cafe2/SideMenuList?cafeId={np_.CAFE_ID}'
    d = _get_json(u, headers=np_.UA)
    ms = d.get('message', {}).get('result', {}).get('menus') or []
    return {html.unescape(m['menuName']): m['menuId'] for m in ms if m.get('menuType') == 'B' and m.get('menuName')}


def safe_text(t):
    """API가 거부하는 것을 덜어낸다: 큰따옴표 → 「」, 태그는 escape 로 글자가 된다."""
    t = re.sub(r'"([^"\n]{1,80})"', r'「\1」', t)
    t = t.replace('"', "'")
    return t


def build(pkg):
    title, seq, meta = np_.read_pkg(pkg)
    texts = [v for k, v in seq if k == 'text']
    imgs = [v for k, v in seq if k == 'img'][:MAX_IMG]
    body = '\n\n'.join(texts)
    if np_.CAFE_TAIL not in body: body += '\n\n' + np_.CAFE_TAIL   # 주소는 글자로만(<a> 금지)
    body = safe_text(body)
    content = html.escape(body, quote=False).replace('\r\n', '\n').replace('\n', '<br>')
    return safe_text(title), content, imgs, meta.get('게시판', '자유게시판'), body


def multipart(subject, content, imgs):
    b = '----fm' + secrets.token_hex(12)
    out = []
    def field(name, val):
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode())
    field('subject', urllib.parse.quote(subject))
    field('content', urllib.parse.quote(content))
    field('openyn', 'true'); field('searchopen', 'true'); field('replyyn', 'true')
    for i, path in enumerate(imgs):
        ext = os.path.splitext(path)[1].lower()
        ct = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}.get(ext, 'image/png')
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{i}"; filename="{os.path.basename(path)}"\r\n'
                   f'Content-Type: {ct}\r\n\r\n'.encode() + open(path, 'rb').read() + b'\r\n')
    out.append(f'--{b}--\r\n'.encode())
    return b''.join(out), 'multipart/form-data; boundary=' + b


def send(token, menu, subject, content, imgs):
    url = f'https://openapi.naver.com/v1/cafe/{np_.CAFE_ID}/menu/{menu}/articles'
    plans = [('plain+all', imgs)]
    if len(imgs) > 1: plans.append(('plain+one', imgs[:1]))
    if imgs: plans.append(('plain+none', []))
    tried = []
    for tag, im in plans:
        data, ct = multipart(subject, content, im)
        req = urllib.request.Request(url, data=data, method='POST',
                                     headers={'Authorization': 'Bearer ' + token, 'Content-Type': ct})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                status, j = r.status, json.load(r)
        except urllib.error.HTTPError as e:
            status = e.code
            try: j = json.loads(e.read().decode('utf-8', 'ignore'))
            except Exception: j = {}
        link = (((j or {}).get('message') or {}).get('result') or {}).get('articleUrl')
        if link: return link, tag, tried
        raw = json.dumps(j, ensure_ascii=False)[:200]
        tried.append(f'{tag}:{status} {raw}')
        if status == 401 or status == 429 or 'Authentication failed' in raw: break   # 999(내용 거부)만 덜어내며 재시도
    return None, '', tried


def cmd_post(pkg, dry):
    pkg = os.path.abspath(pkg)
    subject, content, imgs, want, plain = build(pkg)
    menus = menu_ids()
    menu = menus.get(want) or menus.get('자유게시판') or '1'
    print(f'제목 {subject}\n게시판 {want} → menuId {menu}\n본문 {len(plain)}자 · 그림 {len(imgs)}장(글 맨 앞에 붙는다)')
    for p in imgs: print('   ', os.path.relpath(p, pkg))
    if dry:
        print('--- 본문 앞 400자 ---\n' + plain[:400])
        tok = cached_token()
        print('토큰', '있음(캐시)' if tok else '없음 — token 으로 받는다')
        log(step='dry', pkg=pkg, chars=len(plain), imgs=len(imgs), menu=menu)
        return
    # 발행 관문 — naverpost.py cafe 와 같은 것을 본다
    title = open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read().strip()
    np_.day_guard('cafe')
    blk = np_.pending_block('cafe', pkg, title)
    if blk: print('올리지 않는다:', blk); sys.exit(3)
    rp = os.path.join(pkg, 'check_read.txt')
    if not os.path.exists(rp) or any(l.strip() and not l.startswith('지적 없음')
                                     for l in open(rp, encoding='utf-8').read().splitlines()):
        print('읽기 검사 미통과 — py -3.12 work/readcheck.py ' + pkg); sys.exit(4)
    import aitell   # AI 티 검사(10/1) — naverpost.py와 같은 관문
    ok_ai, msg_ai, hits_ai = aitell.gate_pkg(pkg)
    if not ok_ai: aitell.refuse(msg_ai, hits_ai); sys.exit(4)
    print(msg_ai)
    up = np_.already_up('cafe', title)
    if up: print('이미 올라가 있음', up); return
    token = get_token()
    link, tag, tried = send(token, menu, subject, content, imgs)
    log(step='post', pkg=pkg, ok=bool(link), url=link, via=tag, tried=tried)
    if not link:
        print('실패:', ' | '.join(tried)); sys.exit(1)
    open(os.path.join(pkg, 'published.txt'), 'w', encoding='utf-8').write(link + '\n')
    print('URL', link, '·', tag)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ('token', 'post'):
        print(__doc__); return
    if a[0] == 'token':
        t = get_token(headless='--show' not in a)
        print('토큰 받음', t[:6] + '…', '→', TOKEN_FILE)
    else:
        cmd_post(a[1], '--dry' in a)


if __name__ == '__main__':
    main()
