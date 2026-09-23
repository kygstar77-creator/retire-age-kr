# 숏폼 대본 — 사장님 2026-09-23 밤: "제미나이 말고 대본 클로드로 써. 무료 요금제라 금방 한도가 차.
# 지금도 firemap loop가 제미나이 한도 끝나서 대본 안 썼대."
# 그래서 대본은 회차 루틴(클로드)이 직접 쓴다. 이 파일은 두 가지만 한다.
#   1) 규칙과 쓸 수 있는 숫자를 한 화면에    py -3.12 work/shortscript.py spec <facts파일> "<주제>"
#   2) 쓴 대본이 규칙을 지켰는지 기계로 검사  py -3.12 work/shortscript.py check <대본.json> [facts파일]
# 품질은 말이 아니라 이 검사로 지킨다. 걸리면 고쳐서 다시 돌린다. 검사를 건너뛰고 발행하지 않는다.
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')

RULES = '''숏폼 대본 규칙 (경쟁 쇼츠 실측에서 나온 값 — 지어낸 규칙이 아니다)

- 장면 4~5개. 총 45~60초.
- 첫 장면 3초 안에 "이걸 왜 봐야 하는지"가 숫자로 나와야 한다(경쟁 쇼츠 제목 43%가 숫자).
- head : 화면에 크게 박힐 한 줄. 공백 포함 22자 이내. 숫자가 반드시 들어간다.
- label: head 위 작은 글. 15자 이내. 없으면 빈 문자열.
- lines: 화면에 작게 붙는 줄 1~3개. 각 24자 이내.
- say  : 읽어 줄 말. head/lines를 그대로 읽지 말고 사람이 설명하듯 풀어서. 한 장면 40~60자.
- outro: 한 줄. 출처를 밝히되 딱딱하지 않게.
- image: 장면마다 실제 자료 화면 경로를 넣는다(차트 chartimg.py · 네이버 부동산 캡처 · 히트맵).
         글자만 있는 장면은 만들지 않는다(사장님 2026-09-23 "저러면 아무도 안 봐").

금지
- 사실표에 없는 수치·주장·전망·추천
- 과장어: 충격 · 역대급 · 대박 · 폭등 · 폭락 · 무조건
- 보고서투: 정리하면 · 핵심은 · 결론적으로 · 시사한다 · 해보자
- 물음표로 끝내는 say

형식(이 구조 그대로, 다른 키 추가 금지):
{"title": "...", "scenes": [{"label": "...", "head": "...", "lines": ["..."], "say": "...", "image": "경로.png"}], "outro": "..."}
'''

BAN = ['충격', '역대급', '대박', '폭등', '폭락', '무조건', '정리하면', '핵심은', '결론적으로', '시사한다', '해보자']

def nums(s):
    return set(re.findall(r'\d[\d,]*\.?\d*', s or ''))

def check(path, facts_path=None):
    d = json.load(open(path, encoding='utf-8'))
    facts = open(facts_path, encoding='utf-8').read() if facts_path and os.path.exists(facts_path) else ''
    fnums = nums(facts)
    bad, warn = [], []
    sc = d.get('scenes') or []
    if not 4 <= len(sc) <= 5: bad.append(f'장면 {len(sc)}개 — 4~5개여야 한다')
    if not d.get('outro'): bad.append('outro 없음')
    first = ' '.join([sc[0].get('head', ''), *(sc[0].get('lines') or [])]) if sc else ''
    if sc and not re.search(r'\d', first): bad.append('첫 장면에 숫자가 없다(3초 안에 숫자가 보여야 한다)')
    for i, s in enumerate(sc):
        h, ls, say = s.get('head', ''), s.get('lines') or [], s.get('say', '')
        if not h: bad.append(f'{i}번 head 없음')
        elif len(h) > 22: bad.append(f'{i}번 head {len(h)}자 — 22자 이내')
        if s.get('label') and len(s['label']) > 15: bad.append(f'{i}번 label {len(s["label"])}자 — 15자 이내')
        if not 1 <= len(ls) <= 3: bad.append(f'{i}번 lines {len(ls)}개 — 1~3개')
        for l in ls:
            if len(l) > 24: bad.append(f'{i}번 lines "{l[:14]}…" {len(l)}자 — 24자 이내')
        if not 30 <= len(say) <= 75: warn.append(f'{i}번 say {len(say)}자 — 40~60자 권장')
        if say.rstrip().endswith('?'): bad.append(f'{i}번 say가 물음표로 끝난다')
        img = s.get('image')
        if not img: bad.append(f'{i}번 image 없음 — 글자만 있는 장면은 만들지 않는다')
        elif not os.path.exists(img): bad.append(f'{i}번 image 파일이 없다: {img}')
        for w in BAN:
            if w in h or w in say or any(w in l for l in ls): bad.append(f'{i}번에 금지어 "{w}"')
        if fnums:
            extra = nums(h + ' ' + ' '.join(ls) + ' ' + say) - fnums
            extra = {x for x in extra if len(x.replace(',', '').replace('.', '')) >= 2}
            if extra: bad.append(f'{i}번에 사실표에 없는 숫자 {sorted(extra)}')
    print(f'[대본 검사] {os.path.basename(path)} · 장면 {len(sc)}개')
    for b in bad: print('  X ' + b)
    for w in warn: print('  · ' + w)
    if not bad: print('  통과 — shorts.py로 만들면 된다')
    return 1 if bad else 0

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'spec'
    if cmd == 'check':
        sys.exit(check(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    facts = sys.argv[2] if len(sys.argv) > 2 else None
    topic = sys.argv[3] if len(sys.argv) > 3 else ''
    print(RULES)
    if topic: print('주제:', topic, '\n')
    if facts and os.path.exists(facts):
        print('=== 쓸 수 있는 숫자(여기 없는 수치는 넣지 않는다) ===')
        print(open(facts, encoding='utf-8').read()[:3000])
    print('\n대본을 쓴 뒤 반드시: py -3.12 work/shortscript.py check <대본.json> <facts파일>')
