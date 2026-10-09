# G-1 '3. 세 조각' 폭포 막대 WaterfallPieces 미리보기 props (2026-10-09 motion)
# 숫자는 calc_out.txt '세 조각 분해' 1년 전 줄만 쓴다 — g1props가 파싱·곱 검산(assert)한 DEC를 그대로 받고, 여기서 막대 몫(%p)도 calc_out과 대조.
# 말 구간: script.md '3.' 장 '작년 영수증부터' ~ 장 끝(PD 장면 piece1·prem·piece1b 자리를 한 장면으로).
#   py -3.12 work/research/longform/ep/G-1/motion_preview/wfprops.py  → g1_wf.json
import json, os, sys, re, math
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(H))
import g1props as G
SC = G.SC
script = os.path.join(G.EP, 'script.md')
txt = open(script, encoding='utf-8').read()
G.check_script(txt)
chap = lambda t: re.sub(r'^\[', '', t).split()[0].rstrip(']')
sec = next(s for s in SC.parse(script) if chap(s['title']) == '3.')
i0 = next(j for j, t in enumerate(sec['lines']) if t.startswith('작년 영수증부터'))
says = sec['lines'][i0:]
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
    j = next((j for j, x in enumerate(lines) if w in x['text']), -1); assert j >= 0, w
    return sum(x['frames'] for x in lines[:j]) + plus

lab = '1년 전'; d = G.DEC[lab]; dt = G.D[lab][1]
xs = [G.pc(d['usd']), G.pc(d['fx']), G.pc(d['prem'])]; tot = G.pc(d['tot'])
# 막대 몫 = 로그 비율로 나눈 %p(합이 정확히 전체) — calc_out 괄호 안 %p와 한 자리까지 같아야 한다
lg = [math.log(1 + x / 100) for x in xs]
pp = [g / sum(lg) * tot for g in lg]
row = re.search(r'^\| 1년 전 \d{4}-\d\d-\d\d \| [^|]+\| [^(]+\(([+\-][\d.]+)%p\) \| [^(]+\(([+\-][\d.]+)%p\) \| [^(]+\(([+\-][\d.]+)%p\) \|', G.CO, re.M)
assert row, 'calc_out 세 조각 %p 못 찾음'
for k in range(3): assert f'{pp[k]:+.1f}' == row[k + 1], (k, pp[k], row[k + 1])
assert abs(sum(pp) - tot) < 1e-9
krx = G.D[lab][3]['KRX']   # (9,556,861원, -4.43%)
assert krx[1] == d['tot']
# 대본 말과 숫자 결이 맞는지(화면 글자가 말보다 앞서지 않게)
assert '7% 가까이 올랐' in txt and '3% 넘게 깎' in txt and '7% 넘게 깎' in txt and '4% 남짓 손실' in txt
note = '금값이 아니라 환율·웃돈에서 잃었다'
assert '금값이 아니라 환율과 웃돈에서 잃은' in txt

wf = {'seed': 'G-1-wf', 'min': -8, 'max': 7.5, 'zeroText': f'{G.dot(dt)} 산 값 = 0',
      'steps': [
          {'name': '달러 금값', 'sub': '금 선물 GC=F', 'pp': pp[0], 'text': d['usd'] + '%', 'at': A('첫 조각', 6)},
          {'name': '환율', 'sub': '원/달러 매매기준율', 'pp': pp[1], 'text': G.M(d['fx']) + '%', 'at': A('둘째 조각', 10)},
          {'name': 'KRX 웃돈', 'sub': '국제값 어림 대비', 'pp': pp[2], 'text': G.M(d['prem']) + '%', 'at': A('셋째 조각이', 6)}],
      'total': {'name': '= 내 금', 'sub': 'KRX 금 1년', 'pp': tot, 'text': G.M(d['tot']) + '%', 'won': f'1천만원 → {G.won(krx[0])}원', 'at': A('세 조각을 곱하면', 6)},
      'prem': [[f'웃돈 그때 {G.M(d["p0"])}%', A('작년엔', 4)], [f'지금 {G.M(d["p1"])}%', A('지금은 오히려', 4)]],
      'hit': A('이 웃돈이 빠진', 4),
      'note': [note, A('그러니까', 4)], 'intro': 0}
scene = {'key': 'wf1', 'kind': 'waterfall', 'title': f'{G.SHORT[lab]}에 산 영수증, 세 조각', 'sub': f'{G.dot(dt)} → {G.dot(G.ASOF)} · 곱이라 % 단순 합과 다름 · 막대 = 몫(%p), 합 = 내 금',
         'source': G.SRC_DEC, 'chapter': '3장', 'lines': lines, 'frames': sum(l['frames'] for l in lines) + 20}
json.dump({'scene': scene, 'wf': wf}, open(os.path.join(H, 'g1_wf.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('frames', scene['frames'], 'missing voice', sum(1 for l in lines if not l['audio']), [round(x, 3) for x in pp], [s['at'] for s in wf['steps']], wf['total']['at'], wf['note'][1])
