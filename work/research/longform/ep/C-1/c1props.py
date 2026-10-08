# C-1 "3억으로 매달 200만원 — 배당으로 받기 vs 팔아서 쓰기" 화면 재료 — script.md(장·문장·[자막]) + voice.json(있으면 길이) + calc_out.txt·raw → work/video/c1.json (Remotion C1 컴포지션)
#   py -3.12 work/research/longform/ep/C-1/c1props.py [--script script.md]
# 숫자 글자는 전부 calc_out.txt(calc.py)와 raw/ecos_731Y004(말일자료) 원문에서 온다. 코드 안 숫자는 배치 좌표·축 눈금뿐.
# 대본 [자막]이 calc_out과 어긋나면 assert로 멈춘다. 목소리 없는 문장은 '말하는 글자 ÷ 5.65음절/초'로 길이를 잡는다(G-1과 같음).
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
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
won = lambda v: f'{v:,}'
M = lambda s: s.replace('-', '−')

# ── calc_out 파싱 ──
m = re.search(r'기하평균 연 수익률: 달러 ([\d.]+)% · 원화 ([\d.]+)%', CO); GEO_USD, GEO_KRW = m[1], m[2]
RET = {int(y): (float(a), float(b)) for y, a, b in re.findall(r'(\d{4}):([+\-][\d.]+)/([+\-][\d.]+)', CO.split('\n')[2])}
YEARS = list(range(1989, 2026)); assert sorted(RET) == YEARS
AVG = {}   # (억, 월만원) → dict
for r in re.finditer(r'^  ([\d.]+)억원 · 월 (\d+)만원: 세금 빼기 전 (\S+) \| A 배당 세금\+건보 (\S+) \| A 배당 세금만 (\S+) \| B 팔기 세금 (\S+)$', CO, re.M):
    AVG[(r[1], int(r[2]))] = dict(pre=r[3], A=r[4], Aonly=r[5], B=r[6])
RC = {}    # 첫해 영수증 월 → 값
for r in re.finditer(r'^  월 (\d+)만원\(연 ([\d,]+)원\): A 분배 ([\d,]+)원 = 미국 세금 ([\d,]+)원 \+ 건보 더 냄 ([\d,]+)원\(월 ([\d,]+)원\).*? \| B 첫해 판 돈 ([\d,]+)원 세금 0원 · 평가액이 산 값의 2배일 때 판 돈 ([\d,]+)원 세금 ([\d,]+)원$', CO, re.M):
    RC[int(r[1])] = {k: int(r[i].replace(',', '')) for k, i in [('net', 2), ('gross', 3), ('us', 4), ('hi', 5), ('him', 6), ('Bsell', 7), ('Bsell2', 8), ('Btax2', 9)]}
SEQ = {}   # (억, 월, A/B) → {시작해: '9' | '29+'}
for r in re.finditer(r'^  ([\d.]+)억원 · 월 (\d+)만원 · ([AB]): .*? · (1989:.*)$', CO, re.M):
    SEQ[(r[1], int(r[2]), r[3])] = dict(x.split(':') for x in r[4].split())
F20 = {}
for r in re.finditer(r'^  ([\d.]+)억원 · 월 (\d+)만원: 20년 안에 바닥 — 배당 (\d+)/18 · 팔기 (\d+)/18$', CO, re.M):
    F20[(r[1], int(r[2]))] = (int(r[3]), int(r[4]))
BAL = {}
for r in re.finditer(r'^  (\d{4})년 시작 ([AB]): (.*)$', CO, re.M):
    BAL[(int(r[1]), r[2])] = [(int(y), float(v)) for y, v in (x.split(':') for x in r[3].split())]
S6 = {}
for r in re.finditer(r'^  월 (\d+)만원 · (\d{4})년 시작: A ([^|]+) \| B ([^|]+) \|', CO, re.M):
    S6[(int(r[1]), int(r[2]))] = (r[3].strip(), r[4].strip())
S7 = {}
for r in re.finditer(r'^  (\d{4})년 시작: 원화 A ([^|]+) \| 원화 B ([^|]+) \| 달러 A ([^|]+) \| 달러 B (.+)$', CO, re.M):
    S7[int(r[1])] = [x.strip() for x in r.groups()[1:]]
m = re.search(r'원화 기준 20년 안에 바닥\(18개 중\): 배당 (\d+) · 팔기 (\d+)\s+달러 기준 20년 안에 바닥\(18개 중\): 배당 (\d+) · 팔기 (\d+)', CO)
KRW20, USD20 = (int(m[1]), int(m[2])), (int(m[3]), int(m[4]))

# ── 원자료: ECOS 731Y004 말일자료 ──
FX = {int(r['TIME']): float(r['DATA_VALUE']) for r in json.load(open(os.path.join(EP, 'raw', 'ecos_731Y004_A_1988_2025.json'), encoding='utf-8')) if r['ITEM_NAME2'] == '말일자료'}
assert FX[1996] == 844.2 and FX[1997] == 1415.2 and FX[2007] == 938.2 and FX[2008] == 1257.5 and FX[2025] == 1434.9

# ── 검산: 화면에 쓰는 값끼리 맞나 ──
R = RC[200]
assert R['gross'] - R['us'] - R['hi'] == R['net'] == 24_000_000 and R['Bsell'] == R['net']
assert abs(R['gross'] * 0.15 - R['us']) <= 1
assert R['Bsell2'] - R['Btax2'] == R['net']
GAP = R['us'] + R['hi']; assert GAP == 7_223_493
for mo in (150, 200, 300):   # 20년 안에 바닥 = 시작 1989~2006 중 연차 ≤20(‘+’ 없음)
    for side, k in (('A', 0), ('B', 1)):
        n = sum(1 for y in range(1989, 2007) if not SEQ[('3.00', mo, side)][str(y)].endswith('+') and int(SEQ[('3.00', mo, side)][str(y)]) <= 20)
        assert n == F20[('3.00', mo)][k], (mo, side, n)
assert F20[('3.00', 200)] == KRW20 == (9, 6) and USD20 == (10, 5)
assert S7[1997][0] == '29년+ 남음 5.81억원' and S7[1997][2] == '17년차 바닥' and S7[1998][0] == '11년차 바닥' and S7[1998][2] == '13년차 바닥'
assert S6[(200, 2000)] == ('9년차 바닥', '11년차 바닥') and S6[(200, 2008)] == ('17년차 바닥', '18년 버팀·2025년 말 5.27억원')
assert AVG[('3.00', 200)]['A'] == AVG[('3.00', 200)]['B'] == '100년+'
assert (AVG[('3.00', 300)]['pre'], AVG[('3.00', 300)]['A'], AVG[('3.00', 300)]['B']) == ('43년차', '12년차', '20년차')
assert RET[2008] == (-37.0, -15.6) and RET[1997] == (33.4, 123.6) and RET[2002][1] == -29.5
worst = sorted(YEARS, key=lambda y: RET[y][1])[:5]; assert worst == [2002, 2008, 2022, 2001, 2004]
for s in ['국민건강보험법 시행령 제41조①', '시행규칙 제44조① 단서', '소득세법 제14조③6호', '연 250만원 기본공제']: assert s in FACTS, s

def check_script(txt):
    for s in [won(R['gross']) + '원', won(R['us']) + '원', won(R['hi']) + '원', won(R['him']) + '원', won(R['Bsell2']) + '원', won(R['Btax2']) + '원', won(GAP) + '원',
              '9/18', '6/18', '15/18', '10/18', '5/18', '3/18', '5.81억원', '5.27억원', '844.2', '1,415.2원', '938.2', '1,257.5원', GEO_KRW + '%', GEO_USD + '%']:
        assert s in txt, f'대본 자막에 calc_out 값 없음: {s}'

SRC = '야후 파이낸스 ^SP500TR(S&P500 총수익) 연말 종가 · 한국은행 ECOS 731Y004 연말 환율 · 파이어맵 계산'
SRC_LAW = '국가법령정보센터 — 국민건강보험법 시행령 제41조 · 시행규칙 제44조 · 소득세법 제14·103·104조 · 한미 조세조약'
PAST = '지나간 기록 · 전망·투자 권유 아님'
SUB = '3억 · 월 200만원 · 원화 계산'
COND = '꺼내는 돈 전부 배당 · 1월 초 1년 치 · 물가 반영 안 함'
yr = lambda v: v if v.endswith('+') else v + '년'
bal_str = lambda s: s.replace('18년 버팀·2025년 말 ', '').replace('29년+ 남음 ', '')

CUTS = [('open', '0.', None), ('vs', '0.', '그런데 실제 시장 순서대로'), ('fx97', '0.', '딱 1년 차이인데'), ('duo', '0.', '오늘은 같은 3억을'), ('road', '0.', '이 둘을 37년'),
        ('logo', '로고', None),
        ('rules', '1.', None), ('assume', '1.', '그러니까 상품 비교가'),
        ('rcptA', '2.', None), ('thresh', '2.', '왜 이렇게 붙을까요'), ('rcptB', '2.', '매도 씨 영수증은'), ('hlist', '2.', '지역 건보료는 이자나'), ('double', '2.', '물론 주식이 오른 뒤에'),
        ('avg', '3.', None), ('gap', '3.', '첫해 영수증 차이가'),
        ('years', '4.', None), ('fx08', '4.', '금융위기 때는'), ('tiles', '4.', '시작한 해를 하나씩'),
        ('path00', '5.', None), ('path08', '5.', '이번엔 금융위기 해에'),
        ('avg300', '6.', None), ('grid', '6.', '실제 순서로는 배당 씨가'),
        ('fxline', '7.', None), ('usd', '7.', '환율을 빼도'),
        ('sum', '8.', None), ('end', '8.', '이 계산은 두 사람이')]
END_MIN = 20 * FPS


def spec(key, A):
    if key == 'open':
        return dict(kind='drain', title='3억에서 매달 200만원, 언제 바닥날까', sub=f'평균 수익률(원화 연 {GEO_KRW}%)이 매년 같다고 놓으면', source=SRC + ' · ' + PAST,
                    data={'tank': '3억원', 'out': '월 200만원', 'in': f'연 {GEO_KRW}% 매년', 'score': [['평균대로', AVG[('3.00', 200)]['A'], 8]]})
    if key == 'vs':
        a, b = S7[1997][0], S7[1998][0]
        return dict(kind='vs', title='딱 1년 차이', sub='실제 시장 순서대로 · 배당으로 받기 · ' + SUB, source=SRC,
                    data={'tiles': [['1997년 시작', bal_str(a), '2025년 말에도 남음', A('1997년에'), 'accent'], ['1998년 시작', b, '통장이 빈 해', A('1년 늦게'), 'fall']],
                          'score': [['1997년 시작', '남음', A('1997년에', 20)], ['1998년 시작', b.replace(' 바닥', ''), A('1년 늦게', 20)]]})
    if key == 'fx97':
        return dict(kind='grid', title='환율을 빼면?', sub=f'원/달러 연말 {FX[1996]:,}원 → {FX[1997]:,}원(1996 → 1997) · 배당 씨', source=SRC,
                    data={'cols': ['원화로 계산', '달러로만 계산'],
                          'rows': [['1997년 시작', [bal_str(S7[1997][0]) + ' 남음', S7[1997][2]], 0], ['1998년 시작', [S7[1998][0], S7[1998][2]], 0]],
                          'hot': [[0, 1, A('환율을 빼고')], [1, 1, A('환율을 빼고', 10)]], 'note': ['1년 차이의 대부분 = 환율 몫', A('그러니까 이 1년')]})
    if key == 'duo':
        return dict(kind='duo', title='같은 3억, 꺼내는 길 둘', sub='같은 지수 · 같은 결과 · 받는 길만 다르다', source=None,
                    data={'mid': '같은 3억', 'a': ['배당 씨', '분배금으로 받기', A('배당으로 받는')], 'b': ['매도 씨', '필요한 만큼 팔기', A('배당으로 받는', 40)]})
    if key == 'road':
        items = ['두 사람의 규칙', '첫해 영수증 — 세금·건보료', '평균이면?', '37년 실제 순서', '두 해 따라가기', '꺼내는 돈을 바꾸면', '환율']
        return dict(kind='road', title='오늘 순서', sub='1989~2025년 37년 실제 기록', source=SRC,
                    data={'rows': [[f'{"①②③④⑤⑥⑦"[i]}  {t}', A('이 둘을', 6 + 10 * i) if i < 4 else A('세금과 지역가입자', 6 + 12 * (i - 4))] for i, t in enumerate(items)]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': '배당으로 받기 vs 팔아서 쓰기 · 1989~2025'})
    if key == 'rules':
        return dict(kind='cards', title='두 사람의 규칙', sub='퇴직한 지역가입자 둘 · 같은 지수', source=SRC,
                    data={'cards': [['①', '같은 지수', 'S&P500 총수익(배당 재투자)', A('두 사람 다')], ['②', '같은 결과', '투자 수익은 똑같다고 놓음', A('투자 결과는')],
                                    ['③', '받는 길만 다름', '배당 씨 = 분배금 · 매도 씨 = 팔기', A('투자 결과는', 40)], ['④', '월 200만원', '손에 쥐는 돈 · 1월 초 1년 치', A('손에 쥐는')]]})
    if key == 'assume':
        return dict(kind='stamps', title='계산에 놓은 가정', sub='상품 비교가 아니라 받는 길 비교', source=SRC,
                    data={'cards': [['상품 비교', '아님 · 같은 결과', A('그러니까')], ['분배', '꺼내는 돈 전부 배당', A('여기선')], ['물가', '반영 안 함', A('여기선', 16)], ['종합과세 추가세', '계산 안 함', A('여기선', 32)]],
                          'stamp': ['가정', A('실제 배당 상품은')], 'no': ['= 배당 쪽 비용은 적게 잡힌 쪽', A('여기선', 50)]})
    if key == 'rcptA':
        return dict(kind='law', title='배당 씨 · 첫해 영수증', sub=SUB + ' · 단위 원', source=SRC_LAW,
                    data={'head': '배당 씨 · 첫해', 'rows': [['세전 분배금', won(R['gross']), 'in', A('배당 씨가')], ['미국 원천징수 15%', '−' + won(R['us']), 'tax', A('미국에서')],
                                                             ['건보료 더 냄(8.1348%)', '−' + won(R['hi']), 'tax', A('여기에 건강보험료')], ['손에 쥐는 돈', won(R['net']), 'net', A('여기에 건강보험료', 40)]],
                          'side': [f'월 {won(R["him"])}원', A('여기에 건강보험료', 10), '건보료 · 다음 해 11월 고지서부터']})
    if key == 'thresh':
        return dict(kind='thresh', title='배당 씨에게 걸리는 선 두 개', sub='한 해 이자+배당 · 만원', source=SRC_LAW,
                    data={'max': 3500, 'marks': [[1000, '1천만원', '넘으면 전부 건보료 소득', A('지역가입자는')], [2000, '2천만원', '종합과세 · 피부양자 탈락', A('분배금이 3천만원')]],
                          'fill': [round(R['gross'] / 10000), f'배당 씨 분배 {won(R["gross"])}원', A('왜 이렇게')],
                          'note': ['종합과세 추가 세금은 사람마다 달라 뺐다 → 실제는 더 길다', A('종합과세로')]})
    if key == 'rcptB':
        return dict(kind='twinr', title='매도 씨 · 첫해 영수증', sub=SUB + ' · 단위 원', source=SRC_LAW,
                    data={'cards': [{'head': '배당 씨', 'rows': [['꺼낸 돈', won(R['gross']), 'in', 0], ['세금+건보료', '−' + won(GAP), 'tax', 0], ['손에 쥐는 돈', won(R['net']), 'net', 0]], 'dim': True},
                                    {'head': '매도 씨', 'rows': [['판 돈', won(R['Bsell']), 'in', A('매도 씨 영수증은')], ['양도세(산 직후)', '0', 'tax', A('산 지 얼마')],
                                                                ['건보료 더 냄', '0', 'tax', A('건강보험료도')], ['손에 쥐는 돈', won(R['net']), 'net', A('건강보험료도', 20)]]}]})
    if key == 'hlist':
        rows = [[n, '들어감', 'in', 4 * i] for i, n in enumerate(['이자소득', '배당소득', '사업소득', '근로소득', '연금소득', '기타소득'])] + [['주식 판 차익(양도소득)', '목록에 없음', 'hi', A('지역 건보료는', 50)]]
        return dict(kind='law', title='지역 건보료에 들어가는 소득', sub='국민건강보험법 시행령 제41조① 목록', source=SRC_LAW,
                    data={'head': '보험료 소득 목록', 'rows': rows, 'side': ['건보료 0원', A('지역 건보료는', 60), '매도 씨가 판 차익']})
    if key == 'double':
        return dict(kind='bars', title='주식이 두 배가 된 뒤 팔면', sub='산 값의 2배일 때 손에 쥐는 2,400만원 · 해외 주식 양도세 22% · 연 250만원 공제', source=SRC_LAW,
                    data={'max': 3_000_000, 'bars': [['양도세', R['Btax2'], won(R['Btax2']) + '원', A('산 값의 두 배'), 'ink', f'판 돈 {won(R["Bsell2"])}원'],
                                                     ['건보료 더 냄', 0, '0원', A('그래도 건보료'), 'fall', '양도소득은 목록 밖']]})
    if key == 'avg':
        return dict(kind='count', title='평균이면 둘 다 평생', sub='1989~2025년 원화 기하평균이 매년 똑같이 나온다면', source=SRC,
                    data={'to': float(GEO_KRW), 'text': GEO_KRW + '%', 'label': '원화로 본 평균 · 연', 'note': f'달러로는 {GEO_USD}%', 'start': A('원화로 본'),
                          'score': [['배당 씨', AVG[('3.00', 200)]['A'], A('이러면')], ['매도 씨', AVG[('3.00', 200)]['B'], A('이러면', 10)]]})
    if key == 'gap':
        return dict(kind='zoom', title='그런데 첫해 영수증 차이는', sub='배당 씨만 빠진 돈 = 미국 세금 + 건보료', source=SRC_LAW,
                    data={'text': won(GAP) + '원', 'start': A('첫해 영수증'), 'label': '배당 씨 첫해 · 매도 씨는 0원', 'note': '평균이 높으면 이 차이가 가려진다', 'noteAt': A('평균이 높으면')})
    if key == 'years':
        vals = [RET[y][1] for y in YEARS]
        return dict(kind='years', title='실제 순서 — 해마다 원화 수익률', sub='S&P500 총수익 · 원화 환산 · 1989~2025', source=SRC,
                    data={'years': YEARS, 'vals': vals, 'start': 0, 'max': 130, 'min': -60,
                          'tags': [[YEARS.index(y), RET[y][1], f'{y} {M(f"{RET[y][1]:+.1f}")}%', A('원화로 가장') + 8 * i] for i, y in enumerate(worst[:3])]})
    if key == 'fx08':
        return dict(kind='diverge', title='2008년, 달러와 원화', sub=f'원/달러 연말 {FX[2007]:,}원 → {FX[2008]:,}원', source=SRC,
                    data={'rows': [['달러로', RET[2008][0], f'{M(f"{RET[2008][0]:+.2f}")}%', 0], ['원화로', RET[2008][1], f'{M(f"{RET[2008][1]:+.1f}")}%', A('금융위기 때는', 60)]],
                          'max': 40, 'q': ['원화로는 절반도 안 됐다', A('금융위기 때는', 90)]})
    if key == 'tiles':
        ys = list(range(1989, 2007))
        cell = lambda side: [[y, SEQ[('3.00', 200, side)][str(y)]] for y in ys]
        return dict(kind='tiles', title='시작한 해 18개 — 20년을 버텼나', sub=SUB + ' · 숫자 = 바닥난 연차(+는 자료 끝까지 버팀)', source=SRC + ' · ' + PAST,
                    data={'rows': [['배당 씨', 'accent', cell('A'), A('배당 씨 쪽은')], ['매도 씨', 'fall', cell('B'), A('매도 씨 쪽은')]],
                          'count': [[f'{KRW20[0]}/18', A('배당 씨 쪽은', 10)], [f'{KRW20[1]}/18', A('매도 씨 쪽은', 10)]],
                          'box': [1998, 2002, A('갈린 건'), '1998~2002 시작 · 큰 하락이 초반에']})
    if key in ('path00', 'path08'):
        y0 = 2000 if key == 'path00' else 2008
        a, b = BAL[(y0, 'A')], BAL[(y0, 'B')]; yrs = [y for y, _ in b] if len(b) >= len(a) else [y for y, _ in a]
        da, db = dict(a), dict(b)
        sa = [3.0] + [da.get(y, 0.0) for y in yrs]; sb = [3.0] + [db.get(y, 0.0) for y in yrs]
        keep = (2002, 2004, 2006, 2008, 2010) if key == 'path00' else (2012, 2016, 2020, 2025)
        xl = [[0, '시작']] + [[i + 1, str(y)] for i, y in enumerate(yrs) if y in keep]
        ea, eb = S6[(200, y0)]
        if key == 'path00':
            tags = [[len(a) - 1, sa[len(a) - 1], f'배당 씨 {ea}', A('배당 씨는 9년째'), 'up', True], [len(b), 0.0, f'매도 씨 {eb}', A('배당 씨는 9년째', 40), 'up', False],
                    [3, sa[3], f'2002년 말 {sa[3]:.2f}억', A('두 사람 다 원금'), 'down', False]]
            score = [['배당 씨', ea.replace(' 바닥', ''), A('배당 씨는 9년째')], ['매도 씨', eb.replace(' 바닥', ''), A('배당 씨는 9년째', 40)]]
        else:
            tags = [[len(a), 0.0, f'배당 씨 {ea}(2024)', A('배당 씨는 17년째'), 'up', True], [len(sb) - 1, sb[-1], f'매도 씨 2025년 말 {sb[-1]:.2f}억원', A('매도 씨는 지난해'), 'left', False]]
            score = [['배당 씨', ea.replace(' 바닥', ''), A('배당 씨는 17년째')], ['매도 씨', bal_str(eb), A('매도 씨는 지난해')]]
        return dict(kind='line', title=f'{y0}년에 시작한 두 사람', sub='연말 잔액 · 억원 · ' + SUB, source=SRC + ' · ' + PAST,
                    data={'series': [['배당 씨', 'accent', sa], ['매도 씨', 'fall', sb]], 'min': 0, 'max': 6 if key == 'path08' else 3.2, 'draw': 0, 'dur': 50,
                          'xlabels': xl, 'ticks': [[v, f'{v}억'] for v in ((0, 1, 2, 3) if key == 'path00' else (0, 2, 4, 6))], 'tags': tags, 'score': score, 'legend': True})
    if key == 'avg300':
        a = AVG[('3.00', 300)]
        return dict(kind='bars', title='월 300만원이면 — 평균대로여도', sub=f'3억 · 원화 평균 {GEO_KRW}% 매년 · 바닥나는 연차', source=SRC,
                    data={'max': 48, 'bars': [['세금·건보 없으면', int(a['pre'][:-2]), a['pre'], A('월 300만원이면'), 'ink', '참고'],
                                              ['배당 씨', int(a['A'][:-2]), a['A'], A('월 300만원이면', 40), 'accent', '세금+건보'], ['매도 씨', int(a['B'][:-2]), a['B'], A('매도 씨는'), 'fall', '양도세']]})
    if key == 'grid':
        rows = [[f'월 {mo}만원', [f'{F20[("3.00", mo)][0]}/18', f'{F20[("3.00", mo)][1]}/18'], at] for mo, at in [(150, A('반대로 월 150')), (200, 0), (300, 0)]]
        return dict(kind='grid', title='20년 안에 바닥난 횟수', sub='3억 · 시작 해 1989~2006년 18개 · 실제 순서(원화)', source=SRC + ' · ' + PAST,
                    data={'cols': ['배당 씨', '매도 씨'], 'rows': rows,
                          'hot': [[2, 0, A('실제 순서로는')], [2, 1, A('매도 씨도 10번')], [1, 1, A('배당 씨 쪽에선', 30)], [0, 0, A('배당 씨 쪽에선', 60)]],
                          'note': ['길 바꾸기(9→6) ≈ 덜 꺼내기(9→5)', A('배당 씨 쪽에선', 90)]})
    if key == 'fxline':
        ys = list(range(1988, 2026)); v = [FX[y] for y in ys]
        return dict(kind='line', title='원/달러 연말 환율', sub='원 · 1988~2025 · 한국은행 말일자료', source='한국은행 ECOS 731Y004 주요국 통화의 대원화환율(말일자료)',
                    data={'series': [['원/달러', 'ink', v]], 'min': 600, 'max': 1600, 'draw': 0, 'dur': 50, 'xlabels': [[i, str(y)] for i, y in enumerate(ys) if y % 5 == 0],
                          'ticks': [[800, '800'], [1000, '1,000'], [1200, '1,200'], [1400, '1,400']],
                          'tags': [[ys.index(1996), FX[1996], f'1996 {FX[1996]:,}원', A('외환위기 해에는'), 'down', False], [ys.index(1997), FX[1997], f'1997 {FX[1997]:,}원 · 원화 수익 {M(f"{RET[1997][1]:+.1f}")}%', A('외환위기 해에는', 40), 'up', True],
                                   [ys.index(2008), FX[2008], f'2008 {FX[2008]:,}원', A('맨 앞에서 본'), 'up', False]]})
    if key == 'usd':
        return dict(kind='grid', title='환율을 빼도 순서는 같았다', sub='3억 · 월 200만원 · 시작 해 1989~2006년 18개 · 20년 안에 바닥', source=SRC,
                    data={'cols': ['원화로 계산', '달러로만 계산'],
                          'rows': [['배당 씨', [f'{KRW20[0]}/18', f'{USD20[0]}/18'], 0], ['매도 씨', [f'{KRW20[1]}/18', f'{USD20[1]}/18'], 0], ['1998 시작 배당 씨', [S7[1998][0], S7[1998][2]], A('그런데 1998년')]],
                          'hot': [[0, 1, A('환율을 빼도', 30)], [1, 1, A('환율을 빼도', 50)], [2, 0, A('그런데 1998년', 30)]],
                          'note': ['앞으로 환율이 어느 쪽일지는 이 계산이 말하지 않는다', A('환율은 어느 해에')]})
    if key == 'sum':
        return dict(kind='law', title='정리 — 세 가지', sub=SUB + ' · ' + COND, source=SRC + ' · ' + PAST,
                    data={'head': '점수판 전체', 'rows': [['평균대로 계산', AVG[('3.00', 200)]['A'], 'dim', 0], ['실제 순서 · 20년 안 바닥', f'배당 {KRW20[0]}/18 · 매도 {KRW20[1]}/18', 'in', A('평균으로 계산한')],
                                                          ['첫해 더 빠진 돈(배당 씨)', won(GAP) + '원', 'tax', A('같은 지수라도')], ['월 300만원 · 20년 안 바닥', f'배당 {F20[("3.00", 300)][0]}/18 · 매도 {F20[("3.00", 300)][1]}/18', 'hi', A('그리고 얼마를')]],
                          'side': ['꺼내는 돈', A('그리고 얼마를', 20), '받는 길만큼 중요했다']})
    if key == 'end':
        return dict(kind='end', title='내 배당이면 건보료는?', sub='금융소득만 넣어 보기 · 전체 표는 설명란의 카페 글', source=PAST,
                    data={'text': 'firemap.kr/health-insurance', 'label': '파이어맵 건보료 계산기', 'note': '금액별 전체 표(1억·3억·5억 × 월 100~300만원) = 카페 글', 'start': A('내 배당이')})
    raise KeyError(key)


def main(script):
    path = os.path.join(EP, script)
    txt = open(path, encoding='utf-8').read()
    check_script(txt)
    secs = SC.parse(path)
    caps, last = {}, None
    for line in txt.split('\n---', 1)[0].splitlines():
        s = line.strip()
        if s.startswith('- '): last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
        elif s.startswith('[자막:') and last: caps[last] = s[4:].rstrip(']').strip()
    voice = {}
    vj = os.path.join(EP, 'voice.json')
    if os.path.exists(vj):
        for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
            for l in s['lines']:
                if l.get('audio'): voice[l['text']] = l
    chap = lambda title: re.sub(r'^\[', '', title).split()[0].rstrip(']')
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
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'script': script, 'rate': RATE}
    json.dump(res, open(os.path.join(VID, 'c1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 말 {n_lines}줄 · 목소리 없는 문장 {missing} · 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})}')
    for s in scenes: print(f"  {s['key']:8} {s['kind']:8} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[a.index('--script') + 1] if '--script' in a else 'script.md')
