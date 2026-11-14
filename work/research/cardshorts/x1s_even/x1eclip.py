# x1s_even — X-1 롱폼(WcBOePkyOOQ) 1장 '본전 환율' 계산을 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-14 22시, p1s_born/p1bclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/x1s_even/x1eclip.py   → work/video/x1s_even.json
# 목소리 = X-1 voice.json 문장 wav 그대로 + 첫 줄 하나만 같은 목소리로 새로 받음(newline.py, Charon 1.1 markup)
# 뺀 줄: '지금 1,339원보다 160원쯤 위'(10/15 환율 — 11/20 공개 땐 '지금'이 틀림) · '석 달 전에 산 경우 1,463원'(상대 날짜, 예 둘로 충분)
# 숫자 원문 = X-1 calc_out.txt §8(본전 환율 = 산 날 환율 ÷ SPY 배수, 끝날 2026-10-15) · facts.txt v3-3(1.16배 = 달러 수익률 16% 예시, SPY 1년 전 배수 1.1640)
# 11/14 이해 1차(43·54·63세): 뜻·할 일 3/3·권유 0/3·응용 계산(10%·1,400원→1,273원) 3/3 · 둘째 예 1,500원이 16%가 아닌 다른 배수라는 말이 없어 '숫자 안 맞음' 3/3 → 칸을 '몇 % 오른 경우 + 나눗셈 식'으로(날짜는 설명란) — 3.6% = facts v3 '3% 넘게 = +3.63%'(SPY 7월 초부터)
# 11/14 2차(47·57·66세): 뜻·할 일·응용·두 예 차이 3/3 · '가장 비싸던 날'이 환율인지 주가인지 3/3 · 1,420.5가 산 날 환율이란 말 없음 2/3 · 렌더 눈 검사: 긴 식에 손 동그라미가 글자를 가로지름 → 칸 이름 '산 날 1,420.5원'·'최고점 1,554.4원', 값 '÷ 배수 = 본전'
# 11/14 렌더 눈 검사(eye/sz27): '조심할 게' 줄 계산기에 상표 글자(CORRECT) → 금화 컷 8369980으로
# 배경 = X-1 stock(Pexels, credits.json) 중 얼굴·지폐 인물·글자 없는 컷 — 11/14 눈 검사(scratchpad x1e/sheet_3)
import os, re, json, sys, subprocess, shutil, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'X-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {}
for s in V['sections']:
    if s.get('title', '').startswith('[0.') or s.get('title', '').startswith('0.'): continue   # 예고 줄(본편 재사용)은 건너뜀 — 같은 글이 본편에 있음
    for l in s['lines']: BYTEXT.setdefault(l['text'], l)
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('facts.txt', 'calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
STOCK = {'dollar_count': 5466769, 'calc_pen': 5923592, 'phone_hands': 6186015, 'clock': 7033607, 'wallet': 34596756, 'gold_coins': 8369980, 'coins': 8661806, 'typing': 6963836}
SEC = {'dollar_count': 13.6, 'calc_pen': 10.4, 'phone_hands': 15.0, 'clock': 32.8, 'wallet': 27.9, 'gold_coins': 7.0, 'coins': 22.6, 'typing': 22.0}   # 11/14 ffmpeg 실측
TAIL = 36
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def sc(label, lines, data, pad=0):
    ls = [L(t) for t in lines]
    if pad: ls[-1] = dict(ls[-1], pad=pad)   # 말 뒤 무음(C1S는 줄 소리를 줄 시작에 두고 장면 길이만큼 화면을 둠 — 11/14 이해 1차 '네 해 묶음 중간 단계 없음' 3/3)
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.~]*', ' '.join(strs)):
        d = d.rstrip('.,~')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·X-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': [{k: v for k, v in l.items() if k != 'pad'} for l in ls], 'frames': sum(l['frames'] for l in ls) + pad, '_pad': pad}


PADX = 50   # 11/14 렌더 미리 보기: 본전 값은 말 닿는 때로 옮겨져 식 칸이 1초만 보임 → 말 뒤 1.7초 쉼에 '산 날 환율 ÷ 배수' 칸(손 동그라미는 마지막 칸 = 나눗셈)
NEW = json.loads(open(os.path.join(HERE, 'newline.json'), encoding='utf-8').read())
BYTEXT[NEW['text']] = NEW
scenes = [
    sc('질문', ['달러로 16% 오른'],
       {'tiles': [['달러 수익률 16%', '본전 환율은?', '', 0, 'ink']]}),
    sc('계산법', ['산 날 환율을, 그 뒤', '증권사 앱에 달러 수익률이'],
       {'tiles': [['본전 환율', '산 날 환율 ÷ 몇 배', '', 0, 'ink'], ['달러 수익률 16%', '÷ 1.16', '', 152, 'ink']]}),
    sc('1년 전', ['1년 전에 산 경우는'],
       {'tiles': [['본전 환율', '1,220원', '', 0, 'ink'], ['산 날 1,420.5원', '÷ 1.1640', '', 130, 'ink']]}, pad=PADX),
    sc('최고점', ['가장 비싸던 날 산 경우는'],
       {'tiles': [['본전 환율', '1,500원', '', 0, 'ink'], ['최고점 1,554.4원', '÷ 1.0363', '', 118, 'ink']]}, pad=PADX),
    sc('조심', ['조심할 게 있어요', '본전 환율은 주가가', '주가가 움직이면 같이'],
       {'tiles': [['본전 환율은', '주가 그대로일 때만', '', 41, 'ink'], ['주가가 움직이면', '본전도 움직여요', '', 157, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st or (s_['_pad'] and t[3] == s_['frames'] - s_['_pad']) for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), s_['label']
for x in ('1,420.5 ÷ SPY 배수 1.1640 = 본전 환율 1,220.3원', '1,554.4 ÷ SPY 배수 1.0363 = 본전 환율 1,500.0원', '1.16배 = 달러 수익률 16%'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'   # safeframe shortKick: 12자 넘는 윗줄은 안 보임(still5) · 큰 값에 긴 식을 두면 손 동그라미가 글자를 가로지름(still_600) → '두 날'은 예마다 '산 날 환율 ÷ 배수' → '본전 환율' 두 박자(본전 값은 말 닿는 때로 safeframe이 옮김)
scenes[-1]['frames'] += TAIL
BG = [('dollar_count', 1), ('calc_pen', 1), ('phone_hands', 1), ('clock', 2), ('wallet', 2), ('gold_coins', 1), ('coins', 1), ('typing', 2)]
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'x1s_even', 'stock', name + '.mp4')
    if not os.path.exists(src):
        os.makedirs(os.path.dirname(src), exist_ok=True); shutil.copyfile(os.path.join(EP, 'stock', f'{STOCK[name]}.mp4'), src)
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/x1s_even/stock/cut/{name}_{st}_{fr}.mp4'   # 11/14: 길이를 이름에 — 쉼(pad)을 더한 뒤 옛 짧은 cut을 다시 쓰던 것
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[str(STOCK[nm])]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'x1s_even', 'v': 1, 'look': 'live', 'question': ['미국 ETF 본전 환율', '달러로 16% 올랐다면, 환율 몇 원까지?'], 'hot': '본전',
     'answer': {'label': '본전 환율 = 산 날 환율 ÷ 주가 몇 배', 'items': ['2025.10.13 매수: 1,220원', '2026.7.2 매수: 1,500원'], 'arrow': False, 'note': 'SPY 2026.10.15 종가 기준 · 주가가 바뀌면 달라짐'},
     'base': '한국은행 매매기준율 · SPY 종가(2026.10.15 기준) · 파이어맵 계산', 'long': 'WcBOePkyOOQ',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'x1s_even.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'x1s_even: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
