# P-1 '5. 519만원 위의 계단' StepCliff 미리보기 props (2026-10-13 motion)
# 숫자: calc_out 4절·facts [F4]·script 자막 원문만 — 아래 assert로 원문에 있는 글자인지 본다. 곡선은 제63조의2 식, calc_out 점 4개와 원 단위로 맞는지 assert.
# 길이: voice.json 있으면 실제 녹음 프레임, 없으면 G-1 녹음 속도(p1timing.py와 같은 값) 어림.
#   py -3.12 work/research/longform/ep/P-1/motion_preview/stepprops.py  → p1_step.json
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
FPS = 30
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
facts = open(os.path.join(EP, 'facts.txt'), encoding='utf-8').read()
src_all = txt + calc + facts
sec = next(s for s in SC.parse(script) if s['title'].startswith('5.'))
says = sec['lines']; assert len(says) == 15, len(says)
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
    elif s.startswith('[자막:') and last: caps[last] = s[4:].rstrip(']').strip()
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(H, 'p1_timing.json'), encoding='utf-8'))['spf']
lines = []
for t in says:
    v = voice.get(t)
    lines.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': v['audio'] if v else None})
beats, a = [], 0
for l in lines: beats.append(a); a += l['frames']

# 숫자 검산 — 만원 단위 곡선(제63조의2, 1·2구간 폐지 뒤): 초과 200~300만 15만+15% · 300~400만 30만+20% · 400만~ 50만+25% · 상한 노령연금 절반
A = 319.3511; GAP = 200; CAP = 50
tiers = [[200, 15, 0.15], [300, 30, 0.20], [400, 50, 0.25]]
def cut(x):
    e = x - A
    if e < GAP: return 0
    v = 0
    for lo, base, k in tiers:
        if e >= lo: v = base + (e - lo) * k
    return min(v, CAP)
for x, won in [(519.3511, 150000), (600, 270973), (700, 461298), (800, 500000)]:
    assert abs(cut(x + 1e-9) * 10000 - won) < 1, (x, cut(x) * 10000)
    assert f'{won:,}원' in calc
for x in (300, 400, 500): assert cut(x) == 0 and f'공제 뒤 월 {x*10000:,}원' in calc
for w in ['3,193,511원', '5,193,511원', '75,865,402원', '6,322,117원', '319만 3,511원', '519만 3,511원', '+200만원', '15만원', '노령연금액의 2분의 1', '최대 5년', '1969년생 65세']:
    assert w in src_all, w

step = {'seed': 'P-1-step', 'xMin': 280, 'xMax': 860, 'yMax': 56, 'a': A, 'gap': GAP, 'cap': CAP, 'tiers': tiers,
        'xticks': [300, 400, 500, 600, 700, 800], 'yticks': [[0, '0원'], [15, '15만'], [30, '30만'], [50, '50만']],
        'oldText': '옛 기준 319만 3,511원', 'newText': '519만 3,511원', 'plusText': '+200만원', 'zeroText': '519만원 아래: 깎이는 돈 0원',
        'axisX': '공제 뒤 월 소득', 'axisY': '한 달에 깎이는 돈 (연금 월 100만원 가정)',
        'notWage': '월급 그대로 ✕', 'formula': ['총급여(비과세 제외)', '− 근로소득공제', '= 근로소득금액'],
        'salary': ['75,865,402원', '한 해 · 월 6,322,117원'], 'ask': '조문대로 계산하면?', 'jumpText': '15만원', 'stair': '계단',
        'pts': [{'x': 600, 'text': '600만 → 270,973원', 'at': beats[10] + 20}, {'x': 700, 'text': '700만 → 461,298원', 'at': beats[10] + 40},
                {'x': 800, 'text': '800만 → 500,000원', 'at': beats[11] + 24}],
        'capText': ['상한 = 노령연금의 절반', '50만'], 'period': ['65세', '70세', '깎이는 기간 최대 5년 (1969년생 65세부터)'],
        'slips': ['519만원 바로 아래', '감액 0원', '519만원 바로 위', '감액 15만원'], 'zone': '이 계단 자리', 'beats': beats}
assert '519만원 바로 아래 0원' in txt and '바로 위 15만원' in txt and '총급여 − 근로소득공제' in txt
scene = {'key': 'step', 'kind': 'step', 'title': '519만원 위의 계단', 'sub': '일하면서 제때 받을 때 · 국민연금법 제63조의2 (2026-06-17 시행)',
         'source': '국민연금법 제63조의2·시행령 제45조① · 보건복지부 보도자료 · 파이어맵 계산(조문대로)', 'chapter': '5장', 'lines': lines, 'frames': a + 20}
json.dump({'scene': scene, 'step': step}, open(os.path.join(H, 'p1_step.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('frames', scene['frames'], f'({scene["frames"]/FPS:.1f}초)', 'missing voice', sum(1 for l in lines if not l['audio']), 'beats', beats)
