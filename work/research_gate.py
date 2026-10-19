# 공들인 자료조사 관문 — naverpost(카페)·ytlong(롱폼)이 부른다.

# 10/16 23:4x 사장님 "자료조사 좀 공들여서 해서 좀 만들어 봐, 전부" — research.md 6칸이 다 차야 나간다.
# 10/17 01시 고침: 잘된 롱폼 6편 1분 단위 실측(research/longform/content-gap-1017.md) — 우리 편엔 '왜·그래서·누구라면'이 0~4%였다.
RESEARCH_HEADS = ('원문', '질문', '왜', '그래서', '누구라면', '함정', '대조')
def research_check(path):
    """research.md 검사. 문제 목록(없으면 통과).
    원문: 대본·글의 숫자마다 원문 1곳(날짜 14일 안·쪽·표·조문)
    질문: 사람들이 실제로 묻는 질문 3개 이상(출처) — 질문 하나가 장 하나
    왜: 숫자마다 원문에 있는 이유(없으면 없다고)
    그래서: 장마다 선택 기준·제도상 할 일(신청·신고·한도, 금액·기한) — 투자 권유 아님
    누구라면: 2갈래 이상(나이·소득·보유 형태 등)
    함정: 놓치면 손해 보는 조건 1개 이상
    대조: 원문 값 ↔ 대본 값 표(틀림 방지)"""
    import os, re, datetime
    if not os.path.exists(path): return ['research.md 없음 — 공들인 자료조사(원문·경쟁·질문·우리만·예외·대조) 없이 못 올림']
    t = open(path, encoding='utf-8').read(); bad = []
    heads = re.findall(r'^#+\s*(.+)$', t, re.M)
    miss = [h for h in RESEARCH_HEADS if not any(h in x for x in heads)]
    if miss: bad.append('research.md 빠진 칸: ' + '·'.join(miss))
    urls = set(re.findall(r'https?://[^\s)>\]]+', t))
    if len(urls) < 3: bad.append(f'research.md 출처 주소 {len(urls)}개(3개 이상 — 대본 숫자마다 원문 1곳)')
    days = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', t)]
    if not days or (datetime.date.today() - max(days)).days > 14: bad.append('research.md 14일 안 확인 날짜 없음')
    return bad

# 10/19 사장님 "이 단계를 넣어. 아무거나 넣어서 이상하게 만들지 못하게 해" — 대본 목차는 경쟁 상위 8편 이상과 맞댄 근거가 있어야 녹음·업로드된다.
# ep/<편>/toc_compare.md 꼴(제목 줄 이름 그대로):
#   # 경쟁 목차      — 같은 주제 상위 영상 8편 이상, 줄마다 유튜브 주소·조회·확인 날짜·그 영상의 장 목록
#   # 기대하는 장    — 경쟁 여러 편이 다루는 장(시청자가 기대함). 줄마다 '→ 우리 N장' 또는 '뺌: 이유'
#   # 우리 목차      — 표 | 장 | 근거 | — 근거 칸마다 주소 1개 이상(그 장을 다룬 경쟁 영상, 또는 아무도 안 다룬 빈칸이면 그 질문이 나온 댓글·검색 주소)
TOC_FROM = '2026-10-23'   # H-3(10/23)부터. H-2·T-1·X-1은 이미 녹음돼 빠짐
def toc_check(ep, chapters=None):
    import os, re, datetime
    p = os.path.join(ep, 'toc_compare.md')
    if not os.path.exists(p): return ['toc_compare.md 없음 — 같은 주제 상위 8편 목차와 맞대지 않은 대본은 녹음·업로드 못 함']
    t = open(p, encoding='utf-8').read(); bad = []
    def sec(name):
        m = re.search(r'^#+\s*' + name + r'.*?$(.*?)(?=^#\s|\Z)', t, re.M | re.S)
        return m.group(1) if m else None
    comp, exp, ours = sec('경쟁 목차'), sec('기대하는 장'), sec('우리 목차')
    for n, s in (('경쟁 목차', comp), ('기대하는 장', exp), ('우리 목차', ours)):
        if s is None: bad.append(f"toc_compare.md '{n}' 칸 없음")
    if comp is not None:
        vids = set(re.findall(r'(?:youtu\.be/|watch\?v=)([\w-]{11})', comp))
        if len(vids) < 8: bad.append(f'경쟁 목차 영상 {len(vids)}편(8편 이상)')
        days = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', comp)]
        if not days or (datetime.date.today() - max(days)).days > 14: bad.append('경쟁 목차 14일 안 확인 날짜 없음')
    if exp is not None:
        lines = [l for l in exp.splitlines() if re.match(r'\s*(?:[-*]|\d+[.)])\s', l)]
        if len(lines) < 3: bad.append(f'기대하는 장 {len(lines)}개(3개 이상)')
        loose = [l.strip()[:40] for l in lines if not re.search(r'→\s*우리|뺌\s*:', l)]
        if loose: bad.append(f"기대하는 장 중 '→ 우리 N장'·'뺌: 이유' 없는 줄 {len(loose)}: " + ' / '.join(loose[:3]))
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
#   # 장면 계획  — 표 | 장 | 대본 줄(요지) | 구상(무엇을 어떻게) | 따라 한 경쟁 장면 # | 도구 | 파일 |
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
CAFE_BENCH_ITEMS = ('제목', '표지', '구성', '사진')
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
    return bad
