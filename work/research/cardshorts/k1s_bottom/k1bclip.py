# k1s_bottom c1clip (firemap-video-producer 2026-11-24 14:5x) — k1s_recover/k1rclip.py 사본, 줄·장면·배경만 바꿈 (비축, 지수 축)
#   py -3.12 work/research/cardshorts/k1s_bottom/k1bclip.py   → work/video/k1s_bottom.json
# 재료: KOSPI-1 롱폼(bBoh8J1Ru_4, 11/24 11:30 공개) 3장 '첫날이 바닥이었나' — voice.json 3:13~3:21·3:26 그대로, 첫 줄 1줄만 새로(newline.json — 3:12 질문 40자를 33자로 바꿔 답 3.6초에), 브랜드 첫·끝 줄 없음
# 숫자: KOSPI-1 calc4_out_1123(무리 15·더 내려간 14·중앙 -11.8)·calc2_out_1123(1년 뒤 15·오른 10·중앙 19.1, 19971024 1년 최저 -51.0%, 20200319 +0.0%)
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
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc2_out_1123.txt', 'calc4_out_1123.txt', 'calc_drop_out_1123.txt', 'facts.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
NEW = json.load(open(os.path.join(HERE, 'newline.json'), encoding='utf-8'))   # 첫 줄 1줄만 새로(꼴 관문 35자 — 3:12는 40자)
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
    sc('첫날이 바닥?', ['NEW'],
       {'tiles': [['-5% 빠진 첫날 종가', '1년 안 더 내려갔나?', '', 0, 'ink']]}),
    sc('더 내려갔다', ['열다섯 번 중 열네 번', '더 내려간 폭을 크기대로'],
       {'tiles': [['1년 지난 15번 중', '14번 더 내려감', '', 0, 'ink'], ['첫날 종가보다 더', '가운데 12% 정도', '', 0, 'ink']]}),
    sc('가장 깊게·한 번', ['외환위기 때는 1년 안에', '안 내려간 한 번은', '그러니까 첫날이 가장'],
       {'tiles': [['1997년 외환위기', '첫날 종가보다 -51.0%', '', 0, 'ink'], ['안 내려간 1번', '2020년 3월 코로나', '', 0, 'ink'], ['첫날이 바닥이었던 적', '거의 없음', '', 0, 'ink']]}),
    sc('1년 뒤엔', ['그럼 1년이 지난 뒤엔', '열다섯 번 중 열 번은', '오른 폭도 줄 세우면', '나머지 다섯 번은', '더 내려갔다가 1년 뒤엔'],
       {'tiles': [['1년 뒤 첫날 종가보다', '15번 중 10번 높음', '', 0, 'ink'], ['오른 10번 가운데', '19% 정도 높음', '', 0, 'ink'], ['나머지 5번(1년 뒤)', '첫날보다 낮음', '', 0, 'ink'], ['가장 나빴던 1997년', '1년 뒤 -44.9%', '', 0, 'ink']]}),
]
# 칸 = 그 칸의 말 줄이 시작한 뒤 숫자가 나오는 자리(줄 길이 비율) — 칸 i ↔ 장면 안 i번째 줄(1년 뒤 장면은 줄 2·3·4)
AT = [[0.45], [0.3, 0.5], [0.4, 0.4, 0.5], [None, 0.4, 0.5, 0.4, 0.35]]
for s_, at_ in zip(scenes, AT):
    off = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    pos = [off[i] + int(s_['lines'][i]['frames'] * f) for i, f in enumerate(at_) if f is not None]
    for t, p_ in zip(s_['data']['tiles'], pos): t[3] = p_
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('1년 다 지난 무리 15 · 그 뒤 1년 안에 첫날 종가보다 더 내려간 무리 14', '중앙 -11.8 %', "('19971024', -51.0)", "('20200319', 1.7)", '무리 첫날 1년 뒤: 편수 15 오른 편 10 중앙 19.1'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: KOSPI-1 롱폼 Pexels 실사만(11/23 PD 눈 확인 — 38557069 'BTCUSDT'·7578632 '$' 글자 화면·5909916 달러 지폐는 뺌, 39494572 휴대폰은 앱 글자 safezone 걸려 뺌, 얼굴 0)
BG = [(0, 'kospi1/stock/8495394', 0), (2, 'kospi1/stock/5224014', 3), (3, 'kospi1/stock/6186015', 2), (4, 'kospi1/stock/8495394', 4),
      (5, 'kospi1/stock/3945008', 18), (6, 'kospi1/stock/6186015', 8), (7, 'kospi1/stock/5224014', 10), (8, 'kospi1/stock/8495394', 12),
      (9, 'kospi1/stock/3945008', 10), (10, 'kospi1/stock/5224014', 14), (11, 'kospi1/stock/6186015', 0)]
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
    fr = l['frames'] + (TAIL if k == BG[-1][0] else 0)
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
p = {'fps': 30, 'name': 'k1s_bottom', 'v': 1, 'look': 'live', 'question': ['코스피 하루 -5% 빠진 첫날', '바닥이었을까?'], 'hot': '바닥',
     'answer': {'label': '1995~2025 하루 5% 넘게 빠진 날 15번(석 달 안쪽으로 이어진 날은 한 번으로, 올해 묶음 뺌)', 'items': ['14번은 1년 안에 더 내려감', '1년 뒤엔 10번 첫날보다 높음'], 'arrow': False, 'note': '더 내려간 폭 가운데 12% 정도 · 1997년 10월은 첫날의 절반 아래까지'},
     'base': '한국은행 ECOS 코스피 일별 종가(원자료 한국거래소, 1995-01-03~2026-11-20, 2026-11-23 내려받음) · 1년 안 최저·1년 뒤 = 빠진 날 종가 대비 · 파이어맵 계산', 'long': 'bBoh8J1Ru_4',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'k1s_bottom.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'k1s_bottom: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
