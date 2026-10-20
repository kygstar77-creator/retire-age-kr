# h1s_helio 판 없는 꼴(10/19 클로드 티 금지 — 예약 쇼츠는 새 틀로 공개 순서대로 다시) (firemap-video-producer 2026-10-20)
#   py -3.12 work/research/cardshorts/h1s_helio/h1helio_live.py   → work/video/h1s_helio_live.json (+ h1s_helio.json 같은 내용)
#   렌더: cd work/video && npx remotion render src/c1s_index.ts C1S out/h1s_helio_live.mp4 --props=h1s_helio_live.json --pixel-format=yuv420p
# 바탕 = h1helioclip.py가 만든 v3 판(video/h1s_helio_v3base.json)(10/16 v3 배경 실사 13컷·말 줄·프레임 그대로, 새 녹음 0)
# 바꾼 것: look 'live' · 억 소수 → '20억'·'23억 8,200만원'(v3redo.fmt_eok, 값 같음) · 판 없는 꼴이 큰 숫자 박자로 그리지 못하는 칸(vs 셋째 줄 설명·line 그래프)을 박자 칸(tiles)으로
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from v3redo import fmt_eok, VID

p = json.load(open(os.path.join(VID, 'h1s_helio_v3base.json'), encoding='utf-8'))   # 10/16 v3 판 props(h1helioclip.py 출력) 사본 — h1s_helio.json은 이 판으로 덮음(업로드 관문이 그 이름을 읽음)
S = p['scenes']
assert [s['kind'] for s in S] == ['bars', 'bars', 'vs', 'line']
assert [l['n'] for l in S[2]['lines']] == [24, 25] and [l['n'] for l in S[3]['lines']] == [30, 20, 31]
st3 = [0, S[3]['lines'][0]['frames'], S[3]['lines'][0]['frames'] + S[3]['lines'][1]['frames']]
pts = S[3]['data']['series'][0][2]
assert min(pts) == 28.0 and pts[5] == 28.0   # 4월(2026.04) = 가장 낮은 달 · h1helioclip.py assert와 같은 값
# 원자료 칸: 큰 글자는 짧게(박자 하나에 값 하나) — 계약·등기 날짜는 설명란에
# 판 없는 꼴 막대 이름은 12자 이하만 보임(parts/safeframe shortKick) — 달을 붙여 5월·2월이 헷갈리지 않게
S[0]['data']['bars'][0][0] = '5월 26층 직거래'; S[0]['data']['bars'][1][0] = '나머지 17건 가운데'
# 첫 렌더(sheet_live1.png): 막대 4개는 위 질문 두 줄과 겹침 → 2개로. 줄 23 '나머지 거래는 모두 30억 이상' = 나머지 3건 중 가장 낮은 15층 30.00억(h1.json h_floor 그대로)
B = {b[0].split(' · ')[0]: b for b in S[1]['data']['bars']}
assert B['9층'][1] == 2382.0 and min(B[k][1] for k in ('18층', '28층', '15층')) == B['15층'][1] == 3000.0
S[1]['data']['bars'] = [['2월 9층', 2382.0, B['9층'][2], 0, 'accent'], ['나머지 3건 최저', 3000.0, B['15층'][2], S[1]['lines'][0]['frames'], 'ink']]
S[2]['kind'] = 'vs'
S[2]['data'] = {'tiles': [['2월 9층 거래', '등기 마침', '', 0, 'ink'], ['왜 이 값이었나', '자료에 없음', '', S[2]['lines'][0]['frames'], 'ink']]}
# 달마다 가운데 값: 선 그래프 대신 박자 셋(한 달 전체 → 가운데 값 뜻 → 가장 낮은 달)
S[3]['kind'] = 'vs'
S[3]['data'] = {'tiles': [['한 건 말고', '한 달 전체', '', 0, 'ink'], ['1년 85건 가운데 값', '28.50억', '', st3[1] + 60, 'ink']],
                'side': ['4월 28.00억', st3[2], '가장 낮은 달']}
# 10/20 14:4x 이해 시험 1차(40·50·60세 3/3 뜻은 맞음) 반영 — 새 녹음 0, 줄 순서·화면 글자만:
#  셋 다 ① 위 문구 '거래 한 건'인데 두 건 ② '7억 넘게'가 화면 23억 8,200만원 vs 30억(6억 남짓)과 안 맞음 → 7억은 28층 31.50억과의 차이라 그 막대로
#  ③ '가운데 값' 뜻이 끝에야 나옴 → 줄 20을 장면 1 끝으로 ④ 직거래 설명이 늦음 → 29를 27 바로 뒤로 ⑤ '손품 씨' 모름 → 줄 30 뺌 ⑥ '등기 마침' 뜻 → '실제로 끝난 거래'
by = {l['n']: l for s_ in S for l in s_['lines']}
S[0]['lines'] = [by[26], by[27], by[29], by[28], by[20]]
assert B['28층'][1] - B['9층'][1] > 700   # 31.50억 − 23.82억 = 7.68억 → 말 '7억 넘게'
S[1]['data']['bars'] = [['2월 9층', 2382.0, B['9층'][2], 0, 'accent'], ['같은 달 28층', 3150.0, B['28층'][2], 0, 'ink']]
S[2]['data'] = {'tiles': [['2월 9층 거래', '등기까지 마침', '', 0, 'ink'], ['왜 이 값이었나', '자료에 없음', '', S[2]['lines'][0]['frames'], 'ink']]}
S[3]['lines'] = [by[31]]
# 2차(새 3명 뜻 맞음) 반영: 장면 3 '이 거래'가 어느 건지 → 꼬리말 '2월 9층 거래' · 장면 4 5초에 숫자 둘 → 하나(위 질문의 답: 가장 낮은 달도 28억)
S[3]['data'] = {'side': ['4월 28.00억', 20, '가장 낮은 달도']}
for s_ in S: s_['frames'] = sum(l['frames'] for l in s_['lines'])
k = 0
for s_ in S:
    for l in s_['lines']: k += 1; l['n'] = k
TAIL = 36; S[-1]['frames'] += TAIL   # 끝 출처 3초가 말과 겹치지 않게(t1s_swap과 같음)
fb = sum(s_['frames'] for s_ in S); at = 0; segs = []
for i, b in enumerate(p['bg']):   # 배경 13컷을 줄 수에 맞춰 다시 나눔(줄 하나에 컷 하나, 같은 클립·시작 초 그대로)
    pass
lines = [l for s_ in S for l in s_['lines']]
for i, l in enumerate(lines):
    b = dict(p['bg'][i]); fr = l['frames'] + (TAIL if i == len(lines) - 1 else 0)
    b['from'] = at; b['frames'] = fr; segs.append(b); at += fr
segs[4]['start'] = 1.0   # 35451155 쓸 수 있는 길이 7.4초(bg_plan) — 192프레임(6.4초)이 2.47초부터면 넘침
p['bg'] = segs
p['question'] = ['튀는 거래 20억·23억,', '헬리오시티 값일까?']; p['hot'] = '튀는 거래'
# 10/20 14:5x bgcheck ⑥: 흰 막대(LiveBars)를 흰 판으로 잡음 — 프레임 61%(10/21부터 거부) → 막대 두 장면도 큰 숫자 박자(tiles)로. 값·말 줄 그대로
S[0]['kind'] = 'vs'; S[0]['data'] = {'tiles': [['5월 직거래 한 건', '20.00억', '', 0, 'ink'], ['5월 17건 가운데 값', '28.10억', '', 0, 'ink']]}
S[0]['data']['tiles'][1][3] = sum(l['frames'] for l in S[0]['lines'][:3])   # 줄 28 '같은 달 다른 거래들과는'에
S[1]['kind'] = 'vs'; S[1]['data'] = {'tiles': [['2월 9층', '23.82억', '', 0, 'ink'], ['같은 달 28층', '31.50억', '', 60, 'ink']]}   # 첫 줄 22 '7억 넘게 차이'(134프레임) 안에 맞붙임
p = fmt_eok(p)
p['look'] = 'live'; p['name'] = 'h1s_helio_live'
p['answer'] = fmt_eok({'label': '헬리오시티 84㎡대 · 1년 85건', 'items': ['한 건 20.00억 · 23억대', '가운데 값 28.50억'], 'arrow': False, 'note': '달마다 가운데 값은 4월이 가장 낮음'})
for fn in ('h1s_helio_live.json', 'h1s_helio.json'): json.dump(p, open(os.path.join(VID, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in p['scenes'])
print(f'h1s_helio_live: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(S)}')
for s in p['scenes']: print(s['kind'], json.dumps(s['data'], ensure_ascii=False)[:200])
