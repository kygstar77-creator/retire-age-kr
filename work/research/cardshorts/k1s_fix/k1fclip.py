# k1s_fix — K-1 롱폼(H9Lv281MaLs) 5장 '2021년 고정 대출, 고정 끝나면 한 달 얼마 늘까'를 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-11, k1s_dep/k1dclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/k1s_fix/k1fclip.py   → work/video/k1s_fix.json
# 목소리 = K-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 예금·미국 금리·변동형 줄 뺌(질문 하나: 고정 끝난 대출)
# 5:9 '새로 빌리는 사람의 163만원보다'(롱폼 앞 장을 가리킴)·5:12 변동형 줄은 뺌
# 11/11 1차 이해 뜻·할 일 3/3·권유 0: 0초 '31만원'이 조건 없이 들려 '내 대출도 31만원' 3/3 → 첫 칸 '3억·30년 평균 셈'·0초 질문 '3억' · '한 해면 370만원' 암산 2/3 → 칸 '열두 달 더하면'
# 11/11 2차 뜻·할 일 3/3·권유 0: 첫 칸을 고쳐도 첫 말 '31만원 늘어요'가 '내 대출'로 들림 3/3 · '갚고 남은 원금' 말 없음 2/3 → 말 순서 바꿈: 조건(3억·30년·2021 평균)→5년 뒤 158만원→31만원 답(새 녹음 0, 답 14.8초 — 0초 질문·제목에 31만원)
# 11/11 눈 검사: 158만원·31만원 장면 배경 money_count가 계산기 화면 숫자('1480'·'250')를 보여 줌 → cup_stir 1·coffee_cloudy 1
# 11/11 눈 검사: 답 칸 '한 달 31만원쯤 늘어'가 긴 글이라 작은 흰 글자(126·158은 큰 주황) → 칸 '평균 셈, 한 달 더 → 31만원쯤'
# 11/11 safezone: 끝 배경 rain_window 60초 구간 빗방울 반사가 30~31초 아래 672px 글자 상자로 잡힘 → k1s_dep에서 통과한 rain_window 40
# 화면 숫자 = calc5_out.txt §5 · facts F12: 2021.08 고정형 2.98% 월 1,261,578 → 남은 원금 266,621,690 → 2026.09 5.11% 월 1,575,779 (차 +314,201, 한 해 +3,770,406)
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'K-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc5_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CR = {c['id']: c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
# K-1 k1props.py STOCK(11/9 id 바꾼 판) — K-1 공개본 눈 검사 통과 클립만
STOCK = {'rain_window': 4786522, 'coffee_cloudy': 6343938, 'notebook_hand': 6326847, 'news_cup': 6975845, 'money_count': 5466763,
         'money_pen': 1188938, 'cup_stir': 946148, 'notepad_calc': 29303349, 'water_drops': 16648343, 'dining_room': 11099870}
SEC = {'rain_window': 90.1, 'coffee_cloudy': 10.9, 'notebook_hand': 12.5, 'news_cup': 12.4, 'money_count': 25.2,
       'money_pen': 19.7, 'cup_stir': 21.4, 'notepad_calc': 37.0, 'water_drops': 12.0, 'dining_room': 14.0}   # 11/10 ffmpeg 실측
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·K-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('2021년', ['3억원을 서른 해 동안 갚는 고정형', '그때 고정형 평균 금리는', '한 달에 126만원'],
       {'tiles': [['2021년 여름 대출', '3억 · 30년 고정형', '', 0, 'ink'], ['그때 고정형 평균', '3%가 안 됨', '', 80, 'ink'], ['그때 한 달', '126만원', '', 174, 'ink']]}),
    sc('5년 뒤', ['5년이 지나 고정 기간이', '한 달에 158만원'],
       {'tiles': [['5년 뒤 고정 끝', '남은 원금에 지금 평균 5.11%', '', 0, 'ink'], ['이제 한 달', '158만원', '', 142, 'ink']]}),
    sc('답', ['2021년에 내던 돈보다', '한 해면 370만원이'],
       {'tiles': [['평균 셈, 한 달 더', '31만원쯤', '', 0, 'ink'], ['열두 달 더하면', '370만원 넘게', '', 116, 'ink']]}),
    sc('할 일', ['이건 평균 금리로 계산한 가정', '2021년 무렵 낮은 금리로'],
       {'tiles': [['평균으로 셈한 가정', '은행·상품마다 달라요', '', 0, 'ink'], ['고정형 대출이라면', '고정 끝나는 날 확인', '', 146, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), ('같은 프레임 두 칸 — live는 뒤 칸만 보임', s_['label'])
for x in ('처음 1,261,578', '남은 원금 266,621,690', '월 1,575,779 (차 +314,201, 한 해 +3,770,406)', '2.98%'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: K-1 공개본에 쓴 Pexels 클립 — 말 줄마다 하나, 같은 클립 다시 쓰면 다른 구간
BG = [('dining_room', 0), ('news_cup', 2), ('money_pen', 12), ('rain_window', 10), ('cup_stir', 1),
      ('coffee_cloudy', 1), ('notebook_hand', 0), ('water_drops', 2), ('rain_window', 40)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'k1', 'stock', name + '.mp4'); assert os.path.exists(src), name
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/k1/stock/cut/{name}_{st}_f.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[STOCK[nm]]['author'].strip() for nm, _ in BG}))
p = {'fps': 30, 'name': 'k1s_fix', 'v': 1, 'look': 'live', 'question': ['한국은행 평균 금리 · 주택담보대출', '2021년 3억 고정 대출, 고정 끝나면 한 달 얼마 늘까?'], 'hot': '고정 끝나면',
     'answer': {'label': '3억·30년 고정형 대출 한 달 납입액(은행 평균 금리)', 'items': ['2021년 8월 2.98%: 126만원', '5년 뒤 5.11%로 다시: 158만원'], 'arrow': False, 'note': '갚고 남은 원금 기준 · 내 금리는 은행마다 달라요'},
     'base': '한국은행 예금은행 신규취급 주택담보대출 고정형 평균 금리 2021년 8월·2026년 9월분 · 원리금균등 30년 · 파이어맵 계산', 'long': 'H9Lv281MaLs',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'k1s_fix.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'k1s_fix: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
