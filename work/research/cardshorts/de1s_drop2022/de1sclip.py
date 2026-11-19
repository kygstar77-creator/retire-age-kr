# de1s_drop2022 — D-ETF-1 롱폼 4장 끝(4:10~4:12, 2022년·코로나 낙폭)을 자른 세로 쇼츠 props · c1clip 틀(C1S live) (firemap-video-producer 2026-11-19, de1s_schdgrow/de1sclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_drop2022/de1sclip.py   → work/video/de1s_drop2022.json
# 목소리 = D-ETF-1 voice.json 문장 wav 그대로(새 녹음 0) · 4:9 '그럼 떨어질 때는 어땠을까요?…'는 답을 5초 뒤로 미는 도입 줄이라 뺌(A-49)
# 화면 숫자 = calc_out.txt 2022 한 해 안 최대 낙폭(분배 재투자) SPY -24.5 · SCHD -16.8 · JEPI -13.7 / 2020 이후 최대 낙폭 SCHD -33.4 · SPY -33.7 · SPYD -46.4 (모두 2020-03-23)
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
# 꼴 관문 ⓐ 첫 줄 35자 이하: 4:10 wav(207프레임)를 쉼 가운데서 셋으로 — 2.77초(쉼 2.66~2.88)·4.90초(쉼 4.74~5.05), silencedetect -38dB · 받아쓰기 stt.py
SPLIT = {'S&P500은 25% 가까이': [('S&P500은 25% 가까이 빠졌는데,', 'audio/de1s_drop2022/drop_a.wav', 83),
                               ('SCHD는 17% 정도였어요.', 'audio/de1s_drop2022/drop_b.wav', 64),
                               ('JEPI는 그보다 덜 빠졌고요.', 'audio/de1s_drop2022/drop_c.wav', 60)]}
n = 0


def L(t):
    global n
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    n += 1
    return {'n': n, 'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}


def Ls(t):   # SPLIT 줄은 나눈 wav 여러 줄로
    global n
    if t not in SPLIT: return [L(t)]
    out = []
    for txt, au, fr in SPLIT[t]:
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·D-ETF-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 11/19 이해 2차(46·57·66세): 뜻·할 일·숫자 뜻 3/3·권유 0/3 · 'S&P500이 뭔지' 3/3 → 칸 머리 '미국 지수'
# 11/19 이해 1차(43·54·63세): 뜻·할 일 3/3·권유 0/3 · 걸림: SCHD·JEPI·SPYD가 뭔지 3/3 → 칸 머리에 '배당 ETF' · 6.9초 -33.4·-33.7 두 숫자 동시 3/3 → 숫자 하나 + '시장만큼' · '배당 다시 넣음'·'수정 종가' 낯섦 3/3 → 끝 칸 '고점에서 바닥까지' · 새 말 0
scenes = [
    sc('2022년', ['S&P500은 25% 가까이'],
       {'tiles': [['2022년 미국 지수', 'S&P500 -24.5%', '', 0, 'ink'], ['배당 ETF SCHD', '-16.8%', '', 83, 'ink'], ['배당 ETF JEPI', '-13.7%', '', 147, 'ink']]}),
    sc('코로나 때', ['그런데 늘 덜 빠지는 건'],
       {'tiles': [['코로나 때 SCHD', '-33.4% · 시장만큼', '', 0, 'ink']]}),
    sc('더 빠진 것도', ['코로나 때 SPYD는'],
       {'tiles': [['배당 ETF SPYD', '-46.4% · 시장보다 더', '', 0, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
for x in ('-33.4(2020-03-23) | -16.8', '-46.4(2020-03-23) | -20.3', '-13.7(2022-09-30) | -13.7', '-33.7(2020-03-23) | -24.5'): assert x in SRC, f'원문에 없음 {x}'
# C1S 꼬리말(safeframe shortKick)은 12자 넘으면 '·' 앞만, 그래도 넘으면 지움 → 칸 이름 12자 이하 assert
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경(B-56 그 줄의 대상): 4:10 하락 차트 보는 손(손+기기 1컷) · 4:11 '2020년' 넘기는 달력 · 4:12 '실제로 어땠는지 봐야' 공책에 적는 손
# 11/19 눈 검사 1판(sheet_1119.png): 7578628 폰 화면에 남의 앱 차트 숫자('-24,8' — 우리 -24.5%와 헷갈림)·어두움(Y 53~59) · 6639799 여자 얼굴 옆모습·어두움(Y 37) → 둘 다 de1s 앞 편에서 눈 검사·밝기 통과한 클립으로
BG = [(1, '7118320', 0), (2, '7118320', 2.77), (3, '7118320', 4.9), (4, '27791953', 5), (5, '5546876', 1)]   # 나눈 세 줄은 같은 클립 이어서
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/detf/stock/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_drop2022', 'v': 2, 'look': 'live', 'question': ['2022년·코로나 하락장', '배당 ETF는 덜 빠졌을까'], 'hot': '덜 빠졌을까',
     'answer': {'label': 'SCHD가 고점에서 바닥까지 빠진 폭', 'items': ['2022년 SCHD -16.8%', '코로나 SCHD -33.4%'], 'arrow': False, 'note': '코로나 SCHD -33.4%'},
     'base': '야후 파이낸스 주가·배당 기록(2026-10-16 마감) · 파이어맵 계산', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_drop2022.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_drop2022: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
