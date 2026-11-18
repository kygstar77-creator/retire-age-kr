# n2s_ladder — N-2 롱폼(kXnAKjC-84Q) 2·3·5·6·7장 '월급 계단 → 100명 중 몇 등' 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-15 06시, x1s_even/x1eclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/n2s_ladder/n2lclip.py   → work/video/n2s_ladder.json
# 목소리 = N-2 voice.json 문장 wav 그대로 + 첫 줄 하나만 같은 목소리로 새로 받음(newline.py, Charon 1.1, markup 끔 = N-2 tts.json) — f0 140.4Hz(쓴 7줄 중앙 136.4Hz, +2.9%)·whisper 받아쓰기 일치
# 11/15 이해 1차(43·54·63세): 뜻·할 일·응용(통장 270 → 세전 약 300 → 50등 안팎) 3/3·권유 0/3 · 0초 등수 방향 멈칫 3/3 → 질문 둘째 줄 '1등 = 가장 많이 받는 사람' · 끝 변환 빠름 3/3 → 말 뒤 1초
# 11/15 더함: 1장 '통장에 300만원 넘게 … 15%쯤' 줄(10%만 두면 통장 300만원 넘는 사람이 틀리게 셈)
# 뺀 것: 4장 한가운데 290만원·7장 평균 375만원(n2s_middle 10/19 공개분과 같은 질문) · 1장 출처 설명 줄(설명란·화면 끝 출처로)
# 숫자 원문 = N-2 script.md 숫자 표(n2nums_out [I]: 150 79.4%·250 58.5%·350 38.4%·450 26.7%·1,000 4.3%) · facts.txt
# 배경 = N-2 stock(Pexels, credits.json) 중 얼굴·상표·글자 없는 컷 — 11/15 눈 검사(scratchpad n2l/sheet.jpg): 11589653(빌딩 꼭대기 상표)·16657004(bdc 간판)·10422116(콜라 상표)·7247869·6927295(글자) 뺌
import os, re, json, sys, subprocess, shutil, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'N-2')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {}
for s in V['sections']:
    for l in s['lines']: BYTEXT.setdefault(l['text'], l)
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('facts.txt', 'calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
STOCK = {'platform': 19103667, 'legs': 853830, 'cross': 4992551, 'suit': 4992563, 'calc': 5923592, 'glass': 7317314, 'night': 27635322, 'road': 33585501, 'sky': 36282124}
SEC = {'platform': 8.1, 'legs': 19.9, 'cross': 8.4, 'suit': 9.8, 'calc': 10.4, 'glass': 18.4, 'night': 37.0, 'road': 42.8, 'sky': 58.3}   # 11/15 ffmpeg 실측
TAIL = 36
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def sc(label, lines, data, pad=0):
    ls = [L(t) for t in lines]
    if pad: ls[-1] = dict(ls[-1], pad=pad)
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.~]*', ' '.join(strs)):
        d = d.rstrip('.,~')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·N-2 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': [{k: v for k, v in l.items() if k != 'pad'} for l in ls], 'frames': sum(l['frames'] for l in ls) + pad, '_pad': pad}


NEW = json.loads(open(os.path.join(HERE, 'newline.json'), encoding='utf-8').read())
BYTEXT[NEW['text']] = NEW
scenes = [
    sc('질문', ['내 월급, 직장인 100명을'],   # 11/19 v2(benchmark 11/19 답 5초): 말 '맨 앞에 서는 1등이…'(4.6초) 뺌 — 첫 숫자 7.5→2.9초, 뜻은 위 질문 둘째 줄 '1등 = 가장 많이 받는 사람'·칸으로
       {'tiles': [['맨 앞 1등', '가장 많이 받는 사람', '', 0, 'ink']]}),   # 11/19 3차 이해 시험(42·53·64) 3/3 '1등 방향을 말로 못 들음, 윗줄은 작음' → 가운데 큰 글자를 방향으로 · 11/19: 두 칸을 0에 같이 두면 뒤 칸만 보여 위 질문 둘째 줄과 같은 말이 겹침 → 말과 맞는 첫 칸 하나
    sc('150', ['먼저 세전 150만원'], {'tiles': [['세전 150만원', '79등쯤', '', 0, 'ink']]}),
    sc('250', ['다음은 세전 250만원'], {'tiles': [['세전 250만원', '59등쯤', '', 0, 'ink']]}),
    sc('350', ['세전 350만원. 38등'], {'tiles': [['세전 350만원', '38등쯤', '', 0, 'ink']]}),
    sc('450', ['세전 450만원. 27등'], {'tiles': [['세전 450만원', '27등쯤', '', 0, 'ink']]}),
    sc('맨 앞', ['맨 앞으로 가 볼까요'], {'tiles': [['월 1,000만원 이상', '100명 중 4명', '', 0, 'ink']]}),
    sc('세전 모르면', ['세금 떼기 전 월급을 모르시면', '통장에 300만원 넘게'], {'tiles': [['세전 모르면', '통장 금액 + 10%쯤', '', 0, 'ink'], ['통장 300만원 넘으면', '+ 15%쯤', '', 151, 'ink']]}, pad=30),   # 11/15 이해 1차 3/3: 마지막 통장 변환이 가장 실용적인데 가장 빨리 지나감 → 말 뒤 1초   # 11/15: 10%만 두면 통장 300만원 넘는 사람이 등수를 낮게 읽음 → 1장 15% 줄도 넣음
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('79.4%', '58.5%', '38.4%', '26.7%', '4.3%', '| 150만원 | 79.4% | 79등', '| 450만원 | 26.7% | 27등'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
BG = [('platform', 0), ('cross', 0), ('suit', 0), ('glass', 1), ('calc', 1), ('night', 15), ('road', 1), ('sky', 1)]   # 11/15 렌더 safezone: 28~29초 책상 전화기 버튼 글자(FLASH·REDIAL)가 오른쪽 버튼 줄에 걸림 → 글자 없는 항공 도로 컷
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'n2s_ladder', 'stock', name + '.mp4')
    if not os.path.exists(src):
        os.makedirs(os.path.dirname(src), exist_ok=True); shutil.copyfile(os.path.join(EP, 'stock', f'{STOCK[name]}.mp4'), src)
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/n2s_ladder/stock/cut/{name}_{st}_{fr}.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[str(STOCK[nm])]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'n2s_ladder', 'v': 2, 'look': 'live', 'question': ['직장인 100명 중 내 월급 몇 등?', '1등 = 가장 많이 받는 사람'], 'hot': '몇 등',
     'answer': {'label': '세전 월급 → 100명 중 몇 등', 'items': ['150만원 79등 · 250만원 59등', '350만원 38등 · 450만원 27등'], 'arrow': False, 'note': '2024년 12월 세전 월 보수 · 일자리 기준'},
     'base': '국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」 · 2024년 12월 세전 · 파이어맵 계산', 'long': 'kXnAKjC-84Q',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'n2s_ladder_v2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'n2s_ladder: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 배경 {len(bg)}컷')
print('credits:', credits)
