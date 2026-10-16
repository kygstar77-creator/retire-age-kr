# N-2 '직장인 100명 월급 줄' 화면 재료 → work/video/n2.json (N2.tsx가 읽는다) · 2026-10-16 N-2 PD
# 말 줄·길이는 voice.json(lfvoice), 숫자는 pilot/n2nums_out.txt [I][J][K](원문 표 경계값만, 보간 0)과 같다.
# 배경(10/16 영상 디자인 총괄 기준): 장면마다 Pexels 실사 영상·사진(work/video/public/bg/n2/), 한 배경은 BG_MAX초 이하로 끊어 다른 클립·다른 구간으로.
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
DUR = json.load(open(os.path.join(W, 'video', 'public', 'bg', 'n2', 'dur.json'), encoding='utf-8'))
FPS = V['fps']; BG_MAX = 6.5
SRC = '국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」(2026.2.23) · 2024년 12월 세전 월 보수 · 일자리 기준'
SRC_NET = SRC + ' · 통장 금액 = 파이어맵 월급 계산기(2026년 간이세액표·4대보험, 1인·식대 비과세 20만원 가정)'

# 원문 표(n2nums [I][J][K]) — 화면 숫자는 여기서만
RANK = {150: 79, 250: 59, 350: 38, 450: 27}   # 세전 X만원 이상 비율 79.4·58.5·38.4·26.7%
MID, MID_NET, AVG, TOP = 290, 260, 375, 4     # 가운데 288(말·화면 290쯤), 통장 2,568,400원, 평균 375, 1,000만원 이상 4.3%

# 배경 묶음(장 성격별) — 실존 인물 얼굴·상표·글자 없는 클립만(10/16 PD 프레임 눈 확인)
POOL = {
    'street': ['4992563', '853830', '15411757', '4992551', '33585501', '19103667', 'img:19271539'],
    'paper': ['5923592', '8691678', '6780084', '3202364', '6927295', '9823115', 'img:4792290'],
    'queue': ['853830', '6223515', '19103667', '26579264', '15411757', '4992563', 'img:761295'],
    'night': ['27635322', '15994652', '8064422', '36282124', '7317314', 'img:3142002'],
    'office': ['30217948', '8691678', '3202364', '9823115', 'img:19271539'],
}
used_at = {}   # 클립마다 다음에 쓸 시작 초(같은 클립을 다시 쓰면 다른 구간)
pool_i = {k: 0 for k in POOL}
last = [None]
def next_bg(pool, sec):
    L = POOL[pool]
    for _ in range(len(L)):
        c = L[pool_i[pool] % len(L)]; pool_i[pool] += 1
        if c == last[0]: continue
        if c.startswith('img:'): last[0] = c; return {'src': f'bg/n2/{c[4:]}.jpg', 'kind': 'image'}
        d = DUR.get(c) or 10; s = used_at.get(c, 0.0)
        if d < sec + 0.3: continue   # 클립이 조각보다 짧으면 끝에서 멈춘 화면이 된다 — 건너뜀
        last[0] = c
        if s + sec > d - 0.2: s = 0.0
        used_at[c] = round(s + sec, 2)
        return {'src': f'bg/n2/{c}.mp4', 'kind': 'video', 'start': round(s, 2)}
    raise SystemExit('배경 묶음 부족 ' + pool)

def segs_for(lines, total, pool):
    # 줄 경계에서 끊고, BG_MAX 넘는 줄·장 끝 꼬리는 반으로 나눈다
    cuts, a = [], 0
    for l in lines:
        n = l['frames']; k = max(1, -(-n // int(BG_MAX * FPS)))
        for j in range(k): cuts.append((a + j * n // k, (j + 1) * n // k - j * n // k))
        a += n
    if total > a: cuts[-1] = (cuts[-1][0], cuts[-1][1] + total - a)
    out = []
    for fr, n in cuts:
        out.append({'from': fr, 'frames': n, 'bg': next_bg(pool, n / FPS)})
    return out

S = V['sections']
assert len(S) == 9, len(S)
def L(si):
    return [{'text': l['text'], 'frames': l['frames'], 'audio': l['audio'], 'cap': None} for l in S[si]['lines']]

scenes = []
def add(si, kind, title, sub, pool, data, source=SRC, board=True, caps=None):
    lines = L(si)
    for i, c in (caps or {}).items(): lines[i]['cap'] = c
    scenes.append({'key': f's{si}', 'kind': kind, 'title': title, 'sub': sub, 'source': source, 'board': board, 'data': data,
                   'lines': lines, 'frames': S[si]['frames'], 'segs': segs_for(lines, S[si]['frames'], pool)})

add(0, 'queue0', '직장인 100명, 월급 순서로 한 줄', '맨 앞 1등 = 가장 많이 받는 사람', 'street',
    {'big': '100명', 'bigSub': '우리나라 직장인 전체를 100명으로 줄이면'}, board=True)
add(1, 'doc', '이 숫자는 어디서 왔나', '국가데이터처(옛 통계청) · 2024년 12월 한 달 월급', 'paper',
    {'img': 'bg/n2/wagejob_dist.png', 'row': [0.51, 0.67], 'tags': ['세금 떼기 전(세전)', '며칠만 일한 사람도 들어 있음'],
     'conv': [['통장 180만원', '세전 약 200만원', '통장에 10%쯤 더하기'], ['통장 300만원 넘으면', '15%쯤 더하기', '세금이 늘어서']], 'convAt': 3},
    source=SRC_NET, caps={4: '세전 200만원 → 통장 1,808,470원(실수령/세전 0.904)', 5: '세전 350만원 = 통장 × 1.14쯤 · 세전 450만원 = 통장 × 1.18쯤 (실수령/세전 0.876·0.849)'})
add(2, 'queue', '세전 150만원', '100명 중 79등쯤 · 아직 줄 뒤쪽', 'queue',
    {'from': 100, 'to': RANK[150], 'money': '세전 150만원'}, caps={0: '월 150만원 이상 79.4%'})
add(3, 'queue', '세전 250만원', '100명 중 59등쯤 · 아직 절반보다 뒤', 'queue',
    {'from': RANK[150], 'to': RANK[250], 'money': '세전 250만원', 'between': [RANK[150], RANK[250]], 'betweenAt': 1}, caps={0: '월 250만원 이상 58.5%'})
add(4, 'big', '줄 한가운데, 50등', '이 사람보다 많이 받는 사람 절반 · 적게 받는 사람 절반', 'queue',
    {'items': [{'at': 0, 'big': '50등은?', 'small': '100명 줄 딱 한가운데'}, {'at': 1, 'big': f'{MID}만원', 'small': f'세전 기준 · 통장 약 {MID_NET}만원'}]},
    source=SRC_NET, board=False, caps={1: '가운데 288만원 · 통장 2,568,400원'})
add(5, 'queue', '세전 350만원', '100명 중 38등쯤 · 줄 앞쪽 절반', 'paper',
    {'from': RANK[250], 'to': RANK[350], 'money': '세전 350만원', 'mid': 50}, caps={0: '월 350만원 이상 38.4%'})
add(6, 'queue', '세전 450만원', '100명 중 27등쯤 · 꽤 앞쪽', 'office',
    {'from': RANK[350], 'to': RANK[450], 'money': '세전 450만원', 'mid': 50}, caps={0: '월 450만원 이상 26.7%'})
add(7, 'avg', '맨 앞 — 평균이 높은 까닭', '평균 = 모두 더해서 사람 수로 나눈 값', 'night',
    {'big': f'{TOP}명', 'bigSub': '월 1,000만원 이상 받는 사람, 100명 중', 'avg': AVG, 'mid': MID, 'barsAt': 1, 'floorAt': 3, 'topAt': 4},
    board=False, caps={0: '월 1,000만원 이상 4.3%', 1: '평균 375만원 · 가운데 288만원 · 차 87만원'})
add(8, 'summary', '내 자리 보는 법', '평균 말고 줄 한가운데와 견주기', 'office',
    {'rows': [['세전 150만원', '79등'], ['세전 250만원', '59등'], [f'세전 {MID}만원 · 통장 약 {MID_NET}만원', '50등 · 한가운데'], ['세전 350만원', '38등'], ['세전 450만원', '27등'], ['1,000만원 이상', '100명 중 4명']],
     'hi': 2, 'note': '나이별 줄 → 댓글 맨 위', 'noteAt': 3}, source=SRC_NET)

props = {'fps': FPS, 'scenes': scenes, 'missing': V.get('missing', 0)}
out = os.path.join(W, 'video', 'n2.json')
json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
mx = max(g['frames'] for s in scenes for g in s['segs']) / FPS
print('장면', len(scenes), '· 길이', round(sum(s['frames'] for s in scenes) / FPS, 1), '초 · 배경 조각', sum(len(s['segs']) for s in scenes), f'· 최장 배경 {mx:.1f}초 →', out)
used = sorted({g['bg']['src'] for s in scenes for g in s['segs']})
json.dump(used, open(os.path.join(EP, 'bg_used.json'), 'w'), indent=0)
print('쓴 배경', len(used))

# ── 배경 조각 파일: N2.tsx는 장 안에서 TallyFrame 시계를 이어 가려고 조각마다 Sequence(from=-조각 시작)를 쓴다.
#    그러면 OffthreadVideo 시계도 장 시작부터 흐르므로, 조각 영상 앞에 '조각 시작'만큼 첫 화면을 채운 파일을 만든다(startFrom 0).
if '--cut' in sys.argv:
    import subprocess, imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe(); pub = os.path.join(W, 'video', 'public'); od = os.path.join(pub, 'bg', 'n2', 'seg'); os.makedirs(od, exist_ok=True)
    jobs = []
    for s in scenes:
        for i, g in enumerate(s['segs']):
            b = g['bg']
            if b['kind'] != 'video': continue
            name = f"{s['key']}_{i}.mp4"; pad = g['from'] / FPS; dur = g['frames'] / FPS + 0.2
            vf = f"trim=start={b['start']}:duration={dur},setpts=PTS-STARTPTS,tpad=start_duration={pad:.3f}:start_mode=clone"
            jobs.append([ff, '-v', 'error', '-y', '-i', os.path.join(pub, b['src']), '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p', '-r', '30', os.path.join(od, name)])
            g['bg'] = {'src': f'bg/n2/seg/{name}', 'kind': 'video', 'start': 0, 'from_clip': b['src'], 'clip_start': b['start']}
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:
        rcs = list(ex.map(lambda c: subprocess.run(c, capture_output=True).returncode, jobs))
    print('조각 파일', len(jobs), '실패', sum(1 for r in rcs if r))
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
