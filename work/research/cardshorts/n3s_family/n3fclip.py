# n3s_family — N-3 롱폼 6장 '같은 연봉, 다른 통장'(가족 수 → 월 16만원) 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-16 06시, n3s_raise/n3rclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/n3s_family/n3rclip.py   → work/video/n3s_family.json
# 목소리 = N-3 voice.json 6장 7~11줄 wav 그대로 + 첫 줄 하나만 새로 받음(newline.py, Charon 1.1 = N-3 tts.json) — f0 134.8Hz(-4%)·whisper small 받아쓰기 일치
# 숫자 원문 = N-3 calc_out.txt §B(5,000만 1인 3,571,586 vs 4인·자녀2 3,734,606 = 163,020 · 1억 295,530)
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
    sc('질문', ['연봉이 똑같이 5천인데', '배우자와, 여덟 살부터'],
       {'tiles': [['같은 연봉 5천', '통장은 다를 수 있음', '', 0, 'ink'], ['네 식구라면', '나·배우자·자녀 2', '', NEW['frames'], 'ink']]}),
    sc('5천', ['연봉 5천이면, 혼자일'],
       {'tiles': [['연봉 5천 · 네 식구', '부양가족 0명보다 +16만원', '', 0, 'ink']]}),
    sc('1억', ['연봉 1억이면 그보다'],
       {'tiles': [['연봉 1억 · 네 식구', '부양가족 0명보다 +30만원쯤', '', 0, 'ink']]}),
    sc('이유', ['달마다 떼는 소득세가 가족'],
       {'tiles': [['나라가 정한 세금표', '가족 수마다 칸이 따로', '', 0, 'ink']]}),
    sc('신고', ['회사에 부양가족 신고가'],
       {'tiles': [['신고 안 돼 있으면', '연말에 한꺼번에 돌려받음', '', 0, 'ink']]}, pad=30),   # 11/16 이해 2차 2/3 '혼자'가 누구 → '부양가족 0명보다' · 1차 3/3 '4인' 누구·'칸' 뭔지·2/3 '결국 같은 돈?' → 화면만 고침(새 녹음 0)
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('163,020', '295,530', '3,571,586', '3,734,606'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
BG = [('853830', 0), ('5923592', 0), ('7822029', 0), ('6771533', 0), ('4992563', 0), ('8783211', 0)]   # n3s_raise 11/15 눈 검사 통과 컷만
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(STK, name + '.mp4')
    D = dur(src); assert D - st >= fr / 30 + 0.3, (name, D, st, fr / 30)
    cut = f'bg/n3s_family/stock/cut/{name}_{st}_{fr}.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[nm]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'n3s_family', 'v': 1, 'look': 'live', 'question': ['같은 연봉 5천', '통장 한 달 16만원 차이?'], 'hot': '16만원',
     'answer': {'label': '같은 연봉, 가족 수에 따라 통장에 더 들어오는 돈', 'items': ['연봉 5천: 한 달 +16만원', '연봉 1억: 한 달 +30만원쯤'], 'arrow': False, 'note': '배우자·자녀 2(8~20세) vs 혼자 · 식대 비과세 월 20만원 · 2026년 기준'},
     'base': '2026년 근로소득 간이세액표·4대 보험료율 · 식대 비과세 월 20만원 · 파이어맵 계산', 'long': None,
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'n3s_family.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'n3s_family: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
