# 이미 올라간 카페 글에서 잘린 주소 조각만 지우고 빠진 주소 줄을 되살린다(2026-10-15, 사장님 "tps, y, ou 이런 건 왜 적힌 거야").
# 원인과 새 글 쪽 고침은 naverpost.py '주소 줄' 설명. 이 파일은 이미 나간 글 수리 전용이다.
#
#   py -3.12 work/cafe_urlfix.py scan [첫번호 끝번호]     # 브라우저 없이 글 API로 훑는다. 원고(published.txt)와 대조
#   py -3.12 work/cafe_urlfix.py fix <글번호>             # dry: 수정 화면을 열어 고친 문서를 넣어 보고 검사만, 등록 안 함
#   py -3.12 work/cafe_urlfix.py fix <글번호> --apply     # 검사가 다 맞을 때만 등록(수정)
#
# 고치는 법: 편집기가 저장하는 문서(getDocumentData)에서 원고와 다른 문단만 원고대로 맞춘다.
# - 원고와 같은 문단, 사진·카드·첨부 덩어리, 제목, 공개 설정은 그대로 둔다(등록 전·후 비교).
# - 다른 문단은 주소 조각이거나 주소 줄이 옆 줄과 붙은 것이어야 한다. 그 밖의 차이가 하나라도 있으면 고치지 않고 멈춘다.
# - 원본 문서·HTML은 research/_cafe_edit/<글번호>/urlfix_*.json 에 남긴다(되돌리기용).
import os, re, sys, json, time, copy, uuid, difflib, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import naverpost as np

OUT = os.path.join(HERE, 'research', '_cafe_edit')
ZW = '​‌‍﻿'
clean = lambda s: re.sub(r'[\s' + ZW + r']+', '', s or '')
SETTING_KEYS = ('subject', 'isOpen', 'isEnableScrap', 'isEnableExternal', 'isEnableSocialPlugin', 'isWriteComment', 'isNotice')

def fetch(aid):
    u = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{np.CAFE_ID}/articles/{aid}?_={int(time.time())}'
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=np.UA), timeout=20))['result']

def settings(res):
    a = res.get('article') or {}
    s = {k: a.get(k) for k in SETTING_KEYS}
    s['menu'] = (a.get('menu') or {}).get('id')
    s['attaches'] = len(res.get('attaches') or [])
    s['tags'] = [t.get('name') if isinstance(t, dict) else t for t in (res.get('tags') or [])]
    s['components'] = blocks_html(a.get('contentHtml', ''))
    return s

def blocks_html(h):
    """글이 아닌 덩어리 순서와 사진 주소(바뀌면 안 된다)."""
    out = []
    for p in re.split(r'(?=<div class="se-component se-)', h or '')[1:]:
        k = re.match(r'<div class="se-component se-([\w-]+)', p).group(1)
        if k == 'text': continue
        m = re.search(r'<img src="([^"?]+)', p) if k == 'image' else None
        out.append(k + (':' + m.group(1) if m else ''))
    return out

def pkg_map():
    import glob
    pk = {}
    for f in glob.glob(os.path.join(HERE, 'research', '**', 'published.txt'), recursive=True):
        for m in re.finditer(r'cafe\.naver\.com/firemap/(\d+)', open(f, encoding='utf-8').read()):
            pk.setdefault(int(m.group(1)), os.path.dirname(f))
    return pk

def want_lines(seq):
    return [np.HEAD_RE.sub('', l).strip() for k, v in seq if k == 'text' for l in (v or '').splitlines() if clean(l)]

def scan(lo, hi):
    pk = pkg_map(); bad = []
    for aid in range(lo, hi + 1):
        try: res = fetch(aid)
        except Exception: continue
        h = (res.get('article') or {}).get('contentHtml') or ''
        paras = np.html_paras(h)
        if aid in pk:
            try: _t, seq, _m = np.read_pkg(pk[aid])
            except Exception as e: seq = None; print(aid, '원고 못 읽음', repr(e)[:60])
        else: seq = None
        if seq is None:
            probs = [f'잘린 링크 "{a[:20]}"' for t, l in paras for u, a in l if a != u]
        else:
            probs = np.url_problems(paras, seq)
        if probs:
            bad.append(aid); print(aid, len(probs), '·', ' / '.join(probs[:4]))
        time.sleep(0.25)
    print('주소 깨진 글:', bad or '없음')
    return bad

# ---------- 문서 고치기(브라우저 없이 계산) ----------
def _nid(): return 'SE-' + str(uuid.uuid4())

def _ptext(p): return ''.join(n.get('value', '') for n in p.get('nodes', []))

def _slice(nodes, rs, re_):
    out, off = [], 0
    for n in nodes:
        v = n.get('value', ''); a, b = off, off + len(v); off = b
        s, e = max(a, rs), min(b, re_)
        if s >= e: continue
        m = copy.deepcopy(n); m['value'] = v[s - a:e - a]; m['id'] = _nid()
        if m.get('link') and m['value'] != m['link'].get('url'): m.pop('link')   # 주소가 아닌 글에 붙은 링크는 뗀다('ht헬리오시티…')
        out.append(m)
    return out

def _fresh(raw):
    nodes, pos = [], 0
    for m in np.URL_RE.finditer(raw):
        if m.start() > pos: nodes.append({'id': _nid(), 'value': raw[pos:m.start()], '@ctype': 'textNode'})
        nodes.append({'id': _nid(), 'value': m.group(0), 'link': {'url': m.group(0), '@ctype': 'urlLink'}, '@ctype': 'textNode'})
        pos = m.end()
    if pos < len(raw): nodes.append({'id': _nid(), 'value': raw[pos:], '@ctype': 'textNode'})
    return nodes

def _find(raw_para, want_raw):
    """원고 한 줄이 문단 안 어디에 있나(공백 무시) → 원래 글자 위치 (시작, 끝) 또는 None."""
    idx = [i for i, ch in enumerate(raw_para) if not (ch.isspace() or ch in ZW)]
    c = ''.join(raw_para[i] for i in idx); w = clean(want_raw)
    k = c.find(w) if w else -1
    if k < 0: return None
    return idx[k], idx[k + len(w) - 1] + 1

def plan_fix(doc, seq):
    """편집기 문서(getDocumentData 결과)와 원고 → (고친 문서, 바뀐 것 목록). 고칠 수 없으면 ValueError."""
    doc = copy.deepcopy(doc); comps = doc['document']['components']
    refs = [(ci, pi) for ci, c in enumerate(comps) if c.get('@ctype') == 'text' for pi, _ in enumerate(c.get('value', []))]
    para = lambda r: comps[r[0]]['value'][r[1]]
    ne = [r for r in refs if clean(_ptext(para(r)))]
    got = [clean(_ptext(para(r))) for r in ne]
    wraw = want_lines(seq); want = [clean(l) for l in wraw]
    url_lines = [w for w in want if np.URL_RE.search(w)]
    sm = difflib.SequenceMatcher(None, want, got, autojunk=False)
    placed = {}                    # 원고 줄 번호 → 놓인 자리(문단 ref)
    out_at = {}                    # 문단 ref → 그 자리에 들어갈 새 문단들(None이면 그대로)
    after = {}                     # 문단 ref → 그 뒤에 끼울 새 문단들
    changes = []
    template = copy.deepcopy(para(ne[0])) if ne else None
    def newp(nodes):
        p = copy.deepcopy(template); p['id'] = _nid(); p['nodes'] = nodes; return p
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1): placed[i1 + k] = ne[j1 + k]
            continue
        slots = [ne[j] for j in range(j1, j2)]
        for r in slots: out_at[r] = []
        for w in range(i1, i2):
            hit = None
            for r in slots:
                f = _find(_ptext(para(r)), wraw[w])
                if f: hit = (r, f); break
            if hit:
                r, (s, e) = hit
                out_at[r].append(newp(_slice(para(r)['nodes'], s, e))); placed[w] = r
                changes.append(f'고침 "{_ptext(para(r))[:40]}" → "{wraw[w][:40]}"')
            else:
                if w == 0 or (w - 1) not in placed: raise ValueError(f'"{wraw[w][:30]}" 넣을 자리를 못 찾음')
                if not np.URL_RE.search(wraw[w]): raise ValueError(f'주소 없는 줄 "{wraw[w][:30]}"이 빠져 있다 — 주소 조각 문제가 아니다')
                anchor = placed[w - 1]
                (out_at[anchor] if anchor in out_at else after.setdefault(anchor, [])).append(newp(_fresh(wraw[w])))
                placed[w] = anchor
                changes.append(f'되살림 "{wraw[w][:50]}"')
        for r in slots:
            if not out_at[r]:
                t = clean(_ptext(para(r)))
                if not any(t in u for u in url_lines):   # 지우는 문단은 원고 주소 줄의 한 토막이어야 한다('htt', '/rVg0pQVo_wk', '산기: https://…')
                    raise ValueError(f'지울 문단 "{_ptext(para(r))[:30]}"이 주소 조각이 아니다')
                changes.append(f'지움 "{_ptext(para(r))[:40]}"')
    # 실제로 다시 쌓는다
    empty_tpl = None
    for c in comps:
        if c.get('@ctype') == 'text':
            for p in c['value']:
                if not clean(_ptext(p)): empty_tpl = p; break
        if empty_tpl: break
    for ci, c in enumerate(comps):
        if c.get('@ctype') != 'text': continue
        new = []
        for pi, p in enumerate(c['value']):
            r = (ci, pi)
            new.extend(out_at[r] if r in out_at else [p])
            new.extend(after.get(r, []))
        if not new:
            e = copy.deepcopy(empty_tpl or p); e['id'] = _nid()
            if not empty_tpl: e['nodes'] = [{'id': _nid(), 'value': '', '@ctype': 'textNode'}]
            new = [e]
        c['value'] = new
    return doc, changes

def doc_paras(doc):
    return [(_ptext(p), [(n['link']['url'], n.get('value', '')) for n in p.get('nodes', []) if n.get('link')])
            for c in doc['document']['components'] if c.get('@ctype') == 'text' for p in c.get('value', [])]

def doc_blocks(doc):
    return [json.dumps(c, sort_keys=True, ensure_ascii=False) for c in doc['document']['components'] if c.get('@ctype') != 'text']

def check_doc(doc, seq, orig=None):
    """고친 문서가 원고와 문단 단위로 같고, 주소 검사를 통과하고, 글 아닌 덩어리는 그대로인가."""
    got = [clean(t) for t, _ in doc_paras(doc) if clean(t)]
    want = [clean(l) for l in want_lines(seq)]
    probs = []
    if got != want:
        d = [x for x in difflib.unified_diff(want, got, lineterm='', n=0) if not x.startswith(('---', '+++', '@@'))]
        probs.append('원고와 다른 문단: ' + ' | '.join(x[:50] for x in d[:6]))
    probs += np.url_problems(doc_paras(doc), seq)
    if orig is not None and doc_blocks(doc) != doc_blocks(orig): probs.append('사진·카드 덩어리가 바뀜')
    return probs

# ---------- 브라우저 ----------
GET_DOC = f"() => {{ const ed = {np.EDITOR_JS}; return ed ? ed.getDocumentData() : null; }}"
SET_DOC = f"(d) => {{ const ed = {np.EDITOR_JS}; ed.setDocumentData(d); return true; }}"

def fix(aid, apply=False):
    pk = pkg_map()
    if aid not in pk: raise SystemExit(f'{aid}: 원고(published.txt)를 못 찾음')
    _t, seq, meta = np.read_pkg(pk[aid])
    before = fetch(aid); s0 = settings(before)
    live_probs = np.url_problems(np.html_paras(before['article']['contentHtml']), seq)
    if not live_probs: print(f'{aid}: 이미 멀쩡하다 — 할 일 없음'); return True
    os.makedirs(os.path.join(OUT, str(aid)), exist_ok=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    json.dump(before, open(os.path.join(OUT, str(aid), f'urlfix_{stamp}_api.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = np.launch(p, headless=os.environ.get('NAVER_HEADED') != '1')
        page = ctx.new_page()
        try:
            if not np.logged_in(page): print('LOGIN_LOST — 로그인이 풀렸다. 비밀번호는 사람이 넣는다'); return False
            edit = np.open_cafe_edit(page, aid)
            edit.on('dialog', lambda d: d.accept())
            frame = edit.main_frame
            for _ in range(40):
                if frame.evaluate(GET_DOC): break
                edit.wait_for_timeout(500)
            orig = frame.evaluate(GET_DOC)
            if not orig: raise RuntimeError('편집기 문서를 못 읽음(구 편집기 글?)')
            json.dump(orig, open(os.path.join(OUT, str(aid), f'urlfix_{stamp}_doc.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            vis = edit.evaluate("() => { const a=document.querySelector('input#all[name=public], input[name=public][value=\"true\"]'); return a ? a.checked : null; }")
            title0 = (edit.locator('textarea[placeholder*="제목"], input[placeholder*="제목"]').first.input_value() or '').strip()
            new, changes = plan_fix(orig, seq)
            for c in changes: print('  ', c)
            probs = check_doc(new, seq, orig)
            if probs: raise RuntimeError('고친 문서 검사 실패: ' + ' / '.join(probs[:5]))
            frame.evaluate(SET_DOC, new); edit.wait_for_timeout(1500)
            for _ in range(40):
                if not np._editor_busy(frame): break
                edit.wait_for_timeout(500)
            back = frame.evaluate(GET_DOC)
            probs = check_doc(back, seq, orig)
            dom = frame.evaluate("() => [...document.querySelectorAll('.se-component.se-text .se-text-paragraph')].map(p => [p.innerText, [...p.querySelectorAll('a[href]')].map(a => [a.getAttribute('href'), a.innerText])])")
            got_dom = [clean(t) for t, _ in dom if clean(t)]
            if got_dom != [clean(l) for l in want_lines(seq)]: probs.append('화면 글이 원고와 다름')
            title1 = (edit.locator('textarea[placeholder*="제목"], input[placeholder*="제목"]').first.input_value() or '').strip()
            if title1 != title0: probs.append('제목이 바뀜')
            vis1 = edit.evaluate("() => { const a=document.querySelector('input#all[name=public], input[name=public][value=\"true\"]'); return a ? a.checked : null; }")
            if vis1 != vis: probs.append('공개 설정이 바뀜')
            np.shot(edit, f'cafe_urlfix_{aid}')
            if probs: raise RuntimeError('넣은 뒤 검사 실패: ' + ' / '.join(probs[:5]))
            print(f'{aid}: 편집기 검사 통과(바뀐 문단 {len(changes)}곳, 전체공개={vis})')
            if not apply:
                print(f'{aid}: dry — 등록하지 않고 닫는다'); return True
            url = np.submit_cafe(edit, None, members=(vis is False))
            print('수정 등록:', url)
        finally:
            try: ctx.close()
            except Exception: pass
    for i in range(5):
        time.sleep(6)
        after = fetch(aid); s1 = settings(after)
        probs = np.url_problems(np.html_paras(after['article']['contentHtml']), seq)
        got = [clean(t) for t, _ in np.html_paras(after['article']['contentHtml']) if clean(t)]
        same_text = got == [clean(l) for l in want_lines(seq)]
        if not probs and same_text: break
    diff = {k: (s0[k], s1[k]) for k in s0 if s0[k] != s1[k]}
    ok = not probs and same_text and not diff
    print(f'{aid}: 고친 뒤 글 API — 주소 문제 {len(probs)}곳, 원고와 문단 일치 {same_text}, 설정 변화 {diff or "없음"} → {"OK" if ok else "확인 필요"}')
    with open(os.path.join(OUT, 'urlfix_log.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps({'at': time.strftime('%Y-%m-%d %H:%M'), 'aid': aid, 'ok': ok, 'changes': changes, 'left': probs, 'settings_diff': diff}, ensure_ascii=False) + '\n')
    return ok

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('scan', 'fix'): print(__doc__ or open(__file__, encoding='utf-8').read()[:900]); sys.exit(1)
    if a[0] == 'scan':
        lo, hi = (int(a[1]), int(a[2])) if len(a) >= 3 else (90, 400)
        sys.exit(1 if scan(lo, hi) else 0)
    sys.exit(0 if fix(int(a[1]), '--apply' in a) else 1)
