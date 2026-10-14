# h1s_helio — H-1 롱폼(rVg0pQVo_wk) 가락동 장 '헬리오시티 84㎡대 같은 달 23.82억과 31.50억'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-15)
#   py -3.12 work/research/cardshorts/h1s_helio/h1helioclip.py   → work/video/h1s_helio.json (틀 C1S — h1clips.py h1s_gap과 같은 길)
# 틀: M1S로 먼저 짰으나 log.jsonl 최근 9편 중 m1clip 5편 → 이 편까지 6/10 = 꼴 관문 ⓓ 거부. C1S(c1clip 5/10)로.
# shorts_cuts.md 'A. 가락동'에서 N1(새 녹음 필요)·지도·가락쌍용1차를 빼고 질문 하나(같은 달 7억 차이 한 건이 그 단지 값인가)만.
# 목소리 = H-1 롱폼 문장 wav 그대로(Chirp 3 HD Charon, 새 녹음 0). 줄 번호 = video/h1.json 전체 순번(0부터), assert로 글자 확인.
# 화면 숫자 = h1.json h_floor·h_deal·h_may·h_line·h_map 데이터 그대로(새 계산 0).
# 줄 순서: 5월 20억 직거래(26~29, 첫 줄 17자·숫자 — 꼴 ⓐ: 줄 22는 42자라 첫 줄 못 함) → 2월 7억 차이(22·23) → 원자료 칸·층(24·25) → 한 달 전체·가운데 값(30·20·31)으로 끝(꼴 ⓑ 끝 줄 면책 아님).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import load, mk, at, scene, build, VID

HL, HS = load('h1')
L = mk(HL)
assert HL[22]['text'].startswith('같은 달, 같은 단지') and HL[24]['text'].startswith('이 거래는 중개사') and HL[26]['text'].startswith('봄에는 20억')
assert HL[30]['text'].startswith('그래서 손품 씨는 한 건') and HL[20]['text'].startswith('가운데 값은 거래를') and HL[31]['text'].startswith('달마다 가운데 값')
FL = HS['h_floor']; DL = HS['h_deal']; MY = HS['h_may']; LN = HS['h_line']; MP = HS['h_map']
deals = {r[0]: r for r in FL['data']['deals']}   # 층: [층, 값, 일]
card = dict(DL['data']['cards'][0])
assert card['거래금액'] == '23.82억' and card['거래 유형'] == '중개거래' and card['등기일'] == '2026.04.14' and deals[9][1] == '23.82억' and deals[28][1] == '31.50억'
pts = LN['data']['series'][0][2]   # [달, 가운데 값(억), 건수]
M = {p[0]: p for p in pts}
assert M['2026.04'][1:] == [28.0, 25] and M['2026.05'][1:] == [28.1, 17] and min(p[1] for p in pts) == 28.0
may = [d for d in MY['data']['dots'] if d[0] == '2026.05']; low = [d for d in may if d[4] == 1]
assert len(may) == 18 and low == [['2026.05', 28, 200000, 26, 1]]
assert '28.50억' in json.dumps(MP['data'], ensure_ascii=False) and '1년 85건' in json.dumps(MP['data'], ensure_ascii=False)

a = L(22, 23); b = L(24, 25); c = L(26, 27, 28, 29); e = L(30, 20, 31)
eok = lambda s: float(s.replace('억', '')) * 100
SH = dict(
  question=['20억·23억 거래 한 건,', '헬리오시티 값일까?'], hot='한 건',
  base='국토교통부 실거래 2025.11~2026.10 계약 · 84㎡대',
  answer=dict(label='헬리오시티 84㎡대 · 1년 85건', items=['한 건 20.00억 · 23.82억', '가운데 값 28.50억'], arrow=False, note='한 달 전체로 보면 4월 28.00억이 가장 낮음'),
  scenes=[
   scene('bars', '봄에는 20억 거래도', MY['source'], c, head='헬리오시티 84㎡대 · 2026년 5월 계약 18건', max=3300, full=True,   # full = 판 90프레임 당김(0초부터 20억 막대가 다 보이게)
         bars=[['5월 28일 · 26층 · 직거래', 2000, '20.00억', 0, 'accent'],
               ['5월 나머지 17건 가운데 값', 2810, '28.10억', at(c, 2) + 90, 'ink']]),   # 10/15 눈 검사: 첫 판 12.5초 그대로 → 둘째 막대 5.5초에(같은 화면 8초 이하)
   scene('bars', '같은 달 4건', FL['source'], a, head='헬리오시티 84㎡대 · ' + FL['sub'].split(' · ')[1], max=3300,
         bars=[[f'{fl}층 · {deals[fl][2]}', eok(deals[fl][1]), deals[fl][1], 0 if fl == 9 else at(a, 1), 'accent' if fl == 9 else 'ink'] for fl in (9, 18, 28, 15)]),   # 10/15 눈 검사: 9.7초 같은 판 → 나머지 3건은 줄 23('나머지 거래는 모두 30억 이상')에
   scene('vs', '원자료 칸 그대로', DL['source'], b,
         tiles=[[f"{card['거래금액']} · {card['층']} · {card['거래 유형']}", '등기 마침', f"계약 {card['계약일']} · 등기 {card['등기일']}", 0, 'accent'],
                [FL['data']['why'][0], '자료에 없음', '층이 달랐다는 것만 · ' + FL['data']['why'][1], at(b, 1), 'ink']]),
   scene('line', '달마다 가운데 값', LN['source'], e, head='달마다 가운데 값 · 동떨어진 거래 1건 뺌',
         series=[['헬리오시티 84㎡대', 'accent', [p[1] for p in pts]]], min=26, max=32, draw=0, dur=60,
         ticks=[[26, '26억'], [28, '28억'], [30, '30억'], [32, '32억']], xlabels=[[0, '2025.11'], [5, '2026.04'], [10, '2026.09']],
         tags=[[5, 28.0, '4월 28.00억 · 25건', at(e, 2), 'down', True], [3, 30.35, '2월 30.35억 · 4건', at(e, 1.5), 'up', False]]),
  ],
)

if __name__ == '__main__':
    p = build('h1s_helio', SH)
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'h1s_helio.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"h1s_helio: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
