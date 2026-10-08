# W-1 1화 "이번 주 뉴스가 내 돈에 얼마" 화면 재료 — script.md(장·문장·[자막]) + voice.json(있으면 길이) + calc_out.txt·w1009/raw → work/video/w1.json (Remotion W1 컴포지션)
#   py -3.12 work/research/longform/ep/W-1/w1props.py [--script script.md]
# 숫자 글자는 전부 calc_out.txt(calc.py)와 w1009/raw 원문(DART 공시 표·ECOS 일별)에서 온다. 코드 안 숫자는 배치 좌표·축 범위뿐.
# 미국 금요일 종가(10/10 06시 뒤 fetch_us → calc)가 들어오면 이 파일을 다시 돌리기만 하면 4·5장 숫자가 따라 바뀐다. 대본 [자막]이 calc_out과 어긋나면 assert로 멈춘다.
# 목소리 없는 문장은 '말하는 글자 ÷ 5.65음절/초'로 길이를 잡는다(C-1·G-1과 같음).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
RATE = 5.65
FPS = 30
CO = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
won = lambda v: f'{v:,}'
M = lambda s: s.replace('-', '−')

# ── calc_out 파싱 ──
V = {k: v.strip() for k, v in re.findall(r'^\[(\w+)\][^=\n]*= (.+)$', CO, re.M)}
num = lambda k: float(V[k].replace(',', ''))
A1, A2, A4, A5 = num('A1'), num('A2'), num('A4'), num('A5')
B1, B2, B3, B4, B5, B6, B7 = (num(k) for k in ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'))
C1, C2, C3, C4, C5, C6, C7, C8, C9 = (num(k) for k in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'))
D1, D2, D3, D4 = (num(k) for k in ('D1', 'D2', 'D3', 'D4'))
E1, E2, E3, E4, E5, E6 = (num(k) for k in ('E1', 'E2', 'E3', 'E4', 'E5', 'E6'))
F1 = V['F1']; F2, F3, F4, F5 = (num(k) for k in ('F2', 'F3', 'F4', 'F5'))
G6 = num('G6'); G1, G2, G3 = V['G1'], V['G2'], V['G3']
S4, S5 = int(num('S4')), int(num('S5'))
iw = lambda v: won(int(round(v)))
man1 = lambda v: f'{abs(v) / 10000:,.1f}'                      # 1,359.6 (만원, 소수 한 자리)
sgn = lambda v: '−' if v < 0 else '+'

# ── 원자료: DART 잠정실적 표 · ECOS 일별 · 야후 SPY ──
D = open(os.path.join(EP, 'w1009', 'raw', 'dart_20261008800004.txt'), encoding='utf-8').read()
m = re.search(r'매출액 당해실적 ([\d.]+) ([\d.]+) ([\d.]+) - ([\d.]+) ([\d.]+)', D); REV = [m[1], m[2], m[4]]
m = re.search(r'영업이익 당해실적 ([\d.]+) ([\d.]+) ([\d.]+) - ([\d.]+) ([\d.]+)', D); OP = [m[1], m[2], m[4]]; OPQ, OPY = m[3], m[5]
assert float(OP[0]) == A1 and float(OP[1]) == B3 and float(OP[2]) == A2 and float(REV[0]) == A4 and float(OPY) == A5
QUOTE = re.search(r'(외부감사인의 회계감사가 완료되지 않은 상태에서 [^.]*?실제 실적과는 차이가 발생할 수 있음을 양지하시기 바랍니다\.)', D)[1]   # 원문 그대로(줄임 없음)
EC = json.load(open(os.path.join(EP, 'w1009', 'raw', 'ecos_d_20261009.json'), encoding='utf-8'))['data']
KO = {t: v for t, v in EC['802Y001']}; FXD = {t: v for t, v in EC['731Y001']}
assert KO['20261002'] == D1 and KO['20261008'] == D2 and FXD['20261002'] == E1 and FXD['20261008'] == E2
WEEK = ['20261006', '20261007', '20261008']
assert all(d in KO for d in WEEK) and '20261005' not in KO and '20261009' not in KO   # 10/5 대체공휴일 · 10/9 한글날 — ECOS에도 값 없음
import datetime as dt
j = json.load(open(os.path.join(EP, 'w1009', 'raw', 'yh_SPY.json'), encoding='utf-8'))['chart']['result'][0]; tz = j['meta']['gmtoffset']
SPY = {dt.datetime.fromtimestamp(t + tz, dt.UTC).strftime('%Y-%m-%d'): v for t, v in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if v}
SPYW = [(d, SPY[d]) for d in sorted(SPY) if '2026-10-02' <= d <= F1]
assert round((SPYW[-1][1] / SPYW[0][1] - 1) * 100, 2) == F2

# ── 검산: 화면에 쓰는 값끼리 맞나 ──
assert C6 - C7 == -C8 == 1_400_000 and round(C6 / 1e4) == 2760 and round(C7 / 1e4) == 2620
assert B5 - round(B5 * 0.154) == B6 and round(-C8 / B6, 1) == C9
assert round(D4 / 1e4) == S4 and E5 - E4 == E6 and F3 == E4
STOCK = F4 - E5                          # 주가 몫(원) = 마지막 원화 − 환율만 바뀐 원화
assert abs(E6 + STOCK - F5) <= 1
UP = F2 > 0                              # 금요일 종가로 방향이 바뀌면 화면 동사도 같이 바뀐다

def check_script(txt):
    for s in ['107.40조원', '12.17조원', '195.00조원', '89.49조원', '276,000원', '262,000원', '268,500원', f'{C4:.2f}%'.replace('-', '−'),
              '7,003.74', '6,625.93', f'{D3:.2f}%'.replace('-', '−'), '1,359.60원', '1,339.20원', iw(B6), '374원', '370원', f'{C9}분기', iw(-D4),
              f'{man1(F3)}만원', f'{man1(F4)}만원', f'{man1(F5)}만원', f'{G6}%', '21:30']:
        assert s in txt, f'대본 자막에 calc_out 값 없음: {s}'

SRC_DART = '금융감독원 전자공시(DART) 삼성전자 연결 영업(잠정)실적 공정공시 2026.10.08'
SRC_DIV = 'DART 현금·현물배당결정 2026.07.30 · 2025.10.30 · 소득세법 제129조 원천징수 15.4%'
SRC_KR = '한국은행 ECOS 802Y001 코스피 · 731Y001 원달러 매매기준율(일)'
SRC_PX = '야후 파이낸스 일별 종가(삼성전자 005930.KS)'
SRC_US = '야후 파이낸스 SPY 일별 종가 · 한국은행 ECOS 원달러 매매기준율'
SRC_CAL = '미국 노동통계국(BLS)·한국은행·미국 연준 일정표 · FRED CPIAUCNS'
NOTE = '평가액 기준 · 팔지 않으면 확정 아님 · 수수료 빼고 계산 · 전망·투자 권유 아님'
md = lambda d: f'{int(d[4:6])}/{int(d[6:])}'
TOT_HEAD = '이번 주 영수증'
TOT = lambda a=None, b=None, c=None: [['삼성전자 100주', f'−{round(-C8 / 1e4):,}만원', a if a is not None else 10**9],
                                      ['코스피 1천만원', f'−{-S4}만원' if S4 < 0 else f'+{S4}만원', b if b is not None else 10**9],
                                      ['미국 1만 달러', f'{sgn(F5)}{man1(F5)}만원', c if c is not None else 10**9]]
US_TXT = (f'달러 {sgn(F2)}{abs(F2):.2f}%', f'원화 {sgn(F5)}{round(abs(F5) / 1e4)}만원')

CUTS = [('open', '0.', None), ('dayfall', '0.', '발표한 날'), ('three', '0.', '이번 주에 내 돈이'),
        ('logo', '로고', None),
        ('week', '1.', None), ('kospi', '1.', '그 짧은 사흘'), ('fx', '1.', '같은 기간에'),
        ('dart', '2.', None), ('quote', '2.', '다만 이건'), ('rcpt1', '2.', '이제 100주를'), ('div', '2.', '그럼 배당은요'), ('pairs', '2.', '1년 전 3분기'),
        ('dots', '2.', '그래서 이번 주'), ('pending', '2.', '실적이 배당으로'),
        ('kbars', '3.', None), ('diverge', '3.', '107조 실적을'), ('noreason', '3.', '실적 발표 하나'),
        ('dual', '4.', None), ('fxonly', '4.', '먼저 환율만'), ('bridge', '4.', '그 사이 S&P500'),
        ('trio', '5.', None),
        ('cal', '6.', None), ('cpi', '6.', '지난 8월'), ('later', '6.', '그 뒤로는'),
        ('sum', '7.', None), ('end', '7.', '이 계산은')]
END_MIN = 20 * FPS


def spec(key, A):
    if key == 'open':
        return dict(kind='open', title='삼성전자 100주, 이번 주 영수증', sub='종가 10/2 → 10/8 · 단위 원', source=SRC_PX + ' · ' + SRC_DART,
                    data={'head': '삼성전자 100주 · 이번 주', 'rows': [['10/2 종가 × 100주', iw(C6), 'in', 0], ['10/8 종가 × 100주', iw(C7), 'in', 8], ['평가액', '−' + iw(-C8), 'net', 16]],
                          'big': [f'{OP[0]}조원', A('같은 주에'), f'3분기 영업이익(잠정) · 1년 전 {OP[2]}조원']})
    if key == 'dayfall':
        return dict(kind='bars', title='발표한 날 주가는', sub='삼성전자 종가 · 원', source=SRC_PX,
                    data={'min': 0, 'max': 290_000, 'bars': [['10/7 발표 전날', C2, iw(C2), 0, 'ink', None], ['10/8 발표한 날', C3, iw(C3), 10, 'fall', M(f'{C4:+.2f}%')]]})
    if key == 'three':
        return dict(kind='three', title='영수증 세 장', sub='이번 주 뉴스 세 개 → 내 돈', source=None,
                    data={'cards': [['삼성전자 100주', '조금 가진 사람', 6], ['코스피 1천만원', '시장 전체에 넣어 둔 사람', 16],
                                    ['미국 주식 1만 달러', '미국 주식을 가진 사람', 26]]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': '이번 주 뉴스가 내 돈에 얼마 · 1화'})
    if key == 'week':
        days = [['월', '10/5', '개천절 대체공휴일', None, None, 0], ['화', md(WEEK[0]), None, KO[WEEK[0]], f'{KO[WEEK[0]]:,.2f}', 6], ['수', md(WEEK[1]), None, KO[WEEK[1]], f'{KO[WEEK[1]]:,.2f}', 12],
                ['목', md(WEEK[2]), None, KO[WEEK[2]], f'{KO[WEEK[2]]:,.2f}', 18], ['금', '10/9', '한글날', None, None, A('월요일은', 50)]]
        return dict(kind='week', title='이번 주 한국 증시는 사흘', sub='코스피 그날 종가', source=SRC_KR, data={'days': days, 'lo': 0, 'hi': 7200, 'barAt': A('먼저 달력', 40)})
    if key == 'kospi':
        return dict(kind='count', title='코스피, 사흘 동안', sub=f'{md("20261002")} {D1:,.2f} → {md("20261008")} {D2:,.2f}', source=SRC_KR,
                    data={'to': D3, 'text': M(f'{D3:.2f}%'), 'label': '코스피 · 10/2 → 10/8', 'note': f'{D1:,.2f} → {D2:,.2f}', 'start': 0})
    if key == 'fx':
        pts = [[md(d), FXD[d]] for d in ['20261002'] + WEEK]
        return dict(kind='mline', title='원달러 환율도 내려왔다', sub='매매기준율 · 원 · 달러 값이 싸졌다', source=SRC_KR,
                    data={'lines': [['원달러', pts, [f'{E1:,.1f}원', f'{E2:,.1f}원'], 'fall', 0, M(f'{E3:+.2f}%')]]})
    if key == 'dart':
        return dict(kind='grid', title='공시 원문 — 연결 영업(잠정)실적', sub='단위 조원 · 원문 표를 다시 그림', source=SRC_DART,
                    data={'cols': ['2026년 3분기', '2026년 2분기', '1년 전 3분기'], 'rows': [['매출', REV, A('3분기 매출')], ['영업이익', OP, A('3분기 매출', 30)]],
                          'hot': [[1, 0, A('바로 앞 분기')], [1, 1, A('바로 앞 분기', 20)]], 'note': [f'영업이익 전분기 대비 +{OPQ}% · 전년동기 대비 +{OPY}%', A('바로 앞 분기', 40)]})
    if key == 'quote':
        return dict(kind='quote', title='잠정치라는 뜻', sub='공시 원문 4. 기타', source=SRC_DART,
                    data={'quote': QUOTE, 'stamp': ['잠정', 30]})
    if key == 'rcpt1':
        return dict(kind='rcpt', title='영수증 1 · 삼성전자 100주', sub='종가 10/2 → 10/8 · 단위 원', source=SRC_PX,
                    data={'head': '삼성전자 100주', 'rows': [['10/2 평가액', iw(C6), 'in', 0], ['10/8 평가액', iw(C7), 'in', A('이번 주 사흘')], ['평가액 차이', '−' + iw(-C8), 'net', A('이번 주 사흘', 30)]],
                          'stamp': ['평가액 · 팔기 전엔 확정 아님', A('물론 팔지')], 'total': TOT(A('이번 주 사흘', 30))})
    if key == 'div':
        return dict(kind='div', title='그럼 배당은', sub='가장 최근 분기 배당 · 2026년 2분기', source=SRC_DIV,
                    data={'head': '배당 · 100주', 'rows': [[f'1주 {won(int(B2))}원 × 100주', iw(B5), 'in', 0], ['세금 15.4%', '−' + iw(B5 - B6), 'tax', A('100주면')], ['통장에', iw(B6), 'net', A('100주면', 20)]],
                          'segs': [['6월 말', '배당 기준일', 'dim', 10], ['8/28', '지급 예정일', 'accent', 40]], 'total': TOT(0)})
    if key == 'pairs':
        return dict(kind='pairs', title='1년 사이 — 이익과 배당', sub='1년 전 3분기 → 2026년 2분기', source=SRC_DART + ' · ' + SRC_DIV,
                    data={'groups': [['영업이익', [['1년 전 3분기', A2, f'{OP[2]}조', 0], ['2026년 2분기', B3, f'{OP[1]}조', A('영업이익은 그사이')]], f'{B4}배', A('영업이익은 그사이', 20)],
                                     ['1주 배당', [['1년 전 3분기', B1, f'{int(B1)}원', 0], ['2026년 2분기', B2, f'{int(B2)}원', 8]], '거의 그대로', A('영업이익은 그사이', 60)]]})
    if key == 'dots':
        return dict(kind='dots', title='이번 주 영수증은 이렇게 기운다', sub=f'평가액 −{round(-C8 / 1e4)}만원 ÷ 세후 분기 배당 {iw(B6)}원', source=SRC_PX + ' · ' + SRC_DIV,
                    data={'n': int(C9), 'at': A('이번 주에 줄어든'), 'big': f'×{C9}', 'label': '세후 분기 배당 몇 번 치인가'})
    if key == 'pending':
        return dict(kind='pending', title='3분기 배당은 아직', sub='배당 금액은 이사회가 정한다', source=SRC_DIV,
                    data={'cards': [['1년 전 3분기 배당', '이사회 결의 2025-10-30 · 기준일 2025-09-30', 0], ['올해 3분기 배당', '금액 공시 전', A('올해 3분기')]],
                          'stamp': ['아직 공시 안 됨', A('올해 3분기', 20)]})
    if key == 'kbars':
        bars = [[md(d), KO[d], f'{KO[d]:,.2f}', 0 if d == '20261002' else A('코스피를 그대로') + 8 * i, 'fall' if d == '20261008' else 'ink', None] for i, d in enumerate(['20261002'] + WEEK)]
        return dict(kind='kbars', title='영수증 2 · 코스피 1천만원', sub='지수 그대로 따라간 돈 · 보수·세금·추적 오차 빼고', source=SRC_KR,
                    data={'min': 0, 'max': 7600, 'bars': bars, 'total': TOT(0, A('이번 주 사흘')), 'big': [f'−{-S4}만원', A('이번 주 사흘'), iw(D4) + '원 · ' + M(f'{D3:.2f}%')]})
    if key == 'diverge':
        return dict(kind='diverge', title='한 종목이나 시장 전체나', sub='10/2 → 10/8 · %', source=SRC_PX + ' · ' + SRC_KR,
                    data={'rows': [['삼성전자', C5, M(f'{C5:.2f}%'), 0], ['코스피', D3, M(f'{D3:.2f}%'), 12]], 'max': 8, 'q': ['비슷한 비율로 줄었다', 30]})
    if key == 'noreason':
        return dict(kind='stamp', title='왜 내렸나?', sub='원문 자료로는 이유까지 확인되지 않는다', source=None,
                    data={'cards': [['실적 발표', '삼성전자 공시 10/8', 0], ['시장 하락', f'코스피 {M(f"{D3:.2f}%")}', 10]], 'stamp': ['이유 · 확인 안 함', 40],
                          'no': ['영수증엔 움직인 크기만 적는다', A('그래서 여기서는')]})
    if key == 'dual':
        sp = [[d[5:].lstrip('0').replace('-', '/').replace('/0', '/'), v] for d, v in SPYW]
        fx = [[md(d), FXD[d]] for d in ['20261002'] + WEEK]
        return dict(kind='mline', title='미국 주식 = 주가 × 환율', sub='같은 주 · 위 달러 기준 주가, 아래 원달러', source=SRC_US,
                    data={'lines': [['SPY(달러)', sp, [f'${SPYW[0][1]:,.2f}', f'${SPYW[-1][1]:,.2f}'], 'rise' if UP else 'fall', 0, M(f'{F2:+.2f}%')],
                                    ['원달러', fx, [f'{E1:,.1f}원', f'{E2:,.1f}원'], 'fall', A('미국 주식은 주가랑', 30), M(f'{E3:+.2f}%')]]})
    if key == 'fxonly':
        return dict(kind='bridge', title='환율만 떼어 보면', sub='1만 달러 그대로 · 원화로 세면 · 만원', source=SRC_KR,
                    data={'steps': [['10/2 환율', E4 / 1e4, f'{man1(E4)}만', 0], ['환율 몫', E6 / 1e4, f'−{man1(E6)}만', A('달러는 그대로', 20)], ['10/8 환율', E5 / 1e4, f'{man1(E5)}만', A('달러는 그대로', 40)]],
                          'lo': 1300, 'hi': 1365, 'total': TOT(0, 0)})
    if key == 'bridge':
        return dict(kind='bridge', title='영수증 3 · 미국 1만 달러', sub=f'SPY 10/2 → {md(F1.replace("-", ""))} · 원화 · 만원', source=SRC_US,
                    data={'steps': [['10/2', F3 / 1e4, f'{man1(F3)}만', 0], ['환율 몫', E6 / 1e4, f'−{man1(E6)}만', 0], ['주가 몫', STOCK / 1e4, f'{sgn(STOCK)}{man1(STOCK)}만', 0],
                                    ['원화 합계', F4 / 1e4, f'{man1(F4)}만', A('둘을 합치면')]], 'lo': 1300, 'hi': 1365, 'total': TOT(0, 0, A('둘을 합치면', 20))})
    if key == 'trio':
        return dict(kind='trio', title='영수증 세 장', sub=NOTE, source=SRC_PX + ' · ' + SRC_KR + ' · ' + SRC_US,
                    data={'cards': [{'head': '삼성전자 100주', 'rows': [['평가액', '−' + iw(-C8), 'net'], ['지난 분기 배당(세후)', '+' + iw(B6), 'in']], 'pct': M(f'{C5:.2f}%'), 'at': A('삼성전자 100주는')},
                                    {'head': '코스피 1천만원', 'rows': [['평가액', iw(D4).replace('-', '−'), 'net']], 'pct': M(f'{D3:.2f}%'), 'at': A('비율로 보면')},
                                    {'head': '미국 1만 달러', 'rows': [['달러로', M(f'{F2:+.2f}%'), 'in'], ['원화로', ('−' if F5 < 0 else '+') + iw(abs(F5)), 'net']], 'pct': US_TXT[0], 'at': A('미국 주식을 가진')}],
                          'q': ['무엇을 · 어떤 돈으로 갖고 있느냐', A('같은 한 주라도')]})
    if key == 'cal':
        cells = [['월', '10/12', None, 0, False], ['화', '10/13', None, 0, False], ['수', '10/14', '미국 9월 CPI\n밤 9:30', A('수요일 밤'), True], ['목', '10/15', None, 0, False], ['금', '10/16', None, 0, False]]
        return dict(kind='cal', title='다음 주에 볼 날짜', sub='한국 시각', source=SRC_CAL, data={'cells': cells, 'later': []})
    if key == 'cpi':
        return dict(kind='count', title='지난 8월 미국 물가', sub='소비자물가지수 · 1년 전 같은 달 대비', source=SRC_CAL,
                    data={'to': G6, 'text': f'+{G6}%', 'label': '미국 CPI · 2026년 8월', 'note': '2025년 8월 대비', 'start': 0})
    if key == 'later':
        return dict(kind='road', title='그 뒤 날짜', sub='각 기관 일정표', source=SRC_CAL,
                    data={'head': '다음에 볼 날짜', 'rows': [['10/14(수) 21:30 · 미국 9월 CPI', 0], ['10/22(목) · 한국은행 금리 결정', 8], [f'10/27~28 · 미국 연준 FOMC', A('그 뒤로는', 40)],
                                                         ['삼성전자 3분기 배당 · 공시 나오면 계산', A('삼성전자 3분기')]]})
    if key == 'sum':
        return dict(kind='sum', title='정리', sub=NOTE, source=SRC_DART + ' · ' + SRC_KR,
                    data={'head': '이번 주', 'rows': [['가장 큰 숫자 · 3분기 영업이익(잠정)', f'{OP[0]}조원', 'in', 0], ['삼성전자 100주 평가액', '−' + iw(-C8), 'tax', A('하지만 100주')],
                                                     ['지난 분기 배당(세후)', iw(B6), 'dim', A('하지만 100주', 40)], ['미국 1만 달러', f'{US_TXT[0]} · {US_TXT[1]}', 'hi', A('미국 주식은 달러로')]],
                          'side': [f'{OP[0]}조', 0, '3분기 영업이익(잠정)']})
    if key == 'end':
        return dict(kind='end', title='내 배당엔 세금이 얼마?', sub='설명란 링크 · 다음 주 이 시간 새 영수증', source='전망·투자 권유 아님',
                    data={'text': 'firemap.kr/guide/dividend-tax-thresholds.html', 'label': '파이어맵 배당 세금 정리', 'note': '이번 주 숫자를 그대로 곱한 계산 · 다음 주는 말하지 않는다', 'start': A('내 배당에')})
    raise KeyError(key)


def main(script):
    path = os.path.join(EP, script)
    txt = open(path, encoding='utf-8').read()
    check_script(txt)
    secs = SC.parse(path)
    caps, last, pend = {}, None, None
    for line in txt.split('\n---', 1)[0].splitlines():
        s = line.strip()
        if s.startswith('## '): last, pend = None, None                      # 장 머리: 앞 장 마지막 문장에 다음 장 자막이 붙지 않게
        elif s.startswith('- '):
            last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
            if pend: caps[last], pend = pend, None                         # 장 첫 문장 앞 [자막] → 그 장 첫 문장
        elif s.startswith('[자막:'):
            if last: caps[last] = s[4:].rstrip(']').strip()
            else: pend = s[4:].rstrip(']').strip()
    voice = {}
    vj = os.path.join(EP, 'voice.json')
    if os.path.exists(vj):
        for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
            for l in s['lines']:
                if l.get('audio'): voice[l['text']] = l
    chap = lambda title: re.sub(r'^\[', '', title).split()[0].rstrip(']')
    plain = lambda t: t.replace('{F} ', '').replace('{F}', '')
    scenes = []
    for key, ch, start in CUTS:
        sec = next(s for s in secs if chap(s['title']) == ch)
        lines = sec['lines']
        cuts = [c for c in CUTS if c[1] == ch]
        idx = [0 if c[2] is None else next(j for j, t in enumerate(lines) if plain(t).startswith(c[2])) for c in cuts]
        me = [c[0] for c in cuts].index(key)
        part = lines[idx[me]:(idx[me + 1] if me + 1 < len(idx) else None)]
        out = []
        for t in part:
            v = voice.get(t) or voice.get(plain(t))
            fr = v['frames'] if v else max(12, round(SC.syl(SC.speak(plain(t))) / RATE * FPS))
            cap = caps.get(t)
            out.append({'text': plain(t), 'cap': cap.replace('{F} ', '') if cap else None, 'frames': fr, 'audio': v['audio'] if v else None})

        def A(w, plus=0, _o=out, _k=key):
            j = next((j for j, x in enumerate(_o) if w in x['text']), -1)
            assert j >= 0, (_k, w)
            return sum(x['frames'] for x in _o[:j]) + plus
        d = spec(key, A)
        frames = sum(x['frames'] for x in out) if out else 72
        if key == 'end': frames = max(frames, END_MIN)
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch in ('0.', '로고') else ch.rstrip('.') + '장', 'data': d['data'], 'lines': out, 'frames': frames})
    n_lines = sum(len(s['lines']) for s in secs)
    assert n_lines == sum(len(s['lines']) for s in scenes), f'빠진 문장: 대본 {n_lines} vs 장면 {sum(len(s["lines"]) for s in scenes)}'
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'script': script, 'rate': RATE, 'us_last': F1}
    json.dump(res, open(os.path.join(VID, 'w1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 말 {n_lines}줄 · 목소리 없는 문장 {missing} · 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})} · 미국 마지막 날 {F1}')
    for s in scenes: print(f"  {s['key']:8} {s['kind']:8} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[a.index('--script') + 1] if '--script' in a else 'script.md')
