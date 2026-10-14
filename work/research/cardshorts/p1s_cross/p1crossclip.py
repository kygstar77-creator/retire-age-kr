# p1s_cross — P-1 롱폼(vsL7mojDW7w, 10/16 11:30 공개) 2장 금액~3장 '따라잡히는 나이'를 자른 세로 쇼츠 props (firemap-video-producer 2026-10-14, g1s_why/g1whyclip.py 복사)
#   py -3.12 work/research/cardshorts/p1s_cross/p1crossclip.py   → work/video/p1s_cross.json (M1S v2 틀: 'bars' + 'pieces')
# 목소리 = P-1 롱폼 문장 wav 그대로(새 녹음 0) · 줄은 번호가 아니라 p1.json 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 화면 숫자 = p1.json(편집 통과한 롱폼 화면 글자) 또는 ep/P-1/calc_out.txt에 있는 글자만 — need()로 기계 대조.
# pieces 막대 길이 = 그 나이 − 65(제때 받기 시작한 나이, 1969년생). 막대 옆 글자는 calc_out 나이 그대로.
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
P1 = json.load(open(os.path.join(VID, 'p1.json'), encoding='utf-8'))
CALC = open(os.path.join(WORK, 'research', 'longform', 'ep', 'P-1', 'calc_out.txt'), encoding='utf-8').read()
BYTEXT = {l['text']: l for s in P1['scenes'] for l in s['lines']}
SRCTXT = json.dumps(P1, ensure_ascii=False) + CALC
def need(*xs):
    for x in xs: assert x in SRCTXT, f'p1.json·calc_out에 없음: {x}'
TAIL = 36

def L(*texts):
    out = []
    for t in texts:
        hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
        l = BYTEXT[hit[0]]; assert l.get('audio'), t
        out.append({'n': 0, 'text': l['text'], 'cap': None, 'audio': l['audio'], 'frames': l['frames']})
    return out

SRC_ALL = '국민연금법 제61조②·제62조②·제63조② · 1969년생·제때 월 100만원 가정 · 파이어맵 계산'
need('70만원', '100만원', '136만원', '6%', '7.2%', '76.67세', '83.89세', '80.67세', '79.89세', '1969년생', '제61조②')
AGE = {'76.67세': 76.67, '83.89세': 83.89, '80.67세': 80.67, '79.89세': 79.89}

def sc(kind, label, lines, **data):
    return {'kind': kind, 'label': label, 'source': SRC_ALL, 'data': data, 'lines': lines}

scenes = [
    sc('bars', '제때 받으면', L('연금 씨가 제때 받으면'), full=True, tall=True, max=140, note=['매달 받는 돈 ', '(제때 100만원 가정)'],
       bars=[['제때 · 65세', 100, '100만원', 'ink']], stamp='1969년생 · 제때 = 65세'),
    sc('bars', '5년 당기면', L('5년을 당기면 70만원', '한 해 당길 때마다 6%씩'), tall=True, max=140, note=['5년 당기면 ', '70만원'],
       bars=[['5년 당김 · 60세', 70, '70만원', 'fall'], ['제때 · 65세', 100, '100만원', 'ink']], stamp='한 해 당길 때마다 6%씩 깎임'),
    sc('bars', '5년 미루면', L('반대로 5년을 미루면', '이쪽은 한 해 미룰 때마다'), tall=True, max=140, note=['5년 미루면 ', '136만원'],
       bars=[['5년 당김 · 60세', 70, '70만원', 'fall'], ['제때 · 65세', 100, '100만원', 'ink'], ['5년 미룸 · 70세', 136, '136만원', 'rise']],
       stamp='한 해 미룰 때마다 7.2%씩 붙음'),
    sc('pieces', '쌓인 돈이 같아지는 나이', L('당겨 받으면 먼저 받기 시작하죠', '연금 씨가 세 길로 받은 돈을', '그러다 어느 날, 제때 받은 쪽이', '그 나이가 77세가', '미루는 쪽도 똑같이 쌓아 보면'),
       head=['쌓인 돈이 제때와 같아지는 나이', 0], zero='65세 = 제때 받기 시작', cx=60, half=880, max=20, ghost=True,
       rows=[['5년 당김', '제때가 따라잡는 나이', round(AGE['76.67세'] - 65, 2), '76.67세', 0, 'fall'],
             ['5년 미룸', '제때를 넘어서는 나이', round(AGE['83.89세'] - 65, 2), '83.89세', 4, 'rise']],
       hi=[[0], 2], notes=[['처음엔 당긴 쪽이 앞섬', 1], ['그 전에 끝나면 당긴 쪽이 더 받은 것', 3]]),
    sc('pieces', '1년만 당기거나 미루면', L('1년만 당기면, 따라잡히는', '1년만 미루면, 앞서는'),
       head=['1년만 바꾸면 같아지는 나이', 0], zero='65세 = 제때 받기 시작', cx=60, half=880, max=20,
       rows=[['5년 당김', '', round(AGE['76.67세'] - 65, 2), '76.67세', -1, 'ink'], ['1년 당김', '오히려 늦어짐', round(AGE['80.67세'] - 65, 2), '80.67세', 0, 'fall'],
             ['5년 미룸', '', round(AGE['83.89세'] - 65, 2), '83.89세', -1, 'ink'], ['1년 미룸', '빨라짐', round(AGE['79.89세'] - 65, 2), '79.89세', 1, 'rise']],
       hi=[[1, 3], 0], note=['1969년생 · 제때 월 100만원 가정', 0]),
]
for s in scenes: s['frames'] = sum(l['frames'] for l in s['lines'])
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'p1s_cross', 'v': 2, 'question': ['국민연금 5년 당기면', '몇 살에 따라잡히나'], 'hot': '몇 살',
     'track': None, 'answer': {'label': '쌓인 돈이 같아지는 나이', 'items': ['당김 76.67세', '미룸 83.89세'], 'arrow': False, 'note': '1년만 당기면 80.67세'},
     'base': '1969년생 · 제때 월 100만원 가정 · 국민연금법 조문 비율', 'long': '전체 계산은 롱폼에서 · 설명란 첫 줄 링크', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'p1s_cross.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'p1s_cross: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {sum(len(s["lines"]) for s in scenes)}')
