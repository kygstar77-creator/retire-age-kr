# j1s_couple — J-1 롱폼 6장 '부부 공동명의, 따로 낼까 한 사람으로 낼까'을 자른 세로 쇼츠 props · c1clip 틀(C1S live, E-18 통과 틀) (firemap-video-producer 2026-11-04, de1s_jepqhealth/de1qclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/j1s_couple/j1uclip.py   → work/video/j1s_couple.json
# 목소리 = J-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 답 5초 안(A-49): '14억을 겨우 넘겨도 → 50만원 이상'을 맨 앞으로
# 11/4 이해 1차(41·52·63): 뜻·할 일 3/3·명의 바꾸라 0(오해 여지 1/3) · '공제 18억' 2/3 모름 → '따로 내면 공제 9억+9억' · '일흔에 15년' 2/3 → 칸 '70세·15년 산 부부' · 정부안이 끝에야 2/3 → 첫 칸 '정부안 2028' · 신청 안 하면? → 롱폼 줄 '아무것도 신청하지 않으면 각자 따로' 넣음(칸 '신청 안 하면 / 따로 계산') · '그 전에' 1/3 애매 → 끝 줄을 '한 번 신청하면 다음 해부터는…계속'으로 바꿈
# 11/4 이해 2차(44·56·67): 뜻·할 일 3/3·권유 0 · '한 사람으로 계산'이 명의 바꾸기로 들릴 수 있음 3/3(설명란 보고 풀림) → 칸 '명의는 그대로 / 계산만 고름' · 정부안 늦음 2/3 → 0초 질문 맨 앞 '정부안' · '9억+9억' 1/3 → '각자 빼 주는 금액 9억씩'
# 11/4 이해 3차(42·51·65): 뜻·할 일 3/3·명의 오해 0(칸 '명의는 그대로' 3/3 봄)·권유 0 · '한 집안에서 한 사람이 집 한 채…'(21.9초) 3/3 멈칫 → 그 줄 뺌(할인은 한 사람 계산만 — 칸·앞 줄이 말함)
# 화면 숫자 = calc2_out.txt 2028 각자 53.8 · 특례 114.0(55세·10년) / 38.0(70세·15년) · 답 5초 안: '쉰다섯·10년' 줄은 0초 질문 화면으로 옮기고 '공시 20억 집이라면요'부터
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
    sc('55세·10년', ['공시 20억 집이라면요', '따로 내는 쪽이 60만원'],
       {'tiles': [['따로 내면', '54만원', '', 0, 'ink'], ['한 사람으로 계산', '114만원', '', 52, 'ink']]}),
    sc('70세·15년', ['그런데 일흔에 15년을', '한 사람으로 계산하는 쪽이 15만원'],
       {'tiles': [['70세 15년 따로', '54만원', '', 0, 'ink'], ['한 사람으로 계산', '38만원', '', 83, 'ink']]}),
    sc('고르기', ['공동명의 부부는 두 가지 중에', '아무것도 신청하지 않으면'],
       {'tiles': [['명의는 그대로', '계산만 고름', '', 0, 'ink'], ['신청 안 하면', '따로 계산', '', 102, 'ink']]}),
    sc('왜', ['따로 내면 빼 주는 금액이 크고'],
       {'tiles': [['각자 빼 주는 금액', '9억씩', '', 0, 'ink'], ['나이·햇수 할인', '한 사람 계산만', '', 0, 'ink']]}),
    sc('갈림', ['나이와 햇수 할인이 커질수록'],
       {'tiles': [['할인이 클수록', '한 사람이 유리', '', 0, 'ink']]}),
    sc('할 일', ['한 사람으로 계산해 달라는 신청은', '한 번 신청하면 다음 해부터는'],
       {'tiles': [['한 사람으로 신청', '9월 16일부터', '', 0, 'ink'], ['한 번 신청하면', '계속 그대로', '', 151, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('각자 납부(둘 합) 종부세 53.8 · 보유세 536.2 | 특례 신청(한 사람 1주택으로) 종부세 114.0', '특례 신청(한 사람 1주택으로) 종부세 38.0', '부부 반반 · 각자 냄 · 산다 | 18억(각 9억)'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: J-1 롱폼에 쓴(눈 검사 통과) Pexels 클립 — 얼굴·상표·글자 없는 것만(7247869 'tax fraud' 글자 보여 뺌) · 말 줄마다 하나
# 11/4 눈 검사: 칸 이름 12자 넘으면 safeframe shortKick이 '·' 앞만 남김('70세'만 보임) → '따로 내면'·'70세 15년 따로'
# 11/4 밝기 2: 렌더본 22~26초 Y 37~47(8794903@9)·34~36초 Y 21~35(9902446@10) → 30975009@50·38029457@7
# 11/4 밝기: 4553292(짐 상자) 어두움 → 4번 줄 8439245@1(서명)
# 11/4 렌더: 5923592_1 1.7초 No frame found 4번 → 2번 줄 9902446_2·4번 줄 4553292_2(j1s_cliff에서 렌더 통과한 cut) · 7710745(영수증 숫자) 뺌
BG = [(1, '30975009', 30), (2, '9902446', 2), (3, '8970842', 2), (4, '8439245', 1), (5, '8794903', 2), (6, '8293019', 1), (7, '1395943', 2), (8, '30975009', 50), (9, '7308166', 1), (10, '38029457', 7)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'j1', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    cut = f'bg/j1/stock/cut/{cid}_{st}.mp4'   # 11/3 de1q: 원본 긴 클립 찾기가 빈 메모리 적을 때 No frame found → 쓰는 구간만 잘라(원본 fps·GOP 10) 읽음
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', os.path.join(VID, 'public', 'bg', 'j1', 'stock', cid + '.mp4'), '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CRED[c]['author'].strip() for _, c, _ in BG}))   # 11/4: 클립 번호는 숫자 대조에 걸려 작가 이름만 + ' (Pexels License)'
p = {'fps': 30, 'name': 'j1s_couple', 'v': 1, 'look': 'live', 'question': ['정부안 · 공동명의 20억·55세', '따로? 한 사람으로 계산?'], 'hot': '한 사람',
     'answer': {'label': '정부안(국회 통과 전) 2028년 종부세', 'items': ['55세·10년: 따로 54만원', '70세·15년: 한 사람 38만원'], 'arrow': False, 'note': '할인이 클수록 한 사람'},
     'base': '종합부동산세법 개정안(정부안 · 국회 통과 전) · 공시 20억·부부 반반·그 집에 삶 가정 · 파이어맵 계산', 'long': 'NNcjTE0L7yg',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'j1s_couple.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'j1s_couple: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
