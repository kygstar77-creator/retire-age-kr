# 공들인 자료조사 관문 — naverpost(카페)·ytlong(롱폼)이 부른다.

# 10/16 23:4x 사장님 "자료조사 좀 공들여서 해서 좀 만들어 봐, 전부" — research.md 6칸이 다 차야 나간다.
# 10/17 01시 고침: 잘된 롱폼 6편 1분 단위 실측(research/longform/content-gap-1017.md) — 우리 편엔 '왜·그래서·누구라면'이 0~4%였다.
RESEARCH_HEADS_OLD = ('원문', '질문', '왜', '그래서', '누구라면', '함정', '대조')
# 기준 리뉴얼 10/19(work/research/criteria/registry.md A-01): '한계' 칸 더함 — 확인 못 한 것·원문에 이유 없는 것·자료 기준일의 한계(없으면 '없음').
#   근거: Full Fact 체크리스트 '무엇이 불확실한지 구체적으로'·영국 통계 실천규약 3.0 '맥락과 한계를 알린다'·BBC 편집지침 3.4.6.
RESEARCH_HEADS = ('원문', '질문', '왜', '그래서', '누구라면', '함정', '한계', '대조')
# 새 기준(A-01 한계 칸·A-02 대조 줄마다 출처·A-04 질문 3개+주소·A-10 기준일·출처 전부 다시 확인)은 이 날 뒤 것부터(소급 없음).
#   롱폼: publishAt이 RENEW_FROM 이상(TOC_FROM과 같은 날 — H-2·T-1·X-1은 이미 조사·녹음 끝). 카페: order.txt를 CAFE_RENEW_FROM 뒤에 만든 묶음.
RENEW_FROM = '2026-10-23'
CAFE_RENEW_FROM = (2026, 10, 20, 0, 0)
URL_RE = r'https?://[^\s)>\]|]+'

def _sec(t, name):
    import re
    m = re.search(r'^#+\s*' + name + r'.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
    return m.group(1) if m else None

def _table_rows(s):
    import re
    return [l for l in s.splitlines() if l.strip().startswith('|') and not re.match(r'\s*\|\s*[-:]', l)][1:]

def source_urls(t):
    """대조 칸 표 줄마다의 출처 주소 → [(줄, {주소})]. 줄에 주소가 없으면 '원문' 칸에서 그 줄이 가리키는 S번호(S1·S4 …)의 주소를 쓴다."""
    import re
    dz, src = _sec(t, '대조'), _sec(t, '원문') or ''
    if dz is None: return []
    lab = {}
    for l in src.splitlines():
        for k in re.findall(r'\b(S\d{1,2})\b', l):
            lab.setdefault(k, set()).update(re.findall(URL_RE, l))
    out = []
    for r in _table_rows(dz):
        us = set(re.findall(URL_RE, r))
        for k in re.findall(r'\b(S\d{1,2})\b', r): us |= lab.get(k, set())
        out.append((r, us))
    return out

def research_check(path, strict=False):
    """research.md 검사. 문제 목록(없으면 통과). strict=True면 10/19 기준 리뉴얼(registry A-01·A-02·A-04) 값으로 본다.
    원문: 대본·글의 숫자마다 원문(날짜·쪽·표·조문)
    질문: 사람들이 실제로 묻는 질문 3개 이상, 줄마다 주소(지식iN·댓글·연관검색어) — 질문 하나가 장 하나
    왜: 숫자마다 원문에 있는 이유(없으면 없다고)
    그래서: 장마다 선택 기준·제도상 할 일(신청·신고·한도, 금액·기한) — 투자 권유 아님
    누구라면: 2갈래 이상(나이·소득·보유 형태 등)
    함정: 놓치면 손해 보는 조건 1개 이상
    한계: 확인 못 한 것·원문에 이유 없는 것·자료 기준일의 한계(없으면 '없음') — strict만
    대조: 원문 값 ↔ 대본 값 표(틀림 방지). strict면 줄마다 출처 주소 1개+, '2차' 줄은 2개+"""
    import os, re, datetime
    if not os.path.exists(path): return ['research.md 없음 — 공들인 자료조사(원문·질문·왜·그래서·누구라면·함정·한계·대조) 없이 못 올림']
    t = open(path, encoding='utf-8').read(); bad = []
    heads = re.findall(r'^#+\s*(.+)$', t, re.M)
    miss = [h for h in (RESEARCH_HEADS if strict else RESEARCH_HEADS_OLD) if not any(h in x for x in heads)]
    if miss: bad.append('research.md 빠진 칸: ' + '·'.join(miss))
    if strict:
        # A-02(EFCSN 기준 2조 G '핵심 주장마다 at least two'·IFCN 이름 있는 출처 둘 이상·Full Fact): 파일 전체 개수가 아니라 주장(대조 줄) 단위.
        #   1차(법령·고시·공식 통계표·공시 원문)는 1곳으로 되고, 줄에 '2차'라고 적은 것은 2곳 이상. 파일 전체 3개 검사는 뺐다.
        rows = source_urls(t)
        if not rows: bad.append("대조 칸에 표 줄 없음 — | 원문 | 원값 | 대본 값 | 출처 | 줄마다 주소")
        weak = [r.strip('| ')[:30] for r, us in rows if len(us) < 1 or ('2차' in r and len(us) < 2)]
        if weak: bad.append(f'대조 줄 출처 부족 {len(weak)}줄(1차 1곳·2차 2곳, 줄에 주소나 원문 칸 S번호): ' + ' / '.join(weak[:3]))
        # A-04(유튜브 챕터 최소 3개 answer/9884579 + 경쟁 챕터 13편 최소 3): 질문 3개 이상을 코드로 센다, 줄마다 주소.
        q = _sec(t, '질문') or ''
        ql = [l for l in q.splitlines() if re.match(r'\s*(?:[-*]|\d+[.)])\s', l)] + _table_rows(q)
        qn = [l for l in ql if re.search(URL_RE, l)]
        if len(qn) < 3: bad.append(f'질문 {len(qn)}개(주소 있는 줄 3개 이상 — 지식iN·댓글·연관검색어)')
    else:
        urls = set(re.findall(r'https?://[^\s)>\]]+', t))
        if len(urls) < 3: bad.append(f'research.md 출처 주소 {len(urls)}개(3개 이상 — 대본 숫자마다 원문 1곳)')
    # A-03: 날짜 창(14일)은 근거 없음 → 날짜가 있기만 하면 됨(기록용, BBC 3.4.15). 최신성은 prepublish_check 하나에서 본다.
    if not re.findall(r'(20\d\d-\d\d-\d\d)', t): bad.append('research.md 확인 날짜 없음')
    return bad

# 10/19 사장님 "이 단계를 넣어. 아무거나 넣어서 이상하게 만들지 못하게 해" — 대본 목차는 경쟁 상위 10편 이상(A-05, 처음 8편)과 맞댄 근거가 있어야 녹음·업로드된다.
# ep/<편>/toc_compare.md 꼴(제목 줄 이름 그대로):
#   # 경쟁 목차      — 같은 주제 상위 영상 10편 이상 + "포화:" 줄(A-05), 줄마다 유튜브 주소·조회·확인 날짜·그 영상의 장 목록
#   # 기대하는 장    — 경쟁 여러 편이 다루는 장(시청자가 기대함). 줄마다 '→ 우리 N장' 또는 '뺌: 이유'
#   # 우리 목차      — 표 | 장 | 근거 | — 근거 칸마다 주소 1개 이상(그 장을 다룬 경쟁 영상, 또는 아무도 안 다룬 빈칸이면 그 질문이 나온 댓글·검색 주소)
TOC_FROM = '2026-10-23'   # H-3(10/23)부터. H-2·T-1·X-1은 이미 녹음돼 빠짐
TOC_MIN_VIDS = 10         # A-05 (Francis 2010 10+3)
ENDING_MIN_VIDS = 6       # A-09 (Guest 2006 기본 뼈대 6 · 경쟁 14편 끝 8갈래) — 목차 표본 영상의 끝을 그대로 써도 됨
def toc_check(ep, chapters=None):
    import os, re, datetime
    p = os.path.join(ep, 'toc_compare.md')
    if not os.path.exists(p): return ['toc_compare.md 없음 — 같은 주제 상위 10편 목차와 맞대지 않은 대본은 녹음·업로드 못 함']
    t = open(p, encoding='utf-8').read(); bad = []
    def sec(name):
        m = re.search(r'^#+\s*' + name + r'.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
        return m.group(1) if m else None
    comp, exp, ours = sec('경쟁 목차'), sec('기대하는 장'), sec('우리 목차')
    for n, s in (('경쟁 목차', comp), ('기대하는 장', exp), ('우리 목차', ours)):
        if s is None: bad.append(f"toc_compare.md '{n}' 칸 없음")
    if comp is not None:
        vids = set(re.findall(r'(?:youtu\.be/|watch\?v=)([\w-]{11})', comp))
        # A-05(registry): 8편 → 10편 + '포화:' 줄. 근거 Francis 외 2010 '처음 10개 + 새 생각 없는 3개 연속이면 멈춤'·Guest 2006(12번째에 88%).
        if len(vids) < TOC_MIN_VIDS: bad.append(f'경쟁 목차 영상 {len(vids)}편({TOC_MIN_VIDS}편 이상)')
        if not re.search(r'포화\s*[:：]\s*\S', comp): bad.append("경쟁 목차 '포화:' 줄 없음(10편 + 새 장 없는 3편 연속, 예 '포화: 11·12·13번째 새 장 0')")
        # A-06: 14일 창은 근거 없음 → 확인 날짜만 요구
        if not re.findall(r'(20\d\d-\d\d-\d\d)', comp): bad.append('경쟁 목차 확인 날짜 없음')
    if exp is not None:
        lines = [l for l in exp.splitlines() if re.match(r'\s*(?:[-*]|\d+[.)])\s', l)]
        if len(lines) < 3: bad.append(f'기대하는 장 {len(lines)}개(3개 이상)')
        loose = [l.strip()[:40] for l in lines if not re.search(r'→\s*우리|뺌\s*:', l)]
        if loose: bad.append(f"기대하는 장 중 '→ 우리 N장'·'뺌: 이유' 없는 줄 {len(loose)}: " + ' / '.join(loose[:3]))
    bad += ending_check(t)
    if ours is not None:
        rows = [l for l in ours.splitlines() if l.strip().startswith('|') and not re.match(r'\s*\|\s*[-:]', l)][1:]
        if len(rows) < 3: bad.append(f'우리 목차 {len(rows)}장(표로)')
        nohit = [r.split('|')[1].strip()[:30] for r in rows if not re.search(r'https?://', r)]
        if nohit: bad.append(f'근거 주소 없는 장 {len(nohit)}개 — 뺄지 근거를 찾을지: ' + ' / '.join(nohit[:4]))
        if chapters:
            miss = [c for c in chapters if c not in ours and c not in ('예고', '마무리', '정리')]
            if miss: bad.append(f'영상 챕터가 우리 목차 표에 없음 {len(miss)}개: ' + ' / '.join(miss[:4]))
    return bad

# 10/19 사장님 "이미지도 우리 마음대로 넣지 말고 경쟁 채널·자료조사 철저히 하고, 만들 때 이미지를 구상하고, 구상한 걸 만들려면 여러 툴이 필요할 거 아니야.
#   AI 툴들을 찾아서 이미지·움직이는 영상 구상한 대로 만들면 되잖아. 경쟁 채널의 영상·이미지·움직이는 영상·AI로 사람·상황·장면 만든 것들 다 따라 하면 되잖아, 우리 대본대로! 이걸 단계에 넣어"
# ep/<편>/shot_plan.md 꼴(제목 줄 이름 그대로):
#   # 경쟁 장면  — 표 | # | 영상 주소(&t=초) | 채널 | 무엇을 어떻게 보여 줬나 | 종류 | 확인일 | — 4편 이상에서 10장면 이상, 14일 안
#                 종류 예: 실사 영상·AI 인물·AI 상황 장면·움직이는 그래픽·지도·자료 화면·사진
#   # 장면 계획  — 표 | 장 | 대본 줄(요지) | 구상(무엇을 어떻게) | 따라 한 경쟁 장면 # | 도구 | 파일 | 비교 그림 | 품질 판정(같음·나음, 심사한 사람) |
#                 장마다 1줄 이상, 줄마다 경쟁 장면 번호(#3) 또는 주소, 도구 이름, 만든 파일 경로(ep 폴더나 work/video/public 기준)
SHOT_FROM = '2026-10-23'
def shot_check(ep, chapters=None, need_files=True):
    import os, re, datetime
    p = os.path.join(ep, 'shot_plan.md')
    if not os.path.exists(p): return ['shot_plan.md 없음 — 경쟁 장면 조사·장면 구상·도구·만든 파일 없이 렌더·업로드 못 함']
    t = open(p, encoding='utf-8').read(); bad = []
    def sec(name):
        m = re.search(r'^#+\s*' + name + r'.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
        return m.group(1) if m else None
    def rows(s): return [[c.strip() for c in l.strip().strip('|').split('|')] for l in s.splitlines() if l.strip().startswith('|') and not re.match(r'\s*\|\s*[-:]', l)][1:]
    ref, plan = sec('경쟁 장면'), sec('장면 계획')
    if ref is None: bad.append("shot_plan.md '경쟁 장면' 칸 없음")
    if plan is None: bad.append("shot_plan.md '장면 계획' 칸 없음")
    nums = set()
    if ref is not None:
        rr = rows(ref); nums = {r[0].lstrip('#') for r in rr if r}
        vids = set(re.findall(r'(?:youtu\.be/|watch\?v=|shorts/)([\w-]{11})', ref))
        if len(rr) < 10: bad.append(f'경쟁 장면 {len(rr)}개(10개 이상)')
        if len(vids) < 4: bad.append(f'경쟁 장면 영상 {len(vids)}편(4편 이상)')
        days = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', ref)]
        if not days or (datetime.date.today() - max(days)).days > 14: bad.append('경쟁 장면 14일 안 확인 날짜 없음')
    if plan is not None:
        pr = rows(plan)
        if len(pr) < 5: bad.append(f'장면 계획 {len(pr)}줄')
        noref, notool, nofile = [], [], []
        here = os.path.dirname(os.path.abspath(__file__))
        for r in pr:
            r += [''] * (6 - len(r)); name = r[0][:20] or r[1][:20]
            refs = re.findall(r'#?(\d+)', r[3])
            if not (re.search(r'https?://', r[3]) or any(x in nums for x in refs)): noref.append(name)
            if not r[4] or r[4] in ('-', '없음'): notool.append(name)
            if need_files:
                fs = [f.strip() for f in re.split(r'[,·]', r[5]) if f.strip()]
                if not fs or not all(os.path.exists(os.path.join(ep, f)) or os.path.exists(os.path.join(here, 'video', 'public', f)) or os.path.exists(f) for f in fs): nofile.append(name)
        # 10/19 사장님 "구상했는데 퀄리티도 비슷하거나 더 좋게 만들어야 해! 이상하게 만든 걸 넣지 마!" — 줄마다 | 비교 그림 | 품질 판정 | 칸:
        #   비교 그림 = 경쟁 장면과 우리 장면을 나란히 놓은 파일, 판정 = 우리가 만든 사람이 아닌 심사(새 심사관·제미나이 등)가 '같음' 또는 '나음'. '못함'이면 다시 만든다.
        noq = []
        for r in pr:
            r += [''] * (8 - len(r)); name = r[0][:20] or r[1][:20]
            cmp_ok = any(os.path.exists(os.path.join(ep, f.strip())) for f in re.split(r'[,·]', r[6]) if f.strip())
            if not cmp_ok or not re.search(r'같음|나음', r[7]) or re.search(r'못함|떨어', r[7]): noq.append(name)
        if noq: bad.append(f'경쟁 장면보다 못하거나 비교 안 한 줄 {len(noq)}: ' + ' / '.join(noq[:4]) + ' — 같거나 나을 때까지 다시 만듦')
        if noref: bad.append(f'따라 한 경쟁 장면 없는 줄 {len(noref)}: ' + ' / '.join(noref[:4]) + ' — 우리 마음대로 넣은 장면')
        if notool: bad.append(f'도구 칸 빈 줄 {len(notool)}: ' + ' / '.join(notool[:4]))
        if nofile: bad.append(f'만든 파일 없는 줄 {len(nofile)}: ' + ' / '.join(nofile[:4]) + ' — 구상만 하고 안 만듦')
        if chapters:
            body = plan
            miss = [c for c in chapters if c not in body and c not in ('예고',)]
            if miss: bad.append(f'장면 계획에 없는 챕터 {len(miss)}: ' + ' / '.join(miss[:4]))
    return bad

# 10/19 사장님 "카페도 똑같이 하라고! 포스팅·이미지·썸네일·내용·운영 방식·회원 모아 오는 거·수익화 등등 모두!"
# research/<글>/bench.md 꼴(제목 줄 이름 그대로):
#   # 경쟁 글   — 표 | # | 주소 | 어디(카페·블로그 이름) | 반응(조회·댓글·공감, 보이는 만큼) | 확인일 | — 3편 이상, 14일 안
#   # 따라 한 것 — 표 | 항목 | 경쟁 # | 우리 글에서 | — 항목에 제목·표지·구성·사진은 꼭(줄마다 경쟁 번호나 주소)
CAFE_BENCH_FROM = (2026, 10, 19, 15, 0)   # 이 시각 뒤 만든 묶음(order.txt)부터
CAFE_BENCH_ITEMS = ('제목', '표지', '구성', '사진', '끝맺음')   # 끝맺음 10/19 — 맺음말·파이어맵 안내·댓글 질문도 잘되는 글 따라
def cafe_bench_check(path):
    import os, re, datetime
    if not os.path.exists(path): return ['bench.md 없음 — 경쟁 글 3편 보고 제목·표지·구성·사진을 무엇을 따라 했는지 없이 못 올림']
    t = open(path, encoding='utf-8').read(); bad = []
    def sec(name):
        m = re.search(r'^#+\s*' + name + r'.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
        return m.group(1) if m else None
    def rows(s): return [[c.strip() for c in l.strip().strip('|').split('|')] for l in s.splitlines() if l.strip().startswith('|') and not re.match(r'\s*\|\s*[-:]', l)][1:]
    ref, cp = sec('경쟁 글'), sec('따라 한 것')
    if ref is None: return ["bench.md '경쟁 글' 칸 없음"]
    rr = rows(ref); nums = {r[0].lstrip('#') for r in rr if r}
    if sum(1 for r in rr if re.search(r'https?://', '|'.join(r))) < 3: bad.append(f'경쟁 글 주소 {len(rr)}편(3편 이상)')
    days = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', ref)]
    if not days or (datetime.date.today() - max(days)).days > 14: bad.append('경쟁 글 14일 안 확인 날짜 없음')
    if cp is None: bad.append("bench.md '따라 한 것' 칸 없음"); return bad
    cr = rows(cp)
    for it in CAFE_BENCH_ITEMS:
        hit = [r for r in cr if r and it in r[0]]
        if not hit: bad.append(f"따라 한 것에 '{it}' 줄 없음")
        elif not any(re.search(r'https?://', '|'.join(r)) or any(x in nums for x in re.findall(r'#?(\d+)', r[1] if len(r) > 1 else '')) for r in hit): bad.append(f"'{it}' 줄에 경쟁 번호·주소 없음")
    ph = sec('사진 비교')   # 10/19 사장님 '이상하게 만든 걸 넣지 마' — 사진·표지가 경쟁 글과 같거나 나은지
    if ph is None: bad.append("bench.md '사진 비교' 칸 없음 — 우리 사진·표지를 경쟁 글 사진과 나란히 놓고 같거나 나은지 판정한 기록 없이 못 올림")
    else:
        prs = rows(ph); base = os.path.dirname(path)
        if not prs: bad.append('사진 비교 줄 없음')
        weak = [r[0][:20] for r in prs if len(r) < 4 or not any(os.path.exists(os.path.join(base, f.strip())) for f in re.split(r'[,·]', r[2]) if f.strip()) or not re.search(r'같음|나음', r[3]) or re.search(r'못함|떨어', r[3])]
        if weak: bad.append(f'경쟁보다 못하거나 비교 안 한 사진 {len(weak)}: ' + ' / '.join(weak[:3]))
    return bad

# 10/19 사장님 "유튜브·카페 한 편 한 편 올리기 전에 자료조사 새로 철저히 하는 것도 단계에 넣어! 모두 최신성이 있어야지!"
# research.md에 '# 올리기 전 확인' 칸 — 올리는 날(또는 전날) 날짜, 원문 주소 3개 이상을 다시 열어 본 기록,
#   '바뀐 것:' 줄(숫자·제도·시세가 바뀌었으면 무엇을 고쳤나, 없으면 '없음'), '새로 찾은 것:' 줄(그 사이 나온 뉴스·발표·댓글 질문 1개 이상)
# 기준 리뉴얼 10/19(registry A-10·D-11): 1일 유지(실거래 다음 날 공개·대출 규제 13개월 6번 — 근거 ① + BBC 편집지침 3.4.33 '내기 전에 사건에 추월당하지 않았나').
#   strict(새 편): ① 주소는 '3곳'(근거 없음) 대신 대조 칸 출처 주소 전부가 여기 다시 나와야 한다 ② '기준일:' 줄(숫자 묶음마다 '○월분, ○/○ 공표'·'○/○ 15:30 종가' —
#   UK 통계 실천규약 3.0·방송심의규정 제16조 참고) ③ 조사한 날과 오늘 사이에 그 주제 공표(data/release_calendar.json: 금통위·소비자물가 등)가 끼었으면 '바뀐 것:'에 그 공표를 적는다.
#   카페 금리·특판·분배금 글은 days=0(발행 당일) + '바뀐 것:'에 숫자(D-11 — 특판은 하루 만에 '[마감]', 티끌·월재연 실측).
RELEASE_CAL = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'data', 'release_calendar.json')

def release_hits(t, since, until):
    """research.md 글(t)에 낱말이 나오는 공표 중 since < 날짜 <= until 인 것 → [(이름, 날짜)]."""
    import json, re, datetime
    try: cal = json.load(open(RELEASE_CAL, encoding='utf-8'))
    except Exception: return []
    out = []
    for e in cal.get('releases', []):
        if not any(k in t for k in e.get('keywords', [])): continue
        ds = [datetime.date.fromisoformat(d) for d in e.get('dates', [])]
        if e.get('weekly') is not None:   # 0=월 … 3=목
            d = since + datetime.timedelta(days=1)
            while d <= until:
                if d.weekday() == e['weekly']: ds.append(d)
                d += datetime.timedelta(days=1)
        out += [(e['name'], d) for d in ds if since < d <= until]
    return out

def prepublish_check(path, days=1, strict=False, need_num=False):
    import os, re, datetime
    if not os.path.exists(path): return ['research.md 없음']
    t = open(path, encoding='utf-8').read()
    m = re.search(r'^#+\s*올리기 전 확인.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
    if not m: return ["research.md '올리기 전 확인' 칸 없음 — 올리는 날 원문을 다시 열어 최신인지 확인한 기록 없이 못 올림"]
    s = m.group(1); bad = []
    ds = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', s)]
    if not ds or (datetime.date.today() - max(ds)).days > days: bad.append(f'올리기 전 확인 날짜가 {days}일 넘음 — ' + ('발행 당일' if days == 0 else '오늘') + ' 다시 확인')
    here = set(re.findall(URL_RE, s))
    src = set().union(*[us for _, us in source_urls(t)]) if strict and source_urls(t) else set()
    if src:
        miss = src - here
        if miss: bad.append(f'올리기 전 확인에 대조 칸 출처 {len(miss)}곳이 다시 안 나옴: ' + ' '.join(sorted(miss)[:3]))
    elif len(here) < 3: bad.append('올리기 전 확인 원문 주소 3개 미만')
    ch = re.search(r'바뀐 것\s*[:：]\s*(\S.*)$', s, re.M)
    if not ch: bad.append("올리기 전 확인 '바뀐 것:' 줄 없음")
    elif need_num and not re.search(r'\d', ch.group(1)): bad.append("금리·특판·분배금 글 — '바뀐 것:'에 기준일·금리(분배금) 숫자를 적는다(D-11)")
    if not re.search(r'새로 찾은 것\s*[:：]\s*\S', s): bad.append("올리기 전 확인 '새로 찾은 것:' 줄 없음")
    if strict:
        if not re.search(r'기준일\s*[:：]\s*\S', s): bad.append("올리기 전 확인 '기준일:' 줄 없음 — 숫자 묶음마다 '(○월분, ○/○ 공표)'·'(○/○ 15:30 종가)'·'(○/○ 신고분)'")
        o = _sec(t, '원문') or ''
        od = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', o)]
        od = [d for d in od if d <= datetime.date.today()]
        if od:
            for name, d in release_hits(t, max(od), datetime.date.today()):
                line = ch.group(1) if ch else ''
                if name.split()[0] not in line and f'{d.month}/{d.day}' not in line and d.isoformat() not in line:
                    bad.append(f"조사 뒤 {d:%m/%d} {name} 공표가 있었다 — '바뀐 것:'에 그 공표(바뀐 숫자 또는 '그대로')를 적는다")
    return bad

# 10/19 사장님 "맨 뒤에 파이어맵 넣고나 이상한 질문하거나 이런 거 추가한 것도 경쟁 채널·자료조사 해서 별로면 좋은 걸로 바꿔 끼워! 억지로 끼워 맞추지 말고! 카페 글도 똑같이!"
# toc_compare.md '# 끝맺음' 칸 — 잘되는 영상 3편 이상이 어떻게 끝내는지(주소&t=초), 우리 끝(마지막 30초·고정 댓글 질문·파이어맵 안내)을 무엇을 따라 했나 '우리:' 줄.
def ending_check(text):
    import re
    m = re.search(r'^#+\s*끝맺음.*?$(.*?)(?=^#\s|\Z)', text, re.M | re.S)
    if not m: return [f"toc_compare.md '끝맺음' 칸 없음 — 잘되는 영상 끝맺음 {ENDING_MIN_VIDS}편 보고 우리 끝(파이어맵 안내·질문)을 정한 기록 없이 못 올림"]
    s = m.group(1); bad = []
    # A-09: 3편 → 6편(Guest 2006 기본 뼈대 6, 경쟁 14편 끝이 8갈래). 우리 끝 마지막 20초는 최종 화면 자리(answer/6388789) — '우리:' 줄에 적는다.
    if len(set(re.findall(r'(?:youtu\.be/|watch\?v=)([\w-]{11})', s))) < ENDING_MIN_VIDS: bad.append(f'끝맺음 경쟁 영상 {ENDING_MIN_VIDS}편 미만')
    if not re.search(r'우리\s*[:：]\s*\S', s): bad.append("끝맺음 '우리:' 줄 없음(무엇을 따라 했나, 뺀 것은 무엇인가)")
    return bad
