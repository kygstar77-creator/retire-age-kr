# K-1 움직이는 판 셋 props (2026-11-03 motion) — shot_plan r09 '5% 넘은 날'(DaysOver) · r20+r21 '고정·변동 순서 바뀜'(CrossOver) · r29 '같은 쪽 달 점판'(SameDirDots)
#   over  = 1장 '이 금리가 처음 그 선에' ~ '그달 평균이 4.8%' 5줄
#   cross = 3장 '1년 동안 새로 받은 대출 금리를' ~ '올해 4월부터 순서가 바뀌어서' 5줄
#   dots  = 4장 '예를 들어 국채가 오른 달에' ~ '고정형 대출도 한국 3년 국채와는' 4줄
# 점·선은 raw 원자료(FRED DGS10·한은 ECOS) 그대로, 화면 숫자 글자는 facts.txt·calc*_out.txt에 있는 것만(assert). 새 계산 없음.
#   py -3.12 work/research/longform/ep/K-1/motion_preview/k1props.py → k1_motion.json (voice.json 생기면 그 길이로 다시 돌린다)
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md')
rd = lambda n: open(os.path.join(EP, n), encoding='utf-8').read()
SRC = rd('facts.txt') + rd('calc_out.txt') + rd('calc4_out.txt') + rd('calc5_out.txt')
def has(*ws):
    for w in ws: assert w in SRC, w
secs = SC.parse(script)
GAP_TRIM = 3   # 11/9 PD: B-31 쉼 — ../k1props.py GAP_TRIM과 같은 값
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
    return [{'text': t, 'frames': voice[t]['frames'] - GAP_TRIM if t in voice else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': voice[t]['audio'] if t in voice else None} for t in s[i:j + 1]]
def scene(key, title, sub, chapter, source, lines, data):
    return {'key': key, 'title': title, 'sub': sub, 'chapter': chapter, 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}

R = json.load(open(os.path.join(EP, 'raw', 'series.json'), encoding='utf-8'))
R2 = json.load(open(os.path.join(EP, 'raw', 'series_1103.json'), encoding='utf-8'))

# over — DGS10 일별 2023-01-03 ~ 2026-10-15(F1 끝날), 5% 이상 19일 · 처음 9/15 · 최고 5.31 10/5 · 2023.10 월평균 4.80(F11)
END = '2026-10-15'
days = sorted((d, v) for d, v in R['us_d'].items() if d <= END)
assert max(v for d, v in days if d < '2024') < 5   # '5%엔 못 닿음' 근거 = F1 '2023~ 5% 이상 처음 2026-09-15'
over = [i for i, (d, v) in enumerate(days) if v >= 5]
assert len(over) == 19 and days[over[0]][0] == '2026-09-15', (len(over), days[over[0]])
pk = max(range(len(days)), key=lambda i: days[i][1]); assert days[pk] == ('2026-10-05', 5.31), days[pk]
m23 = [v for d, v in days if d.startswith('2023-10')]; assert round(sum(m23) / len(m23), 2) == 4.8 or abs(R['us_m']['202310'] - 4.80) < 0.005, R['us_m']['202310']
has('2026-09-15 처음 5% 이상', '5% 이상 19일', '최고 5.31%(2026-10-05)', '월평균 4.80%(4.8%)')
oct23 = [i for i, (d, v) in enumerate(days) if d.startswith('2023-10')]
L1 = cut('1.', '이 금리가 처음 그 선에', '그달 평균이 4.8%')
assert len(L1) == 5, [l['text'] for l in L1]   # 0 9월 중순 · 1 열아홉 날 · 2 5.3% · 3 2023년 10월 · 4 4.8%
months = [(i, d[:4]) for i, (d, v) in enumerate(days) if d[5:7] == '01' and (i == 0 or days[i - 1][0][5:7] != '01')]
over_d = {'seed': 'K-1-over', 'v': [v for d, v in days], 'min': 3.2, 'max': 5.5, 'line': 5, 'lineText': '5%',
  'ticks': [3.5, 4, 4.5, 5], 'years': [{'i': i, 'text': y + '년'} for i, y in months],
  'first': {'i': over[0], 'text': '9월 15일', 'at': 0.15}, 'days': over, 'countText': '5% 이상인 날', 'countN': 19, 'countUnit': '일', 'countAt': 1.1,
  'peak': {'i': pk, 'text': '5.31% · 10월 5일', 'at': 2.2},
  'past': {'a': oct23[0], 'b': oct23[-1], 'name': '2023년 10월', 'below': '5%엔 못 닿음', 'text': '그달 평균 4.8%', 'at': 3.15, 'avg': 4.8, 'avgAt': 4.15}}

# cross — 한은 주담대 신규취급액 고정형·변동형 2025.09 ~ 2026.09(F6·F17)
ms = [m for m in sorted(R2['mfix']) if '202509' <= m <= '202609']; assert len(ms) == 13
fx = [R2['mfix'][m] for m in ms]; vr = [R2['mvar'][m] for m in ms]
assert (fx[0], fx[-1], vr[0], vr[-1]) == (3.94, 5.11, 4.08, 4.76), (fx, vr)
sw = next(i for i in range(len(ms)) if fx[i] > vr[i]); assert ms[sw] == '202604' and all(fx[i] < vr[i] for i in range(sw)) and all(fx[i] > vr[i] for i in range(sw, len(ms)))
has('고정형 3.94 → 5.11% (+1.17%p', '변동형 4.08 → 4.76% (+0.68%p', '2026.04 +0.06%p(올해 4월부터 순서 바뀜)', "2025.09 −0.14%p(1년 전엔 변동형이 더 비쌈)")
L2 = cut('3.', '1년 동안 새로 받은 대출 금리를', '올해 4월부터 순서가 바뀌어서')
assert len(L2) == 5, [l['text'] for l in L2]   # 0 같이 놓고 · 1 고정 1%p 넘게 · 2 변동 절반 · 3 1년 전 변동이 비쌈 · 4 4월부터
cross_d = {'seed': 'K-1-cross', 'months': [f"{int(m[4:])}월" if m[4:] != '01' else f"{m[2:4]}년 1월" for m in ms],
  'min': 3.6, 'max': 5.4, 'ticks': [4, 4.5, 5],
  'a': {'name': '고정형', 'v': fx, 'from': '3.94%', 'to': '5.11%', 'up': '+1.17%p', 'at': 1.1},
  'b': {'name': '변동형', 'v': vr, 'from': '4.08%', 'to': '4.76%', 'up': '+0.68%p', 'at': 2.1},
  'start': {'text': '1년 전엔 변동형이 더 비쌈', 'at': 3.15}, 'swap': {'i': sw, 'text': '4월부터 고정형이 더 비쌈', 'at': 4.1}, 'draw': 0.1}

# dots — 월 변화 방향(F23·calc4): 2013.02 ~ 2026.08 163달, calc.py와 같은 달 목록(네 줄 모두 있는 달)
mm = sorted(set(R['dep1']) & set(R['mfix']) & set(R['kr3']) & set(R['us_m']) & set(R['kr10']) & set(R['mvar']))
mm = [m for m in mm if '201301' <= m <= '202608']; assert len(mm) == 164, len(mm)
def marks(y, x):
    out = []
    for i in range(1, len(mm)):
        a = R[x][mm[i]] - R[x][mm[i - 1]]; b = R[y][mm[i]] - R[y][mm[i - 1]]
        out.append(1 if a * b > 0 else (-1 if a * b < 0 else 0))
    return out
dk = marks('dep1', 'kr3'); du = marks('dep1', 'us_m'); fk = marks('mfix', 'kr3'); fu = marks('mfix', 'us_m')
assert (dk.count(1), dk.count(-1), du.count(1), du.count(-1), fk.count(1), fk.count(-1), fu.count(1), fu.count(-1)) == (112, 43, 88, 63, 119, 35, 96, 51), (dk.count(1), du.count(1), fk.count(1))
has('예금1년 vs 한3년: 같은 쪽 112달', '예금1년 vs 미10년: 같은 쪽 88달', '주담대 고정 vs 한3년: 같은 쪽 119달', '주담대 고정 vs 미10년: 같은 쪽 96달', '미국 10년 96달(59%)')
L3 = cut('4.', '예를 들어 국채가 오른 달에', '고정형 대출도 한국 3년 국채와는')
assert len(L3) == 4, [l['text'] for l in L3]   # 0 예 · 1 한3년 일곱 · 2 미국 다섯 · 3 고정형
dots_d = {'seed': 'K-1-dots', 'first': mm[1], 'n': 163, 'legend': ['같은 쪽', '반대', '한쪽 그대로'], 'legendAt': 0.05,
  'left': {'name': '정기예금 · 한국 3년 국채', 'm': dk, 'same': 112, 'at': 1.05},
  'right': {'name': '정기예금 · 미국 10년 국채', 'm': du, 'same': 88, 'at': 2.05},
  'swap': {'name': '고정형 대출 · 한국 3년 국채', 'm': fk, 'same': 119, 'at': 3.05},
  'swapR': {'name': '고정형 대출 · 미국 10년 국채', 'm': fu, 'same': 96, 'at': 3.05}, 'unit': '163달 중'}   # 11/3 심사: 왼쪽만 바꾸면 '고정형 119 vs 예금 88'로 짝이 어긋남 → 오른쪽도 같은 고정형 기준(F23 96달)

out = {
  'over': scene('over', '미국 10년 국채금리, 하루하루', None, '1. 미국 국채금리 5%, 무슨 숫자인가', '미국 연준 FRED DGS10 · 2023.1.3~2026.10.15 일별 종가', L1, over_d),
  'cross': scene('cross', '새로 받은 주택담보대출 금리', None, '3. 내 대출 이자는 — 고정형과 변동형', '한국은행 ECOS 예금은행 신규취급액 가중평균 · 2025.9~2026.9 월별', L2, cross_d),
  'dots': scene('dots', '같은 쪽으로 움직인 달', None, '4. 미국 때문일까', '한국은행 ECOS · 미국 연준 FRED 월평균 · 2013.2~2026.8 달마다 전달 대비', L3, dots_d)}
json.dump(out, open(os.path.join(H, 'k1_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k, s in out.items(): print(k, s['frames'], 'f', round(s['frames'] / 30, 1), '초', [l['text'][:18] for l in s['lines']])
