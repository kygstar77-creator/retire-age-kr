# N-1 화면 재료 — script.md(장·문장) + voice.json(있으면 길이) + 원자료 → work/video/n1.json (Remotion N1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/N-1/n1props.py
# 숫자는 전부 원자료(nts_pct.json = 국세청 근로소득 백분위 원본 CSV 변환)와 facts.txt 원문 줄에서 온다 — 코드 안 숫자는 facts 줄과 기계 대조한다.
# 목소리가 없는 문장은 초당 5.5음절로 길이를 어림해 화면만 본다(preview). 업로드는 missing=0일 때만.
# 장면은 제목 열쇠말로 찾고, 장을 쪼갤 땐 '그 문장에 든 말'로 자른다(E-2와 같은 방식).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK)
import lfvoice
FPS = 30
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
def need(*ss):
    for s in ss: assert s in FACTS, f'facts.txt에 없는 줄: {s}'

# ── 연봉 줄(국세청 백분위 원본) ──
NT = json.load(open(os.path.join(EP, 'nts_pct.json'), encoding='utf-8'))
R = NT['rows']; assert len(R) == 109
TH = R[:10]                                   # 천분위 0.1%~1.0%
PC = R[10:]                                   # 상위 2%~100%
def top(k): return R[k + 8]['avg_man'] if k >= 2 else None   # 상위 k% 구간 평균(만원)
AVG = round(NT['G_eok'] * 1e8 / NT['N'] / 1e4)
assert (NT['N'], AVG) == (21078535, 4475)
TOP1 = round(sum(x['pay_eok'] for x in TH) / sum(x['n'] for x in TH) * 1e4)   # 상위 1% 구간 전체 평균(막대 높이용, 숫자로 말하지 않음)
BARS = [TOP1] + [x['avg_man'] for x in PC]                                   # 100칸
assert len(BARS) == 100
need('전체 신고 인원 21,078,535명', '1인 평균 4,475만원', '상위 0.1% 구간 평균 99,937', '50% 3,417', '100% 21', '상위 2% 17,332', '10% 9,117')
assert (TH[0]['avg_man'], TH[0]['n'], top(50), top(100), top(2), top(10)) == (99937, 21078, 3417, 21, 17332, 9117)
def where(x):                                 # 연봉 x가 들어가는 '두 구간 평균 사이' → (위 칸, 아래 칸) 백분위
    for k in range(2, 100):
        if top(k) >= x > top(k + 1): return (k, k + 1)
    if TH[-1]['avg_man'] >= x: return (1.0, 0.9) if x > TH[-2]['avg_man'] else None
LOOK = []
for x, s in [(3000, '3,000만원 → 상위 57%(3,009)와 58%(2,964) 사이'), (4000, '4,000만원 → 상위 41%(4,021)와 42%(3,945) 사이'),
             (4475, '4,475만원(평균) → 상위 35%(4,537)와 36%(4,443) 사이'), (5000, '5,000만원 → 상위 30%(5,063)와 31%(4,947) 사이'),
             (7000, '7,000만원 → 상위 17%(7,148)와 18%(6,932) 사이'), (10000, '1억원 → 상위 7%(10,456)와 8%(9,925) 사이'),
             (20000, '2억원 → 상위 1.0%(19,953)과 0.9%(20,752) 사이')]:
    need(s); w = where(x) if x < 20000 else (0.9, 1.0)
    if x < 20000:
        m = re.search(r'상위 (\d+)%\(([\d,]+)\)와 (\d+)%\(([\d,]+)\)', s)
        assert w == (int(m[1]), int(m[3])) and top(w[0]) == int(m[2].replace(',', '')) and top(w[1]) == int(m[4].replace(',', '')), (x, w)
    else:
        assert TH[9]['avg_man'] == 19953 and TH[8]['avg_man'] == 20752 and TH[8]['avg_man'] >= x > TH[9]['avg_man']
    LOOK.append({'x': x, 'a': w[0], 'b': w[1]})
need('+2,000만원에 약 27칸', '+1억원에 약 6칸', '상위 2% 1억 7,332 - 상위 10% 9,117 = 8,215만원')
assert round((57.5 - 30.5)) == 27 and round(7.5 - 0.95) in (6, 7)

# ── 세금 몫(facts 표B 그대로) ──
need('상위 1%(천분위 10줄): 총급여의 7.7% · 결정세액의 30.3%', '상위 10%: 총급여의 31.7% · 결정세액의 71.7%',
     '아래 50%(상위 51~100%): 총급여의 20.4% · 결정세액의 1.43%', '결정세액 합계 65조 1,605억원')
TAX = [['상위 1%', 7.7, 30.3], ['상위 10%', 31.7, 71.7], ['아래 절반', 20.4, 1.43]]

# ── 가구 순자산 경계값(facts 표C 원문 줄 파싱) ──
PS = {}
for m in re.finditer(r'^P(\d0)\s+([\d,]+)\s+([\d,]+)\s+([+-][\d,]+)', FACTS, re.M):
    a, b, dlt = (int(m[i].replace(',', '')) for i in (2, 3, 4))
    assert b - a == dlt, m[0]; PS[int(m[1])] = [a, b, dlt]
assert sorted(PS) == [10, 20, 30, 40, 50, 60, 70, 80, 90] and PS[90] == [104592, 110020, 5428] and PS[50][1] == 23860
need('평균  44,894    47,144     +2,250', '+5,428 (+5.19%)', '5,428만원 ÷ 12 = 452.3 → 한 달 452만원', "P50 -0.5833% → '0.6%'", "P90 +5.1897% → '5.2%'")
MEAN = 47144
def pin(x):                                   # 순자산 x(만원)을 백분위 눈금 위 자리(10~90 사이 선형 보간)로
    ks = sorted(PS); v = [PS[k][1] for k in ks]
    if x <= v[0]: return 10 * x / v[0]
    for i in range(len(ks) - 1):
        if v[i] <= x <= v[i + 1]: return ks[i] + 10 * (x - v[i]) / (v[i + 1] - v[i])
    return 90 + 5 * min(1, (x - v[-1]) / v[-1])
for x, lo in [(10000, 20), (50000, 70), (100000, 80), (MEAN, 70)]: assert lo < pin(x) < lo + 10, (x, pin(x))
need('5분위(상위 20%) 2024 63.08 → 2025 64.56 (+1.48%p) · 1분위 0.48 · 2분위 4.44 · 3분위 10.22 · 4분위 20.30')
Q5 = [0.48, 4.44, 10.22, 20.30, 64.56]; assert round(sum(Q5), 2) == 100.0

SRC_NTS = '국세청 근로소득 백분위(천분위) 2024년 귀속 · 공공데이터포털 15082063'
SRC_GFS = '국가데이터처·금융감독원·한국은행 2025년 가계금융복지조사 통계표 12(순자산 2025.3.31 기준)'
RAIL = ['100칸 줄', '내 연봉 자리', '세금 몫', '우리 집 순자산', '1년 새 문턱']
won = lambda m: (f"{m // 10000}억 {m % 10000:,}만원" if m % 10000 else f"{m // 10000}억원") if m >= 10000 else f"{m:,}만원"
SPEC = [
    ('여는', lambda L: dict(kind='open', title='나 vs 남들 — 연봉·순자산 줄', source=SRC_NTS + ' · ' + SRC_GFS,
                          data={'avg': AVG, 'a': 35, 'b': 36, 'bars': BARS, 'p90': PS[90], 'at': [0, L('35%와 36%'), L('5,428만원'), L('하나씩')]})),
    ('로고', lambda L: dict(kind='logo', data={'sub': '나 vs 남들 · 숫자로 줄 세우기'})),
    ('100칸:crowd', lambda L: dict(kind='crowd', rail=1, title='연말정산한 직장인 전부를 한 줄로', sub='2024년 귀속 근로소득 · 연봉 높은 순 → 100칸', source=SRC_NTS,
                                  data={'n': NT['N'], 'per': round(NT['N'] / 100), 'at': [0, L('100칸으로')]})),
    ('100칸:bars', lambda L: dict(kind='bars100', rail=1, title='칸마다 평균 연봉', sub='만원 · 칸 = 그 구간 사람들 총급여 합 ÷ 인원 · 왼쪽 = 상위 1%', source=SRC_NTS,
                                 data={'bars': BARS, 'mid': top(50), 'avg': AVG, 'top01': TH[0]['avg_man'], 'top01n': TH[0]['n'], 'last': top(100),
                                       'at': [0, L('3,417'), L('끌어올리'), L('9억 9,937'), L('21만원'), L('정규직')]})),
    ('자리:look', lambda L: dict(kind='lookup', rail=2, title='연봉 ___이면 상위 몇 %?', sub='칸 평균 두 개 사이로 읽음(정확한 경계값 아님)', source=SRC_NTS,
                                 data={'rows': LOOK[:2] + LOOK[3:6], 'bars': BARS, 'hi': 2, 'at': [0, L('3,000만원'), L('4,000만원'), L('5,000만원'), L('7,000만원'), L('1억원.')]})),
    ('자리:climb', lambda L: dict(kind='climb', rail=2, title='같은 칸을 오르는 데 드는 돈', sub='상위 %(칸 평균 사이 가운데 자리) · 2024년 귀속', source=SRC_NTS,
                                  data={'pts': [[r['x'], (r['a'] + r['b']) / 2] for r in LOOK if r['x'] != 4475], 'bars': BARS,
                                        'arrows': [['+2,000만원', 3000, 5000, '약 27칸'], ['+1억원', 10000, 20000, '약 6칸']],
                                        'at': [0, L('재밌는'), L('1억원에서')]})),
    ('자리:gap', lambda L: dict(kind='gap', rail=2, title='위로 갈수록 칸 사이가 벌어진다', sub='만원 · 상위 2%~10% 칸 평균', source=SRC_NTS,
                                data={'rows': [[k, top(k)] for k in range(2, 11)], 'diff': top(2) - top(10), 'at': [0]})),
    ('세금:total', lambda L: dict(kind='taxsplit', rail=3, title='근로소득세(결정세액) 합계', sub='2024년 귀속 · 칸마다 낸 세금을 더함', source=SRC_NTS,
                                  data={'jo': 65, 'eok': 1605, 'at': [0]})),
    ('세금:twin', lambda L: dict(kind='twin', rail=3, title='받은 연봉 몫 vs 낸 세금 몫', sub='% · 전체 총급여·전체 결정세액 중', source=SRC_NTS + ' · 몫은 구간 합계로 계산',
                                 data={'rows': TAX, 'at': [0, L('상위 10%로'), L('아래 절반'), L('세율이 올라가')]})),
    ('순자산:ruler', lambda L: dict(kind='ruler', rail=4, title='두 번째 줄 — 가구 순자산', sub='만원 · 집·예금·주식 − 빚 · 2025년 3월 말 · 아래에서 10%~90% 경계값', source=SRC_GFS,
                                    data={'ps': [[k, PS[k][1]] for k in sorted(PS)], 'pins': [[won(10000), pin(10000)], [won(50000), pin(50000)], [won(100000), pin(100000)]],
                                          'at': [0, L('경계선'), L('2억 3,860'), L('핀 세 개'), L('11억 20만')]})),
    ('순자산:mean', lambda L: dict(kind='meanmed', rail=4, title='평균은 가운데가 아니다 — 순자산도', sub='만원 · 2025년 3월 말', source=SRC_GFS,
                                   data={'med': PS[50][1], 'mean': MEAN, 'x': round(MEAN / PS[50][1], 2), 'pin': pin(MEAN), 'at': [0]})),
    ('순자산:share', lambda L: dict(kind='share', rail=4, title='순자산 5칸 — 누가 얼마를 갖고 있나', sub='% · 가구 순자산 5분위 점유율', source=SRC_GFS,
                                    data={'q': Q5, 'prev5': 63.08, 'at': [0, L('그런데 우리 집')]})),
    ('문턱:shift', lambda L: dict(kind='shift', rail=5, title='1년 새 경계값은 얼마나 움직였나', sub='만원 · 2024년 3월 말 → 2025년 3월 말 · 표본 조사', source=SRC_GFS,
                                  data={'rows': [[k] + PS[k] for k in sorted(PS)], 'at': [0, L('중앙값은'), L('아래에서 10%'), L('위로 갈수록'), L('10억 4,592')]})),
    ('문턱:month', lambda L: dict(kind='month', rail=5, title='상위 10% 문턱 이동을 한 달로 나누면', sub='만원 · 저축 + 집값·주가 변화가 함께 들어간 값', source=SRC_GFS,
                                  data={'y': 5428, 'm': 452, 'at': [0, L('한 해 변화')]})),
    ('정리:sum', lambda L: dict(kind='sum3', title='정리 — 숫자 세 개', source=SRC_NTS + ' · ' + SRC_GFS,
                                data={'cards': [['평균 연봉 4,475만원', '상위 35~36%', '평균은 가운데가 아니다'], ['연봉 1억원', '상위 7~8%', '상위 10%가 근로소득세 71.7%'],
                                                ['가구 순자산 상위 10% 문턱', '11억 20만원', '1년 새 +5,428만원 · 가운데는 거의 그대로']],
                                      'at': [0, L('첫째'), L('둘째'), L('셋째')]})),
    ('정리:two', lambda L: dict(kind='twopins', title='같은 사람, 두 줄에서 다른 자리', sub='예: 연봉 5,000만원 · 가구 순자산 1억원', source=SRC_NTS + ' · ' + SRC_GFS,
                                data={'pay': [LOOK[3]['a'], LOOK[3]['b']], 'nw': pin(10000), 'at': [0, L('나이의 가구')]})),
    ('정리:cta', lambda L: dict(kind='cta', title='내 연봉 넣어 보기', sub='설명란 첫 줄 — firemap.kr 계산기', source='파이어맵 계산기 · 국세청·국가데이터처 원자료 정리',
                                data={'x': 5000, 'at': [0, L('다음 나 vs 남들')]})),
]
SPLIT = {'100칸': [('100칸:crowd', None), ('100칸:bars', '국세청은')],
         '내 연봉': [('자리:look', None), ('자리:climb', '2억원까지'), ('자리:gap', '간격이 넓어')],
         '세금': [('세금:total', None), ('세금:twin', '상위 1%가')],
         '순자산은': [('순자산:ruler', None), ('순자산:mean', '평균 순자산은'), ('순자산:share', '위쪽 20%')],
         '문턱이': [('문턱:shift', None), ('문턱:month', '열두 달')],
         '정리': [('정리:sum', None), ('정리:two', '처음 빈칸'), ('정리:cta', '지금 할 일')]}

v = None
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj): v = json.load(open(vj, encoding='utf-8'))
secs = v['sections'] if v else [{'title': s['title'], 'lines': [{'text': t, 'say': lfvoice.speak(EP, t), 'audio': None} for t in s['lines']]} for s in lfvoice.sections(EP)]
cur = {t for s in lfvoice.sections(EP) for t in s['lines']}

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
        ok = l.get('audio') and l['text'] in cur
        lines.append({'text': l['text'], 'audio': l['audio'] if ok else None, 'frames': l['frames'] if ok else int(lfvoice.syl(l.get('say') or l['text']) / 5.5 * FPS) + 8})
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
                   'data': d['data'], 'lines': lines, 'frames': frames})
missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
out = {'fps': FPS, 'rail': RAIL, 'scenes': scenes, 'missing': missing, 'holes': 0}
json.dump(out, open(os.path.join(VID, 'n1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.1f}분 · 목소리 없는 문장 {missing}')
kinds = sorted({s['kind'] for s in scenes}); print('종류', len(kinds), kinds)
bad = [(s['title'], i) for s in scenes for i, x in enumerate(s['data'].get('at', [])) if x == -1]
if bad: print('문장 못 찾은 단계', bad)
for s in scenes: print(f"  {s['kind']:9} {s['frames']/FPS:5.1f}초 문장{len(s['lines'])}")
long = [(s['title'], round(s['frames'] / FPS, 1)) for s in scenes if s['frames'] / FPS > 40]
if long: print('40초 넘는 장(단계 더 필요)', long)
