"""E-2 테슬라 분기표 (2026-10-01). SEC XBRL companyfacts, 분기 3개월값 + 4분기=연간-3개 분기(calc 표시).
출력 quarters.json — 화면·대본 숫자는 이 파일에서만."""
import json, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(os.path.join(H, 'raw', 'tsla_facts.json'), encoding='utf-8'))['facts']['us-gaap']
d = datetime.date.fromisoformat
def series(tag):
    q, fy = {}, {}
    for x in f[tag]['units']['USD']:
        if 'start' not in x: continue
        n = (d(x['end']) - d(x['start'])).days
        if 80 <= n <= 100: q[x['end']] = x['val']
        elif 350 <= n <= 380: fy[x['end']] = (x['start'], x['val'])
    out = {k: {'v': v, 'calc': False} for k, v in q.items()}
    for end, (start, val) in fy.items():
        if end in out: continue
        three = [v for k, v in q.items() if start < k < end]
        if len(three) == 3: out[end] = {'v': val - sum(three), 'calc': True}
    return dict(sorted(out.items()))
T = {'매출': 'Revenues', '매출총이익': 'GrossProfit', '영업이익': 'OperatingIncomeLoss', '순이익': 'NetIncomeLoss', '연구개발비': 'ResearchAndDevelopmentExpense'}
out = {k: series(v) for k, v in T.items()}
ends = sorted(out['매출'])[-10:]
print('분기말      ' + ' '.join(f'{k:>8}' for k in T) + '  영업이익률')
for e in ends:
    row = [out[k].get(e, {}).get('v') for k in T]
    mark = '*' if out['매출'][e]['calc'] else ' '
    print(e + mark, ' '.join(f'{(v or 0)/1e6:8,.0f}' for v in row), f"{row[2]/row[0]*100:6.1f}%")
json.dump({'source': 'SEC XBRL companyfacts CIK0001318605, 받은 날 2026-10-01', 'unit': 'USD', 'q': {k: {e: out[k].get(e) for e in ends} for k in T}}, open(os.path.join(H, 'quarters.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
