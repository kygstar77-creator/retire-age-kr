# M-1 화면 재료 — script.v2.md(장·문장·[자막]) + voice.json(있으면 길이) + calc_out.txt·facts.txt → work/video/m1.json (Remotion M1 컴포지션이 읽는다)
#   py -3.12 work/research/longform/ep/M-1/m1props.py
# 숫자 글자는 전부 calc_out.txt·facts.txt 원문 줄에서 온다 — need()로 원문에 있는지, assert로 계산이 맞는지 기계 대조한다.
# 목소리가 없는 문장은 길이를 '말하는 글자 ÷ 5.65음절/초'로 잡는다(r1props와 같은 규칙). voice.json이 생기면 그 길이를 쓴다.
# 첫 장면은 motion-designer ReverseAsk(motion.md) — 프레임을 문장 시작점으로 다시 잰다(motion_preview/m1props.py는 미리보기 판).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
RATE = 5.65
FPS = 30
SCRIPT = 'script.v2.md'
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
SCR = open(os.path.join(EP, SCRIPT), encoding='utf-8').read()
def need(*ss, src=None):
    for s in ss: assert s in (src or FACTS), f'원문에 없는 줄: {s}'
calc = lambda *ss: need(*ss, src=CALC)
scr = lambda *ss: need(*ss, src=SCR)

# ── 거꾸로 계산(calc_out.txt) ──
P = ['JEPQ', 'SCHD', 'ACE 미국배당다우존스']
SEC = {k: CALC.split(f'## {k}')[1].split('##')[0] for k in P}
NEED = {}
for k in P:
    for m in (100, 200, 300):
        mm = re.search(rf'월 {m}만원: 연 세전 분배 ([\d,]+)원 → 필요 원금 ([\d.]+)억원', SEC[k]); NEED[(k, m)] = (mm[1], mm[2])
assert [NEED[(k, 100)][1] for k in P] == ['1.38', '4.85', '5.10']
assert [NEED[(k, 200)][1] for k in P] == ['2.77', '9.69', '10.20'] and [NEED[(k, 300)][1] for k in P] == ['4.15', '14.54', '15.30']
calc('가장 적은 달 기준이면 1.71억원(×1.23)', '가장 적은 달 기준이면 8.92억원(×1.75)', '분기 1회 — 매달이 아님')
calc('분배 1.0541달러 ÷ 종가 32.72달러 = 분배율 3.22%', '분배 6.88454달러 ÷ 종가 61.04달러 = 분배율 11.28%', '분배 441원 ÷ 종가 14330원 = 분배율 3.08%')
calc('월 세후 708,333원', '월 세후 705,000원', '연 세전 분배 15,611,746원', '연 세전 분배 15,693,413원', '건보 더 냄 연 1,269,984원(월 105,832원)')
calc('연 세전 분배 31,223,493원', '연 세전 분배 31,386,827원')
assert round(10_000_000 * 0.85 / 12) == 708333 and round(10_000_000 * 0.846 / 12) == 705000
assert round(15611746 * 0.85) - 1269984 == 12_000_000      # 세전 → 미국 15% → 건보 뺀 뒤 = 1년 1,200만원(월 100만원)
TOT = {}
for k in P:
    mm = re.search(rf'{re.escape(k)}: 가격 \+([\d.]+)% · 분배 ([\d.]+)% · 합 \+([\d.]+)% → 1억이 ([\d,]+)원', CALC); TOT[k] = mm.groups()
    assert abs(float(mm[1]) + float(mm[2]) - float(mm[3])) < 0.011, k
assert [TOT[k][2] for k in P] == ['14.65', '19.46', '18.55']

# ── 달별 분배(facts.txt [J1]·[K1]·[S1]) ──
J = re.search(r'달별: (25-11 0\.47553.*?)\n', FACTS)[1]
JM = [(a, float(b)) for a, b in re.findall(r'(\d\d-\d\d(?:-\d\d)?) ([\d.]+)', J)]
assert len(JM) == 12 and abs(sum(v for _, v in JM) - 6.88454) < 1e-9 and min(JM, key=lambda x: x[1]) == ('26-02', 0.46572) and max(JM, key=lambda x: x[1]) == ('26-08', 0.70497)
K = re.search(r'달별: (25-10 37.*?)\n', FACTS)[1]
KM = [(a, int(b)) for a, b in re.findall(r'(\d\d-\d\d) (\d+)', K)]
assert len(KM) == 12 and sum(v for _, v in KM) == 441 and min(KM, key=lambda x: x[1]) == ('25-11', 21) and max(KM, key=lambda x: x[1]) == ('25-12', 53)
need('가장 적은 달 0.46572(2026-02-02) · 가장 많은 달 0.70497(2026-08-03)', '가장 적은 달 21원(2025-11-14) · 가장 많은 달 53원(2025-12-15)')
SQ = [('25-12', '0.2782'), ('26-03', '0.2569'), ('26-06', '0.2525'), ('26-09', '0.2665')]
need('최근 4회 합 1.0541달러(12/10 0.2782·3/25 0.2569·6/24 0.2525·9/23 0.2665)'); assert abs(sum(float(v) for _, v in SQ) - 1.0541) < 1e-9
need('원/달러 2025-10-02 1,406.0 → 2026-10-02 1,359.6', '국민건강보험법 시행령 제41조③', '하한 월 22,800원', '시행규칙 제44조①')
scr('월 22,800원(최저 보험료) → 월 105,832원(전체 보험료)', '2026년 배당 → 2027년 11월분 보험료부터', '피부양자 소득 요건 연 2,000만원 이하')
won = lambda v: f'{v:,}'
def jlab(a):     # JEPQ 배당락 달 → 몇 월분(1월분은 2025-12-31 배당락)
    return '1월' if a == '25-12-31' else f'{int(a[3:5])}월'

SRC_DIST = '운용사·거래소 분배 기록(나스닥·찰스슈왑·한국투자신탁운용) · 거래소 종가(야후 파이낸스)'
SRC_TAX = '한미 조세조약 제10조(IRS Table 1) · 소득세법 제14조·제129조 · 지방세법 제103조의13'
SRC_NHI = '국민건강보험법 시행규칙 제44조 · 시행령 제41조 · 국민건강보험공단(보험료율 7.19%·장기요양)'
SRC_CALC = '파이어맵 계산 · ' + SRC_DIST
PAST = '과거 값 · 미래 보장 아님 · 투자 권유 아님'
NAMEV = {'JEPQ': 'JEPQ', 'SCHD': 'SCHD', 'ACE 미국배당다우존스': 'ACE 미국배당다우존스'}

CUTS = [('open', '0.', None), ('road', '0.', '오늘은 이 계산을'), ('logo', '로고', None),
        ('rules', '1.', None), ('tax', '1.', '둘째, 세금을'), ('rules3', '1.', '셋째, 건강보험료'),
        ('gauge', '2.', None), ('premium', '2.', '다른 소득도 재산도'), ('when', '2.', '하나 더 있어요'),
        ('flow', '3.', None), ('schd', '3.', '먼저 SCHD예요'), ('cal', '3.', '근데 SCHD, 매달'), ('jepq', '3.', '다음은 JEPQ예요'),
        ('ace', '3.', '마지막은 우리나라에'), ('three', '3.', '여기까지만 보면'),
        ('jm', '4.', None), ('am', '4.', 'ACE 미국배당다우존스는 차이가'), ('pair', '4.', '월배당이라는 이름만'),
        ('gauge2', '5.', None), ('table', '5.', '그 경우 JEPQ로도'),
        ('total', '6.', None), ('split', '6.', '분배금은 가장 많이 받았는데'),
        ('sum', '7.', None), ('end', '7.', '설명란 파이어맵 계산기')]
END_MIN = 20 * FPS


def spec(key, A):
    if key == 'open':
        return dict(kind='open', title='매달 100만원 받으려면 얼마 있어야 하나', sub='지난 1년 실제 분배금 · 세금·건강보험료 뗀 뒤 · 2026-10-02 기준',
                    source='운용사·거래소 분배 기록, 거래소 종가, 한국은행 ECOS, 법제처 · ' + PAST, data={})   # rev는 main에서
    if key == 'road':
        items = ['계산 규칙 세 줄', '건강보험료가 붙는 선', '세 상품 거꾸로 계산', '가장 적게 나온 달', '목표를 올리면 · 분배 뒤 가격']
        return dict(kind='road', title='오늘 따라갈 순서', sub='월 100만원에서 거꾸로', source=None,
                    data={'rows': [[f'{"①②③④⑤"[i]}  {t}', A('순서는', 8 + i * 22)] for i, t in enumerate(items)]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': '월배당 거꾸로 계산 · 2026.10.2 기준'})
    if key == 'rules':
        return dict(kind='rules', title='계산 규칙 세 줄', sub='숫자가 어디서 왔는지 먼저', source=SRC_DIST + ' · 한국은행 ECOS 731Y001',
                    data={'cards': [['①', '지난 1년 실제 분배금', '2025.10 ~ 2026.10 · JEPQ·ACE 12회 · SCHD 4회', A('첫째', 0)],
                                    ['②', '세금 뗌', '미국 상장 15% · 국내 상장 15.4%', 10 ** 6], ['③', '건강보험료 뗌', '지역가입자 · 재산·다른 소득 없음', 10 ** 6]],
                          'active': [[0, A('첫째', 0)]], 'warn': ['앞으로도 똑같다는 뜻 아님', A('앞으로도', 0)],
                          'fx': ['원/달러', '1,406.0원', '1,359.6원', A('미국 상장 상품은 원화로', 0)]})
    if key == 'tax':
        return dict(kind='receipt', title='둘째, 세금', sub='분배금이 들어오기 전에 먼저 빠지는 돈', source=SRC_TAX,
                    data={'head': '분배금 100이 들어오면', 'rows': [['미국 상장(JEPQ·SCHD)', '미국 원천징수 15%', 'tax', A('미국에서 먼저', 0)],
                                                            ['국내 상장(ACE)', '배당소득세 15.4%', 'tax', A('국내 상장 상품은', 0)],
                                                            ['연 금융소득 2,000만원 안쪽', '국내 추가 세금 없음', 'net', A('미국에서 먼저', 30)]],
                          'side': ['15%', A('미국에서 먼저', 6), '미국 상장 분배금에서 먼저'], 'callout': ['분배금 전체에 매김 — 세금 크게 잡은 쪽', A('국내 상장 상품은', 40)]})
    if key == 'rules3':
        return dict(kind='rules', title='셋째, 건강보험료', sub='퇴직 뒤 지역가입자 기준', source=SRC_NHI,
                    data={'cards': [['①', '지난 1년 실제 분배금', '2025.10 ~ 2026.10 · JEPQ·ACE 12회 · SCHD 4회', 0],
                                    ['②', '세금 뗌', '미국 상장 15% · 국내 상장 15.4%', 4], ['③', '건강보험료 뗌', '지역가입자 · 재산·다른 소득 없음', A('셋째', 0)]],
                          'active': [[2, A('셋째', 0)]], 'warn': ['직장가입자는 기준 다름', A('퇴직하고', 20), 2],
                          'stamp': ['기준일 2026.10.2 · 종가·환율 같은 날', A('가격과 환율은', 0)]})
    if key == 'gauge':
        return dict(kind='gauge', title='건강보험료가 붙는 선', sub='이자 + 배당, 1년 합계 · 세금 떼기 전', source=SRC_NHI,
                    data={'max': 1800, 'lines': [[1000, '1,000만원', A('1,000만원까지는', 0)]], 'fill': [[900, A('1,000만원까지는', 20), 'ink'], [1100, A('조금이라도 넘으면', 0), 'ink'], [1100, A('조금이라도 넘으면', 40), 'rise'], [1561, A('근데 오늘 목표는', 10), 'rise']],
                          'all': ['넘으면 전부 합산', A('조금이라도 넘으면', 40)],
                          'side': [['세후 월 70.8만원', '미국 상장 · 국내 상장은 70.5만원', A('이 선을 매달', 0)]],
                          'target': [1561, '오늘 목표 연 1,561만원', A('근데 오늘 목표는', 0)]})
    if key == 'premium':
        return dict(kind='receipt', title='선을 넘으면 붙는 몫', sub='월 100만원을 손에 쥐려면 — 미국 상장 예시', source=SRC_NHI + ' · 파이어맵 계산',
                    data={'head': '1년 · 단위 원', 'rows': [['연 세전 분배', won(15611746), 'in', A('그래서 목표 금액을', 0)], ['세금(미국 원천징수)', '−15%', 'tax', A('그래서 목표 금액을', 18)],
                                                        ['건강보험료(장기요양 포함)', '−' + won(1269984), 'tax', A('그래서 목표 금액을', 36)], ['손에 남는 돈', '월 100만원 × 12', 'net', A('그래서 목표 금액을', 54)]],
                          'count': ['월 22,800원', '월 105,832원', '최저 보험료', '재산·다른 소득 없을 때', A('다른 소득도', 10)],
                          'callout': ['피부양자: 소득만 보면 연 2,000만원까지 따로 안 냄', A('자녀 건강보험에', 0)]})
    if key == 'when':
        return dict(kind='timeline', title='보험료는 1년 늦게 따라온다', sub='올해 받은 배당 → 내년 11월분 고지서부터', source='국민건강보험법 시행령 제41조③',
                    data={'segs': [['2026년', '배당 받는 해', 'ink', A('하나 더', 0)], ['2027년 1~10월', '고지서 그대로', 'dim', A('올해 받은 배당은', 10)], ['2027년 11월~', '이때부터 반영', 'accent', A('올해 받은 배당은', 40)]],
                          'note': ['첫해에 괜찮아도 1년쯤 뒤 바뀜', A('첫해에', 0)]})
    if key == 'flow':
        return dict(kind='flow', title='거꾸로 계산하는 법', sub='오른쪽 목표에서 왼쪽 필요한 돈으로', source='파이어맵 계산 · 세율 1장 · 건보료 2장',
                    data={'boxes': [['필요한 돈', '= 연 세전 분배 ÷ 분배율', A('필요한 돈은 결국', 0)], ['연 세전 분배', '15,611,746원', A('세금과 건강보험료를', 0)], ['월 100만원', '세금·건보료 뗀 뒤', 0]],
                          'note': ['국내 상장은 15,693,413원', A('세금과 건강보험료를', 40)]})
    if key in ('schd', 'jepq', 'ace'):
        nm = {'schd': 'SCHD', 'jepq': 'JEPQ', 'ace': 'ACE 미국배당다우존스'}[key]
        d = {'schd': ('미국 배당주를 모아 담은 ETF · 미국 상장', '3.22%', '분배금 1.0541달러 ÷ 종가 32.72달러', '연 4회(분기)', '먼저 SCHD예요', '지난 1년 분배율은 3.2%', '그래서 필요한 돈은 4억'),
             'jepq': ('나스닥 주식 + 옵션 매도(커버드콜) · 미국 상장', '11.28%', '분배금 6.88454달러 ÷ 종가 61.04달러', '연 12회', '다음은 JEPQ예요', '지난 1년 분배율이 11%', '그래서 필요한 돈이 확'),
             'ace': ('Dow Jones U.S. Dividend 100 · 국내 상장', '3.08%', '분배금 441원 ÷ 종가 14,330원', '연 12회', '마지막은 우리나라에', '지난 1년 분배율은 3.1%', '필요한 돈은 5억')}[key]
        return dict(kind='card', title=f'{nm} — 월 100만원이면', sub='세금·건보료 뗀 뒤 · 지난 1년 실제 분배', source=SRC_DIST,
                    data={'name': nm, 'desc': d[0], 'rate': d[1], 'rateCalc': d[2], 'freq': d[3], 'need': NEED[(nm, 100)][1] + '억원',
                          'at': A(d[4], 0), 'rateAt': A(d[5], 0), 'needAt': A(d[6], 0),
                          'note': (['같은 지수 상품은 다른 운용사에도 있음 · 예시 1종', A('같은 지수를 따르는', 0)] if key == 'ace' else None), 'hot': key == 'jepq'})
    if key == 'cal':
        ms = ['25.10', '25.11', '25.12', '26.1', '26.2', '26.3', '26.4', '26.5', '26.6', '26.7', '26.8', '26.9']
        coin = {'25.12': SQ[0][1], '26.3': SQ[1][1], '26.6': SQ[2][1], '26.9': SQ[3][1]}
        return dict(kind='calendar', title='SCHD는 매달 주지 않는다', sub='지난 1년 분배 4회 · 1주당 달러', source='찰스슈왑 SCHD 분배금 표 · 야후 파이낸스',
                    data={'months': [[m, coin.get(m, '')] for m in ms], 'at': A('근데 SCHD', 10), 'note': ['석 달 치가 한꺼번에 · 나눠 쓰는 건 내 몫', A('매달이 아니라', 0)]})
    if key == 'three':
        return dict(kind='bars', title='월 100만원에 필요한 돈 — 평균 기준', sub='세금·건보료 뗀 뒤 · 지난 1년 평균 분배', source=SRC_CALC,
                    data={'max': 6, 'bars': [[NAMEV[k], float(NEED[(k, 100)][1]), NEED[(k, 100)][1] + '억원', 4 + i * 6, 'accent' if k == 'JEPQ' else 'ink'] for i, k in enumerate(P)],
                          'note': ['분배율이 높을수록 필요한 돈이 적다?', A('여기까지만', 10)], 'note2': ['그런데 이건 평균', A('근데 이건 평균', 0)]})
    if key in ('jm', 'am'):
        if key == 'jm':
            ms = JM; lab = [jlab(a) for a, _ in ms]; vt = [f'{v}' for _, v in ms]; mn, mx = 3, 9
            return dict(kind='months', title='JEPQ 1주당 분배금, 달마다', sub='지난 12회 · 달러 · 1월분은 2025-12-31 배당락', source='나스닥 배당 이력 · 야후 파이낸스',
                        data={'vals': [v for _, v in ms], 'labels': lab, 'texts': vt, 'min': mn, 'max': mx, 'lo': 0.3, 'hi': 0.75, 'at': A('매달 들어온 돈', 6),
                              'minAt': A('가장 적은 달이 2월', 0), 'maxAt': A('가장 많은 달과', 0), 'ratio': ['최대 ÷ 최소 1.51배', A('가장 많은 달과', 20)],
                              'jump': ['1.38억원', '1.71억원', '×1.23', A('그러면 JEPQ는', 0)]})
        ms = KM; lab = [f'{a[:2]}.{int(a[3:])}' for a, _ in ms]; vt = [f'{v}원' for _, v in ms]
        return dict(kind='months', title='ACE 미국배당다우존스 1주당 분배금, 달마다', sub='지난 12회 · 원 · 지급기준일 달', source='한국투자신탁운용 공식 분배 기록 · 야후 파이낸스',
                    data={'vals': [v for _, v in ms], 'labels': lab, 'texts': vt, 'min': 1, 'max': 2, 'lo': 0, 'hi': 60, 'at': A('ACE 미국배당다우존스는', 6),
                          'minAt': A('가장 적은 달은 1주에', 0), 'maxAt': A('가장 많은 달은 그', 0), 'ratio': ['최대 ÷ 최소 2.52배', A('가장 많은 달은 그', 20)],
                          'jump': ['5.10억원', '8.92억원', '×1.75 · 최소값', A('그래서 가장 적은 달 기준', 0)]})
    if key == 'pair':
        return dict(kind='pair', title='평균으로 잴까, 가장 적은 달로 잴까', sub='월 100만원에 필요한 돈 · 억원', source=SRC_CALC,
                    data={'max': 10, 'groups': [['JEPQ', [[1.38, '1.38억원', 'ink'], [1.71, '1.71억원', 'accent']]], ['SCHD', [[4.85, '4.85억원', 'ink']]],
                                               ['ACE 미국배당다우존스', [[5.10, '5.10억원', 'ink'], [8.92, '8.92억원', 'accent']]]],
                          'legend': [['평균 기준', 'ink'], ['가장 적은 달 기준', 'accent']], 'at': 4,
                          'chip': [1, '분기 1회 · 나눠 쓰기 전제', 20], 'save': ['많은 달에 남겨 두면 → 평균 기준으로', A('아니면 많이 나온', 0)]})
    if key == 'gauge2':
        return dict(kind='gauge', title='목표를 올리면 두 번째 선', sub='이자 + 배당, 1년 합계 · 세금 떼기 전', source='소득세법 제14조 제3항 제6호 · 국민건강보험공단 피부양자 소득 요건 · ' + SRC_NHI.split(' · ')[0],
                    data={'max': 3600, 'lines': [[1000, '1,000만원 · 건보료', 0], [2000, '2,000만원 · 종합과세 · 피부양자', A('여기서 두 번째 선', 0)]],
                          'fill': [[1561, 4, 'ink'], [3122, A('매달 200만원이면', 10), 'rise']],
                          'side': [['월 200만원 → 연 세전 3,122만원', '미국 상장 31,223,493원 · 국내 31,386,827원', A('매달 200만원이면', 0)]],
                          'all': ['여기부터 사람마다 다름 → 최소값', A('다른 소득이 얼마인지', 0)], 'target': None})
    if key == 'table':
        rows = [[f'월 {m}만원', [NEED[(k, m)][1] + '억원' for k in P], A(t, 0)] for m, t in [(200, '그 경우 JEPQ로도'), (300, '목표를 300만원으로')]]
        return dict(kind='table', title='월 200만원 · 300만원이면', sub='모두 최소값 — 2,000만원 넘는 추가 세금은 사람마다 달라 빼고 계산', source=SRC_CALC,
                    data={'cols': [NAMEV[k] for k in P], 'rows': rows, 'stamp': '최소', 'hot': [[0, 0, A('그 경우 JEPQ로도', 10)], [1, 2, A('분배율이 높은 상품이', 0)]]})
    if key == 'total':
        return dict(kind='bars', title='1년 전 1억을 넣었다면', sub='분배금 + 가격 변화 · 원화 · 세전 · 분배금은 2026-10-02 환율(1달러 1,359.6원)로 바꾼 어림값', source=SRC_DIST + ' · 한국은행 ECOS 731Y001',
                    data={'max': 22, 'bars': [[NAMEV[k], float(TOT[k][2]), f'+{TOT[k][2]}%', A(t, 6), 'accent' if k == 'SCHD' else 'ink', TOT[k][3] + '원']
                                              for k, t in [('SCHD', '1등은 SCHD'), ('ACE 미국배당다우존스', 'ACE 미국배당다우존스도'), ('JEPQ', 'JEPQ는 셋 중에')]],
                          'note': ['어느 쪽이 가장 많이 남았을까?', A('그럼 작년에', 0)]})
    if key == 'split':
        g = [[NAMEV[k], [[float(TOT[k][0]), f'+{TOT[k][0]}%', 'ink'], [float(TOT[k][1]), f'{TOT[k][1]}%', 'accent']]] for k in ['JEPQ', 'SCHD', 'ACE 미국배당다우존스']]
        return dict(kind='pair', title='분배금과 가격 변화, 따로 보면', sub='1년 · 원화 · 세전 · %', source=SRC_DIST + ' · 한국은행 ECOS 731Y001',
                    data={'max': 18, 'groups': g, 'legend': [['가격 변화', 'ink'], ['분배금', 'accent']], 'at': 4, 'chip': None,
                          'save': ['커버드콜: 오를 때 몫 일부를 내주고 분배금을 만듦', A('커버드콜은', 0)], 'save2': ['지난 기록 — 옆으로 기는 해엔 반대일 수도', A('물론 지난', 0)]})
    if key == 'sum':
        return dict(kind='table', title='정리', sub='월 100만원 · 세금·건보료 뗀 뒤 · 2026-10-02 기준', source=SRC_CALC + ' · ' + PAST,
                    data={'cols': [NAMEV[k] for k in P], 'rows': [['평균 기준', ['1.38억원', '4.85억원', '5.10억원'], A('첫째', 0)],
                                                               ['가장 적은 달 기준', ['1.71억원', '분기 지급', '8.92억원'], A('둘째', 0)],
                                                               ['1년 총수익', [f'+{TOT[k][2]}%' for k in P], A('셋째', 0)]],
                          'stamp': None, 'hot': [[1, 2, A('둘째', 20)], [2, 1, A('셋째', 20)]], 'top': ['세후 월 70만원쯤부터 건보료', A('첫째', 0)]})
    if key == 'end':
        return dict(kind='end', title='내 목표 금액으로 다시 계산', sub='firemap.kr 계산기 · 설명란 링크', source='출처·기준일 전부 설명란 · ' + PAST,
                    data={'cta': 'firemap.kr', 'ctaSub': '내 목표 금액을 넣어 보세요', 'at': 4})
    raise KeyError(key)


def main():
    path = os.path.join(EP, SCRIPT)
    secs = SC.parse(path)
    caps, last = {}, None
    for line in SCR.split('\n---', 1)[0].splitlines():
        s = line.strip()
        if s.startswith('- '): last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
        elif s.startswith('[자막:') and last: caps[last] = s[4:].rstrip(']').strip()
    voice = {}
    vj = os.path.join(EP, 'voice.json')
    if os.path.exists(vj):
        for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
            for l in s['lines']:
                if l.get('audio'): voice[l['text']] = l
    chap = lambda t: re.sub(r'^\[', '', t).split()[0].rstrip(']')
    scenes = []
    for key, ch, start in CUTS:
        sec = next(s for s in secs if chap(s['title']) == ch)
        lines = sec['lines']; cuts = [c for c in CUTS if c[1] == ch]
        idx = [0 if c[2] is None else next(j for j, t in enumerate(lines) if t.startswith(c[2])) for c in cuts]
        me = [c[0] for c in cuts].index(key)
        part = lines[idx[me]:(idx[me + 1] if me + 1 < len(idx) else None)]
        out = []
        for t in part:
            v = voice.get(t)
            out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / RATE * FPS)), 'audio': v['audio'] if v else None})
        def A(w, plus=0, _o=out, _p=part, _k=key):
            j = next((j for j, t in enumerate(_p) if w in t), -1)
            assert j >= 0, (_k, w)
            return sum(x['frames'] for x in _o[:j]) + plus
        d = spec(key, A)
        frames = sum(x['frames'] for x in out) if out else 72
        if key == 'end': frames = max(frames, END_MIN)
        if key == 'open':
            st = [0]
            for l in out: st.append(st[-1] + l['frames'])
            assert len(out) == 9, len(out)
            d['data']['rev'] = {'seed': 'M-1', 'hook': '매달 100만원', 'hookSub': '지금 얼마가 있어야 할까요?', 'big': '큰돈', 'ask0': '매달 ?', 'goal': '매달 100만원', 'goalSub': '세금·건보료 뗀 뒤',
                                'bars': [['JEPQ', 1.38, '1.38억원'], ['SCHD', 4.85, '4.85억원'], ['ACE 미국배당다우존스', 5.10, '5.10억원']],
                                'low': {'i': 2, 'v': 8.92, 'label': '8.92억원', 'times': '×1.75', 'tag': '가장 적은 달 기준'},
                                'also': [{'i': 0, 'v': 1.71, 'label': '1.71억원', 'times': '×1.23'}], 'note': [[1, '분기 1회 · 달마다 아님']],
                                'fwd': st[0] + 66, 'nope': st[1] + 20, 'rev': st[2] + 10, 'land': st[3] + 20, 'grow': st[3] + 110,
                                'stamp': '2026년 10월 2일 기준', 'stampSub': '사라는 얘기가 아니라, 지난 기록으로 한 계산', 'stampAt': st[4] + 8,  # motion 10/6 첫 30초 힘(정지 11.2→4.2초)
                                'hi': [[st[5] + 6, 0], [st[6] + 6, 2], [st[7] + 6, -1]], 'low0': st[8] + 30}
            frames += 20
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch in ('0.', '로고') else ch.rstrip('.') + '장', 'data': d['data'], 'lines': out, 'frames': frames})
    used = [l['text'] for s in scenes for l in s['lines']]
    allx = [t for s in secs for t in s['lines']]
    assert used == allx, '대본 문장이 장면에 빠짐/중복'
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'script': SCRIPT, 'rate': RATE}
    json.dump(res, open(os.path.join(VID, 'm1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 목소리 없는 문장 {missing} · 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})}')
    for s in scenes: print(f"  {s['key']:7} {s['kind']:9} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    main()
