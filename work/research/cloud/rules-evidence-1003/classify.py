"""규칙 후보 줄 1차 자동 분류 — 줄에 '붙어 있는 근거 표시'만 보고 판정한다(내용이 맞는지는 안 본다).

판정 순서(먼저 걸리는 것 하나):
  출처       : 줄(또는 바로 아래 3줄 안 '출처' 줄)에 http 주소, 또는 법 조문 번호(제N조)·예규 번호
  사장님 결정: 줄에 '사장님'과 따옴표 인용("…" “…” '…')이 같이 있음
  약함       : 근거가 사건 1~2건뿐(날짜 하나 붙은 사고·'1편'·'한 편'·'2편' 등)
  실측       : 숫자와 함께 실측·측정·중앙·근거 파일(.md .json .py)·N편/N개 표본이 붙음
  근거 없음  : 위 어느 것도 없음(누가·언제 정했는지만 있거나 아무것도 없음)
이 1차 결과는 verdicts_manual.tsv의 손 판정으로 덮어쓴다(build.py).
"""
import re

URL = re.compile(r'https?://\S+')
LAW = re.compile(r'제\s?\d+\s?조|(?:법|령|규칙)\s?\d+(?:·\d+)*조|예규 제?\d+|별표\s?\d')
QUOTE = re.compile(r'"[^"]{3,}"|“[^”]{3,}”|「[^」]{3,}」|\'[^\']{6,}\'')
BOSS = re.compile(r'사장님')
WEAK = re.compile(r'(?<![\d,.])(?:1|2|한|두)\s?(?:편|건|번|회|장|명)(?:뿐|만| 사례)|\((?:\d{1,2}/\d{1,2})\)|\(lessons? \d+\)|9/2\d\)|#\d{3}(?![0-9a-f])(?:~\d{3})?')
DATA = re.compile(r'실측|측정|중앙값?|근거\s|\.json|조회|표본|x\d+(?:\.\d+)?|\d+(?:\.\d+)?배|\d[^|]*\S+\.(?:md|py)\b|\S+\.(?:md|py)\b[^|]*\d')


def auto(text, ahead=''):
    if URL.search(text) or LAW.search(text):
        return '출처', (URL.search(text) or LAW.search(text)).group(0)[:80]
    if '출처' in ahead and URL.search(ahead):
        return '출처', URL.search(ahead).group(0)[:80]
    if BOSS.search(text) and QUOTE.search(text):
        return '사장님 결정', QUOTE.search(text).group(0)[:80]
    if WEAK.search(text):
        return '약함', WEAK.search(text).group(0)
    if DATA.search(text):
        return '실측', DATA.search(text).group(0)
    return '근거 없음', ''
