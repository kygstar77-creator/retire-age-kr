# G-1 '6. 산 값까지의 산수' AsymClimb 미리보기 props (2026-10-10 motion)
# 숫자는 calc_out.txt 첫 줄(KRX 오늘·1년 고점·고점 대비 %·돌아가려면 %)만 쓴다 — g1props가 파싱·검산(assert)한 값을 그대로 받는다.
# 화면에 새 숫자(차액 90,810원 등)는 만들지 않는다: '같은 폭'은 글자 없이 높이로만 보인다.
# 말 구간: script.md '6.' 장 전체(PD 장면 math 자리).
#   py -3.12 work/research/longform/ep/G-1/motion_preview/asymprops.py  → g1_asym.json
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(H))
import g1props as G
SC = G.SC
script = os.path.join(G.EP, 'script.md')
txt = open(script, encoding='utf-8').read()
G.check_script(txt)
chap = lambda t: re.sub(r'^\[', '', t).split()[0].rstrip(']')
sec = next(s for s in SC.parse(script) if chap(s['title']) == '6.')
says = sec['lines']
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = re.sub(r'\s*\(화면.*$', '', s[2:]).strip()
    elif s.startswith('[자막:') and last: caps[last] = s[4:].rstrip(']').strip()
voice = {}
vj = os.path.join(G.EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
lines = []
for t in says:
    v = voice.get(t)
    lines.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / G.RATE * G.FPS)), 'audio': v['audio'] if v else None})

def A(w, plus=0):
    """w가 든 문장 안에서 w가 시작하는 프레임(문장 안 위치는 음절 비례 어림)."""
    j = next((j for j, x in enumerate(lines) if w in x['text']), -1); assert j >= 0, w
    t = lines[j]['text']; pre = t[:t.index(w)]
    inside = round(lines[j]['frames'] * SC.syl(SC.speak(pre)) / max(1, SC.syl(SC.speak(t)))) if pre.strip() else 0
    return sum(x['frames'] for x in lines[:j]) + inside + plus

# 숫자 — calc_out 첫 줄(g1props 검산 통과분)
NOWP, PEAKP, PEAKPCT, BACK = G.NOWP, G.PEAKP, G.PEAKPCT, G.BACK
assert abs((PEAKP - NOWP) / PEAKP * 100 + G.pc(PEAKPCT)) < 0.005        # 내려온 폭 = 고점 기준 33.66%
assert abs((PEAKP / NOWP - 1) * 100 - float(BACK)) < 0.05                 # 올라갈 폭 = 오늘 기준 50.7%
# 대본 말과 숫자 결(화면 글자가 말보다 앞서지 않게)
assert '51% 올라야' in txt and '34% 떨어진 걸 메우는 데 51%' in txt and '떨어진 만큼만 올라서는 모자라요' in txt
assert f'{G.won(PEAKP)} ÷ {G.won(NOWP)} − 1 = +{BACK}%' in txt

asym = {'seed': 'G-1-asym', 'top': PEAKP, 'now': NOWP,
        'peakText': f'{G.won(PEAKP)}원', 'nowText': f'{G.won(NOWP)}원',
        'peakName': f'1월 고점 {G.dot(G.PEAKD)}', 'nowName': f'오늘 {G.dot(G.ASOF)}',
        'downText': G.M(PEAKPCT) + '%', 'upText': '+' + BACK + '%',
        'downBase': f'{G.won(PEAKP)}원의 {PEAKPCT.lstrip("-")}%', 'upBase': f'{G.won(NOWP)}원의 {BACK}%',
        'intro': 0,
        'drop': A('고점에 산 금이', 0),          # 고점 막대 위 몫이 '내려온 폭'으로 바뀜
        'slide': A('지금부터', 0),               # 오늘 값 막대가 오른쪽 칸으로
        'climb': A('51% 올라야', 0),             # 올라갈 폭이 쌓여 고점 선까지
        'base': A('34% 떨어진', 0),              # 기준 괄호 두 개 + 같은 폭
        'short': A('떨어진 만큼만', 0),           # 34%만 오르면 → 모자람
        'shortText': '34%만 오르면', 'shortLack': '모자라요',
        'fee': ['수수료·팔 때 값 차이는 뺀 숫자', A('이것도', 0)],
        'calm': '전망 아님, 산수'}
scene = {'key': 'math', 'kind': 'asym', 'title': '산 값까지의 산수', 'sub': f'1월 고점에 산 금 · 1g {G.won(NOWP)}원 → {G.won(PEAKP)}원 · 막대 높이 = 1g 값(0부터)',
         'source': G.SRC_KRX + ' · 전망 아님, 산수', 'chapter': '6장', 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 20}
json.dump({'scene': scene, 'asym': asym}, open(os.path.join(H, 'g1_asym.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('frames', scene['frames'], 'missing voice', sum(1 for l in lines if not l['audio']), {k: asym[k] for k in ('drop', 'slide', 'climb', 'base', 'short')}, asym['fee'][1])
