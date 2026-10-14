# g1s_why — G-1 롱폼(xBTZtRp5lMs) 2장 끝~3장 '세 조각'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-14)
#   py -3.12 work/research/cardshorts/g1s_why/g1whyclip.py   → work/video/g1s_why.json (M1S v2 틀, 새 장면 종류 'pieces')
# 틀을 M1S로 한 이유: w1g1clips_check ⓓ — 최근 10편이 모두 c1clip(C1S)이라 C1S 새 쇼츠는 업로드 거부.
# 목소리 = G-1 롱폼 문장 wav 그대로(새 녹음 0) · 줄은 번호가 아니라 g1.json 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 화면 숫자 = g1.json(편집 통과한 롱폼 화면 글자: odd·wf1 장면 값·자막)에 있는 글자만 — 아래 need()로 기계 대조. 7자리 원은 만원으로(쇼츠 꼴 ⓒ).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
G1 = json.load(open(os.path.join(VID, 'g1.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in G1['scenes'] for l in s['lines']}
SRC = {s['key']: s.get('source') for s in G1['scenes']}
G1TXT = json.dumps(G1, ensure_ascii=False)
def need(*xs):
    for x in xs: assert x in G1TXT, f'g1.json 화면 글자에 없음: {x}'
TAIL = 36

def L(*texts):
    out = []
    for t in texts:
        hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
        l = BYTEXT[hit[0]]; assert l.get('audio'), t
        out.append({'n': 0, 'text': l['text'], 'cap': None, 'audio': l['audio'], 'frames': l['frames']})
    return out

need('+6.65%', '−4.43%', '−3.38%', '−7.26%', 'KRX 웃돈 +6.3%', 'KRX 웃돈 −1.4%', '956만원', 'KRX 금값 = 달러 금값 × 환율 × KRX 웃돈')
SRC_ALL = '금 선물 GC=F(야후) · 한국은행 ECOS 원/달러 매매기준율 · KRX 금시장 종가 · 2025-10-02 → 2026-10-06'

def sc(kind, label, lines, **data):
    return {'kind': kind, 'label': label, 'source': SRC_ALL, 'data': data, 'lines': lines}

scenes = [
    sc('pieces', '국제 금값은 올랐는데', L('작년과 비교하면, 국제 금값은', '그런데 왜 한국에서 산 금은', '천만원어치가 지금 956만원'),
       head=['작년 10월 2일에 산 금, 1년 뒤', 0], zero='0 = 산 날 값', max=8,
       rows=[['달러 금값', '국제 금 시세', 6.65, '+6.65%', -1, 'rise'], ['한국 KRX 금', '내가 산 금', -4.43, '−4.43%', -1, 'fall']],
       note=['1천만원 → 956만원', 2]),
    sc('pieces', '한국 금값 = 세 조각의 곱', L('한국에서 사는 금값은 세 가지를', '첫 조각, 달러 금값은', '둘째 조각은 환율인데요', '셋째 조각이 제일 커요', '작년엔 KRX 금이,', '지금은 오히려 조금 싸요', '이 웃돈이 빠진 것만으로도'),
       head=['한국 금값 = 달러 금값 × 환율 × KRX 웃돈', 0], zero='0 = 산 날 값', max=8, ghost=True,
       rows=[['① 달러 금값', '국제 금 시세', 6.65, '+6.65%', 1, 'rise'], ['② 환율', '원/달러 1,406.0원 → 1,358.5원', -3.38, '−3.38%', 2, 'fall'],
             ['③ KRX 웃돈', '+6.3% → −1.4%', -7.26, '−7.26%', 3, 'accent']],
       hi=[[2], 3], notes=[['작년 KRX 웃돈 +6.3% · 국제 값보다 비쌌다', 4], ['지금 KRX 웃돈 −1.4% · 오히려 쌌다', 5], ['가장 큰 조각 = 웃돈', 6]]),
    sc('pieces', '세 조각을 곱하면', L('세 조각을 곱하면 결국', '그러니까 작년에 산 분은'),
       head=['(1+6.65%) × (1−3.38%) × (1−7.26%) − 1', -1], zero='0 = 산 날 값', max=8,
       rows=[['① 달러 금값', '', 6.65, '+6.65%', -1, 'rise'], ['② 환율', '', -3.38, '−3.38%', -1, 'fall'], ['③ KRX 웃돈', '', -7.26, '−7.26%', -1, 'accent'],
             ['= 내 금', 'KRX 금 1년', -4.43, '−4.43%', 0, 'ink']],
       hi=[[1, 2, 3], 1], note=['잃은 곳: 환율과 웃돈', 1]),
]
need('1,406.0원', '1,358.5원', '(1+6.65%) × (1−3.38%) × (1−7.26%) − 1')
for s in scenes: s['frames'] = sum(l['frames'] for l in s['lines'])
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'g1s_why', 'v': 2, 'question': ['국제 금값은 올랐는데', '내 금은 왜 떨어졌나'], 'hot': '왜',
     'track': None, 'answer': {'label': '작년에 산 금 1년 · 세 조각', 'items': ['달러 +6.65%', '웃돈 −7.26%'], 'arrow': False, 'note': '환율 −3.38% · 내 금 −4.43%'},
     'base': '2026년 10월 6일 기준 · 지난 1년 실제 기록', 'long': '전체 계산은 롱폼에서 · 설명란 첫 줄 링크', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'g1s_why.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'g1s_why: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {sum(len(s["lines"]) for s in scenes)}')
