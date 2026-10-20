# H-3 화면 재료 — say_v4.txt(260줄) + voice.json + script.md [자막] + calc_out·calc2_out·facts.txt → work/video/h3.json (Remotion H3가 읽는다)
#   py -3.12 work/research/longform/ep/H-3/h3props.py
# 10/21 PD: 틀은 H-2(h2props.py·H2.tsx = C2 견본 판)와 같다. 다른 곳:
#   ① 줄은 say_v4 줄 번호(1~260)로 부른다(voice.json 줄 순서 = say 순서) ② 자막(cap)은 script.md의 그 말 줄 바로 아래 [자막: …]을 자동으로 붙인다
#   ③ 'pic' 장면 = shot_plan.md 장면 계획의 지도(OSM)·종이 판(자체)·AI 실사(RealVisXL, badge 'AI 생성') — 심사 '못함'으로 뺀 4장(r04·r13·r17·r28)은 안 씀
#   ④ 실사 영상은 bg/h3 credits.json(Pexels) — 상표·각인 클립(38259254·38259256·38259259·31400388·7578842)과 37246286(심사 못함)은 안 씀
# 숫자: props 안 숫자 글자는 전부 calc_out·calc2_out·facts.txt·script.md에 있는 글자만 — 맨 아래 numcheck가 막는다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
# 10/21 PD: B-31 쉼 관문(렌더본 앞 180초, 0.25초 넘는 쉼 비율 ≤12%, 공개 10/23~)에 13.4%로 걸림 — 줄 사이 틈(GAP 6프레임 0.2초 + wav 앞뒤 무음 0.1초 = 0.3초)이
#   줄마다 '쉼'으로 잡힘(줄 사이 7.7% · 줄 안 5.7%). 줄 사이 빈틈만 3프레임 줄여 중앙 0.30초·7.4%(경쟁 사람 진행자 0.3초·6%에 가장 가까움, 2프레임 11.5%·4프레임 5.6% · 같은 잣대로 X-1·T-1 렌더본 값과 계산값이 일치하는 것 확인, scratchpad simpause.py). 소리는 안 자름.
GAP_TRIM = 3
rd = lambda p: open(os.path.join(EP, p), encoding='utf-8').read()
CALC = rd('calc_out.txt') + rd('calc2_out.txt') + rd('facts.txt')
SCRIPT = rd('script.md')
SAYV = [l.rstrip('\n') for l in open(os.path.join(EP, 'say_v4.txt'), encoding='utf-8') if l.strip()]
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == len(SAYV) == 260, (len(ALL), len(SAYV))
# 자막: script.md 말 줄('- ') 다음에 오는 [자막: …] 줄들 → 그 말 줄의 cap
CAP = {}; k = 0
for ln in SCRIPT.split('\n## [0.', 1)[1].splitlines():
    t = ln.strip()
    if t.startswith('- '): k += 1
    elif t.startswith('[자막:') and k:
        CAP[k] = (CAP[k] + ' · ' if k in CAP else '') + t[len('[자막:'):].rstrip(']').strip()
assert k == 260, ('script 말 줄 수', k)
USED = set()
def L(n):
    assert n not in USED, ('두 번 쓴 줄', n); USED.add(n); l = ALL[n - 1]
    assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), ('소리 없음', n)
    fr = l['frames'] - GAP_TRIM; assert fr >= int(l['sec'] * FPS + 0.999), ('소리가 잘림', n)   # 줄 사이 빈틈만 줄임, 소리는 그대로
    return {'text': l['text'], 'audio': l['audio'], 'frames': fr, 'cap': CAP.get(n), 'i': n}
def S(kind, ns, pause=0, **data):
    ls = [L(n) for n in ns]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls) + pause, 'data': data}
def L_len(ns): return sum(ALL[n - 1]['frames'] for n in ns)

# 실사 영상(Pexels) — credits.json 셋에서
BG = {}
for sub in ['stock', 's2/stock', 's3/stock']:
    for c in json.load(open(os.path.join(VID, 'public', 'bg', 'h3', sub, 'credits.json'), encoding='utf-8')):
        BG.setdefault(c['id'], {'file': f"bg/h3/{sub}/{c['file']}", 'usable_sec': c['sec'] - 0.5, 'author': c['author'], 'desc_line': c['desc_line']})
BAN = {38259254, 38259256, 38259259, 31400388, 7578842, 37246286}
USEDBG = {}
def lic(cid): return f"Pexels {cid} 무료({BG[cid]['author']})"
def clip_from(cid, sec, start=0):
    assert cid not in BAN, ('안 쓰는 클립', cid)
    c = BG[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1
    frm = start + (0 if k == 0 else min(max(0, c['usable_sec'] - start - sec), k * 5))
    assert frm + sec <= c['usable_sec'] + 0.5, ('실사 클립이 말보다 짧다', cid, round(frm + sec, 1), c['usable_sec'])
    return frm
def broll(cid, ns, say, side='left', start=0):
    assert not re.search(r'\d', say), ('실사 say 숫자', say)
    frm = clip_from(cid, L_len(ns) / FPS, start)
    return S('broll', ns, src=BG[cid]['file'], license=lic(cid), say=say, side=side, **({'from': int(frm * FPS)} if frm else {}))
def live(cid, ns, who=None, say=None, past=False, start=0, pause=0):
    frm = clip_from(cid, (L_len(ns) + pause) / FPS, start)
    d = dict(src=BG[cid]['file'], license=lic(cid), past=past, **({'from': int(frm * FPS)} if frm else {}))
    if who: d['who'] = who
    if say: d['say'] = say
    return S('live', ns, pause=pause, **d)
# 그림(지도·종이 판·AI 실사) — shot_plan.md 장면 계획
OSM = '지도 자료 © OpenStreetMap 기여자 (ODbL) · 파이어맵 그림'
OWN = '파이어맵 자체 그림'
AIL = 'AI 생성 그림(RealVisXL V5.0, 이 PC) · 특정 단지 아님'
def mapx(name, ns, zoom=(1.0, 1.08)): return S('pic', ns, pic=f'bg/h3/map/{name}.png', license=OSM, badge='', zoom=list(zoom), dark=True, inset=0.84, baked=True)
def board(name, ns, zoom=(1.0, 1.08)): return S('pic', ns, pic=f'bg/h3/board/{name}.png', license=OWN, badge='', zoom=list(zoom), dark=True, inset=0.84, baked=True)
def ai(name, ns, zoom=(1.0, 1.1)): return S('pic', ns, pic=f'bg/h3/ai/{name}.png', license=AIL, badge='AI 생성', zoom=list(zoom))
def brand(ns, line, sub=None, pause=0): return S('brand', ns, pause=pause, line=line, **({'sub': sub} if sub else {}))

SRC = '국토교통부 아파트 매매·전월세 실거래(2025.11~2026.10 계약) · 파이어맵 계산'
SRC_BLD = '국토교통부 실거래 · 건축물대장 총괄표제부 세대수(2026.10.17 조회) · 파이어맵 계산'
SRC_LAW = '법제처 국가법령정보센터 · 국토교통부·금융위원회 공고·보도자료(원문)'
SRC_GOV = '서울시 정비사업 정보몽땅 · 도시 및 주거환경정비법(법제처)'
SRC_EDU = '서울특별시교육청 공고 제2026-157호'
def big(title, v, s, ns, icon='Building2', c='accent', src=SRC, **d): return S('big', ns, title=title, v=v, s=s, icon=icon, c=c, source=src, **d)
def pair(title, a, b, ns, icon='Scale', src=SRC, **d): return S('pair', ns, title=title, v1=a[0], s1=a[1], c1=a[2], v2=b[0], s2=b[1], c2=b[2], icon=icon, source=src, **d)
def rows(title, rs, ns, icon='ListChecks', src=SRC, **d): return S('rows', ns, title=title, rows=rs, icon=icon, source=src, **d)
def bars(title, bs, ns, mx, dir='h', icon='ChartColumn', src=SRC, **d): return S('bars', ns, title=title, bars=bs, max=mx, dir=dir, icon=icon, source=src, **d)
def ask(n, q, frm, ns): return S('ask', ns, n=n, q=q, **({'from': frm} if frm else {}))

R = 'rise'; A = 'accent'; B = 'fall'; K = 'ink'
scenes = [
    # ── 0. 결론부터 ──
    live(37522115, [1], who='2026년 10월 23일 금요일', say='오늘은 압구정·신천·목동 아파트 실거래가 이야기', pause=20),   # 고정 여는 말 — 날짜는 화면 글자로만
    mapx('map_seoul3', [2]),
    board('board_rooms', [3, 4, 5]),
    big('강남구 압구정동 · 30억 안팎', '0건', '가장 싼 거래도 35억 넘음', [6, 7], icon='Ban', c=R),
    S('list5', [8, 9], title='댓글과 검색창에 나온 질문', icon='MessageCircleQuestion', source='유튜브 댓글 · 네이버 검색어 자동완성',
      items=['목동 12단지 20억 맞나요?', '65평 130억이라고요?', '파크리오 전세는?', '1년에 백 집 중 몇 집 팔렸나?']),
    # ── 기초 ──
    ask('기초', '세 동네, 처음 보시는 분을 위해', '강남구 압구정동 · 송파구 신천동 · 양천구 목동', [10]),
    broll(38029457, [11, 12], '압구정, 한강 바로 남쪽'),
    broll(37500921, [13, 14, 15], '신천동, 잠실 바로 옆'),
    ai('kold_s1', [16, 17]),
    mapx('map_seoul_tohu', [18]),
    rows('오늘 숫자는 이런 분께', [['이 동네 집을 사려는 사람'], ['세 들어 살려는 사람'], ['이미 집이 있는 사람']], [19], icon='Users'),
    board('board_pyeong_unit', [20, 21, 22]),
    big('광고에 나오는 평수', '공용 부분 포함', '오늘은 집 안 넓이(전용 ㎡)로만 비교', [23], icon='Ruler', c=K),
    # ── 1. 어떻게 셌나 ──
    ask('1장', '어떻게 셌나, 그리고 이 1년의 조건', '국토교통부 아파트 매매 실거래 · 2025.11~2026.10 계약 · 해제·공공기관 매수 제외', [24]),
    broll(8471105, [25], '딱 그 값만 센 게 아니다'),
    big('30억 안팎', '27억 ~ 33억', '위아래로 3억씩 넓혀 셈', [26], icon='Calculator', c=K),
    big('평당 가격', '전용면적으로 나눔', '집 안에서 실제로 쓰는 넓이', [27], icon='Ruler', c=K),
    rows('토지거래허가구역 · 아파트', [['서울 25개 구', '2025.10.20 ~ 2026.12.31'], ['압구정·목동 14개 단지', '서울시가 따로 지정', K, 1]], [28, 29], icon='MapPinned', src=SRC_LAW),
    broll(8482325, [30, 31], '허가 먼저, 그리고 직접 살기'),
    big('오늘 보는 거래', '대부분 직접 살 사람', '허가구역 · 2년 실거주 · 가격 영향은 자료에 없음', [32, 33], icon='Home', c=K, src=SRC_LAW),
    broll(30975009, [34], '먼저 세 동네 숫자부터'),
    # ── 2. 신천동 ──
    ask('2장', '신천동, 30억이면 85㎡쯤', '국토교통부 실거래 · 30억 안팎 = 27억~33억', [35]),
    mapx('map_sincheon_175', [36]),
    broll(38029457, [37], '가장 많이 팔린 크기, 국민평형'),
    pair('82~84㎡대 평당 · 같은 신천동', ['12,810만원', '장미1·2 · 34건', R], ['11,384만원', '파크리오 · 95건', A], [38, 39]),
    big('한 채 값 차이', '약 3억', '장미1·2 82㎡ 31.95억 · 파크리오 84㎡대 29.20억', [40], icon='Scale', c=R),
    broll(29303349, [41], '한 해 사이 많이 움직였을까'),
    pair('파크리오 84~85㎡ 중간 가격', ['29.25억', '2025.11~2026.04 · 58건', K], ['29.00억', '2026.05~10 · 37건', A], [42, 43]),
    broll(16392935, [44], '검색창에 자주 나온 평수 질문'),
    rows('평수 말과 실거래 넓이', [['16평 같은 말', '공용 부분까지 넣은 넓이'], ['실거래 자료', '집 안 넓이만', K, 1]], [45, 46], icon='Ruler'),
    big('파크리오 가장 작은 집', '35㎡', '전용 · 1년 20번 팔림', [47, 48], icon='Ruler', c=K),
    big('파크리오 35㎡대 중간 가격', '14억', '최저 10.00억 · 최고 15.50억', [49], icon='Home'),
    broll(29303349, [50], '아주 큰 단지'),
    big('1년에 팔린 집', '164채', '6,864세대 중 · 2.4%', [51, 52], icon='Building', src=SRC_BLD),
    # ── 3. 목동 ──
    ask('3장', '목동, 번호는 이어지는데 주소가 갈린다', '국토교통부 실거래 법정동', [53]),
    mapx('map_mokdong', [54, 55]),
    pair('30억 안팎 거래', ['67건', '목동 쪽 · 전용 중앙 96㎡', A], ['16건', '신정동 쪽 · 전용 중앙 115㎡', K], [56, 57, 58, 59], at2=2),
    broll(37527858, [60], '크기를 똑같이 맞추면'),
    pair('60~70㎡대 평당', ['11,957만원', '목동 쪽 1~7단지', R], ['9,931만원', '신정동 쪽 8~14단지', K], [61]),
    big('한 채로 치면', '약 4억', '60~70㎡대 매매 중앙 23.70억 vs 19.90억', [62], icon='Scale', c=R),
    pair('같은 작은 평수 · 평당', ['12,757만원', '7단지', R], ['9,881만원', '11단지', K], [63, 64]),
    broll(37527858, [65], '이유는 자료에 없다'),
    ask('댓글', '목동 12단지가 지금 20억 정도 하는데, 맞나요?', '유튜브 댓글', [66, 67]),
    broll(30975009, [68, 69], '주소는 신정동, 부르는 이름은 목동'),
    bars('목동신시가지12 · 면적별 중간 가격', [['72㎡', 20.40, '20.40억', A], ['57㎡', 18.00, '18.00억', K, 1], ['53㎡', 17.20, '17.20억', K, 2]], [70, 71, 72], 22),
    ask('댓글', '총투자금 20억이라면, 어디서 몇 ㎡?', '유튜브 댓글', [73, 74]),
    pair('20억 안팎 · 전용 중앙', ['85㎡', '목동 전체 · 105건', A], ['71㎡', '신정동 · 164건', K], [75, 76, 77], at2=2),
    broll(29303349, [78], '열네 단지, 큰 동네'),
    big('목동신시가지 14단지 · 1년', '429채', '26,635세대 중 · 1.6%', [79, 80], icon='Building', src=SRC_BLD),
    pair('1년에 팔린 비율', ['2.0%', '1~7단지 · 250건', A], ['1.2%', '8~14단지 · 179건', K], [81], src=SRC_BLD),
    ai('kold_s2', [82, 83]),
    broll(37500921, [84], '검색창에 자주 나온 그 단지 가격'),
    pair('7단지 66~68㎡ 중간 가격', ['25.45억', '2025.11~2026.04 · 10건', K], ['25.70억', '2026.05~10 · 10건', A], [85, 86]),
    # ── 4. 압구정 ──
    ask('4장', '압구정동, 30억 거래가 없었다', '국토교통부 실거래 · 30억 안팎 = 27억~33억', [87]),
    mapx('map_apgu_0', [88]),
    big('가장 싼 거래 1건', '35.70억', '한양1차 63.87㎡ · 2026.03 · 직거래', [89], icon='Home', c=K),
    broll(12079562, [90], '돈을 더 올려 보면'),
    rows('40억 안팎 · 전용 중앙', [['압구정동', '50㎡', A], ['신천동', '121㎡', K, 2], ['목동 쪽', '145㎡', K, 2]], [91, 92, 93], icon='Ruler'),
    ask('댓글', '65평 130억이라고요?', '유튜브 댓글 · 압구정 현대 집 안을 보여 준 영상', [94, 95]),
    big('65평 = 공용 부분까지', '200㎡에 조금 못 미침', '실거래 자료의 집 안 넓이(전용)', [96, 97], icon='Ruler', c=K),
    bars('현대1·2차 전용 197~198㎡ · 1년 4건', [['가장 싼 거래', 92, '92.00억', K], ['둘째', 97, '97.00억', K, 1], ['셋째', 102, '102.00억', K, 1], ['가장 비싼 거래', 110, '110.00억', A, 2]], [98, 99, 100], 120),
    big('130억에 신고된 거래', '0건', '1년 실거래 기준', [101], icon='Ban', c=R),
    broll(31251626, [102], '뉴스 속 낮춘 값'),
    pair('같은 집, 두 가지 값', ['호가', '집주인이 부른 값 · 오늘 안 씀', K], ['실거래', '계약 뒤 신고된 값', A], [103, 104], icon='Scale'),
    big('압구정 1년 최고가', '128억', '신현대11차 전용 183.41㎡ · 2025.12', [105], icon='Building', c=K),
    broll(12079562, [106], '몇 건으로는 방향을 말하기 어렵다'),
    bars('해제 신고 비율', [['압구정동', 7.6, '7.6%', R], ['신천동', 2.8, '2.8%', K, 2], ['목동', 2.7, '2.7%', K, 2], ['신정동', 2.9, '2.9%', K, 2]], [107, 108, 109, 110], 9),
    broll(30975009, [111], '최고 기록 거래는 해제 표시까지'),
    big('현대·신현대 3,788세대', '91채', '1년 매매 · 2.4%', [112], icon='Building', src=SRC_BLD),
    # ── 5. 평당 착시 ──
    ask('5장', '평당 값만 보면 생기는 착시', '같은 단지 안 작은 집 vs 큰 집', [113]),
    board('board_pyeong', [114]),
    pair('목동신시가지3 평당', ['11,955만원', '65㎡ · 29건', R], ['8,484만원', '122㎡ · 6건', K], [115]),
    big('크기별 거래 넉넉한 단지 26곳', '24곳', '가장 작은 집이 평당 더 비쌈 · 거꾸로 2곳', [116, 117], icon='ListChecks'),
    broll(16392935, [118, 119], '집이 작아져도 값은 넓이만큼 안 준다'),
    big('그래서 먼저 본 것', '같은 돈이면 몇 ㎡', '평당 줄 세우기 대신', [120], icon='Search', c=K),
    # ── 6. 허가구역 ──
    ask('6장', '허가구역에서 산다면, 2년 실거주와 예외', '부동산 거래신고 등에 관한 법률 · 시행령 §14의2', [121]),
    rows('허가 절차', [['사는 사람·파는 사람 같이 신청'], ['기간 안 통지 없으면 허가로 봄', None, None, 1], ['허가 없는 계약은 효력 없음', None, None, 2]], [122, 123, 124], icon='FileCheck', src=SRC_LAW),
    ai('key', [125, 126, 127]),
    ask('궁금증', '세입자가 사는 집은 아예 못 살까요?', '시행령 §14의2② · 2026.10.1 시행', [128]),
    board('board_permit', [129, 130, 131, 132]),
    big('특례로 넉 달 안 취득하면', '세입자 계약 끝난 날부터', '2년 직접 거주를 그때부터 셈', [133], icon='CalendarClock', c=K, src=SRC_LAW),
    broll(8478946, [134, 135], '조심할 것 둘'),
    rows('특례를 못 쓰는 경우', [['허가 뒤 넉 달 안에 계약이 끝남', '원래 규칙', R], ['이미 집이 있는 사람', '해당 없음', R, 1]], [136, 137], icon='TriangleAlert', src=SRC_LAW),
    broll(8482325, [138], '집이 있는 사람은 해당 없음'),
    big('세입자가 갱신했다면', '갱신 계약 끝나는 날', '2027년 말 전에 시작된 갱신만', [139, 140], icon='CalendarClock', c=K, src=SRC_LAW),
    broll(8471105, [141, 142], '세입자 있는 집도 사고팔 수 있게'),
    rows('2년 못 채워도 예외', [['해외 이주'], ['병역 복무'], ['재해 · 공익사업 등']], [143], icon='ListChecks', src=SRC_LAW),
    rows('세입자 있는 집 · 먼저 있어야 할 돈', [['파크리오 국민평형', '18.20억', A, 1], ['한양1차 작은 집', '35.17억', R, 2]], [144, 145, 146], icon='Wallet'),
    broll(8482325, [147], '세입자 계약 끝나는 날부터 확인'),
    board('board_loan', [148, 149, 150, 151]),
    big('15억이 안 넘는 집', '6억까지', '시세는 은행이 한국부동산원·KB 시세로', [152, 153], icon='Landmark', c=K, src=SRC_LAW),
    broll(6962707, [154, 155], '지금 기준은 은행에서 확인'),
    big('1주택 · 9억 넘는 집 취득세', '3%', '지방세법 §11①8다', [156, 157], icon='Receipt', c=K, src=SRC_LAW),
    big('30억 집이라면', '9,000만원', '취득세만 · 지방교육세 등은 별도', [158, 159], icon='Receipt', src=SRC_LAW),
    # ── 7. 재건축 ──
    ask('7장', '재건축 단계와 조합원 자격', '도시 및 주거환경정비법 §39 · 서울시 정비사업 정보몽땅', [160]),
    ai('kold_s1', [161], zoom=(1.1, 1.0)),
    big('투기과열지구', '서울 25개 구 전부', '국토교통부공고 제2025-1225호', [162], icon='MapPinned', c=K, src=SRC_LAW),
    big('조합설립인가 뒤 산 사람', '조합원 못 됨', '새 집 대신 돈으로 손실보상', [163, 164], icon='Ban', c=R, src=SRC_GOV),
    broll(8478946, [165], '신탁 방식은 지정된 날이 기준'),
    rows('투기과열지구 지정', [['강남구 · 송파구', '그 전부터'], ['양천구', '2025년 10월 새로', R, 1]], [166, 167], icon='MapPinned', src=SRC_LAW),
    board('board_stages', [168, 169, 170]),
    rows('목동신시가지 14단지', [['조합설립 · 사업시행자 지정', '12곳'], ['3단지', '추진위원회', K, 1], ['2단지', '지정 날짜 확인 안 함', R, 2]], [171, 172, 173], icon='ListChecks', src=SRC_GOV),
    big('파크리오', '정비사업 아님', '서울시 정비사업 정보몽땅에 없음', [174], icon='Building', c=K, src=SRC_GOV),
    broll(37527858, [175, 176], '지금 사면 원칙적으로 조합원이 안 된다'),
    big('사업 기간 · 분담금', '다루지 않음', '정해진 자료가 없음', [177], icon='CircleSlash', c=K, src=SRC_GOV),
    rows('사는 사람이 조합원 되는 예외', [['파는 사람 1주택 · 10년 보유'], ['그 집에 5년 거주까지', None, None, 2]], [178, 179, 180], icon='ListChecks', src=SRC_GOV),
    broll(30975009, [181, 182], '이사·상속·해외 이주도 예외'),
    rows('계약 전 확인 둘', [['조합설립인가를 받았나'], ['파는 사람이 예외에 드나', None, None, 1]], [183, 184], icon='ListChecks', src=SRC_GOV),
    broll(8471105, [185, 186], '거주 기간은 주민등록표로'),
    # ── 8. 전세 ──
    ask('8장', '세 들어 살 사람이라면', '국토교통부 아파트 전월세 실거래', [187]),
    broll(4553292, [188], '자주 찾는 전세 시세'),
    pair('파크리오 84~85㎡ 전세 중간값', ['11.00억', '새로 맺은 전세 · 158건', A], ['10.50억', '다시 맺은 전세 · 157건', K], [189, 190], icon='Home'),
    big('전세 시세 볼 땐', '새로 맺은 계약만', '섞으면 실제보다 싸 보임', [191, 192], icon='Search', c=K),
    broll(37500921, [193], '목동 쪽 작은 평수'),
    pair('목동신시가지7 66~68㎡', ['7.00억', '새로 맺은 전세', A], ['25.60억', '매매', K], [194, 195], icon='Home'),
    pair('한양1차 49~51㎡', ['5.50억', '새로 맺은 전세', A], ['40.67억', '매매', K], [196, 197], icon='Home'),
    broll(4553292, [198, 199], '매매값 중 전세 보증금 비율'),
    board('board_jeonse', [200, 201, 202, 203]),
    broll(37527858, [204], '이유는 자료에 없다'),
    big('30%를 넘은 단지', '파크리오만', '1980년대까지 지은 단지는 모두 그 아래', [205, 206], icon='Building', c=K),
    rows('누구라면', [['새로 집을 구하는 분', '새로 맺은 계약 가격'], ['지금 집에서 다시 계약', '다시 맺은 가격도', K, 1]], [207, 208], icon='Users'),
    broll(37527858, [209], '지금 집에서 다시 계약한다면'),
    broll(8482325, [210, 211], '세입자 두고 사기는 큰돈, 지금은 막힘'),
    # ── 9. 학교 ──
    ask('9장', '학교 배정, 숫자로 말할 수 있는 것', SRC_EDU, [212]),
    broll(39704991, [213], '학교마다는 잴 수 없었다'),
    mapx('map_seoul_school', [214, 215]),
    rows('일반고 추첨 순서', [['1단계', '서울 전역에서 고른 학교'], ['2단계', '사는 곳 학교군', A, 1]], [216], icon='School', src=SRC_EDU),
    ai('school2_s2', [217, 218]),
    # ── 10. 갈아타기 ──
    ask('10장', '이미 한 채가 있고, 갈아탄다면', '소득세법 · 지방세법 · 국토교통부 조정대상지역 공고', [219]),
    ai('window_s1', [220, 221]),
    big('1주택 양도세', '12억까지 비과세', '넘는 부분에만 세금', [222, 223], icon='Receipt', src=SRC_LAW),
    big('조정대상지역에서 산 집', '2년 보유 + 2년 거주', '그래야 1주택 혜택', [224], icon='CalendarClock', c=K, src=SRC_LAW),
    board('board_swap', [225, 226, 227]),
    big('8월 3일 전에 샀거나 계약금 냈다면', '3년 그대로', '줄기 전 기간', [228, 229], icon='CalendarClock', c=K, src=SRC_LAW),
    broll(8478946, [230], '취득세에도 같은 기한'),
    big('기한 넘기면 취득세', '8%', '조정대상지역 두 번째 집', [231], icon='TriangleAlert', c=R, src=SRC_LAW),
    big('양도세도 기한 넘기면', '+20%p', '기본세율에 더함', [232], icon='TriangleAlert', c=R, src=SRC_LAW),
    broll(30975009, [233, 234], '국회에 있는 정부안'),
    rows('정부안 · 국회 통과 전', [['10년 이상 산 집', '기본공제 커짐'], ['2028년부터', '오래 가진 집 공제 바뀜', K, 0]], [235, 236], icon='FileText', src=SRC_LAW),
    broll(8471105, [237], '새 집도 허가구역이면'),
    big('새 집도 허가구역이면', '허가 + 2년 실거주', '특례는 집 없는 사람만', [238], icon='KeyRound', c=R, src=SRC_LAW),
    # ── 11. 직접 확인 ──
    ask('11장', '직접 확인하는 법', '국토교통부 실거래가 공개시스템 · 정보몽땅 · 토지이음', [239]),
    board('board_check', [240, 241, 242]),
    broll(6962695, [243, 244], '면적은 전용으로 맞추기'),
    rows('확인할 것', [['해제 거래는 빼기'], ['전세는 신규·갱신 나눠 보기', None, None, 1], ['재건축 단계는 정보몽땅', None, None, 2]], [245, 246, 247, 248], icon='ListChecks', src='국토교통부 실거래가 공개시스템 · 서울시 정비사업 정보몽땅'),
    broll(29303349, [249], '허가구역인지는 토지이음에서'),
    rows('허가구역 기한', [['서울 아파트 전체', '2026.12.31'], ['압구정 · 목동신시가지', '2027.4.26', K, 0]], [250], icon='CalendarClock', src=SRC_LAW),
    broll(37500921, [251], '압구정·목동은 서울시가 따로 지정'),
    big('특례 신청 기한', '2027년 말', '그때 그 집이 허가구역인지는 따로 확인', [252], icon='CalendarClock', c=K, src=SRC_LAW),
    broll(12079562, [253, 254], '이번 달 거래는 아직 덜 들어왔다'),
    # ── 12. 정리 ──
    board('board_summary', [255, 256, 257, 258]),
    live(37522115, [259], start=8, pause=105),   # 숨 쉴 실사 3.5초
    brand([260], '토요일 오전 11시 반 · 종부세'),   # 고정 맺는 말 — 10/24 J-1
]
missing = [n for n in range(1, 261) if n not in USED]
assert not missing, ('안 쓴 줄', missing)
order = [l['i'] for s in scenes for l in s['lines']]
assert order == sorted(order), ('줄 순서', [(a, b) for a, b in zip(order, sorted(order)) if a != b][:3])
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

# 답 열기(rv): 큰 값에 숫자가 있으면 말에서 그 숫자가 나오는 자리까지 '?'
NUM = re.compile(r'\d[\d,.]*')
def rv_of(lines, v):
    lead = NUM.search(v).group() if NUM.search(v) else None
    a = 0; hits = []
    for l in lines:
        for m in NUM.finditer(l['text']): hits.append((a + int(l['frames'] * m.start() / max(1, len(l['text']))), m.group()))
        a += l['frames']
    if not hits: return None
    same = [h for h in hits if lead and h[1].split('.')[0].replace(',', '') == lead.split('.')[0].replace(',', '')]
    return (same[0] if same else hits[-1])[0]
for s in scenes:
    d = s['data']
    if s['kind'] == 'big' and re.search(r'\d', d.get('v', '')):
        r = rv_of(s['lines'], d['v']); d['rv'] = max(12, min(r if r is not None else 12, s['frames'] - 45))
    elif s['kind'] == 'pair' and len(s['lines']) == 1 and re.search(r'\d', d.get('v2', '')):
        r = rv_of(s['lines'], d['v2']); d['rv'] = max(int(s['lines'][0]['frames'] * 0.45), r or 0)
run = mx = live_f = brk = 0; tot = sum(s['frames'] for s in scenes); RUNS = []; grp = []
for s in scenes:
    if s['kind'] in ('broll', 'live'): live_f += s['frames']
    if s['kind'] in ('broll', 'pic', 'ask', 'live', 'brand'):
        if run / FPS > 19.5: RUNS.append((round(run / FPS, 1), grp))
        run = 0; grp = []; brk += 1
    else: run += s['frames']; mx = max(mx, run); grp.append(s['data'].get('title'))
if run / FPS > 19.5: RUNS.append((round(run / FPS, 1), grp))
LONGPIC = [(s['data']['pic'], round(s['frames'] / FPS, 1)) for s in scenes if s['kind'] == 'pic' and s['frames'] / FPS > 20]
print('판 이어짐 20초 넘음:', RUNS or '없음', '· 그림 한 장 20초 넘음:', LONGPIC or '없음')
assert not RUNS, RUNS

SKIP = {'inset', 'baked', 'rv', 'past', 'who', 'part', 'beats', 'seed', 'audio', 'src', 'license', 'kind', 'icon', 'c', 'c1', 'c2', 'from', 'at2', 'max', 'side', 'hot', 'dir', 'pic', 'zoom', 'badge', 'dark'}
def strings(x):
    if isinstance(x, dict):
        for k2, v in x.items():
            if k2 not in SKIP: yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            if not isinstance(v, (int, float)): yield from strings(v)
    elif isinstance(x, str): yield x
SRCDOC = CALC + SCRIPT
bad = []
for s in scenes:
    for st in list(strings(s['data'])) + [l['cap'] for l in s['lines'] if l['cap']]:
        for dd in re.findall(r'\d[\d,.]*', st):
            dd = dd.rstrip('.,')
            if dd not in SRCDOC: bad.append((st[:40], dd))
assert not bad, bad

p = {'fps': FPS, 'scenes': scenes, 'boxOn': None, 'badge': ''}
json.dump(p, open(os.path.join(VID, 'h3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
used_clips = sorted(USEDBG)
json.dump({'clips': [{'id': c, 'file': BG[c]['file'], 'desc_line': BG[c]['desc_line']} for c in used_clips]}, open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
kinds = set(s['kind'] for s in scenes)
print(f'h3.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(kinds)}'
      f' · 실사 영상 {live_f / tot * 100:.1f}% · 바뀜 장면 {brk}(분당 {brk / (tot / FPS / 60):.1f}) · 판 이어짐 최장 {mx / FPS:.1f}초 · 숫자 대조 통과')
