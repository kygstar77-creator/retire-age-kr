# R-1 화면 재료 v6 — script.v6.md(장·문장·[자막]) + voice.json(있으면 길이) + 원자료 → work/video/r1.json (Remotion R1 컴포지션이 읽는다)
#   python3 work/research/longform/ep/R-1/r1props.py [--script script.v6.md]
# 숫자는 전부 calc2_out.txt(영수증)·raw/collect_20261003.json(금리·공시)·facts.txt 원문 줄에서 온다 — 코드 안 숫자는 facts 줄과 기계 대조한다(need·assert).
# 화면 글자(valueText 등)는 facts.txt 문구를 그대로 쓰고, 막대 높이만 계산값을 쓴다.
# 목소리가 없는 문장은 길이를 '말하는 글자(한글+숫자) ÷ 5.65음절/초'로 잡는다(RULES '목소리 한결같음' — Charon 고정 속도, 장면이 목소리를 따라감).
# 목소리가 생기면(voice.json에 같은 문장 + audio) 그 길이를 쓴다. 업로드는 missing=0일 때만.
# v5용(장면 17종, script.md) 옛 판은 git 기록(2026-10-03 dev 719eadc9)에 있다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC   # parse(대본) · syl · speak — lfvoice와 같은 규칙(numpy 없이)
RATE = 5.65
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
    RC[k] = dict(sell=num(m[2]), gain=num(m[3]), dist=num(m[4]), tax=num(m[5]), net=num(m[6]), pct=float(m[7]))   # tax = 양도세 + 분배금 원천징수 15% [15]
    RC[k]['wht'] = int(RC[k]['dist'] * 0.15); RC[k]['cgt'] = RC[k]['tax'] - RC[k]['wht']
assert sorted(RC) == ['DEP', 'GLD', 'SCHD', 'SPY'], RC
need('예금(2025-10 신규 평균 2.58%): 이자 2,580,000 · 세금 397,320 · 통장 102,182,680 (+2.18%)',
     '금(GLD): 매도 103,609,129(차익 3,609,129) · 분배 0 · 양도세 244,007 · 통장 103,365,122 (+3.37%)',
     'S&P500(SPY): 매도 111,210,188(차익 11,210,188) · 분배(세전) 1,095,716 · 분배 원천징수 15% 164,357 · 양도세 1,916,240 · 통장 110,225,307 (+10.23%)',
     'SCHD: 매도 115,728,578(차익 15,728,578) · 분배(세전) 3,728,285 · 분배 원천징수 15% 559,242(세후 3,169,043) · 양도세 2,910,286 · 통장 115,987,335 (+15.99%)')
for k, line in [('DEP', (2580000, 0, 397320, 102182680)), ('GLD', (3609129, 0, 244007, 103365122)), ('SPY', (11210188, 164357, 1916240, 110225307)), ('SCHD', (15728578, 559242, 2910286, 115987335))]:
    assert (RC[k]['gain'], RC[k]['wht'], RC[k]['cgt'], RC[k]['net']) == line, k
    assert abs(RC[k]['net'] - (100_000_000 + RC[k]['gain'] + RC[k]['dist'] - RC[k]['tax'])) <= 1, k     # 통장 = 원금 + 차익 + 분배 − 세금
# 해외 양도세 = (차익 − 250만) × 22%, 원 미만 버림 [13]
for k in ['SPY', 'SCHD', 'GLD']: cg = max(0, RC[k]['gain'] - 2_500_000); assert abs(RC[k]['cgt'] - (int(cg * 0.20) + int(cg * 0.02))) <= 1, k
assert RC['DEP']['tax'] == 397320 and int(2580000 * 0.14 / 10) * 10 + int(2580000 * 0.014 / 10) * 10 == 397320
FX = (1406.0, 1359.6); need('2025-10-02 1,406.0원 → 2026-10-02 1,359.6원 (-3.30%)', '약 -330만원(3,300,142)')
assert '환율 효과만 -3,300,142원' in C2; FXLOSS = 3300142
USD = {'SPY': (669.22, 769.64, 15.01), 'SCHD': (27.34, 32.72, 19.68), 'GLD': (354.79, 380.14, 7.15)}
need('SPY 669.22 → 769.64(+15.01%)', 'SCHD 27.34 → 32.72(+19.68%)', 'GLD 354.79 → 380.14(+7.15%)')
for k, (a, b, p) in USD.items(): assert abs((b / a - 1) * 100 - p) < 0.015, k   # 종가 표시는 소수 2자리라 0.01%p 차 허용
PRE = {k: RC[k]['sell'] + RC[k]['dist'] for k in RC}; PRE['DEP'] = 102_580_000          # 세전(분배 포함)
ORD = ['SCHD', 'SPY', 'GLD', 'DEP']
assert sorted(PRE, key=lambda k: -PRE[k]) == ORD and sorted(RC, key=lambda k: -RC[k]['net']) == ORD
GAP = (PRE['SCHD'] - PRE['DEP'], RC['SCHD']['net'] - RC['DEP']['net'])
need('예금 vs SCHD 차이: 세전 16,876,863', '→ 통장 13,804,655', '약 307만원 줄였다(3,072,208)'); assert GAP == (16876863, 13804655) and GAP[0] - GAP[1] == 3072208
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


# ── v6 추가 확인 ──
need('연평균: 2020 1.16 · 2021 1.19 · 2022 3.11 · 2023 3.84 · 2024 3.48 · 2025 2.73 · 2026(1~8월) 3.11')
YEARLY = [['2020', 1.16], ['2021', 1.19], ['2022', 3.11], ['2023', 3.84], ['2024', 3.48], ['2025', 2.73], ['2026', 3.11]]
for y, v in YEARLY:   # 월 자료(raw)로 다시 평균 내서 facts 값과 같은지
    ms = [x for t, x in DEPM if t.startswith(y)]
    assert round(sum(ms) / len(ms) + 1e-9, 2) == v, (y, sum(ms) / len(ms))
assert len([t for t, _ in DEPM if t.startswith('2026')]) == 8
need('2026-07 2.75% → 2026-08 3.0%'); need('A 1년 전 은행 평균 2.51% → 세전 2,510,000 · 세금 386,540 · 세후 2,123,460')
need('B-A 1년 새 세후 이자 +744,480'); need('"60만원" ← 600,660'); assert 3468600 - 2867940 == 600660 and 2867940 - 2123460 == 744480

SRC_DEP = '한국은행 ECOS 121Y002(은행 신규 정기예금 1년 가중평균) · 소득세법 제129조 · 지방세법 제103조의13'
SRC_FX = '한국은행 ECOS 731Y001(원/달러 매매기준율)'
SRC_ETF = '거래소 종가·분배금(야후 파이낸스·나스닥, SCHD 분배금은 찰스슈왑 원문) · 원/달러 ECOS 731Y001'
SRC_TAX = '소득세법 제94·103·104·110조 · 지방세법 제103조의3 · 한미 조세조약 제12조(IRS Table 1)'
SRC_RATE = '한국은행 ECOS 121Y002(신규 정기예금 1년) · 722Y001(기준금리)'
SRC_FL = '금융감독원 금융상품통합비교공시(2026년 9월, 12개월 정기예금 기본금리)'
SRC_CPI = '한국은행 ECOS 901Y009(소비자물가지수) · 121Y002'
SRC_TH = '예금자보호법 제32조·시행령 제18조 · 소득세법 제14조 · 국민건강보험법 시행규칙 제44조'
PAST = '과거 값 · 미래 보장 아님 · 투자 권유 아님'
won = lambda v: f'{v:,}'
PCT = {k: f"+{RC[k]['pct']:.2f}%" for k in RC}
SAYNET = {'SCHD': '1억 1,599만원', 'SPY': '1억 1,023만원', 'GLD': '1억 337만원', 'DEP': '1억 218만원'}
need(*SAYNET.values())
NAME = {'DEP': '예금', 'SPY': 'S&P500', 'SCHD': 'SCHD', 'GLD': '금'}

# 장면 = (키, 장 번호, 시작 문장 조각 — None이면 장 처음부터)
CUTS = [('open', '0.', None), ('road', '0.', '오늘 순서는'), ('logo', '로고', None), ('dep', '1.', None), ('fx', '2.', None),
        ('spy', '3.', None), ('spytax', '3.', '자, 이제 세금이에요'), ('spycal', '3.', '그런데 이 세금은 좀 특이해요'),
        ('schd', '4.', None), ('gold', '5.', None), ('rank', '6.', None), ('gap', '6.', '그럼 세금은 아무것도'), ('mine', '6-1.', None),
        ('rate', '7.', None), ('now', '7.', '그럼 지금 평균 금리로'), ('posted', '7.', '이번엔 은행들이 내건'),
        ('cpi', '8.', None), ('thresh', '9.', None), ('sum', '10.', None), ('cta', '10.', '이제 여러분 차례예요')]


def spec(key, L, A):
    """L(조각) = 장면 안 문장 번호, A(조각, 더할 프레임) = 그 문장 시작 프레임(장면 안 기준)"""
    if key == 'open':
        return dict(kind='open', title='1억, 어디에 두면 1년 뒤 얼마가 남을까', sub='2025년 10월 2일에 넣고 2026년 10월 2일에 뺐다면 · 세금·환율 뗀 뒤',
                    source='한국은행·금융감독원·법제처 원문, 거래소 종가 · ' + PAST,
                    data={'bars': [[NAME[k], A('통장에 1억', 8 + 7 * i)] for i, k in enumerate(['DEP', 'SPY', 'SCHD', 'GLD'])], 'q': A('네 군데에', 0)})
    if key == 'road':
        items = ['예금 영수증', '달러로 바꿀 때 생기는 줄', '미국 ETF 영수증 세 장', '순위는 바뀌었을까', '지금 예금은 얼마를 줄까']
        return dict(kind='road', title='오늘 확인할 다섯 가지', sub=None, source=None,
                    data={'rows': [[f'{"①②③④⑤"[i]}  {t}', A('예금 영수증,' if i < 4 else '마지막으로', 10 + (i if i < 4 else 0) * 16)] for i, t in enumerate(items)]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': '1억의 1년 영수증 · 2025.10.2 → 2026.10.2'})
    if key == 'dep':
        return dict(kind='receipt', title='예금 영수증', sub='2025년 10월 새로 가입한 1년 정기예금 평균 금리로 1억', source=SRC_DEP,
                    data={'head': '정기예금 1년 · 연 2.58% · 단위 원',
                          'rows': [['넣은 돈', won(100_000_000), 'in', 0], ['이자', '+' + won(RC['DEP']['gain']), 'in', A('258만원', 0)],
                                   ['세금 15.4%', '−' + won(RC['DEP']['tax']), 'tax', A('40만원', 0)], ['1년 뒤 통장', won(RC['DEP']['net']), 'net', A('2.18%', 0)]],
                          'side': [PCT['DEP'], A('2.18%', 10), '넣은 돈보다 늘어난 비율']})
    if key == 'fx':
        return dict(kind='fx', title='달러로 바꿀 때 생기는 줄', sub='1달러를 사는 데 드는 원화 · 작년 그날과 올해 같은 날', source=SRC_FX,
                    data={'a': '1,406.0원', 'b': '1,359.6원', 'av': FX[0], 'bv': FX[1], 'start': A('올해 같은 날', 0), 'aAt': A('1,406원', 0), 'pct': '달러 값 −3.30%',
                          'loss': '−' + won(FXLOSS) + '원', 'lossAt': A('330만원', 0), 'blankAt': A('환전 수수료', 0)})
    if key == 'spy':
        return dict(kind='receipt', title='S&P500 영수증', sub='SPY · 달러로 사서 1년 뒤 원화로 판 값 · 1억', source=SRC_ETF,
                    data={'head': 'S&P500 ETF(SPY) · 1억 · 단위 원', 'side': ['+15.01%', A('약 15%', 10), '달러로 1년 동안 오른 폭'],
                          'rows': [['달러로 오른 폭', '+15.01%', 'in', A('약 15%', 0)], ['원화로 판 돈', won(RC['SPY']['sell']), 'in', A('1,121만원', 0)],
                                   ['그중 이익', won(RC['SPY']['gain']), 'hi', A('1,121만원', 18)], ['분배금 4번(세금 전)', '+' + won(RC['SPY']['dist']), 'in', A('110만원', 0)]]})
    if key == 'spytax':
        return dict(kind='receipt', title='세금은 두 군데서 뗀다', sub='분배금은 미국에서 15% · 판 이익은 공제 250만원 넘는 부분에 22%', source=SRC_TAX,
                    data={'head': 'SPY 세금 계산 · 단위 원', 'side': ['22%', A('22%를', 10), '공제 250만원 넘는 이익에 붙는 세율'],
                          'rows': [['분배금에서 (미국 15%)', '−' + won(RC['SPY']['wht']), 'tax', A('16만원', 0)], ['판 이익', won(RC['SPY']['gain']), 'in', A('판 이익에 붙는', 0)],
                                   ['빼 주는 돈(공제)', '−2,500,000', 'dim', A('250만원까지는', 0)], ['곱하는 세율', '× 22%', 'in', A('22%를', 0)],
                                   ['판 이익 세금', '−' + won(RC['SPY']['cgt']), 'tax', A('192만원', 0)]]})
    if key == 'spycal':
        return dict(kind='zoom', title='판 이익 세금은 나중에 낸다', sub='팔 때 바로 빠지지 않는다 — 직접 신고하고 낸다', source=SRC_TAX,
                    data={'text': '다음 해 5월', 'label': '판 이익 세금 내는 때', 'note': '확정신고 기간 5월 1일~31일', 'start': A('다음 해 5월', 0),
                          'after': ['세금 뒤 통장', won(RC['SPY']['net']) + '원', PCT['SPY'], A('10% 조금', 0)]})
    if key == 'schd':
        return dict(kind='receipt', title='SCHD 영수증', sub='배당 ETF · 계산 방법은 S&P500과 같다 · 1억', source=SRC_ETF,
                    data={'head': 'SCHD · 1억 · 단위 원', 'side': ['+15.99%', A('16% 가까이', 10), '세금 뗀 뒤, 넣은 돈보다 늘어난 비율'],
                          'rows': [['달러로 오른 폭', '+19.68%', 'in', A('약 20%', 0)], ['원화로 판 돈', won(RC['SCHD']['sell']), 'in', A('약 20%', 30)],
                                   ['분배금 4번(세금 전)', '+' + won(RC['SCHD']['dist']), 'in', A('373만원', 0)], ['미국이 뗀 세금 15%', '−' + won(RC['SCHD']['wht']), 'tax', A('56만원', 0)],
                                   ['판 이익 세금', '−' + won(RC['SCHD']['cgt']), 'tax', A('291만원', 0)], ['세금 뒤 통장', won(RC['SCHD']['net']), 'net', A('16% 가까이', 0)]]})
    if key == 'gold':
        return dict(kind='bars', title='금은 환율이 주인공', sub='GLD · 같은 1년을 두 가지로 잰 늘어난 비율', source=SRC_ETF,
                    data={'dir': 'v', 'max': 8, 'bars': [['달러로 잰 오른 폭', 7.15, '+7.15%', A('약 7%', 0), 'ink'], ['원화로, 세금 뗀 뒤', 3.37, '+3.37%', A('3% 조금', 0), 'accent']],
                          'note': ['환율 −3.30%가 깎아 먹음', A('361만원', 0)]})
    if key == 'rank':
        bars = [[NAME[k], RC[k]['net'] - 100_000_000, SAYNET[k], A('맨 위' if k == 'SCHD' else '그다음이', 0 if k == 'SCHD' else 14 * i),
                 'accent' if k == 'SCHD' else 'ink', PCT[k]] for i, k in enumerate(ORD)]
        return dict(kind='bars', title='세금·환율 뗀 뒤 순위', sub='2025년 10월 2일 하루에 넣은 경우 · 막대 = 넣은 돈 1억보다 늘어난 만큼', source=SRC_ETF + ' · ' + PAST,
                    data={'dir': 'v', 'max': 17_000_000, 'bars': bars, 'note': ['세금 떼기 전에도 같은 순서', A('맨 위', 0)]})
    if key == 'gap':
        return dict(kind='count', title='달라진 건 간격', sub='SCHD와 예금, 통장에 남은 돈의 차이', source=SRC_ETF + ' · ' + SRC_TAX.split(' · ')[0],
                    data={'from': GAP[0], 'to': GAP[1], 'text': won(GAP[1]) + '원', 'label': 'SCHD − 예금, 세금 뗀 뒤', 'start': A('세금을 떼고 나니', 0),
                          'pre': '세금 떼기 전 ' + won(GAP[0]) + '원', 'preAt': A('1,688만원', 0), 'cut': '세금이 줄인 간격 ' + won(GAP[0] - GAP[1]) + '원', 'cutAt': A('307만원', 0)})
    if key == 'mine':
        return dict(kind='receipt', title='내 돈에 옮겨 보려면', sub='넣은 돈에 비례하는 줄과, 비례하지 않는 줄', source=None,
                    data={'head': '영수증 줄 나눠 보기', 'side': ['두 줄만 조심', A('다만 비례하지', 10), '나머지 줄은 돈에 비례'],
                          'rows': [['이자 · 분배금', '돈에 비례', 'dim', A('대부분의 줄', 0)], ['환율로 빠지는 돈', '돈에 비례', 'dim', A('대부분의 줄', 16)],
                                   ['판 이익 공제 250만원', '금액 고정', 'hi', A('하나는 판 이익', 0)], ['문턱 세 개', '넘으면 걸림', 'hi', A('다른 하나는', 0)]]})
    if key == 'rate':
        bars = [[y if y != '2026' else '2026(1~8월)', v, f'{v:.2f}%', A('한 해 평균으로', 12 + 12 * i), 'accent' if y == '2026' else 'ink'] for i, (y, v) in enumerate(YEARLY)]
        return dict(kind='bars', title='은행 1년 예금 금리, 한 해 평균', sub='% · 새로 가입한 예금 기준(실제 가입 금리) · 2026년은 1~8월', source=SRC_RATE,
                    data={'dir': 'v', 'max': 4.5, 'bars': bars, 'note': ['지금(2026년 8월) 3.39% · 기준금리 3.0%', A('기준금리가', 0)]})
    if key == 'now':
        return dict(kind='receipt', title='지금 1억을 1년 넣으면', sub='2026년 8월 새로 가입한 1년 예금 평균 3.39% 기준', source=SRC_DEP,
                    data={'head': '정기예금 1년 · 연 3.39% · 단위 원',
                          'rows': [['이자', '+' + won(NOW['int']), 'in', A('339만원', 0)], ['세금 15.4%', '−' + won(NOW['tax']), 'tax', A('52만원', 0)],
                                   ['세금 뒤 이자', won(NOW['net']), 'net', A('287만원', 0)], ['한 달로 나누면', won(NOW['mon']), 'hi', A('24만원', 0)]],
                          'side': ['작년 금리(2.51%)였다면', A('212만원', 0), '세금 뒤 이자 2,123,460원']})
    if key == 'posted':
        return dict(kind='bars', title='은행들이 내건 금리', sub='1년 예금 상품마다 내건 기본금리 · 가장 낮은 곳 ~ 가장 높은 곳', source=SRC_FL,
                    data={'dir': 'h', 'min': 1.5, 'max': 4.5,
                          'bars': [['은행', 3.92, '3.92%', A('은행 상품은', 0), 'ink', '상품 39개', 1.90, '1.90%'],
                                   ['저축은행', 4.10, '4.10%', A('저축은행은', 0), 'ink', '상품 320개', 2.45, '2.45%']],
                          'marker': [3.39, '실제 가입 평균 3.39%', A('공시 금리는', 0)]})
    if key == 'cpi':
        return dict(kind='bars', title='이자가 물가를 따라갔을까', sub='1억 기준 · 지난 1년(2025년 8월 → 2026년 8월) 물가 +3.09%', source=SRC_CPI,
                    data={'dir': 'v', 'max': 3_400_000,
                          'bars': [['세금 뗀 이자', NOW['net'], won(NOW['net']) + '원', A('287만원', 0), 'ink'], ['물가만큼 필요한 돈', 3_090_000, '3,090,000원', A('309만원', 0), 'rise']],
                          'note': ['모자란 돈 −222,060원', A('22만원', 0)]})
    if key == 'thresh':
        return dict(kind='bars', title='금액이 커지면 만나는 문턱 세 개', sub='넣은 돈(원금) 기준 · 금리 3.39% · 다른 금융소득은 없다고 가정', source=SRC_TH,
                    data={'dir': 'h', 'min': 0, 'max': 72000,
                          'bars': [['예금자보호 한도', 10000, '1억원', A('첫 번째 문턱', 0), 'ink', '한 사람 기준'],
                                   ['건보료에 이자 합산', 29499, '약 2억 9,499만원', A('두 번째 문턱', 0), 'ink', '이자 1천만원 넘으면'],
                                   ['종합과세·피부양자', 58997, '약 5억 8,997만원', A('세 번째 문턱', 0), 'ink', '이자 2천만원 넘으면']]})
    if key == 'sum':
        return dict(kind='receipt', title='정리 — 1억의 1년 영수증', sub='2025.10.2 → 2026.10.2 · 세금(이자·분배금·판 이익)과 환율을 다 뗀 뒤', source=SRC_ETF + ' · ' + PAST,
                    data={'head': '세금 뒤 통장', 'side': ['순위 그대로', A('순위는 그대로', 10), '세금은 간격만 줄였다'],
                          'rows': [[f'{NAME[k]}  {PCT[k]}', SAYNET[k], 'net' if k == 'SCHD' else 'in', A(['SCHD는', 'SPY는', '금은', '예금은'][i], 0)] for i, k in enumerate(ORD)]})
    if key == 'cta':
        return dict(kind='zoom', title='이 돈이면 은퇴가 몇 년 당겨질까', sub='설명란 링크 · firemap.kr 은퇴 나이 계산기', source='파이어맵 은퇴 나이 계산기',
                    data={'text': '1억', 'card': '파이어맵 은퇴 나이 계산기', 'label': '계산기 자산 칸에 넣어 보기', 'note': '내 은퇴 나이가 바로 나온다', 'start': A('궁금하시면', 0)})
    raise KeyError(key)


def main(script):
    path = os.path.join(EP, script)
    secs = SC.parse(path)
    # 문장마다 [자막] 붙이기: '- ' 줄 바로 뒤의 [자막] 줄을 그 문장에 붙인다
    caps, last = {}, None
    for line in open(path, encoding='utf-8').read().split('\n---', 1)[0].splitlines():
        s = line.strip()
        if s.startswith('- '):
            last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
        elif s.startswith('[자막:') and last:
            caps[last] = s[4:].rstrip(']').strip()
    voice = {}
    vj = os.path.join(EP, 'voice.json')
    if os.path.exists(vj):
        for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
            for l in s['lines']:
                if l.get('audio'): voice[l['text']] = l

    def chap(title):
        return re.sub(r'^\[', '', title).split()[0].rstrip(']')
    scenes = []
    for key, ch, start in CUTS:
        sec = next(s for s in secs if chap(s['title']) == ch)
        lines = sec['lines']
        cuts = [c for c in CUTS if c[1] == ch]
        idx = [0 if c[2] is None else next(j for j, t in enumerate(lines) if t.startswith(c[2])) for c in cuts]
        me = [c[0] for c in cuts].index(key)
        part = lines[idx[me]:(idx[me + 1] if me + 1 < len(idx) else None)]
        out = []
        for t in part:
            v = voice.get(t)
            fr = v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / RATE * FPS))
            out.append({'text': t, 'cap': caps.get(t), 'frames': fr, 'audio': v['audio'] if v else None})

        def L(w, _p=part):
            return next((j for j, t in enumerate(_p) if w in t), -1)

        def A(w, plus=0, _o=out, _k=key):
            j = L(w)
            assert j >= 0, (_k, w)
            return sum(x['frames'] for x in _o[:j]) + plus
        d = spec(key, L, A)
        frames = sum(x['frames'] for x in out) if out else 72
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch in ('0.', '로고') else ('6장 · 덧붙임' if ch == '6-1.' else ch.rstrip('.') + '장'),
                       'data': d['data'], 'lines': out, 'frames': frames})
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'script': script, 'rate': RATE}
    json.dump(res, open(os.path.join(VID, 'r1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 목소리 없는 문장 {missing} · 종류 {sorted({s["kind"] for s in scenes})}')
    for s in scenes:
        print(f"  {s['key']:7} {s['kind']:8} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[a.index('--script') + 1] if '--script' in a else 'script.v6.md')
