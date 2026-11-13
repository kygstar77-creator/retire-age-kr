# h4s_ladder c1clip (firemap-video-producer 2026-11-14 06:5x) — h4s_rank/h4rclip.py 사본, 줄·장면·배경·제목만 바꿈
#   py -3.12 work/research/cardshorts/h4s_ladder/h4lclip.py [big]   → work/video/h4s_ladder.json (big: 윗줄 2배 시험판 h4s_ladder_big.json)
# 재료: spec h4s_specs.md #3 — H-4 say_v2 55~64줄(롱폼 녹음 그대로) + 첫 줄 1줄 새로(Charon 1.1·같은 설정, 받아쓰기 '광명 철산동 84제곱미터…' 일치, f0 134.8Hz)
# 숫자: H-4 calc_out §2(철산동 84㎡대 1년 매매 2025.11~2026.10 계약 가운데 값, 5건 이상): 맨 위 롯데캐슬&SKVIEW(2022) 15.95억·센트럴푸르지오(2021) 15.09억 · 주공13(1986) 13.85억 > 래미안자이(2009) 13.40억 · 맨 아래 리버빌주공(2001) 6.35억
# 주의: 사라·팔라·전망 0 · 단지 값은 실거래 가운데 값(호가 아님)
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
Q1 = '광명 철산동 84㎡, 같은 동 안에서 값 차이는 얼마일까요?'
BYTEXT[Q1] = {'text': Q1, 'audio': 'audio/h4s/79d4240096307278.wav', 'frames': 125}   # 11/14 PD 새로 받음(say '팔십사 제곱미터' — '㎡' 그대로는 받아쓰기 '84M')
BIG = len(sys.argv) > 1 and sys.argv[1] == 'big'
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
    sc('같은 동 값 차이', [Q1, '같은 동, 같은 크기인데 맨 위는', '맨 아래는 6억쯤', '차이가 10억 가까이'],
       {'tiles': [['84㎡ 단지 16곳', '단지마다 1년 거래 가운데 값', '', 0, 'ink'], ['맨 위 롯데캐슬', '15.95억', '', 0, 'ink'], ['맨 아래 리버빌주공', '6.35억', '', 0, 'ink'], ['두 단지 차이', '10억 가까이', '', 0, 'ink']]}),
    sc('새 단지', ['맨 위 두 곳은 2020년대', '둘 다 15억이 넘었'],
       {'tiles': [['롯데캐슬·센트럴푸르지오', '2022·2021년 지음', '', 0, 'ink'], ['둘 다', '15억 넘음', '', 0, 'ink']]}),
    sc('순서 뒤집힘', ['그런데 비싼 순서로', '80년대에 지은 주공13단지가', '래미안자이는 2009년에', '차이는 5천만원 아래'],
       {'tiles': [['비싼 순서', '중간에 뒤집힘', '', 0, 'ink'], ['주공13 1986년', '13.85억', '', 0, 'ink'], ['래미안자이 2009년', '13.40억', '', 0, 'ink'], ['둘 차이', '5천만원 아래', '', 0, 'ink']]}),
    sc('새 집일수록?', ['새 집일수록 비싸다는 말'],
       {'tiles': [['새 집일수록 비싸다?', '철산동에선 꼭 아님', '', 0, 'ink']]}),
]
for s_ in scenes:   # 칸 i = 줄 i 시작 프레임
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert len(st) == len(s_['data']['tiles'])
    for t, f0 in zip(s_['data']['tiles'], st): t[3] = f0
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), [t[0] for s_ in scenes for t in s_['data']['tiles'] if len(t[0]) > 12]
need = ['15.95억', '15.09억', '13.85억', '13.40억', '6.35억', '(2022)', '(2021)', '(1986)', '(2009)']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 H-4 롱폼 Pexels 풀(bg/h4/stock) — 계산기·휴대폰 화면·현수막·외벽 글자·키릴 서류·너무 어두운 클립(6964247·7651886·31907490·28803181·37527858·8478946·9431584) 안 씀(playbook 11/10, 9:16 첫 판 눈 검사 11/13)
BG = [(1, '37500921', 2), (2, '40294066', 2), (3, '7317305', 1), (4, '38259259', 2), (5, '40294066', 12), (6, '37873585', 2),
      (7, '17860854', 5), (8, '7317305', 8), (9, '37873585', 15), (10, '35865018', 2), (11, '37500921', 10)]   # 11/14 눈 검사: 29354411 거리 실사에 얼굴·간판 → 항공 실사
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
p = {'fps': 30, 'name': 'h4s_ladder', 'v': 1, 'look': 'live', 'question': ['광명 철산동 84㎡', '같은 동네 값 차이는?'], 'hot': '값 차이',
     'answer': {'label': '철산동 84㎡대 1년 실거래 가운데 값', 'items': ['맨 위 15.95억', '맨 아래 6.35억'], 'arrow': False, 'note': '2025.11~2026.10 계약'},
     'base': '국토교통부 아파트 매매 실거래가(철산동 84㎡대, 계약 2025.11~2026.10, 5건 이상 단지) · 파이어맵 계산', 'long': 'MRQqitzEgDw',
     'scenes': scenes, 'bg': bg, 'credits': credits}
if BIG:   # 11/14 윗줄 2배 시험(thumb-gap-1114 1위): 지금 판 제목 글자 75px → 150px, 줄을 짧게(한 줄 4~5자)
    p.update(name='h4s_ladder_big', question=['철산동 84㎡', '값 차이는?'], titleMax=150)
json.dump(p, open(os.path.join(VID, p['name'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f"{p['name']}: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s['frames'] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b['frames'] for b in bg) / 30:.1f}초)")
print('credits:', credits)
