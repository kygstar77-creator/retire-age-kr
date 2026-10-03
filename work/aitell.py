# AI 티 자동 검사 — 글이 기계로 찍은 것처럼 읽히는 신호를 점수로 낸다(2026-10-01).
#   py -3.12 work/aitell.py <묶음 폴더|텍스트 파일>          → 점수와 걸린 곳
#   py -3.12 work/aitell.py text "<문장>"                    → 짧은 글(제목·설명·댓글)
#   py -3.12 work/aitell.py gate <묶음>                      → 기준 넘고 편집 통과 표시 없으면 종료코드 4
#   py -3.12 work/aitell.py pass <묶음> <편집자>             → 편집 통과 표시(editor_ok.txt)를 남긴다
#   py -3.12 work/aitell.py scan <묶음 폴더 여러 개>         → 기준 조정용 분포
#   py -3.12 work/aitell.py frame <묶음>                     → 카페 틀 v2 3줄 점검(소제목 3~5개·끝 FAQ/정리·제목 명사 끝 또는 B틀 물음, 반전 금지). 어기면 종료코드 5
#   py -3.12 work/aitell.py commaday 2026-10-04               → 그 날 카페 칸 쉼표 없는 제목 수(하루 2편 이상, 10/4 칸부터 frame이 쉼표 제목을 막는다)
#   py -3.12 work/aitell.py --script <voice.json|script.md|txt>  → 롱폼 대본 말투(숫자 밀도·숫자 2개 이상 문장). 넘으면 종료코드 6
#        근거: research/editor/script-gate.md (경쟁 사람 자막 12편 vs 우리 대본 4편, 10/3 클라우드 ①)
#   --skip-list (아무 자리)  → 번호·글머리 목록 줄과 법 문구·면책 줄을 끝맺음 반복(연속·'~요'·머리·꼬리)에서 뺀다.
#                              사전(AI 말·설명조) 검사는 그대로. 기본은 꺼짐 — 기존 통과 점수가 안 바뀐다(10/1 대역 X-KR-1 요청).
# 사장님 10/1 "사소한 것까지 모든 글을 다 검토해서 사람이 쓴 글로 바꿔야 하는데" — 순돌이 지시 [지시·긴급].
# 재는 것: ① 사전(work/aitell_dict.json — 한·영 AI 티 말, 과한 설명조, 맺음 틀) ② 같은 끝맺음 연속
#          ③ 같은 틀 반복(문장 머리 두 어절·문장 꼬리 두 어절이 세 번 넘게) ④ 문단 맺음 틀 반복.
# 발행기(naverpost.py·cafeapi.py·ytupload.py·f2_coupang.py)가 올리기 전에 gate를 부른다.
# 편집 통과 표시는 표시 뒤에 원고가 바뀌면 무효다 — 고친 뒤 편집자가 다시 봐야 한다.
import sys, os, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = json.load(open(os.path.join(HERE, 'aitell_dict.json'), encoding='utf-8'))
KO_TELLS, KO_EXPLAIN, KO_CLOSING, EN_TELLS = DICT['ko'], DICT['ko_explain'], DICT['ko_closing'], DICT['en']
LIMIT = 12.0          # 1,000자당 점수. 10/1 scan: 최근 묶음 59개 중앙 0·상위 25% 5.2 → 12를 넘는 건 5개('~요' 70%대·7문장 넘게 연속)
LIMIT_SHORT = 6.0     # 300자 미만(제목·설명·댓글)은 원점수로 본다.
OK_FILE = 'editor_ok.txt'


def sentences(text):
    text = re.sub(r'^\s*[|#>*-]+\s*', '', text, flags=re.M)
    parts = re.split(r'(?<=[.?!])\s+|\n+', text)
    return [p.strip() for p in parts if len(re.sub(r'[^가-힣A-Za-z]', '', p)) >= 4]


def end_kind(s):
    """문장 끝 두 음절(예: 어요·예요·있다·였다). 평어체 글은 거의 다 '다'로 끝나서 한 글자로는 틀 반복을 못 본다."""
    tail = re.sub(r'[^가-힣]', '', s)[-2:]
    return tail if len(tail) == 2 and re.search(r'(요|다|죠|까)$', tail) else '기타'



LIST_LINE = re.compile(r'^\s*(\d{1,2}[.)]\s|\(\d{1,2}\)\s|[①-⑳]|[-*•·▪]\s|[가-하][.)]\s)')
LEGAL_LINE = re.compile(r'제\s?\d+\s?조|면책|투자\s?권유|책임지지|책임을 지지|법적 효력|참고용')
SKIP = False
SKIP_MARK = 'BLOCKSKIP'   # 한글 없음 → 끝맺음 '기타'로 잡혀 연속을 끊고, 어절이 하나라 머리·꼬리에도 안 들어간다


def skip_blocks(text):
    """번호 목록·법 문구 줄을 표시 줄로 바꾼다(끝맺음 반복 계산용). 바뀐 줄 수도 돌려준다."""
    out, k = [], 0
    for ln in text.splitlines():
        if ln.strip() and (LIST_LINE.search(ln) or LEGAL_LINE.search(ln)): out.append(SKIP_MARK); k += 1
        else: out.append(ln)
    return '\n'.join(out), k


def score(text, skip_list=False):
    """점수와 걸린 곳 목록. 점수는 1,000자당(짧은 글은 원점수). skip_list면 목록·법 문구 줄은 끝맺음 반복에서 뺀다."""
    if skip_list:
        rtext, k = skip_blocks(text)
        sents = sentences(rtext)
    else:
        sents, k = sentences(text), 0
    hits, pts = [], 0.0
    low = text.lower()
    for w in KO_TELLS:
        c = text.count(w)
        if c: pts += 3 * c; hits.append(f'AI 말 "{w}" ×{c}')
    for w in EN_TELLS:
        c = len(re.findall(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low))
        if c: pts += 3 * c; hits.append(f'AI 말(영) "{w}" ×{c}')
    for w in KO_EXPLAIN:
        c = text.count(w)
        if c: pts += 2 * c; hits.append(f'설명조 "{w}" ×{c}')
    # 문단 맺음 틀: 문단 마지막 문장이 같은 맺음 말로 끝나는 게 두 번 넘으면
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    closes = collections.Counter()
    for p in paras:
        ss = sentences(p)
        if not ss: continue
        for w in KO_CLOSING:
            if w in ss[-1]: closes[w] += 1; break
    for w, c in closes.items():
        if c >= 2: pts += 3 * (c - 1); hits.append(f'문단 맺음 틀 "{w}" ×{c}')
    # 같은 끝맺음 연속
    run, best, prev, at = 1, 1, None, ''
    for s in sents:
        e = end_kind(s)
        run = run + 1 if e == prev and e != '기타' else 1
        if run > best: best, at = run, s
        prev = e
    if best >= 3: pts += 3 * (best - 2); hits.append(f'같은 끝 두 음절 {best}연속 — "…{at[-30:]}"')
    # 해요체 쏠림: '~요'만 다섯 문장 넘게 잇따르거나, 문장 열에 여섯 넘게 '~요'(카페 실측 9/27 '요' 16%, 우리 글 75%)
    # 평어체 '~다'는 블로그 기본 말투라 쏠림으로 치지 않는다(editor style-guide 블로그 기준).
    yo = [s for s in sents if re.search(r'요[.?!]?$', s)]
    run, yrun = 0, 0
    for s in sents:
        run = run + 1 if re.search(r'요[.?!]?$', s) else 0; yrun = max(yrun, run)
    if yrun >= 5: pts += 2 * (yrun - 4); hits.append(f"'~요' {yrun}문장 연속")
    if len(sents) >= 10 and len(yo) / len(sents) > 0.6:
        pts += 10 * (len(yo) / len(sents) - 0.6) * 10 / 2; hits.append(f"'~요' 비율 {round(len(yo) / len(sents) * 100)}% (카페 실측 16%)")
    # 같은 틀 반복: 문장 머리 두 어절 / 꼬리 두 어절
    heads = collections.Counter(' '.join(s.split()[:2]) for s in sents if len(s.split()) >= 4)
    tails = collections.Counter(' '.join(s.split()[-2:]) for s in sents if len(s.split()) >= 4)
    for label, cnt in (('머리', heads), ('꼬리', tails)):
        for k, c in cnt.items():
            if c >= 3 and re.search(r'[가-힣A-Za-z]', k):
                pts += 2 * (c - 2); hits.append(f'같은 문장 {label} "{k}" ×{c}')
    if k: hits.append(f'목록·법 문구 {k}줄은 끝맺음 반복에서 뺌(--skip-list)')
    n = len(re.sub(r'[\s\W_]', '', text))
    val = pts if n < 300 else pts / (n / 1000)
    return round(val, 1), hits, n


def pkg_text(pkg):
    """묶음의 본문(order.txt 순서의 텍스트 조각) + 제목."""
    parts = []
    tp = os.path.join(pkg, 'title.txt')
    if os.path.exists(tp): parts.append(open(tp, encoding='utf-8').read().strip())
    op = os.path.join(pkg, 'order.txt')
    files = []
    if os.path.exists(op):
        for ln in open(op, encoding='utf-8').read().splitlines():
            tok = (ln.strip().split() or [''])[0]
            if tok.endswith('.txt') and os.path.exists(os.path.join(pkg, tok)): files.append(os.path.join(pkg, tok))
    if not files:
        files = sorted(glob.glob(os.path.join(pkg, 'c[0-9]*.txt')) + glob.glob(os.path.join(pkg, 'b[0-9]*.txt')))
    for f in files: parts.append(open(f, encoding='utf-8').read())
    return '\n\n'.join(parts), files


def editor_ok(pkg, files=None):
    """편집 통과 표시가 있고, 표시 뒤에 원고가 안 바뀌었으면 (True, 누가)."""
    p = os.path.join(pkg, OK_FILE)
    if not os.path.exists(p): return False, ''
    files = files if files is not None else pkg_text(pkg)[1]
    t = os.path.getmtime(p)
    newer = [os.path.basename(f) for f in files if os.path.getmtime(f) > t + 1]
    if newer: return False, '편집 통과 뒤 바뀐 조각: ' + ', '.join(newer)
    return True, open(p, encoding='utf-8').read().strip()[:80]


FRAME_FROM = '2026-10-03'   # 카페 틀 v2는 '다음 카페 발행분부터'(10/02 지시) — slot 날짜가 이 날 이후면 gate가 막고, 그 전은 경고만 낸다.
FRAME_END = re.compile(r'FAQ|자주\s*묻|정리|요약|한눈에|체크')


def is_cafe_pkg(pkg):
    op = os.path.join(pkg, 'order.txt')
    return os.path.exists(op) and open(op, encoding='utf-8').read().lstrip().startswith('카페 발행 순서')


def frame_check(pkg):
    """카페 틀 v2 3줄(10/02 brand-director): ① 소제목 3~5개 ② 끝 FAQ/정리 소제목 ③ 제목: 명사 끝 또는 B틀 물음(얼마·몇), 반전(왜·는데) 금지. 어긴 곳 목록."""
    text, files = pkg_text(pkg)
    bad = []
    heads = [ln.strip() for ln in text.splitlines() if re.match(r'\s*(##\s|■)', ln)]
    if not 3 <= len(heads) <= 5: bad.append(f'소제목 {len(heads)}개 — 3~5개로(##·■ 줄 기준)')
    if not any(FRAME_END.search(h) for h in heads[-2:]): bad.append('끝 FAQ·정리 소제목이 없다 — 마지막 두 소제목 안에 FAQ/자주 묻는/정리/요약')
    # 10/03 12:2x write: 10/3 카페 칸 6개 중 5개가 사진 1~2장·표지 '평균:' 줄 없이 gates_ok를 받았다.
    # naverpost는 발행 순간에야 막아(사진 3장·cover_review 평균 7) 12:10 칸이 그 자리에서 걸렸다 — 도장 찍을 때 미리 잡는다.
    op = os.path.join(pkg, 'order.txt')
    if os.path.exists(op):
        n_img = sum(1 for ln in open(op, encoding='utf-8') if ln.strip().startswith('img/'))
        if n_img < 3: bad.append(f'사진 {n_img}/3장 — naverpost가 발행을 막는다')
    cr = os.path.join(pkg, 'cover_review.md')
    avg = re.findall(r'평균\s*[:：]\s*([0-9.]+)', open(cr, encoding='utf-8').read()) if os.path.exists(cr) else []
    if not avg or float(avg[-1]) < 7: bad.append('cover_review.md에 "평균: N"(3명, 7 이상) 줄이 없다 — naverpost가 발행을 막는다')
    tp = os.path.join(pkg, 'title.txt')
    if os.path.exists(tp):
        t = open(tp, encoding='utf-8').read().strip()
        core = re.sub(r"[\s\)\]\.!·~…\"']+$", '', t)
        # 10/02 10:2x brand-director 바로잡음: 물음 끝 하루 조회 중앙 1.77 > 명사 끝 0.66(benchmark-2026-10-02.md 제목 틀 v2).
        # 물음은 B틀('얼마·몇')만 허용, '왜·~는데' 반전은 금지(0.85 vs 1.26).
        if re.search(r'왜|는데', t): bad.append(f'제목에 반전 연결(왜·~는데) — "…{t[-14:]}"')
        elif (t.endswith('?') or re.search(r'(까|나요|가요|죠|요|니다)$', core)) and not re.search(r'얼마|몇', t):
            bad.append(f'물음 제목은 B틀(얼마·몇)만 — "…{t[-14:]}"')
        # 10/03 19:54 audit: RULES 179행 '하루 2편 이상 쉼표 없는 제목'이 관문에 없어 10/3 칸 11편이 전부 '키워드, 이야기' 틀.
        # 같은 날 카페 칸 중 쉼표 없는 제목이 2편 안 되면, 쉼표 제목은 막는다(쉼표 없는 쪽은 통과).
        sp = os.path.join(pkg, 'slot.txt')
        day = open(sp, encoding='utf-8').read().strip()[:10] if os.path.exists(sp) else ''
        if day >= COMMA_FROM and ',' in t:
            n, tot = comma_day(day, pkg, t)
            if n < 2: bad.append(f'{day} 카페 칸 쉼표 없는 제목 {n}/{tot}편 — 하루 2편 이상 필요, 이 제목을 쉼표 없이(질문 한 문장·숫자 한 문장)')
    return bad


COMMA_FROM = '2026-10-04'


def comma_day(day, pkg=None, title=None):
    """slots.json에서 그 날 카페 칸 제목을 모아 (쉼표 없는 편수, 전체 편수). pkg가 칸에 없으면 그 제목도 센다."""
    root = os.path.dirname(os.path.abspath(__file__))
    sl = json.load(open(os.path.join(root, 'research', 'slots.json'), encoding='utf-8'))
    titles, seen = [], set()
    for s in sl.get('slots', []):
        if s.get('kind') != 'cafe' or not str(s.get('at', '')).startswith(day) or not s.get('item'): continue
        tp = os.path.join(root, 'research', s['item'], 'pkg', 'title.txt')
        if os.path.exists(tp):
            titles.append(open(tp, encoding='utf-8').read().strip()); seen.add(os.path.normcase(os.path.abspath(os.path.dirname(tp))))
    if pkg and os.path.normcase(os.path.abspath(pkg)) not in seen and title: titles.append(title)
    return sum(',' not in x for x in titles), len(titles)


def gate_pkg(pkg):
    """발행기용. (올려도 되나, 한 줄 사유, 걸린 곳)."""
    text, files = pkg_text(pkg)
    if is_cafe_pkg(pkg):
        fb = frame_check(pkg)
        if fb:
            sp = os.path.join(pkg, 'slot.txt')
            slot = open(sp, encoding='utf-8').read().strip()[:10] if os.path.exists(sp) else '9999'
            if slot >= FRAME_FROM: return False, '카페 틀 v2 어김 — ' + '; '.join(fb), fb
            print('[경고] 카페 틀 v2 어김(이 슬롯은 경고만):', '; '.join(fb))
    val, hits, n = score(text)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    if val <= lim: return True, f'AI 티 {val}(기준 {lim})', hits
    ok, who = editor_ok(pkg, files)
    if ok: return True, f'AI 티 {val}(기준 {lim}) — 편집 통과 {who}', hits
    return False, f'AI 티 {val}이 기준 {lim}을 넘는다' + (f' ({who})' if who else ''), hits


def gate_text(text, ok_flag=False):
    """유튜브 제목·설명, 쿠팡 문구 같은 짧은 글용."""
    val, hits, n = score(text)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    if val <= lim or ok_flag: return True, f'AI 티 {val}(기준 {lim})' + (' — 편집 통과' if val > lim else ''), hits
    return False, f'AI 티 {val}이 기준 {lim}을 넘는다', hits


def refuse(msg, hits):
    print('올리지 않는다:', msg)
    for h in hits[:10]: print('   ', h)
    print('  고친 뒤 다시 올리거나, 편집자가 보고 py -3.12 work/aitell.py pass <묶음> <편집자> 를 남긴다.')


# ---- 대본 모드(10/3 클라우드 ① — research/editor/script-gate.md) ----
# 기존 score()는 경쟁 사람 자막과 우리 대본을 못 가렸다(6편 모두 0~3.5, 기준 12).
# 실측: 경쟁 롱폼 사람 자막 12편 숫자/1000단어 중앙 52·최대 91, 숫자 2개 이상 문장 중앙 11%·최대 20%
#       우리 대본 4편(E-1·D-1·E-2·N-1) 148~197, 33~44% — 두 지표 모두 각각 하나만으로도 16편을 다 가른다.
# 기준 = 경쟁 최대값(반올림 전 범위까지: 91 → 91.5 미만, 20 → 20.5 미만). 둘 다 지켜야 통과.
# research/editor/script_gate.json(speechcompare.py --loo --write가 자막 원본으로 다시 맞춘 값)이 있으면 그 값을 쓴다.
SCRIPT_RULES = [{'metric': '숫자/1000단어', 'op': 'le', 'value': 91.4},
                {'metric': '숫자 2개 이상 문장 %', 'op': 'le', 'value': 20.4}]
SCRIPT_GATE_JSON = os.path.join(HERE, 'research', 'editor', 'script_gate.json')
SPEECH_PY = os.path.join(HERE, 'research', 'longform', 'loop', 'speechcompare.py')


def _speech():
    import importlib.util
    spec = importlib.util.spec_from_file_location('speechcompare', SPEECH_PY)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def script_rules():
    try:
        r = json.load(open(SCRIPT_GATE_JSON, encoding='utf-8')).get('rules')
        if r: return r
    except (OSError, ValueError):
        pass
    return SCRIPT_RULES


def script_say(path):
    """읽는 말만 뽑는다. voice.json → say, .md → '- ' 줄(화면·[자막] 표시 뺌), 그 밖 → 글 전체(표시만 뺌)."""
    if path.endswith('.json'):
        v = json.load(open(path, encoding='utf-8'))
        return ' '.join(l['say'] for sec in v['sections'] for l in sec['lines'])
    raw = open(path, encoding='utf-8').read()
    if path.endswith('.md'):
        raw = '\n'.join(ln.strip()[2:] for ln in raw.splitlines() if ln.strip().startswith('- '))
    raw = re.sub(r'\[자막[^\]]*\]', ' ', raw)
    raw = re.sub(r'\(화면[^)]*\)', ' ', raw)
    return re.sub(r'\s+', ' ', raw).strip()


def script_score(text, rules=None):
    """(통과?, 지표 dict, 걸린 기준 목록)."""
    m = _speech().metrics(text)
    bad = []
    for r in rules or script_rules():
        v = m[r['metric']]
        ok = v <= r['value'] if r['op'] == 'le' else v >= r['value']
        if not ok: bad.append(f"{r['metric']} {v} — 기준 {'≤' if r['op'] == 'le' else '≥'} {r['value']}")
    return not bad, m, bad


def main(a):
    global SKIP
    if '--script' in a:
        i = a.index('--script')
        if i + 1 >= len(a): print('사용: aitell.py --script <voice.json|script.md|txt>'); return 2
        ok, m, bad = script_score(script_say(a[i + 1]))
        print(f"대본 말투 {'통과' if ok else '걸림'} — 숫자/1000단어 {m['숫자/1000단어']} · 숫자 2개 이상 문장 {m['숫자 2개 이상 문장 %']}% "
              f"· 숫자 하나 이하 문장 {m['숫자 하나 이하 문장 %']}% · 문장 {m['문장수']}")
        for b in bad: print('  ', b)
        if not ok: print('   말에는 반올림한 숫자 하나만, 정확한 값은 [자막: …]으로(research/editor/script-gate.md)')
        return 0 if ok else 6
    SKIP = '--skip-list' in a
    a = [x for x in a if x != '--skip-list']
    if not a: print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); return 0
    if a[0] == 'text':
        val, hits, n = score(' '.join(a[1:]), SKIP); print(f'AI 티 {val} ({n}자)'); [print('  ', h) for h in hits]; return 0
    if a[0] == 'gate':
        ok, msg, hits = gate_pkg(a[1])
        if ok: print(msg); return 0
        refuse(msg, hits); return 4
    if a[0] == 'commaday':
        n, tot = comma_day(a[1])
        print(f'{a[1]} 카페 칸 쉼표 없는 제목 {n}/{tot}편 — ' + ('통과' if n >= 2 else '걸림(하루 2편 이상)')); return 0 if n >= 2 else 5
    if a[0] == 'frame':
        bad = frame_check(a[1])
        if not bad: print('카페 틀 v2 통과', a[1]); return 0
        print('카페 틀 v2 어김', a[1]); [print('  ', b) for b in bad]; return 5
    if a[0] == 'pass':
        who = a[2] if len(a) > 2 else 'editor'
        import datetime
        val, _, _ = score(pkg_text(a[1])[0])
        open(os.path.join(a[1], OK_FILE), 'w', encoding='utf-8').write(
            f'{who} {datetime.datetime.now():%Y-%m-%d %H:%M} · 그때 점수 {val}\n')
        print('편집 통과 표시', a[1]); return 0
    if a[0] == 'scan':
        rows = []
        for p in a[1:]:
            if os.path.isdir(p) and os.path.exists(os.path.join(p, 'order.txt')):
                val, hits, n = score(pkg_text(p)[0], SKIP); rows.append((val, n, p, hits))
        rows.sort(reverse=True)
        for val, n, p, hits in rows: print(f'{val:6} {n:5}자 {os.path.basename(os.path.dirname(p))}  {"; ".join(hits[:3])[:110]}')
        if rows:
            vs = sorted(r[0] for r in rows)
            print(f'묶음 {len(vs)} · 중앙 {vs[len(vs)//2]} · 상위 25% {vs[int(len(vs)*0.75)]} · 기준 {LIMIT} 넘는 것 {sum(v > LIMIT for v in vs)}')
        return 0
    p = a[0]
    if os.path.isdir(p):
        text, files = pkg_text(p)
    else:
        text = open(p, encoding='utf-8').read()
    val, hits, n = score(text, SKIP)
    lim = LIMIT if n >= 300 else LIMIT_SHORT
    print(f'AI 티 {val} (기준 {lim}, {n}자) — {"넘음" if val > lim else "통과"}')
    for h in hits: print('  ', h)
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
