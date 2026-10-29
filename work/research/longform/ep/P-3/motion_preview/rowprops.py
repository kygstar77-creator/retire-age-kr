# P-3 가로식 장면 셋 props (2026-10-27 motion, backlog 'EqRow를 다음 롱폼 계산 줄에' — T-1과 다르게 plain(키 칸·검은 카드 없음)·seed·꼬리)
#   calc = 2장 보험료 식 3줄(167만원 × 절반 × 7.19% → 6만원 / + 장기요양 13.14% → 8천원 / 더하면 6만 8천원)  shot_plan r13·r14
#   rise = 2장 내년 연금 3줄(165만원 × 1.021 → 168만원 남짓 / 6만 8천원 × 12달 → 80만원 넘음 / 164만원 × 1.021 → 167.4만원) shot_plan r19·r20
#   mix  = 5장 이자·배당 합산 1줄(1,000만원 + 1,100만원 → 2,100만원, 꼬리 '탈락 · 매달 약 11만원')          shot_plan r32
# 숫자 글자는 script.md(말·자막)·calc_out.txt에 있는 것만(assert). 새 계산 없음(곱셈은 calc_out 값과 맞는지만 assert).
#   py -3.12 work/research/longform/ep/P-3/motion_preview/rowprops.py → p3_row.json (voice.json 생기면 그 길이로 다시 돌린다)
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
SRC = txt + open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
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
def scene(key, title, sub, chapter, source, lines, data):
    return {'key': key, 'title': title, 'sub': sub, 'chapter': chapter, 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}
V = lambda t, at, sub=None: {'t': t, 'at': at, **({'sub': sub} if sub else {})}
O = lambda t, at: {'t': t, 'op': True, 'at': at}

# calc — 자막 '1,670,000원 × 50% × 7.19% = 60,037원' · '60,037원 × 13.14% = 7,889원 · 합계 월 67,926원'
has('1,670,000원 × 50% × 7.19% = 60,037원', '60,037원 × 13.14% = 7,889원', '합계 월 67,926원', '6만원 정도', '8천원 정도', '6만 8천원쯤')
assert round(1670000 * 0.5 * 0.0719) == 60037 and round(60037 * 0.1314) == 7889 and 60037 + 7889 == 67926
L1 = cut('2.', '계산은 생각보다 단순해요', '둘을 더하면')
assert len(L1) == 7, [l['text'] for l in L1]   # 0 절반 · 1 7.19% · 2 6만원 · 3 장기요양 · 4 13.14% · 5 8천원 · 6 둘을 더하면
calc = {'seed': 'P-3-calc', 'plain': True, 'paper': False, 'heroOut': 0.55,   # 10/28 '지역가입자가 되어' 자리에서 167만원이 식 크기로(U5 3.0~11.0초 8.0초 → 쪼갬)
  'note': '재산 0 가정 · 2026년 요율 · 소득분만',
  'rows': [{'label': '건강보험료 · 연금 한 달 167만원', 'parts': [V('167만원', 0.33, '연금 한 달'), O('×', 0.7), V('절반', 0.78, '보험료 매길 땐'), O('×', 1.3), V('7.19%', 1.45, '보험료율')],
            'ans': '약 6만원', 'ansSub': '60,037원', 'reveal': 2.25},
           {'label': '장기요양보험료 · 같이 붙음', 'parts': [V('6만원', 3.35, '건강보험료'), O('×', 4.2), V('13.14%', 4.35, '장기요양')], 'ans': '약 8천원', 'ansSub': '7,889원', 'reveal': 5.3},
           {'label': '고지서 한 달', 'parts': [V('6만원', 6.0, '건강보험'), O('+', 6.15), V('8천원', 6.25, '장기요양')], 'ans': '약 6만 8천원', 'ansSub': '67,926원', 'reveal': 6.35}]}

# rise — 자막 '1,650,000원 × 1.021 = 1,684,650원 · 연 2,022만원' · '올해 164만원 × 1.021 = 167.4만원 · 연 2,009만원 → 탈락 / 163만원 → 연 1,997만원 → 유지'
has('월 68,521원 · 한 해 822,252원', '80만원이 넘어요')
assert 68521 * 12 == 822252
has('1,650,000원 × 1.021 = 1,684,650원', '연 2,022만원', '164만원 × 1.021 = 167.4만원', '연 2,009만원 → 탈락', '163만원 → 연 1,997만원 → 유지', '168만원을 조금 넘습니다', '올해는 2.1% 올랐어요')
assert round(1650000 * 1.021) == 1684650 and round(164 * 1.021, 1) == 167.4
L2 = cut('2.', '올해는 2.1% 올랐어요', '올해 월 164만원을')
assert len(L2) == 5, [l['text'] for l in L2]   # 0 2.1% · 1 168만원 · 2 그다음 해 탈락 · 3 80만원 · 4 164만원부터
rise = {'seed': 'P-3-rise', 'plain': True, 'paper': False, 'note': '가정 — 내년 인상률은 2027년 1월 발표 · 올해처럼 2.1%',
  'rows': [{'label': '올해 한 달 165만원 → 내년', 'parts': [V('165만원', 0.3, '올해'), O('×', 1.0), V('1.021', 1.1, '물가만큼 2.1%')], 'ans': '168만원 남짓', 'ansSub': '연 2,022만원 · 기준 위', 'reveal': 1.55},
           {'label': '그다음 해부터 · 한 해', 'parts': [V('약 6만 8천원', 2.15, '매달'), O('×', 3.0), V('12달', 3.1)], 'ans': '80만원 넘음', 'ansSub': '822,252원', 'reveal': 3.45},
           {'label': '올해 한 달 164만원이라면', 'parts': [V('164만원', 4.05, '올해'), O('×', 4.25), V('1.021', 4.3, '2.1%')], 'ans': '167.4만원', 'ansSub': '연 2,009만원 · 기준 위', 'reveal': 4.6}],
  'tail': {'at': 4.85, 'text': '163만원이면 연 1,997만원 · 기준 아래'}}

# mix — 자막 '연 1,000만원 + 1,100만원 = 2,100만원 → 탈락 · 월 108,464원'
has('연 1,000만원 + 1,100만원 = 2,100만원 → 탈락', '월 108,464원', '매달 11만원쯤', '1,100만원 있으면')
assert 1000 + 1100 == 2100
L3 = cut('5.', '예를 들어 연금이 한 해', '보험료는 연금의 절반에')
assert len(L3) == 4, [l['text'] for l in L3]   # 0 1,000만 · 1 1,100만 · 2 탈락 · 3 11만원
mix = {'seed': 'P-3-mix-c', 'plain': True, 'paper': False, 'note': '이자·배당 1천만원 넘으면 전부 더함 · 재산 0 · 소득분만',
  'rows': [{'label': '한 해 소득으로 셈', 'parts': [V('1,000만원', 0.35, '국민연금'), O('+', 1.05), V('1,100만원', 1.2, '이자·배당 전부')], 'ans': '2,100만원', 'ansSub': '기준 2,000만원 위', 'reveal': 1.7}],
  'tail': {'at': 2.1, 'text': '탈락', 'more': {'at': 3.92, 'text': '매달 약 11만원'}}}   # 10/28 '그러면 탈락이에요'에 먼저(U5)

# 10/28 제목 밑 sub 뺌 — 식·이름표와 같은 말이 작은 글자로 한 줄 더(no-claude '작은 글자 출처 포함 2줄') · 가정은 note 한 줄에 남김
out = {'fps': 30,
 'calc': scene('calc', '고지서 한 달은 얼마?', None, '2', '국민건강보험법 시행령 제44조 · 시행규칙 제44조 · 복지부 2025.11.4 · 파이어맵 계산', L1, calc),
 'rise': scene('rise', '아무것도 안 해도 넘는 자리', None, '2', '복지부 2026.1.9 · 파이어맵 계산', L2, rise),
 'mix': scene('mix', '1천만원을 넘으면 전부', None, '5', '국민건강보험법 시행규칙 제44조 · 파이어맵 계산', L3, mix)}
json.dump(out, open(os.path.join(H, 'p3_row.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('calc', 'rise', 'mix'):
    s = out[k]; print(k, round(s['frames'] / 30, 1), 's · 녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '· 줄', [round(l['frames'] / 30, 1) for l in s['lines']])
