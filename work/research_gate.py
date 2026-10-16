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
