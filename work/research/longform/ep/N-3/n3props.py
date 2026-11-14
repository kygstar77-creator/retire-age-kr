# N-3 화면 재료 — script.md(편집 서명 11/14 07:07 016e3499) + voice.json(Chirp 3 HD Charon 1.1, 173줄) + shot_plan.md 장면 계획 → work/video/n3.json (Remotion 'N3' = H4.tsx 부품 + Mo 움직이는 판 넷)
#   py -3.12 work/research/longform/ep/N-3/n3props.py
# 11/14 PD(정기 10:1x): h4props.py 틀을 빌림. 판 = visual 종이 판 그림(bg/n3/board, 숫자 박힘, shot_plan 품질 판정 끝) ↔ 움직이는 판(mo: cap·blocks·stairs·mean, motion_preview/n3_motion.json)
#   ↔ Pexels 실사(bg/n3/stock, 11/14 PD 받음·눈 확인 — 간판·상표·번호판·외국 지폐·숫자 화면 클립은 뺌) ↔ 장 카드(ask 'N장').
#   shot_plan에 실사 줄이 없어(11/4 실사 11줄 '못함' 뒤 판으로 바뀜) 판 묶음 20초(bgcheck)·실사 10%를 맞추려고 판 사이에 실사를 끼움 — 실사 say는 숫자 없는 말만.
#   안 쓴 판: n3_why_q(4장 질문은 ask 카드가 받음)·n3_back357(6장 첫 줄은 ask)·n3_rev_q 대신 rev300 앞 짧게 씀 — 아래 표 참고.
# 가상 인물 없음. 숫자: props 안 숫자 글자는 script·calc_out·research에 있는 글자만 — 맨 아래 numcheck가 막는다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
GAP_TRIM = 3   # B-31 쉼 관문 — K-1·P-3·H-4와 같은 값
END_PAD = 20 * 30 - TAIL   # 마지막 말 뒤 화면 20초(TAIL 포함) — registry B-50
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'calc_mean_out.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 173, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)][:9]
assert len(HEADS) == 9 and HEADS[2].startswith('연봉 사다리'), HEADS
MO = json.load(open(os.path.join(EP, 'motion_preview', 'n3_motion.json'), encoding='utf-8'))
USED = set()

CR = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'n3', 'stock', 'credits.json'), encoding='utf-8'))}
HAVE = {'3202364': 15.0, '7687970': 11.0, '9823115': 5.0, '5923592': 10.0, '7822029': 8.0, '7535095': 9.0,
        '6771533': 10.0, '4992563': 10.0, '28587785': 15.0, '8783211': 20.0}   # 11/14 cv2 실측(눈 확인 통과 10개)
END_PIC = 'bg/n3/over/n3_end_r41.png'   # shot_plan r41(Pexels 8890683 노을 창 + 자체 글자)

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
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'n3', 'board', f + '.png')), f
    return S('pic', idx, pic=f'bg/n3/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)
def mo(key, idx):
    m = MO[key]; want = [t['text'] for t in m['lines']]
    assert [ALL[i]['text'] for i in idx] == want, ('움직이는 판 줄 다름', key)
    return S('mo', idx, part=key, title=m['title'], sub=m['sub'], chapter=m['chapter'], source=m['source'], p=m['data'])
USEDBG = {}
def broll(cid, idx, say=None, frm=None, **kw):
    assert cid in HAVE, ('눈 확인 안 한 클립', cid)
    c = CR[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; have = HAVE[cid] - 0.5
    s = S('broll', idx, src=f'bg/n3/stock/{cid}.mp4', license=f"Pexels {cid} 무료({c['author'].strip()})", say=say, side='left', **kw)
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, have - sec), k * 5)
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = have
    return s

scenes = []
# ── 0. 여는 말 (0~6) ──
scenes += [
    broll('7687970', [0], '연봉 실수령액'),
    board('n3_hook357', [1, 2]),
    board('n3_line100_33', [3, 4, 5]),
    board('n3_toc', [6]),
]
# ── 1. '연봉'은 어느 돈인가 (7~20) ──
scenes += [
    ask(1, [7]),
    board('n3_gross', [8, 9, 10]),
    broll('3202364', [11], '국세청은 다른 숫자로 센다'),
    board('n3_three_money', [12]),
    board('n3_4760', [13, 14, 15]),
    broll('7535095', [16, 17], '계약서 말고 총급여'),
    board('n3_percentile_box', [18, 19, 20]),
]
# ── 2. 연봉 사다리 (21~53) ──
scenes += [
    ask(2, [21]),
    board('n3_seven', [22, 23, 24]),
    broll('7822029', [25, 26], '한 칸 위로'),
    board('n3_ladder_a', [27, 28, 29, 30, 31]),
    broll('28587785', [32, 33], '칸이 높아지면'),
    board('n3_ladder_b', [34, 35, 36, 37, 38, 39]),
    broll('8783211', [40], '막대로 놓으면'),
    board('n3_share_bars', [41, 42, 43]),
    board('n3_netcheck', [44, 45]),
    broll('4992563', [46], '두 칸만 더'),
    board('n3_ladder_c', [47, 48, 49, 50, 51, 52, 53]),
]
# ── 3. 어디서 빠지나 (54~73) ──
scenes += [
    ask(3, [54]),
    board('n3_leak_q', [55]),
    board('n3_waterfall', [56, 57, 58]),
    broll('5923592', [59], '빠지는 돈의 구성'),
    board('n3_donuts', [60, 61, 62, 63, 64, 65, 66]),
    mo('blocks', [67, 68]),
    mo('cap', [69, 70, 71, 72, 73]),
]
# ── 4. 1천만원 오를 때 (74~100) ──
scenes += [
    ask(4, [74]),
    board('n3_x18', [75, 76]),
    broll('6771533', [77, 78], '오른 연봉, 통장에는?'),
    board('n3_raise_table', [79, 80, 81, 82, 83]),
    broll('9823115', [84], '남는 몫이 줄어드는 칸'),
    board('n3_taxsteps', [85, 86, 87, 88]),
    broll('28587785', [89], '다시 올라가는 칸'),
    board('n3_raise_table_b', [90, 91]),
    broll('8783211', [92, 93], '통장 금액으로 바꿔 보기'),
    board('n3_raise_top', [94, 95, 96, 97, 98, 99, 100]),
]
# ── 5. 거꾸로 (101~122) ──
scenes += [
    ask(5, [101]),
    board('n3_rev_q', [102]),
    board('n3_rev300', [103, 104]),
    mo('stairs', [105, 106, 107, 108, 109, 110, 111, 112, 113, 114]),
    broll('4992563', [115], '세율 계단을 거꾸로'),
    broll('7535095', [116], '세후를 연봉으로'),
    board('n3_rev_cond', [117, 118, 119, 120]),
    broll('5923592', [121, 122], '사람마다 다른 연봉'),
]
# ── 6. 같은 연봉, 다른 통장 (123~145) ──
scenes += [
    ask(6, [123]),
    broll('7822029', [124], '훨씬 적게 들어온다는 댓글'),
    board('n3_nontax', [125, 126, 127, 128]),
    broll('6771533', [129, 130], '가족 수로도 달라진다'),
    board('n3_family', [131, 132, 133, 134]),
    broll('3202364', [135], '떼는 크기를 고른다'),
    board('n3_8020', [136, 137, 138, 139, 140]),
    broll('28587785', [141], '내는 때만 바뀐다'),
    board('n3_trap_yearend', [142, 143, 144, 145]),
]
# ── 7. 평균과 상위 25% (146~165) ──
scenes += [
    ask(7, [146]),
    board('n3_top25_q', [147, 148, 149, 150]),
    broll('9823115', [151], '자동완성에 뜨는 상위권'),
    board('n3_top25_10', [152, 153]),
    mo('mean', [154, 155, 156, 157, 158, 159, 160, 161]),
    board('n3_partyear', [162, 163, 164, 165]),
]
# ── 8. 내 숫자 넣기 (166~172) ──
scenes += [
    ask(8, [166]),
    board('n3_calc_site', [167, 168]),
    board('n3_sameformula', [169, 170]),
    broll('7687970', [171]),
    S('pic', [172], pic=END_PIC, license='Pexels 8890683 무료(Yaroslav Shuraev) + 파이어맵 글자', baked=True, zoom=[1.0, 1.10], cx=50, cy=50),
]
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})
assert os.path.exists(os.path.join(VID, 'public', END_PIC))

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
mo_long = [(s['data']['part'], round(s['frames'] / FPS, 1)) for s in scenes if s['kind'] == 'mo' and s['frames'] / FPS > 19.5]
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

SKIP = {'audio', 'src', 'license', 'kind', 'from', 'side', 'pic', 'inset', 'zoom', 'cx', 'cy', 'baked', 'dark', 'badge', 'blur', 'x', 'part', 'seed'}
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
    for st in strings({k: v for k, v in s['data'].items() if not (s['kind'] == 'mo' and k == 'p')}):   # 움직이는 판 속 숫자(8.9% 같은 반올림)는 motion_preview/n3props.py가 calc_out으로 assert
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,'); nnum += 1
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

tot = sum(s['frames'] for s in scenes)
live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and '/board/' not in s['data']['pic']))
p = {'fps': FPS, 'scenes': scenes, 'badge': ''}
json.dump(p, open(os.path.join(VID, 'n3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)] + [{'id': 8890683, 'used': 1, 'desc_line': 'end r41(visual stock_credits.json window_dusk)'}],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'N-3 n3.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))}'
      f' · 실사(Pexels+끝) {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
      f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · numcheck {nnum}덩이 불일치 0 · 20초 넘는 움직이는 판 {mo_long}')
