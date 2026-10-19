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
