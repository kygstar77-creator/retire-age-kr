# N-3 움직이는 판 둘 props (2026-10-29 motion) — shot_plan r19 '연금 상한 멈춤'(CapStop) · r37 '평균 깃발 끌려감'(MeanPull)
#   cap  = 3장 '그런데 국민연금에는 끝이 있어요' ~ '이게 다음 장에서' 5줄
#   mean = 7장 '평균도 마찬가지예요' ~ "그래서 '평균 연봉'은" 7줄
# 숫자 글자는 script.md(말)·calc_out.txt·research.md 대조 표에 있는 것만(assert). 새 계산 없음(빼기 1,058 → '약 1천만원'은 말 그대로).
#   py -3.12 work/research/longform/ep/N-3/motion_preview/n3props.py → n3_motion.json (voice.json 생기면 그 길이로 다시 돌린다)
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md')
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
RES = open(os.path.join(EP, 'research.md'), encoding='utf-8').read()
SRC = open(script, encoding='utf-8').read() + CALC + RES
def has(*ws):
    for w in ws: assert w in SRC, w
secs = SC.parse(script)
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(EP, '..', 'P-1', 'motion_preview', 'p1_timing.json'), encoding='utf-8'))['spf']
def cut(sec, a, b):
    s = next(x for x in secs if x['title'].lstrip('[').startswith(sec))['lines']
    i = next(k for k, t in enumerate(s) if t.startswith(a)); j = next(k for k, t in enumerate(s) if t.startswith(b))
    return [{'text': t, 'frames': voice[t]['frames'] if t in voice else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': voice[t]['audio'] if t in voice else None} for t in s[i:j + 1]]
def scene(key, title, sub, chapter, source, lines, data):
    return {'key': key, 'title': title, 'sub': sub, 'chapter': chapter, 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}

# cap — 연봉별 국민연금(내 몫) 한 달, calc_out 'A' 줄·'J' 줄의 '연금 N' 값 그대로
import re
pen = {}
for m in re.finditer(r'연봉 ([\d,]+)만 \| 월 세전[^\n]*?연금 ([\d,]+)', CALC):
    pen[int(m.group(1).replace(',', ''))] = int(m.group(2).replace(',', ''))
want = [3000, 4000, 5000, 6000, 7000, 8000, 10000, 12000, 15000]
assert all(k in pen for k in want), pen
CAP = 313020   # 659만원 × 4.75%, 10원 미만 버림(research 대조 표 313,020)
assert 6590000 * 475 // 10000 // 10 * 10 == CAP and pen[10000] == pen[12000] == pen[15000] == CAP and pen[8000] < CAP
has('세전 월급', '그러니까 중간값은', '연금은 한 달 659만원까지만 보험료를 붙입니다.', '31만원 정도에서 더 늘지 않습니다.', '기준소득월액 상한 659만원(2026.7~2027.6')
L1 = cut('3.', '그런데 국민연금에는 끝이 있어요', '이게 다음 장에서')
assert len(L1) == 5, [l['text'] for l in L1]   # 0 끝 · 1 659만원 · 2 높은 칸 · 3 31만원 · 4 다음 장
name = lambda k: {10000: '1억', 12000: '1억 2천', 15000: '1억 5천'}.get(k, f'{k // 1000}천')
low = [k for k in want if pen[k] < CAP]; top = [k for k in want if pen[k] >= CAP]
cap = {'seed': 'N-3-cap', 'cap': CAP, 'capLabel': '연금은 월급 659만원까지만', 'capAt': 1.15, 'stopText': '31만원에서 멈춤', 'stopAt': 3.1,
  'axis': '연봉별 · 국민연금 보험료(내 몫) 한 달',
  'bars': [{'label': name(k), 'v': pen[k], 'at': 0.08 + i * 0.13} for i, k in enumerate(low)] + [{'label': name(k), 'v': pen[k], 'at': 2.1 + i * 0.22} for i, k in enumerate(top)]}

# mean — 국세청 2024년 귀속(S1) · 평균 4,475 · 상위 50% 구간 평균 3,417 · 상위 1% 평균 3억 4,630만원
has('전체 평균 4,475', '상위 50% 구간 평균 3,417만', '3억 4,630만원', '국세청 자료에서 직장인 평균 총급여는 4,475만원입니다.', '평균 3억 5천만원 가까이 벌어요.', "1천만원쯤 높게 나와요")
assert 1000 <= 4475 - 3417 < 1100
L2 = cut('7.', '평균도 마찬가지예요', "그래서 '평균 연봉'은")
assert len(L2) == 7, [l['text'] for l in L2]   # 0 마찬가지 · 1 4,475 · 2 중간값 · 3 상위 1% · 4 3억 5천 · 5 끌어올려요 · 6 1천만원
mean = {'seed': 'N-3-mean', 'xMax': 6000, 'ticks': [0, 1000, 2000, 3000, 4000, 5000, 6000], 'unit': '한 해 총급여 · 만원',
  'mean': {'v': 4475, 'label': '평균', 'text': '4,475만원', 'at': 1.25},
  'mid': {'v': 3417, 'label': '중간값', 'text': '3,417만원', 'at': 2.15, 'stay': '그대로'},   # at 2.15 = '줄 한가운데' 자리(2.45는 U5 9.0초 — 회색 깃발이 4%를 못 넘김, 10/29)
  'top': {'label': '상위 1%', 'text': '평균 3억 4,630만원', 'at': 3.3, 'pull': 5.1},
  'gap': {'text': '약 1천만원 차이', 'at': 6.35}}

out = {'fps': 30,
 'cap': scene('cap', '국민연금에는 끝이 있다', None, '3', '국민연금법 · 국민연금공단 기준소득월액 상한(2026.7~2027.6) · 파이어맵 계산', L1, cap),
 'mean': scene('mean', '평균은 위쪽으로 쏠린다', None, '7', '국세청 근로소득 천분위(2024년 귀속, 2,108만 명) · 파이어맵 계산', L2, mean)}
json.dump(out, open(os.path.join(H, 'n3_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('cap', 'mean'):
    s = out[k]; print(k, round(s['frames'] / 30, 1), 's · 녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '· 줄', [round(l['frames'] / 30, 1) for l in s['lines']])
