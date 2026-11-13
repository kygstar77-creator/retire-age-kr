# de1s_basket — D-ETF-1 롱폼 3장(3:4·3:12·3:13)을 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-13, de1s_schdgrow/de1sclip.py 사본 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_basket/de1bclip.py   → work/video/de1s_basket.json
# 목소리 = D-ETF-1 voice.json wav(3:4·3:12) + 3:13 앞 '예를 들어'(0~0.52초, 에너지 골) 잘라낸 basket.wav + 새 녹음 2줄(Charon 1.1, 쉼 태그 pause_v 2 같은 설정)
#   새 줄을 받은 이유: ① 꼴 ⓐ 첫 줄 35자 이하·질문(롱폼 0:1은 49자) ② 롱폼 0:3 '55%'는 10/15 SCHD 보유 기준 — 11/13 네이버 다시 받은 국내 4종 세 업종 합이 53.4% 안팎이라 '절반 넘게'로 말함(올리기 전 확인, raw/etf_*.json)
#   11/13 22:4x 꼴 ⓐ(첫 줄 37자·숫자 없음)에 걸려 첫 줄을 q2 'SCHD랑 미국배당다우존스, 2개 담으면 나눠 담은 걸까요?'(33자)로 다시 받음 — 3번 받아 f0가 롱폼(약 136Hz)에 가장 가까운 것(125.7Hz) 고름
#   받아쓰기(11/13 gemini-3-flash-preview): q2 'SCHD랑 미국 배당 다우존스 2개 담으면 나눠 담은 걸까요?' · half1 '생활용품 제약 석유 이 세 업종에 돈이 절반 넘게 들어 있어요.' · basket '슈드와 국내 미국 배당 다우존스를 같이 담으면…한 바구니인 셈이죠.'
#   f0 중앙(lfvoice.f0): q1 135.6 · half1 123.1 · basket 138.7 · 롱폼 3:4 137.9 · 3:12 131.1 · 0:1 136.0 Hz (±25% 안)
# 숫자: '2개' = SCHD 1 + 국내 미국배당다우존스 1(둘 다 담기) · calc_out 1절(10/16 SCHD 합산과 4종 0.2%p 안) · 11/13 네이버 4종 필수소비재 20.11~20.21·헬스케어 18.52~18.59·에너지 14.69~14.76
# 사라·팔라·전망 0
# 11/13 22:4x 눈 검사(sheet_1113.png): 장면2·3에서 같은 프레임 칸 두 개 중 뒤 칸만 보임('상품마다 담긴 돈'·'TIGER · SOL · ACE · KODEX' 빠짐) → half1(1.47초)·3:4 wav(5.11초, 쉼 4.96~5.27)를 나눠 칸마다 줄 시작에
# 이해 시험 1차(11/13 43·54·63세): 뜻 3/3·할 일(겹치는지 확인, 안 사고 안 팖) 3/3 · 헷갈림 '절반 넘게 — 무엇의' 3/3 → 칸 '두 상품 안의 돈 / 절반 넘게 세 업종에' · '큰 칸' 3/3 → 화면 '큰 업종' · 장면3 네 이름 정체 3/3 → '국내 상품 이름' 칸 · 장면1 숫자 없음 2/3 → '0.2%p 안' (화면만, 새 녹음 0)
# 이해 시험 2차(11/13 46·57·66세): 뜻 3/3·할 일(업종 구성 찾아봄, 안 사고 안 팖) 3/3·권유 0/3 → 통과 · 남은 멈칫 '%p' 3/3 → '%포인트' · '절반 — 합친 돈인지 각각인지' 3/3 → '상품마다 담긴 돈'(2차 뒤 글자 2곳, 3차 시험 안 함)
import os, re, json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
NEW = {'SCHD랑 미국배당다우존스, 2개 담으면 나눠 담은 걸까요?': ('audio/de1s_basket/q2.wav', 129),
       '생활용품, 제약, 석유.': ('audio/de1s_basket/half_a.wav', 45),
       '이 세 업종에 돈이 절반 넘게 들어 있어요.': ('audio/de1s_basket/half_b.wav', 105),
       'SCHD는 재무가 튼튼하고 배당을 꾸준히 준 미국 기업 100개를 고르는 지수를 따라가요.': ('audio/de1s_basket/index_a.wav', 154),
       '그렇게 고른 회사들이 이 세 업종에 많았던 거예요.': ('audio/de1s_basket/index_b.wav', 85),
       'SCHD와 국내 미국배당다우존스를 같이 담으면, 업종마다 비율이 거의 똑같거든요. 이름만 둘이지 한 바구니인 셈이죠.': ('audio/de1s_basket/basket.wav', 251)}
for t, (au, fr) in NEW.items(): BYTEXT[t] = {'text': t, 'audio': au, 'frames': fr}
TODAY = {}
for f in glob.glob(os.path.join(HERE, 'raw', 'etf_*.json')):
    d = json.load(open(f, encoding='utf-8')); TODAY[d['itemName']] = {x['detailTypeCode']: x['weight'] for x in d['sectorPortfolioList']}
assert len(TODAY) == 4, TODAY.keys()
three = [round(w['CONSUMER_STAPLES'] + w['HEALTHCARE'] + w['ENERGY'], 2) for w in TODAY.values()]
assert all(50 < x < 55 for x in three), three          # '절반 넘게' 근거(11/13)
assert max(w['CONSUMER_STAPLES'] for w in TODAY.values()) - min(w['CONSUMER_STAPLES'] for w in TODAY.values()) <= 0.2
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
SRC += json.dumps(TODAY, ensure_ascii=False)
CRED = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'detf', 'stock', 'credits.json'), encoding='utf-8'))}
TAIL = 36
n = 0


def L(t):
    global n
    hit = [t] if t in BYTEXT else [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)   # 11/13: 나눈 줄은 글 전체가 같으면 그것
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·D-ETF-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('같이 담으면', ['SCHD랑 미국배당', 'SCHD와 국내 미국배당다우존스를 같이'],
       {'tiles': [['SCHD + 국내 상품', '둘 다 담으면?', '', 0, 'ink'], ['업종마다 비율', '차이 0.2%포인트 안', '', 129, 'ink']]}),
    sc('세 업종', ['생활용품, 제약, 석유.', '이 세 업종에 돈이'],
       {'tiles': [['세 업종', '생활용품 · 제약 · 석유', '', 0, 'ink'], ['상품마다 담긴 돈', '절반 넘게 세 업종에', '', 45, 'ink']]}),
    sc('같은 지수', ['SCHD는 재무가 튼튼하고 배당을 꾸준히 준 미국 기업 100개를 고르는 지수를 따라가요.', '그렇게 고른 회사들이'],
       {'tiles': [['국내 상품 이름', 'TIGER · SOL · ACE · KODEX', '', 0, 'ink'], ['모두 SCHD와', '같은 지수를 따라감', '', 154, 'ink']]}),
    sc('같이 담을 땐', ['그래서 두 개를 같이 담을'],
       {'tiles': [['같이 담을 땐', '큰 업종이 겹치는지 먼저', '', 0, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
assert '0.2%p 안' in SRC and 'Dow Jones U.S. Dividend 100' in SRC
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: D-ETF-1 롱폼에 쓴 Pexels(credits.json) — 두 찻잔(둘 다 담으면) · 장바구니(한 바구니) · 동전 손 · 노트 쓰는 손 · 동전 쌓기
BG = [(1, '6343634', 2), (2, '4121749', 0.5), (3, '7118320', 0), (4, '7118320', 1.6), (5, '5546876', 1), (6, '5546876', 6.2), (7, '8661806', 2)]   # 11/13 눈 검사: 한 줄에 칸 두 개면 뒤 칸만 보임 → 3:4·half 줄을 문장 끝 쉼에서 나눔(받아쓰기 확인), 배경은 같은 클립 이어서
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/detf/stock/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_basket', 'v': 2, 'look': 'live', 'question': ['SCHD + 국내 미국배당다우존스', '둘 다 담으면 나눠 담은 걸까'], 'hot': '나눠 담은 걸까',
     'answer': {'label': '업종 비중', 'items': ['거의 똑같다', '한 바구니'], 'arrow': False, 'note': '한 바구니'},
     'base': '슈왑 보유 종목(10/15) · 네이버 증권 ETF 분석(11/13) · 파이어맵 계산', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_basket.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_basket: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('세 업종 합(11/13):', three)
print('credits:', credits)
