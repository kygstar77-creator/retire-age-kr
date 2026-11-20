# h5s_half c1clip (firemap-video-producer 2026-11-20 22:3x) — h2s_banpo/h2bclip.py 사본, 줄·장면·배경만 바꿈 (11/26 19:20 칸)
#   py -3.12 work/research/cardshorts/h5s_half/h5hclip.py   → work/video/h5s_half.json
# 재료: H-5 롱폼(3dzKukPP3ac, 11/22 공개) 3장 '반값' — voice.json 4:7·4:9·4:10·4:13·4:14·4:15·4:16·4:18 그대로(새 녹음 0), 브랜드 첫·끝 줄 없음
# 숫자: H-5 calc2_out §4·§6 · facts [F9''] — 2022.07~2026.10 33곳 84㎡대 4,284건 · 절반 이하 2건(둘 다 직거래) · 60% 이하 27건 중 직거래 21건 · 직거래 131건 3.1%
# 11/20 1차 이해 시험(43·52·63세) 뜻 3/3·권유 0/3 · 고점이 언제인지 3/3 → 칸 '21년 고점 절반 이하'·출처 줄 '값 순서로 세운 한가운데' · 7~11초 칸 없어 빈 듯 2/3 → '넓혀서 세면 · 고점의 60% 아래' 칸 · 3%의 기준 1/3 → '4천여 건 중 직거래' · 남은 궁금증 '보통 거래는 고점의 몇 %' → 끝 답 칸 82%(calc2 §1)
# 11/20 2차(46·55·65세) 뜻·할 일 3/3·권유 0/3 · '21년 고점' vs 끝 줄 2021.07~2022.06 엇갈림 2/3 → 칸 '21~22년 고점의 반 · 그 아래 2건' · '가운데 값'·'82%(전체 영상)' 낯섦 2/3 → '보통 거래 값은 지금 고점의 82%쯤'·'거래의 보통 값'
# 11/20 22:2x 다시 받은 실거래(rtmolit 28185 202608~202611, 스크래치 h5re → calc2_out_1120pd.txt): 4,286건 · 절반 이하 2건(직거래 2) · 60% 이하 27건 중 21건 · 직거래 3.1% → 말 그대로 맞음
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-5')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
SRC += open(os.path.join(HERE, 'calc2_out_1120pd.txt'), encoding='utf-8').read()
SRC += json.dumps(json.load(open(os.path.join(VID, 'h5.json'), encoding='utf-8'))['scenes'], ensure_ascii=False)
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-5 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('4천 건 중', ['4천 건이 넘습니다.', '절반 이하로 팔린 건, 두 건'],
       {'tiles': [['33개 단지 84㎡대', '4천 건 넘게', '', 0, 'ink'], ['21~22년 고점의 반', '그 아래 2건', '', 0, 'ink']]}),
    sc('그 두 건은', ['그리고 그 두 건 모두'],
       {'tiles': [['2건 모두', '직거래', '', 0, 'ink']]}),
    sc('60% 아래로 넓히면', ['이번엔 고점의 60% 아래로', '그래도 스물일곱 건뿐', '그중 스물한 건이 직거래'],
       {'tiles': [['넓혀서 세면', '고점의 60% 아래', '', 0, 'ink'], ['그래도', '27건', '', 0, 'ink'], ['그중 직거래', '21건', '', 0, 'ink']]}),
    sc('직거래는', ['직거래는 전체 거래에선 3%', '직거래가 왜 쌌는지는'],
       {'tiles': [['4천여 건 중 직거래', '약 3%', '', 0, 'ink'], ['왜 쌌는지', '신고 자료에 없음', '', 0, 'ink']]}),
]
FR = [[0, 0.72], [0.70], [0, 0.53, 0.78], [0.35, 0.62]]   # 칸 = 말 닿는 자리(낱말이 들릴 때): 4천 건·두 건 / 직거래(줄 끝) / 스물일곱·스물한 / 3%·왜
for s_, fr_ in zip(scenes, FR):
    for t, f in zip(s_['data']['tiles'], fr_): t[3] = int(s_['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('절반 이하 2건 중 직거래 2건', '고점 반기의 60% 이하 27건 중 직거래 21건', '직거래 131건(3.1%)'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 11/20 눈 검사 1차(sheet_1120): 8.5초·17.5초 눈길(15082793) 위 흰 글자 약함 → 단지 컷·센트럴파크 컷으로 바꿈 · 끝 답 칸은 live 꼴에서 안 그려짐(Hero until 0) — 82%는 화면에 없음
# 배경: (줄 번호, 경로, 시작 초) · H-5 롱폼 Pexels(송도 센트럴파크·수로·단지 — 34438613은 라이선스 기록 없어 안 씀) + H-2 열쇠 건네는 손(직거래 줄, 얼굴 0) + H-4 단지 컷 · 11/20 PD 눈 확인(scratchpad h5bg/sheet.jpg)
BG = [(1, 'h5/stock/18495181', 1), (2, 'h5/stock/37736994', 1), (3, 'h2/8293504', 1), (4, 'h4/stock/37873585', 15),
      (5, 'h4/stock/37873585', 2), (6, 'h5/stock/37736994', 9), (7, 'h5/stock/18495181', 5), (8, 'h5/stock/18495181', 9)]
DUR = {'h5/stock/18495181': 20.0, 'h5/stock/37736994': 20.0, 'h2/8293504': 12.0, 'h4/stock/37873585': 32.9, 'h5/stock/15082793': 30.0}
LIC = {}
def _w(x):
    if isinstance(x, dict):
        if 'src' in x and 'license' in x: LIC[x['src'].split('/')[-1][:-4]] = x['license']
        [_w(v) for v in x.values()]
    elif isinstance(x, list): [_w(v) for v in x]
for j in ('h5.json', 'h2.json', 'h4.json'):
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
    cut = f'bg/h5/cut/{cid}_{st}_r{fr}.mp4'; cp = os.path.join(VID, 'public', cut)   # B프레임 없이 -g 10으로 잘라 'No frame found' 피함
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-r', '30', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({re.search(r'[(](.*)[)]', LIC[c.split('/')[-1]]).group(1).strip() for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'h5s_half', 'v': 1, 'look': 'live', 'question': ['송도 아파트 반값 거래', '4천 건 중 몇 건이었을까?'], 'hot': '반값',
     'answer': {'label': '송도동 33개 단지 84㎡대 · 2022.07~2026.10 거래', 'items': ['고점 절반 이하 2건 — 둘 다 직거래', '고점 60% 아래 27건 — 21건 직거래'], 'arrow': False, 'note': '직거래는 전체의 약 3% · 보통 거래 값은 지금 고점의 82%쯤'},
     'base': '국토교통부 아파트 매매 실거래(송도동 84㎡대, 2026-11-20 다시 받아 같은 값 확인) · 고점 = 단지별 2021.07~2022.06 거래의 보통 값 · 파이어맵 계산', 'long': '3dzKukPP3ac',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h5s_half.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h5s_half: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
