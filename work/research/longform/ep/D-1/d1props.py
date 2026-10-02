# D-1 화면 재료 — script.md(장·문장) + voice.json(있으면 길이) + facts.txt → work/video/d1.json (Remotion D1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/D-1/d1props.py
# 숫자는 전부 facts.txt에서 뽑고, 공식([1][3][9][10])으로 다시 계산해 [계산] 줄과 기계 대조한다 — 어긋나면 화면을 만들지 않는다.
# 목소리가 없는 문장은 초당 5.5음절(RULES 목소리 규칙 2 목표)로 길이를 어림해 화면만 본다(리허설). 업로드는 missing=0일 때만.
# 장면은 제목 열쇠말로 찾고, 문장 시점은 '그 문장에 든 말'로 찾는다(e1props.py와 같은 방식).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK)
import lfvoice
FPS = 30

FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
def need(s, where=FACTS, name='facts'):
    assert s in where, f'{name}에 없음: {s}'
    return s

# ── 사실표에서 숫자 뽑기 ──
need('"1만분의 719" = 7.19%'); RATE = 719                      # 1만분의 719
need('211.5원'); PT = 211.5
need('건강보험료 × 0.9448 ÷ 7.19'); need('건보료의 13.14%'); LTC = 0.9448
FLOOR = int(re.search(r'지역 월 보험료 하한 ([\d,]+)원', FACTS).group(1).replace(',', ''))
assert FLOOR == 20160
TABLE = [(int(a.replace(',', '')), int(b.replace(',', ''))) for a, b in re.findall(r'연 금융소득 ([\d,]+)만원:.*?= ([\d,]+)원', FACTS)]
assert [t[0] for t in TABLE] == [900, 1000, 1001, 1200, 2000, 3000], TABLE
PEN = {}
for k, pat in (('pen', r'국민연금 월 150만원\(연 1,800만원.*?= ([\d,]+)원'), ('pen1000', r'국민연금 월 150만원 \+ 금융 1,000만원: ([\d,]+)원'),
               ('pen1001', r'국민연금 월 150만원 \+ 금융 1,001만원:.*?= ([\d,]+)원')):
    PEN[k] = int(re.search(pat, FACTS).group(1).replace(',', ''))

# ── 공식으로 다시 계산해 대조(10원 미만 버림, [9] 소득분이 하한보다 작으면 하한) ──
from fractions import Fraction as Fr
def f10(x): return int(x // 10 * 10)
def premium(income_man):   # 분수로 계산(부동소수 오차로 10원 버림이 틀어지지 않게)
    hp = max(FLOOR, f10(Fr(income_man * 10000, 12) * Fr(RATE, 10000))) if income_man else FLOOR
    return hp + f10(hp * Fr(str(LTC)) / Fr(RATE, 100))
for inc, v in TABLE:
    reflected = inc if inc > 1000 else 0
    assert premium(reflected) == v, (inc, premium(reflected), v)
assert premium(900) == PEN['pen'] == PEN['pen1000'], PEN
assert premium(900 + 1001) == PEN['pen1001'], PEN
T = dict(TABLE)
JUMP = T[1001] - T[1000]; JUMP_Y = JUMP * 12
PJUMP = PEN['pen1001'] - PEN['pen']; PJUMP_Y = PJUMP * 12
need(f'월 {JUMP:,}원 더'); need(f'연 {JUMP_Y:,}원'); need(f'월 {PJUMP:,}원 더'); need(f'연 {PJUMP_Y:,}원')
for s in ('5억4천만원 이하', '9억원 이하이면서 연 소득 1천만원 이하', '연 2,000만원 이하', '36개월', '1억 원이 공제', '{보증금 + (월세 × 40)} × 30%', '6월 1일 기준'):
    need(s)
# 읽기 표기 → 화면 표기 대조(대본이 사실표와 같은 수를 말하는지)
READ = {22800: '2만 2,800원', 67850: '6만 7,850원', 81340: '8만 1,340원', 135570: '13만 5,570원', 203370: '20만 3,370원',
        61000: '6만 1,000원', 128860: '12만 8,860원', 67860: '6만 7,860원', 814320: '81만 4,320원', 20160: '2만 160원'}
for n, r in READ.items(): need(r, SCRIPT, 'script.md')
assert f'{JUMP // 10000}만 {JUMP % 10000:,}원' == '4만 5,050원'
won = lambda v: f'{v:,}원'
man = lambda v: f'{v:,}만원'
kr = lambda v: f'{v // 10000}만 {v % 10000:,}원' if v % 10000 else f'{v // 10000}만원'

# ── 출처 줄(script.md '숫자 출처' 절과 facts 머리의 원문 이름) ──
S_LAW = '국민건강보험법 시행령(대통령령 제36675호)·시행규칙(보건복지부령 제1202호) — 국가법령정보센터'
S_CALC = '국민건강보험공단 지역보험료 모의계산 안내문'
S_OURS = '우리 계산(재산 0·다른 소득 0, 장기요양 포함 월액, 10원 미만 버림)'
SRC = {
    'open': f'시행규칙 제44조① 단서 · 시행령 제44조 · 고시 제2025-222호(하한) · {S_CALC} · {S_OURS}',
    'agenda': f'{S_LAW} · {S_CALC}',
    'fork': '국민건강보험공단 피부양자 소득·재산요건 안내 · 국민건강보험법 시행령 제42조①(재산) · ' + S_CALC,
    'formula': f'국민건강보험법 시행령 제44조①②(7.19%·211.5원) · {S_CALC}(계산식·장기요양 0.9448%) · 시행령 제41조①(소득 종류)',
    'statute': '국민건강보험법 시행규칙 제44조① 단서(보건복지부령 제1202호, 2026. 9. 28. 시행) — 국가법령정보센터',
    'cliff': f'시행규칙 제44조① · 시행령 제44조 · 보건복지부고시 제2025-222호(하한 20,160원, 법제처 생활법령) · {S_CALC} · {S_OURS}',
    'etf': '소득세법 제17조①5호 · 소득세법 시행령 제26조의2④(대통령령 제36737호) — 국가법령정보센터',
    'pension': f'시행규칙 제44조②(연금·근로 50%) · 시행규칙 제44조① 단서 · {S_CALC} · {S_OURS}',
    'calendar': f'국민건강보험법 시행령 제41조③ · {S_CALC}',
    'check': '국민건강보험공단 피부양자 소득요건·재산요건 안내(2026-10-01 확인)',
    'band': '국민건강보험법 시행령 제77조① · 국민건강보험공단 보험료 모의계산(임의계속보험료 메뉴)',
    'property': f'국민건강보험법 시행령 제42조① · {S_CALC}(6월 1일 과세표준·1억원 공제·전월세 환산)',
    'steps': '국민건강보험공단 홈페이지 보험료 모의계산 → 지역보험료(nhis.or.kr) 화면 안내문',
    'summary': f'{S_LAW} · 소득세법 시행령 제26조의2④ · {S_CALC} · 공단 피부양자 안내',
    'calc': '파이어맵 은퇴 나이 계산기(firemap.kr) · 건보료 숫자는 2026년 법령·공단 계산식 기준',
}
TAG = '예시 조건: 지역가입자 1인 · 재산 0 · 2026년 기준'
RAIL = ['계산식', '1,000만원 경계', '연금', '반영 시기', '피부양자·확인']
assert '계산식 · 1,000만원 경계 · 연금 · 반영 시기 · 피부양자·확인' in SCRIPT
CLIFF = [[f'{a:,}만', v] for a, v in TABLE]

SPEC = [
    ('여는', lambda L: dict(kind='open', source=SRC['open'], data={
        'cards': [[man(1000), T[1000]], [man(1001), T[1001]]], 'diff_y': JUMP_Y, 'pen_y': PJUMP_Y,
        'label': '1년 배당+이자', 'unit': '월 건보료',
        'at': [L('1,000만원인 사람이'), L('매달 얼마'), L('1,000만원이면 월'), L('1만원 더 받았을'), L('월 150만원씩'), L('법령 원문')]})),
    ('로고', lambda L: dict(kind='logo', tag=False, data={'sub': '은퇴 나이, 숫자로'})),
    ('다섯 가지', lambda L: dict(kind='agenda', title='오늘 볼 다섯 가지', source=SRC['agenda'], data={'items': RAIL,
        'at': [L('다섯 가지를'), L('먼저 지역'), L('이어서 국민연금')]})),
    ('무엇이 바뀌나', lambda L: dict(kind='fork', title='퇴직하면 길이 갈립니다', sub='건강보험 자격 — 피부양자 또는 지역가입자', source=SRC['fork'],
        data={'at': [L('회사에 다닐'), L('길이 갈립'), L('피부양자로 들어가면'), L('지역가입자가 되고'), L('오늘 계산은')]})),
    ('계산식', lambda L: dict(kind='formula', rail=1, title='지역 건보료 계산식 한 줄', sub='2026년 요율 · 공단 모의계산 화면의 식 그대로', source=SRC['formula'],
        data={'rate': RATE / 100, 'pt': PT, 'ltc': '13.14%', 'kinds': ['이자', '배당', '사업', '근로', '연금', '기타소득'],
              'at': [L('모의계산 화면에'), L('12로 나눠'), L('211.5원씩'), L('장기요양보험료가'), L('올해 보험료율'), L('소득에 들어가는'), L('똑같이 다')]})),
    ('경계:law', lambda L: dict(kind='statute', rail=2, title='금융소득 1,000만원의 경계', sub='이자 + 배당 = 금융소득, 1년 합계 기준', source=SRC['statute'],
        data={'head': '국민건강보험법 시행규칙 제44조① 단서', 'quote': '1천만원 이하인 경우에는\n해당 이자소득과 배당소득은 합산하지 않는다',
              'rows': [['1,000만원 이하', '이자·배당 합산 안 함', False], ['1,000만원 초과', '넘은 부분만이 아니라 전액 합산', True]],
              'at': [L('단서가 하나'), L('합산하지 않는다는'), L('전액이 들어갑')]})),
    ('경계:cliff', lambda L: dict(kind='cliff', rail=2, title='연 금융소득별 월 건보료', sub='다른 소득 0 · 장기요양 포함 월 금액', source=SRC['cliff'],
        data={'rows': CLIFF, 'jump': f'+{kr(JUMP)}/월', 'jumpAt': 1, 'floor': FLOOR, 'floorLabel': f'최저 보험료(하한) {won(FLOOR)} + 장기요양',
              'year': f'1년이면 +{won(JUMP_Y)}',
              'at': [L('표로 보겠습니다'), L('900만원이면'), L('최저 보험료'), L('1,001만원이 되는'), L('1,200만원이면'), L('3,000만원이면'), L('언저리에서는')]})),
    ('경계:etf', lambda L: dict(kind='etf', rail=2, title='ETF 분배금도 여기 들어갑니다', sub='소득세법상 집합투자기구 이익 = 배당소득', source=SRC['etf'],
        data={'at': [L('개별 주식'), L('ETF가 주는'), L('사고판 손익만'), L('해외 주식을'), L('예금 이자까지')]})),
    ('국민연금', lambda L: dict(kind='pension', rail=3, title='국민연금이 있을 때', sub='국민연금 월 150만원(연 1,800만원) · 연금은 50%만 반영', source=SRC['pension'],
        data={'pen': 1800, 'half': 900, 'p0': PEN['pen'], 'p1': PEN['pen1001'], 'fin': [1000, 1001], 'diff': f'+{kr(PJUMP)}/월', 'year': f'1년이면 +{won(PJUMP_Y)}',
              'at': [L('국민연금을 받는'), L('50%만'), L('1,800만원 받으면'), L('6만 1,000원이 나옵'), L('합산이 안 되니까'), L('12만 8,860원이'), L('1년이면'), L('연금을 받는 사람일수록')]})),
    ('언제 반영', lambda L: dict(kind='calendar', rail=4, title='고지서에는 언제 반영되나', sub='2026년에 받은 소득 기준 예시', source=SRC['calendar'],
        data={'at': [L('바로 다음 달'), L('11월 고지서부터'), L('연금소득만'), L('2027년 11월분'), L('몇 년도 소득')]})),
    ('피부양자:check', lambda L: dict(kind='check', rail=5, title='피부양자로 남는 조건', sub='소득·재산 둘 다 맞아야 — 본인 보험료 0원', source=SRC['check'],
        data={'items': [['소득', '1년 2,000만원 이하', '사업·금융·연금·근로 소득 합계 · 사업소득은 원칙적으로 없어야'],
                        ['재산', '재산세 과세표준 5억 4,000만원 이하', '또는 9억원 이하 + 1년 소득 1,000만원 이하']],
              'at': [L('조건은 소득과'), L('2,000만원 이하여야'), L('5억 4,000만원 이하면'), L('9억원까지는'), L('하나라도 넘으면')]})),
    ('피부양자:band', lambda L: dict(kind='band', rail=5, title='퇴직 직후 — 임의계속가입', sub='퇴직 다음 날부터 36개월을 넘지 않는 범위', source=SRC['band'],
        data={'months': 36, 'at': [L('임의계속가입'), L('어느 쪽이 적은지')]})),
    ('집이 있으면:p', lambda L: dict(kind='property', tag=False, rail=5, title='집이 있으면 — 재산분', sub='재산 점수표는 60등급 · 금액은 공단 모의계산으로', source=SRC['property'],
        data={'at': [L('재산을 0으로'), L('6월 1일'), L('전월세 보증금'), L('60개나')]})),
    ('집이 있으면:s', lambda L: dict(kind='steps', tag=False, rail=5, title='직접 확인하는 방법', sub='건강보험공단 홈페이지 → 보험료 모의계산', source=SRC['steps'],
        data={'steps': [['지역보험료 선택', '보험료 모의계산 메뉴'], ['사업소득 등 칸', '이자 + 배당 합계'], ['연금 칸', '받은 금액 그대로\n50%는 화면이 반영']],
              'at': [L('대신 건강보험공단'), L('사업소득 등'), L('사업소득 등')]})),
    ('정리:s', lambda L: dict(kind='summary', title='정리', sub='2026년 법령·공단 계산식 기준', source=SRC['summary'],
        data={'cards': [['계산식', f'소득월액 × 7.19% + 재산 점수 × 211.5원', '+ 장기요양 13.14%'],
                        ['1,000만원 경계', '이하면 빠지고, 넘으면 전액', 'ETF 분배금도 배당소득'],
                        ['국민연금', '50%만 반영', '금융 1,000만원 넘으면 절벽이 더 큼'],
                        ['반영 시기', '이자·배당 등: 전년도 소득 → 11월분부터', '연금: 전년도 → 1월분부터'],
                        ['피부양자·확인', '소득 2,000만원 이하 + 재산 조건', '정확한 금액은 공단 모의계산']],
              'at': [L('첫째'), L('둘째'), L('셋째'), L('넷째'), L('다섯째')]})),
    ('정리:c', lambda L: dict(kind='calc', title='은퇴 계획에 건보료 넣기', sub='파이어맵 은퇴 나이 계산기', source=SRC['calc'],
        data={'url': 'firemap.kr', 'at': [L('빼먹기 쉬운'), L('생활비랑 건보료'), L('은퇴 나이가')]})),
]
SPLIT = {'1,000만원의 경계': [('경계:law', None), ('경계:cliff', '표로 보겠습니다'), ('경계:etf', '배당이라고 하면')],
         '피부양자로 남는': [('피부양자:check', None), ('피부양자:band', '또 하나')],
         '집이 있으면': [('집이 있으면:p', None), ('집이 있으면:s', '대신 건강보험공단')],
         '정리': [('정리:s', None), ('정리:c', '은퇴 생활비')]}

v = None
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    v = json.load(open(vj, encoding='utf-8'))
secs = v['sections'] if v else [{'title': s['title'], 'lines': [{'text': t, 'say': lfvoice.speak(EP, t), 'audio': None} for t in s['lines']]} for s in lfvoice.sections(EP)]

def chunks(sc):
    rule = next((r for k, r in SPLIT.items() if k in sc['title']), None)
    if not rule: return [dict(sc, key=None)]
    cut = [(0 if w is None else next(j for j, l in enumerate(sc['lines']) if w in l['text']), key) for key, w in rule]
    return [dict(sc, key=key, lines=sc['lines'][i:(cut[n + 1][0] if n + 1 < len(cut) else None)]) for n, (i, key) in enumerate(cut)]
secs = [c for sc in secs for c in chunks(sc)]

scenes = []
for sc in secs:
    lines = []
    for l in sc['lines']:
        if l.get('audio'): lines.append({'text': l['text'], 'audio': l['audio'], 'frames': l['frames']})
        else: lines.append({'text': l['text'], 'audio': None, 'frames': int(lfvoice.syl(l['say']) / 5.5 * FPS) + 8})
    texts = [l['text'] for l in sc['lines']]
    def L(word, _t=texts):
        for i, t in enumerate(_t):
            if word in t: return i
        return -1
    spec = next((fn for k, fn in SPEC if k == sc['key']), None) or next((fn for k, fn in SPEC if ':' not in k and k in sc['title']), None)
    d = spec(L) if spec else dict(kind='bullets', data={})
    frames = sum(x['frames'] for x in lines) + 18 if lines else 72
    title = d.get('title') or re.sub(r'^[\d\-\. \[]+|\s*·.*$|\]$', '', sc['title'])
    scenes.append({'kind': d['kind'], 'title': title, 'sub': d.get('sub'), 'source': d.get('source'), 'rail': d.get('rail', 0),
                   'tag': TAG if d.get('tag', True) else None, 'data': d['data'], 'lines': lines, 'frames': frames})
missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
out = {'fps': FPS, 'rail': RAIL, 'scenes': scenes, 'missing': missing, 'holes': 0}
json.dump(out, open(os.path.join(VID, 'd1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.2f}분 · 목소리 없는 문장 {missing}')
print('종류', len({s['kind'] for s in scenes}), [s['kind'] for s in scenes])
for s in scenes: print(f"  {s['kind']:9s} {s['frames']/FPS:5.1f}s  문장 {len(s['lines'])}  {s['title']}")
bad = [(s['title'], i) for s in scenes for i, x in enumerate(s['data'].get('at', [])) if x == -1]
if bad: print('문장 못 찾은 단계', bad)
print('숫자 대조 통과: 표', [v for _, v in TABLE], '연금', PEN, '절벽', JUMP, JUMP_Y, PJUMP, PJUMP_Y)
