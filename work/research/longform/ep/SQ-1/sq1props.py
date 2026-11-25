# SQ-1 화면 재료 — script.md(v1.6+C-37 인사 뺌) + voice.json(Chirp 3 HD Charon 1.1, 117줄 중 0번 인사 뺌) + shot_plan.md → work/video/sq1.json (Remotion 'SQ1' = KOSPI1.tsx 틀 그대로)
#   py -3.12 work/research/longform/ep/SQ-1/sq1props.py          # sq1.json을 쓰고 Root.tsx에 SQ1을 붙인다
#   py -3.12 work/research/longform/ep/SQ-1/sq1props.py --check  # 배치 점검만(재료 빠진 것·길이·8분 바닥)
# 11/24 14:3x PD(정기 14:1x): kospi1props.py 틀. 판 = visual 종이 판(bg/sq1/board, sq1boards.py — calc 출력에서 숫자를 읽어 박음)
#   ↔ Pexels 실사(bg/sq1/stock/credits.json — visual 11/25 12:00 shot_plan 실사 7줄) ↔ 장 카드(ask). 실사 say는 숫자 없는 말만(18자 이하). 가상 인물 없음.
#   C-37: voice.json 0번(인사)은 장면에 넣지 않는다(H-6처럼 다시 녹음 없음). script.md '- ' 줄 116개 = voice 1~116번.
#   실사 자리(ROLE)는 shot_plan '장면 계획' 구상 그대로 — visual이 credits.json에 고른 Pexels id를 ROLE에 적으면 MISSING이 풀린다.
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
                          ('calc_mix_out_1112.txt', 'calc_krw_out_1120.txt', 'calc_tax_out_1121b.txt', 'calc_dca_out_1120.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 122, len(ALL)   # 11/24 18시 PD: v1.7 새 줄 6개(59·74·85·86·101·112, editor cd3317c4) — make가 인사 줄 없는 script대로 다시 짜 voice 0번 = 첫 질문(인사 소리 없음)
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
SAY = [re.sub(r'^-\s*', '', s).strip() for s in SCRIPT.split('\n') if s.startswith('- ')]
assert len(SAY) == 122, len(SAY)
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 9 and HEADS[1].startswith('나스닥100') and HEADS[8] == '끝', HEADS
HEADS[8] = '정리'

MISSING = []
stale = [i for i in range(len(ALL)) if ALL[i]['text'].strip() != SAY[i]]
if stale: MISSING.append(f'녹음이 script.md와 다른 줄 {len(stale)}개 — 재녹음 먼저: ' + ','.join(map(str, stale)))

CRF = os.path.join(PUB, 'bg', 'sq1', 'stock', 'credits.json')
CR = {str(c['id']): c for c in json.load(open(CRF, encoding='utf-8'))} if os.path.exists(CRF) else {}
for c in CR.values():   # visual credits.json은 file이 'id.mp4'(폴더 없음) — public 기준 경로로
    if not c['file'].startswith('bg/'): c['file'] = 'bg/sq1/stock/' + c['file']
# shot_plan '장면 계획' 실사 구상 → Pexels id (visual이 고르면 여기 적는다)
ROLE = {
    'NOTE': 5466772,      # 아침 식탁 노트·펜·계산기 근접, 얼굴 없음 (여는 말·계산 조건 줄)
    'CITY': 40806780,      # 저녁 빌딩 유리에 번진 전광판 불빛, 글자 흐림 (1장 머리)
    'MAIL': 6851679,      # 우편함 봉투를 꺼내는 손 근접 (2장 머리·배당)
    'FX': None,        # 환율 전광판 빛이 번진 유리, 숫자 흐림 (4장 머리)
    'PASSBOOK': 7710769,  # 통장 정리기에서 나오는 통장 근접, 글자 흐림 (5장 머리)
    'FOLDERS': 8135727,   # 서류를 서류철에 나눠 넣는 손 38초 (6장 머리·두 갈래) — visual 11/25 7710340(12.3초) 바꿈
    'PLANT': 7578510,     # 창가 화분 위로 번지는 아침 햇빛 (끝 숨 쉴 3초)
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
    if not os.path.exists(os.path.join(PUB, 'bg', 'sq1', 'board', f + '.png')): MISSING.append(f'판 bg/sq1/board/{f}.png (visual)')
    return S('pic', idx, pic=f'bg/sq1/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


USEDBG = {}


def broll(role, idx, say=None, frm=None):
    cid = cid_of(role)
    s = S('broll', idx, src=CR[cid]['file'] if cid in CR else f'bg/sq1/stock/{role}.mp4',
          license=f"Pexels {cid} 무료({CR[cid]['author'].strip()})" if cid in CR else '', say=say, side='left', _role=role)
    h = have(cid) if cid else None
    if h is None or cid not in CR: MISSING.append(f'실사 {role}(Pexels id·파일·credits — visual)'); return s
    k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; h -= 0.5
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, h - sec), k * 3)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = h
    return s


scenes = []
# 0 여는 말 (1~10) — 답 숫자는 판 sq1_open3 하나에만
scenes += [broll('NOTE', [0], '어디가 더 불었을까'), board('sq1_open3', [1, 2, 3, 4]), broll('NOTE', [5], '넣은 때를 바꾸면'),
           broll('FX', [6, 7], '원화로 다시 세면'), broll('FOLDERS', [8, 9], '세금을 떼면')]
# 1 나스닥100은 어떻게 갈아 끼우나 (11~20)
scenes += [ask(1, [10, 11]), broll('CITY', [12, 13], '금융회사는 빼고'), board('sq1_cal12', [14, 15]), broll('CITY', [16], '갑자기 커지면'), board('sq1_cap20', [17, 18, 19])]
# 2 SCHD는 무엇을 담나 (21~31)
scenes += [ask(2, [20]), board('sq1_sieve4', [21, 22, 23, 24]), broll('MAIL', [25, 26, 27, 28], '위에서부터 담아요'), board('sq1_fee2', [29, 30])]
# 3 섞는 비율별 지난 15년과 5년 (32~52)
scenes += [ask(3, [31]), broll('NOTE', [32], '비율을 나눠 셌어요'), board('sq1_mix5', [33, 34, 35]), broll('CITY', [36], '더 깊이 빠질 때'),
           board('sq1_y2022', [37]), broll('NOTE', [38], '넣은 때를 바꾸면'), board('sq1_line5', [39, 40, 41, 42, 43]),
           broll('MAIL', [44, 45, 46], '어디서 자르느냐'), board('sq1_dca', [47, 48, 49, 50, 51])]
# 4 원화로 다시 보면 (53~67)
scenes += [ask(4, [52, 53]), board('sq1_fx', [54, 55, 56]), broll('FX', [57, 58, 59], '환율이 오른 몫'),
           board('sq1_valley2', [60, 61, 62, 63, 64]), broll('CITY', [65, 66, 67], '지난 환율 이야기')]
# 5 매달 들어오는 돈 (68~75)
scenes += [ask(5, [68]), broll('PASSBOOK', [69, 70], '나눠 주는 배당'), board('sq1_dist3', [71, 72, 73, 74]), broll('PASSBOOK', [75, 76], '생활비로 쓰신다면')]
# 6 직접 사나, 국내 상장으로 사나 (76~100)
scenes += [ask(6, [77]), board('sq1_tax2way', [78, 79, 80]), broll('FOLDERS', [81, 82, 83, 84], '금융소득이란'), broll('PASSBOOK', [85, 86], '연금은 따로 셈'),   # 85·86 = v1.7 새 줄(연금은 2천만원 셈 밖) · youtube-loop 11/25 20:51: 장 머리 실사(r18) 세 번 못함 → 경쟁 #15처럼 판이 장 머리, ask 4.8+판 14.7=19.5초
           broll('NOTE', [87, 88, 89], '이렇게 쳤어요'), board('sq1_tax15', [90, 91, 92, 93]), broll('FOLDERS', [94], '늘 낫지는 않아요'),
           board('sq1_tax5', [95, 96, 97, 98]), broll('MAIL', [99, 100, 101], '직접 받은 배당'), broll('FOLDERS', [102, 103, 104], '내 계좌부터')]
# 7 함정 (101~110)
scenes += [ask(7, [105]), board('sq1_traps3', [106, 107, 108, 109]), broll('NOTE', [110, 111, 112], '따라가는 지수 이름'), board('sq1_traps3', [113, 114, 115])]
# 8 정리 (111~116) — 끝 줄 앞 숨 쉴 실사는 PLANT 끝 그림 위 END_PAD
scenes += [ask(8, [116]), board('sq1_summary', [117, 118, 119]), broll('CITY', [120], '전체 표는 카페에')]
END_PIC = 'bg/sq1/stock/plant_last.jpg'
pc = cid_of('PLANT')
scenes += [S('pic', [121], pic=END_PIC, license=f"Pexels {pc} 무료({CR[pc]['author']})" if pc in CR else '', baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
if pc not in CR: MISSING.append('실사 PLANT(끝 그림 — visual)')
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
    print('SQ-1 배치 점검:', stat)
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

# 11/24 22시 PD: 상시 장 띠(benchmark-loop 11/24 ②2, SQ-1/motion.md 'PD 할 일', 장 이름 = 장 카드 q와 같은 HEADS) — 시작 = 장 카드(ask) 장면 첫 프레임, 0. 여는 말 없음, 전 구간 dark(틀 바탕이 어두움)
STRIP = json.load(open(os.path.join(EP, 'sq1_strip.json'), encoding='utf-8'))['strip']
_st, _a = [], 0
for s in scenes:
    if s['kind'] == 'ask': _st.append(_a)
    _a += s['frames']
_dk = [[0, _a + 999]]   # KOSPI1 틀은 장 카드(ask)도 어두운 바탕(still 11/24 22시: 회색 글자가 묻힘) → 전 구간 흰 글자
assert len(_st) == 8, _st
strip = {'chapters': [{'n': c, 'name': HEADS[c]} for c in range(1, 9)], 'starts': _st, 'total': 8, 'topic': None, 'side': 'right', 'dark': _dk, 'top': 3, 'fs': 20}   # 판(inset 0.80) 위 어두운 틈이 약 35px — 주제 줄 빼고 20px(still 4556: 24px+주제 줄은 밝은 판에 걸림)
json.dump({'fps': FPS, 'scenes': scenes, 'badge': '', 'strip': strip}, open(os.path.join(VID, 'sq1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'file': CR[n]['file'], 'used': USEDBG[n], 'desc_line': CR[n].get('desc_line', '')} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tsx = os.path.join(VID, 'src', 'SQ1.tsx')
if not os.path.exists(tsx):
    src = open(os.path.join(VID, 'src', 'KOSPI1.tsx'), encoding='utf-8').read()
    src = src.replace('KOSPI1Props', 'SQ1Props').replace('kospi1Frames', 'sq1Frames').replace('export const KOSPI1', 'export const SQ1')
    open(tsx, 'w', encoding='utf-8').write('// SQ-1(나스닥100·SCHD 15년) 롱폼 화면 — 11/24 PD: KOSPI1.tsx 그대로(이름만). props work/video/sq1.json ← ep/SQ-1/sq1props.py\n' + src)
root = os.path.join(VID, 'src', 'Root.tsx'); r = open(root, encoding='utf-8').read()
if "from './SQ1'" not in r:
    r = r.replace("import kospi1 from '../kospi1.json';", "import kospi1 from '../kospi1.json';\nimport {SQ1, SQ1Props, sq1Frames} from './SQ1';\nimport sq1 from '../sq1.json';", 1)
    r = r.replace('  const kk1 = kospi1 as unknown as KOSPI1Props;', '  const kk1 = kospi1 as unknown as KOSPI1Props;\n  const sqq = sq1 as unknown as SQ1Props;', 1)
    i = r.index('<Composition id="KOSPI1"')
    r = r[:i] + ('<Composition id="SQ1" component={SQ1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={sq1Frames(sqq)} fps={sqq.fps}\n'
                 '      width={1920} height={1080} defaultProps={sqq as unknown as Record<string, unknown>}\n'
                 '      calculateMetadata={({props: pp}) => ({durationInFrames: sq1Frames(pp as unknown as SQ1Props)})} />\n    ') + r[i:]
    assert "from './SQ1'" in r and 'const sqq' in r, 'Root.tsx 붙이기 실패'
    open(root, 'w', encoding='utf-8').write(r)
print(f'SQ-1 sq1.json: {stat} · numcheck {nnum}덩이 불일치 0 · 다음: lfrender.py text → editor stamp → render')
