# t1s_live — T-1 롱폼 2장 '살았던 햇수'(정부안 2029년 장기보유특별공제→거주만)를 자른 세로 쇼츠 props · 판 없는 꼴(M1S v2 look 'live', 10/19 클로드 티 금지) (firemap-video-producer 2026-10-21)
#   py -3.12 work/research/cardshorts/t1s_live/t1lclip.py   → work/video/t1s_live.json
#   렌더: cd work/video && npx remotion render src/m1s_index.ts M1S out/t1s_live.mp4 --props=t1s_live.json
# 목소리 = T-1 voice.json 문장 wav 그대로(새 녹음 0) · 줄은 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤)
# 숫자 = 그 장면 말 줄 또는 T-1 research.md·calc 출력에 있는 글자만 · 배경 = ep/T-1/stock/credits.json Pexels 클립(video/public/bg/t1)
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'T-1')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
SRC = ''.join(open(os.path.join(EP, f), encoding='utf-8').read() for f in ('research.md', 'calc_more_out.txt', 'calc_out.txt') if os.path.exists(os.path.join(EP, f)))
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
        assert d in spoken or d in SRC, f'숫자 {d} — 말 줄·T-1 원문에 없음'
    return {'kind': 'vs', 'label': label, 'source': None, 'data': data, 'lines': ls, 'frames': sum(l['frames'] for l in ls)}


# 10/21 06:2x: 첫 줄 2:20 '수진 씨는 해마다 줄어서, 2029년엔 16%만 남습니다.'(32자·숫자, 꼴 관문 ⓐ) · 정부안이라 답 칸에 '정부안·국회 통과 전'
# 4~15초 줄: 둘째·셋째 줄 = 답의 이유(10년 갖고 2년만 삶 → 지금 48%) · 방법·가정 줄 없음 · 팔 시기 권유 0(끝은 '세는 법')
# 10/21 06:5x 이해 시험 1차(40·50·60세 3/3 뜻 맞음) 반영: 셋 다 '수진 씨가 누군지'·'48%가 어떻게'·'해마다 3천만원이 매년 낸다는 뜻?'·'2028년은?'·'10년 넘는 내 집은?' 헷갈림
#   → 첫 장면에 '가상 인물 수진 씨·12억 넘게 판 집 한 채' · 48% = 10년×4% + 2년×4% · 2028년 줄(2:13·2:14) 더함 · 3천만원 = 판 해별 세금 세 칸 · '2029년 = 살았던 해 × 8%(최대 80%)'
#   · '둘 다 10년 이하일 때'는 화면만(2:39 뺌), 2:22 뺌(길이)
# 10/21 07:2x 0초 화면에 답 숫자(쇼츠 제목 규칙): 첫 판 '가상 인물 수진 씨 / 지금 48%'를 0프레임부터, '12억 넘게 판 집'은 둘째 장면 옆 글 위로
# 10/21 07:1x 끝 줄 2:36(등본 전입~전출)은 지난 주소 이력이 등본에 안 나올 수 있어 빼고 2:35(갖고 있던 햇수 = 잔금일~잔금일)로 · 0초 답 칸 '12억 넘는 집 한 채'
# 10/21 07:0x 이해 시험 2차: 12년 보유 50세가 '−4%포인트' 셈법(둘 다 10년 이하에만 맞음)에서 막힘 → 2:40 줄 빼고 누구나 셀 수 있는 '지금 = 갖고×4% + 살았던×4%, 2029년 = 살았던×8%, 각각 10년까지'
scenes = [
    sc('2029년 공제', ['수진 씨는 해마다 줄어서'],
       {'tiles': [['가상 인물 수진 씨', '지금 48%', '', 0, 'ink'], ['2029년, 정부안', '16%', '', 40, 'ink']]}),
    sc('48%는 어떻게', ['수진 씨도 똑같이 10년을', '그래서 48%에 그치고요.'],
       {'tiles': [['갖고 있던 10년×4%', '40%', '', 0, 'ink'], ['살았던 2년 × 4%', '8%', '', 80, 'ink']], 'side': ['지금 법 48%', 130, '12억 넘게 판 집']}),
    sc('정부안', ['이제 정부안이에요.', '2028년엔 살았던', '대신 갖고 있던 해는 2%', '정부안대로라면 2029년부터는 갖고'],
       {'tiles': [['2028년', '살았던 해 6% · 갖고 있던 해 2%', '', 115, 'ink'], ['2029년부터', '살았던 해 × 8%', '', 290, 'ink']], 'side': ['10년 살면 80%', 330, '2029년 최대']}),
    sc('판 해만 달라도', ['같은 집을 판 해만 다르게'],
       {'tiles': [['2027년까지(지금 법)', '8,135만원', '', 0, 'ink'], ['2028년', '1억 1,398만원', '', 60, 'ink'], ['2029년', '1억 4,777만원', '', 120, 'ink']], 'side': ['1년 늦을수록 +3천만원', 150, '수진 씨 세금']}),
    sc('내 집 셈법', ['그래서 내 집이라면'],
       {'tiles': [['지금 법', '두 햇수 × 4%씩', '', 0, 'ink'], ['2029년 정부안', '살았던 해 × 8%', '', 75, 'ink']], 'side': ['각각 10년까지', 120, '햇수는']}),
    sc('갖고 있던 햇수 세기', ['갖고 있던 햇수는 산 날부터'],
       {'tiles': [['갖고 있던 햇수', '산 날 → 판 날', '', 20, 'ink']], 'side': ['잔금 치른 날', 80, '날짜는']}),
]
need = ['48%', '16%', '8%', '4%', '2029', '8,135', '11,398', '14,777', '최대 80']
for x in need: assert x in SRC, f'원문에 없음 {x}'
scenes[-1]['frames'] += TAIL
# 배경: 줄마다 말을 받는 그림 하나 — (줄 번호, 클립, 시작 초)
BG = [(1, '35082942', 0), (2, '31400388', 2), (3, '1793371', 1), (4, '8478946', 2), (5, '1793371', 6), (6, '32986074', 1), (7, '6221101', 1),
      (8, '8471105', 3), (9, '7710453', 2), (10, '7710495', 2)]
allines = [l for s in scenes for l in s['lines']]
assert len(allines) == len(BG), (len(allines), len(BG))
bg = []; at = 0
for (k, cid, st), l in zip(BG, allines):
    fr = l['frames'] + (TAIL if k == len(BG) else 0)
    assert os.path.exists(os.path.join(VID, 'public', 'bg', 't1', cid + '.mp4')), cid
    assert CRED[cid]['sec'] - st >= fr / 30 + 0.3, (cid, CRED[cid]['sec'], fr / 30)
    bg.append({'src': f'bg/t1/{cid}.mp4', 'from': at, 'frames': fr, 'start': st}); at += fr
credits = ' · '.join(sorted({f"{c} {CRED[c]['author'].strip()}" for _, c, _ in BG})) + ' (Pexels License)'
p = {'fps': 30, 'name': 't1s_live', 'v': 2, 'look': 'live', 'question': ['10년 갖고 2년만 산 집', '양도세 공제 2029년엔?'], 'hot': '2029년',
     'answer': {'label': '12억 넘는 집 한 채 · 정부안', 'items': ['지금 48%', '2029년 16%'], 'arrow': False, 'note': '2029년 = 살았던 해 × 8%'},
     'base': '재정경제부 2026 세법개정안(국회 제출, 통과 전) · 소득세법 §95② · 가상 인물 계산', 'long': 'Qg5Tj2fuJ3A',
     'scenes': scenes, 'bg': bg, 'credits': credits}
json.dump(p, open(os.path.join(VID, 't1s_live.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f't1s_live: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 배경 {len(bg)}컷(최장 {max(b["frames"] for b in bg) / 30:.1f}초)')
print('credits:', credits)
