# de1s_kofin — D-ETF-1 롱폼 3장(3:7·3:8·3:9·3:14, 국내 고배당 ETF 금융 쏠림)을 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-20, de1s_divo/de1sclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_kofin/de1kclip.py   → work/video/de1s_kofin.json
# 목소리 = D-ETF-1 voice.json 문장 wav를 쉼(silencedetect -40dB)에서 자른 것(새 녹음 0): 3:7 → 5.37초에서 둘 · 3:8 앞 '보면 바로 이해가 돼요'(곁가지) 빼고 3.30초부터 · 3:9 앞 지식인 두 문장 빼고 5.50초부터 · 3:14 앞 '조심할 곳도 있어요.' 빼고 1.33초부터
# 화면 숫자 = 올리기 전 확인(prepub_1120.txt, 네이버 증권 ETF 분석 기준일 11/19): PLUS 금융 55.6% · TIGER 은행 99.2% · SOL 56.4%
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = open(os.path.join(HERE, 'prepub_1120.txt'), encoding='utf-8').read()
CRED = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'detf', 'stock', 'credits.json'), encoding='utf-8'))}
TAIL = 36
# 11/20 이해 2차(46·57·66세) 뜻·% 뜻·할 일 3/3·권유 0/3 · 걸림: TIGER는 이름이 은행이라 99%가 당연·부풀린 느낌 2/3 → 값 '이름대로 99.2%가 금융' · '지주' 2/3 → '금융지주'
# 11/20 이해 1차(43·54·63세) 뜻·할 일 3/3·권유 0/3 · 걸림(화면만 고침): SOL이 말에 없음 3/3 → 칸 머리 'SOL 코리아고배당도' · '%가 무엇의 몇 %' 3/3 → '담은 돈의 ○% 금융' · '칸' 3/3 → 칸 '금융 비중이 더 커짐' · '맨 위 셋' 뜻 2/3 → '많이 담은 셋' · 장바구니 배경 1/3 → 휴대폰 주식 화면
A = 'audio/de1s_kofin/'
# 꼴 관문 ⓐ(첫 줄 숫자·35자): 3:7 앞 '국내 고배당 ETF는 더 한쪽으로 쏠려 있어요.'(숫자 없음·'더'는 롱폼 앞 그림과 비교라 홀로 뜻 없음) 빼고, 뒤 문장 'TIGER…100%'를 첫 줄로 · 'PLUS…넘고,'(2.97~5.37초)는 3:8 뒤 문장과 이어 한 문장
# 11/20 이해 4차(44·55·64세) 뜻·% 뜻 3/3·권유 0/3 · 걸림: 은행 ETF 99%는 당연한 숫자인데 나란히 놓으니 과장 3/3(셋째로 옮겨도) → **TIGER 줄 뺌**(고배당 일반 상품 둘만) · 질문 '돈은 어디에 몰렸을까'가 '투자금 몰림'으로도 읽힘 2/3 → '담은 돈은 어디에 있을까' · 진열대 배경 2/3 → 계산하며 적는 손
# 11/20 이해 3차(41·52·62세) 3/3 'TIGER는 이름부터 은행이라 99%가 당연, 맨 앞에 두니 과장' → 첫 줄을 새 녹음 1줄 'PLUS 고배당주는 담은 돈의 55% 넘게가 금융이에요.'(D-ETF-1 tts.json 같은 설정 Chirp 3 HD Charon·1.1·markup, 3번 받아 k0_2 — f0 138.7Hz, 받아쓰기 gemini-3.8-flash 글자 그대로, 앞 무음 0.41초 중 0.30초 잘라 k0.wav)로 바꾸고, TIGER 줄은 '은행만 담는 상품'으로 셋째에 · 3:7 앞 'PLUS…넘고,'(k7a2)는 뺌
SPLIT = {'NEW@': [('PLUS 고배당주는 담은 돈의 55% 넘게가 금융이에요.', A + 'k0.wav', 118)],
         'TIGER@': [('TIGER 은행고배당플러스는 거의 100%가 금융입니다.', A + 'k7b.wav', 96)],
         'PLUS 고배당주에 많이 담긴': [('맨 위 세 종목이 DB손해보험, 기업은행, 우리금융지주예요.', A + 'k8b.wav', 106)],
         '지식인에도 국내 배당': [('국내 고배당은 이름이 달라도 금융이 중심이었습니다.', A + 'k9b.wav', 95)],
         '조심할 곳도 있어요. 이미 은행주': [('이미 은행주를 가진 분이 국내 고배당 ETF를 더 담으면, 금융 칸이 더 쌓입니다.', A + 'k14b.wav', 149)]}
n = 0


def Ls(t):
    global n
    key = '국내 고배당 ETF는 더 한쪽으로' if t.endswith('@') else t
    hit = [k for k in BYTEXT if k.startswith(key)]; assert len(hit) == 1, (t, hit)
    if t == 'NEW@': hit = [SPLIT[t][0][0]]   # 새 녹음 줄 — 롱폼 원문 대조 대신 받아쓰기(stt.log)
    out = []
    for txt, au, fr in SPLIT[t]:
        assert txt.rstrip(',.') in hit[0] or txt in hit[0], (txt, hit[0])
        assert os.path.exists(os.path.join(VID, 'public', au)), au
        n += 1; out.append({'n': n, 'text': txt, 'audio': au, 'frames': fr})
    return out


def sc(label, lines, data):
    ls = [x for t in lines for x in Ls(t)]
    spoken = ' '.join(l['text'] for l in ls)
    strs = []
    walk = lambda x: [walk(y) for y in x] if isinstance(x, list) else ([walk(y) for y in x.values()] if isinstance(x, dict) else (strs.append(x) if isinstance(x, str) else None))
    walk(data)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·올리기 전 확인에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


scenes = [
    sc('PLUS', ['NEW@', 'PLUS 고배당주에 많이 담긴'],
       {'tiles': [['PLUS 고배당주', '담은 돈의 55.6% 금융', '', 0, 'ink'], ['PLUS 많이 담은 셋', 'DB손보 · 기업은행 · 우리금융', '', 118, 'ink']]}),
    sc('SOL', ['지식인에도 국내 배당'],
       {'tiles': [['SOL 코리아고배당도', '담은 돈의 56.4% 금융', '', 0, 'ink']]}),
    sc('조심', ['조심할 곳도 있어요. 이미 은행주'],
       {'tiles': [['은행주 이미 있다면', '금융 비중이 더 커짐', '', 0, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('금융 55.57', '금융 56.40', '기준일 2026.11.19'): assert x in SRC, f'원문에 없음 {x}'
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경(B-56 그 줄의 대상): 1줄 'PLUS 금융 55%' 휴대폰 주식 화면(11/20 이해 1차: 장바구니 뜻 모름 1/3) · 2줄 '종목' 휴대폰 주식 화면 · 3줄 '이름 달라도' 진열대 · 4줄 '은행 거의 100%' 동전 · 5줄 '금융 칸이 더 쌓임' 동전 쌓기 — 모두 de1s 앞 편 눈 검사 통과 클립
BG = [(1, '7118320', 0), (2, '5546876', 1), (3, '6964247', 0.5), (4, '8661806', 2)]   # 11/20 렌더 3판 safezone 걸림: 휴대폰 주식 화면(39494572·7578628) 속 글자 13상자 + 남의 차트 → 동전 만지는 손·공책에 적는 손(앞 편 통과 클립)
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    src = f'bg/detf/stock/{cid}.mp4'
    if cid == '39494572': src, st = 'bg/detf/stock/cut/39494572_1.mp4', st - 1   # 11/20 렌더 3판: 원본 'No frame found at position 31147'(43프레임) → 1초부터 5.5초만 잘라 GOP 10(앞 편 cut/ 수법)
    bg.append({'src': src, 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_kofin', 'v': 2, 'look': 'live', 'question': ['국내 고배당 ETF', '담은 돈은 어디에 있을까'], 'hot': '어디에 있을까',
     'answer': {'label': '담은 돈 중 금융주(은행·보험·금융지주)', 'items': ['PLUS 고배당주 55.6%', 'SOL 코리아고배당 56.4%'], 'arrow': False, 'note': 'SOL 코리아고배당 56.4%'},
     'base': '네이버 증권 ETF 분석(2026-11-19 기준) · 파이어맵 정리', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_kofin.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_kofin: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
