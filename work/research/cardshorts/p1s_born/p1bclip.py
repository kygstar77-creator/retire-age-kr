# p1s_born — P-1 롱폼(vsL7mojDW7w) 1장 '하루 차이로 한 살?' + 7장 '68세, 정해진 걸까'를 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-14, k1s_fix/k1fclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/p1s_born/p1bclip.py   → work/video/p1s_born.json
# 목소리 = P-1 voice.json 문장 wav 그대로(새 녹음 0, Chirp 3 HD Charon 1.1) · 브랜드 첫·끝 줄 뺌
# 뺀 줄: '화면에서 내 칸을 찾아 보세요'(live 꼴엔 표가 없어 말과 화면이 어긋남) · '다른 해에 태어나셨다면…비율은 똑같거든요'(조기·연기 비율 — 질문 밖) · 가상 인물 '연금 씨' 줄(10/21 가상 인물 금지)
# 숫자 원문 = P-1 facts.txt(국민연금법 부칙 법률 제8541호 제8조, 공단 노령연금 안내) · 68세 = [F7] 국회 토론회 발제안, 법 개정 아님(11/14 다시 확인: compete.md 끝 줄)
# 배경 = P-1 stock(Pexels, credits.json) 중 얼굴·글자 없는 컷 — 11/14 눈 검사(scratchpad p1f/sheet0·1): 케이크 초·별 초·책장·종이 묶음·도장 책상·도장 손·산책 발
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
STOCK = {'cal_hand': 8134590, 'cake': 19875346, 'star_candle': 3325982, 'book_flip': 6219901, 'paper_stack': 7235016, 'stamp_desk': 7344550, 'stamp_hand': 6424125, 'walk_boots': 5612232}
SEC = {'cal_hand': 31.2, 'cake': 21.4, 'star_candle': 13.6, 'book_flip': 39.3, 'paper_stack': 18.1, 'stamp_desk': 16.6, 'stamp_hand': 11.1, 'walk_boots': 32.9}   # 11/14 ffmpeg 실측
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


# 11/14 꼴 관문 ⓐ(첫 줄 숫자·35자): 롱폼 순서 첫 줄 '한 해의 마지막 날…'(43자·숫자 0)에 걸림 → 답 줄 '지금 법으로는 1969년생부터 65세가 끝'을 맨 앞(A-49 답 먼저), 끝은 '법이 바뀐 건 아니에요'
# 11/14 이해 1차(43·54·63세): 첫 말 '65세가 끝' 뜻 헷갈림 3/3 → 첫 칸 '지금 법의 마지막 칸 → 1969년생 65세' · '네 해 묶음' 중간 단계 없음 3/3·63세는 자기 칸 못 찾음 → 말 뒤 3초 더해 다섯 칸 계단 · '발제안' 낯섦 2/3 → 칸 '제안일 뿐'
# 11/14 이해 2차(47·57·66세): 첫 말 '65세가 끝' 여전히 3/3 → 첫 줄만 같은 목소리로 새로 받음 · 계단 1.2초씩 너무 빠름 3/3·말 없는 3초 '멈춘 줄' 2/3
#   → 롱폼 녹음 '화면에서 내 칸을 찾아 보세요.'(1장)를 계단에 붙이고 무음 66프레임, 칸마다 1.5초 · '하루 차이 = 태어난 해 경계' 2/3 → 칸 이름 '1968년생 마지막 날'·'1969년생 첫날'
# 새 줄: 같은 목소리·빠르기(Charon 1.1, P-1 tts.json, lfvoice.chirp_one) f0 129.0Hz vs 이 클립 롱폼 줄 중앙 123.7Hz(+4%), 4.16초
BYTEXT['지금 법으로는 1969년생부터 모두 65세에 받아요.'] = {'text': '지금 법으로는 1969년생부터 모두 65세에 받아요.', 'audio': 'audio/p1s/8cf5da7c92b0c19b.wav', 'frames': 125}
# 11/14 4차: '1968년생까지'의 '까지'가 그 앞 해도 64세로 읽힘 2/3 → '1968년생'·'1969년생'
STAIR = 111   # 11/14 3차: 1.5초도 빠름 3/3 → 칸마다 1.8초(54프레임), 말 없는 구간에도 칸이 계속 바뀜
scenes = [
    sc('지금 법', ['지금 법으로는 1969년생부터 모두'],
       {'tiles': [['지금 법으로는', '1969년생부터 65세', '', 0, 'ink']]}),
    sc('하루 차이', ['한 해의 마지막 날 태어난 사람과', '둘은 국민연금을 받기 시작하는 나이가'],
       {'tiles': [['1968년생', '64세부터', '', 0, 'ink'], ['1969년생', '65세부터', '', 146, 'ink']]}),
    sc('네 해마다', ['받는 나이는 네 해 묶음마다', '화면에서 내 칸을'],
       {'tiles': [['1953~56년생', '61세', '', 0, 'ink'], ['1957~60년생', '62세', '', 54, 'ink'], ['1961~64년생', '63세', '', 108, 'ink'],
                  ['1965~68년생', '64세', '', 162, 'ink'], ['1969년생부터', '65세', '', 216, 'ink']]}, pad=STAIR),
    sc('68세?', ["요즘 '받는 나이를 68세로", '이건 국회 토론회에서', '법이 바뀐 건 아니에요'],
       {'tiles': [['요즘 도는 이야기', '68세?', '', 0, 'ink'], ['국회 토론회 발제안', '제안일 뿐', '', 124, 'ink'], ['법 개정', '아직 없음', '', 217, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    if s_['_pad']: assert all(0 <= t[3] < s_['frames'] - 30 for t in s_['data']['tiles']), s_['label']   # 계단 칸은 줄 중간·무음 구간에 섬
    else: assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), ('같은 프레임 두 칸 — live는 뒤 칸만 보임', s_['label'])
for x in ('1957~60 62세', '1961~64 63세', '1965~68 64세', '1969~ 65세', '1953~56 61세', '법률 제8541호', '국회 토론회 발제안, 법 개정 아님'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: 말 줄마다 하나(같은 클립 두 번 안 씀)
BG = [('paper_stack', 1), ('cake', 1), ('star_candle', 1), ('book_flip', 2), ('cal_hand', 2), ('stamp_desk', 1), ('stamp_hand', 1), ('walk_boots', 2)]
allines = [dict(l, _pad=(s['_pad'] if j == len(s['lines']) - 1 else 0)) for s in scenes for j, l in enumerate(s['lines'])]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + l['_pad'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'p1s_born', 'stock', name + '.mp4')
    if not os.path.exists(src):
        os.makedirs(os.path.dirname(src), exist_ok=True); shutil.copyfile(os.path.join(EP, 'stock', f'{STOCK[name]}.mp4'), src)
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/p1s_born/stock/cut/{name}_{st}_f.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-g', '10', '-bf', '0', '-r', '30', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[str(STOCK[nm])]['author'].strip() for nm, _ in BG}))
for s_ in scenes: s_.pop('_pad')
p = {'fps': 30, 'name': 'p1s_born', 'v': 5, 'look': 'live', 'question': ['국민연금 수령나이 · 출생연도', '몇 년생부터 65세? 하루 차이로 한 살 갈린다'], 'hot': '한 살',
     'answer': {'label': '국민연금 받기 시작하는 나이(출생연도별)', 'items': ['1961~64년생: 63세', '1965~68년생: 64세', '1969년생부터: 65세'], 'arrow': False, 'note': '68세는 국회 토론회 제안 · 법 개정 아님'},
     'base': '국민연금법 부칙(법률 제8541호) 제8조 · 국민연금공단 노령연금 안내 · 68세: 2026년 국회 토론회 발제안(법 개정 아님)', 'long': 'vsL7mojDW7w',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'p1s_born.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'p1s_born: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
