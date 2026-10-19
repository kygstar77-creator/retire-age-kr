# T-1 2장 견본 방식 가로식 장면 셋 props (2026-10-19 motion, backlog '2년 살면 약 12배' — EqStack 세로 영수증과 다르게 EqRow 한 줄 식)
#   ratio = 2029년 두 사람 세금 나눗셈 2줄(1억 4,777만원 ÷ 1,241만원 = 11.9배)
#   year  = 한 해 더 살면 3줄(거주 2→3년, 3→4년 뺄셈 = 약 1,690만원)
#   gap   = 공제율 차이 3줄(지금 48% → 2029년 16% → 차이 32%p)
# 숫자 글자는 script.md(말·자막)·facts.txt·calc_out·calc_more_out에 있는 것만(assert). 새 계산 없음(뺄셈은 calc_more 값과 맞는지만 assert).
#   py -3.12 work/research/longform/ep/T-1/motion_preview/rowprops.py → t1_row.json
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
SRC = txt + ''.join(open(os.path.join(EP, n), encoding='utf-8').read() for n in ('facts.txt', 'calc_out.txt', 'calc_more_out.txt'))
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
    s = next(x for x in secs if x['title'].startswith(sec))['lines']
    i = next(k for k, t in enumerate(s) if t.startswith(a)); j = next(k for k, t in enumerate(s) if t.startswith(b))
    return [{'text': t, 'frames': voice[t]['frames'] if t in voice else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': voice[t]['audio'] if t in voice else None} for t in s[i:j + 1]]
def scene(key, title, sub, source, lines, data):
    return {'key': key, 'title': title, 'sub': sub, 'chapter': '2', 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}
V = lambda t, at, sub=None: {'t': t, 'at': at, **({'sub': sub} if sub else {})}
O = lambda t, at: {'t': t, 'op': True, 'at': at}
SRC_GOV = '재정경제부 2026 세법개정안 상세본 p.58·p.68 · 파이어맵 계산(지방세 포함)'

# ratio — 자막 '1억 4,777만원 ÷ 1,241만원 = 11.9배'
has('1억 4,777만원 ÷ 1,241만원 = 11.9배', '2029년 16%(8%×2)', '2027~2029년 1,241만원', '기본공제 250만원 → 2,500만원')
assert round(14777 / 1241, 1) == 11.9
L1 = cut('2.', '같은 2029년에 수현 씨', '두 사람이 열두 배 가까이')
assert len(L1) == 2, [l['text'] for l in L1]
ratio = {'seed': 'T-1-ratio', 'who': '정민 씨·수현 씨 · 가상 인물', 'note': '같은 20억 집 · 2029년에 판다면 · 정부안 · 지방세 포함',
  'rows': [{'label': '2029년 세금, 두 사람', 'parts': [V('1억 4,777만원', 0.12, '수현 씨 · 공제율 16% · 기본공제 250만원'), O('÷', 1.0),
            V('1,241만원', 1.08, '정민 씨 · 공제율 80% · 기본공제 2,500만원')], 'ans': '11.9배', 'reveal': 1.32}]}

# year — calc_more ④ 거주 2년 14,777 · 3년 13,088 · 4년 11,398 · 한 해 1,690
has('거주 2년 1억 4,777만원 → 3년 1억 3,088만원 → 4년 1억 1,398만원', '한 해에 약 1,690만원', '한 해 더 살면 1,690만원 줄어')
assert abs((14777 - 13088) - 1690) <= 1 and abs((13088 - 11398) - 1690) <= 1
L2 = cut('2.', '그럼 살았던 해 한 해는', '이 값은 집마다 달라요')
assert len(L2) == 3, [l['text'] for l in L2]
has('이 값은 집마다 달라요', '번 돈이 클수록 한 해의 값도 커집니다')
year = {'seed': 'T-1-year-b', 'who': '수현 씨 · 가상 인물', 'note': '20억·취득 8억·10년 보유 · 2029년 정부안 · 지방세 포함 · 파이어맵 계산',
  'rows': [{'label': '수현 씨 · 거주 2년 → 3년', 'parts': [V('1억 4,777만원', 0.25, '거주 2년'), O('−', 0.85), V('1억 3,088만원', 1.12, '거주 3년')], 'ans': '약 1,690만원', 'reveal': 1.72, 'ansSub': '한 해 더 살면 줄어드는 세금'}],
  'tail': {'at': 2.08, 'text': '집마다 다름 · 번 돈이 클수록 커짐'}}   # 10/19 Claude 심사: 3→4년 식(같은 1,690)을 '커집니다' 줄에 두면 '안 커졌는데?'로 읽힘 → 뺌

# gap — 자막 '수현 씨 = 보유 40% + 거주 8% = 48%' · '2029년 16%(8%×2)' · '차이 = 4 × (보유 − 거주) · 수현 씨 8년 차이 = 32%p'
has('보유 40% + 거주 8% = 48%', '2029년 16%(8%×2)', '차이 = 4 × (보유 − 거주)', '수현 씨 8년 차이 = 32%p', '48%가 16%로')
assert 40 + 8 == 48 and 8 * 2 == 16 and 4 * (10 - 2) == 32 == 48 - 16
L3 = cut('2.', '조심할 것도 있어요', '수현 씨는 여덟 해 차이라서')
assert len(L3) == 3, [l['text'] for l in L3]
gap = {'seed': 'T-1-gap', 'who': '수현 씨 · 가상 인물', 'note': '거주 2년 이상 · 보유·거주 모두 10년 이하일 때 · 정부안',
  'rows': [{'label': '수현 씨 지금 공제율 · 보유 10년·거주 2년', 'parts': [V('보유 40%', 0.3, '10년 × 4%'), O('+', 0.6), V('거주 8%', 0.68, '2년 × 4%')], 'ans': '48%', 'reveal': 0.9},
           {'label': '낮아지는 폭', 'parts': [V('4%p', 1.15, '한 해 차이마다'), O('×', 1.5), V('8년', 1.7, '보유 10년 − 거주 2년')], 'ans': '32%p', 'reveal': 2.12},
           {'label': '2029년 공제율', 'parts': [V('48%', 2.3, '지금'), O('−', 2.38), V('32%p', 2.44, '8년 차이')], 'ans': '16%', 'reveal': 2.62}]}

out = {'fps': 30,
 'ratio': scene('ratio', '같은 해, 세금은 몇 배?', '같은 20억 집 · 두 사람', SRC_GOV, L1, ratio),
 'year': scene('year', '살았던 한 해의 값', '수현 씨 집 · 2029년', '파이어맵 계산 · 정부안 공제율(상세본 p.58)', L2, year),
 'gap': scene('gap', '햇수 차이 한 해마다 4%p', '갖고 있던 해 − 살았던 해', '재정경제부 2026 세법개정안 상세본 p.58 · 소득세법 §95②', L3, gap)}
json.dump(out, open(os.path.join(H, 't1_row.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('ratio', 'year', 'gap'):
    s = out[k]; print(k, round(s['frames'] / 30, 1), 's · 녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '· 줄', [round(l['frames'] / 30, 1) for l in s['lines']])
