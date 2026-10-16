# 공들인 자료조사 관문 — naverpost(카페)·ytlong(롱폼)이 부른다.

# 10/16 23:4x 사장님 "자료조사 좀 공들여서 해서 좀 만들어 봐, 전부" — research.md 6칸이 다 차야 나간다.
RESEARCH_HEADS = ('원문', '경쟁', '질문', '우리만', '예외', '대조')
def research_check(path):
    """research.md 검사. 문제 목록(없으면 통과).
    ① 원문: 기관 원문 3개 이상, 이번에 새로 확인한 날짜(14일 안)와 쪽·표·조문
    ② 경쟁: 같은 주제 상위 5개(유튜브·카페·블로그)가 말한 것과 빠뜨린 것
    ③ 질문: 사람들이 실제로 묻는 질문 5개(지식iN·카페 질문·유튜브 댓글·연관검색어, 출처 포함)
    ④ 우리만: 원자료로 직접 계산한 새 숫자 1개 이상
    ⑤ 예외: 이 결론이 안 맞는 사람·조건
    ⑥ 대조: 원문 값 ↔ 글·대본 값 표"""
    import os, re, datetime
    if not os.path.exists(path): return ['research.md 없음 — 공들인 자료조사(원문·경쟁·질문·우리만·예외·대조) 없이 못 올림']
    t = open(path, encoding='utf-8').read(); bad = []
    heads = re.findall(r'^#+\s*(.+)$', t, re.M)
    miss = [h for h in RESEARCH_HEADS if not any(h in x for x in heads)]
    if miss: bad.append('research.md 빠진 칸: ' + '·'.join(miss))
    urls = set(re.findall(r'https?://[^\s)>\]]+', t))
    if len(urls) < 5: bad.append(f'research.md 출처 주소 {len(urls)}개(5개 이상)')
    days = [datetime.date.fromisoformat(x) for x in re.findall(r'(20\d\d-\d\d-\d\d)', t)]
    if not days or (datetime.date.today() - max(days)).days > 14: bad.append('research.md 14일 안 확인 날짜 없음')
    return bad
