# h6s_gangnam c1clip (firemap-video-producer 2026-11-26 14:2x) — h6s_before/h6bclip.py 사본, 줄·장면·배경만 바꿈 (비축, 부동산 축)
#   py -3.12 work/research/cardshorts/h6s_gangnam/h6gclip.py   → work/video/h6s_gangnam.json
# 재료: H-6 롱폼(YE6FXSezHXc, 11/26 11:30 공개) 2:24~2:31 그대로 + 첫 줄 1줄만 새로(newline.json — 롱폼 2:23 '그럼 은마만…'은 '그럼'이 앞 말에 기댐, H-6 tts.json Charon 1.1, f0 120.0Hz = 편 중앙 131.5Hz −8.7%) · 2:32~2:33(이유는 자료에 없음)은 빼고 2:31에서 닫음
# 숫자: H-6 calc3_out_1125.txt(강남구 80~86㎡ 23곳·내린 곳 16·가운데 −5.9%·은마 −19.4% 2번째·양쪽 2건 이상 8곳 가운데 −10.1%)
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
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out_1125.txt', 'calc2_out_1125.txt', 'calc3_out_1125.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
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
    sc('23곳 줄 세우기', ['NEW', '같은 강남구에서 34평', '스물세 곳이었고', '내린 폭 순서로'],
       {'tiles': [['강남구 34평 23곳', '16곳 내림 · 7곳 오름', '', 0, 'ink'], ['1년 전 · 요즘', '둘 다 거래 있는 단지', '', 0, 'ink'], ['23곳 중', '16곳 내림', '', 0, 'ink'], ['내린 폭 줄 세우면', '중간 단지 −5.9%', '', 0, 'ink']]}),
    sc('은마는 몇 번째', ['은마는 20% 가까이', '다만 단지 대부분은', '1년 전과 요즘 모두 두 건', '은마는 그 여덟 곳', '이 스물세 곳은'],
       {'tiles': [['은마 −19.4%', '23곳 중 2번째', '', 0, 'ink'], ['단, 단지 대부분', '거래 한두 건뿐', '', 0, 'ink'], ['두 건 이상 8곳만', '중간 단지 −10.1%', '', 0, 'ink'], ['8곳 중에서도', '은마가 가장 많이↓', '', 0, 'ink'], ['이유는 자료에 없음', '은마는 더 많이 내림', '', 0, 'ink']]}),
]
# 11/26 이해 1차(43·54·63세): '한가운데' 뜻·은마 금액·건수·23곳↔8곳 → 칸만 고침(새 녹음 0)
# 11/26 이해 2차(46·55·65세): '한가운데'→'중간 단지', '3건→10건' 칸이 오히려 헷갈림 → 뺌(설명란에), 이유 없음을 끝 칸에 → 칸만(새 녹음 0)
# 11/26 눈 검사 1차(eye/row_a·row_b): 은마 칸·끝 칸 글이 길어 작아지고 끝 칸은 손 동그라미와 겹침 → 은마 금액은 설명란으로, 끝 칸 머리를 '이유는 자료에 없음'으로 줄임
# 칸 = 그 칸의 말 줄이 시작한 뒤 숫자가 나오는 자리(줄 길이 비율) — 칸 i ↔ 장면 안 i번째 줄 · 첫 칸 0.1 → 약 0.2초(A-49 답 0초)
AT = [[0.08, 0.3, 0.45, 0.6], [0.1, 0.3, 0.6, 0.35, 0.2]]
for s_, at_ in zip(scenes, AT):
    off = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    for i, (t, f) in enumerate(zip(s_['data']['tiles'], at_)): t[3] = off[i] + int(s_['lines'][i]['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('단지 23곳 · 변화 가운데 값 -5.9% · 내린 곳 16 · 오른 곳 7', '대치동 은마 · 3건 42.80억 → 10건 34.50억 · -19.4%', '양쪽 2건 이상 8곳 · 가운데 값 -10.1%', '대치동 한보미도맨션1 · 1건'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: H-6 롱폼 Pexels 실사만(아파트 외관·도시 하늘, 얼굴·글자 0 — 렌더 뒤 눈 검사)
BG = [(1, 'h6/stock/30975009', 0), (2, 'h4/stock/38259259', 2), (3, 'h6/stock/38259256', 1), (4, 'h4/stock/37873585', 2), (5, 'h6/stock/29303349', 1),
      (6, 'h4/stock/38259259', 12), (7, 'h4/stock/37873585', 12), (8, 'h6/stock/38259256', 5.5), (9, 'h4/stock/38259259', 22)]
DUR = {'h4/stock/37873585': 32.9, 'h4/stock/38259259': 40.5, 'h6/stock/30975009': 6.4, 'h6/stock/38259256': 10.0, 'h6/stock/29303349': 8.4}
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
p = {'fps': 30, 'name': 'h6s_gangnam', 'v': 1, 'look': 'live', 'question': ['강남 34평', '은마만 내렸을까?'], 'hot': '은마만',
     'answer': {'label': '강남구 전용 80~86㎡ · 2025년 10~12월과 2026년 10~11월 둘 다 거래 있는 단지 23곳', 'items': ['16곳 내림 · 가운데 −5.9%', '은마 −19.4% · 2번째'], 'arrow': False},
     'base': '국토교통부 아파트 매매 실거래(강남구 전용 80~86㎡, 2025.10~12·2026.10~11 계약, 해제·직거래 제외, 2026-11-25 받음) · 단지별 가운데 값 · 파이어맵 계산', 'long': 'YE6FXSezHXc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'h6s_gangnam.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'h6s_gangnam: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
