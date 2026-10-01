# 이미 공개된 카페 글의 본문 글자만 고친다(2026-10-01, editor 요청 · 순돌이 지시).
# 편집 전수 점검(work/research/editor/sweep.md)의 유일한 적용 길이다. 새 글 발행 경로(naverpost.py cafe)는 건드리지 않는다.
#
#   py -3.12 work/naverpost.py edit 44 work/research/editor/2026-10-01/cafe/44.txt          # dry(기본): 원본 백업 + 대조표, 브라우저 안 씀
#   py -3.12 work/naverpost.py edit-ok work/research/editor/2026-10-01/cafe/44.txt firemap-editor   # editor가 대조표를 보고 통과 표시
#   py -3.12 work/naverpost.py edit 44 work/research/editor/2026-10-01/cafe/44.txt --apply  # 적용(통과 표시 + 하루 상한 + STOP 확인)
#
# 원칙
# - 사진은 손대지 않는다. 글 덩어리(se-text)만 갈아 끼우고, 사진(se-image)은 원래 자리·원래 파일 그대로 둔다.
#   새 원고의 어느 줄이 어느 글 덩어리로 가는지는 '각 덩어리 첫 줄(소제목)'을 닻으로 찾는다. 닻이 없으면 거절.
# - 숫자는 한 글자도 안 바뀐다: 원본 글과 새 원고의 숫자 목록(Counter)이 다르면 거절.
# - 하루 EDIT_CAP편까지만. 네이버 무인 게시 확대 금지 — 수정은 이미 올라간 글에 한정한다.
# - 적용 전 원본 HTML을 work/research/_cafe_edit/<글번호>/에 남기고, 적용 뒤 글 API를 다시 읽어
#   사진 주소 목록이 그대로인지·글 덩어리가 새 원고와 같은지 대조한다. 되돌리기는 .orig 원고로 같은 명령을 돌린다.
import os, re, sys, json, time, hashlib, html as _html, collections, datetime, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'research', '_cafe_edit')
LOG = os.path.join(OUT, 'log.jsonl')
CAFE_ID = '31789001'
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://cafe.naver.com/'}
EDIT_CAP = 3          # 하루 수정 상한(편). 카페 새 글 상한 5편과 따로 센다.
ZW = '​‌‍﻿'

def norm(s):
    return re.sub(r'[\s' + ZW + r']+', '', _html.unescape(re.sub(r'<[^>]+>', ' ', s or '')))

def nums(s):
    return collections.Counter(re.findall(r'\d[\d,.]*\d|\d', _html.unescape(s or '')))

# ---------- 읽기 ----------
def fetch_live(aid):
    u = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{CAFE_ID}/articles/{aid}?_={int(time.time())}'
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20))
    art = (d.get('result') or {}).get('article') or {}
    if not art.get('contentHtml'): raise RuntimeError(f'글 {aid} 본문을 못 읽음')
    return (art.get('subject') or '').strip(), art['contentHtml']

def components(html):
    """[('image', src), ('text', [문단…]), …] — se-viewer HTML을 덩어리 순서대로."""
    out = []
    for p in re.split(r'(?=<div class="se-component se-)', html)[1:]:
        k = re.match(r'<div class="se-component se-([\w-]+)', p).group(1)
        if k == 'image':
            m = re.search(r'<img src="([^"?]+)', p)
            out.append(('image', m.group(1) if m else ''))
        elif k == 'text':
            paras = [_html.unescape(re.sub(r'<[^>]+>', '', x)).strip(ZW + ' \n\t')
                     for x in re.findall(r'<p class="se-text-paragraph[^>]*>(.*?)</p>', p, re.S)]
            out.append(('text', paras))
        else:
            out.append((k, ''))
    return out

# ---------- 계획(브라우저 없이) ----------
def plan(aid, txt_path, subject, html):
    comps = components(html)
    texts = [c[1] for c in comps if c[0] == 'text']
    others = [c[0] for c in comps if c[0] not in ('text', 'image')]
    if others: raise ValueError(f'글/사진 말고 다른 덩어리({others})가 있다 — 이 도구는 글·사진만 다룬다')
    if not texts: raise ValueError('글 덩어리가 없다')
    raw = open(txt_path, encoding='utf-8').read()
    if 'coupang' in raw.lower(): raise ValueError('쿠팡 링크가 든 원고는 네이버 무인 경로로 안 올린다(coupang-policy.md 6)')
    lines = [l.rstrip() for l in raw.strip().splitlines()]
    if lines and norm(lines[0]) == norm(subject): lines = lines[1:]      # 원고 첫 줄이 제목이면 뺀다(제목은 안 바꾼다)
    # 닻: 둘째 덩어리부터 각 덩어리 첫 글 문단이 새 원고에 같은 줄로 있어야 한다
    cuts = [0]
    for i, paras in enumerate(texts[1:], 1):
        head = next((p for p in paras if norm(p)), '')
        hit = [j for j, l in enumerate(lines) if j > cuts[-1] and norm(l) == norm(head)]
        if not head or not hit:
            raise ValueError(f'{i + 1}번째 글 덩어리 첫 줄 "{head[:30]}"이 새 원고에 그대로 없다 — 사진 자리를 못 정한다(소제목은 바꾸지 않는다)')
        cuts.append(hit[0])
    cuts.append(len(lines))
    blocks = []
    for a, b in zip(cuts, cuts[1:]):
        blk = lines[a:b]
        while blk and not blk[0].strip(): blk.pop(0)
        while blk and not blk[-1].strip(): blk.pop()
        tidy = []
        for l in blk:                                    # 빈 줄은 한 줄만
            if l.strip() or (tidy and tidy[-1].strip()): tidy.append(l)
        blocks.append(tidy)
    old_all = '\n'.join(p for t in texts for p in t)
    new_all = '\n'.join(l for b in blocks for l in b)
    if not norm(new_all): raise ValueError('새 원고가 비었다')
    no, nn = nums(old_all), nums(new_all)
    if no != nn:
        raise ValueError(f'숫자가 다르다 — 빠짐 {dict(no - nn)} · 새로 생김 {dict(nn - no)}')
    if '##' in new_all: raise ValueError("'##' 마크다운이 남아 있다")
    return {'aid': int(aid), 'subject': subject, 'images': [c[1] for c in comps if c[0] == 'image'],
            'layout': [c[0] for c in comps], 'old': texts, 'blocks': blocks,
            'sha_txt': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
            'sha_live': hashlib.sha256(html.encode('utf-8')).hexdigest(),
            'old_chars': len(norm(old_all)), 'new_chars': len(norm(new_all)), 'numbers': sum(nn.values())}

def preview(p):
    L = [f'# 카페 {p["aid"]} 수정 대조 (dry)', '', f'- 제목(안 바꿈): {p["subject"]}',
         f'- 덩어리: {" · ".join(p["layout"])} — 사진 {len(p["images"])}장은 그대로',
         f'- 글자 {p["old_chars"]} → {p["new_chars"]} · 숫자 {p["numbers"]}개 전후 동일', '']
    ti = ii = 0
    for k in p['layout']:
        if k == 'image':
            ii += 1; L.append(f'[사진 {ii} 그대로: {p["images"][ii - 1].rsplit("/", 1)[-1]}]'); L.append(''); continue
        L.append(f'## 글 덩어리 {ti + 1}'); L.append('**지금**'); L += ['> ' + x for x in p['old'][ti] if x.strip()]
        L.append('**바꿀 글**'); L += ['> ' + x for x in p['blocks'][ti] if x.strip()]; L.append(''); ti += 1
    return '\n'.join(L)

# ---------- 상한·통과 표시 ----------
def edits_today(day=None):
    day = day or datetime.date.today().isoformat()
    try: rows = [json.loads(l) for l in open(LOG, encoding='utf-8') if l.strip()]
    except FileNotFoundError: return 0
    return sum(1 for r in rows if r.get('applied') and r.get('at', '').startswith(day))

def ok_path(txt): return txt + '.editor_ok'

def mark_ok(txt, who):
    sha = hashlib.sha256(open(txt, encoding='utf-8').read().encode('utf-8')).hexdigest()
    json.dump({'sha': sha, 'by': who, 'at': datetime.datetime.now().isoformat(timespec='seconds')},
              open(ok_path(txt), 'w', encoding='utf-8'), ensure_ascii=False)
    return sha

def check_ok(txt, sha):
    try: d = json.load(open(ok_path(txt), encoding='utf-8'))
    except FileNotFoundError: return False, 'editor 통과 표시가 없다 — editor가 대조표를 보고 edit-ok 를 돌려야 한다'
    if d.get('sha') != sha: return False, '통과 표시 뒤 원고가 바뀌었다 — 다시 확인받는다'
    return True, f'통과 {d.get("by")} {d.get("at")}'

def log(row):
    os.makedirs(OUT, exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(json.dumps(row, ensure_ascii=False) + '\n')

def backup(aid, subject, html):
    d = os.path.join(OUT, str(aid)); os.makedirs(d, exist_ok=True)
    ts = time.strftime('%Y%m%d-%H%M%S')
    path = os.path.join(d, f'{ts}_before.html')
    open(path, 'w', encoding='utf-8').write(html)
    json.dump({'aid': aid, 'subject': subject, 'at': ts}, open(path[:-5] + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
    # 되읽기 대조: 저장한 파일을 다시 읽어 받은 것과 같은지
    if open(path, encoding='utf-8').read() != html: raise RuntimeError('백업 되읽기 불일치')
    return path

# ---------- 적용 뒤 대조 ----------
def compare_after(p, html_after):
    comps = components(html_after)
    imgs = [c[1] for c in comps if c[0] == 'image']
    texts = [c[1] for c in comps if c[0] == 'text']
    bad = []
    if [c[0] for c in comps] != p['layout']: bad.append(f'덩어리 순서 달라짐 {[c[0] for c in comps]}')
    if imgs != p['images']: bad.append('사진 주소가 달라졌다')
    for i, (got, want) in enumerate(zip(texts, p['blocks'])):
        if norm(''.join(got)) != norm(''.join(want)): bad.append(f'글 덩어리 {i + 1} 불일치')
    return bad

# ---------- 브라우저(적용 때만) ----------
def _replace_block(page, frame, i, lines):
    comp = frame.locator('.se-component.se-text').nth(i)
    paras = comp.locator('.se-text-paragraph')
    first, last = paras.first, paras.last
    first.evaluate("e => e.scrollIntoView({block: 'center'})"); page.wait_for_timeout(200)
    a = first.bounding_box()
    last.evaluate("e => e.scrollIntoView({block: 'center'})"); page.wait_for_timeout(200)
    b = last.bounding_box()
    page.mouse.click(b['x'] + b['width'] - 2, b['y'] + b['height'] - 3); page.keyboard.press('End')
    first.evaluate("e => e.scrollIntoView({block: 'center'})"); page.wait_for_timeout(200)
    a = first.bounding_box()
    page.keyboard.down('Shift'); page.mouse.click(a['x'] + 1, a['y'] + 3); page.keyboard.press('Home'); page.keyboard.up('Shift')
    page.wait_for_timeout(200); page.keyboard.press('Backspace'); page.wait_for_timeout(400)
    for j, l in enumerate(lines):
        if l.strip(): page.keyboard.insert_text(l.strip())
        if j < len(lines) - 1: page.keyboard.press('Enter')
        page.wait_for_timeout(100)
    got = comp.evaluate("e => [...e.querySelectorAll('.se-text-paragraph')].map(p=>p.innerText).join('')")
    if norm(got) != norm(''.join(lines)):
        raise RuntimeError(f'글 덩어리 {i + 1} 편집기 안 대조 실패({len(norm(got))}/{len(norm("".join(lines)))}자) — 등록하지 않는다')

def apply_browser(p):
    import naverpost as N
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        ctx = N.launch(pw, headless=os.environ.get('NAVER_HEADED') != '1'); page = ctx.new_page()
        try:
            if not N.logged_in(page): raise RuntimeError('로그인 안 됨 — py -3.12 work/naverpost.py login')
            edit = N.open_cafe_edit(page, p['aid']); frame = edit.main_frame
            if not frame.locator('.se-component').count(): raise RuntimeError('새 편집기가 아님(구 편집기 글은 미지원)')
            n_img = frame.locator('.se-component.se-image').count()
            n_txt = frame.locator('.se-component.se-text').count()
            if n_img != len(p['images']) or n_txt != len(p['blocks']):
                raise RuntimeError(f'편집기 덩어리 수가 글과 다르다(사진 {n_img}/{len(p["images"])}, 글 {n_txt}/{len(p["blocks"])})')
            for i, lines in enumerate(p['blocks']): _replace_block(edit, frame, i, lines)
            if frame.locator('.se-component.se-image').count() != n_img: raise RuntimeError('편집 중 사진 수가 바뀌었다 — 등록하지 않는다')
            N.shot(edit, f'cafe_edit_{p["aid"]}')
            if not N.set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
            return N.submit_cafe(edit)
        finally:
            try: ctx.close()
            except Exception: pass

# ---------- 명령 ----------
def cli(args):
    if args and args[0] == 'ok':                      # edit-ok <txt> <who>
        txt, who = os.path.abspath(args[1]), (args[2] if len(args) > 2 else 'firemap-editor')
        print('통과 표시:', mark_ok(txt, who)[:12], who); return 0
    aid, txt = int(args[0]), os.path.abspath(args[1])
    apply = '--apply' in args
    subject, html = fetch_live(aid)
    bk = backup(aid, subject, html)
    p = plan(aid, txt, subject, html)
    d = os.path.dirname(bk)
    json.dump(p, open(os.path.join(d, 'plan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    pv = os.path.join(d, 'preview.md'); open(pv, 'w', encoding='utf-8').write(preview(p))
    print(f'원본 백업 {bk}\n대조표 {pv}\n덩어리 {"·".join(p["layout"])} · 글자 {p["old_chars"]}→{p["new_chars"]} · 숫자 {p["numbers"]}개 동일')
    if not apply:
        log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'txt': txt, 'applied': False, 'dry': True})
        print('dry — 적용하지 않았다. editor 확인 뒤 --apply'); return 0
    import naverpost as N
    sf = N.stop_flag('cafe')
    if sf: print('감사 정지 스위치 —', sf[:120]); return 2
    ok, why = check_ok(txt, p['sha_txt'])
    if not ok: print('적용 안 함:', why); return 4
    n = edits_today()
    if n >= EDIT_CAP: print(f'오늘 이미 {n}편 고쳤다 — 하루 {EDIT_CAP}편까지'); return 5
    url = apply_browser(p)
    bad = ['읽기 실패']
    for _ in range(4):
        time.sleep(8)
        try: bad = compare_after(p, fetch_live(aid)[1])
        except Exception as e: bad = [repr(e)[:80]]
        if not bad: break
    log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'txt': txt, 'applied': True,
         'ok': not bad, 'bad': bad, 'backup': bk, 'url': url})
    if bad: print('저장 뒤 대조 실패:', bad, '— 원본', bk); return 3
    print('저장 확인: 사진 주소·자리 그대로, 글 덩어리 전부 새 원고와 일치', url); return 0

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(cli(sys.argv[1:]))
