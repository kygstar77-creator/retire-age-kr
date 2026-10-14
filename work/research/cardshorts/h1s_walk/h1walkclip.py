# h1s_walk — H-1 롱폼(rVg0pQVo_wk) 고덕동 장 '역 180m vs 640m · 평당 값 · 학교·마트 길'을 자른 세로 쇼츠 props (firemap-video-producer 2026-10-15)
#   py -3.12 work/research/cardshorts/h1s_walk/h1walkclip.py   → work/video/h1s_walk.json (M1S v2 틀, 'pieces')
# 틀 M1S: w1g1clips_check ⓓ(최근 10편 한 틀 50% 초과 거부)를 피하려고 C1S 대신 · H-1 앞 클립 h1s_gap(계산서)과 다른 질문.
# 목소리 = H-1 롱폼 문장 wav 그대로(Chirp 3 HD Charon, 새 녹음 0) · 줄은 h1.json 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 화면 숫자·글자 = h1.json(편집 통과한 롱폼 화면 글자: g_ruler·g_bars·g_walk2·g_cards 값·자막)에 있는 것만 — need()로 기계 대조.
# 줄 순서: 역 거리(53·54·55) → 평당(56) → '역 때문이라고 말할 수 없음'(61·62) → 학교·마트 뒤집힘(57~60)으로 끝(꼴 ⓑ: 끝 줄 면책 금지라 61을 가운데로).
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
H1 = json.load(open(os.path.join(VID, 'h1.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in H1['scenes'] for l in s['lines']}
SRC = {s['key']: s.get('source') for s in H1['scenes']}
H1TXT = json.dumps(H1, ensure_ascii=False)
def need(*xs):
    for x in xs: assert x in H1TXT, f'h1.json 화면 글자에 없음: {x}'
TAIL = 36

def L(*texts):
    out = []
    for t in texts:
        hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
        l = BYTEXT[hit[0]]; assert l.get('audio'), t
        out.append({'n': 0, 'text': l['text'], 'cap': None, 'audio': l['audio'], 'frames': l['frames']})
    return out

need('180m', '640m', '640 ÷ 180 = 3.56배', '9,457만원', '7,865만원', '25건', '33건', '그라시움이 +20.2%', '2019.09', '2016.12', '4,932세대', '3,658세대',
     '390m', '600m', '960m', '1,170m', '학교는 그라시움이 210m 짧고, 마트는 손품 씨네가 짧음', '배정 학교 아님', '상일동역 출입구', '고덕역 출입구')
WALK = SRC['g_ruler']; PRICE = SRC['g_bars']

def sc(kind, label, src, lines, **data):
    return {'kind': kind, 'label': label, 'source': src, 'data': data, 'lines': lines}

scenes = [
    sc('pieces', '역 출입구까지 걸어서', WALK, L('고덕그라시움은 상일동역', '손품 씨네 래미안힐스테이트고덕은', '같은 동네 안에서 역까지'),
       head=['지하철 출입구까지 · OSM 보행로', -1], zero='0m', max=700, cx=60, half=880, ghost=True,
       rows=[['고덕그라시움', '상일동역 출입구', 180, '180m', -1, 'accent'],
             ['래미안힐스테이트고덕', '고덕역 출입구 · 손품 씨네(가상 인물)', 640, '640m', -1, 'ink']],
       # 10/15 눈 검사: hi로 0초에 640m 줄이 흐려 보여 뺌(0초 판 두 막대 다 진하게)
       notes=[['640 ÷ 180 = 3.56배', -1]]),   # 10/15 빈 곳 아래 절반 44% → 0초부터
    sc('pieces', '84㎡대 평당 값', PRICE, L('같은 평형 평당 값은 그라시움이'),
       head=['84㎡대 평당 · 국토교통부 실거래 1년', -1], zero='', max=11000, cx=60, half=880,
       rows=[['고덕그라시움', '25건', 9457, '9,457만원', -1, 'accent'],
             ['래미안힐스테이트고덕', '33건', 7865, '7,865만원', -1, 'ink']],
       notes=[['그라시움이 +20.2%', 0]]),
    sc('pieces', '입주·세대 수', PRICE, L('그렇다고 평당 값 차이가', '지은 해도, 세대 수도'),
       head=['입주 · 세대 수', -1], zero='', max=6000, cx=60, half=880,   # 10/15 02시 빈 곳 44% → 막대 처음부터·아래 칸
       rows=[['고덕그라시움', '2019.09 입주', 4932, '4,932세대', -1, 'accent'],
             ['래미안힐스테이트고덕', '2016.12 입주', 3658, '3,658세대', -1, 'ink']],
       notes=[['역 말고도 지은 해·세대 수가 다름', 1]]),
    sc('pieces', '학교 길 · 장 보러 가는 길', WALK, L('아이 학교 길도 봤어요', '손품 씨네보다 200m쯤', '그런데 장 보러 가는 길은', '이마트까지 손품 씨네는'),
       head=['걸어서 · OSM 보행로', -1], zero='초등학교는 가장 가까운 곳 · 배정 학교 아님', max=1400, cx=60, half=880, ghost=True,
       rows=[['고덕그라시움', '가장 가까운 초등학교', 390, '390m', 0, 'accent'],
             ['래미안힐스테이트고덕', '가장 가까운 초등학교', 600, '600m', 0, 'ink'],
             ['래미안힐스테이트고덕', '이마트', 960, '960m', 2, 'accent'],
             ['고덕그라시움', '이마트', 1170, '1,170m', 3, 'ink']],
       hi=[[0, 1], 0, 2]),
]
for s in scenes: s['frames'] = sum(l['frames'] for l in s['lines'])
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'h1s_walk', 'v': 2, 'question': ['역까지 180m vs 640m,', '평당 값은?'], 'hot': '평당 값',
     'track': None, 'answer': {'label': '고덕동 84㎡대 평당 · 국토교통부 실거래 1년', 'items': ['9,457만원', '7,865만원'], 'arrow': False,
                              'note': '학교는 그라시움이 210m 짧고, 마트는 손품 씨네가 짧음'},
     'base': '실거래 2025.11~2026.10 · OSM 보행로 · 손품 씨 = 가상 인물', 'long': '전체 계산은 롱폼에서 · 설명란 첫 줄 링크', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'h1s_walk.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h1s_walk: {fr} 프레임 = {fr / 30:.1f}초 · 줄 {sum(len(s["lines"]) for s in scenes)}')
