# h4s_new15 c1clip (firemap-video-producer 2026-11-15 18:2x) — h4s_ladder/h4lclip.py 사본, 줄·장면·배경·제목만 바꿈
#   py -3.12 work/research/cardshorts/h4s_new15/h4nclip.py  → work/video/h4s_new15.json
# 재료: spec h4s_specs.md #2 — H-4 voice 3장 2~6·8~11줄(롱폼 녹음 그대로) + 첫 줄 1줄 새로(Charon 1.1·같은 설정, take a2 f0 134.1Hz vs 쓴 줄 중앙 139.2Hz −3.6%, whisper turbo '광명아파트 15억, 이 말은 어디서 나왔을까요?' 일치)
# 숫자: H-4 calc_out §1(2026.07~09 계약 84㎡대 가운데 값): 광명 2019년 이후 지은 단지 24건 14.71억 > 영등포구 14.30억(11위) < 강동구 15.00억 → 서울 25개 구 중 15곳보다 위 · 광명 전체 9.70억
# 주의: 사라·팔라·전망 0 · 실거래 가운데 값(호가 아님) · 3장 7줄(관악구 5억쯤)은 숫자 덩어리라 뺌
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-4')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
Q1 = '광명 아파트 15억, 이 말은 어디서 나왔을까요?'
Q2 = '이 값을 서울 스물다섯 개 구 사이에 놓으면, 열다섯 곳보다 비싸요.'
BYTEXT[Q2] = {'text': Q2, 'audio': 'audio/h4s/a3318db31d18eddb.wav', 'frames': 117}   # 11/15 PD 2차 3/3 '서울 줄에 끼우면'·'서울보다 비싸다는 말' 갑작스러움 → 롱폼 3장 5·6줄 대신 새로 받음(take d2 f0 127.0Hz −9%, whisper '이 값을 서울 25개 구사이에 놓으면 15곳보다 비싸요.')
BYTEXT[Q1] = {'text': Q1, 'audio': 'audio/h4s/ea7ab94e25318701.wav', 'frames': 96}   # 11/15 PD 새로 받음(take a2, newline.py)
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-4 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('15억의 출처', [Q1, '광명에서 2019년 뒤에 지은', '가운데 값이 15억 가까이'],   # 11/19 v2(benchmark 11/19 답 5초·A98): '2019년 뒤라는 건 … 새로 지은 단지라는 뜻'(5.2초, 앞 줄 되풀이) 뺌 — 출처 답 3.2초·15억 줄 11.2→6.0초, 새 녹음 0
       {'tiles': [['흔히 듣는 말', '"광명 15억"', '', 0, 'ink'], ['새 단지만', '2019년 이후 지음', '', 0, 'ink'], ['새 단지 24건 가운데', '14.71억, 15억 가까이', '', 0, 'ink']]}),
    sc('서울 줄에 끼우면', [Q2],
       {'tiles': [['서울 25개 구 사이', '15곳보다 비쌈', '', 0, 'ink']]}),
    sc('착각', ['그래서 새 단지 값만'],
       {'tiles': [['광명 전체 가운데 값', '9.70억', '', 0, 'ink']]}),   # 1차 3/3 '자료가 말해 주는 건 하나뿐' 보고서 말투 → 3장 8줄 뺌
    sc('이렇게 보기', ["그러니 시세를 볼 땐", '국토교통부 실거래가 공개'],
       {'tiles': [['시세 볼 때', '같은 동·같은 크기', '', 0, 'ink'], ['국토부 실거래가', '1년 가운데 값', '', 0, 'ink']]}),
]
for s_ in scenes:   # 칸 i = 줄 i 시작 프레임
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert len(st) == len(s_['data']['tiles'])
    for t, f0 in zip(s_['data']['tiles'], st): t[3] = f0
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), [t[0] for s_ in scenes for t in s_['data']['tiles'] if len(t[0]) > 12]
need = ['14.71억', '14.30억', '15.00억', '9.70억', '24건']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: H-4 롱폼 Pexels 풀(bg/h4/stock) 중 앞 클립에서 눈 검사 통과한 7개만 — 안 쓰는 것 6964247·7651886·31907490·28803181·37527858·8478946·9431584·29354411(얼굴·간판)
BG = [(1, '17860854', 2), (2, '37500921', 2), (3, '35865018', 10), (4, '37873585', 2), (5, '35865018', 2),
      (6, '38259259', 20), (7, '37500921', 10)]   # 11/19 v2: 뺀 줄 몫 38259259_2 컷 뺌, 번호 당김   # 11/15 눈 검사: 40294066 아파트 외벽 상표 글자(브랜드 로고) → 4·8줄 바꿈   # 11/15 safezone 23~24초: 17860854 12초~ 간판·전화번호 현수막 → 항공 실사
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
p = {'fps': 30, 'name': 'h4s_new15', 'v': 2, 'look': 'live', 'question': ['광명 아파트 15억', '어디서 나온 말?'], 'hot': '15억',
     'answer': {'label': '광명 2019년 이후 지은 단지 84㎡대 실거래 가운데 값', 'items': ['14.71억(24건)', '광명 전체 9.70억'], 'arrow': False, 'note': '2026.07~09 계약'},
     'base': '국토교통부 아파트 매매 실거래가(84㎡대, 계약 2026.07~09) · 파이어맵 계산', 'long': 'MRQqitzEgDw',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, p['name'] + '_v2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f"{p['name']}: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s['frames'] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b['frames'] for b in bg) / 30:.1f}초)")
print('credits:', credits)
