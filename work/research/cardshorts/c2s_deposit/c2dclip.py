# c2s_deposit — C-2 롱폼 5장 '차라리 예금은요?'를 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live', 10/19 클로드 티 금지) (firemap-video-producer 2026-10-20)
#   py -3.12 work/research/cardshorts/c2s_deposit/c2dclip.py   → work/video/c2s_deposit.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/c2s_deposit.mp4 --props=c2s_deposit.json
# 목소리 = C-2 voice.json 문장 wav 그대로(새 녹음 0) · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# 숫자 = 그 장면 말 줄 또는 C-2 research.md·calc 출력에 있는 글자만 · 배경 = ep/C-2/stock/credits.json Pexels 클립(video/public/bg/c2, 얼굴·간판 없음 눈 확인)
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'C-2')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_n1_out.txt') if os.path.exists(os.path.join(EP, f)))
CRED = {str(c['id']): c for c in json.load(open(os.path.join(EP, 'stock', 'credits.json'), encoding='utf-8'))}
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
    walk(data)   # 글자 칸만(줄 위치 숫자 0.6·1.4 같은 배치 값은 뺌)
    for d in re.findall(r'\d[\d,.]*', ' '.join(strs)):
        d = d.rstrip('.,')
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·C-2 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 10/20 02:5x: 첫 줄은 꼴 관문 ⓐ(숫자 있음·35자 이하) — 옛 첫 줄 5:2 '대신 지난 기록에서…'(45자·숫자 없음)·5:5 '다음은…' 뺌, 끝에 계산 한계 5:26
# 박자 at = 장면 안 프레임(숫자 든 값은 말에 맞춰 parts/safeframe beatsOf가 다시 잡음) · 꼬리말(kicker) 12자 이하만 보임
# 10/20 03:0x 이해 시험 1차(40·50·60세) 셋 다 '정우 씨가 S&P500 쪽인지'·'2003년 반대가 뭔지'·'민수 씨가 누군지' 헷갈림 → 꼬리말로 풂
scenes = [
    sc('예금 통장이 바닥난 해', ['같은 규칙이면, 예금 통장은', '2011년에 바닥난 정우 씨보다'],
       {'tiles': [['예금 통장 바닥', '2018년 1월', '', 0, 'ink'], ['S&P500은 바닥', '2011년', '', 119, 'ink']], 'side': ['일곱 해 더', 180, '예금이 더 간 기간']}),
    sc('왜 예금이 이겼나', ['왜 예금이 이겼을까요?', '그 뒤 세 해도 금리가', '외환위기 때라 은행 이자가'],
       {'tiles': [['그동안 지수는', '하락', '', 300, 'ink'], ['2025년 1월 금리', '3%대', '', 470, 'ink']], 'side': ['15% 넘음', 120, '1998년 예금 금리']}),
    sc('2003년에 시작했다면', ['민수 씨처럼 2003년에 시작했다면', '예금은 2019년에 바닥났어요.'],
       {'tiles': [['2003년 시작이면', '반대', '', 0, 'ink'], ['예금은 바닥', '2019년', '', 98, 'ink']], 'side': ['2억 7천만원', 214, 'S&P500은 남음']}),
    sc('가른 건 시작한 해', ['1998년엔 예금 이자가 15%를'],
       {'tiles': [['1998년 예금 이자', '15% 넘음', '', 0, 'ink'], ['2003년 예금 이자', '5% 안 됨', '', 96, 'ink']], 'side': ['시작한 해', 150, '둘을 가른 것']}),
    sc('계산에서 뺀 것', ['조심할 점이 있어요. 예금 계산도'],
       {'tiles': [['이자 세금', '지금 세율로', '', 60, 'ink'], ['건보료', '안 넣음', '', 150, 'ink']]}),
]
need = ['2018년 1월', '15.85', '2.72억', '3.06']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나(분위기용 금지) — (줄 번호, 클립, 시작 초)
BG = [(1, '31602655', 0), (2, '34282980', 0), (3, '12033695', 1), (4, '6785719', 2), (5, '7118320', 1),
      (6, '6219901', 3), (7, '12412380', 1), (8, '6651088', 0), (9, '5562942', 4)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG)
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 'c2', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/c2/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 'c2s_deposit', 'v': 2, 'look': 'live', 'question': ['3억, 매달 200만원', '예금이면 더 오래 갔을까'], 'hot': '예금',
     'answer': {'label': '가상 인물 정우 씨 · 1998년 1월 시작', 'items': ['S&P500 2011년 바닥', '예금 2018년 바닥'], 'arrow': False, 'note': '2003년 시작이면 반대 — S&P500이 남음'},
     'base': '한국은행 정기예금 금리 · S&P500 총수익 · 한국은행 환율 · 물가 미반영 · 지나간 기록', 'long': 'SGx7UD-6RNE',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 'c2s_deposit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'c2s_deposit: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
