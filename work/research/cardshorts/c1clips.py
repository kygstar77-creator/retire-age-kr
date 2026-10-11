# C-1 롱폼(DBJaHJ2pVTw)을 잘라 세로 쇼츠 4편 props를 만든다 (firemap-video-producer 2026-10-11, m1clips.py를 본뜸).
#   py -3.12 work/research/cardshorts/c1clips.py            # → work/video/c1s_<편>.json 4개 + c1s.json(첫 편, Root 기본값)
# 목소리 = ep/C-1/voice.json 기존 wav 그대로(Chirp 3 HD Charon, 새 녹음 없음). 줄 번호 = video/c1.json 장면 순서대로 센 전체 순번(0부터).
# 화면 숫자 = video/c1.json(편집 통과한 롱폼 화면 글자 = calc_out 문구) 그대로. 이 파일에서 숫자를 새로 계산하지 않는다(프레임 배치만 바꾼다).
import os, json, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
VID = os.path.join(WORK, 'video')

c1 = json.load(open(os.path.join(VID, 'c1.json'), encoding='utf-8'))
LINES = [l for s in c1['scenes'] for l in s['lines']]
SC = {s['key']: s for s in c1['scenes']}
D = lambda k: copy.deepcopy(SC[k]['data'])
TAIL = 36            # 마지막 줄 뒤 1.2초 여유


def L(*idx):
    return [{'n': i, 'text': LINES[i]['text'], 'cap': LINES[i].get('cap'), 'audio': LINES[i]['audio'], 'frames': LINES[i]['frames']} for i in idx]


def at(lines, x):
    """줄 번호(소수면 그 줄 안 비율) → 장면 안 프레임"""
    i = min(int(x), len(lines) - 1); a = sum(l['frames'] for l in lines[:i])
    return int(round(a + (x - i) * lines[i]['frames']))


def scene(kind, label, src, lines, **data):
    return {'kind': kind, 'label': label, 'source': SC[src]['source'] if src in SC else src, 'data': data, 'lines': lines}


def same(kind, key, lines, label=None, **over):
    """롱폼 장면을 줄 그대로 가져올 때 — 데이터 시각(프레임)도 롱폼 그대로(줄 구성이 같으므로)"""
    d = D(key); d.update(over)
    return scene(kind, label or SC[key]['title'], key, lines, **d)


TL = D('tiles')
TILE_FOOT = '색칸 = 20년 안에 바닥 · 칸 숫자 = 버틴 햇수(+는 2025년 말까지 남음)'
TILE_HEAD = '3억 · 월 200만원 · 시작한 해 1989~2006년'


def tilerows(on):
    """on = [배당 켜짐, 매도 켜짐, 배당 개수, 매도 개수] 프레임"""
    (n1, c1_, cells1, _), (n2, c2, cells2, _) = TL['rows']
    return [[n1, c1_, cells1, on[0], TL['count'][0][0], on[2]], [n2, c2, cells2, on[1], TL['count'][1][0], on[3]]]


SHORTS = {}

# ① 평균이면 평생, 실제 순서로 돌리면 — 시작 해 18칸(배당 9/18 · 매도 6/18) → 평균 가정 → 해마다 수익률 → 2000년 시작 두 사람
l1 = L(48, 47)
m18 = D('me18'); m18['rows'] = [[r[0], r[1], r[2], 0 if i < 2 else (6 if i == 2 else 70)] for i, r in enumerate(m18['rows'])]
SHORTS['c1s_half'] = dict(
  question=['평균이면 평생,', '실제로 돌리면?'], hot='실제로',
  answer=dict(label='3억 · 월 200만원 · 시작한 해 18개 중 20년 안에 바닥', items=['배당 씨 9/18', '매도 씨 6/18'], arrow=False, note='S&P500 총수익 · 원화 · 1989~2006년 시작'),
  scenes=[
   scene('tilegrid', '20년 안에 바닥난 시작 해', 'tiles', l1, head=TILE_HEAD, rows=tilerows([0, 0, 0, 0]), foot=TILE_FOOT, full=True),
   same('tank', 'open', L(0), head='평균대로 매년 같다고 놓으면', tank=SC['open']['data']['tank'], scoreAt=20,
        score=['평균대로', SC['open']['data']['score'][0][1]]),
   same('years', 'years', L(42, 43), head='해마다 수익률 · 원화 · S&P500 총수익'),
   scene('persona', '배당 씨 18명', 'me18', L(49), **m18),
   same('persona', 'me00', L(50, 51, 52)),
   same('line', 'path00', L(53, 54, 55), head='2000년 시작 · 통장 잔액', tags=[t[:4] + (['left'] if t[2].startswith('배당') else [t[4]]) + t[5:] for t in D('path00')['tags']]),
  ],
)

# ② 배당으로 받으면 첫해 얼마 더 빠지나 — 7,223,493원 vs 0원
m1 = D('me1'); m1['rows'] = [[r[0], r[1], r[2], 0] for r in m1['rows']]; m1['stamp'] = [m1['stamp'][0], 0]
ra = D('rcptA'); off = SC['rcptA']['lines'][0]['frames']
ra['rows'] = [[r[0], r[1], r[2], max(0, r[3] - off)] for r in ra['rows']]; ra['side'] = [ra['side'][0], ra['side'][1] - off, ra['side'][2]]
th = D('thresh'); th['marks'] = th['marks'][:1]; th['note'] = None
SHORTS['c1s_receipt'] = dict(
  question=['배당으로 받으면', '첫해 얼마 빠질까?'], hot='얼마',
  answer=dict(label='3억 · 손에 쥐는 돈 월 200만원 · 첫해 더 빠진 돈', items=['배당 씨 7,223,493원', '매도 씨 0원'], arrow=False, note='미국 원천징수 15% + 지역 건보료 8.1348%'),
  scenes=[
   scene('persona', '배당 씨의 한 달', 'me1', L(76), full=True, **m1),
   scene('receipt', '배당 씨 첫해 영수증', 'rcptA', L(23, 24, 25), **ra),
   scene('thresh', '금융소득 문턱', 'thresh', L(26, 27), head='이자 + 배당, 1년 합계', **{k: v for k, v in th.items()}),
   same('twin', 'rcptB', L(30, 31, 32)),
   same('receipt', 'hlist', L(33)),
  ],
)

# ③ 3억에서 월 300만원 꺼내면 — 평균이어도 배당 12년차 · 매도 20년차 / 실제 순서 15/18 · 10/18
a3 = D('avg300'); a3['bars'] = [[b[0], b[1], b[2], 0, b[4], b[5]] for b in a3['bars']]
SHORTS['c1s_300'] = dict(
  question=['3억에서 월 300만원', '꺼내면 몇 년?'], hot='몇 년',
  answer=dict(label='3억 · 월 300만원 · 평균 13.57%가 매년 같다고 놓아도', items=['배당 씨 12년차', '매도 씨 20년차'], arrow=False, note='실제 순서로는 20년 안에 바닥 — 배당 15/18 · 매도 10/18'),
  scenes=[
   scene('bars', '월 300만원이면', 'avg300', L(62, 63), head='3억 · 월 300만원 · 바닥나는 해', full=True, **a3),
   same('duo', 'duo', L(12, 13), a=[D('duo')['a'][0], D('duo')['a'][1], 0], tag=[D('duo')['tag'][0], 20]),   # 쇼츠: 배당 씨는 장면 시작부터(빈 판 3초 없앰)
   scene('receipt', '두 사람 조건', 'rules', L(16), head='두 사람 조건', side=None, size=48,
         rows=[['건강보험', '지역가입자', 'in', 0], ['넣은 곳', 'S&P500 총수익', 'in', 15], ['배당 씨', '분배금으로 받기', 'hi', 30], ['매도 씨', '필요한 만큼 팔기', 'hi', 45]]),
   scene('tilegrid', '20년 안에 바닥난 시작 해', 'tiles', L(45, 46, 47), head=TILE_HEAD, foot=TILE_FOOT,
         rows=tilerows([at(L(45, 46, 47), 1), at(L(45, 46, 47), 2), at(L(45, 46, 47), 1.5), at(L(45, 46, 47), 2.4)])),
   same('grid', 'grid', L(64, 65, 66, 67), head='20년 안에 바닥 · 시작한 해 18개 중'),
  ],
)

# ④ 환율이 통장을 받쳐 주기도, 깎기도 — 1997년 달러 +33.4% → 원화 +123.6%
fx = D('fxline'); fx['tags'] = [t[:3] + [0] + t[4:] for t in fx['tags']]
vs = D('vs'); off = SC['vs']['lines'][0]['frames']; vs['tiles'] = [t[:3] + [max(0, t[3] - off)] + t[4:] for t in vs['tiles']]; vs.pop('score', None)
g97 = D('fx97'); g97['note'] = [g97['note'][0], 200]
SHORTS['c1s_fx'] = dict(
  question=['외환위기 1년에', '통장이 두 배?'], hot='두 배',
  answer=dict(label='1997년 S&P500 총수익 · 원/달러 844.2 → 1,415.2원', items=['달러 +33.4%', '원화 +123.6%'], arrow=True, note='2008년은 반대 — 달러 −37.00% · 원화 −15.6%'),
  scenes=[
   scene('line', '원/달러 연말 환율', 'fxline', L(69), head='원/달러 연말 환율', full=True, **fx),
   scene('vs', '1년 차이', 'vs', L(2, 3), **vs),
   same('grid', 'fx97', L(4, 5), head='3억 · 월 200만원 · 배당으로 받기', note=g97['note']),
   same('diverge', 'fx08', L(44), head='2008년 S&P500 총수익'),
   same('grid', 'usd', L(71, 72, 73), head='20년 안에 바닥 · 시작한 해 18개 중'),
  ],
)


def build(name, d):
    sc = d['scenes']
    for s in sc: s['frames'] = sum(l['frames'] for l in s['lines'])
    sc[-1]['frames'] += TAIL
    return {'fps': 30, 'name': name, 'question': d['question'], 'hot': d['hot'], 'answer': d.get('answer'),
            'base': '1989~2025년 실제 기록 계산 · 지나간 기록', 'scenes': sc}


if __name__ == '__main__':
    first = None
    for name, d in SHORTS.items():
        p = build(name, d)
        fr = sum(s['frames'] for s in p['scenes'])
        json.dump(p, open(os.path.join(VID, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
        first = first or p
    json.dump(first, open(os.path.join(VID, 'c1s.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
