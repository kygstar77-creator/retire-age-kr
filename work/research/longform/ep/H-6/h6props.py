# H-6 화면 재료 — script.md + voice.json(Chirp 3 HD Charon 1.1, 142줄) + shot_plan.md 장면 계획 → work/video/h6.json (Remotion 'H6' = H5.tsx + DealDots·GapBars)
#   py -3.12 work/research/longform/ep/H-6/h6props.py          # 재료가 다 있으면 h6.json을 쓰고 Root.tsx에 H6를 붙인다
#   py -3.12 work/research/longform/ep/H-6/h6props.py --check  # 무엇이 아직 없는지만 본다(아무것도 안 씀)
# 11/22 14:2x PD(정기 14:1x): h5props.py 틀. 판 = visual 종이 판(bg/h6/board, 숫자 박힘) ↔ Pexels 실사(shot_plan) ↔ motion 부품 둘
#   DealDots(2장 34평 점 26개 — 세 토막: 최고가·마지막 / 묶음 계단 / 인가 선) · GapBars(강남구 21곳 — 두 토막: 막대·가운데·은마 / 여섯 곳 자막 뒤 되돌아보기).
#   motion 재료(motion_preview/h6_motion.json·h6_gap.json)의 숫자·글자는 그대로 쓰고, 박자(at)만 이 편 녹음 줄에 맞춘다. 앞 토막에서 끝난 움직임은 at=-1(이미 끝난 꼴).
#   실사 say는 숫자 없는 말만. 가상 인물 없음. r19(세입자 실사)는 visual이 다시 고르는 중 — 파일이 바뀌면 R19만 고치고 다시 돌린다.
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
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('calc_out.txt', 'calc2_out.txt', 'calc3_out.txt', 'gangnam_count_1122_out.txt', 'gangnam_count_1125_out.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 142, len(ALL)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 9 and HEADS[1].startswith('은마는') and HEADS[8] == '정리', HEADS
# 장 첫 줄이 녹음 구역 첫 줄과 같은지(장 카드가 엉뚱한 줄에 붙지 않게)
FIRST = [sum(len(s['lines']) for s in V['sections'][:k]) for k in range(len(V['sections']))]
assert FIRST == [0, 10, 23, 57, 69, 97, 107, 129, 138], FIRST

MISSING = []
R19 = '29303349'   # visual 11/22 17시 다시 고름(4277488 → 한국 아파트·동네 드론 29303349, 0~4.2초 반 속도 8.4초 — '110' 동 번호 나오기 전) — 바뀌면 이 값과 bg/h6/stock/credits.json

CR = {}
for c in json.load(open(os.path.join(PUB, 'bg', 'h4', 'stock', 'credits.json'), encoding='utf-8')):
    CR[str(c['id'])] = dict(c, file=f"bg/h4/stock/{c['id']}.mp4")
for c in json.load(open(os.path.join(WORK, 'research', 'longform', 'ep', 'H-5', 'stock_credits.json'), encoding='utf-8')):
    CR[str(c['id'])] = dict(c, desc_line=c.get('desc_line') or f"영상 일부: {c['author']} / Pexels ({c['url']})")
for c in json.load(open(os.path.join(PUB, 'bg', 'h6', 'stock', 'credits.json'), encoding='utf-8')):
    CR[str(c['id'])] = dict(c, file=f"bg/h6/stock/{c['file']}")
for k, c in CR.items():
    c.setdefault('desc_line', f"영상 일부: {c['author'].strip()} / Pexels ({c.get('page') or c.get('url')})")
HAVE = {}
END_PIC = 'bg/h6/stock/38259256_last.jpg'
SIGN = [{'x': 20, 'y': 560, 'w': 210, 'h': 110}, {'x': 340, 'y': 800, 'w': 150, 'h': 90}]   # 30975009 왼쪽 건물 꼭대기 상호·유리 건물 글자(11/22 0.5·4초 눈 확인)


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


def silent(fr): return {'text': '', 'audio': None, 'frames': fr, 'cap': None, 'i': None}


def S(kind, idx, **data):
    ls = [L(i) for i in idx]
    return {'kind': kind, 'lines': ls, 'frames': sum(l['frames'] for l in ls), 'data': data}


def ask(ch, idx): return S('ask', idx, n=f'{ch}장', q=HEADS[ch])


def silent_ask(ch, fr=36):
    return {'kind': 'ask', 'lines': [silent(fr)], 'frames': fr, 'data': {'n': f'{ch}장', 'q': HEADS[ch]}}


def board(f, idx, z=(1.0, 1.04)):
    if not os.path.exists(os.path.join(PUB, 'bg', 'h6', 'board', f + '.png')): MISSING.append(f'판 bg/h6/board/{f}.png')
    return S('pic', idx, pic=f'bg/h6/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


USEDBG = {}


def broll(cid, idx, say=None, frm=None, blur=None, quiet=0):
    s = S('broll', idx, src=CR[cid]['file'] if cid in CR else f'bg/h6/stock/{cid}.mp4', license=f"Pexels {cid} 무료({CR[cid]['author'].strip()})" if cid in CR else '',
          say=say, side='left', **({'blur': blur} if blur else {}))
    if quiet: s['lines'].append(silent(quiet)); s['frames'] += quiet
    h = have(cid)
    if h is None or cid not in CR: MISSING.append(f'실사 {cid}(파일·credits)'); return s
    k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; h -= 0.5
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, h - sec), k * 5)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = h
    return s


MO = {}
for f, k in (('h6_motion.json', 'deals'), ('h6_gap.json', 'gap')):
    MO[k] = json.load(open(os.path.join(EP, 'motion_preview', f), encoding='utf-8'))[k]


def mo(key, idx, **at):
    """motion 부품 한 토막. at: 박자 칸 이름 → 이 토막 안 줄 번호(소수 = 줄 안 비율, -1 = 앞 토막에서 이미 끝남, 99 = 이 토막에선 안 일어남)."""
    m = MO[key]; p = json.loads(json.dumps(m['data'])); title = at.pop('title', m['title'])   # 11/23 PD: 토막마다 판 제목(aitell A47 같은 판 제목 3장)
    for name, v in at.items():
        if '.' in name: a, b = name.split('.'); p[a][b] = v
        else: p[name] = v
    s = S('mo', idx, part='deals' if key == 'deals' else 'gaps', p=p, title=title, sub=m['sub'], source=m['source'], chapter=m['chapter'])
    return s


NEVER, DONE = 99, -1
scenes = []
# 0 여는 말 (0~9)
scenes += [broll('30975009', [0], '은마아파트 재건축', blur=SIGN), broll('37873585', [1], '한 해 사이 얼마나?'),
           board('open85', [2, 3]), broll('6964247', [4], '신고된 실제 거래만'), broll('38259259', [5], '인가가 나기 전에'),
           broll('15082793', [6, 7], '몰린 두 달, 줄어든 신고'), board('cards3', [8]), broll('6611954', [9], '직접 세는 법')]
# 1 은마는 지금 어디까지 (10~22)
scenes += [silent_ask(1), broll('8103672', [10], '대치동 은마아파트'), board('built', [11, 12, 13]),
           broll('30975009', [14], '계단을 오르듯', blur=SIGN), board('steps', [15, 16]), board('plan49', [17]), board('steps', [18, 19]),
           broll('15082793', [20, 21, 22], '착공은 언제?')]
# 2 1년 실거래, 평형별 (23~56)
scenes += [ask(2, [23]), board('count75', [24, 25, 26]), broll('7651886', [27], '큰 평형부터'),
           mo('deals', [28, 29, 30], dropAt=0.0, **{'peak.at': 0.45, 'last.at': 1.1, 'last.gapAt': 1.6}, stepsAt=NEVER, **{'stepGap.at': NEVER, 'mark.at': NEVER, 'before.at': NEVER}),
           board('pairs', [31]), broll('6964247', [32, 33, 34], '가운데 값으로 본다'),
           mo('deals', [35, 36, 37], dropAt=DONE, **{'peak.at': DONE, 'last.at': DONE, 'last.gapAt': DONE}, stepsAt=0.1, **{'stepGap.at': 2.0, 'mark.at': NEVER, 'before.at': NEVER}, title='은마 84㎡ 묶음별 가운데 값'),
           board('pairs_2', [38]), broll('9057559', [39], '작은 평형도 같은 방법으로'),
           mo('deals', [40, 41, 42], dropAt=DONE, **{'peak.at': DONE, 'last.at': DONE, 'last.gapAt': DONE}, stepsAt=DONE, **{'stepGap.at': DONE, 'mark.at': 0.1, 'before.at': 1.3}, title='은마 84㎡ 인가 전과 뒤'),
           board('m77', [43, 44, 45]), broll('38259259', [46], '은마만 내렸을까?'),
           mo('gap', [47, 48, 49, 50], countAt=1.0, growAt=1.5, midAt=2.1, hiAt=3.1, backAt=NEVER),
           broll('7317305', [51], '거래가 적은 단지들'),
           mo('gap', [52, 53, 54], countAt=DONE, growAt=DONE, midAt=DONE, hiAt=DONE, backAt=2.05),
           broll('37873585', [55, 56], '이유는 자료에 없다')]
# 3 거래는 언제 몰렸나 (57~68)
scenes += [ask(3, [57]), broll('38259259', [58], '한 달에 몇 건씩'), board('monthly', [59, 60]), broll('15082793', [61], '강남구 전체는'),
           board('monthly', [62, 63, 64, 65]), broll('31907490', [66, 67], '매물 수와 거래 수'), broll('6611954', [68], '신고된 거래를 세기')]
# 4 세 가지 숙제 (69~96)
scenes += [ask(4, [69]), board('cards3', [70, 71]), board('share2', [72, 73, 74]), broll('6964247', [75, 76], '조합 원문은 확인 못 함'),
           broll('7651886', [77], '공사비'), board('cards3', [78, 79]), broll('9057559', [80, 81], '이익이 클수록'),
           board('charge', [82, 83]), broll('7317305', [84, 85, 86], '왜 이때 통지가?'), board('charge', [87, 88, 89, 90, 91, 92]),
           broll('38259259', [93, 94], '이주 비용은?'), board('move', [95, 96])]
# 5 세입자 계약 신고 (97~106)
scenes += [ask(5, [97]), broll(R19, [98], '세입자 쪽 숫자'), board('rent', [99, 100, 101, 102]), broll('15082793', [103], '여름에 갑자기?'),
           board('rent', [104]), broll('37873585', [105, 106], '이유는 자료에 없다')]
# 6 누구라면 (107~128)
scenes += [ask(6, [107]), broll('6143908', [108], '계속 가질 조합원'), board('relief', [109, 110, 111, 112, 113]),
           broll('7651886', [114], '집이 두 채라면'), broll('9057559', [115, 116], '보유 기간 세는 법'), broll('38259259', [117, 118, 119], '나이 든 조합원'),
           broll('37873585', [120, 121], '분양신청 기간'), board('cash', [122, 123]), board('recent9', [124]),
           broll('15082793', [125, 126, 127], '사려는 분이라면'), broll('30975009', [128], '전세를 구한다면', blur=SIGN)]
# 7 함정과 직접 확인 (129~137)
scenes += [ask(7, [129]), board('traps_1', [130]), board('traps_2', [131]), board('traps_3', [132]), board('traps_4', [133]),
           broll('31907490', [134], '직접 보는 법'), board('rt4', [135, 136, 137])]
# 8 정리 (138~141) — 끝 문장 뒤 숨 쉴 실사 3초(말 없음) → 다음 편 안내 + 최종 화면 20초
scenes += [ask(8, [138]), board('summary', [139, 140]), broll('38259256', [], None, quiet=96),
           S('pic', [141], pic=END_PIC, license=f"Pexels 38259256 무료({CR['38259256']['author'].strip()})" if '38259256' in CR else '', baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append(silent(END_PAD))

assert len(USED) == len(ALL), ('안 쓴 줄', [i for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines'] if l['i'] is not None]; assert order == sorted(order), '줄 순서'
# 11/24 10:2x PD(C-37, loop 05:02 지시 ①): script.md 첫 줄 인사 지움(editor dec54aa6) → 인사 장면 scenes.0(줄 0, 119프레임) 통째로 뺌.
#   voice.json은 다시 녹음 안 함(142줄 그대로, 줄 0은 안 씀). 렌더본은 통렌더 대신 h6_dsl1124.mp4 앞 119프레임 잘라 냄(h6_c37.mp4).
assert [l['i'] for l in scenes[0]['lines']] == [0] and ALL[0]['text'].startswith('안녕하세요'), scenes[0]['lines']
scenes = scenes[1:]
for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
for s in scenes: assert s['kind'] != 'broll' or len(s['data']['say'] or '') <= 18, ('say 18자 넘음', s['data']['say'])
for a, b in zip(scenes, scenes[1:]):
    assert a['data'].get('pic') is None or a['data'].get('pic') != b['data'].get('pic'), ('같은 그림 연달아', a['data']['pic'])
    assert a['data'].get('src') is None or a['data'].get('src') != b['data'].get('src'), ('같은 클립 연달아', a['data']['src'])
    assert not (a['kind'] == b['kind'] == 'mo'), '움직이는 판 연달아'
short = []
for s in scenes:
    d = s['data']
    if '_need' in d:
        if d['_need'] > d['_have'] + 0.5: short.append((d['src'], d['_need'], d['_have']))
isboard = lambda s: (s['kind'] == 'pic' and '/board/' in s['data']['pic']) or s['kind'] == 'mo'
long = [(s['data'].get('pic') or s['data'].get('part'), round(s['frames'] / FPS, 1)) for s in scenes[:-1] if isboard(s) and s['frames'] / FPS > 19.5]
runs, cur = [], 0
for s in scenes[:-1]:
    if isboard(s): cur += s['frames']
    else: runs.append(cur); cur = 0
runs.append(cur)
tot = sum(s['frames'] for s in scenes) + TAIL
live = sum(s['frames'] for s in scenes if s['kind'] == 'broll' or (s['kind'] == 'pic' and '/board/' not in s['data']['pic']))
stat = (f'{tot / FPS:.1f}초 · 장면 {len(scenes)} · 실사 {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if isboard(s)) / FPS:.1f}초'
        f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · 실사 모자람 {short} · 20초 넘는 판 {long}')
if CHECK or MISSING or short or long or max(runs) / FPS > 19.5:
    print('H-6 배치 점검:', stat)
    print('아직 없는 것' if MISSING else '재료 다 있음', *sorted(set(MISSING)), sep='\n  ')
    sys.exit(0 if CHECK else 1)

if not os.path.exists(os.path.join(PUB, END_PIC)):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-sseof', '-0.6', '-i', os.path.join(PUB, CR['38259256']['file']),
                    '-frames:v', '1', '-q:v', '2', os.path.join(PUB, END_PIC)], check=True)
for s in scenes:
    d = s['data']
    if 'from_' in d: d['from'] = d.pop('from_'); d.pop('_need'); d.pop('_have')
scenes[-1]['frames'] += TAIL
for s in scenes:
    for l in s['lines']: l.pop('i')

SKIP = {'audio', 'src', 'license', 'kind', 'from', 'side', 'pic', 'inset', 'zoom', 'cx', 'cy', 'baked', 'dark', 'badge', 'blur', 'x', 'part', 'seed', 'd', 'a', 'b', 'months'}


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

json.dump({'fps': FPS, 'scenes': scenes, 'badge': ''}, open(os.path.join(VID, 'h6.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'file': CR[n]['file'], 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# H6.tsx(H5.tsx 복사 + Mo에 deals·gaps) + Root.tsx 등록 — 처음 한 번만
tsx = os.path.join(VID, 'src', 'H6.tsx')
if not os.path.exists(tsx):
    src = open(os.path.join(VID, 'src', 'H5.tsx'), encoding='utf-8').read()
    src = src.replace('H5Props', 'H6Props').replace('h5Frames', 'h6Frames').replace('export const H5', 'export const H6')
    src = src.replace("import {SumRace} from './motion/SumRace';", "import {SumRace} from './motion/SumRace';\nimport {DealDots} from './motion/DealDots';\nimport {GapBars} from './motion/GapBars';", 1)
    src = src.replace("{d.part === 'race' || d.part === 'gap' ?", "{d.part === 'deals' ? <DealDots {...d.p} beats={B} /> : d.part === 'gaps' ? <GapBars {...d.p} beats={B} /> : d.part === 'race' || d.part === 'gap' ?", 1)
    assert 'DealDots {...d.p}' in src and "from './motion/GapBars'" in src
    open(tsx, 'w', encoding='utf-8').write('// H-6(은마 재건축 실거래) 롱폼 화면 — 11/22 PD: H5.tsx 그대로 + Mo에 DealDots(deals)·GapBars(gaps). props work/video/h6.json ← ep/H-6/h6props.py\n' + src)
root = os.path.join(VID, 'src', 'Root.tsx'); r = open(root, encoding='utf-8').read()
if "from './H6'" not in r:
    r = r.replace("import h5 from '../h5.json';", "import h5 from '../h5.json';\nimport {H6, H6Props, h6Frames} from './H6';\nimport h6 from '../h6.json';", 1)
    r = r.replace('  const hh5 = h5 as unknown as H5Props;', '  const hh5 = h5 as unknown as H5Props;\n  const hh6 = h6 as unknown as H6Props;', 1)
    i = r.index('<Composition id="H5"')
    r = r[:i] + ('<Composition id="H6" component={H6 as unknown as React.FC<Record<string, unknown>>} durationInFrames={h6Frames(hh6)} fps={hh6.fps}\n'
                 '      width={1920} height={1080} defaultProps={hh6 as unknown as Record<string, unknown>}\n'
                 '      calculateMetadata={({props: pp}) => ({durationInFrames: h6Frames(pp as unknown as H6Props)})} />\n    ') + r[i:]
    assert "from './H6'" in r and 'const hh6' in r
    open(root, 'w', encoding='utf-8').write(r)
print(f'H-6 h6.json: {stat} · numcheck {nnum}덩이 불일치 0 · 다음: lfrender.py text → editor stamp → render')
