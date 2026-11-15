# p1s_avg — P-1 롱폼(vsL7mojDW7w) 2장 금액 2줄 + 4장 '평균까지 살면 누가 앞서나'를 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-15, p1s_born/p1bclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/p1s_avg/p1aclip.py   → work/video/p1s_avg.json
# 목소리 = P-1 voice.json 문장 wav 그대로 + 첫 줄 하나만 같은 목소리로 새로 받음(newline.py, Charon 1.1 = P-1 tts.json)
# 뺀 줄: '연금 씨' 줄 둘(10/21 가상 인물 금지) · '이 나이들, 빠른 편일까요'·'당긴 쪽이 따라잡히는 나이는'·'미룬 쪽이 앞서는 나이는'·'생각보다 아슬아슬하죠'(3장 따라잡는 나이를 가리킴 — p1s_cross와 같은 질문)
# 숫자 원문 = P-1 facts.txt [F2] 조기·연기 비율(제61조·제62조②) · [F5] 간이생명표 2024 65세 기대여명 · calc_out 누적(84.5세·88.7세)
# 11/15: 26753905(작가 이름 'Celeste 2305'의 숫자가 설명란 숫자 대조에 걸림) → 뺌, 6424125 도장 손
# 배경 = P-1 stock(Pexels, credits.json) 중 얼굴·글자 없는 컷 — 11/15 눈 검사(scratchpad p1a/sheet.jpg): 8970851(얼굴)·1793371(손글씨)·6282368(PAYROLL)·12021845(글자판)·5408798(2021·상표)·7344550(병 상표)·8134590(달력 숫자) 뺌
import os, re, json, sys, subprocess, shutil, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'P-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {}
for s in V['sections']:
    if s.get('title', '').startswith('[0.'): continue   # 예고 줄(본편 재사용)은 건너뜀 — 같은 글이 본편에 있음
    for l in s['lines']: BYTEXT.setdefault(l['text'], l)
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('facts.txt', 'calc_out.txt', 'script.md') if os.path.exists(os.path.join(EP, f)))
CR = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
STOCK = {'pages': 6219901, 'candle_dark': 15517231, 'cake_many': 19875346, 'stamp_hand': 6424125, 'leaves_feet': 5790914, 'jeans_feet': 34418451, 'couple_back': 8970858, 'book_edge': 7235016, 'cake_party': 7100823, 'boots': 5612232, 'star_candle': 3325982, 'path_feet': 3978362}
SEC = {'pages': 39.3, 'candle_dark': 10.8, 'cake_many': 21.4, 'stamp_hand': 11.1, 'leaves_feet': 28.0, 'jeans_feet': 12.8, 'couple_back': 20.7, 'book_edge': 18.1, 'cake_party': 16.9, 'boots': 32.9, 'star_candle': 13.6, 'path_feet': 6.7}   # 11/15 ffmpeg 실측(sheet 라벨)
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
    if pad: ls[-1] = dict(ls[-1], pad=pad)   # 말 뒤 무음(C1S는 줄 소리를 줄 시작에 두고 장면 길이만큼 화면을 둠 — 11/14 이해 1차 '네 해 묶음 중간 단계 없음' 3/3)
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.~]*', ' '.join(strs)):
        d = d.rstrip('.,~')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·P-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': [{k: v for k, v in l.items() if k != 'pad'} for l in ls], 'frames': sum(l['frames'] for l in ls) + pad, '_pad': pad}


# 11/15 이해 1차(43·54·63세): 뜻·할 일·응용 3/3·권유 0/3 · 0초 '누가'를 남녀로 읽음 3/3 → 질문 둘째 줄 '당겨·제때·미뤄 받기 중 어느 쪽이 더?' · '5년 당기면' 기준 나이 없음 3/3 → 첫 칸 '제때 65세부터'·칸 '60세로 당기면'·'70세로 미루면' · '제때'가 14초에 처음 나옴 3/3·'−' 빼기 기호 1/3 → 칸 '제때가 당김보다'·'미룸이 제때보다' (새 녹음 0)
# 11/15 이해 2차(47·57·66세): 뜻·할 일·응용 3/3·권유 0/3·'제때' 바로 앎 3/3 · '누가'가 사람(남녀·부부)으로 잠깐 읽힘 3/3(뜻은 맞게 읽음) → 질문 둘째 줄 '어느 쪽이' · '그 사이' 언제인지 2/3 → 칸 '미루는 동안 쓸 돈' (새 녹음 0)
NEW = json.loads(open(os.path.join(HERE, 'newline.json'), encoding='utf-8').read())
BYTEXT[NEW['text']] = NEW
scenes = [
    sc('질문', ['국민연금 월 100만원, 평균 수명까지면'],
       {'tiles': [['제때 65세부터', '월 100만원이라면', '', 0, 'ink']]}),
    sc('세 길', ['5년을 당기면 70만원', '반대로 5년을 미루면'],
       {'tiles': [['60세로 당기면', '월 70만원', '', 0, 'ink'], ['70세로 미루면', '월 136만원', '', 69, 'ink']]}),
    sc('남자 평균', ['통계청 생명표로 보면', '남자 평균까지면', '그런데 미룸은'],
       {'tiles': [['65세 남자 평균', '84.5세까지', '', 0, 'ink'], ['제때가 당김보다', '+2,820만원', '', 173, 'ink'], ['미룸이 제때보다', '+264만원', '', 294, 'ink']]}),
    sc('여자 평균', ['여자는 89세', '여자 평균까지 가면', '미룸이 제때보다'],
       {'tiles': [['65세 여자 평균', '88.7세까지', '', 0, 'ink'], ['미룸이 제때보다', '+2,078만원', '', 157, 'ink']]}),
    sc('갈림', ['오래 받을수록 미룬', '그래서 답은 평균에', '내 건강, 그리고'],
       {'tiles': [['오래 받으면', '미룬 쪽이 앞섬', '', 0, 'ink'], ['답을 가르는 것', '건강 · 그동안 쓸 돈', '', 199, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    if s_['_pad']: assert all(0 <= t[3] < s_['frames'] - 30 for t in s_['data']['tiles']), s_['label']   # 계단 칸은 줄 중간·무음 구간에 섬
    else: assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), ('같은 프레임 두 칸 — live는 뒤 칸만 보임', s_['label'])
for x in ('84.5세', '88.7세', '2,820만원', '264만원', '2,078만원', '연 7.2%', '제62조②', '제61조②', '5년 당김 70만원', '5년 미룸 136만원'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
BG = [('pages', 2), ('candle_dark', 1), ('cake_many', 1), ('couple_back', 8), ('leaves_feet', 1), ('jeans_feet', 1), ('stamp_hand', 1), ('path_feet', 0.5), ('cake_party', 1), ('boots', 2), ('star_candle', 1), ('boots', 18)]   # 11/15 눈 검사: 7235016 책 옆면 글자(키릴 문자)·끝 칸 주황 글자가 밝은 흙길 위 대비 낮음 → 책 빼고 흙길은 8장, 끝은 어두운 부츠 뒤 구간
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'p1s_avg', 'stock', name + '.mp4')
    if not os.path.exists(src):
        os.makedirs(os.path.dirname(src), exist_ok=True); shutil.copyfile(os.path.join(EP, 'stock', f'{STOCK[name]}.mp4'), src)
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/p1s_avg/stock/cut/{name}_{st}_f.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[str(STOCK[nm])]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'p1s_avg', 'v': 1, 'look': 'live', 'question': ['국민연금 평균 수명까지 받으면', '당겨·제때·미뤄 받기 중 어느 쪽이 더?'], 'hot': '누가 더',
     'answer': {'label': '월 100만원 · 평균 수명까지 받은 돈', 'items': ['남자 84.5세: 미룸이 제때보다 264만원', '여자 88.7세: 미룸이 제때보다 2,078만원'], 'arrow': False, 'note': '1969년생 · 제때 65세 · 평균일 뿐, 개인 수명 아님'},
     'base': '국민연금법 제61조·제62조 · 국가데이터처 간이생명표 2024(65세 기대여명) · 월 100만원 가정 · 파이어맵 계산', 'long': 'vsL7mojDW7w',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'p1s_avg.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'p1s_avg: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
