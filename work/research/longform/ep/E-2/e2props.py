# E-2 화면 재료 — script.md(장·문장) + voice.json(있으면 길이) + 원자료 → work/video/e2.json (Remotion E2 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/E-2/e2props.py
# 숫자는 전부 원자료(quarters.json·raw/nasdaq_TSLA.json·price.json·fireage.json)와 facts.txt 원문 줄에서 온다 — 코드 안 숫자는 facts 줄과 기계 대조한다.
# 목소리가 없는 문장은 초당 5.5음절로 길이를 어림해 화면만 본다(preview). 업로드는 missing=0일 때만.
# 장면은 제목 열쇠말로 찾고, 장을 쪼갤 땐 '그 문장에 든 말'로 자른다 — 루프가 문장을 고쳐도 어긋나지 않게(E-1과 같은 방식).
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

# ── 10분기(XBRL) ──
Q = json.load(open(os.path.join(EP, 'quarters.json'), encoding='utf-8'))['q']
KS = sorted(Q['매출'])[-10:]
def mq(k): return f"{k[2:4]}.{(int(k[5:7]) + 2) // 3}Q"
REV = [round(Q['매출'][k]['v'] / 1e8) for k in KS]                  # 억 달러
OPK = [k for k in Q if k.startswith('영업이익')][0]
RDK = [k for k in Q if '연구' in k][0]
OP = [Q[OPK][k]['v'] / 1e6 for k in KS]
MARGIN = [round(o / (Q['매출'][k]['v'] / 1e6) * 100, 1) for o, k in zip(OP, KS)]
RD = [round(Q[RDK][k]['v'] / 1e6) for k in KS]                      # 백만 달러
for k, r, o, m, d in zip(KS, REV, OP, MARGIN, RD):                  # facts [10] 표 줄과 한 줄씩 대조
    row = re.search(rf"{k}\*?\s+([\d,]+) / ([\d,]+) / ([\d.]+)% / ([\d,]+)", FACTS)
    assert row, k
    assert (round(int(row[1].replace(',', '')) / 100), round(o), float(row[3]), int(row[4].replace(',', ''))) == (r, int(row[2].replace(',', '')), m, d), (k, r, o, m, d)
assert REV.index(max(REV)) == 9 and MARGIN.index(min(MARGIN)) == 9 and round(RD[9] / RD[0], 2) == 2.06

# ── 원문 숫자(facts 줄 그대로 확인) ──
need('[2] 2026년 2분기 영업이익 398 (1년 전 923, -56.9%)', '[1] 2026년 2분기 매출 28,236 (1년 전 22,496, +25.5%)',
     '이자수익 422 > 영업이익 398', '세전이익 1,329 · 순이익 1,128(1년 전 1,190)', '세전이익 중 영업에서 번 몫 30%',
     'Total automotive revenues: 20,516 (16,661, +23.1%) · 총이익률 16.9% (17.2%)', 'Energy generation and storage: 3,139 (2,789, +12.5%) · 총이익률 20.4% (30.3%)',
     'Services and other: 4,581 (3,046, +50.4%) · 총이익률 14.1% (5.4%)', '규제 크레딧 146 (439, -66.7%)', '규제 크레딧 줄어든 금액 293',
     '연구개발비 2,371 (1년 전 1,589, +49.2%) · 판매관리비 1,982 (1년 전 1,366, +45.1%) · 영업비용 합계 4,353(1년 전 2,955)', '매출총이익 4,751(1년 전 3,878, +22.5%)',
     '설비투자 8,282 (1년 전 3,886, 2.13배) · 영업현금흐름 8,634(1년 전 4,696) · SpaceX 지분 매입 2,002', '하반기에 최소 16,718 남음',
     '설비투자+SpaceX 10,284 vs 영업현금흐름 8,634 → 차이 1,650', '"will necessitate additional funding beyond our operating cash flow"',
     '6월 말 현금 15,219 + 단기투자 28,305 = 43,524', 'three-year=200억 달러·five-year=80억 달러·364-day=20억 달러 = 합계 300억 달러',
     '해지된 옛 회전 한도 50억 달러', '"Recent governmental and regulatory actions have restricted certain regulatory credit programs"',
     '약 838천 대', '22.3 GWh', 'began production of Cybercab', 'advance the development of Optimus')

# ── 주가(나스닥 공식 종가) ──
rows = json.load(open(os.path.join(EP, 'raw', 'nasdaq_TSLA.json'), encoding='utf-8'))['data']['tradesTable']['rows']
PTS = sorted((f"{r['date'][6:]}{r['date'][:2]}{r['date'][3:5]}", float(r['close'].replace('$', '').replace(',', ''))) for r in rows)
PJ = json.load(open(os.path.join(EP, 'price.json'), encoding='utf-8'))
assert PTS[-1] == tuple(PJ['last']) and abs(PTS[0][1] - PJ['first'][1]) < 0.01, (PTS[-1], PJ['last'])
pk = max(PTS, key=lambda p: p[1]); assert pk[0] == PJ['peak'][0]
step = max(1, len(PTS) // 160); THIN = PTS[::step] + ([PTS[-1]] if (len(PTS) - 1) % step else [])
def idx(d): return min(range(len(THIN)), key=lambda i: abs(int(THIN[i][0]) - int(d)))
PRICE = {'d': [p[0] for p in THIN], 'v': [round(p[1], 2) for p in THIN], 'last': PJ['last'], 'y1': PJ['y1'], 'y5': PJ['y5'], 'peak': PJ['peak'],
         'mdd': PJ['mdd'], 'from_peak': round((PJ['last'][1] / PJ['peak'][1] - 1) * 100, 1),
         'i': {'y1': idx(PJ['y1'][0]), 'peak': idx(PJ['peak'][0]), 'mf': idx(PJ['mdd']['from']), 'mt': idx(PJ['mdd']['to'])}}
assert PRICE['from_peak'] == -27.6 and PJ['mdd']['pct'] == -73.6
AGE = json.load(open(os.path.join(EP, 'fireage.json'), encoding='utf-8'))
assert (AGE['p35']['now']['drawdown'], AGE['p35']['max5y']['drawdown']) == (27.6, 73.6)

# ── 장면 지정(제목 열쇠말 → 종류·재료). 목록에 없는 장은 'bullets'(문장 카드) ──
Q10 = '테슬라 10-Q(2026-07-23 제출) · SEC EDGAR'
XB = 'SEC XBRL companyfacts(테슬라 CIK 1318605, 2024년 4분기·2025년 4분기는 연간−3개 분기 계산)'
K8 = '테슬라 8-K(2026-09-29 제출) · SEC EDGAR'
PSRC = '나스닥 공식 과거 시세(TSLA) 종가 · 2021-09-29 → 2026-09-30 · 분할 반영'
RAIL = ['10분기 흐름', '무엇을 팔았나', '줄어든 수입', '돈이 나간 곳', '신용 한도 공시', '주가와 은퇴']
SPEC = [
    ('여는', lambda L: dict(kind='open', source=Q10, data={'op': 398, 'int': 422, 'rev': REV[9], 'margin': MARGIN[9], 'at': [0, L('282억'), L('1달러 40센트'), L('은퇴 나이'), L('신용 한도')]})),
    ('로고', lambda L: dict(kind='logo', data={'sub': '은퇴 나이, 숫자로'})),
    ('오늘 볼 것', lambda L: dict(kind='agenda', title='오늘 볼 여섯 가지', data={'items': RAIL, 'at': [0]})),
    ('장부:ledger', lambda L: dict(kind='ledger', rail=1, title='10분기 장부 — 매출과 영업이익률', sub='막대 = 분기 매출(억 달러) · 선 = 영업이익률(%) · 2024년 1분기 → 2026년 2분기', source=XB,
                                   data={'q': [mq(k) for k in KS], 'rev': REV, 'margin': MARGIN, 'at': [0, L('213억'), L('10.8%')]})),
    ('장부:yoy', lambda L: dict(kind='yoy', rail=1, title='같은 분기끼리 — 2025년 2분기 vs 2026년 2분기', sub='백만 달러 · 3개월', source=Q10,
                                data={'rows': [['매출', 22496, 28236, '+25.5%'], ['영업이익', 923, 398, '−56.9%']], 'at': [0, L('4분의 1')]})),
    ('장부:pretax', lambda L: dict(kind='pretax', rail=1, title='순이익은 왜 덜 줄었나', sub='백만 달러 · 2026년 2분기', source=Q10,
                                   data={'net': [1190, 1128], 'pre': 1329, 'op': 398, 'int': 422, 'oth': 590, 'share': 30, 'at': [0, L('세전이익')]})),
    ('부문:mix', lambda L: dict(kind='mix', rail=2, title='무엇을 팔았나 — 2026년 2분기 매출', sub='억 달러 · 괄호는 1년 전 같은 분기 대비', source=Q10,
                                data={'rows': [['자동차', 205, '+23.1%', '상반기 인도 약 83만 8천 대'], ['에너지 저장·발전', 31, '+12.5%', '상반기 설치 22.3GWh'], ['서비스·기타', 46, '+50.4%', '가장 빨리 늘어남']],
                                      'at': [0, L('205억'), L('31억'), L('46억')]})),
    ('부문:gm', lambda L: dict(kind='slope', rail=2, title='매출총이익률 — 원가를 빼고 남은 비율', sub='% · 2025년 2분기 → 2026년 2분기', source=Q10,
                               data={'rows': [['자동차', 17.2, 16.9], ['에너지 저장·발전', 30.3, 20.4], ['서비스·기타', 5.4, 14.1]], 'hi': 1, 'at': [0, L('17.2%에서'), L('30.3%'), L('5.4%에서')]})),
    ('부문:gp', lambda L: dict(kind='stairs', rail=2, title='전체 매출총이익은 늘었다', sub='백만 달러 · 같은 분기 비교', source=Q10,
                               data={'rows': [['2025년 2분기', 3878], ['2026년 2분기', 4751]], 'tag': '+22.5%', 'at': [0, L('22.5%')]})),
    ('규제', lambda L: dict(kind='credit', rail=3, title='규제 크레딧 — 자동차 매출 안의 한 줄', sub='백만 달러 · 같은 분기 비교', source=Q10,
                           data={'a': 439, 'b': 146, 'pct': '−66.7%', 'cut': 293, 'op': 398,
                                 'quote': ['Recent governmental and regulatory actions have restricted certain regulatory credit programs', '최근 정부·규제 당국의 조치로 일부 규제 크레딧 제도가 제한됐다'],
                                 'at': [0, L('자동차 매출 안'), L('66.7%'), L('규제 당국'), L('2억 9,300만')]})),
    ('비용:fall', lambda L: dict(kind='waterfall', rail=4, title='매출총이익에서 영업이익까지', sub='백만 달러 · 2026년 2분기', source=Q10,
                                 data={'steps': [['매출총이익', 4751], ['연구개발비', -2371], ['판매관리비', -1982], ['영업이익', 398]],
                                       'yoy': ['+22.5%', '+49.2%', '+45.1%', '−56.9%'], 'opex': [2955, 4353],
                                       'at': [0, L('23억 7,100만'), L('19억 8,200만'), L('영업비용은'), L('훨씬 빨리')]})),
    ('비용:rd', lambda L: dict(kind='rd10', rail=4, title='연구개발비 10분기', sub='백만 달러 · 분기', source=XB + ' · ' + Q10,
                               data={'q': [mq(k) for k in KS], 'v': RD, 'x': round(RD[9] / RD[0], 2),
                                     'notes': [['사이버캡', '생산 시작(10-Q 문장)'], ['옵티머스', '개발 계속 · 대수 없음']], 'at': [0, L('사이버캡')]})),
    ('설비:capex', lambda L: dict(kind='capex', rail=4, title='설비투자 — 올해 계획 대비 상반기', sub='백만 달러 · 전망은 회사 표현 "in excess of $25 billion"', source=Q10,
                                  data={'h1': 8282, 'prev': 3886, 'x': 2.13, 'plan': 25000, 'left': 16718, 'at': [0, L('82억'), L('250억'), L('하반기')]})),
    ('설비:cash', lambda L: dict(kind='cash', rail=4, title='상반기 — 들어온 현금 vs 나간 돈', sub='백만 달러 · 2026년 1~6월', source=Q10 + ' 현금흐름표',
                                 data={'in': 8634, 'capex': 8282, 'spacex': 2002, 'gap': 1650,
                                       'quote': ['will necessitate additional funding beyond our operating cash flow', '영업으로 버는 현금 말고 추가 자금이 필요할 것'],
                                       'at': [0, L('86억'), L('이렇게 적었')]})),
    ('신용:line', lambda L: dict(kind='facility', rail=5, title='9월 29일 공시 — 새 신용 한도 3개', sub='억 달러 · 무담보 · 공시일 빌린 돈 0', source=K8,
                                 data={'tl': [['7/23', '분기 보고서(10-Q)'], ['9/29', '신용 계약 공시(8-K)']],
                                       'rows': [['3년', 200], ['5년', 80], ['364일', 20]], 'total': 300, 'at': [0, L('세 개를'), L('미리 열어 둔')]})),
    ('신용:x6', lambda L: dict(kind='circles', rail=5, title='옛 한도 vs 새 한도', sub='억 달러 · 용도: "general corporate purposes"', source=K8 + ' · ' + Q10 + ' 재무상태표',
                               data={'old': 50, 'new': 300, 'cash': 43524, 'at': [0, L('6배'), L('435억'), L('짐작')]})),
    ('주가', lambda L: dict(kind='price5', rail=6, title='테슬라 5년 주가', sub='달러 · 종가', source=PSRC,
                          data=dict(PRICE, at=[0, L('354.81'), L('260.44'), L('489.88'), L('73.6%')]))),
    ('은퇴', lambda L: dict(kind='age2', rail=6, title='이 흔들림을 내 은퇴 계획에 넣으면', sub='파이어맵 은퇴 계산기 · 연 5%·물가 3%·국민연금 65세 월 100만원 · 모은 돈 전부가 이 주식 하나라는 극단 가정',
                          source='파이어맵 은퇴 계산기(retirementSimulator)',
                          data={'groups': [{'who': '35세 · 1억 · 월 300만원 저축', 'ages': [AGE['p35'][k]['age'] for k in ('none', 'now', 'max5y')]},
                                           {'who': '50세 · 5억 · 월 200만원 저축', 'ages': [AGE['p50'][k]['age'] for k in ('none', 'now', 'max5y')]}],
                                'labels': ['그대로', '−27.6%', '−73.6%'], 'at': [0, L('공통 가정'), L('35세에'), L('56세'), L('50세에'), L('65세'), L('차이가')]})),
    ('정리', lambda L: dict(kind='check2', title='한 장 정리 — 장부로 확인되는 것, 안 되는 것', sub='2026년 2분기 10-Q · 9/29 8-K 기준', source=Q10 + ' · ' + K8,
                          data={'yes': ['매출 10분기 최대 · 영업이익률 최저 1.4%', '규제 크레딧 약 3분의 1로', '연구개발·판관비 +49%·+45%', '설비투자 올해 250억 달러 넘게(계획)', '신용 한도 300억 달러(빌린 돈 0)'],
                                'no': ['로보택시·옵티머스 수익 시점', '3분기 인도량', '신용 한도 실제 사용'], 'next': ['영업이익률', '규제 크레딧', '설비투자'],
                                'at': [0, L('10분기 중 최대'), L('250억'), L('확인되지 않는'), L('세 칸'), L('투자 권유'), L('딱 하나')]})),
]
SPLIT = {'10분기 장부': [('장부:ledger', None), ('장부:yoy', '같은 분기끼리'), ('장부:pretax', '순이익은')],
         '무엇을 팔았나': [('부문:mix', None), ('부문:gm', '매출총이익률로'), ('부문:gp', '설명이 안 돼')],
         '돈은 어디로': [('비용:fall', None), ('비용:rd', '길게 보면')],
         '설비투자': [('설비:capex', None), ('설비:cash', '스페이스X')],
         '신용 한도': [('신용:line', None), ('신용:x6', '옛 한도')]}

v = None
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj): v = json.load(open(vj, encoding='utf-8'))
secs = v['sections'] if v else [{'title': s['title'], 'lines': [{'text': t, 'say': lfvoice.speak(EP, t), 'audio': None} for t in s['lines']]} for s in lfvoice.sections(EP)]
# voice.json이 옛 대본이면 문장이 다를 수 있다 — 지금 script.md 문장과 맞는 것만 목소리로 쓴다
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
json.dump(out, open(os.path.join(VID, 'e2.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.1f}분 · 목소리 없는 문장 {missing}')
kinds = sorted({s['kind'] for s in scenes}); print('종류', len(kinds), kinds)
bad = [(s['title'], i) for s in scenes for i, x in enumerate(s['data'].get('at', [])) if x == -1]
if bad: print('문장 못 찾은 단계', bad)
long = [(s['title'], round(s['frames'] / FPS, 1)) for s in scenes if s['frames'] / FPS > 40]
if long: print('40초 넘는 장(단계 더 필요)', long)
