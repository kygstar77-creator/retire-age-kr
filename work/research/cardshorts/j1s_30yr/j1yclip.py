# j1s_30yr — J-1 롱폼 6장 '한집에 30년 살면 할인이 더 클까'를 자른 세로 쇼츠 props · c1clip 틀(C1S live, E-18 통과 틀) (firemap-video-producer 2026-11-08, j1s_couple/j1uclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/j1s_30yr/j1yclip.py   → work/video/j1s_30yr.json
# 목소리 = J-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · '앞의 고지서 사람처럼 10년'·'40%예요' 2줄은 롱폼 앞 장을 가리켜 뺌
# 화면 숫자 = calc_out.txt 70세·15년 표 20억 2028 종부세 38.0 · 보유세 527.9→520.4(−7.5) · 거주공제 15년 이상 50%(상세본 p.64) · 나이+거주 80% 한도
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'J-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'calc2_out.txt', 'calc3_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'j1', 'stock', 'credits.json'), encoding='utf-8'))}
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·J-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('기준', ['이런 댓글이 있었어요. 한집에 30년', "정부안은 그 기준을 '갖고 있던 해'"],
       {'tiles': [['30년 살면', '할인 더 클까', '', 0, 'ink'], ['할인 기준', '그 집에 산 해', '', 101, 'ink']]}),
    sc('5년', ['산 햇수 할인은 5년을 살면'],
       {'tiles': [['산 햇수 할인', '5년부터', '', 0, 'ink']]}),
    sc('15년', ['할인은 15년에서 끝나요', '그때 50%가 되고'],
       {'tiles': [['산 햇수 할인', '15년에서 끝', '', 0, 'ink'], ['15년 이상', '종부세 50% 깎음', '', 56, 'ink']]}),
    sc('같음', ['그래서 15년을 산 사람과 30년을'],
       {'tiles': [['15년 = 30년', '세금 같음', '', 0, 'ink'], ['공시 20억·70세', '종부세 38만원', '', 66, 'ink']]}),
    sc('할 일', ['이 법안은 아직 국회에서 심사 중', '고지서의 공시가격, 그리고'],
       {'tiles': [['정부안', '국회 심사 중', '', 0, 'ink'], ['내 경우 찾기', '공시가격·사는지', '', 116, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert s_['label'] == '같음' or all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)   # 11/8 눈 검사: 같은 프레임 두 칸이면 live는 뒤 칸만 보임('15년 = 30년' 가려짐) → 38만원 칸 66프레임(말 '30년을 산 사람은' 자리) 늦춤
for x in ('20억 | 45.5 | 38.0 | 38.0 | 527.9 | 520.4 | -7.5', '70세·보유 15년·거주 15년'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: J-1 롱폼·j1s_cliff·j1s_couple에 쓴(눈 검사·렌더 통과) Pexels 클립 — 얼굴·상표·글자 없는 것만 · 말 줄마다 하나
BG = [(1, '8970842', 2), (2, '8439245', 1), (3, '8293019', 1), (4, '12079562', 4), (5, '30975009', 10), (6, '8794903', 2), (7, '7308166', 1), (8, '30975009', 50)]
# 11/8 2차 이해 3/3: 19.7초 '보유세는 올해보다 조금 줄고요'·24.5초 '보유세는 재산세와 종부세' 두 줄이 15년=30년 흐름을 끊고 38만원과 따로 놂 → 두 줄 뺌, 38만원 칸은 '15년 = 30년' 장면으로
# 11/8 1차 이해 3/3: 16초 보유세≠종부세 → '여기서 보유세는…' 줄 · 21초 80% 줄 3/3 멈칫 → 뺌 · 산 햇수 vs 가진 햇수 2/3 → '정부안은 그 기준을…' 줄 · 할 일 0/3 → '고지서의 공시가격…' 줄 · 통과 전이 말로 없음 1/3 → '이 법안은 아직 국회에서' 줄 · cut 이름 _y(다른 편 cut 길이 재사용 막음)
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'j1', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    cut = f'bg/j1/stock/cut/{cid}_{st}_y.mp4'   # 11/3 de1q: 원본 긴 클립 찾기가 빈 메모리 적을 때 No frame found → 쓰는 구간만 잘라(원본 fps·GOP 10) 읽음
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', os.path.join(VID, 'public', 'bg', 'j1', 'stock', cid + '.mp4'), '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CRED[c]['author'].strip() for _, c, _ in BG}))   # 11/4: 클립 번호는 숫자 대조에 걸려 작가 이름만 + ' (Pexels License)'
p = {'fps': 30, 'name': 'j1s_30yr', 'v': 1, 'look': 'live', 'question': ['정부안 · 종부세 산 햇수 할인', '30년 살면 더 깎일까?'], 'hot': '30년',
     'answer': {'label': '정부안(국회 통과 전) 2028년 종부세', 'items': ['15년 산 70세: 38만원', '30년 산 70세: 38만원'], 'arrow': False, 'note': '내 경우는 아래 연결 영상 전체 표'},
     'base': '종합부동산세법 개정안(정부안 · 국회 통과 전) · 재정경제부 세제개편 상세본 · 공시 20억·70세·그 집에 삶 가정 · 파이어맵 계산', 'long': 'NNcjTE0L7yg',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'j1s_30yr.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'j1s_30yr: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
