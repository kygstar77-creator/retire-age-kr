# H-4 화면 재료 — script.md(편집 서명 11/11 07:06) + voice.json(Chirp 3 HD Charon 1.1, 124줄) + shot_plan.md 장면 계획 → work/video/h4.json (Remotion 'H4' = P3.tsx 부품 그대로 + blur)
#   py -3.12 work/research/longform/ep/H-4/h4props.py
# 11/11 PD(정기 20:4x): p3props.py 틀을 빌림. 판 = visual 종이 판 그림(bg/h4/board, 숫자 박힘) ↔ AI 실사(bg/h4/ai) ↔ Pexels(bg/h4/stock) ↔ 장 카드(ask 'N장').
# shot_plan과 다른 곳: 대본 보강(11/11 36줄) 뒤라 shot_plan의 '대본 줄(요지)'와 줄 위치가 달라짐 — 판은 그 판이 보여 주는 숫자를 말하는 줄에 붙임.
#   memo30·gosi2 판은 지금 대본에 그 말(신고 30일·정비구역 고시)이 없어 안 씀. 실사 위 큰 흰 글(say)은 숫자 금지(TallyBroll)라 말 없는 글로만.
#   판끼리는 ffmpeg 컷이 안 잡혀(K-1 11/8 실측) 판 묶음이 20초 넘는 곳에 실사를 끼움.
# 가상 인물 없음. 숫자: props 안 숫자 글자는 script·calc_out·research에 있는 글자만 — 맨 아래 numcheck가 막는다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
GAP_TRIM = 3   # B-31 쉼 관문 — K-1·P-3과 같은 수법(만드는 값), 줄 사이 빈틈 6→3프레임, 소리는 안 자름
END_PAD = 23 * 30   # 맺는 말 뒤 숨 3초 + 최종 화면 자리 20초(answer/6388789)
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'calc_renew_out.txt', 'research.md', 'facts.txt'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 124, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)][:7]
assert len(HEADS) == 7 and HEADS[1].startswith('서울'), HEADS
USED = set()

CR = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'h4', 'stock', 'credits.json'), encoding='utf-8'))}
NOUSE_EXTRA = {'28803181'}   # 11/11 PD 눈 확인: 캠퍼스 건물 큰 글자 현수막(간판 금지), shot_plan 심사 밖
HAVE = {'31907490': 8.3, '9057559': 11.4, '38259259': 40.5, '31727145': 21.3, '7205591': 5.8, '37873585': 32.9,
        '40294066': 25.5, '6964247': 14.6, '7651886': 11.1, '7317305': 15.4, '28803181': 22.5}   # 11/11 cv2 실측
NOUSE = {k for k, c in CR.items() if str(c.get('use', '')).startswith('안 씀') or '안 씀' in str(c.get('note', ''))}

def L(i):
    assert i not in USED, ('두 번 씀', i); USED.add(i)
    l = ALL[i]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), i
    fr = l['frames'] - GAP_TRIM; assert fr >= int(l['sec'] * FPS + 0.999), ('소리가 잘림', i)
    return {'text': l['text'], 'audio': l['audio'], 'frames': fr, 'cap': None, 'i': i}

def S(kind, idx, **data):
    ls = [L(i) for i in idx]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}

def ask(ch, idx): return S('ask', idx, n=f'{ch}장', q=HEADS[ch])
def board(f, idx, z=(1.0, 1.04)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'h4', 'board', f + '.png')), f
    return S('pic', idx, pic=f'bg/h4/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)
def ai(f, idx, z=(1.0, 1.08)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'h4', 'ai', f + '.png')), f
    return S('pic', idx, pic=f'bg/h4/ai/{f}.png', license='AI 생성 그림(RealVisXL V5.0, openrail++)', badge='AI 생성 그림', zoom=list(z))
USEDBG = {}
def broll(cid, idx, say=None, frm=None, **kw):
    assert cid not in NOUSE | NOUSE_EXTRA, ('심사 못함 클립', cid)
    c = CR[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; have = HAVE[cid] - 0.5
    s = S('broll', idx, src=f'bg/h4/stock/{cid}.mp4', license=f"Pexels {cid} 무료({c['author'].strip()})", say=say, side='left', **kw)
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, have - sec), k * 6)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = have
    return s

TOPBLUR = [{'x': 0, 'y': 0, 'w': 1920, 'h': 660}]   # 31727145 위쪽 건물 상호·전광판·버스 광고(11/11 눈 확인 0·3·6초)
scenes = []
# ── 0. 여는 말 (0~6) ──
scenes += [
    broll('31907490', [0], '광명 아파트 실거래가'),
    broll('38259259', [1], '서울 구 사이에 세우면?'),
    broll('9057559', [2]),
    board('rank26', [3]),
    broll('38259259', [4], '광명이 서울보다 비싸다?'),
    broll('6964247', [5, 6], '예산 안쪽 단지는 어디?', x=70),
]
# ── 1. 서울 25개 구 옆에 세우면 (7~32) ──
scenes += [
    ask(1, [7]),
    broll('31727145', [8], '관악 역 앞보다 비싸다?', blur=TOPBLUR),
    board('source', [9, 10]),
    board('rank_zoom', [11, 12, 13]),
    broll('40294066', [14, 15], '광명보다 낮은 서울 구는?'),
    broll('37873585', [16, 17, 18], '구로·금천은 바로 옆'),
    broll('7651886', [19, 20], '거래 수도 넉넉했다'),
    board('rank_ends', [21, 22, 23, 24]),
    broll('7205591', [25]),
    broll('40294066', [26], '새 단지라면 이야기가 다르다'),
    board('dong3', [27, 28]),
    board('hagan', [29, 30, 31]),
    broll('9057559', [32], '한 해로 늘리면 넉넉하다'),
]
# ── 2. 그럼 '광명 15억'은 어디서 나왔을까 (33~52) ──
scenes += [
    ask(2, [33]),
    broll('37873585', [34, 35], '최근 지은 단지만 떼어 보면'),
    board('new_vs_all', [36]),
    board('new_rank', [37, 38]),
    board('gap171', [39]),
    broll('40294066', [40, 41], '단지 값은 동네 값이 아니다'),
    board('rt_steps', [42, 43]),
    broll('6964247', [44], '가장 많이 찾는 단지', x=70),
    board('zero_deal', [45, 46]),
    broll('38259259', [47, 48], '어디서 나온 숫자인지부터'),
    broll('37873585', [49, 50, 51, 52], '이름 비슷한 다른 단지'),
]
# ── 3. 철산동 안의 사다리 (53~65) ──
scenes += [
    ask(3, [53]),
    board('ladder16', [54, 55, 56, 57, 58]),
    ai('old_stair', [59]),
    board('duel', [60, 61, 62]),
    broll('37873585', [63], '새 집일수록 비싸다?'),
    board('ladder16', [64, 65]),
]
# ── 4. 9억으로 철산동 84㎡ (66~101) ──
scenes += [
    ask(4, [66, 67]),
    broll('6964247', [68], '예산 안쪽 단지는 몇 곳?', x=70),
    board('under9', [69]),
    board('under9b', [70, 71, 72, 73]),
    broll('40294066', [74], '같은 동네 새 단지 전세는?'),
    board('jeonse_line', [75, 76, 77]),
    broll('38259259', [78], '옛 집 매매가 더 낮았다'),
    board('newjeonse_eq', [79, 80]),
    broll('40294066', [81, 82], '신고가 몰린 곳'),
    broll('9057559', [83], '전세 만기를 앞뒀다면'),
    board('jeonse3', [84, 85, 86, 87, 88]),
    broll('6964247', [89, 90, 91], '같은 크기 전세, 폭이 크다', x=70),
    board('ratio', [92, 93, 94]),
    broll('7651886', [95, 96], '새 집 전세냐, 옛 집 매매냐'),
    broll('9057559', [97], '새로 맺은 계약만 보세요'),
    board('trap_renew', [98, 99, 100, 101]),
]
# ── 5. 사려면 붙는 조건 (102~120) ──
scenes += [
    ask(5, [102]),
    board('reg_map', [103]),
    board('loan_q', [104]),
    board('loan6', [105, 106]),
    broll('6964247', [107], '한도는 사람마다 다르다', x=70),
    broll('40294066', [108], '비싼 집은 한도가 준다'),
    board('ladder16', [109, 110]),
    board('cal1231', [111, 112]),
    broll('31907490', [113], '국토교통부 공고 확인'),
    board('steps3', [114, 115, 116]),
    broll('7205591', [117], '세부 조건은 시청에서'),
    board('cal1231', [118, 119]),
    broll('7317305', [120], '은행에서 먼저 확인'),
]
# ── 6. 정리 (121~123) ──
scenes += [
    ask(6, [121]),
    board('summary4', [122]),
    broll('37873585', [123], frm=0),   # 끝 숨 3초+최종 화면 20초 — 33초 클립 앞에서부터
]
scenes[-1]['frames'] += END_PAD
scenes[-1]['data']['_need'] += END_PAD / FPS + TAIL / FPS
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})

for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
for s in scenes: assert s['kind'] != 'broll' or len(s['data']['say'] or '') <= 18, ('say 18자 넘음', s['data']['say'])
short = []
for s in scenes:
    d = s['data']
    if 'from_' in d:
        d['from'] = d.pop('from_')
        if d['_need'] > d['_have'] + 0.5: short.append((d['src'], d['_need'], d['_have']))
        d.pop('_need'); d.pop('_have')
assert not short, ('실사 클립이 말보다 짧다', short)
assert len(USED) == len(ALL), ('안 쓴 줄', [ALL[i]['text'][:24] for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines'] if l['i'] is not None]; assert order == sorted(order), '줄 순서'
for a, b in zip(scenes, scenes[1:]):
    assert a['data'].get('pic') is None or a['data'].get('pic') != b['data'].get('pic'), ('같은 그림 연달아', a['data']['pic'])
    assert a['data'].get('src') is None or a['data'].get('src') != b['data'].get('src'), ('같은 클립 연달아', a['data']['src'])
long = [(s['data'].get('pic'), round(s['frames'] / FPS, 1)) for s in scenes[:-1] if s['kind'] == 'pic' and s['frames'] / FPS > 19.5]
assert not long, ('판 하나 20초 넘음', long)
runs, cur = [], 0
for s in scenes[:-1]:
    if s['kind'] == 'pic' and '/board/' in s['data']['pic']: cur += s['frames']
    else: runs.append(cur); cur = 0
runs.append(cur)
assert max(runs) / FPS <= 19.5, ('판 묶음 20초 넘음', max(runs) / FPS)
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

SKIP = {'audio', 'src', 'license', 'kind', 'from', 'side', 'pic', 'inset', 'zoom', 'cx', 'cy', 'baked', 'dark', 'badge', 'blur', 'x'}
def strings(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in SKIP: continue
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            if not isinstance(v, (int, float)): yield from strings(v)
    elif isinstance(x, str): yield x
bad = []; nnum = 0
for s in scenes:
    for st in strings(s['data']):
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,'); nnum += 1
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

tot = sum(s['frames'] for s in scenes)
live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and '/board/' not in s['data']['pic']))
p = {'fps': FPS, 'scenes': scenes, 'badge': ''}
json.dump(p, open(os.path.join(VID, 'h4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'H-4 h4.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))}'
      f' · 실사(Pexels+AI) {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
      f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · numcheck {nnum}덩이 불일치 0')
