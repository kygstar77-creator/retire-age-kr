# AI 티 자동 검사 — 글이 기계로 찍은 것처럼 읽히는 신호를 점수로 낸다(2026-10-01).
#   py -3.12 work/aitell.py <묶음 폴더|텍스트 파일>          → 점수와 걸린 곳
#   py -3.12 work/aitell.py text "<문장>"                    → 짧은 글(제목·설명·댓글)
#   py -3.12 work/aitell.py gate <묶음>                      → 기준 넘고 편집 통과 표시 없으면 종료코드 4
#   py -3.12 work/aitell.py pass <묶음> <편집자>             → 편집 통과 표시(editor_ok.txt)를 남긴다
#   py -3.12 work/aitell.py scan <묶음 폴더 여러 개>         → 기준 조정용 분포
#   py -3.12 work/aitell.py sameday 2026-10-05               → 그 날 카페 칸끼리 숫자 핵심값 겹침(≥3, 같은 예시)·제목 끝말 같은 칸 ≥3 검사. 걸리면 종료코드 5. gate는 숫자 겹침만 막고 끝말은 경고(10/5부터)
#   py -3.12 work/aitell.py frame <묶음>                     → 카페 틀 v2 3줄 점검(소제목 3~5개·끝 FAQ/정리·제목 명사 끝 또는 B틀 물음, 반전 금지). 어기면 종료코드 5
#   py -3.12 work/aitell.py aibrief <묶음>                   → AI 브리핑 인용 구조 3줄(10/5 ai-lab): 첫 문단 2~3문장 안 숫자 답·질문형 소제목 ≥2·표 1개. 어기면 종료코드 5. gate에는 안 넣음(모든 글 같은 틀 금지 — 칸 1편씩 고른 글만)
#   py -3.12 work/aitell.py commaday 2026-10-04               → 그 날 카페 칸 쉼표 없는 제목 수(하루 2편 이상, 10/4 칸부터 frame이 쉼표 제목을 막는다)
#   py -3.12 work/aitell.py script <편 폴더|voice.json|자막 .json3|대본 텍스트>  → 롱폼 대본 실측 기준 2개(10/4 speechcompare 경쟁 자막 12편 vs 우리 4편): 숫자 1,000단어당 ≤92(경쟁 최대 91.4) · 숫자 2개 이상 문장 ≤20%. 넘으면 종료코드 6
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
    # FAQ 'Q.' 질문 줄은 연속에서 건너뛴다(세지도 끊지도 않음) — 10/7 parking1007: Q줄 '~요?'가 답의 '~요'와 이어져 연속을 부풀림
    qs = [m.group(1).strip() for m in re.finditer(r'(?m)^\s*Q\s*[.:)]\s*(.+)$', text)]
    run, yrun = 0, 0
    for s in sents:
        if qs and s.strip().endswith('?') and any(s.strip() in q for q in qs): continue
        run = run + 1 if re.search(r'요[.?!]?$', s) else 0; yrun = max(yrun, run)
    if yrun >= 5: pts += 2 * (yrun - 4); hits.append(f"'~요' {yrun}문장 연속")
    if len(sents) >= 10 and len(yo) / len(sents) > 0.6:
        pts += 10 * (len(yo) / len(sents) - 0.6) * 10 / 2; hits.append(f"'~요' 비율 {round(len(yo) / len(sents) * 100)}% (카페 실측 16%)")
    # 같은 틀 반복: 문장 머리 두 어절 / 꼬리 두 어절
    heads = collections.Counter(' '.join(s.split()[:2]) for s in sents if len(s.split()) >= 4)
    tails = collections.Counter(' '.join(s.split()[-2:]) for s in sents if len(s.split()) >= 4)
    for label, cnt in (('머리', heads), ('꼬리', tails)):
        for w, c in cnt.items():
            if c >= 3 and re.search(r'[가-힣A-Za-z]', w):
                pts += 2 * (c - 2); hits.append(f'같은 문장 {label} "{w}" ×{c}')
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
    sc, why = scope_check(pkg)
    if sc == '밖': bad.append(why)
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


# 10/05 brand-director 12:09 [지시]: 카페 주제 범위(brand/guide.md ①-카페 주제 범위). 밖 9편은 20회 넘은 글 0편.
# '밖'은 제목 낱말로 막고(관문), '경계'는 세후·노후 현금흐름 숫자로 끝나는지 사람이 보도록 경고만 낸다.
SCOPE_OUT = re.compile(r'한능검|한국사\s*능력|토익|TOEIC|토플|오픽|시험\s*일정|대형\s*폐기물|폐기물\s*스티커|장례\s*절차|장례식\s*절차|청년\s*(전용|도약|내일|희망|미래|주택|월세)')
SCOPE_EDGE = re.compile(r'실거래|아파트|분양|대출\s*금리|주담대|전세|(?<![가-힣])금\s*(시세|\d)|금값|주가|종목')
SCOPE_TIE = re.compile(r'세후|노후|은퇴|퇴직|연금|월\s*\d|매달|건보|건강보험|생활비|현금|배당|분배금|이자')


def scope_check(pkg):
    """카페 주제 범위 한 줄: '50대 전후 퇴직·노후 돈 숫자로 이어지나?' → ('안쪽'|'경계'|'밖', 이유)."""
    tp = os.path.join(pkg, 'title.txt')
    t = open(tp, encoding='utf-8').read().strip() if os.path.exists(tp) else ''
    m = SCOPE_OUT.search(t)
    if m: return '밖', f'카페 주제 밖("{m.group(0)}") — X-CN-1·R31 새 사이트 쪽으로(brand/guide.md ①-카페 주제 범위)'
    m = SCOPE_EDGE.search(t)
    if m and not SCOPE_TIE.search(text_head(pkg)):
        return '경계', f'경계 주제("{m.group(0)}")인데 제목·첫 문단에 세후·노후 현금흐름 말이 안 보인다 — 끝이 노후 돈 숫자로 이어지는지 확인'
    return ('경계' if m else '안쪽'), ''


def text_head(pkg):
    text, _ = pkg_text(pkg)
    return text[:400]


AIB_NUM = re.compile(r'\d|[천만억]\s*원|[일이삼사오육칠팔구십]\s*(?:만|억|천|%)')
AIB_Q = re.compile(r'(\?|？|까|나요|가요|얼마|몇|무엇|뭘|뭐)\s*$')


def aibrief_check(pkg):
    """AI 브리핑 인용 구조(10/5 ai-lab study-2026-10-05.md 2번). ① 첫 문단 2~3문장 안에 숫자 답 ② 질문형 소제목 2개 이상 ③ 표 1개. 빠진 것 목록."""
    text, files = pkg_text(pkg)
    body = '\n\n'.join(open(f, encoding='utf-8').read() for f in files)
    bad = []
    paras = [b.strip() for b in re.split(r'\n\s*\n', body) if b.strip() and not re.match(r'\s*(##|■)', b.strip())]
    first = ' '.join(sentences(paras[0])[:3]) if paras else ''
    if not AIB_NUM.search(first): bad.append('첫 문단 2~3문장 안에 숫자 답이 없다 — 질문의 답(금액·%)을 맨 앞에')
    heads = [re.sub(r'^\s*(##+|■)\s*', '', ln).strip() for ln in body.splitlines() if re.match(r'\s*(##\s|■)', ln)]
    nq = sum(1 for h in heads if AIB_Q.search(h))
    if nq < 2: bad.append(f'질문형 소제목 {nq}개 — 2개 이상(소제목 하나에 질문 하나)')
    tj = os.path.join(pkg, 'tables.json')
    has_t = os.path.exists(tj) and os.path.getsize(tj) > 4
    has_t = has_t or any(ln.count('|') >= 2 for ln in body.splitlines())
    if not has_t: bad.append('표가 없다 — tables.json 또는 | 표 1개')
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


SAMEDAY_FROM = '2026-10-05'   # 같은 날 칸끼리 숫자·끝말 겹침 검사(10/5 audit 07:57: nhisprop1005와 nhisrent1005가 586점 예시를 같이 씀, 7칸 중 5칸이 '월 얼마'로 끝남)
OVERLAP_MIN = 3               # 같은 날 다른 칸과 겹치는 '둥글지 않은' 숫자(586·211.5·7.19처럼 끝이 0이 아닌 3자리 이상)가 이 수 이상이면 같은 예시
END_SAME_MIN = 3              # 같은 날 같은 끝말 칸 수(그 칸 포함)가 이 수 이상이면 걸림


def _day_pkgs(day):
    """slots.json 그 날 카페 칸 중 묶음 폴더가 있는 것 → [(item, pkg 경로)]."""
    root = os.path.dirname(os.path.abspath(__file__))
    sl = json.load(open(os.path.join(root, 'research', 'slots.json'), encoding='utf-8'))
    out = []
    for s in sl.get('slots', []):
        if s.get('kind') != 'cafe' or s.get('skip') or not str(s.get('at', '')).startswith(day) or not s.get('item'): continue
        d = os.path.join(root, 'research', s['item'], 'pkg')
        # 못 나간 칸을 같은 날 뒤 칸으로 옮기면 한 묶음이 두 칸에 남는다(10/8 sanghan1008 08:10·14:10) — 한 번만 센다
        if os.path.exists(os.path.join(d, 'title.txt')) and s['item'] not in [i for i, _ in out]: out.append((s['item'], d))
    return out


def _key_nums(pkg):
    """본문에서 숫자 핵심값: 3자리 이상이고 끝이 0이 아닌 것(연도·URL 제외). 586·211.5·7.19 같은 값이 겹치면 같은 예시다."""
    t = re.sub(r'https?://\S+', '', pkg_text(pkg)[0])
    out = set()
    for x in re.findall(r'\d[\d,]*\.?\d*', t):
        x = x.replace(',', '').rstrip('.')
        if len(x) >= 3 and not x.endswith('0') and x not in ('2025', '2026', '2027', '2028'): out.add(x)
    return out


def end_key(title):
    """제목 끝말 묶음: 끝 12자 안에 '얼마'·'몇'이 있으면 그 말, 아니면 끝 두 글자(까·요·다 뺀 것)."""
    t = re.sub(r"[\s?!.…'\"]+$", '', title.strip())
    tail = t[-12:]
    for k in ('얼마', '몇'):
        if k in tail: return k
    return t.rstrip('까요다죠')[-2:]


def sameday_check(day, pkg=None):
    """같은 날 카페 칸끼리 ① 숫자 핵심값 겹침 ② 같은 끝말 3칸 이상. pkg가 있으면 그 묶음이 낀 것만 돌려준다. → (숫자 겹침 목록, 끝말 목록)."""
    items = _day_pkgs(day)
    me = os.path.normcase(os.path.abspath(pkg)) if pkg else None
    if me and me not in [os.path.normcase(os.path.abspath(d)) for _, d in items]:
        items.append((os.path.basename(os.path.dirname(os.path.abspath(pkg))), pkg))
    nums = {i: _key_nums(d) for i, d in items}
    dirs = dict(items)
    over = []
    names = [i for i, _ in items]
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            x, y = names[a], names[b]
            if me and me not in (os.path.normcase(os.path.abspath(dirs[x])), os.path.normcase(os.path.abspath(dirs[y]))): continue
            sh = nums[x] & nums[y]
            if len(sh) >= OVERLAP_MIN: over.append(f'{x}·{y} 숫자 {len(sh)}개 겹침({", ".join(sorted(sh)[:5])}) — 같은 예시면 다른 날로 옮기거나 예시를 바꾼다')
    ends = collections.defaultdict(list)
    for i, d in items: ends[end_key(open(os.path.join(d, 'title.txt'), encoding='utf-8').read())].append(i)
    endbad = []
    for k, v in ends.items():
        if len(v) >= END_SAME_MIN and (not me or os.path.basename(os.path.dirname(os.path.abspath(pkg))) in v):
            endbad.append(f"제목 끝말 '{k}' {len(v)}칸({', '.join(v)}) — 같은 날 {END_SAME_MIN}칸 이상이면 다른 끝말로")
    # 10/9 editor: 그날 4칸 c00이 모두 '…표로 정리했습니다.'로 끝났다(216묶음 중 그 4편뿐) — 첫 덩어리 맺음 문장 끝 두 어절도 같은 기준으로 본다
    leads = collections.defaultdict(list)
    for i, d in items:
        c0 = os.path.join(d, 'c00.txt')
        ss = sentences(open(c0, encoding='utf-8').read()) if os.path.exists(c0) else []
        if ss: leads[' '.join(ss[-1].split()[-2:])].append(i)
    for k, v in leads.items():
        if len(v) >= END_SAME_MIN and (not me or os.path.basename(os.path.dirname(os.path.abspath(pkg))) in v):
            endbad.append(f"첫 덩어리 맺음 '{k}' {len(v)}칸({', '.join(v)}) — 같은 날 {END_SAME_MIN}칸 이상이면 다른 문장으로")
    return over, endbad


def gate_pkg(pkg):
    """발행기용. (올려도 되나, 한 줄 사유, 걸린 곳)."""
    text, files = pkg_text(pkg)
    if is_cafe_pkg(pkg):
        sp0 = os.path.join(pkg, 'slot.txt')
        day0 = open(sp0, encoding='utf-8').read().strip()[:10] if os.path.exists(sp0) else ''
        if day0 >= SAMEDAY_FROM:
            over, endbad = sameday_check(day0, pkg)
            for e in endbad: print('[경고]', e)
            if over: return False, '같은 날 칸과 같은 예시 — ' + '; '.join(over), over
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


SCRIPT_NUM_PER_1000 = 92   # 지시는 ≤90이나 경쟁 자막 mOBsKBLWrN4가 91.4라 표본이 걸림 → 경쟁 최대(91.4)를 올림해 92. 경쟁 12편 중앙값 52 / 우리 중앙값 187 (longform/loop/speechcompare.py, 2026-10-04)
SCRIPT_MULTI_NUM_PCT = 20  # 숫자 2개 이상 문장 비율: 경쟁 중앙값 11%·최대 20% / 우리 40%


def script_text(p):
    """편 폴더(voice.json)·voice.json·자막 json3·일반 텍스트에서 말하는 글만 뽑는다."""
    if os.path.isdir(p): p = os.path.join(p, 'voice.json')
    if p.endswith('.json3'):
        d = json.load(open(p, encoding='utf-8'))
        return ' '.join(''.join(s.get('utf8', '') for s in e.get('segs', [])) for e in d.get('events', []) if e.get('segs')).replace(chr(10), ' ')
    if p.endswith('.json'):
        v = json.load(open(p, encoding='utf-8'))
        return ' '.join(l['say'] for s in v['sections'] for l in s['lines'])
    return open(p, encoding='utf-8').read()


def script_check(text):
    """(통과 여부, 숫자/1000단어, 숫자 2개 이상 문장 %, 문장 수, 메시지 목록). speechcompare.py와 같은 식."""
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', text) if len(x.strip()) > 3]
    W = max(1, len(text.split()))
    per = len(re.findall(r'\d[\d,.]*', text)) * 1000 / W
    multi = 100 * sum(len(re.findall(r'\d[\d,.]*', s)) >= 2 for s in sents) / max(1, len(sents))
    bad = []
    if per > SCRIPT_NUM_PER_1000: bad.append(f'숫자 {per:.1f}/1,000단어 > {SCRIPT_NUM_PER_1000}(경쟁 최대 91·중앙 52)')
    if multi > SCRIPT_MULTI_NUM_PCT: bad.append(f'숫자 2개 이상 문장 {multi:.0f}% > {SCRIPT_MULTI_NUM_PCT}%(경쟁 최대 20%·중앙 11%)')
    return not bad, per, multi, len(sents), bad


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


def main(a):
    global SKIP
    SKIP = '--skip-list' in a
    a = [x for x in a if x != '--skip-list']
    if not a: print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); return 0
    if a[0] == 'text':
        val, hits, n = score(' '.join(a[1:]), SKIP); print(f'AI 티 {val} ({n}자)'); [print('  ', h) for h in hits]; return 0
    if a[0] == 'script':
        ok, per, multi, n, bad = script_check(script_text(a[1]))
        print(f'대본 실측 숫자 {per:.1f}/1,000단어(기준 ≤{SCRIPT_NUM_PER_1000}) · 숫자 2개 이상 문장 {multi:.0f}%(기준 ≤{SCRIPT_MULTI_NUM_PCT}%) · 문장 {n} — ' + ('통과' if ok else '실패'))
        for b in bad: print('  ', b)
        if not ok: print('  숫자·사실 문장은 바꾸지 않는다: 말에는 숫자 하나·반올림, 정확한 값은 화면 자막으로 옮긴다.')
        return 0 if ok else 6
    if a[0] == 'gate':
        ok, msg, hits = gate_pkg(a[1])
        if ok: print(msg); return 0
        refuse(msg, hits); return 4
    if a[0] == 'commaday':
        n, tot = comma_day(a[1])
        print(f'{a[1]} 카페 칸 쉼표 없는 제목 {n}/{tot}편 — ' + ('통과' if n >= 2 else '걸림(하루 2편 이상)')); return 0 if n >= 2 else 5
    if a[0] == 'sameday':
        over, endbad = sameday_check(a[1])
        for x in over + endbad: print('걸림:', x)
        print(f'{a[1]} 같은 날 칸 검사 — ' + ('통과' if not (over or endbad) else f'숫자 겹침 {len(over)}건·끝말 {len(endbad)}건'))
        return 5 if (over or endbad) else 0
    if a[0] == 'frame':
        bad = frame_check(a[1])
        if not bad: print('카페 틀 v2 통과', a[1]); return 0
        print('카페 틀 v2 어김', a[1]); [print('  ', b) for b in bad]; return 5
    if a[0] == 'scope':
        sc, why = scope_check(a[1])
        print(f'카페 주제 범위: {sc}', a[1]); why and print('  ', why)
        return 5 if sc == '밖' else 0
    if a[0] == 'aibrief':
        bad = aibrief_check(a[1])
        if not bad: print('AI 브리핑 구조 통과', a[1]); return 0
        print('AI 브리핑 구조 빠짐', a[1]); [print('  ', b) for b in bad]; return 5
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
