# P-3 화면 재료 — script.md(편집 서명) + voice.json(Chirp 3 HD Charon 1.1, 111줄) + shot_plan.md 장면 계획 → work/video/p3.json (Remotion 'P3' = K1.tsx 부품 그대로)
#   py -3.12 work/research/longform/ep/P-3/p3props.py
# 11/9 PD(06:1x 회차): k1props.py 틀을 빌림. 판 = visual 종이 판 그림(bg/p3/board, 숫자 박힘) ↔ AI 실사(bg/p3/ai) ↔ 글자 박힌 실사(bg/p3/over) ↔ Pexels(bg/p3/stock) ↔ 장 카드(ask 'N장').
# shot_plan 행과 다른 곳(visual이 shot_plan 줄·비교 그림 맞춤): 장 첫 줄은 장 카드가 가져감(kin_q·trap_cut 첫 줄·next_year·early_q 첫 줄),
#   판끼리는 ffmpeg 컷이 안 잡혀(K-1 11/8 실측 0.09~0.15) 판 묶음이 20초 넘는 곳에 실사를 끼움 · 11/3 심사에서 뺀 클립(passbook_finger·old_paper·drawer_paper·calendar_flip·passbook_atm·phone_pickup)은 안 씀(11/9 눈 확인).
# 가상 인물 없음. 숫자: props 안 숫자 글자는 calc_out·script·research에 있는 글자만 — 맨 아래 numcheck가 막는다.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
GAP_TRIM = 3   # 11/9 PD: B-31 쉼 관문 — K-1 11/9·H-3 10/21과 같은 수법(만드는 값), 줄 사이 빈틈 6→3프레임, 소리는 안 자름
END_PAD = 23 * 30   # 맺는 말 뒤 숨 3초 + 최종 화면 자리 20초(answer/6388789)
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 111, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)][:9]
assert len(HEADS) == 9 and HEADS[1].startswith('문턱'), HEADS
USED = set()

CR = {c['scene'].split('/')[-1][:-4]: c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'p3', 'stock', 'credits.json'), encoding='utf-8'))}
HAVE = {'mailbox_hand': 10.8, 'open_bill': 12.0, 'calculator_hand': 11.2, 'calendar_jan': 17.2, 'queue_ticket': 6.2,
        'mail_november': 12.7, 'bench_backs': 12.0, 'apartment_windows': 19.8}   # 11/9 ffprobe 실측

def L(i):
    assert i not in USED, ('두 번 씀', i); USED.add(i)
    l = ALL[i]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), i
    fr = l['frames'] - GAP_TRIM; assert fr >= int(l['sec'] * FPS + 0.999), ('소리가 잘림', i)   # 줄 사이 빈틈만 줄임
    return {'text': l['text'], 'audio': l['audio'], 'frames': fr, 'cap': None, 'i': i}

def S(kind, idx, **data):
    ls = [L(i) for i in idx]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}

def ask(ch, idx): return S('ask', idx, n=f'{ch}장', q=HEADS[ch])
def board(f, idx, z=(1.0, 1.04)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'p3', 'board', f + '.png')), f
    return S('pic', idx, pic=f'bg/p3/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)
def ai(f, idx, z=(1.0, 1.08)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'p3', 'ai', f + '.png')), f
    return S('pic', idx, pic=f'bg/p3/ai/{f}.png', license='AI 생성 그림(RealVisXL V5.0, openrail++)', badge='AI 생성 그림', zoom=list(z))
def over(f, idx, license, badge=None, z=(1.0, 1.05)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'p3', 'over', f + '.png')), f
    return S('pic', idx, pic=f'bg/p3/over/{f}.png', license=license, baked=True, zoom=list(z), **({'badge': badge} if badge else {}))
USEDBG = {}
def broll(name, idx, say=None):
    c = CR[name]; k = USEDBG.get(name, 0); USEDBG[name] = k + 1; have = HAVE[name] - 0.5
    s = S('broll', idx, src=f'bg/p3/stock/{name}.mp4', license=f"Pexels {c['id']} 무료({c['author'].strip()})", say=say, side='left')
    sec = s['frames'] / FPS; frm = 0 if k == 0 else min(max(0, have - sec), k * 6)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = have
    return s

scenes = []
# ── 0. 여는 말 (r01~r06) ──
scenes += [
    broll('mailbox_hand', [0], '파이어맵 · 건강보험 피부양자'),
    board('p3_hook', [1]),
    over('p3_over_r03', [2, 3], 'AI 생성 그림(RealVisXL V5.0, openrail++) 위 파이어맵 글자', badge='AI 생성 그림'),
    ai('notice_magnifier', [4]),
    board('p3_answer', [5, 6, 7]),
    board('p3_auto_over', [8]),
    broll('mail_november', [9]),
]
# ── 1. 문턱 (r07~r12) ──
scenes += [
    ask(1, [10]),
    board('p3_ruler', [11, 12]),
    board('p3_public_all', [13]),
    broll('queue_ticket', [14]),
    board('p3_public_private', [15]),
    broll('mailbox_hand', [16]),
    board('p3_two_bars', [17, 18, 19, 20]),
]
# ── 2. 넘으면 매달 얼마 (r13~r22) ──
scenes += [
    ask(2, [21]),
    board('p3_calc_health', [22, 23, 24]),
    broll('open_bill', [25]),
    board('p3_calc_ltc', [26, 27, 28]),
    broll('calculator_hand', [29]),
    board('p3_step_table', [30]),
    board('p3_four_rows', [31, 32, 33, 34]),
    broll('mail_november', [35, 36], '선을 처음 넘는 그 한 칸'),
    board('p3_10years', [37, 38, 39]),
    broll('calendar_jan', [40, 41]),
    board('p3_raise', [42, 43, 44]),
    board('p3_164_163', [45]),
]
# ── 3. 깎아 준다던데요 (r23~r26) ──
scenes += [
    ask(3, [46]),
    board('p3_trap_cut', [47, 48, 49]),
    board('p3_cut_steps', [50, 51]),
    broll('queue_ticket', [52]),
    board('p3_cut_calendar', [53, 54]),
    board('p3_old_erase', [55]),
]
# ── 4. 언제 다시 보나 (r27~r30) ──
scenes += [
    ask(4, [56]),
    board('p3_calendar_rule', [57]),
    board('p3_timeline', [58]),
    broll('mail_november', [59]),
    board('p3_nov_notice', [60, 61, 62, 63, 64]),
    broll('open_bill', [65, 66], '공단 고객센터에 먼저 물어보기'),
]
# ── 5. 이자·배당 (r31~r36) ──
scenes += [
    ask(5, [67]),
    board('p3_1000_line', [68, 69]),
    board('p3_call_first', [70]),
    broll('calculator_hand', [71], '넘은 만큼이 아니라 전부'),
    board('p3_mix_calc', [72, 73, 74, 75]),
    broll('calendar_jan', [76]),
    board('p3_scale_999', [77, 78, 79]),
]
# ── 6. 누구라면 (r37~r40) ──
scenes += [
    ask(6, [80]),
    over('p3_over_r34', [81], f"Pexels {CR['apartment_windows']['id']} 무료({CR['apartment_windows']['author'].strip()}) 위 파이어맵 글자"),
    board('p3_property', [82, 83]),
    broll('calculator_hand', [84], '사업자등록이 있으면'),
    board('p3_couple', [85, 86, 87]),
    broll('bench_backs', [88], '두 사람 다 빠져요'),
    board('p3_three_roads', [89, 90]),
]
# ── 7. 흔한 말 하나 (r41~r43) ──
scenes += [
    ask(7, [91]),
    board('p3_early_q', [92, 93, 94]),
    broll('bench_backs', [95, 96]),
    board('p3_scale', [97, 98]),
    broll('open_bill', [99, 100]),
    board('p3_four_years', [101, 102, 103, 104]),
    broll('apartment_windows', [105]),
]
# ── 8. 그래서 할 일 (r44~r46) ──
scenes += [
    ask(8, [106]),
    board('p3_take_notice', [107]),
    ai('tea_bill_steam', [108, 109, 110]),
]
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})

USEDBG_IDS = {}
for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
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
for a, b in zip(scenes, scenes[1:]): assert a['data'].get('pic') is None or a['data'].get('pic') != b['data'].get('pic'), ('같은 그림 연달아', a['data']['pic'])
long = [(s['data'].get('pic'), round(s['frames'] / FPS, 1)) for s in scenes[:-1] if s['kind'] == 'pic' and s['frames'] / FPS > 19.5]
assert not long, ('판 하나 20초 넘음', long)
# 판(board)끼리 이어진 묶음 — 컷이 안 잡히는 길이(bgcheck '같은 판 20초')
runs, cur = [], 0
for s in scenes[:-1]:
    if s['kind'] == 'pic' and '/board/' in s['data']['pic']: cur += s['frames']
    else: runs.append(cur); cur = 0
runs.append(cur)
assert max(runs) / FPS <= 19.5, ('판 묶음 20초 넘음', max(runs) / FPS)
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

SKIP = {'audio', 'src', 'license', 'kind', 'from', 'side', 'pic', 'inset', 'zoom', 'cx', 'cy', 'baked', 'dark', 'badge'}
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
json.dump(p, open(os.path.join(VID, 'p3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': CR[n]['id'], 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)]
          + [{'id': CR['apartment_windows']['id'], 'used': 1, 'desc_line': CR['apartment_windows']['desc_line']}] * ('apartment_windows' not in USEDBG),
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'P-3 p3.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))}'
      f' · 실사(Pexels+AI+over) {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
      f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · numcheck {nnum}덩이 불일치 0')
