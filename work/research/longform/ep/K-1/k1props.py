# K-1 화면 재료 — script.md(편집 서명) + voice.json(Chirp 3 HD Charon 1.1, 123줄) + shot_plan.md 장면 계획 → work/video/k1.json (Remotion 'K1' = DETF1 부품 그대로)
#   py -3.12 work/research/longform/ep/K-1/k1props.py
# 11/3 PD(18:1x 회차): de1props.py 틀을 빌림. K-1은 판이 visual 종이 판 그림(bg/k1/board, 숫자 박힘 — visual이 9월분으로 다시 그리는 중, 파일 이름 그대로)이라
#   판 = pic(baked·inset·어두운 바깥) ↔ AI 실사(bg/k1/ai, 'AI 생성 그림' 표시) ↔ Pexels 실사(bg/k1/stock) ↔ 장 카드(ask 'N장', 띠링).
# 장면은 shot_plan.md '# 장면 계획' r01~r36 순서 — 판 하나 20초 넘지 않게(bgcheck) 같은 판을 두 번 쓸 땐 사이에 실사를 둔다. 가상 인물 없음.
# 숫자: props 안 숫자 글자는 facts·calc5_out·script.md에 있는 글자만 — 맨 아래 numcheck가 막는다(판 그림 안 숫자는 visual·편집 서명 몫).
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
FPS, TAIL = 30, 75
END_PAD = 23 * 30   # 맺는 말 뒤 숨 3초 + 최종 화면 자리 20초(answer/6388789)
CALC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc5_out.txt', 'facts.txt'))
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 123, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
USED = set()

CR = {c['id']: c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
STOCK = {'newspaper_hand': (5905282, 8.0), 'loan_papers': (7821634, 7.3), 'rain_window': (4786522, 90.1),
         'coffee_cloudy': (6343938, 10.9), 'notebook_hand': (6326847, 12.5), 'dusk_table': (6780621, 6.0)}   # 길이는 11/3 ffmpeg 실측

def L(t, cap=None):
    hit = [i for i, l in enumerate(ALL) if l['text'].startswith(t)]; assert len(hit) == 1, (t, hit)
    i = hit[0]; assert i not in USED, ('두 번 씀', t); USED.add(i)
    l = ALL[i]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    return {'text': l['text'], 'audio': l['audio'], 'frames': l['frames'], 'cap': cap, 'i': i}

def S(kind, lines, **data):
    ls = [L(t) for t in lines]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}

def ask(n, q, lines, frm=None): return S('ask', lines, n=n, q=q, **({'from': frm} if frm else {}))
def board(f, lines, z=(1.0, 1.04)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'k1', 'board', f + '.png')), f
    return S('pic', lines, pic=f'bg/k1/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)
def ai(f, lines, z=(1.0, 1.08)):
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'k1', 'ai', f + '.png')), f
    return S('pic', lines, pic=f'bg/k1/ai/{f}.png', license='AI 생성 그림(RealVisXL V5.0, openrail++)', badge='AI 생성 그림', zoom=list(z))
USEDBG = {}
def broll(name, lines, say, **kw):
    cid, have = STOCK[name]; c = CR[cid]; k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; have -= 0.5
    s = S('broll', lines, src=f'bg/k1/stock/{name}.mp4', license=f"Pexels {cid} 무료({c['author'].strip()})", say=say, side='left', **kw)
    sec = s['frames'] / FPS; frm = 0 if k == 0 else int(min(max(0, have - sec), k * 6))   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = frm * FPS; s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = have
    return s

scenes = []
# ── 0. 예고 (r01~r06) ──
scenes += [
    S('brand', ['안녕하세요, 파이어맵입니다.'], line='오늘은 금리 이야기', sub='한국은행 9월분 숫자로'),
    ai('bank_ticket', ['미국 국채금리가 올가을']),
    board('k1_two_q', ['그럼 내 예금 이자와']),
    ai('phone_tea_over', ['먼저, 정기예금 1억원이']),
    ai('keys_envelope', ['그리고 2021년 여름에']),
    board('k1_answer2', ['답부터 말하면', '고정 기간이 끝난 대출은']),
    board('k1_q5', ['뉴스는 대부분', '오늘은 지난 1년', '그런데 흔히 하는 말']),
]
# ── 1. 미국 국채금리 5% (r07~r11) ──
scenes += [
    ask('1장', '미국 국채금리 5%, 무슨 숫자인가', ['국채금리는 나라가']),
    broll('newspaper_hand', ['미국 정부가 10년 동안'], '뉴스에 자주 나오는 미국 국채금리'),
    board('k1_bond_note', ['미국 정부에 만 달러를']),
    board('k1_dgs10', ['이 금리가 처음 그 선에', '그 뒤 한 달 사이', '가장 높았던 날은', '지난번 이만큼', '그달 평균이 4']),
    ai('passbook', ['그때 우리 예금 금리가']),
    board('k1_2007', ['더 거슬러 가면', '그달 평균은 5', '그때 한국 주택담보대출', '지금 평균은 그때보다']),
    board('k1_us_kr_now', ['이 영상을 만든 무렵', '%포인트는 금리']),
    broll('newspaper_hand', ['미국 금리가 왜 이렇게'], '오늘은 내 통장 쪽 숫자만'),
]
# ── 2. 내 예금 이자 (r12~r18) ──
scenes += [
    ask('2장', '내 예금 이자는 얼마나 따라왔나', ['먼저 예금부터']),
    board('k1_passbook', ['한국은행은 은행들이', '1년짜리 정기예금']),
    board('k1_dep_bar', ['작년엔 2', '올해는 3', '그사이 1%포인트']),
    board('k1_dep_calc', ['다음 달 만기인', '작년 금리라면', '지금 금리면 3', '차이가 87', '한 달로 나누면']),
    board('k1_coins3', ['더 예전과 비교하면', '다섯 해 전 이맘때', '같은 돈을 맡겼다면']),
    ai('phone_scroll', ['다른 금리 영상 댓글에 이런', '그래서 2억원을 평균', '작년보다, 세금']),
    board('k1_cofix89', ['예금 금리와 같이', '코픽스는 은행들이', '그달 새로 모은 돈을 보는', '은행이 돈 모으는 값이']),
    board('k1_gap', ['다른 금리 영상 댓글에서', '새로 맺은 주택담보대출', '작년이나 지금이나', '그사이엔 거의']),
]
# ── 3. 내 대출 이자 (r19~r25) ──
scenes += [
    ask('3장', '내 대출 이자는 — 고정형과 변동형', ['이번엔 대출인데요']),
    broll('loan_papers', ['정해진 기간 동안'], '고정형과 변동형'),
    board('k1_fix_var', ['1년 동안 새로 받은', '고정형은 1%포인트', '변동형은 그 절반을']),
    board('k1_cross', ['그런데 1년 전엔', '올해 4월부터']),
    board('k1_3eok_table', ['3억원을 서른 해 동안 갚는 대출', '작년 고정형 금리라면', '지금 금리면 1', '새로 빌리는 사람이라면', '변동형으로 새로 빌렸다면']),
    broll('rain_window', ['그럼 고정형과 변동형 중', '그럼 변동형은 왜'], '어느 쪽이 나을지는 앞으로 금리에 달린 일'),
    board('k1_cofix3', ['변동형 금리는 보통', '그런데 코픽스는 한 가지가', '그달 새로 모은 돈만', '잔액 기준 코픽스에는']),
    broll('rain_window', ['찬물이 가득한'], '온도가 천천히 오르듯'),
    board('k1_cofix89', ['같은 기간 신규 코픽스는', '잔액 코픽스는', '다만 변동형 평균이']),
    board('k1_trap', ['여기서 조심할 게', '하나, 내 변동금리는', '둘, 오늘 본']),
]
# ── 4. 미국 때문일까 (r26~r30) ──
scenes += [
    ask('4장', '미국 때문일까', ['이제 흔한 말 하나를']),
    broll('coffee_cloudy', ['은행 금리 자료가'], '작년과 올해 같은 달끼리'),
    board('k1_us_kr_1y', ['한 해 동안 미국 국채금리는', '같은 기간 한국 국채금리는', '한국 쪽이 두 배']),
    broll('newspaper_hand', ['그리고 은행 평균 금리와'], '더 닮은 쪽은 미국이 아니었다'),
    ai('calendar_hand', ['2013년부터 달마다', '정기예금과 고정형 대출은', '예를 들어 국채가']),
    board('k1_samedir', ['정기예금 평균은 한국', '미국 국채와는 열 달에', '고정형 대출도 한국']),
    broll('dusk_table', ['다만 같이 움직였다는'], '같이 움직였다는 뜻이지 그 때문은 아니다'),
    board('k1_samedir', ['변동형은 오르내림 폭', '미국과 한국 10년', '그래도 은행 평균 금리에']),
    board('k1_base_steps', ['이 비교 기간에', '한국 국채가 왜']),
    board('k1_2023', ['그럼 앞에서 본 그때', '예금 평균 금리는 그해', '4.2%였죠', '그로부터 석 달', '그때는 오를 때도']),
]
# ── 5. 고정 끝나는 사람 (r31~r33) ──
scenes += [
    ask('5장', '고정 끝나는 사람은 얼마나 오르나', ['이제 고정금리 대출']),
    board('k1_calendar', ['고정 기간이 끝나는 사람은', '여기서부터는 작년이']),
    ai('keys_envelope', ['처음에 말한 분', '3억원을 서른 해 동안 갚는 고정형']),
    board('k1_reset_flow', ['그때 고정형 평균', '한 달에 126', '5년이 지나', '한 달에 158', '새로 빌리는 사람의']),
    board('k1_answer2', ['2021년에 내던 돈보다', '한 해면 370']),
    board('k1_reset_two', ['변동형 평균으로 다시', '이건 평균 금리로']),
    ai('phone_scroll', ['고정 5년이 길어', '2021년 무렵 낮은']),
    board('k1_reset_two', ['그날이 오면 다시']),
]
# ── 6. 그래서 볼 날짜 (r34~r36) ──
scenes += [
    ask('6장', '그래서 볼 날짜', ['오늘 하실 일은 하나']),
    board('k1_check3', ['변동형이면 금리가', '대출이라면 그날 금리로']),
    broll('notebook_hand', ['이 셈은 파이어맵'], '대출이자 계산기'),
    ai('passbook', ['예금이라면 만기 날']),
    ai('dusk_table', ['미국 금리 5%라는', '다음 영상에서']),
]
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})

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
SRCDOC = CALC + SCRIPT
bad = []; nnum = 0
for s in scenes:
    for st in strings(s['data']):
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,'); nnum += 1
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

tot = sum(s['frames'] for s in scenes); live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and 'bg/k1/ai/' in s['data']['pic']))
p = {'fps': FPS, 'scenes': scenes, 'badge': ''}
json.dump(p, open(os.path.join(VID, 'k1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': c, 'used': USEDBG[c], 'desc_line': CR[c]['desc_line']} for c in sorted(USEDBG)], open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'K-1 k1.json: {tot} 프레임 = {tot / FPS:.1f}초 · 장면 {len(scenes)} · 줄 {len(ALL)} · 종류 {len(set(s["kind"] for s in scenes))}'
      f' · 실사(Pexels+AI) {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초 · numcheck {nnum}덩이 불일치 0')
