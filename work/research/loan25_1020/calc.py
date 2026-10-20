# loan25_1020 — 서울 84㎡대(전용 80~86㎡) 매매 최근 계약 가격 구간 비율. raw/ 11xxx_2026MM.json (2026-10-20 새로 받음)
import sys, os, json, glob, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
num = lambda s: float(str(s).replace(',', '') or 0)
out = []
tot = dict(n=0, a=0, b=0, c=0, all=0)
for code, name in sgg.items():
    if not code.startswith('11'): continue
    rows = []
    for f in sorted(glob.glob(os.path.join(H, 'raw', f'{code}_2026*.json'))):
        rows += json.load(open(f, encoding='utf-8'))
    allrows = [r for r in rows if not r.get('cdealType')]
    r84 = [r for r in allrows if 80 <= num(r['excluUseAr']) < 86]
    p = sorted(num(r['dealAmount']) / 10000 for r in r84)   # 억
    n = len(p)
    over25 = sum(1 for x in p if x > 25); mid = sum(1 for x in p if 15 < x <= 25); low = sum(1 for x in p if x <= 15)
    med = st.median(p) if p else None
    out.append(dict(code=code, name=name, all=len(allrows), n=n, over25=over25, mid=mid, low=low, med=med, mx=max(p) if p else None))
    tot['n'] += n; tot['a'] += over25; tot['b'] += mid; tot['c'] += low; tot['all'] += len(allrows)
print('서울 25개 구 2026-07~10 계약(해제 뺌) 아파트 매매', tot['all'], '건 · 84㎡대', tot['n'], '건')
print('전체 84㎡대: 25억 초과', tot['a'], f"{tot['a']/tot['n']*100:.1f}%", '· 15억 초과~25억', tot['b'], f"{tot['b']/tot['n']*100:.1f}%", '· 15억 이하', tot['c'], f"{tot['c']/tot['n']*100:.1f}%")
print('구 | 84㎡대 건수 | 25억 초과 % | 15~25억 % | 15억 이하 % | 가운데 가격(억) | 최고')
for o in sorted(out, key=lambda o: -(o['over25'] / o['n'] if o['n'] else 0)):
    if not o['n']: print(o['name'], 0); continue
    print(f"{o['name']} | {o['n']} | {o['over25']} ({o['over25']/o['n']*100:.0f}%) | {o['mid']} ({o['mid']/o['n']*100:.0f}%) | {o['low']} ({o['low']/o['n']*100:.0f}%) | {o['med']:.2f} | {o['mx']:.2f}")
json.dump(dict(total=tot, gu=out), open(os.path.join(H, 'calc_out.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
