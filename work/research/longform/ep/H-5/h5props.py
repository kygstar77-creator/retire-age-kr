# H-5 화면 재료 — script.md + voice.json(Chirp 3 HD Charon 1.1, 156줄) + shot_plan.md 장면 계획 → work/video/h5.json (Remotion 'H5' = JT1.tsx 틀 그대로)
#   py -3.12 work/research/longform/ep/H-5/h5props.py          # 재료가 다 있으면 h5.json을 쓰고 Root.tsx에 H5를 붙인다
#   py -3.12 work/research/longform/ep/H-5/h5props.py --check  # 무엇이 아직 없는지만 본다(아무것도 안 씀)
# 11/17 02:3x PD(정기 02:1x): jt1props_pd.py 틀을 빌림. 판 = visual 종이 판(bg/h5/board, 숫자 박힘 — today [요청] 시한 11/19 22:00)
#   ↔ Pexels 실사(shot_plan: 34438613 송도 수로 · H-4 재사용 37873585·40294066·7205591·31907490 · visual 새로 받을 7697045 신문 손
#   + H-4에서 눈 확인 끝낸 6964247·9057559·7651886·38259259·7317305 — 판 묶음 20초·실사 10%를 맞추는 사이 컷, 송도라고 말하지 않음)
#   ↔ 장 카드(ask). 실사 say는 숫자 없는 말만. 가상 인물 없음.
# 녹음이 지금 say_v2.txt와 다르면(재녹음 전) 멈춘다 — 11/17 youtube-loop가 말 20줄을 고쳤다.
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
SRCDOC = SCRIPT + ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('facts.txt', 'calc_out.txt', 'calc2_out.txt', 'calc4_out.txt', 'research.md'))
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
ALL = [l for s in V['sections'] for l in s['lines']]
assert len(ALL) == 155, len(ALL)   # 11/19 PD: editor 11/18 17:00이 say_v2 13행('처음 보시는 분을…')을 뺌 → 155줄, 그 뒤 번호 한 칸씩 당김
assert abs(V.get('speakingRate', 0) - 1.1) < 1e-9 and V['voice'] == 'ko-KR-Chirp3-HD-Charon'
SAY = [s.strip() for s in open(os.path.join(EP, 'say_v2.txt'), encoding='utf-8').read().split('\n') if s.strip() and not s.lstrip().startswith(('[', '#'))]
HEADS = [re.sub(r'^\[?\d+\.\s*|\]$', '', h).strip() for h in re.findall(r'^## (.+)$', SCRIPT, re.M)]
assert len(HEADS) == 8 and HEADS[1].startswith('[기초]') and HEADS[3].startswith('단지'), HEADS
HEADS[1] = HEADS[1].replace('[기초]', '').strip()

MISSING = []
stale = [(i, ALL[i]['text'][:30]) for i in range(len(ALL)) if i >= len(SAY) or ALL[i]['text'].strip() != SAY[i]]
if stale: MISSING.append(f'녹음이 say_v2와 다른 줄 {len(stale)}개 — 재녹음 먼저: ' + ','.join(str(i) for i, _ in stale))

CR = {}
for c in json.load(open(os.path.join(PUB, 'bg', 'h4', 'stock', 'credits.json'), encoding='utf-8')):
    CR[str(c['id'])] = dict(c, file=f"bg/h4/stock/{c['id']}.mp4")
for c in json.load(open(os.path.join(EP, 'stock_credits.json'), encoding='utf-8')):
    CR[str(c['id'])] = dict(c, desc_line=c.get('desc_line') or f"영상 일부: {c['author']} / Pexels ({c['url']})")
# 길이(초): H-4 h4props 11/11 cv2 실측 + 34438613 11/17 cv2 실측. 7697045(신문, 제호 읽힘) → visual 11/17 6611954(휴대폰 손)로 바꿈.
HAVE = {'31907490': 8.3, '9057559': 11.4, '38259259': 40.5, '7205591': 5.8, '37873585': 32.9, '40294066': 25.5,
        '6964247': 14.6, '7651886': 11.1, '7317305': 15.4, '34438613': 8.2}
X = {'6964247': 70}   # H-4와 같은 자리 맞춤
END_PIC = 'bg/h5/stock/37736994_last.jpg'   # visual 11/17: 34438613(기둥 가림) → 37736994 마지막 장면


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


def ask(ch, idx): return S('ask', idx, n='기초' if ch == 1 else f'{ch - 1}장', q=HEADS[ch])


def silent_ask(ch, fr=36):   # 11/19 PD: 기초 장 카드에 붙던 말('처음 보시는 분을…')이 빠져 말 없이 1.2초 — 띠링이 쉬는 틈에 울림
    return {'kind': 'ask', 'lines': [{'text': '', 'audio': None, 'frames': fr, 'cap': None, 'i': None}], 'frames': fr,
            'data': {'n': '기초' if ch == 1 else f'{ch - 1}장', 'q': HEADS[ch]}}


def board(f, idx, z=(1.0, 1.04)):
    if not os.path.exists(os.path.join(PUB, 'bg', 'h5', 'board', f + '.png')): MISSING.append(f'판 bg/h5/board/{f}.png')
    return S('pic', idx, pic=f'bg/h5/board/{f}.png', license='파이어맵 자체 제작 판(출처는 판 안)', baked=True, inset=0.80, dark=True, zoom=list(z), cx=50, cy=45)


USEDBG = {}


def broll(cid, idx, say=None, frm=None):
    s = S('broll', idx, src=CR[cid]['file'] if cid in CR else f'bg/h5/stock/{cid}.mp4', license=f"Pexels {cid} 무료({CR[cid]['author'].strip()})" if cid in CR else '',
          say=say, side='left', **({'x': X[cid]} if cid in X else {}))
    h = have(cid)
    if h is None or cid not in CR: MISSING.append(f'실사 {cid}(파일·credits)'); return s
    k = USEDBG.get(cid, 0); USEDBG[cid] = k + 1; h -= 0.5
    sec = s['frames'] / FPS
    if frm is None: frm = 0 if k == 0 else min(max(0, h - sec), k * 5)   # 같은 클립을 다시 쓰면 다른 구간
    s['data']['from_'] = int(frm * FPS); s['data']['_need'] = round(sec + frm, 1); s['data']['_have'] = h
    return s


scenes = []
# 0 결론부터 (0~11)
scenes += [broll('18495181', [0, 1], '송도 아파트 실거래가'), broll('37873585', [2], '같은 넓이 거래 전부'),
           board('search', [3, 4]), board('open82', [5]), broll('15082793', [6], '단지마다 달랐다'),
           broll('31907490', [7, 8], '반값 거래는 몇 건?'), board('ruler', [9]), broll('37873585', [10, 11], '내 단지도 직접')]
# 기초 (12~24)
scenes += [silent_ask(1), board('map', [12, 13, 14]), broll('6964247', [15, 16, 17], '같은 크기끼리만'),
           broll('9057559', [18, 19], '신고된 실제 거래만'), board('median9', [20, 21, 22]), broll('37873585', [23], '사는 분도 세 들 분도')]
# 1 5년 흐름 (25~59)
scenes += [ask(2, [24]), board('half', [25, 26, 27, 28, 29, 30]), broll('37873585', [31, 32], '그 뒤로는 비슷한 값'),
           board('count', [33, 34, 35, 36, 37]), broll('7651886', [38], '가장 최근 넉 달'), board('eq82', [39, 40, 41, 42, 43]),
           broll('38259259', [44], '가장 낮았던 한 해'), board('eq82', [45, 46, 47, 48]),
           broll('7317305', [49, 50, 51, 52], '이유는 자료에 없다'), broll('37873585', [53, 54, 55, 56], '고점에 샀다면'),
           broll('15082793', [57, 58], '바닥에 샀다면')]
# 2 단지 서른두 곳 (60~96)
scenes += [ask(3, [59]), board('rank32', [60, 61, 62, 63, 64, 65]), broll('38259259', [66, 67, 68, 69], '고점을 다시 넘은 곳은?'),
           board('top3', [70, 71, 72, 73, 74]), broll('15082793', [75, 76, 77, 78], '덜 돌아온 쪽'), board('pair', [79, 80, 81]),
           broll('7651886', [82], '새 아파트일수록?'), board('built', [83, 84, 85, 86]), broll('9057559', [87, 88], '내 단지의 두 숫자'),
           broll('15082793', [89, 90, 91], '거래 서너 건뿐인 단지'), broll('37873585', [92, 93, 94, 95], '셈에서 빠진 단지')]
# 3 '반값'과 '6~70%' (97~128)
scenes += [ask(4, [96]), broll('6611954', [97, 98, 99, 100], '오피스텔·경매 물건'), board('dots', [101, 102, 103, 104, 105]),
           broll('6964247', [106, 107, 108], '직거래란'), board('dots', [109, 110, 111, 112, 113]), broll('7317305', [114, 115], '직거래 표시만 있다'),
           broll('38259259', [116, 117, 118], '무엇으로 나눴나'), board('ruler', [119, 120, 121]), broll('7651886', [122], '훨씬 낮게 나온다'),
           board('ruler', [123, 124, 125]), broll('9057559', [126, 127], '최고 한 건인지부터')]
# 4 전세 (129~138)
scenes += [ask(5, [128]), broll('7205591', [129], '전세는 얼마'), board('jeonse', [130, 131, 132, 133]),
           broll('7205591', [134], '단지마다 전세 비율'), board('ratio', [135, 136, 137])]
# 5 직접 확인 (139~149)
scenes += [ask(6, [138]), broll('31907490', [139], '실거래가 공개시스템'), board('check5', [140, 141, 142, 143]),
           broll('6964247', [144, 145, 146], '이번 달 거래는 덜 들어옴'), board('check5', [147, 148])]
# 6 정리 (150~155)
scenes += [ask(7, [149]), board('summary', [150, 151, 152]), broll('37736994', [153], '전체 표는 카페에'),
           S('pic', [154], pic=END_PIC, license=f"Pexels 37736994 무료({CR['37736994']['author']})", baked=True, zoom=[1.0, 1.10], cx=50, cy=50)]
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
    if '_need' in d:
        if d['_need'] > d['_have'] + 0.5: short.append((d['src'], d['_need'], d['_have']))
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
    print('H-5 배치 점검:', stat)
    print('아직 없는 것' if MISSING else '재료 다 있음', *sorted(set(MISSING)), sep='\n  ')
    sys.exit(0 if CHECK else 1)

if not os.path.exists(os.path.join(PUB, END_PIC)):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-sseof', '-0.6', '-i', os.path.join(PUB, CR['34438613']['file']),
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

json.dump({'fps': FPS, 'scenes': scenes, 'badge': ''}, open(os.path.join(VID, 'h5.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': n, 'file': CR[n]['file'], 'used': USEDBG[n], 'desc_line': CR[n]['desc_line']} for n in sorted(USEDBG)],
          open(os.path.join(EP, 'bg_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# H5.tsx(JT1.tsx 복사, 이름만) + Root.tsx 등록 — 처음 한 번만
tsx = os.path.join(VID, 'src', 'H5.tsx')
if not os.path.exists(tsx):
    src = open(os.path.join(VID, 'src', 'JT1.tsx'), encoding='utf-8').read()
    src = src.replace('JT1Props', 'H5Props').replace('jt1Frames', 'h5Frames').replace('export const JT1', 'export const H5')
    open(tsx, 'w', encoding='utf-8').write('// H-5(송도 실거래) 롱폼 화면 — 11/17 PD: JT1.tsx 그대로(이름만). props work/video/h5.json ← ep/H-5/h5props.py\n' + src)
root = os.path.join(VID, 'src', 'Root.tsx'); r = open(root, encoding='utf-8').read()
if "from './H5'" not in r:
    r = r.replace("import jt1 from '../jt1.json';", "import jt1 from '../jt1.json';\nimport {H5, H5Props, h5Frames} from './H5';\nimport h5 from '../h5.json';", 1)
    r = r.replace('  const jjt1 = jt1 as unknown as JT1Props;', '  const jjt1 = jt1 as unknown as JT1Props;\n  const hh5 = h5 as unknown as H5Props;', 1)
    i = r.index('<Composition id="JT1"')
    r = r[:i] + ('<Composition id="H5" component={H5 as unknown as React.FC<Record<string, unknown>>} durationInFrames={h5Frames(hh5)} fps={hh5.fps}\n'
                 '      width={1920} height={1080} defaultProps={hh5 as unknown as Record<string, unknown>}\n'
                 '      calculateMetadata={({props: pp}) => ({durationInFrames: h5Frames(pp as unknown as H5Props)})} />\n    ') + r[i:]
    open(root, 'w', encoding='utf-8').write(r)
print(f'H-5 h5.json: {stat} · numcheck {nnum}덩이 불일치 0 · 다음: lfrender.py text → editor stamp → render')
