# 제목 수정 실험 — 사장님 2026-09-23 "수정이력 남으면 안 돼? 제목 고치면 SEO에 안 좋아?"
#   py -3.12 work/titletest.py before <글번호>            → 고치기 전 상태를 잰다
#   py -3.12 work/titletest.py change <글번호> "<새 제목>"  → 제목만 바꾼다(본문은 건드리지 않는다)
#   py -3.12 work/titletest.py after <글번호>             → 고친 뒤 상태를 재고 before와 견준다
#
# 내가 "수정 이력이 남아서 안 된다"고 확인 없이 말했다가 지적받았다. 그래서 직접 재서 답한다.
# 재는 것: (1) 화면·API에 수정 표시가 붙는가 (2) 제목 검색에서 그 글이 계속 나오는가 (3) 조회수
import sys, os, re, json, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LOG = os.path.join(HERE, 'titletest.json')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Referer': 'https://cafe.naver.com/'}
CAFE_ID = '31789001'
MARKS = ('수정됨', '수정 됨', '수정일', '편집됨', '(수정)', '수정함')

# 검색은 Referer가 cafe.naver.com이면 403이 난다(2026-09-23 확인) → 검색에는 평범한 브라우저 헤더만 쓴다
SUA = {'User-Agent': UA['User-Agent']}

def get(u, h=None):
    return urllib.request.urlopen(urllib.request.Request(u, headers=h or UA), timeout=25).read().decode('utf-8', 'ignore')

def api_article(aid):
    u = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{CAFE_ID}/articles/{aid}?query=&useCafeId=true'
    try:
        art = json.loads(get(u))['result']['article']
        return {'subject': art.get('subject'), 'writeDate': art.get('writeDate'), 'readCount': art.get('readCount'),
                '수정 관련 필드': {k: v for k, v in art.items() if re.search('updat|modif|edit', k, re.I)} or '없음'}
    except Exception as e:
        return {'오류': str(e)[:100]}

def search_hit(title, aid):
    """제목 그대로 검색했을 때 그 글이 검색 결과에 나오는가"""
    out = {}
    for tab in ('cafe', 'all'):
        try:
            s = get(f'https://search.naver.com/search.naver?ssc=tab.{tab}.all&query=' + urllib.parse.quote(title), SUA)
            out[tab] = f'/{aid}' in s and 'firemap' in s
        except Exception as e:
            out[tab] = '오류 ' + str(e)[:40]
        time.sleep(1.2)
    return out

def page_marks(aid):
    """글 화면에 수정 표시 문구가 있는지 — 전용 브라우저로 실제 화면을 읽는다"""
    import naverpost as N
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = N.launch(p, headless=True); page = ctx.new_page()
        try:
            page.goto(f'https://cafe.naver.com/firemap/{aid}', wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(6000)
            t = ' '.join(f.evaluate('document.body.innerText') for f in page.frames if f.url)
            t = re.sub(r'\s+', ' ', t)
            return {'화면 글자': len(t), '수정 표시': [m for m in MARKS if m in t] or '없음'}
        finally:
            ctx.close()

def snap(aid, label):
    a = api_article(aid)
    rec = {'when': time.strftime('%Y-%m-%d %H:%M'), 'label': label, 'article': aid, 'api': a}
    rec['page'] = page_marks(aid)
    if a.get('subject'): rec['search'] = search_hit(a['subject'], aid)
    log = []
    if os.path.exists(LOG):
        try: log = json.load(open(LOG, encoding='utf-8'))
        except Exception: log = []
    log.append(rec); json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"[{label}] {rec['when']}  글 {aid}")
    print('  제목      :', a.get('subject'))
    print('  조회      :', a.get('readCount'))
    print('  API 수정필드:', a.get('수정 관련 필드'))
    print('  화면 수정표시:', rec['page']['수정 표시'])
    print('  제목검색 노출:', rec.get('search'))
    return rec

def change_title(aid, new_title):
    """제목만 바꾼다. 본문·사진은 손대지 않는다."""
    import naverpost as N
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = N.launch(p, headless=True); page = ctx.new_page()
        try:
            edit = N.open_cafe_edit(page, aid)
            frame = edit.main_frame
            # 카페 새 편집기의 제목 칸. 입력창이면 fill, 편집기 문단이면 전체선택 후 입력.
            box = None
            for sel in ('input#subject', 'input[name="subject"]', '.textarea_input', 'textarea#subject'):
                q = edit.locator(sel).first
                if q.count(): box = ('input', q); break
            if box is None:
                q = frame.locator('.se-documentTitle .se-text-paragraph, .se-title-text').first
                if q.count(): box = ('editor', q)
            if box is None: raise RuntimeError('제목 칸을 못 찾음')
            kind, q = box
            before = (q.input_value() if kind == 'input' else q.inner_text()).strip()
            print('  편집 화면의 지금 제목:', before)
            if kind == 'input':
                q.fill(new_title)
            else:
                q.click(); edit.keyboard.press('Control+A'); edit.wait_for_timeout(200)
                edit.keyboard.press('Delete'); edit.wait_for_timeout(300)
                edit.keyboard.insert_text(new_title)
            edit.wait_for_timeout(600)
            N.shot(edit, f'titletest_{aid}')
            if not N.set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
            url = N.submit_cafe(edit)
            print('  수정 완료:', url)
            return url
        finally:
            ctx.close()

if __name__ == '__main__':
    cmd = sys.argv[1]; aid = int(sys.argv[2])
    if cmd == 'before': snap(aid, '수정 전')
    elif cmd == 'change': change_title(aid, sys.argv[3])
    elif cmd == 'after': snap(aid, '수정 후')
    else: print('before | change <새 제목> | after')
