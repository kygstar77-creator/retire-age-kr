# M-1 롱폼(eTjVs1vDTwg)을 잘라 세로 쇼츠 4편 props를 만든다 (firemap-video-producer 2026-10-10).
#   py -3.12 work/research/cardshorts/m1clips.py            # → work/video/m1s_<편>.json 4개 + m1s.json(첫 편, Root 기본값)
# 목소리 = ep/M-1/voice.json 기존 wav 그대로(새 녹음 없음). 줄 번호 = voice.json 전체 순번(0부터).
# 화면 숫자 = video/m1.json(편집 통과한 롱폼 화면 글자) · calc_out.txt 문구만. 이 파일에서 숫자를 새로 계산하지 않는다.
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'M-1')
VID = os.path.join(WORK, 'video')

voice = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
LINES = [l for s in voice['sections'] for l in s['lines']]
m1 = json.load(open(os.path.join(VID, 'm1.json'), encoding='utf-8'))
CAP = {l['text']: l.get('cap') for s in m1['scenes'] for l in s['lines']}
SRC = {s['key']: s.get('source') for s in m1['scenes']}
SC = {s['key']: s for s in m1['scenes']}
TAIL = 36            # 마지막 줄 뒤 1.2초 여유


def L(*idx):
    out = []
    for i in idx:
        l = LINES[i]
        out.append({'n': i, 'text': l['text'], 'cap': CAP.get(l['text']), 'audio': l['audio'], 'frames': l['frames']})
    return out


def scene(kind, label, src, lines, **data):
    return {'kind': kind, 'label': label, 'source': SRC[src] if src in SRC else src, 'data': data, 'lines': lines}


jm, am = SC['jm']['data'], SC['am']['data']

SHORTS = {
 # ① 월 100만원 받으려면 얼마? — 세 상품 거꾸로 계산(롱폼 3장)
 'm1s_need100': dict(
  question=['월배당으로 매달 100만원,', '얼마 있어야 할까?'], hot='얼마',
  scenes=[
   scene('ask', '거꾸로 묻기', 'open', L(2), goal='매달 100만원', goalSub='세금·건보료 뗀 뒤 손에 남는 돈', ask='지금 얼마 있어야?',
         names=['JEPQ', 'SCHD', 'ACE 미국배당다우존스']),
   scene('flow', '거꾸로 계산하는 법', 'flow', L(36), top=['월 100만원', '세금·건보료 뗀 뒤 손에 남는 돈'], mid='+ 세금 + 건강보험료',
         bottom=['1년 세전 분배', '15,611,746원', '국내 상장은 15,693,413원'], rule='필요한 돈 = 연 세전 분배 ÷ 분배율'),
   scene('card', 'SCHD — 월 100만원이면', 'schd', L(37, 38, 39), name='SCHD', desc='미국 배당주를 모아 담은 ETF · 미국 상장', freq='연 4회(분기)',
         rate='3.22%', rateCalc='분배금 1.0541달러 ÷ 종가 32.72달러', need='4.85억원', rateAt=1, needAt=2, hot=False, track=0, count=4),
   scene('card', 'JEPQ — 월 100만원이면', 'jepq', L(42, 43, 44), name='JEPQ', desc='나스닥 주식 + 옵션 매도(커버드콜) · 미국 상장', freq='연 12회',
         rate='11.28%', rateCalc='분배금 6.88454달러 ÷ 종가 61.04달러', need='1.38억원', rateAt=1, needAt=2, hot=True, track=1, count=12),
   scene('card', 'ACE 미국배당다우존스 — 월 100만원이면', 'ace', L(45, 48, 49), name='ACE 미국배당다우존스', desc='Dow Jones U.S. Dividend 100 · 국내 상장',
         freq='연 12회', rate='3.08%', rateCalc='분배금 441원 ÷ 종가 14,330원', need='5.10억원', rateAt=1, needAt=2, hot=False, track=2, count=12,
         note='같은 지수 상품은 다른 운용사에도 있음 · 예시 1종'),
   scene('bars', '월 100만원에 필요한 돈 — 평균 기준', 'three', L(50), max=6,
         bars=[['JEPQ', 1.38, '1.38억원', 'accent'], ['SCHD', 4.85, '4.85억원', 'ink'], ['ACE 미국배당다우존스', 5.1, '5.10억원', 'ink']],
         note=['분배율이 높을수록', '필요한 돈이 적다?'], stamp='2026년 10월 2일 기준 · 지난 기록 계산 · 투자 권유 아님'),
  ],
  track=[['SCHD', 4.85, '4.85억원'], ['JEPQ', 1.38, '1.38억원'], ['ACE 미국배당다우존스', 5.1, '5.10억원']],
 ),
 # ② 가장 적게 나온 달로 다시 재면 — JEPQ 1.38→1.71억, ACE 5.10→8.92억(롱폼 4장)
 'm1s_minmonth': dict(
  question=['월배당, 가장 적게 나온 달로', '다시 재면 얼마?'], hot='가장 적게 나온 달',
  scenes=[
   scene('jump', 'ACE 미국배당다우존스 · 월 100만원에 필요한 돈', 'am', L(60), name='ACE 미국배당다우존스', what='월 100만원에 필요한 돈',
         a=[5.1, '5.10억원', '평균 기준'], b=[8.92, '8.92억원', '가장 적은 달 기준'], mult='×1.75 · 최소값', max=10),
   scene('morph', '월배당 = 매달 같은 돈?', 'am', L(61), name='ACE 미국배당다우존스 1주당 분배금, 달마다', vals=am['vals'], labels=am['labels'],
         texts=am['texts'], min=am['min'], max=am['max'], hi=am['hi'], ask='매달 같은 돈?', ans='실제 기록은 달마다 달랐다'),
   scene('months', 'JEPQ 1주당 분배금, 달마다', 'jm', L(52, 53, 54, 55, 56), name='JEPQ', unit='1주당 분배금(달러)', vals=jm['vals'], labels=jm['labels'],
         texts=jm['texts'], min=jm['min'], max=jm['max'], lo=jm['lo'], hi=jm['hi'], minAt=1, maxAt=2, ratio=['최대 ÷ 최소 1.51배', 2.4],
         note=['생활비는 가장 적은 달에도 나간다', 3], jump=['1.38억원', '1.71억원', '×1.23', 4]),
   scene('months', 'ACE 미국배당다우존스 1주당 분배금, 달마다', 'am', L(57, 58, 59, 60), name='ACE 미국배당다우존스', unit='1주당 분배금(원)',
         vals=am['vals'], labels=am['labels'], texts=am['texts'], min=am['min'], max=am['max'], lo=am['lo'], hi=am['hi'], minAt=1, maxAt=2,
         ratio=['최대 ÷ 최소 2.52배', 2.4], note=None, jump=['5.10억원', '8.92억원', '×1.75 · 최소값', 3]),
   scene('pair', '평균으로 잴까, 가장 적은 달로 잴까', 'pair', L(62), max=10,
         groups=[['JEPQ', [[1.38, '1.38억원', 'ink'], [1.71, '1.71억원', 'accent']]], ['ACE 미국배당다우존스', [[5.1, '5.10억원', 'ink'], [8.92, '8.92억원', 'accent']]]],
         legend=[['평균 기준', 'ink'], ['가장 적은 달 기준', 'accent']], call=[['평균 말고 가장 적은 달을 먼저', 0.35]],
         stamp='2026년 10월 2일 기준 · 지난 기록 계산 · 투자 권유 아님'),
  ],
 ),
 # ③ 건강보험료는 얼마부터 붙나 — 세금 떼고 월 70만원 선(롱폼 2장)
 'm1s_nhis70': dict(
  question=['배당 받으면 건강보험료,', '얼마부터 붙을까?'], hot='얼마부터',
  scenes=[
   scene('first', '제일 먼저 부딪히는 것', 'gauge', L(22), a='세금', b='건강보험료', sub='지역가입자 · 재산·다른 소득 없음 가정'),
   scene('gauge', '건강보험료가 붙는 선', 'gauge', L(23, 24, 25, 26, 27), max=1800, line=[1000, '연 1,000만원'],
         fill=[[900, 0.3, 'ink'], [1100, 1.35, 'ink'], [1100, 1.6, 'rise'], [1561, 4.3, 'rise']],
         rows=[[0.45, '1,000만원까지', '보험료 소득에 안 넣음', 'ink'], [1.5, '넘으면', '넘은 몫만이 아니라 전부 합산', 'rise'],
               [2.25, '세후 월 70.8만원', '미국 상장 · 국내 상장은 70.5만원', 'accent'], [4.3, '오늘 목표 연 1,561만원', '선을 넘는다', 'rise']],
         head='이자 + 배당, 1년 합계(세전)', under=['1,000만원까지 보험료 소득에 안 넣음', 3.05, 4.25]),
   scene('premium', '선을 넘으면 붙는 몫', 'premium', L(28), who='재산·다른 소득 없을 때', a=['월 22,800원', '최저 보험료', 22800], b=['월 105,832원', '총 보험료(건강 + 장기요양)', 105832],
         at=0.45, note='건강보험 7.19% + 장기요양 · 연 세전 분배 1,561만원 기준'),
   scene('timeline', '보험료는 1년 늦게 따라온다', 'when', L(31, 32, 33), y0='2026', y1='2027', hit=10,
         segs=[['2026년', '배당 받는 해'], ['2027년 1~10월', '고지서 그대로'], ['2027년 11월~', '이때부터 반영']], fillAt=1, hitAt=1.45,
         note=['첫해에 괜찮아도 1년쯤 뒤 바뀜', 2]),
  ],
 ),
 # ④ 분배금 많이 받으면 더 번 걸까 — 1년 원화 총수익(롱폼 6장)
 'm1s_total1y': dict(
  question=['분배금 많이 받으면', '더 번 걸까?'], hot='더 번 걸까',
  scenes=[
   scene('bars', '월 100만원에 필요한 돈 — 평균 기준', 'three', L(76), max=6,
         bars=[['JEPQ', 1.38, '1.38억원', 'accent'], ['SCHD', 4.85, '4.85억원', 'ink'], ['ACE 미국배당다우존스', 5.1, '5.10억원', 'ink']],
         note=['같은 목표에', '필요한 돈 가장 적은 JEPQ'], stamp=None),
   scene('ask1', '1년 전 1억을 넣었다면', 'total', L(77, 78), names=['SCHD', 'ACE 미국배당다우존스', 'JEPQ'], put='1억', ask='지금 얼마?', when='1년 전(2025-10-02)에 넣었다면', now='2026-10-02',
         chips=['분배금 + 가격 변화', '원화 · 세전'], chipAt=1),
   scene('total', '1년 전 1억을 넣었다면', 'total', L(79, 80, 81), max=22,
         bars=[['SCHD', 19.46, '+19.46%', 'accent', '119,456,864원', 0], ['ACE 미국배당다우존스', 18.55, '+18.55%', 'ink', '118,547,352원', 1],
               ['JEPQ', 14.65, '+14.65%', 'ink', '114,649,910원', 2]]),
   scene('pair', '분배금과 가격 변화, 따로 보면', 'split', L(82, 83, 84, 85), max=18,
         groups=[['JEPQ', [[3.03, '+3.03%', 'ink'], [11.62, '11.62%', 'accent']]], ['SCHD', [[15.73, '+15.73%', 'ink'], [3.73, '3.73%', 'accent']]],
                 ['ACE 미국배당다우존스', [[15.01, '+15.01%', 'ink'], [3.54, '3.54%', 'accent']]]],
         legend=[['가격 변화', 'ink'], ['분배금', 'accent']], pre=True, dimPlan=[[0, -1], [0, -1], [-1, 0], [-1, -1]],
         call=[['커버드콜: 오를 때 몫 일부를 내주고 분배금을 만듦', 1], ['지난 기록 — 옆으로 기는 해엔 반대일 수도', 3]],
         stamp='2025-10-02 → 2026-10-02 · 원화 · 세전 · 투자 권유 아님'),
  ],
 ),
}


def build(name, d):
    sc = d['scenes']
    for s in sc: s['frames'] = sum(l['frames'] for l in s['lines'])
    sc[-1]['frames'] += TAIL
    p = {'fps': 30, 'name': name, 'question': d['question'], 'hot': d['hot'], 'track': d.get('track'),
         'base': '2026년 10월 2일 기준 · 지난 1년 실제 기록 계산', 'long': '전체 계산은 7분 영상에서 · 설명란 첫 줄 링크', 'scenes': sc}
    return p


if __name__ == '__main__':
    first = None
    for name, d in SHORTS.items():
        p = build(name, d)
        fr = sum(s['frames'] for s in p['scenes'])
        fn = os.path.join(VID, name + '.json')
        json.dump(p, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"{name}: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
        first = first or p
    json.dump(first, open(os.path.join(VID, 'm1s.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
