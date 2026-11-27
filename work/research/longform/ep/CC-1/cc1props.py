# CC-1 화면 재료 — script.md(v1.3, editor 3ab1ab0f) + voice.json(Chirp 3 HD Charon 1.1, 115줄 — 인사 줄 없음) + shot_plan.md → work/video/cc1.json (Remotion 'CC1' = KOSPI1.tsx 틀 그대로)
#   py -3.12 work/research/longform/ep/CC-1/cc1props.py          # cc1.json을 쓰고 Root.tsx에 CC1을 붙인다
#   py -3.12 work/research/longform/ep/CC-1/cc1props.py --check  # 배치 점검만(재료 빠진 것·길이·8분 바닥)
# 11/25 02시 PD(정기 02:1x): sq1props.py 틀. 판 = visual 종이 판(bg/cc1/board, cc1boards.py — calc 출력에서 숫자를 읽어 박음)
#   ↔ Pexels 실사(bg/cc1/stock/credits.json — ROLE 8자리, shot_plan '장면 계획' 구상 그대로) ↔ 장 카드(ask). 실사 say는 숫자 없는 말만(18자 이하). 가상 인물 없음.
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
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in
                          ('cc1_calc_out_1122.txt', 'cc1_windows_out_1122.txt', 'cmp_div_out_1122.txt', 'cmp_px_out_1122.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 117, len(ALL)   # v1.6 (11/27 이해 시험 2줄 더함 88·94, editor 577ce117) · 11/27 18시 PD
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
SAY = [re.sub(r'^-\s*', '', s).strip() for s in SCRIPT.split('\n') if s.startswith('- ')]
assert len(SAY) == 117, len(SAY)
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 9 and HEADS[1].startswith('이 상품은') and HEADS[8] == '끝', HEADS
HEADS[8] = '정리'

MISSING = []
stale = [i for i in range(len(ALL)) if ALL[i]['text'].strip() != SAY[i]]
if stale: MISSING.append(f'녹음이 script.md와 다른 줄 {len(stale)}개 — 재녹음 먼저: ' + ','.join(map(str, stale)))

CRF = os.path.join(PUB, 'bg', 'cc1', 'stock', 'credits.json')
CR = {str(c['id']): c for c in json.load(open(CRF, encoding='utf-8'))} if os.path.exists(CRF) else {}
for c in CR.values():   # visual credits.json은 file이 'id.mp4'(폴더 없음) — public 기준 경로로
    if not c['file'].startswith('bg/'): c['file'] = 'bg/cc1/stock/' + c['file']
# shot_plan '장면 계획' 실사 구상 → Pexels id (visual이 고르면 여기 적는다)
ROLE = {   # 같은 클립을 여러 번 쓰면 다른 구간(3초씩 밀림) — 길이 모자람은 --check '실사 모자람'이 잰다
    'PASSBOOK2': 8731583,  # 나무 식탁 위 손글씨 공책을 펼친 손, 얼굴 없음 (여는 말·5장·6장 계좌 줄) — 경쟁 #18 · 11/27 visual 교체(옛 6197178 지폐 인물)
    'LEDGER': 5466768,     # 월말 가계부에 적는 손·계산기 두드리는 손 (여러 곳) — 경쟁 #19
    'FOG': 35830059,        # 안개 속 흙길, 표지판·글자 없음 (여는 말 끝·7장) — 경쟁 #24 · 11/27 visual 교체(옛 34942921 표지판·번호판)
    'ORCHARD': 8439245,     # 서류에 서명하는 나이 든 손, 얼굴 없음 (1장 '살 권리를 팔고') — 경쟁 #15·#16 · 11/27 visual 2차(사과 손은 뜻 약함)
    'CALENDAR': 8134590,   # 달력을 한 장씩 넘기는 손 (2장 머리·5장) — 경쟁 #19
    'DRAWER': 6550666,     # 서랍 속 오래된 통장 묶음을 꺼내는 손, 바랜 색 (3장 머리·6장) — 경쟁 #18
    'SCALE': 7955150,      # 모래가 천천히 빠지는 모래시계와 손 (4장 '덜 빠진다') — 경쟁 #20 · 11/27 visual 2차(저울은 뜻 약함)
    'MELT': 6552966,       # 녹아내리는 얼음덩이 (4장 '원금이 녹을까') — 경쟁 #20 · 11/27 visual
    'FRAME': 37224949,     # 필름 여러 칸 중 한 칸을 돋보기로 보는 손 (7장 '한 장면일 뿐') — 경쟁 #24 · 11/27 visual 3차(2021 달력 뺌)
    'DRIP': 4571346, # 수도꼭지에서 물방울만 똑, 사람 없음 (2장 '분배율 9%인데 못 미침') — 11/27 visual(동전 쌓임은 반대 뜻이라 심사 H 못함)
    'START': 8456204, # 육상 트랙 출발선에 선 발, 얼굴 없음 (3장 '상장한 날부터') — 경쟁 #18 · 11/27 visual(DRAWER 재탕 뺌)
    'CALC': 6963484, # 계산기를 두드리는 두 손, 얼굴 없음 (3장 '다시 사들였다면') — 경쟁 #19 · 11/27 visual(LEDGER 재탕 뺌)
    'MIXER': 12213088,     # 여러 손잡이 중 하나를 옮기는 손 (7장 '바뀔 수 있어요') — 경쟁 #15 · 11/27 visual
    'JAR': 34263260,       # 빈 유리병에 동전이 떨어짐 (8장 '받는 돈과 남는 돈') — 경쟁 #23 · 11/27 visual
    'WINDOW': 30763459,     # 햇빛 드는 창가 식탁·찻잔, 사람 없음 (끝 숨 쉴 3초·끝 그림) — 경쟁 #23 · 11/27 visual 교체(옛 6374411 노트북)
}
HAVE = {}


def cid_of(role):
    c = ROLE[role]
    return str(c) if c else None


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
    if not os.path.exists(os.path.join(PUB, 'bg', 'cc1', 'board', f + '.png')): MISSING.append(f'판 bg/cc1/board/{f}.png (visual)')
    return S('pic', idx, pic=f'bg/cc1/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


# 11/26 22시 PD: 7장 '끝날 6개' = 움직이는 판 EndFlip(motion 11:59, ep/CC-1/motion.md) — 숫자는 cc1_ends.json(endflipprops.py가 자막·windows_out과 assert)
MO = json.load(open(os.path.join(EP, 'motion_preview', 'cc1_ends.json'), encoding='utf-8'))


def mo(key, idx):
    m = MO[key]; p = json.loads(json.dumps(m['data']))
    s = S('mo', idx, part=key, p=p, title=m['title'], sub=m['sub'], source=m['source'], chapter=m['chapter'])
    p['end'] = s['frames']
    return s


USEDBG = {}


def broll(role, idx, say=None, frm=None):
    cid = cid_of(role)
    s = S('broll', idx, src=CR[cid]['file'] if cid in CR else f'bg/cc1/stock/{role}.mp4',
          license=f"Pexels {cid} 무료({CR[cid]['author'].strip()})" if cid in CR else '', say=say, side='left', _role=role)
    h = have(cid) if cid else None
    if h is None or cid not in CR: MISSING.append(f'실사 {role}(Pexels id·파일·credits — visual)'); return s
    k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; h -= 0.5
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, h - sec), k * 3)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = h
    return s


scenes = []
# 0 여는 말 (voice 0~5) — 답 숫자는 판 cc1_open2 하나에만
scenes += [broll('PASSBOOK2', [0], '얼마가 남았을까'), board('cc1_open2', [1, 2]), broll('LEDGER', [3], '분배금만 놓고 보면'), broll('FOG', [4, 5], '끝을 어디로 잡느냐')]
# 1 이 상품은 어떻게 분배금을 만드나 (6~14)
# 11/27 18시 PD: visual 2차 ORCHARD 8439245는 6.8초라 [7,8] 9.1초가 모자람 → 8은 LEDGER
scenes += [ask(1, [6]), broll('ORCHARD', [7], '살 권리를 미리 팔고'), broll('LEDGER', [8], '배당에 더해져서'), board('cc1_cap', [9, 10]), broll('MIXER', [11], '파는 양을 조절해요'), board('cc1_two', [12, 13, 14])]
# 2 최근 1년, 같은 날 1억 (15~25)
scenes += [ask(2, [15]), broll('CALENDAR', [16], '한 달도 빠짐없이'), board('cc1_acct_cc', [17, 18]), board('cc1_acct_dj', [19, 20]), board('cc1_gap', [21]),
           broll('DRIP', [22, 23], '분배율은 높았는데'), board('cc1_yield', [24, 25])]
# 3 더 길게 보면 (26~39)
scenes += [ask(3, [26]), broll('DRAWER', [27], '그때로 돌아가면'), board('cc1_long2', [28, 29, 30]), broll('START', [31], '상장한 날부터'),
           board('cc1_since', [32, 33, 34, 35, 36]), broll('CALC', [37], '다시 사들였다면'), board('cc1_divyear', [38, 39])]
# 4 분배금은 많았는데 왜 덜 남았나 (40~53)
scenes += [ask(4, [40]), board('cc1_step_cc', [41, 42, 43]), board('cc1_step_dj', [44, 45]), broll('SCALE', [46, 47, 48], '덜 빠진다는 말'),
           board('cc1_dd', [49]), board('cc1_dd_long', [50, 51]), broll('MELT', [52, 53], '원금이 녹을까')]
# 5 매달 얼마 들어왔나 · 받아 씀 vs 다시 넣음 (54~69)
scenes += [ask(5, [54]), board('cc1_month12', [55, 56, 57, 58]), broll('LEDGER', [59], '고르게 들어온 돈'), board('cc1_month12', [60, 61], z=(1.04, 1.10)),
           broll('PASSBOOK2', [62], '생활비로 쓰신다면'), board('cc1_reinvest', [63, 64, 65, 66]), broll('CALENDAR', [67], '더 길게 늘리면'), board('cc1_reinvest', [68, 69], z=(1.04, 1.08))]
# 6 세금 한 장 (70~85)
scenes += [ask(6, [70]), board('cc1_tax', [71, 72, 73]), broll('PASSBOOK2', [74, 75], '분배금 전부는 아니에요'), broll('LEDGER', [76, 77], '이자와 배당을 합쳐'),
           board('cc1_ruler', [78, 79, 80]), broll('DRAWER', [81, 82], '다른 배당이 있으면'), broll('PASSBOOK2', [83, 84, 85], '계좌마다 다른 셈')]
# 7 함정 (86~106) — 11/27 18시 PD: v1.6 새 88(넣는 날·끝날 같이 옮김)은 FOG에, 새 94(일반형 앞선 두 번=최근)는 EndFlip 'cc 4·일반 2' 찍힌 뒤에 — beats 0~3=89~92 그대로라 cc1_ends.json 손 안 댐
scenes += [ask(7, [86]), broll('FOG', [87, 88], '어디서 자르느냐'), mo('ends', [89, 90, 91, 92, 93, 94]), broll('FRAME', [95], '한 장면일 뿐'),
           board('cc1_chart2', [96, 97, 98, 99]), broll('LEDGER', [100, 101], '한쪽 가격으로만'), broll('MIXER', [102, 103], '바뀔 수 있어요'), board('cc1_fee', [104, 105, 106])]
# 8 정리 (107~116) — 끝 줄 앞 숨 쉴 실사 WINDOW, 끝 그림 위 END_PAD
# 11/27 02시 PD: 185행 말이 길어져 정리 판 20.5초 → 108(일반 계좌) 줄을 실사로 끊음(판 20초 규칙)
scenes += [ask(8, [107]), board('cc1_summary', [108, 109]), broll('PASSBOOK2', [110], '일반 계좌라면'), board('cc1_summary', [111, 112], z=(1.04, 1.08)), broll('JAR', [113], '받는 돈과 남는 돈'), broll('LEDGER', [114, 115], '직접 세어 보세요')]
END_PIC = 'bg/cc1/stock/window_last.jpg'
pc = cid_of('WINDOW')
scenes += [S('pic', [116], pic=END_PIC, license=f"Pexels {pc} 무료({CR[pc]['author']})" if pc in CR else '', baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
if pc not in CR: MISSING.append('실사 WINDOW(끝 그림 — visual)')
scenes[-1]['frames'] += END_PAD
scenes[-1]['lines'].append({'text': '', 'audio': None, 'frames': END_PAD, 'cap': None, 'i': None})

assert USED == set(range(len(ALL))), ('안 쓴 줄', [i for i in range(len(ALL)) if i not in USED])
order = [l['i'] for s in scenes for l in s['lines'] if l['i'] is not None]; assert order == sorted(order), '줄 순서'
for s in scenes: assert s['kind'] != 'broll' or not re.search(r'\d', s['data']['say'] or ''), ('실사 say 숫자', s['data']['say'])
for s in scenes: assert s['kind'] != 'broll' or len(s['data']['say'] or '') <= 18, ('say 18자 넘음', s['data']['say'])
for a, b in zip(scenes, scenes[1:]):
    assert a['data'].get('pic') is None or a['data'].get('pic') != b['data'].get('pic'), ('같은 그림 연달아', a['data']['pic'])
    ra, rb = a['data'].get('_role'), b['data'].get('_role')
    assert ra is None or ra != rb, ('같은 실사 연달아', ra)
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
stat = (f'{tot / FPS:.1f}초({tot / FPS / 60:.2f}분) · 장면 {len(scenes)} · 실사 {live / tot * 100:.1f}% · 판 최장 {max(s["frames"] for s in scenes[:-1] if s["kind"] == "pic") / FPS:.1f}초'
        f' · 판 묶음 최장 {max(runs) / FPS:.1f}초 · 실사 모자람 {short} · 20초 넘는 판 {long}')
assert not short and not long and max(runs) / FPS <= 19.5, stat
if tot / FPS < 480: MISSING.append(f'롱폼 8분 바닥 미달 {tot / FPS:.1f}초 — 말 {480 - tot / FPS:.0f}초 넘게 더 필요(youtube-loop 대본, 채우려 늘리기 금지)')
if CHECK or MISSING:
    print('CC-1 배치 점검:', stat)
    print('아직 없는 것' if MISSING else '재료 다 있음', *sorted(set(MISSING)), sep='\n  ')
    sys.exit(0 if CHECK else 1)

if not os.path.exists(os.path.join(PUB, END_PIC)):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-sseof', '-0.6', '-i', os.path.join(PUB, CR[pc]['file']),
                    '-frames:v', '1', '-q:v', '2', os.path.join(PUB, END_PIC)], check=True)
for s in scenes:
    d = s['data']; d.pop('_role', None)
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

# 상시 장 띠(SQ-1과 같은 방식, 장 이름 = 장 카드 q와 같은 HEADS) — 시작 = 장 카드(ask) 장면 첫 프레임, 전 구간 dark
_st, _a = [], 0
for s in scenes:
    if s['kind'] == 'ask': _st.append(_a)
    _a += s['frames']
_dk = [[0, _a + 999]]
assert len(_st) == 8, _st
strip = {'chapters': [{'n': c, 'name': HEADS[c]} for c in range(1, 9)], 'starts': _st, 'total': 8, 'topic': None, 'side': 'right', 'dark': _dk, 'top': 3, 'fs': 20}
json.dump({'fps': FPS, 'scenes': scenes, 'badge': '', 'strip': strip}, open(os.path.join(VID, 'cc1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'file': CR[n]['file'], 'used': USEDBG[n], 'desc_line': CR[n].get('desc_line', '')} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tsx = os.path.join(VID, 'src', 'CC1.tsx')
if not os.path.exists(tsx):
    src = open(os.path.join(VID, 'src', 'KOSPI1.tsx'), encoding='utf-8').read()
    src = src.replace("import {SumRace} from './motion/SumRace';", "import {SumRace} from './motion/SumRace';\nimport {EndFlip} from './motion/EndFlip';", 1)
    src = src.replace("{d.part === 'race' || d.part === 'gap' ?", "{d.part === 'ends' ? <EndFlip {...d.p} beats={B} /> : d.part === 'race' || d.part === 'gap' ?", 1)
    assert 'EndFlip {...d.p}' in src and "from './motion/EndFlip'" in src, 'CC1.tsx EndFlip 붙이기 실패'
    src = src.replace('KOSPI1Props', 'CC1Props').replace('kospi1Frames', 'cc1Frames').replace('export const KOSPI1', 'export const CC1')
    open(tsx, 'w', encoding='utf-8').write('// CC-1(커버드콜 vs 일반 배당 ETF) 롱폼 화면 — 11/25 PD: KOSPI1.tsx 그대로(이름만). props work/video/cc1.json ← ep/CC-1/cc1props.py\n' + src)
root = os.path.join(VID, 'src', 'Root.tsx'); r = open(root, encoding='utf-8').read()
if "from './CC1'" not in r:
    r = r.replace("import kospi1 from '../kospi1.json';", "import kospi1 from '../kospi1.json';\nimport {CC1, CC1Props, cc1Frames} from './CC1';\nimport cc1 from '../cc1.json';", 1)
    r = r.replace('  const kk1 = kospi1 as unknown as KOSPI1Props;', '  const kk1 = kospi1 as unknown as KOSPI1Props;\n  const ccq = cc1 as unknown as CC1Props;', 1)
    i = r.index('<Composition id="KOSPI1"')
    r = r[:i] + ('<Composition id="CC1" component={CC1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={cc1Frames(ccq)} fps={ccq.fps}\n'
                 '      width={1920} height={1080} defaultProps={ccq as unknown as Record<string, unknown>}\n'
                 '      calculateMetadata={({props: pp}) => ({durationInFrames: cc1Frames(pp as unknown as CC1Props)})} />\n    ') + r[i:]
    assert "from './CC1'" in r and 'const ccq' in r, 'Root.tsx 붙이기 실패'
    open(root, 'w', encoding='utf-8').write(r)
print(f'CC-1 cc1.json: {stat} · numcheck {nnum}덩이 불일치 0 · 다음: lfrender.py text → editor stamp → render')
