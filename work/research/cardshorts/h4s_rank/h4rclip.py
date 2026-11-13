# h4s_rank c1clip (firemap-video-producer 2026-11-13 14:5x) — h3s_number/h3nclip.py 사본, 줄·장면·배경만 바꿈
#   py -3.12 work/research/cardshorts/h4s_rank/h4rclip.py   → work/video/h4s_rank.json
# 재료: h4s_rank/understand.md 2차 판(say 2·4·11·13·15~21, 49.6초) · 목소리 = H-4 voice.json 문장 wav 그대로(새 녹음 0), 브랜드 첫·끝 줄 뺌
# 숫자: H-4 calc_out(2026-10-16 받음, 7~9월 계약 84㎡대 가운데 값: 성북 10.00억·광명 9.70억(171건)·관악 9.44억(140건)·구로 8.26억·금천 7.10억, 낮은 서울 구 8개)
# 주의: 사라·팔라·전망 0 · 11/12 다시 받은 값(9.78억·177건)은 설명란에 기준일과 함께
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-4')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
# 11/13 15시 PD: 꼴 ⓐ 첫 줄 35자 이하 — 롱폼 첫 줄(39자) 대신 같은 목소리·빠르기(Charon 1.1)로 한 줄만 새로 받음(f0 135.2Hz vs 롱폼 첫 줄 134.8Hz, aitell 0.0)
BYTEXT['광명 84㎡, 서울 스물다섯 개 구 사이 몇 번째일까요?'] = {'text': '광명 84㎡, 서울 스물다섯 개 구 사이 몇 번째일까요?', 'audio': 'audio/h4s/8539189016d103ea.wav', 'frames': 117}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {}
for _d in ('stock',):
    for c in json.load(open(os.path.join(VID, 'public', 'bg', 'h4', _d, 'credits.json'), encoding='utf-8')):
        CRED.setdefault(str(c['id']), dict(c, dir=_d))
TAIL = 36
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def sc(label, lines, data):
    ls = [L(t) for t in lines]
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-3 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('몇 번째', ['광명 84㎡, 서울', '답부터 말하면, 광명까지 넣은'],
       {'tiles': [['84㎡대', '전용 80~85㎡', '', 0, 'ink'], ['26곳 중', '위에서 18번째', '', 0, 'ink']]}),
    sc('가운데 값', ['값은 가운데 값으로 봤습니다', '바로 위가 성북구'],
       {'tiles': [['광명 가운데 값', '9.70억', '', 0, 'ink'], ['위 성북 · 아래 관악', '10.00억 · 9.44억', '', 0, 'ink']]}),
    sc('광명보다 낮은 서울 구', ['광명보다 낮은 서울 구는', '관악, 은평, 구로'],
       {'tiles': [['광명보다 낮은 구', '8곳', '', 0, 'ink'], ['관악·은평·구로·노원', '강북·중랑·금천·도봉', '', 0, 'ink']]}),
    sc('붙어 있는 구', ['이 가운데 구로구와 금천구는', '구로구는 8억대', '광명이 구로구보다 1억'],
       {'tiles': [['광명과 붙은 구', '구로 · 금천', '', 0, 'ink'], ['구로 · 금천', '8.26억 · 7.10억', '', 0, 'ink'], ['광명 9.70억', '구로보다 1억 넘게', '', 0, 'ink']]}),
    sc('거래 수', ['거래 수도 적지 않았어요', '관악구 140건보다'],
       {'tiles': [['석 달 거래', '광명 171건', '', 0, 'ink'], ['관악 140건보다', '광명이 많아요', '', 0, 'ink']]}),
]
for s_ in scenes:   # 칸 i = 줄 i 시작 프레임
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert len(st) == len(s_['data']['tiles'])
    for t, f0 in zip(s_['data']['tiles'], st): t[3] = f0
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), [t[0] for s_ in scenes for t in s_['data']['tiles'] if len(t[0]) > 12]
need = ['9.70억 (171건)', '10.00억', '9.44억 (140건)', '8.26억', '7.10억']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 H-4 롱폼 Pexels 풀(bg/h4/stock) — 계산기·휴대폰 화면·현수막·외벽 글자·키릴 서류·너무 어두운 클립(6964247·7651886·31907490·28803181·37527858·8478946·9431584) 안 씀(playbook 11/10, 9:16 첫 판 눈 검사 11/13)
BG = [(1, '37873585', 2), (2, '38259259', 2), (3, '40294066', 12), (4, '37500921', 2), (5, '40294066', 2), (6, '35865018', 2), (7, '37500921', 10),
      (8, '7317305', 1), (9, '38259259', 20), (10, '7205591', 0), (11, '7263304', 2)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    src = os.path.join(VID, 'public', 'bg', 'h4', CRED[cid]['dir'], f'{cid}.mp4')
    assert os.path.exists(src), src
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    cut = f'bg/h4/cut/{cid}_{st}_r{fr}.mp4'; cp = os.path.join(VID, 'public', cut)   # 11/13 2차: 37527858은 -r 30 뒤에도 No frame found → 38259254로 바꿈 · 1차: _n 판(원본 fps 그대로) 37527858 'No frame found' → -r 30 다시 인코딩(_r) · 길이를 이름에 — 옛 클립 cut(다른 길이)과 섞이지 않게
    if not os.path.exists(cp):   # k1s_fix 법: B프레임 없이 -g 10으로 잘라 'No frame found' 피함
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-r', '30', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c].get('author', '').strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'h4s_rank', 'v': 1, 'look': 'live', 'question': ['광명 84㎡ 실거래', '서울 25개 구 사이 몇 번째?'], 'hot': '몇 번째',
     'answer': {'label': '광명 84㎡대 가운데 값', 'items': ['26곳 중 위에서 18번째', '9.70억 · 낮은 서울 구 8곳'], 'arrow': False, 'note': '2026년 7~9월 계약 실거래'},
     'base': '국토교통부 아파트 매매 실거래가(계약 2026.07~09, 2026-10-16 받음) · 파이어맵 계산', 'long': 'MRQqitzEgDw',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h4s_rank.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h4s_rank: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
