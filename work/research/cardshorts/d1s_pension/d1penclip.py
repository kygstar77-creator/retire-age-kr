# d1s_pension — D-1 롱폼(GMc2Rd1-JYA, 10/2 공개) 1장 절벽·6장 '국민연금을 받는 경우'를 자른 세로 쇼츠 props (firemap-video-producer 2026-10-14 23시, r1s_gap/r1gapclip.py 복사)
#   py -3.12 work/research/cardshorts/d1s_pension/d1penclip.py   → work/video/d1s_pension.json (M1S v2 틀 'pieces' — ⓓ: 최근 10편 c1clip 6편이라 C1S는 업로드 거부)
# 목소리 = video/d1.json 문장 wav 그대로(D-1 gemini TTS Charon, 새 녹음 0) · 줄은 d1.json 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 질문: 이미 나간 d1_kunbo(1,000 vs 1,001만원 절벽, 연금 없음)·d1s_when(고지서 언제)과 다른 '연금 받는 사람은 절벽이 얼마나 더 큰가'.
# 화면 숫자 = d1.json pension·open 데이터·ep/D-1/facts.txt 읽기 표기 그대로 — need()로 기계 대조.
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
D1 = json.load(open(os.path.join(VID, 'd1.json'), encoding='utf-8'))
FACTS = open(os.path.join(WORK, 'research', 'longform', 'ep', 'D-1', 'facts.txt'), encoding='utf-8').read()
BYTEXT = {l['text']: l for s in D1['scenes'] for l in (s.get('lines') or [])}
SRCTXT = json.dumps(D1, ensure_ascii=False) + FACTS
def need(*xs):
    for x in xs: assert x in SRCTXT, f'd1.json·facts에 없음: {x}'
TAIL = 36

def L(*texts):
    out = []
    for t in texts:
        hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
        l = BYTEXT[hit[0]]; assert l.get('audio'), t
        out.append({'n': 0, 'text': l['text'], 'cap': None, 'audio': l['audio'], 'frames': l['frames']})
    return out

need('2만 2,800원', '6만 7,850원', '6만 1,000원', '12만 8,860원', '6만 7,860원', '81만 4,320원', '1,800만원', '900만원', '150만원', '50%', '540,600원', '1,000만원', '1,001만원')
SRC_ALL = '국민건강보험법 시행규칙 제44조①②(금융소득 1,000만원 단서·연금 50%) · 국민건강보험공단 지역보험료 모의계산 · 2026년 · 재산 0 가정'

def sc(kind, label, lines, **data):
    return {'kind': kind, 'label': label, 'source': SRC_ALL, 'data': data, 'lines': lines}

scenes = [   # 23:2x 눈 검사: 9초·18초 빈 곳 44%·41%(장면 첫 줄에 칸·띠 없음) → 첫 줄부터 띠 · 오른 쪽 색 fall(파랑)→accent  # 첫 줄 = 롱폼 표 줄 26 '1,001만원이 되는 순간 6만 7,850원.'(답 숫자 먼저 — A27, 꼴 ⓐ 35자 이하). 줄 24는 38자·41 '한 달에 6만 7,860원…'은 37자라 첫 줄 불가 → 끝 장면
    sc('pieces', '연금 없을 때 · 1,000만원 경계', L('1,001만원이 되는 순간', '900만원이면 2만 2,800원'),
       head=['연금 없음 · 1년 배당·이자별 월 건보료', -1], zero='', max=14, cx=60, half=880, ghost=True,
       rows=[['900만원', '합산 안 함', 2.28, '2만 2,800원', -1, 'ink'], ['1,000만원', '합산 안 함', 2.28, '2만 2,800원', -1, 'ink'],   # 10/15 22시 v3: 0초 빈 곳 42.7% > 40% → 세 막대 0초부터(회의 10/15 지시)
             ['1,001만원', '전액 합산', 6.785, '6만 7,850원', -1, 'accent']],
       notes=[['1만원 넘자 월 6만 7,850원', 0], ['1,000만원까지는 최저 보험료', 1]]),
    sc('pieces', '국민연금 월 150만원이면', L('이번엔 국민연금을 받는 경우', '국민연금을 월 150만원, 1년에'),
       head=['국민연금 월 150만원 · 보험료 매길 때', -1], zero='', max=2000, cx=60, half=880, ghost=True,
       rows=[['1년 받은 연금', '월 150만원 × 12', 1800, '1,800만원', 0, 'ink'], ['보험료에 반영', '공적연금은 50%', 900, '900만원', 1, 'accent']],
       notes=[['받은 연금이 다 잡히진 않음', 0], ['공적연금은 50%만 반영', 1]]),
    sc('pieces', '여기에 배당·이자가 붙으면', L('이걸로 계산하면 건보료는 월 6만', '여기에 금융소득이 1,000만원이면', '그런데 1,001만원이면 금융소득 전액이'),
       head=['연금 월 150만원 · 월 건보료', -1], zero='', max=14, cx=60, half=880, ghost=True,
       rows=[['연금만', '900만원 반영', 6.1, '6만 1,000원', 0, 'ink'], ['+ 배당·이자 1,000만원', '합산 안 함', 6.1, '6만 1,000원', 1, 'ink'],
             ['+ 배당·이자 1,001만원', '전액 합산', 12.886, '12만 8,860원', 2, 'accent']],
       hi=[[2], 2], notes=[['연금만 있으면 월 6만 1,000원', 0], ['1,000만원까지는 그대로', 1], ['금융소득 전액이 더해짐', 2]]),
    sc('pieces', '연금 있으면 절벽이 더 크다', L('한 달에 6만 7,860원, 1년이면', '연금을 받는 사람일수록'),
       head=['배당·이자 1,000 → 1,001만원 · 1년 건보료 차이', -1], zero='', max=90, cx=60, half=880, ghost=True,
       rows=[['연금 없음', '다른 소득 0', 54.06, '54만원 넘게', -1, 'ink'], ['연금 월 150만원', '900만원 반영', 81.432, '81만 4,320원', 0, 'accent']],
       hi=[[1], 0], notes=[['한 달 6만 7,860원 · 1년 81만 4,320원', 0], ['연금 받을수록 절벽이 커짐', 1]]),
]
for s in scenes: s['frames'] = sum(l['frames'] for l in s['lines'])
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'd1s_pension', 'v': 3, 'question': ['연금 월 150만원 받는데', '배당 1만원 더 받으면?'], 'hot': '1만원',
     'track': None, 'answer': {'label': '배당·이자 1,000 → 1,001만원 · 월 건보료', 'items': ['6만 1,000원', '12만 8,860원'], 'arrow': True, 'note': '1년 81만 4,320원 차이 · 재산 0 가정'},
     'base': '2026년 법령·공단 계산식 · 지역가입자 · 재산 0 가정', 'long': '전체 계산은 롱폼에서 · 설명란 첫 줄 링크', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'd1s_pension.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'd1s_pension: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {sum(len(s["lines"]) for s in scenes)}')
