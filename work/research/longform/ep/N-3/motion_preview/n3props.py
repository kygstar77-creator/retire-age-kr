# N-3 움직이는 판 넷 props (2026-10-29 motion · 11/1 blocks·stairs 더함) — shot_plan r19 '연금 상한 멈춤'(CapStop) · r37 '평균 깃발 끌려감'(MeanPull)
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
  'mid': {'v': 3417, 'label': '가운데쯤', 'text': '3,417만원', 'at': 2.15, 'stay': '그대로'},   # at 2.15 = '줄 한가운데' 자리(2.45는 U5 9.0초 — 회색 깃발이 4%를 못 넘김, 10/29)
  'top': {'label': '상위 1%', 'text': '평균 3억 4,630만원', 'at': 3.3, 'pull': 5.1},
  'gap': {'text': '약 1천만원 차이', 'at': 6.35}, 'rope': False}   # 11/11 심사: 1% 추→깃발 줄 빼기(1%는 차이의 29%, calc_mean_out) · '중간값'은 실제로 상위 50% 구간 평균 → '가운데쯤'

# blocks — 3장 r18 '보험료는 같은 비율, 소득세만 가파르게'(PayBlocks, 11/1) · calc_out 'A' 줄 공제 내역 ÷ 세전 월급(원 단위 그대로 나눔, % 글자 = 같은 나눗셈)
ded = {}
for m in re.finditer(r'연봉 ([\d,]+)만 \| 월 세전 ([\d,]+) \| 공제 [\d,]+ \(연금 ([\d,]+)·건강 ([\d,]+)·요양 ([\d,]+)·고용 ([\d,]+)·소득세 ([\d,]+)·지방 ([\d,]+)\)', CALC):
    k = int(m.group(1).replace(',', '')); v = [int(x.replace(',', '')) for x in m.groups()[1:]]
    ded.setdefault(k, v)
bk = [3000, 5000, 7000, 8000]
assert all(k in ded and pen[k] < CAP for k in bk), '블록 칸은 연금 상한 아래만(같은 비율이 깨지지 않게)'
assert all(ded[k][1] == pen[k] for k in bk)
has('세금이 보험료보다 많아지는 건 연봉 8천 칸부터예요.', '보험료 네 가지는 월급에 같은 비율로 붙고, 소득세만 많이 벌수록 더 가파르게 붙습니다.')
L3 = cut('3.', '세금이 보험료보다 많아지는 건', '보험료 네 가지는')
assert len(L3) == 2, [l['text'] for l in L3]
blocks = {'seed': 'N-3-blocks', 'insLabel': '보험료 넷', 'taxLabel': '소득세', 'axis': '연봉별 · 세전 월급 중 빠지는 비율(%)',
  'insAt': 0.05, 'taxAt': 0.5, 'flatAt': 1.0, 'steepAt': 1.5, 'circleAt': 0.8,   # 11/4 첫 줄 '8천 칸부터' 끝에 8천 동그라미
  'cols': [{'label': name(k), 'ins': [round(x / ded[k][0], 5) for x in ded[k][1:5]], 'tax': round((ded[k][5] + ded[k][6]) / ded[k][0], 5),
           'insPct': f'{sum(ded[k][1:5]) / ded[k][0] * 100:.1f}%', 'taxPct': f'{(ded[k][5] + ded[k][6]) / ded[k][0] * 100:.1f}%'} for k in bk]}   # % 글자 = calc_out 원 단위 나눗셈만(11/1 심사: % 없이는 금액으로 오독)

# stairs — 5장 r28 거꾸로 계단(RaiseStairs, 11/1) · calc_out 'I' 줄 통장 목표별 필요 연봉 · 칸 사이 차 = research 대조 표 1,580·1,650·1,770
need = {int(m.group(1).replace(',', '')) // 10000: int(m.group(2).replace(',', '')) for m in re.finditer(r'통장 월 ([\d,]+) → 연봉 ([\d,]+)만', CALC)}
assert need.get(400) == 5680 and need.get(500) == 7330 and need.get(600) == 9100, need
P300 = 4100; has('연봉 4,100만원쯤이 필요합니다.', '칸 사이 연봉 차 · 300→400 +1,580만원 · 400→500 +1,650만원 · 500→600 +1,770만원')
gl = [need[400] - P300, need[500] - need[400], need[600] - need[500]]; assert gl == [1580, 1650, 1770], gl
L4 = cut('5.', '통장 400만원이면', '통장을 같은 100만원씩')
assert len(L4) == 10, [l['text'] for l in L4]   # 0 400 · 1 5,680 · 2 500 · 3 7,330 · 4 600 · 5 9,100 · 6 칸 사이 · 7 1,580 · 8 1,770 · 9 같은 100만원씩
won = lambda v: f'{v:,}만원'
stairs = {'seed': 'N-3-stairs', 'axis': '통장 한 달 목표 → 필요한 연봉', 'gapAt': 6.3, 'unitAt': 9.05,
  'steps': [{'goal': '통장 300만원', 'pay': won(P300), 'v': P300, 'at': 0, 'openAt': 0}] +
           [{'goal': f'{g}만원', 'pay': won(need[g]), 'v': need[g], 'at': 2 * i + 0.05, 'openAt': 2 * i + 1.1} for i, g in enumerate([400, 500, 600])],
  'gaps': [{'text': '+' + won(gl[0]), 'at': 7.3}, {'text': '+' + won(gl[1]), 'at': 7.75}, {'text': '+' + won(gl[2]), 'at': 8.35}]}

out = {'fps': 30,
 'cap': scene('cap', '국민연금에는 끝이 있다', None, '3', '국민연금법 · 국민연금공단 기준소득월액 상한(2026.7~2027.6) · 파이어맵 계산', L1, cap),
 'blocks': scene('blocks', '보험료는 같은 비율, 소득세는 가파르게', None, '3', '국민연금법 · 국민건강보험법·노인장기요양보험법·고용보험료징수법 시행령 · 소득세법 시행령 간이세액표 · 파이어맵 계산', L3, blocks),
 'stairs': scene('stairs', '같은 100만원, 더 높아지는 계단', None, '5', '소득세법 시행령 간이세액표 · 4대 보험 법령 요율 · 파이어맵 계산(1인·식대 비과세 월 20만원)', L4, stairs),
 'mean': scene('mean', '평균은 위쪽으로 쏠린다', None, '7', '국세청 근로소득 천분위(2024년 귀속, 2,108만 명) · 파이어맵 계산', L2, mean)}
json.dump(out, open(os.path.join(H, 'n3_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('cap', 'mean', 'blocks', 'stairs'):
    s = out[k]; print(k, round(s['frames'] / 30, 1), 's · 녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '· 줄', [round(l['frames'] / 30, 1) for l in s['lines']])
