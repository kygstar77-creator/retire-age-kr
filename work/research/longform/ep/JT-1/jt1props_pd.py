# JT-1 화면 재료 — script.md(편집 서명 11/16 15:12) + voice.json(Chirp 3 HD Charon 1.1, 165줄, 11/16 18시 녹음) + shot_plan 장면 계획 → work/video/jt1.json (Remotion 'JT1' = N3.tsx 틀 + SumRace)
#   py -3.12 work/research/longform/ep/JT-1/jt1props_pd.py
# 11/16 PD(정기 18:1x): n3props.py 틀을 빌림. 판 = visual 종이 판(bg/jt1/board, 숫자 박힘, shot_plan 품질 판정 끝) ↔ 움직이는 판 race·gap(motion_preview/jt1_motion.json, jt1_cross93·jt1_mid3 자리)
#   ↔ Pexels 실사(bg/jt1/stock: visual 4개 + PD 11/16 8개, 얼굴·글자·숫자·지폐 없는 것만 — check/stock_sheet_*.jpg) ↔ 장 카드(ask).
#   판 묶음 20초(bgcheck)·실사 10%를 맞추려고 판 사이에 실사를 끼움 — 실사 say는 숫자 없는 말만. 가상 인물 없음.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
GAP_TRIM = 3
END_PAD = 20 * 30 - TAIL
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 165, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 8 and HEADS[3].startswith('늦게 들면'), HEADS
MO = json.load(open(os.path.join(EP, 'motion_preview', 'jt1_motion.json'), encoding='utf-8'))
USED = set()
CR = {}
for c in json.load(open(os.path.join(WORK, 'research', 'visual', 'JT-1-shots', 'stock_credits.json'), encoding='utf-8')) + json.load(open(os.path.join(EP, 'stock_pd1116.json'), encoding='utf-8')):
    CR[os.path.basename(c['file']).replace('.mp4', '')] = c
HAVE = {'jt1_handnote': 12.5, 'jt1_market': 10.2, 'jt1_walk': 17.1, 'jt1_window': 17.3, 'jt1_6541138': 21.8, 'jt1_8292925': 14.1, 'jt1_8292929': 10.0,
        'jt1_38781079': 10.6, 'jt1_6781559': 7.3, 'jt1_946148': 21.4, 'jt1_38405960': 8.3, 'jt1_7578842': 11.2}   # 11/16 ffprobe
MINFROM = {'jt1_6541138': 4.0}   # 앞 4초 플래너 표지 글자
END_PIC = 'bg/jt1/stock/jt1_window.jpg'


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
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'jt1', 'board', f + '.png')), f
    return S('pic', idx, pic=f'bg/jt1/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


def mo(key, idx):
    m = MO[key]; want = [t['text'] for t in m['lines']]
    assert [ALL[i]['text'] for i in idx] == want, ('움직이는 판 줄 다름', key)
    return S('mo', idx, part=key, title=m['title'], sub=m['sub'], chapter=m['chapter'], source=m['source'], p=m['data'])


USEDBG = {}


def broll(cid, idx, say=None, frm=None):
    assert cid in HAVE, ('눈 확인 안 한 클립', cid)
    c = CR[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; have = HAVE[cid] - 0.5
    s = S('broll', idx, src=f'bg/jt1/stock/{cid}.mp4', license=f"Pexels {c['id']} 무료({c['author'].strip()})", say=say, side='left')
    sec = s['frames'] / FPS; lo = MINFROM.get(cid, 0)
    if frm is None: frm = lo if k == 0 else max(lo, min(max(0, have - sec), k * 5))
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = have
    return s


scenes = []
# 0 여는 말 (0~11)
scenes += [broll('jt1_handnote', [0, 1, 2], '주택연금'), board('jt1_note', [3, 4, 5, 6, 7]),
           broll('jt1_6541138', [8], '받은 돈 합이 같아지는 나이'), broll('jt1_946148', [9, 10], '공사 표로 직접 계산'), broll('jt1_8292929', [11], '누가 들 수 있나')]
# 1 누가 들 수 있나 (12~27)
scenes += [ask(1, [12]), board('jt1_check3', [13, 14, 15, 16, 17, 18]), broll('jt1_8292925', [19], '실제로 사는 집'),
           broll('jt1_7578842', [20, 21], '입원·요양이어도'), board('jt1_scale2', [22, 23, 24]), broll('jt1_window', [25, 26, 27], '부부 중 젊은 쪽 나이')]
# 2 내 집값·나이면 매달 얼마 (28~58)
scenes += [ask(2, [28]), board('jt1_grid', [29, 30, 31, 32, 33, 34]), broll('jt1_38781079', [35, 36], '나이만 바꾸면'),
           board('jt1_grid', [37, 38, 39, 40]), broll('jt1_6781559', [41], '끝까지 가지 않는 줄'), board('jt1_cap', [42, 43, 44, 45, 46, 47]),
           broll('jt1_946148', [48], '표가 바뀐 날'), board('jt1_mar1', [49, 50, 51, 52]), broll('jt1_6541138', [53, 54], '정해진 금액은 그대로'),
           broll('jt1_38405960', [55], '처음 금액에 이미 넣음'), broll('jt1_946148', [56, 57, 58], '정액형 기준')]
# 3 늦게 들면 몇 살에 같아지나 (59~92)
scenes += [ask(3, [59]), broll('jt1_6541138', [60, 61], '기다렸다 들면'), board('jt1_lost', [62, 63]), board('jt1_diff', [64]),
           mo('race', [65, 66, 67]), mo('gap', [68, 69, 70, 71, 72, 73]), broll('jt1_8292925', [74], '나이를 바꿔서'),
           board('jt1_cross81', [75, 76, 77, 78]), broll('jt1_38781079', [79], '이번엔 더 젊을 때'), board('jt1_age3', [80, 81, 82, 83]),
           broll('jt1_946148', [84, 85], '집값보다 드는 나이'), board('jt1_trap_price', [86, 87, 88, 89]), broll('jt1_6541138', [90, 91, 92], '정답이 아니라 잣대')]
# 4 받은 돈은 어디에 쌓이나 (93~116)
scenes += [ask(4, [93]), broll('jt1_8292929', [94], '빚으로 쌓이는 돈'), board('jt1_stack', [95, 96, 97, 98, 99]),
           broll('jt1_7578842', [100, 101], '현금으로 따로 안 냄'), broll('jt1_handnote', [102], '가입할 때 드는 돈'), board('jt1_stack', [103, 104, 105, 106]),
           broll('jt1_window', [107, 108, 109], '잔액이 불어나도'), board('jt1_trap_exit', [110, 111, 112, 113]), broll('jt1_8292925', [114, 115, 116], '이사를 가면')]
# 5 생활비를 얼마나 메우나 (117~129)
scenes += [ask(5, [117]), broll('jt1_market', [118, 119], '노후에 필요한 돈'), board('jt1_43', [120, 121, 122, 123, 124, 125]),
           broll('jt1_946148', [126, 127], '다른 소득에 보태는 돈'), board('jt1_43', [128, 129])]
# 6 돌아가신 뒤, 세금·기초연금 (130~154)
scenes += [ask(6, [130]), broll('jt1_8292929', [131, 132, 133], '집을 맡기는 두 방식'), broll('jt1_6541138', [134, 135, 136, 137], '남은 분이 이어 받음'),
           board('jt1_flow', [138, 139, 140, 141]), broll('jt1_walk', [142, 143, 144], '집을 남기고 싶다면'), board('jt1_tax2', [145, 146, 147, 148, 149]),
           broll('jt1_38781079', [150], '이자도 빼 줌'), board('jt1_tax2', [151, 152]), broll('jt1_38405960', [153, 154], '우대형 확인')]
# 7 정리 (155~164)
scenes += [ask(7, [155]), board('jt1_summary', [156, 157, 158, 159]), broll('jt1_handnote', [160, 161], '예상연금조회'), board('jt1_summary', [162]),
           S('pic', [163, 164], pic=END_PIC, license=f"Pexels {CR['jt1_window']['id']} 무료({CR['jt1_window']['author'].strip()})", baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
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
    for st in strings({k: v for k, v in s['data'].items() if not (s['kind'] == 'mo' and k == 'p')}):   # 움직이는 판 속 숫자는 motion_preview/jt1props.py가 calc_out으로 assert
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,'); nnum += 1
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

tot = sum(s['frames'] for s in scenes)
live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and '/board/' not in s['data']['pic']))
p = {'fps': FPS, 'scenes': scenes, 'badge': ''}
json.dump(p, open(os.path.join(VID, 'jt1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': CR[n]['id'], 'file': n, 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'JT-1 jt1.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))}'
      f' · 실사 {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
      f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · numcheck {nnum}덩이 불일치 0 · 20초 넘는 움직이는 판 {mo_long}')
