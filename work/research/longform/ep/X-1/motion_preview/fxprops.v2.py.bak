# X-1 '1. 왜 날짜가 네 개인가'·'2. 달러로만 바꿔 뒀다면' FxDates 미리보기 props (2026-10-16 motion)
# 선 = 한국은행 ECOS 731Y001 원/달러 매매기준율 일별 원문(raw/ecos_731Y001_20261013.json) 2025.10.13~2026.10.12 그대로.
# 화면 글자 숫자는 calc_out·script(말·자막)에 있는 것만(assert). 막대 높이 = 그날 바꾼 1억의 10/12 원화 값(0부터).
# 길이: ep/X-1/voice.json 있으면 실제 녹음 프레임, 없으면 P-1 녹음 속도(p1_timing.json spf) 어림.
#   py -3.12 work/research/longform/ep/X-1/motion_preview/fxprops.py  → x1_fx.json
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
src_all = txt + calc
secs = SC.parse(script)
s1 = next(s for s in secs if s['title'].startswith('1.')); s2 = next(s for s in secs if s['title'].startswith('2.'))
assert len(s1['lines']) == 3 and len(s2['lines']) == 7, (s1['lines'], s2['lines'])
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
    elif s.startswith('[자막:') and last and last not in caps: caps[last] = s[4:].rstrip(']').strip()
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(EP, '..', 'P-1', 'motion_preview', 'p1_timing.json'), encoding='utf-8'))['spf']
def mk(says):
    out = []
    for t in says:
        v = voice.get(t)
        out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'] if v else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': v['audio'] if v else None})
    b, a = [], 0
    for l in out: b.append(a); a += l['frames']
    return out, b
L1, B1 = mk(s1['lines']); L2, B2 = mk(s2['lines'])
# 셋째 줄 안 이름 네 개 시점 = 음절 비례
t3 = s1['lines'][2]; sp3 = SC.speak(t3); n3 = SC.syl(sp3)
def word_at(w):
    k = sp3.index(SC.speak(w)); return B1[2] + round(L1[2]['frames'] * SC.syl(sp3[:k]) / n3)

# 원문 선
u = json.load(open(os.path.join(EP, 'raw', 'ecos_731Y001_20261013.json'), encoding='utf-8'))['USD']
pts = [(d, v) for d, v in u if '20251013' <= d <= '20261012']
idx = {d: i for i, (d, _) in enumerate(pts)}
V = dict(pts)
assert pts[0] == ('20251013', 1420.5) and pts[-1] == ('20261012', 1338.0)
assert max(v for _, v in pts) == 1554.4 and V['20260702'] == 1554.4
# 네 날짜(날짜 순) — calc_out 1절 원문과 대조
marks = [
 # 날짜, 이름(말 그대로), 환율 글자, 10/12 원화, %, 말 속 금액
 ('20251013', '작년 이맘때', '1,420.5원', 94192186, '−5.81%', '600만원쯤'),
 ('20260102', '올해 첫날',   '1,434.9원', 93246916, '−6.75%', '700만원 가까이'),
 ('20260702', '가장 높던 날', '1,554.4원', 86078230, '−13.92%', '1,400만원 가까이'),
 ('20260713', '석 달 전',    '1,507.1원', 88779776, '−11.22%', '1천만원 넘게'),
]
fill = [0, 1, 3, 2]   # 2장 말 순서: 작년·첫날·석 달 전·가장 높던 날
for d, name, rt, won, pct, say in marks:
    assert float(rt.replace(',', '').rstrip('원')) == V[d], d
    assert f'{won:,}원' in calc and pct.replace('−', '-') in calc, (d, won, pct)
    assert name in t3, name
for w in ['600만원쯤', '700만원 가까이', '1,400만원 가까이', '1천만원을 넘습니다', '네 날짜 모두 원화로는 줄었습니다', '10.12 1,338.0원 < 네 날짜 환율 전부',
          '결과가 제일 나쁜 날을 고른 셈', '같은 1억', '지금 값은 모두 10월 12일 기준']:
    assert w in src_all, w
mo = [[i, f"{d[:4]}.{int(d[4:6])}"] for i, (d, _) in enumerate(pts) if i > 0 and d[4:6] != pts[i - 1][0][4:6] and d[4:6] in ('01', '04', '07', '10')]
fx = {
 'seed': 'X-1-fx', 'vals': [v for _, v in pts], 'min': 1300, 'max': 1580,
 'yticks': [[1350, '1,350원'], [1450, '1,450원'], [1550, '1,550원']], 'months': [[0, '2025.10']] + mo,
 'now': 1338.0, 'nowText': '10.12 · 1,338.0원', 'nowAll': '10.12 1,338.0원 < 네 날짜 환율 전부',
 'marks': [{'i': idx[d], 'name': n, 'date': f"{d[:4]}.{int(d[4:6])}.{int(d[6:])}", 'rate': rt, 'won': w, 'pct': p, 'say': s} for d, n, rt, w, p, s in marks],
 'peak': 2, 'peakTag': '결과가 제일 나쁜 날을 고른 셈', 'markAt': [word_at(n) for _, n, *_ in marks],
 'fill': fill, 'base': 100000000, 'baseText': '같은 1억', 'allDown': '네 날짜 모두 원화로는 줄었습니다',
 'barHead': '그날 바꾼 1억 → 10.12 원화', 'legendDrop': '바꾼 날보다 내린 환율', 'legendGap': '줄어든 원화',
 'b1': B1, 'b2': B2,
}
src = '한국은행 ECOS 731Y001 원/달러 매매기준율 일별(2025.10.13~2026.10.12) · 환산 수수료 없음'
sc1 = {'key': 'why4', 'title': '왜 날짜가 네 개인가', 'sub': '환율 1년 · 바꾼 날 네 개', 'chapter': '1', 'source': src, 'lines': L1, 'frames': sum(l['frames'] for l in L1) + 12}
sc2 = {'key': 'cash', 'title': '달러로만 바꿔 뒀다면', 'sub': '같은 1억, 바꾼 날마다 지금 원화로', 'chapter': '2', 'source': src, 'lines': L2, 'frames': sum(l['frames'] for l in L2) + 12}
json.dump({'s1': sc1, 's2': sc2, 'fx': fx}, open(os.path.join(H, 'x1_fx.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ch1', [l['frames'] for l in L1], 'ch2', [l['frames'] for l in L2], 'pts', len(pts), 'markAt', fx['markAt'], 'voice' if voice else '어림(P-1 spf)')
