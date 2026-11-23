# k1s_recover c1clip (firemap-video-producer 2026-11-23 22:4x) — h5s_jeonse/h5jclip.py 사본, 줄·장면·배경만 바꿈 (비축, 지수 축)
#   py -3.12 work/research/cardshorts/k1s_recover/k1rclip.py   → work/video/k1s_recover.json
# 재료: KOSPI-1 롱폼(khvIhE8Sf-s, 11/24 11:30 공개) 4장 '전날 값을 되찾기까지' — voice.json 4:2~4:9 그대로, 첫 줄 1줄만 새로(newline.json, KOSPI-1 tts.json Charon 1.1 — f0 122.4Hz = 편 중앙 129.4Hz -5%), 브랜드 첫·끝 줄 없음
# 숫자: KOSPI-1 calc2_out_1123.txt(11/23 ECOS 다시 셈) — 무리 첫날 16 · 되찾기 중앙 8.0 최장 1367 · 2000-01-05 1367 · 2008-09-16 5거래일·1년 최저 -32.4% · 1999-06-09·2026-02-02 1거래일
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'KOSPI-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc2_out_1123.txt', 'calc_drop_out_1123.txt', 'facts.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
NEW = json.load(open(os.path.join(HERE, 'newline.json'), encoding='utf-8'))
SRC += json.dumps(json.load(open(os.path.join(VID, 'kospi1.json'), encoding='utf-8'))['scenes'], ensure_ascii=False)
TAIL = 36
n = 0


def L(t):
    global n
    if t == 'NEW':
        n += 1; return {'n': n, 'text': NEW['text'], 'audio': NEW['audio'], 'frames': NEW['frames']}
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·KOSPI-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('되찾기란', ['NEW'],
       {'tiles': [['되찾기란', '빠지기 전날 종가 다시 넘기', '', 0, 'ink']]}),
    sc('며칠 걸렸나', ['중간은 8거래일', '짧게는 하루 만에'],
       {'tiles': [['보통 · 가운데 값', '8거래일', '', 0, 'ink'], ['가장 짧게', '1거래일', '', 0, 'ink']]}),
    sc('가장 길게', ['그런데 가장 길었던 건', '날짜로 치면 5년 반', '닷컴 거품 때 빠지기 전'],
       {'tiles': [['가장 길게', '1,367거래일', '', 0, 'ink'], ['날짜로', '5년 반', '', 0, 'ink'], ['2000년 1월부터', '2005년 7월', '', 0, 'ink']]}),
    sc('빨리 되찾아도', ['반대로 금융위기 때는', '그런데 그 뒤 1년 안에', '빨리 되찾았다고 해서'],
       {'tiles': [['2008년 9월', '5거래일(일주일)', '', 0, 'ink'], ['빠진 날 종가 대비', '1년 안 -32.4%', '', 0, 'ink']]}),
]
# 칸 = 그 칸의 말 줄이 시작한 뒤 숫자가 나오는 자리(줄 길이 비율) — 칸 i ↔ 장면 안 i번째 줄
AT = [[0.05], [0.35, 0.45], [0.55, 0.3, 0.6], [0.45, 0.4]]
for s_, at_ in zip(scenes, AT):
    off = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    for i, (t, f) in enumerate(zip(s_['data']['tiles'], at_)): t[3] = off[i] + int(s_['lines'][i]['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('무리(60거래일 안 묶음) 첫날 수 16', '전날 값 되찾기 거래일 중앙 8.0 최장 1367', '20000105 -6.87%', '전날 값 되찾기 1367거래일', '20080916 -6.10%', '그 뒤 1년 최저 -32.4%', '19990609 -5.87%', '2005-07-14'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: KOSPI-1 롱폼 Pexels 실사만(11/23 PD 눈 확인 scratchpad k1bg_sheet.jpg — 38557069 'BTCUSDT'·7578632 '$' 글자 화면은 뺌, 얼굴 0)
BG = [(1, 'kospi1/stock/6186015', 5), (2, 'kospi1/stock/3945008', 2), (3, 'kospi1/stock/6186015', 1), (4, 'kospi1/stock/5224014', 1),
      (5, 'kospi1/stock/5224014', 8), (6, 'kospi1/stock/8495394', 1), (7, 'kospi1/stock/3945008', 14), (8, 'kospi1/stock/5224014', 13), (9, 'kospi1/stock/3945008', 24)]
DUR = {'kospi1/stock/39494572': 24.0, 'kospi1/stock/3945008': 30.0, 'kospi1/stock/6186015': 15.0, 'kospi1/stock/5224014': 18.7, 'kospi1/stock/8495394': 22.7}
LIC = {}
def _w(x):
    if isinstance(x, dict):
        if 'src' in x and 'license' in x: LIC[x['src'].split('/')[-1][:-4]] = x['license']
        [_w(v) for v in x.values()]
    elif isinstance(x, list): [_w(v) for v in x]
for j in ('kospi1.json',):
    _w(json.load(open(os.path.join(VID, j), encoding='utf-8')))
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cp_, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    cid = cp_.split('/')[-1]
    src = os.path.join(VID, 'public', 'bg', cp_ + '.mp4')
    assert os.path.exists(src), cp_
    assert DUR[cp_] - st >= fr / 30 + 0.3, (cp_, DUR[cp_], fr / 30)
    cut = f'bg/kospi1/cut/{cid}_{st}_r{fr}.mp4'; cp = os.path.join(VID, 'public', cut)   # B프레임 없이 -g 10으로 잘라 'No frame found' 피함
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-r', '30', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({re.search(r'[(](.*)[)]', LIC[c.split('/')[-1]]).group(1).strip() for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'k1s_recover', 'v': 1, 'look': 'live', 'question': ['코스피 하루 -5% 뒤', '전날 값 되찾기 며칠?'], 'hot': '며칠',
     'answer': {'label': '1995~2026 하루 5% 넘게 빠진 날 16번(석 달 안쪽으로 이어진 날은 한 번으로)', 'items': ['가운데 8거래일', '가장 길게 1,367거래일'], 'arrow': False, 'note': '2008년 9월: 5거래일 만에 되찾고도 1년 안 빠진 날보다 -32.4%'},
     'base': '한국은행 ECOS 코스피 일별 종가(원자료 한국거래소, 1995-01-03~2026-11-20, 2026-11-23 내려받음) · 되찾기 = 빠지기 전날 종가를 다시 넘은 첫 거래일 · 파이어맵 계산', 'long': 'khvIhE8Sf-s',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'k1s_recover.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'k1s_recover: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
