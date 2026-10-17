# X-1 FxDates props — 대본 v3(10/17) 질문 1 '1억을 달러로 바꾼 날을 네 개'(선) · '작년 이맘때 바꿨다면 …'(막대) (2026-10-16 motion, 10/17 PD v3·끝날 10/15로 고침)
# 선 = 한국은행 ECOS 원/달러 매매기준율 일별 원문(raw/collect_20261016.json) 2025.10.13~2026.10.15 그대로.
# 화면 글자 숫자는 calc_out·script(말·자막)에 있는 것만(assert). 막대 높이 = 그날 바꾼 1억의 10/15 원화 값(0부터).
# 길이: ep/X-1/voice.json(v3 녹음) 프레임. 장면 나눔은 x1props와 같다 — 선 = '1억을 달러로 바꾼 날을'~'날짜를 하나만 쓰면'(3줄),
#   막대 = '작년 이맘때 바꿨다면'~'네 날짜 모두 줄었어요'(3줄, 앞줄 '먼저 달러로 바꿔서'는 실사 장면).
#   py -3.12 work/research/longform/ep/X-1/motion_preview/fxprops.py  → x1_fx.json
# 옛 v2(끝날 10/12·1,338.0원) = fxprops.v2.py.bak
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md'); txt = open(script, encoding='utf-8').read()
calc = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
src_all = txt + calc
secs = SC.parse(script)
caps, last = {}, None
for line in txt.splitlines():
    s = line.strip()
    if s.startswith('- '): last = s[2:].strip()
    elif s.startswith('[자막:') and last and last not in caps: caps[last] = s[4:].rstrip(']').strip()
voice = {}
for s in json.load(open(os.path.join(EP, 'voice.json'), encoding='utf-8')).get('sections', []):
    for l in s['lines']:
        if l.get('audio'): voice[l['text']] = l
def cut(sec, a, b):
    s = next(x for x in secs if x['title'].startswith(sec))['lines']
    i = next(k for k, t in enumerate(s) if t.startswith(a)); j = next(k for k, t in enumerate(s) if t.startswith(b))
    out = []
    for t in s[i:j + 1]:
        v = voice[t]; out.append({'text': t, 'cap': caps.get(t), 'frames': v['frames'], 'audio': v['audio']})
    st, a = [], 0
    for l in out: st.append(a); a += l['frames']
    return out, st
L1, S1 = cut('1.', '1억을 달러로 바꾼 날을', '날짜를 하나만 쓰면')
L2, S2 = cut('1.', '작년 이맘때 바꿨다면', '네 날짜 모두 줄었어요')
assert len(L1) == 3 and len(L2) == 3, ([l['text'] for l in L1], [l['text'] for l in L2])
# 둘째 줄 안 이름 네 개 시점 = 음절 비례
t2 = L1[1]['text']; sp2 = SC.speak(t2); n2 = SC.syl(sp2)
def word_at(w):
    k = sp2.index(SC.speak(w)); return S1[1] + round(L1[1]['frames'] * SC.syl(sp2[:k]) / n2)

# 원문 선(끝날 10/15)
raw = json.load(open(os.path.join(EP, 'raw', 'collect_20261016.json'), encoding='utf-8'))
pts = [(d, v) for d, v in raw['USD'] if '20251013' <= d <= '20261015']
idx = {d: i for i, (d, _) in enumerate(pts)}
V = dict(pts)
assert pts[0] == ('20251013', 1420.5) and pts[-1] == ('20261015', 1338.6), (pts[0], pts[-1])
assert max(v for _, v in pts) == 1554.4 and V['20260702'] == 1554.4
# 네 날짜(날짜 순) — calc_out 1절 원문과 대조. say = 막대가 내려앉을 때 위에 뜨는 말(말에 나온 금액만, 안 나온 날은 '줄어듦')
marks = [
 ('20251013', '작년 이맘때', '1,420.5원', 94234424, '−5.77%', '580만원쯤'),
 ('20260102', '올해 첫날',   '1,434.9원', 93288731, '−6.71%', '줄어듦'),
 ('20260702', '가장 비싸던 날', '1,554.4원', 86116830, '−13.88%', '1,400만원 가까이'),
 ('20260713', '석 달 전',    '1,507.1원', 88819587, '−11.18%', '줄어듦'),
]
fill = [0, 2, 1, 3]   # 말 순서: 작년(첫 줄) → 가장 비싸던 날(둘째 줄) → 나머지 둘(둘째 줄 뒤쪽)
for d, name, rt, won, pct, say in marks:
    assert float(rt.replace(',', '').rstrip('원')) == V[d], d
    assert f'{won:,}원' in calc and pct.replace('−', '-') in calc, (d, won, pct)
    assert name in t2, name
for w in ['580만원쯤', '1,400만원 가까이', '네 날짜 모두 줄었어요', '하필 제일 나쁜 날', '1,338.6원', '같은 1억']:
    assert w in src_all, w
mo = [[i, f"{d[:4]}.{int(d[4:6])}"] for i, (d, _) in enumerate(pts) if i > 0 and d[4:6] != pts[i - 1][0][4:6] and d[4:6] in ('01', '04', '07', '10')]
# 박자: B1 = [선 시작, 셋째 줄(제일 나쁜 날) 시작, 그 3초 뒤] — 선은 첫 두 줄 동안 그려지고, 빨간 폭·지금 선은 '하필 제일 나쁜 날' 줄에.
# B2(막대 7박자) = [0, 첫 막대(작년), 둘째 줄(가장 비싸던 날), 둘째 줄 55%(올해 첫날), 둘째 줄 80%(석 달 전), 셋째 줄 시작(네 날짜 모두), 셋째 줄 '. ' 뒤(지금 환율이 다 낮다)]
end1 = S1[2] + L1[2]['frames']
B1 = [S1[0], S1[2], S1[2] + min(90, L1[2]['frames'])]   # 셋째 박자: '하필 제일 나쁜 날' 띠가 3초 뒤 사라짐(끝까지 두면 '석 달 전' 이름을 덮음 — 10/17 스틸)
t3 = L2[2]['text']; q3 = SC.syl(SC.speak(t3[:t3.index('. ') + 1])) / SC.syl(SC.speak(t3))
B2 = [0, 20, S2[1], S2[1] + round(L2[1]['frames'] * 0.55), S2[1] + round(L2[1]['frames'] * 0.8), S2[2], S2[2] + round(L2[2]['frames'] * q3)]
assert B2 == sorted(B2), B2
fx = {
 'seed': 'X-1-fx', 'vals': [v for _, v in pts], 'min': 1300, 'max': 1580,
 'yticks': [[1350, '1,350원'], [1450, '1,450원'], [1550, '1,550원']], 'months': [[0, '2025.10']] + mo,
 'now': 1338.6, 'nowText': '10.15 · 1,338.6원', 'nowAll': '지금 1,338.6원 < 네 날 환율 전부',
 'marks': [{'i': idx[d], 'name': n, 'date': f"{d[:4]}.{int(d[4:6])}.{int(d[6:])}", 'rate': rt, 'won': w, 'pct': p, 'say': s} for d, n, rt, w, p, s in marks],
 'peak': 2, 'peakTag': '하필 제일 나쁜 날', 'markAt': [word_at(n) for _, n, *_ in marks],
 'fill': fill, 'base': 100000000, 'baseText': '같은 1억', 'allDown': '네 날짜 모두 줄었어요',
 'barHead': '그날 바꾼 1억 → 10.15 원화', 'legendDrop': '바꾼 날보다 내린 환율', 'legendGap': '줄어든 원화',
 'b1': B1, 'b2': B2,
}
src = '한국은행 ECOS 원/달러 매매기준율 일별(2025.10.13~2026.10.15) · 환산 수수료 없음'
sc1 = {'key': 'why4', 'title': '바꾼 날 네 개', 'sub': None, 'chapter': '질문 ①', 'source': src, 'lines': L1, 'frames': end1}
sc2 = {'key': 'cash', 'title': '달러로만 들고 있었다면', 'sub': None, 'chapter': '질문 ①', 'source': src, 'lines': L2, 'frames': S2[2] + L2[2]['frames']}
json.dump({'s1': sc1, 's2': sc2, 'fx': fx}, open(os.path.join(H, 'x1_fx.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('선', [l['frames'] for l in L1], 'B1', B1, '· 막대', [l['frames'] for l in L2], 'B2', B2, '· 점', len(pts), 'markAt', fx['markAt'])
