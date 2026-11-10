# k1s_dep — K-1 롱폼(H9Lv281MaLs) 2장 '정기예금 1억 만기, 이자 얼마 늘었나'를 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-10, j1s_30yr/j1yclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/k1s_dep/k1dclip.py   → work/video/k1s_dep.json
# 목소리 = K-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 대출·미국 금리 줄 뺌(질문 하나: 예금)
# 11/10 1차 이해 3/3: '한 달로 7만원'·'5년 전 1.3%·111만원' 흐름 끊음 → 4줄 뺌 · 제목 '더 받는다'가 자동 적용으로 들림(1/3) → '다시 맡기면' · 3.8초 '새로 받은' 2/3 → 칸 '새로 맺은 예금 평균' · 할 일 막연 3/3 → 칸 '그날 금리 확인'
# 11/10 2차 이해 3/3·할 일 3/3·권유 0: '세후' 말 없음 2/3 → '세금 떼고' · 0초 '한국은행 9월 평균' 1/3 → '은행 평균 금리' · 87만원이 내 돈인지 1/3 → '평균으로 셈하면' · 제목 '더'가 권유로 1/3 → '늘었다'
# 11/10 3차 뜻 3/3·할 일 3/3: 87만원이 '이미 든 내 예금'에 붙는 걸로 2/3 · '다시 계산' 뜻 2/3 → 칸 '작년에 새로 맡겼다면/올해 새로 맡기면'·'만기 뒤 다시 맡길 때'(말은 그대로) → 4차
# 11/10 꼴 관문 ⓐ 첫 줄 35자 넘음('먼저, 정기예금 1억원이…' 37자·'먼저'로 시작) → 그 줄 빼고 '1년짜리 정기예금 평균을…'(35자·숫자)로 시작, '한국은행은…' 설명 줄을 금리 뒤로 → 4차
# 11/10 4차 뜻 3/3·할 일 3/3: '다음 달 만기인 1억원이면요'(말)가 87만원을 '이미 든 내 예금' 돈으로 들리게 함 3/3 → 그 줄 뺌, 0초 질문·제목에 '새로 맡기면' → 5차
# 11/10 안전 영역 18초: 계산기 클립 자판·화면 숫자(78)가 글자로 잡힘 → 배경 5·6번째를 coffee_cloudy 1·cup_stir 8로
# 화면 숫자 = calc5_out.txt '2. 1억·2억 1년 정기예금 세후(15.4%)' 202109 1.31%·111만 / 202509 2.54%·215만 / 202609 3.57%·302만 / 차 87만(월 7.3만)
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
    sc('금리', ['1년짜리 정기예금 평균을', '작년엔 2.5%', '올해는 3.6%', '한국은행은 은행들이 그달 새로'],
       {'tiles': [['1년 정기예금', '작년 vs 올해 9월', '', 0, 'ink'], ['작년 9월', '2.5%', '', 119, 'ink'], ['올해 9월', '3.6%', '', 182, 'ink'], ['은행 평균 금리', '새로 맺은 예금 평균', '', 241, 'ink']]}),
    sc('이자', ['작년 금리라면, 세금 떼고', '지금 금리면 302만원', '차이가 87만원'],
       {'tiles': [['작년에 새로 맡겼다면', '세금 떼고 215만원', '', 0, 'ink'], ['올해 새로 맡기면', '세금 떼고 302만원', '', 130, 'ink'], ['평균으로 셈하면', '87만원 차이', '', 194, 'ink']]}),
    sc('할 일', ['예금이라면 만기 날'],
       {'tiles': [['만기 뒤 다시 맡길 때', '그날 금리 확인', '', 0, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
    assert len({t[3] for t in s_['data']['tiles']}) == len(s_['data']['tiles']), ('같은 프레임 두 칸 — live는 뒤 칸만 보임', s_['label'])
for x in ('202509 2.54% 1억 2,148,840원', '202609 3.57% 1억 3,020,220원', '차: 1억 871,380원(월 72,615)'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0]) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: K-1 공개본에 쓴 Pexels 클립 — 말 줄마다 하나, 같은 클립 다시 쓰면 다른 구간
BG = [('notepad_calc', 2), ('cup_stir', 1), ('money_pen', 1), ('news_cup', 0), ('coffee_cloudy', 1),
      ('cup_stir', 8), ('money_pen', 9), ('rain_window', 40)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for k, ((name, st), l) in enumerate(zip(BG, allines)):
    fr = l['frames'] + (TAIL if k == len(BG) - 1 else 0)
    src = os.path.join(VID, 'public', 'bg', 'k1', 'stock', name + '.mp4'); assert os.path.exists(src), name
    assert SEC[name] - st >= fr / 30 + 0.3, (name, SEC[name], st, fr / 30)
    cut = f'bg/k1/stock/cut/{name}_{st}_d.mp4'
    cp = os.path.join(VID, 'public', cut)
    if not os.path.exists(cp):
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', str(st), '-i', src, '-t', f'{fr / 30 + 0.5:.2f}', '-an', '-c:v', 'libx264', '-g', '10', '-crf', '18', '-pix_fmt', 'yuv420p', cp], check=True)
    bg.append({'src': cut, 'from': at, 'frames': fr, 'start': 0}); at += fr
credits = ' · '.join(sorted({CR[STOCK[nm]]['author'].strip() for nm, _ in BG}))
p = {'fps': 30, 'name': 'k1s_dep', 'v': 1, 'look': 'live', 'question': ['은행 평균 금리 · 1년 정기예금', '1억 새로 맡기면, 이자 얼마 늘까?'], 'hot': '1억',
     'answer': {'label': '1억·1년 정기예금 세금 떼고 받는 이자(은행 평균)', 'items': ['작년 9월 2.5%: 215만원', '올해 9월 3.6%: 302만원'], 'arrow': False, 'note': '새로 맡길 때 기준 · 내 금리는 은행마다 달라요'},
     'base': '한국은행 예금은행 신규취급 정기예금(1년) 평균 금리 2025·2026년 9월분 · 이자소득세 15.4% · 파이어맵 계산', 'long': 'H9Lv281MaLs',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'k1s_dep.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'k1s_dep: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
