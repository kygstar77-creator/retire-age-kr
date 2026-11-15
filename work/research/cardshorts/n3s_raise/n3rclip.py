# n3s_raise — N-3 롱폼 4장 '연봉 천만원 오를 때 통장은 얼마 느나' 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-15 14시, n2s_ladder/n2lclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/n3s_raise/n3rclip.py   → work/video/n3s_raise.json
# 목소리 = N-3 voice.json 문장 wav 그대로 + 첫 줄 하나만 새로 받음(newline.py t2, Charon 1.1 markup = N-3 tts.json) — a3판 f0 131.9Hz(쓴 14줄 중앙 141.0Hz, -6%)·whisper turbo 받아쓰기 일치 — 첫 문장 '연봉이 오른 만큼…'은 꼴 ⓐ(첫 줄 숫자)에 걸려 버림
# 숫자 원문 = N-3 calc_out.txt §C(3,000→4,000만 +691,373 · 7,000→8,000만 +545,773 65.5%) · script.md(15%→24%, 과세표준 5천만원)
# 배경 = N-3 stock(Pexels, credits.json) 중 얼굴·상표·글자 없는 컷 — 11/15 눈 검사(scratchpad n3r/sheetA~C): 34298569·34579094·34579093(폴란드 지폐)·4992985(citi·FWD 간판)·7259509(WINNERS 간판)·6780084(얼굴 옆)·28587785(반사 속 포스터, 렌더 1판 눈 검사) 뺌
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'N-3')
STK = os.path.join(VID, 'public', 'bg', 'n3', 'stock')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {}
for s in V['sections']:
    for l in s['lines']: BYTEXT.setdefault(l['text'], l)
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {str(c['id']): c for c in json.load(open(os.path.join(STK, 'credits.json'), encoding='utf-8'))}


def dur(fn):
    r = subprocess.run([FF, '-i', fn], capture_output=True, text=True, encoding='utf-8', errors='ignore').stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r).groups(); return int(h) * 3600 + int(m) * 60 + float(s)


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
    if pad: ls[-1] = dict(ls[-1], pad=pad)
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.~]*', ' '.join(strs)):
        d = d.rstrip('.,~')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·N-3 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': [{k: v for k, v in l.items() if k != 'pad'} for l in ls], 'frames': sum(l['frames'] for l in ls) + pad, '_pad': pad}


NEW = json.loads(open(os.path.join(HERE, 'newline.json'), encoding='utf-8').read())
BYTEXT[NEW['text']] = NEW
F = lambda t: BYTEXT[[k for k in BYTEXT if k.startswith(t)][0]]['frames']
scenes = [
    sc('질문', ['연봉 1천만원 인상', '연봉이 천만원 오르면', '그중 통장에 얼마가'],
       {'tiles': [['연봉 천만원 오르면', '세전 월급 +83만원', '', NEW['frames'], 'ink'], ['칸 = 천만원씩', '3천→4천 · 4천→5천', '', NEW['frames'] + F('연봉이 천만원 오르면'), 'ink']]}),   # 11/15 이해 1차 3/3 '칸'이 뭔지 멈칫
    sc('3천→4천', ['3천에서 4천으로', '69만원 정도가'],
       {'tiles': [['3천 → 4천', '한 달 +69만원', '', F('3천에서 4천으로'), 'ink']]}),
    sc('7천까지', ['그 위로 7천까지'], {'tiles': [['4천→7천 세 칸', '69만원보다 조금 적게', '', 0, 'ink']]}),   # 11/15 이해 1차 3/3 '거의 같음' 숫자 없음 → '62만원 넘게' → 2차 3/3 '69→62는 거의 같다와 안 맞음' → 세 칸끼리 비슷·3천→4천보다 적게(calc_out §C 63.6·62.4·62.6만원)
    sc('7천→8천', ['그런데 7천에서 8천', '55만원 정도만', '오른 돈의 삼분의'],
       {'tiles': [['7천 → 8천', '한 달 +55만원', '', F('그런데 7천에서 8천'), 'ink'], ['세전 +83만원 중', '3분의 2만 남음', '', F('그런데 7천에서 8천') + F('55만원 정도만'), 'ink']]}),
    sc('이유', ['이유는 소득세율', '연봉이 아니라,', '넘는 부분에만', '바로 이 칸에서'],
       {'tiles': [['연봉에서 공제 뺀 돈', '5천만원 넘는 부분', '', F('이유는 소득세율'), 'ink'], ['그 부분 세율', '15% → 24%', '', F('이유는 소득세율') + F('연봉이 아니라,'), 'ink'], ['연봉 7천 → 8천', '이 선을 넘는 칸', '', F('이유는 소득세율') + F('연봉이 아니라,') + F('넘는 부분에만'), 'ink']]}),   # 11/15 이해 1차 3/3 '이것저것'·왜 7~8천인지 멈칫
    sc('그래서', ['그래서 연봉 이야기', '같은 인상이라도'],
       {'tiles': [['오른 연봉은', '통장 금액으로 보기', '', 0, 'ink'], ['같은 천만원 인상', '69만 vs 55만원', '', F('그래서 연봉 이야기'), 'ink']]}, pad=30),   # 11/15 이해 1차 1/3 '10만원 넘게' 대신 두 값
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('691,373', '545,773', '65.5%', '24%', '833,333'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
BG = [('853830', 0), ('3202364', 0), ('5923592', 0), ('7822029', 0), ('6771533', 0), ('853830', 5), ('4992563', 0), ('7535095', 0), ('5923592', 4), ('8783211', 0), ('6771533', 3), ('8783211', 5), ('3202364', 6), ('853830', 11), ('8783211', 10)]   # 11/15 눈 검사 1판: 28587785 유리창 반사 속 글자 포스터(27~31초·45~50초, 출처 줄 옆) → 뺌 · 2판: 7687970 노트북 자판 글자가 안전 영역 관문(28초 왼쪽 아래)에 걸림 → 카드·폰 컷
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(STK, name + '.mp4')
    D = dur(src); assert D - st >= fr / 30 + 0.3, (name, D, st, fr / 30)
    cut = f'bg/n3s_raise/stock/cut/{name}_{st}_{fr}.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[nm]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'n3s_raise', 'v': 1, 'look': 'live', 'question': ['연봉 천만원 오르면', '통장엔 한 달 얼마 남나?'], 'hot': '얼마',
     'answer': {'label': '연봉 천만원 오를 때 통장에 남는 돈', 'items': ['3천 → 4천: 한 달 +69만원', '7천 → 8천: 한 달 +55만원'], 'arrow': False, 'note': '1인 · 식대 비과세 월 20만원 · 2026년 기준'},
     'base': '소득세법 제55조 · 2026년 근로소득 간이세액표·4대 보험료율 · 1인·식대 비과세 월 20만원 · 파이어맵 계산', 'long': None,
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'n3s_raise.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'n3s_raise: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
