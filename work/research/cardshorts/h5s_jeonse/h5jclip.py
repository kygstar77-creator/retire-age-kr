# h5s_jeonse c1clip (firemap-video-producer 2026-11-21 18:3x) — h5s_half/h5hclip.py 사본, 줄·장면·배경만 바꿈 (11/27 19:20 칸)
#   py -3.12 work/research/cardshorts/h5s_jeonse/h5jclip.py   → work/video/h5s_jeonse.json
# 재료: H-5 롱폼(tvCsLWDF814, 11/22 공개) 4장 '전세는 매매의 몇 %' — voice.json 5:7·5:8·5:9·5:2·5:3·5:4 + 5장 6:0·6:1 그대로, 첫 줄 1줄만 새로(newline.json, H-5 tts.json Charon 1.1 — f0 135.6Hz = 편 중앙 129.4Hz +5%), 브랜드 첫·끝 줄 없음
# 숫자: H-5 calc_out_1121.txt §4 — 2026.07~10 순수전세 84㎡대 838건·중앙 4.16억 · 단지 38곳 전세가율 중앙 57%·가장 높은 곳 70%(송도금호어울림)·가장 낮은 곳 39%(퍼스트파크F15BL)
# 11/21 1차 이해 시험(43·52·63세) 뜻 3/3·권유 0/3 · '전세가율' 뜻 안 풀림 3/3 → 0초 칸 '전세가율 → 전세 ÷ 매매값' · '중간'이 무엇의 가운데인지 3/3 → '38곳 줄 세운 가운데' · 반전세 2/3 → '월세 낀 거래 뺌' · 57%(비율)와 4억 1천(금액) 둘 다 '중간'이라 섞임 2/3 → '전세 금액 가운데' (새 녹음 0, 화면 칸만)
# 11/21 2차(46·55·65세) 뜻 3/3·권유 0/3 · '전세 ÷ 매매값' 기호 멈칫 2/3 → '전세가율이란 → 전세금이 집값의 몇 %' · 사이트를 어떻게 찾나 2/3 → '검색: 국토부 실거래가 → 단지·넓이·기간 고르기' · 반전세 3/3은 말 줄이라 칸 '월세 낀 거래 뺌'으로 둠 · 57%가 높은지·매매 가운데 금액 3/3은 기준선·전체 값 없음(지어내지 않음, 롱폼 몫)
# 11/21 렌더 1차 safezone: 20.0초 열쇠고리 집 모양 장식을 글자로 잡음(아래 672px 안) → 7줄(4억 1천) 배경을 단지 노을 37873585 25초로 → 렌더 2차 눈 검사 18.6초 노을이 거의 검정 → 수로 37736994 14초로
# 질문형 첫 줄('몇 %일까요?')은 f0 +29%로 ±25% 밖 → 평서형 '세어 봤어요'(+5%)로
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-5')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'calc_out_1121.txt', 'calc2_out_1121.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
NEW = json.load(open(os.path.join(HERE, 'newline.json'), encoding='utf-8'))
SRC += json.dumps(json.load(open(os.path.join(VID, 'h5.json'), encoding='utf-8'))['scenes'], ensure_ascii=False)
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·H-5 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('단지마다', ['NEW'],
       {'tiles': [['전세가율이란', '전세금이 집값의 몇 %', '', 0, 'ink']]}),
    sc('38곳 가운데', ['중간이 57%', '낮은 곳은 39%', '높은 곳은 70%'],
       {'tiles': [['38곳 줄 세운 가운데', '57%', '', 0, 'ink'], ['가장 낮은 곳', '39%', '', 0, 'ink'], ['가장 높은 곳', '70%', '', 0, 'ink']]}),
    sc('어떤 거래', ['2026년 7월부터 10월까지 84㎡ 전세', '8백 건이 넘습니다.', '중간은 4억 1천만원'],
       {'tiles': [['7~10월 84㎡대', '월세 낀 거래 뺌', '', 0, 'ink'], ['거래', '8백 건 넘게', '', 0, 'ink'], ['전세 금액 가운데', '4억 1천만원쯤', '', 0, 'ink']]}),
    sc('내 단지는', ['내 단지는 직접 세어', '국토교통부 실거래가 공개시스템에서'],
       {'tiles': [['내 단지는', '직접 세어 보기', '', 0, 'ink'], ['검색: 국토부 실거래가', '단지·넓이·기간 고르기', '', 0, 'ink']]}),
]
FR = [[0.05], [0, 0.35, 0.67], [0.05, 0.63, 0.76], [0.05, 0.33]]   # 칸 = 말 닿는 자리: 57·39·70 / 기간·8백·4억 / 직접·국토부
for s_, fr_ in zip(scenes, FR):
    for t, f in zip(s_['data']['tiles'], fr_): t[3] = int(s_['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('단지 38곳 전세가율 중앙 57%', '매매 중앙 5.90억 = 70%', '매매 중앙 12.20억 = 39%', '순수전세 84㎡대 838건', '전체 중앙 4.16억'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 11/20 눈 검사 1차(sheet_1120): 8.5초·17.5초 눈길(15082793) 위 흰 글자 약함 → 단지 컷·센트럴파크 컷으로 바꿈 · 끝 답 칸은 live 꼴에서 안 그려짐(Hero until 0) — 82%는 화면에 없음
# 배경: (줄 번호, 경로, 시작 초) · H-5 롱폼 Pexels(송도 센트럴파크·수로·단지 — 34438613은 라이선스 기록 없어 안 씀) + H-2 열쇠 건네는 손(직거래 줄, 얼굴 0) + H-4 단지 컷 · 11/20 PD 눈 확인(scratchpad h5bg/sheet.jpg)
# 배경: H-5 롱폼 Pexels(송도 센트럴파크 18495181·수로 37736994) + H-4 단지 노을 37873585 + H-2 열쇠 건네는 손 8293504(전세 계약 줄, 얼굴 0) — h5s_half에서 눈 확인한 컷만(15082793 눈길은 흰 글자 약해 뺌)
BG = [(1, 'h5/stock/18495181', 1), (2, 'h4/stock/37873585', 2), (3, 'h5/stock/37736994', 1), (4, 'h4/stock/37873585', 15),
      (5, 'h5/stock/18495181', 7), (6, 'h2/8293504', 1), (7, 'h5/stock/37736994', 14), (8, 'h5/stock/37736994', 9), (9, 'h5/stock/18495181', 12)]
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
p = {'fps': 30, 'name': 'h5s_jeonse', 'v': 1, 'look': 'live', 'question': ['송도 84㎡ 전세', '매매값의 몇 %일까?'], 'hot': '몇 %',
     'answer': {'label': '송도동 84㎡대 단지 38곳 · 2026.07~10 순수 전세', 'items': ['가운데 57%', '낮은 곳 39% · 높은 곳 70%'], 'arrow': False, 'note': '전세 보통 값 4억 1천만원쯤 · 8백 건 넘게'},
     'base': '국토교통부 아파트 전월세·매매 실거래(송도동 84㎡대, 2026-11-21 내려받음) · 전세가율 = 단지별 전세 보통 값 ÷ 매매 보통 값 · 파이어맵 계산', 'long': 'tvCsLWDF814',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h5s_jeonse.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h5s_jeonse: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
