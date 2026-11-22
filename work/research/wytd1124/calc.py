# wytd1124: 2025년 마지막 거래일 종가 → 최신 종가, 현지 통화·원화 기준 수익률
import json, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
def load(n):
    d = json.load(open(os.path.join(HERE, 'raw', n + '.json'), encoding='utf-8'))['chart']['result'][0]
    ts = d['timestamp']; c = d['indicators']['quote'][0]['close']; tz = d['meta']['gmtoffset']
    out = [((datetime.datetime(1970,1,1) + datetime.timedelta(seconds=t + tz)).date(), v) for t, v in zip(ts, c) if v is not None]
    return out, d['meta']
def base_last(s, end=datetime.date(2026, 11, 20)):
    s = [x for x in s if x[0] <= end]
    b = [x for x in s if x[0] <= datetime.date(2025, 12, 31)][-1]
    return b, s[-1]
fx = {}
for n in ['KRW_X', 'JPYKRW_X', 'EURKRW_X']:
    s, m = load(n); b, l = base_last(s); fx[n] = (b, l)
    print(f'{n}: {b[0]} {b[1]:.2f} → {l[0]} {l[1]:.2f}  변화 {l[1]/b[1]-1:+.2%}')
cur = {'GSPC': 'KRW_X', 'NDX': 'KRW_X', 'SP500TR': 'KRW_X', 'N225': 'JPYKRW_X', 'STOXX50E': 'EURKRW_X', 'KS11': None}
for n, f in cur.items():
    s, m = load(n); b, l = base_last(s); loc = l[1] / b[1] - 1
    hi = max(s, key=lambda x: x[1] if x[0] > datetime.date(2025, 12, 31) else -1)
    line = f'{n}: {b[0]} {b[1]:,.2f} → {l[0]} {l[1]:,.2f}  현지 {loc:+.2%}  올해 최고 {hi[0]} {hi[1]:,.2f} (최고 대비 {l[1]/hi[1]-1:+.2%})'
    if f:
        fb, fl = fx[f]; krw = (1 + loc) * (fl[1] / fb[1]) - 1
        line += f'  원화 {krw:+.2%}'
    print(line)

# 한국은행 ECOS 731Y001 매매기준율(1차) — 환율은 모두 2025-12-31 매매기준율 기준(닛케이·유로스톡스·코스피 마지막 거래일 12-30이어도 연말 환율로 통일 — 본문·그림과 같게)
ECOS = {'USD': {'2025-12-30': 1433.9, '2025-12-31': 1434.9, '2026-11-20': 1330.8},
        'JPY100': {'2025-12-30': 919.08, '2025-12-31': 917.63, '2026-11-20': 833.73},
        'EUR': {'2025-12-30': 1688.35, '2025-12-31': 1685.72, '2026-11-20': 1459.62}}
print('\n[원화 환산 — 한국은행 매매기준율]')
for c, v in ECOS.items():
    print(f'{c}: 12/31 {v["2025-12-31"]} → 11/20 {v["2026-11-20"]}  {v["2026-11-20"]/v["2025-12-31"]-1:+.2%}')
cur2 = {'GSPC': 'USD', 'NDX': 'USD', 'SP500TR': 'USD', 'N225': 'JPY100', 'STOXX50E': 'EUR', 'KS11': None}
for n, c in cur2.items():
    s, m = load(n); b, l = base_last(s); loc = l[1] / b[1] - 1
    if c:
        r = ECOS[c]; krw = (1 + loc) * r['2026-11-20'] / r['2025-12-31'] - 1
        print(f'{n}: 현지 {loc:+.2%}  원화 {krw:+.2%}  (환율 2025-12-31 {r['2025-12-31']} → 11/20 {r["2026-11-20"]})')
    else:
        print(f'{n}: 원화 {loc:+.2%}')
# 1,000만원 넣었으면(원화 기준, 수수료·세금·환전 비용 빼고)
