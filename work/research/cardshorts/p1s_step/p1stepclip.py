# p1s_step — P-1 롱폼(vsL7mojDW7w, 10/16 11:30 공개) 5장 '519만원 위의 계단'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-15, h1s_helio/h1helioclip.py 복사)
#   py -3.12 work/research/cardshorts/p1s_step/p1stepclip.py   → work/video/p1s_step.json (틀 C1S)
# 틀: log.jsonl 최근 9편 m1clip 5·c1clip 4 → m1clip이면 6/10 = 꼴 ⓓ 거부, C1S(c1clip)로.
# 목소리 = P-1 롱폼 문장 wav 그대로(Chirp 3 HD Charon, 새 녹음 0). 줄 번호 = video/p1.json 전체 순번(0부터), assert로 글자 확인.
# 화면 숫자 = p1.json step 장면 데이터(조문대로 계산, 연금 월 100만원 가정) — 7자리 원은 만원 반올림(꼴 ⓒ).
# 줄 순서: 계단 줄(57, 17자·숫자 — 꼴 ⓐ)을 첫 줄로 → 50~55 선·월급 → 56·58~60 계단·상한 → 61·62 기간·조심할 자리로 끝(63 '숫자를 가를 수 있습니다'는 길이 때문에 뺌).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w1g1clips import load, mk, at, scene, build, VID

PL, PS = load('p1')
L = mk(PL)
for i, t in ((50, '연금 씨가 65세에 받으면서'), (51, '그 선이 올해 6월부터'), (52, '이제는 한 달 소득이 519만원'), (53, '여기서 소득은 월급'), (54, '근로소득공제를 빼고'),
             (55, '월급만 있다면'), (56, '그런데 조문대로'), (57, '선을 넘는 순간, 15만원'), (58, '계단이 있는 거죠'), (59, '소득이 더 올라가면'), (60, '다만 아무리'),
             (61, '깎이는 기간은'), (62, '그래서 소득이 이 선 바로 위')):
    assert PL[i]['text'].startswith(t), (i, PL[i]['text'])
ST = PS['step']; D = ST['data']['step']
assert D['oldText'] == '옛 기준 319만 3,511원' and D['newText'] == '519만 3,511원' and D['jumpText'] == '15만원' and D['tiers'][0][1] == 15 and D['cap'] == 50
assert [p['text'] for p in D['pts']] == ['600만 → 270,973원', '700만 → 461,298원', '800만 → 500,000원'] and D['salary'] == ['75,865,402원', '한 해 · 월 6,322,117원']
assert D['period'][:2] == ['65세', '70세'] and D['slips'] == ['519만원 바로 아래', '감액 0원', '519만원 바로 위', '감액 15만원']
man = lambda won: round(won / 10000)   # 원 → 만원(반올림)
assert (man(270973), man(461298), man(500000), man(6322117)) == (27, 46, 50, 632)
SRC = ST['source']

a = L(57); b = L(50, 51, 52); c = L(53, 54, 55); d = L(56, 58, 59, 60); e = L(61, 62)
SH = dict(
  question=['일하면서 국민연금 받으면', '얼마부터 깎이나'], hot='얼마부터',
  base='국민연금법 제63조의2(2026-06-17 시행) · 연금 월 100만원 가정 · 조문대로 계산',
  answer=dict(label='공제 뒤 한 달 소득', items=['519만원 넘으면', '15만원 깎임'], arrow=True, note='월급만 있으면 한 해 총급여 7,600만원쯤부터'),
  scenes=[
   scene('bars', '넘는 순간 15만원', SRC, a, head='공제 뒤 한 달 소득 · 깎이는 돈 · 연금 월 100만원', max=18, full=True,   # 10/15: vs 칸은 0초에 튀어나오는 중이라 빈 곳 50% → 0초부터 다 보이는 막대 판
         bars=[['519만원 바로 아래', 0, '0원', 0, 'ink3'],
               ['519만원 바로 위', 15, '15만원', 0, 'accent', '넘는 순간 한 번에']]),
   scene('bars', '선이 올라갔다', SRC, b, head='깎이기 시작하는 선 · 공제 뒤 한 달 소득', max=600,
         bars=[['2026년 6월 전 기준', 319, '319만원', 0, 'ink3'],
               ['2026년 6월 17일부터', 519, '519만원', at(b, 1.5), 'accent', '+200만원']]),
   scene('vs', '월급 그대로가 아님', SRC, c,
         tiles=[['깎일지 보는 소득', D['notWage'], '총급여(비과세 제외) − 근로소득공제 = 근로소득금액', 0, 'ink'],
                ['월급만 있다면 · 한 해 총급여', '7,600만원쯤', f'한 달로는 {man(6322117)}만원쯤', at(c, 2), 'accent']]),
   # 10/15 눈 검사: 긴 이름 3줄 겹침·상한 글 겹침 → 짧은 이름 · 막대가 늦게 들어오면 첫 순간 빈 곳 43% → 800만원만 줄 59에(같은 화면 8초 이하)
   scene('bars', '계단', SRC, d, head='공제 뒤 한 달 소득별 깎이는 돈 · 연금 월 100만원', max=52,
         bars=[['519만원 아래', 0, '0원', 0, 'ink3'],
               ['519만원 위', 15, '15만원', 0, 'accent'],
               ['600만원', 27.0973, f'{man(270973)}만원', 0, 'ink'],
               ['700만원', 46.1298, f'{man(461298)}만원', 0, 'ink'],
               ['800만원', 50, f'{man(500000)}만원', at(d, 2), 'ink']]),
   scene('vs', '조심할 자리', SRC, e,
         tiles=[['깎이는 기간', '최대 5년', '65세 → 70세 · 1969년생', 0, 'ink'],
                ['선 바로 위라면', '한 번에 빠짐', '몇만원 더 버는 사이 · 연봉 바뀌는 해 확인', at(e, 1), 'accent']]),
  ],
)

if __name__ == '__main__':
    p = build('p1s_step', SH)
    for sc_ in p['scenes']:   # 꼴 ⓒ: 줄 55 작은 자막의 7자리 원 → 만원 반올림(75,865,402원 → 7,587만원, 6,322,117원 → 632만원), 말은 그대로
        for l in sc_['lines']:
            if l['n'] == 55:
                assert l['cap'] == '총급여(비과세 제외) 75,865,402원 (월 6,322,117원) · 근로소득만 있을 때 · 파이어맵 계산'
                l['cap'] = f'총급여(비과세 제외) {man(75865402):,}만원 (월 {man(6322117)}만원) · 근로소득만 있을 때 · 파이어맵 계산'
    fr = sum(s['frames'] for s in p['scenes'])
    json.dump(p, open(os.path.join(VID, 'p1s_step.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"p1s_step: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {[l['n'] for s in p['scenes'] for l in s['lines']]}")
