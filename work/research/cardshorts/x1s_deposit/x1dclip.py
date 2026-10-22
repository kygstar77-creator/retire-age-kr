# x1s_deposit — X-1 롱폼 4장 '달러 예금도 원화로는 마이너스'를 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live') (firemap-video-producer 2026-10-22, x1s_hedge/x1hclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/x1s_deposit/x1dclip.py   → work/video/x1s_deposit.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/x1s_deposit.mp4 --props=x1s_deposit.json --concurrency=2
# 목소리 = X-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# say_v3 117~124(원화로 따지면 마이너스 · KB 3.6% 조금 넘 · 세후 3%쯤 · 3%쯤만 내려도 이자 사라짐 · 1,298원) + 126~129(예금자보호 외화예금 1억, 원화 환산·이자 합산)
# spec(x1_specs/spec.md) 주의: '지금' = 10/15 환율(1,338.6원) — 화면에 날짜를 박는다 · 금리는 조회기준일 표시 · 사고팔 시기 권유 0
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'X-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
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


# 첫 줄 = 117 '원화로 따지면, 네. 마이너스가 될 수 있습니다.'(답) → 118(왜: 바꾸는 날 환율) · 0초 화면 답 '환율 3%쯤만 내려도 이자가 사라진다'(날짜에 안 묶이는 값 — 1,298원은 10/15 환율 기준이라 장면 3에서 날짜와 같이)
# 이해 시험 1차(10/22 40·50·60세) 뒤 화면만 고침: 3%가 이자인지 환율인지 → '1년 뒤 환율이' · 장면3 '이 아래' 순서 → '1,298원 아래면 마이너스' · 예금자보호가 환율 손실도 막는 줄 → '은행이 문을 닫을 때 / 돌려주는 돈의 한도'
# 이해 시험 2차 뒤: 3.64833% → '연 3.6%대'(작은 화면에서 못 읽음, 정확한 값은 설명란) · '손에 남는 이자 3%쯤'(이자 3%와 환율 3% 구분) · '지금 = 2026년 10월 15일 환율' · '문을 닫을 때만'(환율 손실까지 막는 줄 오해)
# 4~15초 줄: 118(답의 이유) · 119·120(KB 금리 = 둘째 숫자) — 목차 예고·방법 줄 0
scenes = [
    sc('마이너스?', ['원화로 따지면, 네.', '달러 상품은 이자가 달러로'],
       {'tiles': [['1년 뒤 환율이 3%쯤 내리면', '이자가 사라진다', '', 0, 'ink'], ['이자는', '달러로 붙고', '', 104, 'ink'], ['원화로 바꾸는 날', '그날 환율', '', 180, 'ink']]}),
    sc('달러 1년 예금', ['은행 달러 예금으로 계산해', 'KB국민은행 고시를 보면', '이자에는 세금 15.4%가'],
       {'tiles': [['KB국민은행 달러 1년', '연 3.6%대', '', 80, 'ink'], ['이자 세금 15.4% 떼면', '손에 남는 이자 3%쯤', '', 264, 'ink']],
        'side': ['조회기준일 2026.10.16', 80, 'KB 금리']}),
    sc('1년 뒤 환율', ['지금 1억 원을 달러로', '1년 뒤 환율이 지금보다', '1,298원 아래로 내려가면'],
       {'tiles': [['지금 = 2026년 10월 15일 환율', '1,338.6원', '', 0, 'ink'], ['1년 뒤 환율', '1,298원 아래면 마이너스', '', 236, 'ink']]}),
    sc('예금자보호', ['은행 달러 예금이라면 예금자보호', '은행이 문을 닫아도', '예금보험공사는 외화예금도', '다만 원화로 바꿔서'],
       {'tiles': [['은행이 문을 닫을 때만', '돌려주는 돈의 한도', '', 103, 'ink'], ['예금보험공사 안내', '외화예금도 1억원까지', '', 224, 'ink'], ['원화로 바꿔 계산', '예금과 이자 합쳐 1억원', '', 366, 'ink']]}),
]
need = ['3.64833', '1,298.5', '1,338.6', '15.4%', '외화예금도 1억원까지']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나 — (줄 번호, 클립, 시작 초) · 계산기·달력은 안전 영역 걸림(x1s_hedge 1차) → 뺌
BG = [(1, '5466769', 0), (2, '6963836', 1), (3, '7735915', 1), (4, '34596756', 2), (5, '8661806', 2), (6, '5466779', 1), (7, '9806390', 4),
      (8, '7829075', 0), (9, '6326929', 2), (10, '8439245', 0), (11, '35054136', 1), (12, '34596756', 12)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'x1', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/x1/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'x1s_deposit', 'v': 2, 'look': 'live', 'question': ['달러 예금 이자 3%', '원화로는 마이너스 될까?'], 'hot': '마이너스',
     'answer': {'label': '달러 1년 예금, 세후 이자 3%쯤', 'items': ['1년 뒤 환율이 3%쯤 내리면', '이자가 사라진다'], 'arrow': False, 'note': '환율 3%쯤'},
     'base': 'KB국민은행 외화예금 금리(조회 2026.10.16) · 한국은행 환율 · 예금보험공사 · 파이어맵 계산', 'long': 'WcBOePkyOOQ',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'x1s_deposit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'x1s_deposit: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
