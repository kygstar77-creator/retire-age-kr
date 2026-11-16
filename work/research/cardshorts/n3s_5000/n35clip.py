# n3s_5000 — N-3 롱폼 첫머리 '연봉 5천, 통장엔 한 달 357만원쯤 · 직장인 백 명 중 앞에서 33명 안' + 총급여로 내 자리 찾기 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-17 07시, n3s_family/n3fclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/n3s_5000/n35clip.py   → work/video/n3s_5000.json
# 목소리 = N-3 voice.json 0장 2~6줄 + 1장 17~18줄 wav 그대로(새 녹음 0, Charon 1.1)
# 숫자 원문 = N-3 calc_out.txt(연봉 5,000만 통장 월 3,571,586 · 총급여 4,760만 → 상위 32~33% 구간 사이)
# 배경 = n3s_raise·n3s_family 눈 검사 통과 컷만
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


F = lambda t: BYTEXT[[k for k in BYTEXT if k.startswith(t)][0]]['frames']
scenes = [
    sc('질문', ['연봉 5천이면, 통장에는', '답은 357만원쯤'],
       {'tiles': [['연봉 5천', '통장엔 한 달 얼마?', '', 0, 'ink'], ['부양가족 0명 기준', '한 달 357만원쯤', '', F('연봉 5천이면, 통장에는'), 'ink']]}),
    sc('줄', ['그럼 우리나라 직장인 백 명', '앞에서 서른세 명', '상위 33% 안쪽'],
       {'tiles': [['직장인 백 명 줄', '연봉 5천은 몇 번째?', '', 0, 'ink'], ['직장인 백 명 중', '앞에서 33명 안', '', F('그럼 우리나라 직장인 백 명'), 'ink'], ['같은 말로', '상위 33% 안쪽', '', F('그럼 우리나라 직장인 백 명') + F('앞에서 서른세 명'), 'ink']]}),
    sc('식대', ['식대를 한 달 20만원', '한 해에 240만원이', '그래서 연봉 5천은 국세청'],
       {'tiles': [['비과세 식대 월 20만', '한 해 240만원 빠짐', '', 0, 'ink'], ['33%는 이걸로 잰 값', '총급여 4,760만원', '', F('식대를 한 달 20만원') + F('한 해에 240만원이'), 'ink']]}),
    sc('총급여', ['내 자리를 찾을 때는', '계약서 숫자로 찾으면'],
       {'tiles': [['내 자리 찾을 때', '원천징수영수증 총급여', '', 0, 'ink'], ['계약서 연봉으로 보면', '실제보다 앞에 선 듯', '', F('내 자리를 찾을 때는'), 'ink']]}, pad=30),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('3,571,586', '4,760만', '상위 33%'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
BG = [('7822029', 0), ('853830', 0), ('5923592', 0), ('6771533', 0), ('3202364', 0), ('7535095', 0), ('853830', 5), ('5923592', 5), ('4992563', 0), ('8783211', 0)]   # n3s_raise·n3s_family 눈 검사 통과 컷만 · 11/17 이해 1차 뒤 식대 3줄 더해 10컷
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(STK, name + '.mp4')
    D = dur(src); assert D - st >= fr / 30 + 0.3, (name, D, st, fr / 30)
    cut = f'bg/n3s_5000/stock/cut/{name}_{st}_{fr}.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[nm]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'n3s_5000', 'v': 1, 'look': 'live', 'question': ['연봉 5천 실수령액', '통장엔 한 달 357만원'], 'hot': '357만원',
     'answer': {'label': '연봉 5천, 세금·보험료 다 뗀 통장', 'items': ['한 달 357만원쯤', '직장인 백 명 중 앞에서 33명 안'], 'arrow': False, 'note': '부양가족 0명 · 식대 비과세 월 20만원 · 2026년 기준'},
     'base': '2026년 근로소득 간이세액표·4대 보험료율 · 국세청 근로소득 백분위(2024년 귀속) · 파이어맵 계산', 'long': None,
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'n3s_5000.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'n3s_5000: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
