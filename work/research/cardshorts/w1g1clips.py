# W-1·G-1 롱폼을 잘라 세로 쇼츠 props를 만든다 (firemap-video-producer 2026-10-12, c1clips.py를 본뜸 · 틀 = video/src/C1S.tsx 그대로).
#   py -3.12 work/research/cardshorts/w1g1clips.py       # → work/video/w1s_div.json · g1s_buyday.json
# 목소리 = ep/W-1·G-1 voice.json wav 그대로(Chirp 3 HD Charon, 새 녹음 없음). 줄 번호 = video/w1.json·g1.json 장면 순서대로 센 전체 순번(0부터).
# 화면 숫자 = video/w1.json·g1.json(편집 통과한 롱폼 화면 글자) 그대로. 숫자를 새로 계산하지 않는다(배치·프레임만 정한다).
import os, json, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
VID = os.path.join(WORK, 'video')
TAIL = 36


def load(name):
    p = json.load(open(os.path.join(VID, name + '.json'), encoding='utf-8'))
    lines = [l for s in p['scenes'] for l in s['lines']]
    sc = {s['key']: s for s in p['scenes']}
    return lines, sc


def mk(lines):
    def L(*idx):
        return [{'n': i, 'text': lines[i]['text'], 'cap': lines[i].get('cap'), 'audio': lines[i]['audio'], 'frames': lines[i]['frames']} for i in idx]
    return L


def at(ls, x):
    i = min(int(x), len(ls) - 1); a = sum(l['frames'] for l in ls[:i])
    return int(round(a + (x - i) * ls[i]['frames']))


def scene(kind, label, source, lines, **data):
    return {'kind': kind, 'label': label, 'source': source, 'data': data, 'lines': lines}


SHORTS = {}

# ── W-1: 영업이익 107조인데 내 100주는? (줄 0·1·2 → 15·16 → 17·18 → 19·14 → 20) ──
WL, WS = load('w1')
L = mk(WL)
op = WS['open']['data']; df = WS['dayfall']['data']; dv = WS['div']['data']; pr = WS['pairs']['data']; dt = WS['dots']['data']
a = L(0, 1)
b = L(2)
c = L(15, 16)
d = L(17, 18)
e = L(19, 14)
f_ = L(20)
eg, dg = pr['groups'][0], pr['groups'][1]
SHORTS['w1s_div'] = dict(
  question=['영업이익 107조인데', '내 100주는?'], hot='100주',
  base='지난주 종가·공시 그대로 계산 · 지나간 값',
  answer=dict(label='삼성전자 100주 · 종가 10/2 → 10/8', items=['평가액 −140만원', '분기 배당 44번치'], arrow=False,
              note='세후 분기 배당 31,640원 · 팔기 전엔 확정 손실 아님'),
  scenes=[
   scene('vs', '같은 주, 두 숫자', WS['open']['source'], a, full=True,   # full = 판을 90프레임 당겨 0초부터 첫 칸이 다 보이게(둘째 칸 시각은 +90)
         tiles=[['삼성전자 100주 평가액', '−140만원', '종가 10/2 276,000원 → 10/8 262,000원', 0, 'fall'],
                ['3분기 영업이익(잠정)', op['big'][0], op['big'][2], at(a, 1) + 90, 'rise']]),
   scene('bars', '발표한 날 주가는', WS['dayfall']['source'], b, head='삼성전자 종가 · 원',
         bars=[[x[0], x[1], x[2], 0 if i == 0 else 8, x[4], x[5]] for i, x in enumerate(df['bars'])], max=df['max']),
   scene('receipt', '배당 · 100주', WS['div']['source'], c, head=dv['head'], size=46,
         rows=[[r[0], r[1] + '원', r[2], [0, at(c, 1), at(c, 1.5)][i]] for i, r in enumerate(dv['rows'])],
         side=['31,640원', at(c, 1.6), '100주 분기 배당 · 세금 뗀 뒤']),
   scene('grid', '1년 사이 — 이익과 배당', WS['pairs']['source'], d, head='삼성전자 · 1년 사이',
         cols=['1년 전 3분기', '2026년 2분기'],
         rows=[[eg[0], [eg[1][0][2], eg[1][1][2]], 0], [dg[0], [dg[1][0][2], dg[1][1][2]], at(d, 0.4)]],
         hot=[[0, 1, at(d, 1.2)], [1, 1, at(d, 1.6)]], note=[eg[2] + ' · 배당은 ' + dg[2], at(d, 1.5)]),
   scene('receipt', '줄어든 평가액 = 분기 배당 몇 번', WS['dots']['source'], e, head='줄어든 평가액 ÷ 세후 분기 배당', size=46,
         rows=[['10/2 → 10/8 평가액', '−1,400,000원', 'net', 0], ['세후 분기 배당', '31,640원', 'in', 12]],
         side=[dt['big'], 30, '분기 배당 몇 번치']),
   scene('vs', '3분기 배당은 아직', WS['pending']['source'], f_,
         tiles=[[WS['pending']['data']['cards'][0][0], '370원', WS['pending']['data']['cards'][0][1], 0, 'ink'],
                [WS['pending']['data']['cards'][1][0], '공시 전', '이사회가 정함', at(f_, 0.6), 'accent']]),
  ],
)

# ── G-1: 금 1천만원어치, 언제 샀나요? (줄 0·1·2·3 → 16·17·18 → 68·69·70 → 19·20·21) ──
GL, GS = load('g1')
L = mk(GL)
src = GS['buy']['source']
g0 = L(0, 1, 2, 3)
g1 = L(16, 17, 18)
g2 = L(69, 70)
g3 = L(19, 20, 21)
# 산 날 4개 막대(값 = 오늘 받는 돈, 화면 글자는 g1.json loss 장면 글자 그대로)
loss = GS['loss']['data'] if 'loss' in GS else None
SHORTS['g1s_buyday'] = dict(
  question=['금 1천만원어치,', '언제 샀나요?'], hot='언제',
  base='KRX 금시장 종가 2026-10-06 기준 · 지나간 값',
  answer=dict(label='금 1천만원어치 · 오늘(10/6) 팔면 받는 돈', items=['1월 고점 663만원', '1년 전 956만원'], arrow=False,
              note='KRX 금시장 종가 · 증권사 수수료 별도'),
  scenes=[
   scene('bars', '산 날 4개', src, g0, head='1천만원어치 · 오늘 받는 돈(만원)', full=True,
         bars=[['1월 고점', 663, '663만원', 0, 'fall', '2026-01-29'], ['1년 전', 956, '956만원', 0, 'ink', '2025-10-02'],
               ['3개월 전', 878, '878만원', 0, 'ink', '2026-07-06'], ['1개월 전', 918, '918만원', 0, 'ink', '2026-09-04']], max=1000),
   scene('bars', '넷 다 손실', src, g1, head='1천만원에서 줄어든 비율',
         bars=[['1월 고점', 33.66, '−33.66%', 0, 'fall', None], ['3개월 전', 12.16, '−12.16%', 0, 'ink', None],
               ['1개월 전', 8.19, '−8.19%', at(g1, 1), 'ink', None], ['1년 전', 4.43, '−4.43%', at(g1, 2), 'ink', None]], max=40),
   scene('receipt', '산 값까지의 산수', GS['math']['source'], g2, head='고점에 산 금이 산 값으로 돌아가려면', size=46,
         rows=[['산 값 1g(2026-01-29)', '269,810원', 'in', 0], ['오늘 1g(2026-10-06)', '179,000원', 'tax', 10], ['떨어진 폭', '−33.66%', 'net', at(g2, 1)]],
         side=['+50.7%', 40, '올라야 산 값 · 전망 아님, 산수']),
   scene('vs', '작년 대비', GS['odd']['source'], g3,
         tiles=[['국제 금값(달러, 1년)', '+6.65%', '금 선물 GC=F · 뉴욕 종가', 10, 'rise'],   # 10/12 눈 검사: 첫 줄 2.6초 빈 판 → 장면 시작에 바로
                ['한국에서 산 금(1년)', '−4.43%', 'KRX 금시장 종가', at(g3, 2), 'fall']]),
  ],
)

# ── G-1 둘째 클립: 같은 날 1천만원, 산 길 따라 (줄 52·53 → 40 → 41 → 44 → 47 → 50·51) — PD 10/13, g1s_buyday(산 날)와 다른 질문 ──
def _at_word(ls, i, word):   # 줄 i 안에서 word가 나오는 글자 위치를 말 길이 비율로 프레임에 맞춘다(자막 조각과 같은 어림)
    t = ls[i]['text']; k = t.find(word); assert k >= 0, word
    return sum(l['frames'] for l in ls[:i]) + int(round(k / len(t) * (ls[i]['frames'] - 8)))
p0 = L(52, 53)
p1 = L(40)
p2 = L(41)
p3 = L(44)
pb = L(47)   # 10/13: 첫 판(줄 42 양도세)은 '두 번째→네 번째'로 세 번째가 빠져 들림 → 42 빼고 골드뱅킹 47
p4 = L(50, 51)
SHORTS['g1s_paths'] = dict(
  question=['금 1천만원,', '어느 길로 샀나요?'], hot='어느 길',
  base='KRX 금시장 종가 2026-10-06 기준 · 지나간 값',
  answer=dict(label='2025-10-02 1천만원어치 · 오늘(10/6) 받는 돈', items=['KRX 금시장 956만원', '골드바 869만원'], arrow=False,
              note='금 ETF 947만원 · 골드바는 금값 몫 어림 · 수수료 별도'),
  scenes=[
   scene('bars', '같은 날, 산 길 3개', GS['pathcmp']['source'], p0, head='작년 1천만원어치 · 오늘 받는 돈(만원)', full=True,   # full: 판 +90프레임
         bars=[['골드바', 869, '869만원', 0, 'fall', '금값 몫 어림'], ['KRX 금시장', 956, '956만원', at(p0, 1) + 90, 'ink', None],
               ['금 ETF', 947, '947만원', at(p0, 1) + 120, 'ink', None]], max=1000),
   scene('receipt', '금 사는 길 4개', GS['paths']['source'], p1, head='금 사는 길 4개', size=46,
         rows=[['KRX 금시장', '증권사 계좌', 'in', 0], ['금 ETF', '주식처럼 사고팜', 'in', _at_word(p1, 0, '금 ETF')],
               ['골드뱅킹', '은행 통장', 'in', _at_word(p1, 0, '골드뱅킹')], ['골드바', '실물', 'in', _at_word(p1, 0, '골드바')]]),
   scene('receipt', 'KRX 금시장 세금', GS['krx']['source'], p2, head='KRX 금시장 · 세금', size=46,
         rows=[['부가가치세', '면제', 'in', 0], ['판 차익 양도세', '없음', 'in', 50]],
         side=['세금 0', 85, '사고파는 동안']),
   scene('receipt', '금 ETF', GS['etf']['source'], p3, head='금 ETF · 1천만원 · 단위 원', size=46,
         rows=[['오늘 받는 돈', '9,472,686', 'net', 0], ['KRX 금이었다면', '9,556,861', 'dim', _at_word(p3, 0, 'KRX 금보다')]],
         side=['−5.27%', 20, '1년 전에 산 금 ETF']),
   scene('receipt', '골드뱅킹', GS['bank']['source'], pb, head='골드뱅킹 · 은행 고시 기준', size=46,
         rows=[['기준가격', '국제 금가격 × 환율', 'dim', 0], ['살 때', '+1.00%', 'tax', _at_word(pb, 0, '살 때')], ['팔 때', '−1.00%', 'tax', _at_word(pb, 0, '팔 때')]],
         side=['1%씩', _at_word(pb, 0, '각각'), '살 때 한 번, 팔 때 한 번']),
   scene('receipt', '골드바 부가세', GS['bar']['source'], p4, head='골드바 · 1천만원을 내면', size=46,
         rows=[['부가세', '909,091원', 'tax', 0], ['금값 몫', '9,090,909원', 'in', _at_word(p4, 0, '부가세') - 30],
               ['살 때 수수료·팔 때 값 차이', '별도', 'dim', _at_word(p4, 1, '살 때')]],
         side=['+10%', at(p4, 1), '금값이 올라야 낸 돈만큼']),
  ],
)


# ── W-1: 코스피 1천만원, 사흘 장에 얼마 빠졌나 (줄 22·23 → 4·5 → 6·7 → 1 → 12·13 → 24 → 25) · 10/13 23시 비축 ──
#   w1s_div(배당 44번치)와 다른 질문 · 첫 줄도 다름(w1s_div는 줄 0, 이 편은 줄 22)
WL, WS = load('w1')
L = mk(WL)
kb = WS['kbars']['data']; dvg = WS['diverge']['data']; ks = WS['kbars']['source']
a = L(23, 22)   # 10/14 22시 회의 지시(A27): 첫 줄 = 답 숫자 줄 '지난주 사흘 동안 약 54만원이 줄었습니다.', 가정 줄은 둘째로 — 새 녹음 0
b = L(4, 5)
c = L(6, 7)
d = L(1, 9, 10)   # 10/14: 끝 면책(25)을 빼 39초 → 공시 장면에 매출·전 분기 대비 줄 9·10을 붙여 45초
e = L(12, 13)
f_ = L(24)
SHORTS['w1s_kospi'] = dict(
  question=['코스피 1천만원,', '사흘 장에 얼마 빠졌나?'], hot='사흘',
  base='한국은행 ECOS 코스피 종가 그대로 · 지나간 값',
  answer=dict(label='코스피 1천만원 · 종가 10/2 → 10/8', items=['−54만원 (−5.39%)', '삼성전자 100주 −5.07%'], arrow=False,
              note='107조 실적 낸 종목과 시장이 비슷한 비율 · 이유는 확인 안 함'),
  scenes=[
   scene('vs', '코스피를 따라가는 1천만원', ks, a, full=True,
         tiles=[['코스피 1천만원 · 10/2 → 10/8', kb['big'][0], kb['big'][2], 0, 'fall'],
                ['장이 선 날', '사흘', '10/6 · 10/7 · 10/8', at(a, 1) + 90, 'ink']]),
   scene('receipt', '지난주 달력', WS['week']['source'], b, head='10/5 ~ 10/9 · 코스피 종가', size=46,
         rows=[['화 10/6', '6,941.39', 'in', 20], ['수 10/7', '6,803.90', 'in', 40], ['목 10/8', '6,625.93', 'net', 60],
               ['월 10/5 · 금 10/9', '대체공휴일 · 한글날', 'dim', at(b, 1)]]),   # 23시 눈 검사: 5줄째 잘림·'사흘' 옆 글이 판과 겹침 → 휴일 한 줄·옆 글 뺌
   scene('bars', '코스피 종가', ks, c, head='코스피 · 종가',
         bars=[[x[0], x[1], x[2], [0, 20, 40, 60][i], x[4], '−5.39%' if i == 3 else None] for i, x in enumerate(kb['bars'])], max=kb['max']),
   scene('vs', '같은 주, 삼성전자 공시', WS['dart']['source'], d,
         tiles=[['3분기 영업이익(잠정)', '107.40조원', '1년 전 3분기 12.17조원', 0, 'rise'],
                ['공시한 날', '10/8', 'DART 영업(잠정)실적 공정공시', at(d, 0.55), 'ink']]),
   scene('receipt', '삼성전자 100주', WS['rcpt1']['source'], e, head='삼성전자 100주 · 종가 × 100주', size=46,
         rows=[['10/2 평가액', '2,760만원', 'in', 0], ['10/8 평가액', '2,620만원', 'in', 25], ['평가액 차이', '−140만원', 'net', at(e, 1) + 30]],   # 23시 눈 검사: 첫 줄만 3초 → 둘째 줄 당김
         side=['−5.07%', at(e, 1.5), '삼성전자 100주 · 10/2 → 10/8']),
   scene('diverge', '한 종목 vs 시장 전체', WS['diverge']['source'], f_, head='10/2 → 10/8 · 종가 기준',
         rows=dvg['rows'], max=dvg['max'], q=dvg['q']),
   # 10/14 꼴 관문 ⓑ: 끝 장면 '이유는? 확인 안 함'(줄 25 면책)을 뺌 — 끝은 줄 24 '비슷한 비율로 줄었어요'
  ],
)


def build(name, d):
    sc = d['scenes']
    for s in sc: s['frames'] = sum(l['frames'] for l in s['lines'])
    sc[-1]['frames'] += TAIL
    return {'fps': 30, 'name': name, 'question': d['question'], 'hot': d['hot'], 'answer': d.get('answer'), 'base': d['base'], 'scenes': sc}


if __name__ == '__main__':
    for name, d in SHORTS.items():
        if sys.argv[1:] and name not in sys.argv[1:]: continue   # 10/13: 이름을 주면 그 편만 다시 씀
        p = build(name, d)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
