# G-1 "금값 1천만원 영수증 4장" 화면 재료 — script.md(장·문장·[자막]) + voice.json(있으면 길이) + calc_out.txt·raw → work/video/g1.json (Remotion G1 컴포지션)
#   py -3.12 work/research/longform/ep/G-1/g1props.py [--script script.md]
# 숫자 글자는 전부 calc_out.txt(공개 전날 calc.py 재실행 결과)와 raw/calc_<기준일>.json·ust_*.csv·facts.txt 원문 줄에서 온다.
#   → calc를 다시 돌리면 이 파일도 다시 돌리면 끝. 대본 [자막]이 calc_out과 어긋나면 assert로 멈춘다(대본도 같이 고쳐야 한다는 뜻).
# 목소리가 없는 문장은 '말하는 글자 ÷ 5.65음절/초'로 길이를 잡는다(R-1과 같음). 업로드는 missing=0일 때만.
import csv, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
RATE = 5.65
FPS = 30
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
CO = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
def need(*ss):
    for s in ss: assert s in FACTS, f'facts.txt에 없는 줄: {s}'
num = lambda s: int(s.replace(',', ''))
pc = lambda s: float(s.replace('−', '-'))
M = lambda s: s.replace('-', '−')          # 화면 음수 기호
won = lambda v: f'{v:,}'

# ── calc_out.txt 파싱 ──
m = re.search(r'^KRX 금 (\d{4}-\d\d-\d\d) ([\d,]+)원/g · 1년 고점 (\d{4}-\d\d-\d\d) ([\d,]+)원/g · 고점 대비 (-[\d.]+)% · 산 값\(고점\)으로 돌아가려면 \+([\d.]+)%', CO, re.M)
ASOF, NOWP, PEAKD, PEAKP, PEAKPCT, BACK = m[1], num(m[2]), m[3], num(m[4]), m[5], m[6]
DATES = []   # [(라벨, 날짜, 원/g, {길: (원, %)})]
for r in re.finditer(r'^\| (1년 전|1년 고점|3개월 전|1개월 전) (\d{4}-\d\d-\d\d) \(([\d,]+)원/g\) \| ([\d,]+)원 \((-?[+\-]?[\d.]+)%\) \| ([\d,]+)원 \(([+\-]?[\d.]+)%\) \| ([\d,]+)원 \(([+\-]?[\d.]+)%\) \| ([\d,]+)원 \(([+\-]?[\d.]+)%\) \|', CO, re.M):
    DATES.append((r[1], r[2], num(r[3]), {'KRX': (num(r[4]), r[5]), 'ETF': (num(r[6]), r[7]), 'BANK': (num(r[8]), r[9]), 'BAR': (num(r[10]), r[11])}))
assert [d[0] for d in DATES] == ['1년 전', '1년 고점', '3개월 전', '1개월 전'], DATES
DEC = {}
for r in re.finditer(r'^\| (1년 전|1년 고점|3개월 전|1개월 전) \d{4}-\d\d-\d\d \| ([+\-][\d.]+)% \| ([+\-][\d.]+)% \([^)]*\) \| ([+\-][\d.]+)% \([^)]*\) \| ([+\-][\d.]+)% \([^)]*\) \| ([+\-][\d.]+)% → ([+\-][\d.]+)% \| ([+\-][\d.]+)% \|', CO, re.M):
    DEC[r[1]] = dict(tot=r[2], usd=r[3], fx=r[4], prem=r[5], p0=r[6], p1=r[7], chk=r[8])
assert len(DEC) == 4
for k, d in DEC.items():   # 세 조각 곱 = 전체(검산), KRX 영수증 % = 전체
    prod = (1 + pc(d['usd']) / 100) * (1 + pc(d['fx']) / 100) * (1 + pc(d['prem']) / 100) - 1
    assert abs(prod * 100 - pc(d['tot'])) < 0.015 and d['tot'] == d['chk'], (k, prod)
for lab, dt, g, P in DATES:
    assert P['KRX'][1] == DEC[lab]['tot'], lab
    assert abs(10_000_000 * NOWP / g - P['KRX'][0]) <= 1, lab          # 1천만원 × 지금 ÷ 산 값
    assert abs(P['BAR'][0] - 10_000_000 / 1.1 * NOWP / g) <= 1, lab     # 부가세 10% 뺀 금값 몫이 KRX만큼
D = {d[0]: d for d in DATES}
assert D['1년 고점'][1] == PEAKD and D['1년 고점'][2] == PEAKP and DEC['1년 고점']['tot'] == PEAKPCT
assert abs((PEAKP / NOWP - 1) * 100 - float(BACK)) < 0.05
VAT, GOLDPART = 909_091, 9_090_909; assert VAT + GOLDPART == 10_000_000 and round(10_000_000 / 11) == VAT
need('1천만원 중 부가세 10%(909,091원)가 붙어 금값 몫은 9,090,909원', 'ETF 차익 전부 과세로 보면 15.4% → 154,000원, 남는 846,000원')
assert int(1_000_000 * 0.154) == 154_000

# 대본 [자막]과 calc_out이 같은 기준일인지 — 어긋나면 멈춘다
SCRIPT_TXT = None
def check_script(txt):
    for lab, dt, g, P in DATES:
        for s in [won(P['KRX'][0]) + '원', dt]: assert s in txt, f'대본 자막에 calc_out 값 없음: {s} — calc 재실행 뒤 대본도 고쳐야 함'
    for d in DEC.values():
        for s in [d['usd'].replace('-', '−'), d['fx'].replace('-', '−')]:
            assert s.lstrip('+') in txt, f'대본에 세 조각 값 없음: {s}'
    assert won(NOWP) + '원' in txt and won(PEAKP) + '원' in txt

# ── 원자료(선) ──
RAW = json.load(open(os.path.join(EP, 'raw', f'calc_{ASOF}.json'), encoding='utf-8'))
KRX = sorted((d, v) for d, v in RAW['KRX_M04020000_won_per_g'].items() if d >= '2025-10-01')
FXS = sorted((d, v) for d, v in RAW['ECOS_731Y001_0000001'].items() if '2025-09-01' <= d <= ASOF)
assert dict(KRX)[ASOF] == NOWP and dict(KRX)[PEAKD] == PEAKP and max(v for dd, v in KRX if dd >= '2025-10-02') == PEAKP
need('최고 1,554.4원(2026-07-02)', '2026-10-06 1,358.5원')
fx = dict(FXS); assert fx['2026-07-02'] == 1554.4 and max(fx.values()) == 1554.4 and fx.get('2026-10-06') == 1358.5
UST = []
for fn in ['ust_2025.csv', 'ust_2026.csv']:
    for row in csv.DictReader(open(os.path.join(EP, 'raw', fn), encoding='utf-8')):
        mm, dd, yy = row['Date'].split('/'); UST.append((f'{yy}-{mm}-{dd}', float(row['10 Yr'])))
UST = sorted(x for x in UST if '2025-09-02' <= x[0] <= '2026-10-05')
u = dict(UST); need('2025-10-02 4.10%', '2026-10-05 5.31%', '최고 5.31%(2026-10-05)')
assert u['2025-10-02'] == 4.10 and u['2026-10-05'] == 5.31 and max(u.values()) == 5.31

def thin(rows, step):
    out = rows[::step]
    if out[-1] != rows[-1]: out.append(rows[-1])
    return out
def months(rows, every=2):
    seen, res = set(), []
    for i, (d, _) in enumerate(rows):
        k = d[:7]
        if k not in seen: seen.add(k); res.append([i, f'{int(d[5:7])}월' if d[5:7] != '01' else f'{d[2:4]}.1월'])
    return res[::every]

SRC_KRX = '한국거래소 KRX 금시장 금 1kg 종가(네이버 증권 일별 시세) · ' + ASOF + ' 기준'
SRC_DEC = 'KRX 금 종가 · 금 선물 GC=F(야후, 뉴욕 전날 종가) · 한국은행 ECOS 731Y001 매매기준율(파이어맵 계산, 국제값은 어림)'
SRC_LAW = '국가법령정보센터 — 조세특례제한법 제126조의7 · 소득세법 제94·17·129·14조 · 부가가치세법 제30조'
PAST = '지나간 값 · 전망·투자 권유 아님'
NOTFEE = '증권사 수수료 별도'
SHORT = {'1년 전': '1년 전', '1년 고점': '1월 고점', '3개월 전': '3개월 전', '1개월 전': '1개월 전'}
dot = lambda dt: dt[2:].replace('-', '.')   # 25.10.02

CUTS = [('open', '0.', None), ('pick', '0.', '금을 갖고 계시다면'), ('road', '0.', '오늘은 천만원어치'), ('logo', '로고', None),
        ('today', '1.', None),
        ('buy', '2.', None), ('odd', '2.', '그럼 이상한 점'),
        ('formula', '3.', None), ('piece1', '3.', '작년 영수증부터'), ('prem', '3.', '셋째 조각이'), ('piece1b', '3.', '세 조각을 곱하면'), ('piece2', '3-2.', None), ('grid', '3-2.', '3개월 전은 또'),
        ('paths', '4.', None), ('krx', '4.', '먼저 KRX 금시장'), ('etf', '4.', '두 번째는 금 ETF'), ('bank', '4-2.', None),
        ('bar', '4-2.', '네 번째는 골드바'), ('pathcmp', '4-2.', '작년에 골드바로'), ('up10', '4-2.', '금값이 10% 오른다고'),
        ('ust', '5.', None), ('fxl', '5.', '환율은 여름에'), ('bok', '5.', '한국은행은 8월에'), ('wgc', '5.', '세계금협회'), ('nocause', '5.', '금리, 환율, 중앙은행'),
        ('math', '6.', None), ('sum', '7.', None), ('end', '7.', '산 날 네 개')]
END_MIN = 20 * FPS


def spec(key, L, A):
    K = {lab: P['KRX'] for lab, _, _, P in DATES}
    if key == 'open':
        return dict(kind='twin', title='금 1천만원어치, 지금 얼마?', sub=f'같은 금 · 산 날만 다르다 · {ASOF} KRX 금시장 종가 기준', source=SRC_KRX + ' · ' + PAST,
                    data={'cards': [
                        {'head': '1월 고점에 산 영수증', 'rows': [['산 날', dot(PEAKD), 'in', 0], ['산 값 1g', won(PEAKP) + '원', 'in', 8], ['오늘 1g', won(NOWP) + '원', 'in', 16],
                                                               ['지금 가치', won(K['1년 고점'][0]) + '원', 'net', A('663만원', 20)]], 'big': '663만원', 'bigAt': A('663만원', 30), 'pct': M(K['1년 고점'][1]) + '%'},
                        {'head': '1년 전에 산 영수증', 'rows': [['산 날', dot(D['1년 전'][1]), 'in', A('작년 이맘때', 0)], ['산 값 1g', won(D['1년 전'][2]) + '원', 'in', A('작년 이맘때', 8)],
                                                             ['오늘 1g', won(NOWP) + '원', 'in', A('작년 이맘때', 16)], ['지금 가치', won(K['1년 전'][0]) + '원', 'net', A('956만원', 6)]],
                         'big': '956만원', 'bigAt': A('956만원', 16), 'pct': M(K['1년 전'][1]) + '%'}],
                        'same': A('같은 금인데', 0)})
    if key == 'pick':
        cards = [[f'{"①②③④"[i]}', SHORT[lab], dot(dt) + ' 산 날', A('언제 사셨는지', 10 + 12 * i)] for i, (lab, dt, _, _) in enumerate(DATES)]
        return dict(kind='cards', title='내가 산 날은?', sub='하나만 떠올려 보세요', source=None, data={'cards': cards, 'cycle': True})
    if key == 'road':
        items = ['산 날 영수증 4장', '국제 금값 vs 내 금, 세 조각', '산 길 4개 — 같은 1천만원', '같은 시기에 움직인 숫자', '산 값까지의 산수']
        return dict(kind='road', title='오늘 순서', sub='영수증부터 산수까지', source=None,
                    data={'rows': [[f'{"①②③④⑤"[i]}  {t}', A('오늘은 천만원어치', 8 + 12 * i) if i < 3 else A('그리고 국제 금값', 8 + 12 * (i - 3))] for i, t in enumerate(items)]})
    if key == 'logo':
        return dict(kind='logo', title='', data={'sub': f'금값 1천만원 영수증 · {ASOF} 기준'})
    if key == 'today':
        pts = thin(KRX, 2); vals = [round(v / 1000) for _, v in pts]
        idx = lambda d: next(i for i, (x, _) in enumerate(pts) if x >= d)
        return dict(kind='line', title='오늘 금값 한 장', sub='KRX 금시장 금 1g 값 · 천원', source=SRC_KRX,
                    data={'series': [['KRX 금 1g', 'accent', vals]], 'min': 150, 'max': 290, 'draw': 0, 'xlabels': months(pts),
                          'ticks': [[160, '16만'], [200, '20만'], [240, '24만'], [280, '28만']],
                          'tags': [[len(vals) - 1, vals[-1], f'오늘 {won(NOWP)}원', A('18만원이', 0), 'left', True],
                                   [idx(PEAKD), round(PEAKP / 1000), f'{dot(PEAKD)} {won(PEAKP)}원', A('가장 비쌌던 날', 0), 'up', False]],
                          'callouts': [['고점 대비 ' + M(PEAKPCT) + '%', A('3분의 1쯤', 0), 1300, 300], ['어느 날과 비교하나?', A('어느 날이랑', 0), 1300, 390],
                                       ['→ 내가 산 날 기준', A('그래서 오늘은', 0), 1300, 470]]})
    if key == 'buy':
        pts = thin(KRX, 2); vals = [round(v / 1000) for _, v in pts]
        idx = lambda d: next(i for i, (x, _) in enumerate(pts) if x >= d)
        word = {'1년 전': '첫 번째', '1년 고점': '두 번째는', '3개월 전': '세 번째는', '1개월 전': '네 번째'}
        side = {'1년 전': 'down', '1년 고점': 'right', '3개월 전': 'up', '1개월 전': 'down'}
        tags = [[idx(dt), round(g / 1000), f'{SHORT[lab]} → {won(P["KRX"][0])}원', A(word[lab], 0), side[lab], lab == '1년 고점'] for lab, dt, g, P in DATES]
        return dict(kind='line', title='산 날 영수증 4장', sub=f'1천만원어치를 그날 샀다면, 오늘 팔 때 받는 돈 · 점선 = 오늘 1g {won(NOWP)}원 · ' + NOTFEE, source=SRC_KRX,
                    data={'series': [['KRX 금 1g', 'ink', vals]], 'min': 150, 'max': 290, 'draw': 0, 'dur': 30, 'xlabels': months(pts),
                          'ticks': [[160, '16만'], [200, '20만'], [240, '24만'], [280, '28만']], 'tags': tags,
                          'base': [round(NOWP / 1000), ''], 'callouts': [['네 장 다 손실 · 폭은 4%~34%', A('네 장 다', 0), 1250, 300]]})
    if key == 'range':
        rows = [[SHORT[lab], 10_000_000 - P['KRX'][0], f'{won(P["KRX"][0])}원 ({M(P["KRX"][1])}%)', A('네 장 다', 6 + 8 * i), lab == '1년 고점'] for i, (lab, _, _, P) in enumerate(DATES)]
        return dict(kind='loss', title='네 장 다 손실, 폭은 4%~34%', sub='막대 = 1천만원에서 줄어든 만큼 · 글자 = 오늘 받는 돈', source=SRC_KRX + ' · ' + NOTFEE,
                    data={'rows': rows, 'max': 3_600_000})
    if key == 'odd':
        d = DEC['1년 전']
        return dict(kind='diverge', title='국제 금값은 올랐는데', sub='같은 1년(작년 이맘때 → 오늘) · 늘어난 비율', source=SRC_DEC,
                    data={'rows': [['달러 금값', pc(d['usd']), d['usd'] + '%', A('작년과 비교하면', 0)], ['한국 KRX 금', pc(d['tot']), M(d['tot']) + '%', A('그런데 왜', 0)]],
                          'max': 7, 'q': ['왜?', A('그런데 왜', 10)]})
    if key == 'formula':
        return dict(kind='formula', title='한국 금값 = 세 가지의 곱', sub='세 조각 중 하나만 움직여도 내 금값이 바뀐다', source=SRC_DEC,
                    data={'toks': [['KRX 금값', 0, 'num'], ['=', A('달러로 매긴', 0), 'op'], ['달러 금값', A('달러로 매긴', 0), 'ink'], ['×', A('원/달러 환율', 0), 'op'],
                                   ['환율', A('원/달러 환율', 0), 'ink'], ['×', A('그리고 KRX', 0), 'op'], ['KRX 웃돈', A('그리고 KRX', 0), 'ink']],
                          'subs': ['국제 시세(달러)', '원/달러 매매기준율', 'KRX 금 ÷ 국제값 어림']})
    if key in ('piece1', 'piece1b', 'piece2'):
        lab = '1년 고점' if key == 'piece2' else '1년 전'; d = DEC[lab]
        if key == 'piece1':
            at = [A('첫 조각', 0), A('둘째 조각', 0), 10**9, 10**9]
        elif key == 'piece1b':
            at = [0, 6, 12, A('세 조각을 곱하면', 20)]
        else:
            at = [A('이때는', 0), A('이때는', 20), A('거기에', 0), A('거기에', 30)]
        return dict(kind='pieces', title=f'{SHORT[lab]}에 산 영수증, 세 조각', sub=f'{dot(D[lab][1])} → {dot(ASOF)} · 막대 = 늘어난(줄어든) 비율', source=SRC_DEC,
                    data={'rows': [['달러 금값', pc(d['usd']), d['usd'] + '%', at[0]], ['환율', pc(d['fx']), M(d['fx']) + '%', at[1]],
                                   ['KRX 웃돈', pc(d['prem']), M(d['prem']) + '%', at[2]], ['= 내 금', pc(d['tot']), M(d['tot']) + '%', at[3]]],
                          'max': 34 if key == 'piece2' else 10, 'prem': None if key == 'piece1' else [f'웃돈 그때 {M(d["p0"])}% → 지금 {M(d["p1"])}%', 0 if key == 'piece1b' else A('거기에', 0)],
                          'note': None if key == 'piece1' else ['금값이 아니라 환율·웃돈에서 잃었다' if key == 'piece1b' else '달러 금값 자체가 빠졌다', A('그러니까' if key == 'piece1b' else '이때는', 0)]})
    if key == 'prem':
        d = DEC['1년 전']
        return dict(kind='diverge', title='KRX 웃돈 — 국제값보다 얼마나 비쌌나', sub='KRX 금 ÷ (금 선물 × 매매기준율) − 1 · 어림', source=SRC_DEC,
                    data={'rows': [[f'그때 {dot(D["1년 전"][1])}', pc(d['p0']), M(d['p0']) + '%', A('작년엔', 0)], [f'지금 {dot(ASOF)}', pc(d['p1']), M(d['p1']) + '%', A('지금은 오히려', 0)]],
                          'max': 8, 'q': [f'웃돈 변화 {M(d["prem"])}%', A('이 웃돈이 빠진', 0)]})
    if key == 'grid':
        rows = [[SHORT[lab], [M(DEC[lab]['usd']) + '%', M(DEC[lab]['fx']) + '%', M(DEC[lab]['prem']) + '%', M(DEC[lab]['tot']) + '%'],
                 A(w, 0) if w else 0] for lab, w in [('1년 전', None), ('1년 고점', None), ('3개월 전', '3개월 전은'), ('1개월 전', '한 달 전은')]]
        big = lambda lab: max(range(3), key=lambda i: abs(pc([DEC[lab]['usd'], DEC[lab]['fx'], DEC[lab]['prem']][i])))
        return dict(kind='grid', title='산 날마다 깎인 이유가 다르다', sub='세 조각 · 가장 크게 깎인 칸에 표시', source=SRC_DEC,
                    data={'cols': ['달러 금값', '환율', 'KRX 웃돈', '내 금'], 'rows': rows,
                          'hot': [[0, big('1년 전'), 0], [1, big('1년 고점'), 0], [2, big('3개월 전'), A('3개월 전은', 20)], [3, big('1개월 전'), A('한 달 전은', 20)]]})
    if key == 'paths':
        return dict(kind='cards', title='같은 1천만원, 산 길 4개', sub='길마다 세금·수수료가 다르다', source=SRC_LAW,
                    data={'cards': [['①', 'KRX 금시장', '증권사 계좌 · 1g 단위', A('KRX 금시장', 0)], ['②', '금 ETF', '주식처럼 사고팜', A('금 ETF', 0)],
                                    ['③', '골드뱅킹', '은행 통장 · 0.01g', A('골드뱅킹', 0)], ['④', '골드바', '실물 · 금은방·은행', A('골드바', 0)]]})
    if key == 'krx':
        return dict(kind='law', title='① KRX 금시장 — 세금', sub='사고팔 때 부가세 없음 · 판 차익에 양도세 없음 · 실물로 찾으면 10%', source=SRC_LAW,
                    data={'head': 'KRX 금시장 · 세금 영수증', 'rows': [['부가가치세', '면제', 'in', A('부가가치세가 면제', 0)], ['조특법 제126조의7①', '금 현물시장 매매', 'dim', A('부가가치세가 면제', 16)],
                                                                    ['판 차익 양도세', '없음', 'in', A('양도소득세도', 0)], ['소득세법 제94조', '목록에 금 없음', 'dim', A('양도소득세도', 24)],
                                                                    ['실물로 찾을 때', '부가세 10%', 'tax', A('실물로 찾아가는', 0)]],
                          'side': ['세금 0', A('부가가치세가 면제', 10), '사고파는 동안']})
    if key == 'etf':
        e = D['1년 전'][3]['ETF']
        return dict(kind='law', title='② 금 ETF', sub='ACE KRX금현물(411060) · 작년 이맘때 샀다면', source='야후 파이낸스 종가 · ' + SRC_LAW,
                    data={'head': '금 ETF · 1천만원 · 단위 원', 'rows': [['오늘 받는 돈', won(e[0]), 'net', A('두 번째는', 10)], ['KRX 금이었다면', won(D['1년 전'][3]['KRX'][0]), 'dim', A('두 번째는', 30)],
                                                                    ['차익 세금', '15.4%', 'tax', A('ETF는 차익', 0)], ['손실이면', '세금 0', 'in', A('ETF는 차익', 30)],
                                                                    ['이자·배당 합계 2천만원 넘으면', '종합과세', 'hi', A('이자와 배당이', 0)]],
                          'side': [M(e[1]) + '%', A('두 번째는', 20), '1년 전에 산 금 ETF']})
    if key == 'bank':
        return dict(kind='spread', title='③ 골드뱅킹 — 살 때 +1%, 팔 때 −1%', sub='은행 고시 규칙 · 기준가격 = 국제 금가격 × 환율 ÷ 31.1034768', source='KB국민은행 골드뱅킹 고시 규칙 · 소득세법 제17조①5의2호',
                    data={'mid': A('세 번째는', 0), 'buy': A('살 때는', 0), 'sell': A('팔 때는', 0), 'gap': A('사고팔기만', 0), 'tax': A('사고팔기만', 30), 'stamp': A('은행 고시값은', 0)})
    if key == 'bar':
        return dict(kind='split', title='④ 골드바 — 출발선이 뒤에 있다', sub='1천만원을 내면 그중 부가세 10%', source='부가가치세법 제30조 · 파이어맵 계산',
                    data={'vat': won(VAT) + '원', 'gold': won(GOLDPART) + '원', 'ratio': VAT / 10_000_000, 'at': A('네 번째는', 0), 'vatAt': A('91만원이', 0),
                          'need': ['금값이 +10% 올라야 낸 돈만큼', A('그래서 금값이', 0)], 'fee': ['살 때 수수료·팔 때 값 차이 별도', A('살 때 붙는', 0)]})
    if key == 'pathcmp':
        P = D['1년 전'][3]
        rows = [[n, 10_000_000 - P[k][0], f'{won(P[k][0])}원 ({M(P[k][1])}%)', A(w, 0), k == 'BAR'] for n, k, w in
                [('KRX 금시장', 'KRX', '같은 날 같은 돈'), ('금 ETF', 'ETF', '같은 날 같은 돈'), ('골드바', 'BAR', '작년에 골드바로')]]
        rows[0][3] = A('같은 날 같은 돈', 0); rows[1][3] = A('같은 날 같은 돈', 10)
        rows = [rows[2], rows[0], rows[1]]
        return dict(kind='loss', title='작년에 산 1천만원, 길에 따라', sub='막대 = 1천만원에서 줄어든 만큼 · 골드바는 금값 몫만 · 골드뱅킹은 고시 확인 전이라 뺌', source=SRC_KRX + ' · 부가가치세법 제30조',
                    data={'rows': rows, 'max': 1_500_000, 'gap': [f'KRX − 골드바 {won(P["KRX"][0] - P["BAR"][0])}원', A('길에 따라', 0)]})
    if key == 'up10':
        return dict(kind='bars', title='금값이 10% 오르면 남는 차익', sub='가정 · 1천만원 · ETF는 차익 전부 15.4%로 어림', source=SRC_LAW,
                    data={'max': 1_150_000, 'bars': [['KRX 금시장', 1_000_000, '1,000,000원', A('KRX는', 0), 'accent', '세금 0'], ['금 ETF', 846_000, '846,000원', A('ETF는 세금을', 0), 'ink', '세금 154,000원']]})
    if key == 'ust':
        pts = thin(UST, 2); vals = [v for _, v in pts]
        return dict(kind='line', title='미국 10년 국채 금리', sub='% · 같은 시기에 움직인 숫자(원인 단정 아님)', source='미 재무부 Daily Treasury Par Yield Curve 10 Yr',
                    data={'series': [['10년 금리', 'ink', vals]], 'min': 3.8, 'max': 5.5, 'draw': 0, 'xlabels': months(pts),
                          'ticks': [[4.0, '4.0%'], [4.5, '4.5%'], [5.0, '5.0%'], [5.5, '5.5%']],
                          'tags': [[next(i for i, (d, _) in enumerate(pts) if d >= '2025-10-02'), 4.10, '25.10.02 4.10%', A('작년 이맘때', 0), 'down', False],
                                   [len(vals) - 1, 5.31, '26.10.05 5.31% · 1년 최고', A('미국 장기', 10), 'left', True]]})
    if key == 'fxl':
        pts = thin(FXS, 2); vals = [v for _, v in pts]
        return dict(kind='line', title='원/달러 환율', sub='원 · 매매기준율', source='한국은행 ECOS 731Y001',
                    data={'series': [['원/달러', 'ink', vals]], 'min': 1300, 'max': 1600, 'draw': 0, 'xlabels': months(pts),
                          'ticks': [[1350, '1,350'], [1450, '1,450'], [1550, '1,550']],
                          'tags': [[next(i for i, (d, _) in enumerate(pts) if d >= '2026-07-02'), 1554.4, '26.07.02 1,554.4원', A('환율은 여름에', 10), 'up', False],
                                   [len(vals) - 1, 1358.5, f'{dot(ASOF)} 1,358.5원', A('환율은 여름에', 40), 'left', True]]})
    if key == 'bok':
        need('「한국은행, 국내 생산 금 매입 협력 체계 구축」', '"국내생산금에대한실제매입시기는 … 종합적으로 고려하여 결정할 예정"')
        return dict(kind='quote', title='한국은행 보도자료', sub='2026년 8월 3일 · 국내에서 생산된 금을 사들일 길', source='한국은행 보도자료 2026-08-03(공보 2026-8-7호)',
                    data={'src': '한국은행 보도자료 · 2026.08.03', 'body': '「한국은행, 국내 생산 금 매입 협력 체계 구축」', 'big': '언제·얼마나 = 원문에 없음',
                          'q2': '"실제매입시기는 … 종합적으로 고려하여 결정할 예정"', 'at': 0, 'q2At': A('다만 언제', 0), 'bigAt': A('다만 언제', 30)})
    if key == 'wgc':
        need('"adding US$18bn"', 'record high of 4,189t')
        return dict(kind='count', title='세계 금 ETF로 들어온 돈', sub='2026년 8월 한 달 · 세계금협회(WGC) 9월 9일 자료', source='World Gold Council, Gold ETF holdings and flows 2026-09-09',
                    data={'from': 0, 'to': 18, 'text': 'US$18bn', 'label': '8월 순유입', 'start': A('세계금협회', 10), 'pre': '180억 달러',
                          'tag': ['보유량 4,189t · 사상 최대', A('보유량은', 0)], 'call': ['고점이 지난 뒤에도 들어옴', A('고점이 지난', 0)]})
    if key == 'nocause':
        return dict(kind='stamps', title='무엇이 얼마나 움직였나?', sub='네 가지 모두 원문에 기여도 숫자가 없다', source=PAST,
                    data={'cards': [['금리', '미 10년 5.31%', A('금리, 환율', 0)], ['환율', '1,358.5원', A('금리, 환율', 8)], ['중앙은행', '시기·물량 미정', A('금리, 환율', 16)], ['ETF', 'US$18bn 유입', A('금리, 환율', 24)]],
                          'stamp': ['기여도 숫자 없음', A('원문 어디에도', 0)], 'no': ['전망은 말하지 않습니다', A('그래서 앞으로', 0)]})
    if key == 'math':
        return dict(kind='asym', title='산 값까지의 산수', sub=f'1월 고점에 산 금 · 1g {won(NOWP)}원 → {won(PEAKP)}원', source=SRC_KRX + ' · 전망 아님, 산수',
                    data={'down': [abs(pc(PEAKPCT)), M(PEAKPCT) + '%', A('34% 떨어진', 0)], 'up': [float(BACK), '+' + BACK + '%', A('고점에 산 금이', 0)],
                          'from': NOWP, 'to': PEAKP, 'start': A('고점에 산 금이', 0), 'note': ['떨어진 만큼만 올라서는 모자란다', A('떨어진 만큼만', 0)],
                          'fee': ['수수료·팔 때 값 차이는 뺀 숫자', A('이것도', 0)]})
    if key == 'sum':
        return dict(kind='law', title='정리 — 금 1천만원 영수증 4장', sub=f'{ASOF} 기준 · KRX 금시장 · ' + NOTFEE, source=SRC_KRX + ' · ' + PAST,
                    data={'head': '오늘 팔면 받는 돈', 'rows': [[f'{SHORT[lab]} ({dot(dt)})', won(P['KRX'][0]), 'net' if lab == '1년 고점' else 'in', A('작년에 샀다면', 10 * i)] for i, (lab, dt, _, P) in enumerate(DATES)],
                          'side': ['산 날이 갈랐다', A('작년에 산 분은', 0), '같은 날이라도 골드바는 부가세만큼 뒤']})
    if key == 'end':
        return dict(kind='end', title='전체 표는 카페 글에', sub='산 날 4 × 산 길 4 · 설명란 링크', source=PAST,
                    data={'text': '산 날 4 × 산 길 4', 'label': '전체 영수증 표', 'note': '설명란의 카페 글', 'start': A('산 날 네 개', 0)})
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
        d = spec(key, None, A)
        frames = sum(x['frames'] for x in out) if out else 72
        if key == 'end': frames = max(frames, END_MIN)
        scenes.append({'key': key, 'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub'), 'source': d.get('source'),
                       'chapter': None if ch in ('0.', '로고') else ch.rstrip('.').split('-')[0] + '장', 'data': d['data'], 'lines': out, 'frames': frames})
    n_lines = sum(len(s['lines']) for s in secs)
    assert n_lines == sum(len(s['lines']) for s in scenes), f'빠진 문장: 대본 {n_lines} vs 장면 {sum(len(s["lines"]) for s in scenes)}'
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'script': script, 'rate': RATE, 'asof': ASOF}
    json.dump(res, open(os.path.join(VID, 'g1.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = sum(s['frames'] for s in scenes) / FPS
    print(f'기준일 {ASOF} · 장면 {len(scenes)} · 길이 {tot / 60:.2f}분 · 말 {n_lines}줄 · 목소리 없는 문장 {missing} · 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})}')
    for s in scenes: print(f"  {s['key']:8} {s['kind']:8} {s['frames'] / FPS:6.1f}초 문장{len(s['lines']):3}  {s['title']}")
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[a.index('--script') + 1] if '--script' in a else 'script.md')
