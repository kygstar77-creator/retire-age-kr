# KOSPI-1 화면 재료 — script.md + voice.json(Chirp 3 HD Charon 1.1, 138줄) + shot_plan.md → work/video/kospi1.json (Remotion 'KOSPI1' = H5.tsx 틀 그대로)
#   py -3.12 work/research/longform/ep/KOSPI-1/kospi1props.py          # kospi1.json을 쓰고 Root.tsx에 KOSPI1을 붙인다
#   py -3.12 work/research/longform/ep/KOSPI-1/kospi1props.py --check  # 배치 점검만
# 11/20 18:3x PD(정기 18:1x): h5props.py 틀. 판 = visual 종이 판(bg/kospi1/board, 11/20 값 — 24번·-47%·+13%·+103%·4,870, 숫자 박힘)
#   ↔ Pexels 실사 7개(bg/kospi1/stock/credits.json, 11/20 PD 눈 확인: 신문 12345283은 제호 읽혀 뺌, 38905686은 종목 상표 읽혀 뺌)
#   ↔ 장 카드(ask). 실사 say는 숫자 없는 말만(18자 이하). 가상 인물 없음. [자막] 정확한 값은 판에 박힌 것만(cap 없음 — H-5와 같음).
import json, os, re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
CHECK = '--check' in sys.argv
EP = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(EP, '..', '..', '..', '..'))
VID = os.path.join(WORK, 'video')
PUB = os.path.join(VID, 'public')
FPS, TAIL = 30, 75
GAP_TRIM = 3
END_PAD = 20 * 30 - TAIL
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('facts.txt', 'calc2_out_1120.txt', 'calc3_out_1120.txt', 'calc4_out_1120.txt', 'calc_drop_out_1120.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 138, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
SAY = [re.sub(r'^-\s*', '', s).strip() for s in SCRIPT.split('\n') if s.startswith('- ')]
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 9 and HEADS[1] == '올해 코스피' and HEADS[8] == '정리', HEADS

MISSING = []
stale = [i for i in range(len(ALL)) if i >= len(SAY) or ALL[i]['text'].strip() != SAY[i]]
if stale: MISSING.append(f'녹음이 script.md와 다른 줄 {len(stale)}개 — 재녹음 먼저: ' + ','.join(map(str, stale)))

CR = {str(c['id']): c for c in json.load(open(os.path.join(PUB, 'bg', 'kospi1', 'stock', 'credits.json'), encoding='utf-8'))}
HAVE = {}
END_PIC = 'bg/kospi1/stock/8495394_last.jpg'


def have(cid):
    if cid in HAVE: return HAVE[cid]
    p = os.path.join(PUB, CR[cid]['file']) if cid in CR else None
    if not p or not os.path.exists(p): return None
    import cv2
    v = cv2.VideoCapture(p); HAVE[cid] = round(v.get(7) / v.get(5), 1); return HAVE[cid]


USED = set()


def L(i):
    assert i not in USED, ('두 번 씀', i); USED.add(i)
    l = ALL[i]
    if not (l.get('audio') and os.path.exists(os.path.join(PUB, l['audio']))): MISSING.append(f'소리 파일 없음 {i}')
    fr = l['frames'] - GAP_TRIM; assert fr >= int(l['sec'] * FPS + 0.999), ('소리가 잘림', i)
    return {'text': l['text'], 'audio': l['audio'], 'frames': fr, 'cap': None, 'i': i}


def S(kind, idx, **data):
    ls = [L(i) for i in idx]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}


def ask(ch, idx): return S('ask', idx, n=f'{ch}장', q=HEADS[ch])


def board(f, idx, z=(1.0, 1.04)):
    if not os.path.exists(os.path.join(PUB, 'bg', 'kospi1', 'board', f + '.png')): MISSING.append(f'판 bg/kospi1/board/{f}.png')
    return S('pic', idx, pic=f'bg/kospi1/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


USEDBG = {}


def broll(cid, idx, say=None, frm=None):
    s = S('broll', idx, src=CR[cid]['file'] if cid in CR else f'bg/kospi1/stock/{cid}.mp4',
          license=f"Pexels {cid} 무료({CR[cid]['author'].strip()})" if cid in CR else '', say=say, side='left')
    h = have(cid)
    if h is None or cid not in CR: MISSING.append(f'실사 {cid}(파일·credits)'); return s
    k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; h -= 0.5
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, h - sec), k * 3)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = h
    return s


PHONE, CHART, NUMS, STOP, PAPER, MONEY, RIVER = '39494572', '38557069', '7578632', '4957783', '5224014', '5909916', '8495394'
scenes = []
# 0 여는 말 (0~14)
scenes += [broll(PHONE, [0], '오늘은 코스피 이야기'), board('open23', [1, 2, 3, 4, 5, 6]), broll(NUMS, [7, 8], '먼저 짚을 두 가지'),
           broll(CHART, [9, 10], '장이 끝난 숫자끼리'), broll(PAPER, [11, 12], '지난 기록만 봅니다'), broll(NUMS, [13, 14], '하나하나 셌어요')]
# 1 올해 코스피 (15~30)
scenes += [ask(1, [15]), board('line2026', [16, 17, 18, 19]), broll(CHART, [20], '연초에서 보면'), board('arrows3', [21, 22]),
           board('yearbars', [23, 24]), broll(NUMS, [25], '기준을 더 세게'), board('yearbars', [26, 27]), broll(CHART, [28, 29, 30], '이유는 보도로만')]
# 2 서킷브레이커와 사이드카 (31~51)
scenes += [ask(2, [31]), broll(STOP, [32], '시장 전체를 잠깐 멈춰요'), board('breaker3', [33, 34, 35]), board('sidecar', [36, 37]),
           broll(NUMS, [38], '올해 몇 번 걸렸나'), board('cb11', [39, 40, 41, 42]), broll(STOP, [43], '많이 헷갈리는 것'),
           board('nov6', [44, 45, 46, 47]), broll(CHART, [48], '뉴스와 내 계좌는 따로'), board('check2', [49, 50, 51])]
# 3 지난 31년 (52~78)
scenes += [ask(3, [52]), broll(PAPER, [53], '몰려서 온 날들'), board('group2008', [54, 55]), board('table16', [56]),
           broll(PAPER, [57], '이름이 붙은 날'), board('names4', [58, 59, 60, 61]), broll(NUMS, [62], '올해 묶음은 빼고'),
           board('q14', [63, 64, 65, 66]), broll(PAPER, [67], '외환위기 때는'), board('q14', [68, 69]), broll(CHART, [70], '한 해가 지난 뒤엔'),
           board('dots15', [71, 72, 73]), broll(NUMS, [74], '닷컴 거품이 꺼질 때'), board('dots15', [75, 76, 77]), broll(PAPER, [78], '그렇지 않은 때도')]
# 4 전날 값을 되찾기까지 (79~90)
scenes += [ask(4, [79]), board('recover15', [80, 81, 82]), board('long1367', [83, 84]), broll(PAPER, [85], '닷컴 거품 때'),
           board('pair2008', [86, 87, 88]), broll(NUMS, [89], '외환위기 때도'), broll(CHART, [90], '계속 내려가면?')]
# 5 크게 빠진 해엔 크게 오른 날도 (91~98)
scenes += [ask(5, [91]), board('up17', [92, 93]), board('up8', [94, 95, 96]), broll(NUMS, [97, 98], '하루 숫자만 보면')]
# 6 1천만원을 넣었다면 (99~118)
scenes += [ask(6, [99]), broll(MONEY, [100, 101], '첫날 마감에 넣었다면'), board('split2', [102, 103, 104, 105]),
           broll(MONEY, [106, 107], '열두 번에 나눠'), board('split2', [108, 109, 110, 111]), broll(MONEY, [112], '차이는 흔들린 폭'),
           board('scale', [113, 114, 115, 116]), broll(MONEY, [117, 118], '월급에서 떼어 넣는 분')]
# 7 함정 (119~127)
scenes += [ask(7, [119]), board('trap1', [120, 121, 122]), broll(NUMS, [123], '지난 기록일 뿐'), board('trap2', [124, 125, 126, 127])]
# 8 정리 (128~137)
scenes += [ask(8, [128]), board('summary', [129, 130, 131]), broll(CHART, [132], '전체 표는 카페에'), board('ecos', [133, 134]),
           broll(RIVER, [135], '견딜 수 있는 폭'),
           S('pic', [136, 137], pic=END_PIC, license=f"Pexels {RIVER} 무료({CR[RIVER]['author']})", baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})

assert len(USED) == len(ALL), ('안 쓴 줄', [i for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines'] if l['i'] is not None]; assert order == sorted(order), '줄 순서'
for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
for s in scenes: assert s['kind'] != 'broll' or len(s['data']['say'] or '') <= 18, ('say 18자 넘음', s['data']['say'])
for a, b in zip(scenes, scenes[1:]):
    assert a['data'].get('pic') is None or a['data'].get('pic') != b['data'].get('pic'), ('같은 그림 연달아', a['data']['pic'])
    assert a['data'].get('src') is None or a['data'].get('src') != b['data'].get('src'), ('같은 클립 연달아', a['data']['src'])
short = []
for s in scenes:
    d = s['data']
    if '_need' in d and d['_need'] > d['_have'] + 0.5: short.append((d['src'], d['_need'], d['_have']))
long = [(s['data'].get('pic'), round(s['frames'] / FPS, 1)) for s in scenes[:-1] if s['kind'] == 'pic' and s['frames'] / FPS > 19.5]
runs, cur = [], 0
for s in scenes[:-1]:
    if s['kind'] == 'pic' and '/board/' in s['data']['pic']: cur += s['frames']
    else: runs.append(cur); cur = 0
runs.append(cur)
tot = sum(s['frames'] for s in scenes) + TAIL
live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and '/board/' not in s['data']['pic']))
stat = (f'{tot / FPS:.1f}초 · 장면 {len(scenes)} · 실사 {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
        f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · 실사 모자람 {short} · 20초 넘는 판 {long}')
assert not short and not long and max(runs) / FPS <= 19.5, stat
if CHECK or MISSING:
    print('KOSPI-1 배치 점검:', stat)
    print('아직 없는 것' if MISSING else '재료 다 있음', *sorted(set(MISSING)), sep='\n  ')
    sys.exit(0 if CHECK else 1)

if not os.path.exists(os.path.join(PUB, END_PIC)):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-sseof', '-0.6', '-i', os.path.join(PUB, CR[RIVER]['file']),
                    '-frames:v', '1', '-q:v', '2', os.path.join(PUB, END_PIC)], check=True)
for s in scenes:
    d = s['data']
    if 'from_' in d: d['from'] = d.pop('from_'); d.pop('_need'); d.pop('_have')
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

SKIP = {'audio', 'src', 'license', 'kind', 'from', 'side', 'pic', 'inset', 'zoom', 'cx', 'cy', 'baked', 'dark', 'badge', 'blur', 'x', 'part', 'seed'}


def strings(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in SKIP: continue
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            if not isinstance(v, (int, float)): yield from strings(v)
    elif isinstance(x, str): yield x


bad = []; nnum = 0
for s in scenes:
    for st in strings(s['data']):
        for d in re.findall(r'\d[\d,.]*', st):
            d = d.rstrip('.,'); nnum += 1
            if d not in SRCDOC: bad.append((st[:40], d))
assert not bad, bad

json.dump({'fps': FPS, 'scenes': scenes, 'badge': ''}, open(os.path.join(VID, 'kospi1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'file': CR[n]['file'], 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tsx = os.path.join(VID, 'src', 'KOSPI1.tsx')
if not os.path.exists(tsx):
    src = open(os.path.join(VID, 'src', 'H5.tsx'), encoding='utf-8').read()
    src = src.replace('H5Props', 'KOSPI1Props').replace('h5Frames', 'kospi1Frames').replace('export const H5', 'export const KOSPI1')
    open(tsx, 'w', encoding='utf-8').write('// KOSPI-1(코스피 하루 -5% 24번) 롱폼 화면 — 11/20 PD: H5.tsx 그대로(이름만). props work/video/kospi1.json ← ep/KOSPI-1/kospi1props.py\n' + src)
root = os.path.join(VID, 'src', 'Root.tsx'); r = open(root, encoding='utf-8').read()
if "from './KOSPI1'" not in r:
    r = r.replace("import h5 from '../h5.json';", "import h5 from '../h5.json';\nimport {KOSPI1, KOSPI1Props, kospi1Frames} from './KOSPI1';\nimport kospi1 from '../kospi1.json';", 1)
    r = r.replace('  const hh5 = h5 as unknown as H5Props;', '  const hh5 = h5 as unknown as H5Props;\n  const kk1 = kospi1 as unknown as KOSPI1Props;', 1)
    i = r.index('<Composition id="H5"')
    r = r[:i] + ('<Composition id="KOSPI1" component={KOSPI1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={kospi1Frames(kk1)} fps={kk1.fps}\n'
                 '      width={1920} height={1080} defaultProps={kk1 as unknown as Record<string, unknown>}\n'
                 '      calculateMetadata={({props: pp}) => ({durationInFrames: kospi1Frames(pp as unknown as KOSPI1Props)})} />\n    ') + r[i:]
    assert "from './KOSPI1'" in r and 'const kk1' in r, 'Root.tsx 붙이기 실패'
    open(root, 'w', encoding='utf-8').write(r)
print(f'KOSPI-1 kospi1.json: {stat} · numcheck {nnum}덩이 불일치 0 · 다음: lfrender.py text → editor stamp → render')
