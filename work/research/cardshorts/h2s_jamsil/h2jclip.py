# h2s_jamsil c1clip (firemap-video-producer 2026-11-19 18:5x) — h3s_number/h3nclip.py 사본, 줄·장면·배경만 바꿈
#   py -3.12 work/research/cardshorts/h2s_jamsil/h2jclip.py   → work/video/h2s_jamsil.json
# 재료: cardshorts/h2_specs/spec.md 'h2s_jamsil' · 목소리 = H-2 voice.json 2장 문장 wav 그대로(새 녹음 0), 브랜드 첫·끝 줄·가상 인물 줄 없음
# 숫자: H-2 calc_out §2(5단지 평당 17,408 vs 리센츠 13,283 +31.1% · 84㎡ 중앙 43.45억 vs 34.15억) · calc2_out §1(층: 리센츠 1~3층 30.00억·4층↑ 34.30억, 5단지 차이 1.15억)
# 11/19 다시 받은 실거래(research/rt 11710, 계약 2025.12~2026.11)로도: 평당 +31.3% · 43.25억 vs 34.00억 · 달마다 5단지 최저 > 리센츠 최고 11/11달 · 리센츠 1~3층 30.0억·4층↑ 34.0억 · 5단지 차이 1.2억 → 말 그대로 맞음
# 11/19 1차 이해 시험(43·54·63세) 3/3 걸림 → 화면 칸만 고침(새 녹음 0): 평당↔한 채 30% · 9억 칸 · 층 장면 목적 · '정부 원문'→'정부 자료' · 가운데 값(평당)
# 11/19 2차(47·56·65세) 뜻 3/3·권유 0/3, 층 장면 목적 3/3 → 칸 '5단지는 1~3층도 42억쯤'(calc2_out §1 1~3층 42.60억 > 리센츠 4층↑ 34.30억)
# 11/19 눈 검사(sheet_1119): 칸 머리말 12자 넘으면 safeframe shortKick이 지움 → 12자 이하로
# 뺀 것: spec 끝 우성 '−10.4%'(2:8) — 11/19 다시 받으니 −7.6%(표본 7~10건)라 '10% 쌌다' 말이 지금은 안 맞음
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-2')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
SRC += json.dumps(json.load(open(os.path.join(VID, 'h2.json'), encoding='utf-8'))['scenes'], ensure_ascii=False)
TAIL = 36
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t) and '(재사용' not in k]; assert len(hit) == 1, (t, hit)   # 맺음 장 '(재사용 N장)' 줄은 같은 문장 다른 녹음 — 2장 원래 줄만
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    assert '손품' not in l['text'], '가상 인물 줄'
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-2 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [   # 칸 i = 줄 i 시작(한 줄 장면의 둘째 칸은 아래에서 말 닿는 자리로)
    sc('한 채 값', ['5단지 한 채는 약 43억'],
       {'tiles': [['잠실주공5단지 한 채', '약 43억', '', 0, 'ink'], ['리센츠 한 채', '약 34억 · 9억 차이', '', 0, 'ink']]}),
    sc('평당으로 보면', ['잠실 주공 5단지는 1978년에', '한 채로 보면 차이가 30%가', '거래를 값 순서로 줄 세워'],
       {'tiles': [['같은 넓이(평)당 값', '5단지가 30% 넘게 높음', '', 0, 'ink'], ['한 채론 30% 안 됨', '5단지 집이 조금 작아서', '', 0, 'ink'],
                  ['1년 거래 가운데 값(평당)', '잠실동 1위 5단지', '', 0, 'ink']]}),
    sc('한 해 내내', ['한두 건이 튄 게 아니었고'],
       {'tiles': [['1년 동안 달마다', '5단지가 더 비쌈', '', 0, 'ink']]}),
    sc('층을 따져도', ['층도 단지마다 달랐습니다', '4층부터는 34억쯤', '주공 5단지는 달랐어요'],
       {'tiles': [['리센츠 1~3층', '30억쯤', '', 0, 'ink'], ['리센츠 4층 이상', '34억쯤', '', 0, 'ink'], ['5단지는 1~3층도', '42억쯤 · 층 차이 1억', '', 0, 'ink']]}),
    sc('왜 비쌀까', ['그럼 왜일까요? 값이 왜'],
       {'tiles': [['왜 비싼지 정부 자료', '없음', '', 0, 'ink']]}),
]
for s_ in scenes:
    if len(s_['lines']) > 1:
        st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
        assert len(st) == len(s_['data']['tiles'])
        for t, f0 in zip(s_['data']['tiles'], st): t[3] = f0
s1 = scenes[0]; s1['data']['tiles'][1][3] = int(s1['frames'] * 0.55)   # '리센츠는 약 34억' — 줄 뒤쪽 절반쯤(5.44초 중 3초께)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0].replace('(평)','').replace('(평당)','')) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('17,408 vs 리센츠(2008) 13,283', '43.45억 vs 34.15억', '1~3층 5건 중앙 30.00억', '1~3층 12건 중앙 42.60억', '4층 이상 85건 중앙 34.30억', '차이 1.15억'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: (줄 번호, 클립, 시작 초) · H-2 롱폼 Pexels 풀(bg/h2) · 11/19 PD 눈 확인(scratchpad h2bg/sheet.png): 밝은 서울 아파트·도시 컷 위주, 어두운 밤 컷(34317846·35738744·38035115·9431584·32086385) 안 씀, 손+기기 1컷(6787197)
BG = [(1, '31018013', 1), (2, '5349092', 3), (3, '36216207', 2), (4, '31251627', 2), (5, '32986074', 1),
      (6, '6487935', 1), (7, '36216207', 12), (8, '29826322', 1), (9, '31018013', 8)]   # 11/19 눈 검사: 6787197 흰 종이 위 흰 머리말 안 보임 → 도시 실사
DUR = {'29826322': 8.0, '32986074': 12.0, '36216207': 19.0, '31018013': 15.0, '6787197': 8.0, '5349092': 24.0, '6487935': 13.0, '31251627': 15.0}
LIC = {}
def _w(x):
    if isinstance(x, dict):
        if 'src' in x and 'license' in x: LIC[x['src'].split('/')[-1][:-4]] = x['license']
        [_w(v) for v in x.values()]
    elif isinstance(x, list): [_w(v) for v in x]
_w(json.load(open(os.path.join(VID, 'h2.json'), encoding='utf-8')))
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    src = os.path.join(VID, 'public', 'bg', 'h2', cid + '.mp4')
    assert os.path.exists(src), cid
    assert DUR[cid] - st >= fr / 30 + 0.3, (cid, DUR[cid], fr / 30)
    cut = f'bg/h2/cut/{cid}_{st}_r{fr}.mp4'; cp = os.path.join(VID, 'public', cut)   # k1s_fix·h3s_number 법: B프레임 없이 -g 10으로 잘라 'No frame found' 피함
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-r', '30', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({f"{c} {re.search(r'[(](.*)[)]', LIC[c]).group(1).strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'h2s_jamsil', 'v': 1, 'look': 'live', 'question': ['잠실 아파트 실거래', '1978년 단지 vs 2008년 단지, 어디가 비쌀까?'], 'hot': '1978년',
     'answer': {'label': '잠실동 84㎡대 한 채 가운데 값(1년)', 'items': ['주공5단지(1978년) 약 43억', '리센츠(2008년) 약 34억'], 'arrow': False, 'note': '평당으론 30% 넘게 · 왜 비싼지 적힌 정부 자료는 없어요'},
     'base': '국토교통부 아파트 매매 실거래(계약 2025.11~2026.10, 2026-11-19 다시 받아 같은 값 확인) · 파이어맵 계산', 'long': '_fTgGr0dR0I',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h2s_jamsil.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h2s_jamsil: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
