# JT-1 움직이는 판 props (2026-11-16 motion) — shot_plan '3 같아지는 나이' 줄 '받은 돈 합 두 선이 그려지며 93세에서 만남'(SumRace)
#   race = 3장 '그럼 못 받은 7,600만원을' ~ '그러니 93세보다 오래 사시면' 9줄 (visual 판 jt1_cross93·jt1_mid3 자리를 한 장면으로 — PD가 고름)
# 숫자: 월지급금 5억 65세 1,264천·70세 1,539천(calc §1) · 화면 글자 7,584만원·23년·93세·4,284·2,634·984만원은 calc §1·§7 줄과 assert. 새 숫자 없음.
#   py -3.12 work/research/longform/ep/JT-1/motion_preview/jt1props.py → jt1_motion.json (voice.json 생기면 그 길이로 다시)
import json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(H); WORK = os.path.abspath(os.path.join(EP, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WORK, 'research', 'longform', 'loop'))
import speechcompare_script as SC
script = os.path.join(EP, 'script.md')
CALC = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read()
secs = SC.parse(script)
voice = {}
vj = os.path.join(EP, 'voice.json')
if os.path.exists(vj):
    for s in json.load(open(vj, encoding='utf-8')).get('sections', []):
        for l in s['lines']:
            if l.get('audio'): voice[l['text']] = l
SPF = json.load(open(os.path.join(EP, '..', 'P-1', 'motion_preview', 'p1_timing.json'), encoding='utf-8'))['spf']
def cut(sec, a, b):
    s = next(x for x in secs if x['title'].lstrip('[').lstrip('#').strip().startswith(sec))['lines']
    i = next(k for k, t in enumerate(s) if t.startswith(a)); j = next(k for k, t in enumerate(s) if t.startswith(b))
    return [{'text': t, 'frames': voice[t]['frames'] if t in voice else max(12, round(SC.syl(SC.speak(t)) / SPF)), 'audio': voice[t]['audio'] if t in voice else None} for t in s[i:j + 1]]
lines = cut('3.', '그럼 못 받은', '그러니 93세보다')
T = [l['text'] for l in lines]; print(len(T), 'lines'); [print(' ', i, t) for i, t in enumerate(T)]
idx = lambda w: next(i for i, t in enumerate(T) if w in t)

m = re.search(r'5억 65세 ([\d,]+)천 vs 70세 ([\d,]+)천: 기다린 5년 못 받은 돈 ([\d,]+)만원 · 매달 \+([\d,]+)천 → ([\d.]+)년 뒤 = ([\d.]+)세', CALC)
mA, mB, miss, d, yrs, meet = [float(x.replace(',', '')) for x in m.groups()]
assert (mA, mB) == (1264, 1539) and miss == mA * 60 / 10 and d == mB - mA
a = {'name': '65세에 든 쪽', 'start': 65, 'monthly': mA / 10}; b = {'name': '70세에 든 쪽', 'start': 70, 'monthly': mB / 10}
cross = (b['monthly'] * 70 - a['monthly'] * 65) / (b['monthly'] - a['monthly'])
assert abs(cross - meet) < 0.05 and abs((cross - 70) - yrs) < 0.05, (cross, meet)
S = lambda s, age: max(0, age - s['start']) * 12 * s['monthly']
slices = []
for age, word in ((80, '80세가 됐을'), (85, '85세에는'), (90, '90세에도')):
    m7 = re.search(rf'{age}세까지: 65세 시작 ([\d,]+) · 70세 시작 ([\d,]+) · 차 ([\d,]+)', CALC)
    e, l, df = [int(x.replace(',', '')) for x in m7.groups()]
    assert round(S(a, age)) == e and round(S(b, age)) == l and e - l == df, age
    k = idx(word)   # 80은 '80세가 됐을 때' 줄에서 면·점(값 4,284는 다음 줄 말보다 2초쯤 먼저)
    slices.append({'age': age, 'text': f'{df:,}만원 더', 'at': k + 0.35})
assert '7,600만원' in T[0] and '23년' in T[idx('23년')] and '93세' in T[idx('그러면 93세')]
g0 = idx('중간을 끊어'); R, G = lines[:g0], lines[g0:]
for sl in slices: sl['at'] -= g0
common = {'from': 65, 'to': 95, 'a': a, 'b': b, 'yRace': [0, 50000], 'yGap': [-2500, 9500], 'ticks': [{'v': 20000, 'text': '2억'}, {'v': 40000, 'text': '4억'}]}
race = dict(common, seed='JT-1-race', ageTicks=[65, 70, 80, 90], lam={'from': 0, 'to': 0, 'at': 0}, sweep=[0.15, idx('23년') + 0.6],
            missed={'text': f'70세까지 기다린 5년, 못 받은 {int(miss):,}만원', 'at': 0.45}, years={'text': f'{round(yrs)}년', 'at': idx('23년') + 0.1},
            meet={'text': f'{round(meet)}세', 'at': idx('그러면 93세') + 0.05}, slices=[], after=None)
gap = dict(common, seed='JT-1-race', ageTicks=[65, 70, 80, 85, 90], lam={'from': 0, 'to': 1, 'at': 0.15}, sweep=None,
           missed={'text': f'{int(miss):,}만원', 'at': -1}, years=None, meet={'text': f'{round(meet)}세', 'at': -1},
           slices=[dict(s, text=s['text'].replace(' 더', '')) for s in slices], b=dict(b, name='0선 = 70세에 든 쪽'), after={'text': '93세 뒤로는 70세 쪽이 더 →', 'at': idx('그러니 93세보다') - g0 + 0.45})
SRC = '주택금융공사 월지급금 표(2026.3.1) · 5억 집 · 월지급금 × 받은 달 수'
def sc(key, title, ls, data): return {'key': key, 'title': title, 'sub': '집값이 그대로라는 가정', 'chapter': '3', 'source': SRC, 'lines': ls, 'frames': sum(l['frames'] for l in ls) + 12, 'data': data}
out = {'race': sc('race', '받은 돈 합 · 65세 vs 70세', R, race), 'gap': sc('gap', '65세에 든 쪽이 더 받은 돈', G, gap)}
json.dump(out, open(os.path.join(H, 'jt1_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('frames', out['race']['frames'], out['gap']['frames'], 'voice' if voice else '(어림 길이)')
