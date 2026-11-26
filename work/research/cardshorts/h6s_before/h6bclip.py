# h6s_before c1clip (firemap-video-producer 2026-11-26 11:0x) — k1s_recover/k1rclip.py 사본, 줄·장면·배경만 바꿈 (비축, 부동산 축)
#   py -3.12 work/research/cardshorts/h6s_before/h6bclip.py   → work/video/h6s_before.json
# 재료: H-6 롱폼(YE6FXSezHXc, 11/26 11:30 공개) 0:1·0:2 + 2:17~2:19·2:22 그대로 + 첫 줄 1줄만 새로(newline.json — 롱폼 0:0이 39자라 꼴 관문 35자 넘음, H-6 tts.json Charon 1.1, f0 129.7Hz = 롱폼 0:0 129.0Hz +0.5%) · 첫 줄 인사 없음(C-37로 이미 빠짐)
# 숫자: H-6 calc2_out_1125.txt(84㎡ 42.80억 → 34.50억, 인가 전 반년) · research.md · script.md
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-6')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
NEW = json.load(open(os.path.join(HERE, 'newline.json'), encoding='utf-8'))
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out_1125.txt', 'calc2_out_1125.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
SRC += json.dumps(json.load(open(os.path.join(VID, 'h6.json'), encoding='utf-8'))['scenes'], ensure_ascii=False)
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
    sc('1년 사이', ['NEW', '거래를 값 순서로', '8억 3천만원이 빠진'],
       {'tiles': [['은마 34평 · 84㎡', '1년 사이 8억 3천만원↓', '', 0, 'ink'], ['25년 말 → 요즘', '42.8억 → 34.5억', '', 0, 'ink'], ['내린 값', '8억 3천만원', '', 0, 'ink']]}),
    sc('인가 전에 이미', ['인가가 난 건 여름인데', '34평은 인가 전 반년', '하락의 절반쯤은', '그러니 인가가 나서'],
       {'tiles': [['재건축 사업시행인가', '2026년 7월', '', 0, 'ink'], ['26년 1~6월 계약', '25년 말보다 4억 가까이↓', '', 0, 'ink'], ['하락의', '절반쯤은 인가 전', '', 0, 'ink'], ['인가 탓이라고', '말하기 어렵다', '', 0, 'ink']]}),
]
# 칸 = 그 칸의 말 줄이 시작한 뒤 숫자가 나오는 자리(줄 길이 비율) — 칸 i ↔ 장면 안 i번째 줄
AT = [[0.05, 0.45, 0.1], [0.1, 0.5, 0.2, 0.2]]
for s_, at_ in zip(scenes, AT):
    off = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    for i, (t, f) in enumerate(zip(s_['data']['tiles'], at_)): t[3] = off[i] + int(s_['lines'][i]['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('42.80억', '34.50억', '38.83억'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: H-6 롱폼 Pexels 실사만(11/26 PD 눈 확인 scratchpad f_*.jpg — 아파트 외관·눈 길, 얼굴·글자 0)
BG = [(1, 'h4/stock/37873585', 2), (2, 'h4/stock/38259259', 2), (3, 'h4/stock/38259259', 12), (4, 'h4/stock/37873585', 12), (5, 'h4/stock/37873585', 16),
      (6, 'h5/stock/15082793', 3), (7, 'h4/stock/38259259', 20)]
DUR = {'h4/stock/37873585': 32.9, 'h4/stock/38259259': 40.5, 'h5/stock/15082793': 30.0}
LIC = {}
def _w(x):
    if isinstance(x, dict):
        if 'src' in x and 'license' in x: LIC[x['src'].split('/')[-1][:-4]] = x['license']
        [_w(v) for v in x.values()]
    elif isinstance(x, list): [_w(v) for v in x]
for j in ('h6.json',):
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
    cut = f'bg/h6/cut/{cid}_{st}_r{fr}.mp4'; cp = os.path.join(VID, 'public', cut)   # B프레임 없이 -g 10으로 잘라 'No frame found' 피함
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-r', '30', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({re.search(r'[(](.*)[)]', LIC[c.split('/')[-1]]).group(1).strip() for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'h6s_before', 'v': 1, 'look': 'live', 'question': ['은마 34평', '1년 사이 얼마나?'], 'hot': '얼마나',
     'answer': {'label': '은마 84㎡ 실거래 가운데 값 · 2025년 10~12월 계약 3건 → 2026년 10~11월 계약 10건', 'items': ['−8억 3천만원', '절반쯤은 재건축 인가 전'], 'arrow': False},
     'base': '국토교통부 아파트 매매 실거래(대치동 은마, 2025.10~2026.11 계약, 해제 제외, 2026-11-25 받음) · 가운데 값 · 파이어맵 계산', 'long': 'YE6FXSezHXc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h6s_before.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h6s_before: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
