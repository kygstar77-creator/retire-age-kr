# x1s_hedge — X-1 롱폼 2장 'S&P500 ETF 환노출 vs H형'을 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live') (firemap-video-producer 2026-10-21, t1s_live/t1lclip.py 복사 — 편·줄·배경만)
#   py -3.12 work/research/cardshorts/x1s_hedge/x1hclip.py   → work/video/x1s_hedge.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/x1s_hedge.mp4 --props=x1s_hedge.json --concurrency=2
# 목소리 = X-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# 숫자 = 그 장면 말 줄 또는 X-1 research.md·calc_out.txt·facts.txt(만원 반올림 꼴 포함)에 있는 글자만 · 배경 = ep/X-1/stock/credits.json Pexels 클립(video/public/bg/x1)
# spec(x1_specs/spec.md) 주의: 'H형이 낫다'로 끝내지 않는다 — say_v3 73(이익도 같이 막음)·75~77(어떤 돈으로 쓸 거냐)까지
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'X-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))


def man(v):   # w1g1clips_check.man 과 같은 꼴: 89,583,254 → 8,958만원 · 103,805,193 → 1억 381만원
    m = round(abs(v) / 10000)
    if m >= 10000: e, r = divmod(m, 10000); return f'{e}억' + (f' {r:,}만원' if r else '원')
    return f'{m:,}만원'


SRC += '\n' + ' '.join(man(int(x.replace(',', ''))) for x in re.findall(r'\d{1,3}(?:,\d{3}){2,}(?=원)', SRC))
CRED = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·X-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 첫 줄 = say_v3 64 '차이가 1,400만원을 넘습니다.'(16자·숫자, 꼴 관문 ⓐ) → 62·63(그 차이가 어떻게) · 0초 화면 답 '1,400만원 넘게'
# 4~15초 줄: 62(환노출 9천만원 조금 안 됨)·63(H형 1억 넘음) = 답의 숫자 근거 · 58 = 두 종류가 무엇인지
# 뒤집힌 경우 68·69·70·72 + 73(이익도 같이 막음) + 기준 75·76·77(원화로 쓸 돈 / 달러로 쓸 돈) — 사고팔 시기 권유 0
scenes = [
    sc('1억이 갈렸다', ['차이가 1,400만원을 넘', '달러가 제일 비쌌던 날 1억을', 'H형은 오히려 1억을'],
       {'tiles': [['7월 2일 1억, 차이', '1,422만원', '', 0, 'ink'], ['10월 16일 환노출형', '8,958만원', '', 136, 'ink'], ['10월 16일 H형', '1억 381만원', '', 210, 'ink']],
        'side': ['2026년 7월 2일 1,554원', 66, '달러 제일 비쌌던 날']}),
    sc('이름 끝 H', ['환율 움직임을 그대로 맞는'],
       {'tiles': [['같은 회사 두 상품', '환노출형 · H형', '', 0, 'ink'], ['환노출형', '환율 그대로', '', 45, 'ink'], ['이름 끝 H', '환율을 막은 환헤지형', '', 95, 'ink']]}),
    sc('뒤집힌 날', ['그럼 H형이 늘 나을까요?', '재작년 첫날 넣었다면', '그때 환율은 1,289원', '그 뒤 달러 값이 크게', '이 경우엔 환노출형이'],
       {'tiles': [['2024년 1월 2일', '환율 1,289원', '', 67, 'ink'], ['10월 15일 환율', '1,338.6원', '', 272, 'ink']],
        'side': ['1,500만원 넘게 더', 405, '이번엔 환노출형이']}),
    sc('막으면', ['환율을 막아 두면'],
       {'tiles': [['달러값(환율) 내릴 때', '환율 손실도 막고', '', 0, 'ink'], ['달러값(환율) 오를 때', '환율 이익도 막는다', '', 80, 'ink']]}),
    sc('고르는 기준', ['기준은 이 돈을 결국', '몇 년 안에 원화로', '나중에 달러로 쓸 돈이라면'],
       {'tiles': [['원화로 꺼내 쓸 돈', '흔들림 줄이는 H형', '', 88, 'ink'], ['나중에 달러로 쓸 돈', '원화 값 덜 중요', '', 288, 'ink']], 'side': ['어떤 돈으로 쓸 거냐', 0, '기준은']}),
]
need = ['89,583,254', '103,805,193', '14,221,939', '175,678,252', '160,354,815', '15,323,437', '1,289.4', '2026-07-02', '2024-01-02']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나 — (줄 번호, 클립, 시작 초)
BG = [(1, '5466769', 0), (2, '6326929', 1), (3, '5466779', 1), (4, '6963836', 2), (5, '7829075', 1), (6, '6186015', 2), (7, '8369980', 2),
      (8, '29904000', 3), (9, '34596756', 3), (10, '9806390', 4), (11, '5923592', 1), (12, '34596756', 12), (13, '7308237', 2)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'x1', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/x1/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'x1s_hedge', 'v': 2, 'look': 'live', 'question': ['같은 회사 S&P500 ETF 두 개', '이름 끝 H 하나로 왜 갈리나?'], 'hot': 'H',
     'answer': {'label': '달러 제일 비쌌던 날 1억', 'items': ['환노출형 8,958만원', 'H형 1억 381만원'], 'arrow': False, 'note': '차이 1,400만원 넘게'},
     'base': 'KRX 종가·분배금(2026-10-16) · 한국은행 환율 · 파이어맵 계산', 'long': 'WcBOePkyOOQ',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'x1s_hedge.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'x1s_hedge: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
