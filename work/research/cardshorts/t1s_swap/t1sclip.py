# t1s_swap — T-1 롱폼 3장 '집을 갈아타는 분들'(일시적 2주택 2년 기한)을 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live', 10/19 클로드 티 금지) (firemap-video-producer 2026-10-20)
#   py -3.12 work/research/cardshorts/t1s_swap/t1sclip.py   → work/video/t1s_swap.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/t1s_swap.mp4 --props=t1s_swap.json
# 목소리 = T-1 voice.json 문장 wav 그대로(새 녹음 0) · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# 숫자 = 그 장면 말 줄 또는 T-1 research.md·calc 출력에 있는 글자만 · 배경 = ep/T-1/stock/credits.json Pexels 클립(video/public/bg/t1)
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'T-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_more_out.txt', 'calc_out.txt') if os.path.exists(os.path.join(EP, f)))
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
    walk(data)   # 글자 칸만(줄 위치 숫자 0.6·1.4 같은 배치 값은 뺌)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·T-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 10/20 02:5x: 첫 줄은 꼴 관문 ⓐ(숫자 있음·35자 이하) — 옛 첫 줄 5:2 '대신 지난 기록에서…'(45자·숫자 없음)·5:5 '다음은…' 뺌, 끝에 계산 한계 5:26
# 박자 at = 장면 안 프레임(숫자 든 값은 말에 맞춰 parts/safeframe beatsOf가 다시 잡음) · 꼬리말(kicker) 12자 이하만 보임
# 10/20 03:0x 이해 시험 1차(40·50·60세) 셋 다 '정우 씨가 S&P500 쪽인지'·'2003년 반대가 뭔지'·'민수 씨가 누군지' 헷갈림 → 꼬리말로 풂
# 4~15초 줄 규칙(10/20 벤치마크 지시): 둘째 줄 3:8 = 답 숫자(2년), 셋째 줄 3:12 = 답의 이유 · 방법·가정 줄 없음
# 10/20 13시 안전 영역: 계산기 클립 6963487 버튼 글자(M+ M-)가 OCR로 오른쪽 버튼 줄에 걸림 → 이삿짐 4553301
# 10/20 12:4x 이해 시험 1차(40·50·60세 3/3 뜻 맞음) 반영: 셋 다 물은 '하나만 조정이면?' → 3:10 넣음, 3:28 뺌(길이) · 화면 '예전 규칙 3년'·'산 지 2년 넘어'·'8억에 산 20억 집'·'새 집을 8월 3일까지'
# 첫 줄 3:7 '새 집을 산 날부터 3년 안에…' 27자·숫자(꼴 관문 ⓐ) · 정부안 아닌 이미 시행된 규칙(시행령 §155①, 2026.9.30)이라 '국회 통과 전' 배지 안 씀
scenes = [
    sc('헌 집 파는 기한', ['새 집을 산 날부터 3년 안에', '바뀐 건 기한이에요.'],
       {'tiles': [['예전 규칙', '3년', '', 0, 'ink'], ['지금, 둘 다 조정대상지역', '2년', '', 170, 'ink']], 'side': ['1년 짧아짐', 250, '헌 집 파는 기한']}),
    sc('하나만 조정대상지역이면', ['둘 중 하나라도 조정대상지역이'],
       {'tiles': [['하나라도 아니면', '3년 그대로', '', 0, 'ink']]}),
    sc('왜 줄였나', ['조정지역에서 두 채를 갖게 된'],
       {'tiles': [['두 채인데 한 채 취급', '3년', '', 0, 'ink'], ['정부가 든 이유', '혜택이 너무 큼', '', 95, 'ink']]}),
    sc('서울은', ['서울은 작년 10월에'],
       {'tiles': [['서울', '25개 구 전체', '', 0, 'ink']], 'side': ['조정대상지역', 70, '작년 10월 지정']}),
    sc('기한을 넘기면', ['그런데 2년 기한을 넘겨', '그러면 세금이 7억'],
       {'tiles': [['산 지 2년 넘어 팔면', '두 채 세금', '', 0, 'ink'], ['8억에 산 20억 집', '7억 8천만원쯤', '', 205, 'ink']], 'side': ['5배 넘게', 300, '한 채일 때보다']}),
    sc('예전 규칙 그대로인 사람', ['정부가 세법 개정안을 발표한', '그때는 예전대로 3년'],
       {'tiles': [['새 집을 8월 3일까지', '샀거나 계약금', '', 0, 'ink'], ['그러면', '예전대로 3년', '', 190, 'ink']]}),
    sc('적어 둘 날짜 세 개', ['헌 집을 산 날, 새 집을 산 날'],
       {'tiles': [['날짜 하나', '헌 집 산 날', '', 100, 'ink'], ['날짜 둘', '새 집 산 날', '', 150, 'ink']], 'side': ['2년 되는 날', 215, '새 집 산 날부터']}),
]
need = ['78,368', '5.3배', '2년', '8/3']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나(분위기용 금지) — (줄 번호, 클립, 시작 초)
BG = [(1, '8478946', 2), (2, '1793371', 1), (3, '6221101', 1), (4, '35082942', 0), (5, '31251627', 1), (6, '4553292', 2),
      (7, '4553301', 0), (8, '8471105', 3), (9, '31400388', 2), (10, '7710453', 2)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 't1', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/t1/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 't1s_swap', 'v': 2, 'look': 'live', 'question': ['집 갈아타는 중이라면', '헌 집 파는 기한은?'], 'hot': '기한',
     'answer': {'label': '헌 집·새 집 둘 다 조정대상지역', 'items': ['원래 3년', '지금 2년'], 'arrow': False, 'note': '넘기면 세금 5배 넘게 (20억 집 예)'},
     'base': '소득세법 시행령 §155① (2026.10.1 양도분부터) · 재정경제부 2026.8.3 문답 · 가상 인물 20억 집 계산', 'long': 'Qg5Tj2fuJ3A',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 't1s_swap.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f't1s_swap: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
