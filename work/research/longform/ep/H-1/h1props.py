# H-1 화면 재료 — script.md(장·말 줄·[자막]) + voice.json(줄 길이·소리) + calc_out.txt·facts.txt·raw/tour_*.json → work/video/h1.json (Remotion H1이 읽는다)
#   py -3.12 work/research/longform/ep/H-1/h1props.py
# 장면은 줄 번호가 아니라 '그 장에서 이 말이 처음 나오는 줄'(ANCHOR)로 자른다 — 대본 줄이 늘거나 줄어도 장면 배치가 따라간다(10/13 PD: 줄 번호·글자 하드코딩 금지).
#   장 안에서 찾은 장면들을 줄 위치 순으로 정렬하고, 못 찾은 장면은 뺀다(경고만). 장면 안 박자는 줄 순서(k)로 넘어간다.
# 장면 길이 = 목소리 길이(voice.json frames, 빠르기 1.0). 목소리가 없는 줄은 5.65음절/초 어림 + missing으로 센다(렌더는 missing 0일 때만).
# 숫자: 화면 글자 숫자는 calc_out.txt·facts.txt 문구 그대로(need로 기계 대조), 점·선·막대 위치는 raw/tour_*.json 원자료·calc_out 파싱 값.
import json, os, re, sys, math
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
RATE, FPS = 5.65, 30
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
FACTS = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
def need(*ss):
    for s in ss: assert s in CALC or s in FACTS, f'calc_out·facts에 없는 글: {s}'

# ───────── 숫자(calc_out·facts 원문 대조) ─────────
need('9,510세대', '12,032세대', '4,932세대', '3,658세대', '807세대', '2,064세대', '2018.12', '2024.11', '2019.09', '2016.12', '1996.03', '1997.03')
need('11,087만원(84건)', '8,080', '11,017', '9,457', '7,865', '5,937', '−0.6%', '-27.1%', '-37.2%', '-47.0%', '+20.2%')
need('84㎡대 매매 85건 중앙 28.50억', '신규 순수전세 132건 중앙 12.50억', '신규 순수전세 35건 중앙 14.00억', '전세가율 49.6%', '전세가율 43.9%', '전세가율 41.5%')
need('송파역 출입구 360m', '서울가락초등학교 660m', '둔촌오륜역 출입구 430m', '서울위례초등학교 270m', '상일동역 출입구 180m', '고덕역 출입구 640m',
     '서울고덕초등학교 390m', '서울묘곡초등학교 600m', '이마트 1170m', '이마트 960m', '롯데마트 1400m')
need('1년 113건 · 4~5월 94건(83%) · 2025.11~2026.03 1건 · 6~10월 18건', '84㎡대만: 1년 45건 · 4~5월 34건(76%)', '보증금 9.50억')
need('고덕아남(원자료 이름 \'아남1\'): 1996.03 입주 · 807세대 · 84㎡대 매매 40건 중앙 15.20억')

def monthly_median(name):
    blk = CALC.split(f'- {name}(', 1)[1].split('\n- ', 1)[0]
    return [[ym, float(v), int(n)] for ym, v, n in re.findall(r'(\d{4}\.\d{2}) ([\d.]+)억\((\d+)건\)', blk.split('달별 중앙', 1)[1])]
MED = {'helio': monthly_median('헬리오시티'), 'forest': monthly_median('올림픽파크포레온'), 'gra': monthly_median('고덕 그라시움')}
assert MED['helio'][5] == ['2026.04', 28.0, 25] and MED['forest'][0] == ['2026.04', 27.55, 9] and ['2026.04', 18.85, 19] in MED['gra']

def dong_months(d):
    m = re.search(rf'- {d} 동 전체: 1년 (\d+)건 · 4~5월 (\d+)건\(\d+%\) · 달별 (.+)', CALC)
    xs = re.findall(r'(\d\d\.\d\d) (\d+)', m.group(3))
    assert sum(int(n) for _, n in xs) == int(m.group(1)), d
    end = re.search(rf'{d}: 기간 2025\.11 ~ (\d{{4}}\.\d\d)', CALC).group(1)      # 동마다 자료 마지막 달(calc_out 1: 가락 2026.10, 둔촌·고덕 2026.09)
    ms = [['20' + ym, int(n)] for ym, n in xs if '20' + ym <= end]
    assert sum(n for _, n in ms) == int(m.group(1)), d
    return {'total': int(m.group(1)), 'spring': int(m.group(2)), 'months': ms}
DONGV = {d: dong_months(d) for d in ['가락동', '둔촌동', '고덕동']}

def deals_of(head):
    line = CALC.split(head, 1)[1].split('\n', 1)[0]
    return [dict(d=int(a), amt=float(b), floor=int(c), kind=k, rg=r.strip()) for a, b, c, k, r in
            re.findall(r'(\d+)일 ([\d.]+)억 (\d+)층 (중개거래|직거래) (?:등기 )?([\d.]+|등기 칸 비어 있음)', line)]
FEB = deals_of('- 헬리오시티 2026.02 84㎡대 4건:'); MAY = deals_of('- 헬리오시티 2026.05 84㎡대 18건:'); SEP = deals_of('- 올림픽파크포레온 2026.09 84㎡대 2건:')
assert len(FEB) == 4 and len(MAY) == 18 and len(SEP) == 2, (len(FEB), len(MAY), len(SEP))
GAP = {m.group(1): (float(m.group(2)), float(m.group(3)), float(m.group(4)))
       for m in re.finditer(r'- (\S+) 84㎡ 매매 중앙 ([\d.]+)억 − 보증금 = 더 필요한 돈 ([\d.]+)억 · 그 단지 84㎡ 전세 중앙 ([\d.]+)억', CALC)}
assert GAP['래미안힐스테이트고덕'][1] == 10.7 and GAP['헬리오시티'][1] == 19.0 and GAP['아남1'][2] == 5.3

def tour(n): return json.load(open(os.path.join(EP, 'raw', f'tour_{n}.json'), encoding='utf-8'))
TOUR = {'garak': tour('garak'), 'dunchon': tour('dunchon'), 'godeok': tour('godeok')}
def cx(dong, name): return next(c for c in TOUR[dong]['complexes'] if c['name'] == name)
HELIO, FOREST = cx('garak', '헬리오시티'), cx('dunchon', '올림픽파크포레온')
for d in FEB: assert any(x['ym'] == '2026.02' and x['d'] == d['d'] and x['amt'] == round(d['amt'] * 10000) and int(x['floor']) == d['floor'] for x in HELIO['deals']), d
assert sum(1 for x in HELIO['deals'] if x['ym'] == '2026.05') == 18 and len(HELIO['deals']) == 85
FOREST_MONTHS = {}
for x in FOREST['deals']: FOREST_MONTHS[x['ym']] = FOREST_MONTHS.get(x['ym'], 0) + 1
assert sum(FOREST_MONTHS.values()) == 45 and FOREST_MONTHS['2026.04'] + FOREST_MONTHS['2026.05'] == 34

# ───────── 지도(세 동네 한 좌표계, 미터, 원점 = 헬리오시티) ─────────
LAT0, LON0 = HELIO['lat'], HELIO['lon']
def P(lon, lat): return [round((lon - LON0) * math.cos(math.radians(LAT0)) * 111320), round((LAT0 - lat) * 110540)]
def flat(pts): return [v for q in pts for v in P(q[0], q[1])]
RW = {'motorway': 7, 'trunk': 7, 'primary': 7, 'secondary': 5, 'tertiary': 4}
DONG = {'garak': '가락동', 'dunchon': '둔촌동', 'godeok': '고덕동'}
SHORT = {'고덕 그라시움': '고덕그라시움', '래미안힐스테이트 고덕': '래미안힐스테이트고덕'}
def walk(w): return None if not w else {'name': w['name'], 'm': w['m'], 'pts': flat(w['route']), 'end': P(w['lon'], w['lat'])}
MAPS = {}
for k, t in TOUR.items():
    MAPS[k] = {'name': DONG[k],
               'roads': [[RW.get(r['k'], 2), flat(r['pts'])] for r in t['bg']['roads']],
               'parks': [flat(q) for q in t['bg']['parks']], 'blocks': [flat(q) for q in t['bg']['others']],
               'stations': [[s['name'], *P(s['lon'], s['lat'])] for s in t['stations'] if not re.search(r'\d', s['name'])],
               'cx': [{'name': SHORT.get(c['name'], c['name']), 'poly': [flat(q) for q in c['poly']], 'c': P(c['lon'], c['lat']), 'ppy': c['ppyTop'], 'built': int(c['built']),
                       'walk': {w: walk(c['walk'][w]) for w in ['station', 'school', 'mart']}} for c in t['complexes']]}
CXALL = {c['name']: (k, c) for k, m in MAPS.items() for c in m['cx']}
MW, MH = 1060, 540
def view(names, pad=1.35, minw=900, extra=()):
    pts = []
    for n in names:
        c = CXALL[n][1]; pts += [p for q in c['poly'] for p in zip(q[0::2], q[1::2])]
    pts += list(extra)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w = max(minw, (max(xs) - min(xs)) * pad, (max(ys) - min(ys)) * pad * MW / MH)
    return {'cx': (max(xs) + min(xs)) / 2, 'cy': (max(ys) + min(ys)) / 2, 'w': round(w)}
def wpts(n, kinds):
    c = CXALL[n][1]; out = []
    for k in kinds:
        w = c['walk'].get(k)
        if w: out += list(zip(w['pts'][0::2], w['pts'][1::2]))
    return out
def dongview(k, pad=1.08):
    xs = [v for c in MAPS[k]['cx'] for q in c['poly'] for v in q[0::2]]; ys = [v for c in MAPS[k]['cx'] for q in c['poly'] for v in q[1::2]]
    return view([], pad, 1200, extra=[(min(xs), min(ys)), (max(xs), max(ys))])
ALLV = view([], 1.12, 1200, extra=[(x, y) for k in MAPS for c in MAPS[k]['cx'] for x, y in [c['c']]])

SRC_RT = '국토교통부 아파트 매매·전월세 실거래(2025.11~2026.10 계약, 2026-10-11 받음)'
SRC_MAP = SRC_RT + ' · 공동주택 단지 정보 · 지도·보행로 © OpenStreetMap contributors(ODbL)'
SRC_KAPT = SRC_RT + ' · 국토교통부 공동주택 단지 정보'
PPY = '전용면적 3.3058㎡를 1평으로 계산'
def eok(v): return f'{v:.2f}억'

def deal_dots(c):
    return [[x['ym'], x['d'], x['amt'], int(x['floor']), 1 if x['odd'] else 0] for x in c['deals']]

# ───────── 장면 규칙: (키, 종류, 장 번호, 이 말이 처음 나오는 줄부터 — None = 장 첫 줄) ─────────
RULES = [
    ('t_dots', 'dots', '0.', ('7억',)), ('t_person', 'person', '0.', ('손품 씨',)), ('t_bars', 'bars', '0.', ('6년',)),
    ('t_period', 'period', '0.', ('80%',)), ('t_map', 'map', '0.', ('갈렸',)), ('concl', 'concl', '0.', ('결론부터',)),
    ('person', 'person', '1.', None), ('map3', 'map', '1.', ('송파구 가락동', '세 동네')), ('tiles', 'tiles', '1.', ('국토교통부',)),
    ('h_map', 'map', '2.', None), ('h_dots', 'dots', '2.', ('줄 세웠', '가운데 값은 거래')), ('h_deal', 'deal', '2.', ('등기까지',)),
    ('h_floor', 'floors', '2.', ('층이 달랐',)), ('h_may', 'dots', '2.', ('봄에는',)), ('h_line', 'line', '2.', ('달마다',)),
    ('h_walk', 'map', '2.', ('송파역',)), ('h_ssmap', 'map', '2.', ('가락쌍용1차',)), ('h_ssbar', 'bars', '2.', ('27%',)),
    ('f_map', 'map', '3.', None), ('f_bars', 'bars', '3.', ('6년',)), ('f_cal', 'cal', '3.', ('몰려 있었', '이상한 점')),
    ('f_period', 'period', '3.', ('80%',)), ('f_deal', 'deal', '3.', ('가을',)), ('f_rent', 'rent', '3.', ('전세였', '전세 가운데')),
    ('f_walk', 'map', '3.', ('둔촌오륜',)),
    ('g_map', 'map', '4.', None), ('g_ruler', 'walk', '4.', ('세 배',)), ('g_bars', 'bars', '4.', ('20%',)), ('g_walk2', 'walk', '4.', ('학교 길', '초등학교까지')),
    ('g_cards', 'cards', '4.', ('그렇다고', '지은 해도')), ('g_anam', 'map', '4.', ('고덕아남은',)), ('g_diff', 'diff', '4.', ('갈렸',)),
    ('s_lines', 'line', '5.', None), ('s_vol', 'vol', '5.', ('동 전체',)), ('s_deadline', 'deadline', '5.', ('신고 기한',)),
    ('gap1', 'gap', '6.', None), ('gap2', 'gap', '6.', ('전세로만',)), ('sheet', 'table', '6.', ('표 한 장',)),
    ('e_map', 'map', '7.', None), ('e_table', 'table', '7.', ('37곳', '카페')),
]
CH_NAME = {'0.': None, '1.': '1장', '2.': '2장', '3.': '3장', '4.': '4장', '5.': '5장', '6.': '6장', '7.': '7장'}
END_MIN = 20 * FPS   # 끝 화면 자리(마지막 장면 20초 이상, R-1과 같음)


def spec(key, lines):
    """장면 하나의 제목·부제·출처·data. lines = 그 장면 말 줄(글자) — 박자는 TSX가 줄 순서로 넘긴다."""
    has = lambda w: next((i for i, t in enumerate(lines) if w in t), -1)
    if key == 't_dots':
        return '같은 달, 같은 단지, 같은 평형', '헬리오시티 84㎡대 · 1년 거래 85건 · 점 하나 = 거래 하나', SRC_RT, {'dots': deal_dots(HELIO), 'mode': 'feb', 'feb': FEB, 'gap': '같은 달 최고 − 최저 7.68억'}
    if key in ('t_bars', 'f_bars'):
        need('입주: 헬리오시티 2018.12 · 올림픽파크포레온 2024.11')
        return '6년 가까이 늦게 지었는데', '84㎡대 평당 값 · 1년 가운데 값 · ' + PPY, SRC_KAPT, {
            'bars': [['헬리오시티', 11087, '1억 1,087만원', '2018.12 입주', 'ink'], ['올림픽파크포레온', 11017, '1억 1,017만원', '2024.11 입주', 'accent']],
            'max': 12000, 'diff': '차이 −0.6%', 'note': '매매 가운데 값 28.50억 vs 28.25억'}
    if key == 't_period' or key == 'f_period':
        return '봄 두 달에 몰린 거래', '올림픽파크포레온 · 모든 평형 매매 113건 · 해제·공공기관 매수 제외', SRC_RT, {
            'bars': [['2025.11~2026.03', 1, '1건', '다섯 달'], ['2026.04~05', 94, '94건', '두 달'], ['2026.06~10', 18, '18건', '다섯 달']],
            'hot': 1, 'pct': '113건 중 94건(83%)', 'why': '왜 몰렸는지는 실거래 자료에 없음', 'sub84': '84㎡대만 보면 45건 중 34건(76%)'}
    if key == 't_map' or key == 'g_anam':
        need('고덕 그라시움(2019.09) 9,457(25건) vs 고덕아남(1996.03) 5,937(39건) → -37.2%')
        return ('같은 동네, 지은 해가 다른 단지' if key == 't_map' else '같은 동네의 오래된 단지'), '고덕동 · 84㎡대 평당 값(1년 가운데 값) · ' + PPY, SRC_MAP, {
            'views': [view(['고덕그라시움', '고덕아남'], 1.3)], 'focus': ['고덕그라시움', '고덕아남'], 'color': 'ppy',
            'cards': [['고덕그라시움', '2019.09 입주 · 4,932세대', '9,457만원'], ['고덕아남', '1996.03 입주 · 807세대', '5,937만원'], ['차이', '그라시움보다 −37.2%', '고덕아남 매매 가운데 15.20억']]}
    if key in ('t_person', 'person'):
        need('40대 직장인 · 초등학생 아이 하나 · 래미안힐스테이트고덕 84㎡ 전세 · 보증금 9.50억')
        return ('전세 만기를 앞둔 손품 씨' if key == 't_person' else '오늘 같이 다닐 사람, 손품 씨'), '가상 인물 · 계산을 위해 만든 사람(실존 인물 아님)', SRC_RT, {
            'tags': ['40대 직장인', '초등학생 아이 하나', '지하철 출근'], 'home': ['지금 사는 곳', '래미안힐스테이트고덕 84㎡대 전세'],
            'deposit': ['보증금', '9억 5천만원', '같은 평형 신규 전세 65건의 가운데 값'], 'dday': '전세 만기 D-90',
            'dongs': ['가락동', '둔촌동', '고덕동'], 'rules': ['같은 평형 값', '전세로 계속 살 때 드는 돈', '아이 걸음으로 학교·역까지'],
            'teaser': key == 't_person', 'promise': ['1년 치 거래 전부', '단지마다 더 드는 돈']}
    if key == 'concl':
        return '결론부터', '1년 치를 전부 깔아 놓고 본 세 동네', SRC_RT, {'rows': ['한 건이 아니라 1년 전부를 본다', '헬리오시티·포레온, 평당 값 거의 같음', '같은 동네라도 지은 해 따라 크게 갈림']}
    if key == 'map3':
        return '세 동네를 지도로', '송파구 가락동 · 강동구 둔촌동 · 강동구 고덕동 · 대표 단지는 주황', SRC_MAP, {
            'views': [ALLV], 'focus': ['헬리오시티', '올림픽파크포레온', '고덕그라시움'], 'color': 'focus', 'dongLabels': True,
            'cards': [['가락동', '헬리오시티', '송파구'], ['둔촌동', '올림픽파크포레온', '강동구'], ['고덕동', '고덕그라시움 · 손품 씨네 동네', '강동구']]}
    if key == 'tiles':
        need('매매 596건', '343건', '277건', '84㎡대(80~85㎡)')
        return '무엇으로 쟀나', '국토교통부 실거래 1년 · 오픈스트리트맵 보행로 · 84㎡대 하나', SRC_MAP, {
            'tiles': [['가락동', '596건'], ['둔촌동', '343건'], ['고덕동', '277건']], 'tilesHead': '1년 매매(해제·공공기관 매수 제외)',
            'walk': {'views': [view(['헬리오시티'], 1.6, 900, wpts('헬리오시티', ['station']))], 'focus': ['헬리오시티'], 'routes': [['헬리오시티', 'station']]},
            'walkNote': ['직선거리가 아니라', '실제 걷는 길로 잰 거리'], 'size': ['84㎡대', '전용 80~85㎡ · 국민평형']}
    if key == 'h_map':
        return '첫 동네, 송파구 가락동', '헬리오시티 · 9,510세대 · 2018.12 입주', SRC_MAP, {
            'views': [dongview('garak'), view(['헬리오시티'], 1.8, 1100)], 'focus': ['헬리오시티'], 'color': 'focus',
            'cards': [['헬리오시티', '9,510세대 · 2018.12 입주', ''], ['84㎡대 매매', '1년 85건', '2025.11~2026.10 계약'], ['가운데 값', '28.50억', '최저 20.00억 · 최고 31.50억']]}
    if key == 'h_dots':
        return '헬리오시티 84㎡대, 1년 거래 85건', '점 하나 = 거래 하나 · 2025.11~2026.10 계약', SRC_RT, {'dots': deal_dots(HELIO), 'mode': 'sort', 'feb': FEB, 'gap': '같은 달 최고 − 최저 7.68억', 'median': 28.5}
    if key == 'h_deal':
        d = FEB[0]
        return '23.82억 거래 한 건', '헬리오시티 84㎡대 · 국토교통부 실거래 원자료 칸 그대로', SRC_RT, {'cards': [[
            ['계약일', '2026.02.12'], ['층', f"{d['floor']}층"], ['거래금액', eok(d['amt'])], ['거래 유형', d['kind']], ['등기일', '2026.04.14']]], 'hot': [[2, 3, 4]]}
    if key == 'h_floor':
        return '같은 달 4건, 층과 값', '헬리오시티 84㎡대 · 2026년 2월 계약 · 모두 중개거래', SRC_RT, {
            'deals': [[d['floor'], eok(d['amt']), f"{d['d']}일"] for d in FEB], 'top': 35, 'why': ['왜 이 값이었는지', '실거래 자료에는 나오지 않음']}
    if key == 'h_may':
        return '봄에는 20억 거래도', '헬리오시티 84㎡대 · 2026년 5월 계약 18건', SRC_RT, {'dots': deal_dots(HELIO), 'mode': 'may', 'may': MAY,
            'band': '나머지 17건 27.00~30.50억 · 모두 중개거래', 'def': ['직거래', '중개사 없이 사고판 사람이 직접 신고한 거래']}
    if key == 'h_line':
        return '달마다 가운데 값을 이으면', '헬리오시티 84㎡대 · 동떨어진 거래 1건 뺌 · 단위 억원', SRC_RT, {
            'series': [['헬리오시티 84㎡대', 'accent', MED['helio']]], 'min': 26, 'max': 32, 'band': None}
    if key == 'h_walk':
        return '걸어서 재 보면', '헬리오시티 가운데 → 출입구·학교·마트 · 오픈스트리트맵 보행로', SRC_MAP, {
            'views': [view(['헬리오시티'], 1.4, 1200, wpts('헬리오시티', ['station', 'school']))], 'focus': ['헬리오시티'], 'color': 'focus',
            'routes': [['헬리오시티', 'station'], ['헬리오시티', 'school']],
            'cards': [['송파역 출입구', '360m', '역'], ['서울가락초등학교', '660m', '초등학교'], ['롯데마트', '1,400m', '마트'], ['가장 가까운 학교가', '꼭 다니게 될 학교는 아님', '배정 학교 확인 안 함']]}
    if key == 'h_ssmap':
        return '같은 가락동, 오래된 단지', '가락쌍용1차 · 2,064세대 · 1997.03 입주', SRC_MAP, {
            'views': [view(['헬리오시티', '가락쌍용1차'], 1.35)], 'focus': ['헬리오시티', '가락쌍용1차'], 'color': 'focus',
            'cards': [['가락쌍용1차', '2,064세대 · 1997.03 입주', ''], ['헬리오시티', '9,510세대 · 2018.12 입주', '']]}
    if key == 'h_ssbar':
        return '같은 평형 평당 값', '가락동 · 84㎡대 평당 값(1년 가운데 값) · ' + PPY, SRC_KAPT, {
            'bars': [['헬리오시티', 11087, '1억 1,087만원', '84건 · 2018.12', 'ink'], ['가락쌍용1차', 8080, '8,080만원', '29건 · 1997.03', 'accent']], 'max': 12000, 'diff': '−27.1%'}
    if key == 'f_map':
        return '두 번째 동네, 강동구 둔촌동', '올림픽파크포레온 · 12,032세대 · 2024.11 입주', SRC_MAP, {
            'views': [dongview('dunchon'), view(['올림픽파크포레온'], 1.4, 1200)], 'focus': ['올림픽파크포레온'], 'color': 'focus',
            'cards': [['올림픽파크포레온', '12,032세대 · 2024.11 입주', ''], ['헬리오시티보다 큰 단지', '12,032세대 vs 9,510세대', '']]}
    if key == 'f_cal':
        months = [f'{y}.{m:02d}' for y, m in [(2025, 11), (2025, 12)] + [(2026, i) for i in range(1, 10)]]   # 둔촌동 자료는 2026.09 거래까지(calc_out 1)
        return '거래가 한쪽에 몰렸다', '올림픽파크포레온 84㎡대 · 달마다 매매 건수(1년 45건)', SRC_RT, {'cells': [[m, FOREST_MONTHS.get(m, 0)] for m in months], 'note': '4~5월 34건(76%)'}
    if key == 'f_deal':
        cards = [[['계약일', f"2026.09.{d['d']:02d}"], ['층', f"{d['floor']}층"], ['거래금액', eok(d['amt'])], ['거래 유형', d['kind']], ['등기', '칸 비어 있음']] for d in SEP]
        return '가을의 23억 거래', '올림픽파크포레온 84㎡대 · 2026년 9월 계약 2건(10/11 받은 값)', SRC_RT, {'cards': cards, 'hot': [[2, 3], [2, 3]]}
    if key == 'f_rent':
        return '손품 씨 눈에 들어온 전세', '84㎡대 신규 순수전세 · 1년 가운데 값', SRC_RT, {
            'bars': [['올림픽파크포레온', 14.0, '14.00억', '35건', 'accent'], ['헬리오시티', 12.5, '12.50억', '132건', 'ink']], 'max': 15,
            'ratio': [['올림픽파크포레온', 49.6], ['헬리오시티', 43.9], ['고덕그라시움', 41.5]], 'ratioHead': '전세가율 = 같은 면적 전세 가운데 값 ÷ 매매 가운데 값',
            'say': ['매매 값이 같아도', '보증금이 더 드는 단지']}
    if key == 'f_walk':
        return '둔촌동에서 걸어서', '올림픽파크포레온 가운데 → 출입구·학교 · 오픈스트리트맵 보행로', SRC_MAP, {
            'views': [view(['올림픽파크포레온'], 1.3, 1200, wpts('올림픽파크포레온', ['station', 'school']))], 'focus': ['올림픽파크포레온'], 'color': 'focus',
            'routes': [['올림픽파크포레온', 'station'], ['올림픽파크포레온', 'school']],
            'cards': [['둔촌오륜역 출입구', '430m', '역'], ['서울위례초등학교', '270m', '초등학교'], ['학교가 역보다', '더 가까움', '']]}
    if key == 'g_map':
        return '마지막, 강동구 고덕동', '손품 씨가 지금 사는 동네 · 오픈스트리트맵 보행로', SRC_MAP, {
            'views': [view(['고덕그라시움', '래미안힐스테이트고덕', '고덕아남'], 1.25), view(['고덕그라시움'], 1.6, 900, wpts('고덕그라시움', ['station'])),
                      view(['래미안힐스테이트고덕'], 1.4, 1000, wpts('래미안힐스테이트고덕', ['station']))],
            'focus': ['고덕그라시움', '래미안힐스테이트고덕'], 'color': 'focus', 'home': '래미안힐스테이트고덕',
            'routes': [['고덕그라시움', 'station'], ['래미안힐스테이트고덕', 'station']],
            'cards': [['손품 씨네', '래미안힐스테이트고덕', '지금 사는 곳'], ['고덕그라시움 → 상일동역 출입구', '180m', ''], ['래미안힐스테이트고덕 → 고덕역 출입구', '640m', '']]}
    if key == 'g_ruler':
        return '역까지 걷는 거리', '단지 가운데 → 지하철 출입구 · 오픈스트리트맵 보행로', SRC_MAP, {
            'groups': [['지하철 출입구', [['고덕그라시움', 180, '180m', 'accent'], ['래미안힐스테이트고덕', 640, '640m', 'ink']]]], 'max': 1400, 'note': '640 ÷ 180 = 3.56배'}
    if key == 'g_bars':
        return '같은 평형 평당 값', '고덕동 · 84㎡대 평당 값(1년 가운데 값) · ' + PPY, SRC_KAPT, {
            'bars': [['고덕그라시움', 9457, '9,457만원', '25건', 'accent'], ['래미안힐스테이트고덕', 7865, '7,865만원', '33건', 'ink']], 'max': 11000, 'diff': '그라시움이 +20.2%'}
    if key == 'g_walk2':
        return '학교 길과 장 보는 길', '가장 가까운 초등학교·이마트까지 · 배정 학교 아님 · 오픈스트리트맵 보행로', SRC_MAP, {
            'groups': [['가장 가까운 초등학교', [['고덕그라시움', 390, '390m', 'accent'], ['래미안힐스테이트고덕', 600, '600m', 'ink']]],
                       ['이마트', [['고덕그라시움', 1170, '1,170m', 'ink'], ['래미안힐스테이트고덕', 960, '960m', 'accent']]]], 'max': 1400,
            'note': '학교는 그라시움이 210m 짧고, 마트는 손품 씨네가 짧음'}
    if key == 'g_cards':
        return '지은 해도, 세대 수도 다르다', '평당 값 차이가 역 때문이라고는 말할 수 없음', SRC_KAPT, {
            'cards': [['고덕그라시움', [['입주', '2019.09'], ['세대', '4,932세대'], ['역까지', '180m'], ['평당', '9,457만원']]],
                      ['래미안힐스테이트고덕', [['입주', '2016.12'], ['세대', '3,658세대'], ['역까지', '640m'], ['평당', '7,865만원']]]]}
    if key == 'g_diff':
        return '새 단지와 오래된 단지, 평당 값 차이', '84㎡대 평당 · 같은 동네 새 단지 대비 · ' + PPY, SRC_KAPT, {
            'rows': [['가락동', '가락쌍용1차 vs 헬리오시티', -27.1, '−27.1%', ''], ['고덕동', '고덕아남 vs 고덕그라시움', -37.2, '−37.2%', ''],
                     ['둔촌동', '둔촌신동아 vs 올림픽파크포레온', -47.0, '−47.0%', '4건뿐, 참고']], 'min': -50}
    if key == 's_lines':
        return '세 단지의 달별 가운데 값', '각 단지 거래 가장 많은 평형 · 동떨어진 거래 뺌 · 단위 억원', SRC_RT, {
            'series': [['헬리오시티 84㎡대', 'ink', MED['helio']], ['올림픽파크포레온 84㎡대', 'accent', MED['forest']], ['고덕그라시움 59㎡대', 'fall', MED['gra']]],
            'min': 17, 'max': 33, 'band': ['2026.04', '2026.05', '4·5월']}
    if key == 's_vol':
        return '동 전체, 달마다 거래 수', '매매 · 해제·공공기관 매수 제외 · 4·5월은 주황', SRC_RT, {
            'dongs': [[d, DONGV[d]['months'], f"4~5월 {DONGV[d]['spring']}건 / {DONGV[d]['total']}건"] for d in ['가락동', '둔촌동', '고덕동']],
            'notes': ['여름 이후 대표 단지는 달마다 거래 몇 건뿐', '한 해 치 자료 — 해마다 같다고 말할 수 없음']}
    if key == 's_deadline':
        need('부동산 거래신고 등에 관한 법률 제3조①')
        return '최근 두 달은 아직 늘 수 있다', '부동산 거래신고 등에 관한 법률 제3조① · 계약일부터 30일 안에 신고', '부동산 거래신고 등에 관한 법률 제3조①(국가법령정보센터) · ' + SRC_RT, {
            'months': [[2026, 9, 30, 2], [2026, 10, 31, 4]], 'got': [10, 11], 'from': [9, 11], 'stamp': '마지막 몇 건으로 방향을 읽지 않기'}
    if key in ('gap1', 'gap2'):
        J = key == 'gap2'
        order = [('래미안힐스테이트고덕', '래미안힐스테이트고덕', '지금 사는 단지'), ('아남1', '고덕아남', '고덕아남'), ('고덕그라시움', '고덕그라시움', '그라시움'),
                 ('올림픽파크포레온', '올림픽파크포레온', '포레온'), ('헬리오시티', '헬리오시티', '헬리오시티')]
        rows = []
        for raw, name, word in order:
            sale, more, jeon = GAP[raw]
            if J:
                if raw == '래미안힐스테이트고덕': continue
                d = round(jeon - 9.5, 2); rows.append([name, f'전세 {eok(jeon)}', ('+' if d >= 0 else '−') + f'{abs(d):.2f}억', d, word])
            else:
                rows.append([name, f'매매 {eok(sale)}', f'+{more:.2f}억', more, word])
        if J: rows.sort(key=lambda r: r[3])
        for i, r in enumerate(rows): r.append(has(r[4]) if has(r[4]) >= 0 else min(i + 1, len(lines) - 1))   # 그 단지를 말하는 줄에서 칸이 채워진다
        return ('전세로만 옮긴다면' if J else '손품 씨의 계산서'), (('84㎡대 신규 순수전세 가운데 값 − 지금 보증금 9.50억' if J else '84㎡대 매매 가운데 값 − 지금 보증금 9.50억')), SRC_RT, {
            'deposit': ['지금 보증금', '9.50억', '래미안힐스테이트고덕 84㎡대 전세'], 'rows': rows, 'jeonse': J,
            'foot': '세금·중개보수·대출은 넣지 않은 단순 차액 · 대출 한도는 사람마다 달라 계산 안 함', 'max': 20,
            'extra': (['고덕아남 1996.03 입주 · 고덕동 지도 단지 중 두 번째로 오래됨', '어디로 가라는 말이 아니라, 단순히 뺀 계산'] if J else ['세금·중개보수·대출은 넣지 않은 단순 차액', '대출 한도는 사람마다 달라 계산하지 않음'])}
    if key in ('sheet', 'e_table'):
        rows = []
        tab = open(os.path.join(EP, 'cafe_table.md'), encoding='utf-8').read()
        for n in ['헬리오시티', '가락쌍용1차', '올림픽파크포레온', '둔촌신동아', '고덕 그라시움', '래미안힐스테이트 고덕', '고덕아남']:
            c = [x.strip() for x in re.search(rf'^\| {re.escape(n)} \|.*$', tab, re.M).group(0).strip('|').split('|')]
            rows.append([SHORT.get(c[0], c[0]), c[1], c[2], c[3].split('(')[0], c[8], c[9], c[10]])
        return '세 동네 단지 37곳 표', '파이어맵 카페에 전체 표 · 여기는 대표 단지만 · 계산·비교 자료, 사고팔라는 권유 아님', SRC_MAP + ' · cafe.naver.com/firemap', {
            'cols': ['단지', '입주', '세대', '84㎡대 평당', '전세가율', '역(걸어서)', '초등학교'], 'rows': rows, 'cafe': 'cafe.naver.com/firemap'}
    if key == 'e_map':
        return '평당 값과 걷는 거리', '84㎡대 평당 값 · 대표 단지 셋과 같은 동네 오래된 단지 셋', SRC_MAP, {
            'views': [ALLV], 'focus': ['헬리오시티', '가락쌍용1차', '올림픽파크포레온', '둔촌신동아', '고덕그라시움', '고덕아남'], 'color': 'ppy', 'dongLabels': True, 'labels': ['헬리오시티', '올림픽파크포레온', '고덕그라시움'],
            'cards': [['헬리오시티', '1억 1,087만원', '가락쌍용1차 8,080만원'], ['올림픽파크포레온', '1억 1,017만원', '둔촌신동아 5,840만원(4건)'], ['고덕그라시움', '9,457만원', '고덕아남 5,937만원']]}
    raise KeyError(key)


def script_lines(path):
    """script.md → {장 번호: [(말, 자막|None)]} — 자막은 그 말 줄 바로 뒤 '[자막: …]'."""
    out, cur, last = {}, None, None
    for line in open(path, encoding='utf-8').read().split('\n---', 1)[0].splitlines():
        if line.startswith('## '):
            t = line[3:].strip(); cur = re.sub(r'^\[', '', t).split()[0].rstrip(']'); out[cur] = []; last = None
        elif cur is not None and line.lstrip().startswith('- '):
            t = re.sub(r'\s*\(화면.*$', '', line.strip()[2:]).strip(); t = re.sub(r'\s*\[자막:.*?\]', '', t).strip()
            if t: out[cur].append([t, None]); last = out[cur][-1]
        elif cur is not None and line.strip().startswith('[자막:') and last is not None:
            c = line.strip()[4:].rstrip(']').strip()
            c = re.sub(r'\s*\(calc_out \d+\)', '', c)                       # 내부 근거 표시는 화면에 안 띄운다
            last[1] = c
    return out


def clean(t): return re.sub(r'\s*\(재사용 \d+장\)', '', t).strip()        # 예고 줄의 '(재사용 N장)'은 녹음 메모 — 화면에 안 쓴다


def main():
    sl = script_lines(os.path.join(EP, 'script.md'))
    voice = {}
    vj = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
    for s in vj.get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[clean(l['text'])] = l
    scenes, warn = [], []
    for ch in ['0.', '1.', '2.', '3.', '4.', '5.', '6.', '7.']:
        lines = sl.get(ch, [])
        found = []
        for key, kind, c, anc in RULES:
            if c != ch: continue
            if anc is None: idx = 0
            else: idx = next((i for w in anc for i, (t, _) in enumerate(lines) if w in t), None)
            if idx is None: warn.append(f'{key}: {anc} 못 찾음 — 장면 뺌'); continue
            if any(i == idx for i, *_ in found): warn.append(f'{key}: 시작 줄이 다른 장면과 같음 — 뺌'); continue
            found.append((idx, key, kind))
        found.sort()
        if found and found[0][0] != 0: found[0] = (0,) + found[0][1:]
        for j, (idx, key, kind) in enumerate(found):
            part = lines[idx:(found[j + 1][0] if j + 1 < len(found) else None)]
            out = []
            for t, cap in part:
                ct = clean(t); v = voice.get(ct)
                fr = v['frames'] if v else max(12, round(SC.syl(SC.speak(ct)) / RATE * FPS))
                out.append({'text': ct, 'cap': cap, 'frames': fr, 'audio': v['audio'] if v else None})
            title, sub, src, data = spec(key, [x['text'] for x in out])
            frames = sum(x['frames'] for x in out)
            scenes.append({'key': key, 'kind': kind, 'title': title, 'sub': sub, 'source': src, 'chapter': CH_NAME[ch], 'data': data, 'lines': out, 'frames': frames})
    scenes[-1]['frames'] = max(scenes[-1]['frames'], END_MIN)
    missing = sum(1 for s in scenes for l in s['lines'] if not l['audio'])
    nlines = sum(len(v) for v in sl.values())
    res = {'fps': FPS, 'scenes': scenes, 'missing': missing, 'maps': MAPS, 'mapBox': [MW, MH]}
    json.dump(res, open(os.path.join(VID, 'h1.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    tot = sum(s['frames'] for s in scenes) / FPS
    for w in warn: print('경고 ·', w)
    print(f'장면 {len(scenes)} · 말 줄 {nlines} · 길이 {int(tot // 60)}:{tot % 60:04.1f} · 목소리 없는 줄 {missing} · 그림 종류 {len({s["kind"] for s in scenes})} {sorted({s["kind"] for s in scenes})}')
    t = 0
    for i, s in enumerate(scenes):
        print(f"  {i:2} {int(t // 60)}:{t % 60:04.1f} {s['key']:10} {s['kind']:8} {s['frames'] / FPS:5.1f}초 줄{len(s['lines']):2}  {s['title']}")
        t += s['frames'] / FPS
    return res


if __name__ == '__main__':
    main()
