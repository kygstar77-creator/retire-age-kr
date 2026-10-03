"""규칙 후보 줄 뽑기 — rules-evidence-1003 감사용 일회성 도구.

대상 문서에서 규칙처럼 생긴 줄(글머리표·번호·표 줄)을 '파일:줄 \t 본문'으로 뽑는다.
교본(playbooks)은 '전문가가 아는 것·체크리스트·아마추어 실수·우리 제약·한 회차 순서' 절만 본다
('보고 배울 곳'·'배운 것'·'사례' 절은 관찰 기록이라 뺀다).
today.md는 [지시]·[결정] 줄만 본다.
사용: python extract.py > candidates.tsv   (저장소 work/research 기준 상대 경로)
"""
import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, '..', '..'))          # work/research
DOCS = ['longform/loop/RULES.md', 'conductor-manual.md', 'workflow.md', 'launch-checklist.md',
        'owner-lens.md', 'experiments-registry.md']
PB_KEEP = re.compile(r'전문가가 아는 것|체크리스트|아마추어 실수|우리 제약|한 회차 순서|Rules learned')
ITEM = re.compile(r'^\s*(?:[-*]\s+|\d{1,2}[.)]\s+|\|)')
SEP = re.compile(r'^\s*\|[\s:|-]+\|\s*$')
HEAD = re.compile(r'^\|\s*(ID|직원|트랙|단계|태그|상황|날짜|대상|편집자|성숙도|오늘 한 일|누구|실수|무엇)\s*\|')


def items(path, keep_section=None):
    sec, out = '', []
    for i, ln in enumerate(open(path, encoding='utf-8'), 1):
        s = ln.rstrip('\n')
        if s.startswith('#'):
            sec = s
            continue
        if keep_section and not keep_section.search(sec):
            continue
        if not ITEM.match(s) or SEP.match(s):
            continue
        body = re.sub(r'^\s*(?:[-*]\s+|\d{1,2}[.)]\s+)', '', s).strip()
        if len(re.sub(r'[\s|*~\-]', '', body)) < 12:
            continue
        if HEAD.match(body):
            continue                                       # 표 머리줄
        out.append((i, body))
    return out


def main():
    rows = []
    for d in DOCS:
        for i, b in items(os.path.join(R, d)):
            rows.append((d, i, b))
    for p in sorted(glob.glob(os.path.join(R, 'playbooks', '*.md'))):
        rel = os.path.relpath(p, R).replace(os.sep, '/')
        for i, b in items(p, PB_KEEP):
            rows.append((rel, i, b))
    for i, ln in enumerate(open(os.path.join(R, 'meeting', 'today.md'), encoding='utf-8'), 1):
        if re.search(r'\[(지시|결정)[^\]]*\]', ln):
            rows.append(('meeting/today.md', i, ln.strip()[:600]))
    for d, i, b in rows:
        print(f'{d}:{i}\t{b}'.replace('\r', ''))


if __name__ == '__main__':
    main()
