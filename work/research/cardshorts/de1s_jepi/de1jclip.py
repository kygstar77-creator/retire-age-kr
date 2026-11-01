# de1s_jepi — D-ETF-1 롱폼 4장 '주가까지 합치면'을 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live') (firemap-video-producer 2026-10-29, x1s_deposit/x1dclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_jepi/de1jclip.py   → work/video/de1s_jepi.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/de1s_jepi.mp4 --props=de1s_jepi.json --concurrency=3
# 목소리 = D-ETF-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# voice 4:3(JEPI 8%) → 4:2(흔한 말) → 4:0·4:1(배당 재투자 5년) → 4:4~4:8(7.5% · S&P500 · SCHD · HDV · 기간) — 첫 줄을 숫자 줄로(꼴 ⓐ)
# 화면 숫자 = video/detf1.json(편집 통과한 롱폼 화면) 값만: 8% · 7.5% · 12.8% · 9.8% · 13.1% · 기간 2021-10~2026-10
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_out.txt', 'facts.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {str(c['id']): c for c in json.load(open(os.path.join(VID, 'public', 'bg', 'detf', 'stock', 'credits.json'), encoding='utf-8'))}
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·D-ETF-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 이해 시험 1차(10/29 40·50·60세): '그런데 7.5%도'가 좋은지 나쁜지 3/3 헷갈림 → 장면3 첫 칸 '8% 주는 JEPI, 배당 다시 넣어도 / 매년 7.5%만' ·
#   '두 기간' 10년 숫자 없음 3/3 → 장면4 둘째 칸 calc_out 10년 열(HDV 10.4 · S&P500 15.4 — 5년엔 HDV가 앞, 10년엔 뒤) · 0초 '총수익·매년' 멈칫 → '한 해 평균 불어난 비율'
# 이해 시험 2차(10/29): 6명 뜻 맞음 · 장면4 '총수익' 말 바뀜에 멈칫 2/3 → 'HDV 5년 · 한 해 평균' · '분배율' 뜻 모름 1/3 → '1년에 나눠 주는 돈(분배율)'
# 이해 시험 3차(10/29): 9명 뜻 맞음 · 장면4 HDV 13.1% 옆에 같은 5년 S&P500이 없어 앞 장면을 되짚음 3/3 → 5년·10년 두 칸을 같은 꼴(HDV · S&P500)로
# 11/2 PD(벤치마크 11/1 N2·A71·A72, 회의 c1clip): 답 7.5%를 19.5초→1.9초로 — A71 '많이들 이렇게 생각하시죠' 줄 뺌, 계산법·단서 줄(A72)은 답 뒤로. 말·숫자 새로 0(줄 순서만)
scenes = [
    sc('많이 주면 많이 벌까', ['JEPI는 지금 8%', '그런데 배당을 다시 넣어도'],
       {'tiles': [['JEPI가 1년에 나눠 주는 돈(분배율)', '8%', '', 0, 'ink'], ['8% 주는 JEPI, 배당 다시 넣어도', '매년 7.5%만', '', 58, 'ink']],
        'side': ['기간 2021-10~2026-10 · 달러', 58, '배당 다시 넣음']}),
    sc('주가까지 합치면', ['배당만 보면 반쪽', '받은 배당을 다시 넣었다고'],
       {'tiles': [['배당만 보면', '반쪽', '', 0, 'ink'], ['배당 다시 넣고 주가까지', '5년 동안 매년 얼마씩', '', 179, 'ink']]}),
    sc('5년 · 매년 평균', ['미국 큰 회사들을 담은', 'SCHD는 10% 정도로'],
       {'tiles': [['S&P500', '매년 12.8%', '', 0, 'ink'], ['SCHD', '매년 9.8%', '', 115, 'ink']],
        'side': ['기간 2021-10~2026-10 · 달러', 0, '배당 다시 넣음']}),
    sc('다 뒤처졌나', ['그렇다고 배당 ETF가', '기간을 어디서 자르느냐'],
       {'tiles': [['5년 · 한 해 평균', 'HDV 13.1% · S&P500 12.8%', '', 0, 'ink'], ['10년으로 늘리면 · 한 해 평균', 'HDV 10.4% · S&P500 15.4%', '', 230, 'ink']]}),
]
for s_ in scenes:   # 칸 시각 = 그 줄 시작 프레임(줄 순서 바꿔도 맞게 assert)
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('7.5', '12.8', '9.8', '13.1', '28.1/13.1/10.4', '16.8/12.8/15.4'): assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나 — (줄 번호, 클립, 시작 초) · 롱폼에서 쓴 Pexels 클립만(얼굴·상표 눈 확인은 롱폼 때)
# 11/1 PD: 안전 영역 관문 29프레임 — 7578628(앱 화면 글자)·7490451(계산기 자판)·38667523(tradingview 화면)·39494572('CFDs on Gold' 화면) 글자가 아래 672px·왼쪽 48px에 걸림 → 글자 없는 롱폼 클립으로(손·찻잔·빗창·창가 뒷모습)
# 11/1 PD 2차: 5366344 빗방울을 글자 찾기가 글자로 읽음(23·26초 아래 672px)·6639799 끝 장면 얼굴 보임 → 8060388(탁자 위 손·전화)·7592927(창가 화분 햇빛)
# 11/2 PD(벤치마크 11/1 B-46 밝기 Y≥52): 어두운 클립 27170160(Y 60)·34535507(16)·7592927(36)·8164676(46) 뺌 → 밝은 롱폼 클립(bright.py 원본 Y: 8661806 240·7118320 104·5981346 143·36408448 129(4318548은 렌더 중 1.03초 프레임 못 찾음 오류로 뺌)·8060388 143·6343634 149·4786522 109)
# 11/2 2차 렌더 실측(초당 Y, LiveDim 뒤): 36408448 48~55·4786522 34~50 → 60 미만 42% → 5546876(원본 160)·8661806 뒤쪽(10초~)으로
# 11/2 눈 검사: 8369909는 비트코인 무늬 동전(코인으로 읽힘, JEPI와 다른 말) → 7118320 뒤쪽(8초~, 3번 줄은 0~6초)
BG = [(1, '7118320', 8), (2, '8661806', 2), (3, '7118320', 0), (4, '5981346', 4), (5, '5546876', 1),
      (6, '8060388', 1), (7, '6343634', 2), (8, '8661806', 10)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/detf/stock/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_jepi', 'v': 2, 'look': 'live', 'question': ['분배율 8% JEPI', '5년 동안 돈은 얼마나 불었나'], 'hot': '얼마나',
     'answer': {'label': '5년 동안 한 해 평균 불어난 비율(배당 다시 넣음)', 'items': ['JEPI 7.5%', 'S&P500 12.8%'], 'arrow': False, 'note': 'JEPI 7.5%'},
     'base': '야후 파이낸스 분배·가격(2026-10-16 마감) · 파이어맵 계산', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_jepi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_jepi: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
