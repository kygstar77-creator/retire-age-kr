# jt1s_even — JT-1 롱폼 3장 '기다렸다 들면 몇 살에 같아지나'(5억 65세 vs 70세 → 93세) 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-18 22시, n3s_family/n3fclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/jt1s_even/jt1eclip.py   → work/video/jt1s_even.json
# 목소리 = JT-1 voice.json 3장 4·5·6·7·8·10·11·14·28·29줄 wav 그대로 + 첫 줄 하나만 새로 받음(newline.py, Charon 1.1 = JT-1 tts.json) — f0 139.5Hz(편 중앙 127.7Hz +9%)·whisper small 일치
# 숫자 원문 = JT-1 calc_out.txt §1(5억 65세 1,264천 vs 70세 1,539천 · 못 받은 돈 7,584만원 · +275천 → 23.0년 → 93.0세) §7(80세 차 4,284만원) — 말은 롱폼 편집 통과 어림(7,600·28만·4,300)
# 배경 = JT-1 stock(Pexels, ep/JT-1/stock_pd1116.json — 11/16 PD 눈 확인 통과 컷만, 6541138은 표지 글자 있는 앞 4초 안 씀)
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'JT-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {}
for s in V['sections']:
    for l in s['lines']: BYTEXT.setdefault(l['text'], l)
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock_pd1116.json'), encoding='utf-8'))}


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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·JT-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': [{k: v for k, v in l.items() if k != 'pad'} for l in ls], 'frames': sum(l['frames'] for l in ls) + pad, '_pad': pad}


NEW = json.loads(open(os.path.join(HERE, 'newline.json'), encoding='utf-8').read())
BYTEXT[NEW['text']] = NEW
F = lambda t: BYTEXT[[k for k in BYTEXT if k.startswith(t)][0]]['frames']
scenes = [
    sc('질문', ['주택연금, 지금 바로', '그동안 못 받은 돈을'],
       {'tiles': [['5억 집 · 65세', '지금 들까, 70세에 들까', '', 0, 'ink'], ['못 받는 5년치', '매달 126만원 × 5년', '', NEW['frames'], 'ink']]}),
    sc('더 받음', ['대신 70세에 들면', '그럼 못 받은 7,600만원을'],
       {'tiles': [['70세에 들면', '매달 154만원 · 28만원 더', '', 0, 'ink'], ['메우는 데 몇 년?', '못 받은 7,600만원', '', F('대신 70세에 들면'), 'ink']]}),
    sc('답', ['23년이 걸립니다', '그러면 93세가 됩니다'],
       {'tiles': [['23년 걸림', '매달 28만원씩 메우면', '', 0, 'ink'], ['93세', '받은 돈 합이 같아짐', '', F('23년이 걸립니다'), 'ink']]}),
    sc('80세', ['80세가 됐을 때를', '일찍 든 쪽이 기다린'],
       {'tiles': [['80세까지 받은 돈', '일찍 든 쪽 4,300만원 더', '', 0, 'ink']]}),
    sc('갈림', ['그러니 93세보다 오래'],
       {'tiles': [['93세보다 오래 살면', '기다린 쪽이 더 받음', '', 0, 'ink']]}),
    sc('가정', ['기다리는 동안 집값이 그대로', '매달 받는 돈은 가입할 때', '거꾸로 집값이 오르면'],
       {'tiles': [['집값 그대로 가정', '가입 때 집값으로 다시 정함', '', 0, 'ink'], ['집값이 오르면', '늦게 든 쪽이 더 받을 수도', '', F('기다리는 동안 집값이 그대로') + F('매달 받는 돈은 가입할 때'), 'ink']]}, pad=30),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('7,584만원', '+275천', '93.0세', '4,284'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# (컷 번호, 시작 초) — 줄마다 한 컷, 같은 컷을 다시 쓰면 다른 구간
BG = [('8292929', 3), ('6541138', 5), ('7578842', 0), ('946148', 0), ('38781079', 0), ('38781079', 3),
      ('6781559', 0), ('6541138', 12), ('946148', 8), ('8292929', 0), ('38405960', 0), ('946148', 15)]
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'jt1', 'stock', 'jt1_' + name + '.mp4')
    D = dur(src); assert D - st >= fr / 30 + 0.3, (name, D, st, fr / 30)
    cut = f'bg/jt1s_even/stock/cut/{name}_{st}_{fr}.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[nm]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'jt1s_even', 'v': 1, 'look': 'live', 'question': ['주택연금 기다렸다 들면?', '받은 돈 합 93세에 같아짐'], 'hot': '93세',
     'answer': {'label': '5억 집, 65세에 바로 vs 70세에 들면', 'items': ['70세: 매달 28만원 더', '못 받은 7,600만원 메우는 데 23년 → 93세'], 'arrow': False, 'note': '집값 그대로 가정 · 정액형 · 2026년 3월 1일 이후 신청 기준'},
     'base': '한국주택금융공사 주택연금 월지급금 표(2026.3.1) · 파이어맵 계산', 'long': None,
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'jt1s_even.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'jt1s_even: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
