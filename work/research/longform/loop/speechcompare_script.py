# 대본(script.md 형식) 한 편을 speechcompare.py와 같은 잣대로 잰다 — 2026-10-03 클라우드 R-1 재작업(cloud/r1-remake-1003)
#   python3 work/research/longform/loop/speechcompare_script.py ep/R-1/script.md ep/R-1/script.v6.md [--json]
# 숫자 밀도·숫자 2개 이상 문장 %는 speechcompare.py의 m() 함수를 그대로 불러 쓴다(파일을 고치지 않고 함수 정의만 읽어 온다 —
# speechcompare.py는 불러오면 바로 표를 찍는 스크립트라서). 경쟁 자막 12편과 같은 정규식이라 값끼리 바로 비교된다.
# 읽는 줄: '## '로 장, '- '로 시작하는 줄이 말하는 문장(lfvoice.sections와 같은 규칙). 끝의 '(화면: …)'은 뺀다.
# 읽지 않는 줄: '  (화면: …)', '  [자막: …]' — 화면에만 나오는 글자라 말하기 지표에 넣지 않는다.
# 길이 = 말하는 글자(한글+숫자, lfvoice.syl과 같음, 영문 약어는 lfvoice.speak로 한글 읽기로 바꾼 뒤) ÷ 5.65음절/초(RULES '목소리 한결같음' Charon 고정 속도).
# 숫자를 읽는 소리 길이(lfvoice.est)로 잰 길이도 같이 낸다(참고 — '1,573만'은 글자 4개지만 읽으면 '천오백칠십삼만' 7음절).
import ast, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
RATE = 5.65

def _load(src_file, names):
    tree = ast.parse(open(src_file, encoding='utf-8').read())
    ns = {'re': re, 'json': json, 'os': os}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.Assign)) and (getattr(node, 'name', None) in names or (isinstance(node, ast.Assign) and any(getattr(t, 'id', None) in names for t in node.targets))):
            exec(compile(ast.Module(body=[node], type_ignores=[]), src_file, 'exec'), ns)
    return ns

_sc = _load(os.path.join(HERE, 'speechcompare.py'), {'m', 'subs'})
metrics = _sc['m']            # speechcompare.m(text) -> dict
subs_text = _sc['subs']       # speechcompare.subs(json3 file) -> text
_lv = _load(os.path.join(WORK, 'lfvoice.py'), {'SAY', 'syl', 'nkr', 'est'})
SAY, syl, est = _lv['SAY'], _lv['syl'], _lv['est']

def speak(t):
    for a, b in sorted(SAY, key=lambda p: -len(p[0])): t = t.replace(a, b)
    return t

def parse(path):
    """script.md → [{'title', 'lines': [말하는 문장], 'captions': [자막]}]"""
    body = open(path, encoding='utf-8').read().split('\n---', 1)[0]
    out, cur = [], None
    for line in body.splitlines():
        if line.startswith('## '):
            cur = {'title': line[3:].strip(), 'lines': [], 'captions': []}; out.append(cur)
        elif cur is not None and line.lstrip().startswith('- '):
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip()
            t = re.sub(r'\s*\[자막:.*?\]', '', t).strip()
            if t: cur['lines'].append(t)
        elif cur is not None and line.strip().startswith('[자막:'):
            cur['captions'].append(line.strip()[4:-1].strip() if line.strip().endswith(']') else line.strip()[4:].strip())
    return out

def spoken(path):
    return ' '.join(l for s in parse(path) for l in s['lines'])

def sentences(t):     # speechcompare.m과 같은 문장 자르기
    return [x.strip() for x in re.split(r'(?<=[.?!])\s+', t) if len(x.strip()) > 3]

NUM = re.compile(r'\d[\d,.]*')
def measure(path):
    t = spoken(path)
    r = metrics(t)
    sy = syl(speak(t)); es = est(speak(t))
    r.update({'단어수': len(t.split()), '숫자개수': len(NUM.findall(t)), '말하는 글자(한글+숫자)': sy,
              '예상 길이(분, 글자÷5.65)': round(sy / RATE / 60, 2), '참고: 읽는 음절 길이(분)': round(es / RATE / 60, 2)})
    return r

def offenders(path):  # 숫자 2개 이상 문장 목록(고칠 곳 찾기)
    return [s for s in sentences(spoken(path)) if len(NUM.findall(s)) >= 2]

TARGET = {'숫자/1000단어': 90, '숫자 2개 이상 문장 %': 20, '분': (12, 15)}
def passes(r):
    return r['숫자/1000단어'] <= TARGET['숫자/1000단어'] and r['숫자 2개 이상 문장 %'] <= TARGET['숫자 2개 이상 문장 %'] \
        and TARGET['분'][0] <= r['예상 길이(분, 글자÷5.65)'] <= TARGET['분'][1]

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    rows = [(a, measure(a)) for a in args]
    if '--json' in sys.argv: print(json.dumps(dict(rows), ensure_ascii=False, indent=1)); sys.exit(0)
    keys = list(rows[0][1])
    print('| 대본 | ' + ' | '.join(keys) + ' | 목표 통과 |'); print('|' + '---|' * (len(keys) + 2))
    for n, r in rows: print(f'| {os.path.basename(n)} | ' + ' | '.join(str(r[k]) for k in keys) + f" | {'통과' if passes(r) else '미달'} |")
    if '--why' in sys.argv:
        for n, _ in rows:
            print(f'\n## {n} 숫자 2개 이상 문장'); [print('-', s) for s in offenders(n)]
