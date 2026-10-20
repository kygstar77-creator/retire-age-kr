# p1s_step 판 없는 꼴(10/19 클로드 티 금지 — 예약 쇼츠는 새 틀로 공개 순서대로 다시) (firemap-video-producer 2026-10-20)
#   py -3.12 work/research/cardshorts/p1s_step/p1step_live.py   → work/video/p1s_step_live.json (+ p1s_step.json 같은 내용 — 업로드 관문이 그 이름을 읽음)
#   렌더: cd work/video && npx remotion render src/c1s_index.ts C1S out/p1s_step_live.mp4 --props=p1s_step_live.json --pixel-format=yuv420p
# 바탕 = p1stepclip.py가 만든 v3 판(video/p1s_step_v3base.json) — 말 줄·프레임·배경 실사 그대로(새 녹음 0, 새 숫자 0)
# 바꾼 것: look 'live' · 흰 막대(bgcheck ⑥ 흰 판으로 잡힘, h1s_helio 10/20 61%)를 큰 숫자 박자(tiles)로 · 꼬리말 12자 이하(parts/safeframe shortKick)
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from v3redo import fmt_eok, VID

p = json.load(open(os.path.join(VID, 'p1s_step_v3base.json'), encoding='utf-8'))
S = p['scenes']
assert [s['kind'] for s in S] == ['bars', 'bars', 'vs', 'bars', 'vs']
B = lambda i: {b[0]: b for b in S[i]['data']['bars']}
b0, b1, b3 = B(0), B(1), B(3)
assert b0['519만원 바로 위'][2] == '15만원' and b1['2026년 6월 전 기준'][2] == '319만원' and b1['2026년 6월 17일부터'][2] == '519만원'
assert b3['600만원'][2] == '27만원' and b3['800만원'][2] == '50만원'
t2 = {t[0]: t for t in S[2]['data']['tiles']}; t4 = {t[0]: t for t in S[4]['data']['tiles']}
assert t2['월급만 있다면 · 한 해 총급여'][1] == '7,600만원쯤' and t4['깎이는 기간'][1] == '최대 5년'
st = lambda i, k: sum(l['frames'] for l in S[i]['lines'][:k])   # 장면 i의 k번째 줄 시작 프레임
S[0]['data'] = {'tiles': [['519만원 바로 아래', '0원', '', 0, 'ink'], ['519만원 넘으면', '15만원', '', 30, 'ink']]}
S[1]['data'] = {'tiles': [['6월 전 기준', '319만원', '', st(1, 1), 'ink'], ['6월 17일부터', '519만원', '', st(1, 2), 'ink']]}
S[2]['data'] = {'tiles': [['깎일지 보는 소득', '월급 그대로 ✕', '', 0, 'ink'], ['근로소득공제 빼고', '소득금액', '', st(2, 1), 'ink'], ['월급만 있다면 한 해', '7,600만원쯤', '', st(2, 2), 'ink']]}
S[3]['data'] = {'tiles': [['519만원 넘으면', '15만원', '', 0, 'ink'], ['600만원이면', '27만원', '', st(3, 2), 'ink'], ['아무리 벌어도', '연금의 절반까지', '', st(3, 3), 'ink']]}
S[4]['data'] = {'tiles': [['깎이는 기간', '최대 5년', '', 0, 'ink'], ['선 바로 위라면', '한 번에 빠짐', '', st(4, 1), 'ink']]}
# 10/20 15:2x 이해 시험 1차(40·50·60세 3/3 뜻 맞음) 반영 — 화면 글자만: '0원'이 소득인지 깎이는 돈인지 · 월 519만원과 한 해 7,600만원 단위 섞임 · '연금 월 100만원 가정'이 끝 작은 글씨에만 · '600만원'이 월급인지 공제 뒤인지
S[0]['data']['tiles'] = [['519만원 아래면', '안 깎임', '', 0, 'ink'], ['넘는 순간', '15만원 깎임', '', 30, 'ink']]
S[2]['data']['tiles'][1] = ['근로소득공제 빼고', '공제 뒤 금액', '', st(2, 1), 'ink']
S[2]['data']['tiles'][2] = ['비과세 뺀 연봉', '7,600만원쯤', '', st(2, 2), 'ink']
S[3]['data']['tiles'] = [['연금 월 100만원 예', '15만원부터', '', 0, 'ink'], ['공제 뒤 600만원', '27만원 깎임', '', st(3, 2), 'ink'], ['아무리 벌어도', '연금의 절반까지', '', st(3, 3), 'ink']]
for s in S: s['kind'] = 'vs'
p = fmt_eok(p)
p['look'] = 'live'; p['name'] = 'p1s_step_live'
for fn in ('p1s_step_live.json', 'p1s_step.json'): json.dump(p, open(os.path.join(VID, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in p['scenes'])
print(f'p1s_step_live: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(S)}')
for s in p['scenes']: print(s['kind'], json.dumps(s['data'], ensure_ascii=False)[:220])
