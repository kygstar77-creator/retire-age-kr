# j1s_cliff — J-1 롱폼 5장 '안 사는 집 14억 문턱'을 자른 세로 쇼츠 props · c1clip 틀(C1S live, E-18 통과 틀) (firemap-video-producer 2026-11-04, de1s_jepqhealth/de1qclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/j1s_cliff/j1cclip.py   → work/video/j1s_cliff.json
# 11/4 꼴 관문 ⓐ '그래서'로 시작 → 첫 줄을 '14억 선을 조금이라도 넘으면…'(접속사 없음)으로, '14억까지 없음' 줄은 그 말과 겹쳐 뺌 · ⓒ 의안번호 7자리가 원 값으로 잡혀 출처 줄에서 뺌(설명란에 둠)
# 11/4 이해 1차(40·50·60): 뜻·할 일 3/3·사라/팔라 0 · 12억↔14억 3/3 멈칫 → 칸 '공제(빼 주는 금액)', '14억 위가 아니라 / 12억 위 전부' 칸 더함 · '안 사는 집'이 뭔지 늦게 나옴 → 0초 질문 '세 준 집·빈집' · '국회 통과 전' 작음 3/3 → 답 칸 이름·설명란 첫 줄 · 10년 산 집 왜 0원 2/3 → 설명란
# 11/4 이해 2차(43·55·64): 뜻(12억 위 전부)·할 일 3/3·사라/팔라 0 · 남은 궁금증 '14억 아래면 정말 0원?' 2/3(핵심) → 롱폼 줄 '14억까지 살든 안 살든 종부세가 없습니다'를 다시 넣음(밤 아파트 18029861) · 내 나이·지분·자녀 집은 설명란·롱폼으로
# 목소리 = J-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 답 5초 안(A-49): '14억을 겨우 넘겨도 → 50만원 이상'을 맨 앞으로
# 화면 숫자 = calc_out.txt [비거주 문턱] 14.01억 비거주 54.0 · 10년 거주 0.2(만원)
import os, re, json, sys, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'J-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
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
    sc('안 사는 집', ['14억 선을 조금이라도', '그래서 살지 않는 집은 공시가격이 14억을', '종부세가 50만원 이상', '10년째 살고 있는 집이라면'],
       {'tiles': [['안 사는 집', '54만원', '', 0, 'ink'], ['10년 산 집', '거의 0원', '', 255, 'ink']]}),
    sc('14억까지', ['그래서 정부안대로면 내년부터는 14억까지'],
       {'tiles': [['14억까지는', '종부세 없음', '', 0, 'ink']]}),
    sc('기준이 둘', ['비어 있거나 세를 준 집에는', '그런데 종부세를 내는 사람인지'],
       {'tiles': [['공제 = 빼 주는 금액', '12억', '', 0, 'ink'], ['내는 사람 기준', '14억', '', 134, 'ink']]}),
    sc('넘으면', ['공제는 12억이라', '내는 사람을 가르는 기준과'],
       {'tiles': [['14억 넘는 순간', '세금 붙는 건', '', 0, 'ink'], ['14억 위가 아니라', '12억 위 전부', '', 138, 'ink']]}),
    sc('할 일', ['그래서 살지 않는 집이 14억 근처라면', '공시가격은 매년 바뀌니까'],
       {'tiles': [['14억 근처라면', '공시가격 확인', '', 0, 'ink'], ['공시가격은', '매년 바뀜', '', 149, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('공시 14.01억: 비거주 54.0 · 10년 거주 0.2', '공시 14.0억: 비거주 0.0'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: J-1 롱폼에 쓴(눈 검사 통과) Pexels 클립 — 얼굴·상표·글자 없는 것만(7247869 'tax fraud' 글자 보여 뺌) · 말 줄마다 하나
# 11/4 눈 검사: '공제(빼 주는 금액)' 괄호가 지워져 '공제'만 보임(shortKick) → '공제 = 빼 주는 금액'
# 11/4 밝기(B-46): 11~19초 Y 19~25(밤 아파트 18029861·짐 상자 4553292) → 30975009@40·38029457@8
# 11/4 safezone: 7710745(영수증 숫자 글자가 아래 왼쪽에 OCR로 잡힘·눈에도 숫자) → 8293019
BG = [(1, '30975009', 10), (2, '38029457', 1), (3, '11099870', 2), (4, '9902446', 2), (5, '30975009', 40), (6, '38029457', 8), (7, '5923592', 1), (8, '8293019', 1), (9, '12079562', 4), (10, '7308166', 1), (11, '35757634', 2)]   # 11/4 렌더: 12079562_18 끝 토막 1.2초에서 No frame found 4번 → 35757634(겨울 노을 시내)
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
p = {'fps': 30, 'name': 'j1s_cliff', 'v': 1, 'look': 'live', 'question': ['세 준 집·빈집, 공시가격', '14억 조금 넘으면?'], 'hot': '14억',
     'answer': {'label': '정부안(국회 통과 전) 2028년', 'items': ['안 사는 집 54만원', '10년 산 집 거의 0원'], 'arrow': False, 'note': '안 사는 집 54만원'},
     'base': '종합부동산세법 개정안(정부안 · 국회 통과 전) · 공시 14억 100만원·55세·보유 10년 가정 · 파이어맵 계산', 'long': 'NNcjTE0L7yg',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'j1s_cliff.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'j1s_cliff: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
