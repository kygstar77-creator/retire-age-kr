# r1s_gap — R-1 롱폼(G1oI47miUuo) 7·9·10·13장 'SCHD와 예금 차이, 세금이 줄인 간격'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-14)
#   py -3.12 work/research/cardshorts/r1s_gap/r1gapclip.py   → work/video/r1s_gap.json (M1S v2 틀, 새 장면 종류 'pieces')
# 틀을 M1S로 한 이유: w1g1clips_check ⓓ — 최근 10편이 모두 c1clip(C1S)이라 C1S 새 쇼츠는 업로드 거부.
# 목소리 = R-1 롱폼 문장 wav 그대로(새 녹음 0) · 줄은 번호가 아니라 r1.json 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 화면 숫자 = r1.json(편집 통과한 롱폼 화면 글자: odd·wf1 장면 값·자막)에 있는 글자만 — 아래 need()로 기계 대조. 7자리 원은 만원으로(쇼츠 꼴 ⓒ).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
G1 = json.load(open(os.path.join(VID, 'r1.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in G1['scenes'] for l in s['lines']}
SRC = {s['key']: s.get('source') for s in G1['scenes']}
G1TXT = json.dumps(G1, ensure_ascii=False)
def need(*xs):
    for x in xs: assert x in G1TXT, f'r1.json 화면 글자에 없음: {x}'
TAIL = 36

def L(*texts):
    out = []
    for t in texts:
        hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
        l = BYTEXT[hit[0]]; assert l.get('audio'), t
        out.append({'n': 0, 'text': l['text'], 'cap': None, 'audio': l['audio'], 'frames': l['frames']})
    return out

need('16,876,863원', '13,804,655원', '1억 1,599만원', '1억 1,023만원', '1억 337만원', '1억 218만원', '+15.99%', '+10.23%', '+3.37%', '+2.18%',
     '−559,242', '−2,910,286', '+3,728,285', '많이 번 쪽이 세금도 많이 낸다')
SRC_ALL = '한국은행 ECOS(정기예금 금리·원/달러 매매기준율) · SPY·SCHD·GLD 종가·분배금 · 소득세법 · 한미 조세조약 · 2025-10-02 → 2026-10-02 · 파이어맵 계산'

def sc(kind, label, lines, **data):
    return {'kind': kind, 'label': label, 'source': SRC_ALL, 'data': data, 'lines': lines}

scenes = [   # 10/14 순서: 첫 줄 37자(꼴 ⓐ 35자) → 순위 줄로 시작
    sc('pieces', '세금·환율 다 뗀 뒤 순위', L('SCHD는 16% 가까이', '금은 3% 조금 넘게', '세금 떼기 전에도, 뗀 뒤에도'),
       head=['세금·환율 다 뗀 뒤 · 1억 → 1년 뒤', -1], zero='', max=17, cx=60, half=880, ghost=True,
       rows=[['SCHD', '1억 1,599만원', 15.99, '+15.99%', -1, 'accent'], ['S&P500(SPY)', '1억 1,023만원', 10.23, '+10.23%', -1, 'ink'],
             ['금(GLD)', '1억 337만원', 3.37, '+3.37%', -1, 'ink'], ['예금', '1억 218만원', 2.18, '+2.18%', -1, 'ink']],
       hi=[[0, 1], 0, 1],
       notes=[['SCHD 1억 1,599만원 · 예금 1억 218만원', 1], ['세금 떼기 전에도 같은 순서', 2]]),
    sc('pieces', 'SCHD와 예금, 1억 1년 뒤 차이', L('세금 떼기 전에는 SCHD와 예금 차이가', '세금을 떼고 나니 1,380만원으로'),
       head=['SCHD − 예금 · 1억 넣고 1년 뒤', -1], zero='', max=1800, cx=60, half=880,
       rows=[['세금 떼기 전', '차이', 1688, '1,688만원', -1, 'ink'], ['세금 뗀 뒤', '차이', 1380, '1,380만원', 1, 'accent']],
       notes=[['세금이 줄인 간격 307만원', 1]]),
    sc('pieces', 'SCHD 1억 · 세금 두 군데', L('배당 ETF답게 분배금도 컸어요', '여기서 미국 세금으로', '판 이익에는 291만원', '많이 번 쪽이 세금도', '순위는 그대로였고'),
       head=['SCHD 1억 · 세금은 두 군데서', -1], zero='0', max=400, ghost=True,
       rows=[['분배금 4번(세금 전)', '1년 합계', 373, '+373만원', 0, 'rise'], ['미국이 뗀 세금 15%', '분배금에서', -55.9, '−55만 9천원', 1, 'fall'],
             ['판 이익 세금', '양도세 22%', -291, '−291만원', 2, 'fall']],
       notes=[['많이 번 쪽이 세금도 많이 낸다', 3], ['순위는 그대로 · 넣는 날 바뀌면 달라짐', 4]]),
]
for s in scenes: s['frames'] = sum(l['frames'] for l in s['lines'])
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'r1s_gap', 'v': 2, 'question': ['세금 떼면 SCHD와', '예금 차이는?'], 'hot': '차이',
     'track': None, 'answer': {'label': 'SCHD − 예금 · 1억 넣고 1년 뒤', 'items': ['1,688만원', '1,380만원'], 'arrow': True, 'note': '세금 떼기 전 → 뗀 뒤 · 순위는 그대로'},
     'base': '2025년 10월 2일 → 2026년 10월 2일 · 지난 1년 실제 기록', 'long': '전체 계산은 롱폼에서 · 설명란 첫 줄 링크', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'r1s_gap.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'r1s_gap: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {sum(len(s["lines"]) for s in scenes)}')
