# R-1 화면 재료 — script.md(장·문장) + voice.json(있으면 길이) + 원자료 → work/video/r1.json (Remotion R1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/R-1/r1props.py
# 숫자는 전부 calc2_out.txt(영수증)·raw/collect_20261003.json(금리선·공시 점)·facts.txt 원문 줄에서 온다 — 코드 안 숫자는 facts 줄과 기계 대조한다.
# 목소리가 없는 문장은 초당 5.5음절로 길이를 어림해 화면만 본다(preview). 업로드는 missing=0일 때만. (N-1 n1props.py와 같은 방식)
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, WORK)
import lfvoice
FPS = 30
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
C2 = open(os.path.join(EP, 'calc2_out.txt'), encoding='utf-8').read()
def need(*ss):
    for s in ss: assert s in FACTS, f'facts.txt에 없는 줄: {s}'
num = lambda s: int(s.replace(',', ''))

# ── 영수증 4장(calc2_out.txt [영수증] 표를 그대로 파싱) ──
RC = {}
for m in re.finditer(r'^\s+(SCHD|SPY|GLD|정기예금\(2025-10 신규 평균 2\.58%\)) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \(\+([\d.]+)%\)', C2, re.M):
    k = 'DEP' if m[1].startswith('정기') else m[1]
    RC[k] = dict(sell=num(m[2]), gain=num(m[3]), dist=num(m[4]), tax=num(m[5]), net=num(m[6]), pct=float(m[7]))
assert sorted(RC) == ['DEP', 'GLD', 'SCHD', 'SPY'], RC
need('예금(2025-10 신규 평균 2.58%): 이자 2,580,000 · 세금 397,320 · 통장 102,182,680 (+2.18%)',
     '금(GLD): 매도 103,451,047(차익 3,451,047) · 분배 0 · 양도세 209,229 · 통장 103,241,818 (+3.24%)',
     'S&P500(SPY): 매도 111,215,966(차익 11,215,966) · 분배(세전) 1,095,716 · 양도세 1,917,512 · 통장 110,394,170 (+10.39%)',
     'SCHD: 매도 115,701,341(차익 15,701,341) · 분배(세전) 3,728,285 · 양도세 2,904,294 · 통장 116,525,333 (+16.53%)')
for k, line in [('DEP', (2580000, 397320, 102182680)), ('GLD', (3451047, 209229, 103241818)), ('SPY', (11215966, 1917512, 110394170)), ('SCHD', (15701341, 2904294, 116525333))]:
    assert (RC[k]['gain'], RC[k]['tax'], RC[k]['net']) == line, k
    assert abs(RC[k]['net'] - (100_000_000 + RC[k]['gain'] + RC[k]['dist'] - RC[k]['tax'])) <= 1, k     # 통장 = 원금 + 차익 + 분배 − 세금
# 해외 양도세 = (차익 − 250만) × 22%, 원 미만 버림 [13]
for k in ['SPY', 'SCHD', 'GLD']: cg = max(0, RC[k]['gain'] - 2_500_000); assert abs(RC[k]['tax'] - (int(cg * 0.20) + int(cg * 0.02))) <= 1, k
assert RC['DEP']['tax'] == 397320 and int(2580000 * 0.14 / 10) * 10 + int(2580000 * 0.014 / 10) * 10 == 397320
FX = (1406.0, 1359.6); need('2025-10-02 1,406.0원 → 2026-10-02 1,359.6원 (-3.30%)', '약 -330만원(3,300,142)')
assert '환율 효과만 -3,300,142원' in C2; FXLOSS = 3300142
USD = {'SPY': (669.22, 769.68, 15.01), 'SCHD': (27.34, 32.71, 19.65), 'GLD': (354.79, 379.56, 6.98)}
need('SPY 669.22 → 769.68(+15.01%', 'SCHD 27.34 → 32.71(+19.65%)', 'GLD 354.79 → 379.56(+6.98%)')
for k, (a, b, p) in USD.items(): assert abs((b / a - 1) * 100 - p) < 0.015, k   # 종가 표시는 소수 2자리라 0.01%p 차 허용
PRE = {k: RC[k]['sell'] + RC[k]['dist'] for k in RC}; PRE['DEP'] = 102_580_000          # 세전(분배 포함)
ORD = ['SCHD', 'SPY', 'GLD', 'DEP']
assert sorted(PRE, key=lambda k: -PRE[k]) == ORD and sorted(RC, key=lambda k: -RC[k]['net']) == ORD
GAP = (PRE['SCHD'] - PRE['DEP'], RC['SCHD']['net'] - RC['DEP']['net'])
need('예금 vs SCHD 차이: 세전 16,849,626', '→ 통장 14,342,653'); assert GAP == (16849626, 14342653)
NAME = {'DEP': '예금', 'SPY': 'S&P500', 'SCHD': 'SCHD', 'GLD': '금'}

# ── 금리선·공시 점(raw/collect_20261003.json) ──
RAW = json.load(open(os.path.join(EP, 'raw', 'collect_20261003.json'), encoding='utf-8'))
DEPM = [[t, float(v)] for t, v in RAW['정기예금1년_신규_M']]
dm = dict(DEPM); assert (dm['202508'], dm['202608'], dm['202211']) == (2.51, 3.39, 4.95) and max(dm.values()) == 4.95
need('2025-08 2.51% · 2026-08 3.39%(최신) · 2020년 이후 최고 2022-11 4.95%')
BASE = [[t, float(v)] for t, v in RAW['기준금리_M']]; assert dict(BASE)['202608'] == 3.0
def uniq(rows):                                # calc.py와 같은 규칙: 회사·상품명 기준, 기본금리 높은 쪽
    s = {}
    for x in rows:
        k = (x['은행'], (x['상품'] or '').replace('\n', ' '))
        if x['금리'] is not None: s[k] = max(s.get(k, 0), x['금리'])
    return sorted(s.values())
DOTS = {g: uniq(RAW[f'finlife_예금12개월_{g}']) for g in ['은행', '저축은행']}
b, sv = DOTS['은행'], DOTS['저축은행']
assert (len(b), b[0], b[len(b) // 2], b[-1]) == (39, 1.9, 3.33, 3.92) and (len(sv), sv[0], sv[len(sv) // 2], sv[-1]) == (320, 2.45, 3.8, 4.1)
need('은행 18곳 상품 39개 — 최저 1.90% · 중앙 3.33% · 최고 3.92%', '저축은행 79곳 상품 320개 — 최저 2.45% · 중앙 3.80% · 최고 4.10%')
NOW = dict(int=3390000, tax=522060, net=2867940, mon=238995); need('B 지금 은행 평균 3.39% → 세전 3,390,000 · 세금 522,060 · 세후 2,867,940 · 월로 나누면 238,995')
assert int(3390000 * 0.14 / 10) * 10 + int(3390000 * 0.014 / 10) * 10 == 522060 and round(2867940 / 12) == 238995
need('D 저축은행 공시 최고 4.10% → 세전 4,100,000 · 세금 631,400 · 세후 3,468,600')
CPI = (116.45, 120.05, 3.09); need('2025-08 116.45 → 2026-08 120.05, 1년 상승률 3.09%'); assert round((CPI[1] / CPI[0] - 1) * 100, 2) == 3.09
need('실질(세후 이자 - 3,090,000): A -966,540 · B -222,060', '세전 3.65% 이상'); assert 2867940 - 3090000 == -222060 and round(3.09 / 0.846, 2) == 3.65
need('금리 3.39%면 이자 1천만원(건보 지역 합산 [8]) = 원금 약 2억 9,499만 · 2천만원(종합과세 [7]·피부양자 [8]) = 약 5억 8,997만',
     '금리 4.10%면 1천만원 = 약 2억 4,390만', '예금자보호: 1억 넣으면 만기 채권 1억 339만(B)')
assert round(1e7 / 0.0339 / 1e4) == 29499 and round(2e7 / 0.0339 / 1e4) == 58997 and round(1e7 / 0.041 / 1e4) == 24390

SRC_ECOS = '한국은행 ECOS(121Y002 신규 정기예금 1년 · 731Y001 매매기준율 · 901Y009 소비자물가 · 722Y001 기준금리)'
SRC_ETF = '거래소 종가·분배금(야후 파이낸스 집계, SPY는 FMP 교차 · SCHD 분배금 찰스슈왑 원문) · 원/달러 ECOS 731Y001'
SRC_TAX = '소득세법 제94조·제103조·제104조·제129조 · 지방세법 제103조의3·제103조의13 (법제처 원문)'
SRC_FL = '금융감독원 금융상품통합비교공시(2026-09 공시, 12개월 정기예금 기본금리)'
SRC_TH = '예금자보호법 제32조·시행령 제18조 · 소득세법 제14조 · 국민건강보험법 시행규칙 제44조 (법제처 원문)'
PAST = '과거 값 · 미래 보장 아님 · 투자 권유 아님'
RAIL = ['예금 영수증', '달러로 바꾸면', '세 장 더', '순위', '지금 예금·물가·문턱']
B4 = [[NAME[k], RC[k]['net'], PRE[k], RC[k]['pct']] for k in ['DEP', 'SPY', 'SCHD', 'GLD']]   # 화면 순서 = 대본 첫 장면 순서

SPEC = [
    ('여는', lambda L: dict(kind='open4', title='1억의 1년 영수증', source='한국은행·금융감독원·법제처 원문, 거래소 종가 · ' + PAST,
                          data={'bars': B4, 'gap': GAP[0] - GAP[1], 'at': [0, L('그래서 1년 전'), L('하나만 먼저'), L('영수증을 한 줄씩')]})),
    ('로고', lambda L: dict(kind='logo', data={'sub': '1억의 1년 영수증 · 2025.10.2 → 2026.10.2'})),
    ('예금 영수증', lambda L: dict(kind='receipt', rail=1, title='예금 영수증', sub='2025년 10월 신규 1년 정기예금 평균 연 2.58% · 1억', source=SRC_ECOS.split(' · ')[0] + ') · ' + SRC_TAX.split(' · ')[0],
                                 data={'head': '정기예금 1년 · 1억', 'rows': [['이자', RC['DEP']['gain'], 'in'], ['세금 15.4%', -RC['DEP']['tax'], 'tax']],
                                       'net': RC['DEP']['net'], 'pct': RC['DEP']['pct'], 'split': ['소득세 14%', '지방소득세 1.4%'],
                                       'at': [0, L('258만원'), L('세금이 먼저'), L('39만 7천원')]})),
    ('달러로', lambda L: dict(kind='fx', rail=2, title='달러로 바꾸는 순간 생기는 줄', sub='원/달러 매매기준율 · 2025.10.2 → 2026.10.2', source=SRC_ECOS.split(' · ')[0].replace('121Y002 신규 정기예금 1년', '731Y001 매매기준율') + ')',
                            data={'a': FX[0], 'b': FX[1], 'pct': -3.30, 'loss': FXLOSS, 'names': ['S&P500', 'SCHD', '금'],
                                  'at': [0, L('1,406원'), L('제자리였어도'), L('환전 수수료')]})),
    ('sp:receipt', lambda L: dict(kind='receipt2', rail=3, title='S&P500 영수증', sub='SPY · 달러 기준 +15.01% · 원화로 계산', source=SRC_ETF,
                                  data={'head': 'S&P500 ETF(SPY) · 1억', 'usd': USD['SPY'], 'sell': RC['SPY']['sell'], 'gain': RC['SPY']['gain'], 'dist': RC['SPY']['dist'], 'n': 4,
                                        'at': [0, L('1억 1,122만원')]})),
    ('sp:tax', lambda L: dict(kind='taxcalc', rail=3, title='해외 ETF 차익에 붙는 세금', sub='원 · 다른 양도차익이 없다고 가정', source=SRC_TAX,
                              data={'gain': RC['SPY']['gain'], 'ded': 2500000, 'rate': 22, 'tax': RC['SPY']['tax'], 'at': [0, L('소득세 20%'), L('다른 데서')]})),
    ('sp:cal', lambda L: dict(kind='calendar', rail=3, title='이 세금은 다음 해 5월에', sub='양도소득세 확정신고 · 분배금 세금 줄은 비움', source=SRC_TAX + ' · ' + SRC_ETF.split(' · ')[0],
                              data={'net': RC['SPY']['net'], 'pct': RC['SPY']['pct'], 'tax': RC['SPY']['tax'], 'at': [0, L('그래서 팔고'), L('분배금에 붙는'), L('운용 보수')]})),
    ('sg:duo', lambda L: dict(kind='duo', rail=3, title='SCHD와 금 — 같은 계산', sub='원 · 세금 뒤 = 매도 + 분배금(세전) − 양도세', source=SRC_ETF,
                              data={'L': ['SCHD · 1억', [['매도', RC['SCHD']['sell']], ['분배금(세전)', RC['SCHD']['dist']], ['양도세', -RC['SCHD']['tax']]], RC['SCHD']['net'], RC['SCHD']['pct']],
                                    'R': ['금 ETF(GLD) · 1억', [['매도', RC['GLD']['sell']], ['분배금', 0], ['양도세', -RC['GLD']['tax']]], RC['GLD']['net'], RC['GLD']['pct']],
                                    'at': [0, L('1억 1,570만원')]})),
    ('sg:gold', lambda L: dict(kind='goldfx', rail=3, title='금은 환율이 주인공', sub='1억을 금 ETF(GLD)에 넣었다면 · 원', source=SRC_ETF,
                               data={'usdpct': USD['GLD'][2], 'fxpct': -3.30, 'gain': RC['GLD']['gain'],
                                     'net': RC['GLD']['net'], 'tax': RC['GLD']['tax'], 'at': [0, L('원화로 바꾸면'), L('이 기간 GLD')]})),
    ('rk:ranks', lambda L: dict(kind='ranks', rail=4, title='세금·환율을 떼면 순위가 바뀔까', sub='세전(분배금 포함) → 세금 뒤 통장 · 2025.10.2 하루에 넣은 경우', source=SRC_ETF + ' · ' + PAST,
                                data={'L': [[NAME[k], PRE[k]] for k in ORD], 'R': [[NAME[k], RC[k]['net']] for k in ORD], 'at': [0, L('안 뒤집혔어요'), L('다만 이건')]})),
    ('rk:gap', lambda L: dict(kind='gapbars', rail=4, title='달라진 건 간격', sub='원 · 예금 vs SCHD', source=SRC_ETF + ' · ' + SRC_TAX.split(' · ')[0],
                              data={'pre': [PRE['DEP'], PRE['SCHD']], 'net': [RC['DEP']['net'], RC['SCHD']['net']], 'gap': list(GAP), 'at': [0, L('세금 뒤에는'), L('251만원이')]})),
    ('now:line', lambda L: dict(kind='rateline', rail=5, title='은행 1년 정기예금 신규 금리', sub='% · 월 · 신규취급액 가중평균 · 2020.1~2026.8', source=SRC_ECOS,
                                data={'s': DEPM, 'base': BASE, 'dots': [['202211', 4.95], ['202508', 2.51], ['202608', 3.39]], 'at': [0, L('기준금리가'), L('2022년 11월')]})),
    ('now:receipt', lambda L: dict(kind='receipt', rail=5, title='지금 1억을 1년 넣으면', sub='은행 1년 예금 2026년 8월 신규 평균 3.39%', source=SRC_ECOS.split(' · ')[0] + ') · ' + SRC_TAX.split(' · ')[0],
                                   data={'head': '정기예금 1년 · 1억 · 3.39%', 'rows': [['이자', NOW['int'], 'in'], ['세금 15.4%', -NOW['tax'], 'tax']], 'net': NOW['net'], 'mon': NOW['mon'],
                                         'netLabel': '세후 이자', 'at': [0, 0, 0, 0]})),
    ('now:dots', lambda L: dict(kind='dots', rail=5, title='공시 금리는 넓게 퍼져 있다', sub='% · 12개월 정기예금 기본금리 · 상품 하나 = 점 하나', source=SRC_FL,
                                data={'rows': [['은행', DOTS['은행']], ['저축은행', DOTS['저축은행']]], 'avg': 3.39, 'at': [0, L('저축은행 320개'), L('공시 금리는 회사가')]})),
    ('물가와', lambda L: dict(kind='tug', rail=5, title='물가와 비교하면', sub='원 · 1억 기준 · 지난 1년 물가(2025.8→2026.8)', source=SRC_ECOS.split(' · ')[0] + ' · 901Y009 소비자물가)',
                            data={'net': NOW['net'], 'cpi': 3090000, 'diff': NOW['net'] - 3090000, 'need': 3.65, 'at': [0, L('22만 2천원'), L('물론 이건')]})),
    ('금액이', lambda L: dict(kind='pins', rail=5, title='금액이 커지면 만나는 문턱 세 개', sub='원금 · 금리 3.39%(은행 8월 신규 평균), 다른 금융소득 없음', source=SRC_TH,
                            data={'pins': [['1억', 10000, '예금자보호 한도(1인)'], ['약 2.95억', 29499, '지역 건보료에 금융소득 합산'], ['약 5.9억', 58997, '종합과세·피부양자 2천만원']],
                                  'alt': [24390, '4.1%면 2.44억으로 당겨짐'], 'at': [0, L('첫째'), L('둘째'), L('셋째'), L('금리가 오르면')]})),
    ('sum:card', lambda L: dict(kind='sum4', title='정리 — 1억의 1년 영수증', sub='2025.10.2 → 2026.10.2 · 양도세·이자 세금 뒤 · 분배금 세금 빠진 값', source=SRC_ETF + ' · ' + SRC_ECOS.split(' · ')[0] + ') · ' + PAST,
                                data={'rows': [[NAME[k], RC[k]['net'], RC[k]['pct']] for k in ORD], 'now': [3.39, NOW['mon'], 3.65], 'at': [0, L('지금 예금은')]})),
    ('sum:cta', lambda L: dict(kind='cta', title='1억이면 은퇴가 몇 년 당겨질까', sub='설명란 링크 — firemap.kr 은퇴 나이 계산기', source='파이어맵 계산기',
                               data={'x': 10000, 'at': [0]})),
]
SPLIT = {'S&P500 영수증': [('sp:receipt', None), ('sp:tax', '세금은 이렇게'), ('sp:cal', '참고로 이 세금')],
         'SCHD와 금': [('sg:duo', None), ('sg:gold', '금은 반대로')],
         '순위는': [('rk:ranks', None), ('rk:gap', '달라진 건')],
         '지금 1억이': [('now:line', None), ('now:receipt', '3.39%로 1억을'), ('now:dots', '금리 공시 쪽')],
         '정리': [('sum:card', None), ('sum:cta', '그럼 이 1억이')]}

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
json.dump(out, open(os.path.join(VID, 'r1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f'장 {len(scenes)} · 길이 {sum(s["frames"] for s in scenes)/FPS/60:.1f}분 · 목소리 없는 문장 {missing}')
kinds = sorted({s['kind'] for s in scenes}); print('종류', len(kinds), kinds)
bad = [(s['title'], i) for s in scenes for i, x in enumerate(s['data'].get('at', [])) if x == -1]
if bad: print('문장 못 찾은 단계', bad)
for s in scenes: print(f"  {s['kind']:9} {s['frames']/FPS:5.1f}초 문장{len(s['lines'])}  {s['title']}")
long = [(s['title'], round(s['frames'] / FPS, 1)) for s in scenes if s['frames'] / FPS > 40]
if long: print('40초 넘는 장(단계 더 필요)', long)
