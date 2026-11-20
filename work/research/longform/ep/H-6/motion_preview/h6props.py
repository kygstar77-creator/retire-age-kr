# H-6 은마 84㎡ 실거래 점 줄(DealDots) props — calc_out.txt(국토부 실거래 원표 정리)에서 직접 읽고 calc2_out과 assert (2026-11-20 motion)
# 말 줄은 대본 전 가안(미리보기용). 대본 v1이 나오면 lines만 대본 줄·voice 길이로 바꾼다 — 숫자는 이 파일이 calc에서 만든다.
import re, json, os, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
txt = open(os.path.join(E, 'calc_out.txt'), encoding='utf-8').read()
sec = txt.split('## 전용 84㎡')[1].split('## ')[0]
deals = [{'d': f'{y}-{m}-{d}', 'v': float(v), 'fl': int(fl)} for y, m, d, v, fl in re.findall(r'(\d{4})\.(\d{2})\.(\d{2}) ([\d.]+)억 (\d+)층', sec)]
assert len(deals) == 26, len(deals)
c2 = open(os.path.join(E, 'calc2_out.txt'), encoding='utf-8').read()
def grp(a, b): return [x['v'] for x in deals if a <= x['d'][:7] <= b]
P = [('2025-10', '2025-12', '2025-10-01', '2025-12-31'), ('2026-01', '2026-06', '2026-01-01', '2026-06-30'), ('2026-07', '2026-09', '2026-07-01', '2026-09-30'), ('2026-10', '2026-11', '2026-10-01', '2026-11-15')]
steps = []
for a, b, da, db in P:
    v = statistics.median(grp(a, b)); steps.append({'a': da, 'b': db, 'v': round(v, 3), 'text': f'{v:.1f}억'})
    lab = f"84㎡ {a[:4]}.{a[5:]}~{b[5:]}: {len(grp(a, b))}건 가운데 {v:.2f}억"
    assert lab in c2, lab
peak = max(range(26), key=lambda i: deals[i]['v']); assert deals[peak] == {'d': '2025-10-31', 'v': 43.1, 'fl': 13}
last = [i for i, x in enumerate(deals) if x['d'] == '2026-10-31' and x['fl'] == 14][0]; assert deals[last]['v'] == 35.0
assert "최고 ('2025.10.31', 43.1, 13) · 마지막 ('2026.10.31', 35.0, 14)" in c2
gap = deals[peak]['v'] - deals[last]['v']; sg = steps[0]['v'] - steps[-1]['v']; pre = steps[0]['v'] - steps[1]['v']
assert abs(gap - 8.1) < 1e-9 and abs(sg - 8.5) < 1e-9, (gap, sg)
share = round(pre / sg * 100); assert share == 47, share
data = {'seed': 'h6', 'deals': deals, 'from': '2025-09-20', 'to': '2026-11-15', 'min': 31, 'max': 44.5, 'ticks': [32, 36, 40, 44], 'unit': '억',
  'months': [{'d': '2025-10-01', 'text': '2025.10'}, {'d': '2026-01-01', 'text': '2026.1'}, {'d': '2026-04-01', 'text': '4'}, {'d': '2026-07-01', 'text': '7'}, {'d': '2026-10-01', 'text': '10'}],
  'dropAt': 0.15, 'peak': {'i': peak, 'text': '최고가 43.1억 · 13층', 'at': 1.3},
  'last': {'i': last, 'text': '35.0억 · 14층', 'at': 2.1, 'gap': f'−{gap:.1f}억', 'gapAt': 2.55},
  'steps': steps, 'stepsAt': 3.35, 'stepGap': {'text': f'−{sg:.1f}억', 'at': 3.8},
  'mark': {'d': '2026-07-02', 'text': '사업시행인가 7/2', 'at': 4.1}, 'before': {'text': f'인가 전 −{pre:.1f}억 · 낙폭 {sg:.1f}억 중 {share}%', 'at': 4.55}}
lines = [  # 가안 — 대본 v1 나오면 교체
  ('은마아파트 전용 84㎡, 지난 1년 실거래 26건을 계약한 날 순서대로 찍어 봤습니다.', 190),
  ('작년 10월 31일, 13층이 43억 1천만원. 이 기간 가장 높은 값이었습니다.', 170),
  ('올해 10월 31일 14층은 35억원. 높은 층끼리 놓고 봐도 8억 1천만원 차이예요.', 200),
  ('한 건만 고른 게 아닐까 싶어 석 달씩 묶은 가운데 값도 봤습니다. 42억 8천에서 34억 3천, 8억 5천 내렸습니다.', 240),
  ('사업시행인가가 고시된 7월 2일에 선을 그어 보면, 내린 8억 5천 가운데 약 4억, 47%는 인가 전에 이미 내려 있었습니다.', 240)]
sc = {'key': 'deals', 'kind': 'deals', 'title': '은마 84㎡ 실거래 26건', 'sub': None, 'chapter': '2. 1년 실거래',
  'source': '국토교통부 실거래가 공개시스템 · 계약 2025.10~2026.11 · 해제 거래 뺌', 'data': data,
  'lines': [{'text': t, 'audio': None, 'frames': n} for t, n in lines]}
sc['frames'] = sum(l['frames'] for l in sc['lines'])
json.dump({'deals': sc}, open(os.path.join(H, 'h6_motion.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(deals), 'peak', deals[peak], 'last', deals[last], 'steps', [s['text'] for s in steps], 'gap', gap, 'sg', sg, 'pre', round(pre, 2), share)
