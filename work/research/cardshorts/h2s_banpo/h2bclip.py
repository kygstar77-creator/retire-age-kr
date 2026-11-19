# h2s_banpo c1clip (firemap-video-producer 2026-11-20 07:1x) — h2s_jamsil/h2jclip.py 사본, 줄·장면·배경만 바꿈 (11/23 19:20 칸)
#   py -3.12 work/research/cardshorts/h2s_banpo/h2bclip.py   → work/video/h2s_banpo.json
# 재료: cardshorts/h2_specs/spec.md 'h2s_banpo' · 목소리 = H-2 voice.json 2장 문장 wav 그대로(2:28·2:14·2:29, 새 녹음 0), 브랜드 첫·끝 줄·가상 인물 줄 없음
# 숫자: H-2 calc_out §반포동(원베일리 19건 중앙 59.00억) · calc_out '래미안원베일리 2026.05 11건 차이 18.00억'(53.50억 6층·53.50억 2층 … 60.30억 6층 … 71.50억 13층, 모두 중개거래)
# 11/20 07:1x 다시 받은 실거래(rtmolit.fetch trade 11650 202605, 스크래치 11650_202605_trade_1120.json): 원베일리 84㎡대 11건·53.5억~71.5억·해제 0·모두 중개 → 그대로 맞음
#   1년(2025.11~2026.10 rt 파일) 19건 가운데 값 59.0억 → 그대로 맞음
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


scenes = [
    sc('같은 달 11건', ['반포 래미안원베일리에선 같은 단지, 같은 달에'],
       {'tiles': [['5월 가장 싼 거래', '53억 5천 · 6층·2층', '', 0, 'ink'], ['5월 가장 비싼 거래', '71억 5천 · 13층', '', 0, 'ink']]}),
    sc('1년으로 보면', ['반포 안에선 2023년에 입주한'],
       {'tiles': [['반포 평당 1위', '래미안원베일리', '', 0, 'ink'], ['1년 19건 한가운데', '한 채 약 59억', '', 0, 'ink']]}),
    sc('왜 달랐을까', ['그달 열한 건 모두 중개사를'],
       {'tiles': [['11건 다 중개사 거래', '직거래 0건', '', 0, 'ink'], ['같은 6층끼리도', '53억 5천 · 60억 3천', '', 0, 'ink'], ['그 값을 낸 사정', '신고 자료에 없음', '', 0, 'ink']]}),
]
# 꼴 ⓐ 첫 줄 35자 이하: 2:28 앞머리 '반포 래미안원베일리에선'(1.92초 쉼에서)만 잘라 냄 — m1clips_trim.py, 새 녹음 0, 남은 문장 받아쓰기 '같은 단지 같은 달에 산 값끼리 18억이 차이 나기도 했고요.'(3.1-flash-lite, 11/20) · 0초 화면 질문이 '반포 아파트 실거래'·답 칸 '래미안원베일리'
_l = scenes[0]['lines'][0]; _l.update(text='같은 단지, 같은 달에 산 값끼리 18억이 차이 나기도 했고요.', audio=_l['audio'].replace('.wav', '_from192.wav'), frames=124)
assert os.path.exists(os.path.join(VID, 'public', _l['audio']))
scenes[0]['frames'] = sum(l['frames'] for l in scenes[0]['lines'])
# 11/20 1차 이해 시험(44·53·64세): 59억이 5월인지 1년인지 3/3·'가운데 값' 낯섦 → '1년 19건 한가운데' · 중개 뜻 2/3 → '직거래 0건'(calc_out 직거래 0) · 6층 칸 빠름 3/3 → 0.42→0.30
# 11/20 2차(47·56·65세) 뜻·할 일 3/3·권유 0/3 · 71.5억 몇 층? 2/3 → '13층'(calc_out 29일 71.50억 13층) · '직거래 0건' 뜻 짐작 3/3(맞게) → 머리말 '11건 다 중개사 거래'
# 11/20 눈 검사 1차: 손 동그라미가 긴 값('71억 5천 · 13층 · 18억 차이'·'신고 자료에 칸 없음') 글자 양끝을 지나감 → 값 줄임(18억은 말·답 칸에)
FR = [[0, 0.55], [0, 0.62], [0, 0.30, 0.68]]   # 칸 = 말 닿는 자리(한 줄 장면): 18억·59억·층과 날짜·사정
for s_, fr_ in zip(scenes, FR):
    for t, f in zip(s_['data']['tiles'], fr_): t[3] = int(s_['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('래미안원베일리 2026.05 11건 차이 18.00억', '3일 53.50억 6층 중개거래', '15일 60.30억 6층 중개거래', '29일 71.50억 13층 중개거래', '래미안원베일리(건축 2023) 19건 중앙 59.00억'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: (줄 번호, 클립, 시작 초) · H-2 롱폼 Pexels 풀(bg/h2) · 11/19 PD 눈 확인(scratchpad h2bg/sheet.png): 밝은 서울 아파트·도시 컷 위주, 어두운 밤 컷(34317846·35738744·38035115·9431584·32086385) 안 씀, 손+기기 1컷(6787197)
BG = [(1, '32986074', 1), (2, '5349092', 3), (3, '31251627', 2)]   # 11/20 눈 검사 1차(sheet_1120): 끝 장면 흰 건물(36216207) 위 흰 글자 약함 → jamsil 4번 컷   # h2s_jamsil 11/19 눈 확인한 밝은 서울 도시·아파트 컷(얼굴 0), 시작 초는 jamsil 첫 컷과 다르게
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
p = {'fps': 30, 'name': 'h2s_banpo', 'v': 1, 'look': 'live', 'question': ['반포 래미안원베일리 실거래', '같은 단지 같은 달, 값이 얼마나 달랐을까?'], 'hot': '같은 달',
     'answer': {'label': '래미안원베일리 84㎡대 · 2026년 5월 11건', 'items': ['가장 싼 거래 53억 5천만원', '가장 비싼 거래 71억 5천만원'], 'arrow': False, 'note': '18억 차이 · 1년 19건 한가운데 값은 약 59억'},
     'base': '국토교통부 아파트 매매 실거래(계약 2025.11~2026.10, 2026년 5월분 2026-11-20 다시 받아 같은 값 확인) · 파이어맵 계산', 'long': '_fTgGr0dR0I',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h2s_banpo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h2s_banpo: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
