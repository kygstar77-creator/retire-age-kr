# k1s_split c1clip (firemap-video-producer 2026-11-23) — k1s_recover/k1rclip.py 사본, 줄·장면·배경만 바꿈 (비축, 지수 축)
#   py -3.12 work/research/cardshorts/k1s_split/k1sclip.py   → work/video/k1s_split.json
# 재료: KOSPI-1 롱폼(khvIhE8Sf-s, 11/24 11:30 공개) 6장 '1천만원을 넣었다면' — voice.json 6:4·6:6·6:7·6:9·6:11·6:12·6:14·6:15·6:16·6:17·6:19 그대로, 첫 줄 1줄만 새로(newline.json, Charon 1.1 — f0 142.0Hz = 편 중앙 129.4Hz +9.8%)
# 숫자: KOSPI-1 calc2_out_1123(1천만원 한 번에 최저 5506998·중앙 11914250) · calc3_out_1123(첫날마다 한 번에/나눠) · script.md 6장 자막([S12] 나눠 넣기 중앙 10,852,500·최저 7,714,515·원금 넘은 편 10/15·나눠 더 많은 편 5/15)
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'KOSPI-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc2_out_1123.txt', 'calc3_out_1123.txt', 'calc_drop_out_1123.txt', 'facts.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
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
    sc('1천만원', ['NEW'],
       {'tiles': [['배당·수수료 뺌', '지수 값만으로 셈', '', 0, 'ink']]}),
    sc('한 번에', ['열다섯 번의 결과를', '가장 나빴던 때는 551'],
       {'tiles': [['한 번에 · 가운데', '1년 뒤 1,191만원', '', 0, 'ink'], ['한 번에 · 최악', '1년 뒤 551만원', '', 0, 'ink']]}),
    sc('열두 번 나눠', ['이번엔 같은 돈을 열두 번에', '그러면 중간은 1,085', '가장 나빴던 때는 771'],
       {'tiles': [['약 한 달마다 1/12', '12번 나눠', '', 0, 'ink'], ['나눠서 · 가운데', '1년 뒤 1,085만원', '', 0, 'ink'], ['나눠서 · 최악', '1년 뒤 771만원', '', 0, 'ink']]}),
    sc('갈린 곳', ['원금보다 불어난 횟수는', '한 번에 넣으면 오를 때', '나눠 넣으면 반대로'],
       {'tiles': [['원금 넘은 횟수', '둘 다 10/15', '', 0, 'ink'], ['한 번에', '더 벌고 더 잃음', '', 0, 'ink'], ['나눠서', '덜 벌고 덜 잃음', '', 0, 'ink']]}),
    sc('나눠서가 더', ['나눠 넣은 쪽이 더 많이', '다섯 번 모두', '어느 쪽이 맞다고'],
       {'tiles': [['나눠서가 더 남음', '15번 중 5번', '', 0, 'ink'], ['빠진 날 종가 대비', '1년 안 -20% 넘게', '', 0, 'ink']]}),
]
# 칸 = 그 칸의 말 줄이 시작한 뒤 숫자가 나오는 자리(줄 길이 비율) — 칸 i ↔ 장면 안 i번째 줄
AT = [[0.05], [0.1, 0.6], [0.4, 0.55, 0.6], [0.5, 0.4, 0.4], [0.6, 0.4]]
for s_, at_ in zip(scenes, AT):
    off = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    for i, (t, f) in enumerate(zip(s_['data']['tiles'], at_)): t[3] = off[i] + int(s_['lines'][i]['frames'] * f)
for s_ in scenes:
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles'])
    assert all(0 <= t[3] < s_['frames'] for t in s_['data']['tiles'])
    assert all(len(t[0]) <= 12 for t in s_['data']['tiles']), [t[0] for t in s_['data']['tiles']]
for x in ('최저 5506998 중앙 11914250', '19971024 한 번에 551만 · 나눠 넣기 771만', '1년 뒤 중앙 10,852,500원', '나눠 넣기 최저 7,714,515원', '한 번에 10/15 · 나눠 넣기 10/15', '나눠 넣기가 더 많았던 편 5/15', '21거래일마다 1/12씩'):
    assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: KOSPI-1 롱폼 Pexels 실사(credits.json 라이선스) — 지폐 세는 기계 5909916·지폐 세는 손 6326929·하락 그래프 3945008·휴대폰 손 6186015·옛 책더미 5224014 (11/23 PD 눈 확인 — 39494572 휴대폰 앱 글자가 safezone 왼쪽 가장자리에 걸리고 8495394 노을은 주황 답 칸이 묻혀 뺌, 5909916 8초·6326929 13초는 달러 지폐 앞면 초상·10달러가 크게 보여 뺌, scratchpad k1bg_sheet.jpg, 얼굴·상표 0)
BG = [(1, 'kospi1/stock/5909916', 1), (2, 'kospi1/stock/6326929', 1), (3, 'kospi1/stock/3945008', 4), (4, 'kospi1/stock/6186015', 2), (5, 'kospi1/stock/6326929', 7), (6, 'kospi1/stock/3945008', 9),
      (7, 'kospi1/stock/5224014', 7), (8, 'kospi1/stock/3945008', 16), (9, 'kospi1/stock/6186015', 9), (10, 'kospi1/stock/5224014', 13), (11, 'kospi1/stock/5224014', 1), (12, 'kospi1/stock/3945008', 22)]
DUR = {'kospi1/stock/5224014': 18.7, 'kospi1/stock/39494572': 24.0, 'kospi1/stock/3945008': 30.0, 'kospi1/stock/6186015': 15.0, 'kospi1/stock/5909916': 21.9, 'kospi1/stock/6326929': 20.5, 'kospi1/stock/8495394': 22.7}
LIC = {str(c['id']): f"Pexels {c['id']} 무료({c['author']})" for c in json.load(open(os.path.join(VID, 'public', 'bg', 'kospi1', 'stock', 'credits.json'), encoding='utf-8'))}
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
p = {'fps': 30, 'name': 'k1s_split', 'v': 1, 'look': 'live', 'question': ['코스피 -5% 날 1천만원', '한 번에 vs 나눠서, 1년 뒤?'], 'hot': '1년 뒤',
     'answer': {'label': '1995~2026 하루 5% 넘게 빠진 첫날 15번 · 1년 뒤', 'items': ['가운데 1,191만원 vs 1,085만원', '가장 나쁨 551만원 vs 771만원'], 'arrow': False, 'note': '원금 넘은 횟수는 둘 다 10/15'},
     'base': '한국은행 ECOS 코스피 일별 종가(원자료 한국거래소, 1995-01-03~2026-11-20, 2026-11-23 내려받음) · 지수 값만(배당·보수·세금·수수료 뺌) · 나눠 넣기 = 첫날부터 21거래일마다 1/12씩 · 파이어맵 계산', 'long': 'khvIhE8Sf-s',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'k1s_split.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'k1s_split: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
