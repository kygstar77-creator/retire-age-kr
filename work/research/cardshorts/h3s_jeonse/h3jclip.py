# h3s_jeonse — H-3 롱폼 전세 장(voice.json 172~194)을 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live') (firemap-video-producer 2026-10-23, x1s_deposit/x1dclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/h3s_jeonse/h3jclip.py   → work/video/h3s_jeonse.json
#   렌더(다른 Remotion 렌더와 동시에 돌리지 말 것 — 10/23 'No frame found' 2번): cd work/video && npx remotion render src/m1s_index.ts M1S out/h3s_jeonse.mp4 --props=h3s_jeonse.json --concurrency=1
# 목소리 = H-3 voice.json(say_v5) 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# h3_specs.md h3s_jeonse: 숫자는 calc2_out §3(10/22 다시 받은 실거래, 계약 2025.11~2026.10) · '싸다·비싸다' 판단 0 · 이유는 '자료에 없음'(189줄) 꼭 넣음
# 10/23 이해 시험 1차(40·50·60세)·레드팀: '가장 높/낮'의 범위(본 단지 7곳 — calc2_out §3)·'같은 신천동'(압구정 장면 뒤라 헷갈림)·파크리오 매매값(29.20억) 화면에 · 평형(84㎡대·49~51㎡·81~83㎡ — calc2_out §3 넓이 구간 그대로) 표시
# 10/23 2차(60세): '1980년대까지 지은 단지 모두 아래'가 일반 법칙처럼 들림 → '나머지 6곳'(calc2_out §3 7곳 중 파크리오 뺀 6곳 23~28·14·14%) · '어느 한양' → 한양1차
# 꼴 ⓐ: 첫 줄 = 185 '파크리오가 38%로 가장 높았어요.'(숫자·17자) → 186 14% 한 쌍(compete.md 잘된 이유 1) → 184 전세가율 뜻
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-3')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {}
for _d in ('stock', 's2/stock', 's3/stock'):
    for c in json.load(open(os.path.join(VID, 'public', 'bg', 'h3', _d, 'credits.json'), encoding='utf-8')):
        CRED.setdefault(str(c['id']), dict(c, dir=_d))
TAIL = 36
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def sc(label, lines, data):
    ls = [L(t) for t in lines]
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-3 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('전세가율', ['파크리오가 38%로', '압구정 한양은 14%로', '매매값 중에 전세 보증금이'],
       {'tiles': [['본 단지 7곳 중 가장 높음 · 신천동 파크리오 84㎡대', '38%', '', 0, 'ink'], ['가장 낮음 · 압구정 한양1차 가장 작은 집 49~51㎡', '14%', '', 80, 'ink'], ['전세가율 = 전세 ÷ 매매값', '새로 맺은 전세 기준', '', 154, 'ink']]}),
    sc('차이', ['압구정 한양아파트에서 가장 작은', '매매는 40억이 넘었으니', '같은 신천동 안에서도 장미'],
       {'tiles': [['압구정 한양 가장 작은 집', '새 전세 5억 반', '', 0, 'ink'], ['매매', '40억 넘음', '', 126, 'ink'], ['파크리오와 같은 신천동 · 장미아파트 81~83㎡', '23%', '', 221, 'ink']]}),
    sc('이유', ['왜 이렇게 차이가 날까요?', '다만 숫자로 보이는 건', '1980년대까지 지은 단지'],
       {'tiles': [['왜 차이가 날까', '실거래 자료엔 이유 없음', '', 0, 'ink'], ['새 단지 파크리오만', '30% 넘음', '', 118, 'ink'], ['나머지 6곳 · 1980년대까지 지음', '모두 30% 아래', '', 265, 'ink']]}),
    sc('새 계약만', ['파크리오 국민평형은 새로 맺은', '살던 사람이 다시 맺은', '그러니 전세 시세를 볼 땐'],
       {'tiles': [['파크리오 매매 29억대 · 새로 맺은 전세', '11억 정도', '', 0, 'ink'], ['살던 사람이 다시 맺은 계약', '5천만원쯤 낮음', '', 114, 'ink'], ['전세 시세 볼 때', '새로 맺은 계약만', '', 201, 'ink']]}),
]
need = ['38%', '14%', '23%', '11.00억', '10.50억', '5.50억', '40.67억']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나 — (줄 번호, 클립, 시작 초) · H-3 롱폼에서 눈 검사 통과한 Pexels 풀(bg/h3)
# 10/26 copywriter: 4~15초 질문 안(A-49) — 장면 순서 전세가율→차이→이유→새 계약만, 끝 줄 '새로 집을 구하는…'(바로 앞 줄과 같은 말) 뺌 · 배경은 줄마다 원래 짝 그대로(옛 줄 번호 1,2,3,7,8,9,10,11,12,4,5,6)
# 11/1 PD: 안전 영역 8프레임 — 6962707(미국 세금 서식·계산기 자판)·8482325('HOME FOR SALE' 간판, 우리 글자와 겹침) → 글자 없는 서울 밤 아파트·이삿짐 상자
BG = [(1, '37500921', 0), (2, '30975009', 5), (3, '8471105', 2), (4, '12079562', 5), (5, '38029457', 2), (6, '29303349', 10), (7, '38259256', 2), (8, '34630604', 2), (9, '16392935', 2), (10, '4554447', 1), (11, '8478946', 2), (12, '7578842', 0)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    src = f"bg/h3/{CRED[cid]['dir']}/{cid}.mp4"
    assert os.path.exists(os.path.join(VID, 'public', src)), src
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': src, 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c].get('author', '').strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'h3s_jeonse', 'v': 2, 'look': 'live', 'question': ['서울 아파트 7곳 실거래', '전세는 매매값의 몇 %?'], 'hot': '몇 %',
     'answer': {'label': '새로 맺은 전세 ÷ 매매값', 'items': ['파크리오 38%', '압구정 한양 14%'], 'arrow': False, 'note': '세 배 가까이'},
     'base': '국토교통부 아파트 매매·전월세 실거래가(계약 2025.11~2026.10, 2026-10-22 받음) · 파이어맵 계산', 'long': 'gvlX2KQcI8g',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h3s_jeonse.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h3s_jeonse: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
