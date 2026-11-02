# de1s_schdgrow — D-ETF-1 롱폼 첫 장(0:4~0:6)·2장(2:6~2:10)을 자른 세로 쇼츠 props · c1clip 틀(C1S live, E-18 통과 틀) (firemap-video-producer 2026-11-02, de1s_jepi/de1jclip.py 복사 — 줄·장면·배경만)
#   py -3.12 work/research/cardshorts/de1s_schdgrow/de1sclip.py   → work/video/de1s_schdgrow.json
# 목소리 = D-ETF-1 voice.json 문장 wav 그대로(새 녹음 0) · 브랜드 첫·끝 줄 뺌 · 2:11·2:12(HDV 매달 분배)는 질문 밖 곁가지라 뺌(A-49)
# 0:4 wav는 'SCHD 한 주당…'부터다(voice.json 글자의 '하나 더 있습니다.'는 소리에 없음 — 11/2 받아쓰기 확인) → 자막 글자를 소리대로
# 화면 숫자 = calc_out.txt 해마다 분배 줄(SCHD 2017 +23.8% · 2021 +17.9% · 2025 +5.8% · 2026(최근 12개월) +2.0%)·10년 10.8%(말 '11%')
# 이유는 자료에 없음(2:8 그대로) — 지어내지 않음
# 이해 시험 3차(11/2 41·52·64세): 뜻 3/3·할 일(안 사고 안 팖, 확인) 3/3·SCHD 정체 풀림 · 2017 +23.8% 숫자 복잡 3/3 → 칸에서 숫자 뺌(화면 숫자 11%·2% 둘만)
# 이해 시험 2차(11/2 45·56·66세): 뜻 3/3 · SCHD가 뭔지 2/3 → 0초 질문 '미국 배당 ETF SCHD' · 2017만 왜 2/3 → '가장 많이 는 해'(해마다 줄 최댓값, assert) · '찾은 자료엔 없음' 누가 2/3 → '자료로는 알 수 없음'
# 이해 시험 1차(11/2 40·50·60세): 뜻 3/3 맞음 · 장면3 해·값 짝 안 맞음 3/3 → 칸 하나에 숫자 하나(2017 +23.8% · 최근 +2.0%) · 2:10 '이름에 배당 성장' 3/3 멈칫(SCHD 이름엔 없음 — 롱폼 DGRO·VIG 얘기, 곁가지) → 줄 뺌 · '한 주당 받는 돈 기준·달러' 옆 글 2/3 → 뺌, 칸 글을 '한 주가 주는 배당금'으로 · 끝 출처 '분배' 2/3 → '배당 기록'
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
# 11/2 꼴 관문 ⓐ 첫 줄 35자 이하: 0:4 wav(3.82초)를 두 줄로 나눔 — 0.80초(앞 '하나 더 있습니다.' 뒤 쉼 0.62~0.94 안)부터 2.17초(에너지 골)까지 / 2.17초~끝 (1판, 아래 2판으로 바꿈)
#   받아쓰기(11/2): 0~0.62 '하나 더 있습니다' · 0.94~2.17 '슈드 한 주당 받는 배당금액은'(SCHD를 '슈드'로 읽음) · 2.17~ '지난 10년 동안 꾸준히 늘었어요' — 새 녹음 0, 자르기만
#   꼴 ⓐ '첫 줄에 숫자' → 나누는 곳을 2.90초(쉼 2.857~2.939, silencedetect)로: '…지난 10년 동안' / '꾸준히 늘었어요.' (받아쓰기 확인)
SPLIT = {'하나 더 있습니다. SCHD': [('SCHD 한 주당 받는 배당 금액은 지난 10년 동안', 'audio/de1s_schdgrow/schd10y_a.wav', 64),
                                   ('꾸준히 늘었어요.', 'audio/de1s_schdgrow/schd10y_b.wav', 29)]}
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


scenes = [
    sc('10년 평균', ['하나 더 있습니다. SCHD', '매년 평균 11%'],
       {'tiles': [['SCHD 한 주 배당금', '10년 동안 꾸준히 늘었다', '', 0, 'ink'], ['배당금이 늘어난 비율 · 10년 평균', '매년 11%', '', 93, 'ink']]}),
    sc('최근 12개월', ['그런데 가장 최근 열두 달은'],
       {'tiles': [['최근 12개월 배당금', '2%만 늘었다', '', 0, 'ink']]}),
    sc('해마다 보면', ['아까 말한 11%는', '그리고 최근 열두 달은'],
       {'tiles': [['10년 평균 11%는', '해마다 들쭉날쭉한 값의 평균', '', 0, 'ink'], ['최근 12개월', '+2.0%', '', 135, 'ink']]}),
    sc('왜 꺾였나', ['왜 꺾였는지는', '그래서 볼 때는 긴 평균'],
       {'tiles': [['왜 꺾였는지', '자료로는 알 수 없음', '', 0, 'ink'], ['긴 평균만 보지 말고', '최근 몇 년도 같이', '', 89, 'ink']]}),
]
for s_ in scenes:
    st = [sum(l['frames'] for l in s_['lines'][:i]) for i in range(len(s_['lines']))]
    assert all(t[3] in st for t in s_['data']['tiles']), (s_['label'], st)
assert max(float(m) for m in re.findall(r'\(([+-]\d+\.\d)%\)', SRC.split('  SCHD: 2016')[1].splitlines()[0])) == 23.8, '2017이 가장 많이 는 해가 아님'
for x in ('2017 0.467(+23.8%)', '2021 0.744(+17.9%)', '2025 1.034(+5.8%)', '2026 1.055(+2.0%)', '2.0/6.5/7.2/10.8'): assert x in SRC, f'원문에 없음 {x}'
# 11/2: C1S 꼬리말(safeframe shortKick)은 12자 넘으면 '·' 앞만, 그래도 넘으면 지움 → 칸 이름 12자 이하 assert
assert all(len(t[0].split('·')[0].strip()) <= 12 for s_ in scenes for t in s_['data']['tiles']), '칸 이름 12자 넘음'
scenes[-1]['frames'] += TAIL
# 배경: de1s_jepi 11/2 밝기 실측(LiveDim 뒤 Y≥52)을 넘은 롱폼 클립만(8661806·7118320·5981346·5546876·8060388·6343634)
#   — 얼굴·상표·글자는 de1s_jepi 11/1~2 눈 검사·safezone에서 확인한 같은 구간을 다시 쓴다
# 11/2 밝기 실측(렌더 1판): Y 67.2·60 미만 31%(기준 ≤30%) — 6~10초 5981346 4초~ 구간 Y 50~59 → 8661806 5~8.6초(다른 두 구간 2~4.1·10~15.9와 안 겹침)
# 11/2 렌더: 8060388 3.07초 'No frame found'(합성기) → 5981346 20초~(같은 편 다른 구간)
BG = [(1, '7118320', 0), (1, '7118320', 2.13), (2, '8661806', 2), (3, '8661806', 5), (4, '6343634', 2), (5, '5981346', 20),
      (6, '5546876', 1), (7, '8661806', 10)]
BG = [(i + 1, c, st) for i, (_, c, st) in enumerate(BG)]   # 11/2 첫 줄을 둘로 나눠 번호 다시
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'detf', 'stock', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/detf/stock/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'de1s_schdgrow', 'v': 2, 'look': 'live', 'question': ['미국 배당 ETF SCHD', '배당금, 요즘도 매년 늘어날까'], 'hot': '늘어날까',
     'answer': {'label': '배당금이 1년에 늘어난 비율', 'items': ['10년 평균 11%', '최근 12개월 2%'], 'arrow': False, 'note': '최근 12개월 2%'},
     'base': '야후 파이낸스 배당 기록(2026-10-16 마감) · 파이어맵 계산', 'long': 'mkAxQPGaDqc',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'de1s_schdgrow.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'de1s_schdgrow: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
