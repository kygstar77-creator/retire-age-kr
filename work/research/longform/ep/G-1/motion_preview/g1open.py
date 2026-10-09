# G-1 첫 장면 BuyDateOpen 미리보기 props — 숫자는 g1props.py가 calc_out.txt·raw로 검산한 값만 쓴다(여기서 다시 assert).
# 말·길이: script.md '0.' 장 첫 3문장, voice.json 있으면 그 길이, 없으면 g1props와 같은 어림(음절 ÷ 5.65).
#   py -3.12 work/research/longform/ep/G-1/motion_preview/g1open.py  → g1_open.json
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(H))
import g1props as G
SC = G.SC
script = os.path.join(G.EP, 'script.md')
txt = open(script, encoding='utf-8').read()
G.check_script(txt)
sec = next(s for s in SC.parse(script) if s['title'].lstrip('[').startswith('0.'))
says = sec['lines'][:3]
assert says[0].startswith('올해 1월, 금값이 꼭대기였던 날 천만원어치를 샀다면 지금 ') and says[1].startswith('그런데 작년 이맘때') and says[2].startswith('같은 금인데'), says
caps = {}
last = None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
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
st = [0]
for l in lines: st.append(st[-1] + l['frames'])

D = G.D; K = {lab: P['KRX'] for lab, _, _, P in G.DATES}
# 산 날은 솎아 내지 않는다(10/9: 2칸 솎기에서 2025-10-02가 빠져 1년 전 점이 199,730원 자리에 찍혔다)
KEEP = {G.PEAKD, G.D['1년 전'][1], G.ASOF}
pts = [r for i, r in enumerate(G.KRX) if i % 2 == 0 or r[0] in KEEP or i == len(G.KRX) - 1]
vals = [round(v / 1000) for _, v in pts]
idx = lambda d: next(i for i, (x, _) in enumerate(pts) if x == d)
man = lambda w: f'{round(w / 10000)}만원'
peak, ago = K['1년 고점'], K['1년 전']
assert man(peak[0]) in says[0] and man(ago[0]) in says[1], (man(peak[0]), man(ago[0]), says[:2])   # 대본 말과 같은 반올림(공개 전날 calc 재실행해도 손 안 대고 따라감)
hookTop = '올해 1월, 금값이 꼭대기였던 날 천만원어치를 샀다면'; hookBig = '지금 ' + man(peak[0])
assert hookTop in says[0] and hookBig in says[0]
sameText = '같은 금, 산 날만 달랐다'
assert '같은 금인데, 산 날만 달랐던' in says[2]
buys = [
    {'i': idx(G.PEAKD), 'v': vals[idx(G.PEAKD)], 'date': G.dot(G.PEAKD), 'value': peak[0], 'text': man(peak[0]), 'pct': G.M(peak[1]) + '%', 'at': 0},
    {'i': idx(D['1년 전'][1]), 'v': vals[idx(D['1년 전'][1])], 'date': G.dot(D['1년 전'][1]), 'value': ago[0], 'text': man(ago[0]), 'pct': G.M(ago[1]) + '%', 'at': st[1] + 6},
]
assert pts[buys[0]['i']] == (G.PEAKD, G.PEAKP) and pts[buys[1]['i']] == (D['1년 전'][1], D['1년 전'][2])   # 점 = 그날 실제 종가
open_ = {'seed': 'G-1', 'hookTop': hookTop, 'hookBig': hookBig, 'hookOut': 50,
         'pts': vals, 'min': 150, 'max': 290, 'ticks': [[160, '16만'], [200, '20만'], [240, '24만'], [280, '28만']], 'xlabels': G.months(pts), 'draw': 52,
         'now': [round(G.NOWP / 1000), f'오늘 {G.won(G.NOWP)}원'], 'paid': 10_000_000, 'paidText': '1천만원', 'buys': buys, 'same': st[2] + 4, 'sameText': sameText}
scene = {'key': 'open', 'kind': 'open', 'title': '금 1천만원어치, 지금 얼마?', 'sub': f'같은 금 · 산 날만 다르다 · {G.ASOF} KRX 금시장 종가 기준',
         'source': G.SRC_KRX + ' · ' + G.PAST, 'chapter': None, 'lines': lines, 'frames': st[-1] + 30}
json.dump({'scene': scene, 'open': open_}, open(os.path.join(H, 'g1_open.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('frames', st, 'missing voice', sum(1 for l in lines if not l['audio']), buys)
