# 이미 공개된 카페 글의 본문 글자만 고친다(2026-10-01, editor 요청 · 순돌이 지시).
# 편집 전수 점검(work/research/editor/sweep.md)의 유일한 적용 길이다. 새 글 발행 경로(naverpost.py cafe)는 건드리지 않는다.
#
#   py -3.12 work/naverpost.py edit 44 work/research/editor/2026-10-01/cafe/44.txt          # dry(기본): 원본 백업 + 대조표, 브라우저 안 씀
#   py -3.12 work/naverpost.py edit-ok work/research/editor/2026-10-01/cafe/44.txt firemap-editor   # editor가 대조표를 보고 통과 표시
#   py -3.12 work/naverpost.py edit 44 work/research/editor/2026-10-01/cafe/44.txt --apply  # 적용(통과 표시 + 하루 상한 + STOP 확인)
#
# 사진 교체(2026-10-05 추가): 글은 그대로 두고 그림만 같은 자리에서 바꾼다.
#   py -3.12 work/naverpost.py editimg 193 work/research/editor/2026-10-03/cafe/193/img          # dry: 어느 사진이 어느 파일로 바뀌는지 대조표(브라우저·카페 수정 없음)
#   py -3.12 work/naverpost.py edit-ok work/research/editor/2026-10-03/cafe/193/img/01.png firemap-editor   # (파일마다) 통과 표시 - 사진 파일 해시로 도장
#   py -3.12 work/naverpost.py editimg 193 <img폴더> --apply                                    # 적용(통과 표시 + 하루 상한 + STOP 확인)
# - 짝 맞추기: 폴더의 파일 이름(01.png)이 카페 글 속 사진 주소 끝 이름과 같은 것끼리. 짝 없는 파일/같은 이름 사진이 둘이면 거절.
# - 글·사진 순서·사진 수는 안 바뀐다. 적용 뒤 글 API를 다시 읽어 바뀐 자리 주소만 달라졌는지, 나머지 사진·글 전부 그대로인지 대조한다.
# - 적용 길(편집기에서 새 사진을 앞 글 덩어리 끝에 넣고 옛 사진 덩어리 지우기)은 2026-10-05 현재 실제 편집기에서 시험 못 했다(dry만 검증).
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
    # 링크 카드(oglink)는 사진처럼 제자리에 둔다 — 글 덩어리만 nth로 갈아 끼우므로 건드리지 않는다(2026-10-02 write, 카페 189).
    others = [c[0] for c in comps if c[0] not in ('text', 'image', 'oglink')]
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
        if head and not hit:
            # 첫 문단이 소제목이 아니라 본문 문장이면 editor가 어미만 고친다(카페 187, 2026-10-02).
            # 앞 15글자가 같은 줄이 남은 원고에 하나뿐이면 그 줄을 닻으로 쓴다.
            k = norm(head)[:15]
            pre = [j for j, l in enumerate(lines) if j > cuts[-1] and len(k) >= 10 and norm(l).startswith(k)]
            if len(pre) == 1: hit = pre
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
        if k != 'text': L.append(f'[{k} 그대로]'); L.append(''); continue
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

# ---------- 사진 교체(2026-10-05) ----------
PNG = b'\x89PNG\r\n\x1a\n'

def img_info(data):
    if data[:8] == PNG: return 'png', int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
    if data[:2] == b'\xff\xd8':
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF: i += 1; continue
            m = data[i + 1]
            if m in (0xC0, 0xC1, 0xC2): return 'jpg', int.from_bytes(data[i + 7:i + 9], 'big'), int.from_bytes(data[i + 5:i + 7], 'big')
            i += 2 + int.from_bytes(data[i + 2:i + 4], 'big')
    raise ValueError('png/jpg가 아니다')

def fetch_bytes(url):
    return urllib.request.urlopen(urllib.request.Request(url.split('?')[0], headers=UA), timeout=20).read()

def plan_img(aid, imgdir, html, fetch_old=True):
    comps = components(html)
    live = [(i, c[1]) for i, c in enumerate(comps) if c[0] == 'image']
    files = sorted(f for f in os.listdir(imgdir) if re.search(r'\.(png|jpe?g)$', f, re.I))
    if not files: raise ValueError(f'{imgdir}에 사진 파일이 없다')
    swaps = []
    for f in files:
        hit = [(i, u) for i, u in live if u.rsplit('/', 1)[-1] == f]
        if len(hit) != 1: raise ValueError(f'사진 파일 {f}: 카페 글에서 같은 이름 사진이 {len(hit)}개다 - 자리를 못 정한다')
        i, u = hit[0]
        data = open(os.path.join(imgdir, f), 'rb').read()
        kind, w, h = img_info(data)
        if w < 600: raise ValueError(f'{f}: 가로 {w}px - 600px 미만은 거절')
        row = {'file': f, 'comp': i, 'img_no': [x for x, _ in live].index(i), 'old_url': u, 'new_w': w, 'new_h': h,
               'new_sha': hashlib.sha256(data).hexdigest(), 'new_bytes': len(data)}
        if fetch_old:
            try:
                od = fetch_bytes(u); _, ow, oh = img_info(od)
                row.update(old_w=ow, old_h=oh, old_sha=hashlib.sha256(od).hexdigest())
                if row['old_sha'] == row['new_sha']: row['same_as_live'] = True
                if abs(w / h - ow / oh) > 0.35 * (ow / oh): row['ratio_warn'] = f'가로세로 비 {ow / oh:.2f}→{w / h:.2f}'
            except Exception as e: row['old_note'] = '옛 사진 못 읽음 ' + repr(e)[:60]
        swaps.append(row)
    return {'aid': int(aid), 'layout': [c[0] for c in comps], 'images': [u for _, u in live],
            'texts': [c[1] for c in comps if c[0] == 'text'], 'swaps': swaps,
            'sha_live': hashlib.sha256(html.encode('utf-8')).hexdigest()}

def preview_img(subject, p):
    L = [f'# 카페 {p["aid"]} 사진 교체 대조 (dry)', '', f'- 제목·본문 글자: 안 바꿈 ({subject})',
         f'- 덩어리: {" · ".join(p["layout"])} - 사진 {len(p["images"])}장 중 {len(p["swaps"])}장만 교체', '']
    for r in p['swaps']:
        L.append(f'- 사진 {r["img_no"]} (덩어리 {r["comp"]}) {r["file"]}: {r.get("old_w", "?")}x{r.get("old_h", "?")} → {r["new_w"]}x{r["new_h"]} · {r["new_bytes"]}B'
                 + (' · **지금과 같은 그림(바꿀 것 없음)**' if r.get('same_as_live') else '') + (f' · 경고 {r["ratio_warn"]}' if r.get('ratio_warn') else '')
                 + (f' · {r["old_note"]}' if r.get('old_note') else ''))
    return '\n'.join(L)

def ok_img(imgdir, files):
    miss = []
    for f in files:
        path = os.path.join(imgdir, f)
        sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        try: d = json.load(open(ok_path(path), encoding='utf-8'))
        except FileNotFoundError: miss.append(f'{f} 통과 표시 없음'); continue
        if d.get('sha') != sha: miss.append(f'{f} 통과 뒤 파일이 바뀜')
    return (not miss), '; '.join(miss) or '통과'

def mark_ok_img(path, who):
    sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    json.dump({'sha': sha, 'by': who, 'at': datetime.datetime.now().isoformat(timespec='seconds')}, open(ok_path(path), 'w', encoding='utf-8'), ensure_ascii=False)
    return sha

def compare_after_img(p, html_after):
    comps = components(html_after)
    imgs = [c[1] for c in comps if c[0] == 'image']; texts = [c[1] for c in comps if c[0] == 'text']
    bad = []
    if [c[0] for c in comps] != p['layout']: bad.append('덩어리 순서·수 달라짐')
    if len(imgs) != len(p['images']): return bad + ['사진 수 달라짐']
    swapped = {r['img_no'] for r in p['swaps']}
    for i, (new, old) in enumerate(zip(imgs, p['images'])):
        if i in swapped and new == old: bad.append(f'사진 {i} 안 바뀜')
        if i not in swapped and new != old: bad.append(f'사진 {i} 바뀌면 안 되는데 바뀜')
        if new.rsplit('/', 1)[-1] != old.rsplit('/', 1)[-1]: bad.append(f'사진 {i} 파일 이름 달라짐')
    if [norm(''.join(t)) for t in texts] != [norm(''.join(t)) for t in p['texts']]: bad.append('글 덩어리가 달라짐')
    return bad

def apply_browser_img(p, imgdir):
    # 시험 못 한 길(2026-10-05): 옛 사진 바로 앞 글 덩어리 끝에 새 사진을 넣고, 옛 사진 덩어리를 지운다.
    import naverpost as N
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        ctx = N.launch(pw, headless=os.environ.get('NAVER_HEADED') != '1'); page = ctx.new_page()
        try:
            if not N.logged_in(page): raise RuntimeError('로그인 안 됨 - py -3.12 work/naverpost.py login')
            edit = N.open_cafe_edit(page, p['aid']); frame = edit.main_frame
            if frame.locator('.se-component').count() != len(p['layout']): raise RuntimeError('편집기 덩어리 수가 글과 다르다')
            photo = frame.locator('button[data-name="image"]').first
            for r in sorted(p['swaps'], key=lambda r: -r['comp']):          # 뒤에서부터(앞 번호가 안 밀리게)
                before = frame.locator('.se-component.se-image').count()
                prev = frame.locator('.se-component').nth(r['comp'] - 1)
                if 'se-text' not in (prev.get_attribute('class') or ''): raise RuntimeError('옛 사진 바로 앞이 글 덩어리가 아님 - 자리를 못 정한다')
                last = prev.locator('.se-text-paragraph').last
                last.evaluate("e => e.scrollIntoView({block: 'center'})"); edit.wait_for_timeout(200)
                b = last.bounding_box(); edit.mouse.click(b['x'] + b['width'] - 2, b['y'] + b['height'] - 3); edit.keyboard.press('End')
                with edit.expect_file_chooser(timeout=15000) as fc: photo.click()
                fc.value.set_files(os.path.join(imgdir, r['file']))
                for _ in range(40):
                    edit.wait_for_timeout(500)
                    if frame.locator('.se-component.se-image').count() > before: break
                else: raise RuntimeError(f'{r["file"]} 새 사진이 안 들어감')
                edit.wait_for_timeout(800)
                old = frame.locator('.se-component').nth(r['comp'] + 1)            # 새 사진이 앞에 끼었으니 옛 사진은 한 칸 뒤
                if 'se-image' not in (old.get_attribute('class') or ''): raise RuntimeError('옛 사진 자리를 못 찾음 - 등록하지 않는다')
                old.click(); edit.keyboard.press('Delete'); edit.wait_for_timeout(600)
                if frame.locator('.se-component.se-image').count() != before: raise RuntimeError(f'{r["file"]} 교체 뒤 사진 수가 다르다 - 등록하지 않는다')
            N.shot(edit, f'cafe_editimg_{p["aid"]}')
            if not N.set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
            return N.submit_cafe(edit)
        finally:
            try: ctx.close()
            except Exception: pass

def cli_img(args):
    aid, imgdir = int(args[0]), os.path.abspath(args[1]); apply = '--apply' in args
    subject, html = fetch_live(aid)
    bk = backup(aid, subject, html)
    p = plan_img(aid, imgdir, html)
    d = os.path.dirname(bk)
    json.dump(p, open(os.path.join(d, 'plan_img.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    pv = os.path.join(d, 'preview_img.md'); open(pv, 'w', encoding='utf-8').write(preview_img(subject, p))
    print(f'원본 백업 {bk}\n대조표 {pv}\n' + preview_img(subject, p))
    if not apply:
        log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'imgdir': imgdir, 'applied': False, 'dry': True, 'kind': 'img'})
        print('dry - 적용하지 않았다. editor가 사진 파일마다 edit-ok 한 뒤 --apply'); return 0
    import naverpost as N
    sf = N.stop_flag('cafe')
    if sf: print('감사 정지 스위치 -', sf[:120]); return 2
    if any(r.get('same_as_live') for r in p['swaps']): print('지금과 같은 그림이 있다 - 적용 안 함'); return 6
    ok, why = ok_img(imgdir, [r['file'] for r in p['swaps']])
    if not ok: print('적용 안 함:', why); return 4
    n = edits_today()
    if n >= EDIT_CAP: print(f'오늘 이미 {n}편 고쳤다 - 하루 {EDIT_CAP}편까지'); return 5
    url = apply_browser_img(p, imgdir)
    bad = ['읽기 실패']
    for _ in range(4):
        time.sleep(8)
        try: bad = compare_after_img(p, fetch_live(aid)[1])
        except Exception as e: bad = [repr(e)[:80]]
        if not bad: break
    log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'imgdir': imgdir, 'kind': 'img', 'applied': True, 'ok': not bad, 'bad': bad, 'backup': bk, 'url': url})
    if bad: print('저장 뒤 대조 실패:', bad, '- 원본', bk); return 3
    print('저장 확인: 바뀐 자리만 새 사진, 글·나머지 사진 그대로', url); return 0

# ---------- 제목만 바꾸기(2026-10-08) ----------
# 검색어 손질(refactor-candidates.md '판단' #56)은 제목 앞머리만 바꾸면 된다. rewrite(naverpost)는 본문을 묶음으로
# 통째로 다시 넣어 사진 없는 묶음(fintax)이면 올라간 사진이 빠지고, edit(위)는 제목을 안 바꾼다 — write가 10/8 기한을 못 맞춘 이유.
#   py -3.12 work/naverpost.py edittitle 56 work/research/editor/2026-10-08/cafe/56.title.txt          # dry: 지금/바꿀 제목 대조
#   py -3.12 work/naverpost.py edit-ok work/research/editor/2026-10-08/cafe/56.title.txt firemap-editor
#   py -3.12 work/naverpost.py edittitle 56 <같은 파일> --apply                                          # 적용
# - 파일 첫 줄이 새 제목. 숫자 목록이 지금 제목과 같아야 한다(뜻 바꾸기 금지). 본문·사진은 손대지 않고, 저장 뒤 본문 HTML 덩어리가 전과 같은지 대조한다.
def plan_title(aid, txt, subject, html):
    raw = open(txt, encoding='utf-8').read()
    new = (raw.strip().splitlines() or [''])[0].strip()
    if not new: raise ValueError('새 제목이 비었다')
    if len(new) > 100: raise ValueError(f'제목이 너무 길다({len(new)}자)')
    if new == subject: raise ValueError('지금 제목과 같다')
    if nums(new) != nums(subject): raise ValueError(f'숫자가 달라진다 {dict(nums(subject))} → {dict(nums(new))} — 뜻을 바꾸는 제목은 안 고친다')
    comps = components(html)
    return {'aid': aid, 'subject': subject, 'new': new, 'layout': [c[0] for c in comps],
            'body': [c[1] for c in comps], 'sha_txt': hashlib.sha256(raw.encode('utf-8')).hexdigest()}

def apply_browser_title(p):
    import naverpost as N
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        ctx = N.launch(pw, headless=os.environ.get('NAVER_HEADED') != '1'); page = ctx.new_page()
        try:
            if not N.logged_in(page): raise RuntimeError('로그인 안 됨 — py -3.12 work/naverpost.py login')
            edit = N.open_cafe_edit(page, p['aid']); frame = edit.main_frame
            if not frame.locator('.se-component').count(): raise RuntimeError('새 편집기가 아님(구 편집기 글은 미지원)')
            n_img = frame.locator('.se-component.se-image').count()
            tl = edit.locator('textarea[placeholder*="제목"], input[placeholder*="제목"]').first
            if not tl.count(): raise RuntimeError('제목 칸을 못 찾았다')
            before = (tl.input_value() or '').strip()
            if before != p['subject']: raise RuntimeError(f'편집기 제목이 글과 다르다("{before[:30]}")')
            tl.click(); tl.fill(p['new']); edit.wait_for_timeout(300)
            if (tl.input_value() or '').strip() != p['new']: raise RuntimeError('제목 칸에 새 제목이 안 들어갔다 — 등록하지 않는다')
            if frame.locator('.se-component.se-image').count() != n_img: raise RuntimeError('편집 중 사진 수가 바뀌었다 — 등록하지 않는다')
            N.shot(edit, f'cafe_edittitle_{p["aid"]}')
            if not N.set_cafe_public(edit): raise RuntimeError('전체공개 선택 실패')
            return N.submit_cafe(edit)
        finally:
            try: ctx.close()
            except Exception: pass

def cli_title(args):
    aid, txt = int(args[0]), os.path.abspath(args[1]); apply = '--apply' in args
    subject, html = fetch_live(aid)
    bk = backup(aid, subject, html)
    p = plan_title(aid, txt, subject, html)
    pv = os.path.join(os.path.dirname(bk), 'preview_title.md')
    open(pv, 'w', encoding='utf-8').write(f'# 카페 {aid} 제목 바꾸기 대조 (dry)\n\n- 지금: {subject}\n- 바꿀 제목: {p["new"]}\n'
                                          f'- 본문: 안 바꿈 ({" · ".join(p["layout"])})\n- 숫자: {sum(nums(subject).values())}개 전후 동일\n')
    print(f'원본 백업 {bk}\n대조표 {pv}\n지금: {subject}\n바꿈: {p["new"]}')
    if not apply:
        log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'txt': txt, 'kind': 'title', 'applied': False, 'dry': True})
        print('dry — 적용하지 않았다. editor가 edit-ok 한 뒤 --apply'); return 0
    import naverpost as N
    sf = N.stop_flag('cafe')
    if sf: print('감사 정지 스위치 —', sf[:120]); return 2
    ok, why = check_ok(txt, p['sha_txt'])
    if not ok: print('적용 안 함:', why); return 4
    n = edits_today()
    if n >= EDIT_CAP: print(f'오늘 이미 {n}편 고쳤다 — 하루 {EDIT_CAP}편까지'); return 5
    url = apply_browser_title(p)
    bad = ['읽기 실패']
    for _ in range(4):
        time.sleep(8)
        try:
            s2, h2 = fetch_live(aid); c2 = components(h2); bad = []
            if s2 != p['new']: bad.append(f'제목이 안 바뀜("{s2[:30]}")')
            if [c[0] for c in c2] != p['layout'] or [c[1] for c in c2] != p['body']: bad.append('본문 덩어리가 달라졌다')
        except Exception as e: bad = [repr(e)[:80]]
        if not bad: break
    log({'at': datetime.datetime.now().isoformat(timespec='seconds'), 'aid': aid, 'txt': txt, 'kind': 'title', 'applied': True,
         'ok': not bad, 'bad': bad, 'backup': bk, 'url': url, 'from': subject, 'to': p['new']})
    if bad: print('저장 뒤 대조 실패:', bad, '— 원본', bk); return 3
    print('저장 확인: 제목만 바뀜, 본문·사진 그대로', url); return 0

# ---------- 명령 ----------
def cli(args):
    if args and args[0] == 'ok':                      # edit-ok <txt> <who>
        txt, who = os.path.abspath(args[1]), (args[2] if len(args) > 2 else 'firemap-editor')
        if re.search(r'\.(png|jpe?g)$', txt, re.I): print('사진 통과 표시:', mark_ok_img(txt, who)[:12], who); return 0
        print('통과 표시:', mark_ok(txt, who)[:12], who); return 0
    if args and args[0] == 'img': return cli_img(args[1:])
    if args and args[0] == 'title': return cli_title(args[1:])
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
