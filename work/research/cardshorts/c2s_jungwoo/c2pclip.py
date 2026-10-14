# c2s_jungwoo — C-2 롱폼(정우 씨, 10/19 공개 예정) 이야기 줄기를 자른 세로 쇼츠 props · 틀 'c2person' 첫 편 (firemap-motion-designer 2026-10-14)
#   py -3.12 work/research/cardshorts/c2s_jungwoo/c2pclip.py   → work/video/c2s_jungwoo.json + public/c2p/*.png 복사
#   렌더: cd work/video && npx remotion render src/c2p_index.ts C2P out/c2s_jungwoo.mp4 --props=c2s_jungwoo.json
# 틀 c2person(today.md 10/14 지시): 흰 판 대신 장면마다 그림 1장(정우 씨 SVG 시트 visual/N1-person) + 큰 3줄 자막 + 숫자 하나. 장면 길이 8초 이하(그림이 8초마다 바뀜).
# 목소리 = C-2 voice.json 문장 wav 그대로(새 녹음 0, 10/14 Chirp 3 HD Charon) · 줄은 번호가 아니라 말 글자로 찾는다(대본이 바뀌면 assert로 멈춤).
# 숫자 = 그 장면 말 줄 또는 calc_n1_out.txt에 있는 글자만(need) · 해 카드는 calc_n1_out '1998년 1월 시작' 줄의 해.
import os, json, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
VID = os.path.join(WORK, 'video')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'C-2')
ART = os.path.join(WORK, 'research', 'visual', 'N1-person')
V = json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8'))
BYTEXT = {l['text']: l for s in V['sections'] for l in s['lines']}
CALC = open(os.path.join(EP, 'calc_n1_out.txt'), encoding='utf-8').read()
SCRIPT = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
TAIL = 36

def L(t):
    hit = [k for k in BYTEXT if k.startswith(t)]; assert len(hit) == 1, (t, hit)
    l = BYTEXT[hit[0]]; assert l.get('audio') and os.path.exists(os.path.join(VID, 'public', l['audio'])), t
    return {'text': l['text'], 'audio': l['audio'], 'frames': l['frames']}

def need(x, where):
    assert x in where, f'원문에 없음: {x}'

# 그림 = (파일, 인물 가운데 x(1920 기준, 남색 옷 픽셀 평균 — 10/14 잼), 확대 시작·끝, 가로 흔들림 px)
PIC = {'s1998': 1079, 's2001': 599, 's2002': 899, 's2009': 860, 's2010': 859, 's2011': 859}
os.makedirs(os.path.join(VID, 'public', 'c2p'), exist_ok=True)
for k in PIC: shutil.copyfile(os.path.join(ART, k + '.png'), os.path.join(VID, 'public', 'c2p', k + '.png'))

def sc(pic, year, lines, num, sub, *, zoom=(1.0, 1.08), pan=0, focus=0.36, gray=False, blur=False, red=(), green=()):
    ls = [L(t) for t in lines]
    spoken = ' '.join(l['text'] for l in ls)
    for d in [x for x in __import__('re').findall(r'\d[\d,]*', num + ' ' + sub)]:
        assert d in spoken or d in CALC, f'숫자 {d} — 말 줄·calc에 없음'
    if year:
        for y in __import__('re').findall(r'\d{4}', year): need(y, CALC)
    fr = sum(l['frames'] for l in ls)
    return {'pic': f'c2p/{pic}.png', 'cx': PIC[pic], 'year': year, 'num': num, 'sub': sub, 'zoom': list(zoom), 'pan': pan, 'focus': focus,
            'gray': gray, 'blur': blur, 'red': list(red), 'green': list(green), 'lines': ls, 'frames': fr}

scenes = [
    sc('s1998', '1998년 1월', ['퇴직금 3억을 미국 대형주', '"매달 200만원씩만 팔아 쓰자'], '3억', '매달 200만원씩 팔아 쓰기', zoom=(1.3, 1.0), pan=-30, green=['평생']),
    sc('s1998', '1998년 1월', ['이 통장은 언제 바닥났을까요?'], '언제 바닥?', '같은 돈 · 같은 규칙', zoom=(1.35, 1.45), focus=0.42, red=['바닥났을까요']),
    sc('s2001', '2000~2002년', ['셋째 해부터 지수가 내리', '떨어진 값에 팔면, 같은 돈을'], '3년 연속 하락', '지수(달러 기준) · 떨어진 값에 팔기', zoom=(1.04, 1.12), pan=24, red=['떨어졌어요', '더', '많이']),
    sc('s2002', '2002년', ['"올해도 팔아야 하나."', '하락 셋째 해가 끝났을 때'], '1억 6천만원', '하락 셋째 해 말 통장', zoom=(1.12, 1.02), pan=-20, red=['1억 6천만원이']),
    sc('s2009', '2007~2008년', ['금융위기 직전, 통장은', '그리고 금융위기가 왔어요.'], '1억 밑', '금융위기 직전 통장', zoom=(1.0, 1.06), pan=-24, focus=0.4, red=['밑으로', '금융위기가']),
    sc('s2009', '2009년', ['이듬해엔 지수가 다시 올랐어요.', '그런데 연초에 한 해 치를 꺼내고'], '3천만원도 안 됨', '연초에 꺼내고 남은 오를 돈', zoom=(1.3, 1.4), focus=0.45, pan=30, green=['올랐어요'], red=['안']),
    sc('s2010', '2010년', ['그해 말 통장에 남은 돈은'], '1,150만원', '그해 말 남은 돈', zoom=(1.2, 1.3), focus=0.45),
    sc('s2011', '2011년 1월', ['그리고 2011년 1월, 정우 씨는'], '못 꺼냈다', '한 해 치를 처음으로', zoom=(1.0, 1.07), pan=-26, red=['못']),
    sc('s2011', '2011년 1월', ['시작한 지 열네 해째'], '68살', '시작한 지 14년째', zoom=(1.4, 1.5), focus=0.4),
    sc('s2011', '2003년 시작 → 2025년 말', ['같은 돈, 같은 규칙으로 5년 늦게'], '2억 넘게', '다른 사람 · 5년 늦게 시작', zoom=(1.08, 1.0), gray=True, blur=True, green=['2억', '넘게']),
    sc('s1998', '1998년 1월', ['둘을 가른 건 고른 상품이'], '시작한 해', '37번 시작 중 바닥 6번 · 2025년까지', zoom=(1.0, 1.12), pan=20, red=['시작한', '해였습니다']),
]
need('14', CALC); need('1,154만원', CALC); need('3.00', CALC)   # 68살 = 1998년 55세 + 13 (script.md 인물 줄)
need('1998년 55세', SCRIPT); need('2003년 1월 시작 → 2025년 말 2.72억원', CALC); need('총 6/37', CALC); need('2008: 0.87', CALC)   # 2007년 말 0.87억 = 1억 밑
for s in scenes: assert s['frames'] <= 8 * 30 + 30, (s['num'], s['frames'])   # 그림 8초(+줄 끝 숨 1초) 안
scenes[-1]['frames'] += TAIL
p = {'fps': 30, 'name': 'c2s_jungwoo', 'layout': 'c2person', 'question': ['3억, 매달 200만원', '언제 바닥났을까'], 'hot': '바닥',
     'badge': '가상 인물 · 지수·환율은 실제, 통장은 계산', 'base': 'S&P500 총수익 · 한국은행 환율 · 1월에 1년 치 매도 · 물가 미반영', 'scenes': scenes}
json.dump(p, open(os.path.join(VID, 'c2s_jungwoo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fr = sum(s['frames'] for s in scenes)
print(f'c2s_jungwoo: {fr} 프레임 = {fr / 30:.1f}초 · 장면 {len(scenes)} · 최장 장면 {max(s["frames"] for s in scenes) / 30:.1f}초 · 첫 줄 "{scenes[0]["lines"][0]["text"]}"')
