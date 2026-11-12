# p3s_cliff — P-3 롱폼(vgFx2od9_sg) 0장·1장 '국민연금 월 166만원→167만원, 건보료 0원→매달 6만 8천원쯤'을 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-12, k1s_fix/k1fclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/p3s_cliff/p3cclip.py   → work/video/p3s_cliff.json
# 목소리 = P-3 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 질문 하나: 피부양자 기준선 바로 위 한 칸
# 11/12 꼴 관문 ⓐ: 롱폼 첫 질문 줄(63자)이 35자 넘어 뺌 → 첫 줄 '기준은 한 해 소득 2천만원입니다.'(17자) · 물가 장(2:19·2:24) 더함
# 11/12 이해 1차(43·54·66세) 뜻·할 일 3/3·권유 0 · '왜 164만원' 3/3 → 칸 '2.1% 오르면 기준 위' · 끝 '연금은 절반 반영'이 기준에도 쓰이는 줄로 읽힘 3/3·7.19·13.14 뭘 곱하나 2/3 → 답 칸 비율 빼고 출처 줄 '보험료 = 연금의 절반 × 7.19%'
# 11/12 이해 2차(47·58·64세) 뜻·할 일 3/3·권유 0 · '피부양자에서 빠진다'가 말에 없고 설명란에만 2/3 → 칸 '월 167만원 → 피부양자 빠짐'
# 화면 숫자 = calc_out.txt: 경계 월액 1,666,666 · 166만→167만 보험료 +67,926원/월 · 영순 씨 줄 합계 월 68,521원(건강 60,563+장기요양 7,958)
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'P-3')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {c['scene'].split('/')[-1][:-4]: c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'p3', 'stock', 'credits.json'), encoding='utf-8'))}
SEC = {'open_bill': 12.0, 'mailbox_hand': 10.83, 'calculator_hand': 11.2, 'calendar_jan': 17.2, 'bench_backs': 12.0,
       'apartment_windows': 19.83, 'drawer_paper': 12.6, 'phone_pickup': 13.0}   # 11/12 ffmpeg 실측 · P-3 공개본(bg/p3/stock) 클립만
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·P-3 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('기준', ['기준은 한 해 소득 2천만원', '한 달로 나누면 166만원'],
       {'tiles': [['피부양자 소득 기준', '한 해 2천만원', '', 0, 'ink'], ['한 달로 나누면', '166만원쯤', '', 77, 'ink']]}),
    sc('답', ['166만원이면 한 푼도', '167만원이 되면 보험료가', '매달 6만 8천원쯤'],
       {'tiles': [['월 166만원', '0원', '', 0, 'ink'], ['월 167만원', '피부양자 빠짐', '', 75, 'ink'], ['건보+장기요양', '매달 6만 8천원', '', 151, 'ink']]}),
    sc('물가', ['국민연금은 해마다 1월에 물가만큼', '올해 월 164만원을 받는 분부터'],
       {'tiles': [['해마다 1월', '물가만큼 오름', '', 0, 'ink'], ['올해 월 164만원도', '2.1% 오르면 기준 위', '', 96, 'ink']]}),
    sc('할 일', ['집 같은 재산이 있으면', '연금 통지서를 꺼내서'],
       {'tiles': [['재산이 있으면', '이보다 커져요', '', 0, 'ink'], ['연금 통지서로', '내년 2천만원 넘나', '', 144, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), ('같은 프레임 두 칸 — live는 뒤 칸만 보임', s_['label'])
for x in ('경계 월액 1666666', '보험료 + 67926 원/월', '합계 월 68,521원', '7.19%', '13.14%'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: P-3 공개본에 쓴 Pexels 클립 — 말 줄마다 하나, 같은 클립 다시 쓰면 다른 구간
# 11/12 safezone: calculator_hand(계산기 숫자)·calendar_jan(달력 숫자)이 글자 상자로 잡힘(0~5초·11·13~15초) → 글자 없는 클립으로
BG = [('apartment_windows', 8), ('bench_backs', 6), ('phone_pickup', 0), ('open_bill', 0), ('mailbox_hand', 0),
      ('apartment_windows', 14), ('bench_backs', 0), ('apartment_windows', 2), ('drawer_paper', 0)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'p3', 'stock', name + '.mp4'); assert os.path.exists(src), name
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/p3/stock/cut/{name}_{st}_f.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[nm]['author'].strip() for nm, _ in BG}))
p = {'fps': 30, 'name': 'p3s_cliff', 'v': 1, 'look': 'live', 'question': ['건강보험 피부양자 소득 기준', '국민연금 월 166만원과 167만원, 건보료는?'], 'hot': '167만원',
     'answer': {'label': '국민연금만 받는 피부양자 · 재산 거의 없을 때', 'items': ['월 166만원: 건보료 0원', '월 167만원: 매달 6만 8천원쯤'], 'arrow': False, 'note': '건강보험+장기요양 합친 값 · 재산 있으면 더 커요'},
     'base': '국민건강보험법 시행규칙 피부양자 소득 기준 연 2천만원 · 보험료 = 연금의 절반 × 7.19%, 장기요양은 그 13.14% · 파이어맵 계산', 'long': 'vgFx2od9_sg',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'p3s_cliff.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'p3s_cliff: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
