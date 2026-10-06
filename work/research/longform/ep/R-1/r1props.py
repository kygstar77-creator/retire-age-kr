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

# ── additions-1003 확인(facts.txt [add-1003 …] 줄과 원자료) ──
need('[add-1003 B1]', '최고 1,554.4원(2026-07-02), 최저 1,337.9원(2026-09-10)', '2026-07-02 123,037,245원(최고 구간) → 2026-09-10 107,755,946원',
     '2026-01-28 143,638,454원(가장 높은 날) → 2026-09-28 102,425,567원(−28.69%)', 'SPY 최저 2025-10-10 97,294,730원(−2.71%)',
     '1.0339달러 → +1.95%', '905,832원(12/15, 1,472.5원) · 856,702원(3/30, 1,508.1원) · 862,184원(6/29, 1,544.2원) · 796,727원(9/28, 1,352.0원), 합 3,421,445원',
     '252,402원 더 많다', '지급일이 2026-10-30', '세전 272,929원',
     'GLD>SPY>SCHD 153일 · GLD>SCHD>SPY 34일 · SCHD>GLD>SPY 34일 · SCHD>SPY>GLD 25일 · SPY>GLD>SCHD 4일 · SPY>SCHD>GLD 1일', '251일 중 25일(10.0%), 금이 1위인 날이 187일(74.5%)',
     '월 285,120원꼴', '월 68,930원', '하한 22,800원 → 월 46,130원, 1년 553,560원 더', '19.3%가 건보료 증가분', '2,574만원 폭', '1,528만원이 환율로 빠진 구간')
assert 153 + 34 + 34 + 25 + 4 + 1 == 251 and round(25 / 251 * 100, 1) == 10.0 and round(187 / 251 * 100, 1) == 74.5 and 153 + 34 == 187
assert 905832 + 856702 + 862184 + 796727 == 3421445 and 3421445 - 3169043 == 252402 and round(3421445 / 12) == 285120
assert 68930 - 22800 == 46130 and 46130 * 12 == 553560 and 123037245 - 97294730 == 25742515 and 123037245 - 107755946 == 15281299

# 1년 원화 평가액(분배금 빼고 세전) — raw/yahoo 종가 × ECOS 매매기준율(그날 또는 직전 한국 영업일), 1억 ÷ 1,406원 ÷ 시작 종가 주수 [add-1003 B2~B5]
import bisect
YH = json.load(open(os.path.join(EP, 'raw', 'yahoo_20261003.json'), encoding='utf-8'))
C2R = json.load(open(os.path.join(EP, 'raw', 'collect2_20261003.json'), encoding='utf-8'))
FXD = [(d, float(v)) for d, v in C2R['USDKRW_D']]; FXK = [d for d, _ in FXD]
def won_series(t):
    res = []
    for d, p in sorted(YH[t]['px'].items()):
        k = d.replace('-', '')
        if '20251002' <= k <= '20261002':
            res.append((k, 1e8 / FX[0] / USD[t][0] * p * FXD[bisect.bisect_right(FXK, k) - 1][1]))
    return res
SW = {t: won_series(t) for t in ['SPY', 'SCHD', 'GLD']}
for t, d, v in [('SPY', '20260702', 123037245), ('SPY', '20260910', 107755946), ('SPY', '20251010', 97294730), ('GLD', '20260128', 143638454), ('GLD', '20260928', 102425567)]:
    assert abs(dict(SW[t])[d] - v) < 20, (t, d, dict(SW[t])[d])     # 주수 반올림 차이 몇 원
SWI = {t: {d: i for i, (d, _) in enumerate(SW[t])} for t in SW}

# 장면 = (키, 장 번호, 시작 문장 조각 — None이면 장 처음부터). 장면마다 20~40초, 그 안에서 문장마다 표시가 하나씩 더해진다.
CUTS = [('open', '0.', None), ('promise', '0.', '파이어맵은 이렇게'), ('logo', '로고', None),
        ('dep', '1.', None), ('fx', '2.', None), ('swing', '2.', '그런데 시작과 끝만'),
        ('spy', '3.', None), ('spytax', '3.', '자, 이제 세금이에요'), ('spycal', '3.', '그런데 이 세금은 좀 특이해요'),
        ('schd', '4.', None), ('gold', '5.', None),
        ('rank', '6.', None), ('gap', '6.', '그럼 세금은 아무것도'), ('start', '6.', '그런데 여기서 반론'),
        ('caseA', '7.', None),
        ('sum', '8.', None), ('end', '8.', '오늘 숫자는 모두')]
# v7(10/6, 무료 TTS 한 창 100줄): road·schdfx·caseB·rate·now·posted·cpi·when·thresh·caseC·act 장면은 대본에서 빠져 CUTS에서도 뺐다(spec 코드는 다음 편 재료로 남김 — leftover.md)
END_MIN = 20 * FPS   # 끝 화면(엔드 스크린) 자리는 마지막 20초 이상 — YouTube 도움말 '동영상 마지막 5~20초에 추가'(검색 요약만 봄)
SRC_ADD = '야후 파이낸스 종가 × 한국은행 ECOS 731Y001 매매기준율(파이어맵 계산)'


def R(rows):   # [label, value, tone, at]
    return rows


def spec(key, L, A):
    if key == 'open':
        return dict(kind='open', title='1억, 1년 뒤 얼마가 남을까', sub='2025.10.2에 넣고 2026.10.2에 뺐다면 — 세금·환율 뗀 뒤', source='한국은행·금융감독원·법제처 원문, 거래소 종가 · ' + PAST,
                    data={'bars': [[NAME[k], A('통장에 1억', 8 + 7 * i)] for i, k in enumerate(['DEP', 'SPY', 'SCHD', 'GLD'])], 'q': A('예금에 넣으시겠어요', 0),
                          'gap': A('결과부터', 0), 'gapText': '세금이 줄인 간격 ' + won(GAP[0] - GAP[1]) + '원'})
    if key == 'promise':
        return dict(kind='promise', title='1억의 1년 영수증', sub='공식 원문 숫자로, 내 돈에 실제로 남는 금액만', source='한국은행 ECOS · 금융감독원 · 법제처 · 거래소 종가',
                    data={'stamp': A('오늘은', 0), 'rows': [['원문 숫자', '한국은행·금감원·법령', 'in', A('파이어맵은', 10)], ['세금', '이자·분배금·판 이익', 'in', A('파이어맵은', 22)],
                                                             ['환율', '산 날·판 날 매매기준율', 'in', A('파이어맵은', 34)], ['남는 돈', '통장에 찍히는 금액', 'net', A('파이어맵은', 46)]],
                          'q': A('그럼 순위까지', 0)})
    if key == 'road':
        items = ['예금 영수증', '달러로 바꿀 때 생기는 줄', '미국 ETF 영수증 세 장', '순위 · 반론', '사람마다 · 지금 예금']
        return dict(kind='road', title='오늘 확인할 다섯 가지', sub='영수증 순서대로', source=None,
                    data={'rows': [[f'{"①②③④⑤"[i]}  {t}', A('예금 영수증,' if i < 4 else '마지막으로', 10 + (i if i < 4 else 0) * 16)] for i, t in enumerate(items)]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': '1억의 1년 영수증 · 1편 · 2025.10.2 → 2026.10.2'})
    if key == 'dep':
        return dict(kind='receipt', title='예금 영수증', sub='2025년 10월 새로 가입한 1년 정기예금 평균 연 2.58%', source=SRC_DEP,
                    data={'head': '정기예금 1년 · 1억 · 단위 원', 'rows': R([['넣은 돈', won(100_000_000), 'in', 0], ['이자 연 2.58%', '+' + won(RC['DEP']['gain']), 'in', A('258만원', 0)],
                                                                    ['세금 15.4%', '−' + won(RC['DEP']['tax']), 'tax', A('39만 7천원', 0)], ['1년 뒤 통장', won(RC['DEP']['net']), 'net', A('2.18%', 0)]]),
                          'side': [PCT['DEP'], A('2.18%', 10), '넣은 돈보다 늘어난 비율'], 'callout': ['받을 돈이 처음부터 정해짐', A('줄이 몇 개 없죠', 0)]})
    if key == 'fx':
        return dict(kind='fx', title='달러로 바꿀 때 생기는 줄', sub='1달러를 사는 데 드는 원화 — 작년 그날과 올해 같은 날', source=SRC_FX,
                    data={'a': '1,406.0원', 'b': '1,359.6원', 'av': FX[0], 'bv': FX[1], 'start': A('올해 같은 날', 0), 'aAt': A('1,406원', 0), 'pct': '달러 값 −3.30%',
                          'loss': '−' + won(FXLOSS) + '원', 'lossAt': A('330만원', 0), 'meanAt': A('꼼짝도 안 했어도', 0)})
    if key == 'swing':
        step = 2
        pts = {t: [round(v / 1e4) for _, v in SW[t][::step]] for t in SW}
        n = len(pts['SPY']); idx = lambda t, d: SWI[t][d] / step
        months = [(i // step, f'{int(d[4:6])}월') for i, (d, _) in enumerate(SW['SPY']) if d[6:8] <= '07' and (i == 0 or SW['SPY'][i - 1][0][4:6] != d[4:6])][::2]
        return dict(kind='swing', title='1년 안에서는 훨씬 크게 흔들렸다', sub='1억을 넣었다면 매일의 원화 평가액(분배금 빼고 세금 전) · 만원', source=SRC_ADD,
                    data={'series': [['S&P500', 'ink', pts['SPY']], ['SCHD', 'ink3', pts['SCHD']], ['금', 'accent', pts['GLD']]], 'n': n, 'min': 9000, 'max': 15000,
                          'draw': A('그런데 시작과 끝만', 0), 'xlabels': months,
                          'tags': [['SPY', idx('SPY', '20260702'), 12304, '7.2 · 123,037,245원', A('두 달 남짓', 0), 'up', False],
                                   ['SPY', idx('SPY', '20260910'), 10776, '9.10 · 107,755,946원', A('두 달 남짓', 14), 'left', False],
                                   ['GLD', idx('GLD', '20260128'), 14364, '1.28 · 143,638,454원', A('금은 더 컸어요', 0), 'up', True],
                                   ['GLD', idx('GLD', '20260928'), 10243, '9.28 · 102,425,567원 (−28.69%)', A('금은 더 컸어요', 16), 'down', True]],
                          'fxAt': A('가장 높았던 날은', 0), 'fx': ['환율 최고 1,554.4원', '최저 1,337.9원']})
    if key == 'spy':
        return dict(kind='receipt', title='S&P500 영수증', sub='SPY · 달러로 사서 1년 뒤 원화로 판 값', source=SRC_ETF,
                    data={'head': 'S&P500 ETF(SPY) · 1억 · 단위 원', 'side': ['+15.01%', A('약 15%', 10), '달러로 1년 동안 오른 폭'],
                          'rows': R([['달러로 오른 폭', '+15.01%', 'in', A('약 15%', 0)], ['원화로 판 돈', won(RC['SPY']['sell']), 'in', A('1,121만원', 0)],
                                     ['그중 이익', won(RC['SPY']['gain']), 'hi', A('1,121만원', 18)], ['분배금 4번(세금 전)', '+' + won(RC['SPY']['dist']), 'in', A('110만원', 0)],
                                     ['그중 네 번째(10.30 입금)', '272,929', 'dim', A('재밌는 건', 0)]]),
                          'callout': ['판 날보다 4주 늦게 들어오는 분배금', A('재밌는 건', 10)]})
    if key == 'spytax':
        return dict(kind='receipt', title='세금은 두 군데서 뗀다', sub='분배금은 미국에서 15% · 판 이익은 250만원 넘는 부분에 22%', source=SRC_TAX,
                    data={'head': 'SPY 세금 계산 · 단위 원', 'side': ['22%', A('22%를', 10), '공제 250만원 넘는 이익에 붙는 세율'],
                          'rows': R([['분배금에서 (미국 15%)', '−' + won(RC['SPY']['wht']), 'tax', A('16만 4천원', 0)], ['판 이익', won(RC['SPY']['gain']), 'in', A('다음은 판 이익', 0)],
                                     ['빼 주는 돈(공제)', '−2,500,000', 'dim', A('다음은 판 이익', 14)], ['곱하는 세율', '× 22%', 'in', A('22%를', 0)],
                                     ['판 이익 세금', '−' + won(RC['SPY']['cgt']), 'tax', A('191만 6천원', 0)]]),
                          'callout': ['넣은 돈이 작을수록 세금 비중 ↓', A('공제가 금액과', 0)]})
    if key == 'spycal':
        return dict(kind='zoom', title='판 이익 세금은 나중에 낸다', sub='팔 때 바로 빠지지 않는다 — 다음 해 5월 직접 신고', source=SRC_TAX,
                    data={'text': '다음 해 5월', 'label': '판 이익 세금 내는 때', 'note': '확정신고 5월 1일~31일', 'start': A('그런데 이 세금은', 8),
                          'after': ['세금 두 가지 다 낸 뒤', won(RC['SPY']['net']) + '원', PCT['SPY'], A('10% 조금', 0)]})
    if key == 'schd':
        return dict(kind='receipt', title='SCHD 영수증', sub='배당 ETF · 계산 방법은 S&P500과 같다', source=SRC_ETF,
                    data={'head': 'SCHD · 1억 · 단위 원', 'side': ['+15.99%', A('16% 가까이', 10), '세금 뗀 뒤, 넣은 돈보다 늘어난 비율'],
                          'rows': R([['달러로 오른 폭', '+19.68%', 'in', A('약 20%', 0)], ['원화로 판 돈', won(RC['SCHD']['sell']), 'in', A('약 20%', 30)],
                                     ['분배금 4번(세금 전)', '+' + won(RC['SCHD']['dist']), 'in', A('373만원', 0)], ['미국이 뗀 세금 15%', '−' + won(RC['SCHD']['wht']), 'tax', A('55만 9천원', 0)],
                                     ['판 이익 세금', '−' + won(RC['SCHD']['cgt']), 'tax', A('291만원', 0)], ['세금 다 낸 뒤', won(RC['SCHD']['net']), 'net', A('16% 가까이', 0)]]),
                          'callout': ['1주당 분배금 1.0339 → 1.0541달러 (+1.95%)', A('1주당 분배금', 0)]})
    if key == 'schdfx':
        days = [['12/15', 1472.5], ['3/30', 1508.1], ['6/29', 1544.2], ['9/28', 1352.0]]
        return dict(kind='bars', title='분배금은 받는 날 환율로 들어온다', sub='SCHD 분배금 네 번이 들어온 날의 원/달러 환율 · 원', source='찰스슈왑 분배금 표 × 한국은행 ECOS 731Y001(파이어맵 계산)',
                    data={'dir': 'v', 'min': 1200, 'max': 1600, 'tags': True, 'hline': [FX[1], '끝날 환율 1,359.6원', A('그런데 분배금은', 0)],
                          'bars': [[d, v, f'{v:,.1f}원', A('그런데 분배금은', 14 + 10 * i), 'ink'] for i, (d, v) in enumerate(days)],
                          'note': ['받은 날 환율이면 +252,402원', A('25만원쯤', 0)]})
    if key == 'gold':
        return dict(kind='bars', title='금은 환율이 주인공', sub='GLD · 같은 1년을 두 가지로 잰 늘어난 비율', source=SRC_ETF,
                    data={'dir': 'v', 'max': 8, 'tags': True, 'bars': [['달러로 잰 오른 폭', 7.15, '+7.15%', A('약 7%', 0), 'ink'], ['원화로, 세금 뗀 뒤', 3.37, '+3.37%', A('3% 조금', 0), 'accent']],
                          'note': ['환율 −3.30%가 깎아 먹음', A('361만원', 0)], 'circle': [1, A('3% 조금', 20)]})
    if key == 'rank':
        bars = [[NAME[k], RC[k]['net'] - 100_000_000, SAYNET[k], A('맨 위' if k == 'SCHD' else '그다음이', 0 if k == 'SCHD' else 14 * i), 'accent' if k == 'SCHD' else 'ink', PCT[k]] for i, k in enumerate(ORD)]
        return dict(kind='bars', title='세금·환율 뗀 뒤 순위', sub='막대 = 넣은 돈 1억보다 늘어난 만큼 · 2025.10.2 하루에 넣은 경우', source=SRC_ETF + ' · ' + PAST,
                    data={'dir': 'v', 'max': 17_000_000, 'tags': True, 'bars': bars, 'note': ['세금 떼기 전에도 같은 순서', A('그다음이', 30)], 'circle': [0, A('맨 위', 20)]})
    if key == 'gap':
        return dict(kind='count', title='달라진 건 간격', sub='SCHD와 예금, 통장에 남은 돈의 차이', source=SRC_ETF + ' · ' + SRC_TAX.split(' · ')[0],
                    data={'from': GAP[0], 'to': GAP[1], 'text': won(GAP[1]) + '원', 'label': 'SCHD − 예금, 세금 뗀 뒤', 'start': A('세금을 떼고 나니', 0),
                          'pre': '세금 떼기 전 ' + won(GAP[0]) + '원', 'preAt': A('1,688만원', 0), 'cut': '세금이 줄인 간격 ' + won(GAP[0] - GAP[1]) + '원', 'cutAt': A('307만원', 0),
                          'callout': ['많이 번 쪽이 세금도 많이 낸다', A('많이 번 쪽이', 0)]})
    if key == 'start':
        order = [['금>S&P>SCHD', 153], ['금>SCHD>S&P', 34], ['SCHD>금>S&P', 34], ['SCHD>S&P>금', 25], ['S&P>금>SCHD', 4], ['S&P>SCHD>금', 1]]
        return dict(kind='bars', title='넣는 날을 바꾸면 순위도 바뀐다', sub='시작일 251개(2024.10.2~2025.10.2)마다 1년 들고 판 결과 · 세 ETF 순서별 날 수', source='야후 파이낸스 종가·분배금 · 달러 기준·세금 전(파이어맵 계산)',
                    data={'dir': 'v', 'max': 175, 'tags': True, 'bars': [[o, v, f'{v}일', A('그래서 넣는 날을', 10 + 8 * i), 'accent' if o.startswith('SCHD>S&P') else ('ink' if not o.startswith('금') else 'ink'), None] for i, (o, v) in enumerate(order)],
                          'circle': [3, A('오늘 영수증과 같은', 0)], 'note': ['오늘 순서: 251일 중 25일(10.0%)', A('오늘 영수증과 같은', 10)],
                          'note2': ['금이 1위: 187일(74.5%)', A('오히려 금이', 0)]})
    if key == 'caseA':
        return dict(kind='person', title='30대 · 1년 안에 꺼낼 돈', sub='예: 집 계약금 — 꺼내는 날이 정해진 돈', source=SRC_ADD,
                    data={'who': '30대', 'what': '1년 안에 꺼낼 돈', 'dir': 'h', 'min': 7000, 'max': 14200, 'tags': False,
                          'bars': [['예금', 10218, '102,182,680원', A('예금이면', 0), 'ink', '처음부터 정해짐', 10000, '1억'],
                                   ['S&P500', 12304, '123,037,245원', A('S&P500이었다면', 0), 'accent', '꺼내는 날에 따라', 9729, '97,294,730원']],
                          'callout': ['폭 2,574만원', A('S&P500이었다면', 24)]})
    if key == 'caseB':
        return dict(kind='person', title='55세 · 은퇴 뒤 생활비 보탬', sub='한 달로 나눈 몫 — 예금은 만기에 한 번, SCHD는 석 달에 한 번', source='한국은행 ECOS 121Y002 · 소득세법 제129조 · 찰스슈왑 분배금 표 × ECOS 731Y001(파이어맵 계산)',
                    data={'who': '55세', 'what': '생활비 보탬', 'dir': 'v', 'max': 340000, 'tags': True,
                          'bars': [['예금 3.39% 한 달 몫', 238995, '238,995원', A('지금 예금 평균', 0), 'ink'], ['SCHD 지난 1년 한 달 몫', 285120, '285,120원', A('SCHD는 지난 1년', 0), 'accent']],
                          'callout': ['분기마다 796,727~905,832원', A('다만 석 달에', 0)]})
    if key == 'rate':
        bars = [[y if y != '2026' else '2026(1~8월)', v, f'{v:.2f}%', A('한 해 평균으로', 12 * i), 'accent' if y == '2026' else 'ink'] for i, (y, v) in enumerate(YEARLY)]
        return dict(kind='bars', title='은행 1년 예금 금리, 한 해 평균', sub='% · 새로 가입한 예금 기준(실제 가입 금리)', source=SRC_RATE,
                    data={'dir': 'v', 'max': 4.5, 'tags': True, 'bars': bars, 'note': ['지금(2026.8) 3.39% · 기준금리 3.0%', A('기준금리가', 0)], 'circle': [0, A('바닥이던 해', 0)]})
    if key == 'now':
        return dict(kind='receipt', title='지금 1억을 1년 넣으면', sub='2026년 8월 새로 가입한 1년 예금 평균 3.39% 기준', source=SRC_DEP,
                    data={'head': '정기예금 1년 · 연 3.39% · 단위 원',
                          'rows': R([['이자', '+' + won(NOW['int']), 'in', A('339만원', 0)], ['세금 15.4%', '−' + won(NOW['tax']), 'tax', A('52만원', 0)],
                                     ['세금 뒤 이자', won(NOW['net']), 'net', A('52만원', 30)], ['한 달로 나누면', won(NOW['mon']), 'hi', A('52만원', 60)]]),
                          'side': ['+2,867,940원', A('52만원', 40), '1년 뒤 손에 쥐는 이자']})
    if key == 'posted':
        return dict(kind='bars', title='은행들이 내건 금리', sub='1년 예금 상품마다 내건 기본금리 — 가장 낮은 곳 ~ 가장 높은 곳', source=SRC_FL,
                    data={'dir': 'h', 'min': 1.5, 'max': 4.5,
                          'bars': [['은행', 3.92, '3.92%', A('은행들이 내건', 0), 'ink', '상품 39개', 1.90, '1.90%'], ['저축은행', 4.10, '4.10%', A('저축은행은', 0), 'ink', '상품 320개', 2.45, '2.45%']],
                          'marker': [3.39, '실제 가입 평균 3.39%', A('내건 금리는', 0)]})
    if key == 'cpi':
        return dict(kind='bars', title='이자가 물가를 따라갔을까', sub='1억 기준 · 지난 1년(2025.8 → 2026.8) 물가 +3.09%', source=SRC_CPI,
                    data={'dir': 'v', 'max': 3_400_000, 'tags': True,
                          'bars': [['세금 뗀 이자', NOW['net'], won(NOW['net']) + '원', A('287만원', 0), 'ink'], ['물가만큼 필요한 돈', 3_090_000, '3,090,000원', A('309만원', 0), 'rise']],
                          'note': ['모자란 돈 −222,060원', A('22만원', 0)]})
    if key == 'when':
        need('A 1년 전 은행 평균 2.51% → 세전 2,510,000 · 세금 386,540 · 세후 2,123,460', 'C 은행 공시 최고 3.92% → 세전 3,920,000 · 세금 603,680 · 세후 3,316,320',
             'E 2022-11 고점 4.95% → 세전 4,950,000 · 세금 762,300 · 세후 4,187,700', 'A -966,540 · B -222,060 · C +226,320')
        return dict(kind='bars', title='같은 예금, 넣은 때와 금리에 따라', sub='1억 · 1년 · 세금 뗀 이자 · 점선 = 물가만큼 필요한 돈', source=SRC_RATE + ' · ' + SRC_FL,
                    data={'dir': 'v', 'max': 4_600_000, 'tags': True, 'hline': [3_090_000, '물가만큼 3,090,000원', A('같은 예금도', 0)],
                          'bars': [['작년 8월 평균 2.51%', 2_123_460, '2,123,460원', A('작년 8월', 0), 'ink'], ['지금 평균 3.39%', NOW['net'], won(NOW['net']) + '원', A('같은 예금도', 16), 'ink'],
                                   ['은행 공시 최고 3.92%', 3_316_320, '3,316,320원', A('은행이 내건', 0), 'ink'], ['가장 높던 달 4.95%', 4_187_700, '4,187,700원', A('금리가 가장 높았던', 0), 'accent']],
                          'note': ['넣는 날의 금리가 1년 결과를 정한다', A('예금은 값이', 0)]})
    if key == 'thresh':
        return dict(kind='bars', title='금액이 커지면 만나는 문턱 세 개', sub='넣은 돈(원금) 기준 · 금리 3.39% · 다른 금융소득 없다고 가정', source=SRC_TH,
                    data={'dir': 'h', 'min': 0, 'max': 72000,
                          'bars': [['예금자보호 한도', 10000, '1억원', A('첫 번째는', 0), 'ink', '한 사람 기준'], ['건보료에 이자 합산', 29499, '약 2억 9,499만원', A('두 번째는', 0), 'ink', '이자 1천만원 넘으면'],
                                   ['종합과세·피부양자', 58997, '약 5억 8,997만원', A('세 번째는', 0), 'ink', '이자 2천만원 넘으면']]})
    if key == 'caseC':
        return dict(kind='person', title='60세 · 예금 2억 + 퇴직금 1억', sub='지역가입자 1인 · 재산 0 · 다른 소득 0 가정 · 건보료+장기요양 월액', source='국민건강보험법 시행규칙 제44조 · D-1 계산식(파이어맵 계산) · 실제 고지액과 다를 수 있음',
                    data={'who': '60세', 'what': '퇴직금 1억 더 예금', 'dir': 'v', 'max': 80000, 'tags': True,
                          'bars': [['예금 2억 · 이자 6,780,000원', 22800, '월 22,800원', A('예금 2억이', 0), 'ink'], ['예금 3억 · 이자 10,170,000원', 68930, '월 68,930원', A('원금이 3억이', 0), 'rise']],
                          'callout': ['1년 +553,560원', A('1년에 55만원', 0)]})
    if key == 'sum':
        return dict(kind='receipt', title='정리 — 1억의 1년 영수증', sub='2025.10.2 → 2026.10.2 · 세금과 환율을 다 뗀 뒤', source=SRC_ETF + ' · ' + PAST,
                    data={'head': '세금 다 낸 뒤 남는 돈', 'side': ['순위 그대로', A('순위는 그대로', 0), '하지만 넣는 날이 바뀌면 순위도 바뀜'],
                          'rows': R([[f'{NAME[k]}  {PCT[k]}', SAYNET[k], 'net' if k == 'SCHD' else 'in', A(['SCHD는', 'SCHD는', '금은', '금은'][i], [0, 24, 0, 24][i])] for i, k in enumerate(ORD)])})
    if key == 'act':
        return dict(kind='act', title='오늘 해 볼 일 하나', sub='내 통장에서 — 작년 이자·배당 합계 확인', source='소득세법 제14조 · 국민건강보험법 시행규칙 제44조',
                    data={'head': '내 작년 금융소득', 'rows': R([['① 작년 이자·배당 합계 찾기', '은행·증권사 앱', 'in', A('은행이나 증권사', 0)],
                                                            ['② 1천만원까지 남은 돈', '지역 건보 합산 경계', 'hi', A('그리고 1천만원과', 0)],
                                                            ['③ 2천만원까지 남은 돈', '종합과세·피부양자', 'hi', A('그리고 1천만원과', 18)]])})
    if key == 'end':
        return dict(kind='end', title='다음 영수증은 2편에서', sub='1억의 1년 영수증 시리즈 · 재생목록에 차례대로', source=PAST,
                    data={'text': '다음 편', 'label': '1억의 1년 영수증', 'note': '같은 규칙으로, 실제 그날 넣었다면', 'start': A('다음 편에서도', 0)})
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
        if key == 'end': frames = max(frames, END_MIN)
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch in ('0.', '로고') else (ch.replace('-1.', '장 · 덧붙임') if ch.endswith('-1.') else ch.rstrip('.') + '장'),
                       'data': d['data'], 'lines': out, 'frames': frames})
    # 편집 반려 10/5 12:04 ②: 대본 [자막]의 '세금 뒤 통장'은 판 이익 세금(다음 해 5월)과 부딪힌다 — 대본 해시를 안 바꾸려고 화면에서만 바꾼다
    for sc in scenes:
        for l in sc['lines']:
            if l['cap']: l['cap'] = l['cap'].replace('세금 뒤 통장', '세금 다 낸 뒤')
    # 첫 장면 줌아웃(motion-designer 10/5 [요청], PD 넣음 14:5x) — nameAt은 목소리 길이로 다시 잰다
    sys.path.insert(0, os.path.join(EP, 'motion_preview'))
    from zoomprops import build as zoom_build
    op = next(x for x in scenes if x['key'] == 'open')
    op['data']['zoom'] = zoom_build(op)
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
    main(a[a.index('--script') + 1] if '--script' in a else 'script.v8.md')
