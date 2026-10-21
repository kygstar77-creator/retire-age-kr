# AI 티 자동 검사 — 글이 기계로 찍은 것처럼 읽히는 신호를 점수로 낸다(2026-10-01).
#   py -3.12 work/aitell.py <묶음 폴더|텍스트 파일>          → 점수와 걸린 곳
#   py -3.12 work/aitell.py text "<문장>"                    → 짧은 글(제목·설명·댓글)
#   py -3.12 work/aitell.py gate <묶음>                      → 기준 넘고 편집 통과 표시 없으면 종료코드 4
#   py -3.12 work/aitell.py pass <묶음> <편집자>             → 편집 통과 표시(editor_ok.txt)를 남긴다
#   py -3.12 work/aitell.py scan <묶음 폴더 여러 개>         → 기준 조정용 분포
#   py -3.12 work/aitell.py sameday 2026-10-05               → 그 날 카페 칸끼리 숫자 핵심값 겹침(≥3, 같은 예시)·제목 끝말 같은 칸 ≥3 검사. 걸리면 종료코드 5. gate는 숫자 겹침만 막고 끝말은 경고(10/5부터)
#   py -3.12 work/aitell.py frame <묶음>                     → 카페 틀 점검(기준 리뉴얼 10/19 D갈래: 소제목 0~6 경고·'한눈에 정리' 필수·쉼표 제목 하루 절반 이하·제목 30자 경고, 물음·'왜' 제목 규칙은 뺌). 어기면 종료코드 5
#   py -3.12 work/aitell.py aibrief <묶음>                   → AI 브리핑 인용 구조 3줄(10/5 ai-lab): 첫 문단 2~3문장 안 숫자 답·질문형 소제목 ≥2·표 1개. 어기면 종료코드 5. gate에는 안 넣음(모든 글 같은 틀 금지 — 칸 1편씩 고른 글만)
#   py -3.12 work/aitell.py commaday 2026-10-04               → 그 날 카페 쉼표 제목 수(D-22 10/19: 하루 칸의 절반 이하, 넘으면 frame이 쉼표 제목을 막는다)
#   py -3.12 work/aitell.py script <편 폴더|voice.json|자막 .json3|대본 텍스트>  → 롱폼 대본 실측 기준 2개(10/4 speechcompare 경쟁 자막 12편 vs 우리 4편): 숫자 1,000단어당 ≤92(경쟁 최대 91.4) · 숫자 2개 이상 문장 ≤20%. 넘으면 종료코드 6
#        + 말 습관 4개(10/13 벤치마크 루프): 정밀 숫자 낭독('39만 7천'·6자리↑)·순번 3종↑·말 목차('볼게요') 3연속·꼬리표 낭독({F}·이미지 1·S3) — 걸린 줄 번호 출력, 걸리면 종료코드 6
#        + 구어 아닌 말(10/19 사장님 '사람이 구어체로 쓰지 않는 단어'): work/data/not_spoken.json ban 말이 있으면 줄·바꿀 말을 보이고 종료코드 6, over 말은 경고만
#   py -3.12 work/aitell.py spoken <묶음|글 파일 …>          → 구어 아닌 말만(카페 원고 점검용, gate에는 없음). ban 말이 있으면 종료코드 5
#   py -3.12 work/aitell.py thumb "<썸네일 큰 글>" ["<둘째 줄>" …]  → 썸네일·쇼츠 표지 AI 티 A30·A31·A33·A52(10/15·10/21 editor, 근거 longform/thumb-gap-1015.md ③ — 남 29장 실측). 걸리면 종료코드 5. A32(그리다 만 0초 화면)는 그림이라 눈으로 본다
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
    # '~죠' 쏠림(10/11 editor cardded1011: 95문장 중 13번) — 사람 채널 받아쓰기 기준 8.2%, 12% 넘는 몫만 센다
    zo = [s for s in sents if re.search(r'죠[.?!]?$', s)]
    zlim = int(len(sents) * 0.12)
    if len(sents) >= 20 and len(zo) > zlim: pts += len(zo) - zlim; hits.append(f"'~죠' {len(zo)}문장/{len(sents)} (기준 8%)")
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


# 10/16 editor(근거 growth/cafe-gap-1016.md ③ A34·A36): 첫머리 두 가지는 기계로 본다. A35(백과사전 소개)·A37(직전 3일 같은 예시)은 눈으로.
#   A34 첫 400자에 괄호 낱말 풀이 2개 이상('ETF(주식처럼 사고파는 펀드) SPY(…)') — 풀이는 처음 한 곳만, 괄호 대신 다음 문장.
#   A36 첫 문장이 면책·영상 안내('사라거나 팔라는 글이 아니에요'·'쇼츠가 던진 질문이에요'·주소) — 면책은 끝 출처 옆, 주소는 끝.
# 10/17 슬롯부터 frame이 막고(write 지시 기한 '10/17 첫 회차부터'), 그 전 슬롯은 gate가 경고만 낸다.
OPEN_FROM = '2026-10-17'
GLOSS = re.compile(r'[A-Za-z가-힣0-9]\((?!\d)(?=[^)]*[가-힣])(?![^)]*(?:기준|시간|시각|발표|보도|출처|자료|공시|현지|뉴스|잠정|입주|년생|줄여서|만원|억원))[^)]{6,40}\)')
A36_FIRST = re.compile(r'(사|팔|권유|추천|투자)[^.?!\n]{0,15}(글|영상)[은이]?\s*아니|(쇼츠|영상)[가-힣\s]{0,10}질문이|https?://')


def opening_check(pkg):
    """카페 첫머리 A34·A36. 어긴 곳 목록."""
    _, files = pkg_text(pkg)
    body = '\n\n'.join(open(f, encoding='utf-8').read() for f in files)
    body = re.sub(r'^\s*(##|■).*$', '', body, flags=re.M).strip()
    bad = []
    g = GLOSS.findall(body[:400])
    if len(g) >= 2: bad.append(f'A34 첫 400자 괄호 풀이 {len(g)}개 — 처음 한 곳만, 나머지는 다음 문장으로(아는 말은 풀지 않음)')
    ss = sentences(body)
    if ss and A36_FIRST.search(ss[0]): bad.append(f'A36 첫 문장이 면책·영상 안내 "{ss[0][:30]}" — 독자 질문·고민으로 시작, 면책은 끝 출처 옆')
    return bad


D_FROM = '2026-10-20'   # 기준 리뉴얼 D갈래(10/19) 중 조이는 것('한눈에 정리' 필수)은 이 날 칸부터. 푸는 것(D-07·D-18·D-20·D-21·D-22)은 바로.
SUMMARY_END = re.compile(r'한눈에|정리|요약')
TITLE_WARN_LEN = 30     # D-23: 상위 카페 제목 3,908개 길이 중앙 20자(growth/cafe-copy-1019) — 30자 넘으면 경고만


def frame_check(pkg):
    """카페 틀(기준 리뉴얼 10/19, registry D-18~D-23). 어긴 곳 목록.
    D-18 소제목 수는 막지 않는다(0~6 허용, 7개 넘으면 경고) — 800자 넘는 상위 글 52편 중 33편이 소제목 없이 문단으로만.
    D-19 끝 '한눈에 정리'(정리·요약) 필수, FAQ는 선택 — 사장님 10/19 "한 편만 봐도 … 전부 이해".
    D-20·D-21 물음 제목 B틀만·'왜/는데' 금지는 뺐다(상위 3,908개: 물음 1.04배, 이유·왜 1.09배).
    D-22 쉼표 제목은 하루 카페 칸의 절반 이하(상위 카페 쉼표 제목 10%, 조회 1.05배 — 템플릿 신호만 막음)."""
    text, files = pkg_text(pkg)
    bad = []
    sc, why = scope_check(pkg)
    if sc == '밖': bad.append(why)
    heads = [ln.strip() for ln in text.splitlines() if re.match(r'\s*(##\s|■)', ln)]
    sp1 = os.path.join(pkg, 'slot.txt')
    day1 = open(sp1, encoding='utf-8').read().strip()[:10] if os.path.exists(sp1) else '9999'
    if len(heads) > 6: print(f'[경고] 소제목 {len(heads)}개 — 0~6개 권장(D-18, 쓰면 인용구 블록 꼴)')
    if day1 >= D_FROM and not os.path.exists(os.path.join(pkg, 'notice.txt')):   # 공지 묶음(공지사항 게시판)은 정보글이 아니라 빼고, 옛 규칙도 안 본다
        tail = heads[-2:] if heads else [ln for ln in text.splitlines()[len(text.splitlines()) // 2:]]
        if not any(SUMMARY_END.search(h) for h in tail): bad.append("끝 '한눈에 정리'가 없다 — 마지막 두 소제목(소제목 없으면 글 뒤쪽)에 한눈에/정리/요약(D-19, FAQ는 선택)")
    elif day1 < D_FROM and not any(FRAME_END.search(h) for h in heads[-2:]): bad.append('끝 FAQ·정리 소제목이 없다 — 마지막 두 소제목 안에 FAQ/자주 묻는/정리/요약')
    # 10/03 12:2x write: 10/3 카페 칸 6개 중 5개가 사진 1~2장·표지 '평균:' 줄 없이 gates_ok를 받았다.
    # naverpost는 발행 순간에야 막아(사진 3장·cover_review 평균 7) 12:10 칸이 그 자리에서 걸렸다 — 도장 찍을 때 미리 잡는다.
    op = os.path.join(pkg, 'order.txt')
    if os.path.exists(op):
        n_img = sum(1 for ln in open(op, encoding='utf-8') if ln.strip().startswith('img/'))
        if n_img < 3: bad.append(f'사진 {n_img}/3장 — naverpost가 발행을 막는다')
    # D-07(뺌): 표지 심사 '평균: N' 7점 문턱은 근거 없는 자체 점수 — D-05(100px 읽힘)·D-06(최근 10장 옆 구별)·D-04(경쟁 표지 종류)로 대신(editgate.cover_check).
    tp = os.path.join(pkg, 'title.txt')
    if os.path.exists(tp):
        t = open(tp, encoding='utf-8').read().strip()
        core = re.sub(r"[\s\)\]\.!·~…\"']+$", '', t)
        # D-20·D-21(뺌, 10/19): 물음 B틀만·'왜/~는데' 금지 규칙은 우리 글 표본(10/02)에서 나왔고, 상위 카페 3,908개는 물음 1.04배·이유·왜 1.09배.
        #   낚시(본문에 답 없는 제목)만 공식 기준으로 본다(사람 눈).
        if len(core) > TITLE_WARN_LEN: print(f'[경고] 카페 제목 {len(core)}자 — 30자 넘음(D-23, 상위 제목 중앙 20자)')
        # D-22(10/19): 쉼표 제목은 하루 카페 칸의 절반 이하(12칸이면 6편). 옛 규칙 '쉼표 없는 제목 하루 2편 이상'(10/03 audit)을 바꿈.
        sp = os.path.join(pkg, 'slot.txt')
        day = open(sp, encoding='utf-8').read().strip()[:10] if os.path.exists(sp) else ''
        if day >= COMMA_FROM and ',' in t:
            n, tot = comma_day(day, pkg, t)
            cap = cafe_slots_per_day() // 2
            if tot - n > cap: bad.append(f'{day} 카페 쉼표 제목 {tot - n}편 > 하루 칸 절반 {cap}편 — 이 제목을 쉼표 없이(D-22)')
    sp2 = os.path.join(pkg, 'slot.txt')
    if (open(sp2, encoding='utf-8').read().strip()[:10] if os.path.exists(sp2) else '9999') >= OPEN_FROM: bad += opening_check(pkg)
    return bad


# 10/05 brand-director 12:09 [지시]: 카페 주제 범위(brand/guide.md ①-카페 주제 범위). 밖 9편은 20회 넘은 글 0편.
# '밖'은 제목 낱말로 막고(관문), '경계'는 세후·노후 현금흐름 숫자로 끝나는지 사람이 보도록 경고만 낸다.
SCOPE_OUT = re.compile(r'한능검|한국사\s*능력|토익|TOEIC|토플|오픽|시험\s*일정|대형\s*폐기물|폐기물\s*스티커|장례\s*절차|장례식\s*절차|청년\s*(전용|도약|내일|희망|미래|주택|월세)')
SCOPE_EDGE = re.compile(r'실거래|아파트|분양|대출\s*금리|주담대|전세|(?<![가-힣])금\s*(시세|\d)|금값|주가|종목')
SCOPE_TIE = re.compile(r'세후|노후|은퇴|퇴직|연금|월\s*\d|매달|건보|건강보험|생활비|현금|배당|분배금|이자')
# D-29(10/19): 예금·금리·세금·건보료·연금계좌는 '안쪽'으로 명시 — 예금·파킹 금리는 전 연령 카페(정가거부·짠돌이)에서도 상위(growth/cafe-copy-1019)
SCOPE_IN = re.compile(r'예금|적금|파킹|금리|세금|양도세|종합소득세|건보료|건강보험료|연금계좌|ISA|IRP|연금저축|DC형|DB형')


def scope_check(pkg):
    """카페 주제 범위 한 줄: '50대 전후 퇴직·노후 돈 숫자로 이어지나?' → ('안쪽'|'경계'|'밖', 이유)."""
    tp = os.path.join(pkg, 'title.txt')
    t = open(tp, encoding='utf-8').read().strip() if os.path.exists(tp) else ''
    m = SCOPE_OUT.search(t)
    if m: return '밖', f'카페 주제 밖("{m.group(0)}") — X-CN-1·R31 새 사이트 쪽으로(brand/guide.md ①-카페 주제 범위)'
    if SCOPE_IN.search(t): return '안쪽', ''
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


def cafe_slots_per_day():
    """slots.json cadence.cafe 칸 수(지금 12). 못 읽으면 12."""
    try:
        sl = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research', 'slots.json'), encoding='utf-8'))
        return len(sl['cadence']['cafe']) or 12
    except Exception:
        return 12


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
END_BLOCK_FROM = '2026-10-18'  # 이날 칸부터 끝말 반복을 막는다(그 전 칸은 이미 관문 통과·발행분)
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
    # 통계표 코드(ECOS 731Y001)·종목코드 섞인 말은 예시가 아니다 — 10/13 g1cafe1013·m1stot1013이 출처 줄 731Y001과 세율 15.4로 막힘
    t = re.sub(r'\b\w*\d+[A-Za-z]+\w*\b', '', t)
    out = set()
    for x in re.findall(r'\d[\d,]*\.?\d*', t):
        x = x.replace(',', '').rstrip('.')
        # 10/17 editor: 입주 연도(2016·2018·2024)만 같은 고덕동 글과 상도동 글이 '같은 예시'로 막혔다 — 연도는 예시 값이 아니다(docstring대로 1950~2030 전부 뺌)
        if re.fullmatch(r'(19[5-9]\d|20[0-2]\d|2030)', x): continue
        if len(x) >= 3 and not x.endswith('0') and x not in ('15.4', '16.5', '22.0'): out.add(x)
    return out


def end_key(title):
    """제목 끝말 묶음: 쉼표 뒤(없으면 끝 12자)에 '얼마'·'몇'이 있으면 그 말, 아니면 끝 두 글자(까·요·다 뺀 것)."""
    t = re.sub(r"[\s?!.…'\"]+$", '', title.strip())
    # 10/17 audit: marrygift '…얼마까지 증여세 0원일까'는 '얼마'가 끝 12자 밖이라 '원일'로 셌다 — 쉼표 뒤 물음 덩어리 전체를 본다
    tail = t.rsplit(',', 1)[-1] if ',' in t else t[-12:]
    for k in ('얼마', '몇'):
        if k in tail or k in t[-12:]: return k
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
    # 10/21 R3(registry D-34): 링크 횟수 상한은 근거 없음. 운영원칙 8항 '특정 단어/문구 반복 삽입'에 맞춰 firemap.kr 안내 문장(주소 뺀 글자)이 같은 날 통째로 반복되는 것만 본다
    links = collections.defaultdict(set)
    for i, d in items:
        for f in sorted(glob.glob(os.path.join(d, 'c[0-9][0-9].txt'))):
            for ln in open(f, encoding='utf-8').read().splitlines():
                if 'firemap.kr' not in ln: continue
                k = ' '.join(re.sub(r'(https?://)?firemap\.kr\S*', '', ln).split())
                if len(k) >= 6: links[k].add(i)
    for k, v in links.items():
        if len(v) >= END_SAME_MIN and (not me or os.path.basename(os.path.dirname(os.path.abspath(pkg))) in v):
            endbad.append(f"계산기 안내 문장 '{k[:30]}' {len(v)}칸({', '.join(sorted(v))}) — 같은 날 {END_SAME_MIN}칸 이상 통째 반복(운영원칙 8항), 문장을 바꾼다")
    return over, endbad


RECENT_END_N = 2   # RULES 238: 최근 공개 카페 2편과 끝말이 같으면 3연속 — 막는다(날을 넘어도)


def recent_cafe_titles(n=RECENT_END_N, exclude=None):
    """published.txt가 카페 주소인 묶음 중 최근 n편의 (item, 제목), 최신 먼저."""
    import glob
    root = os.path.dirname(os.path.abspath(__file__))
    ex = os.path.normcase(os.path.abspath(exclude)) if exclude else None
    rows = []
    for f in glob.glob(os.path.join(root, 'research', '*', 'pkg', 'published.txt')):
        d = os.path.dirname(f)
        if ex and os.path.normcase(d) == ex: continue
        try:
            if 'cafe.naver.com' not in open(f, encoding='utf-8').read(): continue
            rows.append((os.path.getmtime(f), os.path.basename(os.path.dirname(d)), open(os.path.join(d, 'title.txt'), encoding='utf-8').read().strip()))
        except OSError:
            continue
    rows.sort(reverse=True)
    return [(i, t) for _, i, t in rows[:n]]


def recent_end_check(pkg):
    """날을 넘는 끝말 연속 검사. 걸리면 사유 한 줄, 아니면 ''."""
    me = end_key(open(os.path.join(pkg, 'title.txt'), encoding='utf-8').read())
    prev = recent_cafe_titles(exclude=pkg)
    if len(prev) == RECENT_END_N and all(end_key(t) == me for _, t in prev):
        return f"제목 끝말 '{me}'이 최근 공개 {RECENT_END_N}편({', '.join(i for i, _ in prev)})과 같아 3연속 — 다른 끝말로"
    return ''


# 기준 리뉴얼 A-26(10/19, registry): 단정·보장 표현 — 자본시장법 시행령 제102조의2제2호·금소법 시행령 제20조①4호('불확실한 사항에 대해 단정적 판단'),
#   자본시장법 제101조의2②2호·금소법 제22조④2호가목(손실보전·이익보장 오인), 유튜브 사기 정책 answer/2801973(get rich quick). ytlong.BANNED·shortsdaily C7과 같은 9개.
#   우리는 유사투자자문업자가 아니라 법 조항을 빌려 쓴 기준. 예금자보호(5천만원 한도) 설명 문장은 확정된 제도라 뺀다.
ASSERT_BANNED = ['확정 수익', '손실 없', '100% 수익', '반드시 오', '절대 안 떨어', '확실한 수익', '급등 예정', '단기간에 부자', '누구나 월']
ASSERT_EXCEPT = re.compile(r'예금자\s*보호')


def assert_check(text):
    """단정·보장 표현이 든 문장 [(말, 문장)]."""
    out = []
    for snt in sentences(text):
        if ASSERT_EXCEPT.search(snt): continue
        out += [(w, snt.strip()[:60]) for w in ASSERT_BANNED if w in snt]
    return out


def repeat_check(pkg):
    """카페 묶음 본문에서 거의 같은 문장이 두 번 나온 곳(끝 '한눈에 정리' 조각은 뺌). 경고만 — 기준 근거 조사 전이라 막지 않는다.
    10/20~21 editor 표본 6건 중 5건이 이 되풀이였다(h1helio1021 '8건을 한꺼번에…16%쯤 낮았' c00·c03, divdrop1020·h2cafe1019 등)."""
    import difflib, glob
    sents = []
    for f in sorted(glob.glob(os.path.join(pkg, 'c??.txt'))):
        t = open(f, encoding='utf-8').read()
        if re.search(r'^##\s*(한눈에|정리|요약)', t, re.M): continue
        for s in re.split(r'(?<=[.?!])\s+|\n+', t):
            k = re.sub(r'[\s,.·\-]|(어요|에요|예요|습니다|니다|요|다)$', '', s.strip().lstrip('- '))
            if len(k) >= 14 and not s.startswith(('http', '##', '|')): sents.append((os.path.basename(f), s.strip(), k))
    out = []
    for i, (fa, sa, ka) in enumerate(sents):
        for fb_, sb, kb in sents[i + 1:]:
            if re.findall(r'\d[\d.]*', sa) != re.findall(r'\d[\d.]*', sb): continue   # 숫자가 다르면 나란한 목록(3.5%·3.6%)이지 되풀이가 아니다
            if difflib.SequenceMatcher(None, ka, kb).ratio() >= 0.8:
                out.append(f'{fa} "{sa[:40]}" ↔ {fb_} "{sb[:40]}" — 한 번만')
    return out


def gate_pkg(pkg):
    """발행기용. (올려도 되나, 한 줄 사유, 걸린 곳)."""
    text, files = pkg_text(pkg)
    # A-31(법): 글에 쿠팡 링크가 있으면 대가 표시를 제목이나 첫 부분에(공정위 추천·보증 심사지침 Ⅴ.6 — 글은 본문과 다른 크기·색으로, 굵게)
    if re.search(r'coupang\.com|쿠팡\s*파트너스', text) and not re.search(r'쿠팡\s*파트너스.{0,40}수수료|수수료.{0,40}쿠팡\s*파트너스', text[:300]):
        return False, "쿠팡 링크 글 — 첫 부분(300자 안)에 '쿠팡 파트너스 … 수수료' 대가 표시를 굵게(공정위 추천·보증 심사지침 Ⅴ.6)", []
    ab = assert_check(text)
    if ab: return False, '단정·보장 표현(자본시장법 시행령 102조의2·금소법 시행령 20조) — ' + '; '.join(f'"{w}" {x}' for w, x in ab[:3]), ab
    if is_cafe_pkg(pkg):
        sp0 = os.path.join(pkg, 'slot.txt')
        day0 = open(sp0, encoding='utf-8').read().strip()[:10] if os.path.exists(sp0) else ''
        if day0 >= SAMEDAY_FROM:
            over, endbad = sameday_check(day0, pkg)
            if over: return False, '같은 날 칸과 같은 예시 — ' + '; '.join(over), over
            # 10/17 audit: endbad를 [경고]만 찍어 '얼마' 끝말이 하루 5칸 나갔다 — 막는다(10/18 칸부터)
            if endbad and day0 >= END_BLOCK_FROM: return False, '같은 날 끝말 반복 — ' + '; '.join(endbad), endbad
            for e in endbad: print('[경고]', e)
            if day0 >= END_BLOCK_FROM:
                rb = recent_end_check(pkg)
                if rb: return False, rb, [rb]
        if day0 < OPEN_FROM:
            for e in opening_check(pkg): print('[경고]', e)
        for e in repeat_check(pkg): print('[경고·되풀이]', e)
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


def script_src(p):
    """편 폴더면 voice.json, 녹음 전 편(H-2 10/14)은 voice.json이 없으니 가장 새 say_v*.txt(말 줄만)."""
    if not os.path.isdir(p): return p
    if os.path.exists(os.path.join(p, 'voice.json')): return os.path.join(p, 'voice.json')
    says = sorted(glob.glob(os.path.join(p, 'say_v*.txt')), key=lambda x: int(re.sub(r'\D', '', os.path.basename(x)) or 0))
    return says[-1] if says else os.path.join(p, 'voice.json')


def script_text(p):
    """편 폴더(voice.json)·voice.json·자막 json3·일반 텍스트에서 말하는 글만 뽑는다."""
    p = script_src(p)
    if p.endswith('.json3'):
        d = json.load(open(p, encoding='utf-8'))
        return ' '.join(''.join(s.get('utf8', '') for s in e.get('segs', [])) for e in d.get('events', []) if e.get('segs')).replace(chr(10), ' ')
    if p.endswith('.json'):
        v = json.load(open(p, encoding='utf-8'))
        # 'say'는 숫자를 한글로 풀어 읽은 줄('이백오십팔만 원')이라 숫자가 0개로 세졌다(10/13 R-1·G-1 0.0/1,000) → 숫자 그대로인 'text'
        return ' '.join(l.get('text') or l['say'] for s in v['sections'] for l in s['lines'])
    if p.endswith('.md'):   # script.md는 말하는 줄('- ')만 — (화면:)·[자막:] 줄은 읽지 않는다(10/19)
        return '\n'.join(re.sub(r'\s*\(재사용[^)]*\)', '', l[2:]) for l in open(p, encoding='utf-8').read().splitlines() if l.startswith('- '))
    return open(p, encoding='utf-8').read()


def script_lines(p, field='text'):
    """말 줄 목록(줄 번호를 붙여 보고하려고). voice.json은 text(숫자 그대로) 또는 say(실제 읽는 글), 텍스트는 빈 줄 뺀 줄."""
    p = script_src(p)
    if p.endswith('.json'):
        v = json.load(open(p, encoding='utf-8'))
        return [l.get(field) or l.get('text') or l['say'] for s in v['sections'] for l in s['lines']]
    return [x.strip() for x in script_text(p).splitlines() if x.strip()]


# 벤치마크 루프 10/13(quality-gap-1013)·U6: 1위급 대본에 없는 말 습관 4개. 걸린 줄을 돌려준다.
_UNIT = {'조': 10**12, '억': 10**8, '천만': 10**7, '백만': 10**6, '만': 10**4, '천': 10**3}
_COMPOUND = re.compile(r'(\d[\d,]*(?:\.\d+)?)\s*(조|억|만)\s*(\d[\d,]*)\s*(천만|백만|억|만|천)?')
_ORD = re.compile(r'(첫|두|세|네|다섯|여섯|일곱)\s?번째|(첫|둘|셋|넷|다섯)째')
_TOC = re.compile(r'(볼게요|보겠습니다|볼까요|알아볼게요|알아보겠습니다|살펴볼게요|살펴보겠습니다)')
_DISC = re.compile(r'법이\s?바뀐\s?(?:건|게)\s?아니|자문이\s?아닙|투자\s?권유|권하는\s?(?:건|게)\s?아니|사라거나\s?팔라는|추천이\s?아니|책임지지\s?않|참고용')  # A40 면책 문장
_TAG = re.compile(r'\{[^}]*\}|\[[^\]]*\]|(이미지|그림|장면|슬라이드)\s?\d|(?<![A-Za-z&])(?!A4|A3|B5|G7|G20)[A-Z]\d{1,2}(?![\d.])')  # 종이·회의 이름은 꼬리표 아님


_TTSMARK = re.compile(r'\[pause(?:\s+(?:short|long))?\]')   # Chirp 3 HD 쉼 표시 — 읽히지 않는다
_BUNIRAMYEON = re.compile(r'분이라면')
_LIMITW = re.compile(r'기록상|이\s?기록에서는|자료에\s?없|자료에\s?나오지\s?않|확인되지\s?않')
_PREVIEW = re.compile(r'(차례로|하나씩|순서대로)\s?(답해|살펴|알아|짚어)\s?(볼게요|보겠습니다|드릴게요)|조금\s?(뒤에|이따|있다가)\s?(볼게요|보겠습니다|말씀드릴게요)')


def screen_titles(p):
    """편 폴더 screen_text.txt의 판 제목([scenes.N.data.title]) 목록. 없으면 []."""
    f = os.path.join(p, 'screen_text.txt') if os.path.isdir(p) else ''
    if not f or not os.path.exists(f): return []
    return [l.split('] ', 1)[1].strip() for l in open(f, encoding='utf-8') if re.match(r'\[scenes\.\d+\.data\.title\] ', l)]


# A48(10/21 editor): 화면 자막에 우리 작업 메모가 샌 것(H-3 '(calc2 §2) — 말에 쓰지 않음'·'(T-1 사실표 L12)' 7곳) — 자막은 script.md [자막: …]에서 그대로 붙는다.
_MEMO = re.compile(r'calc\d?(_out)?\s?§|사실표\s?[A-Z]?\d|말에\s?쓰지\s?않|facts\.txt|\[[A-Z]\d{1,2}\]|DRAFT|TODO')


def screen_memos(p):
    """편 폴더 screen_text.txt에서 작업 메모가 든 화면 글자 줄. 코드에서 뽑은 줄([*.tsx])은 뺀다."""
    f = os.path.join(p, 'screen_text.txt') if os.path.isdir(p) else ''
    if not f or not os.path.exists(f): return []
    return [l.strip() for l in open(f, encoding='utf-8') if l.startswith('[scenes.') and _MEMO.search(l)]


def _sig(n):
    return len(str(int(round(n))).rstrip('0'))


def script_habits(lines, said=None, screen_titles=None):
    """[(검사, 줄 번호(1부터), 줄)] — 정밀 숫자 낭독·순번 3개 이상·말 목차 3연속·꼬리표 낭독.
    said: 실제 읽는 줄(voice.json say). text의 {F} 같은 표시는 say에서 빠지면 낭독이 아니라 꼬리표 검사는 said로 한다."""
    hits = []
    said = said if said and len(said) == len(lines) else lines
    for i, (l, sl) in enumerate(zip(lines, said), 1):
        prec = False
        for m in _COMPOUND.finditer(l):   # '39만 7천원'·'1억 1,087만'·'2,107만 8,535명'. '3억 5천만'처럼 유효숫자 2개는 둔다
            a = float(m.group(1).replace(',', '')) * _UNIT[m.group(2)]
            b = float(m.group(3).replace(',', '')) * (_UNIT[m.group(4)] if m.group(4) else 1)
            if b < _UNIT[m.group(2)] and _sig(a + b) >= 3: prec = True
        if prec or any(len(x.replace(',', '')) >= 6 for x in re.findall(r'\d[\d,]{4,}', l)): hits.append(('정밀 숫자', i, l))
        if _TAG.search(_TTSMARK.sub('', sl)): hits.append(('꼬리표 낭독', i, sl))   # [pause short] 같은 Chirp 쉼 표시는 소리 안 남(10/20 editor, T-1 22건 오탐)
    ords = [(i, l, re.sub(r'\s', '', m.group(0))) for i, l in enumerate(lines, 1) for m in _ORD.finditer(l)]
    if len({o[2] for o in ords}) >= 3: hits += [('순번 나열', i, l) for i, l, _ in ords]
    run = []
    for i, l in enumerate(lines, 1):
        run = run + [(i, l)] if _TOC.search(l) else []
        if len(run) == 3: hits += [('말 목차', j, x) for j, x in run]
        elif len(run) > 3: hits.append(('말 목차', i, l))
    # A40(10/17 순돌이): 같은 면책 한 편 2번 이상(P-1 '법이 바뀐 건 아니에요' 2번·H-1 3줄·W-1 2줄), 끝 3줄 면책(A21·A23 재발 G-1·R-1·W-1) → 편당 1줄·끝 3줄 밖.
    seen = {}
    for i, l in enumerate(lines, 1):
        for m in _DISC.finditer(l): seen.setdefault(re.sub(r'\s', '', m.group(0)), []).append((i, l))
    for v in seen.values():
        if len(v) >= 2: hits += [('면책 반복', i, l) for i, l in v]
    n = len(lines)
    hits += [('끝 3줄 면책', i, l) for i, l in enumerate(lines, 1) if i > n - 3 and _DISC.search(l)]
    # 벤치마크 루프 10/19(quality-gap-1019 ③): A41 '…분이라면' 장 틀 반복(C-2 9줄·H-3 5줄) → 편당 4줄까지.
    sb = [(i, l) for i, l in enumerate(lines, 1) if _BUNIRAMYEON.search(l)]
    if len(sb) > 4: hits += [('A41 분이라면 반복', i, l) for i, l in sb]
    # A46 한계 낱말 되풀이('기록상' 3번 + '이 기록에서는') → 한계는 한 번 말하고 나머지는 화면 작은 줄로.
    lim = {}
    for i, l in enumerate(lines, 1):
        for m in _LIMITW.finditer(l): lim.setdefault(re.sub(r'\s', '', m.group(0))[:3], []).append((i, l))
    for v in lim.values():
        if len(v) >= 3: hits += [('A46 한계 낱말 반복', i, l) for i, l in v]
    # A43 예고 줄('질문 다섯 개에 차례로 답해 볼게요'·'조금 뒤에 볼게요'), A44 끝 '정리하면' 되풀이.
    hits += [('A43 예고 줄', i, l) for i, l in enumerate(lines, 1) if _PREVIEW.search(l)]
    hits += [('A44 끝 정리하면', i, l) for i, l in enumerate(lines, 1) if i > n - 8 and re.match(r'\s*-?\s*(정리하면|정리해 보면|요약하면)', l)]
    # A47 같은 판 제목 3번 이상(C-2 '누구라면' 4장) — 판 제목은 그 판의 내용으로.
    from collections import Counter
    for t, c in Counter(screen_titles or []).items():
        if c >= 3: hits.append(('A47 같은 판 제목', 0, f"'{t}' ×{c} (screen_text 판 제목)"))
    return sorted(hits, key=lambda h: h[1])


# 기준 리뉴얼 A-23(10/19): 말 한 줄 숫자 — NPR Training(Socolovsky) '오디오 대본은 문장에 숫자 하나면 보통 충분'·CDC 명확한 소통 지표 9번(꼭 필요한 숫자만).
#   1개 기본, 2개는 비교 말이 있을 때만, 3개 이상은 실패. '3억 5천만'처럼 한 값은 하나로 센다. ytlong gate가 10/23 공개분부터 쓴다.
_CMP = re.compile(r'보다|대신|에서\s?.*으로|vs|VS|차이')


def script_numbers(lines):
    """[(줄 번호, 줄)] — 숫자 3개+ 줄, 또는 비교 말 없이 숫자 2개인 줄."""
    out = []
    one = re.compile(r'(?:\d{4}\s*년\s*)?\d{1,2}\s*월\s*\d{1,2}\s*일|\d{4}\s*년\s*\d{1,2}\s*월'   # 날짜 하나 = 값 하나
                     r'|\d[\d,.]*\s*(?:조|억|천만|백만|만|천|백)(?:\s*\d[\d,.]*\s*(?:천만|백만|만|천|백|억)?)+')   # '6천8백'·'3억 5천만' = 값 하나
    for i, l in enumerate(lines, 1):
        x = one.sub(' N ', _COMPOUND.sub(' N ', re.sub(r'S&P\s?500|NASDAQ\s?100|나스닥\s?100', 'IDX', l)))   # 10/21 지수 이름 속 숫자는 값이 아님(S&P500 = 이름)
        n = len(re.findall(r'\d[\d,.]*', x)) + x.count(' N ')
        if n >= 3 or (n == 2 and not _CMP.search(l)): out.append((i, l))
    return out


NS_FILE = os.path.join(HERE, 'data', 'not_spoken.json')


def spoken_check(lines):
    """10/19 사장님 '대본에 쓰는 단어도 AI 티를 벗어야 해. 사람이 구어체로 쓰지 않는 단어를 막 쓰잖아.'
    work/data/not_spoken.json(근거 longform/spoken-words-1019.md: 사람 자막 134편 vs 우리 68편 + 58세 심사관 2명).
    → (금지 걸림 [(말, 줄 번호, 줄, 바꿀 말)], 과다 경고 [메시지]). 따옴표·「」 인용과 terms(법·제도 이름, 상품명) 안은 안 센다."""
    if not os.path.exists(NS_FILE): return [], []
    d = json.load(open(NS_FILE, encoding='utf-8'))
    ex = [re.compile(x) for x in d.get('except_rx', [])] + [re.compile(re.escape(t)) for t in d.get('terms', []) if t]
    def mask(l):
        for rx in ex: l = rx.sub(lambda m: ' ' * len(m.group(0)), l)
        return l
    ml = [mask(l) for l in lines]
    hits = []
    for w, v in d.get('ban', {}).items():
        rx = re.compile(v['rx'])
        hits += [(w, i, lines[i - 1], v['to']) for i, l in enumerate(ml, 1) if rx.search(l)]
    warn, E = [], sum(len(l.split()) for l in lines)
    for w, v in d.get('over', {}).items():
        n = sum(len(re.findall(v['rx'], l)) for l in ml)
        cap = max(1, -(-v['human'] * v.get('cap_x', 3) * E // 1000))
        if n > cap: warn.append(f"'{w}' {n}번 — 이 길이면 사람 자막 기준 {int(cap)}번까지 → {v['to']}")
    return sorted(hits, key=lambda h: h[1]), warn


def script_check(text):
    """(통과 여부, 숫자/1000단어, 숫자 2개 이상 문장 %, 문장 수, 메시지 목록). speechcompare.py와 같은 식."""
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', text) if len(x.strip()) > 3]
    W = max(1, len(text.split()))
    per = len(re.findall(r'\d[\d,.]*', text)) * 1000 / W
    multi = 100 * sum(len(re.findall(r'\d[\d,.]*', s)) >= 2 for s in sents) / max(1, len(sents))
    bad = []
    if per > SCRIPT_NUM_PER_1000: bad.append(f'숫자 {per:.1f}/1,000단어 > {SCRIPT_NUM_PER_1000}(경쟁 최대 91·중앙 52)')
    if multi > SCRIPT_MULTI_NUM_PCT: bad.append(f'숫자 2개 이상 문장 {multi:.0f}% > {SCRIPT_MULTI_NUM_PCT}%(경쟁 최대 20%·중앙 11%)')
    # 10/16 사장님 "이상한 단위 할 푼 리 이런 건 쓰지 말아야 할 거고" — 할·푼·리 비율 말과 억·조 뒤 소수 둘째 자리(20.00억)는 금지.
    for m in re.finditer(r'(\d|[일이삼사오육칠팔구십한두세네])\s*할(?![인부머])|\d\s*푼|\d+\.\d{2}\s*[억조]', text):
        bad.append(f'이상한 단위 "{m.group(0)}" — 할·푼·리 대신 %·"10명 중 1명", 억은 "20억"·"23억 8천만원"처럼')
    # A-26: 단정·보장 표현(법 조항 빌려 씀) — 대본도 막는다
    for w, x in assert_check(text): bad.append(f'단정·보장 표현 "{w}" — {x}')
    # A-20 보탬(경고): 비율을 말로 할 때는 "10명 중 1명" 꼴(CDC 위험 소통·Galesic·Gigerenzer 2009) — 막지 않음
    pc = len(re.findall(r'\d+(?:\.\d+)?\s*%|퍼센트', text))
    if pc >= 5: print(f'[경고] 말에 % {pc}번 — 비율은 "10명 중 1명"처럼 자연 빈도로, 비교할 땐 분모를 같게(A-20)')
    # S-소리(10/21 editor, PD 10/20 찬성 — 경고만): '그 안이면·안이었·안이에요'는 받아쓰기에서 '아니면·아니었'으로 들림(H-2 3:7·5:14, J-1 198)
    for m in re.finditer(r'[^.!?\n]{0,20}\s안이(?:면|었|에요|예요|라면)[^.!?\n]{0,10}', text):
        print(f'[경고·소리] "{m.group(0).strip()}" — "아니…"로 들려 뜻이 뒤집힘, "그렇다면"·"그 값 안에 들었"처럼')
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


def thumb_check(lines):
    """썸네일 글자 A30(자릿수 물음표)·A31(큰 글 소수점, 이율 % 빼고)·A33(문서 단서 꼬리) — 남 29장 중 0·1·1장."""
    bad = []
    for l in lines:
        if re.search(r'\?[,.]?\?{2,}|\d\?{2,}|\?{2,}[,.]\d|[?]{1,},[?]{3}', l): bad.append(f'A30 자릿수까지 물음표로 가림: {l} — 말로(이만큼·이것)')
        for m in re.finditer(r'[-−+]?\d+\.\d+\s*(세|%|배|년|억|만)', l):
            if not re.search(r'(연|금리|이율)\s*$', l[:m.start()]): bad.append(f'A31 계산기 소수점 "{m.group(0)}": {l} — "77세쯤"·"3분의 1"로, 정확한 값은 설명란')
        if re.search(r'\((잠정|추정|확정|세전|세후|기준)\)|중앙값?|평당\s*중앙|\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\s*[~–-]|출처', l):
            bad.append(f'A33 문서 단서 꼬리: {l} — 설명란으로')
        if re.search(r'(\d{4}\s*[년.]\s*)?\d{1,2}\s*월(\s*\d{1,2}\s*일)?\s*기준|\d{1,2}[./]\d{1,2}\s*기준', l):
            bad.append(f'A52 날짜 기준 꼬리(알약 속 "(10월 6일 기준)"): {l} — 기준일은 설명란으로')
    return bad


def main(a):
    global SKIP
    SKIP = '--skip-list' in a
    a = [x for x in a if x != '--skip-list']
    if not a: print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); return 0
    if a[0] == 'text':
        val, hits, n = score(' '.join(a[1:]), SKIP); print(f'AI 티 {val} ({n}자)'); [print('  ', h) for h in hits]; return 0
    if a[0] == 'thumb':
        bad = thumb_check(a[1:])
        if not bad: print('썸네일 글자 A30·A31·A33·A52 통과 (A32 그리다 만 화면은 눈으로)'); return 0
        print('썸네일 글자 AI 티'); [print('  ', b) for b in bad]; return 5
    if a[0] == 'script':
        ok, per, multi, n, bad = script_check(script_text(a[1]))
        print(f'대본 실측 숫자 {per:.1f}/1,000단어(기준 ≤{SCRIPT_NUM_PER_1000}) · 숫자 2개 이상 문장 {multi:.0f}%(기준 ≤{SCRIPT_MULTI_NUM_PCT}%) · 문장 {n} — ' + ('통과' if ok else '실패'))
        for b in bad: print('  ', b)
        if not ok: print('  숫자·사실 문장은 바꾸지 않는다: 말에는 숫자 하나·반올림, 정확한 값은 화면 자막으로 옮긴다.')
        habits = script_habits(script_lines(a[1]), script_lines(a[1], 'say'), screen_titles(a[1]))
        habits += [('A48 화면에 작업 메모', 0, m) for m in screen_memos(a[1])]
        print('말 습관(정밀 숫자·순번 3개↑·말 목차 3연속·꼬리표 낭독·A40 면책 반복/끝 3줄·A41 분이라면 5줄↑·A43 예고·A44 끝 정리·A46 한계 낱말 3번↑·A47 같은 판 제목 3장↑·A48 화면 작업 메모) — ' + ('통과' if not habits else f'{len(habits)}건 걸림'))
        for k, i, l in habits: print(f'   [{k}] {i}줄: {l[:70]}')
        if habits: print('  정밀 숫자는 말로 반올림(정확값은 화면), 순번·목차는 질문 한 줄로, 꼬리표는 말에서 지운다, 면책은 편당 1줄·끝 3줄 밖, 한계 말은 한 번만, 판 제목은 그 판 내용으로.')
        sp, over = spoken_check(script_lines(a[1]))
        print('구어 아닌 말(data/not_spoken.json, 10/19) — ' + ('통과' if not sp else f'{len(sp)}줄 걸림'))
        for w, i, l, to in sp: print(f'   [{w} → {to}] {i}줄: {l[:70]}')
        for x in over: print('   [경고·많이 씀]', x)
        if sp: print('  사람 자막에 거의 안 나오는 말이다. 바꿀 말로 고치되 숫자·사실은 그대로. 법·제도 이름·상품명이면 not_spoken.json terms에 그 이름을 더한다.')
        return 0 if ok and not habits and not sp else 6
    if a[0] == 'spoken':   # 카페 묶음·아무 글: 구어 아닌 말만(10/19). 발행 관문(gate)에는 안 넣음 — 글로 쓰는 말과 말로 하는 말은 다르다
        tot = 0
        for p in a[1:]:
            t = pkg_text(p)[0] if os.path.isdir(p) else script_text(p)
            sp, over = spoken_check([x for x in t.splitlines() if x.strip()])
            tot += len(sp)
            print(f'{p} — 구어 아닌 말 ' + ('통과' if not sp else f'{len(sp)}줄'))
            for w, i, l, to in sp: print(f'   [{w} → {to}] {l.strip()[:70]}')
            for x in over: print('   [경고·많이 씀]', x)
        return 5 if tot else 0
    if a[0] == 'gate':
        ok, msg, hits = gate_pkg(a[1])
        if ok: print(msg); return 0
        refuse(msg, hits); return 4
    if a[0] == 'commaday':
        n, tot = comma_day(a[1])
        cap = cafe_slots_per_day() // 2   # D-22(10/19): 쉼표 제목은 하루 칸 절반 이하
        print(f'{a[1]} 카페 쉼표 제목 {tot - n}/{tot}편 — ' + ('통과' if tot - n <= cap else f'걸림(하루 {cap}편까지)')); return 0 if tot - n <= cap else 5
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
