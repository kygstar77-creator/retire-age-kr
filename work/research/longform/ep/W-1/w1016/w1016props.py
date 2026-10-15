# W-1 2화 화면 재료 — script.md(장·문장·[자막]) + voice.json + calc_out.txt·raw → work/video/w1016.json (Remotion 'w1016' 컴포지션 = src/w1016.tsx)
#   py -3.12 work/research/longform/ep/W-1/w1016/w1016props.py
# 1화 w1props.py와 같은 짜임. 숫자 글자는 전부 calc_out.txt와 raw 원문(ECOS 일별·야후 SPY)에서 온다. 코드 안 숫자는 배치 좌표·축 범위뿐.
# 2장은 motion_preview/buyprops.py가 만든 w2_buy.json(BuybackDays, DART 하루 평균단가 29개)을 그대로 쓴다 — 녹음 뒤 buyprops.py 먼저.
# 로고 장면 없음(lfrender 첫 60초 로고 관문, R-1 새 판과 같음). 1화에 쓴 영수증(rcpt) 판은 대본이 '영수증' 비유를 금지해 쓰지 않는다.
import json, os, re, sys, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
FPS = 30
CO = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
won = lambda v: f'{int(round(v)):,}'
M = lambda s: s.replace('-', '−')

V = {}
for k, v in re.findall(r'^\[(\w+)\][^=\n]*= (.+)$', CO, re.M): V.setdefault(k, v.strip())
V1 = {k: v.strip() for k, v in re.findall(r'^\[1화\] \[(\w+)\][^=\n]*= (.+)$', CO, re.M)}
num = lambda k, d=V: float(d[k].replace(',', ''))
D1, D2, D3, D4, D5, D6 = (num(k) for k in ('D1', 'D2', 'D3', 'D4', 'D5', 'D6'))
E1, E2, E3, E4, E5, E6 = (num(k) for k in ('E1', 'E2', 'E3', 'E4', 'E5', 'E6'))
F2, F3, F4, F5 = (num(k) for k in ('F2', 'F3', 'F4', 'F5'))
A1, A2, A3, A4 = (num(k) for k in ('A1', 'A2', 'A3', 'A4'))
B3, B5 = num('B3'), num('B5')
H2, H3 = num('H2'), num('H3')
H4 = [int(x.replace(',', '')) for x in V['H4'].split('·')]
C2, C3 = num('C2'), num('C3')
C6, C7, C8, C9 = (num(k) for k in ('C6', 'C7', 'C8', 'C9'))
C5 = float(V['C5'].split('·')[-1])
S1, S2, S3 = int(num('S1')), int(num('S2')), num('S3')
S5 = int(V['S5'].split('→')[1].split('(')[0].replace(',', ''))
P1_D3, P1_D4, P1_F2, P1_F5 = num('D3', V1), num('D4', V1), num('F2', V1), num('F5', V1)
STOCK = F4 - E5                           # 주가 몫(원) = 마지막 원화 − 환율만 바뀐 원화
assert abs(E6 + STOCK - F5) <= 1 and S1 * 10000 == A4 and round(D4 / 1e4) == S2 and round(F5 / 1e3) / 10 == S3
assert S5 == A4 + D4 + F5                  # 세 칸 합 = 대본 399만원

EC = json.load(open(os.path.join(EP, 'raw', 'ecos_d_20261016.json'), encoding='utf-8'))['data']
KO = {t: v for t, v in EC['802Y001']}; FXD = {t: v for t, v in EC['731Y001']}
WEEK = ['20261012', '20261013', '20261014']
assert KO['20261008'] == D1 and KO['20261014'] == D2 and FXD['20261008'] == E1 and FXD['20261014'] == E2
assert all(d in KO for d in WEEK) and '20261009' not in KO
j = json.load(open(os.path.join(EP, 'raw', 'yh_SPY.json'), encoding='utf-8'))['chart']['result'][0]; tz = j['meta']['gmtoffset']
SPY = {dt.datetime.fromtimestamp(t + tz, dt.UTC).strftime('%Y-%m-%d'): v for t, v in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if v}
SPYW = [(d, SPY[d]) for d in sorted(SPY) if '2026-10-08' <= d <= '2026-10-14']
assert round((SPYW[-1][1] / SPYW[0][1] - 1) * 100, 2) == F2
BUY = json.load(open(os.path.join(EP, 'motion_preview', 'w2_buy.json'), encoding='utf-8'))

def check_script(txt):
    for s in ['262,000원', '232,000원', '263,823원', '−12.06%', '6,625.93', '6,008.81', '−9.31%', '−5.39%', '1,605,000원', '1,443,000원', '−10.09%',
              '1,339.20원', '1,340.50원', '−931,371원', '−539,440원', '−1,420,570원', '−11.45%', '−15.59%', '+3.7%', '8월 +3.4%', '+34.2', '+20.4', '+3.2', '+2.5',
              '+2.6%', '−0.55%', '1,339.2만원', '1,333.1만원', '−60,786원', '−3,992,157원', '10/22', '10/27~28', '2026-10-28 09:00', '2025-10-30', '21:30']:
        assert s in txt, f'대본 자막에 calc_out 값 없음: {s}'

SRC_PX = '다음 금융(KRX 정규장 종가)'
SRC_DART = 'DART 2026.10.12 자기주식취득결과보고서'
SRC_KR = '한국은행 ECOS 802Y001 코스피 · 731Y001 원달러 매매기준율(일)'
SRC_SPY = '야후 파이낸스 SPY 일별 종가'
SRC_US = SRC_SPY + ' · 한국은행 ECOS 원달러 매매기준율'
SRC_CPI = '미국 노동통계국(BLS) CPI · FRED CPIAUCNS'
SRC_CAL = '한국은행·미국 연준 일정표 · DART 2026.10.14 SK하이닉스 IR 안내'
NOTE = '평가액 기준 · 팔지 않으면 확정 아님 · 수수료 빼고 계산 · 전망·투자 권유 아님'
md = lambda d: f'{int(d[4:6])}/{int(d[6:])}'
man1 = lambda v: f'{abs(v) / 10000:,.1f}'
sgn = lambda v: '−' if v < 0 else '+'
HEAD = '이번 주 내 돈'
TOT = lambda a=None, b=None, c=None: [['삼성전자 100주', f'−{-S1}만원', a if a is not None else 10**9],
                                      ['코스피 1천만원', f'−{-S2}만원', b if b is not None else 10**9],
                                      ['미국 1만 달러', f'{sgn(F5)}{abs(S3)}만원', c if c is not None else 10**9]]

# (장면 키, 장, 이 장면이 시작하는 말 줄 머리)
CUTS = [('open', '0.', None), ('avg', '0.', '수요일 종가는'), ('ratio', '0.', '같은 기간'),
        ('week', '1.', None), ('kospi', '1.', '월요일부터'), ('vs1', '1.', '지난주 사흘'), ('hynix', '1.', '화요일 하루'), ('noreason', '1.', '왜 빠졌는지'),
        ('buy', '2.', None),
        ('kbars', '3.', None), ('twoweek', '3.', '1화 때부터'), ('diverge', '3.', '비율로 보면'),
        ('cal', '4.', None), ('cpi', '4.', '1년 전 같은'), ('parts', '4.', '부문별로는'), ('core', '4.', '식품과 에너지'), ('dual', '4.', '발표가 있던'), ('bridge', '4.', '기간 전체로'),
        ('trio', '5.', None), ('last', '5.', '지난주엔'), ('rates', '5.', '이번 주는'),
        ('next', '6.', None), ('pending', '6.', '1화에서'),
        ('end', '7.', None)]
END_MIN = 20 * FPS


def spec(key, A):
    if key == 'open':
        return dict(kind='open', title='삼성전자 100주, 이번 주', sub='종가 10/8 → 10/14(수) · 단위 원', source=SRC_PX + ' · ' + SRC_DART,
                    data={'head': '삼성전자 100주 · 월~수', 'rows': [['10/8 종가 × 100주', won(A1 * 100), 'in', 0], ['10/14 종가 × 100주', won(A2 * 100), 'in', 8], ['평가액', '−' + won(-A4), 'net', 16]],
                          'big': ['15조원', A('삼성전자는'), '회사가 산 자기 회사 주식 · 8/24 ~ 10/6']})
    if key == 'avg':
        return dict(kind='bars', title='회사가 산 값 vs 수요일 종가', sub='1주당 · 원 · 평균 취득가는 수수료 제외', source=SRC_DART + ' · ' + SRC_PX,
                    data={'min': 0, 'max': 300_000, 'bars': [['회사가 산 평균값', B3, won(B3) + '원', 0, 'ink', None], ['10/14 종가', A2, won(A2) + '원', 10, 'fall', M(f'{B5:+.2f}%')]],
                          'dark': ['싸다는 뜻 아님 · 바닥·매수 신호 아님', A('그렇다고')]})
    if key == 'ratio':
        return dict(kind='diverge', title='같은 사흘, 줄어든 비율', sub='10/8 → 10/14 · %', source=SRC_KR + ' · ' + SRC_SPY,
                    data={'rows': [['코스피', D3, M(f'{D3:.2f}%'), 0], ['미국 SPY(달러)', F2, M(f'{F2:.2f}%'), 12]], 'max': 10, 'q': ['열 배 넘게 차이', 40]})
    if key == 'week':
        days = [['월', md(WEEK[0]), None, KO[WEEK[0]], f'{KO[WEEK[0]]:,.2f}', 0], ['화', md(WEEK[1]), None, KO[WEEK[1]], f'{KO[WEEK[1]]:,.2f}', 6],
                ['수', md(WEEK[2]), None, KO[WEEK[2]], f'{KO[WEEK[2]]:,.2f}', 12], ['목', '10/15', '계산에 없음', None, None, A('목요일과', 0)], ['금', '10/16', '계산에 없음', None, None, A('목요일과', 0) + 6]]
        return dict(kind='week', title='이번 주는 수요일 마감까지', sub='코스피 그날 종가', source=SRC_KR, data={'days': days, 'lo': 0, 'hi': 7200, 'barAt': 10})
    if key == 'kospi':
        return dict(kind='count', title='코스피, 월~수 사흘', sub=f'10/8 {D1:,.2f} → 10/14 {D2:,.2f}', source=SRC_KR,
                    data={'to': D3, 'text': M(f'{D3:.2f}%'), 'label': '코스피 · 10/8 → 10/14', 'note': f'{D1:,.2f} → {D2:,.2f}', 'start': 0})
    if key == 'vs1':
        return dict(kind='diverge', title='지난주와 비교하면', sub='코스피 · 사흘씩 · %', source=SRC_KR,
                    data={'rows': [['지난주 · 1화', P1_D3, M(f'{P1_D3:.2f}%'), 0], ['이번 주', D3, M(f'{D3:.2f}%'), 12]], 'max': 10, 'q': ['훨씬 가팔랐다', 40]})
    if key == 'hynix':
        return dict(kind='bars', title='SK하이닉스, 화요일 하루', sub='종가 · 원', source=SRC_PX,
                    data={'min': 0, 'max': 1_800_000, 'bars': [['10/12 월', H4[0], won(H4[0]) + '원', 0, 'ink', None], ['10/13 화', H4[1], won(H4[1]) + '원', 10, 'fall', M(f'{H3:+.2f}%')]],
                          'dark': [f'원달러 {M(f"{E3:+.2f}%")} · 환율은 거의 그대로', A('환율은')]})
    if key == 'fx':
        pts = [[md(d), FXD[d]] for d in ['20261008'] + WEEK]
        return dict(kind='mline', title='원달러 환율은 거의 그대로', sub='매매기준율 · 원', source=SRC_KR,
                    data={'lines': [['원달러', pts, [f'{E1:,.2f}원', f'{E2:,.2f}원'], 'ink', 0, M(f'{E3:+.2f}%')]]})
    if key == 'noreason':
        return dict(kind='stamp', title='왜 내렸나?', sub='이번 주 공시·통계로는 이유가 확인되지 않는다', source=None,
                    data={'cards': [['코스피 월~수', M(f'{D3:.2f}%'), 0], ['SK하이닉스 화요일', M(f'{H3:.2f}%'), 10]], 'stamp': ['이유 · 확인 안 함', 30],
                          'no': ['여기선 금액만 센다', A('그래서', 0)]})
    if key == 'kbars':
        bars = [[md(d), KO[d], f'{KO[d]:,.2f}', 0 if d == '20261008' else 8 * i, 'fall' if d == '20261014' else 'ink', None] for i, d in enumerate(['20261008'] + WEEK)]
        return dict(kind='kbars', title='코스피 1천만원', sub='지수 그대로 따라간 돈 · 보수·세금·추적 오차 빼고', source=SRC_KR,
                    data={'min': 0, 'max': 7600, 'bars': bars, 'total': TOT(0, 30), 'big': [f'−{-S2}만원', 30, won(D4).replace('-', '−') + '원 · ' + M(f'{D3:.2f}%')]})
    if key == 'twoweek':
        return dict(kind='bars', title='1화부터 두 주 들고 있었다면', sub='코스피 1천만원 · 줄어든 돈 · 원', source=SRC_KR,
                    data={'min': 0, 'max': 1_600_000, 'bars': [['지난주(1화)', -P1_D4, '−' + won(-P1_D4), 0, 'ink3', None], ['이번 주', -D4, '−' + won(-D4), 8, 'ink', None],
                                                              ['두 주 이어서', -D6, '−' + won(-D6), 16, 'fall', M(f'{D5:.2f}%')]]})
    if key == 'diverge':
        return dict(kind='diverge', title='한 종목과 시장 전체', sub='10/8 → 10/14 · %', source=SRC_PX + ' · ' + SRC_KR,
                    data={'rows': [['삼성전자', A3, M(f'{A3:.2f}%'), 0], ['코스피', D3, M(f'{D3:.2f}%'), 10], ['SK하이닉스', H2, M(f'{H2:.2f}%'), 20]], 'max': 18,
                          'q': ['삼성전자가 시장보다 조금 더', 40]})
    if key == 'cal':
        cells = [['월', '10/12', None, 0, False], ['화', '10/13', None, 0, False], ['수', '10/14', '미국 9월 소비자물가\n한국 밤 9:30', 6, True], ['목', '10/15', None, 0, False], ['금', '10/16', None, 0, False]]
        return dict(kind='cal', title='수요일 밤, 미국 발표', sub='한국 시각', source=SRC_CPI, data={'cells': cells, 'later': []})
    if key == 'cpi':
        return dict(kind='count', title='미국 9월 소비자물가', sub='1년 전 같은 달 대비 · 비계절조정', source=SRC_CPI,
                    data={'to': C2, 'text': f'+{C2}%', 'label': '미국 CPI · 2026년 9월', 'note': f'8월 +{C3}%', 'start': 0})
    if key == 'parts':
        return dict(kind='bars', title='부문별로는', sub='1년 전 같은 달 대비 · %', source='BLS CUUR0000 계열(비계절조정)',
                    data={'min': 0, 'max': 40, 'bars': [['휘발유', C6, f'+{C6}%', 0, 'rise', None], ['에너지 전체', C7, f'+{C7}%', 10, 'ink', None],
                                                       ['주거', C9, f'+{C9}%', 18, 'ink', None], ['식품', C8, f'+{C8}%', 26, 'ink', None]]})
    if key == 'core':
        return dict(kind='count', title='식품·에너지 뺀 근원 물가', sub='1년 전 같은 달 대비 · 비계절조정', source='BLS CUUR0000SA0L1E',
                    data={'to': C5, 'text': f'+{C5}%', 'label': '근원 CPI · 2026년 9월', 'note': f'전체 +{C2}%', 'start': 0})
    if key == 'dual':
        sp = [[d[5:].lstrip('0').replace('-', '/').replace('/0', '/'), v] for d, v in SPYW]
        fx = [[md(d), FXD[d]] for d in ['20261008'] + WEEK]
        return dict(kind='mline', title='미국 주식 = 주가 × 환율', sub='위 SPY 달러 종가, 아래 원달러', source=SRC_US,
                    data={'lines': [['SPY(달러)', sp, [f'${SPYW[0][1]:,.2f}', f'${SPYW[-1][1]:,.2f}'], 'fall', 0, M(f'{F2:+.2f}%')],
                                    ['원달러', fx, [f'{E1:,.1f}원', f'{E2:,.1f}원'], 'ink', A('환율은'), M(f'{E3:+.2f}%')]],
                          'dark': ['같은 날이었다는 것까지만 확인', A('물가 발표')]})
    if key == 'bridge':
        return dict(kind='bridge', title='미국 1만 달러', sub='SPY 10/8 → 10/14 · 원화 · 만원', source=SRC_US,
                    data={'steps': [['10/8', F3 / 1e4, f'{man1(F3)}만', 0], ['환율 몫', E6 / 1e4, f'+{man1(E6)}만', 0], ['주가 몫', STOCK / 1e4, f'{sgn(STOCK)}{man1(STOCK)}만', 0],
                                    ['10/14', F4 / 1e4, f'{man1(F4)}만', A('미국 주식에')]], 'lo': 1300, 'hi': 1350, 'total': TOT(0, 0, A('미국 주식에', 20))})
    if key == 'trio':
        return dict(kind='trio', title='셋을 나란히', sub=NOTE, source=SRC_PX + ' · ' + SRC_KR + ' · ' + SRC_SPY,
                    data={'cards': [{'head': '삼성전자 100주', 'rows': [['평가액', '−' + won(-A4), 'net']], 'pct': M(f'{A3:.2f}%'), 'at': 0},
                                    {'head': '코스피 1천만원', 'rows': [['평가액', won(D4).replace('-', '−'), 'net']], 'pct': M(f'{D3:.2f}%'), 'at': 10},
                                    {'head': '미국 1만 달러', 'rows': [['원화로', won(F5).replace('-', '−'), 'net']], 'pct': f'달러 {M(f"{F2:.2f}%")}', 'at': 20}],
                          'q': [f'합쳐서 −{won(-S5)}원', A('세 칸을', 40)]})
    if key == 'last':
        return dict(kind='pending', title='미국 1만 달러 · 지난주와 이번 주', sub='달러로 · 원화로', source=SRC_US,
                    data={'cards': [['지난주 · 1화', f'달러 {M(f"{P1_F2:+.2f}%")} · 원화 {won(P1_F5).replace("-", "−")}원', 0], ['이번 주', f'달러 {M(f"{F2:+.2f}%")} · 원화 {won(F5).replace("-", "−")}원', 14]],
                          'dashed': -1})
    if key == 'rates':
        return dict(kind='diverge', title='어디에 넣어 뒀느냐', sub='10/8 → 10/14 · %', source=SRC_PX + ' · ' + SRC_KR + ' · ' + SRC_SPY,
                    data={'rows': [['삼성전자', A3, M(f'{A3:.2f}%'), 0], ['코스피', D3, M(f'{D3:.2f}%'), 8], ['SPY(달러)', F2, M(f'{F2:.2f}%'), 16], ['원달러', E3, M(f'{E3:+.2f}%'), 24]],
                          'max': 12, 'q': ['한국 쪽이 훨씬 컸다', A('똑같은')]})
    if key == 'next':
        cells = [['월', '10/19', None, 0, False], ['화', '10/20', None, 0, False], ['수', '10/21', None, 0, False], ['목', '10/22', '한국은행\n금리 결정', 6, True], ['금', '10/23', None, 0, False]]
        return dict(kind='cal', title='다음에 볼 날짜', sub='각 기관 일정표 · 공시', source=SRC_CAL,
                    data={'cells': cells, 'later': [['10/27~28', '미국 연준 회의', A('그다음 주')], ['10/28 09:00', 'SK하이닉스 3분기 실적', A('SK하이닉스는')]]})
    if key == 'pending':
        return dict(kind='pending', title='삼성전자 3분기 배당은 아직', sub='1화에서 본 것 · DART 공시', source='DART 공시 목록 10/1~10/14 · DART 20251030800075',
                    data={'cards': [['1년 전 3분기 배당', '이사회 결의 2025-10-30', 0], ['올해 3분기 배당', '10/14까지 공시 없음', 10]], 'stamp': ['아직 공시 안 됨', 30]})
    if key == 'end':
        return dict(kind='end', title='수요일 마감 기준', sub='종가와 공시로만 계산 · 전망·투자 권유 아님', source=None,
                    data={'text': '이번 주 뉴스가 내 돈에 얼마 · 1화', 'label': '지난 편 · 지난주 사흘', 'note': '수요일 마감 종가와 공시로만 계산 · 전망도 투자 권유도 아님', 'start': A('수요일 마감 기준으로')})
    raise KeyError(key)


def main():
    path = os.path.join(EP, 'script.md')
    txt = open(path, encoding='utf-8').read()
    check_script(txt)
    secs = SC.parse(path)
    plain = lambda t: re.sub(r'\{[A-Z]\}\s*', '', t).strip()
    caps, last, pend = {}, None, None
    for line in txt.split('\n---', 1)[0].splitlines():
        s = line.strip()
        if s.startswith('## '): last, pend = None, None
        elif s.startswith('- '):
            last = plain(re.sub(r'\s*\(화면.*$', '', s[2:]).strip())
            if pend: caps[last], pend = pend, None
        elif s.startswith('[자막:'):
            c = plain(s[4:].rstrip(']').strip())
            if last and last not in caps: caps[last] = c          # 줄마다 첫 [자막]만(1화와 같음)
            elif not last: pend = c
    voice = {}
    for s in json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[plain(l['text'])] = l
    chap = lambda title: re.sub(r'^\[', '', title).split()[0].rstrip(']')
    scenes = []
    for key, ch, start in CUTS:
        if key == 'buy':
            b = BUY['scene']; scenes.append({**b, 'chapter': '2장', 'data': BUY['buy']}); continue
        sec = next(s for s in secs if chap(s['title']) == ch)
        lines = [plain(t) for t in sec['lines']]
        cuts = [c for c in CUTS if c[1] == ch]
        idx = [0 if c[2] is None else next(j for j, t in enumerate(lines) if t.startswith(c[2])) for c in cuts]
        me = [c[0] for c in cuts].index(key)
        part = lines[idx[me]:(idx[me + 1] if me + 1 < len(idx) else None)]
        out = []
        for t in part:
            v = voice[t]
            out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'], 'audio': v['audio']})

        def A(w, plus=0, _o=out, _k=key):
            j = next((j for j, x in enumerate(_o) if w in x['text']), -1)
            assert j >= 0, (_k, w)
            return sum(x['frames'] for x in _o[:j]) + plus
        d = spec(key, A)
        frames = sum(x['frames'] for x in out)
        if key == 'end': frames = max(frames, END_MIN)
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch == '0.' else ch.rstrip('.') + '장', 'data': d['data'], 'lines': out, 'frames': frames})
    n_lines = sum(len(s['lines']) for s in secs)
    assert n_lines == sum(len(s['lines']) for s in scenes), f'빠진 문장: 대본 {n_lines} vs 장면 {sum(len(s["lines"]) for s in scenes)}'
    assert all(l['audio'] for s in scenes for l in s['lines']), '목소리 없는 문장'
    res = {'fps': FPS, 'scenes': scenes, 'missing': 0, 'script': 'w1016/script.md'}
    json.dump(res, open(os.path.join(VID, 'w1016.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 말 {n_lines}줄 · 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})}')
    for s in scenes: print(f"  {s['key']:8} {s['kind']:8} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    main()
