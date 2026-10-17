# X-1 v3 화면 재료 — script.md(v3, 183줄) + voice.json(Chirp 녹음 줄 길이·소리) + calc_out.txt(끝날 10/15) + raw/collect_20261016.json → work/video/x1.json (Remotion X1이 읽는다)
#   py -3.12 work/research/longform/ep/X-1/x1props.py
# 10/17 PD: 대본 v3(질문 다섯 장)·10/17 롱폼 화면 기준(bgcheck: 실사 10%↑·컷 분당 3↑·같은 판 20초↓·큰 글자 9%↑·판 8줄↓)으로 C2 틀에 맞춰 다시 짰다. 옛 v2 = x1props.v2.py.bak.
# 틀: 판(big·pair·rows·list5·two·eq·dca·slips — TallyFrame) ↔ 꽉 찬 실사(broll — Pexels, bg_plan.json 풀) ↔ 질문 카드(ask, 어두운 판).
#     motion 부품: fxline·fxbars(FxDates — motion_preview/fxprops.py) · mo(HedgeFlip·EvenLadder·DaysBelow — motion_preview/v3props.py → x1_v3.json).
#     부품 장면이 20초를 넘으면 줄 단위 조각(i0~i1)으로 나눠 사이에 실사·질문 카드를 둔다. 조각은 부품 전체 시간표의 off 프레임부터 보여 준다(beats = 전체 줄 시작).
# 줄은 번호가 아니라 '장면 첫 줄 말 앞부분 + 줄 수'로 찾는다(대본이 바뀌면 assert). [자막] 줄은 그 바로 앞 말 줄의 cap(판 위 '정확한 값' 띠)으로 — cap 있는 줄은 실사·질문 카드에 두지 않는다(assert).
# 숫자: props 안 숫자 글자는 전부 calc_out 또는 script.md에 있는 글자만 — 맨 아래 numcheck가 기계로 막는다(축 눈금 글자는 뺌).
import json, os, re, sys, runpy
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [dict(l, sec=si) for si, s in enumerate(V['sections']) for l in s['lines']]
assert len(ALL) == 183 and all(l.get('audio') for l in ALL), len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
# [자막] → 바로 앞 말 줄
CAP, last = {}, None
for line in SCRIPT.split('\n---', 1)[0].splitlines():
    s = line.strip()
    if s.startswith('- '): last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
    elif s.startswith('[자막:') and last: CAP[last] = (CAP[last] + ' · ' if last in CAP else '') + s[4:].rstrip(']').strip()
# 10/17 PD: 화면 띠 낱말만 쉬운 말로(editor 17:18 [81]) — 서명된 대본 글은 그대로 두고 화면에서만
CAPFIX = [('현찰 스프레드 1.75%', '현찰 환전수수료 1.75%'), ('ECOS 731Y001', 'ECOS'), ('SPY 2026.7.2 → 10.15 · 달러 +3.63%', '미국 S&P500 ETF(SPY) 2026.7.2 → 10.15 · 달러 +3.63%')]
for _k in CAP:
    for _a, _b in CAPFIX: CAP[_k] = CAP[_k].replace(_a, _b)
assert all(any(l['text'] == k for l in ALL) for k in CAP), [k for k in CAP if not any(l['text'] == k for l in ALL)]
USED = set()
BG = {c['id']: c for c in json.load(open(os.path.join(EP, 'bg_plan.json'), encoding='utf-8'))['clips']}
CH = {0: None, 1: '질문 ①', 2: '질문 ②', 3: '질문 ③', 4: '질문 ④', 5: '질문 ⑤', 6: '누구라면', 7: None}

def take(first, n):
    hit = [i for i, l in enumerate(ALL) if l['text'].startswith(first)]; assert len(hit) == 1, (first, hit)
    i = hit[0]; out = []
    for j in range(i, i + n):
        assert j not in USED, ('두 번 씀', ALL[j]['text'][:20]); USED.add(j)
        l = ALL[j]; assert os.path.exists(os.path.join(VID, 'public', l['audio'])), l['audio']
        out.append({'text': l['text'], 'audio': l['audio'], 'frames': l['frames'], 'cap': CAP.get(l['text']), 'i': j})
    return out

def S(kind, first, cnt=1, **data):
    ls = take(first, cnt)
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}

SRC_SPY = '미국 S&P500 ETF(SPY) 종가(야후 파이낸스, 배당 미포함 가격) · 한국은행 ECOS 원/달러 매매기준율 · 파이어맵 계산(수수료·세금 없음)'
SRC_FX = '한국은행 ECOS 원/달러 매매기준율 · 파이어맵 계산(수수료 없음)'
SRC_KRX = 'KRX 종가 + 분배금(세전) · 삼성자산운용 KODEX 월간 자료(2026.8.31 기준)'
SRC_BANK = '은행연합회 외환길잡이 · 하나은행 2026.10.15 마지막 고시 · 파이어맵 계산'
SRC_DEP = 'KB국민은행 외화예금 금리안내(조회 2026.10.16) · 예금보험공사 예금자보호제도 FAQ · 파이어맵 계산'
SRC_USE = '한국은행 ECOS 원/달러·원/100엔 매매기준율 · 파이어맵 계산(카드 수수료 없음)'
SRC_FSS = '금융감독원 공식 블로그 「해외 카드결제 취소시 … 환차손 보상을 한층 강화합니다」(2026.10.14)'
def big(title, v, s, first, n=1, icon='CircleDollarSign', c='accent', src=SRC_FX, **d): return S('big', first, n, title=title, v=v, s=s, icon=icon, c=c, source=src, **d)
def pair(title, a, b, first, n=1, icon='Scale', src=SRC_FX, **d): return S('pair', first, n, title=title, v1=a[0], s1=a[1], c1=a[2], v2=b[0], s2=b[1], c2=b[2], icon=icon, source=src, **d)
def rows(title, rs, first, n=1, icon='ListChecks', src=SRC_FX, **d): return S('rows', first, n, title=title, rows=rs, icon=icon, source=src, **d)
def ask(nn, q, frm, first, n=1): return S('ask', first, n, n=nn, q=q, **({'from': frm} if frm else {}))
USEDBG = {}
def broll(cid, first, say, side='left', n=1):
    c = BG[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1
    s = S('broll', first, n, src=c['file'], license=f"Pexels {cid} 무료({c['author']})", say=say, side=side)
    sec = s['frames'] / FPS; frm = 0 if k == 0 else int(min(max(0, c['usable_sec'] - sec), k * 6))
    s['data']['from_'] = frm * FPS; s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = c['usable_sec']
    return s

# ── motion 부품 재료 ──
runpy.run_path(os.path.join(EP, 'motion_preview', 'fxprops.py'), run_name='__main__')
runpy.run_path(os.path.join(EP, 'motion_preview', 'v3props.py'), run_name='__main__')
FXJ = json.load(open(os.path.join(EP, 'motion_preview', 'x1_fx.json'), encoding='utf-8'))
V3 = json.load(open(os.path.join(EP, 'motion_preview', 'x1_v3.json'), encoding='utf-8'))
MOTION = {}
for k in ('hedge', 'even', 'below'):
    m = V3[k]; MOTION[k] = {'title': m['title'], 'source': m['source'], 'lines': [{'text': l['text'], 'audio': l['audio'], 'frames': l['frames'], 'cap': l['cap'] and l['cap'].replace('ECOS 731Y001', 'ECOS')} for l in m['lines']],
                            'frames': sum(l['frames'] for l in m['lines']), 'data': m['data']}
def mo(comp, i0, i1, first, icon):
    m = MOTION[comp]; n = i1 - i0
    s = S('mo', first, n, comp=comp, off=sum(l['frames'] for l in m['lines'][:i0]), icon=icon)
    assert [l['text'] for l in s['lines']] == [l['text'] for l in m['lines'][i0:i1]], (comp, i0, i1)
    for a, b in zip(s['lines'], m['lines'][i0:i1]): assert a['frames'] == b['frames'] and a['audio'] == b['audio'], (comp, a['text'])
    for l in s['lines']: l['cap'] = None   # [자막] 띠는 부품 쪽 전체 줄(motion.lines.cap)이 그린다 — v3props가 2024 쌍 띠를 앞줄로 당긴 것 그대로
    return s
def fxs(kind, first, title, icon):
    sc = FXJ['s1' if kind == 'fxline' else 's2']
    s = S(kind, first, 3, title=title, icon=icon, source=sc['source'])
    assert [l['text'] for l in s['lines']] == [l['text'] for l in sc['lines']] and [l['frames'] for l in s['lines']] == [l['frames'] for l in sc['lines']], kind
    return s

# ── 여는 두 선(2026.7.2 → 10.15 일별) ──
RAW = json.load(open(os.path.join(EP, 'raw', 'collect_20261016.json'), encoding='utf-8'))
USD = dict(RAW['USD']); SPY = {d.replace('-', ''): v for d, v in RAW['SPY']}
keys = sorted(k for k in USD if k in SPY and '20260702' <= k <= '20261015')
s0, u0 = SPY[keys[0]], USD[keys[0]]
UP = [round((SPY[k] / s0 - 1) * 100, 3) for k in keys]; DN = [round((SPY[k] * USD[k] / (s0 * u0) - 1) * 100, 3) for k in keys]
assert round(UP[-1], 2) == 3.63 and round(DN[-1], 2) == -10.76, (UP[-1], DN[-1])
XL = [[0, '7.2']] + [[i, f'{int(k[4:6])}.1'] for i, k in enumerate(keys) if i and k[4:6] != keys[i - 1][4:6]] + [[len(keys) - 1, '10.15']]
XL = [x for j, x in enumerate(XL) if j == len(XL) - 1 or XL[-1][0] - x[0] > 6]
TWO = {'up': UP, 'dn': DN, 'min': -14, 'max': 8, 'ticks': [[5, '+5%'], [0, '0%'], [-5, '−5%'], [-10, '−10%']], 'xl': XL,
       'nameUp': 'S&P500 ETF · 달러로', 'nameDn': '같은 투자 · 원화로', 'tagUp': '+3.63%', 'tagDn': '−10.76%'}

# ── 12칸 달력(calc_out 6절) ──
m6 = re.search(r'날짜·환율: (.+)', CALC).group(1)
CELLS = [[f"{int(d[:2])}월", r, float(r.replace(',', ''))] for d, r in re.findall(r'(\d\d-\d\d) ([\d,]+\.\d)', m6)]
assert len(CELLS) == 12 and CELLS[0][1] == '1,427.4' and CELLS[-1][1] == '1,355.7', CELLS
assert '평균 환율 1,450.4' in CALC and '92,290,941원 (-7,709,059원, -7.71%)' in CALC
CAL = {'cells': CELLS, 'min': 1300, 'max': 1560, 'avg': 1450.4, 'avgText': '평균 1,450.4원', 'now': 1338.6, 'nowText': '지금 1,338.6원',
       'each': '매달 첫 거래일 · 12번 × 8,333,333원', 'res': '770만원쯤 ↓', 'cellsAt': 0, 'avgAt': 1, 'nowAt': 2, 'resAt': 2}

R, A, B, K = 'rise', 'accent', 'fall', 'ink'
scenes = [
    # ── 0. 여는 장면 ──
    S('two', '미국 큰 회사들을', 3, title='주가는 오르고 계좌는 빠졌다', icon='TrendingDown', source=SRC_SPY + ' · 2026.7.2 → 10.15', two=TWO),
    broll(6326929, '주가는 올랐는데 계좌는', '돈은 어디로 샜을까'),
    big('새 나간 곳은 환율', '1,554원 → 1,339원', '원/달러 매매기준율 · 2026.7.2 → 10.15', '새 나간 곳은', 2, icon='ArrowLeftRight', c=B),
    broll(6963836, '요즘 지식iN과', '요즘 많이 묻는 글'),
    S('list5', '그중 많이 나온 질문', 1, title='많이 나온 질문 다섯', icon='MessageCircleQuestion', source='네이버 지식iN · 카페 · 유튜브 댓글',
      items=['주가는 올랐는데 왜 원화로는 깎였나?', '국내 상장 S&P500 ETF와 (H)는?', '달러로 미리 바꿀까, 원화로 살까?', '달러 예금·달러 상품도 마이너스?', '여행·직구, 지금 바꿔 둘까?']),
    broll(7428839, '계산은 1억 원을', '한 사람, 같은 돈으로'),
    broll(8044821, '미국 주식이 없는 분도', '여행·직구에도 해당', side='right'),
    # ── 1. 질문 ① ──
    ask('질문 ①', '주가는 올랐는데, 왜 원화로는 더 깎였나요?', "지식iN 2026.10.1 '-10퍼 손실인데요 원화로 계산하면 -18퍼' · 2026.10.2 '7%정도 차이나는데 왜 … 12%'", '지식iN에 이런 질문', 3),
    broll(5466779, '무슨 일인지 같은', '같은 돈으로 따라가 보기'),
    fxs('fxline', '1억을 달러로 바꾼 날을', '바꾼 날 네 개', 'CalendarDays'),
    broll(34596756, '먼저 달러로 바꿔서', '달러로만 들고 있었다면'),
    fxs('fxbars', '작년 이맘때 바꿨다면', '그냥 들고만 있었다면', 'Wallet'),
    broll(7593891, '이번엔 같은 날', '이번엔 ETF를 샀다면'),
    pair('작년 이맘때 샀다면', ['+16.40%', '달러로 본 수익', K], ['+9.69%', '원화로 · 670만원쯤은 환율 몫', A], '작년 이맘때 샀다면', 3, icon='TrendingUp', src=SRC_SPY),
    broll(8369980, '달러만 들고 있을 때보다', '불어난 돈에도 환율이 붙는다'),
    rows('바꾼 날마다 원화 결과', [['작년 이맘때', '+9.69%', R], ['올해 첫날', '+5.39%', R, 0], ['석 달 전', '−8.50%', B, 1], ['가장 비싸던 날', '−10.76%', B, 1]],
         '올해 첫날 샀다면', 2, icon='ChartColumn', src=SRC_SPY),
    ask('왜?', '왜 이렇게 될까요?', None, '왜 이렇게 될까요'),
    S('eq', '원화로 본 수익은', 4, title='주가 × 환율 = 원화', icon='Calculator', source='파이어맵 계산 예시',
      eq={'formula': ['주가', '×', '환율', '=', '원화 계좌'],
          'steps': [['주가 그대로 · 환율 −10%', '원화 −10%', B, 1], ['주가 −10% · 환율 −10%', '원화 −19%', B, 2], ['1억 → 9천만원 → 8,100만원', '0.9 × 0.9 = 0.81', K, 3]]}),
    ask('질문 ①의 답', '환율 −7%인데 손실 −12%라면, 주가도 빠졌다', '0.93 × 0.95 = 0.8835 → −11.65%', '질문처럼 환율이 7%'),
    broll(29904000, '그럼 환율은 왜', '환율은 왜 내렸을까'),
    rows('공식 문서에 적힌 이유', [['한국은행 · 8월 금리 결정문', '달러 넉넉 · 달러 약세', A], ['한국은행 · 10월 자료', '수출업체 달러 매도', A, 1]], '한국은행은 8월', 2, icon='FileText',
         src='한국은행 통화정책방향(2026.8.27) · 「2026년 9월 이후 국제금융·외환시장 동향」(2026.10.16)'),
    broll(10452020, '정부도 8월 회의에서', '해외에서 번 돈, 사상 최대'),
    big('달러가 흔해지면', '1,910억달러', '상반기 경상수지 · 재정경제부(2026.8.21)', '달러가 많이 들어와', 1, icon='Ship', c=A, src='재정경제부 시장상황점검회의(2026.8.21)'),
    ask('그래서', '내 계좌는 어떻게 보면 될까요?', None, '그래서 내 계좌는'),
    mo('even', 1, 3, '본전 환율을 직접', 'Calculator'),
    broll(6186015, '증권사 앱에', '앱 수익률로 나누면'),
    mo('even', 4, 8, '가장 비싸던 날 산 경우는', 'Calculator'),
    broll(7829075, '조심할 게 있어요', '조심할 것'),
    mo('even', 9, 12, '본전 환율은 주가가', 'TriangleAlert'),
    # ── 2. 질문 ② ──
    ask('질문 ②', '국내 상장 S&P500 ETF는 왜 내렸고, 이름 끝 (H)는 뭔가요?',
        "유튜브 댓글 '미국 현지에서는 최고가갱신 … 국내상장 미국지수는 오히려 하락' · 지식iN 2026.9.25 '(H)가 붙어 있더라고요'", '이번엔 유튜브 댓글에', 3),
    broll(7735914, '한국 증권 계좌에서', '원화로 사는 미국 ETF'),
    pair('환노출 vs 환헤지', ['환노출형', '환율 변동을 그대로 받음', K], ['(H) 환헤지형', '환율 영향 최소화', B], '환율 움직임을 그대로', 2, icon='Split', src=SRC_KRX),
    rows('같은 회사, 두 상품', [['KODEX 미국S&P500', '환노출 · 종목번호 379800', K], ['KODEX 미국S&P500(H)', '환헤지 · 종목번호 449180', B, 0]], '같은 회사가 만든', 1, icon='Tag', src=SRC_KRX),
    broll(8369980, 'ETF가 나눠 주는', '분배금까지 넣어서'),
    mo('hedge', 0, 4, '달러가 제일 비쌌던 날 1억을', 'ChartColumn'),
    broll(6326929, '댓글 질문의 답이', '댓글 질문의 답'),
    mo('hedge', 5, 6, '환노출형은 미국 지수가', 'ChartColumn'),
    ask('그럼', 'H형이 늘 나을까요?', None, '그럼 H형이 늘'),
    mo('hedge', 7, 11, '재작년 첫날 넣었다면', 'ChartColumn'),
    broll(31879939, '환율을 막아 두면', '막으면 이익도 같이 막힌다'),
    ask('그래서', '어떻게 고르면 될까요?', None, '그래서 어떻게 고르면'),
    rows('어떤 돈으로 쓸 건가', [['곧 원화로 꺼내 쓸 돈', '환율 흔들림 = 손익', A, 1], ['H형은', '그 흔들림을 줄임', B, 1], ['나중에 달러로 쓸 돈', '원화 값 덜 중요', K, 2]],
         '기준은 이 돈을', 3, icon='Wallet', src=SRC_KRX),
    broll(7735915, '큰 기관은 어떻게', '큰 기관은 어떻게 할까'),
    big('국민연금 환헤지 비율', '15%', '해외투자 기본값 · 일부만 막는다', '나라 돈을 굴리는 곳도', 1, icon='Landmark', c=A, src='보건복지부 2026년 제3차 국민연금기금운용위원회(2026.4.14)'),
    broll(5651783, '조심할 것도 있습니다', '조심할 것'),
    rows('헤지 비용과 총보수', [['헤지 비용', '들 수 있음 · 숫자 공개 없음', R], ['총보수 KODEX 미국S&P500', '연 0.0062%', K, 1], ['총보수 KODEX 미국S&P500(H)', '연 0.0099%', K, 1]], '운용사는 환헤지 상품에', 2,
         icon='Receipt', src='삼성자산운용 뉴스룸(2026.7.24) · 운용사 월간 자료(2026.8.31 기준)'),
    broll(6963836, '이름이 거의 같아서', '주문 전, 이름 끝 확인', side='right'),
    # ── 3. 질문 ③ ──
    ask('질문 ③', '달러로 미리 바꿀까, 원화로 바로 살까? 바꿀 때 얼마가 새나요?',
        "지식iN 2026.10.9 '달러를 미리 구매 후에 달러로 매수하는 것과 원화(매수시 자동 환전)로 매수하는 것' · 댓글 '1000원 2000원씩 모으기 … 매일 환전하고있는격'", '환전을 묻는 글도', 3),
    broll(8830802, '어느 쪽이든, 원화가', '바뀌는 순간 비용이 붙는다'),
    broll(7593891, '지금까지 계산은 전부', '지금까지는 기준 환율로', side='right'),
    pair('기준 환율과 현찰 값', ['매매기준율', '지금까지 계산 기준', K], ['현찰 살 때', '더 비쌈 · 차이 = 환전수수료', R], '그런데 은행에서 달러 현찰', 2, icon='Banknote', src='은행연합회 외환길잡이'),
    big('하나은행 고시', '+1.75%', '현찰 살 때 − 매매기준율 · 2026.10.15', '은행이 날마다 알리는', 1, icon='Landmark', c=R, src=SRC_BANK),
    broll(5466779, '1억을 우대 없이', '우대 없이 현찰로 바꾸면'),
    rows('우대 없이 현찰로', [['1억 → 덜 받는 달러', '1,281달러', R], ['원화로', '170만원어치쯤', R, 0], ['천 달러 사서 바로 팔면', '46,980원', R, 1]], '원화로 170만원', 2, icon='Banknote', src=SRC_BANK),
    rows('같은 날, 값은 넷', [['현찰 살 때', '1,365.99원', R], ['송금 보낼 때', '1,355.60원', A], ['매매기준율', '1,342.50원', K], ['현찰 팔 때', '1,319.01원', B]], '은행이 알리는 값은 하나가', 1,
         icon='ListChecks', src=SRC_BANK, hot=False),
    ask('그래서', '덜 내려면 어떻게 할까요?', None, '그래서 덜 내려면'),
    big('송금 값은 덜 붙는다', '+0.98%', '송금 보낼 때 · 현찰 살 때는 +1.75%', '해외로 돈을 보낼 때', 1, icon='Send', c=A, src=SRC_BANK),
    broll(6186015, '우대율은 은행마다', '은행별 우대율, 한 화면에서'),
    pair('주요 은행 달러 수수료', ['1.75%', '수수료율 · 주요 은행 같음', K], ['0.2% 미만', '최대 90% 우대 뒤', B], '그 표를 보면 주요 은행', 3, icon='Percent', src='은행연합회 외환길잡이(2026.8~9 기준)'),
    broll(7428839, '증권사에서 바꾸는 달러도', '내 증권사 우대율 먼저', n=2),
    broll(5923592, '한 번에 바꾸지 말고', '나눠 바꾸면 어떨까', side='right'),
    S('dca', '1억을 작년 가을부터', 3, title='매달 나눠 바꾼 1년', icon='CalendarRange',
      source='한국은행 ECOS · 매달 첫 거래일 2025.11.3~2026.10.1 · 파이어맵 계산(수수료 없음)', cal=CAL),
    broll(7735915, '달러가 제일 비쌌던 날 한 번에', '가장 나쁜 날보다는 덜'),
    broll(5466779, '1년 전에 한 번에 바꿨으면', '작년 이맘때보다는 더', side='right'),
    rows('좋은 날과 나쁜 날 사이', [['한 번에 · 작년 이맘때', '94,234,424원', K], ['매달 나눠서', '92,290,941원', A], ['한 번에 · 가장 비싸던 날', '86,116,830원', B]], '나눠 바꾸면 결과가', 1,
         icon='Scale', src=SRC_FX + ' · 10.15 원화', hot=False),
    broll(6963836, '천원, 이천원씩 매일', '매일 바꾸면 매일 붙는다'),
    rows('바꿀 때마다 수수료', [['원화 → 달러', '수수료', R], ['달러 → 원화', '한 번 더', R, 0], ['자주 사고팔 돈이 아니면', '우대율 높은 곳에서 덜 자주', B, 1]], '그 달러를 다시 원화로', 2,
         icon='Repeat', src='은행연합회 외환길잡이'),
    # ── 4. 질문 ④ ──
    ask('질문 ④', '달러 예금·달러 상품도 환율이 내리면 마이너스인가요?',
        "댓글 '달러RP 가입했는데 환율이 떨어지면 마이너스가 되나요?' · 지식iN 2026.10.4 '환율로 생긴 이익도 … 세금을 내야 하는지'", '달러 RP에 넣었는데', 2),
    broll(5778854, '예금보험공사 안내에는', '보호되는지는 증권사에 직접'),
    big('원화로 따지면', '마이너스 가능', '이자는 달러로 · 바꾸는 날 환율로', '원화로 따지면, 네', 2, icon='TrendingDown', c=B, src=SRC_DEP),
    broll(7829075, '은행 달러 예금으로', '은행 달러 예금이라면'),
    rows('달러 1년 정기예금', [['KB국민은행 · 12~18개월 미만', '연 3.64833%', K], ['이자소득세 15.4% 뒤', '연 3.09%', A, 1]], 'KB국민은행 고시를', 2, icon='PiggyBank', src=SRC_DEP),
    broll(7735914, '지금 1억 원을 달러로', '지금 바꿔 맡긴다면'),
    big('이자가 사라지는 환율', '1,298.5원', '이보다 내려가면 환율 손실 > 이자', '1년 뒤 환율이 지금보다', 2, icon='TriangleAlert', c=R, src=SRC_DEP),
    ask('그래서', '무엇부터 볼까요?', None, '그래서 무엇부터'),
    big('예금자보호 한도', '1억원', '외화예금도 · 원화로 환산 · 원금+이자 합쳐', '은행 달러 예금이라면', 4, icon='ShieldCheck', c=B, src='예금보험공사 예금자보호제도 FAQ'),
    broll(7735915, '그래서 1억 원어치를', '원금으로 꽉 채우면 이자는 한도 밖', side='right'),
    big('보호 안 되는 것', '펀드 · ETF', '금융투자상품 · 달러 ETF도 펀드', '그리고 같은 안내에', 1, icon='ShieldOff', c=R, src='예금보험공사 예금자보호제도 FAQ'),
    broll(5923592, '세금도 물어보셨죠', '환율 차익에도 세금?'),
    rows('세금은 어떻게', [['이자', '세금 붙음', R], ['환율로 생긴 차익', '공식 해석 못 찾음', K, 1], ['금액이 크다면', '국세청 상담센터에 직접', B, 2]], '이자에 세금이 붙는 건', 3,
         icon='Receipt', src='파이어맵 조사(2026.10.17) — 국세청 공식 해석 확인 안 됨'),
    broll(8830802, '달러로 바꾸는 순간 드는', '바꾸는 비용도 이자에서 빼고', side='right'),
    big('수수료 메우는 데', '반년 넘게', '현찰 1.75% ÷ 세후 이자 연 3.09% ≈ 0.57년', '우대 없이 현찰로 바꾸면', 2, icon='Hourglass', c=A, src=SRC_DEP),
    # ── 5. 질문 ⑤ ──
    ask('질문 ⑤', '여행·직구 갈 사람은 지금 바꿔 둘까요?', "지식iN 2026.9.13 '지금 엔화가 870정도인데 지금 환전을 힐까요 아니면 기다려야할까요?'", '여행 가는 분들은'),
    broll(10821823, '달러 값이 내리면, 달러를', '달러를 쓸 사람에겐 이득'),
    pair('천 달러를 쓴다면', ['155만원쯤', '7월 2일 · 가장 비싸던 날', K], ['134만원쯤', '10월 15일 · 지금', B], '미국 직구나 여행에서', 2, icon='ShoppingCart', src=SRC_USE),
    broll(32111755, '일본에서 10만엔을', '일본에서 쓴다면', side='right'),
    pair('10만엔을 쓴다면', ['96만원쯤', '7월 2일', K], ['85만원쯤', '지금', B], '그날엔 96만원쯤', 1, icon='ShoppingBag', src=SRC_USE),
    broll(9806390, '언제 바꿀지는 앞날', '앞날은 누구도 모른다'),
    mo('below', 1, 4, '대신 지나간 날과', 'CalendarSearch'),
    broll(38556529, '엔화는 지금보다 쌌던', '엔화는 더 싼 쪽', side='right'),
    mo('below', 5, 7, '지난 2년 가까운', 'CalendarSearch'),
    ask('그래서', '어떻게 결제할까요?', None, '그래서 어떻게 결제할까요'),
    rows('카드 해외 수수료', [['국제브랜드 + 해외서비스', '두 겹', K], ['KB국민카드 비자', '1.35%', A, 1], ['현대카드 비자', '1.28%', A, 2], ['천 달러를 쓰면', '18,071원', R, 3]], '카드로 결제하면 수수료가', 4,
         icon='CreditCard', src='KB국민카드 해외이용 종합안내 · 현대카드 · 파이어맵 계산(매매기준율 1,338.6원)'),
    broll(34596756, '우대 없이 현찰을 사는', '우대 받은 현찰보다 비쌀 수도'),
    big('인터넷 환전 신청', '최대 90%', '우대율 · 은행·공항에서 받기', '현찰이 필요하다면', 2, icon='Globe', c=A, src='은행연합회 외환길잡이(2026.10.17 확인)'),
    broll(6685174, '결제할 때는 현지 통화로', '현지 통화로 결제됐나'),
    big('해외원화결제 차단', 'DCC 차단', '원하지 않으면 카드사에 신청', '원화로 결제되는 해외원화결제', 1, icon='Ban', c=B, src='금융감독원 공식 블로그(2026.10.14)'),
    broll(3740041, '놓치기 쉬운 함정이', '놓치기 쉬운 함정'),
    S('slips', '결제한 날보다 취소한', 3, title='카드 취소, 덜 돌아온 돈', icon='Receipt', source=SRC_FSS + ' · 그림은 파이어맵이 그린 것',
      slips={'a': {'head': '해외 결제', 'label': '항공권 · 결제한 날', 'amt': '185만원', 'sub': '결제한 날 환율로'},
             'b': {'head': '결제 취소', 'label': '같은 달러 · 취소한 날', 'amt': '175만원', 'sub': '취소한 날 환율로'},
             'mid': '환율 80원 ↓', 'foot': '금융감독원이 든 사례 · 같은 달러를 취소해도 원화로는 덜 돌아옴', 'amtAt': 1, 'midAt': 2, 'footAt': 0}),
    broll(5778854, '이 차이는 표준약관에', '카드사가 물어 주는 게 원칙', side='right'),
    rows('환차손 보상', [['일부 취소 · 결제 정보 빠짐', '지금은 직접 신청', R], ['카드사가 찾아 보상', '2027년부터 계획', B, 1]], '그런데 일부만 취소했거나', 2, icon='Undo2', src=SRC_FSS),
    broll(6186015, '그때까지는 취소한 뒤', '돌아온 원화를 꼭 확인'),
    big('덜 돌아왔다면', '보상 신청', '카드사에 환차손 보상', '덜 돌아왔다면', 1, icon='BadgeCheck', c=A, src=SRC_FSS),
    # ── 6. 누구라면 ──
    broll(18757432, '같은 환율이어도, 사람마다', '사람마다 볼 숫자가 다르다'),
    big('원화로 돌아올 돈', '원화 숫자 = 손익', '은퇴 뒤 생활비처럼', '원화로 돌아올 돈이라면', 2, icon='House', c=A, src=SRC_SPY),
    broll(7308237, '달러로 쓸 돈이라면', '달러로 쓸 돈이라면', side='right'),
    rows('달러로 쓰거나 받는 돈', [['자녀 학비 · 해외 생활비', '달러 금액 그대로', B], ['달러 월급 · 배당', '바꿀 때만 덜 받음', A, 1]], '자녀 학비나 해외', 2, icon='Plane', src=SRC_FX),
    broll(34596756, '미국 주식이 재산의', '일부뿐이면 빠진 것도 작다'),
    big('1천만원만 넣었다면', '110만원 가까이 ↓', '줄어든 돈 · 7월 초 → 10.15', '1천만원만 S&P500', 1, icon='User', c=B, src=SRC_SPY),
    big('재작년 초에 바꿨다면', '380만원쯤 ↑', '2024.1.2 · 1,289.4원에 바꾼 1억', '재작년 초처럼 달러가', 2, icon='User', c=R, src=SRC_FX),
    broll(31879939, 'H형을 가진 사람은', '막은 만큼 놓친다', side='right'),
    broll(8044821, '곧 여행이나 직구로', '같은 달러를 더 싸게'),
    # ── 7. 끝 ──
    big('지난 편과 이어서', '환율이 깎았다', "지난 편 '1억, 1년 뒤 남은 돈' · 미국 ETF 세 개", "지난 편 '1억", 1, icon='Link', c=K, src="파이어맵 지난 편 '1억, 1년 뒤 남은 돈'"),
    big('전체 표는 카페 글에', '고정 댓글', '날짜별 전체 표 · 본전 환율 계산법', '날짜별 전체 표와', 1, icon='Table', c=A, src='파이어맵 카페'),
    ask('댓글로', '달러, 언제 바꾸셨나요?', '날짜를 남겨 주시면 같은 식으로 계산해 답글 드립니다', '달러, 언제 바꾸셨나요'),
]
# 장 칩
for s in scenes:
    s['data']['chapter'] = CH[ALL[s['lines'][0]['i']]['sec']]
for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
for s in scenes: assert s['kind'] != 'broll' or len(s['data']['say'].replace(' ', '')) <= 18, ('실사 say 18자', s['data']['say'])
short = []
for s in scenes:   # TallyBroll prop 이름(from) · 클립 길이 확인
    d = s['data']
    if 'from_' in d:
        d['from'] = d.pop('from_')
        if d['_need'] > d['_have'] + 0.5: short.append((d['src'], d['_need'], d['_have']))
        d.pop('_need'); d.pop('_have')
assert not short, ('실사 클립이 말보다 짧다', short)
assert len(USED) == len(ALL), ('안 쓴 줄', [ALL[i]['text'][:24] for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines']]; assert order == sorted(order), '줄 순서'
lost = [l['text'][:24] for s in scenes if s['kind'] in ('broll', 'ask') for l in s['lines'] if l['cap'] and l['cap'] not in (s['data'].get('from') or '')]   # 질문 카드는 from 줄에 같은 글이 있으면 됨
assert not lost, ('[자막] 줄이 실사·질문 카드에 — 판으로 옮길 것', lost)
for s in scenes:
    for l in s['lines']: l.pop('i')
scenes[-1]['frames'] += TAIL

# 화면 관문 어림: 판(실사·질문 카드 아닌 것)이 이어진 구간 최장, 실사 몫, 바뀜 장면 수
BREAK = ('broll', 'ask')
run = mx = live = brk = 0; tot = sum(s['frames'] for s in scenes); RUNS = []; grp = []
for s in scenes:
    if s['kind'] == 'broll': live += s['frames']
    if s['kind'] in BREAK:
        if run / FPS > 19.5: RUNS.append((round(run / FPS, 1), grp))
        run = 0; grp = []; brk += 1
    else: run += s['frames']; mx = max(mx, run); grp.append(s['data'].get('title') or s['data'].get('comp'))
if run / FPS > 19.5: RUNS.append((round(run / FPS, 1), grp))
assert not RUNS, RUNS
# 판 제목 13자(관문 큰 글자 9%: 110px 한 줄)
long_t = [s['data']['title'] for s in scenes if s['kind'] not in BREAK + ('mo',) and len(s['data']['title'].replace(' ', '')) > 13]
assert not long_t, ('제목 13자 넘음', long_t)

# 숫자 대조: props 글자 속 숫자 덩이는 calc_out·대본에 그대로 있어야 한다(축 눈금·선 값·부품 원재료는 뺌 — fxprops·v3props가 따로 assert)
SKIP = {'audio', 'src', 'license', 'kind', 'icon', 'c', 'c1', 'c2', 'from', 'side', 'hot', 'dir', 'max', 'min', 'up', 'dn', 'ticks', 'xl', 'off', 'comp',
        'amtAt', 'midAt', 'footAt', 'cellsAt', 'avgAt', 'nowAt', 'resAt', 'avg', 'now'}
def strings(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in SKIP: continue
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            if not isinstance(v, (int, float)): yield from strings(v)
    elif isinstance(x, str): yield x
SRCDOC = CALC + SCRIPT
bad = []
for s in scenes:
    for st in list(strings(s['data'])) + [l['cap'] for l in s['lines'] if l['cap']]:
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,')
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

p = {'fps': FPS, 'scenes': scenes, 'fx': FXJ['fx'], 'motion': MOTION}
json.dump(p, open(os.path.join(VID, 'x1.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
kinds = sorted({s['kind'] if s['kind'] != 'mo' else 'mo:' + s['data']['comp'] for s in scenes})
print(f'x1.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(kinds)}'
      f' · 실사 {live / tot * 100:.1f}% · 바뀜 장면 {brk}(컷 분당 {brk * 2 / (tot / FPS / 60):.1f} 어림) · 판 이어짐 최장 {mx / FPS:.1f}초 · 숫자 대조 통과')
