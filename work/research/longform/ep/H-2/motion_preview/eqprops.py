# H-2 5장 '사려면 현금이 얼마나' 견본 방식 장면 셋 props (2026-10-18 motion, 순돌이 10/18 [지시] 견본 방식)
#   rule = 대출 규칙 5줄(LoanSteps phase rule: 집값 축 위 한도 선이 줄마다 한 칸씩 그려짐 — 40% 경사 → 15억 6억 → 25억 4억 → 그 위 2억)
#   cash = 손품 씨 계산서 5줄(EqStack ledger: 집값 − 대출 − 보증금 = ? → 단지마다 답이 열리고 손 동그라미, 지난 답은 회색 칩)
#   edge = 25억 경계 3줄(LoanSteps phase edge: 25억 언저리 확대, 점이 넘는 순간 4억 → '?' → 2억)
# 숫자 글자는 facts.txt·calc_out.txt·script.md(말·자막)에 있는 것만(assert). 새 계산은 뺄셈 셋뿐이고 대본 [자막] 값과 맞는지 assert.
# 길이: voice.json에 같은 문장이 있으면 그 녹음 프레임, 없으면 P-1 녹음 속도 어림 — 다시 녹음(10/18 지시) 뒤 이 파일을 다시 돌린다.
#   py -3.12 work/research/longform/ep/H-2/motion_preview/eqprops.py → h2_eq.json
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
SRC = txt + facts + calc
def has(*ws):
    for w in ws: assert w in SRC, w
secs = SC.parse(script)
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
    elif s.startswith('[자막:') and last and last not in caps: caps[last] = s[4:].rstrip(']').strip()
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
    out = []
    for t in s[i:j + 1]:
        v = voice.get(t)
        out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': v['audio'] if v else None})
    return out
def scene(key, title, sub, chapter, source, lines, data):
    return {'key': key, 'title': title, 'sub': sub, 'chapter': chapter, 'source': source, 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 12, 'data': data}
def eok(x):  # 34.15 → '34억 1,500만원'
    e = int(x); m = round((x - e) * 10000)
    return f'{e}억' + (f' {m:,}만원' if m else '')

# 대출 규칙(facts R1·R7)
has('LTV 규제지역 40%', '15억원 이하 6억원', '15~25억원 4억원', '25억원 초과 2억원', '집값의 40%까지', '둘 중 작은 쪽까지만', '15억 이하면 6억까지', '25억까지는 4억', '25억이 넘으면 2억까지')
L1 = cut('5.', '먼저 대출 규칙입니다', '25억이 넘으면 2억까지입니다')
assert len(L1) == 5, [l['text'] for l in L1]
rule = {'seed': 'H-2-rule', 'xMax': 40, 'yMax': 8, 'ltv': 0.4, 'ltvText': '집값의 40%',
  'caps': [[15, 6, '6억'], [25, 4, '4억'], [99, 2, '2억']], 'xTicks': [[15, '15억'], [25, '25억'], [35, '35억']],
  'xName': '집값', 'yName': '주택담보대출 한도', 'minText': '둘 중 작은 쪽',
  # 줄 → 일: 0 축·40% 경사 · 1 금액 한도 점선 덮개(작은 쪽만 진하게) · 2 15억 이하 6억 · 3 25억까지 4억 · 4 그 위 2억
  'show': ['ltv', 'min', 'cap0', 'cap1', 'cap2'], 'phase': 'rule'}

# 손품 씨 계산서 — 매매 가운데 값(calc_out) − 주담대 2억 − 보증금 9.5억 = [자막] 값
L2 = cut('5.', '이제 손품 씨 돈으로 계산합니다', '래미안원베일리 약 59억이면')
assert len(L2) == 5, [l['text'] for l in L2]
cash_rows = []
for name, short, x in [('리센츠', '리센츠', 34.15), ('주공아파트5단지', '주공5단지', 43.45), ('래미안원베일리', '래미안원베일리', 59.00)]:
    has(f'{name}(건축', f'중앙 {x:.2f}억')
    need = round(x - 2 - 9.5, 2); a, b = eok(x), eok(need)
    cap = caps[L2[4]['text']]
    assert f'{short} {a} → {b}' in cap or f'{short} {a.replace("억 ", "억 ")} → {b}' in cap, (short, a, b)
    cash_rows.append({'name': short, 'price': a, 'ans': b})
has('보증금 9억 5,000만원', '주담대 2억', '취득세·중개보수 빼고 계산')
cash = {'seed': 'H-2-cash', 'layout': 'ledger', 'baseLabel': '84㎡대 가운데 값', 'blank': '집값',
  'terms': [{'op': '−', 'label': '주택담보대출', 'v': '2억', 'at': 0}, {'op': '−', 'label': '돌려받는 전세 보증금', 'v': '9억 5,000만원', 'at': 1}],
  'ansLabel': '더 있어야 하는 돈', 'rounds': [{'at': 2 + i, **r} for i, r in enumerate(cash_rows)],
  'revealQ': [0.62, 0.6, 0.55],   # 줄 안에서 답이 열리는 자리(말이 답 숫자에 닿는 쯤 — '22억 넘게'·'32억쯤'·'47억 넘게'가 줄 뒤쪽)
  'note': '취득세·중개보수 빼고 계산', 'who': '손품 씨 · 가상 인물'}

# 25억 경계
L3 = cut('5.', '여기서 조심할 건 25억이라는 선입니다', '그래서 25억 언저리 집을 볼 땐')
assert len(L3) == 3, [l['text'] for l in L3]
has('25억 이하면 한도가 4억', '절반인 2억', '은행이 그 집 값을 얼마로 보는지')
edge = {**rule, 'seed': 'H-2-edge', 'phase': 'edge', 'show': ['line', 'jump', 'ask'], 'edgeLo': '4억', 'edgeHi': '2억', 'half': '절반',
  'ask': '은행이 보는 이 집 값은?'}

SRCL = '금융위원회 2025-10-15 대책 · 2026-08-13 금융 종합대책 · LTV 규제지역 40%'
out = {'fps': 30,
 'rule': scene('rule', '대출은 둘 중 작은 쪽까지', '집값의 40% · 금액 한도 · 규제지역', '5', SRCL, L1, rule),
 'cash': scene('cash', '손품 씨 계산서', '매매 가운데 값 − 대출 − 보증금', '5', '국토교통부 실거래가 84㎡대 1년 가운데 값 · 금융위원회 주담대 한도 · 취득세·중개보수 빼고 계산', L2, cash),
 'edge': scene('edge', '25억이라는 선', '조금만 넘어도 한도가 절반', '5', SRCL, L3, edge)}
json.dump(out, open(os.path.join(H, 'h2_eq.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for k in ('rule', 'cash', 'edge'):
    s = out[k]; print(k, s['frames'], 'f', round(s['frames'] / 30, 1), 's', '녹음 줄', sum(1 for l in s['lines'] if l['audio']), '/', len(s['lines']), '최장 줄', round(max(l['frames'] for l in s['lines']) / 30, 1), 's')
